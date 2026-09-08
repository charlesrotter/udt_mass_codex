#!/usr/bin/env python3
"""BG1 fresh source-first exact algebra; no author code or output imports."""
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import sympy as s

started = time.monotonic()
checks = []
mutations = []


def zero(name, expr):
    expr = s.factor(s.simplify(expr))
    checks.append({"name": name, "residual": str(expr), "pass": expr == 0})
    assert expr == 0, (name, expr)


def catch(name, expr):
    expr = s.factor(s.simplify(expr))
    mutations.append({"name": name, "residual": str(expr), "caught": expr != 0})
    assert expr != 0, (name, expr)


# Full symmetric tensor split, including every independent off-diagonal entry.
t, h = s.symbols("tau h", real=True)
d1, d2, b12, b13, b23 = s.symbols("d1 d2 b12 b13 b23", real=True)
A = s.Matrix([[d1, b12, b13], [b12, d2, b23], [b13, b23, -d1-d2]])
K = A + t*s.eye(3)/3
zero("Hamiltonian_tracefree_split", s.trace(K)**2-s.trace(K*K)-(s.Rational(2,3)*t*t-s.trace(A*A)))

# Exact global family: x=|X|^2>0 for a nowhere-zero Killing vector.
# u sqrt(1-u)=epsilon (m/x)^(3/2), |u|<1/4.
x = s.symbols("x", positive=True)
u = s.symbols("u", real=True)
ux = -3*u*(1-u)/(x*(2-3*u))
alpha = h/s.sqrt(1-u)
beta = -3*alpha*u/(2*x)
Dx = lambda expr: s.diff(expr, x)+s.diff(expr, u)*ux
zero("implicit_u_derivative", s.diff(u*s.sqrt(1-u),u)*ux+3*u*s.sqrt(1-u)/(2*x))
zero("original_Hamiltonian_rank_one", 6*alpha**2+4*alpha*beta*x-6*h*h)
zero("original_momentum_rank_one", -2*Dx(alpha)-x*Dx(beta)-s.Rational(3,2)*beta)
trace = 3*alpha+beta*x
normA = s.Rational(3,2)*alpha**2*u**2
zero("family_trace_norm_relation", s.Rational(2,3)*trace**2-normA-6*h*h)
zero("signed_base_h", alpha.subs(u,0)-h)
zero("trace_excess_identity", (trace/(3*h))**2-1-u**2/(4*(1-u)))
catch("wrong_rank_one_factor_1_instead_3_over_2", 6*alpha**2+4*alpha*(-alpha*u/x)*x-6*h*h)
catch("wrong_Killing_acceleration_sign", -2*Dx(alpha)-x*Dx(beta)-s.Rational(1,2)*beta)
catch("omit_derivative_of_beta", -2*Dx(alpha)-s.Rational(3,2)*beta)

# Koszul and curvature are recomputed from source brackets, not Ricci outputs.
a, c = s.symbols("a c", positive=True)
br = [[[s.S(0) for k in range(3)] for j in range(3)] for i in range(3)]
for i,j,k,value in [(0,1,2,2*c/a**2), (1,2,0,2/c), (2,0,1,2/c)]:
    br[i][j][k], br[j][i][k] = value, -value
G = [[[s.simplify((br[i][j][k]-br[j][k][i]+br[k][i][j])/2)
       for k in range(3)] for j in range(3)] for i in range(3)]


def curvature(i,j,k,l):
    return s.simplify(sum(G[j][k][p]*G[i][p][l]-G[i][k][p]*G[j][p][l]
                          -br[i][j][p]*G[p][k][l] for p in range(3)))


Ric = s.Matrix(3,3,lambda i,j: s.simplify(sum(curvature(k,i,j,k) for k in range(3))))
expected = s.diag(4/a**2-2*c**2/a**4,4/a**2-2*c**2/a**4,2*c**2/a**4)
for i in range(3):
    for j in range(3):
        zero(f"Ricci_from_brackets_{i+1}{j+1}", Ric[i,j]-expected[i,j])
DRic = [[[s.simplify(-sum(G[k][i][p]*Ric[p,j]+G[k][j][p]*Ric[i,p]
                          for p in range(3))) for j in range(3)]
         for i in range(3)] for k in range(3)]
# C_ijk=D_k Ric_ij-D_j Ric_ik, since scalar curvature is constant.
Cotton = [[[s.simplify(DRic[k][i][j]-DRic[j][i][k])
            for k in range(3)] for j in range(3)] for i in range(3)]
cotton_norm = s.factor(sum(Cotton[i][j][k]**2 for i in range(3)
                           for j in range(3) for k in range(3)))
gap = 4*(c*c-a*a)/a**4
zero("nonround_Cotton_component_C132", Cotton[0][2][1]-(c/a**2)*gap)
zero("Cotton_norm_formula", cotton_norm-12*(c/a**2)**2*gap**2)
zero("round_Cotton_control", cotton_norm.subs(c,a))
catch("claim_nonround_Cotton_zero", Cotton[0][2][1])

q11,q22,q33,q12,q13,q23=s.symbols("q11 q22 q33 q12 q13 q23",real=True)
Q=s.Matrix([[q11,q12,q13],[q12,q22,q23],[q13,q23,q33]])
divQ=[s.factor(-sum(G[j][j][p]*Q[p,i]+G[j][i][p]*Q[j,p]
                    for j in range(3) for p in range(3))) for i in range(3)]
zero("invariant_momentum_1", divQ[0]-(2*c/a**2-2/c)*q23)
zero("invariant_momentum_2", divQ[1]-(2/c-2*c/a**2)*q13)
zero("invariant_momentum_3", divQ[2])
for i in range(3):
    zero(f"horizontal_tracefree_TT_{i+1}",divQ[i].subs({q13:0,q23:0,q11:1,q22:-1,q33:0,q12:0}))

result = {
    "scope": "Fresh source-first exact algebra; mathematical proof is in SOURCE_FIRST.md.",
    "python": sys.version,
    "sympy": s.__version__,
    "platform": platform.platform(),
    "checks": checks,
    "executed_mutations": mutations,
    "Ricci": [[str(Ric[i,j]) for j in range(3)] for i in range(3)],
    "Cotton_C132": str(Cotton[0][2][1]),
    "Cotton_norm_squared": str(cotton_norm),
    "invariant_momentum": [str(v) for v in divQ],
    "seconds": time.monotonic()-started,
    "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
print(json.dumps(result,indent=2,sort_keys=True))
