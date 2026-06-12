import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

def aplus(q,s): return (-(1-2*q)+np.sqrt((1-2*q)**2+16*s))/2
def ishoot(q,s,lam,w2,x0=None,rtol=1e-12):
    if x0 is None: x0=-max(40.0,8.0/max(q,1e-6))
    a=aplus(q,s); den=(a+q)**2+(1-2*q)*(a+q)-4*s; c=lam/den
    e0=np.exp(q*x0)
    def rhs(x,y):
        u,up=y
        return [up,-(1-2*q)*up+(lam*np.exp(q*x)+4*s+w2*np.exp((2+2*q)*x))*u]
    sol=solve_ivp(rhs,[x0,0.0],[1+c*e0,a+c*(a+q)*e0],rtol=rtol,atol=1e-14)
    return sol.y[0,-1],sol.y[1,-1]
def L0(q,s,lam):
    u,up=ishoot(q,s,lam,0.0); return up/u

# lam -> 0 limit check
print("L0(1/3,1/9,1e-8) =", L0(1/3,1/9,1e-8), " a+ =", aplus(1/3,1/9))
# critical angular barrier for BC-c at q=1/3
lc = brentq(lambda lam: L0(1/3,1/9,lam)-2/3, 1e-6, 2.0, xtol=1e-12)
print("lambda_c(BC-c, q=1/3) =", lc)
for qv in (0.25, 0.45, 0.49):
    s=qv*(1-qv)/2
    lc=brentq(lambda lam: L0(qv,s,lam)-2*qv, 1e-6, 3.0, xtol=1e-12)
    print(f"lambda_c(BC-c, q={qv}) = {lc:.6f}")
# margins at q edge
for lam in (2.0,6.0,12.0):
    for qv in (0.4999,):
        s=qv*(1-qv)/2
        print(f"lam={lam} q={qv}: BC-c margin 2q-L0 = {2*qv-L0(qv,s,lam):.6f}")
