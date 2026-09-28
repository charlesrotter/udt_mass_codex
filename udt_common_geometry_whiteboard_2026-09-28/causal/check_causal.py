"""Exact supplied-geometry controls. Physical choices are FREE, not adopted."""
import ast
import hashlib
import json
import platform
from pathlib import Path
import sympy as sp

root = Path(__file__).resolve().parents[2]
method = root / 'udt_observation_guided_function_search_2026-09-28/geometry/check_geometry.py'
method_hash = hashlib.sha256(method.read_bytes()).hexdigest()
pins = json.loads((Path(__file__).with_name('SOURCE_PINS.json')).read_text())
assert method_hash == pins['source_sha256'][str(method.relative_to(root))]
nodes = [n for n in ast.parse(method.read_text()).body
         if isinstance(n, ast.FunctionDef) and n.name == 'tensor_geometry']
assert len(nodes) == 1
namespace = {'sp': sp}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(method), 'exec'), namespace)
geometry = namespace['tensor_geometry']

checks, catches, values = {}, {}, {}
def check(name, expressions):
    residuals = [sp.factor(sp.simplify(v)) for v in expressions]
    if any(v != 0 for v in residuals):
        raise AssertionError(name + ': ' + str(residuals))
    checks[name] = 'EXACT_ZERO'

def reject(name, expressions):
    try:
        check(name, expressions)
    except AssertionError as error:
        catches[name] = str(error)
    else:
        raise AssertionError('FALSE_PASS: ' + name)

t,x,y,z = coords = sp.symbols('t x y z', real=True)
c = sp.symbols('c', real=True)
H = sp.symbols('H', positive=True)
eta = [-1,1,1,1]
u = 1+c*(-t*t+x*x+y*y+z*z)/2
diag = [v/u**2 for v in eta]
gam, riem, ric, scalar = geometry(diag, coords)
check('quadratic_original_Ricci', [ric[i,j]-6*c*(diag[i] if i==j else 0)
      for i in range(4) for j in range(4)])
check('quadratic_original_scalar', [scalar-24*c])
check('quadratic_original_constant_curvature', [
    riem.get((a,b,d,e),0)-2*c*((int(a==d)*diag[b] if b==e else 0)
                           -(int(a==e)*diag[b] if b==d else 0))
    for a in range(4) for b in range(4) for d in range(4) for e in range(4)])
R = sp.symbols('R', positive=True)
T = sp.symbols('T', real=True)
ue = sp.simplify(u.subs({t:T-R,x:R,y:0,z:0}))
uo = sp.simplify(u.subs({t:T,x:0,y:0,z:0}))
ratio = sp.simplify(ue/uo)
beam = R/ue
check('exact_received_clock_incidence', [ratio-(1+c*R*T/(1-c*T*T/2))])
check('single_cone_complete_readout', [ue.subs(T,0)-1, uo.subs(T,0)-1,
      ratio.subs(T,0)-1, beam.subs(T,0)-R])
check('proper_clock_redshift_drift_at_vertex', [(uo*sp.diff(ratio,T)).subs(T,0)-c*R])
check('proper_clock_beam_drift_at_vertex', [(uo*sp.diff(beam,T)).subs(T,0)+c*R**2])
check('all_epoch_clock_beam_product', [ratio*beam-R/uo])
check('vertex_clock_beam_drift_cancellation', [(uo*sp.diff(ratio*beam,T)).subs(T,0)])
reject('missing_proper_clock_conversion_at_nonzero_epoch',
       [sp.diff(ratio,T)-uo*sp.diff(ratio,T)])
values['quadratic_redshift_drift_general'] = str(sp.factor(uo*sp.diff(ratio,T)))

s = sp.symbols('s', nonnegative=True)
ray = {t:-s,x:s,y:0,z:0}
tangent = [-1,1,0,0]
check('quadratic_cone_factor', [u.subs(ray)-1])
check('quadratic_original_affine_null_geodesic', [
    sum(gam.get((i,j,k),0).subs(ray)*tangent[j]*tangent[k]
        if hasattr(gam.get((i,j,k),0),'subs') else 0
        for j in range(4) for k in range(4)) for i in range(4)])
check('quadratic_screen_original_tide', [
    sum(riem.get((a,b,d,e),0)*tangent[b]*tangent[d]*(int(e==q))
        for b in range(4) for d in range(4) for e in range(4))
    for a in (2,3) for q in (2,3)])

ua = 1-H*t
adiag = [v/ua**2 for v in eta]
ag, ar, ac, asc = geometry(adiag, coords)
check('affine_profile_original_Ricci', [ac[i,j]-3*H**2*(adiag[i] if i==j else 0)
      for i in range(4) for j in range(4)])
affine_parameter = s/(1+H*s)
check('affine_parameter_derivative', [sp.diff(affine_parameter,s)-(1+H*s)**-2])
check('affine_zero_tide_Jacobi', [
    (1+H*s)**2*sp.diff((1+H*s)**2*sp.diff(s/(1+H*s),s),s)])
check('proper_lookback_derivative', [sp.diff(sp.log(1+H*s)/H,s)-(1+H*s)**-1])
values['affine_extent_limit'] = str(sp.limit(affine_parameter,s,sp.oo))
values['proper_lookback_limit'] = str(sp.limit(sp.log(1+H*s)/H,s,sp.oo))

bad = sp.exp(-H*t)
bg, br, bc, bsc = geometry([v/bad**2 for v in eta],coords)
btf = bc-sp.diag(*[v/bad**2 for v in eta])*bsc/4
reject('arbitrary_positive_conformal_profile_is_Einstein', list(btf))
check('local_value_and_first_jet_agree', [(bad-ua).subs(t,0), sp.diff(bad-ua,t).subs(t,0)])
values['exponential_tracefree_Ricci'] = str(btf.applyfunc(sp.simplify))

a,b = sp.symbols('a b', real=True, nonzero=True)
f = s/(a*(a+b*s))
check('general_affine_parameter', [sp.diff(f,s)-(a+b*s)**-2])
check('general_zero_Schwarzian', [sp.diff(f,s,3)/sp.diff(f,s)
      -sp.Rational(3,2)*(sp.diff(f,s,2)/sp.diff(f,s))**2])
reject('nonaffine_null_scale', [sp.diff(a+b*s+c*s*s,s,2)])
we,wo,ueS,uoS,d = sp.symbols('we wo ue uo d', positive=True)
r = we/wo
rhat = ueS*we/(uoS*wo)
dhat = d/ueS
check('conformal_clock_beam_cancellation', [rhat*dhat-r*d/uoS])
reject('wrong_conformal_clock_weight', [rhat-r*uoS/ueS])
reject('dropped_endpoint_screen_factor', [rhat*d-r*d/uoS])

print(json.dumps({'kind':'AUTHOR_EXACT_SYMBOLIC_CHECKS_SHARED_GEOMETRY_UTILITY',
    'python':platform.python_version(),'sympy':sp.__version__,'checks':checks,
    'actual_hostile_rejections':catches,'values':values,
    'method_sha256':method_hash}, indent=2, sort_keys=True))
