#!/usr/bin/env python3
"""Exact diagnostic anchors, not proofs of apparatus or all metric hypotheses."""
import argparse
from fractions import Fraction as F
import json
import platform
import sys
import sympy as s

parser=argparse.ArgumentParser()
parser.add_argument('--mutant',choices=['delay_sign','clock_factor','record_density','phase_order','wrapped_alias','frequency_error'])
args=parser.parse_args()
passed=[]
def ck(name, condition):
    if not condition:
        print(json.dumps({'status':'FAIL','guard':name,'passed':passed,'mutant':args.mutant},indent=2))
        raise AssertionError(name)
    passed.append(name)
def eq(name,a,b): ck(name,s.simplify(a-b)==0)

# Full original metric pullback; no source scientific implementation imported.
N,L=s.symbols('N L',positive=True)
b=s.symbols('b',real=True)
g=s.Matrix([[-N**2,-N**2*b],[-N**2*b,L**2-N**2*b**2]])
eq('full_raw_determinant',g.det(),-N**2*L**2)
m=s.sqrt(-g.det()); B=b/m
J=s.diag(1,1/m); H=s.simplify(J.T*g*J)
eq('completed_determinant',H.det(),-1)
eq('shift_from_raw_metric',g[0,1]/g[0,0],b)
recovered=B if args.mutant=='record_density' else m*B
eq('original_density_needed',recovered,b)
eq('scalar_depth',-s.log(s.sqrt(-H[0,0])),-s.log(N))
eq('shift_changes_full_H',s.diff(H[0,1],b),-N/L)

# Direct null quadratic for forward and reversed circular spatial tangent.
R,c=s.symbols('R c',positive=True)
k,q,theta=s.symbols('k q theta',real=True)
x,y=s.symbols('x y',real=True)
beta=s.Matrix([-k*y/2,k*x/2,0]); eye=s.eye(3)
G=s.zeros(4);G[0,0]=-1
for i in range(3):
    G[0,i+1]=G[i+1,0]=-beta[i]
    for j in range(3):G[i+1,j+1]=eye[i,j]-beta[i]*beta[j]
dx=s.Matrix([-R*s.sin(theta),R*s.cos(theta),0])
circle={x:R*s.cos(theta),y:R*s.sin(theta)}
polyplus=s.trigsimp((s.Matrix([q,*dx]).T*G.subs(circle)*s.Matrix([q,*dx]))[0])
polyminus=s.trigsimp((s.Matrix([q,*(-dx)]).T*G.subs(circle)*s.Matrix([q,*(-dx)]))[0])
plus=R-k*R**2/2;minus=R+k*R**2/2
eq('forward_original_null_equation',polyplus.subs(q,plus),0)
eq('reverse_original_null_equation',polyminus.subs(q,minus),0)
ck('forward_root_is_solution',plus in s.solve(polyplus,q))
ck('reverse_root_is_solution',minus in s.solve(polyminus,q))
integral=s.integrate(s.trigsimp((beta.subs(circle).T*dx)[0]),(theta,0,2*s.pi))
eq('circle_line_integral',integral,s.pi*k*R**2)
pred=(2 if args.mutant=='delay_sign' else -2)*integral/c
eq('signed_delay_direct_roots',2*s.pi*(plus-minus)/c,pred)
Ndet,Xp,Xm=s.symbols('Ndet Xp Xm',positive=True)
detector_delay=(Xp-Xm)/c if args.mutant=='clock_factor' else Ndet*(Xp-Xm)/c
eq('proper_detector_clock',detector_delay,Ndet*Xp/c-Ndet*Xm/c)
eq('slice_determinant', (eye-beta*beta.T).det(),1-k**2*(x*x+y*y)/4)
eq('same_scalar_at_nonzero_shift',(-s.log(s.sqrt(-G[0,0]))),0)
ck('scalar_omission_has_nonzero_delay',s.simplify(pred.subs({R:2,k:s.Rational(1,4),c:1}))!=0)
eq('zero_shift_control',pred.subs(k,0),0)
# Exact single-valued gauge integral and constant time relabeling.
f=x*x*y+3*x*y+y*y
df=s.Matrix([s.diff(f,x),s.diff(f,y),0])
eq('closed_exact_gradient_invisible',s.integrate(s.trigsimp((df.subs(circle).T*dx)[0]),(theta,0,2*s.pi)),0)
a,I=s.symbols('a I',positive=True)
eq('constant_time_coordinate_invariance',-2*(Ndet/a)*(a*I)/c,-2*Ndet*I/c)

# Common-reception-event phase and exact symbolic nuisance cancellation.
tau,omega,Tp,Tm,bp,bm,D,w0,dw,b0=s.symbols('tau omega Tp Tm bp bm D w0 dw b0',real=True)
phaseplus=omega*(tau-Tp)+bp; phaseminus=omega*(tau-Tm)+bm
phase=phaseplus-phaseminus if args.mutant=='phase_order' else phaseminus-phaseplus
eq('same_event_comparator_order',phase,omega*(Tp-Tm)+bm-bp)
angles=[(w0+j*dw)*D+b0 for j in range(3)]
eq('wrapped_second_contrast_exponent',angles[2]+angles[0]-2*angles[1],0)
for j in (1,2):eq(f'independent_geometry_prediction_{j}',angles[j]-angles[0],j*dw*D)
inst=s.symbols('inst',real=True)
eq('constant_instrument_delay_is_blind',s.expand(((w0+2*dw)*inst+w0*inst-2*(w0+dw)*inst)),0)

# Rational unit-circle arithmetic: numbers below are phase CYCLES (2pi radians).
def z(angle):return angle%1
def triple(delay,offset,w=F(11,7),step=F(3,5)):
    return [z((w+j*step)*delay+offset) for j in range(3)]
def contrast(zs):return z(zs[2]+zs[0]-2*zs[1])
delay=F(5,11);offset=F(2,9);step=F(3,5);w=F(11,7)
zs=triple(delay,offset)
ck('exact_wrapped_prediction',contrast(zs)==0)
for alias in (-3,-1,1,4):
    aliased=triple(delay+alias/step,offset-w*alias/step)
    equal=aliased==zs
    ck(f'full_alias_preserves_all_three_{alias}',not equal if args.mutant=='wrapped_alias' else equal)
ck('non_affine_detectable_departure',contrast([z(zs[j]+F(1,8)*j*j) for j in range(3)])==F(1,4))
ck('non_affine_wrapped_blind_departure',contrast([z(zs[j]+F(1,2)*j*j) for j in range(3)])==0)
ck('arbitrary_phase_can_fit_any_triple',all(z((w+j*step)*delay+(target-(w+j*step)*delay))==target for j,target in enumerate([F(1,7),F(2,5),F(5,6)])))
ck('geometry_departure_detectable',z(step*F(1,3))!=0)
ck('geometry_departure_alias',z(step*(1/step))==0)

# Symbolic uncertainty coefficients, no physical bounds supplied.
e0,e1,e2,eta0,eta1,eta2=s.symbols('e0 e1 e2 eta0 eta1 eta2',real=True)
noisy=[angles[j]+D*[eta0,eta1,eta2][j]+[e0,e1,e2][j] for j in range(3)]
actual=s.expand(noisy[2]+noisy[0]-2*noisy[1])
expected=e2+e0-2*e1
if args.mutant!='frequency_error':expected+=D*(eta2+eta0-2*eta1)
eq('frequency_errors_multiply_delay',actual,expected)
ck('training_phase_error_weights',[s.diff(actual,e) for e in [e0,e1,e2]]==[1,-2,1])
ck('training_frequency_error_weights',[s.diff(actual,e) for e in [eta0,eta1,eta2]]==[D,-2*D,D])
D0,dd=s.symbols('D0 dd',real=True)
for j in (1,2):
    resid=s.expand(noisy[j]-noisy[0]-j*dw*D0).subs(D,D0+dd)
    target=j*dw*dd+(D0+dd)*([eta0,eta1,eta2][j]-eta0)+[e0,e1,e2][j]-e0
    eq(f'independent_geometry_error_{j}',resid,target)
# Finite exact corner diagnostics for circle triangle bounds, not universal proof.
from itertools import product
u=[F(1,100),F(2,100),F(3,100)]
for signs in product([-1,1],repeat=3):
    eps=[a*b for a,b in zip(signs,u)];v=z(eps[2]+eps[0]-2*eps[1]);distance=min(v,1-v)
    ck('triangle_corner_'+''.join('p' if n>0 else 'm' for n in signs),distance<=u[2]+u[0]+2*u[1])

print(json.dumps({'status':'PASS','checks':len(passed),'guards':passed,'mutant':args.mutant,'python':platform.python_version(),'sympy':s.__version__,'mode':'exact symbolic/rational diagnostics; analytical arguments own quantifiers; no empirical validation'},indent=2))
