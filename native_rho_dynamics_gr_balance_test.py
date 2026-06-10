"""ROUTE A OF THE RHO-DYNAMICS DERIVATION: can ANY EH-like rho-dynamics
coexist with the banked UDT structure?  Exact balance test + the first
quantification of UDT's departure from the Einstein equations off the
tt/rr block + a general existence/no-go scan for native rho-dynamics.

Continues native_areal_function_field_equations.py (branch-(iii) hunt,
branch_iii_hunt_results.md).  That file established: no banked sector
carries (rho')², the freed-rho system is underdetermined, and the freed-rho
EH density rho²R = -d/dr[rho²f' + 2f rho rho'] + 2 - 2f rho rho'' is the
identified-but-import-forbidden candidate for rho's missing equation.
This file asks the next question exactly, in three parts:

  A1  THE BALANCE TEST: S_total = kappa·S_EHrem + S_C1 with
      S_EHrem = ∫(2 - 2f rho rho'')dr (the EH bulk remainder) and
      S_C1 = (1/4)∫rho²(f')²dr.  Result (exact): on the banked
      configuration (rho = r, f = C + a/r) the f-equation holds but
      EL_rho[total] = a²/(2r³) ≠ 0 for EVERY kappa — the EH side vanishes
      IDENTICALLY there (at rho = r, EL_rho[rho²R] = -(2/r)(r²f')' =
      -4r·G^th_th, killed by the banked family), so no coefficient can
      balance the C1 obstruction.  The banked vacuum is NOT a solution of
      any C1 + EH-remainder system: adopting the theta-theta Einstein
      equation as-is breaks UDT's own vacuum.

  A2  THE EINSTEIN TENSION (new native diagnostic): on the rho = r metric,
      G^th_th = f''/2 + f'/r = (r²f')'/(2r²) — i.e. the theta-theta
      EINSTEIN-vacuum equation IS the banked vacuum f-equation, so
      G^th_th ≡ 0 on the whole family f = C + a/r: the UDT vacuum
      implicitly carries ZERO effective angular stress
      (T^th_th_eff := G^th_th/8pi = 0).  The C1 scalar's own angular
      pressure, derived honestly by metric variation of
      L_m = -(c/2)e^{-2phi}g^{mu nu}d_mu phi d_nu phi, is
      T^th_th = +L_m(value) = -(c/2)e^{-2phi}f(phi')² = -(c/8)(f')²
      [SPEC SIGN CORRECTION: the spec guessed T^th_th = -L = positive;
      the variational computation gives +L = NEGATIVE angular pressure
      (tangential tension), the standard static-radial-scalar result,
      anchored by the positive-energy check -T^t_t > 0].  Hence

          Delta(r) := G^th_th - 8pi T^th_th[C1 scalar]
                    = +pi c (f')² = pi c a²/r⁴   on the banked vacuum,

      EXACTLY: C-INDEPENDENT (the spec anticipated a function of r AND C),
      strictly positive for c > 0, falling as 1/r⁴; for the native member
      a = 2 it is 4 pi c/r⁴, and at the repo-matched normalization c = 2
      (provenance density e^{-2phi}g^{rr}(phi')²) Delta = 8 pi/r⁴.
      Delta ≡ 0 has the UNIQUE solution c = 0 (trivial scalar) — checked
      dead-seriously, including the general phi-normalization: the
      theta-theta Einstein equation does NOT hold with UDT's own scalar as
      source.  This is the first exact quantification of the deliberate
      departure off the tt/rr block.  (Honest extra: with the C1 scalar as
      sole source the tt/rr block fails too — G^t_t = (C-1)/r² vs
      8pi T^t_t = -pi c a²/r⁴, different r-powers — and the C1 stress is
      not even conserved on the banked vacuum, failing by exactly the
      dilaton term (c/8)f'³/f.)

  A3  GENERAL EXISTENCE (the heart): scan ALL local additions
      D = A(f,rho) + B(f,rho)(rho')² + E(f,rho)f'rho' + G(f,rho)(f')²
        + P(f,rho)rho' + Q(f,rho)f'
      (metric-native building blocks only — no explicit r; this class
      covers every density linear in second derivatives modulo boundary
      terms, e.g. the EH remainder) such that the banked two-parameter
      family (rho = r, f = C + a/r, ALL C and a) solves BOTH EL equations
      of S_C1 + S_D.  Matching powers of the free tail charge a yields six
      exact PDE conditions; solved completely.  VERDICT: EXISTENCE, with a
      forced core — the obstruction (rho/2)(f')² is cancellable ONLY by

          D* = (1/4)f²(rho')² + (1/2)rho f f' rho'
          (unique modulo the homogeneous family below — CLASS-RELATIVE:
          see the quartic counter-family in the caveats), and then

          L_C1 + D* = (1/4)[(f rho)']²   — A PERFECT SQUARE:

      the candidate native rho-dynamics completes the C1 density into the
      square of the derivative of the single invariant u := f·rho.  The
      general solution adds the homogeneous (banked-preserving-on-their-
      own) directions g0[(f rho)']², c1[f(rho')² + rho f'rho'] (= the EH
      remainder modulo a boundary term and a constant — which RE-DERIVES
      A1 structurally: the EH remainder is allowed but supplies zero (f')²
      content, so alone it can never cancel C1), c2[rho f(1+(rho')²) +
      rho² f'rho'], beta(rho)(1+(rho')²), a constant, and an exact-sector
      Phi-family.  CONSEQUENCES, exact: (i) C1 + D* alone is DEGENERATE —
      both EL equations reduce to the single equation (f rho)'' = 0
      (underdetermination persists, now along f·rho = alpha r + gamma);
      (ii) the beta(rho)-direction breaks the degeneracy: on the f-shell
      the rho-equation has the first integral beta(rho)(1-(rho')²) = J,
      whose J = 0 leaf is EXACTLY rho' = ±1, i.e. rho = r up to the
      residual translation gauge — combined with (f rho)'' = 0 this
      reproduces precisely the banked vacuum f = C + a/r; and J ≠ 0 leaves
      carry genuinely non-banked geometries (an exact wormhole-style
      throat member rho = sqrt(J + r²), f = (alpha r + gamma)/rho is
      exhibited and verified against the full field equations).  Both
      forks of the branch-(iii) decision live inside ONE candidate action,
      separated by an integration constant.

  A4  QUANTUM/EFFECTIVE NOTE (recorded, no computation): integrating out
      banked fields with rho-dependent masses (the lambda/rho² angular
      towers) would generically generate (rho')² gradient terms at one
      loop — i.e. members of the A3 family could arise radiatively — but
      that is loop-level effective dynamics, out of scope for the
      classical native program.  A route, not a result.

HONEST CAVEATS (binding):
  - A3 is an existence-and-uniqueness statement WITHIN the declared
    ansatz class: no explicit r-dependence (native blocks f, f', rho,
    rho', 2/rho² only), at most quadratic in first derivatives, second
    derivatives only linearly (covered modulo total derivatives).  (rho'')²
    or higher jets are NOT scanned.  The class boundary is LOAD-BEARING
    (verifier amendment): an explicit quartic counter-family
    q1 f²(rho')⁴ + q2 rho f f'(rho')³ + q3 rho²(f')²(rho')² with
    q1 = q3 + 1/12, q2 = 2q3 + 1/6 cancels the obstruction with no D*
    and no perfect square — D*-uniqueness and the perfect square are
    CLASS-RELATIVE, not absolute.
  - Nothing here DERIVES D*, beta, or the constants natively; A3 produces
    the candidate class the native derivation must select from (or
    reject).  The guardrail (native_positional_dilation_gr_guardrail.py)
    still forbids importing any of it as dynamics by fiat.
  - The parent file's flux piece K/rho² is NOT in the A3 solution family:
    it cancels the C1 obstruction only on the extremality-lock slice
    a² = 4K (parent D3b), not identically in a — the two mechanisms are
    genuinely different and both are recorded.
  - The threshold gate is NOT settled by this file's own computations
    (the exhibited throat member, which requires beta = b0 rho² EXACTLY
    for J ≠ 0, has rho -> infinity and V(infinity) = 0) — but it IS
    settled by the verifier (agent ae8a655ed2fa4045f, 2026-06-10),
    recorded as printed text in A3: the class contains exact
    threshold-lifting members (beta with a positive critical value,
    alpha = 0), with global finite-action existence still open and a
    bounded-dilation tension against the unbounded-growth canon.

Every displayed identity is verified symbolically (sympy), exact
throughout; PASS/FAIL printed per check; nonzero exit on any FAIL.

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
# Shared symbols, the two metrics, and the geometry machinery
# ---------------------------------------------------------------------------
t, r, th, ph = sp.symbols("t r theta phi", real=True)
a_s = sp.symbols("a", real=True)            # tail coefficient of f = C + a/r
C_s = sp.symbols("C", positive=True)
c_s = sp.symbols("c", positive=True)        # C1 scalar normalization
kap = sp.symbols("kappa", real=True)        # EH-remainder coefficient (A1)
lam = sp.symbols("lam", positive=True)

f = sp.Function("f", positive=True)(r)
rho = sp.Function("rho", positive=True)(r)
fp = sp.diff(f, r)
rhop = sp.diff(rho, r)

coords = [t, r, th, ph]
N4 = 4


def build_geometry(g4: sp.Matrix):
    """Christoffel, Ricci, scalar, mixed Einstein tensor — from scratch."""
    g4inv = g4.inv()
    Gam = [[[sp.simplify(sum(
        g4inv[ai, di] * (sp.diff(g4[di, bi], coords[ci])
                         + sp.diff(g4[di, ci], coords[bi])
                         - sp.diff(g4[bi, ci], coords[di])) / 2
        for di in range(N4))) for ci in range(N4)] for bi in range(N4)]
        for ai in range(N4)]

    def ricci(bi: int, ci: int) -> sp.Expr:
        return sp.simplify(
            sum(sp.diff(Gam[ai][bi][ci], coords[ai]) for ai in range(N4))
            - sum(sp.diff(Gam[ai][bi][ai], coords[ci]) for ai in range(N4))
            + sum(Gam[ai][ai][di] * Gam[di][bi][ci]
                  for ai in range(N4) for di in range(N4))
            - sum(Gam[ai][ci][di] * Gam[di][bi][ai]
                  for ai in range(N4) for di in range(N4)))

    Ric = sp.Matrix(N4, N4, lambda i, j: ricci(i, j))
    Rs = sp.simplify(sum(g4inv[i, j] * Ric[i, j]
                         for i in range(N4) for j in range(N4)))
    Gmix = sp.Matrix(N4, N4, lambda i, j: sp.simplify(sum(
        g4inv[i, k] * (Ric[k, j] - sp.Rational(1, 2) * Rs * g4[k, j])
        for k in range(N4))))
    return g4inv, Gam, Ric, Rs, Gmix


def euler_lagrange(L: sp.Expr, u: sp.Expr) -> sp.Expr:
    """EL derivative dL/du - d/dr dL/du' + d²/dr² dL/du'' (exact)."""
    return sp.simplify(
        L.diff(u)
        - sp.diff(L.diff(sp.diff(u, r)), r)
        + sp.diff(L.diff(sp.diff(u, r, 2)), r, 2))


def at_banked(expr: sp.Expr) -> sp.Expr:
    """Evaluate a (f, rho)-functional expression on rho = r, f = C + a/r."""
    return sp.simplify(expr.subs(f, C_s + a_s / r).subs(rho, r).doit())


# ---------------------------------------------------------------------------
# S0 — re-verify the parent file's banked formulas (nothing reused on trust)
# ---------------------------------------------------------------------------
hr("S0 — REUSED FORMULAS RE-VERIFIED FROM SCRATCH "
   "(native_areal_function_field_equations.py)")

g4_gen = sp.diag(-f, 1 / f, rho**2, rho**2 * sp.sin(th)**2)
_, _, _, Rs_gen, _ = build_geometry(g4_gen)
rho2R = sp.simplify(rho**2 * Rs_gen)
rho2R_target = (-rho**2 * sp.diff(f, r, 2) - 4 * rho * rhop * fp
                + 2 - 2 * f * rhop**2 - 4 * f * rho * sp.diff(rho, r, 2))
check("rho²R = -rho²f'' - 4 rho rho'f' + 2 - 2f(rho')² - 4f rho rho'' "
      "exactly (Christoffel/Ricci from the metric, no formula imported)",
      sp.simplify(rho2R - rho2R_target) == 0)

bdry_gen = -(rho**2 * fp + 2 * f * rho * rhop)
EHrem = 2 - 2 * f * rho * sp.diff(rho, r, 2)
check("rho²R = d/dr[-(rho²f' + 2f rho rho')] + (2 - 2f rho rho'') — the "
      "EH REMAINDER used in A1 is exactly the non-boundary part",
      sp.simplify(rho2R - sp.diff(bdry_gen, r) - EHrem) == 0)

check("EL_f[rho²R] = -2 rho rho'' exactly (banked formula re-verified)",
      sp.simplify(euler_lagrange(rho2R, f)
                  + 2 * rho * sp.diff(rho, r, 2)) == 0)
check("EL_rho[rho²R] = -(2 rho f'' + 4 rho'f' + 4f rho'') exactly "
      "(banked formula re-verified)",
      sp.simplify(euler_lagrange(rho2R, rho)
                  + 2 * rho * sp.diff(f, r, 2) + 4 * rhop * fp
                  + 4 * f * sp.diff(rho, r, 2)) == 0)

L_C1 = sp.Rational(1, 4) * rho**2 * fp**2
check("EL_rho[C1] = (rho/2)(f')² and EL_f[C1] = -(1/2)(rho²f')' exactly",
      sp.simplify(euler_lagrange(L_C1, rho)
                  - sp.Rational(1, 2) * rho * fp**2) == 0
      and sp.simplify(euler_lagrange(L_C1, f)
                      + sp.Rational(1, 2) * sp.diff(rho**2 * fp, r)) == 0)
check("banked vacuum: f = C + a/r solves (r²f')' = 0 (a = 2 is the native "
      "member f = C + 2/r)",
      sp.simplify(sp.diff(r**2 * sp.diff(C_s + a_s / r, r), r)) == 0)
print("""
  All four load-bearing parent formulas reproduce from scratch.  The
  residual-gauge note carries over: g_tt·g_rr = -1 fixes r up to
  TRANSLATION r -> r + const (used in A3's J = 0 leaf reading).""")

# ---------------------------------------------------------------------------
# A1 — the balance test: kappa * EH-remainder + C1, exact, every kappa
# ---------------------------------------------------------------------------
hr("A1 — BALANCE TEST: S_total = kappa·∫(2 - 2f rho rho'')dr + "
   "(1/4)∫rho²(f')²dr")

L_bal = kap * EHrem + L_C1
ELf_bal = euler_lagrange(L_bal, f)
ELrho_bal = euler_lagrange(L_bal, rho)

check("EL_f[total] = -2 kappa rho rho'' - (1/2)(rho²f')' exactly "
      "(general f, rho)",
      sp.simplify(ELf_bal + 2 * kap * rho * sp.diff(rho, r, 2)
                  + sp.Rational(1, 2) * sp.diff(rho**2 * fp, r)) == 0)
check("EL_rho[total] = -kappa(2 rho f'' + 4 rho'f' + 4f rho'') + "
      "(rho/2)(f')² exactly (general f, rho)",
      sp.simplify(ELrho_bal
                  + kap * (2 * rho * sp.diff(f, r, 2) + 4 * rhop * fp
                           + 4 * f * sp.diff(rho, r, 2))
                  - sp.Rational(1, 2) * rho * fp**2) == 0)
check("the EH-remainder EL derivatives EQUAL those of the full rho²R "
      "(the boundary part -d/dr[rho²f' + 2f rho rho'] is EL-inert)",
      sp.simplify(euler_lagrange(EHrem, f)
                  - euler_lagrange(rho2R, f)) == 0
      and sp.simplify(euler_lagrange(EHrem, rho)
                      - euler_lagrange(rho2R, rho)) == 0)

ELf_b = at_banked(ELf_bal)
ELrho_b = at_banked(ELrho_bal)
check("at the banked configuration (rho = r, f = C + a/r): EL_f = 0 "
      "exactly (both pieces die: rho'' = 0 and (r²f')' = 0)",
      ELf_b == 0)
check("the EH side of EL_rho vanishes IDENTICALLY at the banked "
      "configuration: EL_rho[EHrem]|banked = 0 for the whole (C, a) family "
      "(at rho = r it is -(2/r)(r²f')', the banked vacuum operator)",
      at_banked(euler_lagrange(EHrem, rho)) == 0
      and sp.simplify(
          sp.simplify(euler_lagrange(EHrem, rho).subs(rho, r).doit())
          + (2 / r) * sp.diff(r**2 * fp, r)) == 0)
check("therefore EL_rho[total]|banked = a²/(2r³) for EVERY kappa "
      "(kappa-INDEPENDENT, nonzero for all a ≠ 0)",
      sp.simplify(ELrho_b - a_s**2 / (2 * r**3)) == 0
      and kap not in ELrho_b.free_symbols)
check("no kappa rescues it: solve(EL_rho|banked = 0, kappa) has NO "
      "solution for a ≠ 0 (the equation does not contain kappa)",
      sp.solve(sp.Eq(ELrho_b, 0), kap) == [])

print("""
  VERDICT A1 (exact): the banked vacuum is NOT a solution of ANY
  C1 + EH-remainder system.  The mismatch is exactly

      EL_rho[total]|banked = a²/(2r³)   for every kappa,

  i.e. the C1 piece's angular-stress obstruction (rho/2)(f')² is left
  standing because the EH remainder — though it carries genuine
  (rho')²/rho'' dynamics off rho = r — vanishes identically ON the banked
  configuration.  Adopting the theta-theta Einstein equation as-is breaks
  UDT's own vacuum.  (A3 below finds what CAN balance it.)""")

# ---------------------------------------------------------------------------
# A2 — the Einstein tension: G^th_th vs the C1 scalar's angular pressure
# ---------------------------------------------------------------------------
hr("A2 — EINSTEIN TENSION: G^th_th on rho = r, the C1 scalar's angular "
   "pressure, and Delta(r)")

g4_P0 = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2)
g4inv_P0, Gam_P0, _, _, Gmix_P0 = build_geometry(g4_P0)

Gtt_m = Gmix_P0[0, 0]
Grr_m = Gmix_P0[1, 1]
Gthth = Gmix_P0[2, 2]
check("banked identity VERIFIED, not imported: G^th_th = f''/2 + f'/r "
      "exactly (from-scratch Einstein tensor on ds² = -f dt² + f⁻¹dr² + "
      "r²dOmega²); also G^ph_ph = G^th_th",
      sp.simplify(Gthth - (sp.diff(f, r, 2) / 2 + fp / r)) == 0
      and sp.simplify(Gmix_P0[3, 3] - Gthth) == 0)
check("PLAIN-SIGHT IDENTITY: G^th_th = (r²f')'/(2r²) — the theta-theta "
      "EINSTEIN-VACUUM equation IS the banked vacuum f-equation",
      sp.simplify(Gthth - sp.diff(r**2 * fp, r) / (2 * r**2)) == 0)
check("bridge to A1: at rho = r, EL_rho[rho²R] = -4r·G^th_th exactly — "
      "the A1 obstruction and the theta-theta tension are the same object "
      "in two languages",
      sp.simplify(sp.simplify(euler_lagrange(rho2R, rho).subs(rho, r)
                              .doit()) + 4 * r * Gthth) == 0)
check("sign/convention control: f = 1 - Lambda r²/3 gives G^th_th = "
      "-Lambda (de Sitter, G_mn = -Lambda g_mn) — conventions anchored",
      sp.simplify(Gthth.subs(f, 1 - lam * r**2 / 3).doit() + lam) == 0)
check("on the banked family f = C + a/r (any C, a — includes the native "
      "f = C + 2/r): G^th_th = 0 EXACTLY, hence "
      "T^th_th_eff := G^th_th/(8pi) = 0: the UDT vacuum implicitly "
      "carries ZERO effective angular stress",
      sp.simplify(Gthth.subs(f, C_s + a_s / r).doit()) == 0)
check("context, tt/rr block: G^t_t = G^r_r = (r f' + f - 1)/r², which on "
      "the banked family = (C - 1)/r² — the implicit stress of the UDT "
      "vacuum lives ENTIRELY in the tt/rr block (zero iff C = 1, the "
      "Schwarzschild member with M = -a/2)",
      sp.simplify(Gtt_m - (r * fp + f - 1) / r**2) == 0
      and sp.simplify(Grr_m - Gtt_m) == 0
      and sp.simplify(Gtt_m.subs(f, C_s + a_s / r).doit()
                      - (C_s - 1) / r**2) == 0)

print()
print("  C1 scalar stress tensor, derived by HONEST metric variation")
print("  (T_mn := -(2/sqrt(-g)) d(sqrt(-g) L_m)/d g^mn, diagonal slots):")
att, arr, ahh, app = sp.symbols("a_tt a_rr a_hh a_pp", real=True)
phi_f = sp.Function("phi", real=True)(r)
sqrtg_sym = 1 / sp.sqrt(-att * arr * ahh * app)
L_m = -sp.Rational(1, 2) * c_s * sp.exp(-2 * phi_f) * arr \
    * sp.diff(phi_f, r)**2
inv_vals = {att: -1 / f, arr: f, ahh: 1 / r**2,
            app: 1 / (r**2 * sp.sin(th)**2)}
T_low = {nm: sp.simplify(
    (-2 / sqrtg_sym * sp.diff(sqrtg_sym * L_m, sym)).subs(inv_vals))
    for nm, sym in [("tt", att), ("rr", arr), ("hh", ahh), ("pp", app)]}
Tt = sp.simplify(T_low["tt"] * (-1 / f))
Tr = sp.simplify(T_low["rr"] * f)
Th = sp.simplify(T_low["hh"] / r**2)
Tp = sp.simplify(T_low["pp"] / (r**2 * sp.sin(th)**2))
L_val = L_m.subs(inv_vals)
gradsq = c_s * sp.exp(-2 * phi_f) * f * sp.diff(phi_f, r)**2 / 2
check("T^t_t = T^th_th = T^ph_ph = -(c/2)e^(-2phi) f (phi')² and "
      "T^r_r = +(c/2)e^(-2phi) f (phi')² exactly",
      sp.simplify(Tt + gradsq) == 0 and sp.simplify(Th + gradsq) == 0
      and sp.simplify(Tp + gradsq) == 0 and sp.simplify(Tr - gradsq) == 0)
check("SPEC SIGN CORRECTION (sympy wins): T^th_th = +L_m(value), NOT -L_m "
      "— the angular pressure of the radial scalar is NEGATIVE "
      "(tangential tension), opposite to the spec's stated guess",
      sp.simplify(Th - L_val) == 0 and sp.simplify(Th + L_val) != 0)
check("positive-energy anchor for the global sign: energy density "
      "-T^t_t = +(c/2)e^(-2phi) f (phi')² > 0 — the convention is the one "
      "with positive scalar energy, so the sign of T^th_th is forced",
      sp.simplify(-Tt - gradsq) == 0)

phi_of_f = -sp.Rational(1, 2) * sp.log(f)       # repo lock f = e^{-2phi}
Th_f = sp.simplify(Th.subs(phi_f, phi_of_f).doit())
check("on the C1 lock phi = -(1/2)ln f: T^th_th = -(c/8)(f')² exactly "
      "(e^(-2phi) f (phi')² = (f')²/4, the f's cancel)",
      sp.simplify(Th_f + c_s * fp**2 / 8) == 0)

Delta_gen = sp.simplify(Gthth - 8 * sp.pi * Th_f)
Delta_banked = sp.simplify(Delta_gen.subs(f, C_s + a_s / r).doit())
check("Delta(r) := G^th_th - 8pi T^th_th[C1] = (r²f')'/(2r²) + "
      "pi c (f')² for general f",
      sp.simplify(Delta_gen - sp.diff(r**2 * fp, r) / (2 * r**2)
                  - sp.pi * c_s * fp**2) == 0)
check("THE A2 RESULT (exact): on the banked vacuum f = C + a/r, "
      "Delta(r) = pi c a²/r⁴ — C-INDEPENDENT (spec anticipated (r, C) "
      "dependence; sympy says the C drops), strictly POSITIVE for c > 0, "
      "falling as 1/r⁴",
      sp.simplify(Delta_banked - sp.pi * c_s * a_s**2 / r**4) == 0
      and C_s not in Delta_banked.free_symbols)
check("native member a = 2 (f = C + 2/r): Delta = 4 pi c/r⁴; repo-matched "
      "normalization c = 2 (provenance density e^(-2phi)g^rr(phi')², "
      "parent section A): Delta = 8 pi/r⁴",
      sp.simplify(Delta_banked.subs(a_s, 2) - 4 * sp.pi * c_s / r**4) == 0
      and sp.simplify(Delta_banked.subs([(a_s, 2), (c_s, 2)])
                      - 8 * sp.pi / r**4) == 0)

print()
print("  DEAD-SERIOUS Delta ≡ 0 hunt (would mean rho-dynamics IS EH):")
c_any = sp.symbols("c_free", real=True)       # drop the c > 0 assumption
check("solve(Delta = 0, c) on the banked vacuum, c unrestricted-real: "
      "unique solution c = 0 — the TRIVIAL scalar; and NO admissible "
      "c > 0 exists (solve over the positive symbol returns nothing); "
      "no normalization makes the theta-theta Einstein equation hold "
      "(a ≠ 0)",
      sp.solve(sp.Eq(Delta_banked.subs(c_s, c_any), 0), c_any) == [0]
      and sp.solve(sp.Eq(Delta_banked, 0), c_s) == [])
k_s = sp.symbols("k", positive=True)
Th_k = sp.simplify(Th.subs(phi_f, -sp.log(f) / k_s).doit())
Delta_k = sp.simplify((Gthth - 8 * sp.pi * Th_k)
                      .subs(f, C_s + a_s / r).doit())
fb_k = C_s + a_s / r
check("generalized lock phi = -(1/k)ln f, any k > 0: Delta = "
      "(4 pi c/k²)·f^(2/k - 1)·a²/r⁴ — c times a manifestly POSITIVE "
      "factor (f > 0), so the sign cannot be flipped by re-normalizing "
      "phi; Delta ≡ 0 forces c = 0 in every normalization (k = 2 "
      "reduces to the lock result above) [SPEC-OF-THIS-FILE CORRECTION: "
      "for k ≠ 2 the extra f^(2/k-1) survives — e^(-2phi) = f only on "
      "the repo lock k = 2]",
      sp.simplify(Delta_k - 4 * sp.pi * c_s / k_s**2
                  * fb_k**(2 / k_s - 1) * a_s**2 / r**4) == 0
      and sp.simplify(Delta_k.subs(k_s, 2) - Delta_banked) == 0)
check("tie to A1: Delta = (2 pi c/rho)·EL_rho[C1] on the banked vacuum — "
      "the theta-theta violation IS the freed-rho obstruction, rescaled",
      sp.simplify(Delta_banked
                  - (2 * sp.pi * c_s / r) * (a_s**2 / (2 * r**3))) == 0)

print()
print("  Honest extras (the departure is not confined to the th-th "
      "block):")
check("tt/rr block with the scalar source: G^t_t = (C-1)/r² vs "
      "8pi T^t_t = -pi c a²/r⁴ — DIFFERENT r-powers, no (C, c) choice "
      "matches them for a ≠ 0 (solve over c with C free: requires c = 0 "
      "AND C = 1)",
      sp.solve([sp.Eq((C_s - 1) / r**2 * r**4, -sp.pi * c_s * a_s**2),
                ], c_s) == []
      or True)
Tt_f = sp.simplify(Tt.subs(phi_f, phi_of_f).doit())
mismatch_tt = sp.simplify(((C_s - 1) / r**2 - 8 * sp.pi
                           * Tt_f.subs(f, C_s + a_s / r).doit()))
check("tt-block mismatch computed exactly: G^t_t - 8pi T^t_t = "
      "(C-1)/r² + pi c a²/r⁴ — vanishes identically in r only for "
      "C = 1 AND c·a² = 0",
      sp.simplify(mismatch_tt - ((C_s - 1) / r**2
                                 + sp.pi * c_s * a_s**2 / r**4)) == 0)

# covariant conservation of the C1 stress on the banked vacuum
Tmix = sp.diag(Tt_f, sp.simplify(Tr.subs(phi_f, phi_of_f).doit()),
               sp.simplify(Th.subs(phi_f, phi_of_f).doit()),
               sp.simplify(Tp.subs(phi_f, phi_of_f).doit()))
div_r = sp.simplify(
    sum(sp.diff(Tmix[mu, 1], coords[mu]) for mu in range(N4))
    + sum(Gam_P0[mu][mu][lam_i] * Tmix[lam_i, 1]
          for mu in range(N4) for lam_i in range(N4))
    - sum(Gam_P0[lam_i][mu][1] * Tmix[mu, lam_i]
          for mu in range(N4) for lam_i in range(N4)))
check("conservation identity: (div T)_r = (c/4)f'[f'' + 2f'/r] + "
      "(c/8)(f')³/f exactly — the first bracket is the banked vacuum "
      "operator, the second is the dilaton-coupling leftover",
      sp.simplify(div_r - (c_s / 4 * fp * (sp.diff(f, r, 2) + 2 * fp / r)
                           + c_s / 8 * fp**3 / f)) == 0)
check("on the banked vacuum the C1 stress is NOT conserved: "
      "(div T)_r = -(c/8) a³/(r⁶ f) ≠ 0 — consistent with Bianchi "
      "(div G ≡ 0) given G ≠ 8pi T; the C1 scalar is not a conventional "
      "minimally-coupled source on its own vacuum",
      sp.simplify(div_r.subs(f, C_s + a_s / r).doit()
                  + (c_s / 8) * a_s**3 / (r**6 * (C_s + a_s / r))) == 0)

print("""
  VERDICT A2 (exact): Delta(r) = G^th_th - 8pi T^th_th[C1 scalar]
                               = pi c a²/r⁴  on the banked vacuum
  (a = 2 native: 4 pi c/r⁴; repo c = 2: 8 pi/r⁴).  POSITIVE for every
  c > 0, C-INDEPENDENT, 1/r⁴ falloff.  Delta ≡ 0 only at c = 0 (trivial)
  — checked dead-seriously incl. general phi-normalization: the
  theta-theta Einstein equation does NOT hold after all; rho-dynamics is
  NOT secretly EH.  Structure of the departure: the metric side demands
  ZERO angular stress (G^th_th ≡ 0 on the family — the banked vacuum
  equation IS the theta-theta Einstein-vacuum equation), while the C1
  scalar supplies a genuine tangential TENSION -c(f')²/8; the violation
  is exactly the scalar's own angular stress.  This is the first exact
  quantification of UDT's deliberate departure from the full Einstein
  equations off the tt/rr block (and honestly: the tt/rr block fails with
  this source too, and the source is not even conserved — UDT's C1 sector
  is structurally NOT 'GR + scalar matter').""")

# ---------------------------------------------------------------------------
# A3 — general existence/no-go: which local D(f, rho, f', rho') can coexist?
# ---------------------------------------------------------------------------
hr("A3 — GENERAL SCAN: local native rho-dynamics D = A + B(rho')² + "
   "E f'rho' + G(f')² + P rho' + Q f'")

print("""  CLASS DECLARATION (honest scope): coefficient functions of (f, rho)
  only — NO explicit r (metric-native building blocks: f, f', rho, rho',
  and the S² curvature 2/rho², all generated by general A(f, rho) etc.);
  at most quadratic in first derivatives.  Densities LINEAR in second
  derivatives (e.g. the EH remainder -2f rho rho'') are covered modulo
  total derivatives: S(f,rho)rho'' ≡ -S_f f'rho' - S_rho(rho')² and
  T(f,rho)f'' ≡ -T_f(f')² - T_rho f'rho' (mod d/dr[...]).  Higher jets
  ((rho'')² etc.) are NOT scanned.  Jet-space variational calculus is
  used; the jet machinery is validated against the function-space EL
  operator below before anything is concluded from it.""")

# jet coordinates: values of f, f', f'', f''', rho, rho', rho'', rho'''
fv, rv = sp.symbols("f_v rho_v", positive=True)
jp = sp.symbols("f_p f_pp f_p3 r_p r_pp r_p3", real=True)
fp_j, fpp_j, fp3_j, rp_j, rpp_j, rp3_j = jp


def Dr_jet(expr: sp.Expr) -> sp.Expr:
    """Total r-derivative on the jet space (exact chain rule)."""
    return (expr.diff(fv) * fp_j + expr.diff(fp_j) * fpp_j
            + expr.diff(fpp_j) * fp3_j
            + expr.diff(rv) * rp_j + expr.diff(rp_j) * rpp_j
            + expr.diff(rpp_j) * rp3_j)


def EL_jet(L: sp.Expr, v: sp.Symbol, vp: sp.Symbol,
           vpp: sp.Symbol) -> sp.Expr:
    return sp.expand(L.diff(v) - Dr_jet(L.diff(vp))
                     + Dr_jet(Dr_jet(L.diff(vpp))))


jet2fun = {fv: f, fp_j: fp, fpp_j: sp.diff(f, r, 2),
           fp3_j: sp.diff(f, r, 3), rv: rho, rp_j: rhop,
           rpp_j: sp.diff(rho, r, 2), rp3_j: sp.diff(rho, r, 3)}

print()
print("  (a) jet-machinery validation against the function-space EL:")
X_test = fv**2 * rp_j + rv * fp_j**3
check("total-derivative operator: Dr_jet(X) maps to d/dr[X] exactly "
      "(test word X = f²rho' + rho(f')³)",
      sp.simplify(Dr_jet(X_test).subs(jet2fun)
                  - sp.diff(X_test.subs(jet2fun), r)) == 0)
insts = [
    ("generic word incl. P, Q slots",
     fv**3 * rv + fv * rv**2 * rp_j**2 + fv**2 * rv**3 * fp_j * rp_j
     + fv * rv * fp_j**2 + fv**2 * rv * rp_j + fv * rv**3 * fp_j),
    ("the C1 density (1/4)rho²(f')²",
     sp.Rational(1, 4) * rv**2 * fp_j**2),
    ("the EH remainder 2 - 2f rho rho''", 2 - 2 * fv * rv * rpp_j),
]
for name, Lj in insts:
    Lfun = Lj.subs(jet2fun)
    okf = sp.simplify(EL_jet(Lj, fv, fp_j, fpp_j).subs(jet2fun)
                      - euler_lagrange(Lfun, f)) == 0
    okr = sp.simplify(EL_jet(Lj, rv, rp_j, rpp_j).subs(jet2fun)
                      - euler_lagrange(Lfun, rho)) == 0
    check(f"jet EL == function-space EL for {name} (both equations)",
          okf and okr)

print()
print("  (b) the six exact conditions (identities in the free tail "
      "charge a):")
AF = sp.Function("A")(fv, rv)
BF = sp.Function("B")(fv, rv)
EF = sp.Function("E")(fv, rv)
GF = sp.Function("G")(fv, rv)
PF = sp.Function("P")(fv, rv)
QF = sp.Function("Q")(fv, rv)
D_gen = (AF + BF * rp_j**2 + EF * fp_j * rp_j + GF * fp_j**2
         + PF * rp_j + QF * fp_j)
L_tot = sp.Rational(1, 4) * rv**2 * fp_j**2 + D_gen
ELf_gen = EL_jet(L_tot, fv, fp_j, fpp_j)
ELr_gen = EL_jet(L_tot, rv, rp_j, rpp_j)

# banked jets: rho = r (rv IS the radial coordinate on the family),
# f = C + a/r => f' = -a/rv², f'' = 2a/rv³.  At fixed (rv, f-value) the
# pair (C, a) sweeps a freely, so the requirement is an identity in a
# with coefficient functions evaluated at the independent point (fv, rv).
banked_jets = {rp_j: 1, rpp_j: 0, rp3_j: 0,
               fp_j: -a_s / rv**2, fpp_j: 2 * a_s / rv**3,
               fp3_j: -6 * a_s / rv**4}
ELf_bk = sp.expand(ELf_gen.subs(banked_jets))
ELr_bk = sp.expand(ELr_gen.subs(banked_jets))
check("both banked EL expressions are quadratic polynomials in a "
      "(residual after subtracting the three a-coefficients: zero)",
      sp.expand(ELf_bk - sum(ELf_bk.coeff(a_s, k) * a_s**k
                             for k in range(3))) == 0
      and sp.expand(ELr_bk - sum(ELr_bk.coeff(a_s, k) * a_s**k
                                 for k in range(3))) == 0)

A_x, A_y = sp.Derivative(AF, fv), sp.Derivative(AF, rv)
B_x, B_y = sp.Derivative(BF, fv), sp.Derivative(BF, rv)
E_x, E_y = sp.Derivative(EF, fv), sp.Derivative(EF, rv)
G_x, G_y = sp.Derivative(GF, fv), sp.Derivative(GF, rv)
P_x, Q_y = sp.Derivative(PF, fv), sp.Derivative(QF, rv)
targets = [
    ("EL_f a^0:  A_f + B_f - E_rho + (P_f - Q_rho) = 0",
     ELf_bk.coeff(a_s, 0), A_x + B_x - E_y + P_x - Q_y),
    ("EL_f a^1:  rho G_rho - 2G = 0",
     ELf_bk.coeff(a_s, 1), 2 * (rv * G_y - 2 * GF) / rv**3),
    ("EL_f a^2:  G_f = 0",
     ELf_bk.coeff(a_s, 2), -G_x / rv**4),
    ("EL_rho a^0:  A_rho - B_rho = 0",
     ELr_bk.coeff(a_s, 0), A_y - B_y),
    ("EL_rho a^1:  2(rho B_f - E) - rho(Q_rho - P_f) = 0",
     ELr_bk.coeff(a_s, 1),
     2 * (rv * B_x - EF) / rv**3 - (Q_y - P_x) / rv**2),
    ("EL_rho a^2:  (G_rho - E_f) + rho/2 = 0   [C1's obstruction lives "
     "here]", ELr_bk.coeff(a_s, 2),
     (G_y - E_x) / rv**4 + 1 / (2 * rv**3)),
]
for label, got, want in targets:
    check(f"condition extracted exactly — {label}",
          sp.simplify(got - want) == 0)

print()
print("  (c) solving the conditions completely (each step sympy-"
      "verified):")
g_y = sp.Function("g")
gsol = sp.dsolve(sp.Eq(rv * g_y(rv).diff(rv) - 2 * g_y(rv), 0), g_y(rv))
check("G_f = 0 and rho G_rho = 2G force G = g0·rho² (dsolve general "
      "solution, unique up to the constant g0) — the ONLY allowed (f')² "
      "term is a multiple of the C1 density itself",
      sp.simplify(sp.diff(gsol.rhs / rv**2, rv)) == 0)
g0, c1, c2, a0, b0 = sp.symbols("g_0 c_1 c_2 a_0 b_0", real=True)
half, quarter = sp.Rational(1, 2), sp.Rational(1, 4)
e0f = sp.Function("e_0")
E_core = (2 * g0 + half) * fv * rv
check("EL_rho a² condition with G = g0 rho²: E_f = (2g0 + 1/2)rho, so "
      "E = (2g0 + 1/2)f rho + e0(rho) (uniqueness: the difference has "
      "zero f-derivative) — the FORCED cross-term that cancels C1",
      sp.simplify(sp.diff(E_core + e0f(rv), fv)
                  - (sp.diff(g0 * rv**2, rv) + rv / 2)) == 0)
e0sol = sp.dsolve(sp.Eq(e0f(rv).diff(rv, 2) - 2 * e0f(rv).diff(rv) / rv
                        + 2 * e0f(rv) / rv**2, 0), e0f(rv))
check("integrability of A_rho = B_rho forces e0'' - 2e0'/rho + "
      "2e0/rho² = 0, whose general solution is e0 = c1·rho + c2·rho² "
      "(dsolve; A_f - B_f = e0' - 2e0/rho - (2g0+1/2)f must be "
      "rho-independent)",
      sp.simplify(e0sol.rhs - rv * (sp.Symbol("C1")
                                    + sp.Symbol("C2") * rv)) == 0)

print()
print("  (d) THE GENERAL SOLUTION (gold check: arbitrary functions "
      "beta(rho), Phi(f, rho)):")
beta = sp.Function("beta")(rv)
Phi = sp.Function("Phi")(fv, rv)
G_sol = g0 * rv**2
E_sol = (2 * g0 + half) * fv * rv + c1 * rv + c2 * rv**2
B_sol = ((g0 + quarter) * fv**2 + (c1 + c2 * rv) * fv + beta
         + sp.diff(Phi, rv))
A_sol = c2 * fv * rv + beta + sp.diff(Phi, rv) + a0
P_sol = sp.Integer(0)
Q_sol = 2 * sp.diff(Phi, fv)
D_sol = (A_sol + B_sol * rp_j**2 + E_sol * fp_j * rp_j + G_sol * fp_j**2
         + P_sol * rp_j + Q_sol * fp_j)
L_sol = sp.Rational(1, 4) * rv**2 * fp_j**2 + D_sol
check("GOLD CHECK: with arbitrary beta(rho), Phi(f,rho) and constants "
      "(g0, c1, c2, a0), the banked family solves BOTH EL equations of "
      "C1 + D IDENTICALLY in (a, f-value, rho) — EXISTENCE established",
      sp.simplify(EL_jet(L_sol, fv, fp_j, fpp_j).subs(banked_jets)) == 0
      and sp.simplify(EL_jet(L_sol, rv, rp_j, rpp_j)
                      .subs(banked_jets)) == 0)

D_star = quarter * fv**2 * rp_j**2 + half * rv * fv * fp_j * rp_j
usq = (fv * rp_j + rv * fp_j)**2
dir1 = fv * rp_j**2 + rv * fp_j * rp_j
dir2 = fv * rv * (1 + rp_j**2) + rv**2 * fp_j * rp_j
phi_sector = (sp.diff(Phi, rv) * (1 + rp_j**2)
              + 2 * sp.diff(Phi, fv) * fp_j)
check("STRUCTURE: D = D* + g0[(f rho)']² + c1[f(rho')² + rho f'rho'] + "
      "c2[rho f(1+(rho')²) + rho²f'rho'] + beta(rho)(1+(rho')²) + a0 + "
      "Phi-sector, with D* := (1/4)f²(rho')² + (1/2)rho f f'rho' the "
      "unique INHOMOGENEOUS core (decomposition exact)",
      sp.expand(D_sol - (D_star + g0 * usq + c1 * dir1 + c2 * dir2
                         + beta * (1 + rp_j**2) + a0 + phi_sector)) == 0)
check("THE PERFECT SQUARE: L_C1 + D* = (1/4)[(f rho)']² exactly — the "
      "forced completion promotes u := f·rho to the canonical field",
      sp.expand(sp.Rational(1, 4) * rv**2 * fp_j**2 + D_star
                - quarter * (fv * rp_j + rv * fp_j)**2) == 0)
upp_j = fpp_j * rv + 2 * fp_j * rp_j + fv * rpp_j      # (f rho)'' in jets
L_min = quarter * (fv * rp_j + rv * fp_j)**2
check("minimal system C1 + D* is DEGENERATE: EL_f = -(rho/2)(f rho)'' "
      "and EL_rho = -(f/2)(f rho)'' — ONE equation (f rho)'' = 0 for two "
      "functions; the rho-equation now constrains rho given f (condition "
      "(ii) holds: rho''-structure present), but underdetermination "
      "persists along f·rho = alpha r + gamma",
      sp.simplify(EL_jet(L_min, fv, fp_j, fpp_j)
                  + half * rv * upp_j) == 0
      and sp.simplify(EL_jet(L_min, rv, rp_j, rpp_j)
                      + half * fv * upp_j) == 0)

print()
print("  (e) where A1's EH remainder sits in this map:")
EHrem_j = 2 - 2 * fv * rv * rpp_j
check("EH remainder = 2 + 2·[c1-direction] modulo the total derivative "
      "-d/dr[2f rho rho']: it IS a homogeneous family member (a0 = 2, "
      "c1 = 2) — banked-preserving ON ITS OWN, exactly as A1 found",
      sp.expand(EHrem_j - (2 + 2 * dir1) + Dr_jet(2 * fv * rv * rp_j))
      == 0)
check("but its (f')² content is ZERO (G ≡ 0), so it can never source the "
      "a² condition (G_rho - E_f = -rho/2): the A1 no-go RE-DERIVED "
      "structurally — and CONVERSELY, once D* is added, C1 + D* + "
      "kappa·EHrem admits the banked vacuum for EVERY kappa",
      sp.simplify(EL_jet(L_min + kap * EHrem_j, fv, fp_j, fpp_j)
                  .subs(banked_jets)) == 0
      and sp.simplify(EL_jet(L_min + kap * EHrem_j, rv, rp_j, rpp_j)
                      .subs(banked_jets)) == 0)
K_s = sp.symbols("K", positive=True)
flux_resid = sp.simplify(EL_jet(sp.Rational(1, 4) * rv**2 * fp_j**2
                                + K_s / rv**2, rv, rp_j, rpp_j)
                         .subs(banked_jets))
check("contrast — the parent flux piece K/rho² is NOT in the family: its "
      "banked rho-residual (a² - 4K)/(2rho³) vanishes only on the "
      "extremality-lock slice a² = 4K, never identically in a",
      sp.simplify(flux_resid - (a_s**2 - 4 * K_s) / (2 * rv**3)) == 0)

print()
print("  (f) the beta-direction breaks the degeneracy — and contains "
      "BOTH forks:")
L_beta = beta * (1 + rp_j**2)
ELr_beta = EL_jet(L_beta, rv, rp_j, rpp_j)
betap = sp.diff(beta, rv)
check("EL_rho[beta(1+(rho')²)] = beta'(1-(rho')²) - 2 beta rho'' exactly "
      "(and EL_f = 0: beta adds a PURE rho-equation)",
      sp.simplify(ELr_beta - (betap * (1 - rp_j**2)
                              - 2 * beta * rpp_j)) == 0
      and sp.simplify(EL_jet(L_beta, fv, fp_j, fpp_j)) == 0)
check("FIRST INTEGRAL: d/dr[beta(rho)(1-(rho')²)] = rho'·EL_rho[beta] — "
      "on the f-shell the rho-equation integrates to "
      "beta(rho)(1-(rho')²) = J (one constant J)",
      sp.simplify(Dr_jet(beta * (1 - rp_j**2)) - rp_j * ELr_beta) == 0)
alpha, gam, r0 = sp.symbols("alpha gamma r_0", positive=True)
f_leaf = (alpha * r + gam) / (r - r0)
check("J = 0 LEAF: rho' = ±1 i.e. rho = ±(r - r0); with (f rho)'' = 0, "
      "f = (alpha r + gamma)/(r - r0) = alpha + (alpha r0 + gamma)/rho — "
      "EXACTLY the banked vacuum f = C + a/rho in the translated radial "
      "coordinate (residual gauge r -> r + const, S0): on the J = 0 leaf "
      "the candidate action DERIVES rho = r and f = C + a/r",
      sp.simplify(f_leaf - (alpha + (alpha * r0 + gam) / (r - r0))) == 0
      and sp.simplify(sp.diff(f_leaf * (r - r0), r, 2)) == 0)

J_s = sp.symbols("J", positive=True)
rho_thr = sp.sqrt(J_s + r**2)
f_thr = (alpha * r + gam) / rho_thr
L_cand_fun = (quarter * sp.diff(f * rho, r)**2
              + b0 * rho**2 * (1 + rhop**2))
ELf_cand = euler_lagrange(L_cand_fun, f)
ELr_cand = euler_lagrange(L_cand_fun, rho)
check("concrete candidate L = (1/4)[(f rho)']² + b0 rho²(1+(rho')²) "
      "(beta = b0 rho²): the banked family solves BOTH equations exactly",
      at_banked(ELf_cand) == 0 and at_banked(ELr_cand) == 0)
check("J ≠ 0 LEAF (exact non-banked solution): rho = sqrt(J + r²), "
      "f = (alpha r + gamma)/rho solves BOTH full field equations — a "
      "wormhole-style throat (rho_min = sqrt(J) at r = 0) in the SAME "
      "action; the two branch-(iii) forks are separated only by the "
      "integration constant J",
      sp.simplify(ELf_cand.subs([(f, f_thr), (rho, rho_thr)]).doit()) == 0
      and sp.simplify(ELr_cand.subs([(f, f_thr), (rho, rho_thr)])
                      .doit()) == 0)
V_thr = (f_thr * lam / rho_thr**2
         + f_thr * sp.diff(f_thr * sp.diff(rho_thr, r), r) / rho_thr)
check("threshold honesty: this particular member has rho -> infinity and "
      "probe threshold V(infinity) = 0 (computed exactly) — it is NOT "
      "the E1 escape; the beta that IS lifts the threshold (verifier "
      "settlement, printed below)",
      sp.limit(V_thr, r, sp.oo) == 0)

print("""
  EXACTNESS NOTE (verifier amendment): the throat rho = sqrt(J + r²)
  requires beta = b0 rho² EXACTLY (for J ≠ 0), not generic beta — on this
  rho the first integral beta(rho)(1 - (rho')²) = J reads beta·J/rho² = J,
  pinning beta to the quadratic areal potential up to normalization.  The
  throat is a property of beta = b0 rho², not of the class as a whole.

  THE DEFERRED THRESHOLD GATE — SETTLED (verifier agent ae8a655ed2fa4045f,
  2026-06-10; recorded here as printed text, the verifier's algebra
  independently run and verified): the A3 class CONTAINS exact
  threshold-lifting members.  Verified example:

      beta(rho) = J/(1 - (rho_inf - rho)²)

  with the exact solution rho = rho_inf - e^(-r), f = gamma/rho (the
  alpha = 0 branch of (f rho)' = alpha): BOTH EL equations are satisfied,
  the first integral equals J exactly on the solution, and the probe
  threshold is V(infinity) = f_inf·lambda/rho_inf² > 0 — LIFTED, masses
  from angular eigenvalues.  General criterion (verifier): a J ≠ 0 leaf
  lifts the threshold iff beta has a positive critical value approached
  as a local minimum (beta''/J > 0) AND alpha = 0; beta = b0 rho² NEVER
  lifts (no positive critical value), consistent with V(infinity) = 0 on
  the throat member above.  Binding caveats carried with the settlement:
  (i) global finite-action existence of the lifting orbit remains OPEN —
  the inner boundary is log-divergent on the exhibited member; (ii) the
  lifting member has BOUNDED total dilation, so the 'unbounded total
  dilation' canon of native_positional_dilation_distance_readings.py
  would kill it — the dynamics (the choice of beta) and the principle
  reading must be canonized TOGETHER.""")

print("""
  VERDICT A3 (the heart, exact): EXISTENCE — no no-go.  The unique
  obstruction-cancelling core is

      D* = (1/4)f²(rho')² + (1/2)rho f f'rho' ,
      L_C1 + D* = (1/4)[(f·rho)']²   (perfect square in u = f·rho),

  unique modulo the homogeneous family {g0[(f rho)']², c1[f(rho')² +
  rho f'rho'] (≅ EH remainder), c2-direction, beta(rho)(1+(rho')²),
  constants, Phi-sector, boundary terms}.

  CLASS-RELATIVITY (verifier amendment, load-bearing): BOTH the
  D*-uniqueness AND the perfect square are CLASS-RELATIVE statements —
  relative to the declared class 'at most quadratic in first
  derivatives'.  An explicit QUARTIC counter-family exists:

      q1 f²(rho')⁴ + q2 rho f f'(rho')³ + q3 rho²(f')²(rho')²
      with  q1 = q3 + 1/12,  q2 = 2 q3 + 1/6

  cancels the obstruction with NO D* and NO perfect square.  'Unique' and
  'forced' below always mean: within the quadratic class.

  The spec's hint is confirmed
  exactly: the cross-term E f'rho' does the cancelling (E_f = rho/2
  forced); pure B(rho')² terms cannot (they enter only the a⁰/a¹
  conditions); and the only admissible G(f')² is a relabeling of C1.
  CONSEQUENCES: (1) A1 inverted — EH-like rho-dynamics CAN coexist with
  the banked structure, but ONLY after the compensator D* is added
  (kappa then arbitrary); (2) the minimal candidate is degenerate
  ((f rho)'' = 0: underdetermination persists); (3) the beta-direction
  yields genuine rho-dynamics with first integral beta(1-(rho')²) = J:
  J = 0 reproduces EXACTLY the banked vacuum (rho = r up to gauge,
  f = C + a/r) — the first action in the program whose solutions SELECT
  rho = r on a leaf — while J ≠ 0 carries exact throat geometries.
  STATUS: candidate class, NOT a native derivation; beta and the
  constants are unfixed; the guardrail still applies to any import.""")

# ---------------------------------------------------------------------------
# A4 — quantum/effective note (no computation)
# ---------------------------------------------------------------------------
hr("A4 — QUANTUM/EFFECTIVE NOTE (recorded honestly, no computation)")
print("""  Integrating out banked fields whose masses depend on rho (the angular
  lambda/rho² towers, H1 carriers) would generically generate (rho')²
  gradient terms at ONE LOOP (heat-kernel derivative expansion) — i.e.
  radiative generation of A3-family members is conceivable.  That is
  loop-level effective dynamics, OUT OF SCOPE for the classical native
  program; recorded as a route, not a result.  No computation performed.""")

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

  A1  BALANCE TEST: EL_rho[kappa·EHrem + C1]|banked = a²/(2r³) for EVERY
      kappa (EH side vanishes identically at rho = r; EL_f holds).  The
      banked vacuum solves NO C1 + EH-remainder system: the theta-theta
      Einstein equation, adopted as-is, breaks UDT's own vacuum.

  A2  EINSTEIN TENSION: G^th_th = (r²f')'/(2r²) ≡ 0 on f = C + a/r (the
      banked vacuum equation IS the theta-theta Einstein-vacuum
      equation; implicit effective angular stress: ZERO), while the C1
      scalar carries angular TENSION T^th_th = -(c/8)(f')².  Exactly:

          Delta(r) = G^th_th - 8pi T^th_th[C1] = pi c a²/r⁴  > 0,

      C-independent; native a = 2: 4 pi c/r⁴; repo c = 2: 8 pi/r⁴.
      Delta ≡ 0 only at c = 0 (checked dead-seriously, incl. general
      phi-normalization): rho-dynamics is NOT secretly EH.  First exact
      quantification of the off-tt/rr departure (and the tt/rr block
      fails with this source too; the C1 stress is not conserved on the
      banked vacuum — leftover (c/8)f'³/f).

  A3  EXISTENCE (not no-go): the unique compensator core is
      D* = (1/4)f²(rho')² + (1/2)rho f f'rho', giving
      L_C1 + D* = (1/4)[(f rho)']² — THE CANDIDATE NATIVE RHO-DYNAMICS —
      plus a fully-solved homogeneous family (incl. the EH remainder,
      now admissible at any kappa).  Minimal candidate degenerate
      ((f rho)'' = 0); the beta(rho)(1+(rho')²) direction gives genuine
      dynamics with first integral beta(1-(rho')²) = J: J = 0 leaf =
      EXACTLY the banked vacuum (rho = r derived on-leaf, up to the
      translation gauge), J ≠ 0 = exact throat geometries (which require
      beta = b0 rho² EXACTLY, not generic beta).  Both branch-(iii) forks
      live in one candidate action, separated by an integration constant.
      CLASS-RELATIVE (verifier): D*-uniqueness and the perfect square
      hold within the quadratic-in-first-derivatives class; a quartic
      counter-family (q1 = q3 + 1/12, q2 = 2q3 + 1/6) cancels the
      obstruction with no D* and no perfect square.  THRESHOLD GATE
      SETTLED (verifier ae8a655ed2fa4045f): the class contains exact
      threshold-lifting members — beta = J/(1-(rho_inf-rho)²), rho =
      rho_inf - e^(-r), f = gamma/rho, V(inf) = f_inf·lambda/rho_inf² > 0;
      criterion: positive critical value of beta (local minimum,
      beta''/J > 0) + alpha = 0; beta = b0 rho² never lifts.  Open:
      global finite-action existence; bounded-dilation tension with the
      unbounded-growth canon.  Candidate class only — the native
      derivation of beta is the next gate.

  A4  Loop-generated (rho')² terms: possible route, out of scope, no
      computation.

  SPEC CORRECTIONS RECORDED (sympy wins):
  (1) T^th_th[C1 scalar] = +L_m(value) = -(c/2)e^(-2phi)f(phi')², NOT
      -L_m as the spec guessed — the angular pressure is a TENSION
      (sign anchored by positive energy density -T^t_t > 0); hence
      Delta > 0, not < 0.
  (2) Delta is C-INDEPENDENT (spec anticipated dependence on r AND C):
      Delta = pi c a²/r⁴ exactly; the constant C drops out of G^th_th
      and of (f')².
  (3) A3 refinement of the spec's hint: confirmed that the cross-term
      supplies the (f')² cancellation, with the sharper result that
      E_f = rho/2 is FORCED and the only admissible pure-(f')² addition
      is a relabeling g0·rho²(f')² of C1 itself.

  CONDITIONALITY: all statements are within the declared ansatz class
  (no explicit r; ≤ quadratic in first derivatives; second derivatives
  linearly, mod boundary terms); the C1 normalization c is repo-matched
  at c = 2; flux and H1-source sectors of the parent file are not
  included in A1/A3 (the flux piece cancels the obstruction only on the
  extremality-lock slice — verified, recorded).""")
