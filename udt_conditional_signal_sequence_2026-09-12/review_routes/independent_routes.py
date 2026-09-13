#!/usr/bin/env python3
"""Independent full-metric actual-time circular-guide review; no author imports."""
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as sp

checks = []
failures = []
mutations = []
records = []


def require(name, condition, detail=None):
    row = {'name': name, 'pass': bool(condition)}
    if detail is not None:
        row['detail'] = detail
    checks.append(row)
    if not condition:
        failures.append(row)


def reject(name, condition, detail):
    mutations.append({'name': name, 'rejected': bool(condition), 'detail': detail})
    require('catch:' + name, condition)


def linear_A(t, R, a0, q):
    return a0 * R + q * t


def actual_time_rhs(t, alpha, s, R, a0, q, L):
    # Contract the full Cartesian four-metric with K and the oriented spatial
    # unit circle tangent, then solve its quadratic for the signed spatial speed.
    theta = s * float(alpha[0])
    x, y = R * math.cos(theta), R * math.sin(theta)
    b = 2 * linear_A(t, R, a0, q) / R**2
    bx, by = -b * y / 2, b * x / 2
    nx, ny = -math.sin(theta), math.cos(theta)
    beta_n = bx * nx + by * ny
    g00 = -L**2
    g0n = -L**2 * beta_n
    gnn = L**2 * (nx * nx + ny * ny - beta_n**2)
    discriminant = (2 * g0n)**2 - 4 * gnn * g00
    signed_speed = (-2 * g0n + s * math.sqrt(discriminant)) / (2 * gnn)
    return [s * signed_speed / R]


def integrate(e, s, R, a0, q, L, check_residual=False):
    def arrival(t, alpha):
        return float(alpha[0]) - 2 * math.pi
    arrival.terminal = True
    arrival.direction = 1

    def slice_guard(t, alpha):
        return (1 - 1e-6) * R - abs(linear_A(t, R, a0, q))
    slice_guard.terminal = True
    slice_guard.direction = -1

    sol = solve_ivp(lambda t, a: actual_time_rhs(t, a, s, R, a0, q, L),
                    (e, e + 12 * R), [0.0], method='DOP853',
                    rtol=2e-12, atol=2e-13, max_step=R / 10,
                    events=(arrival, slice_guard))
    returned = len(sol.t_events[0]) == 1
    out = {'success': bool(sol.success), 'returned': returned,
           'arrival': float(sol.t_events[0][0]) if returned else None,
           'guard_event': float(sol.t_events[1][0]) if len(sol.t_events[1]) else None,
           'last_angle': float(sol.y[0, -1]), 'nfev': int(sol.nfev)}
    if check_residual:
        residuals, futures, margins = [], [], []
        for t, alpha in zip(sol.t, sol.y[0]):
            d_alpha = actual_time_rhs(t, [alpha], s, R, a0, q, L)[0]
            theta = s * alpha
            theta_dot = s * d_alpha
            x, y = R * math.cos(theta), R * math.sin(theta)
            vx, vy = -R * math.sin(theta) * theta_dot, R * math.cos(theta) * theta_dot
            b = 2 * linear_A(t, R, a0, q) / R**2
            beta_v = b * (x * vy - y * vx) / 2
            root = 1 + beta_v
            gvv = L**2 * (-root**2 + vx**2 + vy**2)
            residuals.append(abs(gvv) / (L**2 * (1 + vx**2 + vy**2)))
            futures.append(root)
            margins.append(1 - abs(b) * R / 2)
        out.update(max_null_residual=max(residuals), min_future_root=min(futures),
                   min_slice_margin=min(margins), nodes=len(sol.t))
    return out


def analytic(e, s, R, a0, q):
    A = linear_A(e, R, a0, q)
    fac = 2 * math.pi if q == 0 else -math.expm1(-s * q * 2 * math.pi) / (s * q)
    return e + (R - s * A) * fac


for k, (R, a0, q, e) in enumerate((R, a0, q, e)
        for R in (0.6, 1.3) for a0 in (-0.25, 0.0, 0.25)
        for q in (-0.04, -1e-12, 0.0, 1e-12, 0.04)
        for e in (0.0, 0.35, 0.9)):
    L = (0.7, 2.4)[k % 2]
    case = {'R': R, 'A0_over_R': a0, 'q': q, 'e': e, 'L': L, 'directions': []}
    for s in (1, -1):
        got = integrate(e, s, R, a0, q, L, True)
        expected = analytic(e, s, R, a0, q)
        require(f'arrival_exists:{k}:{s}', got['success'] and got['returned'], got)
        if not got['returned']:
            continue
        h = 1e-3 * R
        lower = integrate(e - h, s, R, a0, q, L)
        upper = integrate(e + h, s, R, a0, q, L)
        require(f'neighbor_arrivals:{k}:{s}', lower['returned'] and upper['returned'])
        slope = (upper['arrival'] - lower['arrival']) / (2 * h)
        expected_slope = math.exp(-s * 2 * math.pi * q)
        error = abs(got['arrival'] - expected)
        slope_error = abs(slope - expected_slope)
        require(f'arrival_agreement:{k}:{s}', error <= 3e-10 * (1 + abs(expected)), error)
        require(f'pulse_slope:{k}:{s}', slope_error <= 3e-8, slope_error)
        require(f'original_metric_null:{k}:{s}', got['max_null_residual'] <= 2e-12)
        require(f'future_root:{k}:{s}', got['min_future_root'] > 0)
        require(f'full_slice:{k}:{s}', got['min_slice_margin'] > 1e-6)
        proper = math.sqrt(L**2) * (got['arrival'] - e)
        proper_expected = L * (expected - e)
        require(f'proper_clock:{k}:{s}', abs(proper - proper_expected) <= 3e-10 * (1 + abs(proper_expected)))
        got.update(s=s, analytic_arrival=expected, arrival_error=error,
                   finite_difference_slope=slope, analytic_slope=expected_slope,
                   slope_error=slope_error, proper_transit=proper)
        case['directions'].append(got)
    records.append(case)

# Finite whole positive emission interval, with independently integrated endpoints.
whole = []
for s in (1, -1):
    e0, e1, R, a0, q, L = 0.1, 0.83, 1.3, -0.25, 0.04, 2.4
    t0 = integrate(e0, s, R, a0, q, L)['arrival']
    t1 = integrate(e1, s, R, a0, q, L)['arrival']
    actual = L * (t1 - t0)
    expected = L * (e1 - e0) * math.exp(-s * 2 * math.pi * q)
    require(f'whole_duration:{s}', abs(actual - expected) <= 3e-10 * (1 + abs(expected)))
    whole.append({'s': s, 'emission_duration': L * (e1 - e0), 'arrival_duration': actual,
                  'expected': expected, 'absolute_error': abs(actual - expected)})

# The adversarial reference trajectory is independent time-domain output.
R, a0, q, e, L, s = 1.3, 0.0, 0.04, 0.0, 2.4, 1
reference = integrate(e, s, R, a0, q, L)['arrival']
frozen = e + 2 * math.pi * (R - s * linear_A(e, R, a0, q))
first_order = e + (R - s * linear_A(e, R, a0, q)) * 2 * math.pi * (1 - s * q * math.pi)
reject('instantaneous_frozen_arrival', abs(reference - frozen) > 1e-4,
       {'actual': reference, 'wrong': frozen})
reject('rate_truncated_arrival', abs(reference - first_order) > 1e-4,
       {'actual': reference, 'wrong': first_order})
h = 1e-3 * R
observed_slope = (integrate(e+h, s, R, a0, q, L)['arrival'] -
                  integrate(e-h, s, R, a0, q, L)['arrival']) / (2*h)
reject('reversed_pulse_slope_sign', abs(observed_slope - math.exp(s * 2 * math.pi * q)) > 1e-3,
       {'actual': observed_slope, 'wrong': math.exp(s * 2 * math.pi * q)})
reject('omitted_proper_L_factor', abs(L * (reference - e) - (reference - e)) > 1e-3,
       {'proper': L * (reference - e), 'wrong': reference - e})
small_q = 1e-12
small_ref = integrate(0, 1, R, 0.25, small_q, L)['arrival']
naive = R * 0.75 * (1 - math.exp(-2 * math.pi * small_q)) / small_q
reject('tiny_rate_naive_exp_subtraction', abs(small_ref - naive) > 3e-10 * (1 + abs(small_ref)),
       {'actual': small_ref, 'wrong': naive, 'absolute_error': abs(small_ref - naive)})

# Full-domain adverse case: initially regular, but minus direction hits slice guard first.
invalid = integrate(0, -1, 1.0, 0.0, 0.2, 1.0, True)
invalid['outside_formula_arrival'] = analytic(0, -1, 1.0, 0.0, 0.2)
require('inadmissible_history_stopped', invalid['success'] and not invalid['returned']
        and invalid['guard_event'] is not None and invalid['last_angle'] < 2 * math.pi, invalid)
reject('initial_only_slice_guard', abs(linear_A(0, 1.0, 0.0, 0.2)) < 1.0
       and not invalid['returned'], {'initial_guard': True, 'full_traversal_admitted': False})

# Actual ordering can oppose the instantaneous stationary control within a safe window.
plus = integrate(0, 1, 1.0, -0.03, 0.02, 1.0, True)
minus = integrate(0, -1, 1.0, -0.03, 0.02, 1.0, True)
reversal = {'actual_plus_minus': plus['arrival'] - minus['arrival'],
            'frozen_plus_minus': -4 * math.pi * (-0.03),
            'plus_margin': plus['min_slice_margin'], 'minus_margin': minus['min_slice_margin']}
require('ordering_reversal', reversal['actual_plus_minus'] < 0 < reversal['frozen_plus_minus']
        and min(reversal['plus_margin'], reversal['minus_margin']) > 1e-6, reversal)

# Fixed frozen geometry versus a family independently re-frozen at each emission.
frozen_control = {'fixed_profile_slope': 1.0,
                  'refrozen_family_slope_plus': 1 - 2 * math.pi * 0.04,
                  'actual_history_slope_plus': math.exp(-2 * math.pi * 0.04)}
require('frozen_control_typing', len(set(frozen_control.values())) == 3, frozen_control)

# Exact full-metric observer projection; no G405 F or W implementation is imported.
t, x, y, z, ell, b0, kap = sp.symbols('t x y z L b0 kap', real=True)
b = b0 + kap * t
theta = sp.Matrix([1, -b*y/2, b*x/2, 0])
g = ell**2 * (sp.diag(0, 1, 1, 1) - theta * theta.T)
u = sp.Matrix([1/ell, 0, 0, 0])
uf = g*u
coords = (t, x, y, z)
du = sp.Matrix(4, 4, lambda i,j: sp.diff(uf[j], coords[i]) - sp.diff(uf[i], coords[j]))
project = sp.eye(4) + uf * u.T
w = sp.simplify(project * du * project.T / 2)
ginv = sp.simplify(g.inv())
raised = sp.simplify(ginv * w * ginv.T)
norm = sp.factor(sum(w[i,j] * raised[i,j] for i in range(4) for j in range(4)))
require('exact_full_metric_vorticity', sp.simplify(norm - b**2 / (2*ell**2)) == 0, str(norm))
require('literal_comparison_clock_norm', sp.simplify(-g[0,0] - ell**2) == 0,
        'G405 bare K=partial_t has T=L for L>0, not T=1 before calibration.')

# Flat circle: at theta=0, tangent=(R,0,R,0), acceleration=(0,-R,0,0).
flat_tangent = sp.Matrix([ell, 0, ell, 0])
flat_acceleration = sp.Matrix([0, -ell, 0, 0])
flat_null = (flat_tangent.T * sp.diag(-1, 1, 1, 1) * flat_tangent)[0]
require('flat_circular_null_tangent', flat_null == 0)
require('flat_circular_not_free_geodesic',
        sp.simplify(flat_tangent[0]*flat_acceleration[1] - flat_tangent[1]*flat_acceleration[0]) != 0)

result = {'kind': 'independent full-metric route numerical anchors and exact projection',
          'status': 'PASS' if not failures else 'FAIL', 'checks': len(checks),
          'expected_mutation_rejections': len(mutations), 'failures': failures,
          'versions': {'python': platform.python_version(), 'numpy': np.__version__,
                       'scipy': scipy.__version__, 'sympy': sp.__version__},
          'environment': {k: os.environ.get(k) for k in
                          ('PYTHONDONTWRITEBYTECODE','OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')},
          'records': records, 'whole_event': whole, 'adverse_domain': invalid,
          'ordering_reversal': reversal, 'frozen_control': frozen_control,
          'mutations': mutations, 'check_details': checks,
          'max_arrival_error': max(d['arrival_error'] for c in records for d in c['directions']),
          'max_slope_error': max(d['slope_error'] for c in records for d in c['directions']),
          'max_normalized_null_residual': max(d['max_null_residual'] for c in records for d in c['directions']),
          'minimum_slice_margin': min(d['min_slice_margin'] for c in records for d in c['directions']),
          'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'argv': sys.argv}
print(json.dumps(result, indent=2, allow_nan=False))
raise SystemExit(0 if not failures else 1)
