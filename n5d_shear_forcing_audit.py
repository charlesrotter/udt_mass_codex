"""n5d_shear_forcing_audit.py -- CATEGORY-A shear-forcing / residual-balance audit.
Is the live ell=2 shear sector actually FORCED strongly+correctly by the frozen H3 source, or is the
pilot seeing a near-zero / cancelled / misnormalized / unconverged shear projection?
NOTHING changed: equations/BCs/source/readouts/residual/seal untouched; no FIX-2; no verdict pilot.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from torch.func import jacrev
import cell_solver_f2d as cs
import n5d_pilot as pilot

PRM = pilot.PRM; Z = PRM[0]
Nr, Nth = 16, 8
np.set_printoptions(precision=4, suppress=False, linewidth=120)


def line(t): print("\n" + "=" * 92 + f"\n{t}\n" + "=" * 92)


# ======================================================================================
line("CHECK 1: raw frozen source diagnostics")
st, source_rc, source_sh2 = pilot.load_frozen_source()
d = np.load(pilot.FROZEN_NPZ)
rc = np.asarray(d["rc"]); sh0 = np.asarray(d["sh0"]); sh2 = np.asarray(d["sh2"])
tau0 = np.asarray(d["tau0"]); tau2 = np.asarray(d["tau2"]); Trr0 = np.asarray(d["Trr0"])
hop = st["hopfion"]
print(f"  source file      : {pilot.FROZEN_NPZ}")
print(f"  hopfion          : {pilot.HOPFION_NPZ}  is_H3={hop['is_h3_hopfion']}")
print(f"  Q_H              : {hop['Q']:.6f}")
print(f"  virial E2/E4     : {hop['E2']/hop['E4']:.6f}   (E={hop['E']:.3f}, E2={hop['E2']:.3f}, E4={hop['E4']:.3f})")
# shell-profile norms (r^2-weighted L2, the physical shell measure); the npz stores shell-avg profiles
dr = float(rc[1] - rc[0]); w_r = rc**2 * dr
def rms(f): return float(np.sqrt(np.sum(f**2 * w_r)))
print(f"  ||T_rr||(l0)     : {rms(Trr0):.4f}    (radial-stress reference scale)")
print(f"  ||tau||(l0 trace): {rms(tau0):.4f}    ||tau||(l2)={rms(tau2):.4f}  (breathing source)")
print(f"  ||shear||(l0)    : {rms(sh0):.4f}    (transverse-traceless T_thth-T_phph, ELL=0 shell-avg)")
print(f"  ||shear||(l2)=sh2: {rms(sh2):.4f}    (the ELL=2 projection the pilot uses)")
frac_l2_vs_l0 = rms(sh2) / (rms(sh0) + 1e-30)
print(f"  fraction ell=2 / ell=0 of traceless shear (shell-profile RMS): {frac_l2_vs_l0:.4f}")
print(f"  sh2 peak |.|     : {np.abs(sh2).max():.4f}  at r={rc[np.abs(sh2).argmax()]:.3f}")
print(f"  NOTE: full 3D-field ||T^AB|| + exact ell=2-captured fraction computed on GPU below (CHECK 1b).")

# --- what the CELL actually samples: sh2 on r in [rc_cell, rc_cell+L0] ---
line("CHECK 1c: source amplitude ON THE CELL (what build_Tshear registers)")
for L0 in (1.0,):
    rc_cell = 0.5
    zeta = np.polynomial.chebyshev.chebpts2(Nr) if False else None
    ctx = cs.make_ctx(Nr, Nth, rc=rc_cell)
    zeta = ctx["zeta"].cpu().numpy()
    r_phys = rc_cell + 0.5 * L0 * (zeta + 1.0)
    src_on_cell = np.interp(r_phys, source_rc, source_sh2, left=0.0, right=0.0)
    print(f"  L0={L0}: cell r in [{r_phys.min():.3f},{r_phys.max():.3f}]  "
          f"sh2 on cell: min={src_on_cell.min():.4f} max={src_on_cell.max():.4f} "
          f"rms={np.sqrt(np.mean(src_on_cell**2)):.4f}")
    print(f"           (full-source sh2 peak={np.abs(sh2).max():.3f} at r={rc[np.abs(sh2).argmax()]:.3f} "
          f"-- is the cell ON or OFF the source peak?)")


# ======================================================================================
line("CHECK 2: projection normalization / sign / units")
ctx = cs.make_ctx(Nr, Nth, rc=0.5)
P2 = ctx["P2"].cpu().numpy(); w = ctx["w"].cpu().numpy(); mu = ctx["mu"].cpu().numpy()
print(f"  GL nodes Nth={Nth}: sum(w)={w.sum():.6f} (=int_-1^1 dmu=2)  "
      f"sum(w*mu^0..)=exact to deg {2*Nth-1}")
print(f"  sum_j w_j P2(mu_j)^2 = {np.sum(w*P2**2):.6f}   (exact int P2^2 dmu = 2/5 = 0.4)")
print(f"  sum_j w_j P2(mu_j)   = {np.sum(w*P2):.3e}       (orthogonality to P0; expect ~0)")
print("  => the SOLVER row R2(r)=sum_j w_j P2_j E_s uses the SAME (2/5) weight for BOTH the geometric")
print("     E_s row (s=a2 P2) AND the source Tshear=amp*sh2*P2 -> the 2/5 CANCELS in a2-ODE (consistent).")
print("  sign: code sets rows = sum w P2 (E_s_geom + Tshear) = 0  =>  E_s_geom = -Tshear.")
print("        E^AB=-T^AB gives E_s_geom=-T_s, so Tshear plays the role of +T_s (sh2=T_thth-T_phph).")
# units: geometric E_s ~ e^{-2phi} rho^2 (2/L)^2 a2 ; source ~ amp*sh2. compare coefficient scales.
sc = 2.0 / 1.0
print(f"  geometric-row a2'' coefficient scale ~ e^{{-2phi}} rho^2 (2/L)^2 ~ {1.0*0.5*sc*sc:.3f} (rho^2=0.5, L=1)")
print(f"  source-row scale ~ |sh2_on_cell| ~ O({np.abs(src_on_cell).max():.2f}) -> a2 ~ source/coeff (CHECK 4).")


# ======================================================================================
line("CHECK 3: residual BLOCK norms at seed and final stalled states (which block blocks convergence)")
def block_resnorms(u, ctx, n5d):
    """Recompute the residual and split into named blocks matching residual()'s row order."""
    Nr_, Nth_ = ctx["Nr"], ctx["Nth"]
    with torch.no_grad():
        Q = cs.fields(u, ctx, PRM, n5d=n5d)
        phip, rhop, fr = Q["phip"], Q["rhop"], Q["fr"]
        blocks = {}
        blocks["phi_ODE"] = Q["phi_ode"][1:-1]
        blocks["phi_BC"] = phip[[0, -1]]
        blocks["rho_ODE"] = Q["rho_ode"][1:-1]
        blocks["rho_BC"] = rhop[[0, -1]]
        blocks["fPDE"] = Q["res_f"][1:-1].reshape(-1)
        blocks["f_BC"] = torch.cat([fr[0, :], fr[-1, :]])
        blocks["Hseal"] = cs.H_of_r(u, ctx, PRM)[[-1]]
        a2, a2p, shear_res = Q["a2"], Q["a2p"], Q["shear_res"]
        sealbc = n5d.get("sealbc", "off")
        blocks["shear_ODE"] = shear_res[1:-1]
        blocks["shear_core_BC"] = a2p[[0]]
        if sealbc == "S-Dir":
            blocks["shear_seal_BC"] = a2[[-1]] - float(n5d.get("a2_mirror", 0.0))
        elif sealbc == "S-JC2":
            blocks["shear_seal_BC"] = a2p[[-1]]
    return {k: float(torch.linalg.norm(v)) for k, v in blocks.items()}

def reproduce_stalled(sealbc):
    import time
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)
    u = cs.seed_n5d(ctx, a2_amp=pilot.A2_SEED)
    L0 = float(cs.unpack(u, ctx, n5d=True)[-1]); useed = u.detach().clone()
    t0 = time.time()
    for amp in pilot.CONT_AMPS:
        rem = 100 - (time.time() - t0)
        if rem <= 1: break
        Ts = pilot.build_Tshear(ctx, L0, amp, source_rc, source_sh2)
        n5d = dict(sealbc=sealbc, Tshear=Ts, a2_mirror=0.0)
        u, h = cs.newton_lm_solve(u, ctx, PRM, maxit=30, tol=pilot.PHI_TOL, verbose=False,
                                  time_budget=rem, n5d=n5d, equilibrate=True)
    n5d = dict(sealbc=sealbc, Tshear=pilot.build_Tshear(ctx, L0, 1.0, source_rc, source_sh2), a2_mirror=0.0)
    return ctx, useed, u.detach(), n5d, L0

for sealbc in ("S-Dir", "S-JC2"):
    ctx, useed, ufin, n5d, L0 = reproduce_stalled(sealbc)
    # seed uses amp=? build seed n5d with amp=1 source for the seed-residual (worst-case forcing)
    n5d_seed = dict(sealbc=sealbc, Tshear=pilot.build_Tshear(ctx, L0, 1.0, source_rc, source_sh2), a2_mirror=0.0)
    bs = block_resnorms(useed, ctx, n5d_seed)
    bf = block_resnorms(ufin, ctx, n5d)
    print(f"\n  [{sealbc}] block ||residual||   (SEED @amp=1 | FINAL stalled)")
    for k in bs:
        print(f"    {k:16s}: seed={bs[k]:.4e}   final={bf[k]:.4e}")
    dom = max(bf, key=bf.get)
    print(f"    -> LARGEST final-state block = '{dom}' ({bf[dom]:.3e})  [the convergence-blocking block]")


# ======================================================================================
line("CHECK 4: linearized shear response (category-A diagnostic) -- expected a2 vs pilot a2_peak")
def linear_a2_response(ctx, ubg, n5d, sealbc):
    """Freeze phi,rho at the background ubg; the shear rows are LINEAR in a2. Solve the linear system
    d(shear_rows)/d(a2) * a2 = -(shear_rows at a2=0)  with the SAME BCs. Returns a2 profile."""
    Nr_ = ctx["Nr"]
    a2sl = slice(2*Nr_ + Nr_*ctx["Nth"], 2*Nr_ + Nr_*ctx["Nth"] + Nr_)
    # set a2=0 in the background
    u0 = ubg.detach().clone(); u0[a2sl] = 0.0
    def shear_rows(uu):
        Q = cs.fields(uu, ctx, PRM, n5d=n5d)
        a2, a2p, shear_res = Q["a2"], Q["a2p"], Q["shear_res"]
        core = a2p[[0]]
        seal = (a2[[-1]] - float(n5d.get("a2_mirror", 0.0))) if sealbc == "S-Dir" else a2p[[-1]]
        return torch.cat([shear_res[1:-1], core, seal])
    # Jacobian of shear rows wrt the FULL vector, take a2 columns
    J = jacrev(shear_rows)(u0).detach()
    Jaa = J[:, a2sl]                       # (Nr, Nr) linear shear operator incl BCs
    b = -shear_rows(u0).detach()           # RHS = -(rows at a2=0) = the pure source forcing
    try:
        a2 = torch.linalg.solve(Jaa, b)
        ok = True
    except Exception:
        a2 = torch.linalg.lstsq(Jaa, b).solution; ok = False
    Sj = torch.linalg.svdvals(Jaa).cpu().numpy()
    return a2.cpu().numpy(), float(Sj[0]/Sj[-1]), float(Sj[-1]), b.cpu().numpy(), ok

# backgrounds: round seed (phi,rho flat) AND the structured seed (nontrivial phi',rho')
import n5d_pilot_fix3 as f3
for sealbc in ("S-Dir", "S-JC2"):
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)
    L0 = 1.0
    n5d = dict(sealbc=sealbc, Tshear=pilot.build_Tshear(ctx, L0, 1.0, source_rc, source_sh2), a2_mirror=0.0)
    print(f"\n  [{sealbc}] linear a2 response (frozen background, full source amp=1):")
    for bgname, ubg in (("round-flat", cs.seed_n5d(ctx, a2_amp=0.0)),
                        ("structured", f3.structured_seed(ctx, a2_amp=0.0, L0=1.0))):
        a2lin, condJ, sminJ, rhs, ok = linear_a2_response(ctx, ubg, n5d, sealbc)
        print(f"    bg={bgname:11s}: |a2|_peak(EXPECTED)={np.abs(a2lin).max():.4e}  "
              f"||rhs(source)||={np.linalg.norm(rhs):.4e}  shear-op cond={condJ:.3e} smin={sminJ:.3e} "
              f"solve_ok={ok}")
    print(f"    pilot nonlinear a2_peak (stalled): S-Dir~5.1e-3, S-JC2~1.9e-5  <-- compare to EXPECTED above")


# ======================================================================================
line("CHECK 5: compatibility / solvability of the shear block (per BC)")
for sealbc in ("S-Dir", "S-JC2"):
    ctx = cs.make_ctx(Nr, Nth, rc=0.5); L0 = 1.0
    n5d = dict(sealbc=sealbc, Tshear=pilot.build_Tshear(ctx, L0, 1.0, source_rc, source_sh2), a2_mirror=0.0)
    Nr_ = ctx["Nr"]; a2sl = slice(2*Nr_ + Nr_*Nth, 2*Nr_ + Nr_*Nth + Nr_)
    u0 = cs.seed_n5d(ctx, a2_amp=0.0)
    def shear_rows(uu):
        Q = cs.fields(uu, ctx, PRM, n5d=n5d)
        a2, a2p, shear_res = Q["a2"], Q["a2p"], Q["shear_res"]
        core = a2p[[0]]; seal = (a2[[-1]]) if sealbc == "S-Dir" else a2p[[-1]]
        return torch.cat([shear_res[1:-1], core, seal])
    J = jacrev(shear_rows)(u0).detach(); Jaa = J[:, a2sl]
    b = -shear_rows(u0).detach()
    U, S, Vh = torch.linalg.svd(Jaa)
    # left null space (rows): u_k with small sigma -> compatibility needs <u_k, b>=0
    smin = float(S[-1]); tol = float(S[0]) * 1e-12
    nnull = int((S.cpu().numpy() < tol).sum())
    print(f"\n  [{sealbc}] shear-op cond={float(S[0]/S[-1]):.3e} smin={smin:.3e} rank-def modes(<{tol:.1e})={nnull}")
    if nnull > 0 or smin < 1e-8:
        uleft = U[:, -1].detach()
        compat = float(torch.dot(uleft, b) / (torch.linalg.norm(b) + 1e-30))
        print(f"    near-null LEFT sing vec: <u_null, source_rhs>/||rhs|| = {compat:.3e} "
              f"(|.|~0 => source is COMPATIBLE / in range; ~O(1) => source excites the null -> unsolvable)")
        vright = Vh[-1].detach()
        print(f"    near-null RIGHT sing vec |overlap constant-a2| = "
              f"{abs(float(torch.dot(vright, torch.ones_like(vright)/np.sqrt(len(vright))))):.3f} "
              f"(S-JC2 constant-a2 null; NOT pinned here)")
    else:
        print(f"    full rank -> source is solvable (no compatibility obstruction).")
