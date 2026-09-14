"""DCR1 independent exact checker; no imports from parent scientific code.

Method/cases frozen in SOURCE_FIRST.md. Python standard library Fraction only.
Original polynomial metric -> polynomial Christoffel linear part -> curvature.
The source argument, not these finite cases, owns the universal theorem.
"""
from fractions import Fraction as F
from itertools import product
import json
import platform

ZERO = (0, 0, 0)
ETA = [-1, 1, 1, 1]
count = 0


def check(condition, label):
    global count
    count += 1
    if not condition:
        raise AssertionError(label)


def add(*polys):
    out = {}
    for p in polys:
        for e, c in p.items():
            out[e] = out.get(e, F(0)) + c
    return {e: c for e, c in out.items() if c}


def scale(p, c):
    return {e: c * a for e, a in p.items() if c * a}


def mul(p, q):
    out = {}
    for e, a in p.items():
        for f, b in q.items():
            ef = tuple(e[i] + f[i] for i in range(3))
            out[ef] = out.get(ef, F(0)) + a * b
    return {e: c for e, c in out.items() if c}


def deriv(p, coord):
    if coord == 0:
        return {}
    k = coord - 1
    out = {}
    for e, c in p.items():
        if e[k]:
            ee = list(e)
            ee[k] -= 1
            out[tuple(ee)] = e[k] * c
    return out


X = [{tuple(int(i == j) for i in range(3)): F(1)} for j in range(3)]


def eps(i, j, k):
    if len({i, j, k}) < 3:
        return 0
    return 1 if (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1


def matrix_zero():
    return [[F(0) for j in range(3)] for i in range(3)]


def trace(m):
    return sum(m[i][i] for i in range(3))


def tf_basis():
    result = []
    for k in (0, 1):
        m = matrix_zero()
        m[k][k], m[2][2] = F(1), F(-1)
        result.append(m)
    for i, j in ((0, 1), (0, 2), (1, 2)):
        m = matrix_zero()
        m[i][j] = m[j][i] = F(1)
        result.append(m)
    return result


def cross_form(u):
    # C_ki = epsilon_kli x_l, so columns encode x cross e_i.
    c = [[add(*(scale(X[l], eps(k, l, i)) for l in range(3)))
          for i in range(3)] for k in range(3)]
    return [[add(*(scale(mul(c[k][i], c[l][j]), u[k][l])
                   for k in range(3) for l in range(3)))
             for j in range(3)] for i in range(3)]


def build(c, q, t):
    a = [[q[i][j] + (c if i == j else 0) for j in range(3)] for i in range(3)]
    u = [[t[i][j] + (c if i == j else 0) for j in range(3)] for i in range(3)]
    h = add(*(scale(mul(X[i], X[j]), a[i][j]) for i in range(3) for j in range(3)))
    b = cross_form(u)
    k = [[add(b[i][j], scale(h, -int(i == j))) for j in range(3)] for i in range(3)]
    g = [[{} for j in range(4)] for i in range(4)]
    g[0][0] = add({ZERO: F(-1)}, scale(h, -1))
    for i in range(3):
        for j in range(3):
            g[i + 1][j + 1] = add({ZERO: F(int(i == j))}, k[i][j])
    return g, k, h, a, u


def center_curvature(g):
    # Inverse metric's constant term suffices: dg has zero constant term.
    christoffel = [[[
        scale(add(deriv(g[a][c], b), deriv(g[a][b], c),
                  scale(deriv(g[b][c], a), -1)), F(ETA[a], 2))
        for c in range(4)] for b in range(4)] for a in range(4)]
    upper = [[[[
        add(deriv(christoffel[a][d][b], c),
            scale(deriv(christoffel[a][c][b], d), -1)).get(ZERO, F(0))
        for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    riem = [[[[ETA[a] * upper[a][b][c][d] for d in range(4)]
               for c in range(4)] for b in range(4)] for a in range(4)]
    ric = [[sum(upper[a][b][a][d] for a in range(4)) for d in range(4)] for b in range(4)]
    scalar = sum(ETA[a] * ric[a][a] for a in range(4))
    return riem, ric, scalar


def mm(c, q, t):
    g, k, h, a, u = build(c, q, t)
    for i in range(3):
        check(add(*(mul(k[i][j], X[j]) for j in range(3)), mul(h, X[i])) == {},
              'strong radial quadratic action')
    check(trace(u) == trace(a), 'area trace relation')
    rr, ric, scalar = center_curvature(g)
    for i, j in product(range(3), repeat=2):
        check(rr[0][i + 1][0][j + 1] == a[i][j], 'clock curvature')
        for k0 in range(3):
            check(rr[0][i + 1][j + 1][k0 + 1] == 0, 'mixed curvature')
    for i, j, k0, l in product(range(3), repeat=4):
        target = (int(i == k0) * a[j][l] + int(j == l) * a[i][k0]
                  - int(i == l) * a[j][k0] - int(j == k0) * a[i][l]
                  - 3 * sum(eps(i, j, p) * eps(k0, l, s) * u[p][s]
                            for p in range(3) for s in range(3)))
        check(rr[i + 1][j + 1][k0 + 1][l + 1] == target, 'spatial curvature')
    for i, j, k0, l in product(range(4), repeat=4):
        check(rr[i][j][k0][l] == -rr[j][i][k0][l], 'first antisymmetry')
        check(rr[i][j][k0][l] == rr[k0][l][i][j], 'pair symmetry')
        check(rr[i][j][k0][l] + rr[i][k0][l][j] + rr[i][l][j][k0] == 0, 'Bianchi')
    check(ric[0][0] == 3 * c and scalar == -12 * c, 'center Ricci scalar')
    for i, j in product(range(3), repeat=2):
        check(ric[i + 1][j + 1] == -3 * c * int(i == j) + 3 * t[i][j], 'center spatial Ricci')
    for i in range(3):
        check(ric[0][i + 1] == ric[i + 1][0] == 0, 'center mixed Ricci')
    tf = [[ric[i][j] - F(1, 4) * scalar * ETA[i] * int(i == j) for j in range(4)] for i in range(4)]
    for aa, bb in ((F(1), F(0)), (F(2, 3), F(-1, 6)), (F(-3), F(7, 5)), (F(0), F(1))):
        ee = [[aa * ric[i][j] + bb * scalar * ETA[i] * int(i == j) for j in range(4)] for i in range(4)]
        tr_e = sum(ETA[i] * ee[i][i] for i in range(4))
        for i, j in product(range(4), repeat=2):
            observed = ee[i][j] - tr_e * F(ETA[i] * int(i == j), 4)
            target = 3 * aa * t[i - 1][j - 1] if i and j else 0
            check(observed == target, 'full response tracefree shape')
    electric = [[rr[0][i + 1][0][j + 1] + F(1, 2) * ric[i + 1][j + 1]
                 - F(1, 2) * int(i == j) * ric[0][0]
                 - F(1, 6) * int(i == j) * scalar for j in range(3)] for i in range(3)]
    for i, j in product(range(3), repeat=2):
        check(electric[i][j] == q[i][j] + F(3, 2) * t[i][j], 'electric Weyl')
    for n in range(3):
        screen = [i for i in range(3) if i != n]
        for v, w in product(screen, repeat=2):
            observed = rr[v + 1][0][w + 1][0] + rr[v + 1][n + 1][w + 1][n + 1]
            target = 2 * q[v][w] + int(v == w) * q[n][n] - 3 * sum(
                eps(p, v, n) * t[p][s] * eps(s, w, n) for p in range(3) for s in range(3))
            check(observed == target, 'signed null screen contraction')
    return tf, rr, electric


def rank(rows):
    a = [[F(x) for x in row] for row in rows]
    rr = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(rr, len(a)) if a[j][col]), None)
        if pivot is None:
            continue
        a[rr], a[pivot] = a[pivot], a[rr]
        value = a[rr][col]
        a[rr] = [x / value for x in a[rr]]
        for j in range(len(a)):
            if j != rr and a[j][col]:
                multiplier = a[j][col]
                a[j] = [x - multiplier * y for x, y in zip(a[j], a[rr])]
        rr += 1
        if rr == len(a):
            break
    return rr


def sphere_average(p):
    # Exact normalized S^2 moments for the degrees used here, all from Cartesian monomials.
    def odd_df(n):
        value = 1
        for k in range(1, n + 1, 2):
            value *= k
        return value
    total = F(0)
    for e, c in p.items():
        if any(k % 2 for k in e):
            continue
        numerator = 1
        for k in e:
            numerator *= odd_df(k - 1)
        total += c * F(numerator, odd_df(sum(e) + 1))
    return total


def area_coefficient(k):
    tangent_trace = add(*(k[i][i] for i in range(3)),
                        *(scale(mul(mul(X[i], X[j]), k[i][j]), -1)
                          for i in range(3) for j in range(3)))
    return sphere_average(tangent_trace) / 2


def linear_algebra_check():
    pairs = [(i, j) for i in range(3) for j in range(i, 3)]
    monomials = [tuple(int(k == i) + int(k == j) for k in range(3)) for i, j in pairs]
    cubics = [e for e in product(range(4), repeat=3) if sum(e) == 3]
    basis_b = []
    columns = []
    for i, j in pairs:
        for e in monomials:
            b = [[{} for _ in range(3)] for _ in range(3)]
            b[i][j] = {e: F(1)}
            b[j][i] = {e: F(1)}
            basis_b.append(b)
            bx = [add(*(mul(b[k][l], X[l]) for l in range(3))) for k in range(3)]
            columns.append([p.get(ee, F(0)) for p in bx for ee in cubics])
    rows = list(map(list, zip(*columns)))
    check(rank(rows) == 30, 'transverse constraint rank30')
    area_row = [area_coefficient(b) for b in basis_b]
    check(rank(rows + [area_row]) == 31, 'transverse plus area rank31')
    cross_columns = []
    for i, j in pairs:
        u = matrix_zero()
        u[i][j] = u[j][i] = F(1)
        b = cross_form(u)
        for k in range(3):
            check(add(*(mul(b[k][l], X[l]) for l in range(3))) == {}, 'cross image in transverse kernel')
        cross_columns.append([b[k][l].get(e, F(0)) for k, l in pairs for e in monomials])
        check(area_coefficient(b) == trace(u) / 3, 'cross area trace')
    check(rank(list(map(list, zip(*cross_columns)))) == 6, 'cross image independent dimension6')
    # Every Cartesian quadratic clock basis, including traceful anisotropic basis.
    for i, j in pairs:
        a = matrix_zero()
        a[i][j] = a[j][i] = F(1)
        h = add(*(scale(mul(X[k], X[l]), a[k][l]) for k in range(3) for l in range(3)))
        k = [[scale(h, -int(m == n)) for n in range(3)] for m in range(3)]
        check(area_coefficient(k) == -trace(a) / 3, 'clock area contribution')
    return {'transverse_matrix_shape': [30, 36], 'transverse_rank': 30,
            'transverse_nullity': 6, 'area_augmented_rank': 31, 'cross_image_rank': 6}


def main():
    basis = tf_basis()
    z = matrix_zero()
    cases = [('flat', F(0), z, z), ('isotropic_positive', F(2, 3), z, z),
             ('isotropic_negative', F(-5, 7), z, z)]
    cases += [('clock_basis_' + str(i), F(0), b, z) for i, b in enumerate(basis)]
    cases += [('angular_basis_' + str(i), F(0), z, b) for i, b in enumerate(basis)]
    q = [[F(2, 3), F(-3, 5), F(4, 7)], [F(-3, 5), F(-7, 11), F(5, 13)],
         [F(4, 7), F(5, 13), F(-2, 3) + F(7, 11)]]
    t = [[F(-5, 3), F(2, 9), F(-1, 8)], [F(2, 9), F(6, 7), F(7, 10)],
         [F(-1, 8), F(7, 10), F(5, 3) - F(6, 7)]]
    cases.append(('dense_rational_mixed', F(7, 5), q, t))
    results = []
    for name, c, q, t in cases:
        tf, rr, electric = mm(c, q, t)
        _, k, _, _, _ = build(c, q, t)
        check(area_coefficient(k) == 0, 'allowed full jet leading area')
        results.append({'case': name, 'tf': [str(x) for row in tf for x in row]})
    algebra = linear_algebra_check()
    map_cols = []
    for c, q, t in [(F(1), z, z)] + [(F(0), b, z) for b in basis] + [(F(0), z, b) for b in basis]:
        rr, ric, scalar = center_curvature(build(c, q, t)[0])
        map_cols.append([ric[i][j] - F(1, 4) * scalar * ETA[i] * int(i == j)
                         for i in range(4) for j in range(i, 4)])
    check(rank(list(map(list, zip(*map_cols)))) == 5, 'eleven-parameter center TF map rank5')
    check(all(not value for col in map_cols[:6] for value in col), 'clock c,Q in center TF kernel')
    # Hostile claim 1/2: DDR forces clock isotropy / zero tide.
    q = [[F(1), F(0), F(0)], [F(0), F(-1), F(0)], [F(0), F(0), F(0)]]
    rr, ric, scalar = center_curvature(build(F(0), q, z)[0])
    tide11 = rr[1][0][1][0] + rr[1][3][1][3]
    tide22 = rr[2][0][2][0] + rr[2][3][2][3]
    check(all(x == 0 for row in ric for x in row) and (tide11, tide22) == (2, -2),
          'hostile DDR implies isotropy/zero tide rejected')
    # Hostile claim 3: trace U=0 is still correct before splitting off c.
    a = [[F(1), F(0), F(0)], [F(0), F(0), F(0)], [F(0), F(0), F(0)]]
    h = mul(X[0], X[0])
    bad_k = [[scale(h, -int(i == j)) for j in range(3)] for i in range(3)]
    check(area_coefficient(bad_k) == F(-1, 3), 'hostile wrong area trace condition rejected')
    # Hostile claim 4: Weyl=0 alone implies all-null-screen quietness.
    t = basis[0]
    q = [[-F(3, 2) * t[i][j] for j in range(3)] for i in range(3)]
    rr, ric, scalar = center_curvature(build(F(0), q, t)[0])
    check(rr[2][0][2][0] + rr[2][1][2][1] != 0, 'hostile Weyl-only quietness rejected')
    print(json.dumps({'status': 'PASS', 'python': platform.python_version(),
                      'arithmetic': 'fractions.Fraction exact', 'assertions': count,
                      'parameter_cases': len(cases), 'cases': results, 'linear_algebra': algebra,
                      'center_tf_rank': 5, 'hostile_claims_rejected': 4,
                      'witness_screen_diagonal': [str(tide11), str(tide22)],
                      'limits': 'finite exact supports plus independent analytic argument; no neighborhood DDR proof'},
                     indent=2))


if __name__ == '__main__':
    main()
