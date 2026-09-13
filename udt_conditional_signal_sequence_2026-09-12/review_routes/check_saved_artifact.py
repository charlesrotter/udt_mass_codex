#!/usr/bin/env python3
"""Outcome-exposed inverse-quadrature check of exact parent saved cases."""
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import scipy
from scipy.integrate import quad
from scipy.optimize import brentq

source = Path('udt_conditional_signal_sequence_2026-09-12/checks/routes.stdout')
data = json.loads(source.read_text())
results, failures = [], []
R, scale = 1.0, 1.7


def arrival(e, sign, b0, kappa):
    # At the supplied circle point (R,0), n=partial_y is a spatial unit tangent.
    if max(abs(b0+kappa*(e-1)), abs(b0+kappa*(15-1))) * R / 2 >= 1:
        raise ValueError('Entire fixed integration bracket must have positive slices')
    def angular_rate(t):
        beta_n = (b0+kappa*(t-1)) * R / 2
        g00, g0n, gnn = -scale**2, -scale**2*beta_n, scale**2*(1-beta_n**2)
        speed = (-g0n + sign*math.sqrt(g0n*g0n - gnn*g00))/gnn
        return sign*speed/R
    def angle_residual(t):
        return quad(angular_rate, e, t, epsabs=2e-12, epsrel=2e-12)[0] - 2*math.pi
    return brentq(angle_residual, e, 15, xtol=2e-12, rtol=2e-14)


for record in data['records']:
    e, b0, kappa = record['emission_t'], record['b_star'], record['kappa']
    directions = []
    for saved in record['directions']:
        sign = saved['sign']
        t = arrival(e, sign, b0, kappa)
        h = 1e-4
        slope = (arrival(e+h, sign, b0, kappa) - arrival(e-h, sign, b0, kappa))/(2*h)
        row = {'sign':sign, 'arrival':t, 'proper_duration':scale*(t-e), 'slope':slope,
               'duration_error':abs(scale*(t-e)-saved['proper_duration']),
               'slope_error':abs(slope-saved['slope'])}
        if row['duration_error'] > 3e-9 or row['slope_error'] > 3e-8:
            failures.append(row)
        directions.append(row)
    kr = math.log(directions[1]['slope']/directions[0]['slope'])/(2*math.pi*R*R)
    C = R*R*kr/2
    F = 2*math.pi if C == 0 else -math.expm1(-C*2*math.pi)/C
    B = R-directions[0]['proper_duration']/(scale*F)
    be_recovered = 2*B/R**2
    be_original = b0+kappa*(e-1)
    row = {'b_star':b0, 'kappa':kappa, 'emission_t':e, 'directions':directions,
           'kappa_recovered':kr, 'kappa_error':abs(kr-kappa),
           'b_at_emission_recovered':be_recovered, 'b_at_emission_original':be_original,
           'b_error':abs(be_recovered-be_original)}
    if row['kappa_error'] > 3e-8 or row['b_error'] > 3e-8:
        failures.append(row)
    results.append(row)

out = {'status':'PASS' if not failures else 'FAIL', 'records':results, 'failures':failures,
       'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'max_duration_error':max(d['duration_error'] for r in results for d in r['directions']),
       'max_slope_error':max(d['slope_error'] for r in results for d in r['directions']),
       'max_kappa_error':max(r['kappa_error'] for r in results),
       'max_b_error':max(r['b_error'] for r in results),
       'versions':{'python':platform.python_version(),'scipy':scipy.__version__},
       'scope':'Outcome-exposed independent quadrature/Brent readout and noiseless algebra calibration'}
print(json.dumps(out,indent=2,allow_nan=False))
raise SystemExit(0 if not failures else 1)
