# Paper-to-code map

This map identifies exactly which parts of the manuscript have a
public reference implementation. Line numbers are intentionally avoided because
the manuscript is still being revised.

| Manuscript component | Public artifact | Released behavior | Deliberately withheld |
|---|---|---|---|
| Sec. 3, utility definition | `museselect.evaluation.realized_utility` | Mean seeded change between anchor and augmented validation macro-F1 | Learner fitting and dataset-specific preprocessing |
| Sec. 3, information boundary | `museselect.boundary.SelectionView` | Rejects sealed outcome, validation, test, and oracle fields | Internal experiment registry and data loaders |
| Sec. 4, common representations | `configs/paper_protocol.yaml` | Names encoders and block sizes | Model caches and copyrighted media |
| Sec. 4, static evidence | `museselect.signatures` | Centroid distances, paired linear CKA gap, size and missingness | Full feature engineering and learned-selector pipeline |
| Sec. 4, frozen predictions | `museselect.selection.freeze_predictions` | Immutable decision, timestamp, deterministic SHA-256 digest | Private run orchestration |
| Sec. 4, candidate-trained probes | `museselect.probes` | LEEP and fixed-point LogME scoring from supplied head outputs | Candidate head training and corpus loaders |
| Sec. 5, source routing baseline | `museselect.workflow.route_source_by_centroid` | Mean joint-centroid score over buckets from each source | Alternative experimental selectors |
| Sec. 5, staged compromise | `museselect.workflow` | Corpus-level distance route and probe-ranked top-k shortlist | Exact downstream pilot training |
| Sec. 5, ranking evaluation | `museselect.evaluation.selection_report` | Selected utility, Top-1 regret, harm, coverage, Kendall tau | Target-cluster bootstrap implementation and internal result ledger |

## What “official code” means here

The repository is an auditable paper-facing reference, not a dump of the full
research workspace. It is sufficient to inspect the information boundary,
recompute the released signature definitions, create a frozen decision record,
and evaluate it after utilities are revealed. It is not sufficient to recreate
the licensed corpora or every experiment reported in the submission.

## Consistency rules

1. A selector must receive `SelectionView`, never a dictionary containing
   realized utility or validation/test labels.
2. The freeze record must exist before sealed outcomes are loaded.
3. Synthetic examples and unit tests must never be described as paper evidence.
4. Public result tables must be generated from aggregate, non-identifying
   records and must match the manuscript values.
5. `museselect.probes` scores supplied candidate-head outputs; it must not be
   described as a static or training-free candidate selector.
