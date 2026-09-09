"""Preserved reviewer guard repair: initial ±1 test did not certify full support.

The first script remains byte-unchanged. This is same-reviewer repair/regression,
not another independent review. A third harmonic is actually injected below.
"""
import importlib.util
import json
import pathlib

path = pathlib.Path(__file__).with_name('independent_adm_check.py')
spec = importlib.util.spec_from_file_location('reviewer_initial_adm', path)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
s, z = r.s, r.z


def support(expr):
    expanded = s.expand(expr)
    return sorted({int(term.as_powers_dict().get(z, 0))
                   for term in s.Add.make_args(expanded) if term != 0})


def complete_guard(expr):
    return set(support(expr)).issubset({-2, 0, 2})


def old_guard(expr):
    return r.zero(s.expand(expr).coeff(z,1)) and r.zero(s.expand(expr).coeff(z,-1))


fourM = s.expand(r.M2.subs(r.four, simultaneous=True))
fourH = s.expand(r.H2.subs(r.four, simultaneous=True))
third_mutant = fourM + z**3 + z**-3
checks = {
    'initial_guard_false_pass_reproduced': old_guard(third_mutant),
    'M2_complete_support_verified': complete_guard(fourM),
    'H2_complete_support_verified': complete_guard(fourH),
    'new_guard_rejects_actual_third_harmonic_mutant': not complete_guard(third_mutant),
    'new_guard_rejects_actual_fourth_harmonic_mutant': not complete_guard(fourH+z**4+z**-4),
}
assert all(checks.values()), checks
print(json.dumps({
    'kind':'NR1_REVIEWER_HARMONIC_GUARD_FALSE_PASS_AND_REPAIR',
    'initial_code_and_output_preserved':True,
    'old_test_excluded_as_full_support_evidence':True,
    'science_implication':'NONE: explicit quadratic product analytic argument and NR1 necessity unchanged',
    'M2_support':support(fourM),'H2_support':support(fourH),
    'actual_mutant_support':support(third_mutant),'checks':checks,
},indent=2))
