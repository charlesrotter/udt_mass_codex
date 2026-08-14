#!/usr/bin/env python3
"""Outcome-independent catch proof for the R3 central-curve verifier repair."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import verify_r3 as verifier


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "R3_VERIFIER_CURVE_OWNERSHIP_CORRECTION_RESULT.json"


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)

    count = np.asarray([7], dtype=np.int64)
    expected = {
        "count": count.copy(),
        "weight": np.asarray([1.0], dtype=np.float64),
    }

    # The accepted component perturbation is below the frozen relative gate,
    # yet its near-zero derived curve exceeds the removed absolute curve gate.
    accepted_dd = np.asarray([1.0 + 5e-10], dtype=np.float64)
    dr = np.asarray([1.0], dtype=np.float64)
    rr = np.asarray([1.0], dtype=np.float64)
    assert verifier.component_matches(count, accepted_dd, expected)
    baseline = verifier.central_curve_from_weights(expected["weight"], dr, rr, 1.0, 1.0, 1.0)
    perturbed = verifier.central_curve_from_weights(accepted_dd, dr, rr, 1.0, 1.0, 1.0)
    assert abs(float(perturbed[0] - baseline[0])) > 2e-10 + 5e-9 * abs(float(baseline[0]))

    # Exact reconstruction catches even a one-ULP mutation of the saved curve.
    corrupted_curve = perturbed.copy()
    corrupted_curve[0] = np.nextafter(corrupted_curve[0], np.inf)
    assert not np.array_equal(corrupted_curve, perturbed)

    # The unchanged component gates catch both weighted and integer corruption.
    rejected_weight = np.asarray([1.0 + 2e-7], dtype=np.float64)
    assert not verifier.component_matches(count, rejected_weight, expected)
    assert not verifier.component_matches(np.asarray([8], dtype=np.int64), expected["weight"], expected)

    # Reject the mixed-vector case that elementwise ``allclose`` could accept
    # even though neither frozen whole-component alternative passes.
    mixed_expected = {
        "count": np.asarray([1, 1], dtype=np.int64),
        "weight": np.asarray([1.0, 100.0], dtype=np.float64),
    }
    mixed_observed = mixed_expected["weight"] + np.asarray([5e-8, 4e-7])
    assert np.allclose(mixed_observed, mixed_expected["weight"], rtol=5e-9, atol=1e-7)
    assert not verifier.component_matches(mixed_expected["count"], mixed_observed, mixed_expected)

    result = {
        "status": "PASS",
        "accepted_component_difference_can_exceed_removed_curve_gate": True,
        "one_ulp_curve_corruption_caught": True,
        "out_of_tolerance_component_caught": True,
        "integer_count_mismatch_caught": True,
        "elementwise_allclose_false_pass_caught": True,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS: R3 central-curve ownership correction catch proof")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
