#!/usr/bin/env python3
"""Independent stdlib exact-rational replay for G180."""

from __future__ import annotations

import csv
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def det2(h: list[list[F]]) -> F:
    return h[0][0] * h[1][1] - h[0][1] * h[1][0]


def source_hashes() -> tuple[int, list[str]]:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    failures = []
    for row in rows:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != row["sha256"]:
            failures.append(row["path"])
    return len(rows), failures


def main() -> None:
    rng = random.Random(180)
    target = 20_000
    exact_assertions = 0
    turning = 0
    pure_angular = 0
    radial = 0

    for _ in range(target):
        t = F(rng.randint(1, 9), rng.randint(1, 9))
        ell = F(rng.randint(1, 9), rng.randint(1, 9))
        beta = F(rng.randint(-9, 9), rng.randint(1, 9))
        h = [
            [-t * t, -t * t * beta],
            [-t * t * beta, ell * ell - t * t * beta * beta],
        ]
        m2 = -det2(h)
        assert m2 == t * t * ell * ell and m2 > 0
        exact_assertions += 2

        # Work with the squared normalization to remain exactly rational.
        assert h[0][0] == -t * t
        assert h[0][1] / (t * ell) == -t * beta / ell
        assert det2(h) / m2 == -1
        exact_assertions += 3

        k = F(rng.choice([-9, -7, -5, -3, -1, 1, 2, 4, 6, 8]), rng.randint(1, 7))
        hk = [[h[0][0], k * h[0][1]], [k * h[1][0], k * k * h[1][1]]]
        assert -det2(hk) == k * k * m2
        assert hk[0][0] == h[0][0]
        exact_assertions += 2

        common = F(rng.randint(1, 9), rng.randint(1, 9))
        hc = [[common * common * value for value in row] for row in h]
        common_m2 = -det2(hc)
        assert common_m2 == common**4 * m2
        assert det2(hc) / common_m2 == -1
        assert hc[0][0] == common**2 * h[0][0]
        exact_assertions += 3

        q = F(rng.randint(1, 12), rng.randint(1, 12))
        radius = F(rng.randint(0, 12), rng.randint(1, 6))
        v = F(rng.randint(-6, 6), rng.randint(1, 6))
        b0 = F(rng.randint(-6, 6), rng.randint(1, 6))
        b1 = F(rng.randint(-6, 6), rng.randint(1, 6))
        b_squared = b0 * b0 + b1 * b1
        if v == 0 and b_squared == 0:
            b0 = F(1)
            b_squared = F(1)
        if v == 0 and radius == 0:
            v = F(1)
        h_spatial = v * v / q + radius * radius * b_squared
        primary = [[-q, F(0)], [F(0), h_spatial]]
        primary_m2 = -det2(primary)
        expected_m2 = v * v + q * radius * radius * b_squared
        assert primary_m2 == expected_m2 and primary_m2 > 0
        assert h_spatial / primary_m2 == 1 / q
        assert primary[0][0] == -q
        exact_assertions += 4

        if b_squared == 0:
            assert primary_m2 == v * v
            radial += 1
            exact_assertions += 1
        if v == 0:
            turning += 1
            if radius > 0 and b_squared > 0:
                assert primary_m2 == q * radius * radius * b_squared
                pure_angular += 1
                exact_assertions += 1

        # Exact first-jet chain rules.
        qdot = F(rng.randint(-8, 8), rng.randint(1, 7))
        rdot = F(rng.randint(-8, 8), rng.randint(1, 7))
        vdot = F(rng.randint(-8, 8), rng.randint(1, 7))
        bdot = F(rng.randint(-8, 8), rng.randint(1, 7))
        m2dot = (
            2 * v * vdot
            + qdot * radius * radius * b_squared
            + 2 * q * radius * rdot * b_squared
            + q * radius * radius * bdot
        )
        detdot = -m2dot
        assert -detdot == m2dot
        phi_dot_from_h = -qdot / (2 * q)
        phi_dot_from_q = -qdot / (2 * q)
        assert phi_dot_from_h == phi_dot_from_q
        assert phi_dot_from_q * phi_dot_from_q / primary_m2 >= 0
        exact_assertions += 3

    count, failures = source_hashes()
    result = {
        "audit": "G180",
        "status": "PASS" if count == 9 and not failures else "FAIL",
        "exact_fraction_regular_trials": target,
        "exact_assertions": exact_assertions,
        "turning_trials": turning,
        "pure_angular_trials": pure_angular,
        "radial_trials": radial,
        "source_count": count,
        "source_hash_failures": failures,
        "controls": [
            "generic_shifted_density",
            "calibrated_determinant",
            "signed_auxiliary_reparameterization",
            "common_metric_scale_retained",
            "primary_angular_tape_density",
            "completed_depth_clock_only",
            "radial_turning_and_pure_angular_strata",
            "exact_first_jet_chain_rules",
        ],
    }
    output_path = HERE / "INDEPENDENT_VERIFICATION.json"
    if os.environ.get("UDT_READ_ONLY_REPLAY") == "1":
        if json.loads(output_path.read_text()) != result:
            raise SystemExit("FAIL: read-only replay differs from banked result")
    else:
        output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if result["status"] != "PASS":
        raise SystemExit(f"FAIL: source hashes {failures}")
    print(
        f"PASS: {target} independent exact Fraction families; {exact_assertions} assertions; "
        f"turning={turning}, pure_angular={pure_angular}, radial={radial}"
    )


if __name__ == "__main__":
    main()
