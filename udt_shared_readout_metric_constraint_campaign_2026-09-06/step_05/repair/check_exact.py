"""Same-premise repaired controls; initial frozen check_exact.py remains unchanged."""
import argparse
from fractions import Fraction as Q
from itertools import product
import json

ap = argparse.ArgumentParser()
ap.add_argument('--mutant', choices=('unrelaxed', 'wrong_sign', 'missing_half', 'fixed_weights', 'reject_nonzero'))
mode = ap.parse_args().mutant
guards = []


def check(name, condition):
    if not condition:
        print(json.dumps({'status': 'FAIL', 'guard': name, 'mutant': mode,
                          'passed_before_failure': guards}, sort_keys=True))
        raise SystemExit(1)
    guards.append(name)


def residuals(z, e):
    a, b = 1-e, 1+e
    if mode == 'unrelaxed':
        a, b = Q(1), Q(1)
    if mode == 'wrong_sign':
        a, b = b, a
    return tuple(b*(sum(z)-v)-a*v for v in z)


def construct(z, e):
    if mode == 'reject_nonzero' and any(z):
        return None
    if min(z) < 0 or min(residuals(z, e)) < 0:
        return None
    a, b = 1-e, 1+e
    s = [v/a for v in z]
    bad = [i for i in range(3) if s[i] > sum(s)-s[i]]
    if bad:
        i = bad[0]
        s[i] = sum(s)-s[i]
    divisor = 1 if mode == 'missing_half' else 2
    masses = ((s[0]+s[2]-s[1])/divisor, (s[0]+s[1]-s[2])/divisor,
              (s[1]+s[2]-s[0])/divisor)
    weights = tuple(z[i]/s[i] if s[i] else Q(1) for i in range(3))
    if mode == 'fixed_weights':
        weights = (Q(1),)*3
    return masses, weights, tuple(s)


def original_integrals(m, f):
    return f[0]*(m[0]+m[1]), f[1]*(m[1]+m[2]), f[2]*(m[0]+m[2])


target = (Q(1), Q(1), Q(3))
check('sharp_boundary_not_rejected', min(residuals(target, Q(1, 5))) == 0)
check('strict_subthreshold_exclusion', residuals(target, Q(1, 10))[2] == Q(-1, 2))
sharp_m, sharp_f = (Q(5, 4), Q(0), Q(5, 4)), (Q(4, 5), Q(4, 5), Q(6, 5))
check('explicit_original_integral_sharpness', original_integrals(sharp_m, sharp_f) == target)

# Pointwise certificate on every rectangle corner; arbitrary measurable
# pointwise values are handled by the analytic bound in the argument.
for e in (Q(0), Q(1, 10), Q(1, 5), Q(1, 2), Q(9, 10)):
    a, b = 1-e, 1+e
    for x, y in product((a, b), repeat=2):
        check('pointwise_pair_certificate', b*x-a*y >= 0)

control_records, accepted, rejected = 0, 0, 0
for e in (Q(0), Q(1, 10), Q(1, 5), Q(1, 2), Q(9, 10)):
    for zz in product((Q(-1), Q(0), Q(1, 2), Q(1), Q(3)), repeat=3):
        control_records += 1
        result = construct(zz, e)
        feasible = min(zz) >= 0 and (sum(zz) == 0 or
                    e >= max(Q(0), 2*max(zz)/sum(zz)-1))
        check('record_feasibility_not_silently_discarded', (result is not None) == feasible)
        if result is None:
            rejected += 1
            continue
        accepted += 1
        m, f, s = result
        check('constructed_mass_positivity', min(m) >= 0)
        check('constructed_weight_bounds', all(1-e <= v <= 1+e for v in f))
        check('original_weighted_integrals_reconstruct', original_integrals(m, f) == zz)
        check('constructed_window_amounts', (m[0]+m[1], m[1]+m[2], m[0]+m[2]) == s)
        check('triangle_interval_bounds', all(zz[i]/(1+e) <= s[i] <= zz[i]/(1-e)
                                            for i in range(3)))
    for zz in product((Q(0), Q(1, 2), Q(1), Q(3)), repeat=3):
        if sum(zz) == 0:
            check('zero_record_separate', construct(zz, e) is not None)
            continue
        threshold = max(Q(0), 2*max(zz)/sum(zz)-1)
        check('closed_form_threshold_equivalence', (min(residuals(zz, e)) >= 0) == (e >= threshold))

check('target_threshold', 2*max(target)/sum(target)-1 == Q(1, 5))
check('one_positive_excluded_below_one', all(construct((Q(1), Q(0), Q(0)), e) is None
                                          for e in (Q(0), Q(1, 5), Q(9, 10), Q(999, 1000))))
check('fixed_unit_weight_counterexample', (target[0]+target[1]-target[2])/2 == Q(-1, 2))

# Supplied constant observers in the SC2 flat geometry; actual contractions.
alpha, spacing = Q(2), Q(3)
references = (Q(2, 3), Q(4, 3), Q(2))
for r, f in zip(references, sharp_f):
    d = spacing*r*f/alpha
    ut, uz = (d+1/d)/2, (1/d-d)/2
    check('observer_future_unit', ut > 0 and -ut*ut+uz*uz == -1)
    check('original_frequency_contraction', alpha*(ut-uz)/spacing == r*f)

print(json.dumps({
    'status': 'PASS', 'mutant': mode, 'assertions': len(guards),
    'guard_groups': sorted(set(guards)), 'control_records': control_records,
    'constructed_records': accepted, 'rejected_records': rejected,
    'sharpness_original_integrals': list(map(str, original_integrals(sharp_m, sharp_f))),
    'sharpness_masses': list(map(str, sharp_m)), 'sharpness_weights': list(map(str, sharp_f)),
    'target_threshold': '1/5', 'strict_subthreshold_residual': '-1/2',
    'evidence_type': 'same-context exact regression and controls, not independent proof',
    'not_checked': ['arbitrary measurable integration theorem', 'actual calibration bound',
                    'actual device identity', 'physical content', 'arbitrary fixed-kernel sufficiency'],
}, indent=2, sort_keys=True))
