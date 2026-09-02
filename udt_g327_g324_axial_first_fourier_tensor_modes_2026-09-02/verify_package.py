#!/usr/bin/env python3
"""Aggregate, provenance, and no-write replay verifier for G327."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


LANDING = (
    "PRIMITIVE_AXIAL_TENSOR_MODE_CLOSES_AS_TWO_GAUGE_INVARIANT_POLARIZATIONS__"
    "BESSEL_ZERO_TIME_BASIS__FINITE_AND_LOGARITHMIC_PAST_BRANCHES__"
    "OSCILLATORY_T_MINUS_TWO_THIRDS_FUTURE_DECAY__NO_FULL_STABILITY_CLAIM"
)

SOURCE_SHA256 = {
    "derive_axial_tensor_modes.py":
        "3bb966992088d279a8a13444048ef4ba62fec93f2667e7d7b312166c21926e21",
    "verify_independent.py":
        "aed32b5fd4003ad3674944edfd3fb58de6b29a94a53472a58f89623285c24ba6",
    "run_catch_proofs.py":
        "7c972121356cfe9900e19b1544ea62c48c8e0bd97745c7e407ad6479b4d21d4e",
}

EVIDENCE_SHA256 = {
    "sealed_runtime.py":
        "32a3aa6ed3b676ffd1572b5f21b08a6ee7e381983c3fb9b2aea1635d5e480199",
    "VENDORED_SYMPY_RUNTIME.zip":
        "caa6a0b9aae296979d86b54ae5ce8a1df50081c0701aaae4c2e370867a233d9d",
    "VENDORED_RUNTIME_MANIFEST.json":
        "91a9ecc39986c64748745473519b641011a4b642127f9d3692cd3891ba5f7ce7",
    "verify_preregistration_proof.py":
        "d70c07079d7d6429f7c8818621e03e9e7c9daeff88772c1cc332daa96c5c5726",
    "PREREGISTRATION_COMMIT_OBJECT.txt":
        "7d20d13530475fc8ef76d30b987b08404ac8c028ef79c142c04eb6b65841018e",
    "PREREGISTRATION_CHANGESET.tsv":
        "072dd0c606df7bad099782c90f772e811fff540b6d258a3f940316f7695ebbe7",
    "PREREGISTRATION_TREE.tsv":
        "17ce00cc1874016dbc0cd7e293fe60491738d7ce8f09ed4bbd7ea8b74eb0ebbe",
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
    nested_replay = os.environ.get("UDT_G327_NESTED_AGGREGATE") == "1"
    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    production = load(package / "DERIVATION_RESULT.json")
    independent = load(package / "INDEPENDENT_VERIFICATION.json")
    hostile = load(package / "CATCH_PROOF_RESULT.json")

    gate(production["landing"] == LANDING, "production_landing")
    gate(independent["landing"] == LANDING, "independent_landing")
    gate(production["status"] == "INTERNAL_VERIFIED_PENDING_EXTERNAL_REVIEW",
         "production_status")
    gate(independent["status"] == "INDEPENDENT_VERIFIED", "independent_status")
    gate(hostile["status"] == "PASS", "hostile_status")
    gate(production["assertion_count"] == 32, "production_assertion_count")
    gate(independent["assertion_count"] == 25, "independent_assertion_count")
    gate(hostile["caught"] == hostile["attempted"] == 6, "hostile_six_of_six")
    gate(production["mode_ode"] == "H''+H'/T+nu^2*T^(2/3)*H=0", "exact_mode_ode")
    gate(production["time_basis"] == ["J_0(z)", "Y_0(z)"], "complete_time_basis")
    gate(production["time_wronskian"] == "T*W_T=8/(3*pi)", "nonzero_wronskian")
    gate(production["real_solution_dimension"] == 8, "production_dimension_eight")
    gate(independent["real_solution_dimension"] == 8, "independent_dimension_eight")
    gate(production["linearized_scalar_curvature"] == "0", "production_scalar_zero")
    gate(independent["linearized_scalar_curvature"] == "0", "independent_scalar_zero")
    gate(production["plus_tidal_on_shell"] == (
        "-Derivative(h_plus(T), T)/(3*T) + 4*h_plus(T)/(9*T**2) + "
        "T**(2/3)*k**2*h_plus(T)/C1**2"
    ), "plus_tidal_formula_exact")
    gate(production["cross_tidal_on_shell"] == (
        "-Derivative(h_cross(T), T)/(3*T) + 4*h_cross(T)/(9*T**2) + "
        "T**(2/3)*k**2*h_cross(T)/C1**2"
    ), "cross_tidal_formula_exact")
    gate(production["compact_time_norm_finite"], "compact_time_norm_finite")
    gate("T^(-2/3)" in production["future_endpoint"], "future_power_recorded")
    gate(not production["full_fourier_spectrum_classified"], "full_spectrum_open")
    gate(not production["full_linear_stability_proved"], "linear_stability_open")
    gate(not production["nonlinear_stability_proved"], "nonlinear_stability_open")
    gate(not production["physical_occupancy_selected"], "occupancy_open")
    gate(not production["physical_scale_selected"], "scale_open")
    gate(not production["Xmax_selected"], "xmax_open")
    gate(not production["metric_changed"] and not production["kernel_changed"]
         and not production["angular_sector_changed"] and not production["equation_changed"],
         "native_objects_and_equation_unchanged")

    for name, expected in SOURCE_SHA256.items():
        gate(digest(package / name) == expected, f"source_integrity:{name}")
    manifest_rows = {
        fields[0]: fields[1]
        for line in (package / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
        if line.strip()
        for fields in [line.split("\t")]
    }
    gate(manifest_rows == SOURCE_SHA256, "source_manifest_exact")
    for name, expected in EVIDENCE_SHA256.items():
        gate(digest(package / name) == expected, f"evidence_integrity:{name}")

    runtime_manifest = load(package / "VENDORED_RUNTIME_MANIFEST.json")
    gate(runtime_manifest["archive_sha256"] == EVIDENCE_SHA256[
        "VENDORED_SYMPY_RUNTIME.zip"
    ], "runtime_manifest_archive_hash")
    gate(runtime_manifest["packages"] == {"mpmath": "1.3.0", "sympy": "1.13.1"},
         "runtime_versions_registered")
    isolated_environment = os.environ.copy()
    isolated_environment["PYTHONNOUSERSITE"] = "1"
    runtime_probe = subprocess.run(
        [sys.executable, "-c", (
            "from sealed_runtime import activate_runtime; p=activate_runtime(); "
            "import json,sympy,mpmath; print(json.dumps({"
            "'archive':str(p),'sympy':sympy.__version__,'sympy_file':sympy.__file__,"
            "'mpmath':mpmath.__version__,'mpmath_file':mpmath.__file__},sort_keys=True))"
        )],
        cwd=package, env=isolated_environment, check=True, capture_output=True, text=True,
    )
    runtime_state = json.loads(runtime_probe.stdout)
    gate(runtime_state["sympy"] == "1.13.1" and runtime_state["mpmath"] == "1.3.0",
         "dependency_isolated_runtime_versions")
    gate("VENDORED_SYMPY_RUNTIME.zip" in runtime_state["sympy_file"]
         and "VENDORED_SYMPY_RUNTIME.zip" in runtime_state["mpmath_file"],
         "dependency_isolated_runtime_paths")

    preregistration = subprocess.run(
        [sys.executable, "-S", "verify_preregistration_proof.py"],
        cwd=package, check=True, capture_output=True, text=True,
    )
    preregistration_result = json.loads(preregistration.stdout)
    gate(preregistration_result["status"] == "PASS", "preregistration_proof_pass")
    gate(preregistration_result["commit"] ==
         "9bec301bc265bf67afa5f8398f7557ccdabb855b",
         "preregistration_commit_object_authenticated")

    independent_text = (package / "verify_independent.py").read_text(encoding="utf-8")
    gate("import derive_axial_tensor_modes" not in independent_text,
         "independent_no_production_import")
    gate("from derive_axial_tensor_modes" not in independent_text,
         "independent_no_production_from_import")
    gate("DERIVATION_RESULT.json" not in independent_text,
         "independent_no_production_result_read")

    exact = (package / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (package / "LAY_REPORT.md").read_text(encoding="utf-8")
    ledger = (package / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    gate(LANDING in exact.replace("\n", ""), "exact_landing_token")
    gate("9bec301b" in audit, "preregistration_commit_recorded")
    gate("not the complete nonzero Fourier problem" in audit, "audit_scope_boundary")
    gate("not proof that the whole spacetime is stable" in lay, "lay_stability_boundary")
    gate("OWNER_ADOPTED_PROVISIONAL_POSTULATE" in ledger, "owner_postulate_visible")
    gate("ABSENT" in ledger and "source action matter observation fit scale Xmax" in ledger,
         "forbidden_imports_absent")

    replay_lines = [
        line.strip()
        for line in (package / "REPLAY_COMMANDS.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    gate(len(replay_lines) == 4, "registered_command_count")
    gate(all(".review_runtime/" in line for line in replay_lines),
         "all_registered_outputs_ephemeral")
    gate(replay_lines[3] == (
        "python3 -S verify_package.py --output "
        ".review_runtime/PACKAGE_VERIFICATION_RESULT.json"
    ), "fourth_command_self")

    artifact_names = (
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
    )
    literal_replay_count = 0
    literal_fourth_command_replayed = False
    if not nested_replay:
        with tempfile.TemporaryDirectory(prefix="udt_g327_replay_") as temporary:
            copy = Path(temporary) / "package"
            shutil.copytree(package, copy, ignore=shutil.ignore_patterns(".review_runtime"))
            for index, (line, artifact) in enumerate(zip(replay_lines, artifact_names)):
                environment = isolated_environment.copy()
                if index == 3:
                    environment["UDT_G327_NESTED_AGGREGATE"] = "1"
                completed = subprocess.run(
                    shlex.split(line), cwd=copy, env=environment, check=True,
                    capture_output=True, text=True,
                )
                literal_replay_count += 1
                gate(completed.returncode == 0, f"replay_exit:{artifact}")
                generated = copy / ".review_runtime" / artifact
                gate(generated.is_file(), f"replay_created:{artifact}")
                if index < 3:
                    gate(generated.read_bytes() == (package / artifact).read_bytes(),
                         f"replay_byte_exact:{artifact}")
                else:
                    child = load(generated)
                    gate(child["status"] == "PASS_INTERNAL_PENDING_EXTERNAL_REPAIR_REVIEW",
                         "fourth_command_child_status")
                    gate(child["nested_replay"] is True,
                         "fourth_command_child_recursion_guard")
                    literal_fourth_command_replayed = True
        gate(literal_replay_count == 4, "all_four_registered_commands_replayed")
        gate(literal_fourth_command_replayed, "literal_fourth_command_replayed")
    else:
        gate(nested_replay, "nested_replay_guard_active")

    # Reject a replacement that merely republishes the banked artifact.
    canned_targets = {
        "derive_axial_tensor_modes.py": "DERIVATION_RESULT.json",
        "verify_independent.py": "INDEPENDENT_VERIFICATION.json",
        "run_catch_proofs.py": "CATCH_PROOF_RESULT.json",
    }
    if not nested_replay:
        for script_name, artifact_name in canned_targets.items():
            with tempfile.TemporaryDirectory(prefix="udt_g327_canned_") as temporary:
                copy = Path(temporary) / "package"
                shutil.copytree(package, copy, ignore=shutil.ignore_patterns(".review_runtime"))
                (copy / script_name).write_text(canned_emitter(artifact_name), encoding="utf-8")
                completed = subprocess.run(
                    [sys.executable, "-S", "verify_package.py"], cwd=copy,
                    capture_output=True, text=True
                )
                gate(completed.returncode != 0
                     and f"source_integrity:{script_name}" in completed.stderr,
                     f"canned_substitution_rejected:{script_name}")

    result = {
        "schema": "udt-g327-package-verification-v1",
        "status": "PASS_INTERNAL_PENDING_EXTERNAL_REPAIR_REVIEW",
        "landing": LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "exact_replay": True,
        "registered_replay_count": literal_replay_count,
        "literal_fourth_command_replayed": literal_fourth_command_replayed,
        "nested_replay": nested_replay,
        "vendored_runtime_used": True,
        "preregistration_commit_authenticated": True,
        "banked_evidence_overwritten": False,
        "python_version": sys.version,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = package / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
