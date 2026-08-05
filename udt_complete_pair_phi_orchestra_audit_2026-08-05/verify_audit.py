#!/usr/bin/env python3
"""Fail-closed verifier for the complete-pair phi/orchestra audit."""

from __future__ import annotations

import csv
import hashlib
import json
import stat
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
OUT = HERE / "VERIFICATION_RESULT.json"
BASE = "3bade43d984711de8398385d419f51db1bcb596d"
PROTECTED_PREFIX = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
PROTECTED_PATH_SHA = "e33471d5aae31d7fcac7dcd531bcf1bf7ad380976f7a6c6043582bf58691222a"
PROTECTED_META_SHA = "94305a15f705c3bd6dd2aea648ce994dabb0334e249c47d076ddb9ed1b047227"

EXPECTED_PACKAGE = {
    f"{HERE.name}/{name}"
    for name in {
        "AUDIT_REPORT.md",
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "DERIVATION_RESULT.json",
        "EXACT_DERIVATION.md",
        "EXTERNAL_ADVERSARIAL_REVIEW.md",
        "INDEPENDENT_RESULT.json",
        "PREREGISTRATION.md",
        "PRIOR_RESULT_SCOPE_CORRECTION.md",
        "REPAIR_PREREGISTRATION.md",
        "STATUS_LEDGER.tsv",
        "VERIFICATION_RESULT.json",
        "derive_complete_pair_phi.py",
        "verify_audit.py",
        "verify_complete_pair_phi_independent.py",
    }
}

SOURCES = {
    "udt_reciprocal_distance_identification_audit_2026-08-05/AUDIT_REPORT.md": "976b35943a8e862fe98f9e7c535941bf5a2313fa41313d8f00ea351471b89e42",
    "udt_reciprocal_distance_identification_audit_2026-08-05/EXACT_DERIVATION.md": "15b19b746e785fbaad0505e59189d967862f3ab72639289a17c00a1c817f0a8e",
    "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27/AUDIT_REPORT.md": "b2cb8ca000964e4a42a30f575ce3db7a2c7dfe0bedbbf45fff1e6f739ceb09e0",
    "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27/EXACT_DERIVATION.md": "d2386f376d1303cef78294ff5a154a8a5cb3b33942e783342b13a237225b4135",
    "udt_complete_relational_configuration_variation_domain_audit_2026-07-26/EXACT_ARCHITECTURE.md": "7e95b3867fcabeb4be148d8abce6ee05c7068ca0a0e652a2309eab0c5ee720d6",
    "udt_factorized_whole_spacetime_skeleton_2026-08-04/AUDIT_REPORT.md": "8a56d5ca8a73069e17eaa69fac5c134bddf07e8db9ab37af40787de06f89761b",
    "udt_native_global_coframe_definition_audit_2026-07-28/AUDIT_REPORT.md": "7aa0b81caa6504974e8ace4fc2c313a9e8394ad293b3d7c316412ca7ec6485f1",
    "udt_intrinsic_clock_transverse_solder_audit_2026-07-24/AUDIT_REPORT.md": "67cc72d71fa5b5b09824ae2a3d2397730e78983cbd7d1060f9afa2e9185cb24b",
    "udt_reciprocal_plane_projector_audit_2026-07-21/AUDIT_REPORT.md": "8833d53428a9e23b4e6f50df81d20ff1b99a35c28612b780a6c1da649d361295",
}

LIVE_SOURCES = {
    "CURRENT_SCIENTIFIC_PREMISES.tsv": {
        "0fa377cb50b775875dd8f2de95acb840f3d38183c71b54caef242a89cfc1fa13",
        "2da7b708495e4ef20f8833edbcb939d61c3ae8d0736bc916d9cfe4e5bf0eb5be",
    },
}


class GateError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_json(script: str) -> dict[str, object]:
    proc = subprocess.run(
        ["python3", str(HERE / script)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    )
    return json.loads(proc.stdout)


def validate_sources() -> dict[str, str]:
    actual = {path: sha((ROOT / path).read_bytes()) for path in SOURCES}
    require(actual == SOURCES, "SOURCE_HASH_DRIFT")
    live_actual = {path: sha((ROOT / path).read_bytes()) for path in LIVE_SOURCES}
    for path, digest in live_actual.items():
        require(digest in LIVE_SOURCES[path], f"LIVE_SOURCE_HASH_DRIFT:{path}")
    return {**actual, **live_actual}


def validate_computation() -> dict[str, object]:
    primary = run_json("derive_complete_pair_phi.py")
    independent = run_json("verify_complete_pair_phi_independent.py")
    require(primary["status"] == "PASS" and primary["check_count"] == 32, "PRIMARY_COUNT")
    require(all(primary["checks"].values()), "PRIMARY_FALSE_CHECK")
    require(independent["status"] == "PASS" and independent["check_count"] == 44, "INDEPENDENT_COUNT")
    require(all(independent["checks"].values()), "INDEPENDENT_FALSE_CHECK")
    require(primary["mixing_control"]["depths_are_distinct"] is True, "MIXING_DISTINCTION")
    require(primary["complete_magnitudes"]["agree_only_on_pure_reciprocal_control"] is True, "MAGNITUDE_NONUNIQUENESS")
    return {"primary_checks": 32, "independent_checks": 44, "sympy": primary["sympy_version"]}


def load_ledger() -> list[dict[str, str]]:
    with (HERE / "STATUS_LEDGER.tsv").open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_semantics() -> dict[str, object]:
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    correction = (HERE / "PRIOR_RESULT_SCOPE_CORRECTION.md").read_text(encoding="utf-8")
    review = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    repair = (HERE / "REPAIR_PREREGISTRATION.md").read_text(encoding="utf-8")
    rows = load_ledger()
    require(len(rows) == 19, f"LEDGER_COUNT:{len(rows)}")
    require(len({row["object"] for row in rows}) == 19, "DUPLICATE_LEDGER_OBJECT")
    by_object = {row["object"]: row for row in rows}
    expected = {
        "complete_arrow_metric_strain": "DERIVED_FRAME_COVARIANT",
        "regular_complete_timelike_extractor": "DERIVED_ON_POSITIVE_REAL_UNIQUE_TIMELIKE_EIGENLINE_STRATUM",
        "mixing_modulation_single_pair": "DERIVED_EXACT_WITNESS",
        "strain_vs_quotient_identification": "OPEN_NONUNIQUE",
        "spectral_norm_as_reciprocal_depth": "REFUTED_FOR_GENERIC_COMPOSITION",
        "signed_depth_mathematical_home": "DERIVED_STRUCTURAL_TYPE",
        "stationary_screen_modulated_family": "DERIVED_CONDITIONAL_EXACT",
        "angular_orchestra_framing": "CONSTRUCTIVELY_VIABLE_NOT_SELECTED",
        "prior_equal_phi_angular_counterexample": "NARROWED_SCOPE",
        "complete_pair_phi_rule": "OPEN_SHARPENED_TARGET",
    }
    for key, status in expected.items():
        require(by_object[key]["status"] == status, f"STATUS:{key}")
    for token in [
        "C_A       = A^dagger A",
        "delta_t(A)=-(1/2) log(lambda_t(A))",
        "delta_quotient=log 2",
        "approximately 0.6481668896",
        "rho_2=sqrt(3/2)",
        "real-valued `1`-cocycle on the observer/path comparison groupoid",
        "delta_a(p,q)",
        "The active premises\ndo not select `a`",
    ]:
        require(token in exact, f"EXACT_TOKEN:{token}")
    require("can change this depth for one A-to-B comparison" in report, "ORCHESTRA_POSITIVE")
    require("Generic complete strain norms fail that\ntest" in report, "COMPOSITION_SCOPE")
    require("EXTERNAL REVIEW ACCEPTED AFTER PREMISE-DISCLOSURE REPAIR" in report, "EXTERNAL_REVIEW_CLOSED")
    require("ACCEPTED_WITH_REPAIRS" in review, "EXTERNAL_VERDICT")
    require("stationary-family ownership wording" in repair, "REPAIR_PREREGISTRATION")
    for premise in [
        "supplying an intrinsic Killing line",
        "screen split",
        "fixed endpoint screen identification",
        "convention relating `R` to screen",
    ]:
        require(premise in report, f"REPORT_STATIONARY_PREMISE:{premise}")
    stationary_scope = by_object["stationary_screen_modulated_family"]["exact_scope"]
    for premise in [
        "supplied Killing line",
        "supplied screen split",
        "fixed endpoint screen identification",
        "R-to-screen-area convention",
    ]:
        require(premise in stationary_scope, f"LEDGER_STATIONARY_PREMISE:{premise}")
    require("the complete metric supplies the exact family" not in report, "METRIC_ALONE_OVERCLAIM")
    require("does **not** establish" in correction, "PRIOR_SCOPE_NARROWED")
    require("full relational pair depth phi_AB" in correction, "RELATIONAL_PHI_PRESERVED")
    require("No action, source, carrier, boundary, bootstrap return, matter, mass, dynamics, signal law, or\nobservational prediction was derived" in report, "DOWNSTREAM_BOUNDARY")
    return {"ledger_rows": len(rows), "guarded_statuses": len(expected)}


def check_scope(tracked: set[str], untracked: set[str]) -> dict[str, object]:
    package_untracked = {path for path in untracked if path.startswith(HERE.name + "/")}
    protected = {path for path in untracked if path.startswith(PROTECTED_PREFIX)}
    unexpected = untracked - package_untracked - protected
    require(not unexpected, f"UNEXPECTED_UNTRACKED:{sorted(unexpected)}")
    observed = tracked | package_untracked
    require(observed == EXPECTED_PACKAGE, f"PACKAGE_SET:{sorted(observed ^ EXPECTED_PACKAGE)}")
    protected_paths = sorted(protected)
    require(len(protected_paths) == 83, f"PROTECTED_COUNT:{len(protected_paths)}")
    require(sha(("\n".join(protected_paths) + "\n").encode()) == PROTECTED_PATH_SHA, "PROTECTED_PATH_SHA")
    return {"observed": sorted(observed), "protected": protected_paths, "package_untracked": sorted(package_untracked)}


def validate_scope() -> dict[str, object]:
    tracked = set(subprocess.check_output(["git", "ls-files", HERE.name], cwd=ROOT, text=True).splitlines())
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-uall"], cwd=ROOT, text=True).splitlines()
    untracked = {line[3:] for line in raw if line.startswith("?? ")}
    scope = check_scope(tracked, untracked)
    metadata = []
    for path in scope["protected"]:
        info = (ROOT / path).stat()
        metadata.append(f"{path}\t{info.st_size}\t{info.st_mtime_ns}\t{stat.S_IMODE(info.st_mode):04o}")
    actual_meta = sha(("\n".join(metadata) + "\n").encode())
    require(actual_meta == PROTECTED_META_SHA, "PROTECTED_METADATA_SHA")
    return {
        "package_paths": len(scope["observed"]),
        "package_untracked": scope["package_untracked"],
        "protected_paths": len(scope["protected"]),
        "protected_metadata_sha256": actual_meta,
    }


def caught(label: str, fn) -> str:
    try:
        fn()
    except GateError:
        return "CAUGHT"
    raise GateError(f"CATCH_FAILED:{label}")


def catch_proofs() -> dict[str, str]:
    primary = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    rows = load_ledger()
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    correction = (HERE / "PRIOR_RESULT_SCOPE_CORRECTION.md").read_text(encoding="utf-8")
    review = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    tracked = set(subprocess.check_output(["git", "ls-files", HERE.name], cwd=ROOT, text=True).splitlines())
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-uall"], cwd=ROOT, text=True).splitlines()
    untracked = {line[3:] for line in raw if line.startswith("?? ")}

    def check_primary(record):
        require(record["mixing_control"]["depths_are_distinct"] is True, "MIXING_ERASED")
        require(record["complete_magnitudes"]["agree_only_on_pure_reciprocal_control"] is True, "MAGNITUDES_COLLAPSED")

    def check_rows(candidate_rows):
        by_object = {row["object"]: row for row in candidate_rows}
        require(by_object["angular_orchestra_framing"]["status"] == "CONSTRUCTIVELY_VIABLE_NOT_SELECTED", "ORCHESTRA_PROMOTED")
        require(by_object["complete_pair_phi_rule"]["status"] == "OPEN_SHARPENED_TARGET", "UNIQUE_RULE_INVENTED")
        require(by_object["spectral_norm_as_reciprocal_depth"]["status"] == "REFUTED_FOR_GENERIC_COMPOSITION", "NONADDITIVITY_DROPPED")

    mutated = json.loads(json.dumps(primary))
    mutated["mixing_control"]["depths_are_distinct"] = False
    promoted = [row.copy() for row in rows]
    next(row for row in promoted if row["object"] == "complete_pair_phi_rule")["status"] = "DERIVED_UNIQUE"
    additive = [row.copy() for row in rows]
    next(row for row in additive if row["object"] == "spectral_norm_as_reciprocal_depth")["status"] = "DERIVED_ADDITIVE"
    first_source = next(iter(SOURCES))
    return {
        "mixing_modulation_removal_rejected": caught("mixing", lambda: check_primary(mutated)),
        "unique_rule_promotion_rejected": caught("unique", lambda: check_rows(promoted)),
        "spectral_additivity_promotion_rejected": caught("additive", lambda: check_rows(additive)),
        "prior_counterexample_rebroadened_rejected": caught(
            "scope", lambda: require("does **not** establish" in correction.replace("does **not** establish", "establishes"), "PRIOR_SCOPE")
        ),
        "stationary_metric_alone_promotion_rejected": caught(
            "metric_alone",
            lambda: require(
                "the complete metric supplies the exact family"
                not in report.replace(
                    "after supplying an intrinsic Killing line, a\nscreen split, a fixed endpoint screen identification, and the convention relating `R` to screen\narea, the exact family is",
                    "the complete metric supplies the exact family",
                ),
                "METRIC_ALONE",
            ),
        ),
        "external_verdict_removal_rejected": caught(
            "external", lambda: require("ACCEPTED_WITH_REPAIRS" in review.replace("ACCEPTED_WITH_REPAIRS", "PENDING"), "EXTERNAL_VERDICT")
        ),
        "frozen_source_mutation_rejected": caught(
            "source", lambda: require(sha((ROOT / first_source).read_bytes() + b"x") == SOURCES[first_source], "SOURCE_MUTATION")
        ),
        "extra_untracked_path_rejected": caught(
            "untracked", lambda: check_scope(tracked, untracked | {"outside_orchestra_audit_synthetic.txt"})
        ),
    }


def main() -> None:
    result = {
        "status": "PASS",
        "sources": validate_sources(),
        "computations": validate_computation(),
        "semantics": validate_semantics(),
        "scope": validate_scope(),
        "catch_proofs": catch_proofs(),
        "maximum_conclusion": (
            "DERIVED_COMPLETE_ARROW_ORCHESTRA_MODULATION_AND_GROUPOID_COCYCLE_HOME__"
            "UNIQUE_PHYSICAL_COMPLETE_PAIR_PHI_OPEN"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
