#!/usr/bin/env python3
"""ACP1 reviewer-only exact arithmetic; no author/source implementation imports."""
import csv
import hashlib
import json
import os
import platform
import resource
import sys
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
assert os.environ.get('OPENBLAS_NUM_THREADS') == '1'
assert os.environ.get('OMP_NUM_THREADS') == '1'
checks = []
cases = []
catches = []

def check(name, value):
    if not value:
        raise RuntimeError(name)
    checks.append(name)

def mat(a):
    return [[F(v) for v in row] for row in a]

def tr(a):
    return [list(row) for row in zip(*a)]

def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def det(a):
    return a[0][0]*a[1][1] - a[0][1]*a[1][0]

def inv(a):
    d = det(a)
    return [[a[1][1]/d, -a[0][1]/d], [-a[1][0]/d, a[0][0]/d]]

def scale(a, s):
    return [[s*x for x in row] for row in a]

def dec(x):
    return Decimal(x.numerator)/Decimal(x.denominator)

# Hyperbolic emitter in 1+1 Minkowski: eta'=a, exp(eta)=r.
# Observer x=0; emitter is locally at x>0; received coordinate time t_o=t+x.
# These are finite samples of a regular exact family, not astronomical metrics.
for i, r in enumerate([F(1,3), F(1,2), F(2,3), F(1), F(3,2), F(2), F(3), F(5)]):
    a=F(i+1,7); al=F(i+2,3); alp=F(i-2,11)
    gam=(r+1/r)/2; vgam=(r-1/r)/2
    tp=gam; xp=vgam; tpp=a*vgam; xpp=a*gam
    arrival=tp+xp; arrival2=tpp+xpp
    check(f'proper_norm_{i}', -gam*gam+vgam*vgam == -1)
    check(f'accel_orthogonal_{i}', -gam*tpp+vgam*xpp == 0)
    omega_e=gam+vgam; omega_o=F(1)
    check(f'arrival_vs_frequency_{i}', arrival == omega_e/omega_o)
    observed_drift=arrival2/arrival
    check(f'optical_drift_from_arrival_{i}', observed_drift == a)
    # Direct source-frequency quotient followed by observed optical definition.
    received_nu=al/omega_e
    source_derivative_nu=alp/omega_e-al*arrival2/omega_e**2
    direct_optical_drift=-source_derivative_nu/(received_nu**2 * arrival)
    formula=arrival2/(al*arrival)-alp/al**2
    check(f'variable_transition_{i}', direct_optical_drift == formula)
    affine=F(i+2,5); affinep=F(2-i,13)
    we=affine*omega_e; wo=affine
    wep=affinep*omega_e+affine*arrival2; wop=affinep
    zprime=(wep*wo-we*wop)/wo**2
    check(f'affine_family_derivative_{i}', zprime == arrival2)
    if r != 1:
        check(f'extra_divisor_caught_{i}', observed_drift/r != a)
        catches.append(f'extra_arrival_divisor_{i}')
    if affine != 1:
        check(f'one_endpoint_scale_caught_{i}', we/omega_o != arrival)
        catches.append(f'one_endpoint_affine_{i}')
    cases.append({'type':'proper_clock','r':str(r),'proper_acceleration':str(a),
                  'Z':str(arrival),'optical_drift_per_c':str(observed_drift)})

I=mat([[1,0],[0,1]])
for i,(j,re,ro) in enumerate([
    ([[3,0],[0,3]], [[1,0],[0,1]], [[1,0],[0,1]]),
    ([[6,0],[0,F(3,2)]], [[1,1],[0,1]], [[2,0],[0,1]]),
    ([[-3,0],[0,3]], [[0,1],[1,0]], [[1,0],[1,1]]),
    ([[2,1],[1,5]], [[2,1],[1,1]], [[1,2],[0,1]])]):
    J=mat(j); Re=mat(re); Ro=mat(ro); omega=F(i+2,3)
    # G348 future-affine reverse block; sky angle equals minus propagation.
    B=scale(J,-1/omega)
    qo=mul(tr(inv(Ro)), inv(Ro)); qe=mul(tr(inv(Re)), inv(Re))
    Bp=mul(mul(Re,B),tr(Ro))
    Jp=scale(mul(Bp,qo),-omega)
    check(f'typed_map_covariance_{i}',Jp == mul(mul(Re,J),inv(Ro)))
    area_squared=omega**4*det(B)**2
    check(f'area_metric_covariance_{i}',area_squared == omega**4*det(Bp)**2*det(qo)*det(qe))
    affine=F(i+3,2)
    check(f'map_affine_invariance_{i}',scale(scale(B,1/affine),-affine*omega)==J)
    theta=mat([[1],[2]])
    source=mul(J,theta)
    wrong=mul(scale(B,omega),theta)
    check(f'fixed_screen_sign_catch_{i}',wrong != source)
    catches.append(f'fixed_screen_sign_{i}')
    recovered=mul(inv(J),source)
    check(f'source_angle_inverse_{i}',recovered==theta)
    cases.append({'type':'screen','determinant':str(det(J)),
                  'area_distance_squared':str(abs(det(J))),
                  'source_vector':[str(x[0]) for x in source]})
check('equal_area_unequal_images',det(mat([[3,0],[0,3]])) == det(mat([[6,0],[0,F(3,2)]])))
check('shear_catch',mul(mat([[3,0],[0,3]]),mat([[1],[0]])) != mul(mat([[6,0],[0,F(3,2)]]),mat([[1],[0]])))
catches.append('determinant_as_full_map')

# Actual observer boost at same event, central future direction -x.
# Rational circle direction n(t)=(-(1-t^2)/(1+t^2),2t/(1+t^2),0).
# At t=0, dn_y/dt=2; tetrad transformation gives 2/F.
for p in [F(1,2),F(2),F(3)]:
    gam=(p+1/p)/2; bgam=(p-1/p)/2
    frequency=gam+bgam
    nx=(-bgam-gam)/frequency; dy=F(2)/frequency
    check(f'boost_clock_{p}',frequency==p and nx == -1)
    check(f'aberration_derivative_{p}',(dy/F(2))**2==1/p**2)
    check(f'area_observer_factor_{p}',(p**2)*(dy/F(2))**2 == 1)
    cases.append({'type':'observer_boost','frequency_multiplier':str(p),
                  'solid_angle_multiplier':str(1/p**2),'area_multiplier':str(p**2)})

input_path=Path('udt_observation_metric_evaluation_2026-10-04/observation/MCP_TABLE1_INPUT.tsv')
with input_path.open() as f:
    source=next(x for x in csv.DictReader(f,delimiter='\t') if x['galaxy']=='CGCG 074-064')
c=F('299792.458'); v=F(source['v_opt_CMB_km_s']); vm=F(source['v_reported_minus_km_s']); vp=F(source['v_reported_plus_km_s'])
d=F(source['D_Mpc']); dm=F(source['D_minus_Mpc']); dp=F(source['D_plus_Mpc'])
summary=[]
with localcontext() as context:
    context.prec=70
    for label,V,D in [('lower_marginals',v-vm,d-dm),('medians',v,d),('upper_marginals',v+vp,d+dp)]:
        Z=1+V/c; chi=(1-Z**2)/(1+Z**2); ell=dec(Z).ln(); phi=-ell
        # Separately check tanh via exponential, against the exact rational form.
        tanh=(2*phi).exp(); tanh=(tanh-1)/(tanh+1)
        check(f'chi_decimal_crosscheck_{label}',abs(tanh-dec(chi)) < Decimal('1e-65'))
        check(f'negative_clock_parameter_{label}',Z>1 and chi<0)
        row={'label':label,'v_opt_CMB_km_s':str(dec(V)),'D_Mpc':str(dec(D)),
             'Z0':str(dec(Z)),'phi_summary':str(phi),'chi_summary':str(dec(chi)),
             'D_squared_Mpc2':str(dec(D*D))}
        summary.append(row);cases.append({'type':'CGCG_marginal_arithmetic','label':label})
    check('frame_center',v-F('263.3')==F('6908.9'))
check('finite_case_budget',len(cases)<=100)
print(json.dumps({'status':'PASS','finite_cases':len(cases),'checks':len(checks),
  'check_names':checks,'wrong_rule_separators':catches,'cases':cases,'CGCG':summary,
  'input_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),
  'runtime':{'python':sys.version,'platform':platform.platform(),'address_space_bytes':resource.getrlimit(resource.RLIMIT_AS),
  'OMP_NUM_THREADS':os.environ.get('OMP_NUM_THREADS'),'OPENBLAS_NUM_THREADS':os.environ.get('OPENBLAS_NUM_THREADS')},
  'limits':'Exact rational controls plus 70-digit Decimal log/exp. No fitted metric, no source posterior replay, no data independence or ordinary systemic clock established.'},indent=2))
