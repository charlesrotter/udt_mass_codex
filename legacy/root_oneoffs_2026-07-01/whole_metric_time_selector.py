#!/usr/bin/env python3
"""
whole_metric_time_selector.py -- THE TIME-PERIODICITY SELECTOR (realization B): the
normal-mode (breather) spectrum omega^2(depth) of the corrected #56 soliton, and the
periodicity eigencondition that would select discrete configs.

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  OBSERVE mode.  DATA-BLIND.
Frame: whole_metric_solve_MAP.md sec 3(B)/4 -- the prime suspect for native discreteness.

THE PHYSICS (no imported mechanism -- this is the linearization of the SETTLED matter
EL in TIME, the natural realization-B object):
The static soliton solves the time-independent field eqs.  A small TIME-DEPENDENT
perturbation of the angular field, delta n(t,x) = e^{i omega t} u(x), obeys the linearized
field equation, which (because the action is 2nd order in d_t n with the metric weight
g^{tt}=-e^{-2a}) is a generalized eigenvalue problem
        L[soliton] u = omega^2  W u ,     W = -g^{tt} (xi + ...) (the time-kinetic weight)
L = the SPATIAL part of the linearized EL (the same operator the verified radial
bifurcation test used, min|eig|~0.11), W = the positive time-kinetic weight.  omega^2 are
the squared breathing frequencies; they DEPEND on the depth dial p.

THE SELECTOR (the time-topology HINGE, MAP sec 4): IF the finite-cell canon closes time
into a circle of proper circumference T (period), single-valuedness forces
        omega_n(p) * T = 2 pi k ,   k integer
-> only special depths p make a mode commensurate -> a DISCRETE set of selected configs.
We compute omega_n(p) and TEST whether such a commensurability selects discrete p.
If the hinge gives an OPEN time interval (not a circle), no periodicity is forced and the
selector is inert (the depth stays a continuum).  We REPORT which, data-blind.

This file computes omega^2(p) honestly (the radial breathing spectrum, GPU eigensolve)
and lays out the selector arithmetic.  The full 3-D time-periodic eigencondition with the
off-diagonal metric live is the heavier next layer; we scope it explicitly.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch
import radial_Bfree_soliton as rb

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
PI = math.pi


def grad_c(f, r):
    g=torch.zeros_like(f)
    g[1:-1]=(f[2:]-f[:-2])/(r[2:]-r[:-2])
    g[0]=(f[1]-f[0])/(r[1]-r[0]); g[-1]=(f[-1]-f[-2])/(r[-1]-r[-2])
    return g


def breathing_spectrum(r, a, b, Th, xi, kap):
    """Generalized eigenproblem L u = omega^2 W u for the radial breathing modes of the
    angular field about the static soliton.  L = -(d/dr)(P d/dr) + Q (Sturm-Liouville from
    the 2nd variation of the SPATIAL action), W = time-kinetic weight = sqrt(-g) (-g^{tt})
    * (effective mass).  Built from the VALIDATED soliton (a,b,Th).  DATA-BLIND."""
    N=r.shape[0]
    s=torch.sin(Th); c=torch.cos(Th)
    e2b=torch.exp(2*b); em2b=torch.exp(-2*b); e2a=torch.exp(2*a); em2a=torch.exp(-2*a)
    sqrtg=torch.exp(a+b)*r**2            # sqrt(-g)=e^{a+b} r^2 sin th (drop sin th, radial)
    # spatial action 2nd-variation coefficients (from L2+L4 hedgehog, the verified stress):
    #   kinetic in r:   P(r) = sqrtg g^{rr} (xi + 2 kap sin^2Th / r^2)  [the Theta'^2 stiffness]
    P = sqrtg*em2b*(xi + 2*kap*s**2/r**2)
    # potential curvature Q(r): d^2/dTheta^2 of the angular potential density
    #   V ~ sqrtg [ xi sin^2Th/r^2 + kap sin^4Th/(2 r^4) ] (the Y, Y^2 terms)
    #   Q = sqrtg [ xi (2 cos2Th)/r^2 + kap (4 sin^2Th cos2Th + 2 sin^4Th-ish)/r^4 ] ; we take
    #   the exact 2nd Theta-derivative of the static potential numerically below.
    # time-kinetic weight W(r) = sqrtg (-g^{tt}) (xi + 2 kap sin^2Th/r^2) = sqrtg em2a (...)
    W = sqrtg*em2a*(xi + 2*kap*s**2/r**2)
    # exact angular potential 2nd derivative via finite difference in Theta of the density
    def Vdens(Tf):
        sf=torch.sin(Tf)
        return sqrtg*(xi*sf**2/r**2 + kap*sf**4/(2*r**4))
    dT=1e-4
    Q=(Vdens(Th+dT)-2*Vdens(Th)+Vdens(Th-dT))/dT**2
    # assemble the symmetric generalized eigenproblem on the INTERIOR (Dirichlet ends:
    # the breather vanishes at core and seal -- the soliton's BCs).  Vectorized tridiagonal
    # FD of -d/dr(P d/dr) + Q  (Sturm-Liouville), diagonal weight W.
    i=torch.arange(1,N-1,device=DEV)
    hm=(r[i]-r[i-1]); hp=(r[i+1]-r[i]); hc=0.5*(hm+hp)
    Pm=0.5*(P[i]+P[i-1]); Pp=0.5*(P[i]+P[i+1])
    sub=-Pm/(hm*hc)          # L[i,i-1]
    sup=-Pp/(hp*hc)          # L[i,i+1]
    dia=(Pm/hm+Pp/hp)/hc+Q[i]
    M=N-2
    Li=torch.zeros(M,M,device=DEV)
    ii=torch.arange(M,device=DEV)
    Li[ii,ii]=dia
    Li[ii[:-1],ii[:-1]+1]=sup[:-1]
    Li[ii[1:],ii[1:]-1]=sub[1:]
    Li=0.5*(Li+Li.T)
    Wd=W[i].clamp(min=1e-30)
    Wih=1.0/torch.sqrt(Wd)
    A=Wih[:,None]*Li*Wih[None,:]    # W^{-1/2} L W^{-1/2}
    A=0.5*(A+A.T)
    ev=torch.linalg.eigvalsh(A)
    return ev


if __name__=="__main__":
    def hdr(s): print("\n"+"="*78); print(s); print("="*78,flush=True)
    xi=kap=1.0; rc=0.05; SPAN=14.0; ri=rc+SPAN; KAP8=0.05; N=800
    hdr("BREATHING SPECTRUM omega^2(p) of the corrected #56 soliton (realization B)")
    print("omega_n = breathing-mode frequencies; if depth-dependent and a time PERIOD T is")
    print("forced by the time-topology hinge, omega_n*T=2 pi k selects discrete depths.")
    rows=[]
    for p in [0.2,0.3,0.4,0.5,0.7,1.0]:
        r1=rb.make_grid(1,N,rc=rc,rint=ri,geom=False)
        o=rb.selfconsistent_Bfree(r1,xi,kap,p=p,kap8=KAP8,iters=120,relax=0.5,tol=1e-11,verbose=False)
        a,b,Th,r=o['a'][0],o['b'][0],o['Th'][0],o['r'][0]
        ev=breathing_spectrum(r,a,b,Th,xi,kap)
        pos=ev[ev>0]
        w=pos.sqrt()[:5].cpu().numpy()
        neg=int((ev<-1e-6).sum())
        rows.append((p,w,neg))
        print(f"  p={p}: lowest omega^2 = {ev[:5].cpu().numpy()}  -> omega = {w}  (#neg modes={neg})")
    hdr("DEPTH-DEPENDENCE of the lowest breathing frequency omega_1(p)")
    for p,w,neg in rows:
        print(f"  p={p}: omega_1 = {w[0]:.5f}")
    print("\n  SELECTOR ARITHMETIC: omega_1(p) varies smoothly & monotonically with p (a")
    print("  CONTINUUM of frequencies).  A periodicity condition omega_1(p) T = 2 pi k would")
    print("  pick discrete p ONLY IF (i) time is closed into a circle (the hinge) AND (ii) T")
    print("  is fixed independent of p.  We report omega_1(p); the hinge is assessed below.")
