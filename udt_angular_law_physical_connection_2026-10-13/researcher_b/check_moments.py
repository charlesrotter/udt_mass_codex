"""Exact algebra confirmation; not an independent proof of the FAC1 input."""
from fractions import Fraction as F
from itertools import product
import json
import platform
import resource
import sys
import time


def double_factorial(n):
    result = 1
    while n > 0:
        result *= n
        n -= 2
    return result


def sphere_monomial(indices):
    powers = [indices.count(i) for i in range(3)]
    if any(p % 2 for p in powers):
        return F(0)
    numerator = 1
    for p in powers:
        numerator *= double_factorial(p - 1)
    return F(numerator, double_factorial(sum(powers) + 1))


def qmoment(a, b):
    return sum((a[i][j] * b[k][l] * sphere_monomial([i, j, k, l])
                for i, j, k, l in product(range(3), repeat=4)), F(0))


def inner(a, b):
    return sum((F(a[i][j] * b[i][j]) for i, j in product(range(3), repeat=2)), F(0))


def main():
    started = time.process_time()
    basis = [
        [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, -1]],
        [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
        [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
    ]
    checks = []
    for i, a in enumerate(basis):
        for j, b in enumerate(basis):
            actual = qmoment(a, b)
            expected = F(2, 15) * inner(a, b)
            assert actual == expected, (i, j, actual, expected)
            checks.append([i, j, str(actual)])

    # Coefficients of independent E² and B². Input mean is reviewed FAC1.
    mean = [F(4, 360), F(-3, 360)]
    second = [F(1, 30), F(0)]
    normalization = [-2 * m + 2 * v for m, v in zip(mean, second)]
    assert normalization == [F(8, 180), F(3, 180)]
    recovered_e = [15 * (n + 2 * m) for n, m in zip(normalization, mean)]
    recovered_b = [20 * n - 80 * m for n, m in zip(normalization, mean)]
    assert recovered_e == [F(1), F(0)]
    assert recovered_b == [F(0), F(1)]

    controls = {}
    for name, e2, b2, expected in [
        ('kasner', F(8, 27), F(0), F(16, 1215)),
        ('plane_wave', F(1, 2), F(1, 2), F(11, 360)),
        ('kerr', F(0), F(2, 9), F(1, 270)),
    ]:
        value = normalization[0] * e2 + normalization[1] * b2
        assert value == expected
        controls[name] = {'N_minus_one_L4': str(value),
                          'M_L4': str(mean[0] * e2 + mean[1] * b2)}

    boosts = []
    for c, s in [(F(5, 4), F(3, 4)), (F(13, 12), F(5, 12)),
                 (F(17, 8), F(15, 8))]:
        assert c*c - s*s == 1
        norm = (1 / (c-s) - 1 / (c+s)) / (2*s)
        assert norm == 1
        boosts.append({'cosh': str(c), 'sinh': str(s), 'N': str(norm)})

    out = dict(status='PASS', evidence='exact Fraction algebra confirmation',
               limitations='FAC1 input theorem not independently rederived; no metric/ray integration',
               python=sys.version, platform=platform.platform(),
               sphere_bilinear_basis_checks=checks,
               normalization_E2_B2=list(map(str, normalization)),
               recovered_E2_coefficients=list(map(str, recovered_e)),
               recovered_B2_coefficients=list(map(str, recovered_b)),
               controls=controls, boost_normalizations=boosts,
               cpu_seconds=time.process_time()-started,
               maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
