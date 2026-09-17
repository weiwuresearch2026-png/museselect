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

The public package also exposes the exact LEEP and fixed-point LogME scoring
equations used after candidate heads have been fitted. Candidate fitting is
deliberately outside the public interface, so these functions do not imply that
the probes are training free. The staged workflow first averages centroid
distance at source level, then ranks buckets only inside the routed source.
The paper's final workflow result comes from a fresh repartition prefix whose
route, adapted LEEP ranking, shortlist sizes, fallback, and success criterion
were frozen before its utility artifact was generated. The public repository
reports aggregate results; the anonymous review supplement carries the full
pipeline and chronological artifact audit.

Reproducing paper numbers additionally requires the official source datasets,
their permitted representations, and the sealed downstream evaluation recipes.
Those are not redistributed by this artifact. Aggregate tables are provided for
verification of reporting consistency, not as a substitute for the underlying
licensed data.

The aggregate mechanism and shortlist summaries in `results/` can be checked
against the manuscript without opening raw data or per-example outcomes.
