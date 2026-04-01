"""Reusable genetic optimizer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


Objective = Callable[[np.ndarray], float]


@dataclass(frozen=True)
class GAConfig:
    population_size: int = 200
    generations: int = 120
    crossover_rate: float = 0.9
    mutation_rate: float = 0.18
    mutation_scale: float = 0.08
    elite_size: int = 2
    tournament_size: int = 4
    seed: int | None = 42


@dataclass(frozen=True)
class GAResult:
    best_individual: np.ndarray
    best_score: float
    history_best: np.ndarray
    history_mean: np.ndarray
    history_std: np.ndarray
    best_trace: np.ndarray


class GeneticOptimizer:
    """A bounded, minimization-focused GA with elitism and blend crossover."""

    def __init__(self, objective: Objective, bounds: np.ndarray, config: GAConfig) -> None:
        self.objective = objective
        self.bounds = np.asarray(bounds, dtype=float)
        if self.bounds.ndim != 2 or self.bounds.shape[1] != 2:
            raise ValueError("bounds must be shape (dimension, 2)")

        self.dimension = self.bounds.shape[0]
        self.config = config
        self.rng = np.random.default_rng(config.seed)

    def _initialize_population(self) -> np.ndarray:
        low = self.bounds[:, 0]
        high = self.bounds[:, 1]
        return self.rng.uniform(low=low, high=high, size=(self.config.population_size, self.dimension))

    def _evaluate(self, population: np.ndarray) -> np.ndarray:
        return np.array([self.objective(individual) for individual in population], dtype=float)

    def _tournament_selection(self, population: np.ndarray, scores: np.ndarray) -> np.ndarray:
        pop_size = len(population)
        draw = self.rng.integers(0, pop_size, size=(pop_size, self.config.tournament_size))
        winners = draw[np.arange(pop_size), np.argmin(scores[draw], axis=1)]
        return population[winners]

    def _crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        if self.rng.random() > self.config.crossover_rate:
            return parent1.copy(), parent2.copy()

        alpha = self.rng.random(self.dimension)
        child1 = alpha * parent1 + (1.0 - alpha) * parent2
        child2 = (1.0 - alpha) * parent1 + alpha * parent2
        return child1, child2

    def _mutate(self, child: np.ndarray) -> np.ndarray:
        mask = self.rng.random(self.dimension) < self.config.mutation_rate
        if np.any(mask):
            child = child.copy()
            child[mask] += self.rng.normal(0.0, self.config.mutation_scale, size=mask.sum())
        low = self.bounds[:, 0]
        high = self.bounds[:, 1]
        return np.clip(child, low, high)

    def run(self) -> GAResult:
        population = self._initialize_population()
        history_best: list[float] = []
        history_mean: list[float] = []
        history_std: list[float] = []
        best_trace: list[np.ndarray] = []

        for _ in range(self.config.generations):
            scores = self._evaluate(population)
            ranking = np.argsort(scores)
            elites = population[ranking[: self.config.elite_size]].copy()

            best_idx = ranking[0]
            history_best.append(float(scores[best_idx]))
            history_mean.append(float(np.mean(scores)))
            history_std.append(float(np.std(scores)))
            best_trace.append(population[best_idx].copy())

            parents = self._tournament_selection(population, scores)
            offspring: list[np.ndarray] = []
            target_size = self.config.population_size - self.config.elite_size

            while len(offspring) < target_size:
                idx1, idx2 = self.rng.integers(0, len(parents), size=2)
                child1, child2 = self._crossover(parents[idx1], parents[idx2])
                offspring.append(self._mutate(child1))
                if len(offspring) < target_size:
                    offspring.append(self._mutate(child2))

            population = np.vstack([elites, np.asarray(offspring, dtype=float)])

        final_scores = self._evaluate(population)
        final_best = int(np.argmin(final_scores))

        return GAResult(
            best_individual=population[final_best].copy(),
            best_score=float(final_scores[final_best]),
            history_best=np.asarray(history_best, dtype=float),
            history_mean=np.asarray(history_mean, dtype=float),
            history_std=np.asarray(history_std, dtype=float),
            best_trace=np.asarray(best_trace, dtype=float),
        )
