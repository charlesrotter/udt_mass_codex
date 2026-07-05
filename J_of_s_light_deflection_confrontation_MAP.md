# J(s) LIGHT-DEFLECTION CONFRONTATION — pre-registration MAP (data-blind)

**Status: BANKED — BLIND-VERIFIED (verifier a66e2da69bfc3c7d9, 2026-07-05: OVERALL sound + non-smuggled
+ data-blind + non-targeting; J(s) math independently re-derived correct; one-body null deflection
confirmed OWED; category discipline sound; GR reference-only; no-retuning genuine. ONE required
correction FOLDED IN: the ambient "deflection = J(s)−π, impact-parameter-independent" was mis-tagged
DERIVED — the swept azimuth is D(ρ₀)·J(s) with D b-dependent + gauge-carrying and s=0 conical, so ONLY
the pure NUMBER J(s) is b-independent; the measured ambient deflection is OPEN, folded into
CF-ABS/CF-ORIGIN. Same latent overstatement flagged in banked R2 row R2-1 for consistency.) NOT yet
data-confronted. STRICTLY DATA-BLIND (grep-clean). This is a FROZEN pre-registration contract; the
actual data load (Cassini / VLBI / any bound) is the NEXT, separately-gated step — and is itself gated
behind first deriving the OWED one-body null deflection (§1.2).**

**Scope.** The derivation half of the *ambient* vacuum deflection `J(s)` is ALREADY BANKED +
blind-verified (R2, `r2_prereg_s_dependence.md`, verifier a82dd36ef191768dd; CAS `r2_final_cas.py`
S7a–d/S10b). This MAP builds the DATA-CONFRONTATION PLAN that R2 explicitly deferred, consolidates
the native derivation path, and — importantly — SEPARATES two distinct frame-robust light
observables that must not be conflated, and finds that the second one (the one that actually
confronts solar-system deflection data) is **OWED, not yet derived**.

**Contract lineage.** `LIVE.md` CURRENT-STATE RESUME-HERE (2026-07-05, Charles): "the J(s)
light-deflection MAP — pre-register the frame-robust J(s) prediction (native derivation path,
allowed parameters, Cassini/solar-system comparison PLAN, clean failures, no-retuning rule), MAP
ONLY / NO data run yet, preserve the s=2μ/Z fork explicitly, GR only as a comparison reference (no
ΛCDM/GR derivation import, no fitting), define what observation falsifies/constrains EACH branch,
blind-verify before any data comparison."

---

## 0. THE LOAD-BEARING PHYSICS DISTINCTION (read before any confrontation row)

There are **TWO** frame-robust light observables in UDT. They are BOTH frame-robust for the SAME
reason (null geodesics are conformally invariant under `ĝ = e^{2φ}g`, so the g-vs-ĝ frame fork of
R2 §0 does not touch them — S10b). But they are **DIFFERENT PHYSICS** and confront **DIFFERENT
DATA**. Conflating them is a category error (pre-registered as clean failure CF-CAT below).

**(i) The AMBIENT vacuum sector — the pure NUMBER `J(s)` is b-independent, but the MEASURED azimuth
is NOT (verifier-corrected, a66e2da69bfc3c7d9).**
A property of the s-deformed vacuum ITSELF, with NO central body. A null ray in the ambient s-vacuum
sweeps a total coordinate azimuth `Δχ = D(ρ₀)·J(s)` between its asymptotes, where
`J(s)=2∫₀¹dw/√(1−w^{2−2s})` is a **pure, impact-parameter-INDEPENDENT NUMBER**, but
`D(ρ₀)=(e^{φ₀}/a)·ρ₀^{−s}=Δρ₀^{−s}` is a **b-DEPENDENT, GAUGE-carrying ruler prefactor** — the turning
point ρ₀ is fixed by the impact parameter (`d ln D/d ln b = s/(s−1) ≠ 0` for s>0), and `Δ=e^{φ₀}/a` is
integration data, never theory-fixed (R2 §2/S4c). ⚠ **So ONLY the number J(s) is
impact-parameter-independent — NOT the swept azimuth, NOT "the deflection."** And at s=0 the azimuth
is `Δ·π` (it equals π only in the normalized gauge Δ=1): the ambient space is a **CONE**
(proper-circumference/radius = 2π/Δ), so any excess-over-π is partly a CONICAL / gauge artifact, not a
clean deflection. **⇒ the ambient "deflection" is NOT simply `J(s)−π` and is NOT shown to be a
b-independent, gauge-invariant observable — tagged OPEN (folded into CF-ABS/CF-ORIGIN), NOT derived.**
What IS derived+banked and robust: the pure number `J(s)` and its values (`J(0)=π`, `J(½)=4`,
slope π(1−ln2)). This is UNLIKE GR either way (GR has no impact-parameter-independent vacuum deflection).

**(ii) The ONE-BODY / solar deflection — IMPACT-PARAMETER-DEPENDENT.**
From a central mass `M = −q` (the banked one-body exterior, R2 §3 / S3), a null ray bends by an
angle that DECREASES with impact parameter (∝ 1/b at leading order, GR-like). This is the quantity
Cassini / VLBI actually measure as PPN-γ. It is built on null geodesics of the **M=−q exterior
metric** (lapse `e^{−2φ̃} = e^{−2φ̃∞}(1 + 2q̂/x + 2q̂²/x² + …)`, `q̂ = −νβ`, `ν = 2√(Z+μ²)/Z`,
S3d). **This deflection has NOT yet been computed** — S3 derives the exterior *fields* and the
*lapse*, S9 derives the one-body *timelike orbits* (Kepler / precession), but **no S-check evaluates
the NULL-geodesic deflection integral on the M=−q metric.** It is **OWED** (see §1.2, §8).

**The confrontation consequence (the whole point of this MAP).** The observable that constrains
`s` is (i), which is impact-parameter-INDEPENDENT — and it is an open question whether an
impact-parameter-independent, cosmic-center-referenced deflection even ENTERS a differential
solar-system angle-vs-elongation measurement (it may be absorbed into calibration / aberration /
absolute-frame reference; see CF-ABS). The observable that Cassini/VLBI directly bound is (ii),
which constrains the **one-body M/q sector**, NOT `s`. **Do NOT claim "Cassini bounds s" until it
is shown that the ambient deflection is separately observable; at leading analysis Cassini bounds
the one-body sector.** Keeping (i) and (ii) on SEPARATE confrontation tracks is the load-bearing
discipline of this MAP.

---

## 1. NATIVE DERIVATION PATH

**Frame (CHOSE-cited, canon C-2026-06-18-1):** `ds² = −e^{−2φ}c²dt² + e^{+2φ}dr² + ρ²dΩ²`.
Reduced-G Lagrangian `L̄_G = (Z/2)ρ²φ'² + 2μρρ'φ' + 2 − 2ρ'²`; flux `Φ = Zρ²φ' + 2μρρ'`;
`s = 2μ/Z`; native point weight `a(φ)=e^{+φ}` (`native_dilation_weight_derivation_results.md` D2,
DERIVED STATIC-ONLY). NO ΛCDM/GR law is imported anywhere below; GR appears ONLY as a labelled
comparison curve in §3.

### 1.1 The ambient deflection J(s) — DERIVED (banked, re-confirmed here)
Branch-G ambient ("flat-analog") vacuum: `ρ = ar + b`, `φ = φ₀ − s·ln ρ`, so in areal coordinates
`A(ρ) ≡ −g_tt/c² = e^{−2φ₀}ρ^{2s}`, `B(ρ) ≡ g_ρρ = e^{2φ₀}ρ^{−2s}/a²`, with `A·B = 1/a²` (form
reciprocity survives, S5a). Null geodesics: conserved `E = Ac²t'`, `L = ρ²(dχ/dλ)`; the null
condition `−Ac²t'² + Bρ'² + ρ²χ'² = 0` gives, with `u = 1/ρ`, the exact orbit equation

  `(du/dχ)² = a²[E²/(L²c²) − e^{−2φ₀}u^{2−2s}]`   (S7a; `A·B=1/a²` collapses the B-factor).

The total swept azimuth between turning points, substituting `w = u/u₀`, factorizes as
`Δχ = D(ρ₀)·J(s)` where the PURE NUMBER is impact-parameter (b = L/E) — INDEPENDENT:

  `J(s) = 2∫₀¹ dw/√(1 − w^{2−2s}) = √π·Γ(1/(2−2s)) / [(1−s)·Γ(1/(2−2s)+½)]`

while the prefactor `D(ρ₀)=Δρ₀^{−s}` (Δ=e^{φ₀}/a) is b-dependent + gauge-carrying (see §0(i);
`r2_final_cas.py:201` "swept azimuth = D(rho0)·J(s)"). **Only J(s) is b-independent; the swept azimuth
is not.**

**Re-confirmed symbolically THIS push (sympy, independent of `r2_final_cas.py`):**
- `J(0) = π` (exact) — the flat straight-line value ⇒ zero deflection at s=0. ✔
- `J(½) = 4` (exact closed form AND `2∫₀¹dw/√(1−w) = 4` numerically) — the Route-B point. ✔
- small-s `J(s) = π[1 + (1−ln2)s + O(s²)]` (exact series match). ✔
- integral-vs-closed-form agree to ~1e-9 at s = 0, ¼, ½. ✔

**Candidate deflection `δ_amb(s) = J(s) − π`** (`= π(1−ln2)s + O(s²)` at small s; `δ_amb(½)=4−π`) is
the NAIVE azimuth-excess of the pure number — but per §0(i) the MEASURED azimuth carries the
b-dependent, gauge-carrying `D(ρ₀)` factor and a conical piece at s=0, so `δ_amb=J(s)−π` is **OPEN as
an observable, NOT derived** (CF-ABS/CF-ORIGIN). **Robustness:** the null geodesic equation from
`ĝ=e^{2φ}g` is identical to that from `g` (S10b) ⇒ the pure number `J(s)` is **frame-robust AND
motion-law-robust**; but a quantity whose observable meaning is unresolved (attack #2) is only as
robust as it is well-defined — the frame-robustness of "the measured ambient deflection" is contingent
on the §0(i) OPEN item being settled.

### 1.2 The one-body / solar deflection — DERIVATION PATH (OWED)
The banked one-body exterior (R2 §3 / S3, attractive branch σ=+1) gives `M = −q = νβ√E > 0` and the
exponential lapse `e^{−2φ̃} = e^{−2φ̃∞}(1 + 2q̂/x + 2q̂²/x² + …)`, `q̂ = −νβ`, `ν = 2√(Z+μ²)/Z`
(S3c/d). The metric functions for the one-body null problem are
`A_body(ρ) = e^{−2φ̃}ρ^{2s}` (S9 uses `A(x)=e^{−2νartanh(β/x)}(x²−β²)^s`) and `B_body = 1/(a²A)`
form-reciprocal up to the constant. The **OWED derivation** is the null-geodesic deflection integral
on THIS metric:

  `δ_body(b; q, s, Z) = 2∫_{ρ_min}^{∞} (dρ / ρ²) · [1/√( (1/b²)·(A(ρ_min)/A(ρ)) − 1/ρ² )] − π`  (schematic; exact form to be derived natively from A_body, B_body).

Expected structure (to be CONFIRMED, not assumed): a leading `∝ q/b` (mass, impact-parameter
dependent) term, plus the ambient `δ_amb(s)` piece, plus `O(q²/b²)` and `O(q·s)` cross terms. The
S3c finding that the φ̃-Coulomb (body) sector and the −s ln ρ (ambient) tilt **split exactly with no
s×q mixing at leading order** predicts the leading one-body deflection and the ambient deflection
ADD without a leading cross-term — TO BE VERIFIED in the null sector (it was shown for the fields
and the timelike orbits, not yet for null rays). **This derivation is a small, bounded CAS task
(one quadrature on a known exact metric); it is the first action of the NEXT step, gated with
Charles, BEFORE any data load.** GR enters here ONLY as the reference curve `δ_GR = 4GM/c²b` (PPN
γ=1); UDT's `δ_body` is derived natively from A_body/B_body and then COMPARED to it.

### 1.3 Why both are frame-robust (the one clean thing in R2)
Under the conformal map `ĝ = e^{2φ}g`, `ĝ_tt = −c²` identically (S13a) — clocks, static forces,
timelike orbits ALL change between g and ĝ (R2 §0, the unresolved fork; ĝ is a REDUCTIO). But null
geodesics are conformally invariant: the null orbit equation is unchanged (S10b). **So BOTH (i) and
(ii) proceed regardless of how the g-vs-ĝ fork is eventually ruled.** This MAP does NOT resolve the
fork; it exploits the fact that light does not care about it. (Flag carried: if any step in the
one-body derivation §1.2 secretly needs a *timelike* input — e.g. a source defined via matter
coupling `a(φ)` — the robustness could be overstated; pre-registered as CF-FRAME.)

---

## 2. ALLOWED PARAMETERS (the premise ledger for the confrontation)

| symbol | meaning | range | tag |
|---|---|---|---|
| `s = 2μ/Z` | the ONE gauge-invariant vacuum-deformation dial (the ambient observable) | `[0, ½]` (Route A: 0; Route B: ½; a continuous sheet, NOT a binary) | **DERIVED** as the sole vacuum invariant (R1 §6 + R2 S4, blind-verified) |
| `(Z, μ)` | the rule-admissible two-parameter action sheet | `Z>0`, `μ` free | **DERIVED-FREE** (R1: principle admits the sheet; picks neither route) |
| `M = −q = νβ√E` | one-body mass parameter (attractive branch σ=+1) | `>0` (attractive) | **DERIVED** (S3c) — a per-object integration constant, NOT tuned to data |
| `ν = 2√(Z+μ²)/Z` | how Z enters the one-body sector | set by (Z,μ) | **DERIVED** (S3) |
| `b` (impact parameter of a ray) | geometry of a given observation | free per ray | observational geometry, not a model param |
| `φ₀`, `Δ = e^{φ₀}/a` (absolute) | ambient gauge / amplitude | φ₀ pure gauge; Δ value = integration data | **gauge / integration-data** (S4b/c) — never a contract row |

**No parameter is tuned to data.** `s`, `(Z,μ)`, `M/q` are pre-registered as free-and-derived; the
later data step may only BOUND them, never adjust the model FORM. `φ₀` and the absolute `Δ` are pure
gauge and never appear in a confrontation row (only D-ratios / log-slope `−s` are measurable, S4c).

---

## 3. DATA-CONFRONTATION PLAN by observable CLASS (abstract, DATA-BLIND)

No numbers here. For each observable class: which UDT quantity it maps to (ambient `s` vs one-body
`M/q`), the functional form to compare, GR as the reference curve, and how a bound would translate.
**The actual data load is the NEXT gated step, after this MAP is blind-verified — NOT part of this
document.**

| class | UDT quantity it maps to | UDT functional form (to compare) | GR reference curve | how a bound translates |
|---|---|---|---|---|
| **C1 — solar light deflection (grazing-ray angle vs impact parameter / elongation)** | **one-body `M/q` sector** (impact-parameter-DEPENDENT) — **OWED derivation §1.2** | `δ_body(b) = [leading ∝ q/b] + [ambient piece, D(ρ₀)-modulated, form OPEN] + O(q²/b², q·s)` (native, TBD) | `δ_GR = 4GM/c²b` (PPN γ=1) | a bound on the departure of `δ_body(b)` from the 1/b GR curve bounds the one-body params (q, Z via ν) and any O(1/b²) term; PPN-γ maps to the leading-coefficient ratio |
| **C2 — Shapiro time delay (radar/VLBI ranging)** | **one-body `M/q` sector** (and, separately, the ambient radar row R2-5) | native null coordinate-time delay on the M=−q metric (**OWED**, same quadrature family as §1.2); ambient radar `F(s;R)` (S6b, banked) | GR log-delay `∝ GM/c³·ln(...)` (PPN γ) | bounds the one-body sector (γ-like) via the delay; the ambient `F(s;R)` piece is frame-DEPENDENT (rides the g-vs-ĝ fork) — NOT a clean-s lever |
| **C3 — PPN γ (aggregate light-sector parameter)** | **one-body `M/q` sector** — the ratio of the space-curvature to time-curvature coefficients of the M=−q metric | derive γ_UDT from A_body, B_body expansions (**OWED**); note `ĝ_tt=−c²` means the time-sector potential is frame-conditional, so γ_UDT is a *null-sector* statement | γ_GR = 1 | γ_UDT − 1 (or its bound) constrains (q, Z); a departure at O(1/r²) is the native signature (S3d exponential lapse) |
| **C4 — ambient / absolute deflection probe (any impact-parameter-INDEPENDENT bending)** | **ambient `s`** — BUT the mapping is OPEN (verifier a66e2da69bfc3c7d9): only the pure number J(s) is b-independent; the measured azimuth = `D(ρ₀)·J(s)`, D b-dependent + gauge-carrying, s=0 conical | candidate `δ_amb(s)=J(s)−π` (`δ_amb(½)=4−π`) — **but NOT established as a clean gauge-invariant observable** (§0(i)) | GR: **zero** | IF a real b-independent gauge-invariant ambient probe exists (NOT established — CF-ABS/CF-ORIGIN), a bound gives `s < s_max`; **this is the ONLY class that could bound s, and whether it is a real observable is itself OPEN** |

**Reading of the plan.** C1–C3 constrain the **one-body sector** (the derivation of which is OWED,
§1.2) and map to GR's PPN-γ machinery as the reference. C4 is the ONLY class that directly bounds
the ambient dial `s` — and whether C4 is even a real, un-calibrated observable is itself an open
question (CF-ABS). **Therefore, at leading analysis, the standard solar-system light tests
(Cassini/VLBI) confront the one-body sector, NOT s.** A claim that they bound s requires first
establishing (a) that the ambient deflection survives differential measurement (C4 is real), or (b)
that the one-body derivation §1.2 contains an s-dependent piece large enough to be constrained by
C1–C3 (the S3c exact split predicts the leading one-body term is s-independent — so the s-sensitivity
of C1–C3 is expected to be WEAK / higher-order; TO BE VERIFIED).

---

## 4. PER-BRANCH FALSIFICATION (what observation constrains EACH branch)

The single physical dial is `s = 2μ/Z ∈ [0,½]` (a continuous sheet). Killing an endpoint does NOT
collapse the sheet (recall R1 §6: killing s=½ leaves the small-μ family alive — NOT a binary A/B
test). Falsification is framed as a BOUND on s, plus a separate constraint on the one-body sector.

- **Route A (s = 0).** The ambient vacuum is exactly flat-analog; `J(0)=π` ⇒ `δ_amb = 0` (no
  ambient deflection). CONFIRMED-consistent by any null result on an impact-parameter-independent
  ambient bending (C4). EXCLUDED only if a *nonzero* ambient impact-parameter-independent deflection
  is measured (C4) that cannot be attributed to a one-body sector — a strong, specific signature.
  Route A makes NO ambient-light prediction that departs from "straight lines"; it is falsified by a
  positive ambient-deflection detection, not by the solar tests (which constrain the one-body sector
  common to all s).
- **Route B (s = ½).** `J(½) = 4` vs `J(0)=π` ⇒ a LARGE ambient deflection `δ_amb(½)=4−π≈0.858 rad`
  per ray, impact-parameter-independent. IF C4 is a real observable, a bound `δ_amb < δ_max` with
  `δ_max < 0.858 rad` KILLS Route B. IF C4 is NOT observable (absorbed into calibration, CF-ABS),
  Route B is NOT killed by ambient light at all — it must be constrained via the one-body sector
  (C1–C3) or via the OTHER s-carrying rows (clock/ruler/radar), which are frame-DEPENDENT (rides the
  g-vs-ĝ fork) and thus not clean. **Pre-registered: the light-deflection confrontation kills Route
  B ONLY if the ambient class C4 is a real observable; this must be established, not assumed.**
- **The continuous sheet (0 < s < ½).** A bound `|s| < s_max` from C4 carves the sheet: it excludes
  `s ≥ s_max` (i.e. `μ/Z ≥ s_max/2`) but leaves the small-μ family alive. Report as a BOUND on
  `μ/Z`, never as "Route A confirmed."
- **The one-body sector (M/q, Z).** A bound on the departure of `δ_body(b)` (OWED §1.2) from the GR
  `4GM/c²b` curve — equivalently a PPN-γ bound — constrains (q, Z via ν) and any native O(1/b²)
  term (the S3d exponential-lapse `2q̂²` structure is the native prediction). A measured γ ≈ 1 to
  high precision does NOT falsify UDT: it BOUNDS the one-body departure (CF-GRMATCH); a measured
  γ ≠ 1 at the O(1/r²) native structure would be a positive UDT signature (and would constrain Z).

---

## 5. PRE-REGISTERED CLEAN FAILURES (FROZEN before any bound is loaded)

Each is a specific, falsifiable outcome committed NOW so the later data step cannot rationalize.

- **CF-CAT (category error).** Conflating the ambient `s` deflection (C4) with the one-body `M/q`
  deflection (C1–C3) — e.g. quoting a Cassini bound as "a bound on s" when it is a bound on the
  one-body sector. If the confrontation ever maps a solar-system light bound onto `s` WITHOUT first
  establishing C4 as a real observable, that is this failure. **FROZEN: Cassini/VLBI ⇒ one-body
  sector by default; s only via C4.**
- **CF-ABS (ambient not observable) — STRENGTHENED (verifier a66e2da69bfc3c7d9).** Two now-derived
  reasons the ambient sector may not bound s: (a) only the pure NUMBER `J(s)` is
  impact-parameter-independent — the measured swept azimuth is `D(ρ₀)·J(s)` with `D(ρ₀)=Δρ₀^{−s}`
  b-DEPENDENT and GAUGE-carrying (`Δ`=integration data), so there is no clean b-independent
  gauge-invariant "ambient deflection" to measure; (b) at s=0 the vacuum is CONICAL (azimuth Δ·π), so
  excess-over-π mixes a conical/gauge artifact with any true bending. Referenced to the areal-chart
  origin ρ=0, it may further be absorbed into an absolute-frame aberration / calibration offset in ANY
  differential angle measurement ⇒ **s is then NOT bounded by light at all** (only by the
  frame-DEPENDENT clock/ruler/radar rows, or not at all). Pre-registered outcome: if C4 has no realizable probe,
  record "s unconstrained by light; the frame-robust light lever bounds only the one-body sector."
- **CF-GRMATCH (one-body matches GR to all measured orders).** If `δ_body(b)` reproduces the GR
  `4GM/c²b` curve within the measured precision at every probed impact parameter, the outcome is
  NO constraint on the one-body params beyond an UPPER BOUND on the native O(1/b²) departure — NOT a
  falsification of UDT and NOT a confirmation of GR-as-the-law. Record as a bound, not a verdict.
- **CF-FRAME (frame fork resurfaces).** Light is conformally invariant, so the g-vs-ĝ fork should
  not enter. IF the OWED one-body derivation §1.2 (or the Shapiro/PPN-γ mapping) secretly requires a
  *timelike/matter* input that IS frame-dependent (e.g. defining the source via `a(φ)` coupling, or
  a clock to define "delay"), then a claimed robustness is OVERSTATED. Pre-registered: flag any
  such step and downgrade the affected row from FR to FD.
- **CF-OWED (deriving on an underived object).** The one-body deflection §1.2 is NOT yet derived.
  Any C1–C3 confrontation that proceeds BEFORE §1.2 is completed (with its own CAS check + the
  no-s×q-mixing null-sector verification) is building on an underived object. **FROZEN: complete and
  verify §1.2 BEFORE loading any solar-deflection / Shapiro / PPN-γ bound.**
- **CF-NUM (forbidden number import).** The confrontation must never require loading a lepton /
  cosmological wall number to proceed (contract 26fc757). If a step needs `G`, `M_⊙`, `z_CMB`, or a
  lepton mass to even FORM the prediction (as opposed to at the final ACCEPT/REJECT), that is a leak
  — this MAP and its derivation must be dimensionless / ratio-form up to the final gated data step.
- **CF-SHEET (false binary).** Reporting a light bound as "Route A vs Route B decided" instead of
  "`|s| < s_max`, small-μ family alive." FROZEN: every light bound is reported as a bound on `s`
  (equivalently `μ/Z`), never as a route verdict.

Additional CF revealed by the derivation: **CF-ORIGIN** — the ambient `δ_amb = J(s)−π` presupposes a
preferred center (ρ=0 of the areal chart); if no physical center exists in the confrontation
geometry (deep vacuum, no cell wall in view), `δ_amb` may not be an operationally-defined angle.
Pre-registered as a sub-case of CF-ABS.

---

## 6. NO-RETUNING RULE (explicit)

The frozen forms and parameter ranges committed in §1–§5 — `J(s)` and `δ_amb(s)=J(s)−π`; the OWED
`δ_body(b;q,s,Z)` FORM (leading ∝ q/b + δ_amb + O(1/b², q·s)); the ranges `s∈[0,½]`, `Z>0`, `M>0`;
the class→quantity map C1–C4; the GR reference curves (`4GM/c²b`, γ=1, as REFERENCE ONLY) — are
committed BEFORE any bound is loaded. **The later, separately-gated data step may only
ACCEPT / REJECT / BOUND against these frozen forms. It may NOT: adjust `s`, `(Z,μ)`, or `M/q` to fit;
re-map which class constrains which quantity; introduce a new term; or reinterpret a clean failure
after seeing the data.** Any model change discovered necessary AFTER seeing data is a NEW
pre-registration, run from scratch — not a retune of this one.

---

## 7. FOR THE VERIFIER / ATTACK SURFACE

1. **Re-derive J(s) from scratch** from the ambient metric `A=e^{−2φ₀}ρ^{2s}`, `B=e^{2φ₀}ρ^{−2s}/a²`
   (own Christoffel/geodesic or own quadrature); confirm `J(0)=π`, `J(½)=4`, slope `π(1−ln2)`.
   Check the closed form `√πΓ(1/(2−2s))/[(1−s)Γ(1/(2−2s)+½)]` against the raw integral at several s.
2. **The impact-parameter-independence claim.** Is the swept azimuth REALLY b-independent? The S7
   code comment reads "swept azimuth = D(ρ0)·J(s)" — reconcile the `D(ρ0)` ruler factor with the
   "J(s) is the deflection" statement. Determine precisely what is b-independent (the coordinate
   azimuth) vs what carries a ρ-scale, and whether the physically measured deflection angle is
   `J(s)−π` or `D(ρ0)J(s)−π`. **This is the weakest-stated link in §0(i)/§1.1 — make it exact.**
3. **The one-body deflection is OWED, not derived** — confirm this (no S-check computes the null
   deflection on the M=−q metric; S9 is timelike). Ensure the MAP nowhere treats `δ_body` as
   derived. Sanity-check the schematic §1.2 form is the right quadrature family.
4. **The s×q split in the NULL sector.** S3c proved no s×q mixing for the FIELDS and S9 for timelike
   orbits; the MAP CONJECTURES it carries to null rays. Flag that this is unproven (part of the OWED
   derivation), not banked.
5. **CF-ABS is load-bearing and honest** — attack whether the ambient impact-parameter-independent
   deflection is EVER a real observable, or always calibrated away. If it is never observable, the
   headline "light bounds s" is false and must be replaced by "light bounds only the one-body
   sector." Do not let the MAP overclaim s-sensitivity.
6. **Data-blindness** — grep the doc for any observational number (G, M_⊙, arcsec, γ-value, Cassini
   figure, z_CMB, lepton mass). There must be none.
7. **Frame robustness not overstated** — confirm the conformal-invariance argument (S10b) genuinely
   covers BOTH (i) and (ii), and that §1.2's OWED derivation will not smuggle a frame-dependent
   timelike input (CF-FRAME).
8. **GR only as reference** — confirm `4GM/c²b`, PPN-γ appear ONLY as comparison curves, never as
   the source law; the UDT forms descend from the canon metric / native action.

---

## 8. DERIVED vs OPEN vs OWED (summary)

- **DERIVED + banked (re-confirmed this push):** the pure NUMBER `J(s)` closed form and its values
  `J(0)=π`, `J(½)=4`, small-s slope `π(1−ln2)` (the number is b-independent); conformal / frame
  robustness of null geodesics (S10b); `s=2μ/Z` as the sole gauge-invariant vacuum observable; the
  one-body exterior fields + exponential lapse `M=−q`, `q̂=−νβ`, `ν=2√(Z+μ²)/Z` (S3); the exact s×q
  field split (S3c).
- **OPEN — NOT derived (verifier-corrected, was mis-tagged DERIVED):** that the MEASURED ambient
  deflection equals `J(s)−π` and is impact-parameter-independent. The swept azimuth is `D(ρ₀)·J(s)`
  with `D(ρ₀)=Δρ₀^{−s}` b-dependent + gauge-carrying, and s=0 is a conical vacuum (azimuth Δ·π) — so
  the ambient "deflection" is not a clean b-independent gauge-invariant observable (§0(i); CF-ABS/CF-ORIGIN).
- **OWED (the first action of the NEXT gated step, BEFORE any data):** the ONE-BODY null-geodesic
  deflection `δ_body(b;q,s,Z)` on the M=−q metric (a bounded CAS quadrature); its expansion vs the GR
  `4GM/c²b` reference; PPN-γ_UDT; the null-sector Shapiro delay; verification that the s×q split
  carries to null rays. **This is the quantity that actually confronts Cassini/VLBI.**
- **OPEN (not resolved here, correctly deferred):** (a) whether the ambient class C4 is a REAL
  observable or absorbed into calibration (CF-ABS) — governs whether light bounds `s` at all;
  (b) the g-vs-ĝ frame fork (unsettled; light is robust regardless, but §1.2 must not smuggle a
  timelike input); (c) the `D(ρ0)` factor / exact meaning of the measured ambient angle (attack #2).
- **NEXT GATED STEP (not this MAP):** derive §1.2 (OWED), blind-verify THIS MAP, then — with
  Charles's go — load the solar-system / VLBI bounds and run the frozen ACCEPT/REJECT/BOUND against
  §3–§4, no retuning.

---

## PREMISE LEDGER (every fixed thing tagged)

| # | premise | tag |
|---|---|---|
| 1 | metric form `ds²=−e^{−2φ}c²dt²+e^{2φ}dr²+ρ²dΩ²` | **CHOSE-cited** (canon C-2026-06-18-1) |
| 2 | `s = 2μ/Z` is the sole gauge-invariant vacuum-deformation observable | **DERIVED** (R1 §6, R2 S4; blind-verified) |
| 3 | ambient Branch-G flat-analog vacuum `ρ=ar+b`, `φ=φ₀−s ln ρ` | **DERIVED** (R1 E2a; R2 S5) |
| 4 | the pure NUMBER `J(s)` closed form + `J(0)=π`, `J(½)=4`, slope `π(1−ln2)` (the number is b-independent) | **DERIVED** (R2 S7; re-confirmed sympy this push) |
| 4b | the MEASURED ambient deflection = `J(s)−π`, impact-parameter-independent | **OPEN — NOT derived** (verifier a66e2da69bfc3c7d9: swept azimuth = D(ρ₀)·J(s), D b-dependent+gauge-carrying, s=0 conical; CF-ABS/CF-ORIGIN) |
| 5 | null geodesics conformally invariant ⇒ light frame-robust | **DERIVED** (R2 S10b) |
| 6 | one-body exterior fields, lapse, `M=−q`, `ν=2√(Z+μ²)/Z` | **DERIVED** (R2 S3) |
| 7 | one-body NULL deflection `δ_body(b;q,s,Z)` | **OWED** (not yet derived — the next action) |
| 8 | ambient deflection is a REAL b-independent gauge-invariant observable (class C4) | **OPEN — leans NO** (verifier: measured azimuth = D(ρ₀)·J(s), D b-dependent+gauge-carrying, s=0 conical; CF-ABS strengthened) |
| 9 | attractive one-body branch σ=+1 (`M>0`) | CHOSE-cited (banked; σ=−1 is the other sheet) |
| 10 | GR curves `4GM/c²b`, γ=1 used ONLY as comparison references | **method** (no GR/ΛCDM derivation imported) |
| 11 | all symbolic re-confirmations this push | DERIVED (sympy; J spot values + slope) |

---

## LAB-LOG

- 2026-07-05: built this DATA-CONFRONTATION MAP (the plan R2 deferred). Re-confirmed `J(0)=π`,
  `J(½)=4`, small-s slope `π(1−ln2)s` symbolically (own sympy, independent of `r2_final_cas.py`) +
  integral-vs-closed-form to ~1e-9 at s=0,¼,½. KEY STRUCTURAL FINDING: the two frame-robust light
  observables are DISTINCT — the ambient `J(s)` (impact-parameter-INDEPENDENT ⇒ bounds `s`, IF
  observable) vs the one-body `M/q` deflection (impact-parameter-DEPENDENT ⇒ what Cassini/VLBI
  measure). **The one-body null deflection is OWED (not derived); at leading analysis the solar
  tests confront the one-body sector, NOT s.** Data-blind, grep-clean; single process, seconds, no
  solves. **DRAFT — blind adversarial verifier pass OWED before banking (verifier-before-record);
  the data load is a separate later gated step (after §1.2 is derived + this MAP is verified).**
