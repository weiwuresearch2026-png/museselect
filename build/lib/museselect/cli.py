"""Small command-line demonstration of the public selection interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .boundary import SelectionView
from .selection import freeze_predictions, route_by_centroid


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--target", default="synthetic_target")
    parser.add_argument("--learner", default="fixed_logistic_recipe")
    args = parser.parse_args()

    rows = json.loads(args.candidates.read_text(encoding="utf-8"))
    view = SelectionView.build(args.target, args.learner, rows)
    record = freeze_predictions(view, route_by_centroid(view))
    args.output.write_text(
        json.dumps(record.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"frozen {record.selected_candidate_id} ({record.selection_digest[:12]})")


if __name__ == "__main__":
    main()

