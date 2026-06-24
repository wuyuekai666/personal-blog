from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


AREA_SIZE = 100.0


@dataclass(frozen=True)
class DemandConfig:
    """Parameters for generating synthetic passenger demand points."""

    num_points: int
    seed: int
    weight_min: float
    weight_max: float
    hotspot_count: int = 4
    hotspot_spread: float = 10.0


def generate_demand_points(config: DemandConfig) -> pd.DataFrame:
    """Generate weighted demand points using several Gaussian urban hotspots."""

    rng = np.random.default_rng(config.seed)
    hotspot_count = max(1, int(config.hotspot_count))

    centers = rng.uniform(15.0, 85.0, size=(hotspot_count, 2))
    hotspot_probs = rng.dirichlet(np.ones(hotspot_count))
    assignments = rng.choice(hotspot_count, size=config.num_points, p=hotspot_probs)

    coords = centers[assignments] + rng.normal(
        loc=0.0,
        scale=config.hotspot_spread,
        size=(config.num_points, 2),
    )
    coords = np.clip(coords, 0.0, AREA_SIZE)
    weights = rng.uniform(config.weight_min, config.weight_max, size=config.num_points)

    return pd.DataFrame(
        {
            "id": np.arange(config.num_points),
            "x": coords[:, 0],
            "y": coords[:, 1],
            "demand_weight": weights,
            "source_hotspot": assignments,
        }
    )


def make_grid(grid_size: int = 180) -> tuple[np.ndarray, np.ndarray]:
    """Create a regular grid covering the 100 x 100 study region."""

    axis = np.linspace(0.0, AREA_SIZE, grid_size)
    return np.meshgrid(axis, axis)

