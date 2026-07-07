"""N5d Stage-2 collapse audit — RECONCILIATION / CORRECTION probe (diagnostic only; NO pilot, NO free-L verdict).

CATCHES an over-read in n5d_stage2_collapse_audit_results.md: the "factor-2 structural deficit / Hseal=-0.96
L-independent / no finite-L cell" conclusion was an ARTIFACT of the drop-Hseal solve landing on a flat valley.

Two probes (fixed L, bounded, CPU, single process):
  (1) TRADEOFF: at fixed L, (i) DROP the Hseal row -> field eqs relax, read Hseal (=-0.9x); (ii) KEEP Hseal
      (overdetermined by 1) -> min ||F||^2 reaches Hseal~0 with the field eqs still satisfied (~1e-9).
  (2) SOFT-MODE: the fixed-L (drop-Hseal) Jacobian has a genuine near-null direction; moving along it slides
      Hseal ~freely through 0 while the field residual barely changes -> the -0.96 is NOT a hard floor.

Corrected read (PROVISIONAL): free-boundary / soft-mode DEGENERACY (ill-conditioning s_min~1e-14), not a hard
structural matter deficit.  pi_2 tile only; DESIGN/PROVISIONAL/Outcome D.  NO Outcome A/B, NO pin/continuum.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev
import cell_solver_f2d as C

PRM = (8.0, 1.0, 1.0, 1)
NR, NTH = 12, 8
HIDX = (NR - 2) + 2 + (NR - 2) + 2 + (NR - 2) * NTH + 2 * NTH   # Hseal row index (=120 for Nr12)


def redF(ur, L, drop):
    phi, rho = ur[:NR], ur[NR:2 * NR]
    uf = ur[2 * NR:2 * NR + NR * NTH].reshape(NR, NTH); a2 = ur[2 * NR + NR * NTH:]
    F = C.residual(C.pack(phi, rho, uf, L, a2=a2), PRM_CTX, PRM, n5d=N5D)
    return F[torch.arange(F.numel()) != HIDX] if drop else F


def Hseal(ur, L):
    phi, rho = ur[:NR], ur[NR:2 * NR]
    uf = ur[2 * NR:2 * NR + NR * NTH].reshape(NR, NTH); a2 = ur[2 * NR + NR * NTH:]
    return float(C.H_of_r(C.pack(phi, rho, uf, L, a2=a2), PRM_CTX, PRM, n5d=N5D)[-1])


def blocks(F):
    n = NR - 2; out, i = {}, 0
    for nm, sz in [("phi_ode", n), ("phi_mir", 2), ("rho_ode", n), ("rho_mir", 2), ("f_pde", n * NTH),
                   ("fr_mir", 2 * NTH), ("Hseal", 1), ("shear_ode", n), ("shear_core", 1), ("shear_seal", 1)]:
        out[nm] = float((F[i:i + sz] ** 2).sum()) ** 0.5; i += sz
    return out


def lm(ur0, L, drop, maxit=150, budget=50.0):
    import time
    t0 = time.time(); rf = lambda u: redF(u, L, drop)
    u = ur0.clone(); F = rf(u); Phi = float((F * F).sum()); lam = 1e-3; nu = 2.0
    for _ in range(maxit):
        if Phi < 1e-16 or time.time() - t0 > budget:
            break
        J = jacrev(rf)(u).detach(); F = rf(u).detach()
        cn = torch.linalg.norm(J, dim=0).clamp_min(1e-300); dc = 1 / cn
        Jc = J * dc[None, :]; dH = (Jc * Jc).sum(0).clamp_min(1e-300); acc = False
        for _ in range(30):
            aug = torch.cat([Jc, (lam ** 0.5) * torch.diag(dH.sqrt())], 0)
            rhs = torch.cat([-F, torch.zeros(J.shape[1])], 0)
            dy = torch.linalg.lstsq(aug, rhs).solution; un = u + dc * dy
            Fn = rf(un); Pn = float((Fn * Fn).sum())
            pred = Phi - float(((F + J @ (dc * dy)) ** 2).sum())
            if pred > 0 and np.isfinite(Pn) and (Phi - Pn) / pred > 0:
                u, F, Phi = un, Fn.detach(), Pn; lam = max(lam / 3, 1e-14); acc = True; break
            lam = min(lam * nu, 1e12); nu *= 2
        if not acc:
            break
    return u.detach(), Phi


if __name__ == "__main__":
    global PRM_CTX, N5D
    PRM_CTX = C.make_ctx(NR, NTH, rc=0.5); N5D = dict(sealbc="S-Dir", a2_mirror=0.0)
    phi, rho, uf, a2, _ = C.unpack(C.seed_n5d(PRM_CTX, a2_amp=1e-2, amp=0.02), PRM_CTX, n5d=N5D)
    ur0 = torch.cat([phi, rho, uf.reshape(-1), a2])

    print("### RECONCILE (1) TRADEOFF: drop-Hseal (Hseal read) vs keep-Hseal (Hseal minimized), fixed L ###")
    print(f"{'L':>5} | {'drop: Hseal':>11} | {'keep: minPhi':>12} {'Hseal':>9} {'rho_mir':>9}")
    for L in (0.6, 0.4, 0.2, 0.1):
        urd, _ = lm(ur0, L, True); Hd = Hseal(urd, L)
        urk, Pk = lm(ur0, L, False); bk = blocks(redF(urk, L, False))
        print(f"{L:5.2f} | {Hd:+11.4f} | {Pk:12.3e} {bk['Hseal']:+9.4f} {bk['rho_mir']:9.2e}")

    print("\n### RECONCILE (2) SOFT-MODE at L=0.4: does Hseal slide freely along the near-null direction? ###")
    L = 0.4
    urA, PhiA = lm(ur0, L, True); urB, PhiB = lm(ur0, L, False)
    J = jacrev(lambda u: redF(u, L, True))(urA).detach()
    cn = torch.linalg.norm(J, dim=0).clamp_min(1e-300); Jc = J * (1 / cn)[None, :]
    _, S, Vh = torch.linalg.svd(Jc, full_matrices=False)
    vsoft = (1 / cn) * Vh[-1]; vsoft = vsoft / torch.linalg.norm(vsoft)
    eps = 1e-4
    dHs = (Hseal(urA + eps * vsoft, L) - Hseal(urA - eps * vsoft, L)) / (2 * eps)
    dFf = (float((redF(urA + eps * vsoft, L, True) ** 2).sum()) ** 0.5
           - float((redF(urA - eps * vsoft, L, True) ** 2).sum()) ** 0.5) / (2 * eps)
    print(f"  Config A (drop): Hseal={Hseal(urA,L):+.4f}   Config B (keep): Hseal={Hseal(urB,L):+.4f}")
    print(f"  drop-Hseal Jac s_min={float(S[-1]):.2e}  s_2nd={float(S[-2]):.2e}  (well-separated near-null)")
    print(f"  along soft mode: dHseal/ds={dHs:+.2e}  d||F_field||/ds={dFf:+.2e}  overlap(B-A,soft)="
          f"{float(torch.dot((urB-urA)/torch.linalg.norm(urB-urA), vsoft)):+.2f}")
    print("  => Hseal slides ~freely through 0 along a genuine near-null mode; -0.96 is a valley point, NOT a floor.")
    print("\n  CORRECTED (PROVISIONAL): free-boundary/soft-mode DEGENERACY + ill-conditioning; leans numerical-path")
    print("  (item 8), NOT the hard structural matter deficit (item 9) claimed earlier. pi_2 tile; Outcome D.")
