#!/usr/bin/env python3
"""Exact author diagnostics. The analytical argument owns continuum claims.

Reuse NCI1's existing coordinate-geometry definitions without running its top-level
campaign. This is author regression, not a fresh review or full source replay.
"""
import ast
import hashlib
import json
from pathlib import Path
import platform
import sympy as s

if not __debug__:
    raise RuntimeError('Evidence checks require assertions enabled')

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
utility = ROOT / 'udt_null_clock_depth_integrability_assessment_2026-09-10/check_integrability.py'
tree = ast.parse(utility.read_text())
nodes = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))
         or isinstance(node, ast.FunctionDef) and node.name in ('simp', 'geometry')]
namespace = {'__file__': str(utility)}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(utility), 'exec'), namespace)
geometry = namespace['geometry']

checks = []
metrics = []


def simp(v):
    return s.simplify(s.expand(v))


def same(name, actual, expected):
    difference = actual - expected
    values = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
    residuals = [simp(v) for v in values]
    if any(v != 0 for v in residuals):
        raise AssertionError((name, residuals))
    checks.append({'name': name, 'type': 'exact identity', 'passed': True})


def catch(name, wrong, direct):
    residual = simp(wrong-direct)
    if residual == 0:
        raise AssertionError(('mutation was not caught', name))
    checks.append({'name': name, 'type': 'wrong formula rejected',
                   'passed': True, 'wrong_minus_direct': str(residual)})


n = s.symbols('nx ny nz', real=True)


def mean(poly):
    """Exact uniform S2 monomial moments; only low-degree polynomials used."""
    ans = s.S.Zero
    for powers, coefficient in s.Poly(s.expand(poly), *n).terms():
        if any(v % 2 for v in powers):
            continue
        numerator = s.prod(s.factorial2(v-1) for v in powers)
        ans += coefficient * numerator / s.factorial2(sum(powers)+1)
    return simp(ans)


def records(q):
    m = mean(q)
    even = (q+q.xreplace({v: -v for v in n}))/2
    return m, mean((even-m)**2)


def prediction(m, drift, variance, acceleration_divergence, vorticity_norm):
    return simp(3*drift-3*m*m-s.Rational(15, 2)*variance
                +acceleration_divergence+vorticity_norm)


def direct(g, u, coords):
    d = geometry(g, u, coords)
    G, gi, nab = d['G'], d['gi'], d['nab']
    ric = s.Matrix(4, 4, lambda b, c: simp(sum(
        s.diff(G[a][b][c], coords[a])-s.diff(G[a][b][a], coords[c])
        +sum(G[a][a][e]*G[e][b][c]-G[a][c][e]*G[e][b][a]
             for e in range(4)) for a in range(4))))
    aup = (gi*d['a']).applyfunc(simp)
    divergence = simp(sum(s.diff(aup[a], coords[a])
                         +sum(G[a][a][b]*aup[b] for b in range(4))
                         for a in range(4)))
    projector = s.eye(4)+d['ul']*u.T
    w = (projector*((nab-nab.T)/2)*projector.T).applyfunc(simp)
    norm = lambda mat: simp(s.trace(gi*mat*gi*mat.T))
    d.update({'Ric': ric, 'RicUU': simp((u.T*ric*u)[0]),
              'A': divergence, 'W': norm(w), 'w': w,
              'sigma2': norm(d['sigma']),
              'dotH': simp(sum(u[i]*s.diff(d['H'], coords[i]) for i in range(4)))})
    same('unit_'+str(len(metrics)), (u.T*g*u)[0], -1)
    same('coordinate_Raychaudhuri_'+str(len(metrics)), d['RicUU'],
         -3*d['dotH']-3*d['H']**2-d['sigma2']+d['A']+d['W'])
    return d


# Arbitrary expansion, acceleration and five independent shear entries.
H = s.symbols('H', real=True)
a = s.Matrix(s.symbols('a1:4', real=True))
x1, x2, x3, x4, x5 = s.symbols('s1:6', real=True)
sigma = s.Matrix([[x1,x3,x4],[x3,x2,x5],[x4,x5,-x1-x2]])
nv = s.Matrix(n)
q = -H-(a.T*nv)[0]-(nv.T*sigma*nv)[0]
m, variance = records(q)
same('angular_mean', m, -H)
same('acceleration_dipole', s.Matrix([-3*mean(q*v) for v in n]), a)
quadrupole = s.Matrix(3,3,lambda i,j: -s.Rational(15,2)*mean(
    q*(n[i]*n[j]-(s.Rational(1,3) if i==j else 0))))
same('full_shear_quadrupole', quadrupole, sigma)
same('even_variance', s.Rational(15,2)*variance, s.trace(sigma*sigma))

# Independently integrate representative sphere moments in ordinary polar variables.
zeta, angle = s.symbols('zeta angle', real=True)
polar_x = s.sqrt(1-zeta*zeta)*s.cos(angle)
for label, integrand, expected in [('x2',polar_x**2,s.Rational(1,3)),
                                 ('x4',polar_x**4,s.Rational(1,5)),
                                 ('x2z2',polar_x**2*zeta**2,s.Rational(1,15))]:
    value = s.integrate(s.integrate(integrand,(angle,0,2*s.pi)),(zeta,-1,1))/(4*s.pi)
    same('polar_moment_'+label,value,expected)

# Pointwise contracted derivative product with arbitrary antisymmetric spatial part.
w1,w2,w3 = s.symbols('w1:4', real=True)
w = s.Matrix([[0,w1,w2],[-w1,0,w3],[-w2,-w3,0]])
K = H*s.eye(3)+sigma+w
same('derivative_square_sign',s.trace(K*K),3*H*H+s.trace(sigma*sigma)-s.trace(w*w.T))

t,x,y,z = coords = s.symbols('t x y z', real=True)
u = s.Matrix([1,0,0,0])
null_at_origin = s.Matrix([1,*n])
origin = {t:0,x:0,y:0,z:0}
beta,kappa,b,alpha = s.symbols('beta kappa b alpha', real=True)

# General positive diagonal homogeneous metric: direct Ricci, not preassigned response.
hs = s.symbols('h1:4', real=True)
js = s.symbols('j1:4', real=True)
g = s.diag(-1,*[s.exp(2*hh*t+jj*t*t) for hh,jj in zip(hs,js)])
d = direct(g,u,coords)
q0 = simp(-(null_at_origin.T*d['nab'].subs(origin)*null_at_origin)[0])
m0,v0 = records(q0)
drift = -d['dotH'].subs(origin)
R0 = d['RicUU'].subs(origin)
same('general_diagonal_clock_prediction',prediction(m0,drift,v0,0,0),R0)
same('general_diagonal_direct_Ricci',R0,-sum(jj+hh*hh for hh,jj in zip(hs,js)))
metrics.append({'name':'general_diagonal', 'q_at_origin':str(q0),
                'mean':str(m0),'variance':str(v0),'drift':str(drift),'direct_RicUU':str(R0)})
isotropic0 = {**dict.fromkeys(hs,0), **dict.fromkeys(js,beta)}
same('drift_witness_instantaneous_q',q0.subs(isotropic0),0)
same('drift_witness_RicUU',R0.subs(isotropic0),-3*beta)
catch('omit_temporal_mean_drift',0,R0.subs(isotropic0).subs(beta,1))
anisotropic = {hs[0]:1,hs[1]:-1,hs[2]:0,**dict.fromkeys(js,0)}
same('shear_witness_mean',m0.subs(anisotropic),0)
same('shear_witness_variance',v0.subs(anisotropic),s.Rational(4,15))
catch('omit_even_quadrupole',0,R0.subs(anisotropic))
catch('wrong_shear_factor_15_instead_of_15_over_2',-15*v0.subs(anisotropic),R0.subs(anisotropic))
expansion = {**dict.fromkeys(hs,1),**dict.fromkeys(js,0)}
catch('omit_mean_square',0,R0.subs(expansion))

# Central stationary clock records miss transverse acceleration divergence.
N=1+kappa*(x*x+y*y+z*z)/2
g=s.diag(-N*N,1,1,1)
d=direct(g,s.Matrix([1/N,0,0,0]),coords)
q0=simp(-(null_at_origin.T*d['nab'].subs(origin)*null_at_origin)[0])
same('static_central_q',q0,0)
same('static_central_acceleration',d['a'].subs(origin),s.zeros(4,1))
same('static_central_A',d['A'].subs(origin),3*kappa)
same('static_central_W',d['W'].subs(origin),0)
same('static_central_RicUU',d['RicUU'].subs(origin),3*kappa)
same('static_time_constancy',s.diff(q0,t),0)
catch('omit_acceleration_divergence',0,d['RicUU'].subs(origin).subs(kappa,1))
metrics.append({'name':'static_lapse','q_at_central_worldline':str(q0),
                'A_at_origin':str(d['A'].subs(origin)),'W':str(d['W']),
                'direct_RicUU_at_origin':str(d['RicUU'].subs(origin))})

# Unit-Killing twist: nonzero RicUU with zero scalar clock slopes throughout.
B=s.Matrix([1,-b*y/2,b*x/2,0])
g=s.diag(0,1,1,1)-B*B.T
d=direct(g,u,coords)
same('twist_det',g.det(),-1)
same('twist_symmetric_derivative',d['nab']+d['nab'].T,s.zeros(4))
same('twist_acceleration',d['a'],s.zeros(4,1))
same('twist_A',d['A'],0)
same('twist_W',d['W'],b*b/2)
same('twist_RicUU',d['RicUU'],b*b/2)
catch('omit_vorticity',0,d['RicUU'].subs(b,1))
catch('wrong_vorticity_half_norm',d['W'].subs(b,1)/2,d['RicUU'].subs(b,1))
metrics.append({'name':'unit_Killing_twist','A':str(d['A']),'W':str(d['W']),
                'direct_RicUU':str(d['RicUU']),'symmetric_derivative_zero':True})

# Acceleration dipole must not contaminate the even quadrupole or divergence type.
N=1+alpha*x
g=s.diag(-N*N,1,1,1)
d=direct(g,s.Matrix([1/N,0,0,0]),coords)
q0=simp(-(null_at_origin.T*d['nab'].subs(origin)*null_at_origin)[0])
m0,v0=records(q0)
same('linear_lapse_q',q0,-alpha*n[0])
same('linear_lapse_even_variance',v0,0)
same('linear_lapse_full_divergence',d['A'],0)
same('linear_lapse_Ricci',d['Ric'],s.zeros(4))
full_variance=mean((q0-m0)**2)
catch('use_total_variance_instead_of_even_variance',-s.Rational(15,2)*full_variance.subs(alpha,1),0)
spatial_divergence=s.diff(alpha/N,x)
catch('replace_four_divergence_by_spatial_divergence',spatial_divergence.subs(origin).subs(alpha,1),0)
metrics.append({'name':'linear_lapse_acceleration_control','q_at_origin':str(q0),
                'full_variance':str(full_variance),'even_variance':str(v0),
                'A':str(d['A']),'direct_RicUU':str(d['RicUU'])})

print(json.dumps({'status':'PASS','evidence_type':'author exact symbolic diagnostics; not independent review',
                  'checks':checks,'check_count':len(checks),'metric_records':metrics,
                  'versions':{'python':platform.python_version(),'sympy':s.__version__},
                  'reused_utility':{'path':str(utility.relative_to(ROOT)),
                                    'sha256':hashlib.sha256(utility.read_bytes()).hexdigest(),
                                    'functions':['simp','geometry'],'top_level_executed':False},
                  'candidate_sha256':hashlib.sha256((HERE/'INITIAL_CANDIDATE.md').read_bytes()).hexdigest(),
                  'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'omissions':['physical measurements','full field-equation or source replay',
                               'finite noisy sampling','global structure','novel-mathematics claim']},indent=2))
