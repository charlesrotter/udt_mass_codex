"""Exact supplied-metric controls for UNADOPTED conformal vacuum anchoring."""
import ast
import hashlib
import json
import platform
from functools import lru_cache
from pathlib import Path

import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
METHOD = ROOT / 'udt_source_metric_connection_campaign_2026-09-08/step_03/check_interface.py'
assert hashlib.sha256(METHOD.read_bytes()).hexdigest() == '8a34a9e57a2b5fab7f67586e6bff6398f76effe4b8f68407fa43f124ca40a416'
nodes = [node for node in ast.parse(METHOD.read_text()).body
         if isinstance(node, ast.FunctionDef) and node.name == 'geometry']
assert len(nodes) == 1
namespace = {'S': S}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(METHOD), 'exec'), namespace)
geometry = namespace['geometry']
checks = {}
values = {}

def simplify(expr):
    return S.simplify(S.expand_trig(expr))

def equal(name, actual, expected):
    residual = (S.Matrix(actual) - S.Matrix(expected)).applyfunc(simplify)
    assert residual == S.zeros(*residual.shape), (name, residual)
    checks[name] = 'EXACT_ZERO'

def reject(name, actual, expected):
    residual = (S.Matrix(actual) - S.Matrix(expected)).applyfunc(simplify)
    assert residual != S.zeros(*residual.shape), name
    checks[name] = 'NONZERO_REJECTED'
    values[name + '_residual'] = str(residual)

def full_geometry(metric, coords):
    connection, ric, scalar = geometry(metric, coords)
    inv = metric.inv()
    schouten = (ric - scalar*metric/6)/2

    @lru_cache(None)
    def riemann(a,b,c,d):
        return simplify(sum(metric[a,e]*(
            S.diff(connection[e][d][b], coords[c])
            - S.diff(connection[e][c][b], coords[d])
            + sum(connection[e][c][q]*connection[q][d][b]
                  - connection[e][d][q]*connection[q][c][b] for q in range(4)))
            for e in range(4)))

    @lru_cache(None)
    def weyl(a,b,c,d):
        return simplify(riemann(a,b,c,d) - metric[a,c]*schouten[b,d]
                        + metric[a,d]*schouten[b,c] + metric[b,c]*schouten[a,d]
                        - metric[b,d]*schouten[a,c])

    @lru_cache(None)
    def dP(direction,a,b):
        return simplify(S.diff(schouten[a,b],coords[direction])
             - sum(connection[q][direction][a]*schouten[q,b]
                   + connection[q][direction][b]*schouten[a,q] for q in range(4)))

    @lru_cache(None)
    def cotton(a,b,c):
        return simplify(dP(b,c,a)-dP(c,b,a))

    def anchor_schouten(du):
        norm = (S.Matrix(du).T*inv*S.Matrix(du))[0]
        return S.Matrix(4,4,lambda a,b: simplify(schouten[a,b]
            - S.diff(du[b],coords[a])
            + sum(connection[q][a][b]*du[q] for q in range(4))
            + du[a]*du[b]-norm*metric[a,b]/2))

    return dict(g=metric, inv=inv, connection=connection, ric=ric, scalar=scalar,
                P=schouten, W=weyl, A=cotton, Q=anchor_schouten)

t,r,theta,phi = coords = S.symbols('t r theta phi', real=True)
M,H,kappa = S.symbols('M H kappa', positive=True)
F = 1-2*M/r
base = S.diag(-F,1/F,r*r,r*r*S.sin(theta)**2)
physical = S.exp(2*H*t)*base
print('BEGIN conformal Schwarzschild original-metric differentiation', flush=True)
G = full_geometry(physical,coords)
equal('conformal_schwarzschild_scalar', [G['scalar']], [6*H**2*S.exp(-2*H*t)/F])
equal('full_anchor_schouten', G['Q']([-H,0,0,0]), S.zeros(4))
du_up = G['inv']*S.Matrix([-H,0,0,0])
cotton_residual = [simplify(G['A'](a,b,c) + sum(
    du_up[d]*G['W'](d,a,b,c) for d in range(4)))
    for a in range(4) for b in range(4) for c in range(4)]
equal('all_64_cotton_weyl_rows', cotton_residual, [0]*64)

# The inverse operation below receives g-derived A,W only, not the known du.
point = {t:0,r:5,theta:S.pi/2,M:1,H:S.Rational(1,10)}
rows = [(a,b,c) for a in range(4) for b in range(4) for c in range(4)]
matrix = S.Matrix([[simplify(sum(G['inv'][d,e]*G['W'](d,a,b,c)
    for d in range(4))).subs(point) for e in range(4)] for a,b,c in rows])
rhs = S.Matrix([-G['A'](a,b,c).subs(point) for a,b,c in rows])
solution, parameters = matrix.gauss_jordan_solve(rhs)
assert matrix.rank()==4 and parameters.rows==0
equal('inverse_reconstruction_at_exact_point', solution, [-S.Rational(1,10),0,0,0])
equal('inverse_reconstruction_all_rows', matrix*solution, rhs)
values['inverse_matrix_shape'] = list(matrix.shape)
values['inverse_rank'] = matrix.rank()
values['inverse_solution_covector'] = [str(q) for q in solution]
values['conformal_schwarzschild_Ricci'] = str(G['ric'])
values['conformal_schwarzschild_scalar'] = str(G['scalar'])
values['conformal_schwarzschild_Cotton_rtr'] = str(G['A'](1,0,1))
values['conformal_schwarzschild_W_trtr'] = str(G['W'](0,1,0,1))
print('PASS conformal Schwarzschild and inverse reconstruction', flush=True)

FK = 1-2*M/r-kappa*r*r
GK = full_geometry(S.diag(-FK,1/FK,r*r,r*r*S.sin(theta)**2),coords)
equal('kottler_original_ricci', GK['ric'], 3*kappa*GK['g'])
equal('kottler_cotton_zero', [GK['A'](*row) for row in rows], [0]*64)
equal('kottler_mass_weyl_component', [GK['W'](0,1,0,1)], [-2*M/r**3])
reject('kottler_constant_anchor_fails_full_equation', GK['Q']([0,0,0,0]), S.zeros(4))
values['kottler_scalar'] = str(GK['scalar'])
print('PASS Kottler obstruction control', flush=True)

x,y,z = S.symbols('x y z', real=True)
b = S.symbols('b', positive=True)
flat_coords = (t,x,y,z)
eta = S.diag(-1,1,1,1)
null_denominator = 1+b*(t+x)
_, ric_null, scalar_null = geometry(eta/null_denominator**2,flat_coords)
equal('flat_nonconstant_null_anchor', ric_null, S.zeros(4))
_, ric_time, scalar_time = geometry(eta/(1+b*t)**2,flat_coords)
reject('timelike_denominator_wrong_vacuum_rejected', ric_time, S.zeros(4))
equal('timelike_denominator_actual_Einstein', ric_time, 3*b*b*eta/(1+b*t)**2)
values['flat_distinct_anchor_origin_normalization'] = str(null_denominator.subs({t:0,x:0}))
values['timelike_denominator_scalar'] = str(scalar_time)
print('PASS degeneracy and gradient-norm catch', flush=True)

sources = [Path(__file__), HERE/'CHECK_PLAN.md', HERE/'INITIAL_PROPOSAL.md', METHOD,
    ROOT/'udt_clock_optical_physical_connection_2026-10-13/REPAIR.md',
    ROOT/'udt_vacuum_common_scale_campaign_2026-09-08/step_01/REVIEWED_RESULT.md',
    ROOT/'udt_vacuum_common_scale_campaign_2026-09-08/step_02/REVIEWED_RESULT.md']
out = {'status':'PASS','scope':'Exact named controls; UNADOPTED CVA; no native-selection claim',
       'versions':{'python':platform.python_version(),'sympy':S.__version__},
       'shared_implementation':'AST-only reviewed coordinate geometry function; author regression, not independent implementation',
       'checks':checks,'values':values,
       'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
with (HERE/'CVA_CHECK_RESULT.json').open('x') as output:
    json.dump(out,output,indent=2);output.write('\n')
print(json.dumps(out,indent=2),flush=True)
