#!/usr/bin/env python3
"""Author exact checks, from original coordinates; no UDT field-law adoption."""
import json
import sys
import sympy as s

checks = []
rejections = []


def normal(expr):
    value = s.simplify(s.together(expr))
    if value != 0 and value.has(s.sinh, s.cosh, s.tanh, s.sin, s.cos):
        value = s.simplify(s.together(value.rewrite(s.exp)))
    return value


def zero(name, expr):
    value = normal(expr)
    if value != 0:
        raise AssertionError((name, value))
    checks.append(name)


def reject(name, expr):
    value = normal(expr)
    if value == 0 or value.free_symbols:
        raise AssertionError((name, 'wrong formula not rejected exactly', value))
    rejections.append({'name': name, 'nonzero_residual': str(value)})


def geometry(g, coords):
    dim = len(coords)
    inv = g.inv()
    G = [[[s.simplify(sum(inv[a, d]*(s.diff(g[d, c], coords[b])
                    + s.diff(g[d, b], coords[c])-s.diff(g[b, c], coords[d]))
                    for d in range(dim))/2)
           for c in range(dim)] for b in range(dim)] for a in range(dim)]
    R = [[[[s.simplify(s.diff(G[a][d][b], coords[c])
                    - s.diff(G[a][c][b], coords[d])
                    + sum(G[a][c][e]*G[e][d][b]-G[a][d][e]*G[e][c][b]
                          for e in range(dim)))
            for d in range(dim)] for c in range(dim)]
          for b in range(dim)] for a in range(dim)]
    return G, R


t, x = s.symbols('t x', real=True)
N, L, b = [s.Function(n)(t, x) for n in ('N', 'L', 'b')]
g = s.Matrix([[-N*N, -N*N*b], [-N*N*b, L*L-N*N*b*b]])
G, R = geometry(g, (t, x))
u = s.Matrix([1/N, 0])
n = s.Matrix([-b/L, 1/L])
D0 = lambda f: s.diff(f, t)/N
D1 = lambda f: (s.diff(f, x)-b*s.diff(f, t))/L
a = (s.diff(N, x)-s.diff(N*b, t))/(N*L)
H = s.diff(L, t)/(N*L)
tide = s.simplify(sum(g[0, i]*R[i][1][0][1] for i in range(2))/(N*N*L*L))
frame_tide = D1(a)+a*a-D0(H)-H*H
zero('generic_shifted_curvature_from_coordinate_Riemann', tide-frame_tide)
zero('orthonormal_u', (u.T*g*u)[0]+1)
zero('orthonormal_n', (n.T*g*n)[0]-1)
zero('orthogonal_frame', (u.T*g*n)[0])
zero('reciprocal_density', -g.det()-(N*L)**2)


def covariant(V, W):
    return s.Matrix([sum(V[j]*s.diff(W[i], (t, x)[j]) for j in range(2))
         + sum(G[i][j][k]*V[j]*W[k] for j in range(2) for k in range(2))
         for i in range(2)])


for i, v in enumerate(covariant(u, u)-a*n):
    zero('observer_acceleration_'+str(i), v)
for i, v in enumerate(covariant(n, u)-H*n):
    zero('spatial_observer_deformation_'+str(i), v)
for eps in (-1, 1):
    ell = u+eps*n
    zero('null_'+str(eps), (ell.T*g*ell)[0])
    for i, v in enumerate(covariant(ell, ell)-(H+eps*a)*ell):
        zero('null_nonaffinity_'+str(eps)+'_'+str(i), v)

Bp, Bm = H+a, H-a
zero('cross_null_clock_curvature', D0(Bp)-D1(Bp)+D0(Bm)+D1(Bm)+2*Bp*Bm+2*tide)
phi, M = -s.log(N), s.log(N*L)
q = s.diff(b, t)/L
zero('calibrated_acceleration', a+D1(phi)+q)
zero('calibrated_expansion', H-D0(phi+M))
zero('full_calibrated_scalar_identity',
     D0(D0(phi+M))+D0(phi+M)**2+D1(D1(phi))+D1(q)
     -(D1(phi)+q)**2+tide)

# Distinct restricted original metric, with an integrable ruler coordinate.
F = s.Function('F', positive=True)(t, x)
gf = s.diag(-1/F, F)
_, Rf = geometry(gf, (t, x))
tf = s.simplify(sum(gf[0, i]*Rf[i][1][0][1] for i in range(2)))
zero('reciprocal_restricted_PDE', s.diff(F, t, 2)-s.diff(1/F, x, 2)+2*tf)
zero('principal_Ftt', s.diff(-2*tf, s.diff(F, t, 2))-1)
zero('principal_Fxx_positive', s.diff(-2*tf, s.diff(F, x, 2))-1/F**2)
f0, k = s.symbols('f0 k', positive=True)
mode = s.cosh(k*t/f0)*s.cos(k*x)
zero('elliptic_linearized_mode', s.diff(mode, t, 2)+s.diff(mode, x, 2)/f0**2)

# A complete nonflat induced surface inside a flat ambient space:
# X=(sinh t, cosh t cos x, cosh t sin x,0). Unit-radius choice is FREE control.
X = s.Matrix([s.sinh(t), s.cosh(t)*s.cos(x), s.cosh(t)*s.sin(x), 0])
eta = s.diag(-1, 1, 1, 1)
Xt, Xx = X.diff(t), X.diff(x)
hs = s.simplify(s.Matrix([[v.dot(eta*w) for w in (Xt, Xx)] for v in (Xt, Xx)]))
zero('embedding_metric_tt', hs[0, 0]+1)
zero('embedding_metric_tx', hs[0, 1])
zero('embedding_metric_xx', hs[1, 1]-s.cosh(t)**2)
zero('embedding_normal_unit', (X.T*eta*X)[0]-1)
_, Rs = geometry(hs, (t, x))
ts = s.simplify(sum(hs[0, i]*Rs[i][1][0][1] for i in range(2))/s.cosh(t)**2)
II00 = s.simplify((X.T*eta*X.diff(t, 2))[0])
II01 = s.simplify((X.T*eta*X.diff(t, x))[0]/s.cosh(t))
II11 = s.simplify((X.T*eta*X.diff(x, 2))[0]/s.cosh(t)**2)
zero('Gauss_with_nonzero_extrinsic_term', ts-(II00*II11-II01**2))
for eps in (-1, 1):
    zero('embedding_both_null_normal_accelerations_'+str(eps), II00+2*eps*II01+II11)
zero('embedding_induced_tide_minus_one', ts+1)

# Wrong-formula controls, evaluated rather than accepted by named constants.
shift_sub = {N: s.Integer(1), L: s.Integer(1), b: t}
actual_shift = tide.subs(shift_sub).doit()
wrong_a = (s.diff(N, x)-b*s.diff(N, t))/(N*L)
wrong_shift = (D1(wrong_a)+wrong_a**2-D0(H)-H**2).subs(shift_sub).doit()
reject('omit_time_derivative_of_shift', actual_shift-wrong_shift)
ruler_sub = {N: s.Integer(1), L: s.exp(t), b: s.Integer(0)}
actual_ruler = tide.subs(ruler_sub).doit()
wrong_H = D0(phi)  # wrong replacement ln L -> phi, discarding ln m
wrong_ruler = (D1(a)+a*a-D0(wrong_H)-wrong_H**2).subs(ruler_sub).doit()
reject('omit_time_dependent_ruler_calibration', actual_ruler-wrong_ruler)
reject('reverse_curvature_sign', actual_shift+frame_tide.subs(shift_sub).doit())
reject('equate_induced_to_flat_ambient_tide', ts)
wrong_wave = s.diff(mode, t, 2)-s.diff(mode, x, 2)/f0**2
reject('insert_hyperbolic_spatial_sign', wrong_wave.subs({t:0, x:0, f0:1, k:1}))

print(json.dumps({'status':'PASS', 'python':sys.version, 'sympy':s.__version__,
    'exact_check_count':len(checks), 'checks':checks,
    'wrong_formula_rejections':rejections,
    'principal_symbol':'xi_t^2 + F^-2 xi_x^2 (F>0)',
    'scope':'Generic local shifted two-metric identities; labeled controls; no field-law selection'}, indent=2))
