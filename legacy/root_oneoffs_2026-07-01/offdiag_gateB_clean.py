#!/usr/bin/env python3
"""
offdiag_gateB_clean.py -- GATE B part 2, CLEANED: the defensible on-shell verdict
=================================================================================
OFF-DIAGONAL ANGULAR ROW push. Driver: Claude (Opus 4.8, 1M). 2026-06-13.

WHAT THE NAIVE part-2 RUN EXPOSED (a real obstruction, recorded honestly):
  In the pure C1 dilation action the sphere-shape field w (g_thth=r^2 e^{2w},
  g_phph=r^2 e^{-2w} sin^2 th) is a RUNAWAY FLAT DIRECTION: L(w) decreases
  MONOTONICALLY toward a finite asymptote as w->+inf with NO interior
  stationary point (dL/dw->0 from below, never crossing zero).  There is NO
  on-shell value of w in the dilation action -- it is exactly the off-shell
  TADPOLE direction angular_completeness flagged ("w-tadpole, formed-only,
  scheme-conditional").  Numerically "slaving" w drives the solver up the
  asymptote (w*~14) and the Schur complement evaluated there is MEANINGLESS;
  that fake stationary point is what manufactured the negative Kthth in the
  naive run.  To bound w one would have to ADD a w-confining term -- an
  IMPORT, forbidden by charter principle 1.  So w CANNOT be carried as a
  self-consistently-slaved field on the dilation action alone.

  q = g_rtheta, by contrast, HAS a genuine interior stationary point of L
  (dL/dq crosses zero near q~phi_r phi_th-driven value); q is cleanly
  slaveable by the metric's OWN algebraic EL.

THE DEFENSIBLE ON-SHELL OPERATOR (this script):
  - slave q to its genuine algebraic stationary point (the metric's own EL);
  - hold w = 0 (the canon areal-ROUND sphere: with no on-shell value and no
    confining term, the metric's own static formed cell is areal-round, w=0,
    per C-1/C-2; dynamically sourcing w is OFF-SHELL/IMPORT and is reported
    as the obstruction, not banked);
  - assemble the GATE-A-validated generalized eigenproblem with the resulting
    q-slaved reduced coefficients; read the sign with GRID CONVERGENCE.
  This is the honest on-shell statement the gate asked for: it carries q LIVE
  (slaved by the metric's own EL), makes the off-shell-vs-on-shell distinction
  rigorous (w is the off-shell tadpole; q is on-shell), and resolves whether
  the q-channel ALONE flips the centrifugal sign on-shell.

TEMPLATE TRIPWIRE: verdict = operator CHARACTER (round-only vs shaped-
supported), NOT masses.  No wall numbers.
"""
import time, json, warnings
import numpy as np
import sympy as sp
import scipy.sparse as sps
warnings.filterwarnings('ignore')
from offdiag_gateA import log, gen_spectrum
from offdiag_gateB_selfconsistent import (build_density, formed_background,
                                          grad_phi)

t0 = time.time()
log("=" * 74)
log("GATE B part 2 CLEAN -- q slaved (on-shell), w=0 (off-shell tadpole, the "
    "obstruction)")
log("=" * 74)

L, S = build_density()
r,th,Phi,phi,q,w,phir,phith = S
# reduce to w=0 plane (canon areal-round): substitute w=0 BEFORE q-slaving.
L0 = L.subs(w, 0)
dLdq0 = sp.diff(L0, q)
Hqq0  = sp.diff(L0, q, q)
Hpp0  = sp.Matrix([[sp.diff(L0, a, b) for b in (phi,phir,phith)]
                   for a in (phi,phir,phith)])
Hpq0  = sp.Matrix([sp.diff(sp.diff(L0, a), q) for a in (phi,phir,phith)])
f_dLdq = sp.lambdify((r,th,Phi,phi,q,phir,phith), dLdq0, 'numpy')
f_Hqq  = sp.lambdify((r,th,Phi,phi,q,phir,phith), Hqq0, 'numpy')
f_Hpp  = sp.lambdify((r,th,Phi,phi,q,phir,phith), Hpp0, 'numpy')
f_Hpq  = sp.lambdify((r,th,Phi,phi,q,phir,phith), Hpq0, 'numpy')
log(f"  w=0 reduced action + q-EL + Hessian blocks built  t={time.time()-t0:.1f}s")

def slave_q(rr,tt,Ph,ph,pr,pth):
    qv = 0.0
    for _ in range(80):
        Fq = float(f_dLdq(rr,tt,Ph,ph,qv,pr,pth))
        if abs(Fq) < 1e-14: break
        H = float(f_Hqq(rr,tt,Ph,ph,qv,pr,pth))
        if abs(H) < 1e-14: break
        d = -Fq/H
        # keep metric nondegenerate: q^2 e^{-2phi} < r^2
        lam=1.0
        for _ in range(50):
            qn=qv+lam*d
            if qn**2*np.exp(-2*ph) < 0.9*rr**2: break
            lam*=0.5
        qv += lam*d
    return qv

def onshell_q_coeffs(rr,tt,Ph,ph,pr,pth):
    qv = slave_q(rr,tt,Ph,ph,pr,pth)
    Hpp_=np.array(f_Hpp(rr,tt,Ph,ph,qv,pr,pth),dtype=float).reshape(3,3)
    Hqq_=float(f_Hqq(rr,tt,Ph,ph,qv,pr,pth))
    Hpq_=np.array(f_Hpq(rr,tt,Ph,ph,qv,pr,pth),dtype=float).reshape(3)
    if abs(Hqq_) > 1e-12:
        Hred = Hpp_ - np.outer(Hpq_,Hpq_)/Hqq_
    else:
        Hred = Hpp_
    # CRITICAL: the action-density Hessian carries the volume sqrt(-g4)|_{w=0}
    # = r^2 sin th.  The GATE-A assembler applies the measure W=r^2 sin th
    # ONCE more.  To avoid SQUARING the measure we divide the reduced coeffs
    # by the volume here -> BARE stiffness/potential the assembler then
    # weights correctly.  (Verified: on spherical bg this gives the diagonal
    # K_r=2e^{-4phi}, K_th=2e^{-2phi}/r^2, both POSITIVE.)
    vol = (rr**2 * np.sin(tt))
    if vol < 1e-300: vol = 1e-300
    return dict(qv=qv, Krr=Hred[1,1]/vol, Kthth=Hred[2,2]/vol,
                Vpp=Hred[0,0]/vol)

def assemble_q(phi_bg, r, th, Phival=1.0):
    Nr,Nth = phi_bg.shape
    pr,pth = grad_phi(phi_bg,r,th)
    R=r[:,None]; sinth=np.sin(th)[None,:]; W=(R**2)*sinth
    dr=r[1]-r[0]; dth=th[1]-th[0]
    Kr=np.zeros((Nr,Nth)); Kth=np.zeros((Nr,Nth)); V=np.zeros((Nr,Nth))
    for i in range(Nr):
        for j in range(Nth):
            co=onshell_q_coeffs(r[i],th[j],Phival,phi_bg[i,j],pr[i,j],pth[i,j])
            Kr[i,j]=co['Krr']; Kth[i,j]=co['Kthth']; V[i,j]=co['Vpp']
    idx=np.arange(Nr*Nth).reshape(Nr,Nth)
    rows,cols,vals=[],[],[]
    def add(a,b,v): rows.append(a);cols.append(b);vals.append(v)
    WKr=W*Kr; WKth=W*Kth
    for j in range(Nth):
        for ir in range(Nr-1):
            we=0.5*(WKr[ir,j]+WKr[ir+1,j])*dth/dr; a=idx[ir,j];b=idx[ir+1,j]
            add(a,a,we);add(b,b,we);add(a,b,-we);add(b,a,-we)
    for i in range(Nr):
        for jt in range(Nth-1):
            we=0.5*(WKth[i,jt]+WKth[i,jt+1])*dr/dth; a=idx[i,jt];b=idx[i,jt+1]
            add(a,a,we);add(b,b,we);add(a,b,-we);add(b,a,-we)
    A=sps.csr_matrix((vals,(rows,cols)),shape=(Nr*Nth,Nr*Nth))
    A=A+sps.diags((V*W*dr*dth).ravel()); M=sps.diags((W*dr*dth).ravel())
    return A.tocsr(),M.tocsr(),dict(Kr=Kr,Kth=Kth,V=V)

def _main():
    log("\nq-slaved on-shell verdict (w=0), with GRID CONVERGENCE")
    log(f"{'depth':>6} {'lobe':>5} {'ell':>4} {'Nr':>4} {'Nth':>4} "
        f"{'lam_min':>13} {'nneg':>6} {'Kth<0':>7} {'verdict':>14}")
    rows=[]
    for depth in [1.0, 2.0, 3.0]:
        for (lobe,ell) in [(0.0,0),(0.20,2)]:
            seq=[]
            for (Nr,Nth) in [(25,21),(35,29),(49,41)]:
                phi_bg,rr,tt = formed_background(Nr=Nr,Nth=Nth,depth=depth,
                                                 lobe=lobe,ell=ell)
                A,M,co = assemble_q(phi_bg,rr,tt)
                wv = gen_spectrum(A,M)
                nneg=int(np.sum(wv<-1e-6*max(1.0,abs(wv[-1]))))
                kthn=float(np.mean(co['Kth']<0))
                vd="INDEF(shape)" if nneg>0 else "def(round)"
                log(f"{depth:6.2f} {lobe:5.2f} {ell:4d} {Nr:4d} {Nth:4d} "
                    f"{wv[0]:13.5e} {nneg:6d} {kthn:7.3f} {vd:>14}")
                seq.append((Nr*Nth, wv[0], nneg, kthn))
                rows.append(dict(depth=depth,lobe=lobe,ell=ell,N=Nr*Nth,
                                 lam_min=float(wv[0]),nneg=nneg,kth_neg=kthn))
            # convergence verdict for this config:
            lams=[s[1] for s in seq]; nnegs=[s[2] for s in seq]; Ns=[s[0] for s in seq]
            converging = abs(lams[-1]-lams[-2]) < 0.5*abs(lams[-2]-lams[0]+1e-30) \
                         if lams[0]<0 else True
            frac_trend = nnegs[-1]/Ns[-1] - nnegs[0]/Ns[0]
            log(f"       -> lam_min seq {np.array2string(np.array(lams),precision=4)} "
                f"; nneg/N trend {frac_trend:+.4f} "
                f"({'CONVERGING(physical)' if (lams[-1]<-1e-3 and frac_trend<0) else ('runaway/artifact' if (lams[-1]<-1e-3 and frac_trend>=0) else 'sign-definite')})")
    json.dump(rows, open("/tmp/offdiag_gateB_clean.json","w"))
    log(f"\nGATE B part 2 CLEAN done  t={time.time()-t0:.1f}s")

if __name__ == "__main__":
    _main()
