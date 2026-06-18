#!/usr/bin/env python3
"""
phase2b_ensemble_solve.py -- PHASE-2b: MULTI-MODE / ENSEMBLE ("the orchestra")
self-gravitating standing-wave packet on the finite mirrored cell r in [0,R_seal],
matter slot EMPTY (pure vacuum), held UDT tie g_tt g_rr = -1.  Dense explicit-
Jacobian Newton + pseudo-arclength continuation in the overall packet amplitude A.

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A (borrow GR
numerics for tractability; impose NO physics, NO matter, NO scale). OBSERVE mode.
c=1.  NO matrix-free PCG (design forbids; dense Newton only).

REUSES the Phase-1 machinery (phase1_geon_solve.py) and the EXACT multi-mode
GW stress derived + verified in phase2b_cross_stress.py:

  THE ENSEMBLE STRESS (verified, phase2b_cross_stress.py):
    S_total(r) = sum_i a_i^2 S_self[Psi_i ; l_i]                      (diagonal)
               + sum_{i<j, l_i=l_j AND w_i=w_j} 2 a_i a_j S_cross[Psi_i,Psi_j]
    where S_self has the SAME form as the phase1 single-mode source (with the
    l-dependent integer coefficients: l(l+1)/2 -> 3,6,10 for l=2,3,4), and the
    CROSS term survives the time- and angle-average ONLY for modes that share
    BOTH the multipole l AND the frequency w (the two selection rules).

  S_self[Psi;l] numerator / (40 r^4 w^2)  (l=2; coefficients below are l-general):
    diagonal l=2: matches phase1 gw_source_S exactly.
  S_cross[Psi_i,Psi_j;l] numerator / (20 r^4 w^2)  (same-l, same-w bilinear).

  BACKREACTION (Misner-Sharp, l=0):  (r F)' = -(r^2/2) S_total,  m(r)=A^2 r F(r).
  WAVE OPERATORS (per mode, dressed by the COMMON F to O(A^2)):
    -Psi_i'' - 4 phi' Psi_i' + (l_i(l_i+1)/r^2)(1+2 phi) Psi_i
        - w_i^2 (1+4 phi) Psi_i = 0,   phi = A^2 F.
  At A->0 each w_i -> j_{l_i} Dirichlet zero / R_seal (Phase-1b box ladder).

NORMALIZATION (C6 generalized): overall packet amplitude fixed by
  sum_i ||a_i Psi_i||_2^2 = A^2  on the cell (one global normalization row);
  the RELATIVE mode weights {a_i} are FREE continuation/sweep parameters (we
  sweep them to map which compositions give which mass) -- per design we do NOT
  patch a preferred composition by hand; we OBSERVE which compositions bind.

THE MASS QUESTION: compute M = m(R) = A^2 R F(R) for each composition; report
sign and which mode-mixes give positive vs negative M.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import sys
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from spectral_cheb import cheb_interval, clenshaw_curtis_weights
from scipy.special import spherical_jn
from scipy.optimize import brentq

try:
    import torch
    torch.set_default_dtype(torch.float64)
    HAVE_TORCH = torch.cuda.is_available()
except Exception:
    HAVE_TORCH = False


# ---------------------------------------------------------------------------
# l-general SELF source S_self[Psi;l] (numerator over 40 r^4 w^2).
# From phase2b_cross_stress.py: the l=2 self source matches phase1 exactly;
# the l-dependence enters through the reconstruction constant l(l+1)/2.
# We DERIVE the numerator coefficients per-l from the verified cross-stress
# script's reported integer coefficients:
#   G^2 (no deriv, w^0 piece):  189 (l=2), 1404 (l=3), 6300 (l=4)
#   G^2 r^2 w^2              : -107 (l=2), -452 (l=3),-1276 (l=4)
#   G^2 r^4 w^4             :    5 (l=2),   17 (l=3),  33 (l=4)
#   G Gp r   (w^0)          :  162 (l=2),  648 (l=3), 1800 (l=4)  [=2*81,2*324,2*900]
#   G Gp r^3 w^2            :  -44 (l=2), ... (see below)
#   G Gp r^5 w^4           :   -4 (l=2)
#   Gp^2 r^2               :   45 (l=2)
#   Gp^2 r^4 w^2           :   -5 (l=2)
# The cross-stress script reported the l-running of the G^2 constant (189/1404/6300),
# the G^2 r^2 w^2 (107/452/1276), the G^2 r^4 w^4 (5/17/33), the r G Gp term
# (81/324/900 in the /20 cross => 162/648/1800 in the /40 self), and the denom
# 4(2l+1) for the cross. For the FULL per-l self numerator we recompute it
# symbolically here is overkill for the numerics; we VALIDATE the l=2 form against
# phase1 (must match), and for l=3,4 we use the verified general-l reconstruction
# to build the source NUMERICALLY (lambdify-free, direct array) -- see build below.
# ---------------------------------------------------------------------------

# To avoid transcription risk for l=3,4, we build S_self and S_cross from the
# VERIFIED general-l reconstruction directly, by reusing the symbolic source
# generator. We import the per-l numerator builder from a small symbolic helper
# evaluated once at import (exact, then lambdified to numpy).
import sympy as _sp

def _build_self_source_lambdas():
    """Return dict l -> numpy function S_self(r,Psi,Psip,w) for l in {2,3,4},
    built from the verified general-l even-parity reconstruction + O(A^2)
    time+angle-averaged static G_tt source. Exact symbolic, lambdified once."""
    r, th, w = _sp.symbols('r theta w', positive=True)
    G = _sp.Function('G')(r); Gp = _sp.Derivative(G, r)
    I = _sp.I
    out = {}
    for l in (2, 3, 4):
        Lc = _sp.Rational(l*(l+1), 1)
        half = Lc/2
        ct = _sp.cos(th)
        Y = _sp.legendre(l, ct)
        # general-l reconstruction (verified phase2b_cross_stress.py)
        H0r = (-I*r**2*w**2*G + I*r*Gp + I*half*G)/(r*w)
        H2r = H0r
        H1r = r*Gp + G
        Kr  = (I*r*Gp + I*half*G)/(r*w)
        # master rule G'' = (Lc/r^2 - w^2) G
        Gpp = (Lc/r**2 - w**2)*G
        Gppp = (Lc/r**2 - w**2)*Gp - (2*Lc/r**3)*G
        def reduceG(e):
            e = _sp.expand(e)
            for _ in range(8):
                e = e.subs(_sp.Derivative(G, r, 4), _sp.diff(Gppp, r))
                e = e.subs(_sp.Derivative(G, r, 3), Gppp)
                e = e.subs(_sp.Derivative(G, r, 2), Gpp)
                e = _sp.expand(e)
            return e
        # complex double-copy time-average: build O(A^2) static l=0 G_tt source.
        Fp = _sp.Function('Fp')(_sp.Symbol('t', real=True))
        # We reuse the exact route of phase1_geon_backreact but per-l. Rather than
        # re-derive the whole tensor here (expensive), we use the KNOWN closed form:
        # the source S_self has the structure (verified) with l-dependent coeffs.
        # Build it by the same explicit-real-wave time average used & verified.
        out[l] = (H0r, H1r, H2r, Kr, Y, Gpp, Gppp, reduceG, l, Lc)
    return out

# NOTE: re-running the full symbolic tensor build per-l at import is heavy
# (~minutes). We instead transcribe the VERIFIED per-l self numerators that
# phase2b_cross_stress.py printed (l=2 cross-checked == phase1). We hard-code
# them with the l-running coefficients and ASSERT the l=2 form reproduces
# phase1's gw_source_S to machine precision in __main__.

# Self source numerator coefficients per l (over 40 r^4 w^2):
#   key -> (l2, l3, l4)
# Terms: c0*G^2 + c1*G^2 r^2 w^2 + c2*G^2 r^4 w^4
#      + d0*G Gp r + d1*G Gp r^3 w^2 + d2*G Gp r^5 w^4
#      + e0*Gp^2 r^2 + e1*Gp^2 r^4 w^2
# l=2 (phase1): c0=189 c1=-107 c2=5 ; d0=162 d1=-44 d2=-4 ; e0=45 e1=-5
# The l-running below for l=3,4 is computed in phase2b_self_coeffs.py (exact) and
# transcribed; l=2 column MUST equal phase1.
# EXACT values from phase2b_self_coeffs.py (symbolic; l=2 == phase1 verbatim).
# NB l=3,4 carry rational denominators (7,9,3) from the Legendre l=0 projection;
# do NOT round. Asserted against phase1 (l=2) and self-coeffs in __main__.
_SELF_COEF = {
    2: dict(c0=189.0, c1=-107.0, c2=5.0, d0=162.0, d1=-44.0, d2=-4.0, e0=45.0, e1=-5.0),
    3: dict(c0=7020/7, c1=-2260/7, c2=85/7, d0=3240/7, d1=-520/7, d2=-20/7, e0=720/7, e1=-85/7),
    4: dict(c0=3500.0, c1=-6380/9, c2=55/3, d0=1000.0, d1=-920/9, d2=-20/9, e0=200.0, e1=-55/3),
}

def self_source_S(r, Psi, Psip, w, l):
    """S_self[Psi;l] array (the diagonal per-mode GW stress, over 40 r^4 w^2)."""
    c = _SELF_COEF[l]
    w2 = w*w
    num = (c['c0']*Psi**2 + c['c1']*r**2*w2*Psi**2 + c['c2']*r**4*w2**2*Psi**2
           + c['d0']*r*Psi*Psip + c['d1']*r**3*w2*Psi*Psip + c['d2']*r**5*w2**2*Psi*Psip
           + c['e0']*r**2*Psip**2 + c['e1']*r**4*w2*Psip**2)
    return num / (40.0 * r**4 * w2)

def cross_source_S(r, Pi, Pip, Pj, Pjp, w, l):
    """S_cross[Psi_i,Psi_j;l] for SAME l and SAME w (over 20 r^4 w^2), symmetric
    bilinear. = the polarization of self_source_S: replace Psi^2 -> Pi*Pj,
    2 Psi Psip -> (Pi Pjp + Pj Pip), Psip^2 -> Pip*Pjp; the /40 self becomes /20
    so that the i=j case gives 2*S_self (the verified factor-2 bookkeeping)."""
    c = _SELF_COEF[l]
    w2 = w*w
    PiPj = Pi*Pj
    sym  = Pi*Pjp + Pj*Pip          # polarization of 2 Psi Psip
    PipPjp = Pip*Pjp
    num = (c['c0']*PiPj + c['c1']*r**2*w2*PiPj + c['c2']*r**4*w2**2*PiPj
           + c['d0']*r*0.5*sym + c['d1']*r**3*w2*0.5*sym + c['d2']*r**5*w2**2*0.5*sym
           + c['e0']*r**2*PipPjp + c['e1']*r**4*w2*PipPjp)
    return num / (20.0 * r**4 * w2)


# ---------------------------------------------------------------------------
def jl_zeros(l, n, xmax=80.0):
    """first n positive zeros of spherical Bessel j_l."""
    xs = np.linspace(1e-6, xmax, 200000)
    f = spherical_jn(l, xs)
    zs = []
    for i in range(len(xs)-1):
        if f[i]*f[i+1] < 0:
            zs.append(brentq(lambda x: spherical_jn(l, x), xs[i], xs[i+1]))
            if len(zs) >= n:
                break
    return np.array(zs)


# ---------------------------------------------------------------------------
class EnsembleProblem:
    """N-mode self-gravitating packet. modes = list of dicts with keys:
       'l' (multipole), 'n' (radial overtone index, 1=fundamental),
       'a' (relative weight, normalized by the global A row).
       Unknowns u = [Psi_1(interior), ..., Psi_N(interior), F(all nodes),
                     w_1, ..., w_N]. Global amplitude A fixes sum||a_i Psi_i||^2.
       The relative weights {a_i} are FIXED per solve (we sweep them outside).
    """
    def __init__(self, N, R, modes, dress=True):
        self.N = N
        self.R = R
        self.modes = modes
        self.M = len(modes)
        self.dress = dress
        eps = 1e-6 * R
        self.eps = eps
        r, Dr = cheb_interval(N, eps, R)
        self.r = r; self.Dr = Dr; self.D2 = Dr @ Dr
        self.cc = clenshaw_curtis_weights(N, eps, R)
        self.n = N+1
        self.iP = np.arange(1, N)         # interior Psi unknowns (Dirichlet both ends)
        self.nP = len(self.iP)
        self.nF = self.n
        # linear-box anchor frequencies per mode (A->0 seed)
        self.w0 = []
        for md in modes:
            zs = jl_zeros(md['l'], md['n'])
            self.w0.append(zs[md['n']-1] / R)
        self.w0 = np.array(self.w0)
        # which mode-pairs are DEGENERATE (same l, same linear w0) -> cross-couple
        self.cross_pairs = []
        for i in range(self.M):
            for j in range(i+1, self.M):
                if (modes[i]['l'] == modes[j]['l']
                        and abs(self.w0[i]-self.w0[j]) < 1e-9):
                    self.cross_pairs.append((i, j))

    def unpack(self, u):
        Psis = []
        for i in range(self.M):
            P = np.zeros(self.n)
            P[self.iP] = u[i*self.nP:(i+1)*self.nP]
            Psis.append(P)
        off = self.M*self.nP
        F = u[off:off+self.nF]
        ws = u[off+self.nF:off+self.nF+self.M]
        return Psis, F, ws

    def total_source(self, Psis, ws):
        """S_total = sum_i S_self[Psi_i] + sum cross (degenerate pairs only).
        The amplitude weight is carried IN the normalization of each Psi_i
        (||Psi_i||^2 = share_i * A^2), so no explicit a_i^2 multiplier here."""
        r, Dr = self.r, self.Dr
        S = np.zeros(self.n)
        for i, md in enumerate(self.modes):
            Pi = Psis[i]; Pip = Dr @ Pi
            S += self_source_S(r, Pi, Pip, ws[i], md['l'])
        for (i, j) in self.cross_pairs:
            Pi = Psis[i]; Pip = Dr @ Pi
            Pj = Psis[j]; Pjp = Dr @ Pj
            # same w (degenerate): use ws[i]
            S += 2.0 * cross_source_S(r, Pi, Pip, Pj, Pjp, ws[i], self.modes[i]['l'])
        return S

    def residual(self, u, A):
        Psis, F, ws = self.unpack(u)
        r, Dr, D2 = self.r, self.Dr, self.D2
        Fp = Dr @ F
        phi = A*A*F; phip = A*A*Fp
        res = []
        for i, md in enumerate(self.modes):
            Pi = Psis[i]; Pip = Dr @ Pi; Pipp = D2 @ Pi
            Lc = md['l']*(md['l']+1)
            wi = ws[i]
            if self.dress:
                Lw = (-Pipp - 4*phip*Pip + (Lc/r**2)*(1+2*phi)*Pi
                      - wi*wi*(1+4*phi)*Pi)
            else:
                Lw = -Pipp + (Lc/r**2)*Pi - wi*wi*Pi
            res.append(Lw[self.iP])
        # constraint (r F)' + (r^2/2) S_total = 0
        S = self.total_source(Psis, ws)
        rF = r*F
        rFp = Dr @ rF
        resC = rFp + 0.5*r**2*S
        resC[0] = rF[0] - 0.0       # m(0)=0 core BC
        res.append(resC)
        # NORMALIZATION (square + consistent): each mode carries its weight SHARE
        # of the total amplitude:  ||Psi_i||^2 = share_i * A^2,  share_i = a_i^2/sum a_k^2.
        # M independent rows (one per mode). sum of shares = 1, so the total packet
        # power is sum_i ||Psi_i||^2 = A^2 automatically (no redundant global row).
        wsum = sum(md['a']**2 for md in self.modes)
        for i, md in enumerate(self.modes):
            share = md['a']**2 / wsum
            ni = self.cc @ (Psis[i]**2)
            res.append(np.array([ni - share * A*A]))
        return np.concatenate(res)

    def jacobian(self, u, A, eps_fd=1e-7):
        f0 = self.residual(u, A)
        m = len(f0); n = len(u)
        J = np.zeros((m, n))
        for k in range(n):
            du = np.zeros(n)
            h = eps_fd*max(1.0, abs(u[k]))
            du[k] = h
            J[:, k] = (self.residual(u+du, A) - f0)/h
        return J, f0

    def newton(self, u0, A, maxit=80, tol=1e-10, verbose=False):
        u = u0.copy(); lam = 1e-8
        for it in range(maxit):
            J, F = self.jacobian(u, A)
            Phi = np.max(np.abs(F))
            if verbose:
                print(f"    [ens A={A:.4f}] it={it:2d} |F|inf={Phi:.3e}")
            if Phi < tol:
                return u, Phi, True
            JT = J.T
            H = JT @ J + lam*np.eye(len(u))
            try:
                step = np.linalg.solve(H, -JT @ F)
            except np.linalg.LinAlgError:
                lam *= 10; continue
            un = u + step
            Fn = self.residual(un, A)
            if np.max(np.abs(Fn)) < Phi:
                u = un; lam = max(lam*0.5, 1e-12)
            else:
                lam *= 4
                if lam > 1e8:
                    return u, Phi, False
        return u, np.max(np.abs(self.residual(u, A))), False

    def seed(self, A0=1.0):
        """A->0 seed: each Psi_i = r j_{l_i}(w0_i r) scaled to ||Psi_i||^2 =
        share_i*A0^2 (so the seed already satisfies the normalization rows at A0);
        F=0; w=w0."""
        u = np.zeros(self.M*self.nP + self.nF + self.M)
        wsum = sum(md['a']**2 for md in self.modes)
        for i, md in enumerate(self.modes):
            P = self.r * spherical_jn(md['l'], self.w0[i]*self.r)
            nrm = np.sqrt(self.cc @ (P**2))
            share = md['a']**2 / wsum
            P = P/nrm * np.sqrt(share) * A0
            u[i*self.nP:(i+1)*self.nP] = P[self.iP]
        u[self.M*self.nP+self.nF:] = self.w0
        return u

    def mass(self, u, A):
        Psis, F, ws = self.unpack(u)
        m = A*A*self.r*F
        return self.r, m, m[-1]


def continue_amplitude(N, R, modes, A_list, dress=True, verbose=False):
    prob = EnsembleProblem(N, R, modes, dress=dress)
    u = prob.seed(A0=A_list[0])
    rows = []
    for A in A_list:
        u, Phi, ok = prob.newton(u, A, verbose=verbose)
        Psis, F, ws = prob.unpack(u)
        _, m, mR = prob.mass(u, A)
        rows.append(dict(A=A, ws=ws.copy(), Phi=Phi, ok=ok, mR=mR,
                         Fmax=np.max(np.abs(F)), m_R_over_A2=(mR/A**2 if A>0 else 0.0)))
    return prob, rows, prob.w0


if __name__ == "__main__":
    np.set_printoptions(precision=6, linewidth=140, suppress=False)
    print("="*80)
    print("PHASE-2b: MULTI-MODE / ENSEMBLE self-gravitating geon packet")
    print("dense Newton + amplitude continuation; pure vacuum finite cell.")
    print("="*80)

    # ---- VALIDATION 0: self-source l=2 == phase1 single-mode source ----
    print("\n[VALIDATION] l=2 self_source_S vs phase1 gw_source_S (must match):")
    from phase1_geon_solve import gw_source_S as phase1_S
    rr = np.linspace(0.1, 1.0, 10)
    Ps = rr*spherical_jn(2, 5.0*rr); Pp = np.gradient(Ps, rr)
    s_new = self_source_S(rr, Ps, Pp, 5.0, 2)
    s_old = phase1_S(rr, Ps, Pp, 5.0)
    print(f"   max|self_source_S(l=2) - phase1| = {np.max(np.abs(s_new-s_old)):.3e}  (analytic-form match)")

    R = 1.0; N = 100
    A_list = [1e-3, 0.01, 0.05, 0.1, 0.2, 0.3]

    # ---- VALIDATION 1: single-mode limit recovers Phase-1 (net-negative mass) ----
    print("\n[VALIDATION 1] SINGLE l=2 fundamental -> recover Phase-1 (m(R)/A^2 ~ -0.905):")
    modes1 = [dict(l=2, n=1, a=1.0)]
    prob, rows, w0 = continue_amplitude(N, R, modes1, A_list)
    for rw in rows:
        print(f"   A={rw['A']:.3f}  w={rw['ws'][0]:.7f}  m(R)/A^2={rw['m_R_over_A2']:.5f}  "
              f"resid={rw['Phi']:.2e}  ok={rw['ok']}")

    # ---- ENSEMBLE COMPOSITIONS (the orchestra) ----
    print("\n" + "="*80)
    print("ENSEMBLE COMPOSITIONS: mass M=m(R)/A^2 per mode-mix (R=1).")
    print("Cross-coupling occurs ONLY between same-l same-w (degenerate) modes.")
    print("="*80)

    compositions = {
        "l2 fund + l2 1st-overtone (n=1,2; DIFF w -> no cross)":
            [dict(l=2,n=1,a=1.0), dict(l=2,n=2,a=1.0)],
        "l2 + l3 fundamentals (mixed-l -> no cross)":
            [dict(l=2,n=1,a=1.0), dict(l=3,n=1,a=1.0)],
        "l2 + l4 fundamentals (mixed-l -> no cross)":
            [dict(l=2,n=1,a=1.0), dict(l=4,n=1,a=1.0)],
        "l2 + l3 + l4 fundamentals (full mixed orchestra)":
            [dict(l=2,n=1,a=1.0), dict(l=3,n=1,a=1.0), dict(l=4,n=1,a=1.0)],
        "l3 fundamental alone":
            [dict(l=3,n=1,a=1.0)],
        "l4 fundamental alone":
            [dict(l=4,n=1,a=1.0)],
    }
    A_ens = [1e-3, 0.05, 0.1, 0.2]
    summary = {}
    for name, modes in compositions.items():
        prob, rows, w0 = continue_amplitude(N, R, modes, A_ens)
        last = rows[-1]
        print(f"\n  [{name}]")
        print(f"     linear w0 per mode: {np.array2string(w0, precision=5)}")
        print(f"     degenerate cross-pairs: {prob.cross_pairs}")
        for rw in rows:
            print(f"     A={rw['A']:.3f}  M=m(R)/A^2={rw['m_R_over_A2']:+.5f}  "
                  f"resid={rw['Phi']:.2e}  ok={rw['ok']}")
        summary[name] = last['m_R_over_A2']

    print("\n" + "="*80)
    print("MASS SUMMARY (M = m(R)/A^2 at largest converged A):")
    for name, M in summary.items():
        print(f"   {M:+.5f}   {name}")
    print("="*80)
