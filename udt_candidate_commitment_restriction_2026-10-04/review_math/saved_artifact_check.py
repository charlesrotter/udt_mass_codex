#!/usr/bin/env python3
"""Recompute parent saved incidence with direct-r quadrature and secant roots."""
import hashlib,json,platform,resource,sys,time
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import mpmath as mp
B=Path(__file__).resolve().parent
parent=B.parent
source=parent/'CONSTRUCTION_RESULT.json'
data=json.loads(source.read_text())
start=time.time()
out={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':platform.python_version(),'mpmath':mp.__version__,'method':'Direct radius quadrature; independently coded secant solve; parent code never imported','finite_endpoint_evaluations':0,'new_neighbor_solved_cases':0,'records':[]}
for batch in data['finite']:
 mp.mp.dps=batch['dps']
 m=mp.mpf(1);a=mp.mpf(10);lam=mp.mpf('0.0001');H=mp.sqrt(lam/3)
 h=1-3*m/a;om=mp.sqrt(m/a**3-lam/3)
 f=lambda r:1-2*m/r-lam*r*r/3
 for saved in batch['rows']:
  E=mp.mpf(saved['E']);R=mp.mpf(saved['R']);b=mp.mpf(saved['b']);te=mp.mpf(saved['te'])
  v=lambda r:mp.sqrt(E*E-f(r))
  ss=lambda r,bb:mp.sqrt(1-f(r)*bb*bb/r**2)
  def mesh(rad):
   vals=[a]
   while 10*vals[-1]<rad:vals.append(10*vals[-1])
   vals.append(rad)
   return vals
  def travel(rad,bb):
   points=mesh(rad)
   U=mp.quad(lambda r:bb*bb/(r*r*ss(r,bb)*(1+ss(r,bb))),points)
   P=mp.quad(lambda r:bb/(r*r*ss(r,bb)),points)
   return U,P
  def tail(rad):return mp.quad(lambda r:1/(v(r)*(E+v(r))),[rad,2*rad,10*rad,mp.inf])
  U,P=travel(R,b);d=tail(R)
  incidence=max(abs(te+U+d),abs(om*te+P))
  g=mp.matrix([[-f(R),-1,0],[-1,0,0],[0,0,R*R]])
  receiver=mp.matrix([1/(E+v(R)),v(R),0])
  ray=mp.matrix([b*b/(R*R*(1+ss(R,b))),ss(R,b),b/R**2])
  A=-(receiver.T*g*ray)[0]
  Z=(1-om*b)/(mp.sqrt(h)*A)
  prod=H*Z*(-mp.sqrt(h)*te)
  err=max(abs(Z/mp.mpf(saved['Z'])-1),abs(prod/mp.mpf(saved['H_Z_delta_tau_e'])-1))
  threshold=mp.mpf('1e-35' if batch['dps']==40 else '1e-65')
  assert incidence<threshold and err<threshold,(incidence,err)
  out['finite_endpoint_evaluations']+=1
  record={'dps':batch['dps'],'E':saved['E'],'R':saved['R'],'incidence_residual_from_saved':mp.nstr(incidence,mp.mp.dps),'relative_endpoint_recomputation_error':mp.nstr(err,mp.mp.dps)}
  if batch['dps']==70:
   reproduced=[]
   def solve(rad):
    td=tail(rad)
    def fun(bb):
     U0,P0=travel(rad,bb)
     return P0-om*(td+U0)
    bb=mp.findroot(fun,(b*mp.mpf('0.9999'),b*mp.mpf('1.0001')),tol=mp.mpf('1e-60'),maxsteps=30)
    U0,P0=travel(rad,bb)
    tt=-td-U0
    assert abs(om*tt+P0)<mp.mpf('1e-55')
    out['new_neighbor_solved_cases']+=1
    return tt
   for eps in [mp.mpf('0.0001'),mp.mpf('0.00005')]:
    lo=R*(1-eps);hi=R*(1+eps)
    tl=solve(lo);th=solve(hi)
    dtau=mp.quad(lambda r:1/v(r),[lo,hi])
    derivative=dtau/(mp.sqrt(h)*(th-tl))
    reproduced.append(abs(derivative/Z-1))
   discrepancy=max(abs(q-mp.mpf(z)) for q,z in zip(reproduced,saved['arrival_relative_errors']))
   assert discrepancy<mp.mpf('1e-35')
   assert reproduced[1]<mp.mpf('.4')*reproduced[0]<mp.mpf('1e-6')
   record['reproduced_derivative_errors']=[mp.nstr(x,70) for x in reproduced]
   record['saved_derivative_error_maximum_difference']=mp.nstr(discrepancy,70)
  out['records'].append(record)
  print(json.dumps(record),flush=True)
out['status']='PASS';out['elapsed_seconds']=time.time()-start
out['peak_rss_KiB']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
(B/'saved_artifact_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'finite_endpoint_evaluations':out['finite_endpoint_evaluations'],'new_neighbor_solved_cases':out['new_neighbor_solved_cases']}),flush=True)
