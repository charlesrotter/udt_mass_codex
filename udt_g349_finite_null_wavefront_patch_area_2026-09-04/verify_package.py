#!/usr/bin/env python3
"""Dependency-free aggregate and no-write verifier for G349."""

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
    "MAP.md": "5bb3ad63acd62794152df4540beb6b08f71e3d39ed6289fb3dd30d684ba277ac",
    "PREREGISTRATION.md": "5921e786d4ad10be5da004ddd59d72109c8126367bf190e4ad932896d9313f1e",
    "PREMISE_LEDGER.tsv": "2a895dda0db8276beed75da0c3734c9f6e57a61d008c2a5e0c867fe1c5609f33",
    "COMPLETENESS_MAP.md": "b1d36c051b385c75392ffe902a2885d3d0154ee0bac03efb2411ed4dfe4a7e87",
    "SOURCE_SCOPE.tsv": "deed29517ce48fcf13b6f38becc1584f31bd5390efefd93df102ae6585dd0bb0",
}

REPAIRED_SCRIPTS = {
    "derive_finite_null_patch_area.py": "bdc85395a5c832077667f6c8a1e323514fd8b52af15ac1cbb7a2de696e5f6e5c",
    "verify_finite_null_patch_area_independent.py": "246a6552cdfcd442739f2fe6d93fe03b0b2361829e5801414fca76693f9167c9",
    "run_catch_proofs.py": "3d1f0727c8b426661c8553e68cada59ed3b9b1dfc4c3c97a4412f29c99a14287",
}

REPAIR_EVIDENCE = {
    "EXTERNAL_REVIEW_RESPONSE.md": "aadf46778a28a074550bb039139095ea3ef16a16c3deac1ec9903384334293c1",
    "REPAIR_PREREGISTRATION.md": "9dad6012e2251886b1506d5c1df23d67ec7ae07836c60122299fe1b148ba6a25",
    "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md": "4852b3a868b2920a1cc2e08c2fe4521a8e1e9b819dc56ea68cb124df700e0dcb",
    "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md": "9d03d3a0a18af04380a8a596dba9afb567bc12780499a51661b94530ef46f862",
}

SOURCE_HASHES = {
    "udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/EXACT_DERIVATION.md":
        "04917cd0336f5c06ee76129f5a8005f5e483e8a6fcdacbb87c96a6e0ad89544c",
    "udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/AUDIT_REPORT.md":
        "b264f4a8959a557884f3e6a668aab68d2831b477caf693f95db7b524c01bd279",
    "udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/EXTERNAL_REVIEW_RESPONSE.md":
        "6d8b02c9ce76d99039318ab03fc0e737a5ab2c456178fae9f66e684c3cce0af5",
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
    checks["repaired_script_hashes"] = all(
        digest(HERE / name) == expected for name, expected in REPAIRED_SCRIPTS.items()
    )
    checks["frozen_external_repair_evidence"] = all(
        digest(HERE / name) == expected for name, expected in REPAIR_EVIDENCE.items()
    )

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    checks["production_44321_of_44321"] = (
        production["status"] == "PASS" and production["assertions"] == 44321
        and production["failed"] == [] and production["preregistration_commit"] == "84cb5264"
        and production["repair_commit"] == "134ecd4a"
        and production["external_repair_preregistration_commit"] == "c2967132"
    )
    checks["independent_14321_of_14321"] = (
        independent["status"] == "PASS" and independent["assertions"] == 14321
        and independent["failed"] == [] and "imports no production" in independent["method"]
        and independent["external_repair_preregistration_commit"] == "c2967132"
    )
    checks["hostile_22_of_22"] = (
        hostile["status"] == "PASS" and hostile["caught"] == hostile["total"] == 22
        and hostile["failed"] == [] and all(hostile["mutations"].values())
        and hostile["external_repair_preregistration_commit"] == "c2967132"
    )
    checks["selected_alternatives"] = production["selected_alternatives"] == [
        "A", "T1", "J1", "M1", "U1", "E1", "C1", "S1", "O1", "L1", "P1"
    ]

    execution = (HERE / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8")
    derivation = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    ledger = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    checks["first_failure_and_repair_recorded"] = all(token in execution for token in (
        "20/21", "text-hook defect", "explicit cusp control", "No alternative, definition",
    ))
    checks["finite_area_formula"] = all(token in derivation for token in (
        "A_{\\rm mult}", "N_s(F,U;y)", "auxiliary positive Riemannian metric", "has cancelled",
    ))
    checks["union_distinction_and_equality"] = all(token in derivation for token in (
        "A_{\\rm union}", "N_s=1", "injectivity is stronger than necessary",
    ))
    checks["critical_and_orientation_branches"] = all(token in derivation for token in (
        "transverse screen rank one or zero", "cusp rather than fold", "signed determinant",
    ))
    checks["mixed_rank_repair"] = all(token in derivation for token in (
        "r_s=1,r_F=2", "image plane is null", "w_g=0",
    )) and production["map_classes"][2] == "mixed_screen_rank_one_ordinary_rank_two_null"
    checks["finite_observer_covariance"] = all(token in derivation for token in (
        "J'_gF\\,d\\Omega_v=J_gF\\,d\\Omega_u", "holding the same numerical", "Null observers remain excluded",
    ))
    checks["metric_only_provenance"] = (
        "area formula" in derivation and "category-A" in derivation
        and "not uniquely diagnostic of UDT" in derivation
        and "PINNED_BY_HABIT" not in ledger
    )
    checks["bounded_physical_scope"] = all(token in audit + lay for token in (
        "brightness", "observational distance", "matter/mass", "`X_max`", "canon",
    ))
    program = (ROOT / "CURRENT_RESEARCH_PROGRAM.md").read_text(encoding="utf-8")
    checks["geometric_not_physical_union_scope"] = (
        "geometric endpoint image-union" in program and "physical image-union" not in program
    )

    allowed_imports = {"__future__", "ast", "hashlib", "json", "math", "os", "pathlib",
                       "random", "subprocess", "sys"}
    imported = set()
    for name in REPAIRED_SCRIPTS:
        tree = ast.parse((HERE / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
    checks["stdlib_only_imports"] = imported <= allowed_imports

    before = package_snapshot()
    replay_production = parse_output("derive_finite_null_patch_area.py")
    replay_independent = parse_output("verify_finite_null_patch_area_independent.py")
    replay_hostile = parse_output("run_catch_proofs.py")
    after = package_snapshot()
    checks["registered_no_write_replays"] = (
        replay_production["assertions"] == 44321 and replay_production["status"] == "PASS"
        and replay_independent["assertions"] == 14321 and replay_independent["status"] == "PASS"
        and replay_hostile["caught"] == replay_hostile["total"] == 22
    )
    checks["aggregate_replay_changes_no_bytes"] = before == after
    checks["no_bytecode_or_special_output"] = not any(
        path.name == "__pycache__" for path in HERE.rglob("*")
    )

    result = {
        "all_passed": all(checks.values()),
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "landing": production["landing"],
        "review_status": "EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_R1_R4_REPAIRS",
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(output, end="")
    if not os.environ.get("UDT_NO_WRITE"):
        (HERE / "VERIFICATION_RESULT.json").write_text(output, encoding="utf-8")
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
