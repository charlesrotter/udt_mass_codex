"""Independent Fraction fixtures; no TM2 author scientific imports or reads."""
import argparse
from fractions import Fraction as F
import json
import platform
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--mutant', choices=['omit_nuisance', 'drop_training_error',
                                       'drop_covariance', 'pretend_unique'])
args = parser.parse_args()
checks = []


def guard(name, passed, evidence):
    item = dict(name=name, passed=bool(passed), evidence=evidence)
    checks.append(item)
    if not passed:
        print(json.dumps(dict(status='FAIL', mutant=args.mutant,
                              checks=checks), default=str, sort_keys=True))
        sys.exit(1)


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def transpose(a):
    return [list(c) for c in zip(*a)]


def multiply(a, b):
    bt = transpose(b)
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in bt] for row in a]


def rref(a):
    a = [row[:] for row in a]
    pivots = []
    for col in range(len(a[0]) if a else 0):
        r = len(pivots)
        found = next((k for k in range(r, len(a)) if a[k][col]), None)
        if found is None:
            continue
        a[r], a[found] = a[found], a[r]
        scale = a[r][col]
        a[r] = [x/scale for x in a[r]]
        for k in range(len(a)):
            if k != r:
                scale = a[k][col]
                a[k] = [x-scale*y for x, y in zip(a[k], a[r])]
        pivots.append(col)
    return a, pivots


def rank(a):
    return len(rref(a)[1])


def null_rows(a, columns):
    reduced, pivots = rref(a)
    basis = []
    for free in range(columns):
        if free in pivots:
            continue
        v = [F(0)]*columns
        v[free] = F(1)
        for row, pivot in enumerate(pivots):
            v[pivot] = -reduced[row][free]
        basis.append(v)
    return basis


def zero(a):
    return all(x == 0 for row in a for x in row)


def design(p, nuisance):
    return [[sum(row, F(0))] + nrow[:] for row, nrow in zip(p, nuisance)]


def append_columns(a, b):
    return [x+y for x, y in zip(a, b)]


def contrast_bound(w, p, rho, sigma):
    wp = multiply([w], p)[0]
    return sum((abs(x)*r for x, r in zip(wp, rho)), F(0)) + sum(
        (abs(x)*s for x, s in zip(w, sigma)), F(0))


i4 = mat([[int(i == j) for j in range(4)] for i in range(4)])
t = list(map(F, [0, 2, 5, 7]))
n_offset_drift = [[F(1), x] for x in t]
d = design(i4, n_offset_drift)
w = null_rows(transpose(d), 4)
guard('offset_drift_dimensions', rank(d) == 2 and len(w) == 2,
      dict(rank=rank(d), annihilator=w))
guard('independent_annihilator_identity', zero(multiply(w, d)), multiply(w, d))

n_for_id = [[x] for x in t] if args.mutant == 'omit_nuisance' else n_offset_drift
id_rank = rank(design(i4, n_for_id))-rank(n_for_id)
guard('constant_nuisance_prevents_absolute_scalar', id_rank == 0, id_rank)
d_drift = design(i4, [[x] for x in t])
guard('without_offset_scalar_identifiable', rank(d_drift)-rank([[x] for x in t]) == 1,
      dict(design_rank=rank(d_drift), nuisance_rank=1))

k = mat([[F(-3, 2), F(5, 2)], [F(-5, 2), F(7, 2)]])
da, db = d[:2], d[2:]
guard('ab_prediction_on_complete_parameter_space', multiply(k, da) == db,
      dict(K=k, DA=da, DB=db))
r = mat([[F(3, 2), F(-5, 2), 1, 0], [F(5, 2), F(-7, 2), 0, 1]])
guard('registered_residual_is_full_annihilator', zero(multiply(r, d)) and rank(r) == 2,
      dict(residual_matrix=r, product=multiply(r, d)))
quadratic = [[x*x] for x in t]
qresult = multiply(r, quadratic)
guard('retained_quadratic_departure', qresult == mat([[15], [35]]), qresult)
guard('all_affine_departures_blind', zero(multiply(r, d_drift)), multiply(r, d_drift))

full = design(i4, i4)
guard('arbitrary_offsets_remove_all_constraints', rank(full) == 4 and
      null_rows(transpose(full), 4) == [], rank(full))

p_dc = mat([[int(i == j)-F(1, 4) for j in range(4)] for i in range(4)])
n_dc = multiply(p_dc, [[x] for x in t])
d_dc = design(p_dc, n_dc)
w_dc = null_rows(transpose(d_dc), 4)
guard('lost_dc_scalar_alias_with_retained_variations',
      all(row[0] == 0 for row in d_dc) and rank(d_dc) == 1 and
      rank(multiply(w_dc, p_dc)) == 2,
      dict(design=d_dc, residual_rank=len(w_dc), latent_sensitive_rank=rank(multiply(w_dc, p_dc))))

p_average = mat([[F(1, 4)]*4 for _ in range(4)])
d_average = design(p_average, [[] for _ in range(4)])
w_average = null_rows(transpose(d_average), 4)
guard('averaging_imposes_record_constraints_but_no_constancy_test',
      len(w_average) == 3 and zero(multiply(w_average, p_average)) and rank(d_average) == 1,
      dict(annihilator=w_average, latent_response=multiply(w_average, p_average)))

da_bad = mat([[1, 0], [1, 0]])
db_bad = mat([[1, 1]])
theta0, theta1 = mat([[0], [0]]), mat([[0], [1]])
claimed_unique = True if args.mutant == 'pretend_unique' else rank(da_bad+db_bad) == rank(da_bad)
guard('rank_deficient_training_does_not_predict_B', not claimed_unique and
      multiply(da_bad, theta0) == multiply(da_bad, theta1) and
      multiply(db_bad, theta0) != multiply(db_bad, theta1),
      dict(A0=multiply(da_bad, theta0), A1=multiply(da_bad, theta1),
           B0=multiply(db_bad, theta0), B1=multiply(db_bad, theta1)))

db_partial = mat([[1, 0], [1, 1]])
guard('partial_prediction_survives_full_prediction_failure',
      rank(da_bad+db_partial) == 2 and multiply(mat([[1, 0]]), db_partial) == [da_bad[0]],
      dict(DB=db_partial, predictable_B_functional=[1, 0]))

rho = list(map(F, [1, 2, 3, 4]))
sigma = list(map(F, [F(1, 10), F(1, 5), F(3, 10), F(2, 5)]))
true_bound = contrast_bound(r[0], i4, rho, sigma)
reported_bound = rho[2]+sigma[2] if args.mutant == 'drop_training_error' else true_bound
guard('full_training_and_confirmation_error_bound', reported_bound == F(209, 20),
      dict(bound=reported_bound, expected_full=F(209, 20)))
epsilon_extreme = [[(1 if v >= 0 else -1)*rr] for v, rr in zip(r[0], rho)]
eta_extreme = [[(1 if v >= 0 else -1)*ss] for v, ss in zip(r[0], sigma)]
achieved = multiply([r[0]], multiply(i4, epsilon_extreme))[0][0] + multiply([r[0]], eta_extreme)[0][0]
guard('box_bound_achieved_without_probability', achieved == true_bound, achieved)

p_mix = mat([[1, 1], [1, -1]])
wmix = list(map(F, [1, 1]))
mix_bound = contrast_bound(wmix, p_mix, list(map(F, [2, 3])), list(map(F, [0, 0])))
guard('propagate_before_componentwise_absolute_value', mix_bound == 4,
      dict(P=p_mix, w=wmix, bound=mix_bound, naive_rowwise_bound=10))

cov = mat([[1, -1], [-1, 1]])
if args.mutant == 'drop_covariance':
    cov = mat([[1, 0], [0, 1]])
diff = mat([[-1, 1]])
variance = multiply(multiply(diff, cov), transpose(diff))[0][0]
guard('cross_covariance_changes_variance', variance == 4, variance)

p_leak = mat([[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
raw_b = [2, 3]
leak_edges = [(i, j) for i in [0, 1] for j in raw_b if p_leak[i][j]]
guard('processed_row_split_does_not_guarantee_raw_holdout', leak_edges == [(0, 2)], leak_edges)

# Check the quotient dimension formula on 25 independently chosen finite
# processing/nuisance combinations, including zero maps and zero-column N.
processors = [i4, p_dc, p_average, mat([[0]*4 for _ in range(4)]),
              mat([[1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]])]
nuisances = [[[] for _ in range(4)], [[F(1)] for _ in range(4)],
             [[x] for x in t], n_offset_drift, i4]
census = []
for p in processors:
    for n in nuisances:
        dd = design(p, n)
        ww = null_rows(transpose(dd), 4)
        response = multiply(ww, p)
        sensitive = rank(response)
        expected = rank(append_columns(dd, p))-rank(dd)
        assert sensitive == expected
        assert zero(multiply(ww, dd))
        assert sensitive <= rank(p)
        census.append([rank(dd), len(ww), sensitive])
guard('finite_quotient_dimension_census', len(census) == 25, census)

print(json.dumps(dict(status='PASS', mutant=args.mutant, checks=checks,
                      check_count=len(checks), python=platform.python_version(),
                      arithmetic='fractions.Fraction; exact rational finite fixtures',
                      author_scientific_imports=False), default=str, sort_keys=True))
