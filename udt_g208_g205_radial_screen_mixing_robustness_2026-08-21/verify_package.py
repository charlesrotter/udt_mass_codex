#!/usr/bin/env python3
"""Byte-stable no-write core package replay for G208."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE / "PACKAGE_VERIFICATION_RESULT.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_json(script: str) -> dict:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["UDT_NO_WRITE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(PACKAGE / script)],
        cwd=PACKAGE,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 9
    for row in rows:
        assert len(row["sha256"]) == 64
        int(row["sha256"], 16)
        assert row["path"] and not Path(row["path"]).is_absolute()

    result_paths = (
        PACKAGE / "PRODUCTION_RESULT.json",
        PACKAGE / "INDEPENDENT_VERIFICATION.json",
        PACKAGE / "BOUNDARY_DIAGNOSTICS.json",
        PACKAGE / "CATCH_PROOF_RESULT.json",
        PACKAGE / "SOURCE_PROVENANCE_VERIFICATION.json",
    )
    before = {path.name: sha256(path) for path in result_paths}
    replay = (
        run_json("derive_radial_screen_mixing.py"),
        run_json("verify_radial_screen_mixing_independent.py"),
        run_json("run_boundary_diagnostics.py"),
        run_json("run_catch_proofs.py"),
    )
    after = {path.name: sha256(path) for path in result_paths}
    assert before == after

    saved = tuple(json.loads(path.read_text(encoding="utf-8")) for path in result_paths)
    assert replay == saved[:4]
    production, independent, diagnostics, catches, provenance = saved
    assert production["assertion_count"] == 20
    assert independent["status"] == "PASS"
    assert independent["distinct_exact_cases"] == 10_000
    assert independent["assertion_count"] == 120_004
    assert independent["production_imported"] is False
    assert diagnostics["status"] == "PASS" and diagnostics["precision_digits"] == 240
    assert diagnostics["profile_count"] == 4 and len(diagnostics["bound_checks"]) == 5
    assert catches["status"] == "PASS" and catches["catch_count"] == 23
    assert provenance["status"] == "PASS"
    assert provenance["checked_in_live_repository_context"] == 9
    assert provenance["package_replay_dependency"] is False

    report = " ".join((PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8").split())
    exact = " ".join((PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").split())
    for token in (
        "RADIAL_SCREEN_MIXING_PRESERVES_SIGNATURE_AND_AMBIENT_VOLUME_BUT_REPLACES_THE_RADIAL_CAUSAL_BOUND",
        "GROWTH_CONTROLLED_AND_BOUNDED_STATIC_CLASSES_SURVIVE",
        "A_SMOOTH_CENTER_REGULAR_UNBOUNDED_STATIC_MIXER_DESTROYS_GLOBAL_HYPERBOLICITY_AND_NULL_COMPLETENESS",
        "COMPLETED_PAIRS_HEAR_RADIAL_MIXING_BEFORE_READOUT",
        "NO_PHYSICAL_MIXER_HISTORY_OR_XMAX_SELECTION",
    ):
        assert token in report and token in exact
    for guard in (
        "not a selected UDT history",
        "does not select a mixer",
        "does not classify timelike/spacelike completeness",
    ):
        assert guard in report or guard in exact

    for name in (
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "EXTERNAL_REVIEW_RAW.md",
        "TRANSMISSION_RECORD.md",
    ):
        assert (PACKAGE / name).is_file()
    evidence = " ".join((PACKAGE / "EVIDENCE_GATES.md").read_text(encoding="utf-8").split())
    assert "PASS WITH CAVEATS" in evidence
    assert "Neither mechanizes the global analytic theorems" in evidence
    execution = " ".join(
        (PACKAGE / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8").split()
    )
    assert "three distinct evidence layers" in execution
    assert "not independently mechanized" in execution
    external = " ".join((PACKAGE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8").split())
    assert external.startswith("VERIFIED_WITH_CAVEATS")
    assert "No mathematical refutation emerged" in external
    assert "they do not change the science" in external
    transmission = " ".join((PACKAGE / "TRANSMISSION_RECORD.md").read_text(encoding="utf-8").split())
    assert "d05048c54ed43fd37bb83ee3d64decdd2881e4e827079980424a1589ab8843fb" in transmission
    assert "6e64da12ace1ec89e66775d16c56942459e00849e3d18fb2de236f86d8fe0fae" in transmission
    assert "VERIFIED_WITH_CAVEATS" in transmission and "Process exit: zero" in transmission

    result = {
        "status": "PASS",
        "provenance_manifest_rows": len(rows),
        "live_source_hash_check": "SEPARATE_REPOSITORY_CONTEXT_GATE",
        "production_assertions": production["assertion_count"],
        "independent_assertions": independent["assertion_count"],
        "independent_cases": independent["distinct_exact_cases"],
        "diagnostic_precision_digits": diagnostics["precision_digits"],
        "mutation_catches": catches["catch_count"],
        "live_source_hashes_recorded": provenance["checked_in_live_repository_context"],
        "no_write_replay": True,
        "global_theorem_evidence": "ANALYTIC_EXTERNALLY_REVIEWED_NOT_MECHANIZED",
        "external_adversarial_review": "VERIFIED_WITH_CAVEATS",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
