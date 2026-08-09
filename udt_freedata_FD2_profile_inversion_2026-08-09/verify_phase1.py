#!/usr/bin/env python3
"""Cross-grid verification of the blind FD2 Phase-I profile-response atlases."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
P180 = ROOT / "phase1_response_g180.json"
P240 = ROOT / "phase1_response_g240.json"
OUTPUT = ROOT / "phase1_verification.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_id(row: dict[str, object]) -> tuple[object, ...]:
    return row["identity"], row["q_ratio"], row["wall"], row["hbar"]


def main() -> None:
    a180 = json.loads(P180.read_text(encoding="utf-8"))
    a240 = json.loads(P240.read_text(encoding="utf-8"))
    r180 = {row_id(row): row for row in a180["rows"]}
    r240 = {row_id(row): row for row in a240["rows"]}
    ids = sorted(r240)
    comparisons = []
    for identity in ids:
        low = r180[identity]
        high = r240[identity]
        j180 = np.asarray(low["response_half_delta"], dtype=float)
        j240 = np.asarray(high["response_half_delta"], dtype=float)
        omega180 = np.asarray(low["omega0"], dtype=float)
        omega240 = np.asarray(high["omega0"], dtype=float)
        grid_drift = float(np.linalg.norm(j240 - j180) / max(np.linalg.norm(j240), 1.0e-14))
        frequency_drift = float(np.max(np.abs(omega240 / omega180 - 1.0)))
        halfstep_drift = max(
            float(low["halfstep_relative_norm_drift"]),
            float(high["halfstep_relative_norm_drift"]),
        )
        comparisons.append({
            "identity": list(identity),
            "grid_response_relative_norm_drift": grid_drift,
            "grid_frequency_max_relative_drift": frequency_drift,
            "maximum_halfstep_relative_norm_drift": halfstep_drift,
            "numerically_resolved": bool(grid_drift <= 0.05 and halfstep_drift <= 0.02),
        })

    counts = Counter(
        (row["motif_class"], row["q_ratio"], row["wall"], row["hbar"])
        for row in a240["rows"]
    )
    gates = {
        "both_atlases_blind": (
            a180["observational_peak_values_loaded"] is False
            and a240["observational_peak_values_loaded"] is False
            and a180["sne_magnitudes_loaded"] is False
            and a240["sne_magnitudes_loaded"] is False
        ),
        "production_complete": a180["production_complete"] and a240["production_complete"],
        "identity_sets_equal": set(r180) == set(r240),
        "exact_unique_count": len(r180) == len(r240) == 320,
        "forty_supports_per_class_background": len(counts) == 8 and set(counts.values()) == {40},
        "internal_gates": all(a180["gates"].values()) and all(a240["gates"].values()),
        "resolved_rows_exist": any(row["numerically_resolved"] for row in comparisons),
    }
    summary = {
        "row_count": len(comparisons),
        "numerically_resolved_row_count": sum(row["numerically_resolved"] for row in comparisons),
        "numerically_unresolved_row_count": sum(not row["numerically_resolved"] for row in comparisons),
        "maximum_grid_response_relative_norm_drift": max(
            row["grid_response_relative_norm_drift"] for row in comparisons
        ),
        "maximum_grid_frequency_relative_drift": max(
            row["grid_frequency_max_relative_drift"] for row in comparisons
        ),
        "maximum_halfstep_relative_norm_drift": max(
            row["maximum_halfstep_relative_norm_drift"] for row in comparisons
        ),
    }
    payload = {
        "phase": "FD2_PHASE1_CROSS_GRID_VERIFICATION",
        "inputs": {P180.name: sha256(P180), P240.name: sha256(P240)},
        "gates": gates,
        "summary": summary,
        "rows": comparisons,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(json.dumps(gates, indent=2, sort_keys=True))
    print(f"WROTE {OUTPUT}")
    if not all(gates.values()):
        raise SystemExit(f"failed gates: {[name for name, passed in gates.items() if not passed]}")


if __name__ == "__main__":
    main()
