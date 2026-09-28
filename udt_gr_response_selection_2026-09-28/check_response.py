#!/usr/bin/env python3
"""Exact, scoped metric/action checks; not a native UDT field-law derivation."""
import hashlib
import itertools
import json
from pathlib import Path
import platform
import sys
import time
import sympy as s

started = time.monotonic()
t = s.symbols('t', positive=True)
x, y, z = s.symbols('x y z')
coords = (t, x, y, z)
N, A = s.Function('N')(t), s.Function('A')(t)
lam = s.symbols('lambda', positive=True)
checks = []


def simp(v):
    return s.factor(s.cancel(s.expand(v)))


def equal(name, left, right=0):
    if isinstance(left, s.MatrixBase) or isinstance(right, s.MatrixBase):
        residuals = [simp(q) for q in s.Matrix(left)-s.Matrix(right)]
    else:
        residuals = [simp(left-right)]
    ok = all(q == 0 for q in residuals)
    checks.append({'name': name, 'pass': ok,
                   'residuals': [str(q) for q in residuals]})
    if not ok:
        raise AssertionError(name + ': ' + str(residuals))


def different(name, left, right):
    residuals = [simp(q) for q in s.Matrix(left)-s.Matrix(right)]
    ok = any(q != 0 for q in residuals)
    checks.append({'name': name, 'pass': ok,
                   'nonzero_residuals': [str(q) for q in residuals if q != 0]})
    if not ok:
        raise AssertionError(name)


def geometry(g):
    inv = g.inv()
    G = [[[simp(sum(inv[a,d]*(s.diff(g[d,c], coords[b])
                  +s.diff(g[d,b], coords[c])-s.diff(g[b,c], coords[d]))
                  for d in range(4))/2) for c in range(4)]
          for b in range(4)] for a in range(4)]
    ric = s.Matrix(4,4,lambda a,b: simp(sum(
        s.diff(G[c][a][b],coords[c])-s.diff(G[c][a][c],coords[b])
        +sum(G[c][c][d]*G[d][a][b]-G[c][b][d]*G[d][a][c]
             for d in range(4)) for c in range(4))))
    R = simp(s.trace(inv*ric))
    return inv, G, ric, R


def hessian_box(q, inv, G):
    hess = s.Matrix(4,4,lambda a,b: simp(s.diff(q,coords[a],coords[b])
        -sum(G[c][a][b]*s.diff(q,coords[c]) for c in range(4))))
    return hess, simp(s.trace(inv*hess))


def response(g, inv, G, ric, R, power):
    f, fp = R**power, power*R**(power-1)
    hess, box = hessian_box(fp, inv, G)
    return (fp*ric-f*g/2+g*box-hess).applyfunc(simp)


def divergence(E, inv, G):
    return s.Matrix([simp(sum(inv[a,c]*(s.diff(E[a,b], coords[c])
       -sum(G[d][c][a]*E[d,b]+G[d][c][b]*E[a,d] for d in range(4)))
       for a in range(4) for c in range(4))) for b in range(4)])


def tf(E, g, inv, divisor=4):
    return (E-s.trace(inv*E)*g/divisor).applyfunc(simp)


def substitute(expr, lapse, scale):
    replacements = {N:lapse, A:scale}
    for j in range(1, 6):
        replacements[s.diff(N,t,j)] = s.diff(lapse,t,j)
        replacements[s.diff(A,t,j)] = s.diff(scale,t,j)
    return expr.subs(replacements, simultaneous=True).applyfunc(simp)


def euler(L, q):
    return simp(s.diff(L,q)-s.diff(s.diff(L,s.diff(q,t)),t)
                +s.diff(s.diff(L,s.diff(q,t,2)),t,2))


g = s.diag(-N**2,A**2,A**2,A**2)
inv, G, ric, R = geometry(g)
equal('metric_inverse', inv*g, s.eye(4))
equal('Ricci_symmetry', ric, ric.T)
equal('R_from_original_metric', R,
      6*(s.diff(A,t,2)/(A*N**2)+s.diff(A,t)**2/(A**2*N**2)
         -s.diff(A,t)*s.diff(N,t)/(A*N**3)))
outputs = {'generic_R': str(R), 'generic_Ricci_diagonal': list(map(str,ric.diagonal()))}
responses = {}
for power in (1,2):
    E = response(g,inv,G,ric,R,power)
    responses[power] = E
    # Different calculation: vary the reduced Lagrangian before fixing lapse.
    L = N*A**3*R**power
    equal(f'R^{power}_lapse_Euler_from_density', euler(L,N), 2*A**3/N**2*E[0,0])
    equal(f'R^{power}_scale_Euler_from_density', euler(L,A), -6*N*E[1,1])
    equal(f'R^{power}_covariant_divergence', divergence(E,inv,G), s.zeros(4,1))
    outputs[f'E_R{power}_diagonal'] = list(map(str,E.diagonal()))
hR, boxR = hessian_box(R,inv,G)
equal('R_squared_trace', s.trace(inv*responses[2]), 6*boxR)
equal('EH_response', responses[1], ric-R*g/2)

# Witness is local t>0; no sourced cosmology is inferred.
w_g = substitute(g,s.Integer(1),s.sqrt(t))
w_ric = substitute(ric,s.Integer(1),s.sqrt(t))
w_R = simp(R.subs({N:1,A:s.sqrt(t)}).doit())
equal('witness_R_zero', w_R)
equal('witness_Ricci', w_ric,s.diag(3/(4*t**2),1/(4*t),1/(4*t),1/(4*t)))
w_E2 = substitute(responses[2],s.Integer(1),s.sqrt(t))
equal('witness_R_squared_response_zero',w_E2,s.zeros(4))
different('witness_tracefree_EH_response_nonzero',tf(w_ric,w_g,w_g.inv()),s.zeros(4))
u, n = s.Matrix([1,0,0,0]), s.Matrix([0,1/s.sqrt(t),0,0])
H = 2*((w_g*u)*(w_g*u).T+(w_g*n)*(w_g*n).T)
equal('reciprocal_tangent_trace',s.trace(w_g.inv()*H))
equal('witness_actual_pair_balance_failure',s.trace(w_g.inv()*w_ric*w_g.inv()*H),2/t**2)
outputs['witness'] = {'metric':str(w_g),'Ricci':str(w_ric),'R':str(w_R),
                      'E_R2':str(w_E2),'Ricci_pair_contraction':str(2/t**2)}

# Control with R=6/t^2. Recompute scaled geometry from original metric.
c_g = s.diag(-1,t**2,t**2,t**2)
c_inv,c_G,c_ric,c_R = geometry(c_g)
equal('control_R_nonconstant',c_R,6/t**2)
c_E2 = response(c_g,c_inv,c_G,c_ric,c_R,2)
c_wrong = 2*c_R*c_ric-c_R**2*c_g/2
different('reject_R_squared_without_derivative_terms',c_E2,c_wrong)
# A=t has Ric_00=0, so the wrong formula accidentally has zero divergence.
# Preserve that false-pass witness, and use A=t^2 to make this control sensitive.
equal('preserved_wrong_formula_divergence_false_pass_at_A_t',
      divergence(c_wrong,c_inv,c_G),s.zeros(4,1))
d_g = s.diag(-1,t**4,t**4,t**4)
d_inv,d_G,d_ric,d_R = geometry(d_g)
d_wrong = 2*d_R*d_ric-d_R**2*d_g/2
equal('sensitive_wrong_formula_divergence',divergence(d_wrong,d_inv,d_G),
      s.Matrix([-864/t**5,0,0,0]))
different('reject_wrong_formula_divergence_at_A_t_squared',
          divergence(d_wrong,d_inv,d_G),s.zeros(4,1))
sg = lam**2*c_g
si,sG,sric,sR = geometry(sg)
equal('scaled_connection',s.Matrix([q for aa in sG for bb in aa for q in bb]),
      s.Matrix([q for aa in c_G for bb in aa for q in bb]))
for power,weight in ((1,0),(2,-2)):
    unscaled = response(c_g,c_inv,c_G,c_ric,c_R,power)
    scaled = response(sg,si,sG,sric,sR,power)
    equal(f'R^{power}_actual_metric_homothety_weight_{weight}',scaled,lam**weight*unscaled)
different('reject_weight_zero_for_R_squared',response(sg,si,sG,sric,sR,2),c_E2)
different('reject_TF_divisor_three_in_four_dimensions',tf(c_ric,c_g,c_inv,3),
          tf(c_ric,c_g,c_inv))
equal('scalar_only_response_DDR_vacuous',tf(c_R*c_g,c_g,c_inv),s.zeros(4))
Lambda = s.symbols('Lambda')
equal('constant_trace_term_DDR_invisible',tf(responses[1]+Lambda*g,g,inv),tf(responses[1],g,inv))

# Finite regression only; arbitrary order is proved analytically in candidate.
monomials = [ds for ds in itertools.product(range(2),repeat=7)
             if sum(k*d for k,d in zip(range(2,9),ds)) == 2]
assert monomials == [(1,0,0,0,0,0,0)]
checks.append({'name':'normal_jet_degree_two_enumeration_through_order_eight',
               'pass':True,'solutions':monomials,'scope':'finite regression, not general proof'})
outputs['control_E_R2'] = str(c_E2)
outputs['control_wrong_E_R2'] = str(c_wrong)
result = {'status':'PASS','scope':'exact homogeneous-family identities and stated controls only',
          'versions':{'python':sys.version,'sympy':s.__version__,'platform':platform.platform()},
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'elapsed_seconds':time.monotonic()-started,'checks':checks,'outputs':outputs,
          'omissions':['general finite-jet theorem owned by analytic argument',
                       'full G301 invariant-basis rank certificate not repeated',
                       'no native admission, empirical fit, stability or causal IVP test']}
dest = Path(sys.argv[1])
with dest.open('x') as f:
    json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'output':str(dest),
                  'elapsed_seconds':result['elapsed_seconds']}))
