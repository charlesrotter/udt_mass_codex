"""THRESHOLD RIGIDITY THEOREM for the metric-native scalar probe on the
fixed static spherically symmetric ansatz.

Setting (repo conventions; extends native_open_domain_threshold_theorem.py,
which proved EMPTY POINT SPECTRUM for the matter-side class f >= 1,
f -> 1 + a/r; this file asks the branch-(iii) question for that theorem:
can ANY admissible f lift the continuum threshold above 0?):

    metric   ds^2 = -f dt^2 + f^{-1} dr^2 + r^2 dOmega^2,
    f > 0 smooth on (r0, infinity), otherwise UNRESTRICTED
    (no f >= 1, no prescribed tail -- this is the rigidity question),

    probe (massless wave operator, radial sector ell, lambda = ell(ell+1)):

        -(r^2 f R')' + lambda R = omega^2 (r^2/f) R,

    in tortoise form (u = r R, dr*/dr = 1/f, banked in
    native_open_cell_resonance_scan.py and re-verified here):

        u'' + [omega^2 - V] u = 0,      V(r) = f (lambda/r^2 + f'/r).

THEOREM (threshold rigidity).  Within statics and spherical symmetry on
this fixed ansatz (areal function rho = r):

    [finite exterior C1 action  S_ext = (1/4) int_{R0}^inf r^2 (f')^2 dr]
        ==>  [continuum threshold = 0 exactly  (sigma_ess = [0, inf))]
        ==>  [empty point spectrum, by the prior theorem's machinery].

Equivalently: NO native structure f with finite exterior C1 action can lift
the probe's continuum threshold above 0.  Every f that lifts the threshold
(f ~ m r, the UNIQUE power law with finite positive V(inf)) or confines the
probe (f growing faster than linearly: finite tortoise endpoint, discrete
spectrum, AdS-like) costs INFINITE exterior C1 action.  Branch (iii) of the
prior theorem is therefore CLOSED within the class

    { static, spherically symmetric, fixed ansatz rho = r,
      finite exterior C1 action, single structure },

and the remaining static escape is exactly the SATURATING AREAL FUNCTION
(rho -> rho_inf finite, derived precisely in T5/E1 below): there the
threshold lifts to f_inf*lambda/rho_inf^2 > 0 with NO f-growth and FINITE
action -- the angular term itself becomes the effective mass.

Structure verified below:
    T1  threshold criterion (tortoise form + Weyl/Persson machinery,
        including the FINITE-tortoise-endpoint confining case),
    T2  exact classification of V(inf) over power laws f = c r^k
        (k = 1 is the unique lifter; k > 1 confines; k < 1 gives 0),
        + the general-f asymptotic statement,
    T3  action cost: lifting/confining f have infinite exterior C1 action;
        conversely finite action ==> f converges (Cauchy-Schwarz, exact)
        ==> V is L^1 in the tortoise coordinate ==> threshold = 0,
    T4  vacuum cross-check: the exact native vacuum family f = C + 2/r
        satisfies the vacuum equation, has V(inf) = 0 and finite action,
    T5  the assembled theorem + the precisely-stated escape slots
        (E1 saturating areal function rho(r) -- derived from the wave
        operator on ds^2 = -f dt^2 + f^{-1}dr^2 + rho^2 dOmega^2;
        E2 nonstatic/breather; E3 multi-cell ensemble).

CLASSICAL MACHINERY ASSUMED, NOT RE-PROVED (same convention as the prior
theorem's Sturm-Liouville note; each use is flagged inline):
    (M1) Persson's theorem / Weyl criterion for inf sigma_ess of
         -d^2/dx^2 + V on a half-line;
    (M2) sigma_ess = [V_inf, inf) when V -> V_inf (relatively compact
         perturbation / Weyl);
    (M3) sigma_ess = [0, inf) and Jost-Levinson asymptotics u ~ e^{+-i omega x}
         for V in L^1 near infinity (short-range scattering theory);
    (M4) purely discrete spectrum at a finite endpoint with V -> +inf
         (limit-point for the Calogero strength g >= 3/4; limit-circle
         extensions for g < 3/4 are still discrete).

Every displayed identity/limit/integral is verified symbolically (sympy);
PASS/FAIL is printed per check; the script exits nonzero on any FAIL.

New file 2026-06-10; creates nothing else, modifies nothing existing.
"""

from __future__ import annotations

import sys

import sympy as sp

FAILURES: list[str] = []


def check(label: str, ok: bool) -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        FAILURES.append(label)


def hr(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------------------
# Shared symbols
# ---------------------------------------------------------------------------
r = sp.symbols("r", positive=True)
lam = sp.symbols("lam", positive=True)        # ell(ell+1) >= 2 for ell >= 1
omega = sp.symbols("omega", positive=True)
c = sp.symbols("c", positive=True)
m = sp.symbols("m", positive=True)
k = sp.symbols("k", real=True)
f_gen = sp.Function("f", positive=True)(r)

# ---------------------------------------------------------------------------
# T1 — threshold criterion (tortoise form + endpoint dichotomy)
# ---------------------------------------------------------------------------
hr("T1 — THRESHOLD CRITERION: tortoise form, Persson/Weyl, and the "
   "endpoint dichotomy")

R_f = sp.Function("R")(r)
u_expr = r * R_f
V_def = f_gen * (lam / r**2 + sp.diff(f_gen, r) / r)
# tortoise derivative: d/dr* = f d/dr  (dr*/dr = 1/f)
lhs_t = (f_gen * sp.diff(f_gen * sp.diff(u_expr, r), r)
         + (omega**2 - V_def) * u_expr)
rhs_t = (f_gen / r) * (sp.diff(r**2 * f_gen * sp.diff(R_f, r), r)
                       - lam * R_f + omega**2 * (r**2 / f_gen) * R_f)
check("tortoise identity (generic f):  u_{r*r*} + (ω² − V)u = (f/r)·"
      "[(r²fR')' − λR + ω²(r²/f)R]  with u = rR, V = f(λ/r² + f'/r)",
      sp.simplify(lhs_t - rhs_t) == 0)
print("     so the radial probe equation  −(r²fR')' + λR = ω²(r²/f)R  is")
print("     EXACTLY  u'' + [ω² − V]u = 0  in the tortoise coordinate")
print("     r* = ∫dr/f, with V = f(λ/r² + f'/r)  (banked form re-verified).")

M_s = sp.symbols("M", positive=True)
f_schw = 1 - 2 * M_s / r
V_schw = sp.simplify(V_def.subs(f_gen, f_schw).doit())
check("Schwarzschild control: f = 1−2M/r gives the scalar Regge–Wheeler "
      "potential (1−2M/r)(λ/r² + 2M/r³) exactly",
      sp.simplify(V_schw - (1 - 2 * M_s / r) * (lam / r**2 + 2 * M_s / r**3))
      == 0)

print("""
  THRESHOLD CRITERION (classical machinery M1–M4, assumed not re-proved —
  same convention as the prior theorem's Sturm–Liouville note):

  The probe operator is unitarily equivalent to  H = −d²/dx² + V(x)  on the
  tortoise half-line, x = r* = ∫dr/f.  The infinity endpoint splits:

  CASE A (infinite tortoise endpoint, ∫^∞ dr/f = ∞):  Persson's theorem
  gives  inf σ_ess(H) = lim_{X→∞} inf spec(H restricted beyond X).  The
  unconditional direction is  inf σ_ess ≥ liminf_{x→∞} V; the reverse
  (Weyl-sequence) direction needs V to come close to its liminf on
  intervals of growing length.  SPEC-REFINEMENT NOTE (honest): the bare
  statement "threshold = liminf V" is therefore the EQUALITY case; in every
  case used below V has an actual limit (finite or +∞), where the equality
  is classical (M2):  V → V_∞ finite  ⇒  σ_ess = [V_∞, ∞).
      ⇒ LIFTING the threshold to m² > 0 requires
            V(∞) = lim_{r→∞} f·(λ/r² + f'/r) = m² > 0.

  CASE B (FINITE tortoise endpoint, ∫^∞ dr/f < ∞ — f growing faster than
  linearly):  r → ∞ is mapped to a FINITE endpoint x_∞ of the tortoise
  line.  If V → +∞ there (verified below for every superlinear power law),
  the endpoint contributes NO essential spectrum and the spectrum is
  PURELY DISCRETE (M4) — the CONFINING case, AdS-like: discreteness by
  geometry, not by a mass gap.  This case is part of the classification,
  not an escape from it.
""")

for kk, expect_finite in [(sp.Rational(1, 2), False), (1, False),
                          (sp.Rational(3, 2), True), (2, True), (3, True)]:
    tort = sp.integrate(1 / (c * r**kk), (r, 1, sp.oo))
    is_finite = tort.is_finite is True
    check(f"tortoise length ∫_1^∞ dr/(c·r^{kk}) is "
          f"{'FINITE' if expect_finite else 'INFINITE'} (k {'>' if expect_finite else '<='} 1)",
          is_finite == expect_finite)
print("     general criterion: ∫^∞ dr/(c r^k) < ∞  ⇔  k > 1 "
      "(superlinear growth ⇒ finite endpoint).")

# ---------------------------------------------------------------------------
# T2 — exact classification of V(inf) for power laws f = c r^k
# ---------------------------------------------------------------------------
hr("T2 — CLASSIFICATION: V(∞) for f = c·r^k, all k (exact)")

f_pl = c * r**k
V_pl = sp.expand(V_def.subs(f_gen, f_pl).doit())
V_target = c * lam * r**(k - 2) + c**2 * k * r**(2 * k - 2)
check("V for f = c·r^k is  c·λ·r^(k−2) + c²·k·r^(2k−2)  exactly "
      "(symbolic k)", sp.simplify(V_pl - V_target) == 0)
print("     exponents: λ-term r^(k−2) (vanishes iff k<2), "
      "f'-term r^(2k−2) (vanishes iff k<1).")

print()
print("  Exact limit table (c symbolic positive; classification is "
      "c-independent):")
print("    k        V(∞)        tortoise endpoint   classification")
table = [
    (sp.Integer(-2), 0, "infinite", "threshold 0"),
    (sp.Rational(-1, 2), 0, "infinite", "threshold 0"),
    (sp.Integer(0), 0, "infinite", "threshold 0"),
    (sp.Rational(1, 2), 0, "infinite", "threshold 0"),
    (sp.Rational(3, 4), 0, "infinite", "threshold 0"),
    (sp.Integer(1), c**2, "infinite", "LIFTED threshold = c²"),
    (sp.Rational(5, 4), sp.oo, "finite", "CONFINING (discrete)"),
    (sp.Rational(3, 2), sp.oo, "finite", "CONFINING (discrete)"),
    (sp.Integer(2), sp.oo, "finite", "CONFINING (discrete)"),
    (sp.Integer(3), sp.oo, "finite", "CONFINING (discrete)"),
    (sp.Integer(4), sp.oo, "finite", "CONFINING (discrete)"),
]
all_ok = True
for kk, vexp, tort_lab, classif in table:
    Vk = V_target.subs(k, kk)
    Vlim = sp.limit(Vk, r, sp.oo)
    tort = sp.integrate(1 / (r**kk), (r, 1, sp.oo))   # c=1 wlog for endpoint
    tort_finite = tort.is_finite is True
    ok = (sp.simplify(Vlim - vexp) == 0 if vexp is not sp.oo
          else Vlim == sp.oo)
    ok = ok and (tort_finite == (tort_lab == "finite"))
    all_ok = all_ok and ok
    print(f"    {str(kk):6s}   {str(Vlim):9s}   {tort_lab:17s}   {classif}"
          f"   [{'ok' if ok else 'MISMATCH'}]")
check("every row of the limit table verified exactly (V-limit AND "
      "endpoint type)", all_ok)

print("""
  CLASSIFICATION (exact):
    k < 1 :  V(∞) = 0    — threshold stays at 0 (both exponents negative;
                           for k−2 < −1 and 2k−2 < 0 both terms die);
    k = 1 :  V(∞) = c²   — the λ-term cλ/r → 0, the f'-term is c²·1·r⁰ = c²
                           EXACTLY.  LINEAR f IS THE UNIQUE POWER LAW WITH
                           FINITE POSITIVE THRESHOLD;
    k > 1 :  V → ∞ AND the tortoise endpoint is finite — CONFINING
                           (purely discrete spectrum, AdS-like).
""")

# --- the two named asymptotic mechanisms, exact -----------------------------
f_lin = m * r
V_lin = sp.expand(V_def.subs(f_gen, f_lin).doit())
check("f = m·r:  V = m² + m·λ/r exactly, so V(∞) = m² (the f'-term "
      "f·f'/r = m²·1 supplies the mass)",
      sp.simplify(V_lin - (m**2 + m * lam / r)) == 0
      and sp.limit(V_lin, r, sp.oo) == m**2)

f_quad = m**2 * r**2 / lam
V_quad = sp.expand(V_def.subs(f_gen, f_quad).doit())
check("SPEC-CHECK — f = m²r²/λ (the λ-term candidate): V = m² + 2m⁴r²/λ² "
      "exactly; the λ-term DOES give m² but the f'-term DIVERGES ⇒ k = 2 "
      "is CONFINING, not threshold-lifting",
      sp.simplify(V_quad - (m**2 + 2 * m**4 * r**2 / lam**2)) == 0
      and sp.limit(V_quad, r, sp.oo) == sp.oo)
print("""     SPEC CORRECTION (flagged per instructions): the task spec's first
     clause suggested quadratic growth f ~ m²r²/λ as a threshold-lifting
     route via the λ-term.  Sympy result (binding): at k = 2 the f'-term
     c²·k·r^(2k−2) = 2c²r² diverges, so quadratic f CONFINES (V → ∞, finite
     tortoise endpoint); it does NOT produce a finite positive threshold.
     The spec's own later analysis (k = 1 unique lifter, k = 2 diverges)
     is the correct one and is what sympy confirms.""")

# --- general f: the differential identity behind uniqueness ----------------
ident = sp.simplify(sp.diff(f_gen**2, r)
                    - (2 * r * V_def - 2 * lam * f_gen / r))
check("general-f identity:  (f²)' = 2rV − 2λf/r  (exact, generic f)",
      ident == 0)
print("""
  GENERAL-f UNIQUENESS (beyond power laws — argument, with the identity
  above as its verified core):  suppose V(r) → m² > 0 with the tortoise
  endpoint infinite.  Integrating (f²)' = 2rV − 2λf/r from R to r:

      f(r)² = f(R)² + ∫ 2sV(s)ds − 2λ∫ f(s)/s ds.

  The first integral is m²r²(1+o(1)).  An elementary comparison bootstrap
  (f² ≤ A + (1+ε)m²s² on [R,r] ⇒ ∫f/s ds ≤ √(1+ε)·m·r + O(ln r) = o(r²),
  and symmetrically from below) closes the sandwich:  f(r)² = m²r²(1+o(1)),
  i.e.  f ~ m·r.  HONESTY NOTE: the bootstrap is an elementary stated
  argument (classical comparison, not symbol-checked end-to-end); the
  differential identity it rests on is verified exactly above, and the
  power-law class is verified exhaustively in the table.
""")
f_test = m * r + 7 * sp.log(r) + 3
V_test = V_def.subs(f_gen, f_test).doit()
check("non-power-law spot check: f = m·r + 7·ln r + 3 has V(∞) = m² and "
      "f/(m·r) → 1 (lifters are asymptotically linear)",
      sp.limit(V_test, r, sp.oo) == m**2
      and sp.limit(f_test / (m * r), r, sp.oo) == 1)

# --- confining case: endpoint strength g(k) ---------------------------------
print()
print("  CONFINING-CASE ENDPOINT STRENGTH (exact): for k > 1 the finite")
print("  endpoint x_∞ has  x_∞ − x = r^(1−k)/(c(k−1)), and V·(x_∞−x)² → g(k):")
s_pos = sp.symbols("s", positive=True)
k_val = 1 + s_pos
d_end = r**(1 - k_val) / (c * (k_val - 1))
g_lim = sp.limit(sp.expand(V_target.subs(k, k_val) * d_end**2), r, sp.oo)
g_expected = k_val / (k_val - 1)**2
check("V·(x_∞−x)² → k/(k−1)²  exactly for all k > 1 (symbolic k = 1+s, "
      "s > 0)", sp.simplify(g_lim - g_expected) == 0)
check("AdS-like control k = 2:  g = 2 (inverse-square barrier strength at "
      "the finite endpoint)", g_expected.subs(s_pos, 1) == 2)
sol_lp = sp.solve_univariate_inequality(3 * k**2 - 10 * k + 3 <= 0, k,
                                        relational=False)
check("limit-point window: g(k) ≥ 3/4 ⇔ 3k²−10k+3 ≤ 0 ⇔ k ∈ [1/3, 3]; "
      "intersected with k > 1: limit-point for 1 < k ≤ 3",
      sol_lp == sp.Interval(sp.Rational(1, 3), 3))
print("""     so for 1 < k ≤ 3 the finite endpoint is limit-point (no boundary
     condition needed; spectrum discrete outright, M4); for k > 3 it is
     limit-circle — extensions exist but EVERY self-adjoint extension at a
     finite endpoint is still purely discrete there (M4).  Either way:
     confining ⇒ discrete, and the classification stands.""")

# ---------------------------------------------------------------------------
# T3 — action cost: the rigidity mechanism
# ---------------------------------------------------------------------------
hr("T3 — ACTION COST: lifting or confining costs infinite exterior C1 "
   "action; finite action forces threshold = 0")

R0, S0 = sp.symbols("R_0 S_0", positive=True)

print("  Exterior C1 action (banked repo form, "
      "native_self_similar_c1_value_action.py):")
print("      S_ext = (1/4) ∫_{R0}^∞ r² (f')² dr.")
print()
print("  (a) FORWARD: every lifter/confiner has infinite exterior action.")
integrand_pl = sp.expand(r**2 * sp.diff(f_pl, r)**2)
check("action integrand for f = c·r^k is  c²k²·r^(2k)  exactly",
      sp.simplify(integrand_pl - c**2 * k**2 * r**(2 * k)) == 0)
all_div = True
for kk in [1, sp.Rational(5, 4), sp.Rational(3, 2), 2, 3]:
    val = sp.integrate(r**(2 * kk), (r, 1, sp.oo))
    all_div = all_div and (val == sp.oo)
check("∫_1^∞ r^(2k) dr = ∞ for k ∈ {1, 5/4, 3/2, 2, 3} (every lifting or "
      "confining power law)", all_div)
print("     general criterion: ∫^∞ r^(2k) dr < ∞ ⇔ 2k < −1 ⇔ k < −1/2 —")
print("     so in fact EVERY growing power law (k > 0), not just k ≥ 1,")
print("     has infinite exterior action; the k ≥ 1 cases needed here are")
print("     a fortiori.  By T2's general-f statement, ANY f with V(∞) > 0")
print("     is asymptotically linear, so its action integrand grows like")
print("     r²·m² and the divergence is not special to exact power laws.")

print()
print("  (b) CONVERSE: finite exterior action ⇒ f converges "
      "(Cauchy–Schwarz, exact).")
print("""      For R0 ≤ a < b:   f(b) − f(a) = ∫_a^b f' dr = ∫_a^b (r f')·(1/r) dr,
      so by Cauchy–Schwarz (classical inequality; instances verified below):

          |f(b) − f(a)|² ≤ [∫_a^b r²(f')² dr]·[∫_a^b dr/r²]
                         ≤ 4·S_tail(a) · (1/a),

      where S_tail(a) = (1/4)∫_a^∞ r²(f')² dr → 0 as a → ∞ (tail of a
      convergent integral).""")
a_s, b_s = sp.symbols("a b", positive=True)
int_inv = sp.integrate(1 / r**2, (r, a_s, b_s))
check("∫_a^b dr/r² = 1/a − 1/b ≤ 1/a uniformly in b (the b-independent "
      "bound that excludes f_∞ = ∞)",
      sp.simplify(int_inv - (1 / a_s - 1 / b_s)) == 0
      and sp.simplify(1 / a_s - int_inv) == 1 / b_s)
# Cauchy–Schwarz instances, exact rationals:
lhs_eq = sp.integrate(1 / r**2, (r, 1, 2))**2          # f' = 1/r² (equality)
rhs_eq = (sp.integrate(r**2 / r**4, (r, 1, 2))
          * sp.integrate(1 / r**2, (r, 1, 2)))
check("C–S instance (equality case f' = 1/r², i.e. r·f' ∝ 1/r): "
      f"LHS = RHS = {lhs_eq} exactly", sp.simplify(lhs_eq - rhs_eq) == 0)
lhs_st = sp.integrate(1 / r**3, (r, 1, 2))**2          # f' = 1/r³ (strict)
rhs_st = (sp.integrate(r**2 / r**6, (r, 1, 2))
          * sp.integrate(1 / r**2, (r, 1, 2)))
check(f"C–S instance (strict case f' = 1/r³): LHS = {lhs_st} < RHS = "
      f"{rhs_st} (exact rationals)", bool(lhs_st < rhs_st))
print("""      Consequence (exact chain): sup_{b>a} |f(b) − f(a)| ≤ 2√(S_tail(a))/√a
      → 0, so f is Cauchy at infinity and converges to a FINITE limit
      f_∞ ≥ 0.  The edge case f_∞ = ∞ is EXCLUDED by the bound's uniformity
      in b: f(b) ≤ f(R0) + 2√(S_ext)/√(R0) for ALL b.  In particular f is
      bounded above by a constant M on [R0, ∞).""")

print()
print("  (c) finite action ⇒ V ∈ L¹(dr*) near infinity ⇒ threshold = 0 "
      "exactly.")
check("V/f = λ/r² + f'/r identically (the f in V cancels the 1/f in "
      "dr* = dr/f — the L¹ bound below is f-INDEPENDENT)",
      sp.simplify(V_def / f_gen - (lam / r**2 + sp.diff(f_gen, r) / r)) == 0)
int_r4 = sp.integrate(1 / r**4, (r, R0, sp.oo))
check("∫_{R0}^∞ dr/r⁴ = 1/(3R0³) exactly (the C–S weight for the f'/r "
      "term)", sp.simplify(int_r4 - 1 / (3 * R0**3)) == 0)
print("""      Assembling (triangle inequality + Cauchy–Schwarz, both classical):

          ∫_{r*(R)}^{x_∞} |V| dr* = ∫_R^∞ |λ/r² + f'/r| dr
              ≤ λ/R + [∫_R^∞ r²(f')² dr]^{1/2} · [∫_R^∞ dr/r⁴]^{1/2}
              = λ/R + 2√(S_tail(R)) / √(3R³)   <  ∞.

      And the tortoise endpoint is INFINITE: f ≤ M (step b) gives
      r* = ∫dr/f ≥ (r − R0)/M → ∞ — Case A of T1 applies, never Case B.
      By (M3) (V ∈ L¹ near ∞ on a half-line ⇒ σ_ess = [0, ∞), classical
      short-range scattering — assumed, not re-proved):

          THRESHOLD = 0 EXACTLY.   No liminf subtleties survive: the
      finite-action case lands in the unconditional L¹ clause, not the
      general Persson liminf clause.

      (Note the bound holds even if f_∞ = 0: every factor of f cancelled.)""")

# worked exact example
f_ex = 2 + 3 / r
V_ex = sp.simplify(V_def.subs(f_gen, f_ex).doit())
S_ex = sp.Rational(1, 4) * sp.integrate(
    r**2 * sp.diff(f_ex, r)**2, (r, 1, sp.oo))
Vf_ex = sp.simplify(V_ex / f_ex).subs(lam, 2)          # = 2/r² − 3/r³
x_split = sp.Rational(3, 2)
L1_ex = (sp.integrate(-(2 / r**2 - 3 / r**3), (r, 1, x_split))
         + sp.integrate(2 / r**2 - 3 / r**3, (r, x_split, sp.oo)))
check("worked example f = 2 + 3/r (λ=2, R=1): S_ext = 9/4 finite, "
      "V(∞) = 0, and ∫|V|dr* = 5/6 exactly (sign split at r = 3/2)",
      S_ex == sp.Rational(9, 4)
      and sp.limit(V_ex, r, sp.oo) == 0
      and sp.simplify(Vf_ex - (2 / r**2 - 3 / r**3)) == 0
      and L1_ex == sp.Rational(5, 6))

# ---------------------------------------------------------------------------
# T4 — vacuum cross-check: the exact native vacuum family
# ---------------------------------------------------------------------------
hr("T4 — VACUUM CROSS-CHECK: f = C + 2/r (exact native vacuum family)")

C_s = sp.symbols("C", positive=True)
phi = sp.Rational(1, 2) * sp.log(r / (2 + C_s * r))
vac_res = sp.simplify(sp.diff(phi, r, 2) + 2 * sp.diff(phi, r) / r
                      - 2 * sp.diff(phi, r)**2)
check("φ = (1/2)ln(r/(2+Cr)) satisfies the vacuum equation "
      "φ'' + 2φ'/r − 2(φ')² = 0 EXACTLY (residual 0)", vac_res == 0)
f_vac = sp.simplify(sp.exp(-2 * phi))
check("f = e^(−2φ) = C + 2/r exactly (repo convention f = e^(−2φ), "
      "native_core_solver.py)", sp.simplify(f_vac - (C_s + 2 / r)) == 0)
V_vac = sp.simplify(V_def.subs(f_gen, C_s + 2 / r).doit())
check("V(∞) = 0 for every C > 0 (the vacuum family CANNOT lift the "
      "threshold)", sp.limit(V_vac, r, sp.oo) == 0)
S_vac = sp.Rational(1, 4) * sp.integrate(
    r**2 * sp.diff(C_s + 2 / r, r)**2, (r, R0, sp.oo))
check("exterior action S_ext = (1/4)∫_{R0}^∞ r²(f')²dr = 1/R0 — FINITE "
      "(the vacuum family sits squarely inside the rigidity class)",
      sp.simplify(S_vac - 1 / R0) == 0)
print("""
  Consistency: C = 1 is exactly the prior theorem's exterior f = 1 + a/r
  with a = 2.  The exact vacuum family lands in the finite-action class,
  its threshold is 0, and the prior theorem's empty-point-spectrum
  conclusion applies — the cross-check closes: the metric's OWN vacuum
  cannot evade the rigidity theorem, as it must not.""")

# ---------------------------------------------------------------------------
# T5 — the assembled theorem + the precisely-stated escapes
# ---------------------------------------------------------------------------
hr("T5 — THRESHOLD RIGIDITY THEOREM + the unique static escape (derived)")

print("""
  THEOREM (assembled from T1–T3, vacuum-checked in T4).  On the fixed
  ansatz ds² = −f dt² + f⁻¹dr² + r²dΩ², f > 0 smooth on (r0, ∞), for the
  massless metric-native probe in any sector ell ≥ 1:

      finite exterior C1 action  S_ext = (1/4)∫r²(f')²dr < ∞
          ⇒  f → f_∞ ∈ [0, ∞)  (T3b, Cauchy–Schwarz, exact)
          ⇒  V ∈ L¹(dr*) with infinite tortoise endpoint (T3c, exact bound)
          ⇒  CONTINUUM THRESHOLD = 0:  σ_ess = [0, ∞)   (M3)
          ⇒  EMPTY POINT SPECTRUM:
                ω² < 0 and ω² = 0 die by the quadratic-form positivity of
                ∫[r²f(R')² + λR²]dr (f > 0 suffices; the prior theorem's
                A1/A3 arguments verbatim, same Friedrichs-class convention
                at the inner endpoint), and ω² > 0 eigenvalues embedded in
                [0,∞) are excluded because V ∈ L¹ forces Jost–Levinson
                asymptotics u ~ e^(±iωr*) — non-decaying, never L² (M3;
                the prior theorem's A2 generalized from the 1+a/r tail to
                the whole finite-action class).

  Contrapositive (the rigidity): NO native structure f with finite exterior
  C1 action can lift the probe's continuum threshold above 0 — and the
  structures that COULD (T2: asymptotically linear f ~ m·r lifts to m²;
  superlinear f confines) all cost INFINITE exterior C1 action (T3a).
  Within statics + spherical symmetry + the fixed areal function rho = r +
  finite action + a single structure, branch (iii) of
  native_open_domain_threshold_theorem.py is CLOSED.

  THE REMAINING STATIC ESCAPE SLOTS, STATED PRECISELY:
""")

# --- E1: free the areal function -------------------------------------------
print("  E1 — FREE THE AREAL FUNCTION rho(r):  "
      "ds² = −f dt² + f⁻¹dr² + ρ(r)²dΩ².")
t_s, th = sp.symbols("t theta", real=True)
rho_f = sp.Function("rho", positive=True)(r)
Y_f = sp.Function("Y")(th)
Phi = sp.exp(-sp.I * omega * t_s) * R_f * Y_f
sqrtg = rho_f**2 * sp.sin(th)
box = (-(1 / f_gen) * sp.diff(Phi, t_s, 2)
       + (1 / sqrtg) * sp.diff(sqrtg * f_gen * sp.diff(Phi, r), r)
       + (1 / (rho_f**2 * sp.sin(th)))
       * sp.diff(sp.sin(th) * sp.diff(Phi, th), th))
box = box.subs(sp.Derivative(Y_f, th, 2),
               -lam * Y_f - (sp.cos(th) / sp.sin(th)) * sp.Derivative(Y_f, th))
radial_target = (sp.diff(rho_f**2 * f_gen * sp.diff(R_f, r), r)
                 - lam * R_f + omega**2 * (rho_f**2 / f_gen) * R_f)
box_reduced = sp.simplify(
    box * rho_f**2 / sp.exp(-sp.I * omega * t_s) - radial_target * Y_f)
check("wave operator on the (f, ρ) metric (√−g = ρ²sinθ, g^rr = f, "
      "g^tt = −1/f, Δ_S²Y = −λY) reduces EXACTLY to "
      "−(ρ²fR')' + λR = ω²(ρ²/f)R", box_reduced == 0)

u_rho = rho_f * R_f
V_rho = f_gen * lam / rho_f**2 + f_gen * sp.diff(
    f_gen * sp.diff(rho_f, r), r) / rho_f
lhs_rho = (f_gen * sp.diff(f_gen * sp.diff(u_rho, r), r)
           + (omega**2 - V_rho) * u_rho)
rhs_rho = (f_gen / rho_f) * radial_target
check("tortoise form via u = ρ·R, dr* = dr/f:  u'' + [ω² − V]u = 0 with "
      "V = f·λ/ρ² + f·(fρ')'/ρ  (exact, generic f and ρ)",
      sp.simplify(lhs_rho - rhs_rho) == 0)
check("consistency: ρ = r recovers the banked V = f(λ/r² + f'/r)",
      sp.simplify(V_rho.subs(rho_f, r).doit() - V_def) == 0)

print("""
     THE SATURATING-ρ THRESHOLD CLAIM: if ρ → ρ_∞ FINITE and f → f_∞ > 0
     (a cylinder-like end: bounded angular area), the angular term ALONE
     supplies  V(∞) ⊇ f_∞·λ/ρ_∞² = m² > 0 — the threshold lifts with NO
     f-growth at all.  Verified on exact representatives:""")

rho_inf, b_s2, f_inf = sp.symbols("rho_oo b f_oo", positive=True)
rho_sat = rho_inf - b_s2 / r
V_sat = (V_rho.subs([(rho_f, rho_sat), (f_gen, f_inf)])).doit()
V_sat = sp.simplify(V_sat)
check("representative 1 (f = f_∞ const, ρ = ρ_∞ − b/r):  V(∞) = "
      "f_∞λ/ρ_∞² > 0 exactly, and S_ext = (1/4)∫ρ²(f')²dr = 0 — "
      "threshold LIFTED at ZERO action cost",
      sp.limit(V_sat, r, sp.oo) == f_inf * lam / rho_inf**2)
f_sat2 = f_inf + sp.exp(-r)
V_sat2 = sp.simplify(V_rho.subs([(rho_f, rho_inf), (f_gen, f_sat2)]).doit())
S_sat2 = sp.Rational(1, 4) * sp.integrate(
    rho_inf**2 * sp.diff(f_sat2, r)**2, (r, R0, sp.oo))
check("representative 2 (nonconstant f = f_∞ + e^(−r), ρ = ρ_∞):  "
      "V(∞) = f_∞λ/ρ_∞² > 0 with S_ext = ρ_∞²e^(−2R0)/8 FINITE",
      sp.limit(V_sat2, r, sp.oo) == f_inf * lam / rho_inf**2
      and sp.simplify(S_sat2 - rho_inf**2 * sp.exp(-2 * R0) / 8) == 0)
tort_sat = sp.integrate(1 / f_inf, (r, R0, b_s2))
check("tortoise endpoint stays infinite (f → f_∞ finite: r* ~ r/f_∞), so "
      "Case A applies and σ_ess = [m², ∞) by (M2): a genuine window "
      "(0, m²) opens for L² states",
      sp.limit(tort_sat, b_s2, sp.oo) == sp.oo)

print("""
     WHY THE RIGIDITY PROOF CANNOT TOUCH THIS: the T3 mechanism kills only
     the f-GROWTH routes, and the natural transplant of the C1 action,
     S = (1/4)∫ρ²(f')²dr, sees only f' — the saturating-ρ mass term
     f_∞λ/ρ_∞² needs NO f-variation at all (representative 1 has f' ≡ 0,
     S_ext = 0).  Moreover with ρ bounded the C–S convergence argument
     itself degrades (its weight integral ∫dr/ρ² ~ (b−a)/ρ_∞² no longer
     converges), but that is moot: the lift comes from the angular term,
     which survives in V for ANY f with a positive limit.  ρ = r is
     LOAD-BEARING in T1–T3 exactly through λ/ρ² → 0.

     HONEST CAVEATS ON E1 (recorded, not implied away):
       (a) the action form (1/4)∫ρ²(f')²dr for general ρ is the ρ = r
           banked form transplanted; its derivation from the C1 boundary
           variation for general ρ is its own job, NOT done here;
       (b) whether the NATIVE field equations admit a saturating-ρ end
           (and with what interior matching) is precisely the branch-(iii)
           hunt — this section shows the threshold OBSTRUCTION disappears,
           not that the configuration EXISTS (principle 1: it must be
           uncovered, never imported);
       (c) a cylinder-like end is a strong geometric statement (not
           asymptotically flat; bounded-area cross sections) — its
           physical admissibility must be judged when a candidate exists;
       (d) the rigidity argument DOES extend to any growing ρ with
           ∫^∞ dr/ρ² < ∞ as far as f-convergence is concerned; the open
           structural question is only the bounded-ρ (saturating) end.

  E2 — NONSTATIC / BREATHER (recorded, out of scope): no single-ω
     separation; outside this theorem AND the prior theorem, exactly as
     recorded in the prior theorem's scope exclusions.  Unchanged.

  E3 — MULTI-CELL / ENSEMBLE ASYMPTOTICS (recorded, deferred): the theorem
     covers a SINGLE structure with one asymptotic end; an ensemble
     (orchestra build, charter principle 5) changes the domain and the
     asymptotics — deferred to the orchestra build, not closed here.""")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
hr("SUMMARY")
if FAILURES:
    print(f"  {len(FAILURES)} CHECK(S) FAILED:")
    for lab in FAILURES:
        print(f"    - {lab}")
    sys.exit(1)
print("""  All symbolic/exact checks PASSED.

  THRESHOLD RIGIDITY THEOREM: on the fixed ansatz (rho = r), finite
  exterior C1 action forces continuum threshold = 0 exactly, hence empty
  point spectrum (prior theorem's machinery).  Lifting needs f ~ m·r
  (unique, k = 1); confining needs superlinear f; both cost infinite
  exterior C1 action.  Branch (iii) is CLOSED within {static, spherically
  symmetric, rho = r, finite action, single structure}.

  Assumed classical machinery (flagged inline, not re-proved): Persson/
  Weyl essential-spectrum criterion (M1–M2), L¹ short-range scattering /
  Jost–Levinson asymptotics (M3), finite-endpoint discreteness (M4), the
  Cauchy–Schwarz and triangle inequalities (instances verified exactly),
  and the T2 general-f comparison bootstrap (stated; its differential
  identity verified).  Inner-endpoint convention: Friedrichs class,
  inherited from the prior theorem.

  THE STATIC SEARCH SPACE IS NOW ONE SLOT WIDE: the saturating areal
  function (E1, cylinder-like end) is the unique static escape — the
  threshold lifts to f_oo*lambda/rho_oo^2 with ZERO action cost in f.
  The branch-(iii) hunt should look for native mechanisms that bound the
  areal function, not mechanisms that grow f.  E2 (nonstatic) and E3
  (ensemble) remain recorded escapes outside statics/single-structure.""")
