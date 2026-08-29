#!/usr/bin/env python3
"""Exact production checks for the preregistered G298 one-jet transfer."""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def minkowski_dot(x, y):
    return -x[0] * y[0] + sum(a * b for a, b in zip(x[1:], y[1:]))


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def scale(a, x):
    return tuple(a * b for b in x)


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def det3(columns):
    a, b, c = columns
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def target_state(r, w1, w2):
    w2norm = w1 * w1 + w2 * w2
    gamma = (r + 1 / r + r * w2norm) / 2
    a = gamma - 1 / r
    u_y = (gamma, a, w1, w2)
    return gamma, a, u_y


def transferred_pair(r, w1, w2):
    u_x = (F(1), F(0), F(0), F(0))
    n_x = (F(0), F(1), F(0), F(0))
    k = add(u_x, n_x)
    gamma, a, u_y = target_state(r, w1, w2)
    v0 = scale(r, u_y)
    v1 = n_x  # flat-control representative of P_gamma n_X
    h00 = minkowski_dot(v0, v0)
    h01 = minkowski_dot(v0, v1)
    h11 = minkowski_dot(v1, v1)
    det_h = h00 * h11 - h01 * h01
    n_y = sub(scale(r, k), u_y)
    return {
        "u_x": u_x,
        "n_x": n_x,
        "k": k,
        "gamma": gamma,
        "a": a,
        "u_y": u_y,
        "v0": v0,
        "v1": v1,
        "h": (h00, h01, h11),
        "det_h": det_h,
        "n_y": n_y,
    }


def verify_sources():
    checked = 0
    for line in (ROOT / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
        digest, rel = line.split("\t")
        got = hashlib.sha256((REPO / rel).read_bytes()).hexdigest()
        assert got == digest, rel
        checked += 1
    return checked


def main():
    source_hashes = verify_sources()
    checks = 0
    cases = 0

    r_values = [F(n, d) for n in range(1, 8) for d in range(1, 6)]
    w_values = [F(-2), F(-1), F(0), F(1, 2), F(1), F(2)]
    for r in r_values:
        for w1 in w_values:
            for w2 in w_values:
                z = transferred_pair(r, w1, w2)
                cases += 1
                assert minkowski_dot(z["u_x"], z["u_x"]) == -1
                assert minkowski_dot(z["n_x"], z["n_x"]) == 1
                assert minkowski_dot(z["u_x"], z["n_x"]) == 0
                assert minkowski_dot(z["k"], z["k"]) == 0
                assert minkowski_dot(z["u_y"], z["u_y"]) == -1
                assert -minkowski_dot(z["k"], z["u_y"]) == 1 / r
                assert minkowski_dot(z["n_y"], z["n_y"]) == 1
                assert minkowski_dot(z["u_y"], z["n_y"]) == 0
                assert z["h"] == (-r * r, r * z["a"], F(1))
                assert z["det_h"] == -r * r * (1 + z["a"] * z["a"])
                assert z["det_h"] < 0
                assert -z["h"][0] == r * r
                assert z["h"][2] - z["h"][1] ** 2 / z["h"][0] == 1 + z["a"] ** 2
                assert (-z["det_h"]) == r * r * (1 + z["a"] ** 2)
                checks += 14

    # Active-screen discriminator: two separately natural projections are both regular and recover
    # the same clock depth, but their planes are gauge-inequivalent when W is active. This is an
    # algebraic projection witness; it does not certify that both projections retain the same
    # complete path-labelled relation state.
    planar = transferred_pair(F(2), F(0), F(0))
    screened = transferred_pair(F(2), F(1), F(0))
    assert planar["h"] != screened["h"]
    local_h_planar = tuple(
        minkowski_dot(x, y)
        for x, y in (
            (planar["v0"], planar["v0"]),
            (planar["v0"], planar["n_y"]),
            (planar["n_y"], planar["n_y"]),
        )
    )
    local_h_screened = tuple(
        minkowski_dot(x, y)
        for x, y in (
            (screened["v0"], screened["v0"]),
            (screened["v0"], screened["n_y"]),
            (screened["n_y"], screened["n_y"]),
        )
    )
    assert local_h_planar == (-F(4), F(0), F(1))
    assert local_h_screened == (-F(4), F(0), F(1))
    assert planar["v0"] != screened["v0"]
    checks += 4

    local_v0 = screened["v0"]
    local_v1 = screened["n_y"]
    assert minkowski_dot(local_v0, local_v0) == -F(4)
    assert minkowski_dot(local_v0, local_v1) == 0
    assert minkowski_dot(local_v1, local_v1) == 1
    # Three-vector rank is 3, so no calibrated pair-domain basis change identifies the planes.
    assert det3((local_v0[:3], screened["v1"][:3], local_v1[:3])) == -F(4)
    checks += 4

    # Full-vector screen orientation survives even when the pair Gram matrix sees only ||W||.
    screen_x = transferred_pair(F(3, 2), F(1), F(0))
    screen_y = transferred_pair(F(3, 2), F(0), F(1))
    assert screen_x["h"] == screen_y["h"]
    assert screen_x["v0"] != screen_y["v0"]
    checks += 2

    # Positive affine rescaling cancels in k/omega and the endpoint frequency ratio.
    c = F(7, 3)
    base = transferred_pair(F(5, 3), F(2, 3), F(-1, 2))
    omega_x = F(1)
    omega_y = F(3, 5)
    assert scale(1 / (c * omega_x), scale(c, base["k"])) == base["k"]
    assert (c * omega_x) / (c * omega_y) == F(5, 3)
    checks += 2

    # Constant homothety: g -> lambda^2 g and unit vectors -> lambda^-1 vectors leave h fixed.
    lam = F(11, 4)
    assert lam * lam * minkowski_dot(scale(1 / lam, base["v0"]), scale(1 / lam, base["v0"])) == base["h"][0]
    assert lam * lam * minkowski_dot(scale(1 / lam, base["v0"]), scale(1 / lam, base["v1"])) == base["h"][1]
    assert lam * lam * minkowski_dot(scale(1 / lam, base["v1"]), scale(1 / lam, base["v1"])) == base["h"][2]
    checks += 3

    # Flat-cylinder antipodal routes: both are regular and the reflection isometry swaps them.
    u = (F(1), F(0), F(0), F(0))
    n_plus = (F(0), F(1), F(0), F(0))
    n_minus = (F(0), F(-1), F(0), F(0))
    branches = {(u, n_plus), (u, n_minus)}
    reflected = {(v0, (v1[0], -v1[1], v1[2], v1[3])) for v0, v1 in branches}
    assert len(branches) == 2
    assert reflected == branches
    assert minkowski_dot(u, u) == -1
    assert minkowski_dot(n_plus, n_plus) == 1
    assert minkowski_dot(n_minus, n_minus) == 1
    checks += 5

    result = {
        "landing": "MULTIPLE_INEQUIVALENT_NATURAL_PAIR_ONE_JET_PROJECTIONS_SURVIVE_FROM_THE_DERIVED_COMPLETE_RELATION_STATE__NO_UNIQUE_TRANSFER_TO_G2_IS_OWNED",
        "grade": "INTERNALLY_DERIVED_WITH_CAVEATS",
        "preregistered_commit": "c7128f21",
        "source_hashes": source_hashes,
        "exact_cases": cases,
        "exact_assertions": checks,
        "pair_metric": ["-r^2", "r*a", "1"],
        "det_pair_metric": "-r^2*(1+a^2)",
        "terminal_depth": "Phi=-log(r)",
        "branch_output": "set-valued complete directed-leg relation state with nonunique natural pair-one-jet projections",
        "nonuniqueness_witness": "active-screen rank-3 separator between transported-source and target-local ruler planes",
        "higher_germ": "OPEN",
        "history_population_dynamics": "OPEN",
    }
    if "--no-write" not in sys.argv:
        (ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
