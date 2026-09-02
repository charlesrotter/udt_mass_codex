#!/usr/bin/env python3
"""Aggregate, provenance, and exact-replay verifier for the bounded G326 package."""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


LANDING = (
    "HOMOGENEOUS_OFFDIAGONAL_MODES_CLOSE_AS_FIVE_QUOTIENT_LATTICE_MODULI__"
    "ONE_LOCAL_TRANSVERSE_KASNER_SHEAR__NO_NEW_GAUGE_OR_SCALAR_MODE__"
    "NO_FULL_STABILITY_CLAIM"
)

SOURCE_SHA256 = {
    "derive_offdiagonal_modes.py":
        "8b7e1187544afc4fb8aff070981cdb5317adf3eabfcdf64cc8e40e9c6bd94ec2",
    "verify_offdiagonal_independent.py":
        "b108e0d981c89693265d81cbb9590ab87a61fb1665e3240c843fb114de4da5a5",
    "run_catch_proofs.py":
        "8e14824c910f131999ccf945fbc753eac8aa8d00050298fea578960f2b025add",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canned_emitter(artifact: str) -> str:
    return f'''#!/usr/bin/env python3
import argparse
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
rendered = (root / "{artifact}").read_text(encoding="utf-8")
output = root / args.output
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(rendered, encoding="utf-8")
print(rendered, end="")
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    production = load(package / "DERIVATION_RESULT.json")
    independent = load(package / "INDEPENDENT_VERIFICATION.json")
    hostile = load(package / "CATCH_PROOF_RESULT.json")

    gate(production["landing"] == LANDING, "production_landing")
    gate(production["assertion_count"] == 33, "production_assertion_count")
    gate(independent["assertion_count"] == 137, "independent_assertion_count")
    gate(hostile["assertion_count"] == 5, "hostile_assertion_count")
    gate(production["mode_dimensions"] == {
        "connected_scalar_curvature": 0,
        "fixed_quotient_lattice_moduli": 5,
        "local_transverse_kasner_shear": 1,
        "quotient_legal_gauge": 0,
    }, "exact_offdiagonal_dimensions")
    gate(production["combined_g325_g326_dimensions"] == {
        "connected_scalar_curvature": 1,
        "fixed_quotient_lattice_moduli": 8,
        "local_kasner_shear_components": 2,
        "residual_time_translation_gauge": 1,
        "total_integration_constants": 12,
    }, "exact_combined_dimensions")
    gate(production["general_solutions"] == {
        "12": ["T^-2/3", "T^4/3"],
        "13": ["T^-2/3", "T^4/3"],
        "23": ["T^4/3", "T^4/3*log(T/Tref)"],
    }, "complete_solution_basis")
    gate(production["linearized_scalar_curvature"] == "0",
         "production_scalar_zero")
    gate(independent["linearized_scalar_curvature"] == "0",
         "independent_scalar_zero")
    gate(independent["transverse_lattice_mixed_tidal"] == {},
         "independent_lattice_tidal_zero")
    gate(independent["transverse_shear_mixed_tidal"] == {
        "T^-2*log^0": "-1/3"
    }, "independent_shear_tidal_witness")
    gate(independent["offdiagonal_lattice_dimension"] == 5,
         "independent_lattice_dimension")
    gate(independent["offdiagonal_local_shear_dimension"] == 1,
         "independent_shear_dimension")
    gate(independent["combined_homogeneous_integration_constants"] == 12,
         "independent_combined_count")
    gate(independent["production_imported"] is False,
         "independent_no_production_import")
    gate(independent["production_result_read"] is False,
         "independent_no_production_result_read")
    gate(hostile["controls"] == [
        "wrong_ode_coefficient_caught",
        "dropped_repeated_root_log_mode_caught",
        "false_torus_periodicity_caught",
        "fake_curvature_free_log_mode_caught",
        "wrong_combined_dimension_caught",
    ], "all_hostile_controls")
    gate(production["full_homogeneous_synchronous_first_variation_closed_with_g325"],
         "bounded_homogeneous_closure")
    gate(not production["full_linear_stability_proved"], "no_full_linear_overclaim")
    gate(not production["nonlinear_stability_proved"], "no_nonlinear_overclaim")
    gate(not production["inhomogeneous_modes_classified"], "inhomogeneous_open")
    gate(not production["physical_occupancy_selected"], "occupancy_open")
    gate(not production["physical_scale_selected"], "scale_open")
    gate(not production["Xmax_selected"], "xmax_open")
    gate(not production["metric_changed"] and not production["kernel_changed"]
         and not production["angular_sector_changed"], "native_objects_unchanged")

    for name, expected in SOURCE_SHA256.items():
        gate(digest(package / name) == expected, f"source_integrity:{name}")

    independent_text = (package / "verify_offdiagonal_independent.py").read_text()
    gate("import derive_offdiagonal_modes" not in independent_text,
         "static_no_production_import")
    gate("from derive_offdiagonal_modes" not in independent_text,
         "static_no_production_from_import")
    gate("DERIVATION_RESULT.json" not in independent_text,
         "static_no_production_result_read")
    exact = (package / "EXACT_DERIVATION.md").read_text()
    lay = (package / "LAY_REPORT.md").read_text()
    status = (package / "STATUS_LEDGER.tsv").read_text()
    gates = (package / "EVIDENCE_GATES.md").read_text()
    note = (package / "PREREGISTRATION_EXECUTION_NOTE.md").read_text()
    gate(LANDING in exact.replace("\n", ""), "exact_landing_token")
    gate("curvature change beyond the" in note and "Lie transport" in note,
         "curvature_falsifier_clarified_preproduction")
    gate("not a physical population or probability count" in exact,
         "count_not_population")
    gate("Every nonzero Fourier mode" in exact, "exact_fourier_boundary")
    gate("It still does not show that the spacetime is stable" in lay,
         "lay_stability_boundary")
    gate("EXTERNAL_SCIENTIFIC_ACCEPTED__EVIDENCE_REPAIRS_R1_R2_PENDING" in status,
         "status_external_science_accepted_repairs_pending")
    gate("ACCEPT__G326_BOUNDED_OFFDIAGONAL_CENSUS" in gates,
         "fresh_external_acceptance_token")
    gate("ACCEPT__G326_BOUNDED_OFFDIAGONAL_CENSUS" in
         (package / "EXTERNAL_REVIEW_RESPONSE.md").read_text(),
         "external_report_acceptance_token")
    precondition = (package / "REPLAY_PRECONDITION.md").read_text()
    gate("cp -r /intake/. /work/g326_review_writable/" in precondition,
         "writable_copy_command_registered")
    gate("chmod -R u+w /work/g326_review_writable" in precondition,
         "writable_permission_command_registered")
    gate("sealed intake itself remains read-only" in precondition,
         "sealed_intake_remains_read_only")

    replay_lines = [
        line.strip() for line in (package / "REPLAY_COMMANDS.txt").read_text().splitlines()
        if line.strip()
    ]
    gate(len(replay_lines) == 4, "registered_command_count")
    with tempfile.TemporaryDirectory(prefix="udt_g326_replay_") as temporary:
        copy = Path(temporary) / "package"
        shutil.copytree(package, copy, ignore=shutil.ignore_patterns(".review_runtime"))
        for line, artifact in zip(replay_lines[:3], (
            "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json"
        )):
            completed = subprocess.run(
                shlex.split(line), cwd=copy, check=True, capture_output=True, text=True
            )
            gate(completed.returncode == 0, f"replay_exit:{artifact}")
            generated = copy / ".review_runtime" / artifact
            gate(generated.is_file(), f"replay_created:{artifact}")
            gate(load(generated) == load(package / artifact), f"replay_exact:{artifact}")
        gate(replay_lines[3] == (
            "python3 -S verify_package.py --output "
            ".review_runtime/PACKAGE_VERIFICATION_RESULT.json"
        ), "fourth_command_self")

    # Repair R1: the exact aggregate verifier must reject scripts replaced by canned emitters.
    canned_targets = {
        "derive_offdiagonal_modes.py": "DERIVATION_RESULT.json",
        "verify_offdiagonal_independent.py": "INDEPENDENT_VERIFICATION.json",
        "run_catch_proofs.py": "CATCH_PROOF_RESULT.json",
    }
    for script_name, artifact_name in canned_targets.items():
        with tempfile.TemporaryDirectory(prefix="udt_g326_canned_") as temporary:
            copy = Path(temporary) / "package"
            shutil.copytree(package, copy, ignore=shutil.ignore_patterns(".review_runtime"))
            (copy / script_name).write_text(canned_emitter(artifact_name), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-S", "verify_package.py"], cwd=copy,
                capture_output=True, text=True
            )
            gate(completed.returncode != 0 and
                 f"source_integrity:{script_name}" in completed.stderr,
                 f"canned_substitution_rejected:{script_name}")

    result = {
        "schema": "udt-g326-package-verification-v1",
        "status": "PASS_EXTERNAL_SCIENCE__R1_R2_IMPLEMENTED_PENDING_FOLLOWUP",
        "landing": LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "python_version": sys.version,
        "exact_replay": True,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = package / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
