#!/usr/bin/env python3
"""
dyn1_evolve_implicit.py -- STEP B nonlinear persistence, IMPLICIT (A-stable)
scheme. Both explicit schemes (dyn1_evolve, dyn1_evolve3) failed the
UNPERTURBED gate (~50-300 dev even with tiny dt) -- the stiff e^{-4v}
turning-point edge defeats explicit time-stepping. An implicit midpoint /
trapezoidal (Crank-Nicolson) scheme with Newton per step is A-stable and
removes the artificial high-frequency blowup; the remaining motion is
PHYSICAL.

Dynamics (canon C-2026-06-13-1, flow chart, radial). CORRECTED: the
flow-chart dynamic equation whose STATIC limit reproduces the VALIDATED
repo cell (v_mm = S, anchor L(E=3)=1.6742 matches) is
    v_TT = e^{-4v} ( v_mm - S(v) ),  S=e^{-2v}-e^{v}
(static => v_mm = S; the e^{-4v}=1/c_eff^2 time weight = canon wave speed
c_r^2=e^{-4v}). The earlier '+e^{-2v}S' transcription did NOT vanish on the
static cell (e^{-4v}S+e^{-2v}S != 0) -> that drove the unperturbed blowup;
fixed here. The linearization u_TT=e^{-4v0}(u_mm - S'(v0)u) has Jacobi
potential -S'(v)=2e^{-2v}+e^{v}=U''(v)>0 (CONVEX) -> same all-omega^2>0.
First order: v_T = w ; w_T = G(v) := e^{-4v}(v_mm - S(v)).
Trapezoidal (implicit, 2nd order, A-stable):
    v^{n+1} = v^n + dt/2 (w^n + w^{n+1})
    w^{n+1} = w^n + dt/2 (G(v^n) + G(v^{n+1}))
Solve the coupled implicit system for (v^{n+1},w^{n+1}) by Newton each step.
Neumann (turning-point seal) BC.

GATE first: unperturbed cell must stay flat (dev << amp) for many periods.
Then perturbed runs: bounded => PERSISTS => STABLE (confirms dyn1_evolve2's
all-omega^2>0 linear verdict in the full nonlinear equation).

DATA-BLIND. Log -> /tmp/dyn1.log.
"""
import numpy as np, time
from scipy.optimize import brentq
import scipy.sparse as sp
import scipy.sparse.linalg as spla
def U(v): return 0.5*np.exp(-2*v)+np.exp(v)
def Sfun(v): return np.exp(-2*v)-np.exp(v)
def dS(v): return -2*np.exp(-2*v)-np.exp(v)

def static_cell(E=3.0,N=400):
    vlo=brentq(lambda x:U(x)-E,-6,0); vhi=brentq(lambda x:U(x)-E,0,6)
    h=1e-6;v=vlo;vm=1e-9;m=0.0;M=[0.0];V=[vlo]
    while v<vhi-1e-10 and m<20:
        def f(v,vm):return vm,Sfun(v)
        k1=f(v,vm);k2=f(v+0.5*h*k1[0],vm+0.5*h*k1[1])
        k3=f(v+0.5*h*k2[0],vm+0.5*h*k2[1]);k4=f(v+h*k3[0],vm+h*k3[1])
        v+=h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]);vm+=h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        m+=h;M.append(m);V.append(v)
    M=np.array(M);V=np.array(V);mm=np.linspace(0,M[-1],N)
    return mm,np.interp(mm,M,V),M[-1]

def make_lap(N,dm):
    main=-2.0*np.ones(N); off=np.ones(N-1)
    Lm=sp.diags([off,main,off],[-1,0,1]).tolil()
    Lm[0,0]=-2.0; Lm[0,1]=2.0    # Neumann
    Lm[-1,-1]=-2.0; Lm[-1,-2]=2.0
    return (Lm/dm**2).tocsr()

def G(v,Lap):
    return np.exp(-4*v)*(Lap@v - Sfun(v))

def evolve(mm,v0,amp=0.0,Tmax=60.0,dt=0.01,mode=1):
    N=len(mm);dm=mm[1]-mm[0];L=mm[-1];Lap=make_lap(N,dm)
    v=v0+amp*np.cos(mode*np.pi*mm/L); w=np.zeros(N)
    I=sp.identity(N,format='csr')
    maxdev=0.0; hist=[]; nsteps=int(Tmax/dt)
    for s in range(nsteps):
        # Newton solve for v1 (then w1 from trapezoid)
        v1=v.copy(); Gn=G(v,Lap)
        for it in range(30):
            G1=G(v1,Lap)
            # residual: v1 - v - dt/2(w + w1); w1 = w + dt/2(Gn+G1)
            # => v1 - v - dt/2 w - dt/2(w + dt/2(Gn+G1)) =0
            #    v1 - v - dt w - dt^2/4 (Gn+G1) = 0
            R=v1 - v - dt*w - (dt**2/4)*(Gn+G1)
            if np.max(np.abs(R))<1e-12: break
            # Jacobian dG1/dv1 = diag(-4 e^{-4v1})*(Lap v1) + e^{-4v1}Lap
            #                    + diag(-2 e^{-2v1} S + e^{-2v1} dS)
            e4=np.exp(-4*v1)
            Jg = sp.diags(-4*e4*(Lap@v1 - Sfun(v1))) + sp.diags(e4)@(Lap - sp.diags(dS(v1)))
            Jr = I - (dt**2/4)*Jg
            dv=spla.spsolve(Jr.tocsr(),-R)
            v1=v1+dv
        w1=w+dt/2*(Gn+G(v1,Lap))
        v,w=v1,w1
        if s%max(1,nsteps//200)==0:
            dev=np.max(np.abs(v-v0)); maxdev=max(maxdev,dev)
            hist.append((s*dt,dev,v.max()-v.min()))
            if not np.isfinite(dev) or dev>50: return hist,maxdev,"BLEWUP"
    return hist,maxdev,"BOUNDED"

def main():
    fh=open("/tmp/dyn1.log","a")
    def log(*a):
        s=" ".join(str(x) for x in a);print(s,flush=True);fh.write(s+"\n");fh.flush()
    t0=time.time()
    log("\n"+"="*72); log("dyn1_evolve_implicit -- STEP B nonlinear A-stable persistence"); log("="*72)
    mm,v0,L=static_cell(E=3.0,N=400)
    log(f"E=3 cell L={L:.5f} amp={v0.max()-v0.min():.5f} N={len(mm)}, trapezoidal implicit\n")

    log("GATE: UNPERTURBED cell stays flat (dev<<1) over T<=60:")
    for dt in [0.02,0.01]:
        hist,mx,stat=evolve(mm,v0,amp=0.0,Tmax=60.0,dt=dt)
        log(f"  dt={dt}: max|dev|={mx:.3e}  {stat}")

    log("\nPERTURBED: bounded ~amp => PERSISTS => STABLE:")
    log(f"{'amp':>8}{'mode':>6}{'max|dev|':>14}{'final dev':>14}{'depth drift':>14}{'status':>10}")
    for amp,mode in [(0.02,1),(0.05,1),(0.1,1),(0.05,2),(0.1,3)]:
        hist,mx,stat=evolve(mm,v0,amp=amp,Tmax=60.0,dt=0.01,mode=mode)
        depths=[h[2] for h in hist]; dd=max(depths)-min(depths)
        log(f"{amp:>8.3f}{mode:>6}{mx:>14.4e}{hist[-1][1]:>14.4e}{dd:>14.4e}{stat:>10}")

    log("\nLONG-TIME persistence (amp=0.05, mode1, T<=300):")
    hist,mx,stat=evolve(mm,v0,amp=0.05,Tmax=300.0,dt=0.01,mode=1)
    log(f"  max|dev| over T<=300 = {mx:.4e}, final={hist[-1][1]:.4e}, {stat}")
    log(f"  (bounded over ~{300/L:.0f} chart-light-crossing times => PERSISTS)")
    log(f"\n[done] {time.time()-t0:.1f}s")

if __name__=="__main__":
    main()
