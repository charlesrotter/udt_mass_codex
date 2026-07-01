#!/usr/bin/env python3
"""
dyn1_evolve.py -- STEP B nonlinear cross-check: dynamic evolution of a
perturbed cell. MANDATORY persistence evidence for the 'stable' claim.

The metric's OWN dynamic field equation (canon C-2026-06-13-1), radial
sector, in the validated flow chart v(m):
    e^{2v} v_TT - e^{-2v}( v_mm ) = S(v),     S = Phi(e^{-2v} - e^{v})
(the (2/r)v_r-2v_r^2 geometric terms are the chart Laplacian already folded
into v_mm in the flow chart; we evolve the canonical reduced wave eq with
the canon wave speed structure c^2 ~ e^{-4v} carried by the e^{2v}/e^{-2v}
prefactors). Rearranged for evolution:
    v_TT = e^{-4v} v_mm + e^{-2v} S(v)
The principal symbol has c_eff^2 = e^{-4v} > 0 (canon: strictly hyperbolic,
well-posed). We integrate with explicit leapfrog in T (CFL on local c_eff),
float64. Neumann (turning-point seal) BC at both chart ends.

TEST: take a converged one-bounce cell v0(m) (E=3), add a perturbation
delta*cos(pi m / L), evolve many dynamical times, and measure:
  - amplitude of the deviation (v - v0): bounded (STABLE/persists) or
    growing (UNSTABLE)?
  - the cell DEPTH / MS content over time: holds or disperses?
  - energy conservation (numerical control).
Run several perturbation amplitudes (linear + nonlinear) and a grid refine
for convergence evidence.

ALSO a SEPARATELY-SEEDED unstable control: a cell sitting on a CONCAVE
potential (artificial W<0) MUST blow up -- confirms the evolver can DETECT
instability (so a 'stable' verdict is not just a dead/over-damped scheme).

DATA-BLIND. Log -> /tmp/dyn1.log. GPU optional (this 1D evolve is cheap CPU).
"""
import numpy as np, json, time
from scipy.optimize import brentq

Phi=1.0
def U(v): return 0.5*np.exp(-2*v)+np.exp(v)
def Sfun(v): return np.exp(-2*v)-np.exp(v)   # = -U'(v)

def static_cell(E=3.0, N=1200):
    """Build the one-bounce static cell v0(m) by integrating v_mm=S from the
    inner turning point. Returns uniform m-grid and v0."""
    vlo=brentq(lambda x:U(x)-E, -5, 0)
    vhi=brentq(lambda x:U(x)-E, 0, 5)
    # integrate vlo->vhi (v_m=0 at vlo)
    h=1e-5; v=vlo; vm=0.0; m=0.0; M=[0.0]; V=[vlo]
    # tiny push to leave turning point
    vm=1e-8
    while v<vhi-1e-9 and m<20:
        def f(v,vm): return vm, Sfun(v)
        k1=f(v,vm);k2=f(v+0.5*h*k1[0],vm+0.5*h*k1[1])
        k3=f(v+0.5*h*k2[0],vm+0.5*h*k2[1]);k4=f(v+h*k3[0],vm+h*k3[1])
        v=v+h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        vm=vm+h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        m+=h; M.append(m); V.append(v)
    M=np.array(M);V=np.array(V)
    mm=np.linspace(0,M[-1],N)
    v0=np.interp(mm,M,V)
    return mm, v0, M[-1]

def evolve(mm, v0, pert_amp=0.0, Tmax=40.0, cfl=0.3, pert_mode=1, concave=False):
    """Leapfrog evolve v_TT = e^{-4v} v_mm + e^{-2v} S(v) (Neumann BC).
    If concave: replace S by a CONCAVE-well source (control that MUST blow up)."""
    N=len(mm); dm=mm[1]-mm[0]; L=mm[-1]
    v=v0 + pert_amp*np.cos(pert_mode*np.pi*mm/L)
    # initial velocity 0
    vT=np.zeros(N)
    def lap(v):
        d2=np.empty(N)
        d2[1:-1]=(v[2:]-2*v[1:-1]+v[:-2])/dm**2
        d2[0]=2*(v[1]-v[0])/dm**2      # Neumann
        d2[-1]=2*(v[-2]-v[-1])/dm**2
        return d2
    def accel(v):
        if concave:
            # artificial concave well: S=+ (e^{-2v}+e^{v})  (so U''<0) -> unstable
            S=np.exp(-2*v)+np.exp(v)
            return np.exp(-4*v)*lap(v)+np.exp(-2*v)*S
        return np.exp(-4*v)*lap(v)+np.exp(-2*v)*Sfun(v)
    # CFL: max c_eff = max e^{-2v}; dt = cfl*dm/cmax
    cmax=np.max(np.exp(-2*v))
    dt=cfl*dm/cmax
    nsteps=int(Tmax/dt)
    a=accel(v); vT=vT+0.5*dt*a
    hist=[]
    dev0=None
    for step in range(nsteps):
        v=v+dt*vT
        # enforce Neumann (reflect) implicitly handled by lap stencil
        a=accel(v)
        vT=vT+dt*a
        if step%max(1,nsteps//200)==0:
            dev=np.max(np.abs(v-v0))
            depth=v.max()-v.min()
            energy=np.trapz(0.5*np.exp(2*v)*vT**2 + 0.5*np.exp(-2*v)*np.gradient(v,dm)**2 + np.exp(2*v)*U(v), mm)
            hist.append((step*dt, dev, depth, energy))
            if not np.isfinite(dev) or dev>1e3:
                return hist, "BLEWUP", dt, nsteps
    return hist, "FINITE", dt, nsteps

def main():
    fh=open("/tmp/dyn1.log","a")
    def log(*a):
        s=" ".join(str(x) for x in a);print(s,flush=True);fh.write(s+"\n");fh.flush()
    t0=time.time()
    log("\n"+"="*72)
    log("dyn1_evolve -- STEP B nonlinear evolution / persistence cross-check")
    log("="*72)
    log("v_TT = e^{-4v} v_mm + e^{-2v} S(v), S=e^{-2v}-e^{v}; leapfrog, Neumann.\n")

    mm, v0, L = static_cell(E=3.0)
    log(f"Static one-bounce cell E=3: chart length L={L:.5f}, "
        f"amp={v0.max()-v0.min():.5f}, N={len(mm)} pts.\n")

    # (0) UNPERTURBED: must hold steady (consistency of evolver + static sol)
    log("(0) UNPERTURBED static cell evolved (should stay flat):")
    hist,stat,dt,ns=evolve(mm,v0,pert_amp=0.0,Tmax=40.0)
    devs=[h[1] for h in hist]
    log(f"    status={stat}, dt={dt:.2e}, steps={ns}, max deviation over T<=40: {max(devs):.3e}")
    log(f"    energy drift: {abs(hist[-1][3]-hist[0][3])/abs(hist[0][3]):.3e} (relative)")

    # (1) PERTURBED -- linear and nonlinear amplitudes
    log("\n(1) PERTURBED cell, deviation max over T (bounded=persists=STABLE):")
    log(f"{'pert_amp':>10}{'mode':>6}{'max|dev|':>14}{'final|dev|':>14}{'depth drift':>14}{'status':>10}")
    cat=[]
    for amp,mode in [(0.01,1),(0.05,1),(0.1,1),(0.2,1),(0.05,2),(0.1,3)]:
        hist,stat,dt,ns=evolve(mm,v0,pert_amp=amp,pert_mode=mode,Tmax=40.0)
        devs=[h[1] for h in hist]; depths=[h[2] for h in hist]
        ddrift=max(depths)-min(depths)
        log(f"{amp:>10.3f}{mode:>6}{max(devs):>14.4e}{devs[-1]:>14.4e}{ddrift:>14.4e}{stat:>10}")
        cat.append(dict(amp=amp,mode=mode,maxdev=float(max(devs)),
                        finaldev=float(devs[-1]),status=stat))

    # (2) CONVERGENCE: refine grid, check max-dev stable
    log("\n(2) CONVERGENCE under grid refinement (pert_amp=0.1, mode 1):")
    log(f"{'N':>8}{'max|dev|':>14}{'status':>10}")
    for N in [600,1200,2400]:
        mmN,v0N,_=static_cell(E=3.0,N=N)
        hist,stat,dt,ns=evolve(mmN,v0N,pert_amp=0.1,Tmax=40.0)
        devs=[h[1] for h in hist]
        log(f"{N:>8}{max(devs):>14.4e}{stat:>10}")

    # (3) CONTROL: a concave (artificial) well MUST blow up -> evolver can see
    #     instability (so STABLE is not a dead scheme).
    log("\n(3) CONTROL -- artificial CONCAVE well (U''<0) MUST go unstable:")
    hist,stat,dt,ns=evolve(mm,v0,pert_amp=0.01,Tmax=40.0,concave=True)
    devs=[h[1] for h in hist]
    log(f"    concave-control status={stat}, max|dev|={max(devs):.4e}  "
        f"({'DETECTED instability (good: evolver is live)' if stat=='BLEWUP' or max(devs)>10 else 'did NOT blow up -- check'})")

    json.dump(cat,open("/tmp/dyn1_evolve.json","w"),indent=2)
    log(f"\n[done] {time.time()-t0:.1f}s")

if __name__=="__main__":
    main()
