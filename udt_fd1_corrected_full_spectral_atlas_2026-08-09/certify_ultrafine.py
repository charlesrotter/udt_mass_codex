#!/usr/bin/env python3
"""Apply the preregistered 24-root ultrafine certification correction."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

import derive_corrected_atlas as core


ROOT = Path(__file__).resolve().parent
PARENT = ROOT / "corrected_full_atlas_strict.json"
OUTPUT = ROOT / "corrected_full_atlas_certified.json"
EXPECTED_PARENT = "46e8aeda120f6c51fbfc000cf56e5db5a78fe2092ae12b06b20523bc468ec1d5"


def is_target(row: dict[str, object]) -> bool:
    return (
        float(row["inv_n"]) == 0.9284
        and float(row["q_ratio"]) == 0.95
        and float(row["hbar"]) == 0.001
        and row["wall"] == "D"
    )


def main() -> None:
    if core.sha256(PARENT) != EXPECTED_PARENT:
        raise SystemExit("strict parent hash mismatch")
    original = json.loads(PARENT.read_text())
    payload = copy.deepcopy(original)
    targets = [row for row in payload["rows"] if is_target(row)]
    if len(targets) != 1:
        raise SystemExit(f"expected one target row, got {len(targets)}")
    row = targets[0]
    maximum_shift = 0.0
    modes: dict[int, np.ndarray] = {}
    residual_max: dict[str, float] = {}
    changed = 0
    for m, field in ((-1, "omega_mminus"), (0, "omega_m0"), (1, "omega_mplus")):
        step = float(row["scan"][str(m)]["scan_step"])
        refined, residuals = [], []
        for old in np.asarray(row[field], dtype=float):
            def value(omega: float) -> float:
                return core.boundary_value(
                    omega, m, float(row["n"]), float(row["q"]), float(row["hbar"]), "D",
                    rtol=core.ROOT_RTOL, atol=core.ROOT_ATOL,
                )
            left, right = max(1.0e-14, old - 0.75 * step), old + 0.75 * step
            if value(left) * value(right) >= 0.0:
                raise RuntimeError("target root lost its frozen scan-cell bracket")
            root = brentq(value, left, right, xtol=1.0e-18, rtol=1.0e-14, maxiter=200)
            shift = abs(root - old)
            if shift >= 2.0e-14 or shift >= step:
                raise RuntimeError("ultrafine root moved outside correction contract")
            maximum_shift = max(maximum_shift, shift)
            refined.append(float(root))
            residuals.append(abs(value(root)))
            changed += 1
        modes[m] = np.asarray(refined)
        row[field] = refined
        residual_max[str(m)] = max(residuals)
    row["max_normalized_wall_residual"] = residual_max
    mean_pair = 0.5 * (modes[-1] + modes[1])
    row["eta_split"] = (np.abs(modes[1] - modes[-1]) / mean_pair).tolist()
    row["same_index_displacement"] = (
        np.maximum(np.abs(modes[1] - modes[0]), np.abs(modes[-1] - modes[0])) / modes[0]
    ).tolist()
    row["full_frequency_order"] = sorted(
        ({"omega": float(v), "m": m, "radial_index": k} for m in core.MS for k, v in enumerate(modes[m])),
        key=lambda item: item["omega"],
    )

    spectral = [item for item in payload["rows"] if float(item["hbar"]) > 0.0]
    all_residuals = [v for item in spectral for v in item["max_normalized_wall_residual"].values()]
    q0 = [item["q0_split_max_abs_error"] for item in spectral if item["q0_split_max_abs_error"] is not None]
    roots = len(spectral) * len(core.MS) * core.NMODES
    keys = {
        "CFA_U1_parent_hash": True,
        "CFA_U2_exact_24_root_target": changed == 24,
        "CFA_U3_correct_10080_root_count": roots == 10080,
        "CFA_U4_original_residual_gate": max(all_residuals) < 2.0e-8,
        "CFA_U5_q0_exact_split": max(q0) < 2.0e-8,
        "CFA_U6_same_462_row_census": len(payload["rows"]) == 462,
    }
    payload["phase"] = "BLIND_CORRECTED_FULL_SPECTRAL_ATLAS_CERTIFIED"
    payload["parent_strict_atlas_sha256"] = EXPECTED_PARENT
    payload["keys"] = keys
    payload["summary"].update(
        corrected_positive_root_count=roots,
        ultrafine_roots_refined=changed,
        ultrafine_maximum_absolute_shift=maximum_shift,
        maximum_normalized_wall_residual=max(all_residuals),
    )
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(keys, sort_keys=True))
    print(json.dumps(payload["summary"], sort_keys=True))
    print(f"WROTE {OUTPUT} SHA256 {core.sha256(OUTPUT)}")
    if not all(keys.values()):
        raise SystemExit("ultrafine certification failed")


if __name__ == "__main__":
    main()
