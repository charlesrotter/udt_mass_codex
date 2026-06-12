import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import iv, kv

QB, SB = 1/3, 1/9
GAMMA = 2*QB

def L0_closed(q,lam,branch='I'):
    nu=np.sqrt(1+4*q*(1-q))/q
    t0=2*np.sqrt(lam)/q
    if branch=='I':
        wp=0.5*(iv(nu-1,t0)+iv(nu+1,t0)); w=iv(nu,t0)
    else:
        wp=-0.5*(kv(nu-1,t0)+kv(nu+1,t0)); w=kv(nu,t0)
    return -(1-2*q)/2+(q*t0/2)*wp/w

def interior_shoot_K(q,s,lam,w2,x0=-10.0,rtol=1e-13):
    nu=np.sqrt(1+4*q*(1-q))/q
    t0=2*np.sqrt(lam)/q
    tau=t0*np.exp(q*x0/2)
    Kv=kv(nu,tau); Kp=-0.5*(kv(nu-1,tau)+kv(nu+1,tau))
    pre=np.exp(-(1-2*q)*x0/2)
    u0=pre*Kv
    up0=pre*(-(1-2*q)/2*Kv + Kp*tau*(q/2))
    def rhs(x,y):
        u,up=y
        return [up,-(1-2*q)*up+(lam*np.exp(q*x)+4*s+w2*np.exp((2+2*q)*x))*u]
    sol=solve_ivp(rhs,[x0,0.0],[u0,up0],rtol=rtol,atol=1e-300)
    return float(sol.y[0,-1]),float(sol.y[1,-1])

# validate at w2=0
for x0 in (-8.0,-10.0,-12.0):
    u,up=interior_shoot_K(QB,SB,2.0,0.0,x0=x0)
    print("x0",x0,"L0_K shoot:",up/u," closed:",L0_closed(QB,2.0,'K'))

def FK(w2,g=GAMMA,x0=-10.0):
    u,up=interior_shoot_K(QB,SB,2.0,w2,x0=x0)
    return up-g*u

grid=np.linspace(0.01,8.0,80)
vals=[FK(w) for w in grid]
roots=[]
for i in range(len(grid)-1):
    if np.sign(vals[i])!=np.sign(vals[i+1]):
        roots.append(brentq(FK,grid[i],grid[i+1],xtol=1e-12))
print("gamma=2q roots:",roots)
vals0=[FK(w,g=0.0) for w in grid]
roots0=[]
for i in range(len(grid)-1):
    if np.sign(vals0[i])!=np.sign(vals0[i+1]):
        roots0.append(brentq(lambda w: FK(w,g=0.0),grid[i],grid[i+1],xtol=1e-12))
print("gamma=0 roots:",roots0)
# x0 stability of the top root
for x0 in (-8.0,-12.0):
    print(x0, brentq(lambda w: FK(w,x0=x0), 0.5,2.0,xtol=1e-12))
