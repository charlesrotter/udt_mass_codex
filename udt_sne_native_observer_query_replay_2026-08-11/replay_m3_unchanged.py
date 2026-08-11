#!/usr/bin/env python3
"""Replay all frozen M3 SNe fits without touching historical outputs."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any

import numpy as np
import scipy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
M2 = ROOT / "udt_xmax_scale_observational_M2_build_2026-08-07"
REFERENCE = ROOT / "udt_xmax_scale_observational_M3_runs_2026-08-07" / "sne_results.json"
PREREG_COMMIT = "523f4aca"
ANCHOR_M_B = -19.253
ANCHOR_M_B_ERR = 0.027
TOL = 5.0e-9
MUTABLE_SOURCE_SNAPSHOT_COMMIT = "307144b5"

sys.path.insert(0, str(M2))
import v_sne  # noqa: E402


def verify_sources() -> dict[str, str]:
    checks: dict[str, str] = {}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            source_bytes = (ROOT / row["path"]).read_bytes()
            digest = hashlib.sha256(source_bytes).hexdigest()
            if digest != row["sha256"] and row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
                snapshot = subprocess.run(
                    ["git", "show", f"{MUTABLE_SOURCE_SNAPSHOT_COMMIT}:{row['path']}"],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                ).stdout
                digest = hashlib.sha256(snapshot).hexdigest()
            if digest != row["sha256"]:
                raise AssertionError(f"source hash mismatch: {row['path']}")
            checks[row["path"]] = "PASS"
    return checks


def compare(reference: Any, replay: Any, path: str = "root") -> tuple[int, float]:
    """Recursively compare labels exactly and finite floats within the frozen tolerance."""
    if isinstance(reference, dict):
        if not isinstance(replay, dict) or set(reference) != set(replay):
            raise AssertionError(f"mapping mismatch at {path}")
        count = 0
        maximum = 0.0
        for key in sorted(reference):
            n, d = compare(reference[key], replay[key], f"{path}.{key}")
            count += n
            maximum = max(maximum, d)
        return count, maximum
    if isinstance(reference, list):
        if not isinstance(replay, list) or len(reference) != len(replay):
            raise AssertionError(f"list mismatch at {path}")
        count = 0
        maximum = 0.0
        for index, (left, right) in enumerate(zip(reference, replay)):
            n, d = compare(left, right, f"{path}[{index}]")
            count += n
            maximum = max(maximum, d)
        return count, maximum
    if isinstance(reference, bool) or reference is None or isinstance(reference, str):
        if reference != replay:
            raise AssertionError(f"exact mismatch at {path}: {reference!r} != {replay!r}")
        return 1, 0.0
    if isinstance(reference, int):
        if type(replay) is not int or reference != replay:
            raise AssertionError(f"integer mismatch at {path}: {reference!r} != {replay!r}")
        return 1, 0.0
    if isinstance(reference, float):
        if isinstance(replay, bool) or not isinstance(replay, (int, float)):
            raise AssertionError(
                f"numeric type mismatch at {path}: expected JSON number, got {type(replay)}"
            )
        difference = abs(reference - float(replay))
        if not np.isfinite(difference) or difference > TOL:
            raise AssertionError(f"float mismatch at {path}: abs diff {difference}")
        return 1, difference
    raise TypeError(f"unhandled reference type at {path}: {type(reference)}")


def run() -> dict[str, Any]:
    source_checks = verify_sources()
    v_sne.authorize_m3(PREREG_COMMIT)
    table = v_sne.read_pantheon_table()
    covariance = v_sne.load_cov()
    fits: dict[str, dict[str, Any]] = {}
    jobs = [("A", "zCMB"), ("B", "zCMB"), ("C", "zCMB")]
    jobs.extend(("D", name) for name in ("zCMB", "zHD", "zHEL"))
    for mode, z_column in jobs:
        mode_data = v_sne.load_mode_data(
            mode, zcol=z_column, table=table, cov_full=covariance
        )
        vector = v_sne.DataVector.from_real(mode_data)
        weighted = v_sne.CovChi2(mode_data.cov) if mode_data.cov is not None else None
        for profile in v_sne.PROFILES:
            key = f"{mode}:{z_column}:{profile}"
            if mode == "A":
                result = v_sne.fit_mode_A(vector, profile, cc=weighted)
            elif mode == "B":
                result = v_sne.fit_mode_B(
                    vector,
                    profile,
                    ANCHOR_M_B,
                    M_B_err=ANCHOR_M_B_ERR,
                    cc=weighted,
                )
            elif mode == "C":
                result = v_sne.fit_mode_C(vector, profile)
            else:
                result = v_sne.fit_mode_D(vector, profile, cc=weighted)
            fits[key] = result

    shifts: dict[str, Any] = {"C_minus_A_shape": {}, "D_shifts_shape": {}}
    for profile in ("P1", "P3"):
        a_shape = fits[f"A:zCMB:{profile}"]["shape"]
        c_shape = fits[f"C:zCMB:{profile}"]["shape"]
        shifts["C_minus_A_shape"][profile] = {
            "A": a_shape,
            "C": c_shape,
            "abs_shift": abs(c_shape - a_shape),
            "note": (
                "quantified BBC-contamination estimate (prereg SS3); "
                "also the point-of-use note on the banked 0.91"
            ),
        }
        for z_column in ("zHD", "zHEL"):
            d_shape = fits[f"D:{z_column}:{profile}"]["shape"]
            shifts["D_shifts_shape"].setdefault(profile, {})[z_column] = {
                "zCMB": a_shape,
                z_column: d_shape,
                "abs_shift": abs(d_shape - a_shape),
            }

    replay = {
        "prereg_commit": PREREG_COMMIT,
        "anchor": {"M_B": ANCHOR_M_B, "err": ANCHOR_M_B_ERR},
        "fits": fits,
        "headline_shifts": shifts,
    }
    reference = json.loads(REFERENCE.read_text(encoding="utf-8"))
    field_count, maximum_difference = compare(reference, replay)
    result = {
        "schema": "udt-sne-native-query-replay-1.0",
        "status": "PASS",
        "source_hash_checks": len(source_checks),
        "fit_count": len(fits),
        "compared_leaf_fields": field_count,
        "maximum_absolute_numeric_difference": maximum_difference,
        "tolerance": TOL,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "reference": str(REFERENCE.relative_to(ROOT)),
        "replay": replay,
    }
    (HERE / "REPLAY_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"PASS fits={len(fits)} fields={field_count} "
        f"max_abs_diff={maximum_difference:.3e}"
    )
    return result


if __name__ == "__main__":
    run()
