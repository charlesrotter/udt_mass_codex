#!/usr/bin/env python3
"""BE1 finite checks; unchanged CSS/NTB flow reused, not independent trajectory code."""
import sys
sys.dont_write_bytecode=True
import argparse,importlib.util,json,math,pathlib,platform,traceback
import numpy as np
import scipy
import sympy as sp
from scipy.special import jv,yv
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('css',ROOT/'udt_conditional_signal_sequence_2026-09-12/step_03/check_evolving.py')
css=importlib.util.module_from_spec(spec);spec.loader.exec_module(css)
ORIGINAL_FIELDS=css.ntb.fields
ORIGINAL_READOUT=css.readout
MUT=None
PROFILES={'S':((1,2),(.3,0.),(0.,0.)), 'M':((1,2),(.3,.15),(0.,0.)),
          'P':((1,2),(.3,.15),(0.,math.pi/3)), 'N':((1,2),(.3,-.15),(0.,math.pi/3))}
class Profile:
    def __init__(self,modes,amplitudes,phases):
        self.k=.75*np.array(modes,dtype=float);self.a=np.array(amplitudes,dtype=float);self.ph=np.array(phases,dtype=float)
        assert len(self.k)==len(self.a)==len(self.ph) and np.all(self.k>0) and np.all(np.diff(self.k)>0)
        self.aa=-3*np.pi*yv(0,self.k)/4;self.bb=3*np.pi*jv(0,self.k)/4
    def parts(self,t,x):
        f=self.aa*jv(0,self.k*t)+self.bb*yv(0,self.k*t)
        fp=-self.k*(self.aa*jv(1,self.k*t)+self.bb*yv(1,self.k*t))
        theta=self.k*x+self.ph;co=np.cos(theta);si=np.sin(theta)
        P=np.sum(self.a*f*co);Pt=np.sum(self.a*fp*co);Px=-np.sum(self.a*self.k*f*si)
        Pxx=-np.sum(self.a*self.k**2*f*co);Ptx=-np.sum(self.a*self.k*fp*si)
        lf=t*t*(fp*fp+self.k*self.k*f*f)/2+t*f*fp/2-9/8
        lam=4*np.log(.75)+np.sum(self.a*self.a*(lf+t*f*fp*np.cos(2*theta)/2))
        cross=0.
        for i in range(len(f)):
            for j in range(i+1,len(f)):
                cp=t*(self.k[j]*fp[i]*f[j]+self.k[i]*fp[j]*f[i])/(self.k[i]+self.k[j])
                cm=t*(self.k[j]*fp[i]*f[j]-self.k[i]*fp[j]*f[i])/(self.k[j]-self.k[i])
                cross+=self.a[i]*self.a[j]*(cp*np.cos(theta[i]+theta[j])+cm*np.cos(theta[j]-theta[i]))
        if MUT!='drop_cross':lam+=cross
        return P,Pt,Px,Pxx,Ptx,lam,cross
    def fields(self,t,x):
        P,Pt,Px,Pxx,Ptx,lam,_=self.parts(t,x)
        a=lam/4-np.log(t)/4;ax=t*Pt*Px/2;axx=t*(Ptx*Px+Pt*Pxx)/2
        le=np.array([np.exp(a),np.sqrt(t)*np.exp(P/2),np.sqrt(t)*np.exp(-P/2)])
        A=np.array([1.,np.exp(2*a-P)/t,np.exp(2*a+P)/t])
        lx=np.array([0.,2*ax-Px,2*ax+Px]);lxx=np.array([0.,2*axx-Pxx,2*axx+Pxx])
        return le,A,A*lx,A*(lx*lx+lxx)
    def initial_Q(self,x):return float(np.sum(self.a*np.cos(self.k*x+self.ph)))
    def sigma(self):return float(np.sum(self.a*self.a*self.k*(self.aa*self.aa+self.bb*self.bb)/np.pi))
MODELS={n:Profile(*p) for n,p in PROFILES.items()}
def fields(t,x,name):return MODELS[name].fields(t,x)
def readout(te,to,name,state,ini,se,frozen=False,implicit=True):
    row=ORIGINAL_READOUT(te,to,name,state,ini,se,frozen=frozen,implicit=False)
    if not frozen and implicit:
        le=fields(te,css.XA[0],name)[0];lo=fields(to,state[0],name)[0]
        _,pt,px,*_=MODELS[name].parts(te,css.XA[0])
        logs=np.array([-1/(4*te)+te*(pt*pt+px*px)/4,1/(2*te)+pt/2,1/(2*te)-pt/2])
        E=css.ntb.screen(se);M=state[6:].reshape(6,6)
        J=np.column_stack((M[:3,3:]@(le[:,None]*E),css.ntb.flow(to,state,name,False)[:3]))
        we=np.r_[np.zeros(3),le*logs*se]-css.ntb.flow(te,ini,name,False)
        deriv=np.linalg.solve(J,-(M@we)[:3]);value=lo[0]/le[0]*deriv[2]
        css.guard('general_profile_initial_time_clock',css.diff(value,row['R']))
        row['implicit_R']=value
    return row
css.ntb.fields=fields;css.readout=readout

def fd1(f,x,h=1e-4):return (f(x-2*h)-8*f(x-h)+8*f(x+h)-f(x+2*h))/(12*h)
def fd2(f,x,h=1e-3):return (-f(x+2*h)+16*f(x+h)-30*f(x)+16*f(x-h)-f(x-2*h))/(12*h*h)
def exact_checks():
    t=sp.symbols('t',positive=True);ki,kj=sp.symbols('ki kj',positive=True)
    fi=sp.Function('fi')(t);fj=sp.Function('fj')(t)
    sub={sp.diff(fi,t,2):-sp.diff(fi,t)/t-ki**2*fi,sp.diff(fj,t,2):-sp.diff(fj,t)/t-kj**2*fj}
    cp=t*(kj*sp.diff(fi,t)*fj+ki*sp.diff(fj,t)*fi)/(ki+kj)
    cm=t*(kj*sp.diff(fi,t)*fj-ki*sp.diff(fj,t)*fi)/(kj-ki)
    assert sp.simplify(sp.diff(cp,t).subs(sub)-t*(sp.diff(fi,t)*sp.diff(fj,t)-ki*kj*fi*fj))==0
    assert sp.simplify(sp.diff(cm,t).subs(sub)-t*(sp.diff(fi,t)*sp.diff(fj,t)+ki*kj*fi*fj))==0
    q=sp.symbols('Q',real=True);v=[sp.Rational(1,3)-3*q*q/4,-sp.Rational(2,3)-q,-sp.Rational(2,3)+q]
    assert sp.expand(sum(v)**2-sum(x*x for x in v))==0
    assert sp.diff(v[1]+v[2],q)==0
    q0=sp.Rational(9,16);r=-sp.Rational(27,80)*sp.sin(sp.pi/3)
    assert sp.simplify((q0-1)*r)!=0
    return {'mixed_time_identities':'EXACT_SYMPY','initial_constraints':'EXACT_SYMPY','reflection_force_coefficient':str(sp.simplify((q0-1)*r)),'limits':'Symbolic reductions, not independent original tensor construction or theorem counts.'}

def geometry_checks():
    rows=[]
    for name,model in MODELS.items():
        for x in (0.,.7,2.1):
            P,pt,px,_,_,lam,_=model.parts(1.,x);Q=model.initial_Q(x)
            css.guard('initial_P',abs(P),2e-12);css.guard('initial_lambda',abs(lam-4*np.log(.75)),2e-12)
            css.guard('initial_Pt',abs(pt-1.5*Q),2e-12);css.guard('initial_lengths',css.diff(fields(1.,x,name)[0],[.75,1,1]),2e-12)
        for t,x in ((1.2,.2),(2.3,.7),(5.,2.1)):
            P,pt,px,pxx,ptx,lam,cross=model.parts(t,x)
            lt=fd1(lambda u:model.parts(u,x)[5],t);lx=fd1(lambda z:model.parts(t,z)[5],x)
            css.guard('lambda_time_constraint',css.diff(lt,t*(pt*pt+px*px)))
            css.guard('lambda_space_constraint',css.diff(lx,2*t*pt*px))
            le,A,Ax,Axx=fields(t,x,name)
            css.guard('actual_A_spatial_derivative',css.diff(fd1(lambda z:fields(t,z,name)[1],x),Ax))
            css.guard('actual_A_spatial_hessian',css.diff(fd2(lambda z:fields(t,z,name)[1],x),Axx))
            af=lambda u,z:model.parts(u,z)[5]/4-np.log(u)/4
            at=fd1(lambda u:af(u,x),t);ax=fd1(lambda z:af(t,z),x)
            att=fd2(lambda u:af(u,x),t);axx=fd2(lambda z:af(t,z),x)
            ric=[-att+axx-pt*pt/2+at/t+1/(2*t*t),-pt*px/2+ax/t,att-axx-px*px/2+at/t]
            css.guard('original_Ricci_reduction_with_actual_metric_derivatives',max(abs(v) for v in ric))
            integral=quad(lambda u:u*sum(v*v for v in model.parts(u,x)[1:3]),1,t,epsabs=2e-11,epsrel=2e-11)[0]
            css.guard('independent_constraint_integral',css.diff(lam-4*np.log(.75),integral))
            if name=='S':
                for j in range(4):css.guard('single_mode_source_correspondence',css.diff(fields(t,x,name)[j],ORIGINAL_FIELDS(t,x,.3)[j]),2e-12)
            rows.append({'profile':name,'t':t,'xi':x,'lambda':lam,'mixed_lambda':cross,'Ricci_tt_txi_xixi':ric,'integrated_lambda':integral})
    model=MODELS['P'];q=model.parts(1.,0.)[1];r=model.parts(1.,0.)[4]
    val=fd1(lambda t:2*t*model.parts(t,0.)[1]*model.parts(t,0.)[2]/2-model.parts(t,0.)[2],1.)
    css.guard('broken_reflection_initial_force',css.diff(val,(q-1)*r))
    return rows

def serial(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    if isinstance(v,dict):return {k:serial(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [serial(x) for x in v]
    return v

def main():
    global MUT
    ap=argparse.ArgumentParser();ap.add_argument('--mutate',choices=['drop_cross','source_epoch']);args=ap.parse_args();MUT=args.mutate
    if MUT=='source_epoch':css.MUT='source_epoch'
    out={'scope':'BE1 finite FLOAT64 supplied profiles; no interval, generic or observational claim.','mutation':MUT,'profiles':PROFILES,'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},'records':[],'events':[],'reverse':[],'axial':[],'finite_differences':[],'frozen':[]}
    try:
        out['exact']=exact_checks();out['geometry']=geometry_checks()
        for name in MODELS:
            for s in (0.,.8):
                row=css.boundary(s,name);tight=css.boundary(s,name,tight=True)
                for key in ['to','R','arrival_clock','source_sky','arrival_sky','widths','area']:
                    css.guard('tight_'+key,css.diff(row[key],tight[key]))
                row['tight_comparison']={key:serial(tight[key]) for key in ['to','R','arrival_clock','source_sky','arrival_sky','widths','area']}
                out['records'].append(row)
            mid=css.boundary(.4,name,tight=True);minus=css.boundary(.4-1e-4,name,tight=True);plus=css.boundary(.4+1e-4,name,tight=True)
            slope=(plus['arrival_clock']-minus['arrival_clock'])/2e-4
            css.guard('actual_proper_clock_difference',css.diff(slope,mid['R']))
            out['finite_differences'].append({'profile':name,'s':.4,'slope':slope,'R':mid['R'],'minus':minus['arrival_clock'],'plus':plus['arrival_clock']})
            rev=css.reverse(mid);rev['forward_input']=mid
            out['reverse'].append(rev);out['axial'].append(css.axial(name,1.6))
            out['frozen'].append(css.boundary(.8,name,frozen=True))
            estimates=[];nodes_saved=[]
            for n in (8,16):
                x,w=leggauss(n);vals=[]
                for z in x:
                    ss=.4*(z+1);rr=css.boundary(ss,name)
                    vals.append(rr['R']);nodes_saved.append({'n':n,'s':ss,'R':rr['R'],'endpoint_residual':rr['endpoint_residual']})
                estimates.append(.4*float(np.dot(w,vals)))
            start=out['records'][-2];end=out['records'][-1];duration=end['arrival_clock']-start['arrival_clock']
            css.guard('whole_event_quadrature_convergence',css.diff(estimates[0],estimates[1]))
            css.guard('whole_event_endpoints',css.diff(estimates[1],duration))
            out['events'].append({'profile':name,'source_duration':.8,'arrival_duration':duration,'mean_Z':duration/.8,'first_pulse_Z':start['R'],'quad8':estimates[0],'quad16':estimates[1],'nodes':nodes_saved,'Q_A':MODELS[name].initial_Q(css.XA[0]),'S_asymptotic':MODELS[name].sigma()})
        out['status']='PASS';out['failure']=None
    except Exception as exc:
        out['status']='FAIL';out['failure']=repr(exc);out['traceback']=traceback.format_exc()
    out['checks']=css.CHECKS;out['check_count']=len(css.CHECKS)
    print(json.dumps(serial(out),indent=2,allow_nan=False));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
