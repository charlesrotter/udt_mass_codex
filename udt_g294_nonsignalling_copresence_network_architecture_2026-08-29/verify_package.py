#!/usr/bin/env python3
"""Dependency-aware, no-persistent-output aggregate verifier for G294."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


LANDING_PARTS = (
    "COPRESENCE_IS_COHERENT_AS_NONPROPAGATING_RELATION_NOT_SIGNAL_SPEED",
    "POSITIVE_PAIR_MAGNITUDE_AND_ORIENTED_DEPTH_ARE_COMPATIBLE",
    "GLOBAL_CORRELATION_CAN_COEXIST_WITH_CAUSAL_RESPONSE_SUPPORT",
    "PAIR_RELATIVE_COPRESENCE_GRAPH_DOES_NOT_DERIVE_GLOBAL_NOW",
    "PHYSICAL_GLOBAL_NOW_REQUIRES_OWNED_INTEGRABLE_TIMELIKE_STRUCTURE",
    "CE_ALONE_DOES_NOT_ATTACH_DEPTH_TO_LENGTH",
    "CURRENT_COPRESENCE_SEMANTICS_DO_NOT_SELECT_HISTORY",
    "COMPLETE_NETWORK_CONSTRAINT_PLUS_CAUSAL_UPDATE_IS_A_WELL_TYPED_MISSING_LAW_ARCHITECTURE",
)
LANDING = "__".join(LANDING_PARTS)

REQUIRED = (
    "OWNER_INPUT.md",
    "MAP.md",
    "PREREGISTRATION.md",
    "REPAIR_PREREGISTRATION.md",
    "PREMISE_LEDGER.tsv",
    "SOURCE_SCOPE.tsv",
    "SOURCE_MANIFEST.tsv",
    "EXACT_DERIVATION.md",
    "ARCHITECTURE_LATTICE.tsv",
    "STATUS_LEDGER.tsv",
    "LAY_REPORT.md",
    "AUDIT_REPORT.md",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "derive_copresence_architecture.py",
    "verify_copresence_independent.py",
    "run_catch_proofs.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path, default=Path("PACKAGE_VERIFICATION_RESULT.json"))
    args = parser.parse_args()

    for name in REQUIRED:
        if not (args.package / name).is_file():
            raise FileNotFoundError(name)

    production = json.loads((args.package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((args.package / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((args.package / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    if production["landing_candidate"] != LANDING:
        raise AssertionError("landing mismatch")
    if not production["all_pass"] or not independent["all_pass"] or not catches["all_pass"]:
        raise AssertionError("evidence route failed")
    if independent["production_imported"] or independent["production_result_read"]:
        raise AssertionError("independent route contaminated")

    report = (args.package / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    for token in LANDING_PARTS:
        if token not in report:
            raise AssertionError(f"report missing landing token: {token}")

    with tempfile.TemporaryDirectory(prefix="g294_verify_") as temp_dir:
        temp = Path(temp_dir)
        prod_out = temp / "DERIVATION_RESULT.json"
        indep_out = temp / "INDEPENDENT_VERIFICATION.json"
        catch_out = temp / "CATCH_PROOF_RESULT.json"
        subprocess.run(
            [sys.executable, str(args.package / "derive_copresence_architecture.py"), "--output", str(prod_out)],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        subprocess.run(
            [sys.executable, str(args.package / "verify_copresence_independent.py"), "--output", str(indep_out)],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        subprocess.run(
            [
                sys.executable,
                str(args.package / "run_catch_proofs.py"),
                "--package",
                str(args.package),
                "--output",
                str(catch_out),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        replay_equal = {
            "production": digest(prod_out) == digest(args.package / "DERIVATION_RESULT.json"),
            "independent": digest(indep_out) == digest(args.package / "INDEPENDENT_VERIFICATION.json"),
            "catches": digest(catch_out) == digest(args.package / "CATCH_PROOF_RESULT.json"),
        }
        if not all(replay_equal.values()):
            raise AssertionError(f"non-deterministic replay: {replay_equal}")

    result = {
        "all_pass": True,
        "required_file_count": len(REQUIRED),
        "production_assertions": production["assertion_count"],
        "independent_assertions": independent["assertion_count"],
        "hostile_catches": catches["catch_count"],
        "semantic_gates": catches["semantic_gate_count"],
        "byte_identical_replays": replay_equal,
        "persistent_runtime_output": False,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
