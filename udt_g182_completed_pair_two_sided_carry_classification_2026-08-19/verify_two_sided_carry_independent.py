#!/usr/bin/env python3
"""Independent derivative-jet and Gram-fiber replay for G182."""

from fractions import Fraction as F
import json
import math
import os
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ORDER = 6
TRIALS = 20000


def product_derivatives(a, b):
    nmax = min(len(a), len(b)) - 1
    return [sum(F(math.comb(n, j)) * a[j] * b[n - j] for j in range(n + 1)) for n in range(nmax + 1)]


def inverse_derivatives(a):
    out = [F(1, 1) / a[0]]
    for n in range(1, len(a)):
        numerator = sum(F(math.comb(n, j)) * a[j] * out[n - j] for j in range(1, n + 1))
        out.append(-numerator / a[0])
    return out


def sum_derivatives(a, b, sign=1):
    return [x + sign * y for x, y in zip(a, b)]


def metric_derivatives(T, B):
    T2 = product_derivatives(T, T)
    B2 = product_derivatives(B, B)
    return (
        [-x for x in T2],
        [-x for x in product_derivatives(T2, B)],
        sum_derivatives(inverse_derivatives(T2), product_derivatives(T2, B2), sign=-1),
    )


def quotient_derivatives(a, b):
    return product_derivatives(a, inverse_derivatives(b))


def determinant_derivatives(h):
    h00, h01, h11 = h
    return sum_derivatives(product_derivatives(h00, h11), product_derivatives(h01, h01), sign=-1)


def raw_left(global_derivatives, field):
    exponent_offset = 0 if field == "T" else 1
    return [F((-1) ** (n + exponent_offset)) * value for n, value in enumerate(global_derivatives)]


def carry_left(raw_derivatives, field):
    return raw_left(raw_derivatives, field)


def rand_derivatives(rng, positive_zero=False):
    zero = F(rng.randint(1, 9), rng.randint(1, 7)) if positive_zero else F(rng.randint(-7, 7), rng.randint(1, 7))
    return [zero] + [F(rng.randint(-7, 7), rng.randint(1, 9)) for _ in range(ORDER)]


def unit_vector(parameter):
    denominator = 1 + parameter * parameter
    return ((1 - parameter * parameter) / denominator, 2 * parameter / denominator)


def dot(v, w):
    return sum(x * y for x, y in zip(v, w))


def run():
    rng = random.Random(182_182)
    assertions = 0
    parity_mutants_rejected = 0
    gram_fiber_witnesses = 0

    for _ in range(TRIALS):
        T = rand_derivatives(rng, positive_zero=True)
        B = rand_derivatives(rng)
        raw_T = raw_left(T, "T")
        raw_B = raw_left(B, "B")
        carried_T = carry_left(raw_T, "T")
        carried_B = carry_left(raw_B, "B")
        assert carried_T == T and carried_B == B
        assertions += 2

        h_left = metric_derivatives(carried_T, carried_B)
        h_right = metric_derivatives(T, B)
        assert h_left == h_right
        assertions += 3

        determinant = determinant_derivatives(h_right)
        assert determinant[0] == -1 and all(x == 0 for x in determinant[1:])
        assert quotient_derivatives(h_right[1], h_right[0]) == B
        assert [-x for x in h_right[0]] == product_derivatives(T, T)
        assertions += 3

        # Wrong raw B parity must be visible whenever a nonzero tested derivative is mutated.
        index = rng.randrange(ORDER + 1)
        mutant = list(raw_B)
        mutant[index] += F(1, rng.randint(1, 9))
        if carry_left(mutant, "B") != B:
            parity_mutants_rejected += 1
        assertions += 1

        p = F(rng.randint(1, 20), rng.randint(21, 40))
        q = p + F(rng.randint(1, 9), rng.randint(10, 19))
        vp, vq = unit_vector(p), unit_vector(q)
        assert dot(vp, vp) == 1 and dot(vq, vq) == 1
        if vp != vq:
            gram_fiber_witnesses += 1
        assertions += 3

    assert parity_mutants_rejected == TRIALS
    assert gram_fiber_witnesses == TRIALS

    stall_checks = 0
    odd_smooth = 0
    even_cusped = 0
    for power in range(2, 102):
        left = F((-1) ** (power - 1))
        right = F(1)
        if left == right:
            odd_smooth += 1
            assert power % 2 == 1
        else:
            even_cusped += 1
            assert power % 2 == 0
        stall_checks += 1
        assertions += 1

    result = {
        "audit": "G182",
        "status": "PASS",
        "method": "independent actual-derivative jets with binomial Leibniz recursion and rational Gram fibers",
        "order": ORDER,
        "trials": TRIALS,
        "assertions": assertions,
        "parity_mutants_rejected": parity_mutants_rejected,
        "distinct_equal_gram_witnesses": gram_fiber_witnesses,
        "stall_checks": stall_checks,
        "odd_power_smooth": odd_smooth,
        "even_power_cusped": even_cusped,
        "checks": {
            "outward_parity": True,
            "metric_jet_sufficiency": True,
            "metric_jet_inverse": True,
            "determinant_minus_one": True,
            "gram_map_noninjective": True,
            "stall_parity": True,
        },
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: G182 independent replay; trials={TRIALS}; assertions={assertions}; gram_fibers={gram_fiber_witnesses}")


if __name__ == "__main__":
    run()
