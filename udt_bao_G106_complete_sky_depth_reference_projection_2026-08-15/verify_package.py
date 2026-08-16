#!/usr/bin/env python3
"""Verify the bounded G106 package without observational outcomes."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "COMPLETE_SKY_DEPTH_REFERENCE_PROJECTOR_DERIVED_CONDITIONALLY"
    "__PURE_RADIAL_MODULATION_REMOVED"
    "__DEPTH_DEPENDENT_ANGULAR_RESPONSE_SURVIVES"
    "__ONE_HISTORY_CROSS_WINDOW_TEST_DEFINED"
    "__PHYSICAL_HISTORY_AND_OUTCOMES_OPEN"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def load_json(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main() -> None:
    required = {
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "SOURCE_MANIFEST_PREREG.tsv",
        "SOURCE_MANIFEST.tsv",
        "OFFICIAL_REFERENCE_SEMANTICS.md",
        "derive_sky_depth_projection.py",
        "verify_sky_depth_independent.py",
        "run_catch_proofs.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "EXACT_DERIVATION.md",
        "REFERENCE_COMPONENT_ATLAS.tsv",
        "WINDOW_WITNESS.tsv",
        "STATUS_LEDGER.tsv",
        "LAY_REPORT.md",
        "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS.md",
        "REVIEW_DISPATCH.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
    }
    missing = sorted(name for name in required if not (HERE / name).is_file())
    manifest = (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8")
    prereg_manifest = (HERE / "SOURCE_MANIFEST_PREREG.tsv").read_text(encoding="utf-8")
    rows = list(csv.DictReader(manifest.splitlines(), delimiter="\t"))
    manifest_checks = {
        row["path"]: (ROOT / row["path"]).is_file()
        and digest(ROOT / row["path"]) == row["sha256"]
        for row in rows
    }
    production = load_json("DERIVATION_RESULT.json")
    independent = load_json("INDEPENDENT_VERIFICATION.json")
    catches = load_json("CATCH_PROOF_RESULT.json")
    with (HERE / "REFERENCE_COMPONENT_ATLAS.tsv").open(encoding="utf-8", newline="") as handle:
        components = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "WINDOW_WITNESS.tsv").open(encoding="utf-8", newline="") as handle:
        windows = list(csv.DictReader(handle, delimiter="\t"))
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    official = (HERE / "OFFICIAL_REFERENCE_SEMANTICS.md").read_text(encoding="utf-8")
    external = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    executables = (
        "derive_sky_depth_projection.py",
        "verify_sky_depth_independent.py",
        "run_catch_proofs.py",
    )
    executable_text = "\n".join((HERE / name).read_text(encoding="utf-8") for name in executables)
    forbidden = {"R2_OUTCOME_REPORT.md", "R3_OUTCOME_REPORT.md", "R4_OUTCOME_REPORT.md", "R5_OUTCOME_REPORT.md", "CMB_OUTCOME"}
    checks = {
        "required_files_present": not missing,
        "manifest_frozen": manifest == prereg_manifest,
        "seven_sources": len(rows) == 7,
        "source_hashes": bool(manifest_checks) and all(manifest_checks.values()),
        "production_pass": production.get("status") == "PASS",
        "landing_exact": production.get("landing") == LANDING and LANDING in exact.replace("\n", ""),
        "production_checks": all(production.get("checks", {}).values()),
        "production_outcomes_empty": production.get("outcome_paths_read") == [],
        "independent_pass": independent.get("status") == "PASS" and all(independent.get("checks", {}).values()),
        "independent_outcomes_empty": independent.get("outcome_paths_read") == [],
        "catch_proofs_12_of_12": catches.get("status") == "PASS" and catches.get("caught_count") == catches.get("total") == 12,
        "component_classes_complete": {row["component_id"] for row in components} == {f"C{i:02d}" for i in range(1, 10)},
        "window_witness_exact": [row["mean_angular_amplitude"] for row in windows] == ["13/108", "1/108", "13/108"]
        and [row["relative_to_middle"] for row in windows] == ["169", "1", "169"],
        "official_semantics_typed": "random redshifts" in official and "p_zeta(zeta) s(n)" in official,
        "no_outcome_tokens": forbidden.isdisjoint(executable_text),
        "read_only_replay": all("UDT_READ_ONLY_REPLAY" in (HERE / name).read_text(encoding="utf-8") for name in executables),
        "ceiling_retained": "not a BAO result" in exact and "physical complete history" in exact and "remain open" in exact,
        "external_review_accepted_with_caveats": "PASS_WITH_CAVEATS" in external
        and "__ONE_HISTORY_CROSS_WINDOW_TEST_DEFINED" in external
        and "ideal per-sample/cap operator" in external
        and "not physical history selection" in external,
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "missing": missing,
        "manifest_checks": manifest_checks,
        "landing": LANDING,
    }
    if result["status"] != "PASS":
        raise AssertionError(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
