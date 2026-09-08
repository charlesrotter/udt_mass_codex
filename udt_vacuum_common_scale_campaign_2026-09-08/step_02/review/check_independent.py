"""Source-first VS2 fixtures: independent argument/fixtures, shared Ricci engine.

All geometry is exact symbolic; samples are not existence/classification proof.
Only the reviewed old geometry function is extracted, not its source-model checks.
"""
import ast
import hashlib
import json
from pathlib import Path
import platform
import sympy as S

root = Path(__file__).resolve().parents[3]
method = root / 'udt_source_metric_connection_campaign_2026-09-08/step_03/check_interface.py'
raw = method.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '8a34a9e57a2b5fab7f67586e6bff6398f76effe4b8f68407fa43f124ca40a416'
tree = ast.parse(raw)
func = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'geometry')
scope = {'S': S}
exec(compile(ast.Module(body=[func], type_ignores=[]), str(method), 'exec'), scope)
geometry = scope['geometry']
checks = []
values = {}

def check(name, condition, value=None):
    assert bool(condition), name
    checks.append(name)
    if value is not None:
        values[name] = str(value)

def zero(matrix):
    return all(S.simplify(a) == 0 for a in matrix)

def tf(ricci, scalar, metric):
    return S.simplify(ricci-scalar*metric/4)

s,v,x,y = S.symbols('s v x y', real=True)
coords = [s,v,x,y]
H = s*(x*x-y*y)  # Free example profile; no symmetry premise in the theorem.
g = S.Matrix([[H,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])
Gamma, Ric, R = geometry(g,coords)
check('original_wave_Ricci_zero',zero(Ric),Ric)
check('null_potential_parallel', all(Gamma[0][a][b] == 0 for a in range(4) for b in range(4)))
check('null_potential_nonzero_and_null',g.inv()[0,0] == 0 and S.diff(s,s) == 1)
u = 1+s  # Positive on s>-1; choose any smaller regular chart.
ghat = g/u**2
_, Richat, Rhat = geometry(ghat,coords)
check('original_nonconstant_wave_conformal_Ricci_zero',zero(Richat),Richat)

# Fresh Riemann differentiation from shared Christoffel output, not a stored
# Weyl formula. Rank at one event controls this tensor only, not neighborhoods.
Riem = [[[[S.simplify(S.diff(Gamma[d][c][b],coords[a])-S.diff(Gamma[d][a][b],coords[c])+
    sum(Gamma[d][a][e]*Gamma[e][c][b]-Gamma[d][c][e]*Gamma[e][a][b] for e in range(4)))
    for c in range(4)] for a in range(4)] for b in range(4)] for d in range(4)]
contraction = S.Matrix([[Riem[d][b][a][c] for d in range(4)]
                       for b in range(4) for a in range(4) for c in range(4)])
at_wave = contraction.subs({s:1,x:0,y:0})
check('nonzero_Weyl_null_line_rank3',at_wave.rank() == 3 and at_wave.nullspace() == [S.Matrix([1,0,0,0])],at_wave.nullspace())
check('pointwise_Weyl_all_zero_at_flat_event',zero(contraction.subs({s:0,x:0,y:0})))

bad_u = 1+s*s  # Positive but Hessian incompatible.
bad_g = g/bad_u**2
_, bad_Ric, bad_R = geometry(bad_g,coords)
bad_tf = tf(bad_Ric,bad_R,bad_g)
check('bad_null_profile_original_residual_rejected',S.simplify(bad_tf[0,0]-4/(1+s*s)) == 0 and not zero(bad_tf),bad_tf)

point_u = 1+x  # Positive near x=0. Algebraic condition at the origin passes.
point_g = g/point_u**2
_, point_Ric, point_R = geometry(point_g,coords)
point_tf = tf(point_Ric,point_R,point_g)
check('pointwise_only_false_pass_at_origin',zero(point_tf.subs({s:0,x:0,y:0})))
check('pointwise_only_original_residual_away_rejected',S.simplify(point_tf[0,0]-2*s*x/(1+x)) == 0 and point_tf[0,0].subs({s:1,x:1}) == 1,point_tf)

t,z = S.symbols('t z',real=True)
eta = S.diag(-1,1,1,1)
ads = eta/z**2  # z>0 local chart, Lambda=-3; method fixture only.
_, ads_Ric, ads_R = geometry(ads,[t,x,y,z])
check('nonzero_scalar_base_original_Ricci',zero(ads_Ric+3*ads))
ads_u = 1/z
_, flat_Ric, flat_R = geometry(S.simplify(ads/ads_u**2),[t,x,y,z])
check('nonzero_scalar_does_not_force_constant_factor',zero(flat_Ric) and S.diff(ads_u,z) != 0)

# Direct algebraic Einstein product control. R_abcd=K(g_ac g_bd-g_ad g_bc)
# on each2D factor; no unreviewed metric-development claim is made by this check.
sign = [-1,1,1,1]
def inner(a,b):
    return sign[a] if a == b else 0
def constant_piece(a,b,c,d):
    return inner(a,c)*inner(b,d)-inner(a,d)*inner(b,c)
W = {}
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                same = (all(j < 2 for j in [a,b,c,d]) or all(j >= 2 for j in [a,b,c,d]))
                W[a,b,c,d] = (1 if same else 0)*constant_piece(a,b,c,d)-S.Rational(1,3)*constant_piece(a,b,c,d)
product_map = S.Matrix([[W[a,b,c,d] for a in range(4)] for b in range(4) for c in range(4) for d in range(4)])
check('Einstein_product_Weyl_injective_rank4',product_map.rank() == 4,product_map.rank())
print(json.dumps({'kind':'exact source-first review fixtures; shared geometry utility; proof separate',
    'python':platform.python_version(),'sympy':S.__version__,'checks':checks,'values':values,
    'count':len(checks)},indent=2,sort_keys=True))
