"""Implementation-distinct replay of parent's saved quantities, not its code."""
from pathlib import Path
import hashlib,json,math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

HERE=Path(__file__).parent
PACKAGE=HERE.parent
# Reuse exactly the sealed reviewer's original metric utility definitions.
# The initial source's top-level result runner is deliberately not executed.
original=(HERE/'INITIAL_check_original_metric.py').read_text()
namespace={'__file__':str(HERE/'INITIAL_check_original_metric.py')}
exec(compile(original[:original.index("\nresults={'versions'")],str(HERE/'INITIAL_check_original_metric.py'),'exec'),namespace)
metric=namespace['metric'];integrate=namespace['integrate']

parent_path=PACKAGE/'CONSTRUCTION_RESULT.json'
parent=json.loads(parent_path.read_text())
rows=next(q['actual_incidences'] for q in parent['precisions'] if q['dps']==70)
mm=1.;a=10.;H=math.sqrt(.0001/3);omega=math.sqrt(mm/a**3-H*H);h=1-3*mm/a
fa=1-2*mm/a-H*H*a*a
results={'parent_result_sha256':hashlib.sha256(parent_path.read_bytes()).hexdigest(),'rows':[],'original_metric':[],'status':'RUNNING','cumulative_cases_before':64}

def save():
 (HERE/'SAVED_REPLAY_RESULT.json').write_text(json.dumps(results,indent=2)+'\n')

try:
 for row in rows:
  E=float(row['E']);R=float(row['R']);x=1/R
  W=lambda y:math.sqrt(H*H+(E*E-1)*y*y+2*mm*y**3)
  tail=quad(lambda y:1/(W(y)*(E*y+W(y))),0,x,epsabs=2e-12,epsrel=2e-12)[0]
  def geo(b):
   s=lambda y:math.sqrt(1+H*H*b*b-b*b*y*y+2*mm*b*b*y**3)
   P=quad(lambda y:b/s(y),x,1/a,epsabs=2e-12,epsrel=2e-12)[0]
   U=quad(lambda y:b*b/(s(y)*(1+s(y))),x,1/a,epsabs=2e-12,epsrel=2e-12)[0]
   I=quad(lambda y:1/s(y)**3,x,1/a,epsabs=2e-12,epsrel=2e-12)[0]
   return P,U,I,s
  def eq(b):
   P,U,I,s=geo(b);return P-omega*(U+tail)
  b=brentq(eq,0,.99*a/math.sqrt(fa),xtol=5e-14,rtol=2e-14)
  P,U,I,s=geo(b);te=-tail-U;sR=s(x);sa=s(1/a)
  v=math.sqrt(E*E-1+2*mm/R+H*H*R*R)
  A=1/(E+v)+v*b*b/(R*R*(1+sR));we=(1-omega*b)/math.sqrt(h);Z=we/A
  bp=a*R*sa*sR*I;bt=a*R*math.sin(P)/b
  # Direct radius quadrature is distinct from parent's tail-subtracted formula.
  L=quad(lambda rr:1/s(1/rr),a,R,epsabs=2e-10,epsrel=2e-12,limit=400)[0]
  DA=A*math.sqrt(abs(bp*bt));Do=A*L
  ratio=Z*(1/H-DA)/((a+E/H)/math.sqrt(h))
  computed=dict(b=b,t_e=te,tail=tail,P=P,U=U,I=I,L=L,A=A,omega_e=we,Z=Z,B_parallel=bp,B_perp=bt,j_parallel=A*bp,j_perp=A*bt,D_A=DA,D_o=Do,area_to_affine=DA/Do,shear_ratio=bp/bt,pole_ratio=ratio)
  errors={k:abs(z-float(row[k]))/max(1,abs(float(row[k]))) for k,z in computed.items()}
  results['rows'].append({'E':E,'R':R,'computed':computed,'errors':errors,'max_scaled_error':max(errors.values()),'incidence_residual':abs(eq(b))});save()
  assert max(errors.values())<=1e-7 and abs(eq(b))<=1e-10
  if (E==1 and R==1000) or (E==10 and R==1000000):
   xo=np.array([0.,R,math.pi/2,0.]);ko=np.array([b*b/(R*R*(1+sR)),sR,0.,b/(R*R)])
   Uo=np.array([1/(E+v),v,0.,0.]);gm=metric(xo,mm,H)
   eo=np.array([[b/(R*sR),0],[0,0],[0,1/R],[1/(R*sR),0]])
   physical=eo+np.outer(ko,Uo@gm@eo/A)
   initial=np.r_[xo,ko,np.zeros(8),(A*physical).ravel()]
   sol=integrate(initial,a,R,mm,H,True,True);last=sol.y[:,-1]
   ge=metric(last[:4],mm,H)
   ee=np.array([[b/(a*sa),0],[0,0],[0,1/a],[1/(a*sa),0]])
   actual=ee.T@ge@last[8:16].reshape(4,2);expected=-np.diag([A*bp,A*bt])
   err=float(np.max(abs(actual-expected))/max(1,np.max(abs(expected))))
   norms=[];energies=[]
   for i in range(sol.y.shape[1]):
    xx=sol.y[:4,i];kk=sol.y[4:8,i];gg=metric(xx,mm,H)
    norms.append(abs(float(kk@gg@kk))/max(1,float(np.sum(abs(kk*(gg@kk))))))
    energies.append(abs(float(-(gg@kk)[0])-1))
   results['original_metric'].append({'E':E,'R':R,'map':actual.tolist(),'expected':expected.tolist(),'scaled_error':err,'null_scaled':max(norms),'energy_error':max(energies),'steps':len(sol.t)});save()
   assert err<=2e-6 and max(norms)<=2e-7 and max(energies)<=2e-7
 results['status']='PASS';results['cumulative_cases_after']=74;save();print('Saved replay PASS, cumulative74/100')
except Exception as ex:
 results['status']='FAIL';results['exception']=repr(ex);save();raise
