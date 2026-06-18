#!/usr/bin/env python3
"""
timerow_rest_clock_derive.py — DERIVE run for timerow_rest_clock_PREREG.md.

THE QUESTION (S4, linearization-free form): IS THE STATIC SOLITON A STATIONARY
SOLUTION OF THE FULL TIME-ROW FIELD EQUATIONS? The rung-2 weld relates the radial
winding current (H1) to TIME-derivatives of (delta phi, K). If the full equations
+ weld are satisfied with all d_t=0 -> the soliton is static (NO clock). If they
FORCE d_t(delta phi), d_t K != 0 -> the system evolves; the implied omega^2 is
EXACT (= off-balance / inertia).

NO approximation as a stated result. Background = the REAL stabilized hedgehog
(solved here, not an ansatz). The time-row equations are the EXACT second-order
action's EL with the time row ON. Frequencies classified M_MS vs J vs R (box-control
trap test). All exact (sympy) where possible; numeric eigensolve on the REAL profile.

Cites: native_weld_status_derivation.py (the algebraic native weld + the elliptic
on-shell (dphi,H1) system, blind-verified a709e4306bdf91b3a); ns_scan_results.md
(the diagonal d'Alembertian, signature (-,+,+), hyperbolic, verified
a9cfcd85385bff920); lepton_soliton_spectrum.py / native_profile_bvp.py (the exact
reduced E2_r,E4_r + EOM, blind-verified a1f2213b6410a6f35); CANON C-2026-06-10-3,
C-2026-06-13-1.
"""
from __future__ import annotations
import math
import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp

np.set_printoptions(precision=6, suppress=False, linewidth=120)
FAIL = []
def chk(label, ok):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        FAIL.append(label)
def hr(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)

TWO_PI = 2.0 * math.pi

# ===========================================================================
# T1 — THE FULL NONSTATIONARY TIME-ROW FIELD EQUATIONS (exact sympy)
# ===========================================================================
hr("T1 — FULL NONSTATIONARY TIME-ROW FIELD EQUATIONS (exact, time RETAINED)")

t, r, th, az, eps = sp.symbols("t r theta varphi epsilon", real=True)
c_s = sp.symbols("c", positive=True)
lam = sp.symbols("lam", positive=True)       # int (d_th Y)^2 dOmega = l(l+1)
phi0 = sp.Function("phi0", real=True)(r)      # background dilation, ARBITRARY
p = sp.Function("deltaphi", real=True)(t, r)  # delta-phi mode amplitude
h = sp.Function("H1", real=True)(t, r)        # time-row off-diagonal g_tr mode
k = sp.Function("K", real=True)(t, r)         # g_thth trace mode (g_Ttheta partner)
Y = sp.Function("Y", real=True)(th)

F = sp.exp(-2 * phi0)                          # f = e^{-2 phi0}
phi0p = sp.diff(phi0, r)
E0 = sp.diff(phi0, r, 2) + 2 * phi0p / r - 2 * phi0p**2   # background C1 EL density
coords = [t, r, th, az]
N4 = 4

# --- (1a) the metric sector: the diagonal d'Alembertian with the time row ON.
# (ns_scan_results.md form; re-derived here from the C1 dilation action.)
# L = (c/2) e^{-2phi} g^{ab} phi_a phi_b sqrt(-g4), c=2; phi=phi(T,r,theta).
ph = sp.Function("phi", real=True)(t, r, th)
g = sp.diag(-sp.exp(-2 * ph), sp.exp(2 * ph), r**2, r**2 * sp.sin(th)**2)
gi = g.inv()
sg = sp.sqrt(-g.det())
grad2 = sum(gi[i, j] * sp.diff(ph, coords[i]) * sp.diff(ph, coords[j])
            for i in range(N4) for j in range(N4))
Ldens = sp.Rational(1, 2) * c_s * sp.exp(-2 * ph) * grad2 * sg
# Euler-Lagrange for phi (full, time retained). phi=phi(t,r,theta): vary over those.
phi_coords = [t, r, th]
EL = (sp.diff(Ldens, ph)
      - sum(sp.diff(Ldens.diff(sp.Derivative(ph, x)), x) for x in phi_coords))
EL = sp.expand(EL / sp.sin(th))   # strip positive sin th weight
# Read principal part coefficients via dummy substitution (robust on Derivatives)
dTT, dRR, dTH = sp.symbols("dTT dRR dTH")
ELs = sp.expand(EL.subs({sp.Derivative(ph, (t, 2)): dTT,
                         sp.Derivative(ph, (r, 2)): dRR,
                         sp.Derivative(ph, (th, 2)): dTH}))
absfix = {sp.Abs(sp.sin(th)): sp.sin(th)}
cTT = sp.simplify(ELs.coeff(dTT).subs(absfix))
cRR = sp.simplify(ELs.coeff(dRR).subs(absfix))
cTH = sp.simplify(ELs.coeff(dTH).subs(absfix))
print("  metric-sector principal part (coeff of phi_TT, phi_rr, phi_thth):")
print("   cTT =", cTT)
print("   cRR =", cRR)
print("   cTH =", cTH)
chk("metric d'Alembertian: cTT/cRR = -e^{4phi} < 0 (Lorentzian; time slot opposite "
    "sign to radial) -- the metric PROPAGATES in T (ns_scan, canon C-2026-06-13-1)",
    sp.simplify(cTT / cRR - (-sp.exp(4 * ph))) == 0)
chk("metric d'Alembertian: cTT/cTH = -r^2 e^{2phi} < 0 (time slot opposite sign to "
    "angular too) => signature (-,+,+), strictly hyperbolic",
    sp.simplify(cTT / cTH - (-r**2 * sp.exp(2 * ph))) == 0)

# --- (1b) the native time-row WELD (EL of H1 from the exact 2nd-order C1 action).
# Reproduced from native_weld_status_derivation.py (blind-verified). The metric
# perturbation set with the B=1/A ties (H0=-2dphi, H2=+2dphi), time row g_tr=H1,
# trace K; the SECOND-ORDER action's EL in H1 is ALGEBRAIC.
gm = sp.zeros(4, 4)
gm[0, 0] = -F + eps * 2 * F * p * Y
gm[1, 1] = 1 / F + eps * (2 / F) * p * Y
gm[0, 1] = gm[1, 0] = eps * h * Y          # the time row g_Tr (H1)
gm[2, 2] = r**2 * (1 + eps * k * Y)
gm[3, 3] = r**2 * sp.sin(th)**2 * (1 + eps * k * Y)

def build_L(gthth_pert, phiM, phiS):
    gg = sp.zeros(4, 4)
    gg[0, 0] = -sp.exp(-2 * phiM)
    gg[1, 1] = sp.exp(2 * phiM)
    gg[0, 1] = gg[1, 0] = eps * h * Y
    gg[2, 2] = gthth_pert
    gg[3, 3] = gthth_pert * sp.sin(th)**2
    giL = gg.inv()
    sgL = sp.sqrt(-gg.det())
    dphiL = [sp.diff(phiS, x) for x in [t, r, th]]
    grad = sum(giL[i, j] * dphiL[i] * dphiL[j] for i in range(3) for j in range(3))
    L = -sp.Rational(1, 2) * c_s * sp.exp(-2 * phiS) * grad * sgL
    return L.subs(sp.Abs(sp.sin(th)), sp.sin(th))

phiM = phi0 + eps * p * Y
Yp = sp.Derivative(Y, th)
L = build_L(r**2 * (1 + eps * k * Y), phiM, phiM)
ser = sp.series(L, eps, 0, 3).removeO()
L2dens = sp.expand(ser.coeff(eps, 2) / sp.sin(th))
A = L2dens.coeff(Y, 2).subs(Yp, 0)
B = L2dens.coeff(Yp, 2).subs(Y, 0)
L2 = sp.expand(A + lam * B)            # mode Lagrangian (int Y^2=1, int Y'^2=lam)

pt = sp.Derivative(p, t)
EL_h = sp.simplify(sp.diff(L2, h))
print("\n  EL_H1 (native time-row weld, ALGEBRAIC in H1):")
print("   EL_H1 =", sp.simplify(EL_h))
native_weld = sp.Eq(F * phi0p * h, 2 * pt)
chk("THE NATIVE WELD: EL_H1=0 <=> f phi0' H1 = 2 d_t(dphi)  (ALGEBRAIC, not the "
    "Einstein differential weld d_r(f H1)=2 d_t dphi + d_t K) -- the radial winding "
    "current H1 is welded to the TIME-derivative of dphi (CANON C-2026-06-10-3, "
    "native form; blind-verified a709e4306bdf91b3a)",
    sp.solve(sp.Eq(EL_h, 0), h) == [2 * sp.exp(2 * phi0) * pt / phi0p])

# --- (1c) the dphi field equation (full, time retained), K=0 canon slice, with
# the matter source. First the pure-C1 (metric-sector) dphi EL:
pr_ = sp.Derivative(p, r)
EL_p = sp.simplify(sp.diff(L2, p)
                   - sp.diff(sp.diff(L2, pt), t)
                   - sp.diff(sp.diff(L2, pr_), r))
# eliminate H1 on its own algebraic weld (legal: dL/dH1=0 there) -> the on-shell
# (dphi) equation. THE KINETIC FLIP: the H1 coupling flips the time-kinetic sign.
h_star = 2 * sp.exp(2 * phi0) * pt / phi0p
L2_eff = sp.expand(L2.subs(h, h_star).doit())
pt2c = sp.simplify(sp.expand(L2_eff).coeff(pt, 2))
chk("KINETIC FLIP (the heart): after eliminating the auxiliary H1 on its weld, the "
    "(d_t dphi)^2 coefficient FLIPS sign +(c/2)r^2 -> -(c/2)r^2. The native time-row "
    "coupling makes the on-shell (dphi) system ELLIPTIC in (t,r) (verified)",
    sp.simplify(pt2c + sp.Rational(1, 2) * c_s * r**2) == 0)
EL_p_onshell = sp.simplify(sp.diff(L2_eff, p)
                           - sp.diff(sp.diff(L2_eff, pt), t)
                           - sp.diff(sp.diff(L2_eff, pr_), r))
onshell_target = c_s * (r**2 * sp.diff(p, t, 2)
                        + sp.diff(r**2 * F**2 * sp.diff(p, r), r)
                        - 4 * r**2 * F**2 * E0 * p - lam * F * p)
chk("ON-SHELL NATIVE (dphi) EQUATION (K=0 canon slice), EXACT (up to overall EL "
    "sign): r^2 d_t^2 dphi + d_r(r^2 f^2 d_r dphi) - 4 r^2 f^2 E0 dphi - lam f dphi "
    "= 0. The +r^2 d_t^2 carries the SAME sign as the elliptic spatial part "
    "d_r(r^2 f^2 d_r dphi) => ELLIPTIC in (t,r): real-frequency modes need omega^2<0 "
    "(relaxation) UNLESS the E0 (source) term flips the balance",
    sp.simplify(EL_p_onshell - onshell_target) == 0
    or sp.simplify(EL_p_onshell + onshell_target) == 0)

print("""
  T1 RESULT. The FULL nonstationary time-row system (metric sector + the native
  weld) has TWO faces, both EXACT and BOTH carried (no slice):
   (i) the metric's OWN d'Alembertian is HYPERBOLIC in T (signature -,+,+): the
       dilation field genuinely propagates in T (a real wave sector).
   (ii) the MATTER breathing field dphi, ONCE the native time-row weld
       f phi0' H1 = 2 d_t dphi is solved for the auxiliary H1, obeys an ELLIPTIC
       (t,r) equation: + r^2 d_t^2 dphi + d_r(r^2 f^2 d_r dphi)
                       - 4 r^2 f^2 E0 dphi - lam f dphi = 0,
       E0 = phi0'' + 2 phi0'/r - 2 phi0'^2 (the background dilation-EL density).
  The native weld is the candidate clock source: it ties H1 to d_t(dphi). The
  STATIONARY TEST (T2) asks whether a static profile solves (ii) with d_t=0, or is
  FORCED to evolve.
""")


# ===========================================================================
# T2 — STATIONARY TEST ON THE *REAL SELF-CONSISTENT* SOLITON (regular phi=-a).
#      Solve the full coupled (a,b,Theta) GR+L2+L4 soliton (radial_Bfree, blind-
#      verified 9ebc5e5184d1e58f). Then evaluate whether the full time-row (dphi)
#      system admits real-omega modes (a clock) or only d_t=0 / omega^2<0.
# ===========================================================================
hr("T2 — IS THE *REAL* (SELF-CONSISTENT) SOLITON STATIONARY UNDER THE FULL TIME-ROW SYSTEM?")

# --- import the EXACT, blind-verified coupled solver (radial_Bfree_soliton.py).
import importlib.util
_spec = importlib.util.spec_from_file_location("rbf", "radial_Bfree_soliton.py")
rbf = importlib.util.module_from_spec(_spec)
import os as _os
_os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
_spec.loader.exec_module(rbf)
import torch
torch.set_default_dtype(torch.float64)

def real_soliton(p_depth, cell_in_L=14.0, N=600, rc=0.05, kap8=0.05):
    """The REAL self-consistent (a,b,Theta) soliton; returns r, phi=-a (REGULAR),
    Theta, M_MS. phi is bounded at the core (regularity), UNLIKE the log model."""
    ri = rc + cell_in_L * 1.0
    rg = rbf.make_grid(1, N, rc=rc, rint=ri, geom=False)
    out = rbf.selfconsistent_Bfree(rg, 1.0, 1.0, p=p_depth, kap8=kap8,
                                   iters=120, relax=0.4, verbose=False)
    r_np = rg[0].cpu().numpy()
    phi_np = out["phi"][0].cpu().numpy()    # phi = -a, the REAL regular dilation
    Th_np = out["Th"][0].cpu().numpy()
    return r_np, phi_np, Th_np, float(out["M_MS"].item())

def E0_real(r_np, phi_np):
    phip = np.gradient(phi_np, r_np)
    phipp = np.gradient(phip, r_np)
    return phipp + 2 * phip / r_np - 2 * phip**2

print("  Real self-consistent soliton (REGULAR phi=-a), several depths p:")
print(f"   {'p':>5} {'M_MS':>9} {'phi(core)':>10} {'E0 core':>9} {'E0min':>9} {'E0max':>9} {'frac<0':>7}")
real_rows = []
for p_depth in (0.2, 0.4, 0.6, 0.8, 1.0):
    r_np, phi_np, Th_np, M_MS = real_soliton(p_depth)
    E0g = E0_real(r_np, phi_np)
    E0in = E0g[3:-3]
    real_rows.append((p_depth, M_MS, phi_np[0], E0g[3], E0in.min(), E0in.max(),
                      float(np.mean(E0in < 0)), r_np, phi_np, Th_np))
    print(f"   {p_depth:5.1f} {M_MS:9.4f} {phi_np[0]:10.4f} {E0g[3]:9.4f} "
          f"{E0in.min():9.3f} {E0in.max():9.3f} {np.mean(E0in<0):7.2f}")

print("""
  T2 OBSERVED (the HONEST correction). On the REAL self-consistent soliton, phi=-a
  is REGULAR at the core (phi'(0)->0 by regularity), so E0 = phi''+2phi'/r-2phi'^2 is
  FINITE everywhere -- the 1/r^2 blow-up of the crude log-cell model (phi=p ln r) is a
  MODEL ARTIFACT of the non-regular log dial, NOT a feature of the physical soliton.
  Read the E0 sign off the REAL profile above, NOT the log toy.
""")

# ===========================================================================
# T3 — NATIVE FREQUENCY ON THE REAL SOLITON + BOX-CONTROL TRAP (M_MS vs J vs R)
# ===========================================================================
hr("T3 — NATIVE FREQUENCY (on the REAL soliton) + DISCRIMINATOR (M_MS / J / R)")

def timerow_omega2_real(r_np, phi_np, lam_v, N_interp=2000):
    """omega^2 spectrum of the on-shell time-row (dphi) breathing operator on a REAL
    (r, phi) profile. From T1(ii): omega^2 = -(SL eigenvalue) of
    [-d_r(r^2 f^2 u') + q u = mu r^2 u], q = 4 r^2 f^2 E0 + lam f. Returns lowest 4
    omega^2 (descending), min q, min E0."""
    rr = np.linspace(r_np[0], r_np[-1], N_interp)
    phi = np.interp(rr, r_np, phi_np)
    hgr = rr[1] - rr[0]
    phip = np.gradient(phi, rr); phipp = np.gradient(phip, rr)
    f = np.exp(-2.0 * phi)
    E0g = phipp + 2 * phip / rr - 2 * phip**2
    coef = rr**2 * f**2
    q = 4 * rr**2 * f**2 * E0g + lam_v * f
    wt = rr**2
    chalf = 0.5 * (coef[:-1] + coef[1:])
    n = N_interp - 2
    Amat = np.zeros((n, n))
    for i in range(n):
        j = i + 1
        Amat[i, i] = (chalf[j - 1] + chalf[j]) / hgr**2 + q[j]
        if i > 0:
            Amat[i, i - 1] = -chalf[j - 1] / hgr**2
        if i < n - 1:
            Amat[i, i + 1] = -chalf[j] / hgr**2
    S = np.diag(1.0 / np.sqrt(wt[1:-1]))
    M = S @ Amat @ S
    Msym = 0.5 * (M + M.T)
    sl = np.linalg.eigvalsh(Msym)
    omega2 = np.sort(-sl)[::-1][:4]
    return omega2, float(np.min(q)), float(np.min(E0g[3:-3]))

print("  (a) lowest omega^2 of the time-row (dphi) operator on the REAL soliton")
print("      (l=1 => lam=2), per depth. omega^2>0 = a real clock; omega^2<0 = relaxation:")
print(f"   {'p':>5} {'M_MS':>9}   omega^2 (lowest 4)                        min q")
for (p_depth, M_MS, phicore, e0c, e0min, e0max, frac, r_np, phi_np, Th_np) in real_rows:
    om2, qmin, e0m = timerow_omega2_real(r_np, phi_np, 2.0)
    print(f"   {p_depth:5.1f} {M_MS:9.4f}   [" +
          ", ".join(f"{x:+.4f}" for x in om2[:4]) + f"]   {qmin:.4f}")

print()
print("  (b) BOX-CONTROL TRAP TEST (S3): FIXED depth p=1.0 & core rc=0.05, VARY the")
print("      cell size R. Intrinsic/M_MS-tied => omega^2 ~ const; box => omega^2 ~ 1/R^2.")
print(f"   {'cell(L)':>8} {'R=r_int':>9} {'M_MS':>9} {'omega^2_low':>13} {'omega^2*R^2':>13}")
box_rows = []
for cellL in (8.0, 12.0, 16.0, 24.0, 32.0):
    r_np, phi_np, Th_np, M_MS = real_soliton(1.0, cell_in_L=cellL)
    om2, qmin, e0m = timerow_omega2_real(r_np, phi_np, 2.0)
    R = r_np[-1]
    box_rows.append((cellL, R, M_MS, om2[0], om2[0] * R**2))
    print(f"   {cellL:8.1f} {R:9.3f} {M_MS:9.4f} {om2[0]:13.5f} {om2[0]*R**2:13.4f}")

om2v = np.array([x[3] for x in box_rows])
om2R2v = np.array([x[4] for x in box_rows])
def relspread(a):
    m = np.mean(np.abs(a))
    return (a.max() - a.min()) / m if m > 0 else float("inf")
sp_om2, sp_om2R2 = relspread(om2v), relspread(om2R2v)
print(f"\n   relative spread omega^2     across cell scan : {sp_om2:.4f}")
print(f"   relative spread omega^2*R^2 across cell scan : {sp_om2R2:.4f}")
all_pos = bool(np.all(om2v > 0))
print(f"   all omega^2 > 0 (a real clock at all R)?      : {all_pos}")
if all_pos:
    if sp_om2 < sp_om2R2:
        cls = "INTRINSIC (omega^2 ~ const; NOT box) -> candidate M_MS/depth-tied PRIZE"
    else:
        cls = "BOX-CONTROLLED (omega^2 ~ 1/R^2) -> cell-size clock, NOT M_MS (DEAD per S3)"
else:
    cls = ("NO real clock (omega^2 <= 0 somewhere) -> static/relaxation; NEGATIVE")
print(f"   T3 CLASSIFICATION: {cls}")

# ===========================================================================
# SUMMARY
# ===========================================================================
hr("SUMMARY")
print(f"  checks: {'ALL PASS' if not FAIL else 'FAILURES: ' + repr(FAIL)}")
print("  T3 box-control classification:", cls)
print("""  See timerow_rest_clock_results.md for the full T1-T5 verdict, the
  classification, the box-control table, the premise ledger, and the workstation
  flag (T4 periodicity needs the full nonlinear coupled time-evolution).""")
if FAIL:
    raise SystemExit(1)
