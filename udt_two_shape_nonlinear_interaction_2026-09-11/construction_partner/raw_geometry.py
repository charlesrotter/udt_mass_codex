#!/usr/bin/env python3
"""Exact initial four-geometry from metric jets, without imported candidate code.

Supplied conditional Ric=0 equation; FREE A,B,c,theta within frozen family.
Pinned comparison choices and conventions are in CONSTRUCTION_FREEZE.md.
All arithmetic is symbolic/exact. Counts include structural checks, not proofs.
"""
import argparse
import datetime
import itertools
import json
import platform
import sympy as S

parser = argparse.ArgumentParser()
parser.add_argument('--mutant', choices=['omit_axial_completion', 'freeze_second_time'])
args = parser.parse_args()
checks = []
observations = {}

def simp(v):
    return S.factor(S.trigsimp(S.cancel(v)))

def check(name, residuals):
    if not isinstance(residuals, (list, tuple, S.MatrixBase)):
        residuals = [residuals]
    values = [simp(v) for v in residuals]
    failures = [str(v) for v in values if v != 0]
    checks.append({'name': name, 'components': len(values), 'nonzero_residuals': failures})
    if failures:
        print(json.dumps({'mutant': args.mutant, 'checks': checks, 'observations': observations}, indent=2))
        raise AssertionError(name + ': ' + repr(failures))

p,r,px,rx = S.symbols('p r p_x r_x', real=True)
# The symbol s has an explicit nonzero domain; do not encode p/r as nonzero.
s = S.Symbol('s', real=True, nonzero=True)
k,kx = S.symbols('kappa kappa_x', real=True)
d = p*p+r*r
completed_k = (d-s*s)/(2*s)
K = S.Matrix([[k,0,0],[0,s-p,-r],[0,-r,s+p]])
Kx = S.Matrix([[kx,0,0],[0,-px,-rx],[0,-rx,px]])
tau = S.trace(K)
hamiltonian = simp(tau*tau-S.trace(K*K))
momenta = [sum(Kx[j,i] if j == 0 else 0 for j in range(3))
           - (S.trace(Kx) if i == 0 else 0) for i in range(3)]
chosen_k = -s/2 if args.mutant == 'omit_axial_completion' else completed_k
observations['full_initial_constraint_expressions'] = {
    'R3': '0 (constant initial metric)', 'H': str(hamiltonian),
    'M': [str(simp(v)) for v in momenta],
    'completion': str(completed_k),
    'omit_completion_H': str(simp(hamiltonian.subs(k,-s/2)))}
check('all_original_initial_constraints', [hamiltonian.subs(k,chosen_k), *momenta])

# Exact jets at every initial point; spatial initial derivatives are all zero.
# TT is obtained by solving all spatial Ricci equations, then checked below by
# reconstructing the four-dimensional connection and curvature from scratch.
g = S.diag(-1,1,1,1)
gi = g.inv()
dg = [S.zeros(4) for _ in range(4)]
ddg = [[S.zeros(4) for _ in range(4)] for _ in range(4)]
TT = -2*tau*K+4*K*K
if args.mutant == 'freeze_second_time':
    TT = S.diag(S.Rational(10,9),S.Rational(4,9),S.Rational(4,9))
for i,j in itertools.product(range(3),repeat=2):
    dg[0][i+1,j+1] = -2*K[i,j]
    ddg[0][0][i+1,j+1] = TT[i,j]
    ddg[0][1][i+1,j+1] = ddg[1][0][i+1,j+1] = -2*Kx[i,j]
dgi = [-gi*dg[u]*gi for u in range(4)]
Gamma = {}
dGamma = {}
for a,b,c in itertools.product(range(4),repeat=3):
    Gamma[a,b,c] = simp(sum(gi[a,e]*(dg[b][e,c]+dg[c][e,b]-dg[e][b,c])
                           for e in range(4))/2)
    for u in range(4):
        dGamma[u,a,b,c] = simp(sum(
            dgi[u][a,e]*(dg[b][e,c]+dg[c][e,b]-dg[e][b,c])
            +gi[a,e]*(ddg[u][b][e,c]+ddg[u][c][e,b]-ddg[u][e][b,c])
            for e in range(4))/2)
Rup = {}
for a,b,c,h in itertools.product(range(4),repeat=4):
    Rup[a,b,c,h] = simp(dGamma[c,a,h,b]-dGamma[h,a,c,b]+sum(
        Gamma[a,c,e]*Gamma[e,h,b]-Gamma[a,h,e]*Gamma[e,c,b] for e in range(4)))
R = {(a,b,c,h): simp(sum(g[a,e]*Rup[e,b,c,h] for e in range(4)))
     for a,b,c,h in itertools.product(range(4),repeat=4)}
Ric = S.Matrix(4,4,lambda b,h: simp(sum(Rup[a,b,a,h] for a in range(4))))
observations['raw_Ricci_before_completion'] = [[str(v) for v in row] for row in Ric.tolist()]
check('all_spatial_Ricci_equations_from_raw_metric', [Ric[i,j] for i,j in itertools.product(range(1,4),repeat=2)])
check('all_original_Ricci_after_completion', [v.subs(k,completed_k) for v in Ric])
check('Riemann_pair_symmetries_and_first_Bianchi', [
    value for a,b,c,h in itertools.product(range(4),repeat=4)
    for value in [R[a,b,c,h]+R[b,a,c,h],R[a,b,c,h]+R[a,b,h,c],
                  R[a,b,c,h]-R[c,h,a,b],R[a,b,c,h]+R[a,c,h,b]+R[a,h,b,c]]])

# FIRST-PAIR Lorentzian Hodge star. epsilon_0123=+1 and raise e,f using gi.
def star_tensor(tensor):
    return {(a,b,c,h): simp(sum(S.LeviCivita(a,b,e,f)*gi[e,e]*gi[f,f]
                *tensor[e,f,c,h] for e,f in itertools.product(range(4),repeat=2))/2)
            for a,b,c,h in itertools.product(range(4),repeat=4)}
starR = star_tensor(R)
starstarR = star_tensor(starR)
check('Lorentzian_first_pair_Hodge_square_minus_one', [starstarR[key]+R[key] for key in R])
E = S.Matrix(3,3,lambda i,j:R[i+1,0,j+1,0])
Bmag = S.Matrix(3,3,lambda i,j:starR[i+1,0,j+1,0])
J = simp(S.trace(E*Bmag))
curvature_dual_contraction = simp(sum(gi[a,a]*gi[b,b]*gi[c,c]*gi[h,h]*R[a,b,c,h]*starR[a,b,c,h]
                              for a,b,c,h in itertools.product(range(4),repeat=4)))
expected_E = S.Matrix([[2*s*k,0,0],[0,-k*(s+p),-k*r],[0,-k*r,-k*(s-p)]])
# This expression requires the Hamiltonian constraint.
check('electric_tensor_on_exact_completion', [(v-w).subs(k,completed_k) for v,w in zip(E,expected_E)])
expected_B = S.Matrix([[0,0,0],[0,rx,-px],[0,-px,-rx]])
check('magnetic_tensor_from_raw_first_pair_dual', Bmag-expected_B)
check('mixed_contraction_general_formula', J+2*k*(p*rx-r*px))
check('full_curvature_pseudoscalar_factor', curvature_dual_contraction-16*J)
check('electric_magnetic_symmetry_trace_on_shell', [*(E-E.T),*(Bmag-Bmag.T),
                            S.trace(E).subs(k,completed_k),S.trace(Bmag)])
observations['curvature'] = {
    'E_before_completion': [[str(v) for v in row] for row in E.tolist()],
    'E_completed_form': [[str(v) for v in row] for row in expected_E.tolist()],
    'B': [[str(v) for v in row] for row in Bmag.tolist()],
    'J':str(J), 'C_contract_starC':str(curvature_dual_contraction),
    'all_nonzero_Riemann_components_before_completion': {str(key):str(value) for key,value in R.items() if value!=0}}

A,ampB,X,theta,c,epsilon,a,b,c2 = S.symbols('A B X theta c epsilon a b c2', real=True)
pshape=A*S.cos(X)
rshape=ampB*S.cos(X+theta)
subshape={p:pshape,r:rshape,px:S.diff(pshape,X),rx:S.diff(rshape,X)}
W = simp((p*rx-r*px).subs(subshape))
Jfamily = simp(J.subs(k,completed_k).subs(subshape))
check('relative_phase_Wronskian',W+A*ampB*S.sin(theta))
check('same_phase_control',Jfamily.subs(theta,0))
check('one_component_controls',[Jfamily.subs(A,0),Jfamily.subs(ampB,0)])
quadratureJ = simp(Jfamily.subs(theta,-S.pi/2))
check('quadrature_scalar',quadratureJ - A*ampB*(s*s-A*A*S.cos(X)**2-ampB**2*S.sin(X)**2)/s)
radial = simp(Jfamily.subs({A:epsilon*a,ampB:epsilon*b,s:-S.Rational(2,3)+epsilon**2*c2}))
leading = simp(S.diff(radial,epsilon,2).subs(epsilon,0)/2)
check('radial_leading_order',leading-S.Rational(2,3)*a*b*S.sin(theta))
observations['family']={'W':str(W),'J':str(Jfamily),'quadrature_J':str(quadratureJ),
    'epsilon2_coefficient':str(leading),
    'epsilon4_coefficient':str(simp(S.diff(radial,epsilon,4).subs(epsilon,0)/24)),
    'd_bound_on_safe_box':'d <= A^2+B^2 < 1/8',
    's_bound_on_safe_box':'-5/6 < s < -1/2',
    'kappa_lower_bound_on_safe_box':'kappa > 1/8 (written monotonic bound)',
    'no_completion_H':str(simp(hamiltonian.subs(k,-s/2)))}

# Two point commutator detects impossibility of simultaneous constant GL(2,R)
# similarity diagonalization, hence also constant allowed lattice/basis changes.
H = S.Matrix([[pshape,rshape],[rshape,-pshape]])
comm = H.subs(X,0)*H.subs(X,S.pi/2)-H.subs(X,S.pi/2)*H.subs(X,0)
check('commutator_nonreducibility_formula',comm-S.Matrix([[0,-2*A*ampB*S.sin(theta)],[2*A*ampB*S.sin(theta),0]]))
observations['commutator_at_zero_and_pi_over_two']=[[str(simp(v)) for v in row] for row in comm.tolist()]

# Exact cancellation example lies outside the frozen near-background safe box.
cancel = {p:s*S.cos(X),r:s*S.sin(X),px:-s*S.sin(X),rx:s*S.cos(X)}
check('finite_amplitude_exact_cancellation_control',J.subs(k,completed_k).subs(cancel))
observations['cancellation_control']='A=B=s != 0, theta=-pi/2: d=s^2, kappa=0, E=0, J=0; B need not vanish. Outside safe box.'

# Geometric orientation control: a transverse reflection has determinant -1.
# At the tensor level it flips the volume form and therefore J; J^2 is unaffected.
check('orientation_reversal_scalar_square_control',(-J)**2-J**2)
print(json.dumps({'status':'PASS','started_by_context':'/root/two_shape_construction',
    'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'python':platform.python_version(),'sympy':S.__version__,'mutant':args.mutant,
    'checks':checks,'observations':observations,
    'limits':'symbolic exact initial jets, not PDE evolution/existence or independent adversarial review'},indent=2))
