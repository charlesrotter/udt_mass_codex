#!/usr/bin/env python3
"""Aggregate dependency-free, no-write verifier for the bounded G351 package."""

import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "OWNER_PROVISIONAL_SOURCE_FREE_LABEL_MEASURE_CONSERVATION"
    "__NONZERO_ABSOLUTELY_CONTINUOUS_REGULAR_DENSITY_AREA_WEIGHT_Q_EQUALS_MINUS_ONE"
    "__OBSERVER_WEIGHT_P_REMAINS_ARBITRARY"
    "__T_P_EQUALS_R_TO_P_A_INVERSE_WITH_IDENTITY_SEWING_REVERSAL_AND_COVARIANCE"
    "__FULL_FINITE_MEASURE_REMAINS_DEFINED_THROUGH_CAUSTIC_RANK_LOSS_WHILE_POINTWISE_DENSITY_NEED_NOT"
    "__SINGULAR_MEASURE_PART_HAS_NO_ORDINARY_DENSITY_EXPONENT"
    "__SOURCE_POPULATION_CROSS_LABEL_PHYSICS_LIGHT_DISTANCE_HISTORY_SCALE_XMAX_AND_CANON_REMAIN_OPEN"
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_bytes():
    return {
        path.relative_to(HERE).as_posix(): digest(path)
        for path in HERE.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }


def run_json(script):
    environment = os.environ.copy()
    environment["UDT_NO_WRITE"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-B", "-S", script],
        cwd=HERE,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def frozen_local_hashes_pass():
    rows = (HERE / "FROZEN_PREREGISTRATION_HASHES.tsv").read_text(encoding="utf-8").splitlines()[1:]
    return all(
        digest(HERE / path) == expected
        for path, expected in (row.split("\t") for row in rows)
    )


def frozen_source_hashes_pass():
    rows = (HERE / "FROZEN_SOURCE_HASHES.tsv").read_text(encoding="utf-8").splitlines()[1:]
    for path, expected in (row.split("\t") for row in rows):
        source = ROOT / path
        if path == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            lines = source.read_bytes().splitlines(keepends=True)
            reconstructed = b"".join(
                line for line in lines if not line.startswith(b"G351\t")
            )
            actual = hashlib.sha256(reconstructed).hexdigest()
        else:
            actual = digest(source)
        if actual != expected:
            return False
    return True


def stdlib_only_pass():
    allowed = {
        "ast", "fractions", "hashlib", "json", "os", "pathlib", "random",
        "shutil", "subprocess", "sys", "tempfile",
    }
    for name in (
        "build_review_intake.py",
        "derive_carried_measure_conservation.py",
        "verify_carried_measure_independent.py",
        "run_catch_proofs.py",
        "verify_package.py",
    ):
        tree = ast.parse((HERE / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [(node.module or "").split(".")[0]]
            else:
                continue
            if any(module not in allowed for module in modules):
                return False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in {"__import__", "eval", "exec"}:
                    return False
    return True


def builder_sources_match_scope():
    tree = ast.parse((HERE / "build_review_intake.py").read_text(encoding="utf-8"))
    configured = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "ROOT_FILES" for target in node.targets
        ):
            configured = tuple(ast.literal_eval(node.value))
            break
    rows = (HERE / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8").splitlines()[1:]
    declared = tuple(row.split("\t", 1)[0] for row in rows)
    return configured is not None and set(configured) == set(declared)


def builder_package_files():
    tree = ast.parse((HERE / "build_review_intake.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "PACKAGE_FILES" for target in node.targets
        ):
            return tuple(ast.literal_eval(node.value))
    return ()


def main():
    sealed_required = (
        "ADVERSARIAL_REVIEW_REQUEST.md", "AUDIT_REPORT.md",
        "BLIND_ADVERSARIAL_REVIEW_RESPONSE.md", "CATCH_PROOF_RESULT.json",
        "COMMANDS.md", "COMPLETENESS_MAP.md", "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md", "EXACT_DERIVATION.md", "FROZEN_PREREGISTRATION_HASHES.tsv",
        "FROZEN_SOURCE_HASHES.tsv", "GIT_PREREGISTRATION_PROOF.txt",
        "INDEPENDENT_VERIFICATION.json", "INTERNAL_VERIFIER_REPAIR_PREREGISTRATION.md",
        "INTERNAL_VERIFIER_REPAIR_RECORD.md", "LAY_REPORT.md", "MAP.md",
        "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "REPAIR_EXECUTION_RECORD.md",
        "R2_REPAIR_PREREGISTRATION.md", "R3_REPAIR_PREREGISTRATION.md",
        "R4_COMPLETION_REVIEW_RESPONSE.md", "R4_REPAIR_PREREGISTRATION.md",
        "R5_PACKAGING_REPAIR_PREREGISTRATION.md",
        "REPAIR_PREMISE_LEDGER.tsv",
        "REPAIR_PREREGISTRATION.md",
        "RUN_RECORD.md", "SOURCE_SCOPE.tsv",
        "STATUS_LEDGER.tsv", "VERIFICATION_RESULT.json", "build_review_intake.py",
        "derive_carried_measure_conservation.py",
        "run_catch_proofs.py", "verify_carried_measure_independent.py", "verify_package.py",
    )
    required = sealed_required + (
        "EXTERNAL_REVIEW_RESPONSE.md", "EXTERNAL_REVIEW_TRANSMISSION.md",
    )
    before = package_bytes()
    production = run_json("derive_carried_measure_conservation.py")
    independent = run_json("verify_carried_measure_independent.py")
    hostile = run_json("run_catch_proofs.py")
    after = package_bytes()

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    premises = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    commands = (HERE / "COMMANDS.md").read_text(encoding="utf-8")
    evidence_gates = (HERE / "EVIDENCE_GATES.md").read_text(encoding="utf-8")
    status_ledger = (HERE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    run_record = (HERE / "RUN_RECORD.md").read_text(encoding="utf-8")
    r4_review = (HERE / "R4_COMPLETION_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    external = (HERE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    transmission = (HERE / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    saved_aggregate = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))

    checks = {
        "all_required_files": all((HERE / name).is_file() for name in required),
        "frozen_preregistration_hashes": frozen_local_hashes_pass(),
        "frozen_source_hashes": frozen_source_hashes_pass(),
        "production_60325_of_60325": production.get("all_passed") is True
        and production.get("checks_passed") == production.get("checks_total") == 60325,
        "independent_11290_of_11290": independent.get("all_passed") is True
        and independent.get("checks_passed") == independent.get("checks_total") == 11290,
        "hostile_12_of_12": hostile.get("all_passed") is True
        and hostile.get("mutations_caught") == hostile.get("mutations_total") == 12,
        "production_result_reproduced": production
        == json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "independent_result_reproduced": independent
        == json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")),
        "hostile_result_reproduced": hostile
        == json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8")),
        "aggregate_replay_changes_no_bytes": before == after,
        "stdlib_only_imports": stdlib_only_pass(),
        "review_builder_sources_match_scope": builder_sources_match_scope(),
        "review_builder_includes_all_required_package_files": set(sealed_required).issubset(
            set(builder_package_files())
        ),
        "owner_premise_visible": "OWNER_ADOPTED_PROVISIONAL_PREMISE" in premises
        and "not derived" in exact,
        "area_weight_unique_in_bounded_domain": "q=-1" in exact
        and "full abstract domain" in exact and "G350" in audit,
        "observer_weight_open": "do not choose `w`" in exact or "do not choose `p`" in exact,
        "observer_weight_open_lay": "Conservation alone does not decide among them" in lay
        and "The exponent `p` is still open" in lay,
        "finite_measure_scope": "finite nonnegative additive measure" in exact,
        "ac_density_scope": "absolutely continuous regular density component" in exact
        and "nonzero-density support" in exact,
        "atomic_counterexample": production.get("atomic_counterexample_passed") is True
        and independent.get("atomic_counterexample_passed") is True
        and production.get("atomic_counterexample_dimension") == 2
        and independent.get("atomic_counterexample_dimension") == 2
        and "delta_(1/2,1/2)" in exact and "[0,1]^2" in exact,
        "singular_q_undefined": production.get("singular_part_has_ordinary_q") is False
        and independent.get("singular_part_has_ordinary_q") is False
        and "no ordinary density exponent `q`" in exact,
        "division_free_zero_density": "n_j=A_ji^-1 n_i" in exact
        and "Zero density obeys (1)" in exact,
        "dimensionless_frequency_reference": "omega_i/omega_*" in exact
        and "dimensionless ratio" in exact,
        "ac_density_derivative_not_full_measure": "n_i=dmu_ac/dArea_i=s/J_i." in exact
        and "n_i=dmu/dArea_i" not in exact,
        "dimensionless_reference_retained_in_conservation_quotient": (
            "(C_j J_j / (omega_j/omega_*)^w)/(C_i J_i / (omega_i/omega_*)^w)" in exact
        ),
        "caustic_boundary": "may diverge" in exact and "singular parts" in exact
        and "finite pointwise scalar" in exact,
        "multiplicity_retained": "retains their multiplicity" in exact
        and "cannot replace the carried measure" in exact,
        "zero_source_stays_zero": "If `mu=0`" in exact and "cannot populate a ray" in exact,
        "cross_label_physics_open": "no phase, cancellation, interference" in exact,
        "metric_kernel_unchanged": "The metric," in audit and "reciprocal kernel, angular sector" in audit
        and "are unchanged" in audit,
        "bounded_physical_ceiling": all(
            token in audit for token in (
                "No source magnitude", "light", "observational distance", "history",
                "scale", "`X_max`", "canon",
            )
        ),
        "preregistered_before_outcomes": "42e4824111aa76890b20483d22cc23bb848aecaf" in prereg
        or "42e48241" in audit,
        "r1_repair_preregistered": "G351 R1 scientific-scope repair preregistration" in (
            HERE / "REPAIR_PREREGISTRATION.md"
        ).read_text(encoding="utf-8") and "atomic counterexample" in (
            HERE / "REPAIR_PREREGISTRATION.md"
        ).read_text(encoding="utf-8"),
        "r2_repair_preregistered": "G351 R2 notation and evidence-state repair preregistration" in (
            HERE / "R2_REPAIR_PREREGISTRATION.md"
        ).read_text(encoding="utf-8"),
        "r3_repair_preregistered": "G351 R3 in-domain atomic-witness repair preregistration" in (
            HERE / "R3_REPAIR_PREREGISTRATION.md"
        ).read_text(encoding="utf-8"),
        "r4_repair_preregistered": "G351 R4 saved-aggregate and evidence-state repair preregistration" in (
            HERE / "R4_REPAIR_PREREGISTRATION.md"
        ).read_text(encoding="utf-8"),
        "r5_packaging_repair_preregistered": (
            "G351 R5 sealed-package self-containment repair preregistration" in (
                HERE / "R5_PACKAGING_REPAIR_PREREGISTRATION.md"
            ).read_text(encoding="utf-8")
            and "omitted `build_review_intake.py`" in (
                HERE / "R5_PACKAGING_REPAIR_PREREGISTRATION.md"
            ).read_text(encoding="utf-8")
        ),
        "evidence_gates_external_complete": (
            "EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED" in evidence_gates
            and "Final aggregate replay is 45/45" in evidence_gates
        ),
        "status_ledger_external_complete": (
            "PASS_LOCAL_NO_WRITE_FINAL\t47/47 post-review" in status_ledger
            and "ACCEPT_FRESH_SEALED_GPT56SOL" in status_ledger
        ),
        "run_record_r1_r5_complete": "R5 sealed-copy aggregate passed 45/45" in run_record,
        "r4_completion_review_acceptance": r4_review.rstrip().endswith("```")
        and "\nACCEPT\n" in r4_review and "repair completion only" in r4_review,
        "external_review_acceptance": external.rstrip().endswith(
            "ACCEPT_G351_BOUNDED_CARRIED_MEASURE_CONSERVATION"
        ) and "standard finite nonnegative countably additive measure" in external
        and "regression evidence, not the analytic proof" in external,
        "external_review_provenance": all(
            token in transmission for token in (
                "2befb81f9ef43a658adf327078ce9c7e1435dd2b6456d6a1b204dcd5e1420fde",
                "47db44c00d8d6ea7cb882bcafb0239cd86d4b732e719c2dedf07d39e98edde01",
                "3622399f5f163c4cc5dcf3154628121d65d2e852068f8d81392dd776264c4e33",
                "01a072a0-91f4-7c01-a048-53047958fe7c",
                "77890a2fd784a9f40230594bf5b20096c10955dfa80b9ccdc1c8e534f975a897",
                "ACCEPT_G351_BOUNDED_CARRIED_MEASURE_CONSERVATION",
            )
        ),
        "registered_no_write_commands": sum(
            "UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S" in line
            for line in commands.splitlines()
        ) == 4,
        "no_bytecode": not any(
            "__pycache__" in path.parts or path.suffix == ".pyc" for path in HERE.rglob("*")
        ),
        "landing_exact": LANDING in exact.replace("\n", ""),
    }
    expected_checks = dict(checks)
    expected_checks["saved_aggregate_exact_current"] = True
    expected_review_status = "EXTERNAL_REVIEW_ACCEPTED"
    checks["saved_aggregate_exact_current"] = (
        saved_aggregate.get("all_passed") is True
        and saved_aggregate.get("checks") == expected_checks
        and saved_aggregate.get("checks_passed") == len(expected_checks)
        and saved_aggregate.get("checks_total") == len(expected_checks)
        and saved_aggregate.get("failed") == []
        and saved_aggregate.get("landing") == LANDING
        and saved_aggregate.get("review_status") == expected_review_status
    )
    failed = sorted(name for name, passed in checks.items() if not passed)
    result = {
        "all_passed": not failed,
        "checks": checks,
        "checks_passed": sum(bool(value) for value in checks.values()),
        "checks_total": len(checks),
        "failed": failed,
        "landing": LANDING,
        "review_status": expected_review_status,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") == "1":
        print(rendered, end="")
    else:
        (HERE / "VERIFICATION_RESULT.json").write_text(rendered, encoding="utf-8")
        print(rendered, end="")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
