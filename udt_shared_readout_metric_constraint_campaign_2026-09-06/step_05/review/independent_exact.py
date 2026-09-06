import itertools
import json
import sys
from fractions import Fraction as F

checks = 0

def require(ok, name):
    global checks
    checks += 1
    assert ok, name

def solve_columns(columns, target):
    n = len(columns)
    aug = [[columns[j][i] for j in range(n)] + [target[i]] for i in range(3)]
    rank = 0
    pivots = []
    for col in range(n):
        found = next((i for i in range(rank, 3) if aug[i][col]), None)
        if found is None:
            continue
        aug[rank], aug[found] = aug[found], aug[rank]
        pivot = aug[rank][col]
        aug[rank] = [v / pivot for v in aug[rank]]
        for i in range(3):
            if i != rank:
                scale = aug[i][col]
                aug[i] = [x-scale*y for x, y in zip(aug[i], aug[rank])]
        pivots.append(col)
        rank += 1
    if any(not any(row[:-1]) and row[-1] for row in aug):
        return None
    if rank != n:
        return None
    result = [F(0)] * n
    for i, col in enumerate(pivots):
        result[col] = aug[i][-1]
    return result

def ray_feasible(z, a, b):
    if not any(z):
        return True
    rays = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        for x, y in ((a, b), (b, a)):
            v = [F(0)] * 3
            v[i], v[j] = x, y
            rays.append(v)
    for count in (1, 2, 3):
        for cols in itertools.combinations(rays, count):
            coef = solve_columns(cols, z)
            if coef is not None and all(x >= 0 for x in coef):
                require(all(sum(c*v[i] for c, v in zip(coef, cols)) == z[i]
                            for i in range(3)), 'original_ray_equations')
                return True
    return False

def bounded(z, a, b):
    return all(v >= 0 for v in z) and all(a*z[i] <= b*sum(z[j] for j in range(3) if j != i) for i in range(3))

records = 0
for e in map(F, ('0', '1/10', '1/5', '1/2', '9/10')):
    a, b = 1-e, 1+e
    for z in itertools.product(map(F, (-1, 0, 1, 2, 3, 4)), repeat=3):
        records += 1
        require(ray_feasible(z, a, b) == bounded(z, a, b), 'six_ray_cone_vs_bound')

# Evaluate an actual discrete label measure through exact registered windows.
labels = ((F(1,2), F(1,2)), (F(3,2), F(1,2)), (F(5,2), F(1,2)))
def active(i, point):
    x, _ = point
    return ((x < 2), (x >= 1), (x < 1 or x >= 2))[i]

mu = (F(5,4), F(0), F(5,4))
weights = (F(4,5), F(4,5), F(6,5))
values = tuple(sum(m*weights[i] for point, m in zip(labels, mu) if active(i, point)) for i in range(3))
require(values == (1,1,3), 'threshold_original_integrals')
for e in map(F, ('0', '1/10', '19/100', '1/5', '1/2', '99/100')):
    require(bounded(values, 1-e, 1+e) == (e >= F(1,5)), 'diagnostic_threshold')
    if e >= F(1,5):
        require(all(1-e <= w <= 1+e for w in weights), 'fixed_sharpness_witness_allowed')
require(not ray_feasible(values, F(1), F(1)), 'fixed_kernels_converse_rejected')

# Independently contract 4D metric, phase and observer, including reference rates.
alpha, delta = F(2), F(3)
for d, c in itertools.product(map(F, (1,2,3)), weights):
    h = d*c
    observer = ((h + 1/h)/2, F(0), F(0), (1/h - h)/2)
    phase = (-alpha, F(0), F(0), alpha)
    norm = -observer[0]**2 + sum(v*v for v in observer[1:])
    omega = -sum(x*y for x,y in zip(observer,phase))
    require(norm == -1 and observer[0] > 0, 'future_unit_observer')
    require(omega/delta/(alpha*d/delta) == c, 'metric_frequency_normalization')

# A condition-only mutant forgetting nonnegativity can pass negative data.
z = (F(-1,10), F(1), F(1))
a, b = F(4,5), F(6,5)
require(all(a*z[i] <= b*sum(z[j] for j in range(3) if j != i) for i in range(3)), 'negative_record_relaxed_triangles')
require(not ray_feasible(z,a,b), 'negative_record_no_positive_measure')

print(json.dumps({'python':sys.version, 'checks':checks, 'records':records,
                  'threshold_integrals':list(map(str,values)),
                  'conclusion':'exact finite regression; analytic notes own universal quantifiers'}, sort_keys=True))
