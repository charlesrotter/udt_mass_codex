"""Method checks and forecast sensitivity; never reads/fits observed clock outcomes.

Inputs: Zheng2023 Table1 published uncertainty/expected-gradient summaries,
Supplement3H gravimeter magnitude, and SI c_E calibration convention.
Finite graph is a noiseless identifiability illustration, not a covariance model.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations
import json
import platform
import sys

getcontext().prec = 60
D = Decimal


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][j]
        a[r] = [x / p for x in a[r]]
        for i in range(len(a)):
            if i != r:
                p = a[i][j]
                a[i] = [x - p*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


pairs = list(combinations(range(5), 2))
incidence = [[int(k == j)-int(k == i) for k in range(5)] for i,j in pairs]
assert rank(incidence) == 4
assert all(sum(row) == 0 for row in incidence)
height = list(range(5))  # arbitrary equal spacing, no observed coordinates
height_column = [[sum(x*z for x,z in zip(row,height))] for row in incidence]
assert rank(height_column) == 1
# Every lapse contrast can be hidden by an unconstrained per-node additive bias.
augmented = [row + row for row in incidence]
assert rank(augmented) == 4

c = D(299792458)  # supplied observed/SI clock-ruler calibration, not UDT selection
g = D('9.803')
height_m = D('.01')
s = g * height_m / c**2
u_stat = D('.7')
u_sys = D('2.5')
u_expected_bound = D('.1')
reference = D('10.9')
u_quad = (u_stat**2 + u_sys**2).sqrt()
# Gaussian independence only for this forecast comparison of summary errors;
# source's reported total2.6 also carried, no independent budget certification.
u_with_reference = (u_quad**2 + u_expected_bound**2).sqrt()
fractional_sensitivity = u_with_reference / reference
assert D('.23') < fractional_sensitivity < D('.25')
exp_remainder_bound = s*s*s.exp()/2
assert exp_remainder_bound < D('1e-36')
# If |a(h)-a(0)| <= B |h|, log-rate integral remainder <= B H^2/(2c^2).
# B below is a sufficient threshold at the entire 1sigma budget, NOT a measured B.
u_fraction_1cm = D('2.6e-19')
b_threshold = 2*c*c*u_fraction_1cm/height_m**2
assert b_threshold > D('400')

out = {
    'classification': 'analytic method/regression and preliminary sensitivity; no observation fit',
    'python': sys.version,
    'platform': platform.platform(),
    'precision_decimal_digits': getcontext().prec,
    'inputs': {'c_E_m_s': str(c), 'g_m_s2_magnitude': str(g),
               'height_m': str(height_m), 'uncertainties_1e19_per_cm':
               {'stat': str(u_stat), 'sys': str(u_sys), 'reference_upper_bound': str(u_expected_bound)},
               'reference_gradient_magnitude_1e19_per_cm': str(reference)},
    'graph': {'shape': [10,5], 'exact_rank': rank(incidence),
              'cycle_dimension': len(pairs)-rank(incidence),
              'linear_height_rank': rank(height_column),
              'nonlinear_node_contrast_directions': rank(incidence)-rank(height_column),
              'with_free_bias_shape': [10,10], 'with_free_bias_rank': rank(augmented)},
    'sensitivity': {'log_rate_magnitude_1cm': str(s),
                   'quadrature_summary_uncertainty_1e19_per_cm': str(u_quad),
                   'including_reference_bound_fraction': str(fractional_sensitivity),
                   'reported_total_fraction': str(D('2.6')/reference),
                   'exponential_remainder_upper_bound': str(exp_remainder_bound),
                   'equivalent_potential_difference_u_m2_s2': str(c*c*u_fraction_1cm),
                   'equivalent_height_u_m': str(c*c*u_fraction_1cm/g),
                   'gradient_bound_B_threshold_s_minus2_at_full_u': str(b_threshold)},
    'omissions': ['no observed gradient/residual/p-value/fit read or calculated',
                  'no raw covariance reconstruction or empirical rank certification',
                  'no stationarity/acceleration-gradient bound measured here',
                  'no atomic/instrument theory derived from UDT']}
print(json.dumps(out, indent=2))
