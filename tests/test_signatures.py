import numpy as np
import pytest

from museselect.signatures import build_static_signature, centroid_distance


def test_identical_centroids_have_zero_distance():
    values = np.asarray([[1.0, 0.0], [0.0, 1.0]])
    assert centroid_distance(values, values) == pytest.approx(0.0)


def test_signature_is_finite():
    audio = np.asarray([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    text = np.asarray([[0.5, 0.2], [0.1, 0.9], [0.6, 0.7]])
    signature = build_static_signature(audio, text, audio, text)
    assert np.isfinite(list(signature.__dict__.values())).all()
    assert signature.interaction_gap == pytest.approx(0.0)

