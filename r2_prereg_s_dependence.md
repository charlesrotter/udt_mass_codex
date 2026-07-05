# R2 — s-dependence of the Branch-G vacuum observables (PRE-REGISTRATION, derivation half)

**Status: PROVISIONAL — blind adversarial verifier NOT yet run (owed before banking,
`verifier-before-record`). NOT committed. STRICTLY DATA-BLIND: no observational number appears
anywhere (grep-clean; the data confrontation is a SEPARATE later step).**

Contract: `PURSUIT_CHARTER_2026-07-04.md` step R2, as **REFRAMED and Charles-BLESSED** —
*measure/bound the vacuum-deformation exponent `s = 2μ/Z`, do not assert a route* (R1 §6;
Route A ⇒ s=0, Route B ⇒ s=1/2; the fork is a two-parameter sheet, not a binary).
CAS: `r2_final_cas.py`, **40/40 PASS** (the banked 34 + the S13 frame/motion-law block).

Frame + banked inputs (all cited in `r2_final_cas.py` header; none re-posited here):
metric `ds² = −e^{−2φ}c²dt² + e^{+2φ}dr² + ρ²dΩ²` (canon C-2026-06-18-1); general rule-admissible
reduced-G Lagrangian `L̄_G = (Z/2)ρ²φ'² + 2μρρ'φ' + 2 − 2ρ'²`; flux `Φ = Zρ²φ' + 2μρρ'`;
`s = 2μ/Z`; native point coupling `a(φ) = e^{+φ}` (`native_dilation_weight_derivation_results.md`
D2, **DERIVED STATIC-ONLY**).

---

## 0. THE MOTION-LAW / FRAME ADJUDICATION (the #1 job — read before any table row)

This gates every orbit AND clock observable. The result is **starker than the LEAD**: the fork is
not merely "which geodesics do test bodies follow" — it is **which metric ALL matter (bodies, rods,
AND clocks) physically couples to**, and it splits the clock rows too.

### 0.1 The native moving law and the conformal (Jordan) frame
The native rest-mass coupling is `S_pp = −mc²∫a(φ)dτ_g` with `a(φ) = e^{+φ}`, **derived for a
STATIC worldline only**. Its minimal covariant moving extension is
`S_pp = −mc²∫a(φ)√(−g_μν ẋ^μ ẋ^ν)`, which is exactly the **geodesic action of the conformal
metric `ĝ_μν = a(φ)² g_μν = e^{2φ} g_μν`** (S13b: `a(φ)²(−g ẋẋ) = −ĝ ẋẋ`, no explicit φ). So `ĝ`
is the **JORDAN (matter) frame**: free bodies, rods and clocks all couple minimally to `ĝ`.

### 0.2 The S10a finding, generalized — ĝ_tt = −c² IDENTICALLY
`ĝ_tt = e^{2φ}(−e^{−2φ}c²) = −c²` for **ANY φ** (S13a) — ambient s-vacuum OR one-body exterior.
**The conformal weight erases the entire time-time gravitational potential of `g`.** The spatial
blocks keep φ: `ĝ_rr = e^{4φ}`, `ĝ_ΩΩ = e^{2φ}ρ²`.

**Meaning — is there any static gravitational force under ĝ-geodesic motion?** NO. The radial
force on a static body is `Γ^r_tt(ĝ) = −½ ĝ^{rr} ∂_r ĝ_tt = 0` because `ĝ_tt` is constant (S13d).
This holds in **both** the pure ambient s-vacuum (no central body) **and** the one-body exterior
(`φ = φ∞ − q/r` deformed by s): `ĝ_tt = −c²` regardless of φ. **Under the native law a central mass
exerts ZERO static gravitational attraction; there are NO bound orbits in ANY static config.**

Self-consistency (S13f): the banked terrestrial no-anomaly check — `a(φ)dτ/dt = e^{φ}e^{−φ} = 1`
⇒ depth-independent rest energy `E = mc²` — **IS** the statement `ĝ_tt = −c²` (zero potential). The
native matter coupling, taken at face value, **POINTS TO the ĝ frame** (zero redshift, zero force).

### 0.3 ADJUDICATION of the orbit rows (hypothesis discipline, charter trap #8 — attacked hardest)
The rotation-curve row **v²/c² = s** (S8b: exactly flat, radius-independent) is precisely the kind
of finding that would CONFIRM a standing UDT hope (flat rotation without dark matter). It was
derived assuming **metric-`g` geodesics**. Under the native law (ĝ-geodesics):

| orbit row | derived (metric-g) | under NATIVE ĝ-law | verdict |
|---|---|---|---|
| flat rotation `v²/c² = s` (S8b) | radius-independent | lives under g / VANISHES under ĝ | **PREMISE-CONDITIONAL (motion-law unsettled) — see verifier note** |
| Kepler deformation `Ω²ρ³/(c²A)=sρ+m̂ρ/√(ρ²+β²)` (S9b) | grows linearly in s | VANISHES | premise-conditional |
| ambient apsidal `(Ψ/π)²=D²/(2(1−s))` (S8c) | exact | VANISHES | premise-conditional |
| one-body apsidal/precession (S9c/d) | exact + β-series | VANISHES | premise-conditional |

**VERDICT (verifier-corrected a82dd36ef191768dd): the orbit rows vanish ONLY under the ĝ law —
which is itself observationally dead (reductio, below).** So v²=s is **PREMISE-CONDITIONAL on the
unsettled motion-law fork, NOT a "killed artifact"**: it survives in the g-branch (the branch that
real gravity selects) and vanishes in the ĝ-branch. **NOT confrontable and NOT banked until the
fork is ruled**, but the earlier "artifact of the GR-imported g-law" headline was backwards — it is
the *native ĝ*-law that kills it and the *g*-law that keeps it. Hypothesis discipline still stands:
do not read this as "UDT gives rotation curves" — it is unsettled, not established.

### 0.4 Is the minimal extension FORCED, or a CHOSE? — genuine CHOSE, and stronger
**CHOSE, load-bearing.** The moving-worldline law is **not** fixed by R1: the native weight was
derived on the static slice, and **NO single `a(φ)` makes the MOVING action R1-invariant** (S13c,
banking the D2 anisotropy inside R2): `a(φ)dτ_g` is shift-invariant only for `dr=0`; for `dr≠0` the
radial block over-shifts by `e^{4λ}`. So:
- the metric-`g` geodesic law (`a=const`, GR test bodies) contradicts the native static weight `e^{+φ}`;
- the ĝ-geodesic law is the minimal covariant reading but is **not R1-forced** (its own action is not R1-invariant off-static);
- **the theory admits NO R1-invariant point-particle worldline law for moving matter.** This is itself a finding: it suggests matter-in-motion is not cleanly a worldline in UDT (consistent with the banked native-matter picture — matter = an S² defect FIELD, not a point worldline). Orbital dynamics should ultimately come from field solutions, not test-particle geodesics — a further reason not to trust S8/S9.

**Every orbit row is therefore premise-conditional on an undetermined (and non-R1-derivable)
motion law. The honest R2 posture: orbit rows are NOT confrontable until the frame is settled.**

### 0.5 The clock rows ride the SAME fork (correction to the LEAD)
The LEAD tagged clock/redshift ratios "solid regardless of the fork" (reasoning: clocks don't
move). **That is wrong.** The fork is a *frame* fork, not only a *motion* fork, and static clocks
feel it (S13e): the static clock-rate ratio is `(ρ₂/ρ₁)^s` in the g-frame but **`= 1` (NO redshift)
in the ĝ matter frame**, because `ĝ_tt = −c²`. Redshift and static force both descend from `g_tt`
and both vanish in ĝ. **Clocks are motion-law-robust (they are static) but NOT frame-robust.**

### 0.6 The one genuinely frame-robust row — light
Null geodesics are **conformally invariant**: the null orbit equation from `ĝ = e^{2φ}g` is
identical to that from `g` (S10b, verified directly). The deflection is an angle (coordinate
azimuth), invariant under the conformal factor. **The light deflection `J(s)` is the ONLY
dynamical observable robust to the frame fork.** Strikingly, light bends (spatial-sector geometry)
even though `ĝ_tt` is flat — a distinctive native signature: **spatial-geometric deflection with
NO accompanying redshift or Newtonian force** (in the ĝ reading).

---

## 1. Exact s-dependences (each row: formula • premise set • robustness tag)

Notation: areal radius ρ; `Δ = e^{φ0}/a` (boost-invariant amplitude); `D(ρ) = Δρ^{−s}` (local
ruler-area factor); `ν = 2√(Z+μ²)/Z`; `m̂ = νβ` (one-body mass parameter); `s = 2μ/Z`.

**LIGHT — vacuum deflection (FRAME-ROBUST).** [S7a–d, S10b]
`J(s) = 2∫₀¹ dw/√(1−w^{2−2s}) = √π·Γ(1/(2−2s)) / [(1−s)·Γ(1/(2−2s)+½)]`; `J(0)=π`;
small-s `J = π[1 + (1−ln2)s + O(s²)]`. **An O(s), impact-parameter-INDEPENDENT deflection of
every ray, however far from any body.** Route-B point: `J(½) = 4` (numerically verified).
> **CORRECTION (2026-07-05, verifier a66e2da69bfc3c7d9 via `J_of_s_light_deflection_confrontation_MAP.md`):**
> "impact-parameter-INDEPENDENT deflection" OVERSTATES — only the pure NUMBER `J(s)` is b-independent.
> The measured swept azimuth is `D(ρ₀)·J(s)` with `D(ρ₀)=Δρ₀^{−s}` b-DEPENDENT + gauge-carrying
> (`d ln D/d ln b = s/(s−1)`; `Δ=e^{φ₀}/a` = integration data), and s=0 is a CONICAL vacuum (azimuth
> Δ·π). So the measured ambient DEFLECTION is NOT `J(s)−π` and NOT shown b-independent — it is OPEN
> (its observability folded into CF-ABS/CF-ORIGIN of the J(s) MAP). The banked J(s) NUMBER + its values
> (J(0)=π, J(½)=4) and the frame-robustness of null geodesics are UNAFFECTED; only the observable-status
> gloss on row R2-1 is corrected.
*Premises:* Branch-G ambient family; null geodesics. *Robustness:* **conformally invariant ⇒
motion-law- AND frame-robust.** The cleanest confrontable row.

**CLOCK — redshift ratio (FRAME-DEPENDENT).** [S6a, S13e]
g-frame: `rate(ρ₂)/rate(ρ₁) = (ρ₂/ρ₁)^s` exactly (φ0, a, b cancel). ĝ-frame: `= 1` (no redshift).
*Premises:* static clocks; **+ physical-frame choice (g vs ĝ)**. *Robustness:* motion-law-robust,
**NOT frame-robust — rides the §0 fork.**

**CLOCK log-gradient — one-body (FRAME-DEPENDENT).** [S9a]
`d ln(rate)/d ln ρ = s + m̂/ρ + O(1/ρ³)` (g-frame): the s-piece is the CONSTANT term, the body
piece falls off as `1/ρ` (separable by a multi-radius clock network); no s·m̂ cross-term.
ĝ-frame: the s-constant vanishes (no ambient redshift), body piece likewise erased.
*Robustness:* NOT frame-robust.

**RULER — proper distance vs areal radius (FRAME-DEPENDENT).** [S5a,b]
g-frame: `dl/dρ = √(g_rr) = Δρ^{−s}`, log-slope `−s`; D-ratio between stations `(ρ₂/ρ₁)^{−s}`;
`g_rr(r-coord) = e^{2φ}` picks up exactly `ρ^{−2s} = ρ^{−4μ/Z}`; and `A·B = 1/a²` (form reciprocity
in areal coordinates). *Robustness:* the areal radius itself rescales by `e^{φ}` under the conformal
map, so this row is **frame-dependent** (spatial geometry survives in both frames but with a
frame-dependent exponent). NOT a clean frame-invariant.

**RADAR — echo/ruler ratio (FRAME-DEPENDENT).** [S6b,c]
`c·τ/(2l) = F(s;R) = (1−s)/(1−2s)·ρ₁^s(ρ₂^{1−2s}−ρ₁^{1−2s})/(ρ₂^{1−s}−ρ₁^{1−s})`, `R=ρ₂/ρ₁`;
`F(0;R)=1`. Route-B point: `F(½;R)=√ρ₁·ln R /(2(√ρ₂−√ρ₁))` (radar time grows only
logarithmically). *Robustness:* mixes a clock (time) and a ruler (space); **frame-dependent.**

**ORBITS — v², Kepler, apsidal (FRAME-DEPENDENT; VANISH under native law).** [S8b, S8c, S9b–d]
g-frame: `v²/c² = s` (radius-independent); `Ω²ρ³/(c²A) = sρ + m̂ρ/√(ρ²+β²)`;
ambient `(Ψ/π)² = D²/(2(1−s))` (→ `π/√2` as s→0, the classic 1/ρ-force apsidal angle);
one-body `(Ψ/π)² = [ambient](s) + c₁(s,Z)β + O(β²)`; s=0 body-only `(Ψ/π)² = 1 + (8/(√Z ρ))β +…`
(closed ellipse recovered, the O(β) precession carries Z = the second dial).
*Robustness:* **VANISH under the native ĝ-law (§0.3); confrontable only under the metric-g premise.**

**SEAL — G|P φ'-jump (STRUCTURAL, motion-law-independent).** [S11a,b]
`ρ'_G = ρ'_P·(e^{−2φ_s}+μ²/Z)/(1+μ²/Z)`; `φ'_G − φ'_P = s·(1−e^{−2φ_s})ρ'_P /(ρ_s(1+μ²/Z))`
— the φ'-jump is **∝ s** (vanishes iff s=0 or φ_s=0 or ρ'_P=0). Reproduces banked d2c M9 at (8,2).
*Robustness:* a property of the field junction, not of test-body motion ⇒ **motion-law-independent.**
Realizability: see §3.

**FLUX — canon odd+odd G-domain (STRUCTURAL).** [S12]
`Φ = 2μ·ln(ρ₂/ρ₁)/I = sZ·ln(ρ₂/ρ₁)/I`, `I=∫dr/ρ²` (at (8,2): `4ln(ρ₂/ρ₁)/I`, matches d2b E3).
∝ s. *Robustness:* structural. Realizability: see §3 — **NO realizable configuration** (not a lever).

---

## 2. Gauge / invariance resolution (measurable-in-principle vs pure gauge) — the LEAD's item 4

Form-preserving maps of the zero-flux family (S4): the r-shift, the global depth-shift
`φ→φ+λ`, and the boost `(t,r,φ)→(λt, r/λ, φ+ln λ)`.

- **`s = 2μ/Z` is gauge-INVARIANT** (boost- and shift-invariant trivially): it is the physical
  content of the sheet — the one vacuum-deformation observable at this order (S4b).
- **`φ0` alone is pure gauge** (absorbable by the shift). The amplitude combination
  **`Δ = e^{φ0}/a` is boost-INVARIANT** but the shift sends `Δ→e^λ Δ`; hence the ruler reader
  `D(ρ) = e^φ/ρ' = Δρ^{−s}` has a **value that is integration data** (which vacuum the universe
  realized), **never theory-fixed** (S4c). Only **D-RATIOS** between stations and the
  **log-slope `−s = d lnD/d lnρ`** are shift- AND boost-invariant contract rows.
- **Measurable-in-principle:** `s` (via any of the s-carrying rows), and D-ratios / log-slopes.
- **Pure gauge (never a contract row):** `φ0`, the absolute value of `D`, absolute `a` or `b`.
- **Frame-conditional (the §0 fork — a DEEPER "gauge" than the coordinate gauges):** which of the
  s-carrying rows is *physical* depends on the g-vs-ĝ frame choice. Only the **conformally-invariant
  light deflection `J(s)`** is unconditional. Clock/ruler/orbit rows are frame-conditional.

---

## 3. One-body exterior verdict + lever-realizability verdicts

**One-body exterior (S3a–e).** Exact `E>0` branch solves both EOMs: `ρ² = E(x²−β²)`,
`φ̃ = φ̃∞ + σν·artanh(β/x)`, `Φ = −σZνEβ`, `x = r−r₀`. Attractive branch σ=+1 gives banked
`M = −q = νβ√E > 0` (Coulomb-in-φ̃, S3c) and an **exponential lapse**
`e^{−2φ̃} = e^{−2φ̃∞}(1 + 2q̂/x + 2q̂²/x² + …)`, `q̂ = −νβ` (S3d) — the banked O(1/r²) departure
structure, Z entering only via `ν = 2√(Z+μ²)/Z`. The φ̃-Coulomb (body) sector and the `−s ln ρ`
tilt (ambient) **split exactly** (no s×q mixing at leading orders, S3c). First integral
`ρ'² = E + Φ²/(4(Z+μ²)ρ²)` characterizes the WHOLE vacuum space (E>0 exterior, E=0 parabolic,
E<0 closed — S3e; observed, not filtered). **Under the native ĝ-law the one-body exterior still
has `ĝ_tt = −c²` ⇒ the central mass exerts zero static force; its ONLY exterior observable is the
light deflection.** The clock and orbit rows around the body are frame-conditional per §0.

**Lever 1 — G|P seal φ'-jump (S11).** REALIZABLE and ∝ s: a G|P seal with φ_s≠0 makes φ' itself
jump, proportional to s (vanishes at s=0). This is an *internal/structural* discriminator (an
eventually-confirmed G|P-architecture particle would evidence μ≠0), **motion-law-independent**. It
is a structural lever, not a direct vacuum observable.

**Lever 2 — odd+odd G-domain flux (S12).** The formula `Φ = sZ ln(ρ₂/ρ₁)/I` is exact, but the
**realizability verdict is NO** (confirmed): the banked frame provides **no realizable
configuration** carrying a flux-bearing pure-G segment between canon (untwisted) folds — a lever
with no realizable configuration is **not a lever**. Recorded, not banked as a discriminator.

---

## 4. THE FROZEN CONFRONTATION TABLE (the pre-registration contract)

One row per observable. `s = 2μ/Z ∈ [0, ½]` across the sheet (Route A: 0, Route B: ½). Observable
CLASSES are named **abstractly** — NO numbers; a later data step loads bounds with **no retuning**.
**Robustness key:** FR = frame-robust (conformally invariant); FD = frame-dependent (rides the §0
g-vs-ĝ fork); ST = structural/internal (motion-law-independent). MOTION key: RB = motion-law-robust,
V = vanishes under the native ĝ-law, N/A = not a motion observable.

| # | observable | EXACT s-dependence | invariant / measurable combination | premise set | robustness | confront CLASS |
|---|---|---|---|---|---|---|
| R2-1 | **vacuum light deflection** | `J(s)=√π Γ(1/(2−2s))/[(1−s)Γ(1/(2−2s)+½)]`; small-s `π[1+(1−ln2)s]`; `J(0)=π`, `J(½)=4` | deflection angle (coordinate azimuth), **impact-parameter-INDEPENDENT** | Branch-G ambient; null geodesics | **FR, RB** | **light-deflection class** |
| R2-2 | **clock redshift ratio** | g: `(ρ₂/ρ₁)^s`; ĝ: `1` | ratio of two static clock rates + areal radii of their spheres | static clocks **+ frame choice** | **FD, RB** | **clock-ratio class** |
| R2-3 | **one-body clock log-gradient** | `d ln rate/d ln ρ = s + m̂/ρ` (g); ĝ: s-term → 0 | constant term (=s) separated from `1/ρ` body term by multi-radius network | static clocks **+ frame choice** | FD, RB | clock-ratio class (gradient) |
| R2-4 | **ruler vs areal radius** | g: `dl/dρ = Δρ^{−s}`, slope `−s`; `g_rr∝ρ^{−4μ/Z}` | **D-ratio** `(ρ₂/ρ₁)^{−s}` / log-slope `−s` (absolute `Δ` = gauge) | Branch-G ambient **+ frame choice** | FD, N/A | **length/ruler class** |
| R2-5 | **radar echo/ruler ratio** | `F(s;R)=(1−s)/(1−2s)·ρ₁^s(ρ₂^{1−2s}−ρ₁^{1−2s})/(ρ₂^{1−s}−ρ₁^{1−s})`; `F(½)=√ρ₁ ln R/(2(√ρ₂−√ρ₁))` | dimensionless `c τ/(2l)`; `F(0;R)=1` | static stations **+ frame choice** | FD, RB | **radar/time-delay class** |
| R2-6 | **flat rotation law** | g: `v²/c² = s` (radius-independent); ĝ: **none** | local orbital speed of a circular test body | motion-law-conditional (g: yes; ĝ: no) | **FD, V** | **orbital/rotation-curve class** (PREMISE-CONDITIONAL — not banked; NOT an artifact) |
| R2-7 | **Kepler deformation** | g: `Ω²ρ³/(c²A)=sρ+m̂ρ/√(ρ²+β²)`; ĝ: none | s-term (∝ρ) vs body-term (→m̂) separable | metric-g geodesics + one-body | **FD, V** | orbital class |
| R2-8 | **apsidal precession** | g: `(Ψ/π)²=D²/(2(1−s))` (ambient) / `+c₁(s,Z)β` (one-body); ĝ: none | apsidal angle per orbit | metric-g geodesics | **FD, V** | orbital/precession class |
| R2-9 | **G\|P seal φ'-jump** | `φ'_G−φ'_P = s(1−e^{−2φ_s})ρ'_P/(ρ_s(1+μ²/Z))` (∝ s) | φ'-discontinuity at a seal | G\|P architecture exists (φ_s≠0) | **ST, N/A** | internal/architecture class |
| R2-10 | **odd+odd G-flux** | `Φ = sZ ln(ρ₂/ρ₁)/I` (∝ s) | flux on a closed G-domain | canon odd+odd — **NO realizable config** | **ST, N/A** | *not a lever* (realizability NO) |

**Pre-registration reading of the table.** The single physical dial is `s = 2μ/Z ∈ [0,½]`. A solid
bound `|s| < s_max` from the **light-deflection class** (row R2-1, the only frame-unconditional row)
is the primary, no-retuning confrontation: if `s_max < ½` it **kills Route B (s=½)** but leaves the
small-μ family alive — **not a binary A/B test** (R1 §6). Rows R2-2..R2-5 add clock/ruler/radar
confrontations **conditional on the g-frame being physical**; if the native ĝ frame is physical they
weaken or vanish. Rows R2-6..R2-8 (orbital) are **premise-conditional on the motion-law fork** (they live under g,
vanish under ĝ) — not banked, but NOT artifacts: the branch that kills them (ĝ) is the
observationally-dead one. Rows R2-9/R2-10 are internal/structural (R2-10 is
not a realizable lever).

---

## 5. Every CHOSE (the premise ledger for this doc)

| # | premise | tag |
|---|---|---|
| 1 | `s = 2μ/Z` is the sheet's one vacuum-deformation observable | **DERIVED** (R1 §6, blind-verified; S2/S4 here) |
| 2 | metric form `ds² = −e^{−2φ}c²dt² + e^{2φ}dr² + ρ²dΩ²` | CHOSE-cited (canon C-2026-06-18-1) |
| 3 | reduced-G Lagrangian / flux / EOMs | banked (R1, d2c; reproduced S1) |
| 4 | native static weight `a(φ) = e^{+φ}` | **DERIVED STATIC-ONLY** (D2) |
| 5 | **moving-worldline law** (metric-g geodesic vs ĝ-geodesic) | **CHOSE — load-bearing, UNSETTLED; no R1-invariant worldline law exists (S13c). Every orbit + clock row is conditioned on it.** |
| 6 | **physical frame** g vs ĝ (which metric matter couples to) | **CHOSE — same fork as #5. The native static weight POINTS to ĝ, but ĝ-as-physical is a REDUCTIO (zero redshift + zero orbits, verifier a82dd36ef191768dd) ⇒ live options are g-coupling or matter-is-a-field; only light J(s) is unconditional** |
| 7 | attractive one-body branch σ=+1 (`M=−q>0`) | CHOSE-cited (banked `M=−q`); the σ=−1 branch is the other sheet |
| 8 | gauge fixing `E=1, φ̃∞=0` for the one-body rows (S9) | CHOSE (S4-legal; results stated as invariants where possible) |
| 9 | all symbolic claims | DERIVED (CAS 40/40, `r2_final_cas.py`) |

**STOP-flags carried to Charles / the verifier:**
1. **The frame fork (#5/#6) is unresolved and load-bearing**, and it is DEEPER than the LEAD stated:
   it splits the CLOCK rows too, not only orbits. **VERIFIER SHARPENING (a82dd36ef191768dd): the fork
   is ASYMMETRIC, not 50/50 — the ĝ branch is a REDUCTIO.** ĝ_tt=−c² gives zero gravitational redshift
   (vs Pound–Rebka/GPS) AND zero static force ⇒ no bound orbits anywhere (vs the solar system). So the
   naive "native weight ⇒ ĝ ⇒ gravity is purely light-bending" reading is REFUTED as a physical frame;
   the derivation is a reductio against ĝ-as-matter-frame, pointing to g being physical OR to
   matter-in-motion not being a worldline at all (S13c). Per solver-first, this indicts the moving-law
   CHOSE, not the metric. Charles's ruling wanted before the data step.
2. **The flat rotation law v²=s is PREMISE-CONDITIONAL** on the motion-law fork (verifier-corrected):
   it lives under g, vanishes under ĝ; the ĝ branch that kills it is itself observationally dead.
   Not banked. Do not read it as "UDT gives rotation curves" — but it is UNSETTLED, not an artifact.
3. **No R1-invariant point-particle worldline law exists** (S13c) — a hint that moving matter is a
   field (S² defect), not a worldline; orbital confrontations may be ill-posed at the test-particle level.

## LAB-LOG
- 2026-07-04: resumed the R2 LEAD. Settled the motion-law fork (S13 block, 6 new checks) BEFORE the
  table. `r2_final_cas.py` = banked 34 + S13 = **40/40 PASS**, single process, seconds, no solves
  beyond trivial quadratures, **data-blind grep-clean**. Results doc + frozen table written. NOT
  committed; blind adversarial verifier pass OWED (`verifier-before-record`).

---

## VERIFIER RECORD (blind adversarial pass — agent a82dd36ef191768dd, opus-4-8, 2026-07-04)

Independent CAS (`r2_bv_verify.py`, own sympy from the source metric/action, 26/26); original
`r2_final_cas.py` 40/40 reproduced; pytest 32/1xfail; data-blind confirmed (all GPS/Pound–Rebka
reasoning in the verifier report only, never in this artifact). Both strong claims attacked equally:

- **Claim A (rotation law): arithmetic RIGHT, "artifact" verdict HASTY → corrected above.** v²=s
  holds under metric-g geodesics and vanishes under ĝ; but the kill leans on the observationally-dead
  ĝ-branch, and v²=s LIVES in the g-branch that gravity selects. Correct status = premise-conditional,
  not artifact. (Corrections applied to §0.3, the table, STOP-flag 2.)
- **Claim B (ĝ ⇒ zero force + zero redshift): algebra RIGHT, frame-conclusion WRONG (reductio).**
  Every step reproduced (ĝ_tt=−c² identically; Γ^r_tt(ĝ)=0; full static radial accel =0 for the
  one-body φ=φ∞−q/r; ĝ-clock ratio =1; and the g-branch CONTRAST: real accel c²q e^{2φ}/r²≠0, real
  redshift (ρ₂/ρ₁)^s). Since zero redshift (vs Pound–Rebka/GPS) AND zero orbits (vs the solar system)
  refute ĝ-as-physical, this is a REDUCTIO against the ĝ frame — NOT a serene "gravity is light-bending"
  signature. The fork is asymmetric (ĝ dead). (Sharpening applied to STOP-flag 1 + CHOSE #6.)
- **S13c (no R1-invariant worldline law): CONFIRMED.** Only an anisotropic/disformal weight
  (e^{−φ} on dr ≠ e^{+φ} on dt) is invariant ⇒ matter-in-motion is not cleanly a point worldline ⇒
  test-particle orbit rows are ill-posed; orbital dynamics should come from field/S²-defect solves.
- **J(s) light deflection: SURVIVES as the ONE frame-robust confrontation lever** (J(0)=π, J(½)=4,
  O(s) impact-parameter-independent; conformal invariance of null geodesics — identical in g and ĝ).
- **s=2μ/Z: the sole gauge-invariant vacuum observable** (D-value gauge; D-ratios + log-slope −s
  measurable). Table robustness tags correct apart from the corrected "artifact" gloss.

**BANKED (safe):** all symbolic s-dependences (40/40); s=2μ/Z as the one gauge-invariant vacuum
observable; **J(s) as the frame-robust light-deflection confrontation row**; the ∝s structural levers
(realizability caveats intact); the pre-registration + data-blindness.
**NOT BANKED (Charles's STOP):** the physical-frame ruling (g vs ĝ vs matter-is-a-field). ĝ-as-physical
is refuted; the live fork is g-coupling vs field/defect. Every orbit + clock row is gated on it; only
J(s) is confrontable regardless. Per solver-first the reductio indicts the moving-law CHOSE, not the metric.
