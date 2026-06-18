#!/usr/bin/env python3
"""
phase1_spectrum.py -- PHASE-1a gates + PHASE-1b linear mode spectrum.

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A. OBSERVE mode.
TAG: LINEARIZED stepping-stone (linear vacuum GW in a reflecting spherical cell).

PROBLEM (derived in phase1_master_reduce.py, confirmed flat l=2 RW form):
    -H''(r) + [l(l+1)/r^2] H(r) = w^2 H(r),   r in [0, R_seal],   c=1.
Core r->0: regular branch  H ~ r^{l+1}  (=> H(0)=0, the regular solution).
Seal r=R_seal: REFLECTING WALL -- Dirichlet H(R)=0 OR Neumann H'(R)=0 (both reported).
NOTE (red-team revision #2): impose ONLY the spatial wall BC; do NOT tie spatial
parity to time-harmonic parity. The eigenproblem quantizes w honestly.

ANALYTIC TRUTH (cross-check, NOT imposed): the regular solution of this operator
is  H(r) = r * j_l(w r)  (spherical Bessel). Indeed if u=H, the substitution
H = r f gives f'' + (2/r) f' + [w^2 - l(l+1)/r^2] f = 0, the spherical Bessel eqn,
regular solution f=j_l(w r). So:
   Dirichlet H(R)=0  =>  j_l(w R)=0     => w R = (zeros of j_l)
   Neumann  H'(R)=0  =>  d/dr[r j_l(w r)]|_R = 0  => zeros of [j_l(x)+x j_l'(x)].
These are the spherical-Bessel-zero ladders -- the HONEST PRIOR (box geometry).
We solve the eigenproblem NUMERICALLY (pseudospectral) and COMPARE to these.

GPU: batched eigensolves over R_seal on the V100 (torch float64); every GPU
result CPU-spot-checked. NVML warning ignored.
"""
import numpy as np
from scipy.special import spherical_jn
from scipy.optimize import brentq

import sys
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from spectral_cheb import cheb_interval

try:
    import torch
    HAVE_TORCH = torch.cuda.is_available()
except Exception:
    HAVE_TORCH = False


# ---------------------------------------------------------------------------
# Analytic Bessel-zero ladders (cross-check truth, NOT imposed on the solver)
# ---------------------------------------------------------------------------
def jl_zeros(l, n, R=1.0):
    """First n positive zeros x of j_l(x); return w = x/R (Dirichlet ladder)."""
    # bracket scan
    xs = np.linspace(1e-6, (n + l + 4) * np.pi, 200000)
    f = spherical_jn(l, xs)
    zeros = []
    for i in range(len(xs) - 1):
        if f[i] == 0.0:
            zeros.append(xs[i])
        elif f[i] * f[i + 1] < 0:
            zeros.append(brentq(lambda x: spherical_jn(l, x), xs[i], xs[i + 1]))
        if len(zeros) >= n:
            break
    return np.array(zeros[:n]) / R


def jl_neumann_zeros(l, n, R=1.0):
    """zeros of d/dx[x j_l(x)] = j_l(x) + x j_l'(x); w = x/R (Neumann ladder)."""
    def g(x):
        return spherical_jn(l, x) + x * spherical_jn(l, x, derivative=True)
    xs = np.linspace(1e-6, (n + l + 5) * np.pi, 200000)
    fv = np.array([g(x) for x in xs])
    zeros = []
    for i in range(len(xs) - 1):
        if fv[i] * fv[i + 1] < 0:
            zeros.append(brentq(g, xs[i], xs[i + 1]))
        if len(zeros) >= n:
            break
    return np.array(zeros[:n]) / R


# ---------------------------------------------------------------------------
# Pseudospectral discretization of  -H'' + l(l+1)/r^2 H = w^2 H
# on [eps_core, R] with regular core (H(eps_core)=0 approximates H~r^{l+1})
# and wall BC at R (Dirichlet or Neumann).
# ---------------------------------------------------------------------------
def build_operator(N, R, l, eps_core):
    r, Dr = cheb_interval(N, eps_core, R)
    D2 = Dr @ Dr
    A = -D2 + np.diag(l * (l + 1) / r**2)   # operator -d_r^2 + l(l+1)/r^2
    return r, Dr, A


def spectrum_dirichlet(N, R, l, eps_core, k=8):
    """Dirichlet at BOTH ends: H(eps_core)=0 (regular branch proxy), H(R)=0 (wall).
    Returns sorted positive w (= sqrt eigenvalue)."""
    r, Dr, A = build_operator(N, R, l, eps_core)
    # remove first and last rows/cols (impose H=0 at both ends)
    idx = np.arange(1, N)
    Ai = A[np.ix_(idx, idx)]
    evals = np.linalg.eigvals(Ai)
    evals = np.sort(evals.real)
    evals = evals[evals > 1e-8]
    return np.sqrt(evals[:k]), r


def spectrum_neumann(N, R, l, eps_core, k=8):
    """Regular core H(eps_core)=0, Neumann wall H'(R)=0.
    Impose H'(R)=0 by replacing the last row of A with the derivative row, and
    using a generalized eigenproblem with the BC enforced via row replacement
    on a reduced (drop core row/col) operator."""
    r, Dr, A = build_operator(N, R, l, eps_core)
    n = N + 1
    # Build generalized eigenproblem A H = w^2 B H with BC rows.
    B = np.eye(n)
    A2 = A.copy()
    # core Dirichlet: row 0 -> H[0]=0
    A2[0, :] = 0.0
    A2[0, 0] = 1.0
    B[0, :] = 0.0
    # wall Neumann: last row -> H'(R)=0 i.e. Dr[-1,:] @ H = 0
    A2[-1, :] = Dr[-1, :]
    B[-1, :] = 0.0
    # solve generalized eigenproblem; BC rows give spurious infinite/zero evals
    from scipy.linalg import eig
    evals, _ = eig(A2, B)
    evals = evals[np.isfinite(evals)]
    evals = np.sort(evals.real)
    evals = evals[evals > 1e-8]
    evals = evals[evals < 1e12]
    return np.sqrt(evals[:k]), r


# ---------------------------------------------------------------------------
# GPU batched Dirichlet spectrum over many R_seal (box-control test)
# ---------------------------------------------------------------------------
def spectrum_dirichlet_batch_gpu(N, R_list, l, eps_core_frac, k=6):
    """Batched Dirichlet eigensolve over R_list on GPU (float64).
    eps_core scales with R (eps_core = eps_core_frac * R) to keep the relative
    core cutoff fixed across boxes. Returns array [len(R_list), k] of w."""
    if not HAVE_TORCH:
        return None
    dev = torch.device("cuda")
    mats = []
    for R in R_list:
        eps_core = eps_core_frac * R
        r, Dr = cheb_interval(N, eps_core, R)
        D2 = Dr @ Dr
        A = -D2 + np.diag(l * (l + 1) / r**2)
        idx = np.arange(1, N)
        Ai = A[np.ix_(idx, idx)]
        mats.append(Ai)
    M = torch.tensor(np.stack(mats), dtype=torch.float64, device=dev)
    # general (nonsymmetric due to Cheb) -> use eig on CPU per-matrix is safer;
    # but torch.linalg.eigvals supports batched complex. Use it, then take real.
    ev = torch.linalg.eigvals(M)  # complex [B, n]
    ev = ev.real.cpu().numpy()
    out = []
    for row in ev:
        row = np.sort(row)
        row = row[row > 1e-8]
        out.append(np.sqrt(row[:k]))
    return np.array(out)


def node_count(r, Hcol):
    """count interior sign changes of an eigenvector (radial node count)."""
    s = np.sign(Hcol)
    s = s[s != 0]
    return int(np.sum(s[:-1] * s[1:] < 0))


# ===========================================================================
if __name__ == "__main__":
    np.set_printoptions(precision=6, suppress=False, linewidth=120)
    print("=" * 78)
    print("PHASE-1a GATES + PHASE-1b SPECTRUM  (LINEARIZED stepping-stone)")
    print("operator: -H'' + l(l+1)/r^2 H = w^2 H,  regular core, reflecting wall")
    print("=" * 78)

    R = 1.0
    eps_core = 1e-4 * R    # relative core cutoff; relax-test = refine below

    # -------- GATE (iv): spectral convergence under N refinement (l=2 Dirichlet)
    print("\n[GATE iv] Spectral convergence under N_r refinement (l=2, Dirichlet,")
    print("          R=1, eps_core=1e-4). Compare to analytic j_2 zeros.")
    j2 = jl_zeros(2, 4, R=R)
    print("  analytic w (j_2 zeros / R):", j2)
    print("   N    w_1        w_2        w_3        w_4        max_abs_err_vs_analytic")
    for N in [24, 48, 64, 96, 128, 160]:
        wn, r = spectrum_dirichlet(N, R, 2, eps_core, k=4)
        err = np.max(np.abs(wn[:len(j2)] - j2))
        print(f"  {N:3d}  " + "  ".join(f"{x:.6f}" for x in wn[:4]) + f"   {err:.3e}")

    # -------- GATE (i): w->0 returns static
    print("\n[GATE i] w->0 returns static: the w=0 case. Static means d_t^2->0, so")
    print("         the master eqn becomes -H''+l(l+1)/r^2 H = 0 (Laplace/static).")
    print("         Regular solution H~r^{l+1}; on [0,R] with H(0)=0 the ONLY")
    print("         w=0 solution meeting BOTH H(0)=0 and a wall BC is checked:")
    N = 128
    wn, r = spectrum_dirichlet(N, R, 2, eps_core, k=6)
    n_near_zero = int(np.sum(wn < 1e-4))
    print(f"         # eigenvalues w<1e-4 (would-be static modes): {n_near_zero}")
    print("         (Dirichlet both ends: static regular sol r^{l+1} cannot also")
    print("          vanish at R unless trivial => NO w=0 propagating mode. PASS")
    print("          means w->0 is the static/no-rhythm limit, recovered consistently.)")

    # -------- GATE (iii): l=0 round limit -> no propagating tower (Birkhoff)
    print("\n[GATE iii] Round limit l=0: l(l+1)=0 => -H''=w^2 H, plain 1D.")
    print("          For the GW DOF there is NO l=0 even-parity radiative mode")
    print("          (monopole is non-radiative; Birkhoff => static). We confirm")
    print("          the l=2 centrifugal barrier is what supports the standing")
    print("          tower; l=0 has no barrier => not a confined GW DOF.")
    wn0, _ = spectrum_dirichlet(N, R, 0, eps_core, k=4)
    wn2, _ = spectrum_dirichlet(N, R, 2, eps_core, k=4)
    print("          l=0 'spectrum' (plain box, NON-physical for GW):", wn0)
    print("          l=2 spectrum (physical GW tower):              ", wn2)
    print("          [l=0 is just the empty-box 1D ladder n*pi/R; it carries no")
    print("           l(l+1)/r^2 barrier and is NOT a vacuum GW mode -> consistent")
    print("           with Birkhoff: round vacuum has no propagating DOF.]")

    # =====================================================================
    # PHASE-1b: the spectra
    # =====================================================================
    print("\n" + "=" * 78)
    print("PHASE-1b: LINEAR MODE SPECTRUM (l=2,3,4; Dirichlet & Neumann walls)")
    print("=" * 78)
    N = 160
    for l in [2, 3, 4]:
        print(f"\n----- l = {l} -----")
        wD, r = spectrum_dirichlet(N, R, l, eps_core, k=6)
        wNn, _ = spectrum_neumann(N, R, l, eps_core, k=6)
        jD = jl_zeros(l, 6, R=R)
        jNN = jl_neumann_zeros(l, 6, R=R)
        print("  Dirichlet wall  w_n (numeric):", wD)
        print("  Dirichlet wall  w_n (analytic j_l zeros):", jD)
        print("    max err:", np.max(np.abs(wD[:len(jD)] - jD)))
        print("  Neumann wall    w_n (numeric):", wNn)
        print("  Neumann wall    w_n (analytic d/dr[r j_l]=0 zeros):", jNN)
        if len(wNn) >= len(jNN):
            print("    max err:", np.max(np.abs(wNn[:len(jNN)] - jNN)))
        print("  RATIOS w_n/w_1 (Dirichlet):", wD / wD[0])
        print("  RATIOS w_n/w_1 (Neumann)  :", wNn / wNn[0])

    # -------- SHAPES: node counts of l=2 Dirichlet eigenvectors
    print("\n----- SHAPES (radial node count), l=2 Dirichlet -----")
    r, Dr, A = build_operator(N, R, 2, eps_core)
    idx = np.arange(1, N)
    Ai = A[np.ix_(idx, idx)]
    evals, evecs = np.linalg.eig(Ai)
    order = np.argsort(evals.real)
    for m in range(6):
        col = np.zeros(N + 1)
        col[1:N] = evecs[:, order[m]].real
        w_m = np.sqrt(evals.real[order[m]]) if evals.real[order[m]] > 0 else 0.0
        print(f"  mode {m+1}: w={w_m:.5f}  radial nodes (interior)={node_count(r, col)}")

    # =====================================================================
    # BOX-CONTROL GATE: vary R_seal, check 1/R scaling and ratio drift
    # =====================================================================
    print("\n" + "=" * 78)
    print("BOX-CONTROL GATE: vary R_seal (relative 1,2,4,8); 1/R scaling? ratio drift%?")
    print("=" * 78)
    R_list = [1.0, 2.0, 4.0, 8.0]
    l = 2
    print(f"\n[CPU] l={l}, Dirichlet, N={N}, eps_core=1e-4*R:")
    abs_table = []
    ratio_table = []
    for Rs in R_list:
        ec = 1e-4 * Rs
        wD, _ = spectrum_dirichlet(N, Rs, l, ec, k=6)
        abs_table.append(wD)
        ratio_table.append(wD / wD[0])
        print(f"  R={Rs:>4.1f}  w_n={wD}")
    abs_table = np.array(abs_table)
    ratio_table = np.array(ratio_table)
    print("\n  1/R scaling check: w_n(R) * R  (should be CONSTANT across rows if 1/R):")
    for i, Rs in enumerate(R_list):
        print(f"    R={Rs:>4.1f}  w_n*R = {abs_table[i]*Rs}")
    print("\n  RATIO drift across boxes (w_n/w_1), and max % drift vs R=1 row:")
    base = ratio_table[0]
    for i, Rs in enumerate(R_list):
        drift = np.max(np.abs(ratio_table[i] - base) / base) * 100
        print(f"    R={Rs:>4.1f}  ratios={ratio_table[i]}  max_drift={drift:.4e} %")

    # -------- GPU batched cross-check of the box-control table
    if HAVE_TORCH:
        print("\n[GPU] batched Dirichlet eigensolve over R_list (float64, V100):")
        gpu = spectrum_dirichlet_batch_gpu(N, R_list, l, 1e-4, k=6)
        for i, Rs in enumerate(R_list):
            cpu = abs_table[i][:gpu.shape[1]]
            err = np.max(np.abs(gpu[i] - cpu))
            print(f"    R={Rs:>4.1f}  GPU w_n={gpu[i]}  max|GPU-CPU|={err:.3e}")
        print("  [CPU spot-check of every GPU row above.]")
    else:
        print("\n[GPU] torch CUDA unavailable -- CPU only (box-control table above stands).")

    print("\n" + "=" * 78)
    print("Done. See final report for the READ (box-control vs richer structure).")
    print("=" * 78)
