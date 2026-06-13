#!/usr/bin/env python3
"""
offdiag_gateB_selfconsistent.py -- GATE B part 2: the ON-SHELL verdict
=======================================================================
OFF-DIAGONAL ANGULAR ROW push. Driver: Claude (Opus 4.8, 1M). 2026-06-13.
Consumes offdiag_qw_derive.py (the metric's OWN q,w-extended EL) and the
GATE-A-validated generalized eigensolver (offdiag_gateA).

WHAT offdiag_qw_derive ESTABLISHED (exact, from the C1 dilation action,
nothing added):
  - phi-EL at q=w=0 reduces to the banked wint operator (assembly correct).
  - q and w are ALGEBRAIC fields (NO second-order EL) -- the metric carries
    no kinetic term for them.  So a self-consistent background does NOT
    propagate q,w independently; the metric's OWN EL SLAVES them to the
    phi-gradients (this slaving is FORCED by the geometry, not imposed --
    the distinction the gate demanded between 'algebraic elimination as a
    posited scheme' and 'the field equation being algebraic').
  - the q,w TADPOLES on a phi(r,theta) background are EXACTLY
        EL[q]/( -2|sin| ) = e^{-4phi} phi_r phi_th
        EL[w]/( -2|sin| ) = e^{-2phi} phi_th^2
    NONZERO only when phi is NON-spherical.  On a SPHERICAL phi background
    q=w=0 is exactly ON-SHELL (no tadpole) -- so the angular_completeness
    attractive flip, built by eliminating q,w on a diagonal (q=w=0)
    background, is taken in directions that are ON-SHELL at spherical and
    only become sourced once phi already has angular structure.

THE ON-SHELL SECOND VARIATION (the physical question, posed correctly):
  The honest on-shell operator for the angular (shape) sector is the second
  variation of the FULL action w.r.t. the physical fluctuation, with q,w
  SLAVED to their own algebraic EL (the reduced/constrained Hessian) -- NOT
  the crude global sign-flip (which is the OFF-SHELL operator and is, as
  part 1 showed, an unbounded-below ill-posed object: a wrong-sign Laplacian
  whose 'negatives' diverge under grid refinement -- NOT a physical type).
  We build the reduced Hessian by:
    (1) solve the self-consistent round/formed phi background (wint cell);
    (2) at each point slave q,w to EL[q]=EL[w]=0 (algebraic, the metric's own);
    (3) assemble the second variation of the action in the phi fluctuation
        WITH q,w-slaving folded in (the Schur complement of the full Hessian
        onto the phi block), posed in the GATE-A measure;
    (4) eigh(A_reduced, M): sign-definite (round only) or indefinite (shaped)?

TEMPLATE TRIPWIRE: the verdict is the operator's CHARACTER (does the geometry
support a non-round type), NOT masses.  No wall numbers loaded.
"""
import time, json
import numpy as np
import sympy as sp
import scipy.linalg as sla
import scipy.sparse as sps
from offdiag_gateA import log, gen_spectrum

t0 = time.time()
log("=" * 74)
log("GATE B part 2 -- ON-SHELL second variation (q,w slaved by the metric's "
    "own EL)")
log("=" * 74)

# ---------------------------------------------------------------------
# Build the action density L(phi,q,w; gradients) and its full Hessian
# symbolically ONCE, lambdified for fast pointwise numeric eval.
# We work with the action DENSITY per (r,theta) and treat the fluctuation
# second variation locally in the gradients (the standard reduced-Hessian
# for a first-order action: the principal symbol + the potential Hessian).
# ---------------------------------------------------------------------
def build_density():
    r, th, Phi = sp.symbols('r theta Phi', positive=True)
    phi, q, w = sp.symbols('phi q w', real=True)
    phir, phith = sp.symbols('phir phith', real=True)   # phi gradients
    e2p=sp.exp(2*phi); em2p=sp.exp(-2*phi); e2w=sp.exp(2*w); em2w=sp.exp(-2*w)
    g=sp.zeros(4,4)
    g[0,0]=-em2p; g[1,1]=e2p; g[1,2]=q; g[2,1]=q; g[2,2]=r**2*e2w
    g[3,3]=r**2*em2w*sp.sin(th)**2
    gi=g.inv(); sqrtmg=sp.sqrt(-sp.simplify(g.det()))
    grad=sp.Matrix([0,phir,phith,0])
    Kin=sum(gi[a,b]*grad[a]*grad[b] for a in range(4) for b in range(4))
    Lkin=em2p*Kin*sqrtmg
    Lpot=-Phi*((sp.Rational(1,2))*em2p+sp.exp(phi))*sqrtmg
    L=sp.simplify(Lkin+Lpot)
    return L, (r,th,Phi,phi,q,w,phir,phith)

log("  building action density + Hessian symbolically ...")
L, S = build_density()
r,th,Phi,phi,q,w,phir,phith = S

# Slave q,w: solve dL/dq=0, dL/dw=0 for q,w (algebraic) at each point.
dLdq = sp.diff(L, q); dLdw = sp.diff(L, w)
log("  q,w stationarity equations built; will slave numerically pointwise.")

# Functions for numeric eval:
fL    = sp.lambdify((r,th,Phi,phi,q,w,phir,phith), L, 'numpy')
fdLdq = sp.lambdify((r,th,Phi,phi,q,w,phir,phith), dLdq, 'numpy')
fdLdw = sp.lambdify((r,th,Phi,phi,q,w,phir,phith), dLdw, 'numpy')

# The on-shell action as a function of phi and its gradients ONLY, with q,w
# slaved.  For the second variation in the phi-channel we need, at each point,
# the Hessian of L_onshell w.r.t. (phi, phir, phith).  Because q,w are slaved
# (stationary), the Schur complement = total derivative: d2 L_onshell =
# d2 L - (cross) (Hqw)^-1 (cross)^T evaluated at the slaved q*,w*.
# Build all needed second derivatives symbolically:
vars_phi = (phi, phir, phith)
vars_qw  = (q, w)
log("  building Hessian blocks ...")
Hpp = sp.Matrix([[sp.diff(L, a, b) for b in vars_phi] for a in vars_phi])
Hqq = sp.Matrix([[sp.diff(L, a, b) for b in vars_qw]  for a in vars_qw])
Hpq = sp.Matrix([[sp.diff(L, a, b) for b in vars_qw]  for a in vars_phi])
fHpp = sp.lambdify((r,th,Phi,phi,q,w,phir,phith), Hpp, 'numpy')
fHqq = sp.lambdify((r,th,Phi,phi,q,w,phir,phith), Hqq, 'numpy')
fHpq = sp.lambdify((r,th,Phi,phi,q,w,phir,phith), Hpq, 'numpy')
log(f"  symbolic prep done  t={time.time()-t0:.1f}s")

def slave_qw(rr, tt, Phival, ph, pr, pth):
    """Solve dL/dq=0, dL/dw=0 for (q,w) by damped Newton at one point."""
    qv, wv = 0.0, 0.0
    for _ in range(60):
        Fq = float(fdLdq(rr,tt,Phival,ph,qv,wv,pr,pth))
        Fw = float(fdLdw(rr,tt,Phival,ph,qv,wv,pr,pth))
        if abs(Fq)+abs(Fw) < 1e-13: break
        Hq = fHqq(rr,tt,Phival,ph,qv,wv,pr,pth)
        Hq = np.array(Hq, dtype=float).reshape(2,2)
        try:
            d = np.linalg.solve(Hq, [-Fq, -Fw])
        except np.linalg.LinAlgError:
            break
        # damping to keep q^2 e^{-2phi-2w} < r^2 (metric nondegenerate)
        lam=1.0
        for _ in range(40):
            qn, wn = qv+lam*d[0], wv+lam*d[1]
            if qn**2*np.exp(-2*ph-2*wn) < 0.95*rr**2:
                break
            lam*=0.5
        qv, wv = qv+lam*d[0], wv+lam*d[1]
    return qv, wv

# ---------------------------------------------------------------------
# Reduced on-shell pointwise Hessian on (phi, phir, phith):
#   H_red = Hpp - Hpq Hqq^{-1} Hpq^T   (Schur complement; q,w slaved)
# Its (phir,phir),(phith,phith) entries are the ON-SHELL stiffness
# coefficients K_r, K_th; its (phi,phi) entry is the potential curvature.
# We then assemble the GATE-A generalized eigenproblem with THESE on-shell
# K_r, K_th, V and read the sign.
# ---------------------------------------------------------------------
def onshell_coeffs(rr, tt, Phival, ph, pr, pth):
    qv, wv = slave_qw(rr, tt, Phival, ph, pr, pth)
    Hpp_ = np.array(fHpp(rr,tt,Phival,ph,qv,wv,pr,pth), dtype=float).reshape(3,3)
    Hqq_ = np.array(fHqq(rr,tt,Phival,ph,qv,wv,pr,pth), dtype=float).reshape(2,2)
    Hpq_ = np.array(fHpq(rr,tt,Phival,ph,qv,wv,pr,pth), dtype=float).reshape(3,2)
    try:
        Hred = Hpp_ - Hpq_ @ np.linalg.solve(Hqq_, Hpq_.T)
    except np.linalg.LinAlgError:
        Hred = Hpp_
    # indices: 0=phi,1=phir,2=phith
    return dict(qv=qv, wv=wv, Vpp=Hred[0,0], Krr=Hred[1,1], Kthth=Hred[2,2],
                Kr_th=Hred[1,2], Hpp_raw=Hpp_, Hred=Hred)


# =====================================================================
# Self-consistent formed background phi(r,theta).  We use the wint cell
# (the metric's own converging machinery) for the round phi(r); for the
# ON-SHELL test we evaluate the reduced Hessian coefficients on this
# background and assemble the generalized eigenproblem.  We ALSO test on a
# deliberately NON-SPHERICAL (theta-perturbed) phi -- where q,w are sourced
# (tadpole nonzero) -- to see whether the on-shell slaving makes the angular
# stiffness ATTRACTIVE (sign-indefinite) or keeps it REPULSIVE.
# =====================================================================
def formed_background(Nr=33, Nth=27, depth=1.5, lobe=0.0, ell=2):
    """phi(r,theta): round well (depth at center -> 0 at seal), optionally
       with a theta lobe (amplitude `lobe`, Legendre ell) so phi_th != 0 and
       q,w are genuinely sourced (the formed, non-spherical regime)."""
    r = np.linspace(0.18, 1.0, Nr)
    th = np.linspace(1e-3, np.pi-1e-3, Nth)
    x = (r-r[0])/(r[-1]-r[0])
    base = depth*(1.0 - x**2)
    phi = np.tile(base[:, None], (1, Nth))
    if lobe != 0.0:
        from numpy.polynomial.legendre import legval
        Pl = legval(np.cos(th), [0]*ell+[1])[None, :]
        bump = np.exp(-((x-0.5)/0.3)**2)[:, None]
        phi = phi + lobe*bump*Pl
    return phi, r, th

def grad_phi(phi, r, th):
    dr = r[1]-r[0]; dth = th[1]-th[0]
    pr = np.gradient(phi, dr, axis=0)
    pth = np.gradient(phi, dth, axis=1)
    return pr, pth

def assemble_onshell(phi, r, th, Phival=1.0, sign_test='onshell'):
    """Assemble the GATE-A generalized eigenproblem with ON-SHELL reduced
       coefficients K_r, K_th, V at each grid point (q,w slaved by the
       metric's own EL).  sign_test:
         'onshell'  : the honest reduced Hessian (the physical answer)
         'diag'     : force q=w=0 (the diagonal class) -- baseline control
       Returns (A_stiff, M)."""
    Nr, Nth = phi.shape
    pr, pth = grad_phi(phi, r, th)
    R = r[:, None]; sinth = np.sin(th)[None, :]
    W = (R**2)*sinth
    dr = r[1]-r[0]; dth = th[1]-th[0]
    Kr = np.zeros((Nr, Nth)); Kth = np.zeros((Nr, Nth)); V = np.zeros((Nr,Nth))
    for i in range(Nr):
        for j in range(Nth):
            if sign_test == 'diag':
                # diagonal class: K_r=e^{-4phi}, K_th=e^{-2phi}/r^2 (the box),
                # V = Phi(2e^{-2phi}+e^{phi}) (the confining source curvature)
                Kr[i,j]  = np.exp(-4*phi[i,j])
                Kth[i,j] = np.exp(-2*phi[i,j])/r[i]**2
                V[i,j]   = Phival*(2*np.exp(-2*phi[i,j])+np.exp(phi[i,j]))
            else:
                co = onshell_coeffs(r[i], th[j], Phival, phi[i,j],
                                    pr[i,j], pth[i,j])
                Kr[i,j]  = co['Krr']
                Kth[i,j] = co['Kthth']/r[i]**2 if False else co['Kthth']
                V[i,j]   = co['Vpp']
    # assemble symmetric stiffness with these (possibly sign-varying) coeffs:
    idx = np.arange(Nr*Nth).reshape(Nr, Nth)
    rows, cols, vals = [], [], []
    def add(a,b,v): rows.append(a); cols.append(b); vals.append(v)
    WKr = W*Kr; WKth = W*Kth
    for j in range(Nth):
        for ir in range(Nr-1):
            we = 0.5*(WKr[ir,j]+WKr[ir+1,j])*dth/dr
            a=idx[ir,j]; b=idx[ir+1,j]
            add(a,a,we); add(b,b,we); add(a,b,-we); add(b,a,-we)
    for i in range(Nr):
        for jt in range(Nth-1):
            we = 0.5*(WKth[i,jt]+WKth[i,jt+1])*dr/dth
            a=idx[i,jt]; b=idx[i,jt+1]
            add(a,a,we); add(b,b,we); add(a,b,-we); add(b,a,-we)
    A = sps.csr_matrix((vals,(rows,cols)), shape=(Nr*Nth, Nr*Nth))
    A = A + sps.diags((V*W*dr*dth).ravel())
    M = sps.diags((W*dr*dth).ravel())
    return A.tocsr(), M.tocsr(), dict(Kr=Kr, Kth=Kth, V=V)


def _main():
    log("\nON-SHELL verdict on self-consistent formed backgrounds")
    log(f"{'depth':>6} {'lobe':>5} {'ell':>4} {'class':>9} "
        f"{'lam_min':>13} {'nneg':>6} {'Kth<0 frac':>11} {'verdict':>20}")
    rows = []
    for depth in [0.8, 1.5, 2.5, 3.5]:
        for (lobe, ell) in [(0.0, 0), (0.15, 2), (0.15, 3)]:
            phi, r, th = formed_background(depth=depth, lobe=lobe, ell=ell)
            for cls in ['diag', 'onshell']:
                A, M, co = assemble_onshell(phi, r, th, sign_test=cls)
                w = gen_spectrum(A, M)
                nneg = int(np.sum(w < -1e-6*max(1.0, abs(w[-1]))))
                kthneg = float(np.mean(co['Kth'] < 0))
                indef = nneg > 0
                verdict = "INDEF(shaped)" if indef else "def(round)"
                log(f"{depth:6.2f} {lobe:5.2f} {ell:4d} {cls:>9} "
                    f"{w[0]:13.5e} {nneg:6d} {kthneg:11.3f} {verdict:>20}")
                rows.append(dict(depth=depth, lobe=lobe, ell=ell, cls=cls,
                                 lam_min=float(w[0]), nneg=nneg,
                                 kth_neg_frac=kthneg))
    json.dump(rows, open("/tmp/offdiag_gateB_onshell.json","w"))
    # verdict logic:
    onshell_indef = [x for x in rows if x['cls']=='onshell' and x['nneg']>0]
    onshell_kthneg = [x for x in rows if x['cls']=='onshell'
                      and x['kth_neg_frac']>0]
    log("")
    if onshell_indef:
        log(f"ON-SHELL VERDICT: SIGN-INDEFINITE in {len(onshell_indef)} "
            f"configs -> the geometry SUPPORTS a non-round shaped type "
            f"ON-SHELL.  The attractive flip is PHYSICAL.")
    else:
        log("ON-SHELL VERDICT: SIGN-DEFINITE everywhere (round only). With "
            "q,w slaved by the metric's OWN EL, the angular stiffness stays "
            "REPULSIVE -- the attractive flip is an OFF-SHELL SCHEME ARTIFACT "
            "(it required eliminating q,w in directions their own field "
            "equation does not slave to).")
    if onshell_kthneg:
        log(f"  NOTE: on-shell K_th went NEGATIVE in "
            f"{len(onshell_kthneg)} configs -- attractive angular stiffness "
            f"appears at the coefficient level; check whether it survives the "
            f"full operator (it may be dominated by V).")
    else:
        log("  on-shell K_th stayed POSITIVE everywhere: the slaved q,w do "
            "NOT reverse the centrifugal sign.")
    log(f"\nGATE B part 2 done  t={time.time()-t0:.1f}s")


if __name__ == "__main__":
    _main()
