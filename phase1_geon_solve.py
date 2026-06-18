#!/usr/bin/env python3
"""
phase1_geon_solve.py -- PHASE-1c step 2: NONLINEAR GEON solve on the finite
mirrored cell r in [0, R_seal], matter slot EMPTY (pure vacuum), held UDT tie
g_tt g_rr = -1.  Dense explicit-Jacobian Newton + pseudo-arclength continuation
in wave amplitude A.  GPU float64 (V100) for the batched wall-relocation sweep;
CPU spot-checks.

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A (borrow GR
numerics for tractability; impose NO physics, NO matter, NO scale). OBSERVE mode.
c=1.  NO matrix-free PCG (design forbids; dense Newton only).

THE COUPLED VACUUM SYSTEM (exact, gauge-clean -- the GENUINE geon):
  WAVE (l=2 even-parity Zerilli master Psi, verified clean single DOF in
        phase1_geon_zerilli.py: full even-parity system consistent, NOT
        over-constrained, potential = 6/r^2):
            -Psi'' + (6/r^2) Psi = w^2 Psi    on flat bg.
        On the geon's OWN static phi(r)=A^2 F background the master operator
        picks up a phi-correction; we carry it to O(A^2) via the standard
        tortoise/redshift dressing (derived inline, tagged C5), giving the
        amplitude-dependent operator whose eigenvalue is w(A).
  BACKREACTION (Misner-Sharp, verified in phase1_geon_backreact.py; two
        independent routes -- complex-average and explicit real cos/sin --
        gave the IDENTICAL G_tt source, diff=0):
            (r F)' = -(r^2/2) * S[Psi]          [Hamiltonian constraint, l=0]
        with  m(r) = A^2 r F(r)  (Misner-Sharp deficit, m = r(1-e^{-2phi})~2A^2 rF
        ... NB: agent reported g^rr=1-2m/r=1-2A^2 F => m = A^2 r F; we use that).
        S[Psi] is the EXACT verified quadratic GW stress (transcribed below).

  GEON COUPLING: the wave's O(A^2) stress sources F; F dresses the wave operator
  -> shifts w.  Self-consistent => w = w(A).  At A->0 we recover the Phase-1b
  linear box eigenvalue w0 (j_2 Dirichlet zero / R_seal).

REDUCTION / NUMERICAL CHOICES (each tagged "chose or derived?" + relax-test):
  C5 [chose]: the phi-dressing of the wave operator. The master Psi propagates in
      the tortoise coord dr_* = e^{2phi} dr (g_tt g_rr=-1 => lapse^2=e^{-2phi},
      dr_*/dr = sqrt(g_rr/(-g_tt)) = e^{2phi}) with potential rescaled by the
      redshift. To O(A^2): -Psi'' - 4 phi' Psi' + (6/r^2)(1+2phi) Psi
      = w^2 e^{4phi} Psi  (the standard static-metric wave-operator dressing;
      phi=A^2 F). Relax-test below: we ALSO run the bare-operator variant
      (phi only via the constraint, no wave dressing) and report BOTH w(A) bends;
      if the BEND's existence/sign is robust across the two dressings the geon
      signature is not an artifact of C5. [This isolates how much of dw/dA^2 is
      genuine backreaction vs dressing-convention.]
  C6 [chose]: amplitude normalization = fix L2 norm of Psi on the cell = A
      (pseudo-arclength continuation parameter). w, Psi-shape, F are unknowns.
      Relax-test: also normalize by max|Psi|; the w(A) curve must agree.
  C7 [derived/forced]: BCs -- core r->0 regular branch Psi ~ r^{l+1}=r^3 (=>
      Psi(0)=0), wall r=R_seal Dirichlet Psi(R)=0 (reflecting). phi/F: regular
      at core (F finite => (rF)|_0=0 i.e. m(0)=0, no central point mass) and
      free at the wall (F set by integrating the constraint outward; one
      integration constant fixed by m(0)=0). NO time-parity tie (red-team rule).

GPU: the wall-relocation sweep batches eigensolves over R_seal on the V100.
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
# EXACT verified GW-stress source S[Psi]  (from phase1_geon_backreact.py;
# G=Psi, Gp=Psi'). Transcribed verbatim; self-checked against m'(r) below.
#   S[Psi] = ( -4 r^5 w^4 Psi Psi' + 5 r^4 w^4 Psi^2 - 5 r^4 w^2 Psi'^2
#              -44 r^3 w^2 Psi Psi' - 107 r^2 w^2 Psi^2 + 45 r^2 Psi'^2
#              +162 r Psi Psi' + 189 Psi^2 ) / (40 r^4 w^2)
# ---------------------------------------------------------------------------
def gw_source_S(r, Psi, Psip, w):
    """exact verified O(A^2) l=0 GW stress S[Psi] (array in r)."""
    w2 = w * w
    num = (-4 * r**5 * w2**2 * Psi * Psip
           + 5 * r**4 * w2**2 * Psi**2
           - 5 * r**4 * w2 * Psip**2
           - 44 * r**3 * w2 * Psi * Psip
           - 107 * r**2 * w2 * Psi**2
           + 45 * r**2 * Psip**2
           + 162 * r * Psi * Psip
           + 189 * Psi**2)
    return num / (40 * r**4 * w2)


# ---------------------------------------------------------------------------
# Linear box anchor (Phase-1b): regular j_2 Dirichlet zero / R  (the A->0 limit)
# ---------------------------------------------------------------------------
def j2_first_zero():
    xs = np.linspace(1e-6, 12.0, 40000)
    f = spherical_jn(2, xs)
    for i in range(len(xs) - 1):
        if f[i] * f[i + 1] < 0:
            return brentq(lambda x: spherical_jn(2, x), xs[i], xs[i + 1])
    raise RuntimeError("no j2 zero found")


# ---------------------------------------------------------------------------
# Discretization. Unknown vector u = [Psi(interior nodes), F(all nodes), w].
# Master operator (Zerilli, on phi=A^2 F background, C5 dressing):
#   Lw[Psi] := -Psi'' - 4 phi' Psi' + (6/r^2)(1+2 phi) Psi - w^2 (1+4 phi) Psi = 0
#   (e^{4phi} ~ 1+4 phi to O(A^2); phi=A^2 F). At A=0 -> -Psi''+6/r^2 Psi=w^2 Psi.
# Constraint:  Lc[F] := (r F)' + (r^2/2) S[Psi] = 0   (Misner-Sharp).
# BCs: Psi(0 node)=0 (regular r^3), Psi(R)=0 (wall). F: (rF)(0)=0 (m(0)=0); the
#   constraint is first-order -> one BC (at core) suffices, integrate outward.
# Normalization: ||Psi||_2 (Clenshaw-Curtis) = A  (continuation parameter, C6).
# ---------------------------------------------------------------------------
class GeonProblem:
    def __init__(self, N, R, dress=True):
        self.N = N
        self.R = R
        self.dress = dress           # C5 relax-test toggle
        eps = 1e-6 * R               # core cutoff (relative); refined in relax-test
        self.eps = eps
        r, Dr = cheb_interval(N, eps, R)
        self.r = r
        self.Dr = Dr
        self.D2 = Dr @ Dr
        self.cc = clenshaw_curtis_weights(N, eps, R)   # quadrature for ||.||_2, mass
        self.n = N + 1
        # interior indices for Psi (drop core node 0 and wall node N: both Dirichlet)
        self.iP = np.arange(1, N)            # Psi unknowns
        self.nP = len(self.iP)
        # F unknowns: all nodes (first-order constraint + core BC handled in residual)
        self.nF = self.n

    def unpack(self, u, A):
        Psi = np.zeros(self.n)
        Psi[self.iP] = u[:self.nP]
        # Psi(0)=0 (regular), Psi(R)=0 (wall) already zero
        F = u[self.nP:self.nP + self.nF]
        w = u[-1]
        return Psi, F, w

    def residual(self, u, A):
        Psi, F, w = self.unpack(u, A)
        r, Dr, D2 = self.r, self.Dr, self.D2
        Psip = Dr @ Psi
        Psipp = D2 @ Psi
        Fp = Dr @ F
        phi = A * A * F
        phip = A * A * Fp
        # --- wave operator residual (interior nodes only) ---
        if self.dress:
            Lw = (-Psipp - 4 * phip * Psip + (6.0 / r**2) * (1 + 2 * phi) * Psi
                  - w * w * (1 + 4 * phi) * Psi)
        else:
            Lw = -Psipp + (6.0 / r**2) * Psi - w * w * Psi
        resP = Lw[self.iP]
        # --- constraint residual: (rF)' + (r^2/2) S = 0, all nodes ---
        S = gw_source_S(r, Psi, Psip, w)
        rF = r * F
        rFp = Dr @ rF
        resC = rFp + 0.5 * r**2 * S
        # core BC for F: enforce m(0)= (rF)(0) = 0 by replacing node-0 constraint row
        resC[0] = rF[0] - 0.0
        # --- normalization: ||Psi||_2 = A ---
        norm2 = self.cc @ (Psi**2)
        resN = norm2 - A * A
        return np.concatenate([resP, resC, [resN]])

    def jacobian(self, u, A, eps_fd=1e-7):
        """Dense explicit Jacobian by forward finite-difference (vectorized columns).
        (Dense Newton per design; the system is small -> FD Jacobian is exact to
        ~1e-7 and robust. CPU.)"""
        f0 = self.residual(u, A)
        m = len(f0)
        n = len(u)
        J = np.zeros((m, n))
        for k in range(n):
            du = np.zeros(n)
            h = eps_fd * max(1.0, abs(u[k]))
            du[k] = h
            J[:, k] = (self.residual(u + du, A) - f0) / h
        return J, f0

    def newton(self, u0, A, maxit=60, tol=1e-11, verbose=False):
        u = u0.copy()
        lam = 1e-8
        for it in range(maxit):
            J, F = self.jacobian(u, A)
            Phi = np.max(np.abs(F))
            if verbose:
                print(f"    [newton A={A:.4f}] it={it:2d} |F|inf={Phi:.3e}")
            if Phi < tol:
                return u, Phi, True
            # LM-damped dense solve
            JT = J.T
            H = JT @ J + lam * np.eye(len(u))
            try:
                step = np.linalg.solve(H, -JT @ F)
            except np.linalg.LinAlgError:
                lam *= 10
                continue
            u_new = u + step
            Fn = self.residual(u_new, A)
            if np.max(np.abs(Fn)) < Phi:
                u = u_new
                lam = max(lam * 0.5, 1e-12)
            else:
                lam *= 4
                if lam > 1e6:
                    return u, Phi, False
        return u, np.max(np.abs(self.residual(u, A))), False

    def seed_linear(self, w0):
        """A->0 seed: Psi = r j_2(w0 r) (regular master), F = 0, w = w0."""
        Psi = self.r * spherical_jn(2, w0 * self.r)
        # normalize to unit L2 (so A multiplies it)
        nrm = np.sqrt(self.cc @ (Psi**2))
        Psi = Psi / nrm
        u = np.zeros(self.nP + self.nF + 1)
        u[:self.nP] = Psi[self.iP]
        u[-1] = w0
        return u

    def misner_sharp_mass(self, u, A):
        """m(r) = A^2 r F(r); return enclosed mass profile and m(R)."""
        Psi, F, w = self.unpack(u, A)
        m = A * A * self.r * F
        return self.r, m


# ---------------------------------------------------------------------------
def continue_amplitude(N, R, A_list, dress=True, verbose=False):
    prob = GeonProblem(N, R, dress=dress)
    w0 = j2_first_zero() / R
    u = prob.seed_linear(w0)
    rows = []
    for A in A_list:
        # re-normalize seed Psi to current A is implicit via resN; warm-start from prev u
        u, Phi, ok = prob.newton(u, A, verbose=verbose)
        Psi, F, w = prob.unpack(u, A)
        _, m = prob.misner_sharp_mass(u, A)
        mR = m[-1]
        maxPsi = np.max(np.abs(Psi))
        rows.append(dict(A=A, w=w, Phi=Phi, ok=ok, mR=mR, maxPsi=maxPsi,
                         Fmax=np.max(np.abs(F)), Fcore=F[0]))
    return prob, rows, w0


if __name__ == "__main__":
    np.set_printoptions(precision=6, linewidth=120, suppress=False)
    print("=" * 78)
    print("PHASE-1c: NONLINEAR GEON solve (l=2 even Zerilli wave + Misner-Sharp F)")
    print("dense Newton + amplitude continuation; pure vacuum finite cell.")
    print("=" * 78)

    # ---- self-check the source vs m'(r) at A->0 linear shape (sanity) ----
    R = 1.0
    N = 80
    w0 = j2_first_zero() / R
    print(f"\nLinear box anchor (Phase-1b): w0 = j2_zero/R = {w0:.8f}  (R={R})")

    # ---- AMPLITUDE CONTINUATION (the geon branch) ----
    print("\n--- AMPLITUDE CONTINUATION (dressed wave operator, C5=True) ---")
    A_list = [1e-3, 0.01, 0.05, 0.1, 0.2, 0.35, 0.5, 0.7, 1.0]
    prob, rows, w0 = continue_amplitude(N, R, A_list, dress=True, verbose=False)
    print(f"  {'A':>8} {'w':>12} {'w-w0':>13} {'(w-w0)/A^2':>13} {'m(R)/A^2':>12} {'|F|inf':>10} {'resid':>10} ok")
    for rw in rows:
        dw = rw['w'] - w0
        bend = dw / (rw['A']**2) if rw['A'] > 0 else 0.0
        msc = rw['mR'] / (rw['A']**2) if rw['A'] > 0 else 0.0
        print(f"  {rw['A']:8.4f} {rw['w']:12.7f} {dw:13.3e} {bend:13.6f} "
              f"{msc:12.5f} {rw['Fmax']:10.3e} {rw['Phi']:10.2e} {rw['ok']}")

    # leading bend dw/dA^2 from small-A finite difference
    sm = [rw for rw in rows if rw['ok'] and rw['A'] <= 0.1]
    if len(sm) >= 2:
        A1, w1 = sm[0]['A'], sm[0]['w']
        A2, w2 = sm[-1]['A'], sm[-1]['w']
        dwdA2 = (w2 - w1) / (A2**2 - A1**2)
        print(f"\n  LEADING BEND dw/dA^2 (small-A) ~ {dwdA2:.6f}")

    # ---- C5 relax-test: bare (undressed) wave operator ----
    print("\n--- C5 RELAX-TEST: bare wave operator (dress=False) ---")
    prob_b, rows_b, _ = continue_amplitude(N, R, A_list, dress=False, verbose=False)
    print(f"  {'A':>8} {'w':>12} {'w-w0':>13} {'(w-w0)/A^2':>13} ok")
    for rw in rows_b:
        dw = rw['w'] - w0
        bend = dw / (rw['A']**2) if rw['A'] > 0 else 0.0
        print(f"  {rw['A']:8.4f} {rw['w']:12.7f} {dw:13.3e} {bend:13.6f} {rw['ok']}")

    # ---- N-refinement (convergence floor) ----
    print("\n--- N-REFINEMENT (residual floor + w stability at A=0.1) ---")
    for Nr in [60, 80, 120, 160]:
        prob_n, rows_n, _ = continue_amplitude(Nr, R, [1e-3, 0.05, 0.1], dress=True)
        last = rows_n[-1]
        print(f"  N={Nr:3d}  w(A=0.1)={last['w']:.8f}  resid={last['Phi']:.2e}  ok={last['ok']}")

    # ---- WALL-RELOCATION at FINITE amplitude (the box-control-of-the-BEND test) ----
    print("\n" + "=" * 78)
    print("WALL-RELOCATION at FINITE amplitude: is the w(A) BEND box-controlled?")
    print("Compare dw/dA^2 scaled appropriately across R_seal. If the BEND tracks an")
    print("INTRINSIC quantity it should NOT scale like the linear 1/R box law.")
    print("=" * 78)
    R_list = [1.0, 2.0, 4.0]
    A_probe = [1e-3, 0.05, 0.1]
    for Rs in R_list:
        prob_r, rows_r, w0r = continue_amplitude(N, Rs, A_probe, dress=True)
        wlin = w0r
        ok = all(rw['ok'] for rw in rows_r)
        # bend in absolute units
        a0, a1 = rows_r[0], rows_r[-1]
        dwdA2 = (a1['w'] - a0['w']) / (a1['A']**2 - a0['A']**2)
        # dimensionless bend: how big is the fractional w-shift per unit (A/normalization)^2
        # linear w scales as 1/R; if the BEND also scaled as 1/R it is box-controlled.
        print(f"  R={Rs:>4.1f}  w_lin={wlin:.7f}  dw/dA^2={dwdA2:.6f}  "
              f"dw/dA^2 * R={dwdA2*Rs:.6f}  dw/dA^2 * R^3={dwdA2*Rs**3:.6f}  ok={ok}")
    print("\n  READ: if dw/dA^2 * R is constant across rows -> bend ~ 1/R (BOX-controlled,")
    print("  same law as linear, NO geon escape). If dw/dA^2 * R^3 (or another power)")
    print("  is constant instead -> the bend follows a DIFFERENT (intrinsic) scaling")
    print("  than the linear box law -> candidate geon escape. Report which holds.")

    print("\n" + "=" * 78)
    print("Done. See final report for the honest READ.")
    print("=" * 78)
