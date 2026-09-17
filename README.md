# MuSeSelect

Official research-preview code for **Stress Testing Prospective Multimodal
Dataset Utility Prediction** (under review for ICLR 2027).

MuSeSelect asks a deliberately prospective question: can an audio and text source
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

> **Status.** This is a public author preprint and research preview, not a claim
> of ICLR acceptance. The authors are Yurong Cheng and Wei Wu, Beijing Institute
> of Technology. Yurong Cheng is the corresponding author.

## What is implemented

- Pre-training-safe audio/text centroid and interaction signatures.
- An explicit `SelectionView` that contains no validation labels or realized
  utility.
- A deterministic source-routing baseline and immutable freeze record.
- Post-freeze utility, regret, harm, coverage, and rank-correlation evaluation.
- Public LEEP and LogME scoring equations for candidate-trained head outputs.
- A staged source-routing and probe-shortlist interface.
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
| Candidate-trained LEEP / LogME scores | `museselect.probes` |
| Route-then-shortlist workflow | `museselect.workflow` |
| Realized utility and regret | `museselect.evaluation` |

## Main empirical conclusion

The release preserves the paper's deliberately narrow conclusion. Under the
fixed logistic regression recipe, source routing is stable over repeated
decisions, but bucket ordering within a source and nonvacuous calibrated
abstention are not reliable. The source distance gap is 22.33 times the typical
bucket spread on the sealed safety family. Matched gate controls reduce route
accuracy from 11/15 with fixed weights to 8/15 with a sample-dependent gate.

Canonical LEEP and LogME do not directly rank additive buckets under a shared
fixed representation. Their candidate-trained adaptations are reported in a
separate cost class. Distance routing followed by adapted LEEP gives mean
selected utility +0.00497 on the exploratory safety family. We then froze the
complete workflow before evaluating a new repartition family. Its top-two rule
gives +0.01084 mean safe utility, with a target-and-salt bootstrap interval of
[+0.00293, +0.01957], while avoiding 87.5% of full candidate runs. The result
contains only three independent target corpora and is not evidence of unseen
domain generalization. Aggregate tables are available in [`results/`](results/).

## Data

Raw CMU-MOSI, CMU-MOSEI, CH-SIMS, and MELD media are not redistributed. Users
must obtain source datasets from their official providers and comply with their
terms. A Hugging Face release is intentionally deferred.

## Repository scope and licensing

Read [PUBLIC_RELEASE_SCOPE.md](docs/PUBLIC_RELEASE_SCOPE.md) before extending this
artifact. The software is released under the MIT License. Original aggregate
tables and metadata under `huggingface/` are released under CC BY 4.0; upstream
dataset terms remain controlling for all third-party materials.

## Citation

```bibtex
@misc{cheng2026museselect,
  title  = {Stress Testing Prospective Multimodal Dataset Utility Prediction},
  author = {Yurong Cheng and Wei Wu},
  year   = {2026},
  note   = {ICLR 2027 submission, author preprint}
}
```
