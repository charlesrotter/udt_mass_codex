import numpy as np
import scipy.sparse as sps
from scipy.sparse.linalg import eigsh
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import kv

def aplus(q,s): return (-(1-2*q)+np.sqrt((1-2*q)**2+16*s))/2

def ishoot(q,s,lam,w2,x0=None,rtol=1e-12):
    if x0 is None: x0 = -max(40.0, 8.0/max(q,1e-6))
    a = aplus(q,s); den=(a+q)**2+(1-2*q)*(a+q)-4*s; c=lam/den
    e0=np.exp(q*x0)
    def rhs(x,y):
        u,up=y
        return [up, -(1-2*q)*up+(lam*np.exp(q*x)+4*s
                                 +w2*np.exp((2+2*q)*x))*u]
    sol=solve_ivp(rhs,[x0,0.0],[1+c*e0,a+c*(a+q)*e0],rtol=rtol,atol=1e-14)
    return sol.y[0,-1],sol.y[1,-1]

def L0(q,s,lam,**kw):
    u,up=ishoot(q,s,lam,0.0,**kw); return up/u

def Dext(w,ell):
    nu=ell+0.5
    kp=-0.5*(kv(nu-1,w)+kv(nu+1,w))
    return -0.5+w*kp/kv(nu,w)

q,s=1/3,1/9
# L0 robustness
for lam in (2.0,6.0,12.0):
    vals=[L0(q,s,lam,x0=x0,rtol=rt) for x0,rt in
          ((-40,1e-12),(-60,1e-12),(-40,1e-10))]
    print(f"L0(lam={lam}): {vals[0]:.10f} {vals[1]:.10f} {vals[2]:.10f}")

# shooting roots, physical gamma=2q
print()
def Fb(lam): return lambda w2: ishoot(q,s,lam,w2)[0]
def Fc(lam,g=2/3):
    def F(w2):
        u,up=ishoot(q,s,lam,w2); return up-g*u
    return F
print("BC-b shoot lam=2:", brentq(Fb(2.0),-30,-27,xtol=1e-11))
print("BC-b shoot lam=6:", brentq(Fb(6.0),-50,-40,xtol=1e-11))
print("BC-c shoot lam=2:", brentq(Fc(2.0),-3.5,-3.0,xtol=1e-12))
print("BC-c shoot lam=6:", brentq(Fc(6.0),-12,-10,xtol=1e-11))
# boosted BC-c gamma=1.5*L0(lam=2)
g15=1.5*L0(q,s,2.0)
print("boosted BC-c gamma=1.5gc shoot:", brentq(Fc(2.0,g15),3.0,5.0,xtol=1e-12))
# boosted BC-a gamma=1.2*(L0+2), ell=1
ga=1.2*(L0(q,s,2.0)+2.0)
def Fa(w2):
    u,up=ishoot(q,s,2.0,w2)
    return up/u-ga-Dext(np.sqrt(w2),1)
print("boosted BC-a shoot:", brentq(Fa,0.5,1.5,xtol=1e-13))

# scale covariance FD
def assemble(q,s,lam,R=1.0,rmin=1e-5,rmax=None,n_int=4000,n_ext=4000,
             bc='c',gamma=None):
    if gamma is None: gamma=2*q/R
    g_int=np.exp(np.linspace(np.log(rmin),np.log(R),n_int)); g_int[-1]=R
    if bc=='a':
        g_ext=np.linspace(R,rmax,n_ext+1)[1:]
        r=np.concatenate([g_int,g_ext]); im=n_int-1
    else:
        r=g_int; im=n_int-1
    h=np.diff(r); rm=0.5*(r[:-1]+r[1:])
    f=np.where(rm<=R,(R/rm)**q,1.0)
    E0=np.where(rm<=R,s/rm**2,0.0)
    Pm=rm**2*f**2; Qm=lam*f+4*rm**2*f**2*E0; Wm=rm**2
    N=len(r); Qn=np.zeros(N); Wn=np.zeros(N)
    Qn[:-1]+=Qm*h/2; Qn[1:]+=Qm*h/2
    Wn[:-1]+=Wm*h/2; Wn[1:]+=Wm*h/2
    if bc!='b': Qn[im]-=gamma*R**2   # form term gamma/R*P(R)=gamma*R... see note
    cp=Pm/h
    d=np.zeros(N); d[:-1]+=cp; d[1:]+=cp
    idx=np.arange(1,N) if bc=='c' else np.arange(1,N-1)
    Kd=d[idx]+Qn[idx]; Ko=-cp[1:len(idx)]
    A=-sps.diags([Ko,Kd,Ko],[-1,0,1],format='csc')
    W=sps.diags(Wn[idx],0,format='csc')
    return A,W
def topE(sig=50.0,**kw):
    A,W=assemble(**kw)
    return np.sort(eigsh(A,k=3,M=W,sigma=sig,which='LM',
                         return_eigenvectors=False))[::-1][0]
# note: physical jump Delta u' = -(2q/R) u(R); form term = (2q/R)*P(R) = 2qR
# with gamma := 2q/R (dimensional jump coeff): form coeff gamma*R^2
for lam in (2.0,):
    e1=topE(q=q,s=s,lam=lam,R=1.0,bc='c',rmin=1e-5,n_int=4000)
    e2=topE(q=q,s=s,lam=lam,R=2.5,bc='c',rmin=1e-5,n_int=5000,sig=10.0)
    print(f"scale cov BC-c lam=2: R=1 w2={e1:.8f}, R=2.5 w2R2={e2*2.5**2:.8f}")
g15d=1.5*L0(q,s,2.0)
e1=topE(q=q,s=s,lam=2.0,R=1.0,bc='c',gamma=g15d/1.0,rmin=1e-5,n_int=4000)
e2=topE(q=q,s=s,lam=2.0,R=2.5,bc='c',gamma=g15d/2.5,rmin=1e-5,n_int=5000,sig=10.0)
print(f"scale cov boosted BC-c: R=1 w2={e1:.8f}, R=2.5 w2R2={e2*2.5**2:.8f}")
