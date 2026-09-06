"""Exact finite controls; analytic proof is in CANDIDATE_ARGUMENT.md.

No production solver, observed data, physical interpretation or file mutation.
--mutant deliberately changes the named calculation to test guard sensitivity.
"""
import argparse
from fractions import Fraction as F
from itertools import product
import json

parser = argparse.ArgumentParser()
parser.add_argument('--mutant', choices=('missing_half', 'wrong_overlap',
                                        'positive_is_enough', 'raw_rates'))
args = parser.parse_args()
passed = []


def guard(name, condition):
    if not condition:
        print(json.dumps({'status': 'FAIL', 'guard': name, 'mutant': args.mutant,
                          'passed_before_failure': passed}, sort_keys=True))
        raise SystemExit(1)
    passed.append(name)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def mv(a, x):
    return tuple(dot(row, x) for row in a)


def inverse(z):
    divisor = F(1) if args.mutant == 'missing_half' else F(2)
    return ((z[0]+z[2]-z[1])/divisor,
            (z[0]+z[1]-z[2])/divisor,
            (z[1]+z[2]-z[0])/divisor)


def feasible(z):
    if args.mutant == 'positive_is_enough':
        return all(x >= 0 for x in z)
    return all(x >= 0 for x in inverse(z))


def normalize(y, rates):
    return y if args.mutant == 'raw_rates' else tuple(x/r for x, r in zip(y, rates))


base = ((F(1), F(1), F(0)), (F(0), F(1), F(1)),
        (F(1), F(0), F(1)))
if args.mutant == 'wrong_overlap':
    base = (base[0], base[1], base[0])

# Cells and windows are evaluated directly on Borel points, not via the matrix.
points = ((F(1, 4), F(1, 2)), (F(5, 4), F(1, 2)),
          (F(9, 4), F(1, 2)))


def cell(point):
    x, y = point
    if not (0 <= x <= 3 and 0 <= y <= 1):
        raise ValueError('outside retained rectangle')
    return 0 if x < 1 else (1 if x < 2 else 2)


window_cells = ({0, 1}, {1, 2}, {0, 2})
incidence = tuple(tuple(F(cell(point) in members) for point in points)
                  for members in window_cells)
guard('actual_window_preimages', incidence == base)

signed_records = list(product(range(-2, 4), repeat=3))
guard('exact_inverse_reconstructs_records',
      all(mv(base, inverse(tuple(map(F, z)))) == z for z in signed_records))
guard('triangle_nonnegative_equivalence',
      all(feasible(tuple(map(F, z))) ==
          (z[0]+z[1] >= z[2] and z[0]+z[2] >= z[1] and z[1]+z[2] >= z[0])
          for z in signed_records))
mass_controls = list(product(range(3), repeat=3))
guard('all_declared_nonnegative_mass_controls_survive',
      all(feasible(mv(base, tuple(map(F, x)))) for x in mass_controls))
guard('zero_measure_allowed', feasible((F(0),)*3))
guard('positive_record_can_be_incompatible', not feasible((F(1), F(1), F(3))))

# Full spacetime covector and observer contractions in (-,+,+,+).
eta = (F(-1), F(1), F(1), F(1))
alpha, spacing = F(2), F(3)
ds = (F(1), F(2), F(3))
kcov = (-alpha, F(0), F(0), alpha)
kvec = tuple(eta[i]*kcov[i] for i in range(4))


def metric(a, b):
    return sum((eta[i]*a[i]*b[i] for i in range(4)), F(0))


observers = tuple(((d+1/d)/2, F(0), F(0), (1/d-d)/2) for d in ds)
omegas = tuple(-dot(kcov, u) for u in observers)
rates = tuple(w/spacing for w in omegas)
guard('full_null_gradient_and_future_orientation', metric(kvec, kvec) == 0 and kvec[0] > 0)
guard('full_unit_future_observers',
      all(metric(u, u) == -1 and u[0] > 0 for u in observers))
guard('full_frequency_contractions', omegas == tuple(alpha*d for d in ds))
guard('screen_cut_metric', metric((0, 1, 0, 0), (0, 1, 0, 0)) == 1 and
      metric((0, 0, 1, 0), (0, 0, 1, 0)) == 1 and
      metric((0, 1, 0, 0), (0, 0, 1, 0)) == 0)
cuts = tuple((F(i), point[0], point[1], F(i))
             for i in range(3) for point in points)
guard('cuts_on_reference_phase', all(dot(kcov, x) == 0 for x in cuts))
weighted = tuple(tuple(rates[i]*x for x in base[i]) for i in range(3))
masses = (F(1), F(2), F(3))
y_good = mv(weighted, masses)
guard('raw_compatible_record', y_good == (F(2), F(20, 3), F(8)))
guard('known_observer_rate_normalization', normalize(y_good, rates) == (F(3), F(5), F(4)))
guard('mass_recovery_from_weighted_readout', inverse(normalize(y_good, rates)) == masses)
y_bad = (rates[0], rates[1], 3*rates[2])
h = (1/rates[0], 1/rates[1], -1/rates[2])
dual_columns = tuple(dot(h, tuple(weighted[i][j] for i in range(3))) for j in range(3))
guard('dual_certificate_nonnegative_columns', dual_columns == (F(0), F(2), F(0)))
guard('dual_certificate_negative_record', dot(h, y_bad) == -1)
phase_scales = (F(1, 5), F(1), F(7, 3))
guard('common_affine_phase_spacing_gauge',
      all(tuple((b*w)/(b*spacing) for w in omegas) == rates for b in phase_scales))


def read_measure(measure):
    return tuple(rates[i]*sum((amount for point, amount in measure.items()
                              if cell(point) in members), F(0))
                 for i, members in enumerate(window_cells))


mu = {points[j]: masses[j] for j in range(3)}
mu_other = {(F(3, 4), F(1, 2)): F(1), points[1]: F(2), points[2]: F(3)}
guard('direct_measure_matches_weighted_matrix', read_measure(mu) == y_good)
guard('distinct_label_measures_same_record', mu != mu_other and read_measure(mu_other) == y_good)
guard('disjoint_queries_allow_all_declared_nonnegative_records',
      all(tuple(rates[i]*(F(z[i])/rates[i]) for i in range(3)) == z
          for z in mass_controls))
with_unseen = tuple(tuple(row)+(F(0),) for row in weighted)
guard('zero_column_mass_is_invisible',
      mv(with_unseen, masses+(F(0),)) == mv(with_unseen, masses+(F(19),)))
# A rank-deficient finite protocol: moving common-cell mass into the two
# individual cells preserves both records, but not the underlying cell vector.
a2 = ((F(1), F(0), F(1)), (F(0), F(1), F(1)))
guard('nonnegative_kernel_displacement',
      mv(a2, (F(1), F(1), F(1))) == mv(a2, (F(2), F(2), F(0))))

print(json.dumps({
    'status': 'PASS', 'guard_count': len(passed), 'guards': passed,
    'signed_record_controls': len(signed_records),
    'nonnegative_mass_controls': len(mass_controls),
    'phase_scale_controls': len(phase_scales),
    'compatible_raw_record': list(map(str, y_good)),
    'incompatible_raw_record': list(map(str, y_bad)),
    'dual_certificate': list(map(str, h)),
    'dual_column_values': list(map(str, dual_columns)),
    'dual_record_value': str(dot(h, y_bad)),
    'ordinary_cell_masses': list(map(str, masses)),
    'arithmetic': 'standard-library Fraction exact rational',
    'evidence_limit': 'finite exact regression; analytic proof owns general claims',
    'mutant': args.mutant,
}, indent=2, sort_keys=True))
