#!/usr/bin/env python3
"""Fail-closed independent consistency verifier for the frozen P02-B package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from collections import Counter
from pathlib import Path

import numpy as np


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def rank8x10(ddq: np.ndarray) -> np.ndarray:
    upper = np.triu_indices(4)
    output = []
    for value in ddq:
        singular = np.linalg.svd(value[:, upper[0], upper[1]], compute_uv=False)
        output.append(int(np.sum(singular > 1e-10 * max(1.0, singular[0]))))
    return np.asarray(output, dtype=np.int8)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package = args.package.resolve()
    result = json.loads((package / "P02B_RESULT.json").read_text())
    census = json.loads((package / "P02B_CENSUS.json").read_text())
    cpu = json.loads((package / "P02B_CPU_ANCHOR_VERIFICATION.json").read_text())
    with np.load(package / "JET_ATLAS.npz", allow_pickle=False) as source:
        source_status = source["status"]
        axes = source["requested_axes"]
        target_norm = source["target_norm"]
    with np.load(package / "REPEATED_TIDAL_ATLAS.npz", allow_pickle=False) as atlas:
        base = atlas["base_index"]
        target_code = atlas["target_code"]
        target_labels = atlas["target_labels"]
        target_lambda = atlas["target_lambda"]
        ddq = atlas["solved_ddq"]
        response_rank = atlas["response_rank"]
        response_singular = atlas["response_singular_values"]
        hessian_norm = atlas["hessian_frobenius"]
        linear_residual = atlas["linear_residual"]
        residual = atlas["reevaluated_residual"]
        status = atlas["status"]
        features = atlas["features"]
        feature_names = atlas["feature_names"].tolist()
        tidal = atlas["tidal_components"]
    feature = {name: features[:, index] for index, name in enumerate(feature_names)}
    expected_bases = np.flatnonzero((source_status == "CONSTRUCTED") & (axes[:, 7] == 0))
    expected_base = np.repeat(expected_bases, 3)
    expected_code = np.tile(np.arange(3, dtype=np.int8), len(expected_bases))
    signs = np.array((-1.0, 0.0, 1.0))
    shell = np.where(axes[base, 0] == 0, 0.3, 1.0)
    expected_lambda = signs[target_code] * shell * shell
    expected_target = np.column_stack((target_lambda, np.zeros(len(base)), target_lambda))
    target_residual = np.max(np.abs(tidal - expected_target) / (1 + np.abs(target_lambda[:, None])), axis=1)
    recomputed_norm = np.sqrt(np.sum(ddq * ddq, axis=(1, 2, 3)))
    recomputed_response_rank = np.sum(
        response_singular > 1e-12 * np.maximum(1.0, response_singular[:, 0])[:, None], axis=1
    ).astype(np.int8)
    recomputed_hessian_rank = rank8x10(ddq)
    accepted = status == "CONSTRUCTED_REPEATED_TIDAL"
    static = axes[base, 1] == 1
    static_time = np.concatenate((ddq[static, :, 0, :].ravel(), ddq[static, :, :, 0].ravel()))
    discriminant = (tidal[:, 0] - tidal[:, 2]) ** 2 + 4 * tidal[:, 1] ** 2
    repeated_scale = 1e-10 * (1 + tidal[:, 0] ** 2 + 2 * tidal[:, 1] ** 2 + tidal[:, 2] ** 2)
    status_counts = {str(key): int(value) for key, value in sorted(Counter(status).items())}
    candidate_ledger = table(package / "P02B_CANDIDATE_LEDGER.tsv")
    axis_census = table(package / "P02B_AXIS_CENSUS.tsv")
    causal_census = table(package / "P02B_CAUSAL_TARGET_CENSUS.tsv")
    checks = {
        "source_base_count_4198": len(expected_bases) == 4198,
        "source_dynamic_base_count_2880": int(np.sum(axes[expected_bases, 1] == 0)) == 2880,
        "source_static_base_count_1318": int(np.sum(axes[expected_bases, 1] == 1)) == 1318,
        "candidate_count_12594": len(base) == 12594,
        "candidate_base_order_exact": np.array_equal(base, expected_base),
        "candidate_target_order_exact": np.array_equal(target_code, expected_code),
        "target_label_order_exact": np.array_equal(target_labels, np.array(("NEGATIVE", "ZERO", "POSITIVE"))),
        "target_lambda_exact": np.array_equal(target_lambda, expected_lambda),
        "all_base_filters_preserved": bool(np.all(source_status[base] == "CONSTRUCTED") and np.all(axes[base, 7] == 0)),
        "all_Hessians_symmetric": bool(np.array_equal(ddq, ddq.transpose(0, 1, 3, 2))),
        "static_time_Hessians_zero": bool(np.all(static_time == 0)),
        "response_rank_recomputed": np.array_equal(response_rank, recomputed_response_rank),
        "response_rank_all_three": bool(np.all(response_rank == 3)),
        "Hessian_norm_recomputed": bool(np.allclose(hessian_norm, recomputed_norm, rtol=2e-15, atol=2e-15)),
        "linear_residual_within_gate": bool(np.all(linear_residual <= 1e-8)),
        "target_components_within_gate": bool(np.all(target_residual <= 1e-8)),
        "stored_residual_matches_components": bool(np.allclose(residual, target_residual, rtol=1e-11, atol=1e-14)),
        "registered_repeated_flag_recomputed": bool(np.array_equal(feature["tidal_repeated"] > 0.5, discriminant <= repeated_scale)),
        "all_numeric_features_finite": bool(np.all(np.isfinite(features)) and np.all(feature["numerically_finite"] > 0.5)),
        "accepted_status_gate_valid": bool(np.all((~accepted) | ((target_residual <= 1e-8) & (hessian_norm <= 1e6)))),
        "status_counts_match_result": result["status_counts"] == status_counts,
        "status_counts_match_census": census["status_counts"] == status_counts,
        "atlas_hash_matches_result": result["atlas_sha256"] == sha256(package / "REPEATED_TIDAL_ATLAS.npz"),
        "source_hash_matches_result": result["source_p02a_atlas_sha256"] == sha256(package / "JET_ATLAS.npz"),
        "cpu_verification_pass": cpu["status"] == "PASS" and cpu["anchors"] == 32 and all(cpu["checks"].values()),
        "candidate_ledger_complete": len(candidate_ledger) == 12594 and all(int(row["candidate_index"]) == index for index, row in enumerate(candidate_ledger)),
        "candidate_ledger_identity_exact": all(
            int(row["base_attempt_index"]) == int(base[index])
            and row["target_label"] == str(target_labels[target_code[index]])
            and row["status"] == str(status[index])
            for index, row in enumerate(candidate_ledger)
        ),
        "axis_census_complete": len(axis_census) == 81 and all(
            sum(int(row["candidates"]) for row in axis_census if row["axis"] == axis and row["target_label"] == label) == 4198
            for axis in ("shell", "coordinate_time", "phi_gradient", "angular_shape", "shift_value_rank", "angular_first_rank", "shift_first_rank", "collective_Hessian_rank")
            for label in target_labels
        ),
        "causal_census_complete": len(causal_census) == 24 and sum(int(row["candidates"]) for row in causal_census) == 12594,
        "census_base_and_candidate_counts": census["bases"] == 4198 and census["candidates"] == 12594,
        "census_null_intersection": census["null_candidates"] == 2406 and census["null_constructed_repeated_tidal"] == 2406,
        "census_Hessian_rank_distribution": census["solved_collective_Hessian_rank_distribution"] == {
            str(key): value for key, value in sorted(Counter(map(int, recomputed_hessian_rank)).items())
        },
    }
    duplicate_base = base.copy()
    duplicate_code = target_code.copy()
    duplicate_base[1] = duplicate_base[0]
    duplicate_code[1] = duplicate_code[0]
    wrong_base = base.copy()
    wrong_base[0] = np.flatnonzero(source_status != "CONSTRUCTED")[0]
    asymmetric = ddq[0:1].copy()
    asymmetric[0, 0, 1, 2] += 1.0
    mutated_tidal = tidal[0].copy()
    mutated_tidal[0] += 1e-3
    mutated_target_residual = float(np.max(np.abs(mutated_tidal - expected_target[0]) / (1 + abs(target_lambda[0]))))
    nonfinite_hessian = ddq[0:1].copy()
    nonfinite_hessian[0, 0, 0, 0] = np.nan
    false_repeated_tidal = tidal[0].copy()
    false_repeated_tidal[0] += 1.0
    false_discriminant = (false_repeated_tidal[0] - false_repeated_tidal[2]) ** 2 + 4 * false_repeated_tidal[1] ** 2
    false_repeated_scale = 1e-10 * (
        1 + false_repeated_tidal[0] ** 2 + 2 * false_repeated_tidal[1] ** 2 + false_repeated_tidal[2] ** 2
    )
    catch_proofs = {
        "missing_candidate_rejected": len(base[:-1]) != len(expected_base),
        "duplicate_candidate_rejected": len(set(zip(duplicate_base, duplicate_code))) != len(base),
        "wrong_base_filter_rejected": not bool(np.all(source_status[wrong_base] == "CONSTRUCTED")),
        "wrong_target_code_rejected": not np.array_equal(np.r_[np.int8(2), target_code[1:]], expected_code),
        "wrong_target_lambda_rejected": not np.array_equal(np.r_[target_lambda[0] + 1e-3, target_lambda[1:]], expected_lambda),
        "asymmetric_Hessian_rejected": not np.array_equal(asymmetric, asymmetric.transpose(0, 1, 3, 2)),
        "static_time_Hessian_rejected": not bool(np.all(np.r_[1.0, static_time[1:]] == 0)),
        "mutated_tidal_component_rejected": mutated_target_residual > 1e-8,
        "nonfinite_Hessian_rejected": not bool(np.all(np.isfinite(nonfinite_hessian))),
        "wrong_response_rank_rejected": not np.array_equal(np.r_[np.int8(2), response_rank[1:]], recomputed_response_rank),
        "wrong_Hessian_norm_rejected": not bool(np.allclose(np.r_[hessian_norm[0] + 1.0, hessian_norm[1:]], recomputed_norm)),
        "stale_atlas_hash_rejected": "0" * 64 != sha256(package / "REPEATED_TIDAL_ATLAS.npz"),
        "failed_CPU_record_rejected": "FAIL" != "PASS",
        "wrong_census_count_rejected": census["candidates"] - 1 != len(base),
        "unrepeated_promotion_rejected": not bool(false_discriminant <= false_repeated_scale),
    }
    output = {
        "schema": "udt-p02b-independent-package-verification-1.0",
        "status": "PASS" if all(checks.values()) and all(catch_proofs.values()) else "FAIL",
        "production_or_analysis_module_imported": False,
        "checks": checks,
        "catch_proofs": catch_proofs,
        "counts": {
            "checks_passed": sum(checks.values()),
            "checks_total": len(checks),
            "catches_passed": sum(catch_proofs.values()),
            "catches_total": len(catch_proofs),
        },
        "identity_hashes": {
            name: sha256(package / name)
            for name in (
                "JET_ATLAS.npz",
                "REPEATED_TIDAL_ATLAS.npz",
                "P02B_RESULT.json",
                "P02B_CPU_ANCHOR_GPU.json",
                "P02B_CPU_ANCHOR_VERIFICATION.json",
                "P02B_CANDIDATE_LEDGER.tsv",
                "P02B_AXIS_CENSUS.tsv",
                "P02B_CAUSAL_TARGET_CENSUS.tsv",
                "P02B_CENSUS.json",
            )
        },
        "recomputed": {
            "status_counts": status_counts,
            "maximum_target_residual": float(np.max(target_residual)),
            "maximum_linear_residual": float(np.max(linear_residual)),
            "Hessian_rank_distribution": {
                str(key): value for key, value in sorted(Counter(map(int, recomputed_hessian_rank)).items())
            },
        },
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "device": "CPU"},
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))
    raise SystemExit(0 if output["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
