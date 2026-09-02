#!/usr/bin/env python3
"""Hostile G321 checks by mutating real package artifacts in ephemeral copies."""

import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
CAUGHT = []
DETAILS = []


def mutate_result(package, **changes):
    path = package / "DERIVATION_RESULT.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data.update(changes)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def mutate_atlas(package, field, value):
    path = package / "DEVELOPMENT_ATLAS.tsv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    rows[0][field] = str(value)
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


def run_mutation(label, mutator, expected_message):
    with tempfile.TemporaryDirectory(prefix="udt_g321_hostile_") as temp:
        package = Path(temp) / "package"
        shutil.copytree(HERE, package, ignore=shutil.ignore_patterns("__pycache__"))
        (package / ".g321_mutation_probe").write_text("ephemeral hostile probe\n", encoding="utf-8")
        mutator(package)
        completed = run_verifier(package)
        combined = completed.stdout + completed.stderr
        rejected = completed.returncode != 0 and expected_message in combined
        if not rejected:
            raise AssertionError(
                f"mutation survived or failed for wrong reason: {label}; "
                f"returncode={completed.returncode}; expected={expected_message!r}; output={combined[-800:]!r}"
            )
        CAUGHT.append(label)
        DETAILS.append({
            "label": label,
            "verifier_returncode": completed.returncode,
            "expected_rejection": expected_message,
            "expected_rejection_observed": True,
        })


# Prove the unmutated real package copy passes the same verifier route before any attack.
with tempfile.TemporaryDirectory(prefix="udt_g321_hostile_baseline_") as temp:
    baseline = Path(temp) / "package"
    shutil.copytree(HERE, baseline, ignore=shutil.ignore_patterns("__pycache__"))
    (baseline / ".g321_mutation_probe").write_text("ephemeral hostile probe\n", encoding="utf-8")
    baseline_run = run_verifier(baseline)
    if baseline_run.returncode != 0:
        raise AssertionError(f"unmutated baseline failed: {(baseline_run.stdout + baseline_run.stderr)[-1200:]}")


run_mutation(
    "R1_wrong_Hamiltonian_sign",
    lambda package: mutate_atlas(package, "max_hamiltonian", 1.0),
    "atlas Hamiltonian",
)
run_mutation(
    "R2_arbitrary_Lambda_despite_H_zero",
    lambda package: mutate_result(package, constraint_sector="Lambda=1"),
    "sector",
)
run_mutation(
    "R3_omitted_momentum_constraint",
    lambda package: mutate_atlas(package, "max_momentum", 0.25),
    "atlas momentum",
)
run_mutation(
    "R4_lapse_shift_called_physical_branches",
    lambda package: mutate_result(package, lapse_shift_are_physical_data=True),
    "gauge variables promoted to physical data",
)
run_mutation(
    "R5_collapsed_K_sign_branches",
    lambda package: mutate_result(package, opposite_signs_are_distinct_full_data=False),
    "K sign branches collapsed",
)
run_mutation(
    "R6_wrong_time_reversal_parity",
    lambda package: mutate_result(package, opposite_signs_are_time_reversed_data=False),
    "time reversal field",
)
run_mutation(
    "R7_first_jet_determinism_called_PDE_proof",
    lambda package: mutate_result(package, local_geometric_uniqueness="DERIVED_FROM_INITIAL_ADM_RHS"),
    "conditional theorem caveat lost",
)
run_mutation(
    "R8_imported_theorem_caveat_erased",
    lambda package: mutate_result(package, local_geometric_uniqueness="UNCONDITIONAL"),
    "conditional theorem caveat lost",
)
run_mutation(
    "R9_marked_local_upgraded_to_unmarked_global",
    lambda package: mutate_result(package, unmarked_same_spacetime_different_slice_classified=True),
    "unmarked quotient overclaim",
)
run_mutation(
    "R10_uniqueness_called_physical_occupancy",
    lambda package: mutate_result(package, physical_initial_data_selected=True, global_history_selected=True),
    "data selection overclaim",
)
run_mutation(
    "R11_raw_rank_nine_called_complete_evolution",
    lambda package: mutate_result(package, raw_tracefree_principal_rank=10, fixed_lambda_principal_rank=9),
    "raw rank",
)
run_mutation(
    "R12_metric_or_kernel_change_smuggled",
    lambda package: mutate_result(package, metric_or_kernel_changed=True),
    "metric/kernel regression",
)


output = {
    "schema": "udt-g321-hostile-catches-v2",
    "status": "PASS_ALL_MUTATIONS_CAUGHT",
    "mutation_method": "EPHEMERAL_PACKAGE_MUTATION_THEN_AGGREGATE_VERIFIER_REJECTION",
    "baseline_verifier_returncode": baseline_run.returncode,
    "caught_count": len(CAUGHT),
    "expected_count": 12,
    "caught": CAUGHT,
    "details": DETAILS,
}
with (HERE / "CATCH_PROOF_RESULT.json").open("w", encoding="utf-8") as handle:
    json.dump(output, handle, indent=2, sort_keys=True)
    handle.write("\n")
print(json.dumps(output, indent=2, sort_keys=True))
