"""N5d Stage-2 Class-B SEAL DIAGNOSTIC (bounded; category-A/formulation; NO production pilot, NO verdict).
Class-B odd-fold seal (canon C-2026-07-04-1): outer phi row swapped phi'(r_s)=0 -> DIRICHLET phi(r_s)=0, phi' free
=> q_raw = Z rho_s^2 phi'(r_s) is a live OUTPUT.  Ask: is the Class-B static isolated tile well-posed? what readouts
go live? does the phi-offset gauge vanish?  Does NOT select absolute L.  pi_2 static S-Dir; DESIGN/PROVISIONAL/Outcome D.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev
import cell_solver_f2d as C

PRM = (8.0, 1.0, 1.0, 1); NR, NTH = 12, 8
CTX = C.make_ctx(NR, NTH, rc=0.5)
HIDX = (NR - 2) + 2 + (NR - 2) + 2 + (NR - 2) * NTH + 2 * NTH   # Hseal row index (=120)


def split(ur):
    return ur[:NR], ur[NR:2 * NR], ur[2 * NR:2 * NR + NR * NTH].reshape(NR, NTH), ur[2 * NR + NR * NTH:]


def tofull(ur, L):
    p, r, u, a = split(ur); return C.pack(p, r, u, L, a2=a)


def n5d_of(cls):
    return dict(sealbc="S-Dir", a2_mirror=0.0, seal_phi=cls)


def keepF(ur, L, cls):
    return C.residual(tofull(ur, L), CTX, PRM, n5d=n5d_of(cls))


def dropF(ur, L, cls):
    F = keepF(ur, L, cls); return F[torch.arange(F.numel()) != HIDX]


def blocks(F):
    n = NR - 2; out, i = {}, 0
    for nm, sz in [("phi_ode", n), ("phi_bc", 2), ("rho_ode", n), ("rho_mir", 2), ("f_pde", n * NTH),
                   ("fr_mir", 2 * NTH), ("Hseal", 1), ("shear_ode", n), ("shear_core", 1), ("shear_seal", 1)]:
        out[nm] = float((F[i:i + sz] ** 2).sum()) ** 0.5; i += sz
    return out


def lm(u0, rf, maxit=200, budget=45.0):
    import time; t0 = time.time(); u = u0.clone(); F = rf(u); Phi = float((F * F).sum()); lam = 1e-3; nu = 2.0
    for _ in range(maxit):
        if Phi < 1e-20 or time.time() - t0 > budget:
            break
        J = jacrev(rf)(u).detach(); F = rf(u).detach()
        cn = torch.linalg.norm(J, dim=0).clamp_min(1e-300); dc = 1 / cn
        Jc = J * dc[None, :]; dH = (Jc * Jc).sum(0).clamp_min(1e-300); acc = False
        for _ in range(30):
            aug = torch.cat([Jc, (lam ** 0.5) * torch.diag(dH.sqrt())], 0); rhs = torch.cat([-F, torch.zeros(J.shape[1])], 0)
            dy = torch.linalg.lstsq(aug, rhs).solution; un = u + dc * dy; Fn = rf(un); Pn = float((Fn * Fn).sum())
            pred = Phi - float(((F + J @ (dc * dy)) ** 2).sum())
            if pred > 0 and np.isfinite(Pn) and (Phi - Pn) / pred > 0:
                u, F, Phi = un, Fn.detach(), Pn; lam = max(lam / 3, 1e-14); acc = True; break
            lam = min(lam * nu, 1e12); nu *= 2
        if not acc:
            break
    return u.detach(), Phi


def condnull(rf, u):
    J = jacrev(rf)(u).detach(); cn = torch.linalg.norm(J, dim=0).clamp_min(1e-300); Jc = J * (1 / cn)[None, :]
    _, S, Vh = torch.linalg.svd(Jc, full_matrices=False); v = (1 / cn) * Vh[-1]; v = v / torch.linalg.norm(v)
    idx = dict(phi=(0, NR), rho=(NR, 2 * NR), uf=(2 * NR, 2 * NR + NR * NTH), a2=(2 * NR + NR * NTH, u.numel()))
    bm = {k: round(float((v[a:b] ** 2).sum()), 3) for k, (a, b) in idx.items()}
    return float(S[0] / S[-1]), float(S[-1]), float(S[-2]), bm


if __name__ == "__main__":
    p, r, uf, a2, _ = C.unpack(C.seed_n5d(CTX, a2_amp=1e-2, amp=0.02), CTX, n5d=n5d_of("A"))
    ur0 = torch.cat([p, r, uf.reshape(-1), a2])
    print("### N5d Stage-2 Class-B SEAL DIAGNOSTIC (pi_2 static S-Dir; Outcome D; no L selection) ###\n")

    # square/finite check
    F = keepF(ur0, 1.0, "B"); u_full = tofull(ur0, 1.0)
    print(f"[square] len(u_free-L)={u_full.numel()} len(F_classB)={F.numel()} (free-L square={u_full.numel()==F.numel()}) "
          f"finite={bool(torch.isfinite(F).all())}")

    # DOF / near-null: does Class B remove the phi-offset gauge? (drop-Hseal Jacobian near-null composition)
    print("\n[DOF] drop-Hseal near-null (gauge) mode composition, Class A vs Class B (at the seed):")
    for cls in ("A", "B"):
        cond, smin, s2, bm = condnull(lambda u: dropF(u, 1.0, cls), ur0)
        print(f"      Class {cls}: cond_eq={cond:.2e} s_min={smin:.2e} s_2nd={s2:.2e}  near-null={bm}")

    # fixed-L Class-B solves (keep-Hseal) across L; report the live readouts
    print("\n[fixL] Class-B keep-Hseal solves at several fixed L (NO L selection attempted):")
    print(f"      {'L':>5} {'Phi':>10} {'Hseal':>10} {'phip(rs)':>11} {'q_raw':>11} {'M=-q':>11} {'2M/rho_s':>9} {'cond_eq':>9}")
    rows_out = []
    for L in (2.0, 1.0, 0.5, 0.25):
        urB, Phi = lm(ur0, lambda u: keepF(u, L, "B"))
        ro = C.readouts(tofull(urB, L), CTX, PRM, n5d=n5d_of("B"))
        Q = C.fields(tofull(urB, L), CTX, PRM, n5d=n5d_of("B"))
        phip_s = float(Q["phip"][-1]); rho_s = float(Q["rho"][-1]); Hs = float(C.H_of_r(tofull(urB, L), CTX, PRM, n5d=n5d_of("B"))[-1])
        comp = 2.0 * ro["M_readout"] / rho_s
        cond, smin, s2, bm = condnull(lambda u: keepF(u, L, "B"), urB)
        bl = blocks(keepF(urB, L, "B"))
        print(f"      {L:5.2f} {Phi:10.2e} {Hs:+10.3e} {phip_s:+11.3e} {ro['q_raw']:+11.3e} {ro['M_readout']:+11.3e} "
              f"{comp:+9.3e} {cond:9.2e}")
        rows_out.append((L, Phi, ro['q_raw'], phip_s, bl, bm))
    # is q_raw genuine (>> residual floor)?
    L0, Phi0, q0, pp0, bl0, bm0 = rows_out[1]
    print(f"\n[q?]  at L=1: q_raw={q0:+.3e}  vs sqrt(Phi)={Phi0**0.5:.1e} (residual floor)  => "
          f"{'GENUINE nonzero' if abs(q0)>10*Phi0**0.5 else 'AMBIGUOUS/near-floor'}")
    print(f"[q?]  Class-A comparison at L=1 (should be q_raw~0):")
    urA, PhiA = lm(ur0, lambda u: keepF(u, 1.0, "A"))
    roA = C.readouts(tofull(urA, 1.0), CTX, PRM, n5d=n5d_of("A"))
    print(f"      Class A: q_raw={roA['q_raw']:+.3e}  M_readout={roA['M_readout']:+.3e}  (Class-A mirror => ~0)")
    print(f"[budget@L=1,ClassB] {{k: round(v,3) for row}}: " + str({k: round(v, 4) for k, v in bl0.items()}))

    # 1  rho-pin only: does Class B need only rho-normalization now (phi-offset removed by Dirichlet)?
    rr = float(split(urA)[1][0])
    def keepF_B_rhopin(u): return torch.cat([keepF(u, 1.0, "B"), (split(u)[1][0] - rr).reshape(1)])
    cond1, smin1, s21, bm1 = condnull(keepF_B_rhopin, ur0)
    print(f"\n[pin] Class-B + ONLY rho(r_c) pin: cond_eq={cond1:.2e} s_min={smin1:.2e} near-null={bm1} "
          f"(if cond good & no phi in near-null => phi-offset gauge already removed by Dirichlet)")

    # tiny free-L check (does L still run away? not scale selection)
    print("\n[freeL] Class-B free-L (L unknown) + rho(r_c) pin, 3 starts (does L still run away?):")
    def fullpin(w):
        ur, Lv = w[:-1], w[-1]; F = C.residual(tofull(ur, Lv), CTX, PRM, n5d=n5d_of("B"))
        return torch.cat([F, (split(ur)[1][0] - rr).reshape(1)])
    for seedL in (0.5, 1.0, 2.0):
        w0 = torch.cat([urA, torch.tensor([seedL])]); wF, PhiF = lm(w0, fullpin, maxit=150, budget=30.)
        print(f"      seedL={seedL:.1f} -> L={float(wF[-1]):+.4e}  Phi={PhiF:.2e}  (L still free = no scale selection)")
    print("\n[scope] pi_2 static S-Dir tile only; category-A/formulation diagnostic; NO Outcome A/B, NO pin/continuum,")
    print("        NO pi_3, NO physics verdict, NO absolute-L selection.")
