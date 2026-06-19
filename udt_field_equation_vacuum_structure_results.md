# UDT Field-Equation Vacuum Structure — Scalar-Sector Verification

**Status:** OBSERVE / independently verified. **NOT canon** (Charles canonizes).
**Author:** verifier+doc-drafter agent (model: Opus 4.8 1M-context), 2026-06-18.
**Method:** independent re-derivation from scratch in sympy 1.13.1 (CPU, exact
symbolic), `/tmp/verify_udt.py`. No reuse of the external derivation's algebra;
Christoffel → Ricci → Einstein computed natively from the metric.

---

## 0. Scope framing (binding — do not soften)

This document characterizes the **VACUUM / GR side** of UDT's field equations
only. Every route registered below lands on the Schwarzschild geometry, or is
reverse-engineered to it. **NONE of these results is a departure from GR.** The
UDT departure — the matter source / coupling that makes the metric do something
GR's vacuum does not — is **NOT addressed here** and remains the open frontier
(Principle 7; SCAR: "UDT = GR in vacuum" is the parent theory sneaking back in,
which is *expected* on the vacuum side and tells us nothing about the source).

Three load-bearing caveats are carried with the survivors:

- **(i)** All routes are the vacuum/curvature side. The canonical metric
  `ds² = -e^{-2φ}c²dt² + e^{2φ}dr² + r²dΩ²` is exactly the Schwarzschild vacuum
  of standard Einstein, in the areal-`r` chart, with `e^{-2φ} = 1 - r_s/r`.
- **(ii)** The dilaton action `K(φ)=e^{-2φ}` (Claim 5) is **REVERSE-ENGINEERED**
  to reproduce the curvature equation. It is a repackaging that matches a known
  answer, **not an independent foundation**. It earns no evidential weight.
- **(iii)** `□_g φ = μ²φ` is a **PROBE / test-field** equation (a field
  propagating *in* the fixed geometry), **NOT φ's self-gravitating EOM.** This
  may bear on the cosmological-profile derivation — see §3.

---

## 1. Premise ledger (chose vs derived)

| Item | Status | Note |
|---|---|---|
| Metric form `-e^{-2φ}c²dt²+e^{2φ}dr²+r²dΩ²` | CHOSE (given; canon C-2026-06-18-1 elsewhere) | the object under test |
| `g_rr = e^{2φ} = 1/g^{tt}-mag = 1/(e^{-2φ})` (so `g^{rr}=e^{-2φ}=A`) | DERIVED from metric | the single-function `B=1/A` family |
| Coordinate chart = areal `r` (`g_θθ=r²`) | CHOSE (chart) | Birkhoff: round-static ⇒ Schwarzschild in this chart |
| Scalar action `S=∫√-g[-½ g^{mn}∂_m φ ∂_n φ - V]` | CHOSE (template) | the action whose EL we test two ways |
| "Probe" variation (g fixed) vs "self-consistent" (g built from φ) | the distinction being TESTED | not assumed — both computed |
| Dilaton `K(φ)` | DERIVED-to-match (reverse-engineered) | forced to `e^{-2φ}` by demanding curvature eq |
| `V=0` for vacuum branches | CHOSE (vacuum definition) | |
| `μ²` value (π/3) | NOT used here | inherited elsewhere; irrelevant to these identities |

---

## 2. Per-claim verdicts (independent sympy)

All "= 0" residuals below are exact symbolic zeros with `φ(r)` abstract.

| # | Claim | Verdict | Independent result |
|---|---|---|---|
| 1 | `G^t_t = G^r_r = (rA'+A-1)/r² = -(1/r²)[1-e^{-2φ}(1-2rφ')]`; `G^θ_θ = A''/2 + A'/r = e^{-2φ}[-φ''+2φ'²-2φ'/r]` (`A=e^{-2φ}`) | **CONFIRMED** | All four forms match; `Gtt-claim=0`, `Gthth-claim=0`, `G^t_t=G^r_r` exactly. |
| 2 | `□_g φ = (1/r²)(r²e^{-2φ}φ')' = e^{-2φ}(φ''+2φ'/r-2φ'²) = -G^θ_θ` | **CONFIRMED** | Both forms match; `□_g φ + G^θ_θ = 0` exactly (machine-exact identity). |
| 3 | Two EL forms from `S`: PROBE (g fixed) → `e^{-2φ}(φ''+2φ'/r-2φ'²)=V'` (coeff **-2**); SELF-CONSISTENT (φ is the metric field) → `e^{-2φ}(φ''+2φ'/r-φ'²)=V'` (coeff **-1**); difference `= e^{-2φ}φ'²` | **CONFIRMED** (sign note) | EL computed both ways. Probe EL = `□_g φ` (coeff -2). Self-consistent EL (varying the explicit `√-g·e^{-2φ}` density) gives coeff -1. `SELF_box - PROBE_box = +e^{-2φ}φ'²` exactly. (The "+" holds for SELF−PROBE; PROBE−SELF = −e^{-2φ}φ'². The magnitude/identity is exact; only the stated sign convention is ordering-dependent.) |
| 4 | Vacuum solutions DIVERGE: probe/curvature (coeff -2 or G=0) → `e^{-2φ}=1-r_s/r` (Schwarzschild); naive self-scalar (coeff -1) → `e^{-φ}=1-a/r` (different geometry) | **CONFIRMED** | `G^t_t=0` and `□_g φ=0` both hold at `e^{-2φ}=1-r_s/r`. Self-box`=0` holds at `e^{-φ}=1-a/r`. Cross-check: self-box at Schwarzschild `= r_s²/[4r³(r-r_s)] ≠ 0` — the two geometries are genuinely distinct. |
| 5 | Dilaton: `S=∫√-g[-½K(φ)g^{mn}∂φ∂φ - V]`, matching canonical metric forces `K=e^{-2φ}`; EL `e^{-4φ}(φ''+2φ'/r-2φ'²)=V'` ⇔ `□_g φ = e^{2φ}V'`; vacuum → `e^{-2φ}=1-r_s/r` | **CONFIRMED** | EL matches `e^{-4φ}(coeff -2)=V'`. Multiplying by `e^{2φ}` gives `□_g φ = e^{2φ}V'`. Vacuum (`V=0`) reduces to the coeff -2 equation ⇒ Schwarzschild; verified `=0` at `e^{-2φ}=1-r_s/r`. **REVERSE-ENGINEERED** — see caveat (ii). |
| 6 | Harmonic structure: with `v=e^{-2φ}`, vacuum eq → `v''+2v'/r=0` (flat-space radial Laplace); `v=1-r_s/r` satisfies it | **CONFIRMED** | `v''+2v'/r = -2·□_g φ` exactly (so the coeff -2 vacuum eq ⇔ flat radial Laplace in `v`). `(v''+2v'/r)|_{v=1-r_s/r}=0`. |
| 7 | EH on this one-function family is a pure boundary term: `r²R = d/dr[2r(1-A)-r²A']` (total derivative) ⇒ `∫√-g R` has no bulk φ-dynamics. `√-g = c r² sinθ` | **CONFIRMED** | `r²R - d/dr[2r(1-A)-r²A'] = 0` exactly. `√-g = c r²|sinθ|`. ⇒ the gravitational action on this family is a surface term; **gravity alone yields no bulk Euler-Lagrange law for φ**. |
| 8 | `□_g φ = μ²φ` is a PROBE/test-field equation, not φ's self-gravitating EOM | **CONFIRMED (scope judgment correct)** | Follows rigorously from Claims 2, 3, 7: `□_g φ` is the EL of the action with the metric held FIXED (Claim 3 probe), equivalently `-G^θ_θ` (Claim 2). φ's *self*-gravitating EOM, obtained when the φ-dependence of `g^{rr}=e^{2φ}` is varied, is the coeff **-1** operator, which differs by `e^{-2φ}φ'²`. So `□_g φ = μ²φ` is matter-in-geometry, not φ-as-metric-field. |

**Errors found in the external claims:** none of substance. One bookkeeping
note only: the "difference = +e^{-2φ}φ'²" in Claim 3 is the **SELF minus PROBE**
ordering; PROBE minus SELF is `-e^{-2φ}φ'²`. The identity itself is exact.

---

## 3. Headline survivors worth banking

1. **EH-on-this-metric-family is a boundary term (Claim 7).** Restricted to the
   single-function `B=1/A` family, `√-g R` is a total `r`-derivative. The
   Einstein–Hilbert action therefore contributes **no bulk dynamics for φ** on
   this family — gravity *alone* cannot fix φ's radial law; **a source / matter
   sector is required** to give φ a bulk equation of motion. (This is the
   structural reason the vacuum is degenerate-to-Schwarzschild and why the UDT
   departure must live in the source, not the curvature side. Connects to
   Principle 1 / Principle 7 and to the "you must add a source" frontier.)

2. **UDT vacuum = a harmonic field in `v = e^{-2φ}` (Claims 4, 6).** The vacuum
   reduces exactly to flat-space radial Laplace `v''+2v'/r=0`, solved by
   `v=1-r_s/r` (Schwarzschild). This is a clean native restatement of the vacuum
   sector — and a clean statement that the vacuum is *only* Schwarzschild.

3. **The probe/self-consistent fork (Claims 2, 3, 8).** `□_g φ` (coeff -2) is the
   fixed-background EL; the metric-field EL is coeff -1; they differ by exactly
   `e^{-2φ}φ'²`. `□_g φ = μ²φ` is therefore a **probe** equation.

---

## 4. Scope flag for the cosmological-profile derivation (action item — NOT a verdict)

The canonical screened scalar equation in `udt_canonical_geometry.md` §2.2
(lines 182–196) is built from the action
`S_φ = ½∫√-g[∇_μφ∇^μφ + μ²φ² - 2φS]` and its EL is written as
`(□_g - μ²)φ = -S`, i.e. radially
`(1/r²)(r²e^{-2φ}φ')' - μ²φ = -S` — the **coeff -2 / probe operator**. The
cosmological/canonical `φ(r)` profile (and the macro pipeline that consumes it:
`udt_validated_results.md`) is built on this equation.

By Claims 3 and 8, `□_g φ` is the EL **with the metric held fixed**. But in
that very action `g^{rr}=e^{-2φ}` is *built from the same φ being varied*. If φ
is playing a **self-gravitating** role (its own profile back-reacting through
the metric), the correct EL is the **coeff -1** operator
`e^{-2φ}(φ''+2φ'/r-φ'²) - μ²φ = -S`, which differs from the §2.2 equation by
`e^{-2φ}φ'²` — a term that is **NOT small** at hadronic/cosmic depth
(`e^{-2φ_0}≈5`, CR-45, line 294), so it cannot be neglected.

**Therefore:** *IF* the §2.2 screened equation is being used to set φ in a
self-gravitating role (φ as the metric's own field), that is a **scope error**
(probe operator used for a self-consistent problem). *IF* φ there is genuinely a
matter test-field propagating in a separately-fixed background, the probe
operator is correct and there is no error. **Which of these is the case is NOT
settled by this document** and must be checked against how §2.2's φ enters the
macro pipeline. This connects directly to the **macro CONDITIONS-CHANGED
question** (NEGATIVES_REGISTRY.md): if a scope error is confirmed, every macro
result resting on the §2.2 profile carries a changed premise and loses blocking
authority until re-graded on the self-consistent (coeff -1) operator.

This is registered as an **open action item / scope flag**, not a refutation.

---

## 5. Verifier-before-record stamp

- **Independent verification:** all eight claims re-derived from scratch in
  sympy by this agent (Christoffel/Ricci/Einstein computed natively from the
  metric, not reused). Script: `/tmp/verify_udt.py`. Result: Claims 1, 2, 4, 5,
  6, 7 CONFIRMED exact; Claim 3 CONFIRMED (sign-ordering note); Claim 8 scope
  judgment CONFIRMED. No substantive error found.
- **Adversarial checks run:** (a) `G^t_t = G^r_r` tested, not assumed; (b)
  probe vs self-consistent EL computed by independent variation of the explicit
  Lagrangian density, not by editing a coefficient; (c) the two vacuum
  geometries cross-checked (self-box ≠ 0 at Schwarzschild) to confirm genuine
  divergence rather than a trivial restatement; (d) `√-g` recomputed from
  `det g`.
- **Premises attached:** §1 ledger; all results carry the vacuum/GR-side scope
  tag (§0) and the reverse-engineered tag on the dilaton.
- **Not canon.** OBSERVE-stage. Awaits Charles.

— verifier+doc-drafter agent (Opus 4.8 1M-context), 2026-06-18
