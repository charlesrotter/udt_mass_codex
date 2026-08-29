#!/usr/bin/env python3
"""Build a sealed, self-contained G298 read-only review intake under /tmp."""

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g298_review_", dir="/tmp"))
    package_dst = intake / PACKAGE.name
    shutil.copytree(PACKAGE, package_dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    source_paths = []
    for line in (PACKAGE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
        digest, rel = line.split("\t")
        src = REPO / rel
        assert sha(src) == digest
        dst = intake / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        source_paths.append(rel)

    scope = {
        "package": PACKAGE.name,
        "review": "fresh read-only adversarial scientific and evidence review",
        "allowed": [
            "inspect only this sealed intake",
            "run registered no-write replays or bounded checks in a writable ephemeral copy",
            "rederive the pair-one-jet transfer and active-screen separator",
        ],
        "forbidden": [
            "edit evidence files",
            "continue the research",
            "access repository or protected packages",
            "use internet or unsealed observations",
            "import action source matter fit scale X_max history or field equation",
        ],
        "frozen_sources": source_paths,
        "scientific_landing_under_review": "MULTIPLE_INEQUIVALENT_NATURAL_COMPLETE_ONE_JET_TRANSFERS_SURVIVE__NO_UNIQUE_TRANSFER",
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2) + "\n")

    payloads = sorted(
        p for p in intake.rglob("*")
        if p.is_file() and p.name not in {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}
    )
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    rows = ["sha256\tpath"]
    for path in payloads:
        rows.append(f"{sha(path)}\t{path.relative_to(intake)}")
    manifest_path.write_text("\n".join(rows) + "\n")
    manifest_digest = sha(manifest_path)
    seal_path = intake / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{manifest_digest}  REVIEW_MANIFEST.tsv\n")

    result = {
        "intake": str(intake),
        "manifest_payloads": len(payloads),
        "total_files": len(payloads) + 2,
        "scope_sha256": sha(scope_path),
        "manifest_sha256": manifest_digest,
        "detached_seal_sha256": sha(seal_path),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
