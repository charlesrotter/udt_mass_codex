"""Independent original-metric/proper-time controls; see CHECK_PLAN.md."""
import json, platform
from pathlib import Path
import sympy as s
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

t,r,theta,phi=s.symbols('t r theta phi', real=True)
coords=(t,r,theta,phi)
f=s.Function('f')(r)
g=s.diag(-f,1/f,r*r,r*r*s.sin(theta)**2)
ginv=g.inv()
Gamma={}
for a in range(4):
 for b in range(4):
  for c in range(4):
   Gamma[a,b,c]=s.simplify(sum(ginv[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in range(4)))
def curv(a,b,c,d):
 return s.simplify(s.diff(Gamma[a,d,b],coords[c])-s.diff(Gamma[a,c,b],coords[d])+sum(Gamma[a,c,e]*Gamma[e,d,b]-Gamma[a,d,e]*Gamma[e,c,b] for e in range(4)))
frame=(1/s.sqrt(f),s.sqrt(f),1/r,1/(r*s.sin(theta)))
def A(i,j,k,l):
 return s.simplify(g[l,l]*curv(l,k,i,j)*frame[i]*frame[j]*frame[k]*frame[l])
pairs=((1,0,0,1),(2,0,0,2),(3,0,0,3),(1,2,2,1),(1,3,3,1),(2,3,3,2))
values=[A(*p) for p in pairs]
targets=(s.diff(f,r,2)/2,s.diff(f,r)/(2*r),s.diff(f,r)/(2*r),-s.diff(f,r)/(2*r),-s.diff(f,r)/(2*r),(1-f)/r**2)
assert all(s.simplify(a-b)==0 for a,b in zip(values,targets))
Ric=s.Matrix(4,4,lambda a,b:s.simplify(sum(curv(c,b,c,a) for c in range(4))))
radial=s.simplify(Ric[0,0]/f+Ric[1,1]*f)
tangential=s.simplify(Ric[0,0]/f+Ric[2,2]/r**2)
assert radial==0
quartic=s.simplify(tangential.subs(f,1-r**4).doit())
assert quartic==-5*r**2
parallel=s.simplify(s.diff(1/s.sqrt(f),r)+Gamma[0,1,0]/s.sqrt(f))
assert parallel==0
# Recover the boosted contraction directly from original-coordinate curvature.
# At r=1/4, mu=1/64, kappa=2, f=3/4: a genuine regular static point.
U=(s.Rational(5,4),0,0,s.Rational(3,4))
n=(0,0,1,0)
C=s.simplify(-sum(n[i]*U[j]*U[k]*n[l]*A(i,j,k,l) for i in range(4) for j in range(4) for k in range(4) for l in range(4) if n[i]*U[j]*U[k]*n[l]))
fk=1-s.Rational(1,32)/r-2*r*r
boost=s.simplify(C.subs(f,fk).doit().subs(r,s.Rational(1,4)))
assert boost==-s.Rational(11,16)
unboost=[s.simplify(-values[i].subs(f,fk).doit().subs(r,s.Rational(1,4))) for i in range(3)]
assert unboost==[4,1,1]
null_at_control=s.simplify(tangential.subs(f,fk).doit())
assert null_at_control==0

def run(rtol,atol,max_step,h):
 def fun(tau,y):
  tc,rr,T,V=y
  ff=1-rr**4; fp=-4*rr**3
  return (T,V,-fp*T*V/ff,-ff*fp*T*T/2+fp*V*V/(2*ff))
 rr0=0.25; ff0=1-rr0**4; E0=np.sqrt(ff0)
 sol=solve_ivp(fun,(0,0.7),(0,rr0,1/E0,0),method='DOP853',rtol=rtol,atol=atol,max_step=max_step,dense_output=True)
 assert sol.success
 def rs(rr):return (np.arctanh(rr)+np.arctan(rr))/2
 def arrival(emission):
  tau=brentq(lambda z:sol.sol(z)[0]-rs(sol.sol(z)[1])-emission,0,0.7,xtol=5e-15,rtol=1e-14)
  tc,rr,T,V=sol.sol(tau)
  return dict(emission=emission,tau=tau,t=tc,r=rr,residual=tc-rs(rr)-emission)
 aa=[arrival(e) for e in (-h,0,h)]
 p=(aa[2]['tau']-aa[0]['tau'])/(2*h)
 tau=aa[1]['tau']; tc,rr,T,V=sol.sol(tau)
 returns=[]
 for shift in (-h,0,h):
  yc=sol.sol(tau+shift)
  returns.append(dict(relay_tau=tau+shift,return_t=yc[0]+rs(yc[1]),relay_r=yc[1]))
 q=(returns[2]['return_t']-returns[0]['return_t'])/(2*h)
 farr=1-rr**4; energy=farr*T
 pe=energy+V; qe=1/(energy-V)
 yc=sol.sol(np.linspace(0,0.7,141)); ff=1-yc[1]**4
 norm=float(np.max(np.abs(-ff*yc[2]**2+yc[3]**2/ff+1)))
 er=float(np.max(np.abs(ff*yc[2]-E0)))
 assert norm<1e-10 and er<1e-10
 assert max(abs(x['residual']) for x in aa)<1e-12
 assert abs(p-pe)<2e-9 and abs(q-qe)<2e-9
 assert p>1 and q>1
 return dict(rtol=rtol,atol=atol,max_step=max_step,h=h,arrivals=aa,returns=returns,p=p,q=q,p_endpoint=pe,q_endpoint=qe,energy_residual=er,normalization_residual=norm,max_r=float(max(yc[1])))
results=[run(1e-11,1e-13,0.003,0.0002),run(1e-12,1e-14,0.0015,0.0001)]
dp=results[1]['p']-results[0]['p'];dq=results[1]['q']-results[0]['q']
assert abs(dp)<2e-9 and abs(dq)<2e-9
saved=json.loads(Path('udt_goal_research_campaign_2026-10-13/researcher_b/checks/arrival_01.stdout').read_text())
prod=saved['runs'][-1]
raw=prod['outgoing']
producer_raw_p=(raw[-1]['arrival_tau']-raw[0]['arrival_tau'])/(raw[-1]['emission']-raw[0]['emission'])
comparison=dict(saved_raw_p_recomputed=producer_raw_p,p_difference=results[-1]['p']-producer_raw_p,q_difference=results[-1]['q']-prod['q_fd'])
assert abs(comparison['p_difference'])<2e-9 and abs(comparison['q_difference'])<2e-9
output=dict(python=platform.python_version(),sympy=s.__version__,numpy=np.__version__,scipy=scipy.__version__,exact_curvature=dict(zip(map(str,pairs),map(str,values))),radial_null_Ricci=str(radial),tangential_null_Ricci=str(tangential),quartic_tangential_null_Ricci=str(quartic),parallel_preparation_residual=str(parallel),adverse_boost_C=str(boost),unboosted_C=list(map(str,unboost)),null_Ricci_adverse=str(null_at_control),runs=results,refinement=dict(p=dp,q=dq),producer_comparison=comparison,passed=True,limits='Independent code and proper-time evolution; shared Python/SymPy/SciPy. Floating diagnostics are not interval proof, global coverage or physical adoption.')
print(json.dumps(output,indent=2))
