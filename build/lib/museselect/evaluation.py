"""Post-freeze evaluation; never import this module into selection pipelines."""

from __future__ import annotations

from typing import Mapping, Sequence

import numpy as np
from scipy.stats import kendalltau

from .selection import FreezeRecord


def realized_utility(anchor_scores: Sequence[float], augmented_scores: Sequence[float]) -> float:
    """Mean seeded validation-score change after the decision is frozen."""
    anchor = np.asarray(anchor_scores, dtype=np.float64)
    augmented = np.asarray(augmented_scores, dtype=np.float64)
    if anchor.shape != augmented.shape or anchor.ndim != 1 or len(anchor) == 0:
        raise ValueError("anchor and augmented scores must be equal non-empty vectors")
    if not np.isfinite(anchor).all() or not np.isfinite(augmented).all():
        raise ValueError("evaluation scores must be finite")
    return float(np.mean(augmented - anchor))


def selection_report(
    freeze: FreezeRecord,
    utilities: Mapping[str, float],
) -> dict[str, float | bool | str]:
    """Open sealed utilities and evaluate a previously frozen decision."""
    if set(utilities) != set(freeze.scores):
        raise ValueError("utilities must match the candidates in the freeze record")
    truth = np.asarray([float(utilities[key]) for key in sorted(utilities)])
    prediction = np.asarray([float(freeze.scores[key]) for key in sorted(utilities)])
    selected_utility = float(utilities[freeze.selected_candidate_id])
    tau = kendalltau(truth, prediction).statistic
    return {
        "selected_candidate_id": freeze.selected_candidate_id,
        "selected_utility": selected_utility,
        "top1_regret": float(truth.max() - selected_utility),
        "harm": bool(selected_utility < 0.0),
        "coverage": 1.0,
        "kendall_tau": float(0.0 if not np.isfinite(tau) else tau),
        "selection_digest": freeze.selection_digest,
    }

