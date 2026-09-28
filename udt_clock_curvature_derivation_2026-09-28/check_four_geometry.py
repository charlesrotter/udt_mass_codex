#!/usr/bin/env python3
"""Exact finite-jet checks of the 4D Ricci identity; author implementation."""
import json
import sympy as s

c = s.symbols('t x y z', real=True)
t, x, y, z = c
N = 1+t*x/5+y/19
L = 1+t/7+x/9+z/23
b = (t+x)/11
P = 1+(t+x)/13
Q = 1+(t-2*x)/17
g = s.Matrix([[-N*N, -N*N*b, 0, 0],
              [-N*N*b, L*L-N*N*b*b, 0, 0],
              [0, 0, P*P, 0], [0, 0, 0, Q*Q]])
dg = [g.diff(v) for v in c]
ddg = [[dg[i].diff(v) for v in c] for i in range(4)]
Ufun = s.Matrix([1/N, 0, 0, 0])
dUfun = [Ufun.diff(v) for v in c]
ddUfun = [[dUfun[i].diff(v) for v in c] for i in range(4)]
all_results = []
rejected = []

for number, vals in enumerate([(0, 0, 0, 0), (s.Rational(1,4), -s.Rational(1,5), 0, 0),
                               (-s.Rational(1,6), s.Rational(1,7), s.Rational(1,8), s.Rational(1,9))]):
    at = dict(zip(c, vals))
    ev = lambda e: e.subs(at)
    gm = ev(g); inv = gm.inv()
    d = [ev(v) for v in dg]
    dd = [[ev(v) for v in row] for row in ddg]
    dinv = [-inv*v*inv for v in d]
    C = lambda j,k,l: d[k][l,j]+d[l][j,k]-d[j][k,l]
    Gamma = [[[sum(inv[a,j]*C(j,k,l) for j in range(4))/2
               for l in range(4)] for k in range(4)] for a in range(4)]
    dGamma = [[[[sum(dinv[q][a,j]*C(j,k,l)+inv[a,j]*(dd[q][k][l,j]
                   +dd[q][l][j,k]-dd[q][j][k,l]) for j in range(4))/2
                for l in range(4)] for k in range(4)] for a in range(4)] for q in range(4)]
    R = [[[[dGamma[k][a][l][bb]-dGamma[l][a][k][bb]
          +sum(Gamma[a][k][j]*Gamma[j][l][bb]-Gamma[a][l][j]*Gamma[j][k][bb]
               for j in range(4))
          for l in range(4)] for k in range(4)] for bb in range(4)] for a in range(4)]
    U = ev(Ufun)
    dU = [ev(v) for v in dUfun]
    ddU = [[ev(v) for v in row] for row in ddUfun]
    M = s.Matrix(4,4, lambda a,bb: dU[bb][a]+sum(Gamma[a][bb][j]*U[j] for j in range(4)))
    dM = [s.Matrix(4,4,lambda a,bb: ddU[q][bb][a]
                  +sum(dGamma[q][a][bb][j]*U[j]+Gamma[a][bb][j]*dU[q][j] for j in range(4)))
          for q in range(4)]
    A = M*U
    dA = [dM[q]*U+M*dU[q] for q in range(4)]
    dotM = s.Matrix(4,4,lambda a,bb: sum(U[q]*(dM[q][a,bb]
                  +sum(Gamma[a][q][j]*M[j,bb]-Gamma[j][q][bb]*M[a,j] for j in range(4)))
                   for q in range(4)))
    nablaA = s.Matrix(4,4,lambda a,bb: dA[bb][a]+sum(Gamma[a][bb][j]*A[j] for j in range(4)))
    E = s.Matrix(4,4,lambda a,bb: sum(R[a][j][bb][k]*U[j]*U[k] for j in range(4) for k in range(4)))
    residual = dotM-nablaA+M*M+E
    assert residual == s.zeros(4), (number,residual)
    assert (U.T*gm*U)[0] == -1
    wrong = dotM-nablaA+M*M-E
    nonzero = [(i,j,str(wrong[i,j])) for i in range(4) for j in range(4) if wrong[i,j] != 0]
    assert nonzero, 'curvature sign guard failed'
    rejected.append({'point':number,'reversed_tidal_sign_first_residual':nonzero[0]})
    all_results.append({'point':list(map(str,vals)), 'unit_observer':True,
                        'all_16_Ricci_identity_components_zero':True,
                        'nonzero_tidal_components':sum(v != 0 for v in E)})

print(json.dumps({'status':'PASS','sympy':s.__version__, 'exact_points':all_results,
                  'wrong_formula_rejections':rejected,
                  'scope':'3 supplied rational points verify implementation, not general theorem or physical admission'},indent=2))
