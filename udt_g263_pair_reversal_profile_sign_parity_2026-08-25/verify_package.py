#!/usr/bin/env python3
"""Fail-closed G263 package and frozen-source verifier."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


PREREG_COMMIT = "43cf54d3"
LANDING = (
    "PAIR_ARROW_REVERSAL_IS_EXACT_RECIPROCAL_INVOLUTION"
    "__WHOLE_PROFILE_SIGN_CONJUGATION_IS_A_DISTINCT_METRIC_INVOLUTION"
    "__SCALAR_DEPTH_INVERSION_SHARED_BUT_COMPLETE_CHANNEL_PARITIES_MIXED"
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def resolve_frozen(repo: Path, relative: str, expected: str) -> str:
    live = repo / relative
    if live.is_file() and digest(live.read_bytes()) == expected:
        return "live_exact"
    try:
        frozen = subprocess.check_output(
            ["git", "show", f"{PREREG_COMMIT}:{relative}"],
            cwd=repo,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as exc:
        raise AssertionError(f"cannot resolve frozen source: {relative}") from exc
    if digest(frozen) != expected:
        raise AssertionError(f"frozen source mismatch: {relative}")
    return "git_object_exact"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify(package: Path, require_repair_catch: bool = True) -> dict[str, object]:
    repo = package.parent
    derivation = json.loads((package / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((package / "INDEPENDENT_VERIFICATION.json").read_text())
    sealed = json.loads((package / "SEALED_REPLAY_RESULT.json").read_text())
    catches = json.loads((package / "CATCH_PROOF_RESULT.json").read_text())
    repair_catches = None
    if require_repair_catch:
        repair_catches = json.loads((package / "REPAIR_CATCH_RESULT.json").read_text())
    if derivation["status"] != "PASS" or derivation["landing"] != LANDING:
        raise AssertionError("derivation landing")
    if derivation["classification"] != "SCALAR_EQUIVALENCE_ONLY":
        raise AssertionError("operation classification")
    if derivation["symbolic_check_count"] != 31:
        raise AssertionError("symbolic count")
    if independent["status"] != "PASS" or independent["assertion_count"] != 29000:
        raise AssertionError("independent verification")
    if independent["case_count"] != 1000 or "no_production_import" not in independent["implementation"]:
        raise AssertionError("independent provenance")
    if sealed["status"] != "PASS" or sealed["assertion_count"] != 38010:
        raise AssertionError("dependency-free sealed replay")
    if sealed["case_count"] != 1000:
        raise AssertionError("sealed case count")
    if sealed["implementation"] != "standard_library_fraction_no_sympy_no_production_import_no_result_read":
        raise AssertionError("sealed replay provenance")
    if sealed["signed_profile_cases"] != {
        "negative_phi": 421,
        "positive_phi": 526,
        "zero_phi": 53,
    }:
        raise AssertionError("sealed signed coverage")
    if sealed["shared_scalar_inversion_cases"] != 1000:
        raise AssertionError("sealed scalar inversion coverage")
    if sealed["areal_sphere_guard_cases"] != 1000:
        raise AssertionError("sealed sphere guard coverage")
    if sealed["nonquiet_conjugate_zero_tide_cases"] != 577:
        raise AssertionError("sealed zero-tide separator coverage")
    if sealed["constant_jet_limit_qualification"] != (
        "elementary_limits_of_N_1_over_s_mu_half_1_minus_1_over_s2_"
        "Aparallel_0_Aperp_1_minus_1_over_s2"
    ):
        raise AssertionError("sealed constant-jet qualification")
    if sealed["qualification"] != "dependency_free_exact_algebra_not_epistemically_independent_physical_derivation":
        raise AssertionError("sealed independence qualification")
    if catches["status"] != "PASS" or catches["caught_count"] != 17:
        raise AssertionError("mutation catches")
    if not all(catches["mutations"].values()):
        raise AssertionError("uncaught mutation")
    if require_repair_catch:
        if repair_catches is None or repair_catches["status"] != "PASS" or repair_catches["caught_count"] != 7:
            raise AssertionError("altered-copy repair catches")
        if not all(repair_catches["caught"].values()):
            raise AssertionError("uncaught altered-copy repair mutation")

    status = {row["id"]: row for row in read_tsv(package / "STATUS_LEDGER.tsv")}
    if status["S04"]["status"] != "MATHEMATICAL_DIAGNOSTIC":
        raise AssertionError("profile conjugation promoted")
    if status["S07"]["guard"] != "not physical mass":
        raise AssertionError("mass aspect promoted")
    if status["S10"]["status"] != "NOT_DERIVED":
        raise AssertionError("universal angular loudness promoted")
    if status["S11"]["status"] != "OPEN":
        raise AssertionError("open physics promoted")
    if status["S12"]["status"] != "PROVISIONAL_REPAIRED_PENDING_EXTERNAL_FOLLOWUP":
        raise AssertionError("premature grade")

    report = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    normalized_report = " ".join(report.split())
    if LANDING not in report.replace("\n", ""):
        raise AssertionError("report landing absent")
    for token in (
        "did not exclude negative `phi`",
        "not the same full geometric operation",
        "not physical mass",
        "No universal angular loudness",
        "38,010",
        "17/17",
        "repair-only follow-up",
    ):
        if token not in normalized_report:
            raise AssertionError(f"report guard absent: {token}")

    resolutions: dict[str, str] = {}
    for row in read_tsv(package / "SOURCE_MANIFEST.tsv"):
        resolutions[row["path"]] = resolve_frozen(repo, row["path"], row["sha256"])
    if len(resolutions) != 10:
        raise AssertionError("source count")

    return {
        "status": "PASS",
        "grade": "PROVISIONAL_REPAIRED_PENDING_EXTERNAL_FOLLOWUP",
        "landing": LANDING,
        "source_count": len(resolutions),
        "source_resolutions": resolutions,
        "symbolic_checks": derivation["symbolic_check_count"],
        "independent_assertions": independent["assertion_count"],
        "sealed_replay_assertions": sealed["assertion_count"],
        "mutation_catches": catches["caught_count"],
        "qualification": "exact_algebra_and_package_consistency_not_independent_physical_derivation",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(Path(__file__).resolve().parent)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
