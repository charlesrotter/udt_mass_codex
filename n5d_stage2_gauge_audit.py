"""N5d Stage-2 phi/rho SOFT-MODE GAUGE AUDIT (diagnostic/design only; category-A conditioning work).
Is the blind-verified fixed-L phi/rho near-null mode a GAUGE / free-boundary redundancy (=> quotient it, no
physics change) or a true physical flat direction?  And does an ADMISSIBLE category-A pin (areal-radius
normalization / null-orthogonality; NOT fixing L, NOT physics) give a well-conditioned finite-L representative?

Scope: NO physics fork, NO S-JC2/FIX-2/higher-ell/time-live, NO finite-L target/penalty/anchor.  Bounded,
CPU, single process, jacrev + small solves only.  pi_2 static S-Dir tile only; DESIGN/PROVISIONAL/Outcome D.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev
import cell_solver_f2d as C

PRM = (8.0, 1.0, 1.0, 1); Z, XI, KAP, N = PRM
NR, NTH = 12, 8
HIDX = (NR - 2) + 2 + (NR - 2) + 2 + (NR - 2) * NTH + 2 * NTH   # Hseal row index (=120)
CTX = C.make_ctx(NR, NTH, rc=0.5); N5D = dict(sealbc="S-Dir", a2_mirror=0.0)


def split(ur):
    return ur[:NR], ur[NR:2 * NR], ur[2 * NR:2 * NR + NR * NTH].reshape(NR, NTH), ur[2 * NR + NR * NTH:]


def to_full(ur, L):
    phi, rho, uf, a2 = split(ur); return C.pack(phi, rho, uf, L, a2=a2)


def redF(ur, L, drop=True):
    F = C.residual(to_full(ur, L), CTX, PRM, n5d=N5D)
    return F[torch.arange(F.numel()) != HIDX] if drop else F


def Hseal(ur, L):
    return float(C.H_of_r(to_full(ur, L), CTX, PRM, n5d=N5D)[-1])


def reads(ur, L):
    return C.readouts(to_full(ur, L), CTX, PRM, n5d=N5D)


def moments(ur, L):
    Q = C.fields(to_full(ur, L), CTX, PRM, n5d=N5D)
    return dict(Ith=float(Q["Ith"][-1]), Is=float(Q["Is"][-1]), I4th=float(Q["I4th"][-1]),
                shear=float((Q["shear_res"] ** 2).sum()) ** 0.5)


def lm(ur0, rf, maxit=150, budget=45.0):
    import time; t0 = time.time(); u = ur0.clone(); F = rf(u); Phi = float((F * F).sum()); lam = 1e-3; nu = 2.0
    for _ in range(maxit):
        if Phi < 1e-18 or time.time() - t0 > budget:
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


def nullvec(ur, L):
    """State-space right singular vector of the smallest equilibrated singular value of the drop-Hseal Jacobian."""
    J = jacrev(lambda u: redF(u, L, True))(ur).detach()
    cn = torch.linalg.norm(J, dim=0).clamp_min(1e-300); Jc = J * (1 / cn)[None, :]
    _, S, Vh = torch.linalg.svd(Jc, full_matrices=False)
    v = (1 / cn) * Vh[-1]; return v / torch.linalg.norm(v), float(S[-1]), float(S[-2])


def cosine(a, b):
    a = a.flatten(); b = b.flatten()
    na, nb = float(torch.linalg.norm(a)), float(torch.linalg.norm(b))
    return float(torch.dot(a, b)) / (na * nb) if na > 1e-30 and nb > 1e-30 else float('nan')


if __name__ == "__main__":
    phi, rho, uf, a2, _ = C.unpack(C.seed_n5d(CTX, a2_amp=1e-2, amp=0.02), CTX, n5d=N5D)
    ur0 = torch.cat([phi, rho, uf.reshape(-1), a2]); L = 1.0
    print("### N5d Stage-2 phi/rho SOFT-MODE GAUGE AUDIT (L=1.0 rep; pi_2 static S-Dir; Outcome D) ###\n")

    urA, PhiA = lm(ur0, lambda u: redF(u, L, True))
    v, smin, s2 = nullvec(urA, L)
    vphi, vrho, vuf, va2 = split(v)
    tot = float((v ** 2).sum())
    frac = {k: round(float((x ** 2).sum()) / tot, 3) for k, x in [("phi", vphi), ("rho", vrho), ("uf", vuf), ("a2", va2)]}
    print(f"[A] drop-Hseal solve Phi={PhiA:.2e}  Hseal={Hseal(urA,L):+.4f}")
    print(f"[A] near-null mode: s_min={smin:.2e} s_2nd={s2:.2e} ratio={s2/smin:.1e}  block-fractions={frac}")

    # what transformation does v approximate?  candidate generators on (phi,rho):
    phiA, rhoA, ufA, a2A = split(urA)
    Dz = CTX["Dz"]; sc = 2.0 / L
    rhop = sc * (Dz @ rhoA); phip = sc * (Dz @ phiA)
    print("[A] shape correlations of the mode's blocks vs candidate generators (|cos|~1 => that transform):")
    print(f"      v_rho vs rho (global rescale)      : cos={cosine(vrho, rhoA):+.3f}")
    print(f"      v_rho vs rho' (radial reparam-rho) : cos={cosine(vrho, rhop):+.3f}")
    print(f"      v_phi vs 1  (phi depth offset)     : cos={cosine(vphi, torch.ones(NR)):+.3f}")
    print(f"      v_phi vs phi' (radial reparam-phi) : cos={cosine(vphi, phip):+.3f}")
    print(f"      v_phi vs -v_rho/rho*... (rescale-linked): cos(v_phi,v_rho)={cosine(vphi, vrho):+.3f}")

    # [B] invariant table along the mode
    print("\n[B] invariants along the mode  u -> urA + eps*v :")
    print(f"    {'eps':>7} {'q_raw':>11} {'Pi_phi':>11} {'M_readout':>11} {'Hseal':>9} {'rho_s/rho_c':>11} "
          f"{'Ith':>7} {'Is':>7} {'I4th':>7} {'||F_field||':>11}")
    for eps in (-0.4, -0.2, 0.0, 0.2, 0.4):
        ue = urA + eps * v; r = reads(ue, L); m = moments(ue, L)
        pe, re_, _, _ = split(ue)
        Ff = float((redF(ue, L, True) ** 2).sum()) ** 0.5
        print(f"    {eps:>7.2f} {r['q_raw']:>11.4e} {r['Pi_phi']:>11.4e} {r['M_readout']:>11.4e} "
              f"{Hseal(ue,L):>+9.4f} {float(re_[-1]/re_[0]):>11.5f} {m['Ith']:>7.4f} {m['Is']:>7.4f} "
              f"{m['I4th']:>7.4f} {Ff:>11.2e}")

    # [C] gauge-dependence verdict
    r0 = reads(urA, L); rp = reads(urA + 0.3 * v, L)
    dq = abs(rp['q_raw'] - r0['q_raw']); dH = abs(Hseal(urA + 0.3 * v, L) - Hseal(urA, L))
    print(f"\n[C] along the mode (eps=0.3): d|q_raw|={dq:.2e}  d|Hseal|={dH:.2e}  => "
          f"{'Hseal GAUGE-DEPENDENT (moves while q_raw fixed)' if dq<1e-6<dH else 'not clearly separated'}")

    # [D] admissible category-A gauge pins on the FIXED-L system (does the mode get removed? readouts invariant?)
    print("\n[D] category-A gauge pins on the fixed-L (keep-Hseal) system -- conditioning + readout invariance:")
    def cond_of(rf, u):
        J = jacrev(rf)(u).detach(); cn = torch.linalg.norm(J, dim=0).clamp_min(1e-300)
        s = torch.linalg.svdvals(J * (1 / cn)[None, :]); return float(s[0] / s[-1]), float(s[-1])
    # (i) baseline keep-Hseal (no pin)
    c0, sm0 = cond_of(lambda u: redF(u, L, False), urA)
    # (ii) null-orthogonality pin: append v^T (u - urA) = 0
    def rf_orth(u): return torch.cat([redF(u, L, False), (torch.dot(v, u - urA)).reshape(1)])
    c1, sm1 = cond_of(rf_orth, urA)
    urO, PhiO = lm(urA, rf_orth); rO = reads(urO, L)
    # (iii) areal-radius normalization pin: rho(r_c) = rho_ref (does NOT fix L)
    rho_ref = float(rhoA[0])
    def rf_rhopin(u): return torch.cat([redF(u, L, False), (split(u)[1][0] - rho_ref).reshape(1)])
    c2, sm2 = cond_of(rf_rhopin, urA)
    urR, PhiR = lm(urA, rf_rhopin); rR = reads(urR, L)
    print(f"    (i)  no pin           : cond_equil={c0:.2e} s_min={sm0:.2e}")
    print(f"    (ii) null-orthogonal  : cond_equil={c1:.2e} s_min={sm1:.2e}  -> solved Phi={PhiO:.2e} "
          f"Hseal={Hseal(urO,L):+.4f} q_raw={rO['q_raw']:.4e} (dq vs A={abs(rO['q_raw']-r0['q_raw']):.1e})")
    print(f"    (iii)areal-rho(r_c)pin: cond_equil={c2:.2e} s_min={sm2:.2e}  -> solved Phi={PhiR:.2e} "
          f"Hseal={Hseal(urR,L):+.4f} q_raw={rR['q_raw']:.4e} (dq vs A={abs(rR['q_raw']-r0['q_raw']):.1e})")

    # [E] FREE-L closed cell with an admissible pin: can we get a well-conditioned finite-L representative?
    print("\n[E] FREE-L closed cell (133 rows: field+BCs+Hseal+shear) + areal-rho(r_c) pin (does NOT fix L):")
    def full_pin(w):  # w = [ur(132-block without L is 132); but here full unknown = ur(132)+L]
        ur = w[:-1]; Lv = w[-1]
        F = C.residual(to_full(ur, Lv), CTX, PRM, n5d=N5D)
        return torch.cat([F, (split(ur)[1][0] - rho_ref).reshape(1)])   # +1 gauge row (overdetermined by 1)
    w0 = torch.cat([urA, torch.tensor([L])])
    def cond_full(w):
        J = jacrev(full_pin)(w).detach(); cn = torch.linalg.norm(J, dim=0).clamp_min(1e-300)
        s = torch.linalg.svdvals(J * (1 / cn)[None, :]); return float(s[0] / s[-1]), float(s[-1])
    cF0, smF0 = cond_full(w0)
    wF, PhiF = lm(w0, full_pin, maxit=150, budget=45.0)
    urF, LF = wF[:-1], float(wF[-1]); rF = reads(urF, LF)
    print(f"    start cond_equil={cF0:.2e}  -> solved Phi={PhiF:.2e}  L={LF:.5f}  Hseal={Hseal(urF,LF):+.4f}  "
          f"q_raw={rF['q_raw']:.4e}")
    print(f"    L stayed finite (>1e-2)? {LF>1e-2}   (if L still drains -> the L-degeneracy is NOT the gauge mode)")
    print("\n[scope] pi_2 static S-Dir tile only; category-A gauge/conditioning audit; NO physics verdict, NO A/B,")
    print("        NO pin/continuum, NO pi_3. Diagnostic/design only.")
