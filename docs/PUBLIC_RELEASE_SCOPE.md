# Public release scope

## Included

- Paper-facing reference package and tests.
- Static signature definitions named in the manuscript.
- Freeze/audit record for enforcing the information boundary.
- Synthetic schema examples.
- Aggregate, non-identifying result tables from the manuscript.
- Dataset provenance and official access links.
- Static project website source.

## Excluded

- Raw or extracted audio/video and transcripts.
- Third-party labels or pretrained-model files.
- Per-example embeddings that could encode restricted source material.
- Credentials, local paths, download cookies, signed URLs, and API tokens.
- The complete internal training/analysis pipeline.
- Unreported experiments, reviewer drafts, research diaries, and failure logs.
- ICLR template files and unpublished manuscript source.

## Why the release is partial

The public surface is designed to audit the paper's method while respecting
third-party dataset terms and preserving a manageable anonymous artifact. The
README must never imply that omitted licensed data can be reconstructed from the
repository.

## Publication blockers

Before public upload, the authors must supply:

1. GitHub owner/organization and final repository name;
2. Hugging Face owner/organization and dataset name;
3. website host or GitHub Pages repository;
4. confirmation that MIT for software and CC BY 4.0 for original aggregate
   data remain appropriate;
5. public author names and archival paper URL, or an explicit decision to keep
   the artifact anonymous during review.
