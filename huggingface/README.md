---
pretty_name: MuSeSelect Paper Aggregate Artifact
license: cc-by-4.0
language:
- en
task_categories:
- text-classification
tags:
- multimodal
- audio-text
- dataset-selection
- transfer-learning
- research-artifact
configs:
- config_name: paper_results
  data_files:
  - split: test
    path: data/paper_results.csv
- config_name: corpus_registry
  data_files:
  - split: train
    path: data/corpus_registry.csv
- config_name: cross_model_summary
  data_files:
  - split: test
    path: data/cross_model_summary.csv
- config_name: synthetic_schema
  data_files:
  - split: train
    path: data/synthetic_candidates.jsonl
---

# MuSeSelect paper aggregate artifact

Companion metadata for **Stress-Testing Prospective Multimodal Dataset Utility
Prediction** (anonymous ICLR 2027 submission).

This repository is **not** a redistribution of CMU-MOSI, CMU-MOSEI, CH-SIMS,
or MELD. It contains only:

- aggregate numbers reported in the manuscript;
- official source links and redistribution status;
- synthetic rows demonstrating the public selection-time schema.

The synthetic rows are marked `synthetic=true` and are not scientific evidence.

## Dataset configurations

### `paper_results`

One row per reported learner/rule combination. Utility is the mean change in
validation macro-F1 after a frozen selection. Positive rate, harm rate, regret,
and route accuracy use the definitions in the paper.

### `corpus_registry`

The four corpora used in the main and auxiliary panels, with official access
pages. `redistributed_here` is false for every corpus.

### `cross_model_summary`

Aggregate rank and sign agreement between the logistic reference and each
matched alternative learner.

### `synthetic_schema`

Three fabricated candidate blocks demonstrating the selection-time fields.
They contain no transcript, media, label, embedding, or observed transfer
outcome.

## Intended use

- Check that public tables match the manuscript.
- Test loaders against the aggregate schema.
- Demonstrate the information boundary and frozen-decision workflow.
- Link users to official dataset providers.

## Out-of-scope uses

This package must not be used as if it were the underlying multimodal training
corpora, and it cannot reproduce the paper's model fits by itself. It is not a
general-purpose benchmark of universal “dataset quality.” Utility is conditional
on the target, learner, training recipe, partition, and metric.

## Main finding and limitations

For the fixed logistic-regression recipe, the centroid route identifies the
oracle source in 44 of 45 repeated decisions across three independent target
corpora. The evidence does not extend to reliable within-source bucket ranking
or nonvacuous calibrated abstention. Matched GaussianNB, neural-MLP, and learned
gated-fusion panels change route accuracy and utility prevalence. These results
support a narrow, model-conditional interpretation.

## Licensing

Original aggregate tables, registry metadata, and synthetic examples in this
package are released under CC BY 4.0; see `LICENSE-DATA`. Upstream dataset terms
remain controlling and are not modified by this repository. No third-party raw
media, transcripts, labels, or per-example embeddings are relicensed here.

## Citation

Final BibTeX will be supplied after author identities and the archival paper URL
are public. During anonymous review, cite the paper title and “Anonymous authors,
ICLR 2027 submission.”
