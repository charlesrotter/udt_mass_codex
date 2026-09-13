"""Source-exposed independent full affine metric trajectories and finite screens.
No BE1/CSS/NTB science imports. Common NumPy/SciPy libraries disclosed.
"""
import json,sys,platform,hashlib
from pathlib import Path
import numpy as np
import scipy
from scipy.special import jv,yv
from scipy.integrate import solve_ivp,quad
BASE=Path(__file__).resolve().parents[1]
INFILE=BASE/'checks/broader_complete_capture.stdout'
DATA=json.loads(INFILE.read_text())
PARAM={n:p for n,p in DATA['profiles'].items()}
COEFF={}
for name,(ns,aa,pp) in PARAM.items():
 w=.75*np.asarray(ns);COEFF[name]=(w,np.asarray(aa),np.asarray(pp),-3*np.pi*yv(0,w)/4,3*np.pi*jv(0,w)/4)

def metric(t,x,name):
 w,amps,ph,A,B=COEFF[name]
 f=A*jv(0,w*t)+B*yv(0,w*t);d=-w*(A*jv(1,w*t)+B*yv(1,w*t));th=w*x+ph
 c=np.cos(th);s=np.sin(th)
 P=np.dot(amps,f*c);Pt=np.dot(amps,d*c);Px=-np.dot(amps,w*f*s)
 lam=4*np.log(.75);lt=0.;lx=0.
 for i in range(len(w)):
  ff,dd,ww,aa,tt=f[i],d[i],w[i],amps[i],th[i]
  lam+=aa*aa*(t*t*(dd*dd+ww*ww*ff*ff)/2+t*ff*dd/2-9/8+t*ff*dd*np.cos(2*tt)/2)
  lt+=aa*aa*t*((dd*dd+ww*ww*ff*ff)+(dd*dd-ww*ww*ff*ff)*np.cos(2*tt))/2
  lx-=aa*aa*t*ff*dd*ww*np.sin(2*tt)
  for j in range(i+1,len(w)):
   vv,bb,h,hd,ps=w[j],amps[j],f[j],d[j],th[j]
   cp=t*(ww*ff*hd+vv*h*dd)/(ww+vv);cm=t*(ww*ff*hd-vv*h*dd)/(ww-vv)
   lam+=aa*bb*(cp*np.cos(tt+ps)+cm*np.cos(tt-ps))
   lt+=aa*bb*t*((dd*hd-ww*vv*ff*h)*np.cos(tt+ps)+(dd*hd+ww*vv*ff*h)*np.cos(tt-ps))
   lx-=aa*bb*((ww+vv)*cp*np.sin(tt+ps)+(ww-vv)*cm*np.sin(tt-ps))
 N=np.exp(lam/4)*t**(-.25);ell=np.array([N,np.sqrt(t)*np.exp(P/2),np.sqrt(t)*np.exp(-P/2)])
 inv=np.array([-1/N**2,1/N**2,np.exp(-P)/t,np.exp(P)/t])
 it=inv*np.array([-.5*lt+.5/t,-.5*lt+.5/t,-1/t-Pt,-1/t+Pt])
 ix=inv*np.array([-.5*lx,-.5*lx,-Px,Px])
 return inv,it,ix,ell

def rhs(lam,z,name):
 inv,it,ix,_=metric(z[0],z[1],name);p=z[4:]
 return np.r_[inv*p,-.5*np.dot(it,p*p),-.5*np.dot(ix,p*p),0.,0.]

def propagate(t0,x0,s,t1,name,tight=True):
 ell=metric(t0,x0[0],name)[3];sign=1 if t1>t0 else -1
 ini=np.r_[t0,x0,-sign*ell[0],ell*s]
 def stop(l,z):return z[0]-t1
 stop.terminal=True;stop.direction=sign
 sol=solve_ivp(lambda l,z:rhs(l,z,name),(0,100),ini,events=stop,method='DOP853',
  rtol=2e-12 if tight else 2e-11,atol=2e-14 if tight else 2e-13,max_step=.07 if tight else .14)
 assert sol.success and len(sol.t_events[0])==1,sol.message
 end=sol.y_events[0][0];null=[]
 for z in sol.y.T:
  inv=metric(z[0],z[1],name)[0];p=z[4:];null.append(abs(np.dot(inv,p*p))/(1+np.sum(abs(inv*p*p))))
 return end,dict(affine_end=float(sol.t_events[0][0]),steps=len(sol.t),max_null=float(max(null)),endpoint=end.tolist())

def screen(s):
 s=np.asarray(s);s=s/np.linalg.norm(s)
 trial=np.array([0.,0.,1.]) if abs(s[2])<.9 else np.array([0.,1.,0.])
 a=np.cross(s,trial);a/=np.linalg.norm(a)
 return np.column_stack([a,np.cross(s,a)])

def beam(t0,x0,se,t1,name,end,delta):
 Ee=screen(se);ell=metric(t1,end[1],name)[3];p=end[5:];so=p/ell;so/=np.linalg.norm(so);Eo=screen(so)
 cols=[]
 for j in range(2):
  xp=propagate(t0,x0,(se+delta*Ee[:,j])/np.sqrt(1+delta**2),t1,name)[0]
  xm=propagate(t0,x0,(se-delta*Ee[:,j])/np.sqrt(1+delta**2),t1,name)[0]
  cols.append(Eo.T@(ell*(xp[1:4]-xm[1:4])/(2*delta)))
 D=np.column_stack(cols)
 return D,Ee,Eo

def err(a,b):return float(np.max(np.abs(np.asarray(a)-np.asarray(b))/(1+np.abs(b))))
def clock(t,x,name):return quad(lambda u:metric(u,x,name)[3][0],1,t,epsabs=2e-12,epsrel=2e-12)[0]
def check(value,tol,label):
 assert np.isfinite(value) and value<tol,(label,value,tol)

out={'exposure':'Written after whole candidate/code/outcome exposure; no parent science imports. Same scipy Bessel/integrator library, different full-affine equations and finite-angle beam method.','input':str(INFILE),'input_sha256':hashlib.sha256(INFILE.read_bytes()).hexdigest(),'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},'records':[],'reverse':[],'events':[]}
for row in DATA['records']:
 name=row['epsilon'];te=row['te'];to=row['to'];se=np.array(row['source_sky']);x0=np.array(row['initial'][:3])
 end,diag=propagate(te,x0,se,to,name);base=propagate(te,x0,se,to,name,False)[0]
 ell=metric(to,end[1],name)[3];R=1/np.linalg.norm(end[5:]/ell);so=end[5:]/ell*R
 D1,Ee,Eo=beam(te,x0,se,to,name,end,2e-4);D2,_,_=beam(te,x0,se,to,name,end,1e-4)
 expected=Eo.T@np.array(row['arrival_screen'])@np.array(row['screen_map'])@np.array(row['source_screen']).T@Ee
 errors={'null':diag['max_null'],'endpoint':err(end[1:4],[1.7,1.2,.7]),'covariant_spatial_momentum':err(end[5:],row['state'][3:6]),'frequency_ratio':err(R,row['R']),'arrival_sky':err(so,row['arrival_sky']),'tight':err(end,base),'screen_map':err(D2,expected),'finite_angle_refinement':err(D2,D1),'widths':err(np.linalg.svd(D2,compute_uv=False),row['widths']),'area':err(abs(np.linalg.det(D2)),row['area']),'source_clock':err(clock(te,.7,name),row['source_clock']),'arrival_clock':err(clock(to,1.7,name),row['arrival_clock'])}
 for label,val in errors.items():check(val,3e-7 if label in ['screen_map','finite_angle_refinement','widths','area'] else 2e-8,label)
 out['records'].append({'profile':name,'source_clock':row['source_clock'],'errors':errors,'independent_R':R,'independent_screen_map':D2.tolist(),'central':diag})
for row in DATA['reverse']:
 f=row['forward_input'];name=f['epsilon'];te=f['te'];to=f['to'];x0=np.array(f['state'][:3]);se=-np.array(f['arrival_sky'])
 end,diag=propagate(to,x0,se,te,name);D,Ee,Eo=beam(to,x0,se,te,name,end,1e-4);ar=abs(np.linalg.det(D))
 errors={'central_endpoint':err(end[1:4],f['initial'][:3]),'reverse_area':err(ar,row['reverse_area']),'reciprocity':err(f['area']/ar,f['R']**2),'null':diag['max_null']}
 for label,val in errors.items():check(val,3e-7,label)
 out['reverse'].append({'profile':name,'errors':errors,'independent_reverse_area':ar,'independent_reverse_map':D.tolist(),'central':diag})
for ev in DATA['events']:
 name=ev['profile'];rows=[r for r in DATA['records'] if r['epsilon']==name]
 dur=clock(rows[1]['to'],1.7,name)-clock(rows[0]['to'],1.7,name)
 results=[]
 for n in [8,16]:
  nd=[r for r in ev['nodes'] if r['n']==n];xx,ww=np.polynomial.legendre.leggauss(n)
  assert len(nd)==n
  value=.4*np.dot(ww,[r['R'] for r in nd]);check(err(value,ev['quad'+str(n)]),1e-13,'saved_quadrature')
  results.append(float(value))
 check(err(dur,results[1]),2e-8,'duration_saved_nodes')
 out['events'].append({'profile':name,'independent_endpoint_duration':dur,'saved_nodes_reintegrated':results,'error':err(dur,results[1]),'scope':'Independent metric proper-clock integral and saved node values; node boundary solves NOT independently replayed.'})
out['status']='PASS'
print(json.dumps(out,indent=2,allow_nan=False))
