"""AHP weighting methods with consistency checking."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


# Saaty Random Index for n=1..10.
RI_TABLE = {
    1: 0.0,
    2: 0.0,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49,
}


@dataclass(frozen=True)
class AHPResult:
    matrix: np.ndarray
    arithmetic_weight: np.ndarray
    geometric_weight: np.ndarray
    eigen_weight: np.ndarray
    combined_weight: np.ndarray
    lambda_max: float
    ci: float
    cr: float
    consistency_passed: bool


def _validate_pairwise(matrix: np.ndarray) -> np.ndarray:
    m = np.asarray(matrix, dtype=float)
    if m.ndim != 2 or m.shape[0] != m.shape[1]:
        raise ValueError("AHP matrix must be square")
    if np.any(m <= 0):
        raise ValueError("AHP matrix must be positive")
    if not np.allclose(np.diag(m), 1.0):
        raise ValueError("Diagonal elements of AHP matrix must be 1")
    return m


def _arithmetic_weight(matrix: np.ndarray) -> np.ndarray:
    col_norm = matrix / np.sum(matrix, axis=0, keepdims=True)
    weight = np.mean(col_norm, axis=1)
    return weight / np.sum(weight)


def _geometric_weight(matrix: np.ndarray) -> np.ndarray:
    geom = np.prod(matrix, axis=1) ** (1.0 / matrix.shape[0])
    return geom / np.sum(geom)


def _eigen_weight(matrix: np.ndarray) -> tuple[float, np.ndarray]:
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    idx = int(np.argmax(np.real(eigenvalues)))
    lambda_max = float(np.real(eigenvalues[idx]))
    vec = np.real(eigenvectors[:, idx])
    vec = np.abs(vec)
    weight = vec / np.sum(vec)
    return lambda_max, weight


def _consistency(lambda_max: float, n: int) -> tuple[float, float, bool]:
    if n <= 2:
        return 0.0, 0.0, True
    ci = (lambda_max - n) / (n - 1)
    ri = RI_TABLE.get(n, RI_TABLE[10])
    cr = ci / ri if ri > 0 else 0.0
    return float(ci), float(cr), cr < 0.1


def compute_ahp(matrix: np.ndarray) -> AHPResult:
    pairwise = _validate_pairwise(matrix)
    arithmetic_weight = _arithmetic_weight(pairwise)
    geometric_weight = _geometric_weight(pairwise)
    lambda_max, eigen_weight = _eigen_weight(pairwise)

    combined = (arithmetic_weight + geometric_weight + eigen_weight) / 3.0
    combined = combined / np.sum(combined)

    ci, cr, passed = _consistency(lambda_max, pairwise.shape[0])

    return AHPResult(
        matrix=pairwise,
        arithmetic_weight=arithmetic_weight,
        geometric_weight=geometric_weight,
        eigen_weight=eigen_weight,
        combined_weight=combined,
        lambda_max=lambda_max,
        ci=ci,
        cr=cr,
        consistency_passed=passed,
    )
