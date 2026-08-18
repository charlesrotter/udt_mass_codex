#!/usr/bin/env python3
"""Independent exact Fraction/dual-number replay for G160."""

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
SOURCE_SNAPSHOT = "4a89d922"
LANDING = (
    "TIMELIVE_PAIR_FIRST_JET_CARRY_DERIVED__FULL_GLPLUS2_PULLBACK_AND_"
    "RIGHT_CONNECTION_COMPOSITION_EXACT__CARRY_CLOSURE_SUFFICIENT_NOT_"
    "NECESSARY_DUE_TO_LORENTZ_STABILIZER__ONLY_COMBINED_CARRIED_FIRST_JET_"
    "IS_LIVE_SOURCE_GAUGE_COVARIANT__JOINED_TOTAL_RATE_IS_LIVE_ENDPOINT_"
    "GAUGE_INVARIANT__KAPPA_HAS_UNIVERSAL_"
    "DETERMINANT_RATE__NO_PHI_BETA_CARRY_ONLY_LAW_ON_UNRESTRICTED_GLPLUS2__"
    "BPLUS2_SUFFICIENT_NOT_NECESSARY_FOR_EXACT_CHARACTER_LAWS__SCALAR_RATE_"
    "CLOSURE_WEAKER_THAN_MATRIX_RATE_CLOSURE__PHYSICAL_"
    "CARRY_HISTORY_QUERY_LAMBDA_AND_COMPLETION_OPEN"
)


class Dual:
    def __init__(self, value, derivative=F(0)):
        self.value, self.derivative = F(value), F(derivative)

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
        return Dual(self.value * other.value,
                    self.derivative * other.value + self.value * other.derivative)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(self.value / other.value,
                    (self.derivative * other.value - self.value * other.derivative)
                    / other.value**2)

    def __rtruediv__(self, other):
        return Dual(other) / self


def read_tsv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest():
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == 10
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"], cwd=ROOT,
            check=True, stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"])
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]
    return len(rows)


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    zero = Dual(0) if isinstance(a[0][0], Dual) or isinstance(b[0][0], Dual) else F(0)
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), zero)
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c, a):
    return [[c * value for value in row] for row in a]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert det
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def trace(a):
    return a[0][0] + a[1][1]


def dual(a, da):
    return [[Dual(a[i][j], da[i][j]) for j in range(len(a[0]))] for i in range(len(a))]


def values(a):
    return [[x.value for x in row] for row in a]


def derivatives(a):
    return [[x.derivative for x in row] for row in a]


def pull(h, dh, m, dm):
    hd, md = dual(h, dh), dual(m, dm)
    out = mm(mm(transpose(md), hd), md)
    return values(out), derivatives(out)


def terminal_from_dual(hd):
    det = hd[0][0] * hd[1][1] - hd[0][1] * hd[0][1]
    minus_det, minus_h00 = -det, -hd[0][0]
    kd = minus_det.derivative / (4 * minus_det.value)
    pd = (minus_det.derivative / minus_det.value
          - 2 * minus_h00.derivative / minus_h00.value) / 4
    bd = (hd[0][1] / hd[0][0]).derivative
    return kd, pd, bd


def random_matrix(rng, lo=-3, hi=3):
    return [[F(rng.randint(lo, hi)) for _ in range(2)] for _ in range(2)]


def random_glplus(rng):
    while True:
        m = random_matrix(rng)
        if m[0][0] * m[1][1] - m[0][1] * m[1][0] > 0:
            return m


def random_pair_metric(rng):
    t, ell = F(rng.randint(1, 4)), F(rng.randint(1, 4))
    beta = F(rng.randint(-3, 3), 2)
    r = [[t, t * beta], [F(0), ell]]
    eta = [[F(-1), F(0)], [F(0), F(1)]]
    return mm(mm(transpose(r), eta), r)


def main():
    source_count = verify_manifest()
    rng = random.Random(160)
    trials = 500

    for _ in range(trials):
        h, dh = random_pair_metric(rng), random_matrix(rng)
        dh[1][0] = dh[0][1]
        while True:
            m, dm = random_glplus(rng), random_matrix(rng)
            hbar, dhbar = pull(h, dh, m, dm)
            if hbar[0][0] < 0:
                break
        k = mm(dm, inv2(m))

        connection_form = add(add(dh, mm(transpose(k), h)), mm(h, k))
        assert dhbar == mm(mm(transpose(m), connection_form), m)

        # Independent derivative of terminal definitions.
        base_rates = terminal_from_dual(dual(h, dh))
        carried_rates = terminal_from_dual(dual(hbar, dhbar))
        assert carried_rates[0] - base_rates[0] == trace(k) / 2
        clock_shift = dhbar[0][0] / hbar[0][0] - dh[0][0] / h[0][0]
        assert carried_rates[1] - base_rates[1] == trace(k) / 2 - clock_shift / 2
        hd, md = dual(h, dh), dual(m, dm)
        m0 = [[md[0][0]], [md[1][0]]]
        m1 = [[md[0][1]], [md[1][1]]]
        numerator = mm(mm(transpose(m0), hd), m1)[0][0]
        denominator = mm(mm(transpose(m0), hd), m0)[0][0]
        assert carried_rates[2] == (numerator / denominator).derivative

        # Metric-self-adjoint/skew split.
        kdag = mm(mm(inv2(h), transpose(k)), h)
        symh = scale(F(1, 2), add(k, kdag))
        assert add(mm(transpose(k), h), mm(h, k)) == scale(F(2), mm(h, symh))
        raw = random_matrix(rng)
        rawdag = mm(mm(inv2(h), transpose(raw)), h)
        skewh = scale(F(1, 2), sub(raw, rawdag))
        assert add(mm(transpose(skewh), h), mm(h, skewh)) == [[F(0), F(0)], [F(0), F(0)]]

        # Closed A->B->C staged/direct carry.
        mba, dmba = random_glplus(rng), random_matrix(rng)
        mcb, dmcb = random_glplus(rng), random_matrix(rng)
        mca = mm(mcb, mba)
        dmca = add(mm(dmcb, mba), mm(mcb, dmba))
        hb, dhb = pull(h, dh, mcb, dmcb)
        staged_h, staged_dh = pull(hb, dhb, mba, dmba)
        direct_h, direct_dh = pull(h, dh, mca, dmca)
        assert (staged_h, staged_dh) == (direct_h, direct_dh)
        kba, kcb, kca = mm(dmba, inv2(mba)), mm(dmcb, inv2(mcb)), mm(dmca, inv2(mca))
        assert kca == add(kcb, mm(mm(mcb, kba), inv2(mcb)))

        # Independently supplied direct route and exact finite-defect right rate.
        mca_free, dmca_free = random_glplus(rng), random_matrix(rng)
        defect = mm(mm(mcb, mba), inv2(mca_free))
        ddefect = add(
            add(mm(mm(dmcb, mba), inv2(mca_free)),
                mm(mm(mcb, dmba), inv2(mca_free))),
            scale(F(-1), mm(mm(defect, dmca_free), inv2(mca_free))),
        )
        kdefect = mm(ddefect, inv2(defect))
        kca_free = mm(dmca_free, inv2(mca_free))
        predicted_defect = sub(
            add(kcb, mm(mm(mcb, kba), inv2(mcb))),
            mm(mm(defect, kca_free), inv2(defect)),
        )
        assert kdefect == predicted_defect

        # Live independent endpoint gauge covariance, obtained by dual products.
        pa, dpa = random_glplus(rng), random_matrix(rng)
        pb, dpb = random_glplus(rng), random_matrix(rng)
        pbd, pad = dual(pb, dpb), dual(pa, dpa)
        pbinvd = inv2(pbd)
        hp_d = mm(mm(transpose(pbd), dual(h, dh)), pbd)
        mp_d = mm(mm(pbinvd, dual(m, dm)), pad)
        outp = mm(mm(transpose(mp_d), hp_d), mp_d)
        expected = mm(mm(transpose(pad), dual(hbar, dhbar)), pad)
        assert values(outp) == values(expected)
        assert derivatives(outp) == derivatives(expected)

        # Total comparison score decomposition.
        ra, dra = random_glplus(rng), random_matrix(rng)
        rb, drb = random_glplus(rng), random_matrix(rng)
        c = mm(mm(rb, m), inv2(ra))
        dc = add(add(mm(mm(drb, m), inv2(ra)), mm(mm(rb, dm), inv2(ra))),
                 scale(F(-1), mm(mm(mm(mm(rb, m), inv2(ra)), dra), inv2(ra))))
        gamma = mm(dc, inv2(c))
        omega_a, omega_b = mm(dra, inv2(ra)), mm(drb, inv2(rb))
        predicted = sub(add(omega_b, mm(mm(rb, k), inv2(rb))),
                        mm(mm(c, omega_a), inv2(c)))
        assert gamma == predicted

        # The joined total comparison and its derivative are invariant under
        # the same live independent endpoint gauges.
        rap = mm(dual(ra, dra), pad)
        rbp = mm(dual(rb, drb), pbd)
        cp = mm(mm(rbp, mp_d), inv2(rap))
        assert values(cp) == c
        assert derivatives(cp) == dc

        # Independent total-transition right-rate composition.
        c1, dc1 = random_glplus(rng), random_matrix(rng)
        c2, dc2 = random_glplus(rng), random_matrix(rng)
        c21 = mm(c2, c1)
        dc21 = add(mm(dc2, c1), mm(c2, dc1))
        gamma1, gamma2 = mm(dc1, inv2(c1)), mm(dc2, inv2(c2))
        gamma21 = mm(dc21, inv2(c21))
        assert gamma21 == add(gamma2, mm(mm(c2, gamma1), inv2(c2)))

    # Independent B+(2) coefficient/rate classification.
    bplus_trials = 500
    for _ in range(bplus_trials):
        t, ell, a, d = [F(rng.randint(1, 5)) for _ in range(4)]
        beta, b = F(rng.randint(-4, 4), 3), F(rng.randint(-4, 4), 3)
        dt, dell, dbeta, da, dd, db = [F(rng.randint(-4, 4), 3) for _ in range(6)]
        r = [[t, t * beta], [F(0), ell]]
        dr = [[dt, dt * beta + t * dbeta], [F(0), dell]]
        m = [[a, b], [F(0), d]]
        dm = [[da, db], [F(0), dd]]
        product = mm(dual(r, dr), dual(m, dm))
        tv, lv = product[0][0], product[1][1]
        betav = product[0][1] / product[0][0]
        k = mm(dm, inv2(m))
        base_k = (dt / t + dell / ell) / 2
        base_p = (dell / ell - dt / t) / 2
        assert (tv.derivative / tv.value + lv.derivative / lv.value) / 2 == base_k + trace(k) / 2
        assert (lv.derivative / lv.value - tv.derivative / tv.value) / 2 == base_p + (k[1][1] - k[0][0]) / 2
        ratio, shift = d / a, b / a
        assert betav.value == shift + ratio * beta
        assert betav.derivative == ratio * (dbeta + k[0][1] + (k[1][1] - k[0][0]) * beta)

    shear = [[F(0), F(1)], [F(0), F(0)]]
    assert trace(shear) == 0 and shear[1][1] - shear[0][0] == 0
    assert shear != [[F(0), F(0)], [F(0), F(0)]]

    mlower = [[F(1), F(0)], [F(1, 2), F(1)]]
    hflat, hscaled = [[F(-1), F(0)], [F(0), F(1)]], [[F(-4), F(0)], [F(0), F(1)]]
    z = [[F(0), F(0)], [F(0), F(0)]]
    flatbar, _ = pull(hflat, z, mlower, z)
    scaledbar, _ = pull(hscaled, z, mlower, z)
    assert (-flatbar[0][0]) / (-hflat[0][0]) == F(3, 4)
    assert (-scaledbar[0][0]) / (-hscaled[0][0]) == F(15, 16)
    assert flatbar[0][1] / flatbar[0][0] != scaledbar[0][1] / scaledbar[0][0]

    # Independent exact witnesses for the two adversarial scope repairs.
    eta = [[F(-1), F(0)], [F(0), F(1)]]
    lorentz = [[F(5, 3), F(4, 3)], [F(4, 3), F(5, 3)]]
    assert lorentz != [[F(1), F(0)], [F(0), F(1)]]
    assert mm(mm(transpose(lorentz), eta), lorentz) == eta
    boost_rate = [[F(0), F(1)], [F(1), F(0)]]
    assert boost_rate != z
    assert add(mm(transpose(boost_rate), eta), mm(eta, boost_rate)) == z
    sign_reversal = [[F(-1), F(0)], [F(0), F(-1)]]
    assert sign_reversal[0][0] * sign_reversal[1][1] == 1
    assert mm(mm(transpose(sign_reversal), hflat), sign_reversal) == hflat

    result = {
        "status": "PASS",
        "method": "stdlib_fraction_dual_number_direct_product_and_definition_replay",
        "registered_outcome_class": (
            "TIMELIVE_PAIR_FIRST_JET_CARRY_DERIVED__FULL_GLPLUS2_TENSOR_AND_"
            "CONNECTION_COMPOSITION__TERMINAL_CHARACTER_BOUNDARY_CLASSIFIED"
        ),
        "landing": LANDING,
        "source_count": source_count,
        "general_glplus2_trials": trials,
        "bplus2_terminal_trials": bplus_trials,
        "live_endpoint_gauge_trials": trials,
        "closed_three_observer_trials": trials,
        "nonclosed_defect_rate_trials": trials,
        "general_phi_beta_rate_trials": trials,
        "total_transition_live_gauge_trials": trials,
        "total_transition_composition_trials": trials,
        "general_glplus2_tensor_carry_derived": True,
        "right_connection_rate_composition_derived": True,
        "combined_first_jet_live_endpoint_gauge_covariant": True,
        "intrinsic_connection_split_gauge_independent": False,
        "phi_beta_carry_only_law_exists_on_full_glplus2": False,
        "bplus2_sufficient_for_phi_beta_character_laws": True,
        "bplus2_necessary_for_every_phi_beta_character_law": False,
        "pair_first_jet_faithfully_detects_carry_closure": False,
        "lorentz_stabilizer_invisible_to_pair_first_jet": True,
        "scalar_rate_closure_implies_matrix_rate_closure": False,
        "physical_carry_derived": False,
        "physical_history_derived": False,
        "physical_lambda_owned": False,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
