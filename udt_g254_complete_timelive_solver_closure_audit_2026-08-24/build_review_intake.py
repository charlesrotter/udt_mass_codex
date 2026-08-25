#!/usr/bin/env python3
"""Build a sealed G254 package-plus-exact-sources review intake."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    output = arguments.output.resolve()
    assert not output.exists(), output
    output.mkdir(parents=True)

    package_target = output / PACKAGE.name
    shutil.copytree(PACKAGE, package_target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    for row in sources:
        source = ROOT / row["path"]
        assert sha256(source) == row["sha256"]
        destination = output / row["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    payloads = []
    for path in sorted(item for item in output.rglob("*") if item.is_file()):
        relative = path.relative_to(output).as_posix()
        payloads.append({"path": relative, "sha256": sha256(path)})
    scope = {
        "purpose": "fresh read-only adversarial review of the bounded G254 closure landing",
        "allowed": "inspect only this intake; run bounded checks in an ephemeral copy",
        "forbidden": "edit evidence files; continue research; access repository or protected packages",
        "package": PACKAGE.name,
        "scientific_source_count": len(sources),
        "payload_file_count_excluding_scope": len(payloads),
        "payloads": payloads,
    }
    (output / "REVIEW_SCOPE.json").write_text(
        json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": "INTAKE_BUILT",
        "path": str(output),
        "file_count_including_scope": len(payloads) + 1,
        "review_scope_sha256": sha256(output / "REVIEW_SCOPE.json"),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
