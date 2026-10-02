"""RCD1 reused-context independent reconstruction; no new parent code imports."""
import hashlib,json,platform
from pathlib import Path
import sympy as s

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
checks=[]
def zero(name,expr):
    q=s.factor(s.cancel(expr))
    checks.append({'name':name,'residual':str(q),'zero':q==0})
    assert q==0,(name,q)
p,p1,p2,p3,p4=s.symbols('p p1 p2 p3 p4',nonzero=True)
alpha,Lambda=s.symbols('alpha Lambda',real=True)
jets=[p,p1,p2,p3,p4]
DL=lambda expr:s.expand(sum(s.diff(expr,jets[i])*jets[i+1] for i in range(4)))
dt=lambda expr:DL(expr)/p
H=p1/p**2
hd=dt(H)
R=s.factor(6*(hd+2*H**2));Rd=s.factor(dt(R));Rdd=s.factor(dt(Rd))
zero('clock_R',R-6*p2/p**3)
zero('clock_Rdot',Rd-6*(p3/p**4-3*p1*p2/p**5))
F=1+2*alpha*R;f=R+alpha*R**2
C=-3*F*(hd+H**2)+f/2+6*alpha*H*Rd-Lambda
D=F*(hd+3*H**2)-f/2-2*alpha*(Rdd+2*H*Rd)+Lambda
U=3*p1**2/p**4
V=36*p1*p3/p**6-18*p2**2/p**6-72*p1**2*p2/p**7
zero('observable_equals_original00',C-U-alpha*V+Lambda)
zero('off_shell_conservation',dt(C)+3*H*(C+D))
zero('denominator_free_equation',(U+alpha*V-Lambda)*p**7-
     (3*p**3*p1**2+36*alpha*p*p1*p3-18*alpha*p*p2**2-72*alpha*p1**2*p2-Lambda*p**7))
zero('turning_constraint',C.subs(p1,0)+18*alpha*p2**2/p**6+Lambda)
zero('constant_p_00',C.subs({p1:0,p2:0,p3:0,p4:0})+Lambda)
zero('constant_p_spatial',D.subs({p1:0,p2:0,p3:0,p4:0})-Lambda)
h=s.symbols('h',real=True)
constH={p1:h*p**2,p2:2*h**2*p**3,p3:6*h**3*p**4,p4:24*h**4*p**5}
zero('constant_H_U',U.subs(constH)-3*h**2)
zero('constant_H_V',V.subs(constH))
zero('constant_H_full00',C.subs(constH).subs(Lambda,3*h**2))
zero('constant_H_fullspatial',D.subs(constH).subs(Lambda,3*h**2))
r0=s.symbols('r0',nonzero=True,real=True)
constR={p2:r0*p**3/6,p3:r0*p**2*p1/2,p4:r0*p*p1**2+r0**2*p**5/12}
zero('Fzero_full00',C.subs(constR).subs({alpha:-1/(2*r0),Lambda:r0/4}))
zero('Fzero_fullspatial',D.subs(constR).subs({alpha:-1/(2*r0),Lambda:r0/4}))
zero('Fzero_observable_affine',V.subs(constR)-2*r0*U+r0**2/2)

# Original ODE from reviewed ERC1, differentiated independently along L with
# d/dL = a d/dt. No parent rational-series helper is imported.
hs,rs,ps,aa=s.symbols('H R P a')
variables=[hs,rs,ps,aa]
flow=[rs/6-2*hs**2,ps,-3*hs*ps-rs/(6*alpha),aa*hs]
along=lambda expr:s.expand(aa*sum(s.diff(expr,x)*v for x,v in zip(variables,flow)))
value=aa;coeff=[]
for n in range(1,6):
    value=along(value)
    coeff.append(s.factor(value.subs({hs:0,rs:0,aa:1})/s.factorial(n)))
zero('flat_p_cubic',coeff[2]-ps/36)
zero('flat_p_quartic',coeff[3])
zero('flat_p_quintic',coeff[4]+ps/(4320*alpha))
zero('flat_alpha_coefficient_relation',coeff[4]+coeff[2]/(120*alpha))

# Original supplied PCC1 metric, differentiated with respect to proper time.
t,b=s.symbols('t b',real=True)
ac=1+b*t**3
hc=s.diff(ac,t)/ac
rc=6*(s.diff(hc,t)+2*hc**2)
pc=s.diff(rc,t)
cc=3*(1+2*alpha*rc)*hc**2-alpha*rc**2/2+6*alpha*hc*pc-Lambda
zero('PCC_initial_constraint',cc.subs(t,0)+Lambda)
fourth=s.factor(s.diff(cc,t,4).subs({t:0,Lambda:0})/24)
zero('PCC_obstruction_t4',fourth-27*b**2)
assert fourth!=0
checks.append({'name':'nonzero_cubic_metric_rejected','t4_coefficient':str(fourth)})

# Rank caveat: collinear determinant alone is not the normalized affine law.
matrix=s.Matrix([[1,0,0],[1,0,1],[1,0,2]])
zero('constant_V_determinant_false_pass',matrix.det())
assert s.linsolve([Lambda-0,Lambda-1,Lambda-2],alpha,Lambda)==s.EmptySet
checks.append({'name':'constant_V_varying_U_no_constants','no_solution':True})

pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
for name,wanted in pins.items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==wanted,name
result={'pass':True,'context':'/root/erc_math','fresh_context':False,
 'new_parent_argument_exposed':False,'prior_exposure':'Full ERC1 mathematical/source/code/result review',
 'python':platform.python_version(),'sympy':s.__version__,'checks':checks,
 'check_count':len(checks),'source_pin_count':len(pins),
 'observable_U':str(U),'observable_V':str(V),
 'flat_event_p_coefficients_1_through_5':[str(x) for x in coeff],
 'PCC_original_constraint':str(s.factor(cc)),'PCC_t4_obstruction':str(fourth),
 'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'argument_sha256':hashlib.sha256((OUT/'SOURCE_FIRST.md').read_bytes()).hexdigest(),
 'limits':'Exact restricted algebra plus analytic proof in SOURCE_FIRST; no empirical data, fresh context, general4D reconstruction or physical response selection.'}
with (OUT/'SOURCE_FIRST_RESULT.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n')
print(json.dumps({'pass':True,'check_count':len(checks),'source_pin_count':len(pins),
 'flat_event_p_coefficients':[str(x) for x in coeff],'PCC_t4_obstruction':str(fourth)},indent=2))
