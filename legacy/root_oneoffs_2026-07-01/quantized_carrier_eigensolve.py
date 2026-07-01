#!/usr/bin/env python3
"""
quantized_carrier_eigensolve.py  (v2 -- overflow-safe, fixed-grid R-scan)
================================================================================
DIRECT eigensolve cross-check of the quantized native carrier (NOT WKB) + the
honest sign/stability reconciliation + clean depth-dependence read.

Agent: claude-opus-4-8[1m].  Date: 2026-06-19.  STRUCTURE-FIRST, DATA-BLIND. NOT canon.

v1 hit (a) exp overflow from a badly-factored lambdified V_L and (b) eig non-conv at
huge R (inner node r->0, FD 1/r-strain). v2: V_eff written in STABLE closed form (only
e^{-t}, e^{-2t}, t=(r/a)^2) and a FIXED inner core r_core + FIXED grid spacing h across
the R-scan (per the verifier's correction: hold the grid to test R-independence cleanly;
per single-cell-spectrum-box-controlled: deep core excluded, flagged).
"""
import numpy as np
from scipy.linalg import eigh_tridiagonal
def hr(s): print("\n"+"="*78+"\n"+s+"\n"+"="*78)

# STABLE closed form. v0=-D e^{-t}, t=(r/a)^2.  s=(ln M)'=2 v0' = 4D (r/a^2) e^{-t}.
#   V_L = (1/2) s' - (1/4) s^2.
#   s'  = 4D/a^2 * e^{-t} * (1 - 2t)               [since d/dr(r e^{-t}) = e^{-t}(1-2t)]
#   s^2 = 16 D^2 (r^2/a^4) e^{-2t} = 16 D^2 t /a^2 * e^{-2t}
#   => V_L = (2D/a^2) e^{-t}(1-2t)  -  (4 D^2 t /a^2) e^{-2t}
# V_eff = l(l+1) + V_L  (only decaying exponentials -> overflow-safe).
def Veff(rr, Dval, aval, l):
    t = (rr/aval)**2
    et = np.exp(-t); e2t = np.exp(-2*t)
    VL = (2*Dval/aval**2)*et*(1-2*t) - (4*Dval**2*t/aval**2)*e2t
    return l*(l+1) + VL

def eigensolve(Dval,aval,l,R,h=0.004,r_core=0.02):
    """-psi''+V_eff psi=E psi on [r_core,R], Dirichlet both ends. FIXED h (grid held
    across R so R-independence is clean), FIXED inner core (deep r->0 FD-strain excluded)."""
    N = int((R-r_core)/h)
    rr = r_core + h*np.arange(1,N+1)
    V = Veff(rr,Dval,aval,l)
    main = 2.0/h**2 + V
    off  = -1.0/h**2*np.ones(N-1)
    # lowest 12 eigenvalues only -- fast tridiagonal solver
    k = min(12, N-1)
    E = eigh_tridiagonal(main, off, select='i', select_range=(0,k), eigvals_only=True)
    E.sort()
    return E, l*(l+1)   # V_inf = l(l+1) (v0->0 exterior)

hr("(1) DIRECT eigensolve: intrinsic bound levels below the continuum threshold V_inf")
print(" V_inf=l(l+1) (centrifugal/charge floor; l=1 => 2.0). BOUND: E<V_inf. R-indep test.\n")
for Dval in [1.5,2.0,3.0,4.0]:
    print(f" depth D={Dval}:")
    for R in [8.,16.,32.,64.]:
        E,Vinf=eigensolve(Dval,1.0,1,R)
        b=E[E<Vinf-1e-6]
        print(f"   R={R:5.1f}: V_inf={Vinf:.3f} #bound={len(b):2d}  lowest E_n={np.round(b[:4],5)}")
    print()

hr("(2) SIGN/STABILITY: when does the deep well push omega^2=E below 0 (unstable)?")
print(" omega^2=E>0 required for a STANDING WAVE (validated carrier). E<0 = tachyon.\n")
print(f"   {'D':>5} {'E_0':>11} {'omega^2':>26} {'#bound':>7}")
Dstar=None; prev='+'
for Dval in np.arange(0.5,6.01,0.25):
    E,Vinf=eigensolve(Dval,1.0,1,20.)
    E0=E[0]; nb=int(np.sum(E<Vinf-1e-6))
    sign='POSITIVE (stable wave)' if E0>0 else 'NEGATIVE (TACHYON/unstable)'
    if prev=='+' and E0<0 and Dstar is None: Dstar=Dval
    prev='+' if E0>0 else '-'
    print(f"   {Dval:5.2f} {E0:11.5f} {sign:>26} {nb:7d}")
print(f"\n => stable standing-wave masses require depth below D* ~ {Dstar}: a deeper")
print(f"    dilation well OVER-BINDS and the ground omega^2 goes NEGATIVE (instability).")
print(f"    The physical-mass window is DEPTH-LIMITED (structural fact, 'this a').")

hr("(3a) n-dependence of m_n=sqrt(E_n) within the stable (E_n>0) window")
for Dval in [1.0,1.3,1.6,1.9]:
    E,Vinf=eigensolve(Dval,1.0,1,28.,h=0.004)
    b=E[(E>1e-9)&(E<Vinf-1e-6)]
    if len(b)<2:
        print(f"  D={Dval}: {len(b)} pos bound level(s): {np.round(b,5)}"); continue
    m=np.sqrt(b); n=np.arange(len(m)); logm=np.log(m)
    se=np.std(logm-np.polyval(np.polyfit(n,logm,1),n))
    sh=np.std(m-np.polyval(np.polyfit(np.sqrt(n+0.5),m,1),np.sqrt(n+0.5)))
    sl=np.std(m-np.polyval(np.polyfit(n,m,1),n))
    best=min({'EXP':se,'HO-sqrt':sh,'LINEAR':sl}.items(),key=lambda x:x[1])[0]
    print(f"  D={Dval}: {len(m)} pos levels m_n={np.round(m,4)} m_n/m_0={np.round(m/m[0],4)}")
    print(f"        resid exp={se:.2e} HO={sh:.2e} lin={sl:.2e} -> {best}")

hr("(3b) DEPTH-dependence: binding (V_inf - E_0) vs depth D -- exp or power-law?")
Ds=np.arange(0.6,4.01,0.2); bind=[]; e0=[]
for Dval in Ds:
    E,Vinf=eigensolve(Dval,1.0,1,20.); bind.append(Vinf-E[0]); e0.append(E[0])
bind=np.array(bind); e0=np.array(e0)
g=bind>0
se=np.polyfit(Ds[g],np.log(bind[g]),1); re=np.std(np.log(bind[g])-np.polyval(se,Ds[g]))
sp_=np.polyfit(np.log(Ds[g]),np.log(bind[g]),1); rp=np.std(np.log(bind[g])-np.polyval(sp_,np.log(Ds[g])))
print(f"  log(binding) = {se[0]:+.3f}*D + c     resid={re:.3e}   [EXP-in-D]")
print(f"  log(binding) = {sp_[0]:+.3f}*lnD + c   resid={rp:.3e}   [POWER D^k, k={sp_[0]:.2f}]")
print(f"  -> {'EXPONENTIAL in depth' if re<rp else 'POWER-LAW (~D^%.1f) in depth (NOT exp)'%sp_[0]}")
print(f"  binding(D)={np.round(bind,4)}")
print(f"  E_0(D)    ={np.round(e0,4)}")
print("""
 STRUCTURAL READ (3b): the well DEPTH ~ (v0')^2 ~ D^2 (V_L's -(1/4)s^2 term). The
 dilation amplitude e^{2v0}=e^{-2D e^{-t}} IS exponential in D, but V_eff sees only its
 LOG-DERIVATIVES (Liouville), which are POLYNOMIAL*exponential -> the well depth and the
 binding scale as a POWER of D, NOT exp(D). So the depth amplitude does NOT pass through
 to an exponential MASS law on this radial-carrier route. (Honest: this is the obstruction.)""")

hr("(4) l-dependence (the area-form CHARGE axis) and multiplicity")
print(" Each l shifts the floor by l(l+1) and the centrifugal well; report the floor +")
print(" ground per l (l=1,2,3). l labels the area-form charge sector; (2l+1) = multiplicity.\n")
for l in [1,2,3]:
    E,Vinf=eigensolve(2.0,1.0,l,20.)
    b=E[E<Vinf-1e-6]
    print(f"  l={l}: V_inf=l(l+1)={Vinf:.1f}  #bound={len(b)}  E_0={E[0]:.4f}  (2l+1)={2*l+1}")
print("DONE.")
