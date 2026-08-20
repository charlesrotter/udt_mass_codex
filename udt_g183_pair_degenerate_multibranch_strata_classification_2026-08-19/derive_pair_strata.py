#!/usr/bin/env python3
"""Dependency-free exact production derivation for G183."""

from fractions import Fraction as F
import json
import os
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TRIALS = 12000


def dot(v, w):
    return -v[0] * w[0] + sum(v[i] * w[i] for i in range(1, 4))


def sub(v, w):
    return tuple(v[i] - w[i] for i in range(4))


def scale(a, v):
    return tuple(a * value for value in v)


def gram(u, v):
    return (dot(u, u), dot(u, v), dot(v, v))


def determinant(h):
    return h[0] * h[2] - h[1] * h[1]


def independent(u, v):
    return any(u[i] * v[j] - u[j] * v[i] != 0 for i in range(4) for j in range(i + 1, 4))


def run():
    rng = random.Random(183_0819)
    assertions = 0
    dependent_trials = 0
    independent_trials = 0

    for trial in range(TRIALS):
        spatial = [F(rng.randint(-6, 6), rng.randint(1, 5)) for _ in range(3)]
        time = sum(abs(value) for value in spatial) + F(rng.randint(1, 5), rng.randint(1, 4))
        u = (time, *spatial)
        assert dot(u, u) < 0
        assertions += 1

        if trial % 4 == 0:
            factor = F(rng.randint(-7, 7), rng.randint(1, 6))
            v = scale(factor, u)
            dependent_trials += 1
        else:
            while True:
                v = tuple(F(rng.randint(-8, 8), rng.randint(1, 7)) for _ in range(4))
                if independent(u, v):
                    break
            independent_trials += 1

        h = gram(u, v)
        det_h = determinant(h)
        alpha = h[1] / h[0]
        orthogonal = sub(v, scale(alpha, u))
        orthogonal_norm = dot(orthogonal, orthogonal)
        assert dot(u, orthogonal) == 0
        assert det_h == h[0] * orthogonal_norm
        assert orthogonal_norm >= 0
        assert (det_h == 0) == (not independent(u, v))
        assert (det_h < 0) == independent(u, v)
        assertions += 5

    # A null path inside a regular pair plane is not pair-plane degeneracy.
    regular_h = (F(-1), F(0), F(1))
    null_path_tangent = (F(1), F(1))
    null_path_norm = regular_h[0] * null_path_tangent[0] ** 2 + regular_h[2] * null_path_tangent[1] ** 2
    assert determinant(regular_h) == -1 and null_path_norm == 0
    assertions += 2

    # A null chosen clock can coexist with a nondegenerate Lorentzian plane.
    null_clock = (F(1), F(1), F(0), F(0))
    ruler = (F(0), F(1), F(0), F(0))
    h_null_clock = gram(null_clock, ruler)
    replacement_clock = sub(null_clock, ruler)
    assert h_null_clock == (0, 1, 1)
    assert determinant(h_null_clock) == -1
    assert dot(replacement_clock, replacement_clock) == -1
    assertions += 3

    # A rank-two null plane may have degenerate induced metric without map rank loss.
    null_generator = (F(1), F(1), F(0), F(0))
    transverse_spacelike = (F(0), F(0), F(1), F(0))
    h_null_plane = gram(null_generator, transverse_spacelike)
    assert h_null_plane == (0, 0, 1)
    assert determinant(h_null_plane) == 0
    assert independent(null_generator, transverse_spacelike)
    assertions += 3

    # A rank-two spacelike plane has no valid observer clock.
    spacelike_a = (F(0), F(1), F(0), F(0))
    spacelike_b = (F(0), F(0), F(1), F(0))
    h_spacelike = gram(spacelike_a, spacelike_b)
    assert h_spacelike == (1, 0, 1)
    assert determinant(h_spacelike) > 0
    assert independent(spacelike_a, spacelike_b)
    assertions += 3

    # Genuine rank loss with a timelike clock.
    timelike = (F(1), F(0), F(0), F(0))
    proportional = scale(F(7, 3), timelike)
    h_rank_loss = gram(timelike, proportional)
    assert h_rank_loss[0] < 0 and determinant(h_rank_loss) == 0 and not independent(timelike, proportional)
    assertions += 3

    # Exact flat normal-exponential (Rindler) focus at tau=0.
    acceleration = F(3, 2)
    focus_s = -1 / acceleration
    for s in (F(0), F(1, 5), focus_s):
        v_tau = (1 + acceleration * s, F(0), F(0), F(0))
        v_s = (F(0), F(1), F(0), F(0))
        h = gram(v_tau, v_s)
        assert h == (-(1 + acceleration * s) ** 2, 0, 1)
        if s == focus_s:
            assert v_tau == (0, 0, 0, 0) and determinant(h) == 0
        else:
            assert independent(v_tau, v_s) and determinant(h) < 0
        assertions += 3

    # Two polynomial branches: same endpoints and metric, different endpoint tangents.
    for s in (F(0), F(1, 4), F(1, 2), F(1)):
        p_plus = (s, s * (1 - s))
        p_minus = (s, -s * (1 - s))
        t_plus = (F(1), 1 - 2 * s)
        t_minus = (F(1), -(1 - 2 * s))
        speed_plus = t_plus[0] ** 2 + t_plus[1] ** 2
        speed_minus = t_minus[0] ** 2 + t_minus[1] ** 2
        assert speed_plus == speed_minus
        if s in (0, 1):
            assert p_plus == p_minus and t_plus != t_minus
        assertions += 2

    # Exact winding family on R x S1 with circumference 2 and antipode theta=1.
    winding = []
    for n in range(-20, 21):
        lift = F(1 + 2 * n)
        h = (F(-1), F(0), lift * lift)
        assert determinant(h) < 0
        assert lift % 2 == 1  # identical endpoint modulo the circumference
        winding.append({"n": n, "lift": int(lift), "h11": int(lift * lift), "Phi": 0})
        assertions += 2
    assert winding[20]["h11"] == winding[19]["h11"] == 1  # n=0 and n=-1
    assert winding[20]["lift"] != winding[19]["lift"]
    assertions += 2

    result = {
        "audit": "G183",
        "landing_candidate": "PAIR_STRATA_SEPARATED__REGULAR_MULTIBRANCH_KERNEL_REMAINS_BRANCH_LABELLED",
        "trials": TRIALS,
        "dependent_trials": dependent_trials,
        "independent_trials": independent_trials,
        "assertions": assertions,
        "checks": {
            "null_curve_regular_plane": True,
            "null_clock_chart_not_plane_degeneracy": True,
            "rank_two_null_plane_metric_degeneracy": True,
            "rank_two_spacelike_plane_outside_domain": True,
            "timelike_clock_det_zero_iff_rank_loss": True,
            "sampled_focal_rank_loss": True,
            "regular_crossing_branches_survive": True,
            "winding_branches_survive": True,
            "scalar_and_metric_do_not_select_branch": True,
        },
        "witnesses": {
            "null_path": {"h": [-1, 0, 1], "path_tangent": [1, 1], "path_norm": 0},
            "null_clock": {"h": [0, 1, 1], "det": -1, "timelike_replacement_norm": -1},
            "null_plane": {"h": [0, 0, 1], "det": 0, "tangent_rank": 2},
            "spacelike_plane": {"h": [1, 0, 1], "det": 1, "tangent_rank": 2},
            "rank_loss": {"h": [str(value) for value in h_rank_loss], "rank": 1},
            "rindler_focus": {"acceleration": str(acceleration), "s_focus": str(focus_s), "rank": 1},
            "polynomial_pair": {"same_metric": True, "same_endpoints": True, "different_endpoint_tangents": True},
            "winding": winding,
        },
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: G183 exact pair strata; trials={TRIALS}; assertions={assertions}")


if __name__ == "__main__":
    run()
