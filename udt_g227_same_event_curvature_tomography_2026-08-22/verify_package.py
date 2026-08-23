#!/usr/bin/env python3
"""Aggregate no-ambiguity verifier and evidence recorder for G227."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SOURCE_HASHES = {
    "udt_g114_common_source_three_observer_network_2026-08-16/AUDIT_REPORT.md": "254e0729245a99125b593f39364f5f56bae987c7ba8a2a965acc0f37ddfe66c6",
    "udt_g212_observer_equivalence_history_bridge_whiteboard_2026-08-22/AUDIT_REPORT.md": "4d2176828922f0036bb65c106f6de3207f187e66e60d26669cdc1acaf24f93b1",
    "udt_g214_completed_tuple_overlap_and_three_observer_carry_2026-08-22/AUDIT_REPORT.md": "9736f98f78ffe7e64c5940984831e06364f1b2b20fd0fcbf0f3e877a49d88af5",
    "udt_g226_null_chain_conformal_symplectic_assembly_2026-08-22/AUDIT_REPORT.md": "1b57ff55688a8e5f1b17827a56c1a66df90e356a6f9d1352099d8fa09fbafc97",
    "udt_g226_null_chain_conformal_symplectic_assembly_2026-08-22/EXACT_DERIVATION.md": "7328366d31e6c704b4881441bf42e9e80d5f8d61ca4ff6da33582a98ed3fc98a",
    "udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/EXACT_DERIVATION.md": "f11744a63faed4a53a0361ef4336afbb56178222b792235213b53fa8cdc02613",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def run(name: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, name], cwd=ROOT, text=True, capture_output=True, timeout=120, check=False
    )
    return {"command": f"{sys.executable} {name}", "returncode": completed.returncode,
            "stdout": completed.stdout, "stderr": completed.stderr}


def main() -> None:
    runs = [run("derive_curvature_tomography.py"), run("verify_independent.py"), run("run_hostile_catches.py")]
    derivation = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((ROOT / "HOSTILE_CATCH_RESULT.json").read_text(encoding="utf-8"))
    source_checks = {path: sha256(REPO / path) == expected for path, expected in SOURCE_HASHES.items()}
    checks = {
        "all_commands_zero": all(item["returncode"] == 0 for item in runs),
        "pilot_disclosed": derivation["whiteboard_pilot_disclosed"] is True,
        "cumulative_ranks": derivation["cumulative_null_ranks"] == [3,6,9,12,15,16,17,18,19],
        "null_rank_19": derivation["null_rank"] == 19,
        "nullity_1": derivation["nullity"] == 1,
        "left_nullity_8": derivation["left_nullity"] == 8,
        "constant_kernel": derivation["kernel_proportional_to_constant_curvature"] is True,
        "timelike_rank_20": derivation["augmented_rank"] == 20,
        "held_out_exact": derivation["held_out_rank_increase"] == 0 and derivation["held_out_prediction_exact"] is True,
        "synthetic_rejected": derivation["synthetic_incompatible_augmented_rank"] == 20,
        "independent_pass": independent["pass"] is True,
        "structural_negative_controls_7_of_7": hostile["pass"] is True and hostile["passed"] == hostile["total"] == 7,
        "source_hashes": all(source_checks.values()),
    }
    result = {"landing": "COMMON_ALGEBRAIC_CURVATURE_COMPATIBILITY_DERIVED_CONDITIONALLY__FROZEN_NINE_DIRECTION_GENERIC_WITNESS_RECOVERS_19_MODES__ONE_CHOSEN_TIMELIKE_SECTIONAL_DATUM_RECOVERS_THE_TWENTIETH",
              "checks": checks, "source_checks": source_checks, "runs": runs, "pass": all(checks.values())}
    (ROOT / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = []
    for item in runs:
        lines.extend((f"$ {item['command']}", item["stdout"].rstrip(), item["stderr"].rstrip(), f"exit={item['returncode']}", ""))
    lines.append(json.dumps({"checks": checks, "pass": result["pass"]}, indent=2, sort_keys=True))
    (ROOT / "RUN_LOG.txt").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(json.dumps({"checks": checks, "pass": result["pass"]}, indent=2, sort_keys=True))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
