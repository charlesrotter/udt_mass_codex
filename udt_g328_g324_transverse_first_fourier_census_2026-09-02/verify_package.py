#!/usr/bin/env python3
"""Aggregate, provenance, and isolated replay verifier for G328."""

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
    "PRIMITIVE_TRANSVERSE_FOURIER_SECTOR_CLOSES_MODULO_PERIODIC_GAUGE__"
    "TWO_PHYSICAL_MODE_FAMILIES__EXACT_BRANCH_CLASSIFICATION__"
    "NO_FULL_STABILITY_CLAIM"
)

SOURCE_SHA256 = {
    "derive_transverse_modes.py":
        "385d25a4814d64eb8b045bf0c05adf02ccce993859fc97224e85d334a1b0bef7",
    "verify_independent.py":
        "b59722ae73430b2df9678c1256bacf83dc16aa1099273bc8e2334865e51a3de6",
    "run_catch_proofs.py":
        "d404e8a1019c8cd6882ce85948793ab38407e5963b0ef3c8618ef5bf435ed08b",
}

EVIDENCE_SHA256 = {
    "sealed_runtime.py":
        "e98a5325298cd2e54756f387a197651337d76aef252e6d180a0847dda27a2b2e",
    "VENDORED_SYMPY_RUNTIME.zip":
        "caa6a0b9aae296979d86b54ae5ce8a1df50081c0701aaae4c2e370867a233d9d",
    "VENDORED_RUNTIME_MANIFEST.json":
        "2c978c1caa001c909bda7eaaba2dc880153386b145bfc86e587b0b3d0fa3f022",
    "verify_preregistration_proof.py":
        "aeae516db71a2bb50215eb27950c0065e2f2d17915cfbf04dbc71da1d9c0946d",
    "PREREGISTRATION_COMMIT_OBJECT.txt":
        "8b6f32b09e23dca8152673008e6569b3b1ac66f482f0b4a40afc5cbdf63fe4f8",
    "PREREGISTRATION_CHANGESET.tsv":
        "f536852cf99f5414bfecd658d8ed63aa5e91193b1a14ca10a020286b17a36e83",
    "PREREGISTRATION_TREE.tsv":
        "1077422a5e84ffdcd2b692ef73a0f47549f76a1a0ee6279343830496e0e54651",
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
    nested = os.environ.get("UDT_G328_NESTED_AGGREGATE") == "1"
    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    production = load(package / "DERIVATION_RESULT.json")
    independent = load(package / "INDEPENDENT_VERIFICATION.json")
    hostile = load(package / "CATCH_PROOF_RESULT.json")

    gate(production["landing"] == LANDING, "production_landing")
    gate(independent["landing"] == LANDING, "independent_landing")
    gate(production["status"] == "PRODUCTION_DERIVED", "production_status")
    gate(independent["status"] == "INDEPENDENT_VERIFIED", "independent_status")
    gate(hostile["status"] == "ALL_HOSTILE_MUTATIONS_REJECTED", "hostile_status")
    gate(production["assertion_count"] == 90, "production_assertion_count")
    gate(independent["assertion_count"] == 23, "independent_assertion_count")
    gate(hostile["assertion_count"] == len(hostile["caught"]) == 7,
         "hostile_seven_of_seven")
    gate(production["physical_masters"]["even"] ==
         "H_e''+H_e'/T+nu^2*T^(-4/3)*H_e=0", "even_master_exact")
    gate(production["physical_masters"]["odd"] ==
         "H_o''+H_o'/T+(nu^2*T^(-4/3)-T^(-2))*H_o=0", "odd_master_exact")
    gate(production["time_bases"]["even"] == ["J_0(argument)", "Y_0(argument)"],
         "even_basis_complete")
    gate(production["time_bases"]["odd"] == ["J_3(argument)", "Y_3(argument)"],
         "odd_basis_complete")
    gate(production["physical_real_solution_dimension"] == 8,
         "production_dimension_eight")
    gate(independent["physical_real_dimension"] == 8,
         "independent_dimension_eight")
    gate(production["arbitrary_gauge_functions"] == 4,
         "four_gauge_functions_before_quotient")
    gate(production["linearized_scalar_on_shell"].startswith("0 for k>0"),
         "nonzero_mode_scalar_zero")
    gate(production["past_branches"] == {
        "even": ["finite", "logarithmic"], "odd": ["T", "T^(-1)"]
    }, "all_past_branches_retained")
    gate(production["future_relative_envelope"].startswith("T^(-1/6)"),
         "future_envelope_recorded")
    gate(production["curvature_witnesses"] == {
        "even": "2*dRic3_XX/a^2+dRic3_zz/b^2=(k^2/b^2)*H_e",
        "odd": "dRic3_Xz/(a*b)=(k^2/(2*b^2))*H_o",
    }, "production_curvature_witnesses_exact")
    gate(not production["full_fourier_spectrum_classified"], "full_spectrum_open")
    gate(not production["full_linear_stability_proved"], "linear_stability_open")
    gate(not production["nonlinear_stability_proved"], "nonlinear_stability_open")
    gate(not production["metric_changed"] and not production["kernel_changed"]
         and not production["angular_sector_changed"] and not production["equation_changed"],
         "native_objects_and_equation_unchanged")

    for name, expected in SOURCE_SHA256.items():
        gate(digest(package / name) == expected, f"source_integrity:{name}")
    manifest_rows = {
        fields[0]: fields[1]
        for line in (package / "SOURCE_MANIFEST.tsv").read_text(
            encoding="utf-8"
        ).splitlines()[1:]
        if line.strip()
        for fields in [line.split("\t")]
    }
    gate(manifest_rows == SOURCE_SHA256, "source_manifest_exact")
    for name, expected in EVIDENCE_SHA256.items():
        gate(digest(package / name) == expected, f"evidence_integrity:{name}")

    runtime_manifest = load(package / "VENDORED_RUNTIME_MANIFEST.json")
    gate(runtime_manifest["archive_sha256"] == EVIDENCE_SHA256[
        "VENDORED_SYMPY_RUNTIME.zip"
    ], "runtime_archive_hash")
    gate(runtime_manifest["packages"] == {"mpmath": "1.3.0", "sympy": "1.13.1"},
         "runtime_versions")
    isolated_environment = os.environ.copy()
    isolated_environment["PYTHONNOUSERSITE"] = "1"
    probe = subprocess.run(
        [sys.executable, "-S", "-c", (
            "from sealed_runtime import activate_runtime; p=activate_runtime(); "
            "import json,sympy,mpmath; print(json.dumps({"
            "'archive':str(p),'sympy':sympy.__version__,'sympy_file':sympy.__file__,"
            "'mpmath':mpmath.__version__,'mpmath_file':mpmath.__file__},sort_keys=True))"
        )],
        cwd=package, env=isolated_environment, check=True, capture_output=True, text=True,
    )
    runtime_state = json.loads(probe.stdout)
    gate(runtime_state["sympy"] == "1.13.1" and runtime_state["mpmath"] == "1.3.0",
         "isolated_runtime_versions")
    gate("VENDORED_SYMPY_RUNTIME.zip" in runtime_state["sympy_file"]
         and "VENDORED_SYMPY_RUNTIME.zip" in runtime_state["mpmath_file"],
         "isolated_runtime_paths")

    preregistration = subprocess.run(
        [sys.executable, "-S", "verify_preregistration_proof.py"],
        cwd=package, check=True, capture_output=True, text=True,
    )
    preregistration_result = json.loads(preregistration.stdout)
    gate(preregistration_result["status"] == "PASS", "preregistration_proof_pass")
    gate(preregistration_result["commit"] ==
         "96298482a035a6ffa9103d3949c6aa4fee987c75",
         "preregistration_commit_authenticated")

    independent_text = (package / "verify_independent.py").read_text(encoding="utf-8")
    gate("import derive_transverse_modes" not in independent_text,
         "independent_no_production_import")
    gate("from derive_transverse_modes" not in independent_text,
         "independent_no_production_from_import")
    gate("DERIVATION_RESULT.json" not in independent_text,
         "independent_no_production_result_read")

    exact = (package / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (package / "LAY_REPORT.md").read_text(encoding="utf-8")
    ledger = (package / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    source_scope = (package / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8")
    gate(LANDING in exact.replace("\n", ""), "exact_landing_token")
    gate("does not prove that the entire\nspacetime is stable" in lay,
         "lay_stability_boundary")
    gate("OWNER_ADOPTED_PROVISIONAL_POSTULATE" in ledger,
         "owner_postulate_visible")
    gate("source action matter observation fit scale Xmax\tABSENT" in ledger,
         "forbidden_imports_absent")
    source_rows = [line for line in source_scope.splitlines()[1:] if line.strip()]
    gate(len(source_rows) == 8, "source_scope_eight_registered_dependencies")
    gate(all("archive/" not in line and "protected" not in line for line in source_rows),
         "source_scope_excludes_archive_and_protected_work")

    replay_lines = [
        line.strip()
        for line in (package / "REPLAY_COMMANDS.txt").read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]
    gate(len(replay_lines) == 4, "registered_command_count")
    gate(all(line.startswith("python3 -S ") for line in replay_lines),
         "dependency_isolated_commands")
    gate(all(".review_runtime/" in line for line in replay_lines),
         "all_outputs_ephemeral")
    gate(replay_lines[3] == (
        "python3 -S verify_package.py --output "
        ".review_runtime/PACKAGE_VERIFICATION_RESULT.json"
    ), "literal_fourth_command_registered")

    artifact_names = (
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
    )
    replay_count = 0
    literal_fourth = False
    if not nested:
        with tempfile.TemporaryDirectory(prefix="udt_g328_replay_") as temporary:
            copy = Path(temporary) / "package"
            shutil.copytree(package, copy, ignore=shutil.ignore_patterns(".review_runtime"))
            for index, (line, artifact) in enumerate(zip(replay_lines, artifact_names)):
                environment = isolated_environment.copy()
                if index == 3:
                    environment["UDT_G328_NESTED_AGGREGATE"] = "1"
                completed = subprocess.run(
                    shlex.split(line), cwd=copy, env=environment, check=True,
                    capture_output=True, text=True,
                )
                replay_count += 1
                gate(completed.returncode == 0, f"replay_exit:{artifact}")
                generated = copy / ".review_runtime" / artifact
                gate(generated.is_file(), f"replay_created:{artifact}")
                if index < 3:
                    gate(generated.read_bytes() == (package / artifact).read_bytes(),
                         f"replay_byte_exact:{artifact}")
                else:
                    child = load(generated)
                    gate(child["status"] == "PASS_INTERNAL_PENDING_EXTERNAL_REVIEW",
                         "fourth_command_child_status")
                    gate(child["nested_replay"] is True,
                         "fourth_command_recursion_guard")
                    literal_fourth = True
        gate(replay_count == 4, "all_four_commands_replayed")
        gate(literal_fourth, "literal_fourth_command_replayed")
    else:
        gate(nested, "nested_replay_guard_active")

    # A script that merely republishes a stored answer must fail source integrity.
    if not nested:
        canned_targets = {
            "derive_transverse_modes.py": "DERIVATION_RESULT.json",
            "verify_independent.py": "INDEPENDENT_VERIFICATION.json",
            "run_catch_proofs.py": "CATCH_PROOF_RESULT.json",
        }
        for script_name, artifact_name in canned_targets.items():
            with tempfile.TemporaryDirectory(prefix="udt_g328_canned_") as temporary:
                copy = Path(temporary) / "package"
                shutil.copytree(package, copy, ignore=shutil.ignore_patterns(".review_runtime"))
                (copy / script_name).write_text(canned_emitter(artifact_name), encoding="utf-8")
                completed = subprocess.run(
                    [sys.executable, "-S", "verify_package.py"], cwd=copy,
                    capture_output=True, text=True,
                )
                gate(completed.returncode != 0
                     and f"source_integrity:{script_name}" in completed.stderr,
                     f"canned_substitution_rejected:{script_name}")

    result = {
        "schema": "udt-g328-package-verification-v1",
        "status": "PASS_INTERNAL_PENDING_EXTERNAL_REVIEW",
        "landing": LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "exact_replay": True,
        "registered_replay_count": replay_count,
        "literal_fourth_command_replayed": literal_fourth,
        "nested_replay": nested,
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
