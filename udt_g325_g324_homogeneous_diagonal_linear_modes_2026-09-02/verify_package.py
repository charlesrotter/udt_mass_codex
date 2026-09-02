#!/usr/bin/env python3
"""Aggregate and exact replay verifier for the bounded G325 package."""

from __future__ import annotations

import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


LANDING = (
    "HOMOGENEOUS_DIAGONAL_MODES_CLOSE_AS_TIME_GAUGE__"
    "THREE_QUOTIENT_LATTICE_MODULI__ONE_LOCAL_KASNER_SHEAR__"
    "ONE_CONNECTED_SCALAR_MODE__NO_FULL_STABILITY_CLAIM"
)


def load(path: Path):
    return json.loads(path.read_text())


def main() -> None:
    package = Path(__file__).resolve().parent
    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    production = load(package / "DERIVATION_RESULT.json")
    independent = load(package / "INDEPENDENT_VERIFICATION.json")
    hostile = load(package / "CATCH_PROOF_RESULT.json")
    gate(production["landing"] == LANDING, "production_landing")
    gate(production["assertion_count"] == 37, "production_assertion_count")
    gate(independent["assertion_count"] == 111, "independent_assertion_count")
    gate(hostile["assertion_count"] == 5, "hostile_assertion_count")
    gate(production["mode_dimensions"] == {
        "connected_scalar_curvature": 1,
        "fixed_quotient_lattice_moduli": 3,
        "local_kasner_shear": 1,
        "residual_time_translation_gauge": 1,
    }, "exact_mode_dimensions")
    gate(production["linearized_scalar_curvature"] == "4*lambda",
         "production_scalar_witness")
    gate(independent["linearized_scalar_curvature"] == {
        "eps^0*T^0*log^0": "4"
    }, "independent_scalar_witness")
    gate(independent["linearized_shear_curvature_split"] == {
        "eps^0*T^-2*log^0": "-2/3"
    }, "independent_shear_witness")
    gate(independent["production_imported"] is False, "independent_no_production_import")
    gate(independent["production_result_read"] is False, "independent_no_result_read")
    gate(all(hostile["controls"].values()), "all_hostile_controls")
    gate(not production["full_linear_stability_proved"], "no_full_linear_overclaim")
    gate(not production["nonlinear_stability_proved"], "no_nonlinear_overclaim")
    gate(not production["inhomogeneous_modes_classified"], "inhomogeneous_open")
    gate(not production["offdiagonal_modes_classified"], "offdiagonal_open")
    gate(not production["physical_occupancy_selected"], "occupancy_open")
    gate(not production["physical_scale_selected"], "scale_open")
    gate(not production["Xmax_selected"], "xmax_open")
    gate(not production["metric_changed"] and not production["kernel_changed"]
         and not production["angular_sector_changed"], "native_objects_unchanged")

    independent_text = (package / "verify_independent.py").read_text()
    gate("import derive_modes" not in independent_text, "static_no_production_import")
    gate("DERIVATION_RESULT.json" not in independent_text, "static_no_production_result_read")
    exact = (package / "EXACT_DERIVATION.md").read_text()
    lay = (package / "LAY_REPORT.md").read_text()
    status = (package / "STATUS_LEDGER.tsv").read_text()
    gates = (package / "EVIDENCE_GATES.md").read_text()
    gate(LANDING in exact.replace("\n", ""), "exact_landing_token")
    gate("does **not** prove uniform linear stability" in exact,
         "exact_stability_boundary")
    gate("not proof that the G324 spacetime is stable" in lay, "lay_stability_boundary")
    gate("INTERNAL_VERIFIED_PENDING_EXTERNAL_REVIEW" in status,
         "status_pending_external")
    gate("Fresh external review | PENDING" in gates, "external_review_pending")

    replay_lines = [line.strip() for line in (package / "REPLAY_COMMANDS.txt").read_text().splitlines()
                    if line.strip()]
    gate(len(replay_lines) == 4, "registered_command_count")
    with tempfile.TemporaryDirectory(prefix="udt_g325_replay_") as temporary:
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
        gate(replay_lines[3] == "python3 -S verify_package.py", "fourth_command_self")

    result = {
        "schema": "udt-g325-package-verification-v1",
        "status": "PASS_PENDING_EXTERNAL_REVIEW",
        "landing": LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "python_version": sys.version,
        "exact_replay": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
