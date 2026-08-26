#!/usr/bin/env python3
"""Fail-closed G264 package and frozen-source verifier."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


PREREG_COMMIT = "8af24ad6aa54e9f69dbe0b00601464a1077c4589"
LANDING = (
    "NEGATIVE_PHI_SIGN_ALONE_DOES_NOT_SELECT"
    "__FINITE_ARBITRARILY_DEEP_SMOOTH_ASYMPTOTICALLY_FLAT_SLICE_COMPLETE_COUNTERFAMILY_EXISTS"
    "__UNBOUNDED_NEGATIVE_ENDS_HAVE_AN_ALPHA_TWO_CURVATURE_ACCELERATION_AND_SLICE_COMPLETENESS_THRESHOLD"
    "__THE_ALPHA_TWO_CRITICAL_REPRESENTATIVE_IS_THE_G201_ZERO_TIDE_FAMILY"
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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


def verify(package: Path) -> dict[str, object]:
    repo = package.parent
    derivation = json.loads((package / "DERIVATION_RESULT.json").read_text())
    metric_first = json.loads((package / "METRIC_FIRST_VERIFICATION.json").read_text())
    independent = json.loads((package / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((package / "CATCH_PROOF_RESULT.json").read_text())
    repair_catches = json.loads((package / "REPAIR_CATCH_RESULT.json").read_text())
    packaging_catches = json.loads((package / "PACKAGING_CATCH_RESULT.json").read_text())

    if derivation["status"] != "PASS" or derivation["landing"] != LANDING:
        raise AssertionError("derivation landing")
    if derivation["classification"] != "SIGN_ONLY_NONSELECTION_WITH_GROWTH_THRESHOLDS":
        raise AssertionError("classification")
    if derivation["symbolic_check_count"] != 27:
        raise AssertionError("symbolic count")
    if metric_first["status"] != "PASS" or metric_first["case_count"] != 250:
        raise AssertionError("metric-first coverage")
    if metric_first["assertion_count"] != 1000:
        raise AssertionError("metric-first assertion count")
    if metric_first["implementation"] != (
        "standard_library_fraction_metric_first_no_sympy_no_production_import_no_result_read"
    ):
        raise AssertionError("metric-first provenance")
    required_constructed = {
        "inverse_metric",
        "inverse_metric_first_derivative",
        "christoffel",
        "christoffel_first_derivative",
        "riemann",
        "ricci",
        "scalar_curvature",
        "kretschmann_scalar",
        "radial_mixed_einstein_channel",
        "angular_mixed_einstein_channel",
    }
    if set(metric_first["constructed_objects"]) != required_constructed:
        raise AssertionError("metric-first object coverage")
    if independent["status"] != "PASS":
        raise AssertionError("consistency replay status")
    if independent["exact_assertion_count"] != 12000:
        raise AssertionError("consistency exact count")
    if independent["numeric_assertion_count"] != 6025:
        raise AssertionError("consistency numeric count")
    if independent["critical_case_count"] != 1000:
        raise AssertionError("critical consistency coverage")
    if independent["implementation"] != (
        "standard_library_fraction_and_decimal_no_production_import_no_result_read"
    ):
        raise AssertionError("consistency provenance")
    if independent["role"] != "consistency_replay_not_metric_first_derivation":
        raise AssertionError("consistency role promotion")
    if catches["status"] != "PASS" or catches["caught_count"] != 18:
        raise AssertionError("mutation catches")
    if not all(catches["mutations"].values()):
        raise AssertionError("uncaught mutation")
    if repair_catches["status"] != "PASS" or repair_catches["caught_count"] != 10:
        raise AssertionError("repair catches")
    if not all(repair_catches["mutations"].values()):
        raise AssertionError("uncaught repair mutation")
    if packaging_catches["status"] != "PASS" or packaging_catches["caught_count"] != 3:
        raise AssertionError("packaging catches")
    if not all(packaging_catches["mutations"].values()):
        raise AssertionError("uncaught packaging mutation")

    status = {row["id"]: row for row in read_tsv(package / "STATUS_LEDGER.tsv")}
    if status["S02"]["status"] != "NOT_DERIVED_COUNTERFAMILY":
        raise AssertionError("sign selection promoted")
    if status["S04"]["status"] != "DERIVED_CONDITIONAL":
        raise AssertionError("slice completeness ownership")
    if status["S09"]["status"] != "DERIVED_CONDITIONAL":
        raise AssertionError("critical intersection ownership")
    if status["S10"]["status"] != "NOT_DERIVED":
        raise AssertionError("physical mass imported")
    if status["S11"]["status"] != "OPEN":
        raise AssertionError("Xmax/history promoted")
    if status["S13"]["status"] != (
        "EXTERNAL_ACCEPT_PACKAGING_REPAIR__PRODUCTION_SYMPY_REPLAY_NOT_RERUN_EXTERNALLY"
    ):
        raise AssertionError("repair package grade")
    if status["S14"]["status"] != "PASS_1000_EXACT_ASSERTIONS":
        raise AssertionError("metric-first status")
    if status["S15"]["status"] != "CONSISTENCY_REPLAY":
        raise AssertionError("consistency role status")
    if status["S17"]["status"] != "EXTERNAL_ACCEPT_PACKAGING_REPAIR":
        raise AssertionError("packaging repair status")

    report = " ".join((package / "AUDIT_REPORT.md").read_text().split())
    if LANDING not in report.replace(" ", ""):
        raise AssertionError("landing absent from report")
    for token in (
        "sign alone rejects nothing",
        "zero-angular-tide family",
        "not a physical selection law",
        "independent dependency-free metric-first tensor derivation",
        "result-blind implementation-distinct consistency replay",
        "12,000 exact rational assertions",
        "No source, physical mass positivity",
    ):
        if token not in report:
            raise AssertionError(f"report guard absent: {token}")

    external = (package / "EXTERNAL_REVIEW_GPT54.md").read_text()
    if "Disposition: `ACCEPT_WITH_REPAIRS`" not in external:
        raise AssertionError("external disposition")
    if "bounded scientific landing survives" not in external:
        raise AssertionError("external scientific acceptance")
    if "hardcodes the target scalar formula" not in external:
        raise AssertionError("external defect missing")

    repair = " ".join((package / "REPAIR_RESULT.md").read_text().split())
    for token in (
        "constructs the inverse metric",
        "1,000/1,000 exact assertions passed",
        "consistency replay",
        "scientific landing is unchanged",
    ):
        if token not in repair:
            raise AssertionError(f"repair guard absent: {token}")

    packaging_review = (package / "EXTERNAL_PACKAGING_REPAIR_FOLLOWUP_GPT54.md").read_text()
    for token in (
        "`ACCEPT_PACKAGING_REPAIR`",
        "seven sources resolved as sealed `live_exact` files",
        "3/3 attacks caught",
        "did not contain SymPy",
        "unchanged",
    ):
        if token not in packaging_review:
            raise AssertionError(f"packaging review guard absent: {token}")

    derivation_text = (package / "EXACT_DERIVATION.md").read_text()
    for token in (
        "not a history law",
        "not as field equations",
        "conditional property",
        "does not establish that Nature selects this family",
        "relation to `X_max`",
    ):
        if token not in derivation_text:
            raise AssertionError(f"derivation guard absent: {token}")

    resolutions: dict[str, str] = {}
    for row in read_tsv(package / "SOURCE_MANIFEST.tsv"):
        resolutions[row["path"]] = resolve_frozen(repo, row["path"], row["sha256"])
    if len(resolutions) != 7:
        raise AssertionError("source count")

    return {
        "status": "PASS",
        "grade": (
            "EXTERNAL_ACCEPT_PACKAGING_REPAIR__PRODUCTION_SYMPY_REPLAY_NOT_RERUN_EXTERNALLY"
        ),
        "landing": LANDING,
        "source_count": len(resolutions),
        "source_resolutions": resolutions,
        "symbolic_checks": derivation["symbolic_check_count"],
        "metric_first_exact_assertions": metric_first["assertion_count"],
        "consistency_exact_assertions": independent["exact_assertion_count"],
        "consistency_numeric_assertions": independent["numeric_assertion_count"],
        "mutation_catches": catches["caught_count"],
        "repair_catches": repair_catches["caught_count"],
        "packaging_catches": packaging_catches["caught_count"],
        "qualification": "exact_bounded_geometry_not_independent_physical_selection",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(Path(__file__).resolve().parent)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
