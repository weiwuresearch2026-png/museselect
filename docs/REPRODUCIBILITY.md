# Reproducibility

The public package targets Python 3.10+ and provides both `pyproject.toml` and a
small conda environment. The reference tests use only synthetic arrays.

```bash
conda env create -f environment.yml
conda activate museselect-public
pytest -q
museselect examples/candidates.json examples/frozen_decisions.json
```

The command writes a timestamped freeze record; its SHA-256 decision digest is
deterministic for a fixed target, learner, candidate set, and score vector.

Reproducing paper numbers additionally requires the official source datasets,
their permitted representations, and the sealed downstream evaluation recipes.
Those are not redistributed by this artifact. Aggregate tables are provided for
verification of reporting consistency, not as a substitute for the underlying
licensed data.

