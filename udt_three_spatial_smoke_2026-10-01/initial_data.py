"""Supplied CMC/conformally-flat initial data for CONDITIONAL Ric=0 only."""
import argparse, io, json
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import LinearOperator, cg

def frequencies(n, period):
    return np.meshgrid(*([2*np.pi*np.fft.fftfreq(n,d=period/n)]*3),indexing='ij')

def gradient(a, freq):
    f=np.fft.fftn(a,axes=(0,1,2));extra=(None,)*(a.ndim-3)
    return [np.fft.ifftn(1j*k[(...,)+extra]*f,axes=(0,1,2)).real for k in freq]

def construct(n, amplitude=1., period=2*np.pi, tau=-1.):
    # FREE supplied comparison data; no values here select a UDT history/scale.
    x=np.meshgrid(*([np.arange(n)*period/n]*3),indexing='ij')
    phase=[0.17,0.43,-0.29];amps=amplitude*np.array([.06,.045,.03])
    seed=np.broadcast_to(np.diag([2/3,-1/3,-1/3]),(n,n,n,3,3)).copy()
    bx=np.diag([0.,1.,-1.]);by=np.diag([1.,0.,-1.]);bz=np.array([[0.,1.,0.],[1.,0.,0.],[0.,0.,0.]])
    for i,mat in enumerate([bx,by,bz]):seed+=amps[i]*np.cos(2*np.pi*x[i]/period+phase[i])[...,None,None]*mat
    a2=np.einsum('...ij,...ij->...',seed,seed);freq=frequencies(n,period);k2=sum(k*k for k in freq)
    def lap(a):return np.fft.ifftn(-k2*np.fft.fftn(a)).real
    def residual(p):return -8*lap(p)-a2*p**(-7)+(2/3)*tau*tau*p**5
    psi=np.full((n,n,n),(a2.mean()/((2/3)*tau*tau))**(1/12))
    history=[]
    for iteration in range(20):
        r=residual(psi);err=float(np.max(np.abs(r)));history.append(err)
        if err<1e-11:break
        potential=7*a2*psi**(-8)+(10/3)*tau*tau*psi**4
        op=LinearOperator((n**3,n**3),matvec=lambda z:(-8*lap(z.reshape(psi.shape))+potential*z.reshape(psi.shape)).ravel(),dtype=float)
        pre=LinearOperator(op.shape,matvec=lambda z:np.fft.ifftn(np.fft.fftn(z.reshape(psi.shape))/(8*k2+potential.mean())).real.ravel(),dtype=float)
        delta,info=cg(op,-r.ravel(),M=pre,rtol=1e-12,atol=1e-14,maxiter=200)
        if info!=0:raise RuntimeError(('CONSTRAINT_LINEAR_SOLVE',info))
        scale=1.
        for backtrack in range(20):
            trial=psi+scale*delta.reshape(psi.shape)
            if trial.min()>0 and np.max(np.abs(residual(trial)))<err:break
            scale*=.5
        else:raise RuntimeError('CONSTRAINT_LINE_SEARCH')
        psi=trial
    else:raise RuntimeError(('CONSTRAINT_NONCONVERGENCE',history))
    gamma=psi[...,None,None]**4*np.eye(3)
    extrinsic=psi[...,None,None]**(-2)*seed+(tau/3)*gamma
    g=np.zeros((n,n,n,4,4));v=np.zeros_like(g)
    g[...,0,0]=-1.;g[...,1:,1:]=gamma;v[...,1:,1:]=-2*extrinsic
    # DERIVED harmonic compatibility for supplied initial lapse1/shift0.
    v[...,0,0]=2*tau
    for i,d in enumerate(gradient(np.log(psi),freq)):
        v[...,0,i+1]=v[...,i+1,0]=-2*d
    return dict(g=g,v=v,gamma=gamma,K=extrinsic,psi=psi,seed=seed,period=np.array(period),
                tau=np.array(tau),amplitude=np.array(amplitude),constraint_history=np.array(history))

def exact_control(kind,n,t,period=2*np.pi):
    x=np.meshgrid(*([np.arange(n)*period/n]*3),indexing='ij')
    g=np.zeros((n,n,n,4,4));v=np.zeros_like(g);acc=np.zeros_like(g)
    if kind=='flat':g[:]=np.diag([-1.,1.,1.,1.])
    elif kind=='kasner':
        p=np.array([1.,-1/3,2/3,2/3]);sign=np.array([-1.,1.,1.,1.])
        for i in range(4):
            g[...,i,i]=sign[i]*np.exp(2*p[i]*t);v[...,i,i]=2*p[i]*g[...,i,i];acc[...,i,i]=4*p[i]**2*g[...,i,i]
    elif kind=='gauge_wave':
        direction=np.ones(3)/np.sqrt(3);k=2*np.pi/period;omega=np.sqrt(3)*k
        theta=k*sum(x)-omega*t;h=1-.05*np.sin(theta);ht=.05*omega*np.cos(theta);htt=.05*omega**2*np.sin(theta)
        g[...,0,0]=-h;v[...,0,0]=-ht;acc[...,0,0]=-htt
        outer=np.outer(direction,direction)
        g[...,1:,1:]=np.eye(3)+(h-1)[...,None,None]*outer
        v[...,1:,1:]=ht[...,None,None]*outer;acc[...,1:,1:]=htt[...,None,None]*outer
    else:raise ValueError(kind)
    return g,v,acc

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('output');ap.add_argument('--n',type=int,required=True);ap.add_argument('--amplitude',type=float,default=1.)
    args=ap.parse_args();data=construct(args.n,args.amplitude)
    buf=io.BytesIO();np.savez_compressed(buf,**data)
    with Path(args.output).open('xb') as f:f.write(buf.getvalue())
    print(json.dumps({'n':args.n,'amplitude':args.amplitude,'residual_history':data['constraint_history'].tolist(),'psi_min':float(data['psi'].min()),'psi_max':float(data['psi'].max())}))
