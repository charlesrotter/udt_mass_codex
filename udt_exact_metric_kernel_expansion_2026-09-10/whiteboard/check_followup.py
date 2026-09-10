#!/usr/bin/env python3
"""Exact follow-up: targeted data ambiguity and actual coordinate transformation."""
import json
import platform
import sympy as sp

checks = []


def zero(name, expr):
    entries = list(expr) if isinstance(expr, sp.MatrixBase) else [expr]
    residuals = [sp.simplify(entry) for entry in entries]
    checks.append({'name': name, 'passed': all(entry == 0 for entry in residuals),
                   'residuals': list(map(str, residuals))})
    if not checks[-1]['passed']:
        raise AssertionError((name, residuals))


def main():
    t, x, y, z = sp.symbols('t x y z', real=True)
    lam = sp.symbols('lam', positive=True)
    coords = (t, x, y, z)
    # FREE exact envelope witness, not a selected native UDT history.
    u_cov = sp.Matrix([-1, 0, -lam*x, 0])
    g = sp.diag(0, lam**2, lam**2, lam**2)-u_cov*u_cov.T
    ginv = sp.simplify(g.inv())
    u = sp.Matrix([1, 0, 0, 0])
    zero('observer_covector', g*u-u_cov)
    zero('observer_unit', (u.T*g*u)[0]+1)
    P = sp.eye(4)+u*u_cov.T  # P^a_b projects vector arguments into U-perp.
    du = sp.Matrix(4, 4, lambda i, j: sp.diff(u_cov[j], coords[i])-sp.diff(u_cov[i], coords[j]))
    omega = sp.simplify(P.T*du*P/2)
    norm = sp.simplify(sum(ginv[a, c]*ginv[b, d]*omega[a, b]*omega[c, d]
                           for a in range(4) for b in range(4)
                           for c in range(4) for d in range(4)))
    zero('direct_projected_vorticity_norm', norm-1/(2*lam**2))
    zero('density_omission_norm_difference', norm.subs(lam, 1)-norm.subs(lam, 2)-sp.Rational(3, 8))
    directions = ((1, 0, 0), (0, 1, 0), (0, 0, 1),
                  (1, 1, 0), (1, 0, 1), (0, 1, 1))
    for k, v in enumerate(directions):
        J = sp.zeros(4, 2)
        J[0, 0] = 1
        J[1:, 1] = sp.Matrix(v)
        h = sp.simplify(J.T*g*J)
        m = sp.sqrt(-h.det())
        C = sp.diag(1, 1/m)
        normalized = sp.simplify(C.T*h*C)
        zero(f'normalized_metric_lambda_independent_{k}', normalized.diff(lam))
        zero(f'density_retains_lambda_{k}', m-lam*sp.sqrt(sum(vi**2 for vi in v)))
        zero(f'normalized_shift_{k}', normalized[0, 1]/normalized[0, 0]
             -x*v[1]/sp.sqrt(sum(vi**2 for vi in v)))
    T, m = sp.symbols('T m', positive=True)
    B, a = sp.symbols('B a', real=True)
    hraw = sp.Matrix([[-T**2, -T**2*m*B],
                      [-T**2*m*B, m**2*(1/T**2-T**2*B**2)]])
    K = sp.Matrix([[1, 0], [-a/m, 1/m]])
    hnew = sp.simplify(K.T*hraw*K)
    expected = sp.Matrix([[-T**2*(1-a*B)**2+a*a/T**2,
                           -T**2*B*(1-a*B)-a/T**2],
                          [-T**2*B*(1-a*B)-a/T**2, 1/T**2-T**2*B**2]])
    zero('general_actual_tape_coordinate_transform', hnew-expected)
    zero('general_actual_tape_determinant', hnew.det()+1)
    original_clock = sp.Matrix([1, a])
    zero('general_original_clock_norm', (original_clock.T*hnew*original_clock)[0]+T**2)
    return {'status': 'PASS', 'python': platform.python_version(), 'sympy': sp.__version__,
            'runtime_model_version': 'UNATTESTED',
            'evidence_type': 'exact symbolic construction regression, not fresh review',
            'check_count': len(checks), 'checks': checks,
            'vorticity_norm': str(norm),
            'parameters': {'lambda': 'arbitrary positive', 'comparison_values': ['1', '2'],
                           'coordinates': ['t', 'x', 'y', 'z'], 'domain': 'R^4'},
            'shapes': {'metric': [4, 4], 'projector': [4, 4], 'pair_metric': [2, 2]}}


if __name__ == '__main__':
    try:
        result = main()
    except Exception as error:
        print(json.dumps({'status': 'FAIL', 'error': repr(error), 'checks': checks}, indent=2))
        raise
    print(json.dumps(result, indent=2))
