#!/usr/bin/env python3
# D1 -- native prediction formulas for M2 (prereg S1 D1; frozen menu S2). Exact sympy, CPU,
# float-free. SETTING (premise tags travel into every formula):
#   lock + areal anchor [THEORY, canon C-2026-08-06-1]: ds^2 = -A c^2 dt^2 + dr^2/A + r^2 dOmega^2
#   A(r) = e^{-2 phi};  observer at r=0 with phi(0)=0 => A(0)=1 [THEORY, observer normalization]
#   1+z = A^{-1/2} [THEORY, banked ratio identity];  d_L = (1+z)^2 r [banked convention,
#   Etherington-consistent with d_A = r; O2 row (g)]
# Ground: O2/O3 DERIVATION_NOTES.md CONSOLIDATED sections (cited; every used value RE-DERIVED here).
import sympy as sp

z = sp.Symbol('z', positive=True)
r = sp.Symbol('r', positive=True)
ell = sp.Symbol('ell', positive=True)
Rw = sp.Symbol('R_w', positive=True)
X = sp.Symbol('X', positive=True)
n = sp.Symbol('n', positive=True)
al = sp.Symbol('alpha', positive=True)

PASS = []
def check(name, cond):
    ok = bool(cond)
    PASS.append((name, ok))
    print(f"KEY {name} = {ok}")

def show(name, expr):
    print(f"KEY {name} = {expr}")

opz = 1 + z

# ---------------- frozen profile menu (prereg S2; F-SHOP) ----------------
A1 = (1 - r/Rw)**n            # P1 class (i),  domain r in [0, R_w)
A2 = sp.exp(-r/X)             # P2 class (ii), domain r in [0, oo)
A3 = (1 + r/X)**(-al)         # P3 class (ii'), domain r in [0, oo)
check("A_observer_normalization_all", all(a.subs(r, 0) == 1 for a in (A1, A2, A3)))

# ---------------- 1. inversion r(z) from 1+z = A^{-1/2} <=> A = (1+z)^{-2} ----------------
r1 = Rw*(1 - opz**(-2/n))
r2 = 2*X*sp.log(opz)
r3 = X*(opz**(2/al) - 1)
check("P1_inversion", sp.simplify(A1.subs(r, r1) - opz**-2) == 0)
check("P2_inversion", sp.simplify(A2.subs(r, r2) - opz**-2) == 0)
check("P3_inversion", sp.simplify(A3.subs(r, r3) - opz**-2) == 0)
show("r1_of_z", r1); show("r2_of_z", r2); show("r3_of_z", r3)

# d_L = (1+z)^2 r ; d_A = r ; mu = 5 log10 d_L + const
dL1 = opz**2 * r1
dL2 = opz**2 * r2
dL3 = opz**2 * r3
check("Etherington_dL_eq_opz2_dA_all",
      all(sp.simplify(dl - opz**2*rr) == 0 for dl, rr in ((dL1, r1), (dL2, r2), (dL3, r3))))
show("dL1_of_z", sp.expand(dL1)); show("dL2_of_z", dL2); show("dL3_of_z", sp.expand(dL3))

# ---------------- 2. cross-checks ----------------
# (a) P1 at n=1 reproduces the banked L form d_L = R_w z(z+2)
check("P1_n1_banked_dL_z_zplus2", sp.simplify(dL1.subs(n, 1) - Rw*z*(z + 2)) == 0)
# (b) monotonicity: dr/dz in manifestly-positive closed form, each profile
dr1 = sp.simplify(sp.diff(r1, z))
dr2 = sp.simplify(sp.diff(r2, z))
dr3 = sp.simplify(sp.diff(r3, z))
check("P1_drdz_closed_form", sp.simplify(dr1 - (2*Rw/n)*opz**(-2/n - 1)) == 0)
check("P2_drdz_closed_form", sp.simplify(dr2 - 2*X/opz) == 0)
check("P3_drdz_closed_form", sp.simplify(dr3 - (2*X/al)*opz**(2/al - 1)) == 0)
check("P1_drdz_positive", ((2*Rw/n)*opz**(-2/n - 1)).is_positive)
check("P2_drdz_positive", (2*X/opz).is_positive)
check("P3_drdz_positive", ((2*X/al)*opz**(2/al - 1)).is_positive)
# (c) z -> oo endpoint per O2/O3 verdicts: P1 -> R_w (wall at finite areal radius); P2, P3 -> oo
check("P1_r_limit_Rw", sp.limit(r1, z, sp.oo) == Rw)
check("P2_r_limit_oo", sp.limit(r2, z, sp.oo) == sp.oo)
check("P3_r_limit_oo", sp.limit(r3, z, sp.oo) == sp.oo)

# ---------------- low-z expansion and the degeneracy structure ----------------
# d_L(z) = 2*X_eff*z*(1 + c2*z + O(z^2)) with X_eff and c2 per profile:
s1 = sp.expand(sp.series(dL1, z, 0, 3).removeO())
s2 = sp.expand(sp.series(dL2, z, 0, 3).removeO())
s3 = sp.expand(sp.series(dL3, z, 0, 3).removeO())
Xeff1, Xeff2, Xeff3 = Rw/n, X, X/al
c2_1 = sp.Rational(3, 2) - 1/n
c2_2 = sp.Rational(3, 2)
c2_3 = sp.Rational(3, 2) + 1/al
check("P1_lowz_slope_2Rw_over_n", sp.simplify(s1.coeff(z, 1) - 2*Xeff1) == 0)
check("P2_lowz_slope_2X", sp.simplify(s2.coeff(z, 1) - 2*Xeff2) == 0)
check("P3_lowz_slope_2X_over_alpha", sp.simplify(s3.coeff(z, 1) - 2*Xeff3) == 0)
check("P1_lowz_curvature_c2", sp.simplify(s1.coeff(z, 2) - 2*Xeff1*c2_1) == 0)
check("P2_lowz_curvature_c2", sp.simplify(s2.coeff(z, 2) - 2*Xeff2*c2_2) == 0)
check("P3_lowz_curvature_c2", sp.simplify(s3.coeff(z, 2) - 2*Xeff3*c2_3) == 0)
# trichotomy: c2 < 3/2 (P1, any n>0); = 3/2 (P2); > 3/2 (P3, any alpha>0); disjoint ranges
check("c2_trichotomy_P1_below", (sp.Rational(3, 2) - c2_1).equals(1/n) and (1/n).is_positive)
check("c2_trichotomy_P3_above", (c2_3 - sp.Rational(3, 2)).equals(1/al) and (1/al).is_positive)
# P2 is the shared degenerate limit of both families (n -> oo, alpha -> oo)
check("c2_P1_limit_n_oo_is_P2", sp.limit(c2_1, n, sp.oo) == c2_2)
check("c2_P3_limit_alpha_oo_is_P2", sp.limit(c2_3, al, sp.oo) == c2_2)
# and profile-level: P1 -> P2 pointwise as n -> oo at fixed X_eff = R_w/n (exp as a power limit)
check("P1_profile_limit_n_oo_is_P2",
      sp.limit(A1.subs(Rw, n*X), n, sp.oo) == sp.exp(-r/X))
# mu(z) low-z: mu = 5 log10 z + 5 log10(2 X_eff) + (5/ln 10) c2 z + O(z^2) + const
lg1 = sp.series(sp.log(dL1 / (2*Xeff1*z)), z, 0, 2).removeO()
check("P1_mu_lowz_linear_term", sp.simplify(lg1.coeff(z, 1) - c2_1) == 0)
lg3 = sp.series(sp.log(dL3 / (2*Xeff3*z)), z, 0, 2).removeO()
check("P3_mu_lowz_linear_term", sp.simplify(lg3.coeff(z, 1) - c2_3) == 0)

# ---------------- 3. transverse BAO projection ----------------
# GEOMETRY (one line, no cosmology): in ds^2 the transverse proper length of an arc of
# coordinate angle theta at areal radius r is  integral r dphi = r*theta  (from the r^2 dOmega^2
# term) => an object of proper transverse length ell at r subtends theta = ell/r.
# [P-STATIC-RULER premise tag: ell = one native proper length, free nuisance]
th1 = ell/r1
th2 = ell/r2
th3 = ell/r3
show("thetaBAO_P1", th1); show("thetaBAO_P2", th2); show("thetaBAO_P3", th3)
# low-z: theta ~ ell/(2*X_eff*z) for every profile (same X_eff degeneracy as d_L)
check("thetaBAO_P1_lowz", sp.limit(th1*z, z, 0) == ell/(2*Xeff1))
check("thetaBAO_P2_lowz", sp.limit(th2*z, z, 0) == ell/(2*Xeff2))
check("thetaBAO_P3_lowz", sp.limit(th3*z, z, 0) == ell/(2*Xeff3))
# P1 signature: a MINIMAL angle ell/R_w as z -> oo (d_A = r -> R_w finite; O2 annotation,
# re-derived); P2/P3: theta -> 0
check("thetaBAO_P1_floor_ell_over_Rw", sp.limit(th1, z, sp.oo) == ell/Rw)
check("thetaBAO_P2_to_zero", sp.limit(th2, z, sp.oo) == 0)
check("thetaBAO_P3_to_zero", sp.limit(th3, z, sp.oo) == 0)

# ---------------- 4. radial BAO projection ----------------
# Ruler tag [REALIZATION premise, prereg S4]: the ruler is PROPER length in the realized
# metric, dl_p = A^{-1/2} dr (physical rods measure proper length). This is NOT the kernel's
# 'spatial' choice, which stays no-pin (CP2 standing).
# General identity, any A(r): with 1+z = A^{-1/2} and depth delta = phi = -ln(A)/2,
#   dz/dl_p = (1+z) * ddelta/dl_p = -A'/(2A)   (exact)
Af = sp.Function('A', positive=True)(r)
z_of_r = Af**sp.Rational(-1, 2) - 1
delta_of_r = -sp.log(Af)/2
dz_dlp = sp.diff(z_of_r, r) / Af**sp.Rational(-1, 2)      # (dz/dr) / (dl_p/dr)
ddelta_dlp = sp.diff(delta_of_r, r) / Af**sp.Rational(-1, 2)
check("radial_identity_dz_dlp_eq_opz_ddelta_dlp",
      sp.simplify(dz_dlp - (1 + z_of_r)*ddelta_dlp) == 0)
check("radial_dz_dlp_closed_form",
      sp.simplify(dz_dlp - (-sp.diff(Af, r)/(2*Af))) == 0)
# note: dz/dl_p = -A'/(2A) = ddelta/dr exactly (redshift-per-proper-length = depth-per-areal-r)
check("radial_dz_dlp_eq_ddelta_dr", sp.simplify(dz_dlp - sp.diff(delta_of_r, r)) == 0)
# per profile: Delta z_BAO(z; ell) = ell * (-A'/(2A)) evaluated at r(z)
Dz1 = sp.simplify((ell*(-sp.diff(A1, r)/(2*A1))).subs(r, r1))
Dz2 = sp.simplify((ell*(-sp.diff(A2, r)/(2*A2))).subs(r, r2))
Dz3 = sp.simplify((ell*(-sp.diff(A3, r)/(2*A3))).subs(r, r3))
check("DzBAO_P1_closed_form", sp.simplify(Dz1 - ell*n/(2*Rw)*opz**(2/n)) == 0)
check("DzBAO_P2_closed_form", sp.simplify(Dz2 - ell/(2*X)) == 0)
check("DzBAO_P3_closed_form", sp.simplify(Dz3 - ell*al/(2*X)*opz**(-2/al)) == 0)
show("DzBAO_P1", ell*n/(2*Rw)*opz**(2/n))
show("DzBAO_P2", ell/(2*X))
show("DzBAO_P3", ell*al/(2*X)*opz**(-2/al))
# z-trend trichotomy (same three-way split as c2): P1 GROWS, P2 CONSTANT, P3 DECAYS
check("DzBAO_P1_increasing", sp.diff(ell*n/(2*Rw)*opz**(2/n), z).is_positive)
check("DzBAO_P2_constant", sp.diff(Dz2, z) == 0)
check("DzBAO_P3_decreasing", sp.diff(ell*al/(2*X)*opz**(-2/al), z).is_negative)
# low-z: Delta z -> ell/(2*X_eff) for every profile (the same X_eff again)
check("DzBAO_lowz_Xeff_all",
      all(sp.limit(D, z, 0) == ell/(2*Xe)
          for D, Xe in ((Dz1, Xeff1), (Dz2, Xeff2), (Dz3, Xeff3))))

# ---------------- 5. scale-translation table (P1 wall in each O2 measure; c0 = 1) ----------------
# Re-derived integrals; must match O2 CONSOLIDATED (proper 2R_w/(2-n) for n<2; optical
# R_w/(1-n) for n<1; divergent otherwise). Areal wall = R_w by construction.
# proper: int_0^{R_w} A^{-1/2} dr with n = 2 - m, m > 0  (i.e. n < 2)
mpos = sp.Symbol('m', positive=True)
Fp = sp.integrate((1 - r/Rw)**(-(2 - mpos)/2), r)          # antiderivative
Ip = sp.limit(Fp, r, Rw, '-') - Fp.subs(r, 0)
check("P1_proper_wall_2Rw_over_2minusn",
      sp.simplify(Ip - 2*Rw/mpos) == 0)                     # m = 2-n  =>  2R_w/(2-n)
check("P1_proper_witness_n_half", sp.integrate((1 - r/Rw)**(-sp.Rational(1, 4)),
      (r, 0, Rw)) == sp.Rational(4, 3)*Rw)
check("P1_proper_witness_n1_2Rw", sp.integrate((1 - r/Rw)**(-sp.Rational(1, 2)),
      (r, 0, Rw)) == 2*Rw)
# n=2 (and optical n=1) integrand is (1-r/R_w)^{-1}: verify divergence via the manifestly
# real antiderivative G = -R_w ln(1-r/R_w) (sympy's definite form emits a complex-log artifact)
G = -Rw*sp.log(1 - r/Rw)
check("P1_log_antiderivative_exact", sp.simplify(sp.diff(G, r) - 1/(1 - r/Rw)) == 0)
check("P1_proper_witness_n2_divergent",
      G.subs(r, 0) == 0 and sp.limit(G, r, Rw, '-') == sp.oo)
# optical: int_0^{R_w} A^{-1} dr with n = 1 - k, k > 0  (i.e. n < 1)
kpos = sp.Symbol('k', positive=True)
Fo = sp.integrate((1 - r/Rw)**(-(1 - kpos)), r)
Io = sp.limit(Fo, r, Rw, '-') - Fo.subs(r, 0)
check("P1_optical_wall_Rw_over_1minusn",
      sp.simplify(Io - Rw/kpos) == 0)                       # k = 1-n  =>  R_w/(1-n)
check("P1_optical_witness_n_half_2Rw", sp.integrate((1 - r/Rw)**(-sp.Rational(1, 2)),
      (r, 0, Rw)) == 2*Rw)
check("P1_optical_witness_n1_divergent",
      G.subs(r, 0) == 0 and sp.limit(G, r, Rw, '-') == sp.oo)  # same integrand as proper n=2

# ---------------- summary ----------------
nfail = [nm for nm, ok in PASS if not ok]
print(f"CHECK_COUNT = {len(PASS)}")
print(f"ALL_CHECKS_PASS = {not nfail}")
if nfail:
    print("FAILED:", nfail)
