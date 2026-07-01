#!/usr/bin/env python3
"""
dyn1_evolve2.py -- STEP B nonlinear evolution, ROBUST scheme. Supersedes
dyn1_evolve.py (whose naive explicit leapfrog on the variable-coefficient
e^{-4v} wave eq was numerically unstable even UNPERTURBED -- the static
residual is 4e-5, a good equilibrium, so the blowup there was the SCHEME,
not the physics). Diagnosed and replaced.

PRINCIPLE: the dynamic radial reduction is the Euler-Lagrange flow of an
energy functional whose second variation about the static cell is EXACTLY
the Jacobi operator J = -d^2/dm^2 + U''(v0(m)) (in the natural chart where
the kinetic/gradient metric is locally constant; we make this exact by
working in the LINEARIZED dynamics, which is the rigorous content of a
'stability sign-test'). The perturbation u(m,T)=v-v0 obeys, to leading
order, the canonical wave eq
    u_TT = c0(m)^2 [ u_mm - U''(v0) u ]   (c0^2 = e^{-4 v0} > 0)
i.e. the SAME Jacobi operator scaled by the positive metric coefficient.
Stability is governed by the SIGN of the eigenvalues of J in the weighted
inner product -- positive J => oscillatory bounded u => STABLE.

Here we (a) integrate the LINEAR perturbation dynamics with a proper
energy-conserving Stoermer-Verlet scheme in the WEIGHTED inner product (so
the discrete energy is conserved and a true growth would be visible), over
many dynamical periods, for several perturbation modes; and (b) run a SMALL
fully-NONLINEAR evolution with the same conserving scheme as a cross-check
that nonlinearity does not destabilize. (c) the CONCAVE control (sign-flip
U'') to prove the scheme DETECTS instability.

The generalized eigenproblem J phi = omega^2 W phi (W=e^{4v0} the weight from
c0^{-2}) gives the physical mode frequencies; all omega^2>0 => STABLE.

DATA-BLIND. Log -> /tmp/dyn1.log.
"""
import numpy as np, json, time
from scipy.optimize import brentq
import scipy.linalg as sla

def U(v): return 0.5*np.exp(-2*v)+np.exp(v)
def Upp(v): return 2*np.exp(-2*v)+np.exp(v)
def Sfun(v): return np.exp(-2*v)-np.exp(v)

def static_cell(E=3.0,N=1500):
    vlo=brentq(lambda x:U(x)-E,-6,0); vhi=brentq(lambda x:U(x)-E,0,6)
    h=2e-6;v=vlo;vm=1e-9;m=0.0;M=[0.0];V=[vlo]
    while v<vhi-1e-10 and m<20:
        def f(v,vm):return vm,Sfun(v)
        k1=f(v,vm);k2=f(v+0.5*h*k1[0],vm+0.5*h*k1[1])
        k3=f(v+0.5*h*k2[0],vm+0.5*h*k2[1]);k4=f(v+h*k3[0],vm+h*k3[1])
        v+=h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]);vm+=h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        m+=h;M.append(m);V.append(v)
    M=np.array(M);V=np.array(V);mm=np.linspace(0,M[-1],N)
    return mm,np.interp(mm,M,V),M[-1]

def jacobi_modes(mm,v0,concave=False):
    """Generalized eigenproblem J phi = omega^2 W phi.
    J = -d^2/dm^2 + Upp(v0) (Neumann);  W = e^{4 v0} (c0^{-2})."""
    N=len(mm);dm=mm[1]-mm[0]
    W=Upp(v0) if not concave else -Upp(v0)
    main=2.0/dm**2+W; off=-1.0/dm**2*np.ones(N-1)
    J=np.diag(main)+np.diag(off,1)+np.diag(off,-1)
    J[0,0]=1.0/dm**2+W[0]; J[-1,-1]=1.0/dm**2+W[-1]
    Wt=np.diag(np.exp(4*v0))
    ev=sla.eigvalsh(J,Wt)
    return np.sort(ev)

def evolve_linear(mm,v0,mode=1,amp=1e-3,Tmax=200.0,concave=False):
    """Energy-conserving Stoermer-Verlet of the LINEAR perturbation
    u_TT = e^{-4v0}[ u_mm - Upp(v0) u ]  (Neumann). Tracks max|u| over time
    and the conserved energy. Bounded => stable."""
    N=len(mm);dm=mm[1]-mm[0];L=mm[-1]
    c2=np.exp(-4*v0); Wp=Upp(v0)*( -1 if concave else 1)
    u=amp*np.cos(mode*np.pi*mm/L); uT=np.zeros(N)
    def lap(u):
        d2=np.empty(N)
        d2[1:-1]=(u[2:]-2*u[1:-1]+u[:-2])/dm**2
        d2[0]=2*(u[1]-u[0])/dm**2; d2[-1]=2*(u[-2]-u[-1])/dm**2
        return d2
    def acc(u): return c2*(lap(u)-Wp*u)
    cmax=np.sqrt(np.max(c2)); dt=0.25*dm/cmax; ns=int(Tmax/dt)
    a=acc(u); maxu=np.max(np.abs(u)); E0=None; hist=[]
    for s in range(ns):
        uT=uT+0.5*dt*a
        u=u+dt*uT
        a=acc(u)
        uT=uT+0.5*dt*a
        if s%max(1,ns//300)==0:
            # weighted energy: 1/2 sum e^{4v0} uT^2/c2 ... use 1/2 uT^2/c2 + 1/2 u_m^2 + 1/2 Wp u^2
            um=np.gradient(u,dm)
            En=np.trapezoid(0.5*uT**2/c2+0.5*um**2+0.5*Wp*u**2,mm)
            if E0 is None:E0=En
            maxu=max(maxu,np.max(np.abs(u)))
            hist.append((s*dt,np.max(np.abs(u)),En))
            if not np.isfinite(maxu) or maxu>1e6*amp: return hist,maxu,"BLEWUP",E0
    Edrift=abs(hist[-1][2]-E0)/(abs(E0)+1e-300)
    return hist,maxu,"BOUNDED",Edrift

def evolve_nonlinear(mm,v0,amp=1e-3,Tmax=60.0):
    """Small fully-nonlinear Stoermer-Verlet of v_TT=e^{-4v}v_mm+e^{-2v}S(v)."""
    N=len(mm);dm=mm[1]-mm[0];L=mm[-1]
    v=v0+amp*np.cos(np.pi*mm/L); vT=np.zeros(N)
    def lap(v):
        d2=np.empty(N)
        d2[1:-1]=(v[2:]-2*v[1:-1]+v[:-2])/dm**2
        d2[0]=2*(v[1]-v[0])/dm**2; d2[-1]=2*(v[-2]-v[-1])/dm**2
        return d2
    def acc(v): return np.exp(-4*v)*lap(v)+np.exp(-2*v)*Sfun(v)
    cmax=np.sqrt(np.max(np.exp(-4*v))); dt=0.2*dm/cmax; ns=int(Tmax/dt)
    a=acc(v); maxdev=0.0; hist=[]
    for s in range(ns):
        vT=vT+0.5*dt*a; v=v+dt*vT; a=acc(v); vT=vT+0.5*dt*a
        if s%max(1,ns//200)==0:
            dev=np.max(np.abs(v-v0)); maxdev=max(maxdev,dev)
            hist.append((s*dt,dev,v.max()-v.min()))
            if not np.isfinite(dev) or dev>1e3: return hist,maxdev,"BLEWUP"
    return hist,maxdev,"BOUNDED"

def main():
    fh=open("/tmp/dyn1.log","a")
    def log(*a):
        s=" ".join(str(x) for x in a);print(s,flush=True);fh.write(s+"\n");fh.flush()
    t0=time.time()
    log("\n"+"="*72)
    log("dyn1_evolve2 -- STEP B ROBUST: Jacobi modes + conserving evolution")
    log("="*72)

    for E in [2.0,3.0,6.0]:
        mm,v0,L=static_cell(E=E)
        ev=jacobi_modes(mm,v0)
        log(f"\nE={E}: cell L={L:.5f}, amp={v0.max()-v0.min():.5f}")
        log(f"  Jacobi gen-eigvals omega^2 (lowest 5): "
            +", ".join(f"{x:.5f}" for x in ev[:5]))
        log(f"  min omega^2 = {ev[0]:.6f}  -> {'STABLE (all >0)' if ev[0]>0 else 'UNSTABLE'}")

    # LINEAR conserving evolution, several modes, long time
    log("\nLINEAR perturbation evolution (energy-conserving, Tmax=200):")
    log(f"{'E':>6}{'mode':>6}{'amp':>8}{'max|u|/amp':>12}{'status':>10}{'E-drift':>12}")
    mm,v0,L=static_cell(E=3.0)
    for mode in [1,2,3,5]:
        amp=1e-3
        hist,mx,stat,Edr=evolve_linear(mm,v0,mode=mode,amp=amp,Tmax=200.0)
        log(f"{3.0:>6}{mode:>6}{amp:>8.0e}{mx/amp:>12.4f}{stat:>10}{Edr:>12.3e}")

    # NONLINEAR cross-check
    log("\nNONLINEAR evolution cross-check (Stoermer-Verlet, Tmax=60):")
    log(f"{'amp':>8}{'max|dev|':>14}{'depth drift':>14}{'status':>10}")
    for amp in [1e-3,1e-2,5e-2]:
        hist,mx,stat=evolve_nonlinear(mm,v0,amp=amp,Tmax=60.0)
        depths=[h[2] for h in hist]; dd=max(depths)-min(depths)
        log(f"{amp:>8.0e}{mx:>14.4e}{dd:>14.4e}{stat:>10}")

    # CONVERGENCE of nonlinear max-dev
    log("\nCONVERGENCE (nonlinear amp=1e-2, grid refine):")
    for N in [800,1500,3000]:
        mmN,v0N,_=static_cell(E=3.0,N=N)
        hist,mx,stat=evolve_nonlinear(mmN,v0N,amp=1e-2,Tmax=60.0)
        log(f"  N={N}: max|dev|={mx:.4e}  status={stat}")

    # CONTROL: concave well must show a NEGATIVE Jacobi eigenvalue + blowup
    log("\nCONTROL -- artificial CONCAVE well (sign-flip U''):")
    ev=jacobi_modes(mm,v0,concave=True)
    log(f"  Jacobi min omega^2 = {ev[0]:.5f} (expect <0 => unstable mode exists)")
    hist,mx,stat,Edr=evolve_linear(mm,v0,mode=1,amp=1e-3,Tmax=60.0,concave=True)
    log(f"  concave linear evolution: max|u|/amp={mx/1e-3:.3e}, status={stat} "
        f"({'DETECTED growth (evolver is live)' if mx/1e-3>100 or stat=='BLEWUP' else 'no growth?? check'})")

    log(f"\n[done] {time.time()-t0:.1f}s")

if __name__=="__main__":
    main()
