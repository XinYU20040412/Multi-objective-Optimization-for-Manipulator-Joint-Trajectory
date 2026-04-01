"""Hamiltonian cycle solvers (TSP-like)."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np


@dataclass(frozen=True)
class HamiltonianResult:
    cost: float
    path: tuple[int, ...]
    method: str


def _validate_graph(weight_matrix: np.ndarray) -> np.ndarray:
    graph = np.asarray(weight_matrix, dtype=float)
    if graph.ndim != 2 or graph.shape[0] != graph.shape[1]:
        raise ValueError("weight_matrix must be a square matrix")
    if np.any(graph < 0):
        raise ValueError("weight_matrix cannot contain negative weights")
    if np.any(np.diag(graph) != 0):
        raise ValueError("Diagonal of weight_matrix must be all zeros")
    return graph


def _solve_dp(graph: np.ndarray, start: int = 0) -> HamiltonianResult:
    n = graph.shape[0]
    all_mask = (1 << n) - 1

    @lru_cache(maxsize=None)
    def dp(mask: int, last: int) -> tuple[float, tuple[int, ...]]:
        if mask == (1 << start) and last == start:
            return 0.0, (start,)

        if not (mask & (1 << last)):
            return float("inf"), ()

        prev_mask = mask ^ (1 << last)
        if prev_mask == 0:
            return float("inf"), ()

        best_cost = float("inf")
        best_path: tuple[int, ...] = ()

        for prev in range(n):
            if not (prev_mask & (1 << prev)):
                continue
            edge = graph[prev, last]
            if edge <= 0:
                continue
            prev_cost, prev_path = dp(prev_mask, prev)
            new_cost = prev_cost + edge
            if new_cost < best_cost:
                best_cost = new_cost
                best_path = prev_path + (last,)

        return best_cost, best_path

    best_total = float("inf")
    best_cycle: tuple[int, ...] = ()

    for last in range(n):
        if last == start:
            continue
        edge_back = graph[last, start]
        if edge_back <= 0:
            continue
        cost, path = dp(all_mask, last)
        total = cost + edge_back
        if total < best_total:
            best_total = total
            best_cycle = path + (start,)

    if not best_cycle:
        raise ValueError("No Hamiltonian cycle found for this graph")

    return HamiltonianResult(cost=float(best_total), path=best_cycle, method="dynamic_programming")


def _solve_branch_and_bound(graph: np.ndarray, start: int = 0) -> HamiltonianResult:
    n = graph.shape[0]
    best_cost = float("inf")
    best_path: tuple[int, ...] = ()

    min_out = np.where(graph > 0, graph, np.inf).min(axis=1)

    def lower_bound(path: list[int], cost_so_far: float, visited: np.ndarray) -> float:
        remaining = np.where(~visited)[0]
        if len(remaining) == 0:
            return cost_so_far
        return cost_so_far + float(np.sum(min_out[remaining]))

    visited = np.zeros(n, dtype=bool)
    visited[start] = True

    def dfs(current: int, path: list[int], cost_so_far: float) -> None:
        nonlocal best_cost, best_path

        if len(path) == n:
            back = graph[current, start]
            if back > 0:
                total = cost_so_far + back
                if total < best_cost:
                    best_cost = total
                    best_path = tuple(path + [start])
            return

        if lower_bound(path, cost_so_far, visited) >= best_cost:
            return

        next_nodes = np.where((graph[current] > 0) & (~visited))[0]
        next_nodes = sorted(next_nodes, key=lambda node: graph[current, node])

        for nxt in next_nodes:
            visited[nxt] = True
            path.append(int(nxt))
            dfs(int(nxt), path, cost_so_far + graph[current, nxt])
            path.pop()
            visited[nxt] = False

    dfs(start, [start], 0.0)

    if not best_path:
        raise ValueError("No Hamiltonian cycle found for this graph")

    return HamiltonianResult(cost=float(best_cost), path=best_path, method="branch_and_bound")


def solve_hamiltonian(
    weight_matrix: np.ndarray,
    method: str = "dp",
    start: int = 0,
) -> HamiltonianResult:
    graph = _validate_graph(weight_matrix)

    if method in {"dp", "dynamic_programming"}:
        return _solve_dp(graph, start)
    if method in {"bnb", "branch_and_bound"}:
        return _solve_branch_and_bound(graph, start)

    raise ValueError("method must be one of: dp, dynamic_programming, bnb, branch_and_bound")
