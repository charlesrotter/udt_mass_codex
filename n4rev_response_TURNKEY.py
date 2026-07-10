#!/usr/bin/env python3
"""
n4rev_response_TURNKEY.py -- corrected + MMS-validated hopfion backreaction pipeline.

Closes the two gaps that left H4-N4 at "outcome D":
  * the GREENBUG (old green_response inverted the WRONG operator, ~8x inflated) -> replaced
    by the canonical, unit-tested L_bare inverse (lbare_inverse.py).
  * the N4a screening omission -> the phi far-field is now solved on the TRUE screened
    background (Zf(r^2 dphi')' + 8 e^{-2 phi_amb} dphi = src), so clean-vs-screened is decided,
    not assumed.

Stages (each validated before use):
  (S1) transverse response   delta_h = -L_bare^{-1} T      [roots {1,2}; validated in lbare_inverse]
  (S2) flux-mass             dq = -delta_m  (sign AND magnitude now trustworthy, GREENBUG gone)
  (S3) SCREENED phi far-field -> clean 1/r monopole (phi_amb > 1/2 ln(32/Zf)) vs
                                 r^{-1/2} cos(w ln r) screened (deeper)         [N4a correction]

TO RUN FOR REAL: regenerate the H3 Q_H=1 field (hopfion_arc_scripts_2026-07-05/, checkpoints
were not committed), shell-project its transverse stress to T_thth(r), T_phph(r), then call
run(r, Tthth, Tphph, Zf=..., phi_amb=<ambient depth at the object>).  Everything else is fixed.

Discipline: DATA-BLIND; no particle labels/masses; no G=8piT (native 2K->phi channel only).
The model_stress() below is ONLY to exercise the machinery -- its sign is NOT a physics verdict.
"""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lbare_inverse import lbare_solve_bvp     # validated L_bare^{-1}

# ---------- S3 operator: screened phi BVP  Zf(r^2 f')' + 8 e^{-2 pa} f = S ----------
def build_Lphi(r, Zf, phi_amb):
    N=len(r); L=np.zeros((N,N)); k=8.0*np.exp(-2*phi_amb)
    for i in range(1,N-1):
        hm=r[i]-r[i-1]; hp=r[i+1]-r[i]; ri=r[i]
        cm2=2/(hm*(hm+hp)); cp2=2/(hp*(hm+hp)); c02=-(cm2+cp2)
        cm1=-hp/(hm*(hm+hp)); cp1=hm/(hp*(hm+hp)); c01=(hp-hm)/(hm*hp)
        L[i,i-1]=Zf*(ri**2*cm2+2*ri*cm1)
        L[i,i]  =Zf*(ri**2*c02+2*ri*c01)+k
        L[i,i+1]=Zf*(ri**2*cp2+2*ri*cp1)
    L[0,0]=1.0; L[-1,-1]=1.0
    return L

def solve_Lphi(r,S,Zf,phi_amb,f_lo,f_hi):
    L=build_Lphi(r,Zf,phi_amb); rhs=S.copy(); rhs[0]=f_lo; rhs[-1]=f_hi
    return np.linalg.solve(L,rhs)

# ---------- MMS validation ----------
def mms_Lphi():
    print("== S3 screened-phi MMS (manufactured f -> source -> recover; expect rate ~4) ==")
    Zf=1.0
    for phi_amb in [3.0,1.0]:
        k=8*np.exp(-2*phi_amb); e={}
        for Nr in (61,121,241):
            r=np.linspace(0.5,6.0,Nr); f=np.sin(r)/r
            fp=np.cos(r)/r-np.sin(r)/r**2
            fpp=-np.sin(r)/r-2*np.cos(r)/r**2+2*np.sin(r)/r**3
            S=Zf*(r**2*fpp+2*r*fp)+k*f
            e[Nr]=np.max(np.abs(solve_Lphi(r,S,Zf,phi_amb,f[0],f[-1])-f))
        rate=e[121]/e[241]
        print(f"  phi_amb={phi_amb} ({'shallow' if np.exp(-2*phi_amb)<1/32 else 'deep'}): "
              f"{e[61]:.2e}->{e[121]:.2e}->{e[241]:.2e} rate={rate:.2f} "
              f"{'PASS' if rate>3.5 else 'CHECK'}")

# ---------- model stress (REPLACE with real H3 shell projection) ----------
def model_stress(r, trace_target=-90.1, shear_target=139.1):
    R0,w=1.5,0.7; shell=np.exp(-((r-R0)/w)**2)
    base=-shell; shr=shell**2
    def si(f): return 4*np.pi*np.trapezoid(r**2*f,r)
    base*= trace_target/si(2*base); shr*= shear_target/si(2*shr)
    Ttt=base+shr; Tpp=base-shr
    return Ttt,Tpp

def si(r,f): return 4*np.pi*np.trapezoid(r**2*f,r)

# ---------- pipeline ----------
def run(r=None, Tthth=None, Tphph=None, Zf=1.0, phi_amb=3.0):
    model = r is None
    if model:
        r=np.linspace(0.3,6.0,241); Tthth,Tphph=model_stress(r)
    abar=lbare_solve_bvp(r,-Tphph,0.0,0.0)      # S1
    bbar=lbare_solve_bvp(r,-Tthth,0.0,0.0)
    def ddr(f):
        g=np.zeros_like(f); g[1:-1]=(f[2:]-f[:-2])/(r[2:]-r[:-2]); g[0]=g[1]; g[-1]=g[-2]; return g
    ap,bp=ddr(abar),ddr(bbar)
    ell2=(-2*r**2*ap*bp+2*r*(abar*ap+abar*bp+bbar*ap+bbar*bp)
          -3*abar**2-2*abar*bbar-3*bbar**2)/(4*r**4)          # S2 flux density
    dq=np.trapezoid(ell2,r)/Zf
    dphi=solve_Lphi(r,-2.0*ell2,Zf,phi_amb,0.0,0.0)           # S3 screened
    m=(r>4.0); Am=np.vstack([np.ones(m.sum()),1/r[m]]).T
    (C0,C1),*_=np.linalg.lstsq(Am,dphi[m],rcond=None)
    crit=0.5*np.log(32/Zf)
    print(f"\n== PIPELINE {'(MODEL -- machinery only)' if model else '(REAL field)'} "
          f"Zf={Zf} phi_amb={phi_amb} crit={crit:.3f} ==")
    print(f"  sectors: trace={si(r,Tthth+Tphph):+.1f}  shear={si(r,Tthth-Tphph):+.1f}")
    print(f"  S2 flux-mass: dq={dq:+.4e} -> delta_m={-dq:+.4e} "
          f"({'NEGATIVE=prime risk' if -dq<0 else 'POSITIVE'})")
    print(f"  S3: {'SHALLOW clean 1/r mass' if phi_amb>crit else 'DEEP screened (no clean monopole)'}; "
          f"monopole C1={C1:+.4e}")
    return dq,C1

if __name__=='__main__':
    mms_Lphi()
    run(phi_amb=3.0)   # shallow ambient
    run(phi_amb=1.0)   # deep ambient (same stress) -> screened
