#!/usr/bin/env python3
"""
INDEPENDENT relax-back with the CORRECT axisym matter EL swapped in.
Re-runs the l=2 quadrupole + a couple of catalog seeds using the corrected EL
(verified consistent with the Hilbert stress / div T), to check whether the
'relaxes to round' conclusion survives the EL fix.

We reuse the committed Einstein + committed Hilbert stress (both verified correct)
and ONLY replace the matter EL residual with the correct one (numpy, via finite-diff
Jacobian LM on CPU -- independent of the committed torch LM).
"""
import numpy as np
from spectral_cheb import cheb_interval, clenshaw_curtis_weights
from spectral_2d import theta_operators
from axisym_matter_el_CORRECT import matter_el_resid_CORRECT as ELc
import axisym_einstein_analytic as GE
from spectral_radial_soliton import solve as rsolve

PI = np.pi
T, RR, TH, PS = 0, 1, 2, 3


class Grid:
    def __init__(self, Nr, Nth, rc=0.05, cell=14.0):
        ri = rc+cell
        self.Nr, self.Nth = Nr, Nth
        self.rc, self.ri = rc, ri
        self.r1, self.Dr = cheb_interval(Nr, rc, ri)
        self.th1, self.wmu, self.Dth, self.sth1 = theta_operators(Nth)
        self.nr, self.nth = self.r1.size, self.th1.size
        self.R, self.THm = np.meshgrid(self.r1, self.th1, indexing='ij')
        self.STH, self.CTH = np.sin(self.THm), np.cos(self.THm)
        self.wr = clenshaw_curtis_weights(Nr, rc, ri)

    def dr(self, f): return self.Dr@f
    def dth(self, f): return f@self.Dth.T


def derivs(G, f):
    fr = G.dr(f); ft = G.dth(f)
    return f, fr, ft, G.dr(fr), G.dth(ft), G.dth(fr)


def stress_hilbert(G, a, b, c, d, Th, xi=1.0, kap=1.0):
    """True Hilbert mixed stress T^mu_nu (=committed C_ab form, verified equal)."""
    sth = G.STH; cth = G.CTH
    sT = np.sin(Th); cT = np.cos(Th)
    drTh = G.dr(Th); dthTh = G.dth(Th)
    nr, nth = G.nr, G.nth
    dn = np.zeros((nr, nth, 4, 4))
    dn[..., RR, 0] = cT*sth*drTh
    dn[..., RR, 2] = cT*cth*drTh
    dn[..., RR, 3] = -sT*drTh
    dn[..., TH, 0] = cT*sth*dthTh + sT*cth
    dn[..., TH, 2] = cT*cth*dthTh - sT*sth
    dn[..., TH, 3] = -sT*dthTh
    dn[..., PS, 1] = sT*sth
    Gmn = np.einsum('...mA,...nA->...mn', dn, dn)
    g = np.zeros((nr, nth, 4, 4))
    g[..., T, T] = -np.exp(2*a); g[..., RR, RR] = np.exp(2*b)
    g[..., TH, TH] = np.exp(2*c)*G.R**2; g[..., PS, PS] = np.exp(2*d)*G.R**2*sth**2
    ginv = np.zeros_like(g)
    for i in range(4): ginv[..., i, i] = 1.0/g[..., i, i]
    L2 = -(xi/2)*np.einsum('...mn,...mn->...', ginv, Gmn)
    GG1 = np.einsum('...mp,...nq->...mnpq', Gmn, Gmn)
    GG2 = np.einsum('...mq,...np->...mnpq', Gmn, Gmn)
    SS = GG1-GG2
    L4 = -(kap/4)*np.einsum('...mp,...nq,...mnpq->...', ginv, ginv, SS)
    L = L2+L4
    C = np.einsum('...nq,...anbq->...ab', ginv, SS)
    C = 0.5*(C+C.transpose(0, 1, 3, 2))
    Tab = xi*Gmn+kap*C+g*L[..., None, None]
    return np.einsum('...md,...dn->...mn', ginv, Tab)


def einstein(G, a, b, c, d):
    A = derivs(G, a); B = derivs(G, b); Cc = derivs(G, c); Dd = derivs(G, d)
    return GE.Gmix_components(G.R, G.THm, a, b, c, d,
                              A[1], B[1], Cc[1], Dd[1], A[2], B[2], Cc[2], Dd[2],
                              A[3], B[3], Cc[3], Dd[3], A[4], B[4], Cc[4], Dd[4],
                              A[5], B[5], Cc[5], Dd[5])


def el_correct(G, a, b, c, d, Th, xi=1.0, kap=1.0):
    A = derivs(G, a); B = derivs(G, b); Cc = derivs(G, c); Dd = derivs(G, d); Tt = derivs(G, Th)
    return ELc(G.R, G.THm, a, A[1], A[2], A[3], A[4], A[5],
               b, B[1], B[2], B[3], B[4], B[5],
               c, Cc[1], Cc[2], Cc[3], Cc[4], Cc[5],
               d, Dd[1], Dd[2], Dd[3], Dd[4], Dd[5],
               Th, Tt[1], Tt[2], Tt[3], Tt[4], Tt[5], xi, kap)


def pack(a, b, c, d, Th): return np.concatenate([x.ravel() for x in (a, b, c, d, Th)])


def unpack(u, G):
    n = G.nr*G.nth
    return [u[i*n:(i+1)*n].reshape(G.nr, G.nth) for i in range(5)]


def residual(u, G, p, kap8, m=1):
    a, b, c, d, Th = unpack(u, G)
    comps = einstein(G, a, b, c, d)
    Tm = stress_hilbert(G, a, b, c, d, Th)
    def gc(k): return comps.get(k, np.zeros_like(a))
    Rtt = gc((0, 0))-kap8*Tm[..., 0, 0]
    Rrr = gc((1, 1))-kap8*Tm[..., 1, 1]
    Rthth = gc((2, 2))-kap8*Tm[..., 2, 2]
    Rpsps = gc((3, 3))-kap8*Tm[..., 3, 3]
    Rrth = gc((1, 2))-kap8*Tm[..., 1, 2]
    REL = el_correct(G, a, b, c, d, Th)
    detg = np.abs(np.exp(2*b)*np.exp(2*c)*G.R**2*np.exp(2*d)*G.R**2*G.STH**2)
    W = np.sqrt(detg); W = W/W.mean(); sw = np.sqrt(W)
    mask = np.ones((G.nr, G.nth)); mask[:2, :] = 0; mask[-2:, :] = 0
    wg = sw*mask
    parts = [wg*Rtt, wg*Rrr, wg*Rthth, wg*Rpsps, wg*Rrth, wg*REL]
    bc = [Th[0, :]-m*PI, Th[-1, :], a[-1, :], b[0, :]-(-p),
          c[0, :], c[-1, :], d[0, :], d[-1, :]]
    F = np.concatenate([pp.ravel() for pp in parts]+[bb.ravel() for bb in bc])
    return F, dict(Tm=Tm, a=a, b=b, c=c, d=d, Th=Th)


def tvar(G, rf):
    Ttt = rf['Tm'][..., 0, 0]
    rsel = (G.r1 > 1.0) & (G.r1 < 4.0)
    col = Ttt[rsel, :]
    return float(np.max(col.std(axis=1)/(np.abs(col).mean(axis=1)+1e-12)))


def M_MS(G, rf, kap8):
    rho = -rf['Tm'][..., 0, 0]
    rho_avg = (rho*G.wmu[None, :]).sum(1)/G.wmu.sum()
    return float((G.wr*kap8*G.r1**2*rho_avg).sum())


def lm(u0, G, p, kap8, maxit=60, lam0=1e-3, eps=1e-7):
    u = u0.copy(); lam = lam0
    n = u.size
    for it in range(maxit):
        F0, rf = residual(u, G, p, kap8)
        phi = float(F0@F0)
        if np.max(np.abs(F0)) < 1e-9: break
        # FD Jacobian (independent of autograd)
        J = np.empty((F0.size, n))
        for j in range(n):
            du = np.zeros(n); h = eps*(1+abs(u[j])); du[j] = h
            Fp, _ = residual(u+du, G, p, kap8)
            J[:, j] = (Fp-F0)/h
        JtJ = J.T@J; JtF = J.T@F0
        acc = False
        for _ in range(8):
            duv = np.linalg.solve(JtJ+lam*np.eye(n), -JtF)
            un = u+duv
            Fn, _ = residual(un, G, p, kap8)
            if float(Fn@Fn) < phi:
                u = un; lam = max(lam*0.4, 1e-12); acc = True; break
            lam *= 5
        if not acc:
            lam *= 5
            if lam > 1e10: break
    F, rf = residual(u, G, p, kap8)
    return u, rf, float(F@F)


def round_seed(G, p=0.4, kap8=0.05):
    rad = rsolve(G.Nr, rc=G.rc, cell=G.ri-G.rc, p=p, kap8=kap8, maxit=120)
    a = np.interp(G.r1, rad['r'], rad['a'])[:, None]*np.ones((1, G.nth))
    b = np.interp(G.r1, rad['r'], rad['b'])[:, None]*np.ones((1, G.nth))
    Th = np.interp(G.r1, rad['r'], rad['Th'])[:, None]*np.ones((1, G.nth))
    c = np.zeros((G.nr, G.nth)); d = np.zeros((G.nr, G.nth))
    return pack(a, b, c, d, Th)


def legP(l, x):
    from numpy.polynomial.legendre import Legendre
    cc = np.zeros(l+1); cc[l] = 1.0
    return Legendre(cc)(x)


if __name__ == "__main__":
    import sys
    G = Grid(40, 6, rc=0.05, cell=14.0)
    seeds = sys.argv[1:] or ['l2']
    u0 = round_seed(G)
    # gate first
    print("=== GATE (round seed), CORRECT EL ===")
    ug, rfg, phig = lm(u0.copy(), G, 0.4, 0.05, maxit=40)
    print(f"  Phi={phig:.3e}  M_MS={M_MS(G,rfg,0.05):.5f}  tvar={tvar(G,rfg):.3e}")
    for kind in seeds:
        a, b, c, d, Th = unpack(u0, G)
        mu = G.CTH; rprof = np.exp(-((G.R-2.0)/1.5)**2)
        amp = 0.30
        if kind.startswith('l'):
            Th = Th + amp*rprof*legP(int(kind[1:]), mu)
        elif kind == 'ring':
            Th = Th + 0.40*rprof*np.sin(G.THm)**2
        elif kind == 'twocenter':
            Th = Th + 0.40*rprof*np.cos(G.THm)**2
        Th[0, :] = PI; Th[-1, :] = 0.0
        us = pack(a, b, c, d, Th)
        F0, rf0 = residual(us, G, 0.4, 0.05)
        print(f"\n=== seed {kind} (CORRECT EL) ===  seed tvar={tvar(G,rf0):.4f} Phi0={float(F0@F0):.2e}")
        u = us.copy()
        for blk in range(5):
            u, rf, phi = lm(u, G, 0.4, 0.05, maxit=12, lam0=1e-4)
            print(f"  block {blk+1}: Phi={phi:.3e}  tvar={tvar(G,rf):.4e}  M_MS={M_MS(G,rf,0.05):.5f}")
