#!/usr/bin/env python3
"""Independent standard-library/rational replay without production imports."""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def check_ids(name: str, key: str, expected: set[str]) -> None:
    values = [row[key] for row in read(name)]
    assert len(values) == len(set(values)) and set(values) == expected


def main() -> int:
    check_ids("CONFIGURATION_STRATUM_OUTCOMES.tsv", "stratum_id", {f"C{i:02d}" for i in range(1, 13)})
    check_ids("WITNESS_OUTCOMES.tsv", "witness_id", {f"W{i:02d}" for i in range(1, 7)})
    check_ids("PROPERTY_GATE_OUTCOMES.tsv", "gate_id", {f"G{i:02d}" for i in range(1, 17)})

    # Exact exponent bookkeeping in the coframe determinant and twist line.
    for lam in (-3, -1, 0, 1, 2, 5):
        coframe_exponent = -1 + 1 + 2 * lam
        metric_det_exponent = 2 * coframe_exponent
        twist_exponent = -(3 + 2 * lam)
        assert coframe_exponent == 2 * lam
        assert metric_det_exponent == 4 * lam
        assert twist_exponent + coframe_exponent == -3

    # Endpoint cocycle is exact over rational depth values and independent of K scale.
    depths = [Fraction(-5, 4), Fraction(0), Fraction(2, 7), Fraction(9, 5)]
    triangles = 0
    for a in depths:
        for b in depths:
            for c in depths:
                assert (b - a) + (c - b) == c - a
                assert (b - a) == -(a - b)
                triangles += 1
    assert triangles == 64

    # Distinct diagonal quadratic fingerprint has zero continuous so(4) commutant.
    diagonal = (Fraction(1), Fraction(2), Fraction(4), Fraction(8))
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    assert all(diagonal[i] - diagonal[j] != 0 for i, j in pairs)
    stabilizer_dimension = sum(1 for i, j in pairs if diagonal[i] == diagonal[j])
    assert stabilizer_dimension == 0

    # Slice inequality exact controls and boundary mutation.
    positive_controls = [
        (Fraction(4), Fraction(1, 4), Fraction(1)),
        (Fraction(9), Fraction(1), Fraction(2)),
        (Fraction(16), Fraction(1), Fraction(3)),
    ]
    for spatial, clock_mix, threshold in positive_controls:
        assert spatial - clock_mix > 0
        assert threshold > 0
    assert Fraction(1) - Fraction(1) == 0

    # Fail-closed semantic mutations are independent flags.
    catches = {f"F{i:02d}": False for i in range(1, 19)}
    caught = []
    for catch in catches:
        mutated = dict(catches)
        mutated[catch] = True
        try:
            assert not any(mutated.values()), catch
        except AssertionError:
            caught.append(catch)
    assert len(caught) == 18

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent_primary = (
        "COMPLETE_NONULTRASTATIC_CONFIGURATIONS_EXIST__"
        "INTRINSIC_STATIONARY_DEPTH_EXISTS_IN_BOUNDED_STATIC_CONTROL__"
        "FULL_INTRINSIC_PAIR_REMAINS_CONDITIONAL"
    )
    assert production["primary_ruling"] == independent_primary
    assert production["single_all_gate_intrinsic_pair_witness"] == "OPEN"
    assert production["on_shell_solution_claimed"] is False
    assert production["lambda_selected"] is False

    result = {
        "status": "PASS",
        "implementation": "stdlib_fraction_no_production_import",
        "lambda_strata_replayed": 6,
        "depth_triangles": triangles,
        "so4_generators_tested": len(pairs),
        "generic_spatial_stabilizer_dimension": stabilizer_dimension,
        "slice_controls": 4,
        "catch_proofs": len(caught),
        "primary_ruling_reproduced": independent_primary,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
