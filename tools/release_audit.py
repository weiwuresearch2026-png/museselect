#!/usr/bin/env python3
"""Audit the curated public artifact for leaks and reporting drift."""

from __future__ import annotations

import argparse
import csv
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".css", ".csv", ".html", ".js", ".json", ".jsonl", ".md", ".py",
    ".toml", ".txt", ".yml", ".yaml",
}
FORBIDDEN_PATTERNS = {
    "local user path": re.compile(r"/Users/|[A-Za-z]:\\\\Users\\\\"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "generic API token assignment": re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"][^'\"]{12,}"
    ),
    "Hugging Face token": re.compile(r"hf_[A-Za-z0-9]{20,}"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
}
BLOCKERS = {
    "LICENSE-TO-CHOOSE.txt": "software/data license is not selected",
    "website/config.js": "required GitHub or website URL is empty",
}


def text_files() -> list[Path]:
    return [
        path for path in ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
        and ".git" not in path.parts
    ]


def audit_secrets() -> list[str]:
    failures: list[str] = []
    for path in text_files():
        if path.resolve() == Path(__file__).resolve():
            continue
        content = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(content):
                failures.append(f"{path.relative_to(ROOT)}: {label}")
    return failures


def audit_results() -> list[str]:
    expected = {
        ("Logistic regression", "Positive-utility classifier"): (0.00178, 97.8),
        ("GaussianNB", "Positive-utility classifier"): (-0.03734, 66.7),
        ("Neural MLP", "Positive-utility classifier"): (0.00755, 80.0),
        ("Gated fusion", "Positive-utility classifier"): (-0.00027, 53.3),
    }
    path = ROOT / "huggingface/data/paper_results.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    found = {
        (row["learner"], row["rule"]):
        (float(row["mean_utility"]), float(row["route_accuracy_percent"]))
        for row in rows
    }
    failures = []
    for key, values in expected.items():
        if found.get(key) != values:
            failures.append(f"paper result mismatch for {key}: {found.get(key)} != {values}")
    return failures


def audit_scope() -> list[str]:
    forbidden_suffixes = {".mp3", ".mp4", ".wav", ".pkl", ".pt", ".ckpt", ".npz"}
    failures = []
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in forbidden_suffixes:
            failures.append(f"forbidden public binary: {path.relative_to(ROOT)}")
    for required_license in (ROOT / "LICENSE", ROOT / "huggingface/LICENSE-DATA"):
        if not required_license.exists():
            failures.append(f"missing license file: {required_license.relative_to(ROOT)}")
    return failures


class _AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        key = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else None
        if key and attributes.get(key):
            self.targets.append(str(attributes[key]))


def audit_website() -> list[str]:
    failures: list[str] = []
    website = ROOT / "website"
    index = website / "index.html"
    content = index.read_text(encoding="utf-8")
    required_claims = ["44 / 45", "97.8%", "+0.00105", "53.3–80.0%"]
    for claim in required_claims:
        if claim not in content:
            failures.append(f"website missing synchronized claim: {claim}")
    for html_path in website.glob("*.html"):
        parser = _AssetParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        for target in parser.targets:
            parsed = urlparse(target)
            if parsed.scheme or target.startswith(("#", "mailto:")):
                continue
            local_target = (html_path.parent / parsed.path).resolve()
            if not local_target.exists():
                failures.append(
                    f"broken local website link in {html_path.name}: {target}"
                )
    return failures


def audit_huggingface() -> list[str]:
    failures: list[str] = []
    data_dir = ROOT / "huggingface/data"
    with (data_dir / "corpus_registry.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["redistributed_here"].lower() != "false":
                failures.append(f"corpus unexpectedly marked for redistribution: {row['corpus']}")
    for line_number, line in enumerate(
        (data_dir / "synthetic_candidates.jsonl").read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue
        if '"synthetic":true' not in line.replace(" ", ""):
            failures.append(f"synthetic row {line_number} lacks synthetic=true")
    return failures


def publication_blockers() -> list[str]:
    failures = []
    if (ROOT / "LICENSE-TO-CHOOSE.txt").exists():
        failures.append(BLOCKERS["LICENSE-TO-CHOOSE.txt"])
    config = (ROOT / "website/config.js").read_text(encoding="utf-8")
    if 'codeUrl: ""' in config or 'websiteUrl: ""' in config:
        failures.append(BLOCKERS["website/config.js"])
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-publication-blockers", action="store_true")
    args = parser.parse_args()
    failures = (
        audit_secrets()
        + audit_results()
        + audit_scope()
        + audit_website()
        + audit_huggingface()
    )
    blockers = publication_blockers()
    if blockers and not args.allow_publication_blockers:
        failures.extend("publication blocker: " + item for item in blockers)
    if failures:
        raise SystemExit("PUBLIC RELEASE AUDIT FAILED\n- " + "\n- ".join(failures))
    suffix = f" ({len(blockers)} acknowledged publication blockers)" if blockers else ""
    print(f"Public release audit passed{suffix}.")


if __name__ == "__main__":
    main()
