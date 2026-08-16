#!/usr/bin/env python3
"""Temp-copy replay and semantic verification of G112."""

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
    return subprocess.run([sys.executable, str(package / script)], cwd=root,
                          text=True, capture_output=True, check=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    parser.add_argument("--pre-blind", action="store_true")
    args = parser.parse_args()
    core = ["PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "FALSIFICATION_CONTRACT.tsv",
            "SOURCE_MANIFEST.tsv", "run_dual_sne.py", "verify_dual_sne_independent.py",
            "run_catch_proofs.py", "PRODUCTION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
            "CATCH_PROOF_RESULT.json", "EXACT_METHOD.md", "AUDIT_REPORT.md", "LAY_REPORT.md",
            "EVIDENCE_GATES.md", "STATUS_LEDGER.tsv", "STATUS.md"]
    blind = ["BLIND_REVIEW_RAW.md", "BLIND_REVIEW_ADJUDICATION.md"]
    required = core if args.pre_blind else core + blind
    present = {name: (HERE / name).is_file() for name in required}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    hashes = {}
    for row in sources:
        path = Path(row["path"])
        if not path.is_absolute():
            path = ROOT / path
        hashes[row["path"]] = sha256(path) == row["sha256"]
    saved_names = ("PRODUCTION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json")
    saved = {name: (HERE / name).read_bytes() for name in saved_names}
    with tempfile.TemporaryDirectory(prefix="udt_g112_verify_") as temp_name:
        temp_root = Path(temp_name)
        temp_package = temp_root / HERE.name
        shutil.copytree(HERE, temp_package)
        for row in sources:
            source = Path(row["path"])
            if source.is_absolute():
                continue
            target = temp_root / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / source, target)
        production = run("run_dual_sne.py", temp_package, temp_root)
        independent = run("verify_dual_sne_independent.py", temp_package, temp_root)
        catches = run("run_catch_proofs.py", temp_package, temp_root)
        replay = {name: saved[name] == (temp_package / name).read_bytes() for name in saved}
        p_result = json.loads((temp_package / "PRODUCTION_RESULT.json").read_text())
        i_result = json.loads((temp_package / "INDEPENDENT_VERIFICATION.json").read_text())
        c_result = json.loads((temp_package / "CATCH_PROOF_RESULT.json").read_text())
    report = (HERE / "AUDIT_REPORT.md").read_text()
    ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
    method = (HERE / "EXACT_METHOD.md").read_text()
    semantic = {
        "distinct_blocks": "distinct pair and sky blocks" in method,
        "screen_conditional": "conditional representative" in method,
        "flux_conditional": "luminosity_transfer\tCONDITIONAL_OBSERVATIONAL_TRANSFER" in ledger,
        "history_open": "complete_metric_history\tOPEN" in ledger,
        "des_warning": "LOW_CHI2_COVARIANCE_OR_EFFECTIVE_DOF_WARNING" in report,
        "no_refit": "no shape optimization" in report,
    }
    if not args.pre_blind:
        semantic["blind_registered"] = "PENDING" not in (HERE / "STATUS.md").read_text()
    result = {"schema": "UDT_G112_PACKAGE_VERIFICATION_V1",
              "mode": "PRE_BLIND" if args.pre_blind else "FINAL",
              "required_files": present, "all_required_files_present": all(present.values()),
              "source_hashes": hashes, "all_19_source_hashes_match": len(hashes) == 19 and all(hashes.values()),
              "production_returncode": production.returncode,
              "independent_returncode": independent.returncode,
              "catch_returncode": catches.returncode,
              "production_pass": p_result["all_checks_pass"],
              "independent_pass": i_result["all_checks_pass"],
              "catches_pass": c_result["all_checks_pass"],
              "replay_matches_saved": replay, "all_replays_match": all(replay.values()),
              "semantic_checks": semantic, "all_semantic_checks_pass": all(semantic.values())}
    result["all_checks_pass"] = all([result["all_required_files_present"],
        result["all_19_source_hashes_match"], production.returncode == 0,
        independent.returncode == 0, catches.returncode == 0, result["production_pass"],
        result["independent_pass"], result["catches_pass"], result["all_replays_match"],
        result["all_semantic_checks_pass"]])
    serialized = json.dumps(result, indent=2, sort_keys=True)
    if args.write_result:
        (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(serialized + "\n")
    print(serialized)
    for process in (production, independent, catches):
        if process.returncode:
            print(process.stdout)
            print(process.stderr, file=sys.stderr)
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
