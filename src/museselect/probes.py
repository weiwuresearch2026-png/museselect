"""Public scoring equations for candidate-trained transferability probes.

This module does not train candidate heads.  It accepts their outputs on a
labeled target anchor, keeping the public release separate from the private
dataset loaders and learner-training pipeline.
"""

from __future__ import annotations

import numpy as np


def _labels(value: np.ndarray, rows: int) -> np.ndarray:
    labels = np.asarray(value, dtype=int).reshape(-1)
    if len(labels) != rows or labels.min(initial=0) < 0:
        raise ValueError("target_labels must be nonnegative and match the rows")
    return labels


def leep_score(source_probabilities: np.ndarray, target_labels: np.ndarray) -> float:
    """Compute LEEP from a candidate-trained head evaluated on a target anchor."""
    probability = np.asarray(source_probabilities, dtype=np.float64)
    if probability.ndim != 2 or len(probability) == 0:
        raise ValueError("source_probabilities must be a nonempty 2D array")
    if not np.isfinite(probability).all() or np.any(probability < 0):
        raise ValueError("source_probabilities must be finite and nonnegative")
    row_sum = probability.sum(axis=1, keepdims=True)
    if np.any(row_sum <= 0):
        raise ValueError("every probability row must have positive mass")
    probability = probability / row_sum
    labels = _labels(target_labels, len(probability))
    target_classes = int(labels.max()) + 1
    joint = np.zeros((target_classes, probability.shape[1]), dtype=np.float64)
    normalized = probability / len(probability)
    for label in range(target_classes):
        joint[label] = normalized[labels == label].sum(axis=0)
    conditional = (
        joint / np.clip(joint.sum(axis=0, keepdims=True), 1e-12, None)
    ).T
    empirical = probability @ conditional
    selected = empirical[np.arange(len(labels)), labels]
    return float(np.log(np.clip(selected, 1e-12, None)).mean())


def logme_score(features: np.ndarray, target_labels: np.ndarray) -> float:
    """Compute classification LogME with the published fixed-point iteration."""
    matrix = np.asarray(features, dtype=np.float64)
    if matrix.ndim != 2 or len(matrix) == 0 or not np.isfinite(matrix).all():
        raise ValueError("features must be a finite nonempty 2D array")
    labels = _labels(target_labels, len(matrix))
    rows, dimensions = matrix.shape
    u, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    sigma = singular.reshape(-1, 1) ** 2
    evidences: list[float] = []
    for label in range(int(labels.max()) + 1):
        target = (labels == label).astype(np.float64).reshape(-1, 1)
        projected = u.T @ target
        projected2 = projected**2
        residual_projection = max(
            0.0, float((target**2).sum() - projected2.sum())
        )
        alpha = beta = 1.0
        for _ in range(11):
            ratio = alpha / beta
            gamma = float((sigma / (sigma + ratio)).sum())
            weight2 = float(
                (sigma * projected2 / ((ratio + sigma) ** 2)).sum()
            )
            residual2 = float(
                (projected2 / ((1 + sigma / ratio) ** 2)).sum()
                + residual_projection
            )
            alpha = gamma / (weight2 + 1e-5)
            beta = (rows - gamma) / (residual2 + 1e-5)
            new_ratio = alpha / beta
            if abs(new_ratio - ratio) / max(ratio, 1e-12) <= 1e-3:
                break
        evidence = (
            dimensions / 2 * np.log(alpha)
            + rows / 2 * np.log(beta)
            - 0.5 * np.log(alpha + beta * sigma).sum()
            - beta / 2 * residual2
            - alpha / 2 * weight2
            - rows / 2 * np.log(2 * np.pi)
        ) / rows
        evidences.append(float(evidence))
    return float(np.mean(evidences))
