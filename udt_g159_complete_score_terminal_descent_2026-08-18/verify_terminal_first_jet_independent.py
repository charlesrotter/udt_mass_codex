#!/usr/bin/env python3
"""Independent Fraction replay of G159 terminal first-jet descent."""

from __future__ import annotations

import csv
import hashlib
import json
import random
import subprocess
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "bd2ba87a"
LANDING = (
    "CALIBRATED_PAIR_FIRST_JET_DERIVED__COMPLETE_SCORE_DESCENDS_WITH_DOTJ_LIVE__"
    "H_AND_DOTH_LIVE_LORENTZ_COFRAME_GAUGE_INVARIANT__KAPPA_DENSITY_COEFFICIENT_"
    "AND_PHI_BETA_CEFF_REQUIRE_PAIR_CALIBRATION_CARRY__PHYSICAL_HISTORY_QUERY_"
    "LAMBDA_AND_GLOBAL_COMPLETION_OPEN"
)


def read_tsv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest():
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == 7
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"],
            cwd=ROOT, check=True, stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"])
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]
    return len(rows)


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c, a):
    return [[c * value for value in row] for row in a]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert det
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


class Dual:
    """First-order dual number, independent of the production SymPy path."""

    def __init__(self, value, derivative=F(0)):
        self.value = F(value)
        self.derivative = F(derivative)

    def __add__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(self.value + other.value, self.derivative + other.derivative)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Dual) else -Dual(other))

    def __rsub__(self, other):
        return Dual(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(
            self.value * other.value,
            self.derivative * other.value + self.value * other.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(
            self.value / other.value,
            (self.derivative * other.value - self.value * other.derivative)
            / other.value**2,
        )

    def __rtruediv__(self, other):
        return Dual(other) / self


def dual_mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Dual(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def dual_transpose(a):
    return [list(row) for row in zip(*a)]


def dual_terminal_rates(h_dual):
    """Differentiate terminal definitions, not the registered rate formulas."""
    det = h_dual[0][0] * h_dual[1][1] - h_dual[0][1] * h_dual[0][1]
    minus_det = -det
    minus_h00 = -h_dual[0][0]
    kappa_dot = minus_det.derivative / (4 * minus_det.value)
    phi_dot = (
        minus_det.derivative / minus_det.value
        - 2 * minus_h00.derivative / minus_h00.value
    ) / 4
    beta_dot = (h_dual[0][1] / h_dual[0][0]).derivative
    log_ceff_dot = (
        minus_h00.derivative / minus_h00.value
        - minus_det.derivative / (2 * minus_det.value)
    )
    return kappa_dot, phi_dot, beta_dot, log_ceff_dot


ETA = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)],
       [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]


def pair_metric(v):
    return mm(mm(transpose(v), ETA), v)


def pair_first_jet(v, p):
    return add(mm(mm(transpose(p), ETA), v), mm(mm(transpose(v), ETA), p))


def rates(h, dh):
    det = h[0][0] * h[1][1] - h[0][1] * h[0][1]
    det_dot = dh[0][0] * h[1][1] + h[0][0] * dh[1][1] - 2 * h[0][1] * dh[0][1]
    kd = det_dot / (4 * det)
    pd = kd - dh[0][0] / (2 * h[0][0])
    bd = (dh[0][1] * h[0][0] - h[0][1] * dh[0][0]) / (h[0][0] ** 2)
    return kd, pd, bd


def random_m(rng, rows, cols, lo=-3, hi=3):
    return [[F(rng.randint(lo, hi)) for _ in range(cols)] for _ in range(rows)]


def rational_lorentz(r, u):
    ch = (1 + r * r) / (1 - r * r)
    sh = 2 * r / (1 - r * r)
    co = (1 - u * u) / (1 + u * u)
    si = 2 * u / (1 + u * u)
    return [[ch, sh, F(0), F(0)], [sh, ch, F(0), F(0)],
            [F(0), F(0), co, -si], [F(0), F(0), si, co]]


def lorentz_generator(boost_rate, rotation_rate):
    return [[F(0), boost_rate, F(0), F(0)],
            [boost_rate, F(0), F(0), F(0)],
            [F(0), F(0), F(0), -rotation_rate],
            [F(0), F(0), rotation_rate, F(0)]]


def main():
    source_count = verify_manifest()
    rng = random.Random(159)
    trials = 500
    executed = 0
    attempts = 0
    while executed < trials:
        attempts += 1
        v = random_m(rng, 4, 2)
        p = random_m(rng, 4, 2)
        h = pair_metric(v)
        det = h[0][0] * h[1][1] - h[0][1] ** 2
        if not (h[0][0] < 0 and det < 0):
            continue
        dh = pair_first_jet(v, p)
        kd, pd, bd = rates(h, dh)
        h_dual = [[Dual(h[i][j], dh[i][j]) for j in range(2)] for i in range(2)]
        dkd, dpd, dbd, dceff = dual_terminal_rates(h_dual)
        assert (dkd, dpd, dbd) == (kd, pd, bd)
        assert dceff == -2 * pd
        assert dh[0][1] == dh[1][0]

        # Exact arbitrary live pair rechart.
        while True:
            a = random_m(rng, 2, 2, -2, 2)
            if a[0][0] * a[1][1] - a[0][1] * a[1][0] <= 0:
                continue
            ha = mm(mm(transpose(a), h), a)
            if ha[0][0] < 0:
                break
        da = random_m(rng, 2, 2)
        dha = add(add(mm(mm(transpose(da), h), a), mm(mm(transpose(a), dh), a)),
                  mm(mm(transpose(a), h), da))
        kda, pda, bda = rates(ha, dha)
        a_dual = [[Dual(a[i][j], da[i][j]) for j in range(2)] for i in range(2)]
        ha_dual = dual_mm(dual_mm(dual_transpose(a_dual), h_dual), a_dual)
        assert [[x.value for x in row] for row in ha_dual] == ha
        assert [[x.derivative for x in row] for row in ha_dual] == dha
        dkda, dpda, dbda, dceffa = dual_terminal_rates(ha_dual)
        assert (dkda, dpda, dbda) == (kda, pda, bda)
        assert dceffa == -2 * pda
        assert kda - kd == trace(mm(inv2(a), da)) / 2
        clock_shift = dha[0][0] / ha[0][0] - dh[0][0] / h[0][0]
        assert pda - pd == trace(mm(inv2(a), da)) / 2 - clock_shift / 2
        assert bda == (dha[0][1] * ha[0][0] - ha[0][1] * dha[0][0]) / ha[0][0] ** 2

        # Exact live Lorentz coframe gauge.
        r = F(rng.randint(-2, 2), 5)
        u = F(rng.randint(-3, 3), 7)
        lam = rational_lorentz(r, u)
        gen = lorentz_generator(F(rng.randint(-2, 2)), F(rng.randint(-2, 2)))
        dlam = mm(gen, lam)
        assert mm(mm(transpose(lam), ETA), lam) == ETA
        assert add(mm(mm(transpose(dlam), ETA), lam), mm(mm(transpose(lam), ETA), dlam)) == scale(F(0), eye(4))
        vp = mm(lam, v)
        pp = add(mm(dlam, v), mm(lam, p))
        assert pair_metric(vp) == h
        assert pair_first_jet(vp, pp) == dh
        assert rates(pair_metric(vp), pair_first_jet(vp, pp)) == (kd, pd, bd)
        executed += 1

    # Independent live diagonal recalibration and query-motion witnesses.
    h = [[F(-2), F(1)], [F(1), F(3)]]
    dh = [[F(3), F(-1)], [F(-1), F(4)]]
    kd, pd, bd = rates(h, dh)
    aa, bb, daa, dbb = F(2), F(3), F(5), F(-2)
    ad, dad = [[aa, F(0)], [F(0), bb]], [[daa, F(0)], [F(0), dbb]]
    hd = mm(mm(transpose(ad), h), ad)
    dhd = add(add(mm(mm(transpose(dad), h), ad), mm(mm(transpose(ad), dh), ad)),
              mm(mm(transpose(ad), h), dad))
    kdd, pdd, bdd = rates(hd, dhd)
    beta = h[0][1] / h[0][0]
    assert kdd - kd == (daa / aa + dbb / bb) / 2
    assert pdd - pd == (dbb / bb - daa / aa) / 2
    assert hd[0][1] / hd[0][0] == bb * beta / aa
    assert bdd == bb / aa * (bd + beta * (dbb / bb - daa / aa))
    # Logarithmic rate avoids introducing an irrational square root into Fraction arithmetic.
    assert -2 * pdd == -2 * pd + daa / aa - dbb / bb

    vq = [[F(1), F(0)], [F(0), F(1)], [F(0), F(0)], [F(0), F(0)]]
    pq = [[F(0), F(1)], [F(0), F(1)], [F(0), F(0)], [F(0), F(0)]]
    assert rates(pair_metric(vq), pair_first_jet(vq, pq)) == (F(1, 2), F(1, 2), F(1))

    result = {
        "status": "PASS",
        "method": "stdlib_fraction_independent_pair_metric_rechart_and_lorentz_replay",
        "registered_outcome_class": (
            "CALIBRATED_PAIR_FIRST_JET_DERIVED__H_DOTH_LORENTZ_GAUGE_INVARIANT__"
            "TERMINAL_COMPONENTS_REQUIRE_CALIBRATION_CARRY"
        ),
        "landing": LANDING,
        "source_count": source_count,
        "exact_fraction_trials": executed,
        "attempts": attempts,
        "live_lorentz_gauge_trials": executed,
        "arbitrary_live_gl2_rechart_trials": executed,
        "independent_dual_number_definition_derivative_trials": executed,
        "query_motion_witnesses": 1,
        "query_motion_frozen": False,
        "h_and_doth_lorentz_coframe_gauge_invariant": True,
        "terminal_coefficients_arbitrary_gl2_invariant": False,
        "physical_history_derived": False,
        "physical_lambda_owned": False,
        "calibration_carry_derived": False,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
