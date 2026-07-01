#!/usr/bin/env python3
"""
spectral_axisym_engine.py -- 2-D axisymmetric SPECTRAL Einstein + L2+L4 engine.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

THE GAUGE-FIXED METRIC (static, axisymmetric, DIAGONAL = Weyl/Lewis-Papapetrou
gauge -- a non-restrictive coordinate condition for a static axisymmetric system,
NOT a physics tie; B=1/A NOT imposed, the four metric functions are independent):
  ds^2 = -e^{2a} dt^2 + e^{2b} dr^2 + e^{2c} r^2 dtheta^2 + e^{2d} r^2 sin^2(th) dpsi^2
  a,b,c,d = a,b,c,d(r,theta).  Round limit: a=a(r), b=b(r), c=d=0 = #56 soliton.

THE ENGINE: standard NR pipeline g -> dg -> Gamma -> dGamma -> Riemann -> Ricci
-> Einstein G^mu_nu, computed with SPECTRAL derivatives (Chebyshev in r, Legendre
in theta).  This is the SAME content as whole_metric_3d_core (validated CLEAN,
infra audit 2026-06-16, off-diag G to 5e-6, O(h^4)) -- here specialized to the
static axisymmetric diagonal class and evaluated SPECTRALLY (the conditioning fix).
Cross-validated below against (i) flat (G=0), (ii) Schwarzschild (G=0), (iii) the
round #56 soliton embedded in 2-D (G - kap8 T -> machine zero).

MATTER: the unit-S^3 hedgehog with a GENERAL profile Theta(r,theta) (the matter
FREE to deform -- the #58 cure).  n = (sinTh sinth cosps, sinTh sinth sinps,
sinTh costh, cosTh).  The L2+L4 stress is the SAME Hilbert form as
whole_metric_3d_matter (validated CLEAN).  With a general Theta(r,theta) the field
gradient has both d_r n and d_theta n; we build the field "first fundamental form"
G_{mn}=d_m n . d_n n and the Hilbert stress T^mu_nu exactly.

CATEGORY-A: spectral discretization + the diagonal Weyl gauge (coordinate
condition; B=1/A free) + axis/core regularity (required physics) + proper-volume
residual weighting.  NO tie, source, linearization, dropped term, or tuned dial.
PRINCIPLE 2: full nonlinear; spectral derivative = sanctioned exact-on-poly
function-replacement.
"""
import numpy as np
import math
from spectral_cheb import cheb_interval, clenshaw_curtis_weights
from spectral_2d import theta_operators
from axisym_einstein_analytic import Gmix_components

PI = math.pi
T, RR, TH, PS = 0, 1, 2, 3


class Grid2D:
    """2-D (r,theta) spectral grid + derivative operators.  Fields stored as
    (Nr, Nth) arrays."""
    def __init__(self, Nr, Nth, rc=0.05, cell=14.0):
        self.Nr = Nr; self.Nth = Nth
        ri = rc + cell
        self.rc = rc; self.ri = ri
        self.r1, self.Dr1 = cheb_interval(Nr, rc, ri)        # (Nr+1,), (Nr+1,Nr+1)
        self.th1, self.wmu, self.Dth1, self.sth1 = theta_operators(Nth)
        self.nr = self.r1.size; self.nth = self.th1.size
        # 2-D meshes (r varies along axis0, theta along axis1)
        self.R, self.TH = np.meshgrid(self.r1, self.th1, indexing='ij')
        self.STH = np.sin(self.TH); self.CTH = np.cos(self.TH)
        self.wr = clenshaw_curtis_weights(Nr, rc, ri)

    def d_r(self, f):
        """d/dr of field f (nr,nth): apply Chebyshev Dr along axis 0."""
        return self.Dr1 @ f
    def d_th(self, f):
        """d/dtheta of field f (nr,nth): apply Dth along axis 1."""
        return f @ self.Dth1.T

    def proper_weight(self, g):
        """proper-volume weight sqrt|g_spatial| at each node (normalized).
        For the diagonal metric, |g_3| = e^{2b} e^{2c} r^2 e^{2d} r^2 sin^2 th."""
        return np.sqrt(np.maximum(g['det3'], 1e-30))


# ---------------------------------------------------------------------------
# Build the full 4x4 metric g_{mu nu}(r,theta) and its inverse from (a,b,c,d).
# Diagonal: g_tt=-e^{2a}, g_rr=e^{2b}, g_thth=e^{2c} r^2, g_psps=e^{2d} r^2 sin^2 th.
# Returns dict of the diagonal entries (each (nr,nth)) + det3 (spatial det).
# ---------------------------------------------------------------------------
def metric_from_fields(G, a, b, c, d):
    r = G.R; sth = G.STH
    g_tt = -np.exp(2*a)
    g_rr = np.exp(2*b)
    g_thth = np.exp(2*c) * r**2
    g_psps = np.exp(2*d) * r**2 * sth**2
    det3 = g_rr * g_thth * g_psps
    return dict(g_tt=g_tt, g_rr=g_rr, g_thth=g_thth, g_psps=g_psps, det3=det3,
                gi_tt=1.0/g_tt, gi_rr=1.0/g_rr, gi_thth=1.0/g_thth, gi_psps=1.0/g_psps)


# ---------------------------------------------------------------------------
# FULL numerical Einstein tensor for a DIAGONAL axisymmetric metric, computed by
# the general g->Gamma->Riemann->Ricci->G pipeline using spectral derivatives.
# We assemble the 4x4 metric stack and run the SAME contractions as
# whole_metric_3d_core (cross-validated).  Coords (t,r,theta,psi); d_t=d_psi=0.
# Returns G^mu_nu mixed (nr,nth,4,4) and the spatial det.
# ---------------------------------------------------------------------------
def einstein_mixed(G, a, b, c, d):
    """Mixed Einstein G^mu_nu via the ANALYTIC axisym formula (cot/1/sin handled
    symbolically), with a,b,c,d derivatives evaluated SPECTRALLY.  This is the
    SAME native G content as whole_metric_3d_core, specialized to the static
    axisym diagonal class; the analytic substitution is the conditioning cure for
    the coordinate-pole terms that a naive nodal d_theta(sin theta) cannot
    represent (sin theta is not polynomial in mu=cos theta).  Cross-validated
    below on flat (G=0), Schwarzschild (G=0), and the round #56 soliton."""
    nr, nth = G.nr, G.nth
    r = G.R; sth = G.STH
    # spectral derivatives of the smooth metric functions
    a_r = G.d_r(a); b_r = G.d_r(b); c_r = G.d_r(c); d_r_ = G.d_r(d)
    a_t = G.d_th(a); b_t = G.d_th(b); c_t = G.d_th(c); d_t = G.d_th(d)
    a_rr = G.d_r(a_r); b_rr = G.d_r(b_r); c_rr = G.d_r(c_r); d_rr = G.d_r(d_r_)
    a_tt = G.d_th(a_t); b_tt = G.d_th(b_t); c_tt = G.d_th(c_t); d_tt = G.d_th(d_t)
    a_rt = G.d_th(a_r); b_rt = G.d_th(b_r); c_rt = G.d_th(c_r); d_rt = G.d_th(d_r_)
    comps = Gmix_components(r, G.TH, a, b, c, d, a_r, b_r, c_r, d_r_,
                            a_t, b_t, c_t, d_t, a_rr, b_rr, c_rr, d_rr,
                            a_tt, b_tt, c_tt, d_tt, a_rt, b_rt, c_rt, d_rt)
    Gmix = np.zeros((nr, nth, 4, 4))
    for (i, j), val in comps.items():
        Gmix[..., i, j] = val
    # build g, ginv (needed by matter stress)
    g = np.zeros((nr, nth, 4, 4))
    g[..., T, T] = -np.exp(2*a)
    g[..., RR, RR] = np.exp(2*b)
    g[..., TH, TH] = np.exp(2*c) * r**2
    g[..., PS, PS] = np.exp(2*d) * r**2 * sth**2
    ginv = np.zeros_like(g)
    ginv[..., T, T] = 1.0/g[..., T, T]
    ginv[..., RR, RR] = 1.0/g[..., RR, RR]
    ginv[..., TH, TH] = 1.0/g[..., TH, TH]
    ginv[..., PS, PS] = 1.0/g[..., PS, PS]
    det3 = g[..., RR, RR]*g[..., TH, TH]*g[..., PS, PS]
    return Gmix, det3, g, ginv


# ---------------------------------------------------------------------------
# MATTER: unit-S^3 hedgehog with general profile Theta(r,theta).  Field
# n=(sinTh sinth cosps, sinTh sinth sinps, sinTh costh, cosTh).  Build the field
# gradient dn[mu,A]=d_mu n_A (mu over coords, A over 4 target comps), then
# G_{mn}=dn.dn, then the L2+L4 Hilbert stress (SAME as whole_metric_3d_matter).
# psi-derivative: n depends on psi only through cos ps, sin ps in slots 0,1;
# d_psi n = (-sinTh sinth sinps, sinTh sinth cosps, 0, 0).  At the working psi
# slice we take psi=0: d_psi n = (0, sinTh sinth, 0, 0).
# Returns T^mu_nu mixed (nr,nth,4,4).
# ---------------------------------------------------------------------------
def matter_stress(G, Th, a, b, c, d, ginv, g, xi=1.0, kap=1.0):
    nr, nth = G.nr, G.nth
    sth = G.STH; cth = G.CTH
    sT = np.sin(Th); cT = np.cos(Th)
    dr_Th = G.d_r(Th); dth_Th = G.d_th(Th)

    # n components at psi=0: (sinTh sinth, 0, sinTh costh, cosTh)
    # build dn[...,mu,A], mu in {r,theta,psi} (t=0)
    dn = np.zeros((nr, nth, 4, 4))
    # d/dr: only through Th
    # n0=sinTh sinth, n1=0, n2=sinTh costh, n3=cosTh
    dn[..., RR, 0] = cT*sth*dr_Th
    dn[..., RR, 2] = cT*cth*dr_Th
    dn[..., RR, 3] = -sT*dr_Th
    # d/dtheta: through Th and through the explicit theta in sinth/costh
    dn[..., TH, 0] = cT*sth*dth_Th + sT*cth
    dn[..., TH, 2] = cT*cth*dth_Th - sT*sth
    dn[..., TH, 3] = -sT*dth_Th
    # d/dpsi at psi=0: n0=sinTh sinth cosps -> d_psi=-sinTh sinth sinps=0;
    #   n1=sinTh sinth sinps -> d_psi=sinTh sinth cosps = sinTh sinth
    dn[..., PS, 1] = sT*sth

    Gmn = np.einsum('...mA,...nA->...mn', dn, dn)    # field first fundamental form

    # Lagrangian L=L2+L4 (Lagrange-identity), ginv diagonal
    L2 = -(xi/2)*np.einsum('...mn,...mn->...', ginv, Gmn)
    GG1 = np.einsum('...mp,...nq->...mnpq', Gmn, Gmn)
    GG2 = np.einsum('...mq,...np->...mnpq', Gmn, Gmn)
    SS = GG1 - GG2
    L4 = -(kap/4)*np.einsum('...mp,...nq,...mnpq->...', ginv, ginv, SS)
    L = L2 + L4
    # T_{ab}=xi G_{ab}+kap[g^{nq}SS_{a n b q}]_sym + g_{ab}L
    C_ab = np.einsum('...nq,...anbq->...ab', ginv, SS)
    C_ab = 0.5*(C_ab + np.einsum('...ab->...ba', C_ab))
    Tab = xi*Gmn + kap*C_ab + g*L[..., None, None]
    Tmix = np.einsum('...md,...dn->...mn', ginv, Tab)
    return Tmix, dict(Gmn=Gmn, L=L, dn=dn)


# ---------------------------------------------------------------------------
# Round #56 embedding: a(r), b(r), c=d=0, Theta(r) -- the validation seed.
# Reuse the spectral RADIAL solution and broadcast over theta.
# ---------------------------------------------------------------------------
def round_seed_2d(G, p=0.4, kap8=0.05, Nr_solve=None):
    from spectral_radial_soliton import solve as solve_radial
    Nr_solve = Nr_solve or G.Nr
    rad = solve_radial(Nr_solve, rc=G.rc, cell=G.ri-G.rc, p=p, kap8=kap8, maxit=100)
    # interpolate radial fields onto G.r1 (same grid if Nr matches)
    if Nr_solve == G.Nr and np.allclose(rad['r'], G.r1):
        a1, b1, Th1 = rad['a'], rad['b'], rad['Th']
    else:
        a1 = np.interp(G.r1, rad['r'], rad['a'])
        b1 = np.interp(G.r1, rad['r'], rad['b'])
        Th1 = np.interp(G.r1, rad['r'], rad['Th'])
    a = np.tile(a1[:, None], (1, G.nth))
    b = np.tile(b1[:, None], (1, G.nth))
    c = np.zeros((G.nr, G.nth))
    d = np.zeros((G.nr, G.nth))
    Th = np.tile(Th1[:, None], (1, G.nth))
    return a, b, c, d, Th, rad


if __name__ == "__main__":
    print("=== spectral axisym engine validation ===")
    # (i) flat: a=b=c=d=0 -> G=0
    G = Grid2D(24, 8, rc=0.5, cell=4.0)
    a=b=c=d=np.zeros((G.nr,G.nth))
    Gm,det3,gg,gi = einstein_mixed(G,a,b,c,d)
    print(f"(i) flat  max|G^mu_nu| = {np.max(np.abs(Gm)):.3e}  (expect ~0)")

    # (ii) Schwarzschild: e^{2a}=1-2M/r, b=-a, c=d=0 -> G=0 (rc>2M)
    M=0.3
    print("    Schwarzschild G convergence in Nr (exponential signature):")
    for Nr in [16,24,32,48]:
        Gt=Grid2D(Nr,8,rc=1.0,cell=6.0)
        f=1-2*M/Gt.R; aS=0.5*np.log(f)
        Gm,_,_,_=einstein_mixed(Gt,aS,-aS,np.zeros_like(aS),np.zeros_like(aS))
        bd=(Gt.R>1.5)&(Gt.R<6.0)
        print(f"      Nr={Nr:3d}  max|G|(body)={np.max(np.abs(Gm[bd])):.3e}")

    # (iii) round #56 soliton embedded in 2-D: G - kap8 T -> machine zero
    print("\n(iii) round #56 soliton embedded in 2-D (the gate):")
    for Nr,Nth in [(48,6),(64,8),(96,10)]:
        Gg=Grid2D(Nr,Nth,rc=0.05,cell=14.0)
        a,b,c,d,Th,rad=round_seed_2d(Gg,p=0.4,kap8=0.05)
        Gm,det3,gg,gi=einstein_mixed(Gg,a,b,c,d)
        Tm,_=matter_stress(Gg,Th,a,b,c,d,gi,gg,1.0,1.0)
        res=Gm-0.05*Tm
        body=(Gg.R>0.6)&(Gg.R<Gg.ri-0.6)
        # diagonal residuals
        rtt=np.max(np.abs(res[...,T,T][body]))
        rrr=np.max(np.abs(res[...,RR,RR][body]))
        rthth=np.max(np.abs(res[...,TH,TH][body]))
        rpsps=np.max(np.abs(res[...,PS,PS][body]))
        # off-diagonal (should be ~0 for round)
        roff=np.max(np.abs(res[...,RR,TH][body]))
        print(f"  Nr={Nr} Nth={Nth}: res_tt={rtt:.2e} res_rr={rrr:.2e} "
              f"res_thth={rthth:.2e} res_psps={rpsps:.2e} res_offdiag={roff:.2e}")
