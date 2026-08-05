#!/usr/bin/env python3
"""Fail-closed verifier for the reciprocal distance-identification audit."""

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
BASE = "01111d9fc32f8a2083af54d6d5bd3be2225965ea"
PREFIX = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
PATH_SHA = "e33471d5aae31d7fcac7dcd531bcf1bf7ad380976f7a6c6043582bf58691222a"
META_SHA = "94305a15f705c3bd6dd2aea648ce994dabb0334e249c47d076ddb9ed1b047227"
EXPECTED_PACKAGE_FILES = {
    f"{HERE.name}/{name}"
    for name in {
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "DERIVATION_RESULT.json",
        "EXACT_DERIVATION.md",
        "EXTERNAL_ADVERSARIAL_REVIEW.md",
        "INDEPENDENT_RESULT.json",
        "PREREGISTRATION.md",
        "REPAIR_PREREGISTRATION.md",
        "STATUS_LEDGER.tsv",
        "VERIFICATION_RESULT.json",
        "derive_reciprocal_distance.py",
        "verify_audit.py",
        "verify_reciprocal_distance_independent.py",
    }
}

SOURCES = {
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md": "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
    "udt_founding_phi_ownership_morphism_audit_2026-08-05/AUDIT_REPORT.md": "65905b6b2718fd9c1057143a7148104bb14d7e65eeee3bdc7a7010af8cbe90eb",
    "udt_founding_phi_ownership_morphism_audit_2026-08-05/EXACT_DERIVATION.md": "0d83baaaa9f0586cb3f3b0cd7af16b201996a124dba6a050c71624a2e638a4fd",
    "udt_founding_phi_ownership_morphism_audit_2026-08-05/STATUS_LEDGER.tsv": "b9e2912487cfc5c22e192aaacd580885c9dd52ce70a82720d0cfcf367b6cc32b",
    "udt_observer_pair_clock_operator_audit_2026-07-24/EXACT_DERIVATION.md": "7e03ef2631908a1e26c636bb9beb7410bdc534c9fde1e15d37eb9de5efadf29d",
    "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27/AUDIT_REPORT.md": "b2cb8ca000964e4a42a30f575ce3db7a2c7dfe0bedbbf45fff1e6f739ceb09e0",
    "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27/EXACT_DERIVATION.md": "d2386f376d1303cef78294ff5a154a8a5cb3b33942e783342b13a237225b4135",
    "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27/STATUS_LEDGER.tsv": "437187d97362adfae16139d4e7fbaba2fc6d70d0ba161a9d492206ff3bbfc3fa",
    "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/AUDIT_REPORT.md": "7296d4fc3e9a44510f05c0a61a5dce498f894e0d9bf6b9bb6f8e947ef1983398",
    "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/EXACT_DERIVATION.md": "8e3de52c571b953ca878c6459235ff1487fb4d16029a33e7cb279cead980170b",
    "udt_global_phi_ownership_overlap_audit_2026-08-05/AUDIT_REPORT.md": "bbf8e91b5f6c594bd12f6c407bca2b9be4fdb3232cbe5c817d814effe863a79f",
    "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md": "8860dbefd6e99f4f9de966497f56022b268d2e0d1299383354b457d60480c638",
    "CURRENT_SCIENTIFIC_PREMISES.tsv": "0fa377cb50b775875dd8f2de95acb840f3d38183c71b54caef242a89cfc1fa13",
}


class GateError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_script(name: str) -> dict[str, object]:
    proc = subprocess.run(
        ["python3", str(HERE / name)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    )
    return json.loads(proc.stdout)


def validate_sources() -> dict[str, str]:
    actual = {path: sha((ROOT / path).read_bytes()) for path in SOURCES}
    require(actual == SOURCES, "SOURCE_HASH_DRIFT")
    return actual


def validate_results() -> dict[str, object]:
    primary = run_script("derive_reciprocal_distance.py")
    independent = run_script("verify_reciprocal_distance_independent.py")
    require(primary["status"] == "PASS" and primary["check_count"] == 21, "PRIMARY_RESULT")
    require(all(primary["checks"].values()), "PRIMARY_FALSE_CHECK")
    require(primary["centralizer"] == {"constraint_rank": 15, "dimension": 1}, "PRIMARY_CENTRALIZER")
    require(independent["status"] == "PASS" and independent["checks"] == 40, "INDEPENDENT_RESULT")
    require(independent["centralizer_rank"] == 15, "INDEPENDENT_CENTRALIZER")
    return {"primary_checks": 21, "independent_checks": 40, "sympy": primary["sympy_version"]}


def validate_semantics() -> dict[str, object]:
    derivation = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    with (HERE / "STATUS_LEDGER.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    require(len(rows) == 17, f"LEDGER_ROWS:{len(rows)}")
    require(len({row["object"] for row in rows}) == 17, "DUPLICATE_LEDGER_OBJECT")
    by_object = {row["object"]: row for row in rows}
    expected = {
        "signed_depth_extractor": "DERIVED_FROM_SUPPLIED_FOUNDED_ARROW",
        "reciprocal_group_magnitude": "DERIVED_FROM_SUPPLIED_FOUNDED_ARROW",
        "one_arrow_two_readouts": "DERIVED_KINEMATIC_SPLIT",
        "reciprocal_magnitude_equals_complete_physical_separation": "NOT_DERIVED_AND_FALSE_FOR_SCALAR_ONLY_WITH_LIVE_ANGULAR_SECTOR",
        "Xmax_profile": "OPEN_NONUNIQUE",
        "pointwise_factorization_extraction": "REFUTED_ON_SUPPLIED_FACTORIZED_ARCHITECTURE",
        "Levi_Civita_transport_as_reciprocal_dilation": "TYPE_MISMATCH",
        "stationary_Killing_two_readouts": "CONDITIONAL_BRANCH_LOCAL_METRIC_DERIVED",
        "holistic_distance_identification": "OWNER_PROPOSED_CONCEPTUAL_FRAME",
        "complete_observer_pair_comparison_map": "OPEN_SHARPENED_TARGET",
    }
    for key, status in expected.items():
        require(by_object[key]["status"] == status, f"STATUS:{key}")
    for token in [
        "delta(A) = (1/2) log(A_22/A_11)",
        "rho(A)=arcosh(Gamma(A))=abs(delta)",
        "F_1(rho)=X_max tanh(kappa rho)",
        "F_2(rho)=X_max[1-exp(-kappa rho)]",
        "same input would\nhave to return arbitrarily many outputs",
        "exact commutator system for full `so(1,3)` holonomy has rank 15",
        "Physical observer separation is to be sought as a readout of one complete observer-pair",
    ]:
        require(token in derivation, f"DERIVATION_TOKEN:{token}")
    require("The proof does not identify `rho` alone with complete physical positional separation" in report, "PHYSICAL_DISTANCE_SCOPE")
    require("owner-proposed conceptual frame" in report, "OWNER_PROPOSAL_DISCLOSURE")
    require("No action, source, carrier, boundary, bootstrap return, mass, or\ndynamics was derived" in report, "AUTHORITY_BOUNDARY")
    review = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    repair = (HERE / "REPAIR_PREREGISTRATION.md").read_text(encoding="utf-8")
    require("`ACCEPTED_WITH_REPAIRS`" in review, "EXTERNAL_VERDICT")
    require("Required repair:" in review and "untracked" in review, "EXTERNAL_REPAIR_DISCLOSURE")
    require("Defect reproduced before mutation" in repair, "REPAIR_PREREGISTRATION")
    require("EXTERNAL ADVERSARIAL REVIEW ACCEPTED WITH MECHANICAL REPAIR" in report, "REVIEW_CLOSURE")
    return {"ledger_rows": len(rows), "guarded_statuses": len(expected), "external_verdict": "ACCEPTED_WITH_REPAIRS"}


def check_change_scope(tracked_changed: set[str], untracked: set[str]) -> dict[str, object]:
    package_untracked = {path for path in untracked if path.startswith(HERE.name + "/")}
    protected = {path for path in untracked if path.startswith(PREFIX)}
    unexpected_untracked = untracked - package_untracked - protected
    require(not unexpected_untracked, f"UNEXPECTED_UNTRACKED:{sorted(unexpected_untracked)}")
    require(all(path.startswith(HERE.name + "/") for path in tracked_changed), f"OUT_OF_SCOPE_TRACKED:{sorted(tracked_changed)}")
    observed_package = tracked_changed | package_untracked
    require(observed_package == EXPECTED_PACKAGE_FILES, f"PACKAGE_SCOPE:{sorted(observed_package ^ EXPECTED_PACKAGE_FILES)}")
    protected_paths = sorted(protected)
    require(len(protected_paths) == 83, f"PROTECTED_COUNT:{len(protected_paths)}")
    require(sha(("\n".join(protected_paths) + "\n").encode()) == PATH_SHA, "PROTECTED_PATH_SET")
    return {
        "tracked_changed": sorted(tracked_changed),
        "package_untracked": sorted(package_untracked),
        "package_paths": len(observed_package),
        "protected_paths": protected_paths,
    }


def validate_scope_and_dirty() -> dict[str, object]:
    tracked_changed = set(subprocess.check_output(["git", "diff", "--name-only", BASE], cwd=ROOT, text=True).splitlines())
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-uall"], cwd=ROOT, text=True).splitlines()
    untracked = {line[3:] for line in raw if line.startswith("?? ")}
    scope = check_change_scope(tracked_changed, untracked)
    paths = scope["protected_paths"]
    metadata = []
    for item in paths:
        info = (ROOT / item).stat()
        metadata.append(f"{item}\t{info.st_size}\t{info.st_mtime_ns}\t{stat.S_IMODE(info.st_mode):04o}")
    actual_meta = sha(("\n".join(metadata) + "\n").encode())
    require(actual_meta == META_SHA, "PROTECTED_METADATA")
    return {
        "tracked_changed": scope["tracked_changed"],
        "package_untracked": scope["package_untracked"],
        "package_paths": scope["package_paths"],
        "protected_paths": len(paths),
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
    with (HERE / "STATUS_LEDGER.tsv").open(encoding="utf-8", newline="") as handle:
        ledger = list(csv.DictReader(handle, delimiter="\t"))
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    tracked_changed = set(subprocess.check_output(["git", "diff", "--name-only", BASE], cwd=ROOT, text=True).splitlines())
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-uall"], cwd=ROOT, text=True).splitlines()
    untracked = {line[3:] for line in raw if line.startswith("?? ")}

    def check_primary(record: dict[str, object]) -> None:
        require(record["derived_reciprocal_subgroup_readouts"]["signed_depth"] == "delta(D)=1/2 log(D_22/D_11)", "SIGNED_FORMULA")
        require(record["profile_counterfamily"]["profile_1"] != record["profile_counterfamily"]["profile_2"], "PROFILE_COLLAPSE")
        require(record["centralizer"] == {"constraint_rank": 15, "dimension": 1}, "CENTRALIZER")

    def check_ledger(rows: list[dict[str, str]]) -> None:
        by_object = {row["object"]: row for row in rows}
        require(by_object["holistic_distance_identification"]["status"] == "OWNER_PROPOSED_CONCEPTUAL_FRAME", "OWNER_PROMOTION")
        require(
            by_object["reciprocal_magnitude_equals_complete_physical_separation"]["status"]
            == "NOT_DERIVED_AND_FALSE_FOR_SCALAR_ONLY_WITH_LIVE_ANGULAR_SECTOR",
            "ANGULAR_PROMOTION",
        )

    def check_report(text: str) -> None:
        require("owner-proposed conceptual frame" in text, "DISCLOSURE_REMOVED")

    def check_source(data: bytes) -> None:
        path = next(iter(SOURCES))
        require(sha(data) == SOURCES[path], "SOURCE_MUTATION")

    mutated = json.loads(json.dumps(primary))
    mutated["derived_reciprocal_subgroup_readouts"]["signed_depth"] = "delta=distance"
    profile_mutated = json.loads(json.dumps(primary))
    profile_mutated["profile_counterfamily"]["profile_2"] = profile_mutated["profile_counterfamily"]["profile_1"]
    centralizer_mutated = json.loads(json.dumps(primary))
    centralizer_mutated["centralizer"]["dimension"] = 2
    owner_rows = [row.copy() for row in ledger]
    next(row for row in owner_rows if row["object"] == "holistic_distance_identification")["status"] = "DERIVED"
    angular_rows = [row.copy() for row in ledger]
    next(row for row in angular_rows if row["object"] == "reciprocal_magnitude_equals_complete_physical_separation")["status"] = "DERIVED"
    first_source = next(iter(SOURCES))
    return {
        "signed_extractor_mutation_rejected": caught("signed", lambda: check_primary(mutated)),
        "profile_counterfamily_collapse_rejected": caught("profile", lambda: check_primary(profile_mutated)),
        "centralizer_dimension_mutation_rejected": caught("centralizer", lambda: check_primary(centralizer_mutated)),
        "owner_proposal_promotion_rejected": caught("owner", lambda: check_ledger(owner_rows)),
        "angular_scalar_promotion_rejected": caught("angular", lambda: check_ledger(angular_rows)),
        "owner_disclosure_removal_rejected": caught("disclosure", lambda: check_report(report.replace("owner-proposed conceptual frame", "derived theorem"))),
        "frozen_source_mutation_rejected": caught("source", lambda: check_source((ROOT / first_source).read_bytes() + b"x")),
        "extra_untracked_path_rejected": caught(
            "extra_untracked",
            lambda: check_change_scope(tracked_changed, untracked | {"outside_audit_synthetic.txt"}),
        ),
    }


def main() -> None:
    result = {
        "status": "PASS",
        "sources": validate_sources(),
        "computations": validate_results(),
        "semantics": validate_semantics(),
        "scope_and_dirty": validate_scope_and_dirty(),
        "catch_proofs": catch_proofs(),
        "maximum_conclusion": (
            "DERIVED_ONE_ARROW_SIGNED_DEPTH_AND_RECIPROCAL_MAGNITUDE__"
            "COMPLETE_PHYSICAL_SEPARATION_READOUT_OPEN"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
