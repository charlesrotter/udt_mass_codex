#!/usr/bin/env python3
"""Build the non-self-referential manifest for the G69 review/adjudication layer."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PATHS = [
    HERE / "EXTERNAL_REVIEW_ADJUDICATION_PREREGISTRATION.md",
    HERE / "EXTERNAL_REVIEW_RAW.md",
    HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt",
    HERE / "EXTERNAL_REVIEW_ADJUDICATION.md",
    HERE / "verify_postreview.py",
    HERE / "POSTREVIEW_VERIFICATION_RESULT.json",
    HERE / "run_postreview_repository_gates.py",
    HERE / "POSTREVIEW_REPOSITORY_GATES.json",
    HERE / "build_postreview_manifest.py",
    ROOT / "LIVE.md",
    ROOT / "HANDOFF.md",
    ROOT / "README.md",
    ROOT / "INDEX.md",
    ROOT / "CURRENT_RESEARCH_PROGRAM.md",
    ROOT / "CURRENT_SCIENTIFIC_PREMISES.md",
    ROOT / "MEMORY.md",
    ROOT / "INFLIGHT_STATE.md",
    ROOT / "research/README.md",
    ROOT / "research/_registry/README.md",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    lines = ["path\tsha256\trole"]
    for path in PATHS:
        role = "G69_REVIEW_LAYER" if HERE in path.parents else "CURRENT_NAVIGATION"
        lines.append(f"{path.relative_to(ROOT)}\t{digest(path)}\t{role}")
    (HERE / "POSTREVIEW_MANIFEST.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
