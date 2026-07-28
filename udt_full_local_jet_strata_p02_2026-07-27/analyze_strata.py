#!/usr/bin/env python3
"""Deterministic, non-selective descriptive analysis of the frozen P02 atlas."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import torch


def load_evaluator(package: Path):
    path = package / "full_local_jet_atlas_gpu.py"
    spec = importlib.util.spec_from_file_location("p02_frozen_evaluator_for_analysis", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    args = parser.parse_args()
    package = args.package.resolve()
    with (package / "STRATUM_UNIVERSE.tsv").open(newline="") as handle:
        strata = list(csv.DictReader(handle, delimiter="\t"))
    with np.load(package / "JET_ATLAS.npz", allow_pickle=False) as data:
        q = data["q"]
        dq = data["dq"]
        ddq = data["ddq"]
        status = data["status"]
        features = data["features"]
        feature_names = data["feature_names"].tolist()
        stratum_ids = data["stratum_id"]
    if len(strata) != 11520 or len(status) != 23040:
        raise AssertionError("frozen universe size mismatch")
    evaluator = load_evaluator(package)
    constructed = status == "CONSTRUCTED"
    constructed_indices = np.flatnonzero(constructed)
    tidal_norm = np.full(len(status), np.nan)
    tidal_trace = np.full(len(status), np.nan)
    for offset in range(0, len(constructed_indices), 512):
        selected = constructed_indices[offset : offset + 512]
        qt = torch.tensor(q[selected], dtype=torch.float64)
        dqt = torch.tensor(dq[selected], dtype=torch.float64)
        ddqt = torch.tensor(ddq[selected], dtype=torch.float64)
        E = evaluator.coframe_jets(qt, dqt, ddqt)
        geo = evaluator.geometry(E, evaluator.metric_jets(E))
        r = geo["rframe"]
        t22 = r[:, 2, 0, 2, 0]
        t23 = 0.5 * (r[:, 2, 0, 3, 0] + r[:, 3, 0, 2, 0])
        t33 = r[:, 3, 0, 3, 0]
        tidal_norm[selected] = torch.sqrt(t22 * t22 + 2 * t23 * t23 + t33 * t33).numpy()
        tidal_trace[selected] = (t22 + t33).numpy()
    index = {name: feature_names.index(name) for name in feature_names}
    repeated = constructed & (features[:, index["tidal_repeated"]] > 0.5)
    repeated_nonzero = repeated & (tidal_norm > 1e-10)
    flat = constructed & (features[:, index["curvature_operator_rank"]] == 0)
    pair_zero = constructed & (features[:, index["pair_screen_ricci_mixing"]] <= 1e-10)
    null_requested = np.array([row["phi_gradient"] == "NULL" for row in strata for _ in range(2)])
    ledger_rows = []
    for stratum_index, row in enumerate(strata):
        attempt_slice = slice(2 * stratum_index, 2 * stratum_index + 2)
        local_status = status[attempt_slice]
        local_constructed = local_status == "CONSTRUCTED"
        count = int(local_constructed.sum())
        if count == 2:
            classification = "CONSTRUCTIVE_BOTH"
        elif count == 1:
            classification = "CONSTRUCTIVE_ONE"
        elif np.all(local_status == "NO_CAUSAL_WITNESS_AT_SAMPLED_VALUE"):
            classification = "NO_CAUSAL_WITNESS_BOTH"
        elif np.all(local_status == "STRUCTURALLY_INCOMPATIBLE_SHIFT_RANK"):
            classification = "STRUCTURALLY_INCOMPATIBLE_SHIFT_RANK"
        elif np.all(local_status == "STRUCTURALLY_INCOMPATIBLE_HESSIAN_RANK"):
            classification = "STRUCTURALLY_INCOMPATIBLE_HESSIAN_RANK"
        else:
            classification = "MIXED_NONCONSTRUCTIVE_REASON"
        local_ranks = sorted({int(value) for value in features[attempt_slice, index["curvature_operator_rank"]] if np.isfinite(value)})
        ledger = dict(row)
        ledger.update(
            {
                "constructive_attempts": count,
                "classification": classification,
                "status_replicate_0": local_status[0],
                "status_replicate_1": local_status[1],
                "flat_attempts": int(flat[attempt_slice].sum()),
                "pair_screen_zero_attempts": int(pair_zero[attempt_slice].sum()),
                "tidal_repeated_attempts": int(repeated[attempt_slice].sum()),
                "tidal_repeated_nonzero_attempts": int(repeated_nonzero[attempt_slice].sum()),
                "curvature_operator_ranks": ";".join(map(str, local_ranks)),
            }
        )
        ledger_rows.append(ledger)
    ledger_fields = list(ledger_rows[0])
    with (package / "STRATUM_LEDGER.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ledger_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(ledger_rows)
    axis_rows = []
    axes = ("shell", "coordinate_time", "phi_gradient", "angular_shape", "shift_value_rank", "angular_first_rank", "shift_first_rank", "collective_Hessian_rank")
    for axis in axes:
        values = []
        for row in strata:
            if row[axis] not in values:
                values.append(row[axis])
        for value in values:
            stratum_mask = np.array([row[axis] == value for row in strata])
            attempt_mask = np.repeat(stratum_mask, 2)
            axis_rows.append(
                {
                    "axis": axis,
                    "value": value,
                    "strata": int(stratum_mask.sum()),
                    "attempts": int(attempt_mask.sum()),
                    "constructed": int(np.sum(constructed & attempt_mask)),
                    "no_causal_witness": int(np.sum((status == "NO_CAUSAL_WITNESS_AT_SAMPLED_VALUE") & attempt_mask)),
                    "structural_rank_incompatible": int(np.sum(np.char.startswith(status, "STRUCTURALLY_INCOMPATIBLE") & attempt_mask)),
                    "flat_constructed": int(np.sum(flat & attempt_mask)),
                    "pair_screen_zero_constructed": int(np.sum(pair_zero & attempt_mask)),
                    "tidal_repeated_constructed": int(np.sum(repeated & attempt_mask)),
                    "tidal_repeated_nonzero_constructed": int(np.sum(repeated_nonzero & attempt_mask)),
                }
            )
    with (package / "AXIS_CENSUS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(axis_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(axis_rows)
    phi_classes = ("ZERO", "TIMELIKE", "NULL", "SPACELIKE")
    time_modes = ("DYNAMIC_4D", "COORDINATE_STATIC")
    causal_time = {}
    for time_mode in time_modes:
        causal_time[time_mode] = {}
        for phi_class in phi_classes:
            mask = np.array(
                [row["coordinate_time"] == time_mode and row["phi_gradient"] == phi_class for row in strata for _ in range(2)]
            )
            causal_time[time_mode][phi_class] = {
                "attempts": int(mask.sum()),
                "constructed": int(np.sum(mask & constructed)),
                "no_causal_witness": int(np.sum(mask & (status == "NO_CAUSAL_WITNESS_AT_SAMPLED_VALUE"))),
                "structural_rank_incompatible": int(np.sum(mask & np.char.startswith(status, "STRUCTURALLY_INCOMPATIBLE"))),
            }
    curvature_rank_distribution = Counter(map(int, features[constructed, index["curvature_operator_rank"]]))
    stratum_classification = Counter(row["classification"] for row in ledger_rows)
    result = {
        "schema": "udt-p02-stratified-local-jet-census-1.0",
        "status": "OBSERVED_BOUNDED_LOCAL_OFF_SHELL_ATLAS",
        "attempt_status_counts": dict(sorted(Counter(status).items())),
        "stratum_classification_counts": dict(sorted(stratum_classification.items())),
        "constructed": int(constructed.sum()),
        "numerically_finite_constructed": int(np.sum(constructed & (features[:, index["numerically_finite"]] > 0.5))),
        "flat_constructed": int(flat.sum()),
        "pair_screen_zero_constructed": int(pair_zero.sum()),
        "tidal_repeated_constructed": int(repeated.sum()),
        "tidal_repeated_nonzero_constructed": int(repeated_nonzero.sum()),
        "null_requested_attempts": int(null_requested.sum()),
        "null_constructed": int(np.sum(null_requested & constructed)),
        "null_and_tidal_repeated": int(np.sum(null_requested & repeated)),
        "null_and_tidal_repeated_nonzero": int(np.sum(null_requested & repeated_nonzero)),
        "curvature_operator_rank_distribution": {str(rank): count for rank, count in sorted(curvature_rank_distribution.items())},
        "coordinate_time_by_phi_class": causal_time,
        "tidal_norm_repeated_range": {
            "minimum": float(np.min(tidal_norm[repeated])) if repeated.any() else None,
            "median": float(np.median(tidal_norm[repeated])) if repeated.any() else None,
            "maximum": float(np.max(tidal_norm[repeated])) if repeated.any() else None,
        },
        "tidal_trace_repeated_range": {
            "minimum": float(np.min(tidal_trace[repeated])) if repeated.any() else None,
            "median": float(np.median(tidal_trace[repeated])) if repeated.any() else None,
            "maximum": float(np.max(tidal_trace[repeated])) if repeated.any() else None,
        },
        "scope_warning": "Counts describe the exact preregistered Cartesian atlas, not physical frequencies, global solutions, or selected branches.",
    }
    (package / "STRATUM_CENSUS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
