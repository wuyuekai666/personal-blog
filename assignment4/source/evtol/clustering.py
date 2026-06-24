from __future__ import annotations

import numpy as np
import pandas as pd


def run_kmeans(demand_df: pd.DataFrame, cluster_count: int, seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Cluster demand points and use weighted cluster centers as candidate vertiports."""

    coords = demand_df[["x", "y"]].to_numpy()
    cluster_count = int(np.clip(cluster_count, 1, len(demand_df)))
    weights = demand_df["demand_weight"].to_numpy()
    rng = np.random.default_rng(seed + 5_000)

    # K-means++ style initialization keeps the demo deterministic and avoids sklearn dependency.
    centers = np.empty((cluster_count, 2), dtype=float)
    first_idx = int(rng.integers(0, len(coords)))
    centers[0] = coords[first_idx]
    min_dist2 = np.sum((coords - centers[0]) ** 2, axis=1)

    for k in range(1, cluster_count):
        probs = min_dist2 * weights
        if np.isclose(probs.sum(), 0.0):
            next_idx = int(rng.integers(0, len(coords)))
        else:
            probs = probs / probs.sum()
            next_idx = int(rng.choice(len(coords), p=probs))
        centers[k] = coords[next_idx]
        min_dist2 = np.minimum(min_dist2, np.sum((coords - centers[k]) ** 2, axis=1))

    labels = np.zeros(len(coords), dtype=int)
    for _ in range(100):
        distances = np.linalg.norm(coords[:, None, :] - centers[None, :, :], axis=2)
        new_labels = np.argmin(distances, axis=1)

        new_centers = centers.copy()
        for k in range(cluster_count):
            mask = new_labels == k
            if np.any(mask):
                new_centers[k] = np.average(coords[mask], axis=0, weights=weights[mask])
            else:
                new_centers[k] = coords[int(rng.integers(0, len(coords)))]

        if np.array_equal(new_labels, labels) and np.allclose(new_centers, centers):
            labels = new_labels
            centers = new_centers
            break
        labels = new_labels
        centers = new_centers

    clustered = demand_df.copy()
    clustered["cluster"] = labels

    candidate_df = pd.DataFrame(
        {
            "candidate_id": np.arange(cluster_count),
            "x": centers[:, 0],
            "y": centers[:, 1],
        }
    )

    cluster_weight = clustered.groupby("cluster")["demand_weight"].sum()
    candidate_df["cluster_demand"] = candidate_df["candidate_id"].map(cluster_weight).fillna(0.0)
    return clustered, candidate_df
