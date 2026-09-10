"""Exact point-jet geometry; no repository imports or target-identity curvature.

Choices: supplied smooth local Lorentz metrics and unit U, signature (-,+,+,+).
Witness symmetries are mathematical examples, not physical restrictions. CPU exact
SymPy only; no approximation, grid, boundary, GPU, or field equations. Run under a
120-second subprocess timeout. Independent implementation written after candidate
and reported results exposure, before exposure to constructor implementation.
"""
import json
import sys
from itertools import product
import sympy as S

t, x, y, z = coords = S.symbols('t x y z', real=True)
nx, ny, nz = ns = S.symbols('nx ny nz', real=True)
p = dict.fromkeys(coords, S.Integer(0))
dim = range(4)
spatial = range(3)
eta = S.diag(-1, 1, 1, 1)
checks, records = [], []

def clean(v):
    return S.factor(S.simplify(v))

def zero(name, value):
    items = list(value) if isinstance(value, S.MatrixBase) else [value]
    reduced = [clean(v) for v in items]
    passed = all(v == 0 for v in reduced)
    checks.append({'name': name, 'passed': passed,
                   'residuals': [str(v) for v in reduced]})
    if not passed:
        raise AssertionError((name, reduced))

def nonzero(name, value):
    value = clean(value)
    checks.append({'name': name, 'passed': value != 0,
                   'deliberately_wrong_minus_direct': str(value)})
    if value == 0:
        raise AssertionError(name)

def at(v):
    return v.subs(p)

def geometry(name, g, U):
    # Differentiate the actual metric first; evaluate only its jets at p.
    # Inverse derivative is independently obtained from d(g^-1 g)=0.
    g0 = at(g)
    inv = g0.inv()
    g1 = [at(g.diff(c)) for c in coords]
    g2 = [[at(g.diff(c, d)) for d in coords] for c in coords]
    iv1 = [-inv * gg * inv for gg in g1]
    Gamma = [[[sum(inv[a, e] * (g1[b][e, c] + g1[c][e, b] -
                 g1[e][b, c]) / 2 for e in dim)
                 for c in dim] for b in dim] for a in dim]
    dGamma = [[[[sum((iv1[d][a, e] * (g1[b][e, c] +
                 g1[c][e, b] - g1[e][b, c]) + inv[a, e] *
                 (g2[d][b][e, c] + g2[d][c][e, b] -
                 g2[d][e][b, c])) / 2 for e in dim)
                 for c in dim] for b in dim] for a in dim] for d in dim]
    # Ric_bd = R^a_b a d, computed without expansion/shear/Raychaudhuri.
    Ric = S.Matrix(4, 4, lambda b, d: clean(sum(
        dGamma[a][a][d][b] - dGamma[d][a][a][b] + sum(
        Gamma[a][a][e]*Gamma[e][d][b] -
        Gamma[a][d][e]*Gamma[e][a][b] for e in dim) for a in dim)))
    U0 = at(U)
    U1 = [at(U.diff(c)) for c in coords]
    U2 = [[at(U.diff(c, d)) for d in coords] for c in coords]
    M = S.Matrix(4, 4, lambda a, b: U1[b][a] +
        sum(Gamma[a][b][c]*U0[c] for c in dim))
    dM = [S.Matrix(4, 4, lambda a, b: U2[d][b][a] + sum(
          dGamma[d][a][b][c]*U0[c] + Gamma[a][b][c]*U1[d][c]
          for c in dim)) for d in dim]
    accel = M*U0
    da = [dM[d]*U0 + M*U1[d] for d in dim]
    Ma = S.Matrix(4,4,lambda b,a: da[a][b] +
                  sum(Gamma[b][a][c]*accel[c] for c in dim))
    spatial_divergence = clean(S.trace((inv+U0*U0.T)*Ma.T*g0))
    A = clean(sum(da[a][a] + sum(Gamma[a][a][c]*accel[c]
                               for c in dim) for a in dim))
    theta = clean(S.trace(M))
    dot_theta = clean(sum(U0[d]*S.trace(dM[d]) for d in dim))
    ucov = g0*U0
    h = g0 + ucov*ucov.T
    proj = S.eye(4) + ucov*U0.T
    # D_ab = nabla_a U_b, covariant derivative index first.
    D = M.T*g0
    B = proj*D*proj.T
    vort = (B-B.T)/2
    shear = (B+B.T)/2 - theta*h/3
    norm = lambda T: clean(S.trace(inv*T*inv*T.T))
    W, sig2 = norm(vort), norm(shear)
    # All witnesses have the SAME coordinate orthonormal frame at p.
    zero(name+'_frame', g0-eta)
    zero(name+'_unit_field', (U.T*g*U)[0]+1)
    K = U0 + S.Matrix([0, nx, ny, nz])
    q = clean(-(K.T*D*K)[0])
    direct = clean((U0.T*Ric*U0)[0])
    m = -theta/3
    V = angular((q.subs(dict(zip(ns, [-nx,-ny,-nz])))+q)/2 - m,
                square=True)
    reconstructed = clean(A+W-dot_theta-theta**2/3-S.Rational(15,2)*V)
    zero(name+'_even_variance', V-S.Rational(2,15)*sig2)
    zero(name+'_formula', reconstructed-direct)
    row = dict(name=name, q=q, mean=m, dot_mean=-dot_theta/3,
               V=V, A=A, W=W, RicUU=direct, acceleration=list(accel),
               spatial_divergence=spatial_divergence)
    records.append({key: str(val) for key,val in row.items()})
    return row

def sphere_monomial(exponents):
    # Exact normalized sphere measure, implemented via beta/gamma integral;
    # separate from a tensor-moment table or constructor implementation.
    if any(v % 2 for v in exponents):
        return S.Integer(0)
    return clean(S.gamma(S.Rational(3,2)) * S.prod(
        S.gamma(S.Rational(v+1,2))/S.gamma(S.Rational(1,2))
        for v in exponents)/S.gamma(S.Rational(sum(exponents)+3,2)))

def angular(poly, square=False):
    pp = S.Poly(S.expand(poly**2 if square else poly), ns)
    return clean(sum(coef*sphere_monomial(power)
                     for power,coef in pp.terms()))

def frame_twist(b):
    # Noncoordinate Koszul implementation, separate from coordinate point jets.
    # Frame brackets [e1,e2]=-b e0 and metric diag(-1,+1,+1,+1).
    c = S.MutableDenseNDimArray.zeros(4,4,4)
    c[1,2,0], c[2,1,0] = -b, b
    signs = [-1,1,1,1]
    connection = S.MutableDenseNDimArray.zeros(4,4,4)
    for i,j,k in product(dim, repeat=3):
        connection[i,j,k] = clean((signs[k]*c[i,j,k] -
            signs[i]*c[j,k,i] + signs[j]*c[k,i,j])/(2*signs[k]))
    # R(e_i,e_j)e_k: coefficients constant in this frame.
    curv = lambda i,j,k,l: clean(sum(
        connection[j,k,m]*connection[i,m,l] -
        connection[i,k,m]*connection[j,m,l] -
        c[i,j,m]*connection[m,k,l] for m in dim))
    tidal = [curv(i,0,0,i) for i in range(1,4)]
    zero('Koszul_twist_tidal', S.Matrix(tidal)-S.Matrix([b*b/4,b*b/4,0]))
    return tidal

def main():
    beta,kappa,b,s,alpha,r = S.symbols('beta kappa b s alpha r', real=True)
    Ubase = S.Matrix([1,0,0,0])
    drift = geometry('missing_drift', S.diag(-1,*([S.exp(beta*t*t)]*3)), Ubase)
    zero('drift_q', drift['q'])
    zero('drift_target', drift['RicUU']+3*beta)
    N = 1+kappa*(x*x+y*y+z*z)/2
    lapse = geometry('missing_A', S.diag(-N*N,1,1,1), Ubase/N)
    zero('lapse_q', lapse['q'])
    zero('lapse_target', lapse['RicUU']-3*kappa)
    form = S.Matrix([1,-b*y/2,b*x/2,0])
    twist = geometry('missing_W', S.diag(0,1,1,1)-form*form.T, Ubase)
    zero('twist_q', twist['q'])
    zero('twist_target', twist['RicUU']-b*b/2)
    frame_twist(b)
    shear = geometry('missing_quadrupole',
                     S.diag(-1,S.exp(2*s*t),S.exp(-2*s*t),1), Ubase)
    zero('shear_q', shear['q']+s*(nx*nx-ny*ny))
    zero('shear_target', shear['RicUU']+2*s*s)
    N = 1+alpha*x
    flataccel = geometry('nonzero_acceleration', S.diag(-N*N,1,1,1), Ubase/N)
    zero('linear_lapse_Ricci', flataccel['RicUU'])
    zero('linear_lapse_divergence', flataccel['A'])
    # A mixed actual metric tests interactions hidden by the individual witnesses.
    N = 1+2*x+S.Rational(3,2)*(x*x+y*y+z*z)
    form = S.Matrix([1,-2*y,2*x,0])
    space = S.diag(0,S.exp(2*t+2*t*t),S.exp(4*t-2*t*t),S.exp(-2*t+3*t*t))
    mixed = geometry('mixed_kinematics', space-N*N*form*form.T, Ubase/N)
    # Failures of intentionally wrong reconstructions, evaluated on actual metrics.
    nonzero('omit_drift_rejected', (-3*drift['dot_mean']).subs(beta,1))
    nonzero('omit_A_rejected', (-lapse['A']).subs(kappa,1))
    nonzero('omit_W_rejected', (-twist['W']).subs(b,1))
    nonzero('half_W_rejected', (-twist['W']/2).subs(b,1))
    nonzero('omit_shear_rejected', (S.Rational(15,2)*shear['V']).subs(s,1))
    nonzero('reverse_curvature_sign_rejected', (2*twist['RicUU']).subs(b,1))
    nonzero('total_variance_rejected', (-S.Rational(15,2)*
            angular(flataccel['q'],square=True)).subs(alpha,1))
    nonzero('spatial_divergence_rejected',
            (flataccel['spatial_divergence']-flataccel['A']).subs(alpha,1))
    # Affine-rescaling check directly from omega -> r omega, lambda -> lambda/r.
    om, odm = S.symbols('omega d_omega', nonzero=True)
    zero('affine_scale_invariance', r*r*odm/(r*om)**2-odm/om**2)
    # Sphere moments independently anchored by elementary one-dimensional integrals.
    zz = S.symbols('zz', real=True)
    zero('sphere_second_integral', S.integrate(zz**2,(zz,-1,1))/2-sphere_monomial((0,0,2)))
    zero('sphere_fourth_integral', S.integrate(zz**4,(zz,-1,1))/2-sphere_monomial((0,0,4)))
    print(json.dumps({'status':'PASS','versions':{'python':sys.version.split()[0],
          'sympy':S.__version__},'checks':checks,'records':records,
          'implementation':'point metric jets and inverse derivative; no repository imports',
          'evidence':'exact symbolic witness checks plus separate Koszul frame calculation'},indent=2))

if __name__ == '__main__':
    main()
