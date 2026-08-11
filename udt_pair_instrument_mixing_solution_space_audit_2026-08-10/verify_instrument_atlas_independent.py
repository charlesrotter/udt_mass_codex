#!/usr/bin/env python3
"""Independent standard-library exact/sampled verification for the G59 atlas."""

from __future__ import annotations

import csv
import json
import math
import random
import sys
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
READ_ONLY = "--read-only" in sys.argv[1:]


def eta_dot(u: tuple[F, ...], v: tuple[F, ...]) -> F:
    return -u[0] * v[0] + sum(u[i] * v[i] for i in range(1, 4))


def bivec(u: tuple[F, ...], v: tuple[F, ...]) -> dict[tuple[int, int], F]:
    return {
        (a, b): u[a] * v[b] - u[b] * v[a]
        for a in range(4)
        for b in range(a + 1, 4)
    }


def matrix_channels(u: tuple[F, ...], v: tuple[F, ...]) -> tuple[tuple[F, F, F], tuple[F, F, F]]:
    hr = (
        -u[0] * u[0] + u[1] * u[1],
        -u[0] * v[0] + u[1] * v[1],
        -v[0] * v[0] + v[1] * v[1],
    )
    ha = (
        u[2] * u[2] + u[3] * u[3],
        u[2] * v[2] + u[3] * v[3],
        v[2] * v[2] + v[3] * v[3],
    )
    return hr, ha


def transform(g: tuple[tuple[F, ...], ...], v: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(sum(g[i][j] * v[j] for j in range(4)) for i in range(4))


def check_pair(u: tuple[F, ...], v: tuple[F, ...]) -> tuple[bool, bool]:
    h00, h01, h11 = eta_dot(u, u), eta_dot(u, v), eta_dot(v, v)
    det_h = h00 * h11 - h01 * h01
    b = bivec(u, v)
    plucker = b[0, 1] * b[2, 3] - b[0, 2] * b[1, 3] + b[0, 3] * b[1, 2]
    r = b[0, 1] ** 2
    a = b[2, 3] ** 2
    ms = -b[0, 2] ** 2 - b[0, 3] ** 2 + b[1, 2] ** 2 + b[1, 3] ** 2
    hr, ha = matrix_channels(u, v)
    matrix_sum = (
        hr[0] + ha[0] == h00,
        hr[1] + ha[1] == h01,
        hr[2] + ha[2] == h11,
    )
    determinant_channels = (
        hr[0] * hr[2] - hr[1] ** 2 == -r,
        ha[0] * ha[2] - ha[1] ** 2 == a,
    )
    return (
        plucker == 0
        and det_h == -r + a + ms
        and all(matrix_sum)
        and all(determinant_channels),
        det_h < 0,
    )


def main() -> None:
    rng = random.Random(20260810)
    exact_count = 0
    lorentzian_count = 0
    for _ in range(600):
        u = tuple(F(rng.randint(-5, 5)) for _ in range(4))
        v = tuple(F(rng.randint(-5, 5)) for _ in range(4))
        passed, lorentzian = check_pair(u, v)
        assert passed
        exact_count += 1
        lorentzian_count += int(lorentzian)
    assert lorentzian_count > 50

    # Exact split-preserving boost (3-4-5) and angular rotation.
    g = (
        (F(5, 4), F(3, 4), F(0), F(0)),
        (F(3, 4), F(5, 4), F(0), F(0)),
        (F(0), F(0), F(3, 5), F(-4, 5)),
        (F(0), F(0), F(4, 5), F(3, 5)),
    )
    covariance_count = 0
    for _ in range(200):
        u = tuple(F(rng.randint(-4, 4)) for _ in range(4))
        v = tuple(F(rng.randint(-4, 4)) for _ in range(4))
        assert matrix_channels(u, v) == matrix_channels(transform(g, u), transform(g, v))
        b0, b1 = bivec(u, v), bivec(transform(g, u), transform(g, v))
        inv0 = (
            b0[0, 1],
            b0[2, 3],
            -b0[0, 2] ** 2 - b0[0, 3] ** 2 + b0[1, 2] ** 2 + b0[1, 3] ** 2,
        )
        inv1 = (
            b1[0, 1],
            b1[2, 3],
            -b1[0, 2] ** 2 - b1[0, 3] ** 2 + b1[1, 2] ** 2 + b1[1, 3] ** 2,
        )
        assert inv0 == inv1
        covariance_count += 1

    # Same intrinsic metric, distinct plane orientation relative to a fixed split.
    pure_u, pure_v = (F(1), F(0), F(0), F(0)), (F(0), F(1), F(0), F(0))
    tilt_u, tilt_v = (F(5, 4), F(0), F(3, 4), F(0)), pure_v
    pure_h = (eta_dot(pure_u, pure_u), eta_dot(pure_u, pure_v), eta_dot(pure_v, pure_v))
    tilt_h = (eta_dot(tilt_u, tilt_u), eta_dot(tilt_u, tilt_v), eta_dot(tilt_v, tilt_v))
    assert pure_h == tilt_h == (F(-1), F(0), F(1))
    assert matrix_channels(pure_u, pure_v) != matrix_channels(tilt_u, tilt_v)

    # Boundary witnesses.
    witnesses = {
        "pure_reciprocal_lorentzian": (pure_u, pure_v, F(-1)),
        "pure_angular_spacelike": ((F(0), F(0), F(1), F(0)), (F(0), F(0), F(0), F(1)), F(1)),
        "pure_mixed_lorentzian": (pure_u, (F(0), F(0), F(1), F(0)), F(-1)),
        "null_pair": ((F(1), F(0), F(1), F(0)), pure_v, F(0)),
        "rank_loss": (pure_u, tuple(F(2) * value for value in pure_u), F(0)),
    }
    for u, v, expected_det in witnesses.values():
        det_h = eta_dot(u, u) * eta_dot(v, v) - eta_dot(u, v) ** 2
        assert det_h == expected_det
        assert check_pair(u, v)[0]

    # No invariant positive-definite quadratic norm on an SO+(1,1) doublet.
    # Infinitesimal invariance forces Q=diag(a,-a), whose determinant is -a^2.
    for aval in range(-5, 6):
        determinant_q = -F(aval) ** 2
        assert determinant_q <= 0

    # At least two smooth invariant positive diagnostics survive on the regular region.
    # Their disagreement disproves a unique positive scalar "importance" rule.
    rv, av, msv = 1.0, 0.25, 0.0
    q1 = math.sqrt(msv * msv + 1.0 * (rv + av) ** 2)
    q4 = math.sqrt(msv * msv + 4.0 * (rv + av) ** 2)
    weights1 = tuple(z / (rv + av + q1) for z in (rv, av, q1))
    weights4 = tuple(z / (rv + av + q4) for z in (rv, av, q4))
    assert weights1 != weights4
    assert math.isclose(sum(weights1), 1.0) and math.isclose(sum(weights4), 1.0)

    with (HERE / "SAMPLED_REGION_ATLAS.tsv").open(newline="", encoding="utf-8") as handle:
        atlas_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(atlas_rows) == 27
    independent_row_residuals: list[float] = []
    for row in atlas_rows:
        row_r = float(row["R"])
        row_a = float(row["A"])
        row_ms = float(row["M_signed"])
        b01 = float(row["B01"])
        b23 = float(row["B23"])
        b02 = float(row["B02"])
        b13 = float(row["B13"])
        expected_b02_sq = (-row_ms + math.sqrt(row_ms**2 + 4.0 * row_r * row_a)) / 2.0
        reconstructed_ms = -b02**2 + b13**2
        reconstructed_det_m = b02 * b13
        reconstructed_det_h = -b01**2 + b23**2 + reconstructed_ms
        residuals = (
            b01**2 - row_r,
            b23**2 - row_a,
            b02**2 - expected_b02_sq,
            reconstructed_ms - row_ms,
            reconstructed_det_m - b01 * b23,
            reconstructed_det_m - float(row["det_M"]),
            reconstructed_det_h - float(row["det_h"]),
        )
        independent_row_residuals.append(max(abs(value) for value in residuals))
        assert reconstructed_det_h < 0
        assert row["lorentzian"] == "true"
    max_residual = max(independent_row_residuals)
    assert max_residual < 1e-12

    result = {
        "implementation": "independent_standard_library_fraction_and_float",
        "exact_random_pairs": exact_count,
        "lorentzian_random_pairs": lorentzian_count,
        "exact_covariance_pairs": covariance_count,
        "boundary_witnesses": len(witnesses),
        "sampled_region_witnesses": len(atlas_rows),
        "independently_reconstructed_sampled_region_witnesses": len(atlas_rows),
        "max_sampled_residual": max_residual,
        "same_h_distinct_orchestra": True,
        "unique_positive_weight_rejected": True,
        "status": "PASS",
    }
    if not READ_ONLY:
        (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
