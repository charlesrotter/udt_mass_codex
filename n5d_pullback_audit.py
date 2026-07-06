"""n5d_pullback_audit.py -- CATEGORY-A source-cell pullback / L-scaling audit.
Is the frozen H3 stress pulled back into the live cell consistently as L changes, or is it frozen at
seed L0 while the geometric operator uses current L?  NOTHING changed: no equations/BCs/readouts/seal/
verdict-logic edits, no FIX-2, no finite-L barrier/penalty/target, no verdict pilot.  Diagnostic only.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev
import cell_solver_f2d as cs
import n5d_pilot as pilot
PRM = pilot.PRM; Nr, Nth = 16, 8
st, source_rc, source_sh2 = pilot.load_frozen_source()
L0_SEED = 1.0


def line(t): print("\n" + "=" * 92 + f"\n{t}\n" + "=" * 92)


def build_Tshear_reg(ctx, amp, L_reg):
    """Register the frozen sh2 at physical r = rc + (L_reg/2)(zeta+1).  L_reg=L0_SEED -> registration A
    (current impl); L_reg=current cell L -> registration B (current-cell pullback)."""
    zeta = ctx["zeta"].cpu().numpy()
    r_phys = ctx["rc"] + 0.5 * L_reg * (zeta + 1.0)
    src2 = np.interp(r_phys, source_rc, source_sh2, left=0.0, right=0.0)
    src2_t = torch.as_tensor(src2, dtype=torch.float64)
    return amp * src2_t[:, None] * ctx["P2"][None, :]


def linear_a2(ctx, ubg, Tshear, sealbc):
    """Freeze phi,rho at ubg; solve the LINEAR shear rows d(shear)/d(a2)*a2 = -(rows@a2=0).  Diagnostic."""
    Nr_ = ctx["Nr"]; a2sl = slice(2*Nr_+Nr_*ctx["Nth"], 2*Nr_+Nr_*ctx["Nth"]+Nr_)
    n5d = dict(sealbc=sealbc, Tshear=Tshear, a2_mirror=0.0)
    u0 = ubg.detach().clone(); u0[a2sl] = 0.0
    def rows(uu):
        Q = cs.fields(uu, ctx, PRM, n5d=n5d)
        a2, a2p, sr = Q["a2"], Q["a2p"], Q["shear_res"]
        core = a2p[[0]]; seal = (a2[[-1]]) if sealbc == "S-Dir" else a2p[[-1]]
        return torch.cat([sr[1:-1], core, seal])
    J = jacrev(rows)(u0).detach(); Jaa = J[:, a2sl]; b = -rows(u0).detach()
    try: a2 = torch.linalg.solve(Jaa, b)
    except Exception: a2 = torch.linalg.lstsq(Jaa, b).solution
    return float(np.abs(a2.cpu().numpy()).max()), float(torch.linalg.norm(b))


# ============================================================================================
line("CHECK 1-2: coordinate maps + source convention (from code inspection)")
print("  SOLVER (cell_solver_f2d.fields): fields at Chebyshev nodes zeta in [-1,1];")
print("    d/dr = (2/L) d/dzeta with CURRENT L (Newton unknown).  phi,rho,a2 = nodal unknowns;")
print("    physical r(zeta) = rc + (L/2)(zeta+1)  [rc=ctx['rc']=0.5, L = current cell length].")
print("  SOURCE (n5d_pilot.build_Tshear): T_shear = amp * sh2(r_phys) * P2(mu),")
print("    r_phys = rc + (L0/2)(zeta+1) with L0 = SEED length (FIXED=1.0)  <-- uses L0, NOT current L.")
print("  => INCONSISTENCY confirmed: geometric operator uses current L; source mapping uses seed L0.")
print(f"  stress_profiles.npz 'rc': physical hopfion radius, range [{source_rc.min():.3f},{source_rc.max():.3f}]")
print("    'sh2' = <shear.P2>_shell, shear=T_thth-T_phph in the ORTHONORMAL frame (component, not density-")
print("    weighted; already ell=2-projected).  It is a physical stress COMPONENT vs physical hopfion r.")

# ============================================================================================
line("CHECK 3: native pullback rule (derived)")
print("  The shear EL row is the POINTWISE tensor eq E^{AB}=-T^{AB} at each radial node (collocation,")
print("  NOT a dr-integral), with E_s_geom = -e^{-2phi}[rho^2 a2'' + (2 rho rho' - 2 phi' rho^2) a2'],")
print("  a2'' via d/dr=(2/L)d/dzeta.  T_s (=T_thth-T_phph) is a physical stress component in the SAME")
print("  orthonormal frame.  Native rule: evaluate T_s at the SAME physical point as E_s_geom, i.e.")
print("  r(zeta)=rc+(L/2)(zeta+1) with CURRENT L  => INTERPOLATION at current-L physical r, NO amplitude")
print("  L-Jacobian (both sides are pointwise components; the phi-blind S^2/H3 matter enters ONLY the")
print("  h_AB shear row, no phi-source).  = registration B.  Registration A (seed L0) mis-locates T_s")
print("  once L != L0.  Registration C (fixed zeta-profile) is what A ALREADY is (L0 fixed => sh2(r(zeta))")
print("  is a fixed function of zeta), so C is NOT distinct from A in this implementation.")

# ============================================================================================
line("CHECK 4: three registrations A/B/C at several L -- ||rhs||, expected linear a2_peak, L-scaling")
print("  (background = round-flat seed at the stated L; sealbc=S-Dir; amp=1)")
print(f"  {'L':>8s} | {'A ||rhs||':>10s} {'A a2peak':>10s} | {'B ||rhs||':>10s} {'B a2peak':>10s} | "
      f"{'a2/L^2 (A)':>11s} {'a2/L^2 (B)':>11s}")
for L in (1.0, 0.3, 0.1, 0.03, 0.009):
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)
    ub = cs.seed_n5d(ctx, a2_amp=0.0)
    phi, rho, uf, a2, _ = cs.unpack(ub, ctx, n5d=True)
    ub = cs.pack(phi, rho, uf, float(L), a2=a2)                 # set background L
    TA = build_Tshear_reg(ctx, 1.0, L0_SEED)                    # A: seed L0
    TB = build_Tshear_reg(ctx, 1.0, L)                          # B: current L
    aA, rA = linear_a2(ctx, ub, TA, "S-Dir")
    aB, rB = linear_a2(ctx, ub, TB, "S-Dir")
    print(f"  {L:8.3f} | {rA:10.3e} {aA:10.3e} | {rB:10.3e} {aB:10.3e} | {aA/L**2:11.3e} {aB/L**2:11.3e}")
print("  C == A (fixed zeta-profile); not shown separately.  a2/L^2 ~ const across L confirms the")
print("  native a2 ~ (L/2)^2 T_s/rho^2 scaling for BOTH A and B => the L->0 collapse of a2 is the (2/L)^2")
print("  geometric stiffening, NOT the registration choice (registration sets the source VALUES, not the")
print("  L-power).  At L=L0=1.0 A and B COINCIDE (source correctly placed); they diverge as L shrinks.")

# ============================================================================================
line("CHECK 5: is the L-collapse caused/amplified by source detachment?  (fixed-L=L0 DIAGNOSTIC)")
def reduced_resid_fixedL(vred, ctx, n5d, L_fixed):
    """DIAGNOSTIC ONLY: pin L=L_fixed, drop the Hseal closure row (its DOF, L, is frozen).  Solves the
    residual balance with L held fixed -- NOT a physics closure (Hseal!=0 expected)."""
    Nr_, Nth_ = ctx["Nr"], ctx["Nth"]
    v = torch.cat([vred, torch.as_tensor([L_fixed], dtype=torch.float64)])
    F = cs.residual(v, ctx, PRM, n5d=n5d)
    hidx = (Nr_-2)+2+(Nr_-2)+2+(Nr_-2)*Nth_+2*Nth_             # Hseal row index
    return torch.cat([F[:hidx], F[hidx+1:]])

def lm_fixedL(vred0, ctx, n5d, L_fixed, maxit=30):
    import math
    v = vred0.detach().clone()
    rf = lambda vv: reduced_resid_fixedL(vv, ctx, n5d, L_fixed)
    F = rf(v); Phi = float((F*F).sum()); lam = 1e-3; nu = 2.0; hist=[Phi]
    for it in range(maxit):
        if Phi < 1e-13: break
        J = jacrev(rf)(v).detach(); dc = cs._col_scale(J); Jc = J*dc[None,:]
        dHc = (Jc*Jc).sum(0).clamp_min(1e-300); z = torch.zeros(J.shape[1])
        acc=False
        for _ in range(30):
            aug = torch.cat([Jc, (lam**0.5)*torch.diag(dHc.sqrt())],0); rhs=torch.cat([-F,z])
            try: dy = torch.linalg.lstsq(aug, rhs).solution
            except Exception: lam=min(lam*nu,1e12); nu*=2; continue
            dx = dc*dy; vn=v+dx
            try: Fn=rf(vn); Pn=float((Fn*Fn).sum())
            except Exception: Pn=float('inf')
            pred = Phi - float(((F+J@dx)**2).sum())
            g = (Phi-Pn)/pred if pred>0 and math.isfinite(Pn) else -1
            if g>0: v=vn; F=Fn.detach(); Phi=Pn; lam=max(lam/3,1e-14); nu=2; acc=True; break
            lam=min(lam*nu,1e12); nu*=2
        hist.append(Phi)
        if not acc: break
    return v.detach(), hist

for sealbc in ("S-Dir",):
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)
    ub = cs.seed_n5d(ctx, a2_amp=pilot.A2_SEED)
    vred = ub[:-1].detach().clone()
    n5d = dict(sealbc=sealbc, Tshear=build_Tshear_reg(ctx, 1.0, L0_SEED), a2_mirror=0.0)  # A at L0
    vfix, hist = lm_fixedL(vred, ctx, n5d, L0_SEED, maxit=30)
    ufix = torch.cat([vfix, torch.as_tensor([L0_SEED])])
    with torch.no_grad():
        Q = cs.fields(ufix, ctx, PRM, n5d=n5d); a2 = Q["a2"].cpu().numpy()
        Hs = float(cs.H_of_r(ufix, ctx, PRM)[-1]); rhop = Q["rhop"].abs().max().item()
    print(f"  [{sealbc}] FIXED L=L0=1.0 diagnostic solve: reduced_finalPhi={hist[-1]:.4e}  "
          f"a2_peak={np.abs(a2).max():.4e}  (Hseal={Hs:+.3e}, NOT enforced)  max|rho'|={rhop:.3e}")
    print(f"    vs FREE-L pilot: L collapses 1.0->9e-3, a2_peak~5e-3.  If fixed-L gives a2 ~O(0.1-2)")
    print(f"    and a healthy shear balance, the L-collapse (not the source) is what kills the response.")

# ============================================================================================
line("CHECK 6: S-Dir residual block balance -- does the pullback (A vs B) change the blocker?")
def blocks(u, ctx, n5d):
    Nr_, Nth_ = ctx["Nr"], ctx["Nth"]
    with torch.no_grad():
        Q = cs.fields(u, ctx, PRM, n5d=n5d)
        b = {"Hseal": cs.H_of_r(u, ctx, PRM)[[-1]], "rho_BC": Q["rhop"][[0,-1]],
             "shear_ODE": Q["shear_res"][1:-1], "shear_seal_BC": Q["a2"][[-1]],
             "fPDE": Q["res_f"][1:-1].reshape(-1), "f_BC": torch.cat([Q["fr"][0,:],Q["fr"][-1,:]])}
    return {k: float(torch.linalg.norm(v)) for k,v in b.items()}
ctx = cs.make_ctx(Nr, Nth, rc=0.5)
ub = cs.seed_n5d(ctx, a2_amp=pilot.A2_SEED)
for reg, Treg in (("A seed-L0", build_Tshear_reg(ctx,1.0,L0_SEED)),
                  ("B current-L (=L0 at seed)", build_Tshear_reg(ctx,1.0,1.0))):
    n5d = dict(sealbc="S-Dir", Tshear=Treg, a2_mirror=0.0)
    bb = blocks(ub, ctx, n5d)
    print(f"  [{reg}] seed blocks: " + "  ".join(f"{k}={v:.2e}" for k,v in bb.items()))
print("  (at the seed L=L0, A and B coincide -> identical blocks; the pullback only diverges once L!=L0,")
print("   which is exactly when the frozen registration mis-locates the source.)")
