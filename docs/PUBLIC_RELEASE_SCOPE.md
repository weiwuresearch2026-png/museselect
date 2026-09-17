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
third-party dataset terms and preserving a manageable public artifact. The
README must never imply that omitted licensed data can be reconstructed from the
repository.

## Publication status

The GitHub repository and GitHub Pages site are live. Software is licensed under
MIT and original aggregate data under CC BY 4.0. Author metadata is public in
the author preprint.

The standalone Hugging Face dataset release is intentionally deferred. The
prepared dataset-card directory remains in this repository for audit and must
not be described as a live Hugging Face publication.
