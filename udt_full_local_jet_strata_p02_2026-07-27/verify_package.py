#!/usr/bin/env python3
"""Deterministic P02 package verification and replay."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(command, cwd=REPO, env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def main() -> None:
    checks: dict[str, bool] = {}
    required = (
        "PREREGISTRATION.md", "P02B_REPEATED_TIDAL_PREREGISTRATION.md", "AUDIT_REPORT.md",
        "LAY_REPORT.md", "STATUS_LEDGER.tsv", "NEXT_STEP.md", "PREMISE_LEDGER.tsv",
        "JET_ATLAS.npz", "REPEATED_TIDAL_ATLAS.npz", "ATLAS_RESULT.json", "P02B_RESULT.json",
        "CPU_ANCHOR_VERIFICATION.json", "P02B_CPU_ANCHOR_VERIFICATION.json",
        "P02B_PACKAGE_VERIFICATION.json", "STRATUM_CENSUS.json", "P02B_CENSUS.json",
    )
    checks["required_files_present"] = all((ROOT / name).is_file() for name in required)
    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_manifest_seven_rows"] = len(sources) == 7
    checks["source_manifest_replays"] = all(
        (REPO / row["path"]).is_file() and sha256(REPO / row["path"]) == row["sha256"] for row in sources
    )
    atlas_result = json.loads((ROOT / "ATLAS_RESULT.json").read_text())
    p02a_cpu = json.loads((ROOT / "CPU_ANCHOR_VERIFICATION.json").read_text())
    p02a_census = json.loads((ROOT / "STRATUM_CENSUS.json").read_text())
    p02b_result = json.loads((ROOT / "P02B_RESULT.json").read_text())
    p02b_cpu = json.loads((ROOT / "P02B_CPU_ANCHOR_VERIFICATION.json").read_text())
    p02b_verify = json.loads((ROOT / "P02B_PACKAGE_VERIFICATION.json").read_text())
    p02b_census = json.loads((ROOT / "P02B_CENSUS.json").read_text())
    checks.update(
        {
            "P02A_result_pass": atlas_result["status"] == "PASS",
            "P02A_counts_exact": atlas_result["strata"] == 11520 and atlas_result["attempts"] == 23040 and atlas_result["constructed"] == 15459,
            "P02A_status_counts_exact": atlas_result["status_counts"] == {
                "CONSTRUCTED": 15459,
                "NO_CAUSAL_WITNESS_AT_SAMPLED_VALUE": 2973,
                "STRUCTURALLY_INCOMPATIBLE_HESSIAN_RANK": 2304,
                "STRUCTURALLY_INCOMPATIBLE_SHIFT_RANK": 2304,
            },
            "P02A_raw_hash_exact": atlas_result["atlas_npz_sha256"] == sha256(ROOT / "JET_ATLAS.npz"),
            "P02A_universe_hash_exact": atlas_result["stratum_universe_sha256"] == sha256(ROOT / "STRATUM_UNIVERSE.tsv"),
            "P02A_controls_pass": bool(atlas_result["controls"]["pass"]),
            "P02A_cpu_pass": p02a_cpu["status"] == "PASS" and p02a_cpu["anchors"] == 64 and all(p02a_cpu["checks"].values()),
            "P02A_census_scope_exact": p02a_census["constructed"] == 15459 and p02a_census["null_constructed"] == 3119,
            "P02B_result_pass": p02b_result["status"] == "PASS",
            "P02B_counts_exact": p02b_result["bases"] == 4198 and p02b_result["candidates"] == 12594,
            "P02B_status_exact": p02b_result["status_counts"] == {"CONSTRUCTED_REPEATED_TIDAL": 12594},
            "P02B_raw_hash_exact": p02b_result["atlas_sha256"] == sha256(ROOT / "REPEATED_TIDAL_ATLAS.npz"),
            "P02B_cpu_pass": p02b_cpu["status"] == "PASS" and p02b_cpu["anchors"] == 32 and all(p02b_cpu["checks"].values()),
            "P02B_independent_package_pass": p02b_verify["status"] == "PASS" and p02b_verify["counts"] == {
                "checks_passed": 32, "checks_total": 32, "catches_passed": 15, "catches_total": 15
            },
            "P02B_census_counts_exact": p02b_census["bases"] == 4198 and p02b_census["candidates"] == 12594,
            "P02B_null_intersection_exact": p02b_census["null_candidates"] == 2406 and p02b_census["null_constructed_repeated_tidal"] == 2406,
            "P02B_timelike_intersection_exact": p02b_census["timelike_candidates"] == 2412 and p02b_census["timelike_constructed_repeated_tidal"] == 2412,
            "P02B_response_rank_exact": p02b_census["response_rank_distribution"] == {"3": 12594},
        }
    )
    with np.load(ROOT / "JET_ATLAS.npz", allow_pickle=False) as atlas:
        status = atlas["status"]
        features = atlas["features"]
        feature_names = atlas["feature_names"].tolist()
    checks["P02A_npz_status_recomputed"] = dict(Counter(status)) == atlas_result["status_counts"]
    finite_column = feature_names.index("numerically_finite")
    checks["P02A_all_constructed_finite_recomputed"] = bool(np.all(features[status == "CONSTRUCTED", finite_column] > 0.5))
    with np.load(ROOT / "REPEATED_TIDAL_ATLAS.npz", allow_pickle=False) as atlas:
        p02b_status = atlas["status"]
        p02b_rank = atlas["response_rank"]
        p02b_residual = atlas["reevaluated_residual"]
    checks["P02B_npz_status_recomputed"] = dict(Counter(p02b_status)) == p02b_result["status_counts"]
    checks["P02B_all_response_rank_three_recomputed"] = bool(np.all(p02b_rank == 3))
    checks["P02B_residual_gate_recomputed"] = bool(np.all(p02b_residual <= 1e-8))
    with (ROOT / "FALSIFICATION_CONTRACT.tsv").open(newline="") as handle:
        falsifications = list(csv.DictReader(handle, delimiter="\t"))
    checks["P02A_falsification_contract_24"] = len(falsifications) == 24 and len({row["catch_id"] for row in falsifications}) == 24
    with (ROOT / "STATUS_LEDGER.tsv").open(newline="") as handle:
        status_ledger = list(csv.DictReader(handle, delimiter="\t"))
    checks["status_ledger_18_unique"] = len(status_ledger) == 18 and len({row["claim_id"] for row in status_ledger}) == 18
    checks["no_physics_promotion_in_status_ledger"] = all(
        row["epistemic_label"] in {"OBSERVED", "DERIVED", "OPEN", "CONDITIONAL", "VERIFIED-WITH-CAVEATS"}
        for row in status_ledger
    )
    report = (ROOT / "AUDIT_REPORT.md").read_text()
    checks["report_four_gates_present"] = all(token in report for token in ("Preregistered", "Full space or bounded scope justified", "Independently verified", "Every premise audited"))
    checks["report_scope_guard_present"] = all(
        token in report.lower() for token in ("local", "off-shell", "does **not** select", "global finite-cell")
    )
    replay_targets = (
        "STRATUM_LEDGER.tsv", "AXIS_CENSUS.tsv", "STRATUM_CENSUS.json",
        "P02B_CANDIDATE_LEDGER.tsv", "P02B_AXIS_CENSUS.tsv", "P02B_CAUSAL_TARGET_CENSUS.tsv",
        "P02B_CENSUS.json", "CPU_ANCHOR_VERIFICATION.json", "P02B_CPU_ANCHOR_VERIFICATION.json",
        "P02B_PACKAGE_VERIFICATION.json",
    )
    before = {name: sha256(ROOT / name) for name in replay_targets}
    commands = (
        [sys.executable, str(ROOT / "analyze_strata.py"), "--package", str(ROOT)],
        [sys.executable, str(ROOT / "analyze_repeated_tidal.py"), "--package", str(ROOT)],
        [sys.executable, str(ROOT / "verify_full_local_jet_cpu.py"), str(ROOT / "CPU_ANCHOR_GPU.json"), "--output", str(ROOT / "CPU_ANCHOR_VERIFICATION.json"), "--step", "2e-4"],
        [sys.executable, str(ROOT / "verify_repeated_tidal_cpu.py"), str(ROOT / "P02B_CPU_ANCHOR_GPU.json"), "--output", str(ROOT / "P02B_CPU_ANCHOR_VERIFICATION.json"), "--step", "2e-4"],
        [sys.executable, str(ROOT / "verify_p02b_package.py"), "--package", str(ROOT), "--output", str(ROOT / "P02B_PACKAGE_VERIFICATION.json")],
    )
    replay_codes = []
    replay_stdout_hashes = []
    for command in commands:
        process = run(command)
        replay_codes.append(process.returncode)
        replay_stdout_hashes.append(hashlib.sha256(process.stdout.encode()).hexdigest())
    after = {name: sha256(ROOT / name) for name in replay_targets}
    checks["all_replay_commands_pass"] = all(code == 0 for code in replay_codes)
    checks["all_replay_outputs_byte_identical"] = before == after
    output = {
        "schema": "udt-full-local-jet-strata-p02-package-verification-1.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "P02B_catches_passed": p02b_verify["counts"]["catches_passed"],
        "P02B_catches_total": p02b_verify["counts"]["catches_total"],
        "replay_stdout_sha256": replay_stdout_hashes,
        "raw_hashes": {
            "JET_ATLAS.npz": sha256(ROOT / "JET_ATLAS.npz"),
            "REPEATED_TIDAL_ATLAS.npz": sha256(ROOT / "REPEATED_TIDAL_ATLAS.npz"),
        },
        "grade": "VERIFIED-WITH-CAVEATS_NO_FRESH_EXTERNAL_MODEL_SEMANTIC_REVIEW",
    }
    (ROOT / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))
    raise SystemExit(0 if output["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
