#!/usr/bin/env python3
"""Read-only temp-copy replay and semantic verification of G110."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(script: str, package: Path, root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(package / script)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    required = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "SOURCE_MANIFEST.tsv",
        "PRE_G110_CURRENT_SCIENTIFIC_PREMISES.tsv",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "derive_full_differential.py",
        "verify_full_differential_independent.py",
        "run_catch_proofs.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "CONTROL_ATLAS.tsv",
        "EXACT_DERIVATION.md",
        "DEPENDENCY_REGRADE.tsv",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv",
        "STATUS.md",
        "BLIND_REVIEW_RAW.md",
        "BLIND_REVIEW_ADJUDICATION.md",
        "BLIND_REVIEW_FOLLOWUP.md",
    ]
    required_checks = {name: (HERE / name).is_file() for name in required}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    hashes = {
        row["path"]: sha256(ROOT / row["path"]) == row["sha256"] for row in sources
    }

    saved = {
        name: (HERE / name).read_bytes()
        for name in (
            "DERIVATION_RESULT.json",
            "INDEPENDENT_VERIFICATION.json",
            "CATCH_PROOF_RESULT.json",
            "CONTROL_ATLAS.tsv",
        )
    }
    with tempfile.TemporaryDirectory(prefix="udt_g110_verify_") as temp_name:
        temp_root = Path(temp_name)
        temp_package = temp_root / HERE.name
        shutil.copytree(HERE, temp_package)
        for row in sources:
            target = temp_root / row["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / row["path"], target)
        production = run("derive_full_differential.py", temp_package, temp_root)
        independent = run("verify_full_differential_independent.py", temp_package, temp_root)
        catches = run("run_catch_proofs.py", temp_package, temp_root)
        replay = {
            name: saved[name] == (temp_package / name).read_bytes() for name in saved
        }
        production_result = json.loads(
            (temp_package / "DERIVATION_RESULT.json").read_text()
        )
        independent_result = json.loads(
            (temp_package / "INDEPENDENT_VERIFICATION.json").read_text()
        )
        catch_result = json.loads((temp_package / "CATCH_PROOF_RESULT.json").read_text())

    exact = (HERE / "EXACT_DERIVATION.md").read_text()
    report = (HERE / "AUDIT_REPORT.md").read_text()
    ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
    regrade = (HERE / "DEPENDENCY_REGRADE.tsv").read_text()
    semantic = {
        "distinct_blocks_explicit": "TERMINAL_PAIR_AND_SKY_JACOBI_ARE_DISTINCT_BLOCKS" in exact,
        "flat_catch_explicit": "W_\\parallel=0" in exact
        and "\\mathcal D=\\lambda I_2" in exact,
        "history_open": "physical complete metric history remains genuinely supplied and open"
        in exact,
        "zero_rate_scope": "not a universal propagation coordinate" in exact,
        "caustic_typed": "second-order Jacobi map and its derivative remain finite" in exact,
        "g108_regraded_not_erased": "G108_Jacobi_Riccati_algebra" in regrade
        and "SURVIVES_FOR_D_SKY" in regrade,
        "g109_terminal_survives": "G109_terminal_phi_pair" in regrade
        and "SURVIVES_UNCHANGED" in regrade,
        "null_pair_rank_bound": "has rank at most one" in exact
        and "REGULAR_RANK2_STRATUM_EMPTY" in regrade,
        "celestial_carry_explicit": "time-dependent celestial trivialization" in exact,
        "outcomes_sealed": "observational_outcomes\tSEALED" in ledger,
        "blind_review_registered": "VERIFIED_WITH_CAVEATS" in report
        and "rank at most one" in (HERE / "BLIND_REVIEW_RAW.md").read_text(),
        "repair_followup_passed": "REPAIRS_VERIFIED"
        in (HERE / "BLIND_REVIEW_FOLLOWUP.md").read_text(),
    }
    result = {
        "schema": "UDT_G110_PACKAGE_VERIFICATION_V1",
        "required_files": required_checks,
        "all_required_files_present": all(required_checks.values()),
        "source_hashes": hashes,
        "all_source_hashes_match": all(hashes.values()),
        "production_returncode": production.returncode,
        "independent_returncode": independent.returncode,
        "catch_returncode": catches.returncode,
        "replay_matches_saved": replay,
        "all_replays_match": all(replay.values()),
        "production_checks_pass": production_result["all_checks_pass"],
        "independent_checks_pass": independent_result["all_checks_pass"],
        "catch_proofs_pass": catch_result["all_catches_pass"],
        "semantic_checks": semantic,
        "all_semantic_checks_pass": all(semantic.values()),
    }
    result["all_checks_pass"] = all(
        [
            result["all_required_files_present"],
            result["all_source_hashes_match"],
            production.returncode == 0,
            independent.returncode == 0,
            catches.returncode == 0,
            result["all_replays_match"],
            result["production_checks_pass"],
            result["independent_checks_pass"],
            result["catch_proofs_pass"],
            result["all_semantic_checks_pass"],
        ]
    )
    serialized = json.dumps(result, indent=2, sort_keys=True)
    if args.write_result:
        (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(serialized + "\n")
    print(serialized)
    if production.returncode:
        print(production.stdout)
        print(production.stderr, file=sys.stderr)
    if independent.returncode:
        print(independent.stdout)
        print(independent.stderr, file=sys.stderr)
    if catches.returncode:
        print(catches.stdout)
        print(catches.stderr, file=sys.stderr)
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
