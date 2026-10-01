"""Independent bounded algebra checks; no producer imports or physical selector."""
import json
import platform
import sympy as s

records = []

def check(name, residual):
    value = s.simplify(s.trigsimp(residual))
    if value != 0:
        raise AssertionError((name, value))
    records.append({"name": name, "residual": str(value)})

K,L,q,r = s.symbols('K L q r', positive=True)
kappa = s.symbols('kappa', real=True)
pplus = 1/s.cos(s.sqrt(K)*L)
pminus = 1/s.cosh(s.sqrt(K)*L)
check('positive_curvature_sensitivity', s.diff(s.log(pplus),K)-L*s.tan(s.sqrt(K)*L)/(2*s.sqrt(K)))
check('negative_curvature_sensitivity', -s.diff(s.log(pminus),K)-L*s.tanh(s.sqrt(K)*L)/(2*s.sqrt(K)))
check('positive_flat_sensitivity', s.limit(s.diff(s.log(pplus),K),K,0,dir='+')-L**2/2)
check('negative_flat_sensitivity', s.limit(-s.diff(s.log(pminus),K),K,0,dir='+')-L**2/2)
check('positive_fourth_order', s.series(s.log(pplus),L,0,5).removeO()-K*L**2/2-K**2*L**4/12)
check('negative_fourth_order', s.series(s.log(pminus),L,0,5).removeO()+K*L**2/2-K**2*L**4/12)
f=1-kappa*r**2
Ap=(r**2*s.diff(f,r,2)-r*s.diff(f,r))/2
At=1-f+r*s.diff(f,r)/2
E0=r*s.diff(f,r)+f-1
E1=r*s.diff(f,r)+r**2*s.diff(f,r,2)/2
check('full_primary_angular_parallel',Ap)
check('full_primary_angular_perp',At)
check('full_primary_vacuum_time',E0+3*kappa*r**2)
check('full_primary_vacuum_angle',E1+3*kappa*r**2)
check('angular_identity',Ap+At-E1+E0)
a,b,v=s.symbols('a b v', real=True)
eta=s.diag(-1,1,1,1)
B=s.eye(4)
B[0,0]=B[1,1]=s.cosh(v)
B[0,1]=B[1,0]=s.sinh(v)
E=s.diag(a,b,b,b)
check('boost_is_lorentz',sum((B.T*eta*B-eta).applyfunc(s.simplify)))
check('boost_tensor_cross',(B.T*E*B)[0,1]-(a+b)*s.cosh(v)*s.sinh(v))
check('isotropic_tensor_metric',sum((E.subs(a,-b)-b*eta)))
for j in range(4):
    for k in range(4):
        check(f'pure_trace_boost_{j}{k}',(B.T*(b*eta)*B-b*eta)[j,k])
ell=s.symbols('ell', positive=True)
check('signed_dimensionless_scale',(kappa/ell**2)*(ell*L)**2-kappa*L**2)
# Exact wrong-formula catches, not evidence of broad semantic coverage.
wrong_angular_vacuum = s.simplify(E0.subs({kappa:1,r:s.Rational(1,2)}))
if wrong_angular_vacuum == 0:
    raise AssertionError('missed_angular_vacuum_false_pass')
wrong_natural=s.simplify((B.T*E*B-E)[0,1].subs({a:1,b:1,v:s.log(2)}))
if wrong_natural == 0:
    raise AssertionError('missed_rotation_only_false_pass')
print(json.dumps({"status":"PASS","checks":records,
  "negative_controls":{"angular_zero_not_vacuum":str(wrong_angular_vacuum),
                       "rotation_only_not_lorentz_invariant":str(wrong_natural)},
  "python":platform.python_version(),"sympy":s.__version__,
  "scope":"Exact bounded identities; analytic domain/monotonicity proof in SOURCE_FIRST.md. No physical selector."},indent=2))
