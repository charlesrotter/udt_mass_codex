#!/usr/bin/env python3
"""Read-only temp-copy replay and semantic verification of G111."""

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
        [sys.executable, str(package / script)], cwd=root, text=True,
        capture_output=True, check=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    parser.add_argument("--pre-blind", action="store_true")
    args = parser.parse_args()
    core_required = [
        "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "FALSIFICATION_CONTRACT.tsv",
        "SOURCE_MANIFEST.tsv", "CORRECTION_RECORD.md", "derive_nonflat_replay.py",
        "verify_nonflat_exact.py", "verify_nonflat_independent.py", "run_catch_proofs.py",
        "DERIVATION_RESULT.json", "EXACT_COMPONENT_HASHES.json",
        "INDEPENDENT_EXACT_VERIFICATION.json", "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json", "CONTROL_ATLAS.tsv",
        "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md", "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv", "STATUS.md",
    ]
    blind_required = ["BLIND_REVIEW_RAW.md", "BLIND_REVIEW_ADJUDICATION.md", "BLIND_REVIEW_FOLLOWUP.md"]
    required = core_required if args.pre_blind else core_required + blind_required
    required_checks = {name: (HERE / name).is_file() for name in required}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    hashes = {row["path"]: sha256(ROOT / row["path"]) == row["sha256"] for row in sources}
    saved_names = ("DERIVATION_RESULT.json", "EXACT_COMPONENT_HASHES.json", "INDEPENDENT_EXACT_VERIFICATION.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json", "CONTROL_ATLAS.tsv")
    saved = {name: (HERE / name).read_bytes() for name in saved_names}
    with tempfile.TemporaryDirectory(prefix="udt_g111_verify_") as temp_name:
        temp_root = Path(temp_name)
        temp_package = temp_root / HERE.name
        shutil.copytree(HERE, temp_package)
        for row in sources:
            target = temp_root / row["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / row["path"], target)
        production = run("derive_nonflat_replay.py", temp_package, temp_root)
        exact_independent = run("verify_nonflat_exact.py", temp_package, temp_root)
        independent = run("verify_nonflat_independent.py", temp_package, temp_root)
        catches = run("run_catch_proofs.py", temp_package, temp_root)
        replay = {name: saved[name] == (temp_package / name).read_bytes() for name in saved}
        production_result = json.loads((temp_package / "DERIVATION_RESULT.json").read_text())
        independent_result = json.loads((temp_package / "INDEPENDENT_VERIFICATION.json").read_text())
        exact_independent_result = json.loads((temp_package / "INDEPENDENT_EXACT_VERIFICATION.json").read_text())
        catch_result = json.loads((temp_package / "CATCH_PROOF_RESULT.json").read_text())
    exact = (HERE / "EXACT_DERIVATION.md").read_text()
    correction = (HERE / "CORRECTION_RECORD.md").read_text()
    report = (HERE / "AUDIT_REPORT.md").read_text()
    ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
    semantic = {
        "distinct_blocks": "distinct pair angular and mixed blocks" in ledger,
        "noncommuting_jet_repair": "q12=q21+2 p3" in correction and "Bianchi" in correction,
        "pair_rank_bound": "rank at most one" in exact,
        "sky_vertex": "D_sky(0)=0" in exact and "D_sky'(0)=I" in exact,
        "history_open": "physical_metric_history\tOPEN" in ledger,
        "observations_sealed": "observations\tSEALED" in ledger,
        "independence_qualified": (
            "independent exact exterior-form replay" in report
            and "finite-difference moving-frame replay remains supplementary" in report
        ),
    }
    if not args.pre_blind:
        semantic["blind_review_registered"] = "PENDING" not in (HERE / "STATUS.md").read_text()
    result = {
        "schema": "UDT_G111_PACKAGE_VERIFICATION_V1",
        "mode": "PRE_BLIND" if args.pre_blind else "FINAL",
        "required_files": required_checks,
        "all_required_files_present": all(required_checks.values()),
        "source_hashes": hashes,
        "all_source_hashes_match": all(hashes.values()),
        "production_returncode": production.returncode,
        "independent_returncode": independent.returncode,
        "exact_independent_returncode": exact_independent.returncode,
        "catch_returncode": catches.returncode,
        "replay_matches_saved": replay,
        "all_replays_match": all(replay.values()),
        "production_checks_pass": production_result["all_checks_pass"],
        "independent_checks_pass": independent_result["all_checks_pass"],
        "exact_independent_checks_pass": exact_independent_result["all_checks_pass"],
        "catch_proofs_pass": catch_result["all_checks_pass"],
        "semantic_checks": semantic,
        "all_semantic_checks_pass": all(semantic.values()),
    }
    result["all_checks_pass"] = all([
        result["all_required_files_present"], result["all_source_hashes_match"],
        production.returncode == 0, exact_independent.returncode == 0,
        independent.returncode == 0, catches.returncode == 0,
        result["all_replays_match"], result["production_checks_pass"],
        result["exact_independent_checks_pass"], result["independent_checks_pass"],
        result["catch_proofs_pass"],
        result["all_semantic_checks_pass"],
    ])
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
    if exact_independent.returncode:
        print(exact_independent.stdout)
        print(exact_independent.stderr, file=sys.stderr)
    if catches.returncode:
        print(catches.stdout)
        print(catches.stderr, file=sys.stderr)
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
