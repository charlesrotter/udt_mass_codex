#!/usr/bin/env python3
"""SD1 full-metric finite support. Reuses BE1 field evaluator; not independent geometry code."""
import sys
sys.dont_write_bytecode=True
import argparse,importlib.util,json,math,pathlib,platform,traceback
import numpy as np
import scipy
import sympy as sp
from numpy.polynomial.legendre import leggauss
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('be1',ROOT/'udt_broader_evolving_signal_geometry_2026-09-13/check_broader.py')
be=importlib.util.module_from_spec(spec);spec.loader.exec_module(be)
XA=.7;K=.75;TH=K*XA;C1=math.cos(TH);C2=math.cos(2*TH)
V=-K*math.tan(TH)*(1+2*C1*C1)
MUT=False;GUARDS=[]
def guard(name,error,tol):
 error=float(error);GUARDS.append({'name':name,'error':error,'tolerance':tol})
 assert np.isfinite(error) and error<=tol,(name,error,tol)
def profile(Q,eta): return be.Profile((1,2),((Q-C2*eta)/C1,eta),(0,0))
def parameter_fields(Q,eta,t,x):
 base=profile(Q,eta);plus=profile(Q,eta+1);minus=profile(Q,eta-1)
 f=base.parts(t,x);p=plus.parts(t,x);m=minus.parts(t,x)
 # Exact polarization of a quadratic polynomial, not a small-step approximation.
 return f,(p[0]-m[0])/2,(p[5]-m[5])/2

def record(Q,eta,d,n):
 nodes,weights=leggauss(n);u=d*(nodes+1)/2;weights=weights*d/2
 f,pe,le=parameter_fields(Q,eta,1+d,XA+d)
 p,pt,px,_,_,lam,_=f
 logR=(lam-4*math.log(.75))/4-math.log1p(d)/4
 vals=[parameter_fields(Q,eta,1+z,XA+z) for z in u]
 minus=[];plus=[];dminus=[];dplus=[];constraint=[]
 for f0,peta,leta in vals:
  P,Pt,Px,_,_,la,_=f0
  t=1+u[len(minus)];W=math.exp(la/2)/t**1.5
  fm=W*math.exp(-P);fp=W*math.exp(P)
  minus.append(fm);plus.append(fp);dminus.append(fm*(leta/2-peta));dplus.append(fp*(leta/2+peta))
  constraint.append(t*(Pt+Px)**2)
 Im=float(weights@minus);Ip=float(weights@plus)
 Dy=math.sqrt(1+d)*math.exp(p/2)*Im/.75
 Dz=math.sqrt(1+d)*math.exp(-p/2)*Ip/.75
 H=p+math.log(Im/Ip);dH=pe+float(weights@dminus)/Im-float(weights@dplus)/Ip
 if MUT:
  # Actual changed readout: omit the full receiver beam rulers.
  Dy=Im/.75;Dz=Ip/.75;H=math.log(Im/Ip);dH=float(weights@dminus)/Im-float(weights@dplus)/Ip
 r=1.5*(-K*((Q-C2*eta)/C1)*math.sin(TH)-2*K*eta*math.sin(2*TH));q=1.5*Q
 return {'Q':Q,'eta':eta,'d':d,'quadrature_nodes':n,'a1':(Q-C2*eta)/C1,'q':q,'r':r,'v':V,
         'logR':logR,'R':math.exp(logR),'H':H,'Dy':Dy,'Dz':Dz,'area':Dy*Dz,
         'deta_logR':le/4,'deta_H':dH,'lambda_endpoint':lam,'P_endpoint':p,
         'I_minus':Im,'I_plus':Ip,'lapse_integral':float(weights@constraint),
         'clock_leading':(q*q-1)/4,'clock_second':1/8-q*q/8+q*r/2,
         'shape_second':r/3+q*(1-q*q)/12,'clock_derivative_second':9*Q*V/8,'shape_derivative_second':V/2}

def symbolic():
 u,d,q,r=sp.symbols('u d q r',real=True)
 pp=q*u+(-q/2+r)*u*u;ww=1+(q*q-3)*u/2
 ints=[]
 for sign in [-1,1]:
  integrand=sp.series(ww*sp.exp(sign*pp),u,0,3).removeO()
  ints.append(sp.integrate(integrand,(u,0,d))/d)
 h=sp.series(pp.subs(u,d)+sp.log(ints[0])-sp.log(ints[1]),d,0,3).removeO().expand()
 lr=sp.series(-sp.log(1+d)/4+sp.integrate((1+u)*(q+(-q+2*r)*u)**2,(u,0,d))/4,d,0,3).removeO().expand()
 assert sp.simplify(h-(r/3+q*(1-q*q)/12)*d*d)==0
 assert sp.simplify(lr-((q*q-1)*d/4+(sp.Rational(1,8)-q*q/8+q*r/2)*d*d))==0
 th,k=sp.symbols('theta k',real=True)
 raw=k*(sp.cos(2*th)*sp.sin(th)/sp.cos(th)-2*sp.sin(2*th))
 assert sp.trigsimp(raw+k*sp.tan(th)*(1+2*sp.cos(th)**2))==0
 return {'logR_series':str(lr),'H_series':str(h),'v_identity':'EXACT_SYMPY','scope':'Exact truncated algebra; prose analytic remainder and source hypotheses are separately reviewed.'}

def main():
 global MUT
 ap=argparse.ArgumentParser();ap.add_argument('--omit_endpoint_rulers',action='store_true');args=ap.parse_args();MUT=args.omit_endpoint_rulers
 out={'scope':'SD1 conditional marked two-mode finite FLOAT64 support; no interval/noise/global inference','mutation':MUT,'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},'records':[],'parameter_difference_checks':[],'convergence':[],'guards':GUARDS}
 try:
  out['symbolic']=symbolic()
  for Q in (0.,.3*C1):
   for eta in (-.15,0.,.15):
    f=profile(Q,eta).parts(1.,XA)
    guard('initial_P',abs(f[0]),2e-11);guard('initial_lambda',abs(f[5]-4*math.log(.75)),2e-11);guard('initial_Q',abs(f[1]-1.5*Q),2e-11)
    sequence=[]
    for j in range(5):
     d=.2/2**j;a=record(Q,eta,d,32);b=record(Q,eta,d,64)
     for key in ['logR','H','Dy','Dz','deta_logR','deta_H']:
      guard('quadrature_'+key,abs(a[key]-b[key]),2e-10)
     guard('original_lapse_along_ray',abs(b['lambda_endpoint']-4*math.log(.75)-b['lapse_integral']),2e-11)
     assert b['Dy']>0 and b['Dz']>0
     fd=[]
     for dh in (1e-4,5e-5):
      lo=record(Q,eta-dh,d,32);hi=record(Q,eta+dh,d,32)
      df={key:(hi[key]-lo[key])/(2*dh) for key in ['logR','H']}
      guard('eta_difference_logR',abs(df['logR']-b['deta_logR']),2e-7)
      guard('eta_difference_H',abs(df['H']-b['deta_H']),2e-7)
      fd.append({'step':dh,'derivatives':df})
     out['parameter_difference_checks'].append({'Q':Q,'eta':eta,'d':d,'checks':fd})
     out['records'].append({'base':a,'tight':b});sequence.append(b)
    for name,estimate,target in [
      ('clock_second',lambda a:(a['logR']-a['clock_leading']*a['d'])/a['d']**2,'clock_second'),
      ('shape_second',lambda a:a['H']/a['d']**2,'shape_second'),
      ('clock_rank',lambda a:a['deta_logR']/a['d']**2,'clock_derivative_second'),
      ('labelled_shape_rank',lambda a:a['deta_H']/a['d']**2,'shape_derivative_second')]:
     errors=[abs(estimate(a)-a[target]) for a in sequence]
     gate=abs(sequence[0][target])>1e-14
     if gate:guard('leading_convergence_'+name,errors[-1],.8*errors[0]+1e-8)
     out['convergence'].append({'Q':Q,'eta':eta,'quantity':name,'d_values':[a['d'] for a in sequence],'estimates':[estimate(a) for a in sequence],'target':sequence[0][target],'absolute_errors':errors,'nonzero_leading_gate':gate})
  zero=[a['tight'] for a in out['records'] if a['tight']['Q']==0]
  for neg in [a for a in zero if a['eta']==-.15]:
   pos=next(a for a in zero if a['eta']==.15 and a['d']==neg['d'])
   for k1,k2 in [('R','R'),('Dy','Dz'),('Dz','Dy'),('area','area')]:guard('zero_Q_exact_symmetry_'+k1,abs(neg[k1]-pos[k2]),2e-11)
  out['status']='PASS';out['guard_count']=len(GUARDS)
 except Exception as e:
  out['status']='FAIL';out['exception']=repr(e);print(json.dumps(out,indent=2));traceback.print_exc();return 1
 print(json.dumps(out,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
