#!/usr/bin/env python3
"""Dependency-free aggregate and no-write verifier for G348."""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

FROZEN_PREREG = {
    "MAP.md": "401e4ef72fc1f29877b2467f12778781df919c80c1aa2e01add3d11e9189472d",
    "PREREGISTRATION.md": "51f953e27f794980c5477d6af5f5b4adfb3f0e9e4cc9b4068c40de61285d9df7",
    "PREMISE_LEDGER.tsv": "f3464a4b1761cd97ab3516f0eeb18e7e2c0cb78f2bd02cce3385f87a5a0edfb5",
    "COMPLETENESS_MAP.md": "b602287b196043233e30b177aab9406679bb8f16bccc4f536b03944ca3cf6d58",
    "SOURCE_SCOPE.tsv": "928eef3372b5fc84fcc66a455129569e6486e658b6d3234b16a541e1e777d10a",
}

FROZEN_SCRIPTS = {
    "derive_generic_null_screen_area.py": "e688a4e7853e8b882e7d7f834fd6d3f58d58ce1cacbc0758203537b4d204d713",
    "verify_generic_null_screen_area_independent.py": "2161d6bcc26d99e56475234f5d72978004353555baab1d23c25951871737b39e",
    "run_catch_proofs.py": "801b680f2f83f2f1eddce428f39429d7d642288437d74aabf9b29673c9ecd2b0",
}

SOURCE_HASHES = {
    "udt_g343_bilocal_screen_phase_space_propagator_2026-09-04/EXACT_DERIVATION.md":
        "b295455e2835e3a04de7e91dbafb61ba0b0cef0f1eaea338c90cfe8a1cab5051",
    "udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md":
        "8af5dd5dfdb259bcafd184155664792c9f6f027428202e3e69039735a604687a",
    "udt_g345_observer_calibrated_screen_scalar_2026-09-04/EXACT_DERIVATION.md":
        "e59887e92b055cc18a8215ae6acbbf88528d1371b2afcc03371935c574079722",
    "udt_g346_directional_angular_area_reciprocity_2026-09-04/EXACT_DERIVATION.md":
        "e406301ea81b617dd971d1f1818ce2cfc402e6fa0f91a2925162992f1047c534",
    "udt_g347_arbitrary_endpoint_observer_angular_area_covariance_2026-09-04/EXACT_DERIVATION.md":
        "b0861e58ccdb99bf849a325e6fc9b9cc93326983f202605f251bd46ae1c9910e",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_snapshot():
    return {
        path.relative_to(HERE).as_posix(): digest(path)
        for path in HERE.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def parse_output(name):
    environment = dict(os.environ)
    environment["UDT_NO_WRITE"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-B", "-S", str(HERE / name)],
        cwd=HERE,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"{name} failed: {completed.stderr}\n{completed.stdout}")
    return json.loads(completed.stdout)


def main():
    checks = {}
    checks["frozen_preregistration_hashes"] = all(
        digest(HERE / name) == expected for name, expected in FROZEN_PREREG.items()
    )
    checks["frozen_source_hashes"] = all(
        digest(ROOT / name) == expected for name, expected in SOURCE_HASHES.items()
    )
    checks["frozen_script_hashes"] = all(
        digest(HERE / name) == expected for name, expected in FROZEN_SCRIPTS.items()
    )

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    checks["production_39542_of_39542"] = (
        production["status"] == "PASS" and production["assertions"] == 39542
        and production["failed"] == [] and production["preregistration_commit"] == "23e50369"
        and production["noncommuting_profiles"] == 420 and production["observer_cases"] == 420
    )
    checks["independent_9759_of_9759"] = (
        independent["status"] == "PASS" and independent["assertions"] == 9759
        and independent["failed"] == [] and independent["smooth_variable_tide_cases"] == 150
        and "imports no production" in independent["method"]
    )
    checks["hostile_21_of_21"] = (
        hostile["status"] == "PASS" and hostile["caught"] == hostile["total"] == 21
        and hostile["failed"] == [] and all(hostile["mutations"].values())
    )
    checks["selected_alternatives"] = production["selected_alternatives"] == [
        "A", "Q1", "J1", "R1", "A1", "O1", "C1", "X1", "S1", "W1", "P1"
    ]

    execution = (HERE / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8")
    derivation = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    ledger = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    checks["first_failure_and_repair_recorded"] = all(token in execution for token in (
        "39541/39542", "finite-offset", "centered first derivative", "No candidate theorem",
        "Canonical-momentum typing clarification",
    ))
    checks["generic_metric_theorem_wording"] = all(token in derivation for token in (
        "Levi-Civita quotient connection", "self-adjoint", "M_{20}=M_{21}M_{10}",
        "B_{01}=-B_{10}^{*}", "not uniquely diagnostic of UDT",
    ))
    checks["rank_and_crossing_classification"] = all(token in derivation for token in (
        "operatorname{ord}_{\\lambda_*}\\det B=\\dim\\ker B", "rank one", "rank zero",
        "higher-order degenerate metric-Jacobi crossings cannot",
    ))
    checks["observer_covariance_generic"] = all(token in derivation for token in (
        "mathscr A'_{1\\leftarrow0}=D_0^2", "mathscr A'_{0\\leftarrow1}=D_1^2",
        "pointwise general, not Taub/Kasner-specific",
    ))
    checks["chartwise_not_global_sewing"] = all(token in derivation for token in (
        "type-I endpoint generator", "If any required `B` is singular",
        "full symplectic composition",
    ))
    checks["metric_only_provenance"] = (
        "owner-provisional trace-free response equation is not used" in derivation
        and "category-A analysis tools" in audit and "PINNED_BY_HABIT" not in ledger
    )
    checks["bounded_physical_scope"] = all(token in audit + lay for token in (
        "not a finite-beam theorem", "observational distance", "matter/mass", "`X_max`", "canon",
    ))

    allowed_imports = {"__future__", "ast", "hashlib", "json", "math", "os", "pathlib",
                       "random", "subprocess", "sys"}
    imported = set()
    for name in FROZEN_SCRIPTS:
        tree = ast.parse((HERE / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
    checks["stdlib_only_imports"] = imported <= allowed_imports

    before = package_snapshot()
    replay_production = parse_output("derive_generic_null_screen_area.py")
    replay_independent = parse_output("verify_generic_null_screen_area_independent.py")
    replay_hostile = parse_output("run_catch_proofs.py")
    after = package_snapshot()
    checks["registered_no_write_replays"] = (
        replay_production["assertions"] == 39542 and replay_production["status"] == "PASS"
        and replay_independent["assertions"] == 9759 and replay_independent["status"] == "PASS"
        and replay_hostile["caught"] == replay_hostile["total"] == 21
    )
    checks["aggregate_replay_changes_no_bytes"] = before == after
    checks["no_bytecode_or_special_output"] = not any(
        path.name == "__pycache__" for path in HERE.rglob("*")
    )

    external_path = HERE / "EXTERNAL_REVIEW_RESPONSE.md"
    transmission_path = HERE / "EXTERNAL_REVIEW_TRANSMISSION.md"
    external = external_path.read_text(encoding="utf-8")
    transmission = transmission_path.read_text(encoding="utf-8")
    checks["fresh_external_acceptance"] = (
        digest(external_path)
        == "6d8b02c9ce76d99039318ab03fc0e737a5ab2c456178fae9f66e684c3cce0af5"
        and external.rstrip().endswith("ACCEPT_G348_GENERIC_NULL_SCREEN_AREA_THEOREM")
        and "No mathematical repair is required" in external
        and "tautological hostile controls" in external
        and "3f1dc71c37a2352c8ecda0b88fb826cd1707a5a0220403b8ec566f24854c10cf"
        in transmission
        and "e6558faf549f1fbf5df09fd947b0ff7bc1e1cbf707a795b06ef299cd73e7c8d2"
        in transmission
        and "ca5dbecc025ce59c80a1896632916f249bc4ccc66bb8a0257c72b353e053c8e4"
        in transmission
        and "01a06f1d-4fda-74a1-b49b-43c57c4778a4" in transmission
    )

    result = {
        "all_passed": all(checks.values()),
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "landing": production["landing"],
        "review_status": "EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
