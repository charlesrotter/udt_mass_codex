"""PART 3: the nonstationary-source reading — the source as phi's own
ell=1 angular activity, time-dependent, within the rotation-closed
ell<=1 class  f(t,y,theta) = F(t,y) + a(t,y) cos(theta).

Exact reduced C1 Lagrangian in the class (c = 2 throughout, FULL-sphere
normalization, explicit bookkeeping):

  L(y) = int dOmega [ (c/8) y^2 f_t^2/f^2  -  (c/8) y^2 f_y^2
                      - (c/8) f_th^2 / f ]
       = T(F,a,Fdot,adot) - (c/8) y^2 2pi (2 F'^2 + (2/3) a'^2) - Q(F,a)

(the three weights are EXACT consequences of the UDT tie: the t-slot
weight e^{-2phi} g^{tt} sqrt(-g) = -y^2 sin th is phi-FREE, the r-slot
weight is f-free, the angular slot carries 1/f).

Then: harmonic forcing delta a ~ e^{i omega t} driven by delta F; the
induced static kernel on delta F is the frequency-domain Schur
complement; its f^n character n_eff(omega) is computed exactly.
"""
import sys
import numpy as np
import sympy as sp

FAIL = []
def check(label, ok):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok: FAIL.append(label)

u_, kap = sp.symbols("u kappa", real=True)
F0, a0, y = sp.symbols("F a y", positive=True)
om, q = sp.symbols("omega q", positive=True)
c2 = 2  # c = 2 (repo normalization)

print("=" * 72)
print("C0 — exact reduced potential and kinetic matrix in the class")
print("=" * 72)
# angular potential: Q(F,a) = int (c/8) f_th^2 / f dOmega,
# f_th^2 = a^2 sin^2 th = a^2 (1-u^2)
Qpot = sp.integrate(sp.Rational(c2, 8) * a0**2 * (1 - u_**2)
                    / (F0 + a0 * u_) * 2 * sp.pi, (u_, -1, 1))
Qpot = sp.simplify(Qpot)
# record's P(F,a) = (3a^2/2F) G1(kappa), kappa = a/F
L_log = sp.log((1 + kap) / (1 - kap))
G1 = (2 * kap + (kap**2 - 1) * L_log) / kap**3
P_rec = (3 * a0**2 / (2 * F0)) * G1.subs(kap, a0 / F0)
ratio = sp.simplify(Qpot / P_rec)
ratio_num = complex(ratio.subs({F0: 1.3, a0: 0.51}).evalf())
check("exact Q(F,a) closed form found; Q / P_record is a pure constant "
      f"= pi/3 (numeric: {ratio_num.real:.12f}; record P verified up to "
      "one global normalization constant)",
      abs(ratio_num.real - np.pi / 3) < 1e-12
      and abs(complex(ratio.subs({F0: 0.7, a0: 0.69}).evalf()).real
              - np.pi / 3) < 1e-12)

# degree-1 homogeneity and the exact rank-1 Hessian identity (any kappa)
mu_ = sp.symbols("mu_", positive=True)
check("Q(mu F, mu a) = mu Q(F,a) exactly (degree-1 homogeneity in the "
      "class, ALL amplitudes)",
      sp.simplify(Qpot.subs({F0: mu_ * F0, a0: mu_ * a0}) - mu_ * Qpot)
      == 0)
Q_FF = sp.diff(Qpot, F0, 2)
Q_aa = sp.diff(Qpot, a0, 2)
Q_Fa = sp.diff(Qpot, F0, a0)
rank1 = sp.simplify(Q_FF * Q_aa - Q_Fa**2)
check("EXACT RANK-1 HESSIAN: Q_FF Q_aa - Q_Fa^2 == 0 identically (all "
      "F, a) — the record's identity re-derived on the exact potential",
      rank1 == 0)

# kinetic matrix: T = (c/8) y^2 int f_t^2/f^2 dOmega
#   = (1/2)[Fdot^2 M_FF + 2 Fdot adot M_Fa + adot^2 M_aa]
I0 = sp.integrate(2 * sp.pi / (F0 + a0 * u_)**2, (u_, -1, 1))
I1 = sp.integrate(2 * sp.pi * u_ / (F0 + a0 * u_)**2, (u_, -1, 1))
I2 = sp.integrate(2 * sp.pi * u_**2 / (F0 + a0 * u_)**2, (u_, -1, 1))
M_FF = sp.simplify(sp.Rational(c2, 4) * y**2 * I0)
M_Fa = sp.simplify(sp.Rational(c2, 4) * y**2 * I1)
M_aa = sp.simplify(sp.Rational(c2, 4) * y**2 * I2)
check("kinetic matrix closed forms exist; M_FF(a -> 0) = 2 pi y^2/F^2 "
      "(the monopole breathing kinetic = the weld's (1/2) y^2 dphi_t^2 "
      "per solid angle x 4pi, under dphi = -dF/2F)",
      sp.simplify(sp.limit(M_FF, a0, 0) - 2 * sp.pi * y**2 / F0**2) == 0)
check("M_Fa(a -> 0) = 0 and M_aa(a -> 0) = (2 pi/3) y^2/F^2 — the "
      "ell = 0/ell = 1 kinetic block-diagonality at zero amplitude",
      sp.simplify(sp.limit(M_Fa, a0, 0)) == 0
      and sp.simplify(sp.limit(M_aa, a0, 0)
                      - 2 * sp.pi * y**2 / (3 * F0**2)) == 0)

# the free ell=1 oscillation frequency at zero amplitude
om0_sq = sp.simplify(sp.limit(Q_aa, a0, 0) / sp.limit(M_aa, a0, 0))
check("free angular frequency omega_0^2 = Q_aa/M_aa |_{a->0} = 2F/y^2 "
      "= lam f0/y^2 with lam = 2 (ell = 1) — EXACTLY the weld "
      "operator's angular dispersion (independent cross-check of the "
      "two routes)", sp.simplify(om0_sq - 2 * F0 / y**2) == 0)

print()
print("=" * 72)
print("C1 — the frequency-domain Schur kernel (the induced second jet)")
print("=" * 72)
# Exact statement (pointwise / collar-local; radial gradients of the
# response dropped — caveat recorded):
#   K_ind(om) = [Q_FF - om^2 dM_FF] - (Q_Fa - om^2 M_Fa)^2/(Q_aa - om^2 M_aa)
# where dM_FF = M_FF(a) - M_FF(0) is the angular EXCESS of the monopole
# kinetic (the a-independent part already lives in the radial sector).
dM_FF = sp.simplify(M_FF - 2 * sp.pi * y**2 / F0**2)
K_ind = sp.simplify((Q_FF - om**2 * dM_FF)
                    - (Q_Fa - om**2 * M_Fa)**2 / (Q_aa - om**2 * M_aa))

# (i) the omega -> 0 theorem, ALL amplitudes:
check("THEOREM (omega -> 0): K_ind(0) = Q_FF - Q_Fa^2/Q_aa = 0 EXACTLY "
      "at EVERY amplitude (rank-1) — the quasi-static responsive source "
      "induces ZERO second jet: the phi-slot n = 0, now DERIVED as the "
      "omega -> 0 character of the nonstationary source",
      sp.simplify(K_ind.subs(om, 0)) == 0)

# (ii) small-amplitude closed form: K_ind = -(4pi/3)(a^2/F^3) W^2/(1-W),
#      W = omega^2/omega_0^2
W = sp.symbols("W", positive=True)
K_small = sp.series(K_ind.subs(om, sp.sqrt(W * 2 * F0 / y**2)),
                    a0, 0, 3).removeO()
K_small = sp.simplify(sp.expand(K_small))
K_target = -(4 * sp.pi / 3) * (a0**2 / F0**3) * W**2 / (1 - W)
check("small-amplitude closed form: K_ind(omega) = -(4 pi/3)(a0^2/F^3) "
      "W^2/(1 - W),  W = omega^2/omega_0^2 — note W^2, not W: the O(W) "
      "pieces of the kinetic excess and the cross-block cancel EXACTLY",
      sp.simplify(K_small - K_target) == 0)

# (iii) the induced slot exponent: match against the f^n family's jet.
#  f^n family, per-solid-angle LAGRANGIAN jet (Part A, verified):
#    +2 n s f0^2 dphi^2   =>  full sphere:  8 pi n s f0^2 dphi^2.
#  Induced full-sphere Lagrangian jet from the Schur elimination:
#    -(1/2) K_ind dF^2,  dF = -2 F dphi  =>  -2 K_ind F^2 dphi^2.
#  Equate (F = f0 on the collar):  n_eff = -K_ind / (4 pi s).
s_ = q * (1 - q) / 2
n_eff = sp.simplify(-K_target / (4 * sp.pi * s_))
n_eff_target = (a0**2 / (3 * s_ * F0**3)) * W**2 / (1 - W)
check("induced slot exponent: n_eff(omega) = (a0^2/(3 s F^3)) "
      "W^2/(1-W) = (kappa0^2/(3 s F)) W^2/(1-W) — exact "
      "small-amplitude form (matching factor: n_eff = -K_ind/(4 pi s))",
      sp.simplify(n_eff - n_eff_target) == 0)
n_eff_kappa = sp.simplify(n_eff.subs(a0, kap * F0))
print(f"      n_eff(omega) = {sp.simplify(n_eff_kappa)}")
check("n_eff in kappa-form: n_eff = (kappa0^2 /(3 s F)) W^2/(1 - W) "
      "(F = f0(y) = y^-q on the collar)",
      sp.simplify(n_eff_kappa - kap**2 * W**2
                  / (3 * s_ * F0 * (1 - W))) == 0)

print("""
      CHARACTER MAP (exact, small amplitude, pointwise):
        W = omega^2/omega_0^2,  omega_0^2 = lam f0/y^2 (lam = 2):
        omega -> 0 :  n_eff -> 0   (PHI-SLOT; quadratic in omega^2)
        0 < W < 1  :  n_eff > 0    (toward and past the f-slot n = 1)
        W -> 1-    :  n_eff -> +oo (ell = 1 resonance)
        W > 1      :  n_eff < 0    (activation-like; n = -1 reachable)
      BUT n_eff is y-UNIFORM only at omega = 0 (W = omega^2 y^2/(2F)
      and kappa0^2/(s F) are y-dependent on the collar at any fixed
      omega =/= 0): the f^n SLOT FAMILY itself forces the quasi-static
      character —
        responsive reading + constant-n completion  ==>  n = 0.""")

print()
print("=" * 72)
print("C2 — numeric verification (exact-kappa Schur vs closed form; "
      "finite-amplitude check at the record's demanded kappa)")
print("=" * 72)
subs_num = {F0: 1.0, y: 1.0, q: sp.Rational(1, 3)}
om0n = float(sp.sqrt(om0_sq.subs(subs_num).subs(a0, 1e-6)))
Kfun = sp.lambdify((a0, F0, y, om), K_ind, "numpy")
for kk, Wn in [(0.05, 0.25), (0.05, 0.5), (0.05, 4.0)]:
    omn = np.sqrt(Wn) * np.sqrt(2.0)
    Kn = Kfun(kk, 1.0, 1.0, omn)
    Kt = -(4 * np.pi / 3) * kk**2 * Wn**2 / (1 - Wn)
    check(f"exact-kappa kernel vs closed form at kappa = {kk}, W = {Wn}:"
          f"  K_exact = {Kn:+.6e}, K_smallamp = {Kt:+.6e} "
          f"(rel. dev. {abs(Kn/Kt-1):.3e} = O(kappa^2))",
          abs(Kn / Kt - 1) < 0.05)
# the record's corrected demanded amplitude kappa(1) = 0.683095:
# K_ind(0) = 0 must hold EXACTLY there too (rank-1 is all-amplitude)
Kn0 = Kfun(0.683095, 1.0, 1.0, 1e-8)
check(f"K_ind(omega -> 0) = {Kn0:+.3e} at the demanded kappa = "
      "0.683095 — the phi-slot theorem holds at FINITE amplitude "
      "(not a small-kappa artifact)", abs(Kn0) < 1e-10)
# finite-kappa resonance shift: the pole of K_ind sits at
# Q_aa - om^2 M_aa = 0 evaluated at finite kappa
om_res_sq = sp.simplify(Q_aa / M_aa).subs(subs_num)
res_num = float(om_res_sq.subs(a0, 0.683095))
check(f"finite-amplitude resonance: omega_res^2 = {res_num:.6f} at "
      f"kappa = 0.683 vs 2.0 at kappa -> 0 — the pole shifts but the "
      "W^2-suppressed omega -> 0 zero is amplitude-independent",
      res_num > 0)

print()
print("=" * 72)
if FAIL:
    print(f"{len(FAIL)} FAILED"); [print("  -", x) for x in FAIL]
    sys.exit(1)
print("ALL CHECKS PASSED (nonstationary responsive source)")
