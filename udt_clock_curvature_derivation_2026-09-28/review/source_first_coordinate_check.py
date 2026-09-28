#!/usr/bin/env python3
"""Reviewer-authored coordinate curvature check, before candidate exposure."""
import json
import platform
import sympy as s

t, x = s.symbols('t x', real=True)
coords = [t, x]
N, L, b = [s.Function(name)(t, x) for name in ['N', 'L', 'b']]
metric = s.Matrix([[-N**2, -N**2*b], [-N**2*b, L**2-N**2*b**2]])
inverse = metric.inv()
Gamma = [[[s.cancel(sum(inverse[a,d]*(s.diff(metric[d,c], coords[q])
    + s.diff(metric[d,q], coords[c])-s.diff(metric[q,c], coords[d]))
    for d in range(2))/2) for c in range(2)] for q in range(2)] for a in range(2)]
# R^a_{b c d}=d_c Gamma^a_{d b}-d_d Gamma^a_{c b}
#                 +Gamma^a_{c e} Gamma^e_{d b}-Gamma^a_{d e} Gamma^e_{c b}.
def curvature(a, q, c, d):
    return s.diff(Gamma[a][d][q], coords[c])-s.diff(Gamma[a][c][q], coords[d])+sum(
        Gamma[a][c][e]*Gamma[e][d][q]-Gamma[a][d][e]*Gamma[e][c][q] for e in range(2))
ricci = s.Matrix(2, 2, lambda q,d: s.cancel(sum(curvature(a,q,a,d) for a in range(2))))
scalar = s.cancel(sum(inverse[q,d]*ricci[q,d] for q in range(2) for d in range(2)))
D0 = lambda f: s.diff(f,t)/N
D1 = lambda f: (s.diff(f,x)-b*s.diff(f,t))/L
a = (s.diff(N,x)-s.diff(N*b,t))/(N*L)
H = s.diff(L,t)/(N*L)
frame_K = D0(H)+H**2-D1(a)-a**2
residual = s.cancel(scalar-2*frame_K)
assert residual == 0, residual
phi = -s.log(N)
measure_log = s.log(N)+s.log(L)
clock_acc = -D1(phi)-s.diff(b,t)/L
clock_expansion = D0(measure_log+phi)
assert s.cancel(a-clock_acc) == 0
assert s.cancel(H-clock_expansion) == 0
print(json.dumps({'python':platform.python_version(), 'sympy':s.__version__,
    'computation':'general two-variable coordinate Christoffel/Ricci/scalar',
    'shape':[2,2], 'arithmetic':'exact symbolic', 'residual_R_minus_2K':str(residual),
    'clock_acceleration_identity':True,'clock_expansion_identity':True,
    'candidate_exposure':False}, indent=2))
