#!/usr/bin/env python3
"""No-write integrity and landing checks for G197."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LANDING = "NATIVE_CORE_RETAINED__PROVENANCE_REPAIRS_REQUIRED"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    rows = []
    for line in (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative = line.split("\t", 1)
        rows.append((expected, relative))
    assert len(rows) == 59, len(rows)
    for expected, relative in rows:
        path = ROOT / relative
        assert path.is_file(), relative
        assert digest(path) == expected, relative

    result = json.loads((PACKAGE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    assert result["status"] == "PASS"
    assert result["landing"] == LANDING
    assert result["production_files_parsed"] == 16
    assert result["repository_local_scientific_imports"] == 0
    assert result["banned_live_family_executable_names"] == 0

    report = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    gates = (PACKAGE / "EVIDENCE_GATES.md").read_text(encoding="utf-8")
    rehearsal_1 = (PACKAGE / "DRESS_REHEARSAL_1_REPORT.md").read_text(encoding="utf-8")
    rehearsal_2 = (PACKAGE / "DRESS_REHEARSAL_2_REPORT.md").read_text(encoding="utf-8")
    assert LANDING in report
    assert "112 tests with one registered xfail" in report
    assert "Two zero-context dress rehearsals | PASS" in gates
    assert "formula-level regression" in rehearsal_1
    for rejected in (
        "globally reconstructs",
        "selects physical germs and functions",
        "native signal speed",
        "establishes transfer",
        "immediate multidirectional derivation",
    ):
        assert rejected in rehearsal_2

    print(
        json.dumps(
            {
                "status": "PASS",
                "landing": LANDING,
                "manifest_sources": len(rows),
                "zero_context_rehearsals": 2,
                "failed_rehearsal_preserved": True,
                "protected_payloads_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
