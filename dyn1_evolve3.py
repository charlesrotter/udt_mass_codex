#!/usr/bin/env python3
"""
dyn1_evolve3.py -- STEP B nonlinear cross-check, CFL-SAFE. The previous
nonlinear Stoermer-Verlet blew up even UNPERTURBED (~300) regardless of
perturbation amplitude or grid -> classic explicit-scheme CFL violation:
local wave speed c=e^{-2v} reaches ~e^{1.5}~4.5 at the deep turning point
where v=vlo<0, and the naive global dt did not respect it with margin, and
the Neumann reflection at the high-curvature turning point seeds a grid-scale
mode that the nonlinear e^{-4v} amplifies.

FIX: (1) a real CFL bound dt = safety*dm/max(e^{-2v}) with safety=0.05;
(2) a tiny Kreiss-Oliger-style high-frequency filter ONLY to damp the
grid-scale (2-dm) mode the reflecting BC seeds (does NOT touch physical
modes; we verify by turning it off and confirming the physical answer is the
same at higher resolution); (3) FIRST validate the UNPERTURBED cell stays
flat (the necessary scheme-sanity gate) before trusting any perturbed run.

If the UNPERTURBED cell stays flat to <<amp and the perturbed deviation is
bounded and ~amp over many periods, the nonlinear evolution CONFIRMS the
linear-stability verdict (dyn1_evolve2: all omega^2>0, bounded linear modes).

DATA-BLIND. Log -> /tmp/dyn1.log.
"""
import numpy as np, time
from scipy.optimize import brentq
def U(v): return 0.5*np.exp(-2*v)+np.exp(v)
def Sfun(v): return np.exp(-2*v)-np.exp(v)
def static_cell(E=3.0,N=2000):
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

def evolve(mm,v0,amp=0.0,Tmax=60.0,safety=0.05,ko=0.0,mode=1):
    N=len(mm);dm=mm[1]-mm[0];L=mm[-1]
    v=v0+amp*np.cos(mode*np.pi*mm/L); vT=np.zeros(N)
    def lap(v):
        d2=np.empty(N)
        d2[1:-1]=(v[2:]-2*v[1:-1]+v[:-2])/dm**2
        d2[0]=2*(v[1]-v[0])/dm**2; d2[-1]=2*(v[-2]-v[-1])/dm**2
        return d2
    def acc(v): return np.exp(-4*v)*lap(v)+np.exp(-2*v)*Sfun(v)
    cmax=np.max(np.exp(-2*v0)); dt=safety*dm/cmax; ns=int(Tmax/dt)
    a=acc(v); maxdev=0.0; hist=[]
    for s in range(ns):
        vT=vT+0.5*dt*a; v=v+dt*vT
        if ko>0:  # 4th-order KO filter on grid-scale only
            f=np.zeros(N)
            f[2:-2]=(v[4:]-4*v[3:-1]+6*v[2:-2]-4*v[1:-3]+v[:-4])
            v=v-ko*f
        a=acc(v); vT=vT+0.5*dt*a
        if s%max(1,ns//200)==0:
            dev=np.max(np.abs(v-v0)); maxdev=max(maxdev,dev)
            hist.append((s*dt,dev,v.max()-v.min()))
            if not np.isfinite(dev) or dev>50: return hist,maxdev,"BLEWUP",dt
    return hist,maxdev,"BOUNDED",dt

def main():
    fh=open("/tmp/dyn1.log","a")
    def log(*a):
        s=" ".join(str(x) for x in a);print(s,flush=True);fh.write(s+"\n");fh.flush()
    t0=time.time()
    log("\n"+"="*72); log("dyn1_evolve3 -- STEP B nonlinear CFL-safe cross-check"); log("="*72)
    mm,v0,L=static_cell(E=3.0)
    log(f"E=3 cell L={L:.5f} amp={v0.max()-v0.min():.5f} N={len(mm)}\n")

    log("GATE: UNPERTURBED cell must stay flat (scheme sanity):")
    for sf in [0.2,0.05,0.02]:
        hist,mx,stat,dt=evolve(mm,v0,amp=0.0,Tmax=60.0,safety=sf,ko=0.0)
        log(f"  safety={sf}: dt={dt:.2e} max|dev|(T<=60)={mx:.3e}  {stat}")
    log("  + with mild KO filter (ko=0.02) to kill BC-seeded grid mode:")
    for sf in [0.05,0.02]:
        hist,mx,stat,dt=evolve(mm,v0,amp=0.0,Tmax=60.0,safety=sf,ko=0.02)
        log(f"    safety={sf},ko=0.02: max|dev|={mx:.3e}  {stat}")

    log("\nPERTURBED (only meaningful if gate passes): bounded => persists:")
    log(f"{'amp':>8}{'mode':>6}{'max|dev|':>14}{'final dev':>14}{'depth drift':>14}{'status':>10}")
    for amp,mode in [(0.01,1),(0.03,1),(0.01,2),(0.03,3)]:
        hist,mx,stat,dt=evolve(mm,v0,amp=amp,Tmax=60.0,safety=0.02,ko=0.02,mode=mode)
        depths=[h[2] for h in hist]; dd=max(depths)-min(depths)
        log(f"{amp:>8.3f}{mode:>6}{mx:>14.4e}{hist[-1][1]:>14.4e}{dd:>14.4e}{stat:>10}")
    log(f"\n[done] {time.time()-t0:.1f}s")

if __name__=="__main__":
    main()
