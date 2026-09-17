"""Transparent static signatures computed without candidate-source training."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def _matrix(value: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(value, dtype=np.float64)
    if array.ndim != 2 or array.shape[0] < 2:
        raise ValueError(f"{name} must be a finite 2D array with at least two rows")
    if not np.isfinite(array).all():
        raise ValueError(f"{name} contains NaN or infinity")
    return array


def centroid_distance(source: np.ndarray, target: np.ndarray) -> float:
    """Euclidean distance between L2-normalized representation centroids."""
    source = _matrix(source, "source")
    target = _matrix(target, "target")
    if source.shape[1] != target.shape[1]:
        raise ValueError("source and target feature dimensions must match")
    source_center = source.mean(axis=0)
    target_center = target.mean(axis=0)
    source_center /= max(float(np.linalg.norm(source_center)), 1e-12)
    target_center /= max(float(np.linalg.norm(target_center)), 1e-12)
    return float(np.linalg.norm(source_center - target_center))


def linear_cka(audio: np.ndarray, text: np.ndarray) -> float:
    """Linear CKA for paired, sample-aligned audio and text representations."""
    audio = _matrix(audio, "audio")
    text = _matrix(text, "text")
    if audio.shape[0] != text.shape[0]:
        raise ValueError("audio and text representations must be sample-aligned")
    audio = audio - audio.mean(axis=0, keepdims=True)
    text = text - text.mean(axis=0, keepdims=True)
    cross = audio.T @ text
    numerator = float(np.square(cross).sum())
    denominator = float(
        np.sqrt(np.square(audio.T @ audio).sum() * np.square(text.T @ text).sum())
    )
    return 0.0 if denominator <= 1e-12 else numerator / denominator


@dataclass(frozen=True)
class StaticSignature:
    audio_centroid_distance: float
    text_centroid_distance: float
    interaction_gap: float
    log_size: float
    missing_rate: float


def build_static_signature(
    source_audio: np.ndarray,
    source_text: np.ndarray,
    target_audio: np.ndarray,
    target_text: np.ndarray,
    missing_rate: float = 0.0,
) -> StaticSignature:
    """Build the public paper-facing source--target signature."""
    source_audio = _matrix(source_audio, "source_audio")
    source_text = _matrix(source_text, "source_text")
    target_audio = _matrix(target_audio, "target_audio")
    target_text = _matrix(target_text, "target_text")
    if source_audio.shape[0] != source_text.shape[0]:
        raise ValueError("source modalities must be sample-aligned")
    if target_audio.shape[0] != target_text.shape[0]:
        raise ValueError("target modalities must be sample-aligned")
    if not 0.0 <= missing_rate <= 1.0:
        raise ValueError("missing_rate must lie in [0, 1]")
    return StaticSignature(
        audio_centroid_distance=centroid_distance(source_audio, target_audio),
        text_centroid_distance=centroid_distance(source_text, target_text),
        interaction_gap=abs(
            linear_cka(source_audio, source_text)
            - linear_cka(target_audio, target_text)
        ),
        log_size=float(np.log1p(source_audio.shape[0])),
        missing_rate=float(missing_rate),
    )

