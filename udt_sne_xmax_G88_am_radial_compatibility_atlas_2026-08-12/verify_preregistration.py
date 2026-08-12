#!/usr/bin/env python3
"""Verify the frozen G88 preregistration before any outcome calculation."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest}) == 15
    for row in manifest:
        path = ROOT / row["path"]
        assert path.is_file() and digest(path) == row["sha256"], row["path"]

    profiles = rows(ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv")
    am = [row for row in profiles if row["lapse_name"] == "AM"]
    assert len(profiles) == 591
    assert len(am) == len({row["profile_id"] for row in am}) == 197
    assert sum(row["shape_id"] == "ZERO" for row in am) == 1

    table = np.genfromtxt(ROOT / "Data/Pantheon+SH0ES.dat", names=True, dtype=None, encoding=None)
    mask = (np.asarray(table["zCMB"], dtype=float) > 0.023) & (np.asarray(table["IS_CALIBRATOR"], dtype=int) == 0)
    z = np.asarray(table["zCMB"], dtype=float)[mask]
    assert len(z) == 1367
    assert float(np.max(z)) == 2.2613
    A_receiver = 1.0 - 0.25**2 / 4.0
    x_source = 2.0 * np.sqrt(1.0 - A_receiver / (1.0 + z) ** 2)
    assert np.all(np.isfinite(x_source)) and np.all(x_source > 0.25)
    assert abs(float(np.max(x_source)) - 1.9052028080619356) <= 1.0e-15
    assert float(np.max(x_source)) < 2.0

    reference = json.loads((ROOT / "udt_xmax_scale_observational_M3_runs_2026-08-07/sne_results.json").read_text())
    p1 = reference["fits"]["A:zCMB:P1"]
    assert p1["n_data"] == 1367 and p1["ndof"] == 1365
    assert p1["chi2"] == 1260.8480887040496

    forbidden_outputs = (
        "PROFILE_COMPATIBILITY_ATLAS.tsv",
        "DERIVATION_RESULT.json",
        "DISTANCE_CURVES.npz",
        "INDEPENDENT_VERIFICATION.json",
    )
    assert not any((HERE / name).exists() for name in forbidden_outputs)
    print(json.dumps({
        "status": "PASS__PREREGISTERED_NO_OUTCOME",
        "source_rows": len(manifest),
        "profile_rows": len(am),
        "data_rows": len(z),
        "x_source_max": float(np.max(x_source)),
        "p1_chi2": p1["chi2"],
        "outcome_files_absent": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
