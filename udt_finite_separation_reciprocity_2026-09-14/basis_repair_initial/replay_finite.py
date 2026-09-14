"""Small exact source-formula diagnostics, not physical-admission tests."""
from pathlib import Path
import datetime, hashlib, json, platform, sys
import sympy as s

eta=s.diag(-1,1,1,1)
zero=lambda x: all(s.simplify(y)==0 for y in x)
def require_zero(x):
    assert zero(x), x
def boost(p):
    p=s.Matrix(p); t=(p.T*p)[0]
    assert t<1
    gamma=(1+t)/(1-t); spatial=2*p/(1-t)
    b=s.eye(4); b[0,0]=gamma
    b[0,1:4]=spatial.T; b[1:4,0]=spatial
    b[1:4,1:4]=s.eye(3)+spatial*spatial.T/(gamma+1)
    return b,spatial/gamma
def project(m):
    return m[1:4,0]/m[0,0]
def values(v):
    return [str(x) for x in v]

a=s.symbols('a',positive=True)
d=s.diag(1/a,a); k=s.Matrix([[0,1],[1,0]]); eta2=s.diag(-1,1)
require_zero(d.T*k*d-k)
squeeze_eta_defect=s.simplify(d.T*eta2*d-eta2)
assert not zero(squeeze_eta_defect)
require_zero(squeeze_eta_defect.subs(a,1))
delta=s.symbols('delta',real=True)
de=s.diag(s.exp(-delta),s.exp(delta))
require_zero(s.diff(de.T*eta2*de,delta).subs(delta,0)-2*s.eye(2))

rz=s.Matrix([[s.Rational(3,5),-s.Rational(4,5),0],
             [s.Rational(4,5),s.Rational(3,5),0],[0,0,1]])
rx=s.Matrix([[1,0,0],[0,s.Rational(5,13),-s.Rational(12,13)],
             [0,s.Rational(12,13),s.Rational(5,13)]])
r=rz*rx; require_zero(r.T*r-s.eye(3)); assert r.det()==1
cases=[]; arrows=[]
for label,p,rotation in [
    ('all_three_components_with_carry',[s.Rational(1,5),s.Rational(1,7),s.Rational(1,9)],r),
    ('zero_vector_with_carry',[0,0,0],r),
    ('radial_without_carry',[s.Rational(1,3),0,0],s.eye(3)),
]:
    b,v=boost(p); rr=s.eye(4);rr[1:4,1:4]=rotation
    arrow=b*rr; inverse=arrow.inv()
    require_zero(arrow.T*eta*arrow-eta)
    assert arrow.det()==1 and arrow[0,0]>0
    require_zero(project(arrow)-v)
    require_zero(project(inverse)+rotation.T*v)
    assert inverse[0,0]==arrow[0,0]
    assert s.simplify((project(inverse).T*project(inverse))[0]-(v.T*v)[0])==0
    require_zero(inverse.inv()-arrow)
    naive=project(inverse)+v
    if label=='all_three_components_with_carry':
        assert all(x!=0 for x in v)
        assert not zero(naive)
    if label=='radial_without_carry': require_zero(naive)
    cases.append({'label':label,'forward':values(v),'reverse':values(project(inverse)),
                  'gamma':str(arrow[0,0]),'omitted_carry_defect':values(naive)})
    arrows.append(arrow)

left,right=arrows[0],arrows[2]
require_zero((right*left).inv()-left.inv()*right.inv())
wrong_order=(right*left).inv()-right.inv()*left.inv()
assert not zero(wrong_order)

print(json.dumps({
    'status':'PASS_SOURCE_FORMULA_DIAGNOSTICS_ONLY',
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'python':sys.version,'sympy':s.__version__,'platform':platform.platform(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'symbolic_squeeze_eta_defect':[[str(x) for x in row] for row in squeeze_eta_defect.tolist()],
    'squeeze_K_identity_and_DDR_tangent':'PASS',
    'finite_reversal_cases':cases,
    'reverse_concatenation_order':'PASS',
    'hostile_controls':{'pretend_squeeze_preserves_eta':'REJECTED',
                        'drop_frame_carry':'REJECTED_ON_DECLARED_NONRADIAL_CASE',
                        'reverse_arrows_in_wrong_order':'REJECTED'},
    'scope':'Source algebra and selected exact controls; no curvature, native-admission, neighborhood-isometry or physical-evolution computation.'
},indent=2))
