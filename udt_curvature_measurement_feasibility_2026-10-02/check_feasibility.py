"""CMF1 exact kinematic/necessary-law checks; no physical simulation or data."""
from pathlib import Path
import json, platform, hashlib
import sympy as s
B=Path(__file__).resolve().parent
tests=[]
def zero(name,expr):
    value=s.simplify(expr)
    if value!=0: raise AssertionError((name,str(value)))
    tests.append(name)
t,x,y,z=s.symbols('t x y z',real=True); coords=[t,x,y,z]
eta=s.diag(-1,1,1,1); v=s.symbols('v',positive=True)
S=s.zeros(4)
for a in range(4):
    for b in range(a,4): S[a,b]=S[b,a]=s.Symbol(f'S{a}{b}')
cs=[(S[0,0]+sign*2*v*S[0,i]+v*v*S[i,i])/(1-v*v)
    for i in range(1,4) for sign in [1,-1]]
R=-S[0,0]+sum(S[i,i] for i in range(1,4))
zero('seven_contraction_reconstruction',(1-v*v)*sum(cs)/(2*v*v)-(1+3/v**2)*S[0,0]-R)
zero('chosen_speed_coefficients',(sum(cs)-10*S[0,0]-R).subs(v,1/s.sqrt(3)))
zero('worst_case_weight_sum',3*(1-v*v)/v**2+1+3/v**2-(6/v**2-2))
rows=[]
independent=[S[a,b] for a in range(4) for b in range(a,4)]
for c in [S[0,0]]+cs:
    rows.append([s.diff(c,q) for q in independent])
rank=s.Matrix(rows).subs(v,s.Rational(3,5)).rank(); assert rank==7

# Compute linear Ricci from a metric perturbation independently of clock formula.
def linear_ric(h):
    trace=sum(eta[a,a]*h[a,a] for a in range(4))
    return s.Matrix(4,4,lambda a,b:s.simplify(sum(eta[c,c]*(
        s.diff(h[c,b],coords[c],coords[a])+s.diff(h[c,a],coords[c],coords[b])
        -s.diff(h[a,b],coords[c],2)) for c in range(4))/2
        -s.diff(trace,coords[a],coords[b])/2))
box=lambda f:sum(eta[a,a]*s.diff(f,coords[a],2) for a in range(4))
rho=s.cos((5*t-3*x)/4); alpha=s.Rational(1,6); sigma=-alpha*rho
ric=linear_ric(2*sigma*eta); rr=sum(eta[a,a]*ric[a,a] for a in range(4))
zero('metric_linear_curvature',rr-rho)
zero('metric_scalar_pole',box(rr)-rr)
for a in range(4):
    for b in range(4):
        E=ric[a,b]-eta[a,b]*rr/2+2*alpha*(eta[a,b]*box(rr)-s.diff(rr,coords[a],coords[b]))
        zero(f'original_linear_tensor_{a}{b}',E)

# Ultrastatic constant-spatial-curvature metric: zero first metric derivatives at o.
# Exact Ricci at o uses precisely its quadratic metric jet, not a weak-field claim.
K=s.symbols('K',real=True)
hs=s.diag(0,-K*(x*x+y*y+z*z)/2,-K*(x*x+y*y+z*z)/2,-K*(x*x+y*y+z*z)/2)
rs=linear_ric(hs)
zero('ultrastatic_Ric00',rs[0,0])
zero('ultrastatic_scalar',sum(eta[a,a]*rs[a,a] for a in range(4))-6*K)

h=s.symbols('h',positive=True); A=s.symbols('A0:4'); D=s.symbols('D0:4')
scalar=7+sum(A[i]*coords[i]**2+D[i]*coords[i]**4 for i in range(4))+t*x+x*y*z
origin={q:0 for q in coords}
def at_axis(f,i,step):
    sub=dict(origin);sub[coords[i]]=step;return f.subs(sub)
stencil=sum(eta[i,i]*(at_axis(scalar,i,h)+at_axis(scalar,i,-h)-2*scalar.subs(origin))/h**2 for i in range(4))
zero('geodesic_scalar_stencil_polynomial',stencil-box(scalar).subs(origin)-2*h*h*sum(eta[i,i]*D[i] for i in range(4)))
weights=[-1,-1]+[1]*6+[-4]; assert sum(abs(q) for q in weights)==12 and sum(weights)==0
eps,Brem,L=s.symbols('eps Brem L',positive=True)
zero('formal_clock_error_minimum',s.diff(eps/L**2+Brem*L,L).subs(L,(2*eps/Brem)**s.Rational(1,3)))

r,aa,bb,lam,Q=s.symbols('r alpha beta Lambda Q')
f=r+aa*r*r; F=s.diff(f,r)
zero('exact_quadratic_trace',3*s.diff(F,r)*Q+F*r-2*f+4*lam-(6*aa*Q-r+4*lam))
r1,r2=s.symbols('r1 r2'); q1=(r1-4*lam)/(6*aa);q2=(r2-4*lam)/(6*aa)
zero('exact_trace_alpha_inference',(r2-r1)/(6*(q2-q1))-aa)
zero('exact_trace_Lambda_inference',(r1-6*aa*q1)/4-lam)
hh=s.symbols('hh',nonzero=True,real=True); scale=s.sqrt(1+2*hh*t)
H=s.diff(scale,t)/scale; badR=6*(s.diff(H,t)+2*H*H)
zero('scalar_only_false_pass',badR)
bad00=s.simplify(3*H*H); assert bad00.subs(t,0)==3*hh*hh
# Same values at three time samples cannot certify the second derivative.
amb=t*t*(t*t-h*h)**2
for at in [0,h,-h]:zero('sample_ambiguity_at_'+str(at),amb.subs(t,at))
assert s.diff(amb,t,2).subs(t,0)==2*h**4

at0=ric.subs(origin); vv=s.Rational(3,5); gamma2=1/(1-vv*vv)
saved_cs=[at0[0,0]]+[s.simplify(gamma2*(at0[0,0]+2*sign*vv*at0[0,i]+vv*vv*at0[i,i])) for i in range(1,4) for sign in [1,-1]]
artifact={'scope':'Exact linear conformal metric control at origin. Not measured data or finite nonlinear solution.',
 'metric_perturbation':'h_ab=-(rho/3) eta_ab, rho=cos((5t-3x)/4)',
 'alpha':'1/6','speed':'3/5','ricci':[[str(q) for q in row] for row in at0.tolist()],
 'c_order':['c0','c1+','c1-','c2+','c2-','c3+','c3-'],'contractions':[str(q) for q in saved_cs],
 'trace_samples':[{'R':str(rv),'Box_R':str((rv-4*s.Rational(1,20))/(6*s.Rational(2,3)))} for rv in [s.Rational(1,3),s.Rational(5,4),s.Rational(-2,5)]]}
result={'status':'PASS','python':platform.python_version(),'sympy':s.__version__,'zero_identities':len(tests),'identity_names':tests,
 'seven_design_rank':rank,'stencil_abs_weight_sum':12,'nonzero_scalar_pass_tensor_failure':str(bad00),
 'finite_sample_second_jet_ambiguity':str(s.diff(amb,t,2).subs(t,0)),
 'limits':'Exact finite checks support stated algebra. General geometric theorem uses PSW1; error bounds conditional. No measured noise, physical source sector or full UDT selection.',
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
for name,data in [('SAVED_CONTROL.json',artifact),('EXACT_RESULT.json',result)]:
    with (B/name).open('x') as out:json.dump(data,out,indent=2);out.write('\n')
print(json.dumps(result,indent=2))
