"""Public reference interface for MuSeSelect."""

from .boundary import CandidateRecord, SelectionView
from .evaluation import realized_utility, selection_report
from .selection import FreezeRecord, freeze_predictions, route_by_centroid
from .signatures import StaticSignature, build_static_signature

__all__ = [
    "CandidateRecord",
    "FreezeRecord",
    "SelectionView",
    "StaticSignature",
    "build_static_signature",
    "freeze_predictions",
    "realized_utility",
    "route_by_centroid",
    "selection_report",
]

__version__ = "0.1.0"

