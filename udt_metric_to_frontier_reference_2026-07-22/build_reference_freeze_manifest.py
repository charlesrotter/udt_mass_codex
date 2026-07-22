#!/usr/bin/env python3
"""Build the immutable input manifest for the cold reference reviews."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "REFERENCE_FREEZE_MANIFEST.tsv"
INPUTS = (
    "PREREGISTRATION.md",
    "REFERENCE.md",
    "CLAIM_DEPENDENCY_LEDGER.tsv",
    "OPEN_JOIN_LEDGER.tsv",
    "SOURCE_MANIFEST.tsv",
    "EXTERNAL_REVIEW_PACKET.md",
    "README.md",
    "verify_reference_packet.py",
    "CATCH_PROOFS.tsv",
    "VERIFICATION_RESULT.json",
    "INTERNAL_VERIFIER_TRANSCRIPT.txt",
    "build_reference_freeze_manifest.py",
    "verify_repository_gates.py",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    missing = [name for name in INPUTS if not (HERE / name).is_file()]
    if missing:
        raise SystemExit(f"missing freeze inputs: {missing}")
    lines = ["path\tsha256\tsize_bytes"]
    for name in INPUTS:
        path = HERE / name
        lines.append(f"{name}\t{digest(path)}\t{path.stat().st_size}")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"reference_freeze_inputs={len(INPUTS)}")
    print(f"reference_freeze_manifest_sha256={digest(OUTPUT)}")


if __name__ == "__main__":
    main()
