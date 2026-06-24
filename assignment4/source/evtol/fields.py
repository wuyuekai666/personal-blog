from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .scene import AREA_SIZE


@dataclass(frozen=True)
class RiskHotspot:
    x: float
    y: float
    sigma: float
    intensity: float
    label: str


def normalize(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    vmin = float(np.min(values))
    vmax = float(np.max(values))
    if np.isclose(vmin, vmax):
        return np.zeros_like(values, dtype=float)
    return (values - vmin) / (vmax - vmin)


def create_risk_hotspots(
    count: int,
    intensity: float,
    seed: int,
) -> list[RiskHotspot]:
    """Create Gaussian risk sources such as no-fly zones and dense population areas."""

    rng = np.random.default_rng(seed + 10_000)
    labels = ["禁飞敏感区", "人口密集区", "重要建筑区", "机场保护区", "医院学校区", "大型活动区"]
    hotspots: list[RiskHotspot] = []

    for idx in range(max(1, count)):
        hotspots.append(
            RiskHotspot(
                x=float(rng.uniform(8.0, 92.0)),
                y=float(rng.uniform(8.0, 92.0)),
                sigma=float(rng.uniform(7.0, 16.0)),
                intensity=float(intensity * rng.uniform(0.75, 1.25)),
                label=labels[idx % len(labels)],
            )
        )
    return hotspots


def risk_value(points: np.ndarray, hotspots: list[RiskHotspot]) -> np.ndarray:
    """Evaluate normalized risk at N two-dimensional points."""

    pts = np.atleast_2d(points).astype(float)
    raw = np.zeros(pts.shape[0], dtype=float)
    for hotspot in hotspots:
        dist2 = (pts[:, 0] - hotspot.x) ** 2 + (pts[:, 1] - hotspot.y) ** 2
        raw += hotspot.intensity * np.exp(-dist2 / (2.0 * hotspot.sigma**2))
    return normalize(raw)


def risk_grid(xx: np.ndarray, yy: np.ndarray, hotspots: list[RiskHotspot]) -> np.ndarray:
    points = np.column_stack([xx.ravel(), yy.ravel()])
    return risk_value(points, hotspots).reshape(xx.shape)


def _gaussian_peak(points: np.ndarray, center: tuple[float, float], sigma: float) -> np.ndarray:
    center_arr = np.asarray(center, dtype=float)
    dist2 = np.sum((points - center_arr) ** 2, axis=1)
    return np.exp(-dist2 / (2.0 * sigma**2))


def _corridor_discount(points: np.ndarray) -> np.ndarray:
    """Simulate lower cost near major traffic corridors and interchange belts."""

    corridor_main = 52.0 + 11.0 * np.sin(points[:, 0] / 15.0)
    corridor_aux = 28.0 + 7.0 * np.cos(points[:, 0] / 18.0)
    d1 = np.exp(-((points[:, 1] - corridor_main) ** 2) / (2.0 * 7.0**2))
    d2 = np.exp(-((points[:, 1] - corridor_aux) ** 2) / (2.0 * 6.0**2))
    return np.clip(0.65 * d1 + 0.35 * d2, 0.0, 1.0)


def _transit_hub_discount(points: np.ndarray) -> np.ndarray:
    """Simulate lower connection cost near existing hubs/interchanges."""

    hub1 = _gaussian_peak(points, (22.0, 78.0), 10.0)
    hub2 = _gaussian_peak(points, (66.0, 70.0), 11.0)
    hub3 = _gaussian_peak(points, (83.0, 58.0), 9.0)
    return np.clip(0.32 * hub1 + 0.40 * hub2 + 0.28 * hub3, 0.0, 1.0)


def cost_value(points: np.ndarray, mode: str = "中心城区高成本") -> np.ndarray:
    """Evaluate normalized construction/operation cost at N points.

    The cost field is intentionally not purely radial. It mixes:
    1. central land price pressure,
    2. local business-district peaks,
    3. discounts near transport corridors,
    4. discounts near existing transfer hubs.
    """

    pts = np.atleast_2d(points).astype(float)
    city_center = np.array([AREA_SIZE / 2.0, AREA_SIZE / 2.0])
    dist_center = np.linalg.norm(pts - city_center, axis=1)
    central_price = 1.0 - normalize(dist_center)

    corridor_discount = _corridor_discount(pts)
    hub_discount = _transit_hub_discount(pts)

    if mode == "靠近交通走廊低成本":
        corridor_bonus = 1.0 - corridor_discount
        hub_bonus = 1.0 - hub_discount
        cbd1 = _gaussian_peak(pts, (72.0, 62.0), 16.0)
        cbd2 = _gaussian_peak(pts, (30.0, 80.0), 12.0)
        raw = 0.28 * central_price + 0.22 * cbd1 + 0.10 * cbd2 + 0.25 * corridor_bonus + 0.15 * hub_bonus
    elif mode == "多中心商务区高成本":
        cbd1 = _gaussian_peak(pts, (34.0, 78.0), 12.0)
        cbd2 = _gaussian_peak(pts, (69.0, 64.0), 14.0)
        cbd3 = _gaussian_peak(pts, (58.0, 42.0), 13.0)
        raw = (
            0.18 * central_price
            + 0.26 * cbd1
            + 0.32 * cbd2
            + 0.24 * cbd3
            - 0.10 * corridor_discount
            - 0.08 * hub_discount
        )
    else:
        inner_core = _gaussian_peak(pts, (52.0, 52.0), 20.0)
        east_cbd = _gaussian_peak(pts, (77.0, 63.0), 15.0)
        north_cbd = _gaussian_peak(pts, (31.0, 80.0), 12.0)
        raw = (
            0.34 * central_price
            + 0.28 * inner_core
            + 0.20 * east_cbd
            + 0.12 * north_cbd
            - 0.12 * corridor_discount
            - 0.08 * hub_discount
        )

    return normalize(raw)


def cost_grid(xx: np.ndarray, yy: np.ndarray, mode: str = "中心城区高成本") -> np.ndarray:
    points = np.column_stack([xx.ravel(), yy.ravel()])
    return cost_value(points, mode).reshape(xx.shape)
