#!/usr/bin/env python3
"""Strictly reroot every saved branch of the failed complete atlas."""

from __future__ import annotations

import copy
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

import derive_corrected_atlas as core


ROOT = Path(__file__).resolve().parent
PARENT = ROOT / "corrected_full_atlas.json"
OUTPUT = ROOT / "corrected_full_atlas_strict.json"
EXPECTED_PARENT = "59842d806439827cfd385fb46ea3cfee757b7d24a822674c6fc872a1b2eb160f"
XTOL = 5.0e-15
RTOL = 1.0e-14
BRACKET_FRACTION = 0.75


def refine_root(row: dict[str, object], m: int, wall: str, old: float, step: float) -> tuple[float, float]:
    n, q, hbar = float(row["n"]), float(row["q"]), float(row["hbar"])
    left = max(1.0e-14, old - BRACKET_FRACTION * step)
    right = old + BRACKET_FRACTION * step

    def value(omega: float) -> float:
        return core.boundary_value(
            omega, m, n, q, hbar, wall, rtol=core.ROOT_RTOL, atol=core.ROOT_ATOL
        )

    lv, rv = value(left), value(right)
    if lv * rv >= 0.0:
        raise RuntimeError(f"frozen local bracket lost: {row['inv_n']=} {row['q_ratio']=} {hbar=} {wall=} {m=} {old=}")
    root = brentq(value, left, right, xtol=XTOL, rtol=RTOL, maxiter=120)
    if abs(root - old) > step:
        raise RuntimeError("refined root left its frozen scan cell")
    return float(root), abs(value(root))


def main() -> None:
    start = time.time()
    if core.sha256(PARENT) != EXPECTED_PARENT:
        raise SystemExit("failed parent atlas hash mismatch")
    parent = json.loads(PARENT.read_text())
    payload = copy.deepcopy(parent)
    spectral = [row for row in payload["rows"] if float(row["hbar"]) > 0.0]
    maximum_shift = 0.0
    residuals: list[float] = []
    roots_done = 0
    for index, row in enumerate(spectral, start=1):
        wall = str(row["wall"])
        modes: dict[int, np.ndarray] = {}
        row_residuals: dict[str, float] = {}
        for m, field in ((-1, "omega_mminus"), (0, "omega_m0"), (1, "omega_mplus")):
            step = float(row["scan"][str(m)]["scan_step"])
            old_roots = np.asarray(row[field], dtype=float)
            new_roots, new_residuals = [], []
            for old in old_roots:
                root, residual = refine_root(row, m, wall, float(old), step)
                new_roots.append(root)
                new_residuals.append(residual)
                maximum_shift = max(maximum_shift, abs(root - old))
                roots_done += 1
            modes[m] = np.asarray(new_roots)
            row[field] = new_roots
            row_residuals[str(m)] = max(new_residuals)
            residuals.extend(new_residuals)
        mean_pair = 0.5 * (modes[-1] + modes[1])
        row["eta_split"] = (np.abs(modes[1] - modes[-1]) / mean_pair).tolist()
        row["same_index_displacement"] = (
            np.maximum(np.abs(modes[1] - modes[0]), np.abs(modes[-1] - modes[0])) / modes[0]
        ).tolist()
        row["full_frequency_order"] = sorted(
            ({"omega": float(v), "m": m, "radial_index": k} for m in core.MS for k, v in enumerate(modes[m])),
            key=lambda item: item["omega"],
        )
        row["max_normalized_wall_residual"] = row_residuals
        if float(row["q_ratio"]) == 0.0:
            row["q0_split_max_abs_error"] = float(
                np.max(np.abs(np.abs(modes[1] - modes[-1]) - 2.0 * float(row["hbar"])))
            )
        if index % 20 == 0:
            print(f"ROWS {index:03d}/420 ROOTS {roots_done}/5040", flush=True)

    q0 = [row["q0_split_max_abs_error"] for row in spectral if row["q0_split_max_abs_error"] is not None]
    ordered = all(
        np.all(np.diff(np.asarray(row[name])) > 0.0)
        for row in spectral
        for name in ("omega_mminus", "omega_m0", "omega_mplus")
    )
    keys = {
        "CFA_R1_parent_hash": True,
        "CFA_R2_all_5040_roots_refined": roots_done == 5040,
        "CFA_R3_positive_ordered": ordered,
        "CFA_R4_original_residual_gate": max(residuals) < 2.0e-8,
        "CFA_R5_q0_exact_split": max(q0) < 2.0e-8,
        "CFA_R6_same_census": len(payload["rows"]) == 462 and len(spectral) == 420,
    }
    payload["phase"] = "BLIND_CORRECTED_FULL_SPECTRAL_ATLAS_STRICT_ROOTS"
    payload["parent_failed_atlas_sha256"] = EXPECTED_PARENT
    payload["keys"] = keys
    payload["summary"].update(
        maximum_normalized_wall_residual=max(residuals),
        q0_max_abs_split_error=max(q0),
        maximum_absolute_root_shift=maximum_shift,
        strict_roots_refined=roots_done,
        strict_refinement_runtime_seconds=time.time() - start,
    )
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(keys, sort_keys=True), flush=True)
    print(f"WROTE {OUTPUT} SHA256 {core.sha256(OUTPUT)}", flush=True)
    if not all(keys.values()):
        raise SystemExit("strict refinement gate failed")


if __name__ == "__main__":
    main()
