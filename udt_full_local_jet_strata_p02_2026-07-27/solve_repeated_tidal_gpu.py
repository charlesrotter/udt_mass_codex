#!/usr/bin/env python3
"""P02-B affine Hessian-response construction of repeated screen tides."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import platform
import sys
import time
from pathlib import Path

import numpy as np
import torch


TARGET_LABELS = ("NEGATIVE", "ZERO", "POSITIVE")
HESSIAN_PAIRS = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3))


def load_evaluator(package: Path):
    path = package / "full_local_jet_atlas_gpu.py"
    spec = importlib.util.spec_from_file_location("p02b_frozen_gpu_evaluator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def tidal_components(evaluator, q: torch.Tensor, dq: torch.Tensor, ddq: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    E = evaluator.coframe_jets(q, dq, ddq)
    geo = evaluator.geometry(E, evaluator.metric_jets(E))
    r = geo["rframe"]
    t22 = r[:, 2, 0, 2, 0]
    t23 = 0.5 * (r[:, 2, 0, 3, 0] + r[:, 3, 0, 2, 0])
    t33 = r[:, 3, 0, 3, 0]
    return torch.stack((t22, t23, t33), dim=-1), geo["g"], geo["scalar"]


def response_batch(evaluator, q: np.ndarray, dq: np.ndarray, static: bool, device: torch.device) -> tuple[np.ndarray, np.ndarray, list[tuple[int, int, int]]]:
    allowed_pairs = [pair for pair in HESSIAN_PAIRS if not static or (pair[0] != 0 and pair[1] != 0)]
    variables = [(amplitude, a, b) for amplitude in range(8) for a, b in allowed_pairs]
    width = len(variables) + 1
    batch = len(q)
    q_expanded = torch.tensor(np.repeat(q, width, axis=0), dtype=torch.float64, device=device)
    dq_expanded = torch.tensor(np.repeat(dq, width, axis=0), dtype=torch.float64, device=device)
    ddq_expanded = torch.zeros((batch * width, 8, 4, 4), dtype=torch.float64, device=device)
    for variable_index, (amplitude, a, b) in enumerate(variables):
        rows = torch.arange(batch, device=device) * width + variable_index + 1
        ddq_expanded[rows, amplitude, a, b] = 1.0
        ddq_expanded[rows, amplitude, b, a] = 1.0
    tidal, _, _ = tidal_components(evaluator, q_expanded, dq_expanded, ddq_expanded)
    tidal = tidal.reshape(batch, width, 3)
    baseline = tidal[:, 0]
    response = tidal[:, 1:] - baseline[:, None, :]
    return baseline.detach().cpu().numpy(), response.detach().cpu().numpy(), variables


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--response-base-batch", type=int, default=8)
    parser.add_argument("--evaluation-batch", type=int, default=512)
    parser.add_argument("--production", action="store_true")
    args = parser.parse_args()
    if args.production and (args.device, args.response_base_batch, args.evaluation_batch) != ("cuda:0", 8, 512):
        raise SystemExit("P02-B production arguments differ from preregistration")
    package = args.package.resolve()
    outputs = ("REPEATED_TIDAL_ATLAS.npz", "P02B_RESULT.json", "P02B_CPU_ANCHOR_GPU.json")
    if any((package / name).exists() for name in outputs):
        raise FileExistsError("P02-B production output already exists")
    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    evaluator = load_evaluator(package)
    start = time.time()
    with np.load(package / "JET_ATLAS.npz", allow_pickle=False) as data:
        q_all = data["q"]
        dq_all = data["dq"]
        status_all = data["status"]
        axes_all = data["requested_axes"]
        target_norm_all = data["target_norm"]
    base_mask = (status_all == "CONSTRUCTED") & (axes_all[:, 7] == 0)
    base_indices = np.flatnonzero(base_mask)
    if len(base_indices) != 4198 or np.sum(axes_all[base_indices, 1] == 0) != 2880 or np.sum(axes_all[base_indices, 1] == 1) != 1318:
        raise AssertionError("P02-B frozen base count mismatch")
    candidate_count = len(base_indices) * 3
    candidate_base = np.repeat(base_indices, 3)
    target_code = np.tile(np.arange(3, dtype=np.int8), len(base_indices))
    base_position = {int(base_index): position for position, base_index in enumerate(base_indices)}
    solved_ddq = np.zeros((candidate_count, 8, 4, 4), dtype=np.float64)
    response_rank = np.zeros(candidate_count, dtype=np.int8)
    response_singular = np.zeros((candidate_count, 3), dtype=np.float64)
    hessian_norm = np.full(candidate_count, np.nan)
    linear_residual = np.full(candidate_count, np.nan)
    preliminary = np.empty(candidate_count, dtype="U32")
    target_lambda = np.empty(candidate_count, dtype=np.float64)
    affine_control_errors = []
    peak_memory = 0
    for static_code in (0, 1):
        group = base_indices[axes_all[base_indices, 1] == static_code]
        for offset in range(0, len(group), args.response_base_batch):
            selected = group[offset : offset + args.response_base_batch]
            baseline, response, variables = response_batch(evaluator, q_all[selected], dq_all[selected], bool(static_code), device)
            if device.type == "cuda":
                peak_memory = max(peak_memory, torch.cuda.max_memory_allocated(device))
            for local, base_index in enumerate(selected):
                A = response[local].T
                singular = np.linalg.svd(A, compute_uv=False)
                rank = int(np.sum(singular > 1e-12 * max(1.0, singular[0])))
                if len(affine_control_errors) < 128:
                    for phase in (0.31, 0.73):
                        coefficients = 0.2 * np.sin(np.arange(A.shape[1]) * phase + base_index * 0.01)
                        ddq_control = np.zeros((1, 8, 4, 4))
                        for coefficient, (amplitude, a, b) in zip(coefficients, variables):
                            ddq_control[0, amplitude, a, b] = coefficient
                            ddq_control[0, amplitude, b, a] = coefficient
                        direct, _, _ = tidal_components(
                            evaluator,
                            torch.tensor(q_all[base_index : base_index + 1], dtype=torch.float64, device=device),
                            torch.tensor(dq_all[base_index : base_index + 1], dtype=torch.float64, device=device),
                            torch.tensor(ddq_control, dtype=torch.float64, device=device),
                        )
                        predicted = baseline[local] + A @ coefficients
                        error = np.max(np.abs(direct.detach().cpu().numpy()[0] - predicted) / (1 + np.abs(predicted)))
                        affine_control_errors.append(float(error))
                shell = 0.3 if axes_all[base_index, 0] == 0 else 1.0
                for code, sign in enumerate((-1.0, 0.0, 1.0)):
                    candidate = 3 * base_position[int(base_index)] + code
                    lam = sign * shell * shell
                    target_lambda[candidate] = lam
                    right = np.array((lam, 0.0, lam)) - baseline[local]
                    try:
                        solution, _, _, _ = np.linalg.lstsq(A, right, rcond=1e-12)
                    except np.linalg.LinAlgError:
                        preliminary[candidate] = "NUMERICALLY_NONFINITE"
                        continue
                    prediction = baseline[local] + A @ solution
                    residual = float(np.max(np.abs(prediction - np.array((lam, 0.0, lam))) / (1 + abs(lam))))
                    response_rank[candidate] = rank
                    response_singular[candidate, : len(singular)] = singular
                    linear_residual[candidate] = residual
                    for coefficient, (amplitude, a, b) in zip(solution, variables):
                        solved_ddq[candidate, amplitude, a, b] = coefficient
                        solved_ddq[candidate, amplitude, b, a] = coefficient
                    hessian_norm[candidate] = np.linalg.norm(solved_ddq[candidate])
                    if not np.all(np.isfinite(solution)) or not math.isfinite(residual):
                        preliminary[candidate] = "NUMERICALLY_NONFINITE"
                    elif residual > 1e-8 and rank < 3:
                        preliminary[candidate] = "RESPONSE_RANK_INSUFFICIENT"
                    elif residual > 1e-8:
                        preliminary[candidate] = "RESIDUAL_FAILED"
                    else:
                        preliminary[candidate] = "PENDING_REEVALUATION"
    if len(affine_control_errors) != 128 or max(affine_control_errors) > 1e-10:
        raise AssertionError(f"affine control failed: {max(affine_control_errors)}")
    features = np.full((candidate_count, len(evaluator.FEATURE_NAMES)), np.nan)
    tidal = np.full((candidate_count, 3), np.nan)
    reevaluated_residual = np.full(candidate_count, np.nan)
    final_status = preliminary.copy()
    pending = np.flatnonzero(preliminary == "PENDING_REEVALUATION")
    for offset in range(0, len(pending), args.evaluation_batch):
        selected = pending[offset : offset + args.evaluation_batch]
        bases = candidate_base[selected]
        q = torch.tensor(q_all[bases], dtype=torch.float64, device=device)
        dq = torch.tensor(dq_all[bases], dtype=torch.float64, device=device)
        ddq = torch.tensor(solved_ddq[selected], dtype=torch.float64, device=device)
        target_norm = torch.tensor(target_norm_all[bases], dtype=torch.float64, device=device)
        evaluated, _ = evaluator.evaluate(q, dq, ddq, target_norm)
        tidal_value, _, _ = tidal_components(evaluator, q, dq, ddq)
        tidal_np = tidal_value.detach().cpu().numpy()
        features[selected] = evaluated
        tidal[selected] = tidal_np
        targets = np.column_stack((target_lambda[selected], np.zeros(len(selected)), target_lambda[selected]))
        residual = np.max(np.abs(tidal_np - targets) / (1 + np.abs(target_lambda[selected, None])), axis=1)
        reevaluated_residual[selected] = residual
        for local, candidate in enumerate(selected):
            if not np.all(np.isfinite(evaluated[local])) or not np.all(np.isfinite(tidal_np[local])):
                final_status[candidate] = "NUMERICALLY_NONFINITE"
            elif hessian_norm[candidate] > 1e6:
                final_status[candidate] = "ILL_CONDITIONED_LARGE_HESSIAN"
            elif residual[local] <= 1e-8:
                final_status[candidate] = "CONSTRUCTED_REPEATED_TIDAL"
            elif response_rank[candidate] < 3:
                final_status[candidate] = "RESPONSE_RANK_INSUFFICIENT"
            else:
                final_status[candidate] = "RESIDUAL_FAILED"
        if device.type == "cuda":
            peak_memory = max(peak_memory, torch.cuda.max_memory_allocated(device))
    if peak_memory > 2 * 1024**3:
        raise RuntimeError(f"P02-B memory gate exceeded: {peak_memory}")
    np.savez_compressed(
        package / "REPEATED_TIDAL_ATLAS.npz",
        base_index=candidate_base,
        target_code=target_code,
        target_labels=np.array(TARGET_LABELS),
        target_lambda=target_lambda,
        solved_ddq=solved_ddq,
        response_rank=response_rank,
        response_singular_values=response_singular,
        hessian_frobenius=hessian_norm,
        linear_residual=linear_residual,
        reevaluated_residual=reevaluated_residual,
        status=final_status,
        features=features,
        feature_names=np.array(evaluator.FEATURE_NAMES),
        tidal_components=tidal,
        tidal_component_names=np.array(("T22", "T23", "T33")),
    )
    accepted = np.flatnonzero(final_status == "CONSTRUCTED_REPEATED_TIDAL")
    if len(accepted) < 32:
        raise RuntimeError("fewer than 32 accepted P02-B CPU anchors")
    anchor_candidates = accepted[np.linspace(0, len(accepted) - 1, 32, dtype=int)]
    bases = candidate_base[anchor_candidates]
    q_anchor = torch.tensor(q_all[bases], dtype=torch.float64, device=device)
    dq_anchor = torch.tensor(dq_all[bases], dtype=torch.float64, device=device)
    ddq_anchor = torch.tensor(solved_ddq[anchor_candidates], dtype=torch.float64, device=device)
    target_anchor = torch.tensor(target_norm_all[bases], dtype=torch.float64, device=device)
    anchor_features, anchor_metric = evaluator.evaluate(q_anchor, dq_anchor, ddq_anchor, target_anchor)
    anchor = {
        "schema": "udt-p02b-repeated-tidal-gpu-cpu-anchor-1.0",
        "candidate_indices": anchor_candidates.tolist(),
        "base_indices": bases.tolist(),
        "q": q_all[bases].tolist(),
        "dq": dq_all[bases].tolist(),
        "ddq": solved_ddq[anchor_candidates].tolist(),
        "metric": anchor_metric.detach().cpu().tolist(),
        "scalar": anchor_features[:, evaluator.FEATURE_NAMES.index("scalar_curvature")].tolist(),
        "dphi_norm": anchor_features[:, evaluator.FEATURE_NAMES.index("dphi_norm")].tolist(),
        "tidal_components": tidal[anchor_candidates].tolist(),
    }
    (package / "P02B_CPU_ANCHOR_GPU.json").write_text(json.dumps(anchor, indent=2, sort_keys=True) + "\n")
    unique_status, status_count = np.unique(final_status, return_counts=True)
    result = {
        "schema": "udt-p02b-repeated-tidal-result-1.0",
        "status": "PASS",
        "epistemic_scope": "LOCAL_AFFINE_HESSIAN_RESPONSE_WITNESSES_NOT_SELECTED_OR_GLOBAL_SOLUTIONS",
        "bases": len(base_indices),
        "candidates": candidate_count,
        "status_counts": {str(name): int(count) for name, count in zip(unique_status, status_count)},
        "affine_control_max_scaled_error": max(affine_control_errors),
        "accepted_max_reevaluated_residual": float(np.max(reevaluated_residual[accepted])),
        "accepted_hessian_norm_range": {
            "minimum": float(np.min(hessian_norm[accepted])),
            "median": float(np.median(hessian_norm[accepted])),
            "maximum": float(np.max(hessian_norm[accepted])),
        },
        "atlas_sha256": hashlib.sha256((package / "REPEATED_TIDAL_ATLAS.npz").read_bytes()).hexdigest(),
        "source_p02a_atlas_sha256": hashlib.sha256((package / "JET_ATLAS.npz").read_bytes()).hexdigest(),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "torch": torch.__version__,
            "device": torch.cuda.get_device_name(device) if device.type == "cuda" else str(device),
            "dtype": "float64",
            "peak_memory_bytes": peak_memory,
            "wall_seconds": time.time() - start,
            "pid": os.getpid(),
        },
        "maximum_conclusion": "LOCAL_CONSTRUCTIBILITY_OR_RESPONSE_OBSTRUCTION_FOR_THREE_NORMALIZED_REPEATED_TIDAL_TARGETS_ON_THE_EXACT_FROZEN_BASES",
    }
    (package / "P02B_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
