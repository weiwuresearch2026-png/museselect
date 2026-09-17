"""Public reference interface for MuSeSelect."""

from .boundary import CandidateRecord, SelectionView
from .evaluation import realized_utility, selection_report
from .selection import FreezeRecord, freeze_predictions, route_by_centroid
from .signatures import StaticSignature, build_static_signature
from .probes import leep_score, logme_score
from .workflow import StagedShortlist, build_staged_shortlist, route_source_by_centroid

__all__ = [
    "CandidateRecord",
    "FreezeRecord",
    "SelectionView",
    "StagedShortlist",
    "StaticSignature",
    "build_static_signature",
    "freeze_predictions",
    "leep_score",
    "logme_score",
    "realized_utility",
    "route_by_centroid",
    "route_source_by_centroid",
    "selection_report",
    "build_staged_shortlist",
]

__version__ = "0.2.0"
