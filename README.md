# MuSeSelect

Official research-preview code for **Stress-Testing Prospective Multimodal
Dataset Utility Prediction** (under review for ICLR 2027).

MuSeSelect asks a deliberately prospective question: can an audio--text source
be screened for a fixed target task and learner *before* its transfer outcome is
known? The paper separates three decisions that are often conflated:

1. route to a source corpus;
2. rank candidate buckets within that source; and
3. select or abstain under an independently calibrated rule.

This repository releases the paper-facing reference surface: the information
boundary, static signature computation, frozen-decision record, post-freeze
evaluation metrics, a synthetic example, and tests. It intentionally excludes
the private research pipeline, raw corpora, cached embeddings, dataset download
automation, and unreleased analysis notebooks.

> **Status.** This is an anonymous submission artifact, not a claim of ICLR
> acceptance. Author, paper, GitHub, and Hugging Face URLs remain release-time
> metadata until anonymity is lifted.

## What is implemented

- Pre-training-safe audio/text centroid and interaction signatures.
- An explicit `SelectionView` that contains no validation labels or realized
  utility.
- A deterministic source-routing baseline and immutable freeze record.
- Post-freeze utility, regret, harm, coverage, and rank-correlation evaluation.
- Schema validation for synthetic or user-supplied aggregate candidate records.

The complete learner training loops and learned selectors are not included.
This mirrors the paper's separation between the selection-time interface and
the sealed evaluation system.

## Install and run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
museselect examples/candidates.json examples/frozen_decisions.json
pytest -q
```

The example contains synthetic aggregate statistics only. It is not paper
evidence and does not reproduce any copyrighted transcript or media.

## Input contract

Each candidate record must contain:

```json
{
  "candidate_id": "source_a::bucket_0",
  "source_id": "source_a",
  "audio_centroid_distance": 0.31,
  "text_centroid_distance": 0.18,
  "interaction_gap": 0.07,
  "log_size": 5.55,
  "missing_rate": 0.0
}
```

No target-validation label, test label, transfer score, or downstream result is
accepted by the selection-time schema. See [the data format](docs/DATA_FORMAT.md).

## Paper-to-code map

The exact scope of each public module and the corresponding paper section is
recorded in [PAPER_CODE_MAP.md](docs/PAPER_CODE_MAP.md). In brief:

| Paper concept | Public code |
|---|---|
| Prospective information boundary | `museselect.boundary` |
| Static source--target signatures | `museselect.signatures` |
| Frozen source routing / decisions | `museselect.selection` |
| Realized utility and regret | `museselect.evaluation` |

## Main empirical conclusion

The release preserves the paper's deliberately narrow conclusion. Under the
fixed logistic-regression recipe, source routing is stable over repeated
decisions, but within-source bucket ordering and nonvacuous calibrated
abstention are not reliable. Matched alternative learners change the utility
prevalence, rankings, and source routes. The project therefore does **not** claim
that a single learner-agnostic scalar measures universal dataset quality.

## Data

Raw CMU-MOSI, CMU-MOSEI, CH-SIMS, and MELD media are not redistributed. The
companion Hugging Face package contains only paper-level aggregate tables,
provenance metadata, and synthetic schema examples. Users must obtain source
datasets from their official providers and comply with their terms.

## Repository scope and licensing

Read [PUBLIC_RELEASE_SCOPE.md](docs/PUBLIC_RELEASE_SCOPE.md) before extending this
artifact. The software is released under the MIT License. Original aggregate
tables and metadata under `huggingface/` are released under CC BY 4.0; upstream
dataset terms remain controlling for all third-party materials.

## Citation

Citation metadata will be added after author identities and the archival paper
URL are public. Until then, cite the anonymous ICLR 2027 submission title.
