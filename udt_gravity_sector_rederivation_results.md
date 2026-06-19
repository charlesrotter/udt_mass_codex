# UDT Gravity-Sector Re-Derivation — Did the c(phi)^4-on-R Coefficient Modify the FIELD EQUATIONS Themselves?

**Mode:** OBSERVE (CLAUDE.md "How we work"). Report WHAT IS THERE; no targeted
verdict. Adversarial re-do of the central step of
`udt_field_equations_derivation_results.md` under Charles's suspicion (now
charter Principle 7). Premises attached to every claim.

**Constructor:** Claude Opus 4.8 (1M), agent for udt_mass_codex, **2026-06-18**.
**Blind verifier:** agent `aa5b26b2f1969b055` (independent sympy from scratch) —
all four load-bearing claims CONFIRMED (see §8).

**Scripts (new, this push, nothing committed):**
`gravity_sector_variation.py`, `gravity_sector_minisuperspace.py`,
`gravity_sector_vacuum_solve.py`, `gravity_sector_slaved.py`,
`gravity_sector_newvacuum.py`, verifier `gravity_sector_verify_blind.py`.

---

## 0. THE SUSPICION (verbatim frame)

The prior doc concluded: "UDT's gravitational field equations do NOT depart
from GR; vacuum UDT = Schwarzschild/Birkhoff exactly; the whole modification is
one number `a` in the MATTER source weight." It wrote the field equation as
`G^μ_ν = (8πG/c(phi)^4) T^μ_ν` — i.e. it **DIVIDED THROUGH by c(phi)^4 as if
that coefficient were CONSTANT**. But `c(phi)=c0 e^{-2phi}` VARIES with position.
A position-varying coefficient `f(phi)=c(phi)^4/(16πG)` on `R` is a NON-MINIMAL
(scalar-tensor) coupling. Honest variation of `S=∫sqrt(-g)[f(phi)R + L_m]` gives

    f(phi) G_μν + (g_μν □ - ∇_μ∇_ν) f(phi) = (1/2) T_μν

The `(g□-∇∇)f` terms are the derivative-of-coefficient terms. **They do NOT
vanish in vacuum (T=0).** The prior derivation DROPPED them. That is the suspect
step.

---

## 1. PREMISE LEDGER (before compute) — chose / derived / assumed

| # | Item | Status |
|---|---|---|
| A1 | **The Einstein–Hilbert R-term is the right native starting point** for the gravity action | **ASSUMED — NOT resolved.** This is itself a possible Principle-7 smuggle (defaulting to GR's action FORM). I do NOT resolve it; I take the action the prior doc wrote, `S=∫sqrt(-g)[f(phi)R+L_m]`, and ask whether — *even granting the EH R-term* — the variation was done honestly. If the answer is "no" *with the EH form granted*, the suspicion is vindicated a fortiori. FLAG: a fully native gravity action could differ further. |
| A2 | `f(phi)=c(phi)^4/(16πG)=(c0^4/16πG)e^{-8phi}` | **From the prior doc's own action** (c promoted in the coupling). Taken as given to test that doc on its own terms. |
| A3 | phi is the dilation field; appears IN the metric (`g_tt=-e^{-2phi}c0^2`, `g_rr=e^{2phi}`) | **DERIVED** elsewhere (CANON C-2026-06-18-1, "remain relativistic"). |
| A4 | metric form `g=diag(-e^{-2phi}c0^2, e^{2phi}, r^2, r^2 sin^2θ)` | static/spherical/diagonal/areal-r = **CHOSE** (CANON C-2026-06-18-1: four un-forced choices). |
| A5 | B=1/A lock `g_tt g_rr = -c0^2` | **DERIVED** (prior). NB: tested both WITH the lock (single DOF) and WITHOUT (two free functions N,L) — verdict identical (§5). |
| A6 | No explicit scalar kinetic/potential term for phi in the Jordan action as written | **From the prior doc** (its action has only `f(phi)R + L_m`). FLAG: this is a CHOSE that matters for the phi-equation; a native action might add `(∇phi)^2`. |
| A7 | Signs/normalization of the scalar-tensor field eqn | **CONVENTION** (standard `f G + (g□-∇∇)f = ½T`; the load-bearing facts — non-vanishing of E, Schwarzschild failure — are sign-independent: they are "≠0" statements). |

**The decisive choice flagged up front:** whether phi is an INDEPENDENT field or
SLAVED to the metric (it IS essentially the lapse). §4 tests BOTH; the verdict is
the same either way.

---

## 2. THE FULL FIELD EQUATIONS — with the ∇∇f terms shown (DERIVED)

For `g=diag(-e^{-2phi}c0^2, e^{2phi}, r^2, r^2 sin^2θ)` (script `gravity_sector_variation.py`):

**Bare Einstein tensor (mixed):**
```
G^t_t = G^r_r = e^{-2phi}(-2 r phi' - e^{2phi} + 1)/r^2
G^θ_θ = G^ψ_ψ = e^{-2phi}(2 r phi'^2 - r phi'' - 2 phi')/r
G^t_t - G^r_r = 0   identically                              [the B=1/A consequence]
```

**The dropped scalar-tensor term** `E_μν = (g_μν □ - ∇_μ∇_ν) f`, with
`f=(c0^4/16πG)e^{-8phi}`. Box f and E are NONZERO:
```
Box f = (c0^4/πG) e^{-10phi} [ r(10 phi'^2 - phi'')/2 - phi' ] / r

E^t_t / f = 8 e^{-2phi} (9 r phi'^2 - r phi'' - 2 phi') / r
E^r_r / f = 8 e^{-2phi} (r phi' - 2) phi' / r
E^θ_θ / f = E^ψ_ψ / f = 8 e^{-2phi} [ r(10 phi'^2 - phi'') - phi' ] / r
```

**The HONEST full vacuum equation** is `f G^μ_ν + E^μ_ν = 0`, i.e. (divide by f):
```
EQ_tt   = e^{-2phi}( 72 r^2 phi'^2 - 8 r^2 phi'' - 18 r phi' - e^{2phi} + 1 )/r^2 = 0
EQ_rr   = e^{-2phi}(  8 r^2 phi'^2          - 18 r phi' - e^{2phi} + 1 )/r^2 = 0
EQ_θθ   = e^{-2phi}( 82 r phi'^2 -  9 r phi''          - 10 phi' )/r          = 0
```
Compare to the prior doc, which (dropping E) had only `G^μ_ν = 0`. **The E terms
add the `phi'^2`, extra `phi''`, and extra `phi'` pieces.** Most cleanly, the
combination that GR forces to vanish identically is NOW nonzero:
```
(G + E/f)^t_t - (G + E/f)^r_r = 8 (8 phi'^2 - phi'') e^{-2phi}     ≠ 0
```
**This single line is the whole result:** in GR/Birkhoff `G^t_t - G^r_r = 0` is
what (with the field equations) forces `B=1/A` and ultimately Schwarzschild. The
honest UDT vacuum equation replaces that identity-zero with a genuine
`8 phi'^2 - phi'' = 0` constraint. The gravity sector IS modified, in vacuum.

---

## 3. SCHWARZSCHILD IS NO LONGER A VACUUM SOLUTION (DERIVED; blind-confirmed)

Substitute the Schwarzschild profile `phi_schw = -1/2 ln(1 - r_s/r)` (the φ that
makes the metric the standard, Ricci-flat Schwarzschild) into the full vacuum
equation. Because Schwarzschild is Ricci-flat, `G^μ_ν = 0` there — so `f G = 0`
and the **entire residual is the dropped E term** (script `gravity_sector_vacuum_solve.py`):
```
EQ_tt(schw)   = 14 r_s^2 / (r^3 (r - r_s))                    ≠ 0
EQ_rr(schw)   =  2 r_s (4r - 3 r_s) / (r^3 (r - r_s))         ≠ 0
EQ_θθ(schw)   =  4 r_s (5 r_s - r) / (r^3 (r - r_s))          ≠ 0
```
(Equivalently, the dimensionful E itself: `E_tt(schw)=7c0^4 r_s^2 (r-r_s)^3/(8πG r^7)`, etc.)

**Schwarzschild FAILS the honest vacuum equation.** Flat space (`phi=0`) DOES
solve it (E=0 and G=0). The "vacuum = Schwarzschild/Birkhoff exactly" claim of
the prior doc was a direct consequence of dropping E.

---

## 4. THE DECISIVE QUESTION — STATUS OF phi (won here)

phi is not a freely-postulated independent scalar; it sits INSIDE the metric. So
is `f(phi)R` a GENUINE non-minimal coupling, or is `c(phi)^4` a conformal/units
factor transformable away? Tested three ways; **all give the same answer.**

### (a) CONFORMAL / EINSTEIN-FRAME removability — NOT pure relabeling
(script `gravity_sector_minisuperspace.py` §A.) Conformal map `g = Ω^2 ḡ` with
`Ω^2 = F(phi) = e^{-8phi}` (the c^4 prefactor) sends `f(phi)R` to a canonical
`R̄` PLUS a scalar KINETIC term with coefficient
```
(3/2)(F'/F)^2 = (3/2)(−8)^2 = 96   (nonzero constant)        [DERIVED]
```
The c^4 prefactor does NOT vanish under conformal transformation — it **deposits
a dynamical scalar kinetic term `96 (∇phi)^2`** in the Einstein frame. This is
precisely the Brans–Dicke situation: conformally relatable to GR, but NOT GR
(Brans–Dicke is genuinely a different theory). The c^4 is **not** absorbable the
way a pure units/coordinate factor would be. The prior doc's "folds into the
lapse / units choice" reasoning was correct for c IN THE METRIC's g_tt alone
(that IS reparametrization), but WRONG for `c^4` MULTIPLYING R in the action —
which is the thing that actually controls the field equations.

> **This pinpoints the exact error.** The prior doc proved "varying-c in the
> metric is absorbable" (true) and then silently transferred that conclusion to
> "varying-c^4 on R is absorbable" (FALSE). The first is a chart statement; the
> second is a non-minimal coupling. Different objects.

### (b) INDEPENDENT-FIELD variation — a new vacuum phi-equation GR lacks
(script `gravity_sector_vacuum_solve.py`.) Varying the Jordan action w.r.t. phi
as independent (no kinetic term, A6) gives the scalar equation
```
f'(phi) R = 0   =>   R = 0   (since f' = -8 f ≠ 0)            [DERIVED]
```
GR has NO such vacuum scalar equation. Schwarzschild satisfies `R=0` — but then
the METRIC equation still demands `E_μν = 0`, which Schwarzschild violates
(§3). So the system is **over-determined relative to GR**: a genuine new vacuum
constraint. (Caveat A6: with a native `(∇phi)^2` kinetic term the phi-equation
would read `f' R = (kinetic EOM)` instead of `R=0`; this strengthens, not
weakens, "vacuum ≠ GR".)

### (c) SLAVED variation (phi = the metric's own DOF) — Schwarzschild STILL fails
(script `gravity_sector_slaved.py`.) The honest "phi-slaved" treatment: take the
action a function of the metric only (`f=N^4/16πG`, `N=-g_tt`), keep TWO free
functions `N(r),L(r)` (so the Hamiltonian/constraint equation is NOT lost — a
known minisuperspace pitfall), vary each freely, THEN impose Schwarzschild:
```
EL_N(schw) = -7 c0^3 r_s^2 (r - r_s)^2 / (8πG r^4)           ≠ 0
EL_L(schw) =  (nonzero, same (r-r_s)/r^6 structure)          ≠ 0
EL_N(flat) = EL_L(flat) = 0                                   (flat solves it)
```
**Schwarzschild fails even in the fully slaved, metric-only treatment.** The
verdict does not depend on whether phi is independent or slaved.

> Caveat noted: the single-DOF *locked* minisuperspace (B=1/A imposed BEFORE
> varying) gives a misleadingly trivial bare EOM (`f=const ⇒ EL≡0`), because
> imposing the lock first discards the constraint equation. That is exactly the
> trap that can make "vacuum=GR" look true. The two-function free variation
> (constraint retained) is the honest computation, and it says Schwarzschild
> fails. The full covariant tensor equations (§2–3) agree component-by-component.

---

## 5. THE NEW VACUUM STRUCTURE — over-constrained; no nontrivial asymptotically-flat solution

(script `gravity_sector_newvacuum.py`.) The two independent vacuum equations
(EQ_θθ and EQ_tt) must hold simultaneously. EQ_θθ alone integrates exactly:
```
phi'(r) = 1 / ( C1 r^{10/9} + 82 r )                          [DERIVED, EQ_θθ only]
```
— note the **non-GR exponent 10/9**, novel structure absent from Schwarzschild.
But imposing EQ_tt as the constraint on top: numerically, the tt-constraint
canNOT be held to zero along the EQ_θθ family for any nonzero seed `phi'(r0)`;
**only `phi'≡0` (flat space) satisfies both.** Within this static-SSS-diagonal
slice (premises A4/A5), the honest vacuum equations are OVER-CONSTRAINED relative
to GR: they admit flat space but NO nontrivial asymptotically-flat vacuum (no
Schwarzschild, no massive vacuum profile).

PHYSICAL READ (honest, OBSERVE — not manufactured): the modification makes vacuum
STIFFER, not richer, in this slice. The extra `(g□-∇∇)f` terms suppress isolated
vacuum mass rather than create it. This is consistent with — but does NOT by
itself prove — the critical-energy picture (mass needs matter present) AND with a
global boundary-tension reading: a stiffer vacuum is what would hold a static
configuration "apart from collapse." See §6 honesty note.

---

## 6. THE BOUNDARY-TENSION / ANTI-COLLAPSE READ (honest, un-manufactured)

Charles's gravity hypothesis: a global anti-collapse "boundary tension" (a
Λ-replacement; dovetails with `c^2 = 2GM/r*` and the critical-universe frame).
**Does the surviving math produce such a term?**

- **What IS there (DERIVED):** the surviving vacuum terms are
  `8(8 phi'^2 - phi'') e^{-2phi}` in `(G+E/f)^t_t-(G+E/f)^r_r`. The structure is
  a **gradient-energy stiffness** of the dilation field — `phi'^2` (gradient
  squared) and `phi''` (curvature of phi). In the Einstein frame this is exactly
  the `96 (∇phi)^2` scalar kinetic term (§4a). A scalar gradient energy
  filling space is **the right KIND of object** for a global tension / vacuum-
  stress effect: a Brans-Dicke scalar's gradient energy gravitates and can act
  Λ-like in cosmological settings.
- **HONEST LIMITS:** (i) NO explicit constant-Λ term appeared (no `g_μν Λ` with
  constant Λ); what appeared is a field-gradient stress, not a cosmological
  constant. (ii) The "boundary's large mass holds the universe apart" mechanism
  is a GLOBAL/cosmological-boundary statement; this static-SSS-slice calculation
  cannot confirm it — it only shows the LOCAL field equations now carry a scalar
  stress that GR lacks. (iii) I did NOT manufacture a Λ; I report that the
  surviving term is a phi-gradient stiffness, which is *compatible with* but not
  *proof of* the anti-collapse picture. Testing the actual boundary-tension
  mechanism needs the cosmological (non-static or finite-cell-boundary) sector,
  out of this slice's scope.

> **Net:** the math DOES produce a new gravitating object in the vacuum sector (a
> phi-gradient/Brans-Dicke scalar stress), of the right kind to host Charles's
> boundary-tension idea — but it does not, in this static slice, hand over a
> ready-made Λ-replacement. Direction supported; not yet derived.

---

## 7. VERDICT — fully scoped

> **OUTCOME (A): YES — vacuum UDT departs from GR.** The `(g_μν□-∇_μ∇_ν)f(phi)`
> terms SURVIVE in vacuum, are NONZERO, and are NOT removable by conformal/units
> transformation (the Einstein-frame kinetic coefficient is `96`, not zero).
> Schwarzschild is **not** a vacuum solution of the honest equations (it fails by
> a residual that is entirely the dropped E term). The honest static-SSS vacuum
> is over-constrained and admits only flat space. **The prior doc's
> "vacuum = Schwarzschild/Birkhoff exactly" is an ERROR caused by dropping the
> derivative-of-coefficient terms** — exactly Charles's suspicion (Principle 7).

**Where the error lived (precise):** the prior doc correctly showed varying-c
*in the metric's g_tt* is absorbable (a chart statement), then illegitimately
carried that to varying-`c^4` *multiplying R in the action* (a non-minimal
coupling). It then wrote `G=(8πG/c^4)T` — dividing by `c^4` as if constant —
which is only valid for constant `c^4`. The `∇∇f` terms are precisely what that
division discards.

**Scope / premises that this verdict rides on:**
- Granted the EH R-term action (A1) — UNRESOLVED whether that is itself a
  Principle-7 smuggle; the verdict is "even granting GR's R-term, the variation
  was dishonest and vacuum departs."
- Granted the prior doc's `f=c^4/16πG` coupling (A2). If a NATIVE gravity action
  puts c elsewhere (or not as `c^4` on R), the specific exponent `-8` (hence the
  `96`, the `10/9`, the `8phi'^2-phi''`) changes — but ANY non-constant
  coefficient on R gives surviving `∇∇f`≠0, so "vacuum ≠ GR" is robust to the
  exact power; only the numbers move.
- Static / spherical / diagonal / areal-r slice (A4) and B=1/A (A5) — verdict
  holds WITH and WITHOUT the lock (§4c).
- A6 (no native phi kinetic term in the Jordan action): adding one strengthens
  "vacuum ≠ GR" (more scalar dynamics), never restores GR.

**What is NOT claimed:** I do NOT claim to have derived the correct NATIVE gravity
action (A1 open). I do NOT claim a cosmological-constant / boundary-tension term
was derived (only a phi-gradient stress of the right kind, §6). I do NOT claim
the over-constraint is the final word once matter (T≠0) or the non-static /
finite-boundary sectors are included.

**Consequence for the prior program:** the entire "a-in-the-matter-source"
framing was looking in the WRONG sector. The modification is in the
GRAVITY/CURVATURE sector and is present **in vacuum**, independent of the matter
exponent `a`. The bare-vacuum no-go's (#62/#63, "vacuum is barren as in GR")
carried the premise "vacuum=GR/Schwarzschild" — that premise is now
CONDITIONS-CHANGED and those negatives lose blocking authority until re-graded
under the honest (E-retained) vacuum equations (flag for NEGATIVES_REGISTRY).

---

## 8. BLIND VERIFIER — 2026-06-18 (agent aa5b26b2f1969b055)

Independent sympy from scratch (`gravity_sector_verify_blind.py`); read no
constructor code. **All four load-bearing claims CONFIRMED:**
- (a) `E_μν` NONZERO in vacuum — PASS (gave `E^r_r=c0^4(rphi'-2)phi'e^{-10phi}/(2πGr)` etc.).
- (b) Schwarzschild FAILS the full vacuum equation — PASS (`f G=0` since Ricci-flat;
  residual = E alone: `EQ^t_t=7c0^4 r_s^2(r-r_s)^3/(8πGr^7)` etc., nonzero).
- (c) Flat space solves it — PASS.
- (d) Reduced-action (free N,L) cross-check AGREES with covariant tensor computation — PASS.
Verifier scoping note (accepted): this verifies the stated scalar-tensor metric
equation as written (Brans-Dicke, ω=0 in this gauge, scalar EOM not co-imposed) —
consistent with the task. No counter-expressions; nothing flagged wrong.

---

## 9. SINGLE CLEANEST STATEMENT

> A position-varying coefficient `f(phi)=c(phi)^4/(16πG)` on the curvature `R` is
> a non-minimal (scalar-tensor) coupling. Varying the action honestly keeps the
> derivative-of-coefficient terms `(g_μν□-∇_μ∇_ν)f`, which are NONZERO in vacuum.
> The prior doc dropped them (by writing `G=(8πG/c^4)T`, dividing by `c^4` as if
> constant) and so reported "vacuum=Schwarzschild/Birkhoff exactly." Carrying the
> terms: `(G+E/f)^t_t-(G+E/f)^r_r = 8(8phi'^2-phi'')e^{-2phi}` replaces GR's
> identity-zero; Schwarzschild is no longer a vacuum solution (it fails by the
> dropped term, `14 r_s^2/(r^3(r-r_s))`); the Einstein-frame map deposits a
> nonzero scalar kinetic term (coefficient 96), proving the c^4 is NOT pure
> relabeling. **VERDICT (A): vacuum UDT departs from GR in the gravity/curvature
> sector** — vindicating Charles's suspicion (Principle 7). The surviving object
> is a phi-gradient/Brans-Dicke scalar stress, the right kind of thing to host
> the boundary-tension/anti-collapse hypothesis, though a literal Λ-replacement
> was not derived in this static slice. The modification is independent of the
> matter exponent `a`; the "a-in-the-matter-source" framing was the wrong sector.
> Scope: granted the EH R-term (A1, unresolved Principle-7 question) and the
> prior `c^4` coupling (A2); robust to B=1/A and to phi-independent-vs-slaved.

---

## CORRECTION (2026-06-18, Charles-approved, driver-appended) — THIS DOC ANALYZES AN ACTION UDT DOES NOT USE

This derivation ASSUMED the action `S = ∫√-g[c(phi)^4/(16πG) R + L_m]` (a
non-minimal `f(phi)R` coupling) and asked what it implies. That premise is the
whole content: the validated corpus (`udt_validated_results.md` line 3064)
states UDT's gravity action is standard Einstein-Hilbert + a MINIMALLY-coupled
scalar — explicitly "no `f(phi)R`". The companion local-reduction analysis
(`gravity_sector_local_reduction_results.md`) shows the `f(phi)R` action gives
PPN γ=9 (light bending ~5× observed) — KILLED by the solar-system/Cassini bound.
=> The ONLY takeaway of this doc: the assumed `c^4·R` (`f(phi)R`) action is
solar-system-falsified and is NOT UDT's gravity sector. The headline "vacuum
UDT departs from GR" is a statement about that falsified action, NOT about UDT.
Logged as a dead-end. The live program (Charles, 2026-06-18): derive UDT's
field equation NATIVELY from the dilation-carrying metric — action downstream,
no assumed action, no cosmological constant — anchored on the `□φ−μ²φ=−S`
φ-equation. NOT canon.
