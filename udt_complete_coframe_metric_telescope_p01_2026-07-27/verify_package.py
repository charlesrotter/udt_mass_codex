#!/usr/bin/env python3
"""Fail-closed mechanical verifier for the banked P01 package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
TAGS = ("0030", "0100", "0300", "1000", "2500")
EXPECTED_RESOLVED = (1024, 1024, 1024, 1021, 9)
EXPECTED_UNRESOLVED = (0, 0, 0, 3, 1015)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    checks: dict[str, bool] = {}
    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_manifest_eight_rows"] = len(sources) == 8
    for row in sources:
        checks[f"source_{row['source_id']}"] = digest(REPO / row["path"]) == row["sha256"]
    result = json.loads((ROOT / "ATLAS_RESULT.json").read_text())
    checks["primary_status_pass"] = result["status"] == "PASS"
    checks["primary_scope_off_shell"] = result["epistemic_scope"] == "OFF_SHELL_CONFIGURATION_ATLAS_NOT_DYNAMICAL_SOLUTIONS"
    checks["configuration_total"] = result["totals"]["production_configurations"] == 5120
    checks["all_local_grids_resolved"] = result["totals"]["grid_unresolved"] == 0
    checks["controls_pass"] = result["controls"]["pass"] is True
    checks["coefficient_hash"] = result["coefficient_universe_sha256"] == "c381c8b87183d8e771e13ad02a68637465d446cd29ca9488d49bcde5303b390e"
    names = result["feature_names"]
    unresolved_index = names.index("transport_numerically_unresolved")
    nontrivial_index = names.index("holonomy_nontrivial")
    coefficient_reference = None
    for tag, expected_resolved, expected_unresolved in zip(TAGS, EXPECTED_RESOLVED, EXPECTED_UNRESOLVED):
        npz_path = ROOT / f"ATLAS_shell_{tag}_N1024_T17_X33_MEXP64.npz"
        summary_path = ROOT / f"ATLAS_shell_{tag}_SUMMARY.json"
        summary = json.loads(summary_path.read_text())
        with np.load(npz_path, allow_pickle=False) as data:
            coefficients = data["coefficients"]
            features = data["features"]
            feature_names = data["feature_names"].tolist()
        checks[f"shell_{tag}_shape"] = coefficients.shape == (1024, 8, 8) and features.shape == (1024, 23)
        checks[f"shell_{tag}_names"] = feature_names == names
        checks[f"shell_{tag}_summary_hash"] = summary["npz_sha256"] == digest(npz_path)
        checks[f"shell_{tag}_local_resolved"] = summary["grid_unresolved"] == 0 and np.all(features[:, names.index("grid_nonfinite_fraction")] == 0)
        unresolved = features[:, unresolved_index] > 0.5
        resolved = ~unresolved
        checks[f"shell_{tag}_transport_counts"] = int(resolved.sum()) == expected_resolved and int(unresolved.sum()) == expected_unresolved
        checks[f"shell_{tag}_resolved_nontrivial"] = int(np.sum((features[:, nontrivial_index] > 0.5) & resolved)) == expected_resolved
        if coefficient_reference is None:
            coefficient_reference = coefficients
        checks[f"shell_{tag}_same_coefficients"] = np.array_equal(coefficients, coefficient_reference)
    anchor = json.loads((ROOT / "CPU_ANCHOR_VERIFICATION.json").read_text())
    checks["independent_cpu_anchor_pass"] = anchor["status"] == "PASS" and anchor["production_module_imported"] is False and all(anchor["checks"].values())
    checks["anchor_hash_link"] = anchor["anchor_sha256"] == digest(ROOT / "CPU_ANCHOR_GPU.json")
    convergence = json.loads((ROOT / "TRANSPORT_CONVERGENCE.json").read_text())
    checks["transport_refinement"] = convergence["all_errors_reduced"] is True and 3.5 < convergence["median_ratio"] < 4.5
    failed_replay = json.loads((ROOT / "RESOURCE_REPLAY_VERIFICATION.json").read_text())
    scoped_replay = json.loads((ROOT / "RESOURCE_REPLAY_SCOPED_VERIFICATION.json").read_text())
    checks["first_replay_failure_preserved"] = failed_replay["status"] == "FAIL"
    checks["scoped_replay_pass"] = scoped_replay["status"] == "PASS" and all(scoped_replay["checks"].values())
    checks["replay_below_6_gib"] = scoped_replay["replay_peak_memory_bytes"] < 6 * 1024**3
    checks["replay_resolved_transport_tolerance"] = scoped_replay["maximum_resolved_transport_scaled_error"] <= scoped_replay["continuous_scaled_tolerance"]
    checks["failed_attempt_npz_hash"] = digest(ROOT / "failed_production_attempt_01/ATLAS_shell_0030_N1024_T17_X33_MEXP64.npz") == "8ae5106079cd1abbb1faaed3fc7441fd1598f181f1ecef8b8d67272c449f2334"
    checks["failed_attempt_summary_hash"] = digest(ROOT / "failed_production_attempt_01/ATLAS_shell_0030_SUMMARY.json") == "4a122753ee3818be58ca685c48834bcb4acc83b72b37afe271456d1f0ee0ad09"
    census = json.loads((ROOT / "STRUCTURE_CENSUS.json").read_text())
    checks["census_totals"] = census["total_configurations"] == 5120 and census["total_local_point_evaluations"] == 2872320
    checks["all_rays_monotonic"] = all(
        row["strictly_increasing_across_all_five_shells"] == 1024 and row["not_strictly_increasing"] == 0
        for row in census["same_configuration_shell_transitions"].values()
    )
    checks["all_configs_causal_type_changing"] = all(row["causal_presence"]["timelike_and_spacelike_present"] == 1024 for row in census["shells"])
    checks["no_registered_tidal_repetition"] = all(row["repeated_screen_tidal"]["registered_repeated_grid_points"] == 0 for row in census["shells"])
    with (ROOT / "FALSIFICATION_CONTRACT.tsv").open(newline="") as handle:
        catches = list(csv.DictReader(handle, delimiter="\t"))
    checks["twenty_catch_rules_present"] = len(catches) == 20 and len({row["catch_id"] for row in catches}) == 20
    checks["reports_scope_stamped"] = all(
        token in (ROOT / "AUDIT_REPORT.md").read_text()
        for token in ("off-shell", "not a physical", "not metric-selected", "OPEN", "bounded scope")
    )
    checks = {name: bool(value) for name, value in checks.items()}
    output = {
        "schema": "udt-complete-coframe-metric-telescope-p01-verification-1.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "checks": checks,
    }
    (ROOT / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))
    raise SystemExit(0 if output["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
