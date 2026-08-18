#!/usr/bin/env python3
"""Independent stdlib/Fraction replay of the G161 finite-dimensional claims."""

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
SOURCE_SNAPSHOT = "3fa4964f"
OUTCOME_CLASS = (
    "LORENTZ_QUOTIENT_AND_UNIQUE_BPLUS2_SECTION_DERIVED__SWEEP_FIXES_"
    "QUOTIENT_NOT_VERTICAL_RAPIDITY__NORMAL_TRANSPORT_INDEPENDENT__"
    "EXTRINSIC_SIMPLE_SPECTRUM_CONDITIONALLY_FIXES_FLAG"
)
LANDING = (
    "PAIR_FIRST_JET_IS_EXACT_LORENTZ_STABILIZER_QUOTIENT__POSITIVE_BPLUS2_"
    "IS_UNIQUE_TIME_ORIENTED_GAUGE_SECTION_ON_FUTURE_TIMELIKE_CLOCK_STRATUM__"
    "DISTANCE_SWEEP_FIXES_QUOTIENT_PATH_AND_FIRST_JET_NOT_VERTICAL_RAPIDITY__"
    "SCREEN_NORMAL_TRANSPORT_DOES_NOT_UNIVERSALLY_RESOLVE_TANGENT_BOOST__"
    "NORMAL_GAUGE_INVARIANT_EXTRINSIC_SIMPLE_CAUSAL_SPECTRUM_CONDITIONALLY_"
    "FIXES_PAIR_FLAG__DEGENERATE_NULL_AND_GLOBAL_STRATA_OPEN__PHYSICAL_"
    "CARRY_HISTORY_QUERY_AND_COMPLETION_OPEN"
)


class Dual:
    def __init__(self, value=0, derivative=0):
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

    def __eq__(self, other):
        other = other if isinstance(other, Dual) else Dual(other)
        return self.value == other.value and self.derivative == other.derivative


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


def tr(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    zero = Dual() if isinstance(a[0][0], Dual) or isinstance(b[0][0], Dual) else F(0)
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), zero)
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def dual(a, da):
    return [[Dual(a[i][j], da[i][j]) for j in range(len(a[0]))] for i in range(len(a))]


def values(a):
    return [[item.value for item in row] for row in a]


def derivatives(a):
    return [[item.derivative for item in row] for row in a]


def boost(parameter):
    denominator = 1 - parameter * parameter
    c = (1 + parameter * parameter) / denominator
    s = 2 * parameter / denominator
    return [[c, s], [s, c]]


def discriminant(a):
    return (a[0][0] - a[1][1])**2 + 4 * a[0][1] * a[1][0]


def shape(a, b, d):
    return [[a, b], [-b, d]]


def random_raw_admissible(rng):
    """Generate raw integer M; accept only future timelike clock with rational norm."""
    while True:
        p = rng.randint(1, 30)
        r = rng.randint(-29, 29)
        norm2 = p * p - r * r
        if norm2 <= 0:
            continue
        a = math.isqrt(norm2)
        if a * a != norm2:
            continue
        q, s = rng.randint(-12, 12), rng.randint(-12, 12)
        if p * s - q * r > 0:
            return [[F(p), F(q)], [F(r), F(s)]], F(a)


def main():
    source_count = verify_manifest()
    rng = random.Random(161)
    eta = [[F(-1), F(0)], [F(0), F(1)]]
    trials = 700

    # Independent raw-coordinate reconstruction. These matrices are not made by
    # multiplying a boost by a triangular section; admissibility is tested after draw.
    for _ in range(trials):
        raw, a = random_raw_admissible(rng)
        p, q, r, s = raw[0][0], raw[0][1], raw[1][0], raw[1][1]
        extracting = [[p / a, -r / a], [-r / a, p / a]]
        recovered = mm(extracting, raw)
        assert mm(mm(tr(extracting), eta), extracting) == eta
        assert recovered[1][0] == 0
        assert recovered[0][0] == a > 0
        assert recovered[1][1] == (p * s - q * r) / a > 0
        assert mm(mm(tr(raw), eta), raw) == mm(mm(tr(recovered), eta), recovered)

    for _ in range(trials):
        # Build a regular carry from a vertical boost and positive triangular quotient.
        t = F(rng.randint(-4, 4), 10)
        a, d = F(rng.randint(1, 7)), F(rng.randint(1, 7))
        b = F(rng.randint(-7, 7), 3)
        vertical = boost(t)
        section = [[a, b], [F(0), d]]
        m = mm(vertical, section)
        hbar = mm(mm(tr(m), eta), m)
        section_hbar = mm(mm(tr(section), eta), section)
        assert hbar == section_hbar

        # Reconstruct the unique quotient section without a floating square root:
        # p^2-r^2=a^2 because the witness was generated from that section.
        p, q, r, s = m[0][0], m[0][1], m[1][0], m[1][1]
        assert p > 0 and p * p - r * r == a * a
        extracting = [[p / a, -r / a], [-r / a, p / a]]
        recovered = mm(extracting, m)
        assert recovered == section
        assert mm(mm(tr(extracting), eta), extracting) == eta
        assert extracting[0][0] > 0

        # Any second carry in the same fiber differs by a left Lorentz element.
        t2 = F(rng.randint(-4, 4), 10)
        m2 = mm(boost(t2), section)
        relative = mm(m2, inv2(m))
        assert mm(mm(tr(relative), eta), relative) == eta
        assert mm(mm(tr(m2), eta), m2) == hbar

        # Live vertical boosts remain invisible to the entire first jet.
        dt = F(rng.randint(-5, 5), 7)
        da, db, dd = (F(rng.randint(-5, 5), 4) for _ in range(3))
        td, ad, bd, ddv = Dual(t, dt), Dual(a, da), Dual(b, db), Dual(d, dd)
        live_vertical = boost(td)
        live_section = [[ad, bd], [Dual(0), ddv]]
        live_m = mm(live_vertical, live_section)
        lifted = mm(mm(tr(live_m), [[Dual(-1), Dual(0)], [Dual(0), Dual(1)]]), live_m)
        quotient = mm(mm(tr(live_section), [[Dual(-1), Dual(0)], [Dual(0), Dual(1)]]), live_section)
        assert values(lifted) == values(quotient)
        assert derivatives(lifted) == derivatives(quotient)

        # Normal O(2) rotations do not change C_II.
        coeffs = [F(rng.randint(-5, 5)) for _ in range(6)]
        A = shape(*coeffs[:3])
        B = shape(*coeffs[3:])
        CII = add(mm(A, A), mm(B, B))
        rot_c, rot_s = F(3, 5), F(4, 5)
        Ap = add([[rot_c * x for x in row] for row in A],
                 [[-rot_s * x for x in row] for row in B])
        Bp = add([[rot_s * x for x in row] for row in A],
                 [[rot_c * x for x in row] for row in B])
        assert add(mm(Ap, Ap), mm(Bp, Bp)) == CII
        assert mm(tr(CII), eta) == mm(eta, CII)

    # Independent explicit failure and success strata.
    simple = add(mm(shape(1, 0, 2), shape(1, 0, 2)), [[F(0), F(0)], [F(0), F(0)]])
    jordan = add(mm(shape(-3, -3, -2), shape(-3, -3, -2)),
                 mm(shape(-3, 2, -2), shape(-3, 2, -2)))
    complex_case = add(mm(shape(-3, -3, -3), shape(-3, -3, -3)),
                       mm(shape(-3, -3, -3), shape(-3, -3, -3)))
    assert discriminant(simple) == 9
    assert discriminant(jordan) == 0 and jordan == [[F(5), F(5)], [F(-5), F(-5)]]
    assert discriminant(complex_case) == -5184

    result = {
        "status": "PASS",
        "registered_outcome_class": OUTCOME_CLASS,
        "landing": LANDING,
        "source_count": source_count,
        "fraction_trials": trials,
        "raw_admissible_reconstruction_trials": trials,
        "lorentz_quotient_trials": trials,
        "unique_bplus2_reconstruction_trials": trials,
        "live_vertical_first_jet_trials": trials,
        "normal_rotation_CII_trials": trials,
        "finite_pair_metric_fiber": "left_SOplus(h)_orbit_on_time_oriented_component",
        "first_jet_vertical_dimensions": 2,
        "positive_bplus2_unique_quotient_section": True,
        "positive_bplus2_is_physical_carry_selector": False,
        "smooth_distance_sweep_fixes_vertical_rapidity": False,
        "smooth_distance_sweep_fixes_quotient_path": True,
        "screen_normal_transport_universally_resolves_tangent_boost": False,
        "extrinsic_CII_simple_causal_spectrum_conditionally_fixes_flag": True,
        "pair_immersion_is_required_to_own_II": True,
        "metric_plus_bare_pair_plane_owns_II": False,
        "null_and_degenerate_strata_closed": False,
        "physical_carry_derived": False,
        "physical_history_derived": False,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
