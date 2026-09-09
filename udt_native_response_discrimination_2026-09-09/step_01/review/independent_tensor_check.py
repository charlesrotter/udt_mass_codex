#!/usr/bin/env python3
"""Independent exact jet reconstruction for the restricted response comparison.

No author or historical production imports. Two-variable Taylor arithmetic builds
the full metric through order two at an equatorial event; ordinary coordinate
formulas then build the full Ricci tensor. Finite checks support, not replace,
the argument in the direct review. All units use c_E dt as the time coordinate.
"""

import json
import platform
from fractions import Fraction as F


POWERS = ((0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2))


class Jet:
    def __init__(self, value=0, terms=None):
        self.c = [F(0)] * 6
        self.c[0] = F(value)
        for power, coefficient in (terms or {}).items():
            self.c[POWERS.index(power)] = F(coefficient)

    def __add__(self, other):
        other = other if isinstance(other, Jet) else Jet(other)
        out = Jet()
        out.c = [a + b for a, b in zip(self.c, other.c)]
        return out

    __radd__ = __add__

    def __neg__(self):
        out = Jet()
        out.c = [-a for a in self.c]
        return out

    def __sub__(self, other):
        return self + -other if isinstance(other, Jet) else self + (-F(other))

    def __mul__(self, other):
        other = other if isinstance(other, Jet) else Jet(other)
        out = Jet()
        for i, a in enumerate(self.c):
            if not a:
                continue
            for j, b in enumerate(other.c):
                if not b:
                    continue
                power = tuple(x + y for x, y in zip(POWERS[i], POWERS[j]))
                if power in POWERS:
                    out.c[POWERS.index(power)] += a * b
        return out

    __rmul__ = __mul__

    def inverse(self):
        value = self.c[0]
        assert value
        tail = self - value
        return Jet(1 / value) + (-1 / value**2) * tail + (1 / value**3) * tail * tail

    def derivative(self, *indices):
        if any(i not in (1, 2) for i in indices):
            return F(0)
        power = (indices.count(1), indices.count(2))
        coefficient = self.c[POWERS.index(power)]
        return 2 * coefficient if 2 in power else coefficient


def raw_ricci(radius, f0, f1, f2, flatten_angular_second_derivative=False):
    r = Jet(radius, {(1, 0): 1})
    f = Jet(f0, {(1, 0): f1, (2, 0): F(f2) / 2})
    sin_squared = Jet(1, {(0, 2): 0 if flatten_angular_second_derivative else -1})
    diagonal = [-f, f.inverse(), r * r, r * r * sin_squared]
    zero = Jet()
    metric = [[diagonal[a] if a == b else zero for b in range(4)] for a in range(4)]
    inverse = [element.inverse() for element in diagonal]

    def bracket(d, b, c, *derivative):
        return (metric[d][c].derivative(b, *derivative)
                + metric[d][b].derivative(c, *derivative)
                - metric[b][c].derivative(d, *derivative))

    gamma = [[[inverse[a].c[0] * bracket(a, b, c) / 2
               for c in range(4)] for b in range(4)] for a in range(4)]

    def dgamma(a, b, c, e):
        return (inverse[a].derivative(e) * bracket(a, b, c)
                + inverse[a].c[0] * bracket(a, b, c, e)) / 2

    ricci = [[sum((dgamma(a, b, d, a) - dgamma(a, b, a, d)
                  + sum((gamma[a][a][e] * gamma[e][b][d]
                         - gamma[a][d][e] * gamma[e][b][a]
                         for e in range(4)), F(0))
                  for a in range(4)), F(0))
              for d in range(4)] for b in range(4)]
    return [entry.c[0] for entry in diagonal], ricci


def responses(metric, ricci):
    inverse = [1 / entry for entry in metric]
    scalar = sum((inverse[a] * ricci[a][a] for a in range(4)), F(0))
    square = [[sum((ricci[a][c] * inverse[c] * ricci[b][c]
                    for c in range(4)), F(0)) for b in range(4)] for a in range(4)]
    square_trace = sum((inverse[a] * square[a][a] for a in range(4)), F(0))
    shape = [[ricci[a][b] - (scalar * metric[a] / 4 if a == b else 0)
              for b in range(4)] for a in range(4)]
    quadratic = [[square[a][b] - (square_trace * metric[a] / 4 if a == b else 0)
                  for b in range(4)] for a in range(4)]
    return scalar, shape, quadratic


def is_zero(tensor):
    return all(not entry for row in tensor for entry in row)


def main():
    cases = []
    assertions = 0
    for radius in (F(1), F(2), F(3, 2)):
        for f0 in (F(1, 2), F(2)):
            for f1 in (F(-2), F(0), F(3, 2)):
                for f2 in (F(-3), F(0), F(5, 2)):
                    metric, ricci = raw_ricci(radius, f0, f1, f2)
                    scalar, shape, quadratic = responses(metric, ricci)
                    e0 = radius * f1 + f0 - 1
                    e1 = radius * f1 + radius**2 * f2 / 2
                    expected_mixed = (-e1 / radius**2,) * 2 + (-e0 / radius**2,) * 2
                    for a in range(4):
                        for b in range(4):
                            assert ricci[a][b] == (expected_mixed[a] * metric[a] if a == b else 0)
                            assert quadratic[a][b] == scalar * shape[a][b] / 2
                            assertions += 2
                    assert 2 * (ricci[0][0] / f0 + ricci[1][1] / metric[1]) == 0
                    assert 2 * (ricci[0][0] / f0 + ricci[2][2] / metric[2]) == 2 * (e1 - e0) / radius**2
                    assert is_zero(quadratic) == (scalar == 0 or is_zero(shape))
                    assertions += 3
                    cases.append([str(radius), str(f0), str(f1), str(f2)])

    branch_records = []
    for branch in ("einstein", "scalar_flat"):
        for radius in (F(1), F(2), F(3)):
            for b in (F(-1, 4), F(0), F(2, 3)):
                extra = F(1, 5)
                if branch == "einstein":
                    f0 = 1 + b / radius + extra * radius**2
                    f1 = -b / radius**2 + 2 * extra * radius
                    f2 = 2 * b / radius**3 + 2 * extra
                else:
                    f0 = 1 + b / radius + extra / radius**2
                    f1 = -b / radius**2 - 2 * extra / radius**3
                    f2 = 2 * b / radius**3 + 6 * extra / radius**4
                assert f0 > 0
                metric, ricci = raw_ricci(radius, f0, f1, f2)
                scalar, shape, quadratic = responses(metric, ricci)
                assert is_zero(quadratic)
                if branch == "einstein":
                    assert is_zero(shape) and scalar == -12 * extra
                else:
                    assert scalar == 0 and not is_zero(shape)
                    assert radius**2 * f2 / 2 - f0 + 1 == 2 * extra / radius**2
                assertions += 3 if branch == "einstein" else 4
                branch_records.append({"branch": branch, "r": str(radius), "b": str(b),
                                       "extra": str(extra), "R": str(scalar),
                                       "S_zero": is_zero(shape), "Q_zero": is_zero(quadratic)})

    metric, spherical_ricci = raw_ricci(F(2), F(3, 2), F(-1, 4), F(1, 4))
    _, corrupted_ricci = raw_ricci(F(2), F(3, 2), F(-1, 4), F(1, 4), True)
    assert is_zero(spherical_ricci)
    assert not is_zero(corrupted_ricci)
    assertions += 2
    print(json.dumps({"status": "PASS", "python": platform.python_version(),
                      "method": "independent_fraction_Taylor_metric_to_Christoffel_derivative_to_Ricci",
                      "generic_two_jet_cases": cases, "branch_witnesses": branch_records,
                      "assertions": assertions,
                      "angular_second_derivative_corruption_detected": True,
                      "limits": "finite exact regression supports analytic proof; no branch-switching proof by sampling"},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
