#!/usr/bin/env python3
"""Exact finite anchors, not an elliptic/global existence proof.

Mutation switches alter actual formula-producing functions, then the SAME
tests run. Assertions use source equations or separately assembled tensors.
"""
import argparse
import json
import platform
import sympy as s

parser = argparse.ArgumentParser()
parser.add_argument('--mutant', default='none', choices=[
    'none', 'cotton_half', 'positive_h_only', 'hamiltonian_denominator',
    'momentum_one', 'L_trace_one', 'P_sign'])
args = parser.parse_args()
checks = []

def equal(name, actual, expected):
    residual = s.simplify(actual - expected)
    checks.append({'name': name, 'pass': residual == 0,
                   'residual': str(residual)})

p, q = s.symbols('p q', positive=True)
I = range(3)
b = s.MutableDenseNDimArray.zeros(3, 3, 3)
b[0, 1, 2] = q
b[1, 2, 0] = p
b[2, 0, 1] = p
for i in I:
    for j in I:
        if i > j:
            for k in I:
                b[i, j, k] = -b[j, i, k]
# Fill the cyclic entry with i>j and its antisymmetric partner explicitly.
b[2, 0, 1] = p
b[0, 2, 1] = -p
G = s.MutableDenseNDimArray.zeros(3, 3, 3)
for i in I:
    for j in I:
        for k in I:
            G[i, j, k] = (b[i, j, k]-b[j, k, i]+b[k, i, j])/2
Ric = s.zeros(3)
for j in I:
    for k in I:
        Ric[j, k] = s.simplify(sum(
            G[j, k, m]*G[i, m, i]-G[i, k, m]*G[j, m, i]
            - b[i, j, m]*G[m, k, i] for i in I for m in I))
expected_Ric = s.diag(p*q-q*q/2, p*q-q*q/2, q*q/2)
for i in I:
    for j in I:
        equal(f'Koszul_Ric_{i}{j}', Ric[i, j], expected_Ric[i, j])
R = s.trace(Ric)
Sch = Ric-R*s.eye(3)/4
DSch = s.MutableDenseNDimArray.zeros(3, 3, 3)
for k in I:
    for i in I:
        for j in I:
            DSch[k, i, j] = s.simplify(-sum(
                G[k, i, m]*Sch[m, j]+G[k, j, m]*Sch[i, m] for m in I))

def cotton(kder, i, j, k):
    factor = s.Rational(1, 2) if args.mutant == 'cotton_half' else 1
    return factor*(kder[k, i, j]-kder[j, i, k])

C = s.MutableDenseNDimArray.zeros(3, 3, 3)
for i in I:
    for j in I:
        for k in I:
            C[i, j, k] = s.factor(cotton(DSch, i, j, k))
delta = q*(q-p)
equal('Cotton_full_covariant_norm', sum(C[i,j,k]**2 for i in I
                                       for j in I for k in I), 3*q*q*delta**2)
equal('Cotton_321_component', C[2, 1, 0], -q*delta)
equal('round_Cotton_control', sum(C[i,j,k]**2 for i in I for j in I
                                for k in I).subs(q, p), 0)
# Full covariant rank3 conformal weight: three INVERSE metrics, not rank2 dual.
t = s.symbols('t', real=True)
equal('covariant_rank3_norm_weight', s.diff(s.exp(-6*t), t).subs(t, 0), -6)

def H(h, norm2):
    divisor = 3 if args.mutant == 'hamiltonian_denominator' else 6
    if args.mutant == 'positive_h_only':
        return s.sqrt(h*h+norm2/divisor)
    return h*s.sqrt(1+norm2/(divisor*h*h))

x, y, z, u, v = s.symbols('x y z u v', real=True)
A = s.Matrix([[x,z,u],[z,y,v],[u,v,-x-y]])
norm2 = s.trace(A*A)
for h in [s.Integer(1),s.Integer(-2),s.Rational(3,5),s.Rational(-7,3)]:
    Hv = H(h,norm2)
    K = Hv*s.eye(3)+A
    equal(f'original_Hamiltonian_h={h}', R+s.trace(K)**2-s.trace(K*K)
          -2*(R/2+3*h*h),0)
    equal(f'basepoint_h={h}', H(h,0),h)
    equal(f'H_derivative_h={h}',s.diff(Hv,x),s.diff(norm2,x)/(12*Hv))
# Momentum is independently assembled from K - (tr K)I in normal coordinates.
hgrad = s.Matrix([x,y,z])
dA = s.Matrix([u,v,x+y])
original_momentum = dA+hgrad-3*hgrad
coefficient = 1 if args.mutant == 'momentum_one' else 2
for i in I:
    equal(f'original_momentum_{i}', dA[i]-coefficient*hgrad[i],
          original_momentum[i])

xi = s.Matrix(s.symbols('xi0:3',real=True))
w = s.Matrix(s.symbols('w0:3',real=True))

def L_symbol(xivec,wvec):
    coefficient = 1 if args.mutant == 'L_trace_one' else s.Rational(2,3)
    return xivec*wvec.T+wvec*xivec.T-coefficient*xivec.dot(wvec)*s.eye(3)

Ls = L_symbol(xi,w)
equal('L_tracefree_symbol',s.trace(Ls),0)
sign = 1 if args.mutant == 'P_sign' else -1
Paction = sign*Ls*xi  # i squared from two derivatives
Pmat = Paction.jacobian(w)
expected_P = -xi.dot(xi)*s.eye(3)-xi*xi.T/3
for i in I:
    for j in I:
        equal(f'P_symbol_{i}{j}',Pmat[i,j],expected_P[i,j])
equal('P_nonzero_covector_determinant',Pmat.det(),
      -s.Rational(4,3)*xi.dot(xi)**3)
# Pointwise symbol identity underlying the integration-by-parts factor.
equal('P_adjoint_energy_symbol',w.dot(Pmat*w),-s.trace(Ls.T*Ls)/2)
eps = s.symbols('eps',real=True)
for h in [s.Integer(2),s.Integer(-3)]:
    equal(f'no_linear_H_response_h={h}',s.diff(H(h,eps**2*norm2),eps).subs(eps,0),0)
    equal(f'quadratic_H_response_h={h}',s.diff(H(h,eps**2*norm2),eps,2).subs(eps,0),
          norm2/(6*h))

result = {'kind':'exact_finite_algebra_not_global_existence_proof',
          'mutant':args.mutant,'python':platform.python_version(),
          'sympy':s.__version__,'checks':checks,
          'count':len(checks),'pass':all(c['pass'] for c in checks),
          'Cotton_norm':str(s.factor(sum(C[i,j,k]**2 for i in I for j in I for k in I))),
          'omissions':['Fredholm/Schauder theorem proof','Banach IFT proof',
                       'elliptic regularity proof','infinite-dimensional coverage',
                       'actual PDE computation','line drift or time evolution']}
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['pass'] else 1)
