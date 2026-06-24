from __future__ import annotations

import numpy as np
import pandas as pd


def sample_field(field: np.ndarray, point: tuple[float, float]) -> float:
    """Sample a normalized grid field at a continuous point in [0, 100] x [0, 100]."""

    nrows, ncols = field.shape
    x = np.clip(point[0], 0.0, 100.0)
    y = np.clip(point[1], 0.0, 100.0)
    col = int(round(x / 100.0 * (ncols - 1)))
    row = int(round(y / 100.0 * (nrows - 1)))
    return float(field[row, col])


def path_length(path: list[tuple[float, float]]) -> float:
    if len(path) < 2:
        return 0.0
    arr = np.asarray(path, dtype=float)
    return float(np.sum(np.linalg.norm(np.diff(arr, axis=0), axis=1)))


def cumulative_field(path: list[tuple[float, float]], field: np.ndarray) -> tuple[float, float]:
    if not path:
        return 0.0, 0.0
    values = [sample_field(field, pt) for pt in path]
    return float(np.sum(values)), float(np.mean(values))


def turn_count(path: list[tuple[float, float]], angle_threshold_deg: float = 25.0) -> int:
    if len(path) < 3:
        return 0
    pts = np.asarray(path, dtype=float)
    turns = 0
    threshold = np.deg2rad(angle_threshold_deg)
    for i in range(1, len(pts) - 1):
        v1 = pts[i] - pts[i - 1]
        v2 = pts[i + 1] - pts[i]
        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)
        if n1 < 1e-9 or n2 < 1e-9:
            continue
        cosang = np.clip(np.dot(v1, v2) / (n1 * n2), -1.0, 1.0)
        if np.arccos(cosang) > threshold:
            turns += 1
    return turns


def tortuosity(path: list[tuple[float, float]]) -> float:
    if len(path) < 2:
        return 0.0
    direct = float(np.linalg.norm(np.asarray(path[-1]) - np.asarray(path[0])))
    if direct < 1e-9:
        return 0.0
    return path_length(path) / direct


def min_obstacle_distance(path: list[tuple[float, float]], obstacle_mask: np.ndarray) -> float:
    """Approximate minimum distance from path to obstacle cells in coordinate units."""

    obstacle_cells = np.argwhere(obstacle_mask)
    if not path or len(obstacle_cells) == 0:
        return 100.0

    nrows, ncols = obstacle_mask.shape
    obstacle_xy = np.column_stack(
        [
            obstacle_cells[:, 1] / max(ncols - 1, 1) * 100.0,
            obstacle_cells[:, 0] / max(nrows - 1, 1) * 100.0,
        ]
    )
    pts = np.asarray(path, dtype=float)
    min_dist = np.inf
    for pt in pts:
        min_dist = min(min_dist, float(np.min(np.linalg.norm(obstacle_xy - pt, axis=1))))
    return float(min_dist)


def analyze_path(
    algorithm: str,
    path: list[tuple[float, float]],
    risk_field: np.ndarray,
    cost_field: np.ndarray,
    obstacle_mask: np.ndarray,
    runtime_s: float,
    node_count: int,
    success: bool,
) -> dict:
    risk_sum, risk_mean = cumulative_field(path, risk_field)
    cost_sum, _ = cumulative_field(path, cost_field)
    return {
        "algorithm": algorithm,
        "success": bool(success),
        "path_length": path_length(path),
        "cumulative_risk": risk_sum,
        "cumulative_cost": cost_sum,
        "average_risk": risk_mean,
        "min_obstacle_distance": min_obstacle_distance(path, obstacle_mask),
        "runtime_s": float(runtime_s),
        "node_count": int(node_count),
        "turn_count": turn_count(path),
        "tortuosity": tortuosity(path),
    }


def metrics_to_frame(metrics: list[dict]) -> pd.DataFrame:
    if not metrics:
        return pd.DataFrame()
    return pd.DataFrame(metrics)

