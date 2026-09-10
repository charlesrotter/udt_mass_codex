#!/usr/bin/env python3
"""Exact author diagnostics; reuse source pullback/geometry, not independent review."""
import ast
import hashlib
import json
from pathlib import Path
import platform
import sympy as s

if not __debug__:
    raise RuntimeError('Evidence diagnostics require assertions enabled')
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
G179=ROOT/'udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/derive_complete_coframe_extension.py'
NCI=ROOT/'udt_null_clock_depth_integrability_assessment_2026-09-10/check_integrability.py'

def load_defs(path,names,namespace):
    tree=ast.parse(path.read_text())
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert len(nodes)==len(names)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),namespace)
    return namespace

eta=s.diag(-1,1,1,1)
pullback=load_defs(G179,{'pullback'},{'sp':s,'ETA4':eta})['pullback']
geom=load_defs(NCI,{'simp','geometry'},{'s':s})['geometry']
checks=[]
records=[]

def simple(v):
    return s.simplify(s.expand(v))

def values(v):
    return list(v) if isinstance(v,s.MatrixBase) else [v]

def same(name,a,b):
    residual=[simple(v) for v in values(a-b)]
    if any(v!=0 for v in residual):
        raise AssertionError((name,residual))
    checks.append({'name':name,'type':'exact identity','passed':True})

def rejected(name,wrong,right):
    residual=[simple(v) for v in values(wrong-right)]
    if all(v==0 for v in residual):
        raise AssertionError(('ineffective rejection control',name))
    checks.append({'name':name,'type':'wrong formula rejected','passed':True,
                   'residual':[str(v) for v in residual]})

def curlform(beta,space):
    return s.Matrix(3,3,lambda i,j:s.diff(beta[j],space[i])-s.diff(beta[i],space[j]))

def lie(v,w,coords):
    return s.Matrix([simple(sum(v[j]*s.diff(w[i],coords[j])-w[j]*s.diff(v[i],coords[j])
                                   for j in range(4))) for i in range(4)])

t,x,y,z,b,a,c=s.symbols('t x y z b alpha gamma',real=True)
coords=(t,x,y,z)
space=(x,y,z)
beta=s.Matrix([-b*y/2,b*x/2,0])
E=s.eye(4)
for i in range(3):E[0,i+1]=beta[i]
g=(E.T*eta*E).applyfunc(simple)
U=s.eye(4)[:,0]
origin={x:0,y:0,z:0}
same('coframe_invertible',E.det(),1)
same('unit_observer',(U.T*g*U)[0],-1)
same('Killing_time_field',g.diff(t),s.zeros(4))

coordinate_h=[]
orthogonal_j=[]
orthogonal_v=[]
tau,q=s.symbols('tau q',real=True)
for i in range(3):
    ei=s.eye(4)[:,i+1]
    J=U.row_join(ei)
    h=pullback(E,J)
    expected=s.Matrix([[-1,-beta[i]],[-beta[i],1-beta[i]**2]])
    same(f'coordinate_pair_{i}',h,expected)
    same(f'direct_coordinate_pullback_{i}',J.T*g*J,h)
    same(f'regular_pair_det_{i}',h.det(),-1)
    same(f'clock_factor_{i}',-h[0,0],1)
    same(f'completed_density_{i}',s.sqrt(-h.det()),1)
    same(f'completed_shift_{i}',h[0,1]/h[0,0],beta[i])
    same(f'completed_scalar_{i}',-s.log(-h[0,0])/2,0)
    same(f'central_snapshot_{i}',h.subs(origin),s.diag(-1,1))
    same(f'time_silence_before_origin_{i}',h.diff(t),s.zeros(2))
    coordinate_h.append(h)
    # Actual coordinate pair immersion; derive its Jacobian, not merely name J.
    F=s.Matrix([t+tau,x,y,z]);F[i+1]+=q
    same(f'coordinate_immersion_jacobian_{i}',F.jacobian((tau,q)),J)
    X=ei-beta[i]*U
    Jo=U.row_join(X)
    ho=pullback(E,Jo)
    V=(E*Jo).applyfunc(simple)
    same(f'orthogonal_pair_{i}',ho,s.diag(-1,1))
    same(f'adapted_V_{i}',V,J)
    for k in range(4):
        same(f'adapted_V_derivative_{i}_{k}',V.diff(coords[k]),s.zeros(4,2))
    Fo=s.Matrix([t+tau-q*beta[i],x,y,z]);Fo[i+1]+=q
    along=dict(zip(coords,Fo))
    same(f'orthogonal_immersion_jacobian_{i}',Fo.jacobian((tau,q)),Jo.subs(along,simultaneous=True))
    same(f'orthogonal_immersion_pullback_{i}',Fo.jacobian((tau,q)).T*g.subs(along,simultaneous=True)*Fo.jacobian((tau,q)),s.diag(-1,1))
    orthogonal_j.append(Jo);orthogonal_v.append(V)

# Derivatives are taken BEFORE origin evaluation; input comes from actual h outputs.
extracted=s.Matrix([h[0,1]/h[0,0] for h in coordinate_h])
C=curlform(extracted,space).applyfunc(simple)
expected_C=s.Matrix([[0,b,0],[-b,0,0],[0,0,0]])
same('shift_first_jet_curl',C,expected_C)
same('central_curl',C.subs(origin),expected_C)
W_from_records=simple(sum(C[i,j]**2 for i in range(3) for j in range(3))/4)
same('vorticity_from_records',W_from_records,b**2/2)
geometry=geom(g,U,coords)
P=s.eye(4)+geometry['ul']*U.T
w=(P*(geometry['nab']-geometry['nab'].T)*P.T/2).applyfunc(simple)
W_direct=simple(s.trace(geometry['gi']*w*geometry['gi']*w.T))
same('independent_quantity_from_coordinate_geometry',W_direct,W_from_records)
same('geodesic_observer',geometry['a'],s.zeros(4,1))
same('orthogonal_germ_commutator',lie(orthogonal_j[0][:,1],orthogonal_j[1][:,1],coords),-b*U)
same('input_coframe_exterior_derivative',s.diff(E[0,2],x)-s.diff(E[0,1],y),b)

# Nonconstant synchronization: matched coordinate change vs a changed query.
f=a*x*y+c*x**2/2
df=s.Matrix([s.diff(f,v) for v in space])
K=s.eye(4)
for i in range(3):K[0,i+1]=df[i]
Ep=(E*K.inv()).applyfunc(simple)
new_beta=[]
for i in range(3):
    J=U.row_join(s.eye(4)[:,i+1])
    same(f'matched_coordinate_covariance_{i}',pullback(Ep,K*J),coordinate_h[i])
    hp=pullback(Ep,J)
    new_beta.append(simple(hp[0,1]/hp[0,0]))
    same(f'reselected_coordinate_shift_{i}',new_beta[-1],beta[i]-df[i])
new_beta=s.Matrix(new_beta)
Cp=curlform(new_beta,space).applyfunc(simple)
same('common_synchronization_curl',Cp,C)
same('pure_gradient_no_twist',Cp.subs(b,0),s.zeros(3))

# Existing source pullback's Lorentz gauge; observer family is unchanged.
L=s.Matrix([[s.Rational(5,3),s.Rational(4,3),0,0],
            [s.Rational(4,3),s.Rational(5,3),0,0],[0,0,0,-1],[0,0,1,0]])
same('Lorentz_gauge_matrix',L.T*eta*L,eta)
for i in range(3):
    J=U.row_join(s.eye(4)[:,i+1])
    same(f'Lorentz_gauge_pullback_{i}',pullback(L*E,J),coordinate_h[i])
    k=s.symbols('k',positive=True)
    hs=pullback(E,J*s.diag(1,k))
    m=s.sqrt(-hs.det())
    same(f'scaled_ruler_density_{i}',m,k)
    same(f'scaled_completed_shift_{i}',simple(hs[0,1]/hs[0,0]/m),beta[i])
    hr=pullback(E,J*s.diag(1,-1))
    same(f'ruler_orientation_shift_{i}',hr[0,1]/hr[0,0],-beta[i])

# Finite exact examples certify these controls, not a continuum theorem.
test={b:s.Rational(3,2),a:s.Rational(2,3),c:s.Rational(-1,5),x:s.Rational(4,7),y:s.Rational(-2,5),z:0,t:0}
rejected('erased_shift',s.zeros(3,1),extracted.subs(test))
rejected('curl_wrong_plus', (s.diff(extracted[1],x)+s.diff(extracted[0],y)).subs(test),C[0,1].subs(test))
rejected('vorticity_half_factor',W_from_records.subs(test)/2,W_direct.subs(test))
rejected('vorticity_double_factor',2*W_from_records.subs(test),W_direct.subs(test))
# Evaluate b=0 before numerical substitutions for the actual flat control.
flat_point_shift=sum(v**2 for v in new_beta).subs(b,0).subs(test)
rejected('flat_shift_norm_as_rotation',flat_point_shift,0)
rejected('one_derivative_as_curl',(2*s.diff(new_beta[1],x)).subs(test),Cp[0,1].subs(test))
rejected('freeze_origin_before_spatial_derivative',curlform(extracted.subs(origin),space),C.subs({b:1}))
rejected('unmatched_coordinate_mapping',pullback(Ep,U.row_join(s.eye(4)[:,1])).subs(test),coordinate_h[0].subs(test))
rejected('infer_zero_twist_from_adapted_V',0,W_direct.subs(b,1))
rejected('infer_zero_twist_from_point_h',0,W_direct.subs(b,1))
rejected('wrong_commutator_sign',(b*U).subs(test),lie(orthogonal_j[0][:,1],orthogonal_j[1][:,1],coords).subs(test))

for bv in [s.Rational(0),s.Rational(1),s.Rational(-1),s.Rational(3,2)]:
    records.append({'b':str(bv),'central_coordinate_h':[str(h.subs(origin).subs(b,bv)) for h in coordinate_h],
                    'spatial_shift_jet_xy':str(s.diff(extracted[1],x).subs(b,bv)),
                    'spatial_shift_jet_yx':str(s.diff(extracted[0],y).subs(b,bv)),
                    'curl_xy':str(C[0,1].subs(b,bv)),'W_direct':str(W_direct.subs(b,bv)),
                    'W_from_records':str(W_from_records.subs(b,bv)),
                    'orthogonal_V':[str(v) for v in orthogonal_v]})
print(json.dumps({'status':'PASS','kind':'author exact diagnostics; shared source utilities disclosed',
    'python':platform.python_version(),'sympy':s.__version__,'checks':checks,'check_count':len(checks),
    'records':records,'candidate_sha256':hashlib.sha256((HERE/'INITIAL_CANDIDATE.md').read_bytes()).hexdigest(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'reused_sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [G179,NCI]},
    'limits':'Analytic proof owns continuum scope; no physical records, whole-registry replay, metric inversion or independent review.'},indent=2))
