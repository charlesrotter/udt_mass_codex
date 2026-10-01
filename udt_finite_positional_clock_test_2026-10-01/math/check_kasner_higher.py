"""FPC1 exact formal check from original Kasner coordinates, no target clock series."""
import json,sys,hashlib
from pathlib import Path
import sympy as S
L,d=S.symbols('L d',real=True)
checks=[]
def tr(x,n=5): return S.series(x,L,0,n).removeO().expand()
def eq(name,x,y=0):
 z=S.simplify(x-y)
 if z!=0: raise AssertionError((name,str(z)))
 checks.append(name)
def primitive(a,u):return sum(S.binomial(a,j)*u**(j+1)/S.Integer(j+1) for j in range(4))
def solve_delta(expr):
 value=S.Integer(0)
 for j in range(1,5):
  c=S.Symbol('c'+str(j));trial=value+c*L**j
  coeff=tr(expr(trial)).coeff(L,j)
  value+=S.solve(coeff,c)[0]*L**j
 return value

def one(p):
 # Solve the spacelike geodesic recurrence, rather than loading preparation coefficients.
 T=S.Integer(1)
 for j in (2,4):
  c=S.Symbol('t'+str(j));trial=T+c*L**j
  residual=tr(S.diff(trial,L,2)+p*trial**(-2*p-1),j-1).coeff(L,j-2)
  T+=S.solve(residual,c)[0]*L**j
 X=S.integrate(tr(T**(-2*p)),L)
 C=tr(T**p*S.diff(T,L))
 Vt=tr(T**(-p));Vx=tr(S.diff(T,L)*T**(-p))
 eq('spatial_geodesic_'+str(p),tr(S.diff(X,L,2)+2*p/T*S.diff(T,L)*S.diff(X,L),4))
 eq('preparation_norm_'+str(p),tr(-S.diff(T,L)**2+T**(2*p)*S.diff(X,L)**2,4),1)
 eq('clock_norm_'+str(p),tr(-Vt**2+T**(2*p)*Vx**2,4),-1)
 eq('parallel_time_'+str(p),tr(S.diff(Vt,L)+p*T**(2*p-1)*S.diff(X,L)*Vx,3))
 eq('parallel_space_'+str(p),tr(S.diff(Vx,L)+p/T*(S.diff(T,L)*Vx+S.diff(X,L)*Vt),3))
 # C is needed to cubic order only; omitted fifth-order terms cannot affect an L^4 readout.
 C=tr(C,4); X=tr(X,5)
 def jb(u):return C*(primitive(-2*p,u)-primitive(-2*p,T-1))-C**3/2*(primitive(-4*p,u)-primitive(-4*p,T-1))
 db=solve_delta(lambda u:primitive(-p,u)-X-jb(u))
 da=solve_delta(lambda u:primitive(-p,u)-2*primitive(-p,db))
 eq('outgoing_incidence_'+str(p),tr(primitive(-p,db)-X-jb(db)))
 eq('return_incidence_'+str(p),tr(primitive(-p,da)-2*primitive(-p,db)))
 w=tr(C*(1+db)**(-p))
 boost=tr(w-w**3/6)
 lp=tr(p*S.log(1+db)+boost)
 lq=tr(p*(S.log(1+da)-S.log(1+db))+boost)
 eq('PSW1_outgoing_L2_'+str(p),lp.coeff(L,2),p*(p-1)/2)
 eq('PSW1_return_L2_'+str(p),lq.coeff(L,2),3*p*(p-1)/2)
 if p in (0,1):
  eq('flat_outgoing_'+str(p),lp)
  eq('flat_return_'+str(p),lq)
 return dict(p=str(p),T=str(T),X=str(X),C=str(C),tb_minus_one=str(db),ta_minus_one=str(da),log_outgoing=str(lp),log_return=str(lq)),lp,lq

rows=[];logs=[]
for p in (S.Rational(-1,3),S.Rational(2,3),S.Integer(0),S.Integer(1)):
 r,lp,lq=one(p);rows.append(r);logs.append((lp,lq))
# Curvature is checked from the Kasner exponents themselves; the spacetime is nonflat.
ps=(S.Rational(-1,3),S.Rational(2,3),S.Rational(2,3))
eq('kasner_sum',sum(ps),1);eq('kasner_squares',sum(p*p for p in ps),1)
for p in ps:eq('kasner_spatial_Ric_factor_'+str(p),p*(sum(ps)-1))
eq('kasner_Ric_tt_factor',sum(p*(p-1)for p in ps))
if all(p*(1-p)==0 for p in ps):raise AssertionError('flat_supplied_geometry')
meanp=S.expand((logs[0][0]+2*logs[1][0])/3);meanq=S.expand((logs[0][1]+2*logs[1][1])/3)
eq('mean_outgoing_L2',meanp.coeff(L,2));eq('mean_return_L2',meanq.coeff(L,2))
result={'status':'PASS','checks':checks,'check_count':len(checks),'controls':rows,'principal_axis_mean_log_outgoing':str(meanp),'principal_axis_mean_log_return':str(meanq),'scope':'Exact formal series through L^4, remainder O(L^5) at fixed t0=1 on regular local branches. Principal-axis mean only; +/- agree by reflection, not signed-length averaging. One supplied nonflat Ricci-flat Kasner metric, plus flat exponents as algebraic controls.','python':sys.version,'sympy':S.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(result,indent=2))
