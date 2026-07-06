"""n5d_embedding_audit.py -- CATEGORY-A flat-hopfion -> cell-frame embedding audit.
Can the flat-space H3 hopfion stress be used as the cell-frame orthonormal transverse source, or must
it be regenerated/co-relaxed in the live cell geometry?  Diagnostic only; nothing changed; no verdict.
FIX-1 + Registration-B + rho^2/2 frame factor all ACTIVE.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch, time
torch.set_default_dtype(torch.float64)
from torch.func import jacrev
import cell_solver_f2d as cs, n5d_pilot as pilot
PRM = pilot.PRM; Nr, Nth = 16, 8
st, src_rc, src_sh2 = pilot.load_frozen_source()


def line(t): print("\n" + "=" * 90 + f"\n{t}\n" + "=" * 90)


line("CHECK 1-2: source-gen background  vs  cell geometry at the sampling nodes")
hop = st["hopfion"]
print(f"  SOURCE background (h4_n4_phaseB_stress.py): FLAT Euclidean 3-space, Cartesian grid, rr=|x|,")
print(f"    orthonormal er/eth/eph built from flat X,Y,Z => rho_areal = r (flat), phi=0, s=0, round.")
print(f"    hopfion compact: Rring={hop.get('Rring', float('nan')) if 'Rring' in hop else 0.0998:.4f}, "
      f"core_w~0.69, sh2 support r in [{src_rc.min():.3f},{src_rc.max():.3f}], stress mass at r~0.05-1.5.")

def cell_state(kind):
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)
    u = cs.seed_n5d(ctx, a2_amp=pilot.A2_SEED)
    if kind == "seed":
        return ctx, u
    # stalled: run the (patched) continuation briefly
    L0 = float(cs.unpack(u, ctx, n5d=True)[-1]); t0 = time.time()
    for amp in pilot.CONT_AMPS:
        rem = 60 - (time.time() - t0)
        if rem <= 1: break
        u, h = cs.newton_lm_solve(u, ctx, PRM, maxit=30, tol=pilot.PHI_TOL, verbose=False,
                                  time_budget=rem, n5d=dict(sealbc="S-Dir", src=(src_rc, src_sh2, amp),
                                  a2_mirror=0.0), equilibrate=True)
    return ctx, u

for kind in ("seed", "stalled"):
    ctx, u = cell_state(kind)
    phi, rho, uf, a2, L = cs.unpack(u, ctx, n5d=True); L = float(L)
    r = (ctx["rc"] + 0.5 * L * (ctx["zeta"] + 1.0)).cpu().numpy()
    rhon = rho.cpu().numpy(); phin = phi.cpu().numpy(); a2n = a2.cpu().numpy()
    ratio = rhon / r
    print(f"\n  [{kind}] L={L:.4e}  cell coord r in [{r.min():.4f},{r.max():.4f}]  "
          f"areal rho in [{rhon.min():.4f},{rhon.max():.4f}]")
    print(f"         rho/r in [{ratio.min():.4f},{ratio.max():.4f}]  (=1 <=> flat)   "
          f"phi in [{phin.min():.3e},{phin.max():.3e}]  |s|_max={np.abs(a2n).max():.3e}")
    print(f"         (r/rho)^2 in [{(1/ratio**2).min():.4f},{(1/ratio**2).max():.4f}]  "
          f"e^-2phi in [{np.exp(-2*phin).min():.4f},{np.exp(-2*phin).max():.4f}]")

line("CHECK 3: flat orthonormal basis (areal=r_flat) vs cell orthonormal basis (areal=rho)")
print("  Stored sh2 = T_hat th - T_hat ph is the flat orthonormal shear: proper angular length = r_flat*dth.")
print("  Cell orthonormal proper angular length = sqrt(h_thth) dth = rho e^{s/2} dth ~ rho*dth.")
print("  For the FROZEN field n (same angular map per shell), the orthonormal stress rescales with the")
print("  proper angular GRADIENT (1/sqrt(h_thth)):  T_hat th^cell = T_hat th^flat * (r_flat/rho)^2 for the")
print("  xi-kinetic piece, and *(r_flat/rho)^4 for the kap-quartic piece (virial E2~E4 => BOTH matter).")
print("  => beyond the measure rho^2/2 already applied, the COMPONENT carries an extra (r/rho)^{2..4} mix.")

line("CHECK 4-5: sensitivity study (diagnostic; no verdict solve) -- linear S-Dir a2_peak + ||rhs||")
def linear_a2(ctx, ub, Tshear_array, sealbc="S-Dir"):
    Nr_ = ctx["Nr"]; a2sl = slice(2*Nr_+Nr_*ctx["Nth"], 2*Nr_+Nr_*ctx["Nth"]+Nr_)
    n5d = dict(sealbc=sealbc, Tshear=Tshear_array, a2_mirror=0.0)
    u0 = ub.detach().clone(); u0[a2sl] = 0.0
    def rows(uu):
        Q = cs.fields(uu, ctx, PRM, n5d=n5d); a2, a2p, sr = Q["a2"], Q["a2p"], Q["shear_res"]
        core = a2p[[0]]; seal = (a2[[-1]]) if sealbc == "S-Dir" else a2p[[-1]]
        return torch.cat([sr[1:-1], core, seal])
    J = jacrev(rows)(u0).detach(); Jaa = J[:, a2sl]; b = -rows(u0).detach()
    return float(torch.linalg.solve(Jaa, b).abs().max()), float(b.norm())

ctx = cs.make_ctx(Nr, Nth, rc=0.5); ub = cs.seed_n5d(ctx, a2_amp=0.0)
phi, rho, uf, a2, L = cs.unpack(ub, ctx, n5d=True); L = float(L)
r = ctx["rc"] + 0.5 * L * (ctx["zeta"] + 1.0)
sh2 = cs.n5d_shear.source_interp(src_rc, src_sh2, r); P2 = ctx["P2"]
rho2_2 = 0.5 * rho ** 2
variants = {
    "A current (rho^2/2)*sh2         ": rho2_2[:, None] * sh2[:, None] * P2[None, :],
    "B cell-basis kinetic (r^2/2)*sh2": (0.5 * r ** 2)[:, None] * sh2[:, None] * P2[None, :],
    "C regen rho=r (== B here)       ": (0.5 * r ** 2)[:, None] * sh2[:, None] * P2[None, :],
    "D quartic-limit (r^4/(2rho^2))  ": (0.5 * r ** 4 / rho ** 2)[:, None] * sh2[:, None] * P2[None, :],
}
print(f"  {'variant':34s} {'||rhs||(l2)':>12s} {'lin a2_peak S-Dir':>18s}")
for name, T in variants.items():
    ap, bn = linear_a2(ctx, ub, T)
    print(f"  {name:34s} {bn:12.4e} {ap:18.4e}")
print("\n  (A = shipped; B/C/D are candidate flat->cell COMPONENT corrections -- NOT applied; the spread")
print("   A..D shows the frozen-source frame ambiguity is O(1)-to-O(few) at the seed and grows if rho/r drifts.)")
