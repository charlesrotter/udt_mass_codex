#!/usr/bin/env python3
"""Independent exact-rational and numerical replay for G157."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import subprocess
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "7b783451"
LANDING = (
    "MIXED_REGRADING__BPLUS2_NO_FIXED_CHANNEL_RATIO_DERIVED__"
    "REGIME_DEPENDENT_BASE_BALANCE_ALLOWED_BY_NATIVE_SEMIDIRECT_COMPOSITION__"
    "SUPPLIED_VALUED_HISTORY_CAN_CARRY_CHANGING_SCORE__FULL_SCREEN_MIXING_"
    "COMPOSITION_PHYSICAL_CROSS_QUERY_CARRY_AND_HISTORY_EVOLUTION_REMAIN_OPEN"
)


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def inv(a):
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / determinant, -a[0][1] / determinant], [F(0), a[0][0] / determinant]]


def eq(a, b):
    return all(a[i][j] == b[i][j] for i in range(2) for j in range(2))


def tri(a, n, d):
    return [[F(a), F(n)], [F(0), F(d)]]


def c_float(sigma, delta, mu):
    a = math.exp(sigma - delta)
    return [[a, a * mu], [0.0, math.exp(sigma + delta)]]


def close_matrix(a, b):
    return all(
        math.isclose(a[i][j], b[i][j], rel_tol=2e-11, abs_tol=2e-11)
        for i in range(2)
        for j in range(2)
    )


def main() -> None:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        manifest = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "REGRADING_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        ledger = list(csv.DictReader(handle, delimiter="\t"))
    assert len(manifest) == len(ledger) == 20
    for row in manifest:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"])
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]
    assert all(row["active_depth_only_lockstep"] == "NO" for row in ledger)

    rng = random.Random(157)
    trials = 500
    for _ in range(trials):
        a1, d1, a2, d2 = (rng.randint(1, 15) for _ in range(4))
        n1, n2 = (rng.randint(-10, 10) for _ in range(2))
        C1, C2 = tri(a1, n1, d1), tri(a2, n2, d2)
        product = mm(C2, C1)
        mu1, mu2 = F(n1, a1), F(n2, a2)
        ratio1 = F(d1, a1)  # exp(2 delta1)
        predicted_mu = mu1 + ratio1 * mu2
        assert F(product[0][1], product[0][0]) == predicted_mu
        assert product[0][0] == a2 * a1
        assert product[1][1] == d2 * d1

        inverse = inv(C1)
        assert eq(mm(inverse, C1), tri(1, 0, 1))
        inverse_mu = inverse[0][1] / inverse[0][0]
        assert inverse_mu == -F(a1, d1) * mu1

    # Arbitrary endpoint frames telescope even when their channel ratios vary.
    frames = [tri(1, 0, 1), tri(2, 1, 2), tri(3, 4, 5)]
    C10 = mm(frames[1], inv(frames[0]))
    C21 = mm(frames[2], inv(frames[1]))
    C20 = mm(frames[2], inv(frames[0]))
    assert eq(mm(C21, C10), C20)
    assert not eq(frames[2], mm(frames[1], frames[1]))

    # Numerically replay the stricter one-parameter subgroup law.
    nonzero_q_trials = 200
    for _ in range(nonzero_q_trials):
        p = rng.uniform(-2.0, 2.0)
        q = rng.choice((-1.0, 1.0)) * rng.uniform(0.1, 2.0)
        r = rng.uniform(-2.0, 2.0)
        t = rng.uniform(-1.0, 1.0)
        u = rng.uniform(-1.0, 1.0)

        def mu(x):
            return r * (math.exp(2 * q * x) - 1.0) / (2 * q)

        lhs = mu(t + u)
        rhs = mu(u) + math.exp(2 * q * u) * mu(t)
        assert math.isclose(lhs, rhs, rel_tol=2e-12, abs_tol=2e-12)
        assert close_matrix(
            mm(c_float(p * t, q * t, mu(t)), c_float(p * u, q * u, mu(u))),
            c_float(p * (t + u), q * (t + u), mu(t + u)),
        )

    zero_q_trials = 100
    for _ in range(zero_q_trials):
        p = rng.uniform(-2.0, 2.0)
        r = rng.uniform(-2.0, 2.0)
        t = rng.uniform(-1.0, 1.0)
        u = rng.uniform(-1.0, 1.0)
        assert math.isclose(r * (t + u), r * u + r * t, rel_tol=2e-12, abs_tol=2e-12)
        assert close_matrix(
            mm(c_float(p * t, 0.0, r * t), c_float(p * u, 0.0, r * u)),
            c_float(p * (t + u), 0.0, r * (t + u)),
        )

    result = {
        "status": "PASS",
        "method": "stdlib_fraction_exact_plus_independent_float_subgroup",
        "source_count": len(manifest),
        "ledger_count": len(ledger),
        "semidirect_exact_trials": trials,
        "endpoint_family_exact_trials": 1,
        "one_parameter_subgroup_trials": nonzero_q_trials + zero_q_trials,
        "one_parameter_subgroup_nonzero_q_trials": nonzero_q_trials,
        "one_parameter_subgroup_zero_q_trials": zero_q_trials,
        "active_depth_only_lockstep_sources": 0,
        "landing": LANDING,
        "registered_outcome_class": "MIXED_REGRADING",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
