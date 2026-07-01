#!/usr/bin/env python3
"""
offdiagII_operator.py -- THE DECISIVE GATE: full-operator sign-indefiniteness
==============================================================================
OFF-DIAGONAL ANGULAR ROW II push. Driver: Claude (Opus 4.8, 1M). 2026-06-13.
Frame: CRITICAL_UNIVERSE_FRAME.md. Charter principle 2 (NO linearization as a
result -- every coefficient is the EXACT nonlinear on-shell value). New files
only (offdiagII_*). Log /tmp/offdiagII.log.

=============================== THE GATE =====================================
A locally-negative on-shell K_th (the verifier's confirmed attractive flip) is
NECESSARY BUT NOT SUFFICIENT for a non-round type. The DECISIVE question:
assemble the FULL even-sector angular operator -- the validated measure-weighted
stiffness with the on-shell q-slaved Schur coefficients K_r, K_th, the source/
curvature potential V, and the centrifugal ell(ell+1) channel term -- on a REAL
self-consistent FORMED CELL, per angular-momentum channel ell, and ask:

   IS THE LOWEST GENERALIZED EIGENVALUE NEGATIVE?
   ( yes  => a non-round deformation LOWERS total energy => the geometry
             SUPPORTS a distinct shaped type : SIGN-INDEFINITE )
   ( >=0  => the attractive wall term is V-dominated over the whole cell
             => round only : SIGN-DEFINITE )

=========================== HOW (binding) ===================================
1. Coefficients are the metric's OWN on-shell values. q is slaved EXACTLY by
   Newton on the metric's own algebraic EL dL0/dq=0 (the verifier's machinery,
   reproduced + anchor-checked below). w=0 (runaway; best-defined on-shell
   prescription -- caveat carried). NOTHING else added/slaved/frozen.
2. Self-adjoint measure M = r^2 sin th (bare); the e^{-2phi} dressing lives in
   the stiffness (GATE A, validated). Generalized eigenproblem A v = lam M v,
   eigh(A,M) via Cholesky-of-M -- NEVER a symmetrized A M^-1.
3. K_th(x) := on-shell Schur d^2/dphi_th^2 L0(q*(phi_th)) / W  (the verifier's
   K_th, three-route validated). K_r(x) likewise. V(x) := the source second
   variation -dS/dphi (CONFINING, +). All evaluated on the BACKGROUND gradients
   p_r, p_th at each grid point -- the EXACT nonlinear on-shell coefficients,
   no linearization (depth exp(-2phi) up to thousands carried honestly).
4. SWEEP TOWARD THE SEAL/MEDIUM: phi around 0 and NEGATIVE (the exterior side
   where the flip strengthens -- the primary stayed at phi>=0.5 and missed it).

=========================== TEMPLATE TRIPWIRE ===============================
The eigen run produces modes. Eigenvalues are NOT masses; a count of modes is
NOT a particle count. The ONLY reading is the SIGN of the lowest eigenvalue per
ell = does an energy-lowering non-round direction EXIST. Report sign-indefinite
vs sign-definite. NO spectrum, ladder, mass, or mode-count for particle counts.
"""
import sys, time, json
import numpy as np
import sympy as sp
import scipy.linalg as sla

_fh = open("/tmp/offdiagII.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()

log("=" * 78)
log("offdiagII_operator -- FULL-OPERATOR sign-indefiniteness gate")
log("time", time.strftime("%Y-%m-%d %H:%M:%S"))
log("=" * 78)

# =====================================================================
# (0) THE METRIC'S OWN REDUCED DENSITY + EXACT q-SLAVING (verifier machinery)
#     L0 = e^{-2phi} (grad . g^{-1} . grad) sqrt(-g) - Phi(.5 e^{-2phi}+e^phi)
#          sqrt(-g),  g = diag-block with off-diagonal q=g_rtheta, w=0.
#     Reproduced EXACTLY from verify_killshot.py / offdiag_kth_probe.py.
# =====================================================================
r_s, th_s, Phi_s = sp.symbols('r theta Phi', positive=True)
phi_s, q_s, pr_s, pth_s = sp.symbols('phi q pr pth', real=True)
em2p = sp.exp(-2*phi_s); e2p = sp.exp(2*phi_s)
g = sp.Matrix([[-em2p, 0, 0, 0],
               [0, e2p, q_s, 0],
               [0, q_s, r_s**2, 0],
               [0, 0, 0, r_s**2*sp.sin(th_s)**2]])
gi = g.inv(); sqrtmg = sp.sqrt(-g.det())
grad = sp.Matrix([0, pr_s, pth_s, 0])
Kin = (grad.T*gi*grad)[0]
# source: V_source(phi) appears as -dS/dphi in the 2nd variation; the density
# carries the matter potential -Phi(.5 e^{-2phi}+e^phi) (verifier/primary form).
Lsrc = -Phi_s*(sp.Rational(1,2)*em2p + sp.exp(phi_s))
L0 = em2p*Kin*sqrtmg + Lsrc*sqrtmg

fL   = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), L0, 'numpy')
fdq  = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), sp.diff(L0,q_s), 'numpy')
fd2q = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), sp.diff(L0,q_s,q_s),'numpy')
# Schur Hessian blocks at slaved q* (analytic, the exact on-shell stiffness):
fHpp = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), sp.diff(L0,pth_s,2),'numpy')
fHrr = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), sp.diff(L0,pr_s,2),'numpy')
fHpq = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), sp.diff(L0,pth_s,q_s),'numpy')
fHrq = sp.lambdify((r_s,th_s,Phi_s,phi_s,q_s,pr_s,pth_s), sp.diff(L0,pr_s,q_s),'numpy')

def qstar(rr, tt, ph, pr, pth, Phi=1.0):
    """slave q EXACTLY on the metric's own algebraic EL dL0/dq=0 (Newton)."""
    qv = 0.0
    for _ in range(400):
        F = float(fdq(rr,tt,Phi,ph,qv,pr,pth)); H = float(fd2q(rr,tt,Phi,ph,qv,pr,pth))
        if abs(F) < 1e-16 or abs(H) < 1e-16: break
        qv += -F/H
        if qv**2*np.exp(-2*ph) > 0.95*rr**2: qv *= 0.5
    return qv

def onshell_coeffs(rr, tt, ph, pr, pth, Phi=1.0):
    """Return (K_r, K_th) = the EXACT on-shell q-slaved Schur stiffness
       coefficients (bare, divided by W=r^2 sin th), and q*/bound.
       K_th = (Hpp - Hpq^2/Hqq)/W  (the verifier's three-route value).
       K_r  = (Hrr - Hrq^2/Hqq)/W  (same Schur for the radial channel)."""
    qs = qstar(rr, tt, ph, pr, pth, Phi)
    W = rr**2*np.sin(tt)
    Hqq = float(fd2q(rr,tt,Phi,ph,qs,pr,pth))
    Hpp = float(fHpp(rr,tt,Phi,ph,qs,pr,pth)); Hpq = float(fHpq(rr,tt,Phi,ph,qs,pr,pth))
    Hrr = float(fHrr(rr,tt,Phi,ph,qs,pr,pth)); Hrq = float(fHrq(rr,tt,Phi,ph,qs,pr,pth))
    Kth = (Hpp - Hpq**2/Hqq)/W
    Kr  = (Hrr - Hrq**2/Hqq)/W
    bnd = rr*np.exp(ph)
    return Kr, Kth, abs(qs)/bnd, qs, Hqq

# ---- ANCHOR (mandatory before trusting assembly) --------------------
def _anchor():
    Kr,Kth,ratio,qs,Hqq = onshell_coeffs(0.5, 1.0, 0.5, 8.0, 0.5)
    log("\nANCHOR (verifier kill-shot): phi=0.5 r=0.5 pr=8 pth=0.5 (theta=1.0)")
    log(f"  q*={qs:.5f}  |q*|/bound={ratio:.4f} (deg locus ~0.9)  Hqq={Hqq:.3e}(>0)")
    log(f"  on-shell K_th = {Kth:.4f}   (verifier anchor: -2.033)")
    ok = abs(Kth - (-2.0326)) < 2e-3 and Hqq > 0
    log(f"  ANCHOR {'REPRODUCED' if ok else 'FAILED'}: K_th matches -2.0326 to 2e-3.")
    return ok

# =====================================================================
# (1) THE SOURCE / CONFINING POTENTIAL V(x) -- the matter second variation.
#     The fluctuation operator's mass term is the second phi-variation of the
#     matter source S(phi) = -Phi(.5 e^{-2phi}+e^phi):  V = d^2/dphi^2 (-Lsrc)
#     Wait: the EL operator is delta(action)/delta phi; the OPERATOR mass term
#     is -d^2 Lsrc/dphi^2 with sign s.t. a CONFINING source gives V>0.
#     d^2/dphi^2 [-(-Phi(.5e^{-2phi}+e^phi))] = d^2/dphi^2[Phi(.5e^{-2phi}+e^phi)]
#       = Phi(2 e^{-2phi} + e^phi)  > 0   (the GATE-A V, the metric's own).
# =====================================================================
def V_source(ph, Phi=1.0):
    return Phi*(2.0*np.exp(-2.0*ph) + np.exp(ph))   # >0 confining (GATE A)

# =====================================================================
# (2) FULL-OPERATOR ASSEMBLY (per ell channel), validated GATE-A measure.
#     Even-sector fluctuation u(r,th)=R(r)Y_ell(th); we keep theta EXPLICIT
#     (the flip is anisotropic in theta) and solve the 2D generalized problem
#     with the ell azimuthal/centrifugal term folded in as the m^2-style
#     diagonal (here ell labels the polar channel via the seed; we solve the
#     FULL 2D operator so no separability is assumed -- the honest object).
#
#     Bilinear form:
#       a(u,u) = INT [ K_r(x) u_r^2 + K_th(x) u_th^2
#                      + (ellterm) K_th(x) u^2 / sin^2 th
#                      + V(x) u^2 ] W dr dth,    W = r^2 sin th
#     with K_r,K_th the ON-SHELL Schur coefficients (anisotropic background),
#     V the confining source. ellterm = m^2 (azimuthal); the polar ell>=2
#     structure is captured by solving the full 2D operator (its low modes
#     ARE the ell-channels). We report BOTH: (a) the full-2D lowest eigenvalue
#     (any polar structure), and (b) explicit azimuthal m=0,1,2 channels.
# =====================================================================
def assemble_full(phi, r, th, pr, pth, Phi=1.0, m_az=0, include_V=True,
                  flip_on=True):
    """Assemble (A,M) for the full on-shell operator. flip_on=True uses the
       q-slaved Schur K_r,K_th (the real on-shell coefficients). flip_on=False
       uses the bare diagonal coefficients (control: must be sign-definite)."""
    Nr, Nth = phi.shape
    R = r[:, None]; TH = th[None, :]
    sinth = np.sin(TH)
    W = (R**2)*sinth
    dr = r[1]-r[0]; dth = th[1]-th[0]
    # pointwise on-shell stiffness coefficient fields:
    Kr = np.zeros_like(phi); Kth = np.zeros_like(phi)
    qratio = np.zeros_like(phi)
    for i in range(Nr):
        for j in range(Nth):
            if flip_on:
                kr, kth, ratio, _, _ = onshell_coeffs(r[i], th[j], phi[i,j],
                                                       pr[i,j], pth[i,j], Phi)
            else:
                kr = np.exp(-4.0*phi[i,j]); kth = np.exp(-2.0*phi[i,j])/r[i]**2
                ratio = 0.0
            Kr[i,j] = kr; Kth[i,j] = kth; qratio[i,j] = ratio
    # symmetric weak-form stiffness (P1 flux, GATE-A stencil):
    idx = np.arange(Nr*Nth).reshape(Nr, Nth)
    N = Nr*Nth
    import scipy.sparse as sps
    rows, cols, vals = [], [], []
    def add(i,j,v): rows.append(i); cols.append(j); vals.append(v)
    WKr = W*Kr; WKth = W*Kth
    for j in range(Nth):
        for ir in range(Nr-1):
            we = 0.5*(WKr[ir,j]+WKr[ir+1,j])*dth/dr
            a=idx[ir,j]; b=idx[ir+1,j]
            add(a,a,we); add(b,b,we); add(a,b,-we); add(b,a,-we)
    for ir in range(Nr):
        for jt in range(Nth-1):
            we = 0.5*(WKth[ir,jt]+WKth[ir,jt+1])*dr/dth
            a=idx[ir,jt]; b=idx[ir,jt+1]
            add(a,a,we); add(b,b,we); add(a,b,-we); add(b,a,-we)
    A = sps.csr_matrix((vals,(rows,cols)), shape=(N,N))
    Mdiag = (W*dr*dth).ravel()
    # azimuthal centrifugal m^2/sin^2 th using the ON-SHELL K_th (consistent):
    if m_az != 0:
        cent = (m_az**2)*Kth/(sinth**2)
        A = A + sps.diags((cent*W*dr*dth).ravel())
    # confining source potential V:
    if include_V:
        V = V_source(phi, Phi)
        A = A + sps.diags((V*W*dr*dth).ravel())
    M = sps.diags(Mdiag)
    return A.tocsr(), M.tocsr(), Mdiag, qratio, Kth

def gen_lowest(A, M, k=6):
    Ad = A.toarray(); Md = np.asarray(M.todense())
    Ad = 0.5*(Ad+Ad.T)
    w = sla.eigh(Ad, Md, eigvals_only=True)
    return np.sort(w)[:k]

if __name__ == "__main__":
    ok = _anchor()
    if not ok:
        log("ANCHOR FAILED -- aborting (assembly not trusted)."); _fh.close(); sys.exit(1)
    log("\nAnchor good. Module ready. (driver runs scans in offdiagII_scan.py)")
    _fh.close()
