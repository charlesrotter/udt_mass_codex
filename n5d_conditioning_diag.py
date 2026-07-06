"""n5d_conditioning_diag.py -- CATEGORY-A conditioning diagnosis of the N5d Stage-1 pilot.

NOT a verdict run.  Does NOT change equations/BCs/source/readouts.  It:
  1. reproduces the EXACT non-converged final state of the pilot (same seed, continuation, BCs),
  2. SVDs the Jacobian at (a) the final non-converged state and (b) the nonzero shear seed,
  3. reports the near-zero right singular vector(s): block dominance (phi/rho/uf/a2/L), profile,
  4. tests whether moving along the null vector changes the OBSERVABLES (Hseal, q_raw, Pi_phi,
     M_readout, phi node / turning-point counts) or an unobservable/gauge direction,
  5. tests CATEGORY-A fixes ONLY: column/block rescaling, lbare shear-block preconditioner,
     variable normalization; reports resulting condition numbers.
No physics conclusion is drawn.  Prints a structured report.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import json
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev

import cell_solver_f2d as cs
import n5d_pilot as pilot

PRM = pilot.PRM
Nr, Nth = 16, 8
A2_SEED = pilot.A2_SEED
CONT_AMPS = pilot.CONT_AMPS


def block_slices(ctx):
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    b = {}
    b["phi"] = slice(0, Nr)
    b["rho"] = slice(Nr, 2 * Nr)
    b["uf"] = slice(2 * Nr, 2 * Nr + Nr * Nth)
    b["a2"] = slice(2 * Nr + Nr * Nth, 2 * Nr + Nr * Nth + Nr)
    b["L"] = slice(2 * Nr + Nr * Nth + Nr, 2 * Nr + Nr * Nth + Nr + 1)
    return b


def reproduce_final_state(sealbc, source_rc, source_sh2, maxit=30, budget=100.0):
    """Re-run the exact pilot continuation to reproduce the final (non-converged) u for this BC."""
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)
    u = cs.seed_n5d(ctx, a2_amp=A2_SEED)
    _, _, _, _, L0 = cs.unpack(u, ctx, n5d=True)
    L0 = float(L0)
    u_seed = u.detach().clone()
    import time
    t0 = time.time()
    for amp in CONT_AMPS:
        remaining = budget - (time.time() - t0)
        if remaining <= 1.0:
            break
        Tshear = pilot.build_Tshear(ctx, L0, amp, source_rc, source_sh2)
        n5d = dict(sealbc=sealbc, Tshear=Tshear, a2_mirror=0.0)
        u, hist = cs.newton_lm_solve(u, ctx, PRM, maxit=maxit, tol=pilot.PHI_TOL,
                                     verbose=False, time_budget=remaining, n5d=n5d)
    # final n5d config at the last amplitude
    n5d = dict(sealbc=sealbc, Tshear=pilot.build_Tshear(ctx, L0, CONT_AMPS[-1], source_rc, source_sh2),
               a2_mirror=0.0)
    n5d_seed = dict(sealbc=sealbc, Tshear=pilot.build_Tshear(ctx, L0, CONT_AMPS[0], source_rc, source_sh2),
                    a2_mirror=0.0)
    return ctx, u.detach(), u_seed, n5d, n5d_seed, L0


def jac(u, ctx, n5d):
    return jacrev(lambda uu: cs.residual(uu, ctx, PRM, n5d=n5d))(u).detach()


def block_norms(vec, ctx):
    b = block_slices(ctx)
    v = vec.detach().cpu().numpy()
    tot = np.linalg.norm(v)
    return {k: float(np.linalg.norm(v[s]) / (tot + 1e-300)) for k, s in b.items()}


def svd_report(J, tag):
    U, S, Vh = torch.linalg.svd(J)
    S = S.cpu().numpy()
    print(f"  [{tag}] shape={tuple(J.shape)}  cond={S[0]/S[-1]:.3e}  "
          f"smax={S[0]:.3e}  smin={S[-1]:.3e}")
    print(f"  [{tag}] smallest 5 singular values: {['%.3e' % x for x in S[-5:]]}")
    print(f"  [{tag}] largest 3 singular values : {['%.3e' % x for x in S[:3]]}")
    # numeric-null floor test: smin vs smax*eps
    eps = np.finfo(np.float64).eps
    print(f"  [{tag}] smin / (smax*eps) = {S[-1]/(S[0]*eps):.3e}  "
          f"(<~1 => mode below float64 assembly floor = numerically null)")
    return U, S, Vh


def analyze_nullvec(J, ctx, u, n5d, tag, n_modes=2):
    U, S, Vh = torch.linalg.svd(J)
    b = block_slices(ctx)
    for k in range(n_modes):
        v = Vh[-(k + 1)].detach()   # right singular vector for k-th smallest singular value
        bn = block_norms(v, ctx)
        print(f"\n  [{tag}] near-zero right-singular-vector #{k+1} (sigma={S[-(k+1)]:.3e}):")
        print("    block L2-fraction: " + "  ".join(f"{kk}={bn[kk]:.3f}" for kk in
                                                    ["phi", "rho", "uf", "a2", "L"]))
        # a2 profile: is it near-constant? (constant-Neumann null mode signature)
        a2part = v[b["a2"]].cpu().numpy()
        if np.linalg.norm(a2part) > 1e-12:
            a2n = a2part / np.linalg.norm(a2part)
            const_dir = np.ones_like(a2n) / np.sqrt(len(a2n))
            const_overlap = abs(float(const_dir @ a2n))
            # low-order content: overlap with a linear ramp too
            zeta = ctx["zeta"].cpu().numpy()
            ramp = zeta - zeta.mean(); ramp /= np.linalg.norm(ramp)
            ramp_overlap = abs(float(ramp @ a2n))
            print(f"    a2-subvector: |overlap with CONSTANT|={const_overlap:.3f}  "
                  f"|overlap with LINEAR ramp|={ramp_overlap:.3f}  "
                  f"(const+linear low-order => Neumann/scaling null; high-order => Cheb/oscillatory)")
        # observable sensitivity along this mode
        observable_sensitivity(J, ctx, u, n5d, v, S[-(k + 1)], tag=f"{tag}/mode{k+1}")
    return U, S, Vh


def _observables(u, ctx, n5d):
    with torch.no_grad():
        ro = cs.readouts(u, ctx, PRM, n5d=n5d)
        Hr = cs.H_of_r(u, ctx, PRM).cpu().numpy()
        Q = cs.fields(u, ctx, PRM, n5d=n5d)
        phi = Q["phi"].cpu().numpy()
        sc = 2.0 / float(Q["L"])
        phipp = sc * sc * (ctx["Dz2"] @ Q["phi"])
        rhs = (phipp - Q["phi_ode"]).cpu().numpy()
        a2 = Q["a2"].cpu().numpy()
    return dict(q_raw=ro["q_raw"], Pi_phi=ro["Pi_phi"], M_readout=ro["M_readout"],
                Hseal=float(Hr[-1]), phi_nodes=pilot._sign_changes(phi),
                rhs_turns=pilot._turning_points(rhs), a2_peak=float(np.abs(a2).max()))


def observable_sensitivity(J, ctx, u, n5d, vmode, sigma, tag, eps=1e-4):
    """Move u += eps*vmode (unit vector) and report change in observables vs a RANDOM unit direction."""
    base = _observables(u, ctx, n5d)
    up = (u + eps * vmode).detach()
    obs_mode = _observables(up, ctx, n5d)
    # calibration: a deterministic 'generic' direction (fixed pattern, unit norm) of same eps
    g = torch.cos(3.0 * torch.arange(u.numel(), dtype=torch.float64))
    g = g / torch.linalg.norm(g)
    obs_gen = _observables((u + eps * g).detach(), ctx, n5d)

    def d(a, b):
        return {k: b[k] - a[k] for k in a}
    dm = d(base, obs_mode); dg = d(base, obs_gen)
    print(f"    [{tag}] observable change moving eps={eps} along NULL mode  vs  GENERIC dir:")
    for k in ["q_raw", "Pi_phi", "M_readout", "Hseal", "a2_peak"]:
        print(f"      d{k:10s}: null={dm[k]:+.3e}   generic={dg[k]:+.3e}")
    for k in ["phi_nodes", "rhs_turns"]:
        print(f"      d{k:10s}: null={dm[k]:+d}   generic={dg[k]:+d}")


# =========================================================================================
# CATEGORY-A FIX TESTS
# =========================================================================================
def col_norm_report(J, ctx, tag):
    b = block_slices(ctx)
    cn = torch.linalg.norm(J, dim=0).cpu().numpy()  # column norms
    print(f"\n  [{tag}] per-block column-norm ranges (reveals block-scaling imbalance):")
    for k, s in b.items():
        seg = cn[s]
        print(f"    {k:4s}: min={seg.min():.3e}  max={seg.max():.3e}  median={np.median(seg):.3e}")
    return cn


def diagonal_column_scaling(J, tag):
    """Jacobi (per-column) scaling: J' = J @ diag(1/colnorm). Standard category-A reconditioning."""
    cn = torch.linalg.norm(J, dim=0)
    cn = torch.where(cn > 0, cn, torch.ones_like(cn))
    Js = J / cn[None, :]
    S = torch.linalg.svdvals(Js).cpu().numpy()
    print(f"  [{tag}] after per-column (Jacobi) scaling: cond={S[0]/S[-1]:.3e}  smin={S[-1]:.3e}")
    return S


def two_sided_ruiz(J, tag, iters=20):
    """Ruiz equilibration (two-sided row+col scaling). Category-A."""
    A = J.clone()
    m, n = A.shape
    dr = torch.ones(m, dtype=torch.float64); dc = torch.ones(n, dtype=torch.float64)
    for _ in range(iters):
        rn = torch.linalg.norm(A, dim=1); cn = torch.linalg.norm(A, dim=0)
        rn = torch.where(rn > 0, rn, torch.ones_like(rn))
        cn = torch.where(cn > 0, cn, torch.ones_like(cn))
        A = A / rn.sqrt()[:, None] / cn.sqrt()[None, :]
        dr /= rn.sqrt(); dc /= cn.sqrt()
    S = torch.linalg.svdvals(A).cpu().numpy()
    print(f"  [{tag}] after Ruiz two-sided equilibration: cond={S[0]/S[-1]:.3e}  smin={S[-1]:.3e}")
    return S


def block_a2_rescale_sweep(J, ctx, tag):
    """Scale ONLY the a2-block columns by factor f; sweep f; report best cond."""
    b = block_slices(ctx)["a2"]
    best = (None, np.inf)
    print(f"  [{tag}] a2-block column-scale sweep:")
    for f in [1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6]:
        Js = J.clone(); Js[:, b] = Js[:, b] * f
        S = torch.linalg.svdvals(Js).cpu().numpy()
        cond = S[0] / S[-1]
        print(f"    f={f:.0e}: cond={cond:.3e}  smin={S[-1]:.3e}")
        if cond < best[1]:
            best = (f, cond)
    print(f"    -> best a2-scale f={best[0]:.0e} gives cond={best[1]:.3e}")
    return best


def shear_subblock_analysis(J, ctx, tag):
    """Isolate the pure shear sub-Jacobian d(shear_rows)/d(a2) and diagnose IT directly.
    Row layout of residual (n5d): base rows [ (Nr-2)+2 phi ; (Nr-2)+2 rho ; (Nr-2)*Nth uf ;
    2*Nth fr ; 1 Hseal ] then shear rows [ (Nr-2) shear_res ; 1 core_bc ; 1 seal_bc ].
    The shear rows are the LAST Nr rows; the a2 cols are block 'a2'."""
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    b = block_slices(ctx)
    a2cols = b["a2"]
    shear_rows = slice(J.shape[0] - Nr, J.shape[0])
    Jss = J[shear_rows, a2cols]              # (Nr, Nr) shear-vs-a2 sub-block
    S = torch.linalg.svdvals(Jss).cpu().numpy()
    print(f"\n  [{tag}] SHEAR sub-block d(shear_rows)/d(a2)  shape={tuple(Jss.shape)}:")
    print(f"    cond={S[0]/S[-1]:.3e}  smax={S[0]:.3e}  smin={S[-1]:.3e}")
    print(f"    smallest 4 sv: {['%.3e' % x for x in S[-4:]]}")
    # null vector of the shear sub-block
    U2, S2, V2h = torch.linalg.svd(Jss)
    vnull = V2h[-1].cpu().numpy(); vnull /= np.linalg.norm(vnull)
    const_dir = np.ones_like(vnull) / np.sqrt(len(vnull))
    print(f"    shear-block null vec: |overlap with CONSTANT a2|={abs(const_dir@vnull):.3f}")
    # cross-coupling: how much does a2 feed back into phi/rho rows?
    phi_rows = slice(0, Nr - 2)
    rho_rows = slice(Nr, 2 * Nr - 2)
    cpl_phi = float(torch.linalg.norm(J[phi_rows, a2cols]))
    cpl_rho = float(torch.linalg.norm(J[rho_rows, a2cols]))
    print(f"    a2 -> phi-row coupling ||.||={cpl_phi:.3e}   a2 -> rho-row coupling ||.||={cpl_rho:.3e}")
    print(f"    (near-zero coupling => a2 block nearly DECOUPLED from phi/rho => the quadratic a2 source)")
    return S


def lbare_precond_test(ctx, u, n5d, tag):
    """Category-A: use the certified L_bare inverse as a shear-block preconditioner / cross-check.
    Report the L_bare interior operator eigen-index (roots {1,2} expected) on the physical nodes."""
    with torch.no_grad():
        Q = cs.fields(u, ctx, PRM, n5d=n5d)
        L = float(Q["L"])
    zeta = ctx["zeta"].cpu().numpy()
    r_phys = ctx["rc"] + 0.5 * L * (zeta + 1.0)
    try:
        ev, ndec = cs.n5d_shear.lbare_tt_eigindex(r_phys)
        print(f"\n  [{tag}] L_bare TT eigen-index on physical nodes r in [{r_phys[0]:.3f},{r_phys[-1]:.3f}]:")
        print(f"    interior eigenvalues (sorted, real): {['%.3e' % x for x in ev[:6]]} ...")
        print(f"    n_decaying (eigenvalue<0) = {ndec}  (round expects roots ~{{1,2}} both growing => 0 decaying)")
    except Exception as e:
        print(f"  [{tag}] lbare_tt_eigindex failed: {e}")


# =========================================================================================
# MAIN
# =========================================================================================
def run_bc(sealbc, source_rc, source_sh2):
    print("\n" + "=" * 90)
    print(f"SEAL BC = {sealbc}")
    print("=" * 90)
    ctx, u_final, u_seed, n5d, n5d_seed, L0 = reproduce_final_state(sealbc, source_rc, source_sh2)

    # sanity: reproduce the banked diagnostics
    diag = pilot.final_diagnostics(u_final, ctx, n5d)
    print(f"[reproduce] jac_cond={diag['jac_cond']:.3e}  a2_peak={diag['a2_peak_abs']:.3e}  "
          f"H_seal={diag['H_seal']:+.3e}  q_raw={diag['q_raw']:.3e}  seed_L0={L0:.4f}")

    Jf = jac(u_final, ctx, n5d)
    Js = jac(u_seed, ctx, n5d_seed)

    print("\n--- SVD @ FINAL non-converged state ---")
    svd_report(Jf, "final")
    print("\n--- SVD @ nonzero shear SEED (a2=1e-3) ---")
    svd_report(Js, "seed")

    print("\n--- near-zero right-singular-vector analysis @ FINAL ---")
    analyze_nullvec(Jf, ctx, u_final, n5d, "final", n_modes=2)

    print("\n--- block column-norm imbalance @ FINAL ---")
    col_norm_report(Jf, ctx, "final")

    print("\n--- shear sub-block direct diagnosis @ FINAL ---")
    shear_subblock_analysis(Jf, ctx, "final")

    print("\n--- CATEGORY-A FIX TESTS @ FINAL ---")
    diagonal_column_scaling(Jf, "final/jacobi")
    two_sided_ruiz(Jf, "final/ruiz")
    block_a2_rescale_sweep(Jf, ctx, "final")
    lbare_precond_test(ctx, u_final, n5d, "final")
    return dict(sealbc=sealbc, jac_cond=diag['jac_cond'])


def main():
    st, source_rc, source_sh2 = pilot.load_frozen_source()
    if st.get("blocker"):
        print("BLOCKER loading frozen source:", st["blocker"]); return
    print("frozen source OK:", st.get("hopfion", {}).get("is_h3_hopfion"),
          "Q=", st.get("hopfion", {}).get("Q"))
    for sealbc in ("S-Dir", "S-JC2"):
        run_bc(sealbc, source_rc, source_sh2)


if __name__ == "__main__":
    main()
