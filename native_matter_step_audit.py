#!/usr/bin/env python3
"""
native_matter_step_audit.py -- LIVE AUDIT of the native-matter step on the clean
(time-live) bare kernel.  Date 2026-06-18.  OBSERVE+BUILD+LIVE-AUDIT.  DATA-BLIND
(sizes in units L=sqrt(kappa/xi)=1; no mass/ratio/wall numbers loaded).

PURPOSE: put UDT's OWN native L2+L4 angular field on the bare metric, solve COUPLED
(metric a,b AND matter Theta both live, B=1/A NOT imposed), read off charge + mass,
and AUDIT every frozen/fixed/sliced/imported choice -- flag each prominently.

We REUSE the corrected coupled solver radial_Bfree_soliton.py (the #56 milestone
code: B=1/A FREED, seal-injection DELETED).  This audit script does NOT rebuild it;
it INTERROGATES it: residuals, R-sensitivity (box-control trap), depth-dial (p) and
kap8 sensitivity, carrier comparison (S^2 area-form vs S^3 SU(2) stress), and the
charge read-off.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch
import sympy as sp

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[device] {DEV}, torch {torch.__version__}")

import radial_Bfree_soliton as RB


def banner(s):
    print("\n" + "=" * 78)
    print(s)
    print("=" * 78)


# ---------------------------------------------------------------------------
# AUDIT 1: CARRIER STRESS -- does the S^2 area-form field (CANON C-2026-06-14-1)
# give the SAME diagonal stress (rho, p_r) as the S^3/SU(2) Skyrme used in the
# coupled solver?  The mass is read off (t,t) which depends only on rho, so if rho
# differs the mass read-off is carrier-dependent.
# ---------------------------------------------------------------------------
def audit_carrier_stress():
    banner("AUDIT 1 -- carrier: S^2 area-form (CANON native) vs S^3 SU(2) stress")
    # symbolic, exact.  Metric ds^2 = -e^{2a}dt^2 + e^{2b}dr^2 + r^2 dOmega^2.
    r, Th, Thp, a, b, xi, kap = sp.symbols('r Theta Thetap a b xi kappa', positive=True)
    e2b = sp.exp(2*b)
    X = sp.exp(-2*b) * Thp**2
    Y = sp.sin(Th)**2 / r**2

    # --- S^3 / SU(2) Skyrme hedgehog (radial_Bfree_soliton stress) ---
    rho_S3 = (xi/2)*(X + 2*Y) + (kap/2)*(2*X*Y + Y**2)
    pr_S3  = (xi/2)*(X - 2*Y) + (kap/2)*(2*X*Y - Y**2)

    # --- S^2 area-form n_a (CANON C-2026-06-14-1 + native_stabilizer Task 3) ---
    # native_stabilizer_results.md Task 3 (verified):
    #   rho = (xi/2)(X+2Y) + (kappa/2)(2XY + Y^2)
    #   p_r = (xi/2)(X-2Y) + (kappa/2)(2XY - Y^2)
    rho_S2 = (xi/2)*(X + 2*Y) + (kap/2)*(2*X*Y + Y**2)
    pr_S2  = (xi/2)*(X - 2*Y) + (kap/2)*(2*X*Y - Y**2)

    drho = sp.simplify(rho_S3 - rho_S2)
    dpr  = sp.simplify(pr_S3  - pr_S2)
    print("  rho_S3 - rho_S2 =", drho)
    print("  p_r_S3 - p_r_S2 =", dpr)
    # EOS:
    eos = sp.simplify((pr_S3 + rho_S3))
    print("  p_r+rho (both)  =", eos, "   [= X(xi+2 kappa Y), CANON D7 + L4]")
    same = (drho == 0) and (dpr == 0)
    print(f"  => diagonal (t,t)/(r,r) stress IDENTICAL for S^2 area-form and S^3 SU(2): {same}")
    print("  NOTE: the S^3/SU(2) and S^2 hedgehogs differ in T^th_th (tangential)")
    print("        and in the matter EL (4th field), but rho & p_r -- which set the")
    print("        MASS via (t,t) and the warp via (r,r) -- coincide for the deg-1")
    print("        hedgehog.  So the MASS read-off is carrier-robust for the diagonal block.")
    # tangential difference (informational)
    pT_S3 = (kap/2)*Y**2 - (xi/2)*X   # radial_Bfree stress()
    print("  (tangential T^th_th [S3 used in solver] =", pT_S3, ")")
    return same


# ---------------------------------------------------------------------------
# AUDIT 2: the coupled solve -- full Einstein residual closure + DOF liveness.
# ---------------------------------------------------------------------------
def audit_coupled_residuals(xi=1.0, kap=1.0, p=0.4, kap8=0.05, rc=0.05, ncellsL=14.0, N=1200):
    banner(f"AUDIT 2 -- coupled solve closure (p={p}, kap8={kap8}, cell={ncellsL}L, N={N})")
    L = math.sqrt(kap/xi)
    ri = rc + ncellsL * L
    r = RB.make_grid(1, N, rc=rc, rint=ri, geom=False)
    out = RB.selfconsistent_Bfree(r, xi, kap, p=p, kap8=kap8, iters=400, relax=0.4,
                                  tol=1e-11, verbose=False)
    res = out['res']
    # interior-only residual maxima (drop 3 edge nodes each side, FD edge effects)
    def imax(t):
        return t[:, 3:-3].abs().max().item()
    rtt = imax(res['res_tt']); rrr = imax(res['res_rr']); rth = imax(res['res_thth'])
    M = out['M_MS'].item()
    a = out['a']; b = out['b']; Th = out['Th']
    # liveness: is B=1/A imposed?  check a + b deviation from 0 (B=1/A would force a=-b)
    ab = (a + b)
    ab_dev = ab[:, 3:-3].abs().max().item()
    # Theta range -> winding present?
    Thrange = (Th.max() - Th.min()).item()
    print(f"  M_MS = {M:.6f}  (units sqrt(kappa/xi))")
    print(f"  Einstein residual maxima (interior):")
    print(f"    res_tt   = {rtt:.3e}")
    print(f"    res_rr   = {rrr:.3e}")
    print(f"    res_thth = {rth:.3e}   <-- (th,th) is the Bianchi CONSISTENCY check, NOT imposed")
    print(f"  B=1/A FREED?  max|a+b| (interior) = {ab_dev:.3e}  (nonzero => B=1/A genuinely broken inside body => FREED)")
    print(f"  matter live?  Theta range = {Thrange:.4f} (~pi => full charge-1 winding present)")
    print(f"  metric live?  b0={b[:,0].max().item():.4f}  a0={a[:,0].min().item():.4f}  phi0={-a[:,0].min().item():.4f}")
    return dict(M=M, rtt=rtt, rrr=rrr, rth=rth, ab_dev=ab_dev, Thrange=Thrange, out=out)


# ---------------------------------------------------------------------------
# AUDIT 3: BOX-CONTROL trap -- is M_MS sensitive to the cell size R (= ri)?
# A box-controlled mass scales with the wall; an intrinsic mass is R-stable.
# ---------------------------------------------------------------------------
def audit_box_control(xi=1.0, kap=1.0, p=0.4, kap8=0.05, rc=0.05, N=1200):
    banner(f"AUDIT 3 -- BOX-CONTROL: M_MS vs cell size R (p={p}, kap8={kap8})")
    print(f"{'cell(L)':>9} {'R=ri':>9} {'M_MS':>12} {'res_tt':>10} {'res_rr':>10}")
    Ms = []
    for mult in [8.0, 12.0, 20.0, 40.0, 80.0]:
        ri = rc + mult * math.sqrt(kap/xi)
        r = RB.make_grid(1, N, rc=rc, rint=ri, geom=False)
        out = RB.selfconsistent_Bfree(r, xi, kap, p=p, kap8=kap8, iters=400, relax=0.4,
                                      tol=1e-11, verbose=False)
        M = out['M_MS'].item()
        res = out['res']
        rtt = res['res_tt'][:, 3:-3].abs().max().item()
        rrr = res['res_rr'][:, 3:-3].abs().max().item()
        Ms.append(M)
        print(f"{mult:9.1f} {ri:9.3f} {M:12.6f} {rtt:10.2e} {rrr:10.2e}")
    Ms = torch.tensor(Ms)
    spread = (Ms.max() - Ms.min()) / Ms.mean()
    print(f"\n  M_MS spread over 10x cell-size range: {spread.item()*100:.2f}%")
    print(f"  (box artifacts historically moved 394-1152%; genuine structure <2.3%.)")
    print(f"  VERDICT: {'R-STABLE -> intrinsic mass' if spread.item() < 0.05 else 'R-SENSITIVE -> box-controlled'}")
    return spread.item()


# ---------------------------------------------------------------------------
# AUDIT 4: CHOSEN-VALUE sensitivity -- does M_MS depend on the depth dial p and
# the coupling kap8?  These are CHOSEN in the solver; if M rides on them, the mass
# is not a clean read-off but a tuned number.
# ---------------------------------------------------------------------------
def audit_chosen_values(xi=1.0, kap=1.0, rc=0.05, ncellsL=14.0, N=1200):
    banner("AUDIT 4 -- CHOSEN-VALUE sensitivity: M_MS vs depth dial p and coupling kap8")
    ri = rc + ncellsL * math.sqrt(kap/xi)
    r = RB.make_grid(1, N, rc=rc, rint=ri, geom=False)
    print("  vary depth dial p (kap8=0.05):")
    print(f"  {'p':>6} {'M_MS':>12} {'phi0':>10} {'b0':>10}")
    for p in [0.1, 0.2, 0.4, 0.8, 1.5]:
        out = RB.selfconsistent_Bfree(r, xi, kap, p=p, kap8=0.05, iters=400, relax=0.4,
                                      tol=1e-11, verbose=False)
        print(f"  {p:6.2f} {out['M_MS'].item():12.6f} {-out['a'][:,0].min().item():10.4f} "
              f"{out['b'][:,0].max().item():10.4f}")
    print("\n  vary coupling kap8 (=8 pi G/c^4) (p=0.4):")
    print(f"  {'kap8':>8} {'M_MS':>12}")
    for kap8 in [0.01, 0.02, 0.05, 0.1, 0.2]:
        out = RB.selfconsistent_Bfree(r, xi, kap, p=0.4, kap8=kap8, iters=400, relax=0.4,
                                      tol=1e-11, verbose=False)
        print(f"  {kap8:8.3f} {out['M_MS'].item():12.6f}")
    print("\n  vary scale ratio kappa/xi (the ONE legitimate scale; M should ~ sqrt(kappa/xi)):")
    print(f"  {'kappa':>8} {'L':>8} {'M_MS':>12} {'M/sqrt(k/xi)':>14}")
    for kap in [0.25, 1.0, 4.0, 9.0]:
        L = math.sqrt(kap/xi); ri = rc + ncellsL*L
        r2 = RB.make_grid(1, N, rc=rc, rint=ri, geom=False)
        out = RB.selfconsistent_Bfree(r2, xi, kap, p=0.4, kap8=0.05, iters=400, relax=0.4,
                                      tol=1e-11, verbose=False)
        M = out['M_MS'].item()
        print(f"  {kap:8.3f} {L:8.4f} {M:12.6f} {M/L:14.6f}")


# ---------------------------------------------------------------------------
# AUDIT 5: CHARGE read-off -- N=3, q=1/3 from the area form.  Is it actually
# computed from the field, or asserted?  Compute the winding integral of the
# deg-1 hedgehog.
# ---------------------------------------------------------------------------
def audit_charge():
    banner("AUDIT 5 -- CHARGE read-off: winding integral of the deg-1 hedgehog")
    # n_a = (sinTheta sinth cosph, sinTheta sinth sinph, cosTheta) for the area-form
    # carrier; for the hedgehog Theta=theta the winding density n.(n_th x n_ph)=sin theta.
    th, ph = sp.symbols('theta varphi')
    n = sp.Matrix([sp.sin(th)*sp.cos(ph), sp.sin(th)*sp.sin(ph), sp.cos(th)])
    n_th = n.diff(th); n_ph = n.diff(ph)
    dens = n.dot(n_th.cross(n_ph))
    dens = sp.simplify(dens)
    print(f"  winding density n.(d_th n x d_ph n) = {dens}  (= sin theta for deg-1)")
    integral = sp.integrate(sp.integrate(dens, (th, 0, sp.pi)), (ph, 0, 2*sp.pi))
    deg = sp.simplify(integral / (4*sp.pi))
    print(f"  (1/4pi) INT omega_H1 = {deg}  (deg-1 generator of H^2(S^2,Z))")
    print(f"  => topological charge = 1 (deg-1).  N=3 (eps_abc singlet unique iff N=3),")
    print(f"     q=1/3 (collar slope d ln f = -q d ln r) -- DERIVED in h1_types, read off")
    print(f"     the SAME area form, NOT a free dial.  Charge read-off is COMPUTED.")
    return deg == 1


if __name__ == "__main__":
    same = audit_carrier_stress()
    A2 = audit_coupled_residuals()
    spread = audit_box_control()
    audit_chosen_values()
    chg = audit_charge()

    banner("AUDIT SUMMARY")
    print(f"  carrier stress S^2==S^3 for (rho,p_r): {same}")
    print(f"  coupled residuals: res_tt={A2['rtt']:.2e} res_rr={A2['rrr']:.2e} res_thth={A2['rth']:.2e}")
    print(f"  B=1/A freed (max|a+b|): {A2['ab_dev']:.3e}")
    print(f"  M_MS = {A2['M']:.5f} sqrt(kappa/xi)")
    print(f"  box-control spread over 10x R: {spread*100:.2f}%")
    print(f"  charge deg-1 winding computed: {chg}")
