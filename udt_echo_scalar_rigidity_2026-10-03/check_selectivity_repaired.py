"""ESR1 exact Q jets and original signed-geometry clock controls."""
from pathlib import Path
import sympy as s,mpmath as mp,json,platform,time
B=Path(__file__).resolve().parent;start=time.monotonic();exact=[];cases=[]
e,T,aa,ab,bb,a,b,v2,vw=s.symbols('e T aa ab bb a b v2 vw',real=True)
p=1-T*e/2+(T**2/s.Integer(6)-ab/6-bb/24)*e**2
q=1-3*T*e/2+(T**2/4+2*aa+ab/2-bb/8)*e**2
trial=1+a*(p-1)+b*(p-1)**2/2
res=s.Poly(s.expand(q-trial),e)
assert s.expand(res.coeff_monomial(e)-(a-3)*T/2)==0;exact.append('nonzero_eigenvalue_fixes_Qprime_3')
r4=s.factor(res.coeff_monomial(e**2).subs(a,3))
assert s.expand(r4.subs({aa:T**2,ab:0})-(14-b)*T**2/8)==0;exact.append('nonzero_eigendirection_fixes_Qsecond_14')
d4=s.expand(r4.subs(b,14));assert d4==2*aa+ab-2*T**2;exact.append('arbitrary_Q_quartic_obstruction')
expr=s.expand(d4.subs({aa:T**2+v2,ab:vw}));assert expr==2*v2+vw
assert s.expand(expr+expr.subs(vw,-vw))==4*v2;exact.append('opposite_direction_positive_sum')
assert s.simplify(r4.subs({a:3,b:14,T:0})-(2*aa+ab))==0;exact.append('zero_leading_direction_kept')
assert s.expand(r4.subs({b:12,aa:T**2,ab:0})-T**2/4)==0;exact.append('wrong_Qsecond_does_not_pass')

# Original signed quadric null incidence, with C=C_{-kappa}, S=S_{-kappa}.
c,k,h=s.symbols('c k h',nonzero=True,real=True)
z=1/c**2-1;Cb=1/c;Ca=(1+z)/(1-z);Sa=2*h/(1-z)
reduce=lambda x:s.factor(s.cancel(s.expand(x)).subs(h**2,z/k))
assert reduce(Ca-k*Sa*h-1)==0;exact.append('actual_nonzero_return_incidence')
assert reduce(Ca**2-k*Sa**2-1)==0;exact.append('return_unit_quadric_identity')
ps=s.cancel(-(-k*h)/(c*k*h));qs=s.cancel(-(k*(c*Ca*h-Sa*Cb))/(k*(c*Sa*Cb-Ca*h)))
assert ps==1/c and s.factor(qs-c/(2*c**2-1))==0
assert s.factor(qs-ps/(2-ps**2))==0;exact.append('signed_original_endpoint_ratios')

mp.mp.dps=80
for kval in ['1','2.25','-1','-2.25']:
 K=mp.mpf(kval);root=mp.sqrt(abs(K))
 C=(lambda t:mp.cosh(root*t)) if K>0 else (lambda t:mp.cos(root*t))
 S=(lambda t:mp.sinh(root*t)/root) if K>0 else (lambda t:mp.sin(root*t)/root)
 for lval in ['0.05','0.1','0.2','0.4']:
  L=mp.mpf(lval);cl=mp.cos(root*L) if K>0 else mp.cosh(root*L)
  def F(x,y):return cl*C(x)*C(y)-K*S(x)*S(y)-1
  rec=mp.findroot(lambda y:F(0,y),(L,mp.mpf('1.1')*L),tol=mp.mpf('1e-72'),maxsteps=40)
  ret=mp.findroot(lambda x:F(x,rec),(mp.mpf('1.8')*L,mp.mpf('2.2')*L),tol=mp.mpf('1e-72'),maxsteps=40)
  Fx=lambda x,y:K*(cl*S(x)*C(y)-C(x)*S(y))
  Fy=lambda x,y:K*(cl*C(x)*S(y)-S(x)*C(y))
  pnum=-Fx(0,rec)/Fy(0,rec);qnum=-Fy(ret,rec)/Fx(ret,rec)
  errors=[abs(F(0,rec)),abs(F(ret,rec)),abs(pnum-1/cl),abs(qnum-cl/(2*cl**2-1)),abs(qnum-pnum/(2-pnum**2))]
  assert ret>rec>0 and pnum>0 and qnum>0 and pnum<mp.sqrt(2)
  assert max(errors)<mp.mpf('1e-65'),(kval,lval,errors)
  cases.append({'kappa':kval,'L':lval,'first':str(rec),'return':str(ret),'p':str(pnum),'q':str(qnum),'max_original_or_identity_error':str(max(errors)),'future':True})

# Flat branch uses original affine null equations, not a singular kappa division.
ls=s.symbols('L',positive=True);em=s.symbols('s',real=True)
first=em+ls;later=first+ls
assert s.diff(first,em)==1 and s.diff(later,em)/s.diff(first,em)==1
exact.append('flat_Q_value_only')
# Smooth unused-side freedom: each derivative is exp(-1/t²) times a polynomial
# in1/t, tending to0 as t→0. Finite values check branch routing, not smoothness.
q0=lambda p:p/(2-p*p)
for attained_sign in [1,-1]:
 for pp in ['0.9','1','1.1']:
  pv=mp.mpf(pp);delta=attained_sign*(pv-1)
  bump=mp.mpf(0) if delta>=0 else mp.exp(-1/(pv-1)**2)
  if delta>=0:assert bump==0
  else:assert bump>0
  assert q0(pv)+bump>0
exact.append('smooth_Q_unused_side_freedom_routing')
out={'status':'PASS','python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__,'duration_seconds':time.monotonic()-start,'families':3,'exact_assertion_groups':exact,'original_root_cases':len(cases),'flat_controls':1,'smooth_Q_routing_cases':6,'precision_digits':mp.mp.dps,'numeric_absolute_gate':'1e-65','cases':cases,'scope':'Coefficient algebra and actual short signed-curvature incidences; universal rigidity belongs to the proof, not finite checks.'}
(B/'PARENT_CHECK_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='cases'}))
