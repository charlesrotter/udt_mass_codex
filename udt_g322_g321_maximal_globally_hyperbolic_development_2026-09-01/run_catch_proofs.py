#!/usr/bin/env python3
"""Hostile G322 checks by mutating actual evidence in ephemeral package copies."""

import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
DETAILS = []


def mutate_result(package, **changes):
    path = package / "DERIVATION_RESULT.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data.update(changes)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def mutate_json(package, name, **changes):
    path = package / name
    data = json.loads(path.read_text(encoding="utf-8"))
    data.update(changes)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def remove_text(package, name, target):
    path = package / name
    text = path.read_text(encoding="utf-8")
    if target not in text:
        raise AssertionError(f"hostile target missing: {target}")
    path.write_text(text.replace(target, "", 1), encoding="utf-8")


def mutate_tsv(package, name, key_name, key_value, field, value):
    path = package / name
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    target = next(row for row in rows if row[key_name] == key_value)
    target[field] = str(value)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_verifier(package):
    return subprocess.run(
        [sys.executable, "-S", "verify_package.py"],
        cwd=package,
        text=True,
        capture_output=True,
        check=False,
    )


def run_mutation(label, mutator, expected):
    with tempfile.TemporaryDirectory(prefix="udt_g322_hostile_") as temp:
        package = Path(temp) / "package"
        shutil.copytree(HERE, package, ignore=shutil.ignore_patterns("__pycache__"))
        (package / ".g322_mutation_probe").write_text("ephemeral hostile probe\n", encoding="utf-8")
        mutator(package)
        completed = run_verifier(package)
        combined = completed.stdout + completed.stderr
        if completed.returncode == 0 or expected not in combined:
            raise AssertionError(
                f"mutation survived or failed for wrong reason: {label}; "
                f"returncode={completed.returncode}; expected={expected!r}; output={combined[-800:]!r}"
            )
        DETAILS.append({
            "label": label,
            "verifier_returncode": completed.returncode,
            "expected_rejection": expected,
            "expected_rejection_observed": True,
        })


with tempfile.TemporaryDirectory(prefix="udt_g322_baseline_") as temp:
    baseline = Path(temp) / "package"
    shutil.copytree(HERE, baseline, ignore=shutil.ignore_patterns("__pycache__"))
    (baseline / ".g322_mutation_probe").write_text("ephemeral hostile probe\n", encoding="utf-8")
    baseline_run = run_verifier(baseline)
    if baseline_run.returncode != 0:
        raise AssertionError(f"unmutated baseline failed: {(baseline_run.stdout + baseline_run.stderr)[-1200:]}")

run_mutation(
    "R1_constraint_residual_corrupted",
    lambda package: mutate_tsv(package, "DATA_INTERFACE.tsv", "mode", "1", "max_hamiltonian", 1.0),
    "atlas Hamiltonian",
)
run_mutation(
    "R2_Lambda_sector_changed",
    lambda package: mutate_result(package, constraint_sector="Lambda=1"),
    "constraint sector drift",
)
run_mutation(
    "R3_principal_completion_reversed",
    lambda package: mutate_result(package, raw_tracefree_principal_rank=10, fixed_lambda_principal_rank=9),
    "raw rank drift",
)
run_mutation(
    "R4_imported_theorem_called_machine_proved",
    lambda package: mutate_result(package, theorem_interface_status="NATIVE_MACHINE_PROVED"),
    "theorem import boundary drift",
)
run_mutation(
    "R5_maximal_conclusion_made_unconditional",
    lambda package: mutate_result(package, maximal_GH_per_fixed_datum="UNCONDITIONAL_DERIVED"),
    "maximal conclusion drift",
)
run_mutation(
    "R6_maximality_called_geodesic_completeness",
    lambda package: mutate_result(package, geodesic_completeness="DERIVED_TRUE"),
    "completeness overclaim",
)
run_mutation(
    "R7_maximality_called_absolute_inextendibility",
    lambda package: mutate_result(package, arbitrary_Lorentzian_inextendibility="DERIVED_TRUE"),
    "inextendibility overclaim",
)
run_mutation(
    "R8_per_datum_called_physical_occupancy",
    lambda package: mutate_result(package, physical_occupancy="SELECTED"),
    "occupancy overclaim",
)
run_mutation(
    "R9_marked_called_unmarked_classification",
    lambda package: mutate_result(package, unmarked_cross_datum_classification="CLASSIFIED"),
    "unmarked classification overclaim",
)
run_mutation(
    "R10_metric_kernel_change_smuggled",
    lambda package: mutate_result(package, metric_kernel_angular_interface="CHANGED"),
    "metric/kernel regression",
)
run_mutation(
    "R11_theorem_interface_H8_promoted",
    lambda package: mutate_tsv(package, "THEOREM_INTERFACE.tsv", "id", "H8", "status", "DERIVED_NATIVE"),
    "theorem interface drift",
)
run_mutation(
    "R12_scope_matrix_completeness_promoted",
    lambda package: mutate_tsv(package, "SCOPE_MATRIX.tsv", "claim", "geodesic_completeness", "status", "DERIVED_TRUE"),
    "scope matrix drift",
)
run_mutation(
    "R13_primary_abstract_word_count_corrupted",
    lambda package: mutate_json(package, "S09_PRIMARY_ABSTRACT_EVIDENCE.json", bounded_excerpt_word_count=24),
    "primary excerpt word count",
)
run_mutation(
    "R14_human_run_record_command_omitted",
    lambda package: remove_text(package, "RUN_RECORD.md", "python3 -S verify_package.py"),
    "human run record incomplete",
)

output = {
    "schema": "udt-g322-hostile-catches-v1",
    "status": "PASS_ALL_MUTATIONS_CAUGHT",
    "mutation_method": "EPHEMERAL_ACTUAL_EVIDENCE_MUTATION_THEN_AGGREGATE_REJECTION",
    "baseline_verifier_returncode": baseline_run.returncode,
    "caught_count": len(DETAILS),
    "expected_count": 14,
    "details": DETAILS,
}
with (HERE / "CATCH_PROOF_RESULT.json").open("w", encoding="utf-8") as handle:
    json.dump(output, handle, indent=2, sort_keys=True)
    handle.write("\n")
print(json.dumps(output, indent=2, sort_keys=True))
