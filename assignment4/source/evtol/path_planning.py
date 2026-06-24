from __future__ import annotations

import heapq
import math
import time
from dataclasses import dataclass

import numpy as np

from .path_analysis import analyze_path, sample_field


@dataclass(frozen=True)
class AStarConfig:
    grid_resolution: int
    heuristic: str
    obstacle_threshold: float
    obstacle_inflation: int
    alpha_distance: float
    beta_risk: float
    gamma_cost: float
    max_snap_radius: int = 8


@dataclass(frozen=True)
class RRTStarConfig:
    max_iterations: int
    step_size: float
    neighbor_radius: float
    goal_bias: float
    obstacle_threshold: float
    safety_buffer: float
    alpha_distance: float
    beta_risk: float
    gamma_cost: float
    seed: int


@dataclass
class PlannerResult:
    algorithm: str
    success: bool
    path: list[tuple[float, float]]
    explored: list[tuple[float, float]]
    frontier: list[tuple[float, float]]
    tree_edges: list[tuple[tuple[float, float], tuple[float, float]]]
    samples: list[tuple[float, float]]
    rewired_edges: list[tuple[tuple[float, float], tuple[float, float]]]
    metrics: dict


def make_obstacle_mask(risk_field: np.ndarray, threshold: float, inflation: int = 0) -> np.ndarray:
    mask = risk_field >= threshold
    if inflation <= 0:
        return mask
    inflated = mask.copy()
    obstacle_idx = np.argwhere(mask)
    rows, cols = mask.shape
    for r, c in obstacle_idx:
        r0 = max(0, r - inflation)
        r1 = min(rows, r + inflation + 1)
        c0 = max(0, c - inflation)
        c1 = min(cols, c + inflation + 1)
        inflated[r0:r1, c0:c1] = True
    return inflated


def _point_to_grid(point: tuple[float, float], n: int) -> tuple[int, int]:
    col = int(round(np.clip(point[0], 0.0, 100.0) / 100.0 * (n - 1)))
    row = int(round(np.clip(point[1], 0.0, 100.0) / 100.0 * (n - 1)))
    return row, col


def _grid_to_point(cell: tuple[int, int], n: int) -> tuple[float, float]:
    row, col = cell
    return col / max(n - 1, 1) * 100.0, row / max(n - 1, 1) * 100.0


def _snap_free(cell: tuple[int, int], obstacle: np.ndarray, max_radius: int) -> tuple[int, int] | None:
    rows, cols = obstacle.shape
    r, c = cell
    if 0 <= r < rows and 0 <= c < cols and not obstacle[r, c]:
        return cell
    for radius in range(1, max_radius + 1):
        candidates = []
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < rows and 0 <= cc < cols and not obstacle[rr, cc]:
                    candidates.append((rr, cc))
        if candidates:
            return min(candidates, key=lambda item: (item[0] - r) ** 2 + (item[1] - c) ** 2)
    return None


def _resample_field(field: np.ndarray, n: int) -> np.ndarray:
    rows = np.linspace(0, field.shape[0] - 1, n).round().astype(int)
    cols = np.linspace(0, field.shape[1] - 1, n).round().astype(int)
    return field[np.ix_(rows, cols)]


def _heuristic(a: tuple[int, int], b: tuple[int, int], mode: str) -> float:
    dr = abs(a[0] - b[0])
    dc = abs(a[1] - b[1])
    if mode == "曼哈顿距离":
        return float(dr + dc)
    return float(math.hypot(dr, dc))


def _reconstruct(came_from: dict, current: tuple[int, int], n: int) -> list[tuple[float, float]]:
    cells = [current]
    while current in came_from:
        current = came_from[current]
        cells.append(current)
    cells.reverse()
    return [_grid_to_point(cell, n) for cell in cells]


def run_astar(
    start: tuple[float, float],
    goal: tuple[float, float],
    risk_field: np.ndarray,
    cost_field: np.ndarray,
    config: AStarConfig,
) -> PlannerResult:
    t0 = time.perf_counter()
    n = int(config.grid_resolution)
    risk = _resample_field(risk_field, n)
    cost = _resample_field(cost_field, n)
    obstacle = make_obstacle_mask(risk, config.obstacle_threshold, config.obstacle_inflation)

    start_cell = _snap_free(_point_to_grid(start, n), obstacle, config.max_snap_radius)
    goal_cell = _snap_free(_point_to_grid(goal, n), obstacle, config.max_snap_radius)
    if start_cell is None or goal_cell is None:
        metrics = analyze_path("A*", [], risk, cost, obstacle, time.perf_counter() - t0, 0, False)
        return PlannerResult("A*", False, [], [], [], [], [], [], metrics)

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    open_heap = [(0.0, start_cell)]
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g_score = {start_cell: 0.0}
    open_set = {start_cell}
    closed_set: set[tuple[int, int]] = set()
    explored_trace: list[tuple[float, float]] = []
    frontier_trace: list[tuple[float, float]] = []

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current not in open_set:
            continue
        open_set.remove(current)
        closed_set.add(current)
        explored_trace.append(_grid_to_point(current, n))

        if current == goal_cell:
            path = _reconstruct(came_from, current, n)
            metrics = analyze_path(
                "A*",
                path,
                risk,
                cost,
                obstacle,
                time.perf_counter() - t0,
                len(closed_set),
                True,
            )
            return PlannerResult(
                "A*",
                True,
                path,
                explored_trace,
                frontier_trace,
                [],
                [],
                [],
                metrics,
            )

        for dr, dc in moves:
            neighbor = (current[0] + dr, current[1] + dc)
            nr, nc = neighbor
            if nr < 0 or nr >= n or nc < 0 or nc >= n or obstacle[nr, nc]:
                continue
            if neighbor in closed_set:
                continue

            distance_cost = math.hypot(dr, dc)
            step_cost = (
                config.alpha_distance * distance_cost
                + config.beta_risk * float(risk[nr, nc])
                + config.gamma_cost * float(cost[nr, nc])
            )
            tentative_g = g_score[current] + step_cost
            if tentative_g < g_score.get(neighbor, np.inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + _heuristic(neighbor, goal_cell, config.heuristic)
                heapq.heappush(open_heap, (f_score, neighbor))
                open_set.add(neighbor)
                frontier_trace.append(_grid_to_point(neighbor, n))

    metrics = analyze_path("A*", [], risk, cost, obstacle, time.perf_counter() - t0, len(closed_set), False)
    return PlannerResult("A*", False, [], explored_trace, frontier_trace, [], [], [], metrics)


def _segment_samples(a: np.ndarray, b: np.ndarray, spacing: float = 1.0) -> np.ndarray:
    length = float(np.linalg.norm(b - a))
    count = max(2, int(math.ceil(length / spacing)) + 1)
    ts = np.linspace(0.0, 1.0, count)
    return a[None, :] * (1.0 - ts[:, None]) + b[None, :] * ts[:, None]


def _collision_free(
    a: np.ndarray,
    b: np.ndarray,
    risk_field: np.ndarray,
    obstacle_threshold: float,
    safety_buffer: float,
) -> bool:
    for x, y in _segment_samples(a, b, spacing=max(0.6, safety_buffer / 2.0)):
        if x < 0.0 or x > 100.0 or y < 0.0 or y > 100.0:
            return False
        if sample_field(risk_field, (float(x), float(y))) >= obstacle_threshold:
            return False
    return True


def _edge_cost(
    a: np.ndarray,
    b: np.ndarray,
    risk_field: np.ndarray,
    cost_field: np.ndarray,
    alpha: float,
    beta: float,
    gamma: float,
) -> float:
    samples = _segment_samples(a, b, spacing=1.2)
    length = float(np.linalg.norm(b - a))
    risks = np.array([sample_field(risk_field, (float(x), float(y))) for x, y in samples])
    costs = np.array([sample_field(cost_field, (float(x), float(y))) for x, y in samples])
    return alpha * length + beta * float(np.mean(risks)) * length + gamma * float(np.mean(costs)) * length


def _nearest(nodes: list[np.ndarray], sample: np.ndarray) -> int:
    dists = [float(np.linalg.norm(node - sample)) for node in nodes]
    return int(np.argmin(dists))


def _extract_rrt_path(nodes: list[np.ndarray], parents: list[int], goal_idx: int) -> list[tuple[float, float]]:
    path = []
    idx = goal_idx
    while idx != -1:
        path.append((float(nodes[idx][0]), float(nodes[idx][1])))
        idx = parents[idx]
    path.reverse()
    return path


def smooth_path(
    path: list[tuple[float, float]],
    risk_field: np.ndarray,
    obstacle_threshold: float,
    attempts: int = 80,
) -> list[tuple[float, float]]:
    if len(path) <= 2:
        return path
    rng = np.random.default_rng(1234)
    smoothed = [np.asarray(p, dtype=float) for p in path]
    for _ in range(attempts):
        if len(smoothed) <= 2:
            break
        i, j = sorted(rng.choice(len(smoothed), size=2, replace=False))
        if j <= i + 1:
            continue
        if _collision_free(smoothed[i], smoothed[j], risk_field, obstacle_threshold, 1.0):
            smoothed = smoothed[: i + 1] + smoothed[j:]
    return [(float(p[0]), float(p[1])) for p in smoothed]


def run_rrtstar(
    start: tuple[float, float],
    goal: tuple[float, float],
    risk_field: np.ndarray,
    cost_field: np.ndarray,
    config: RRTStarConfig,
    enable_smoothing: bool = True,
) -> PlannerResult:
    t0 = time.perf_counter()
    rng = np.random.default_rng(config.seed + 40_000)
    start_arr = np.asarray(start, dtype=float)
    goal_arr = np.asarray(goal, dtype=float)

    nodes = [start_arr]
    parents = [-1]
    costs = [0.0]
    edges: list[tuple[tuple[float, float], tuple[float, float]]] = []
    rewired: list[tuple[tuple[float, float], tuple[float, float]]] = []
    samples_trace: list[tuple[float, float]] = []
    best_goal_idx: int | None = None

    for _ in range(max(1, int(config.max_iterations))):
        if rng.random() < config.goal_bias:
            sample = goal_arr
        else:
            sample = rng.uniform(0.0, 100.0, size=2)
        samples_trace.append((float(sample[0]), float(sample[1])))

        nearest_idx = _nearest(nodes, sample)
        nearest = nodes[nearest_idx]
        direction = sample - nearest
        norm = float(np.linalg.norm(direction))
        if norm < 1e-9:
            continue
        new_node = nearest + direction / norm * min(config.step_size, norm)

        if not _collision_free(nearest, new_node, risk_field, config.obstacle_threshold, config.safety_buffer):
            continue

        neighbor_indices = [
            i for i, node in enumerate(nodes) if np.linalg.norm(node - new_node) <= config.neighbor_radius
        ]
        best_parent = nearest_idx
        best_cost = costs[nearest_idx] + _edge_cost(
            nearest,
            new_node,
            risk_field,
            cost_field,
            config.alpha_distance,
            config.beta_risk,
            config.gamma_cost,
        )

        for idx in neighbor_indices:
            if _collision_free(nodes[idx], new_node, risk_field, config.obstacle_threshold, config.safety_buffer):
                candidate_cost = costs[idx] + _edge_cost(
                    nodes[idx],
                    new_node,
                    risk_field,
                    cost_field,
                    config.alpha_distance,
                    config.beta_risk,
                    config.gamma_cost,
                )
                if candidate_cost < best_cost:
                    best_parent = idx
                    best_cost = candidate_cost

        nodes.append(new_node)
        parents.append(best_parent)
        costs.append(best_cost)
        new_idx = len(nodes) - 1
        edges.append(
            (
                (float(nodes[best_parent][0]), float(nodes[best_parent][1])),
                (float(new_node[0]), float(new_node[1])),
            )
        )

        for idx in neighbor_indices:
            if idx == best_parent:
                continue
            reconnect_cost = best_cost + _edge_cost(
                new_node,
                nodes[idx],
                risk_field,
                cost_field,
                config.alpha_distance,
                config.beta_risk,
                config.gamma_cost,
            )
            if reconnect_cost < costs[idx] and _collision_free(
                new_node,
                nodes[idx],
                risk_field,
                config.obstacle_threshold,
                config.safety_buffer,
            ):
                parents[idx] = new_idx
                costs[idx] = reconnect_cost
                rewired.append(
                    (
                        (float(new_node[0]), float(new_node[1])),
                        (float(nodes[idx][0]), float(nodes[idx][1])),
                    )
                )

        if np.linalg.norm(new_node - goal_arr) <= config.step_size and _collision_free(
            new_node,
            goal_arr,
            risk_field,
            config.obstacle_threshold,
            config.safety_buffer,
        ):
            goal_cost = best_cost + _edge_cost(
                new_node,
                goal_arr,
                risk_field,
                cost_field,
                config.alpha_distance,
                config.beta_risk,
                config.gamma_cost,
            )
            if best_goal_idx is None or goal_cost < costs[best_goal_idx]:
                nodes.append(goal_arr)
                parents.append(new_idx)
                costs.append(goal_cost)
                best_goal_idx = len(nodes) - 1
                edges.append(
                    (
                        (float(new_node[0]), float(new_node[1])),
                        (float(goal_arr[0]), float(goal_arr[1])),
                    )
                )

    success = best_goal_idx is not None
    path = _extract_rrt_path(nodes, parents, best_goal_idx) if success else []
    if enable_smoothing and success:
        path = smooth_path(path, risk_field, config.obstacle_threshold)

    obstacle = make_obstacle_mask(risk_field, config.obstacle_threshold, 0)
    metrics = analyze_path(
        "RRT*",
        path,
        risk_field,
        cost_field,
        obstacle,
        time.perf_counter() - t0,
        len(nodes),
        success,
    )
    return PlannerResult(
        "RRT*",
        success,
        path,
        [(float(n[0]), float(n[1])) for n in nodes],
        [],
        edges,
        samples_trace,
        rewired,
        metrics,
    )

