"""GRC1 A4 exact identities; no physical premise adoption or sampled proof."""
import json
import platform
import sympy as s

checks = {}
outputs = {}


def connection(g, coords):
    inv = g.inv()
    n = len(coords)
    return [[[s.simplify(sum(inv[a, d] * (
        s.diff(g[d, c], coords[b]) + s.diff(g[d, b], coords[c])
        - s.diff(g[b, c], coords[d])) for d in range(n)) / 2)
        for c in range(n)] for b in range(n)] for a in range(n)]


def curvature(G, coords):
    # R[a][b][c][d] is (R(partial_c,partial_d)partial_b)^a.
    n = len(coords)
    return [[[[s.simplify(s.diff(G[a][d][b], coords[c])
        - s.diff(G[a][c][b], coords[d])
        + sum(G[a][c][j] * G[j][d][b] - G[a][d][j] * G[j][c][b]
              for j in range(n))) for d in range(n)]
        for c in range(n)] for b in range(n)] for a in range(n)]


def ricci(R):
    return s.Matrix(4, 4, lambda b, d: s.simplify(sum(R[a][b][a][d] for a in range(4))))


def iszero(expr):
    if isinstance(expr, s.MatrixBase):
        return all(s.simplify(v) == 0 for v in expr)
    return s.simplify(expr) == 0


# Generic positive radius and reduction of order, I'=1/r^2.
lam, le = s.symbols('lambda lambda_e', real=True)
re = s.symbols('r_e', positive=True)
rad = s.Function('r')(lam)
integ = s.Function('I')(lam)
D = re * rad * integ
formal = {s.diff(integ, lam, 2): -2*s.diff(rad, lam)/rad**3,
          s.diff(integ, lam): 1/rad**2}
checks['generic_jacobi_equation'] = iszero(
    (s.diff(D, lam, 2) - s.diff(rad, lam, 2)*D/rad).subs(formal))
checks['generic_vertex_normalization'] = iszero(
    s.diff(D, lam).subs(formal).subs({integ: 0, rad: re}) - 1)

H = s.symbols('H', positive=True)
Ds = s.sinh(H*(lam-le))/H
checks['sinh_jacobi_equation'] = iszero(s.diff(Ds, lam, 2)-H**2*Ds)
checks['sinh_vertex_data'] = iszero(Ds.subs(lam, le)) and iszero(s.diff(Ds, lam).subs(lam, le)-1)
checks['sinh_reciprocity'] = iszero(Ds + Ds.xreplace({lam: le, le: lam}))
rs = s.exp(H*lam)/H
checks['sinh_integral_representation'] = iszero(
    rs.subs(lam, le)*rs*(H/2)*(s.exp(-2*H*le)-s.exp(-2*H*lam))-Ds)

# Original four-dimensional spherical metric: q=exp(H*t).
t, r, th, ph = s.symbols('t r theta phi', real=True)
coords = [t, r, th, ph]
q = s.exp(H*t)
g = s.diag(-q, 1/q, r**2, r**2*s.sin(th)**2)
G = connection(g, coords)
R = curvature(G, coords)
Ric = ricci(R)
k = s.Matrix([1, q, 0, 0])
accel = s.Matrix([sum(k[b]*s.diff(k[a], coords[b]) for b in range(4))
    + sum(G[a][b][c]*k[b]*k[c] for b in range(4) for c in range(4)) for a in range(4)])
checks['spherical_ray_null'] = iszero((k.T*g*k)[0])
checks['spherical_ray_affine'] = iszero(accel)
rk = s.simplify((k.T*Ric*k)[0].subs(r, q/H))
checks['spherical_ray_null_ricci'] = iszero(rk+2*H**2)
outputs['spherical_ray_Ric_kk'] = str(rk)

# Independent direct coordinate expression for a time-dependent conformal factor.
eta, x, y, z = s.symbols('eta x y z', real=True)
psi = s.Function('psi', positive=True)(eta)
cc = [eta, x, y, z]
gc = s.diag(-1, 1, 1, 1)/psi**2
RC = curvature(connection(gc, cc), cc)
RicC = ricci(RC)
null = s.Matrix([1, 1, 0, 0])
cn = s.simplify((null.T*RicC*null)[0])
checks['conformal_null_ricci_identity'] = iszero(cn-2*s.diff(psi, eta, 2)/psi)
checks['conformal_spatial_isotropy'] = (
    iszero(RicC[1, 1]-RicC[2, 2]) and iszero(RicC[1, 1]-RicC[3, 3])
    and all(iszero(RicC[i, j]) for i in range(4) for j in range(4) if i != j))
checks['slab_negative_null_ricci'] = iszero(cn.subs(psi, s.cos(H*eta)).doit()+2*H**2)
outputs['conformal_Ric_kk'] = str(cn)

# Original cosmic-time flat FLRW metric, arbitrary positive a(t), then cosh.
a = s.Function('a', positive=True)(t)
cf = [t, x, y, z]
gf = s.diag(-1, a**2, a**2, a**2)
RF = curvature(connection(gf, cf), cf)
RicF = ricci(RF)
E = s.simplify(RF[1][0][1][0])  # g(e1,R(e1,e0)e0)
B = s.simplify(RF[1][2][1][2]/a**2)  # g(e1,R(e1,e2)e2)
checks['flrw_electric_curvature'] = iszero(E+s.diff(a, t, 2)/a)
checks['flrw_spatial_curvature'] = iszero(B-s.diff(a, t)**2/a**2)
# Isotropy and vanishing mixed blocks justify all-frame bivector formula.
checks['flrw_curvature_blocks'] = (
    all(iszero(RF[i][0][i][0]-E) for i in range(1, 4))
    and all(iszero(RF[i][j][i][j]/a**2-B) for i in range(1, 4) for j in range(1, 4) if i != j)
    and all(iszero(RF[i][0][j][k]) for i in range(1, 4) for j in range(1, 4) for k in range(1, 4)))
ab = s.cosh(H*t)
Eb, Bb = [s.simplify(v.subs(a, ab).doit()) for v in [E, B]]
scalar = s.simplify(sum(gf.inv()[i, j]*RicF[i, j] for i in range(4) for j in range(4)))
scalar_b = s.simplify(scalar.subs(a, ab).doit())
checks['cosh_scalar_curvature'] = iszero(scalar_b-6*H**2*(1+s.tanh(H*t)**2))
m2 = s.symbols('m_squared', nonnegative=True)
coef = s.simplify(-Eb*(1+m2)-Bb*m2)
checks['cosh_all_frame_coefficient'] = iszero(coef-H**2*(1+m2/s.cosh(H*t)**2))
outputs['cosh_C'] = str(coef)
outputs['cosh_scalar_R'] = str(scalar_b)
tc = s.log(s.sec(H*eta)+s.tan(H*eta))/H
checks['cosmic_time_derivative'] = iszero(s.diff(tc, eta)-s.sec(H*eta))
checks['slab_conformal_boundary_normal'] = iszero(s.diff(s.cos(H*eta), eta)**2+H**2*s.cos(H*eta)**2-H**2)

result = dict(python=platform.python_version(), sympy=s.__version__, checks=checks,
    passed=all(checks.values()), outputs=outputs,
    domains='r>0, spherical coordinate regular patch; H>0; positive C2 psi; slab |H eta|<pi/2; cosmic t in R',
    meaning='Exact grouped symbolic identities. Completeness, positive concavity, and all-frame quantifiers are analytic arguments, not sampled certification. Same author and SymPy as earlier checks; no independent-review claim.')
print(json.dumps(result, indent=2))
assert result['passed'], result
