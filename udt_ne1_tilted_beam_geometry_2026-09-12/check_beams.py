#!/usr/bin/env python3
"""NTB1 same-source verification; independent trajectory checks belong to review/."""
import argparse,json,math,platform,sys,warnings
import numpy as np
import scipy
from scipy.integrate import solve_ivp,quad
import discover_beams as d

ETA=np.diag([-1.,1.,1.,1.])

def boost(v):
    v=np.array(v);v2=v@v;ga=1/math.sqrt(1-v2)
    return np.block([[np.array([[ga]]),-ga*v[None,:]],[-ga*v[:,None],np.eye(3)+(ga-1)/v2*np.outer(v,v)]])

def area(X):
    gram=X.T@X
    return math.sqrt(max(0,float(np.linalg.det(gram))))

def invariant(eps,psi,to=400.,tight=False):
    py,pz=math.cos(psi),math.sin(psi)
    def rhs(t,u):
        f=d.AA*d.jv(0,d.K*t)+d.BB*d.yv(0,d.K*t)
        fp=-d.K*(d.AA*d.jv(1,d.K*t)+d.BB*d.yv(1,d.K*t))
        P=eps*f; ey=py*py*math.exp(-P);ez=pz*pz*math.exp(P);mt=ey+ez
        rr=(ez-ey)/mt;ww=eps*t*fp;qq=ww*ww/4+rr*ww/2
        n=d.fields(t,0.,eps)[0][0]
        Z,Y,I=u
        return [Y/t-(qq-1.75)*Z/t,(1-rr*rr)*ww*ww*Z/(2*t),n/(math.sqrt(t)*mt**1.5)]
    ctrl=(2e-11,2e-13,.1) if tight else (2e-10,2e-12,.2)
    sol=solve_ivp(rhs,(1.,to),(0.,1.,0.),method='DOP853',rtol=ctrl[0],atol=ctrl[1],max_step=ctrl[2],dense_output=True)
    assert sol.success,sol.message
    return sol

def invread(t,u,eps,psi):
    lo=d.fields(t,0.,eps)[0];mt=t*(math.cos(psi)**2/lo[1]**2+math.sin(psi)**2/lo[2]**2)
    dx=lo[0]*u[0];dp=math.sqrt(t*mt)*u[2]
    bgx=3/7*(t**1.5-t**-.25);bgp=3*(t**.75-t**.5)
    return {'t':t,'Z':float(u[0]),'Y':float(u[1]),'I':float(u[2]),'D_xi':float(dx),'D_perp':float(dp),
            'area':float(dx*dp),'shape_ratio':float(dx/dp),'clock_contrast':float(1/math.sqrt(mt)),
            'log_area_contrast_over_t':float(math.log(dx*dp/(bgx*bgp))/t)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mutate',choices=['drop_source_lapse','wrong_reverse_normalization'])
    args=parser.parse_args();checks={};failure=None
    try:
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter('always')
            herrors=[]
            for t,xe,eps,p in [(2.,.7,.5,[.8,.4,-.3]),(8.,-.3,1.,[-.5,.6,.7]),(3.,.2,0.,[1.,.4,.2])]:
                z=np.r_[xe,0.,0.,p];jac=np.column_stack([np.imag(d.flow(t,z.astype(complex)+1e-25j*np.eye(6)[i],eps,False))/1e-25 for i in range(6)])
                actual=d.flow(t,np.r_[z,np.eye(6).ravel()],eps)[6:].reshape(6,6)
                err=float(np.max(np.abs(jac-actual)));herrors.append(err)
                assert err<=2e-8,('hessian_original_flow',err)
            checks['complex_step_hessian_abs_errors']=herrors
            reversals=[]
            for mu,psi,xe in [(.8,.7,.7),(-.8,0.,.7),(0.,math.pi/4,0.)]:
                eps=.5;t=8.;sol,s,E=d.solve(eps,mu,psi,xe,to=t);end=sol.y[:,-1]
                row=d.readout(t,end,eps,E);lo=d.fields(t,end[0],eps)[0];le=d.fields(1.,xe,eps)[0]
                wo=row['frequency'];so=end[3:6]/lo/wo;Eo=d.screen(so);Mf=end[6:].reshape(6,6)
                back=solve_ivp(lambda t,y:d.flow(t,y,eps),(t,1.),np.r_[end[:6],np.eye(6).ravel()],method='DOP853',rtol=2e-10,atol=2e-12,max_step=.2)
                assert back.success,back.message
                Mb=back.y[6:,-1].reshape(6,6);scale=1. if args.mutate=='wrong_reverse_normalization' else wo
                XR=le[:,None]*(Mb[:3,3:]@(scale*lo[:,None]*Eo))
                ar=area(XR);rel=abs(row['area']/(ar*row['clock_ratio']**2)-1)
                err=np.max(np.abs(back.y[:6,-1]-sol.y[:6,0])/(1+np.abs(sol.y[:6,0])))
                symback=np.max(np.abs(Mb@Mf-np.eye(6)))/(1+np.linalg.norm(Mb)*np.linalg.norm(Mf))
                assert rel<=2e-7,('directional_reciprocity',rel)
                assert max(err,symback)<=2e-7,('backward_flow',err,symback)
                ve=[.2,-.1,.15];vo=[-.15,.25,.1];Be=boost(ve);Bo=boost(vo)
                ke=np.r_[1.,s];kv=Be@ke;se=kv[1:]/kv[0];Ev=d.screen(se)
                dke=boost(-np.array(ve))@np.vstack((np.zeros((1,2)),kv[0]*Ev))
                X=lo[:,None]*(Mf[:3,3:]@(le[:,None]*dke[1:]))
                source_area=area(X);srcerr=abs(source_area/(kv[0]**2*row['area'])-1)
                ko=wo*np.r_[1.,so];v4=boost(-np.array(vo))@np.array([1.,0.,0.,0.]);wv=-(ko@ETA@v4)
                J=np.vstack((np.zeros((1,2)),X));Jv=J+ko[:,None]*(v4@ETA@J)[None,:]/wv
                gram=Jv.T@ETA@Jv;obs_area=math.sqrt(max(0,float(np.linalg.det(gram))))
                gramerr=np.max(np.abs(gram-X.T@X))/(1+np.max(np.abs(X.T@X)))
                targeterr=abs(obs_area/source_area-1)
                assert max(srcerr,gramerr,targeterr)<=2e-7,('observer_covariance',srcerr,gramerr,targeterr)
                reversals.append({'mu':mu,'psi':psi,'source_xi':xe,'forward_area':row['area'],'reverse_area':ar,'R':row['clock_ratio'],
                                  'reciprocity_error':rel,'backward_state_error':float(err),'backward_matrix_scaled_error':float(symback),
                                  'source_observer_doppler':float(kv[0]),'target_observer_doppler':float(wv/wo),
                                  'observer_source_area_error':srcerr,'observer_target_area_error':targeterr,'observer_gram_error':float(gramerr)})
            checks['reversal_and_observers']=reversals
            inv=[]
            for eps in (0.,-.5,.5,1.):
                for psi in (0.,math.pi/4,math.pi/2):
                    sol,s,E=d.solve(eps,0.,psi,0.,to=40.);base=d.readout(40.,sol.y[:,-1],eps,E)
                    aux=invariant(eps,psi,40.);ex=invread(40.,aux.y[:,-1],eps,psi)
                    source_factor=.75 if args.mutate=='drop_source_lapse' else 1.
                    measured=np.sort(base['singular_values'])*source_factor;expected=np.sort([ex['D_xi'],ex['D_perp']])
                    err=float(np.max(np.abs(measured-expected)/(1+expected)))
                    assert err<=2e-7,('invariant_width_source_normalization',err,eps,psi)
                    assert ex['Z']>0 and ex['Y']>=1-2e-8,('positive_auxiliary',ex)
                    inv.append({'epsilon':eps,'psi':psi,'scaled_error':err,'auxiliary':ex})
            checks['invariant_full_flow']=inv
            bgs=[]
            for mu,psi in [(.8,.7),(-.8,0.),(0.,math.pi/4)]:
                sol,s,E=d.solve(0.,mu,psi,.7,to=8.);p=sol.y[3:6,0];t=8.
                def hp(u,i,j):
                    # Independently expanded epsilon0 homogeneous Hessian.
                    aa=np.array([1.,9/16*u**-1.5,9/16*u**-1.5]);hh=math.sqrt(np.dot(aa,p*p))
                    return (aa[i]/hh if i==j else 0.)-aa[i]*p[i]*aa[j]*p[j]/hh**3
                B=np.array([[quad(lambda u:hp(u,i,j),1,t,epsabs=1e-11,epsrel=1e-11)[0] for j in range(3)] for i in range(3)])
                err=float(np.max(np.abs(B-sol.y[6:,-1].reshape(6,6)[:3,3:]))/(1+np.max(np.abs(B))))
                assert err<=2e-7,('background_quadrature',err)
                bgs.append({'mu':mu,'psi':psi,'error':err})
            checks['background_quadrature']=bgs
            from pathlib import Path
            raw=json.loads((Path(__file__).parent/'checks/discovery_beams.stdout').read_text())
            c,r=max(((c,r) for c in raw['records'] for r in c['samples']),key=lambda cr:cr[1]['screen_orthogonality_scaled'])
            tight,s,E=d.solve(*(c[x] for x in ('epsilon','mu','psi','source_xi')),to=r['t'],rtol=2e-11,atol=2e-13,step=.1)
            tr=d.readout(r['t'],tight.y[:,-1],c['epsilon'],E)
            re=max(abs(tr[x]-r[x])/(1+abs(tr[x])) for x in ('area','frequency'))
            ste=float(np.max(np.abs(np.array(tr['state'])-r['state'])/(1+np.abs(tr['state']))))
            assert max(re,ste)<=2e-6,('tighter_repeat',re,ste)
            checks['discovery_worst_tighter_repeat']={'case':{k:c[k] for k in ('epsilon','mu','psi','source_xi')},'t':r['t'],'output_error':re,'state_error':ste,'tighter':tr}
            long=[]
            for eps in (-.5,-1/6,1/6,.5):
                for psi in (0.,math.pi/2):
                    sol=invariant(eps,psi);samples=[invread(t,sol.sol(t),eps,psi) for t in (10.,40.,100.,400.)]
                    long.append({'epsilon':eps,'psi':psi,'samples':samples})
            tighter=invariant(.5,0.,tight=True);original=long[-2]['samples'];trep=[invread(t,tighter.sol(t),.5,0.) for t in (10.,40.,100.,400.)]
            err=max(abs(a[k]-b[k])/(1+abs(b[k])) for a,b in zip(original,trep) for k in ('D_xi','D_perp','clock_contrast'))
            assert err<=2e-6,('long_tighter_repeat',err)
            checks['long_reception_illustrations']=long;checks['long_tighter_repeat']={'error':err,'samples':trep}
        status='PASS';warning_text=[str(w.message) for w in ws]
    except Exception as exc:status='FAIL';failure=repr(exc);warning_text=[]
    result={'status':status,'mutation':args.mutate,'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'scope':'Finite float64 consistency/regression, no interval or asymptotic certificate. Shared source field/Hessian code.',
            'checks':checks,'warnings':warning_text,'failure':failure}
    print(json.dumps(result,indent=2,allow_nan=False));return 0 if status=='PASS' else 1
if __name__=='__main__':sys.exit(main())
