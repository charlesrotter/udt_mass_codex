"""N5d Stage-2 STATIC S-Dir COLLAPSE MECHANISM AUDIT (diagnostic only; NO pilot, NO free-L solve).
Determine WHY the static S-Dir co-relaxed pi_2 tile has no finite-L closed cell (L->0 collapse).
Probes: (A) empirical small-L scaling of each residual block; (B) FIXED-L relaxation -> Hseal(L) curve
(the decisive test: does Hseal cross 0 at finite L?); (C) mirror-BC residual, row budget, near-null vs L.
Bounded / anti-hang: Nr<=12, Nth=8, CPU, single process, hard caps, forward evals + small jacrev only.
NO finite-L target/penalty/anchor.  Status DESIGN/PROVISIONAL/Outcome D; pi_2 tile only.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev
import cell_solver_f2d as C

PRM = (8.0, 1.0, 1.0, 1)
Z, XI, KAP, N = PRM
NR, NTH = 12, 8
HSEAL_IDX = (NR - 2) + 2 + (NR - 2) + 2 + (NR - 2) * NTH + 2 * NTH   # index of the Hseal row (=120 for Nr12)


def blocks_of(F, Nr=NR, Nth=NTH):
    n = Nr - 2
    out, i = {}, 0
    for name, sz in [("phi_ode", n), ("phi_mir", 2), ("rho_ode", n), ("rho_mir", 2), ("f_pde", n * Nth),
                     ("fr_mir", 2 * Nth), ("Hseal", 1), ("shear_ode", n), ("shear_core", 1), ("shear_seal", 1)]:
        out[name] = float((F[i:i + sz] ** 2).sum()) ** 0.5
        i += sz
    return out


# ---------------- (A) EMPIRICAL SMALL-L SCALING: hold the ZETA-profile fixed, vary L, read block norms ----
def scaling_probe():
    print("\n===== (A) SMALL-L SCALING of each residual block (FIXED zeta-profile = seed; only L varies) =====")
    print("     expectation from d/dr=(2/L)Dz:  kinetic/2nd-deriv rows ~ 1/L^2 ;  angular-tension pieces ~ O(1)")
    ctx = C.make_ctx(NR, NTH, rc=0.5)
    n5d = dict(sealbc="S-Dir", a2_mirror=0.0)
    phi, rho, uf, a2, _ = C.unpack(C.seed_n5d(ctx, a2_amp=1e-2, amp=0.02), ctx, n5d=n5d)
    Ls = [1.0, 0.5, 0.25, 0.125]
    hist = {}
    for L in Ls:
        F = C.residual(C.pack(phi, rho, uf, L, a2=a2), ctx, PRM, n5d=n5d)
        bl = blocks_of(F); hist[L] = bl
    names = list(next(iter(hist.values())).keys())
    print(f"     {'block':11s} " + "".join(f"L={L:<7.3f}" for L in Ls) + "  ~scaling(norm ratio L:1->1/8)")
    for nm in names:
        vals = [hist[L][nm] for L in Ls]
        # ratio between L=1 and L=1/8 ; 1/L^2 would give factor 64, 1/L factor 8, O(1) factor 1
        r = vals[-1] / vals[0] if vals[0] > 1e-30 else float('nan')
        approx = "~1/L^2" if r > 30 else ("~1/L" if r > 4 else "~O(1)")
        print(f"     {nm:11s} " + "".join(f"{v:.3e} " for v in vals) + f"  ratio={r:8.1f}  {approx}")


# ---------------- FIXED-L reduced system: drop the Hseal row + the L unknown, relax fields at fixed L ------
def reduced_residual(ur, ctx, Lval, n5d):
    Nr, Nth = ctx["Nr"], ctx["Nth"]
    phi = ur[:Nr]; rho = ur[Nr:2 * Nr]
    uf = ur[2 * Nr:2 * Nr + Nr * Nth].reshape(Nr, Nth)
    a2 = ur[2 * Nr + Nr * Nth:2 * Nr + Nr * Nth + Nr]
    u_full = C.pack(phi, rho, uf, Lval, a2=a2)
    F = C.residual(u_full, ctx, PRM, n5d=n5d)
    keep = torch.arange(F.numel()) != HSEAL_IDX
    return F[keep]


def lm_reduced(ur0, ctx, Lval, n5d, maxit=60, lam0=1e-3, tol=1e-14, budget=40.0):
    """Bounded column-equilibrated damped-lstsq LM on the FIXED-L reduced system (mimics FIX-1)."""
    import time
    t0 = time.time()
    rf = lambda u: reduced_residual(u, ctx, Lval, n5d)
    u = ur0.clone(); F = rf(u); Phi = float((F * F).sum()); lam = lam0; nu = 2.0
    for it in range(maxit):
        if Phi < tol or (time.time() - t0) > budget:
            break
        J = jacrev(rf)(u).detach(); F = rf(u).detach()
        cn = torch.linalg.norm(J, dim=0).clamp_min(1e-300); dc = 1.0 / cn
        Jc = J * dc[None, :]; dHc = (Jc * Jc).sum(0).clamp_min(1e-300)
        acc = False
        for _ in range(30):
            aug = torch.cat([Jc, (lam ** 0.5) * torch.diag(dHc.sqrt())], 0)
            rhs = torch.cat([-F, torch.zeros(J.shape[1])], 0)
            dy = torch.linalg.lstsq(aug, rhs).solution
            un = u + dc * dy
            Fn = rf(un); Pn = float((Fn * Fn).sum())
            pred = Phi - float(((F + J @ (dc * dy)) ** 2).sum())
            if pred > 0 and np.isfinite(Pn) and (Phi - Pn) / pred > 0:
                u, F, Phi = un, Fn.detach(), Pn; lam = max(lam / 3, 1e-14); nu = 2.0; acc = True; break
            lam = min(lam * nu, 1e12); nu *= 2.0
        if not acc:
            break
    return u.detach(), Phi


# ---------------- (B/C) FIXED-L Hseal(L) curve + mirror-BC + row-budget + near-null vs L ------------------
def fixedL_scan():
    print("\n===== (B/C) FIXED-L relaxation -> Hseal(L), mirror-BC, row-budget, near-null (L held, NOT freed) =====")
    ctx = C.make_ctx(NR, NTH, rc=0.5); n5d = dict(sealbc="S-Dir", a2_mirror=0.0)
    base = C.seed_n5d(ctx, a2_amp=1e-2, amp=0.02)
    phi, rho, uf, a2, _ = C.unpack(base, ctx, n5d=n5d)
    ur0 = torch.cat([phi, rho, uf.reshape(-1), a2])
    Ls = [2.0, 1.0, 0.6, 0.4, 0.25, 0.15, 0.1, 0.06, 0.03, 0.015]
    print(f"     {'L':>6s} {'Phi_fixedL':>11s} {'Hseal(L)':>11s} {'fr_mir':>9s} {'rho_mir':>9s} "
          f"{'f_pde':>9s} {'shear':>9s} {'nullblk':>8s} {'smin_eq':>9s}")
    rows = []
    ur = ur0.clone()
    for L in Ls:
        ur, Phi = lm_reduced(ur, ctx, L, n5d, maxit=60, budget=40.0)   # warm-start from previous L
        phi_, rho_, uf_, a2_ = ur[:NR], ur[NR:2 * NR], ur[2 * NR:2 * NR + NR * NTH].reshape(NR, NTH), ur[2 * NR + NR * NTH:]
        u_full = C.pack(phi_, rho_, uf_, L, a2=a2_)
        F = C.residual(u_full, ctx, PRM, n5d=n5d); bl = blocks_of(F)
        Hs = float(C.H_of_r(u_full, ctx, PRM, n5d=n5d)[-1])
        J = jacrev(lambda uu: reduced_residual(uu, ctx, L, n5d))(ur).detach()
        cn = torch.linalg.norm(J, dim=0).clamp_min(1e-300); Jc = J * (1.0 / cn)[None, :]
        svc = torch.linalg.svdvals(Jc); smin_eq = float(svc[-1])
        _, _, Vh = torch.linalg.svd(Jc, full_matrices=False); v = Vh[-1]
        idx = dict(phi=(0, NR), rho=(NR, 2 * NR), uf=(2 * NR, 2 * NR + NR * NTH), a2=(2 * NR + NR * NTH, ur.numel()))
        bm = {k: float((v[a:b] ** 2).sum()) for k, (a, b) in idx.items()}; nullblk = max(bm, key=bm.get)
        print(f"     {L:6.3f} {Phi:11.3e} {Hs:+11.3e} {bl['fr_mir']:9.2e} {bl['rho_mir']:9.2e} "
              f"{bl['f_pde']:9.2e} {bl['shear_ode']:9.2e} {nullblk:>8s} {smin_eq:9.2e}")
        rows.append((L, Phi, Hs, bl))
    # Hseal sign-change check
    Hs_vals = [r[2] for r in rows]
    signs = [np.sign(h) for h in Hs_vals]
    crossed = any(signs[i] != signs[i + 1] for i in range(len(signs) - 1))
    print(f"\n     Hseal(L) sign sequence: {[f'{h:+.2e}' for h in Hs_vals]}")
    print(f"     ==> Hseal(L) crosses zero at some finite L?  {crossed}")
    if not crossed:
        print(f"     ==> Hseal stays {'NEGATIVE' if Hs_vals[0] < 0 else 'POSITIVE'} for all probed finite L "
              f"(min|Hseal|={min(abs(h) for h in Hs_vals):.2e}); the closure never opens -> STRUCTURAL.")
    return rows


def Hseal_decompose(L=0.4):
    """Break H(r_s) into its terms at the FULLY-RELAXED fixed-L solution -> WHY is Hseal stuck negative?"""
    print(f"\n===== (D) H(r_s) TERM DECOMPOSITION at the relaxed fixed-L solution (L={L}) =====")
    ctx = C.make_ctx(NR, NTH, rc=0.5); n5d = dict(sealbc="S-Dir", a2_mirror=0.0)
    phi, rho, uf, a2, _ = C.unpack(C.seed_n5d(ctx, a2_amp=1e-2, amp=0.02), ctx, n5d=n5d)
    ur0 = torch.cat([phi, rho, uf.reshape(-1), a2])
    ur, Phi = lm_reduced(ur0, ctx, L, n5d, maxit=120, budget=60.0)
    phi_, rho_, uf_, a2_ = ur[:NR], ur[NR:2 * NR], ur[2 * NR:2 * NR + NR * NTH].reshape(NR, NTH), ur[2 * NR + NR * NTH:]
    u = C.pack(phi_, rho_, uf_, L, a2=a2_)
    Q = C.fields(u, ctx, PRM, n5d=n5d)
    rs = -1
    phip, rhop, e2m = Q["phip"][rs], Q["rhop"][rs], Q["e2m"][rs]
    rho_s = Q["rho"][rs]; a2p = Q["a2p"][rs]
    Ir, I4th, Ith, Is, I4r = Q["Ir"][rs], Q["I4th"][rs], Q["Ith_es"][rs], Q["Is_es"][rs], Q["I4r_es"][rs]
    terms = {
        "(Z/2)rho^2 phi'^2 [kin phi]": float((Z / 2) * rho_s ** 2 * phip ** 2),
        "-2 e^{-2phi} rho'^2 [kin rho]": float(-2 * e2m * rhop ** 2),
        "-2 [boundary const]": -2.0,
        "+(1/10)e^{-2phi}rho^2 a2'^2 [shear kin]": float(C.SHEAR_KIN_COEFF * e2m * rho_s ** 2 * a2p ** 2),
        "-(xi/2)rho^2 I_r [matter kin]": float(-(XI / 2) * rho_s ** 2 * Ir),
        "+(xi/2)(Ith+N^2 Is) [ANG pot]": float((XI / 2) * (Ith + N ** 2 * Is)),
        "-(kap N^2/2) I4r [matter kin]": float(-(KAP * N ** 2 / 2) * I4r),
        "+(kap N^2/2) I4th/rho^2 [ANG pot]": float((KAP * N ** 2 / 2) * I4th / rho_s ** 2),
    }
    print(f"     fixed-L relax Phi={Phi:.2e}  mirror slopes phi'(rs)={float(phip):.2e} rho'(rs)={float(rhop):.2e} a2'(rs)={float(a2p):.2e}")
    tot = 0.0
    for k, v in terms.items():
        tot += v; print(f"     {k:42s} = {v:+.5f}")
    print(f"     {'H(r_s) SUM':42s} = {tot:+.5f}")
    ang = terms["+(xi/2)(Ith+N^2 Is) [ANG pot]"] + terms["+(kap N^2/2) I4th/rho^2 [ANG pot]"]
    print(f"     ==> angular matter POTENTIAL = {ang:+.4f}  vs the boundary constant -2  "
          f"=> deficit {ang-2.0:+.4f} (needs +2 to close; matter supplies only {ang:+.3f}).")


def coldstart_check():
    """Confirm Hseal(L)=const is NOT a warm-start artifact: solve 2 L values from the COLD seed."""
    print("\n===== (E) COLD-START robustness (each L relaxed from the SEED, no warm-start) =====")
    ctx = C.make_ctx(NR, NTH, rc=0.5); n5d = dict(sealbc="S-Dir", a2_mirror=0.0)
    for L in (1.0, 0.1):
        phi, rho, uf, a2, _ = C.unpack(C.seed_n5d(ctx, a2_amp=1e-2, amp=0.02), ctx, n5d=n5d)
        ur0 = torch.cat([phi, rho, uf.reshape(-1), a2])
        ur, Phi = lm_reduced(ur0, ctx, L, n5d, maxit=120, budget=60.0)
        u = C.pack(ur[:NR], ur[NR:2 * NR], ur[2 * NR:2 * NR + NR * NTH].reshape(NR, NTH), L, a2=ur[2 * NR + NR * NTH:])
        Hs = float(C.H_of_r(u, ctx, PRM, n5d=n5d)[-1])
        print(f"     L={L:5.2f} cold-start: Phi={Phi:.2e}  Hseal={Hs:+.4f}")


if __name__ == "__main__":
    import time
    t0 = time.time()
    print("### N5d Stage-2 STATIC S-Dir COLLAPSE MECHANISM AUDIT (diagnostic only; pi_2 tile; Outcome D) ###")
    scaling_probe()
    rows = fixedL_scan()
    Hseal_decompose(0.4)
    coldstart_check()
    print(f"\nwall={time.time()-t0:.1f}s  (forward evals + bounded fixed-L relaxations; NO free-L solve, NO pilot)")
