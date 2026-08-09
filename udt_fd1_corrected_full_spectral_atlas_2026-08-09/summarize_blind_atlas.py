#!/usr/bin/env python3
"""Metric-only summary of the certified atlas; no observational table is loaded."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
ATLAS = ROOT / "corrected_full_atlas_certified.json"
OLD = REPO / "udt_freedata_FD1_mixing_bound_2026-08-09" / "phase1_atlas_g240.json"
OUTPUT = ROOT / "blind_summary.json"
EXPECTED_ATLAS = "042138fb73cc9f3bef4faf97fc0357f2a2f079daced5e39d6532c4a6f770dfbb"
EXPECTED_OLD = "534713dea58c7a99a0b5ed149c33c08972f458d558bedb681f67c0d3f376110d"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_id(row: dict[str, object]) -> tuple[float, float, float, str]:
    return (round(1.0 / float(row["n"]), 4), float(row["q_ratio"]), float(row["hbar"]), str(row["wall"]))


def quantiles(values: list[float]) -> dict[str, float]:
    array = np.asarray(values, dtype=float)
    return {
        "minimum": float(np.min(array)),
        "median": float(np.median(array)),
        "p95": float(np.quantile(array, 0.95)),
        "maximum": float(np.max(array)),
    }


def main() -> None:
    if digest(ATLAS) != EXPECTED_ATLAS or digest(OLD) != EXPECTED_OLD:
        raise SystemExit("input hash mismatch")
    atlas = json.loads(ATLAS.read_text())
    old = json.loads(OLD.read_text())
    rows = [row for row in atlas["rows"] if float(row["hbar"]) > 0.0]
    old_rows = {row_id(row): row for row in old["rows"] if float(row["hbar"]) > 0.0}
    fields = {-1: "omega_mminus", 0: "omega_m0", 1: "omega_mplus"}
    drift: dict[int, list[float]] = defaultdict(list)
    motif_counts: Counter[str] = Counter()
    between_count = 0
    total_same_index = 0
    all_between_rows = 0
    eta: list[float] = []
    displacement: list[float] = []
    frequencies: list[float] = []
    xwalls: list[float] = []
    for row in rows:
        previous = old_rows[row_id(row)]
        modes = {m: np.asarray(row[field], dtype=float) for m, field in fields.items()}
        for m, field in fields.items():
            earlier = np.asarray(previous[field], dtype=float)
            drift[m].extend(np.abs(modes[m] / earlier - 1.0).tolist())
            frequencies.extend(modes[m].tolist())
        row_between = []
        for k in range(8):
            order = tuple(m for _, m in sorted((modes[m][k], m) for m in (-1, 0, 1)))
            motif_counts[",".join(map(str, order))] += 1
            inside = min(modes[-1][k], modes[1][k]) <= modes[0][k] <= max(modes[-1][k], modes[1][k])
            row_between.append(inside)
        between_count += sum(row_between)
        total_same_index += 8
        all_between_rows += int(all(row_between))
        eta.extend(row["eta_split"])
        displacement.extend(row["same_index_displacement"])
        xwalls.append(float(row["xwall"]))

    by_config: dict[tuple[float, float, float], dict[str, dict[str, object]]] = defaultdict(dict)
    for row in rows:
        by_config[(float(row["inv_n"]), float(row["q_ratio"]), float(row["hbar"]))][str(row["wall"])] = row
    interlaced = 0
    interlace_total = 0
    for pair in by_config.values():
        for field in fields.values():
            D, N = np.asarray(pair["D"][field]), np.asarray(pair["N"][field])
            labels = [label for _, label in sorted([(v, "D") for v in D] + [(v, "N") for v in N])]
            interlaced += int(all(labels[i] != labels[i + 1] for i in range(len(labels) - 1)))
            interlace_total += 1

    q_groups: dict[str, dict[str, float]] = {}
    for ratio in (-2.0, -1.0, 0.0, 0.25, 0.50, 0.75, 0.95):
        selected = [float(row["xwall"]) for row in rows if float(row["q_ratio"]) == ratio]
        q_groups[str(ratio)] = quantiles(selected)
    summary = {
        "phase": "BLIND_GEOMETRY_SUMMARY",
        "observational_values_loaded": False,
        "input_hashes": {"certified_atlas": EXPECTED_ATLAS, "withdrawn_old_atlas": EXPECTED_OLD},
        "census": {"spectral_rows": len(rows), "positive_roots": len(frequencies)},
        "frequency_range": quantiles(frequencies),
        "xwall_range": quantiles(xwalls),
        "xwall_by_q_ratio": q_groups,
        "withdrawn_atlas_absolute_relative_drift": {str(m): quantiles(values) for m, values in drift.items()},
        "same_radial_index_order_motifs": dict(sorted(motif_counts.items())),
        "m0_between_mminus_mplus_same_index": {
            "positions": int(between_count),
            "total": total_same_index,
            "all_eight_rows": int(all_between_rows),
            "rows": len(rows),
        },
        "eta_split": quantiles(eta),
        "same_index_displacement": quantiles(displacement),
        "D_N_strict_interlacing": {"channel_configurations": interlaced, "total": interlace_total},
        "q0_exact_split_max_error": atlas["summary"]["q0_max_abs_split_error"],
    }
    OUTPUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"WROTE {OUTPUT} SHA256 {digest(OUTPUT)}")


if __name__ == "__main__":
    main()
