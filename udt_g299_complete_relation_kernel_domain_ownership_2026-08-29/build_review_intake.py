#!/usr/bin/env python3
"""Build a sealed, self-contained G299 read-only review intake under /tmp."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g299_review_", dir="/tmp"))
    package_dst = intake / PACKAGE.name
    shutil.copytree(PACKAGE, package_dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    source_paths = []
    for line in (PACKAGE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
        expected, relative = line.split("\t")
        source = REPO / relative
        assert sha(source) == expected
        destination = intake / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        source_paths.append(relative)

    scope = {
        "package": PACKAGE.name,
        "review": "fresh read-only adversarial scientific premise-ownership and evidence review",
        "allowed": [
            "inspect only this sealed intake",
            "run registered checks in a writable ephemeral copy",
            "rederive active-screen and right-carry separators from frozen sources",
        ],
        "forbidden": [
            "edit evidence files or continue the research",
            "access repository or protected packages",
            "use internet or unsealed observational outcomes",
            "import selector field equation history source matter action fit scale distance law or X_max",
        ],
        "frozen_sources": source_paths,
        "scientific_landing_under_review": (
            "W5_OWNS_COMPLETE_PATH_LABELLED_RELATION_AS_PHYSICAL_NORMALIZED_PAIR_POSITION"
            "__RANK_TWO_GERMS_ARE_TYPED_QUERY_PROJECTIONS__NO_UNIQUE_G2_TRANSFER_IS_REQUIRED"
        ),
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2) + "\n")

    payloads = sorted(
        path for path in intake.rglob("*")
        if path.is_file() and path.name not in {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}
    )
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    rows = ["sha256\tpath"]
    rows.extend(f"{sha(path)}\t{path.relative_to(intake)}" for path in payloads)
    manifest_path.write_text("\n".join(rows) + "\n")
    manifest_sha = sha(manifest_path)
    seal_path = intake / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{manifest_sha}  REVIEW_MANIFEST.tsv\n")

    print(json.dumps({
        "intake": str(intake),
        "manifest_payloads": len(payloads),
        "total_files": len(payloads) + 2,
        "scope_sha256": sha(scope_path),
        "manifest_sha256": manifest_sha,
        "detached_seal_sha256": sha(seal_path),
    }, indent=2))


if __name__ == "__main__":
    main()
