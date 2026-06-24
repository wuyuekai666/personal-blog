from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .fields import cost_value, risk_value


@dataclass(frozen=True)
class GAConfig:
    selected_count: int
    population_size: int
    generations: int
    crossover_prob: float
    mutation_prob: float
    w_demand: float
    w_risk: float
    w_cost: float
    service_radius: float
    seed: int


@dataclass
class GAResult:
    best_indices: np.ndarray
    best_score: float
    history: pd.DataFrame
    candidate_metrics: pd.DataFrame


def _coverage_by_candidate(
    candidates: pd.DataFrame,
    demand: pd.DataFrame,
    service_radius: float,
) -> tuple[np.ndarray, np.ndarray]:
    candidate_xy = candidates[["x", "y"]].to_numpy()
    demand_xy = demand[["x", "y"]].to_numpy()
    demand_w = demand["demand_weight"].to_numpy()

    distances = np.linalg.norm(candidate_xy[:, None, :] - demand_xy[None, :, :], axis=2)
    covered = distances <= service_radius
    weighted_coverage = covered @ demand_w
    return weighted_coverage, covered


def _repair_chromosome(chromosome: np.ndarray, selected_count: int, rng: np.random.Generator) -> np.ndarray:
    repaired = chromosome.copy().astype(int)
    selected = np.flatnonzero(repaired == 1)
    missing = selected_count - len(selected)

    if missing > 0:
        zeros = np.flatnonzero(repaired == 0)
        repaired[rng.choice(zeros, size=missing, replace=False)] = 1
    elif missing < 0:
        repaired[rng.choice(selected, size=-missing, replace=False)] = 0
    return repaired


def _initialize_population(
    population_size: int,
    gene_count: int,
    selected_count: int,
    rng: np.random.Generator,
) -> np.ndarray:
    population = np.zeros((population_size, gene_count), dtype=int)
    for row in population:
        row[rng.choice(gene_count, size=selected_count, replace=False)] = 1
    return population


def run_ga(
    candidates: pd.DataFrame,
    demand: pd.DataFrame,
    hotspots,
    cost_mode: str,
    config: GAConfig,
) -> GAResult:
    """Select final vertiports from candidates using a binary genetic algorithm."""

    rng = np.random.default_rng(config.seed + 20_000)
    gene_count = len(candidates)
    selected_count = int(np.clip(config.selected_count, 1, gene_count))
    population_size = max(6, int(config.population_size))

    coverage_raw, covered_matrix = _coverage_by_candidate(candidates, demand, config.service_radius)
    total_demand = max(float(demand["demand_weight"].sum()), 1e-9)
    coverage_norm = coverage_raw / total_demand
    risks = risk_value(candidates[["x", "y"]].to_numpy(), hotspots)
    costs = cost_value(candidates[["x", "y"]].to_numpy(), cost_mode)

    candidate_metrics = candidates.copy()
    candidate_metrics["coverage"] = coverage_raw
    candidate_metrics["coverage_ratio"] = coverage_norm
    candidate_metrics["risk"] = risks
    candidate_metrics["cost"] = costs
    candidate_metrics["single_score"] = (
        config.w_demand * coverage_norm - config.w_risk * risks - config.w_cost * costs
    )

    def fitness(population: np.ndarray) -> np.ndarray:
        scores = np.zeros(population.shape[0], dtype=float)
        for idx, chrom in enumerate(population):
            selected = np.flatnonzero(chrom == 1)
            union_covered = np.any(covered_matrix[selected], axis=0)
            coverage = float(np.sum(demand.loc[union_covered, "demand_weight"])) / total_demand
            risk_penalty = float(np.mean(risks[selected]))
            cost_penalty = float(np.mean(costs[selected]))
            scores[idx] = (
                config.w_demand * coverage
                - config.w_risk * risk_penalty
                - config.w_cost * cost_penalty
            )
        return scores

    population = _initialize_population(population_size, gene_count, selected_count, rng)
    best_chromosome = population[0].copy()
    best_score = -np.inf
    history_rows = []

    for generation in range(max(1, int(config.generations))):
        scores = fitness(population)
        gen_best_idx = int(np.argmax(scores))
        if scores[gen_best_idx] > best_score:
            best_score = float(scores[gen_best_idx])
            best_chromosome = population[gen_best_idx].copy()

        history_rows.append(
            {
                "generation": generation + 1,
                "best_fitness": best_score,
                "mean_fitness": float(np.mean(scores)),
            }
        )

        shifted = scores - np.min(scores) + 1e-9
        probs = shifted / np.sum(shifted)
        parent_indices = rng.choice(population_size, size=population_size, replace=True, p=probs)
        parents = population[parent_indices]

        next_population = []
        elite = best_chromosome.copy()
        next_population.append(elite)

        while len(next_population) < population_size:
            p1 = parents[rng.integers(0, population_size)].copy()
            p2 = parents[rng.integers(0, population_size)].copy()

            if rng.random() < config.crossover_prob and gene_count > 1:
                point = int(rng.integers(1, gene_count))
                child1 = np.concatenate([p1[:point], p2[point:]])
                child2 = np.concatenate([p2[:point], p1[point:]])
            else:
                child1, child2 = p1.copy(), p2.copy()

            for child in (child1, child2):
                mutation_mask = rng.random(gene_count) < config.mutation_prob
                child[mutation_mask] = 1 - child[mutation_mask]
                child = _repair_chromosome(child, selected_count, rng)
                next_population.append(child)
                if len(next_population) >= population_size:
                    break

        population = np.asarray(next_population, dtype=int)

    return GAResult(
        best_indices=np.flatnonzero(best_chromosome == 1),
        best_score=best_score,
        history=pd.DataFrame(history_rows),
        candidate_metrics=candidate_metrics,
    )

