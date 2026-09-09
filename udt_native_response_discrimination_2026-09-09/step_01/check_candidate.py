#!/usr/bin/env python3
"""ND1 exact support using the unchanged G260 production tensor-jet method.

This is shared-source computational support, not independent review and not
a finite-sample proof of the ODE classification. Writes only stdout.
"""
import hashlib
import importlib.util
import json
import platform
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'udt_g260_gr_quiet_angular_nondiscard_audit_2026-08-25/derive_angular_nondiscard.py'
EXPECTED = '34d91536f8529819aa6ffd90cb5b7ce23af6b92edcafcef2b63e1c7626075e0e'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
spec = importlib.util.spec_from_file_location('nd1_g260_shared_method', SOURCE)
method = importlib.util.module_from_spec(spec)
spec.loader.exec_module(method)

records = []
checks = []


def gate(name, condition):
    checks.append({'name': name, 'passed': bool(condition)})
    if not condition:
        raise AssertionError(name)


def run_case(name, r, f, fp, fpp, family=None, extra=None):
    r, f, fp, fpp = map(F, (r, f, fp, fpp))
    gate(name + ':domain', r > 0 and f > 0)
    metric, first, second = method.four_metric_jets(r, f, fp, fpp, True)
    ricci, einstein, scalar = method.curvature_from_metric_jets(metric, first, second)
    inverse = method.diagonal_inverse(metric)
    mixed = [[sum(inverse[i][k] * ricci[k][j] for k in range(4))
              for j in range(4)] for i in range(4)]
    square = [[sum(mixed[i][k] * mixed[k][j] for k in range(4))
               for j in range(4)] for i in range(4)]
    trace2 = sum(square[i][i] for i in range(4))
    smix = [[mixed[i][j] - (scalar / 4 if i == j else 0)
             for j in range(4)] for i in range(4)]
    qmix = [[square[i][j] - (trace2 / 4 if i == j else 0)
             for j in range(4)] for i in range(4)]
    a = -fpp / 2 - fp / r
    b = (1 - f) / r**2 - fp / r
    angular = r**2 * fpp / 2 - f + 1
    expected = [a, a, b, b]
    gate(name + ':complete_Ricci_blocks', all(
        mixed[i][j] == (expected[i] if i == j else 0)
        for i in range(4) for j in range(4)))
    gate(name + ':scalar', scalar == 2 * (a + b))
    gate(name + ':full_tensor_factorization', all(
        qmix[i][j] == scalar * smix[i][j] / 2
        for i in range(4) for j in range(4)))
    gate(name + ':angular_not_discarded', angular == r**2 * (b - a))
    radial = 2 * (-smix[0][0] + smix[1][1])
    transverse = 2 * (-smix[0][0] + smix[2][2])
    gate(name + ':radial_blind', radial == 0)
    gate(name + ':transverse_Ricci_probe', transverse == 2 * angular / r**2)
    qzero = all(value == 0 for row in qmix for value in row)
    szero = all(value == 0 for row in smix for value in row)
    gate(name + ':quadratic_factor_zero_set', qzero == (a == b or a == -b))
    gate(name + ':angular_iff_S', (angular == 0) == szero)
    if family == 'E':
        gate(name + ':E_survivor', qzero and szero and angular == 0)
        gate(name + ':E_scalar', scalar == -12 * extra)
    elif family == 'Z':
        gate(name + ':Z_survivor', qzero and scalar == 0)
        gate(name + ':Z_angular', angular == 2 * extra / r**2)
        gate(name + ':Z_extra_is_detectable', szero == (extra == 0))
        if extra:
            gate(name + ':radial_false_pass_discriminator', radial == 0 and transverse != 0)
    elif family == 'outside':
        gate(name + ':genuine_nonzero_control', not qzero and not szero and angular != 0)
    records.append({'name': name, 'r': str(r), 'f': str(f), 'fp': str(fp),
                    'fpp': str(fpp), 'A': str(a), 'B': str(b),
                    'R': str(scalar), 'C_ang': str(angular),
                    'Q_zero': qzero, 'S_zero': szero})


for n in range(1, 9):
    run_case('arbitrary_' + str(n), F(n + 1, 3), F(n + 2, 5),
             F((-1)**n * n, 7), F(n - 4, 11))
for r in map(F, (1, 2, 3)):
    for a, b in ((F(0), F(1)), (F(1, 9), F(2)), (F(-1, 100), F(0))):
        run_case(f'E_{r}_{a}_{b}', r, 1 + a*r*r + b/r,
                 2*a*r - b/r**2, 2*a + 2*b/r**3, 'E', a)
    for b, d in ((F(1), F(0)), (F(0), F(1)), (F(1), F(-1, 4))):
        run_case(f'Z_{r}_{b}_{d}', r, 1 + b/r + d/r**2,
                 -b/r**2 - 2*d/r**3, 2*b/r**3 + 6*d/r**4, 'Z', d)
run_case('outside_both', 1, 2, 0, 1, 'outside')

# Counter-controls: these are checks of materially different geometric cases,
# not execution of a mutated production solver or a claimed mutation harness.
z = next(row for row in records if row['name'] == 'Z_1_0_1')
gate('false_generalization_Q_implies_angular_zero_is_refuted', z['Q_zero'] and z['C_ang'] != '0')
e = next(row for row in records if row['name'] == 'E_1_1/9_2')
gate('false_generalization_balanced_implies_Ricci_flat_is_refuted', e['S_zero'] and e['R'] != '0')
gate('nonvacuous_support', any(row['Q_zero'] for row in records)
     and any(not row['Q_zero'] for row in records)
     and any(row['Q_zero'] and not row['S_zero'] for row in records))
gate('shared_method_unchanged', hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED)

print(json.dumps({'status': 'PASS_EXACT_SUPPORT_NOT_CLASSIFICATION_PROOF',
    'python': platform.python_version(), 'arithmetic': 'fractions.Fraction',
    'shared_method': str(SOURCE.relative_to(ROOT)), 'shared_method_sha256': EXPECTED,
    'independent_implementation': False, 'checks_passed': len(checks),
    'cases': records, 'checks': checks,
    'omissions': ['general metric classification', 'proof by finite sampling',
                  'physical law adoption', 'dynamical or stability claims']}, indent=2))
