# Data format

MuSeSelect separates selection-time evidence from evaluation-time outcomes.

## Selection-time candidate record

| Field | Type | Meaning |
|---|---|---|
| `candidate_id` | string | Stable identifier for one predeclared block |
| `source_id` | string | Corpus/source identifier used for hierarchical routing |
| `audio_centroid_distance` | float | Source--target distance from frozen audio representations |
| `text_centroid_distance` | float | Source--target distance from frozen text representations |
| `interaction_gap` | float | Absolute difference in paired audio--text linear CKA |
| `log_size` | float | `log(1 + candidate examples)` |
| `missing_rate` | float in [0, 1] | Fraction of unavailable modality records |

The public loader rejects fields named `utility`, `realized_utility`,
`transfer_gain`, validation/test labels, test scores, and oracle ranks.

## Sealed evaluation record

Evaluation utilities are stored separately and opened only after a
`FreezeRecord` has been serialized. They map every `candidate_id` to the mean
validation macro-F1 change over the locked seeds.

## Embedding arrays

`build_static_signature` expects four finite two-dimensional NumPy arrays:
source audio, source text, target-anchor audio, and target-anchor text. Modalities
must be sample-aligned within each dataset. Source and target dimensions must
match within a modality.

## Data not distributed here

No audio, video, transcript, label table, or cached per-example representation
from CMU-MOSI, CMU-MOSEI, CH-SIMS, or MELD is included. Obtain those artifacts
from the original providers.

