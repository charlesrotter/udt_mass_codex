# The a(phi) PROFILE — is the mass-dilation exponent a NUMBER or a FUNCTION? — MAP + OBSERVE

**Agent:** Claude Opus 4.8 (1M), driver-delegated | **Date:** 2026-06-18
**MODE: MAP + OBSERVE.** Premises made VISIBLE; report WHAT IS THERE with premises
attached. **NO particle mass/ratio derived (DERIVE gated on Charles). NO verdict
targeted.** Anti-smuggling is the whole point. **NOT canon. Do not commit (per task).**
Script: `a_profile_absorb_and_cassini.py` (sympy, CPU).

**Builds ON (does not redo) this session's prior passes:**
- `udt_field_equation_running_rate_results.md` + `running_rate_verifier_results.md`: a CONSTANT scalar source-weight is ABSORBABLE (blind-verified).
- `udt_matter_source_MAP_results.md`: the entire UDT-vs-GR matter-side question collapses to the single number `a+1`; `a` under-determined; a=-1 (GR) admissible; the menu {-3,-1,0,+1,+3} spans GR and modified values; the decisive pin needs a covariant rest-mass of an actual object.

**The new reframe under test (Charles, 2026-06-18, lay):** `a` may be a FUNCTION
`a(phi)`, not a number — `a(phi) = -1` in the weak field (solar, Cassini-safe BY
STRUCTURE), departing from -1 only at the EXTREMES (|phi| large: hadronic core,
cosmic boundary). UDT's thesis "GR in the middle, departs at the extremes,"
expressed as a profile.

**Definitions used (flag if changed):** `a(phi) = d(ln m)/dphi`, so
`m(phi) = m0 exp(∫_0^phi a(phi') dphi')`. Non-absorbable fingerprint (matter
ruler / metric ruler) `~ exp(-∫_0^phi (a(phi')+1) dphi')`; runs wherever
`a(phi)+1 != 0`. Carried-over premise (the chosen GR-leak, unchanged):
**P2 = standard Einstein tensor on the left.**

---

## 0. ONE-LINE BOTTOM LINE (no false convergence)

> **a(phi) as a function is a PHYSICAL-PICTURE REFRAME, NOT a new mathematical
> escape from GR-equivalence.** The make-or-break math (#3) is NEGATIVE: a
> position-varying scalar weight `exp(∫(a(phi)+1)dphi)` is STILL absorbable by the
> SAME Bianchi tautology that killed the constant case — for ANY profile a(phi),
> including one that departs only at the extremes. The phi-dependence of `a` does
> NOT manufacture a non-absorbable object. **What the reframe genuinely buys** is
> in the COMPOSITION fork (#2): it correctly identifies that for `a` to be a
> function at all, matter must BREAK the additive composition law the metric
> obeys — and that breaking is tied to matter HAVING AN INTRINSIC SCALE. That ties
> the deep-a(phi) shape to the matter object, exactly as expected. **The payoff
> still waits on the matter object.** The principle level settles a(0)=-1, the
> Cassini orders, and the fork; it does NOT settle whether a departs, nor how.

---

## 1. ANCHOR a(0) = -1 — DERIVED, and what Cassini bounds about its DERIVATIVES

### 1a. a(0) = -1 from the equivalence principle (DERIVED, not assumed)
Sense-1 (CANON, observer-frame): no local-physics modification; lab/solar matter
free-falls with the metric, NO fifth force. A test mass at phi~0 follows the
metric geodesic with NO extra coupling. The extra coupling matter feels beyond
pure geodesic motion is exactly the Bianchi exchange force
`nabla T = -(a(phi)+1) phi' T` (from P2 + the weight, prior passes). "Free-fall
with the metric / no fifth force" = that exchange force VANISHES as phi->0:
```
   (a(phi)+1) -> 0   as phi -> 0   <=>   a(0) = -1.
```
This is DERIVED from the equivalence-principle content of Sense-1, not chosen. It
is the same statement as "the weight `e^{(a+1)phi}` -> 1 and the matter ruler runs
IN STEP with the metric ruler at phi=0." **a(0)=-1 is the GR-locked anchor; it is
forced. (Tag: DERIVED from Sense-1 EP.)**

### 1b. Cassini on the DERIVATIVES — the allowed peel-off order n
Write `a(phi) = -1 + sum_{k>=n} c_k phi^k`, so `(a+1) = c_n phi^n + ...`. The
non-absorbable fingerprint over a path is `F(phi) = exp(-∫_0^phi (a+1) dphi')`;
with leading term (script (C)):
```
   F(phi) = exp(-c_n phi^{n+1}/(n+1))  ~  1 - c_n phi^{n+1}/(n+1) + ...
```
The fractional departure of the matter ruler from the metric ruler over a
lab/solar path scales as `c_n phi^{n+1}`. Solar/planetary phi ~ U/c^2 ~ 1e-6
down to ~1e-8. Cassini: |gamma-1| < 2.3e-5.

**OBSERVED (honest, and it cuts against an over-strong claim):** because solar phi
is TINY (~1e-6), the departure `phi^{n+1}` is far below Cassini for EVERY order
n>=0 with O(1) coefficient. So **Cassini does NOT, by itself, force a(0)=-1
numerically** — even a CONSTANT a != -1 with |a+1| up to ~20 sits under the
Cassini bound at solar phi. The structural anchor a(0)=-1 comes from the
EQUIVALENCE PRINCIPLE (1a), not from Cassini. Cassini's actual bite is a BOUND on
the low-order coefficients c_n, and that bound is LOOSE because phi_solar is small.

**Leading allowed departure / lowest order n:** GIVEN the EP anchor a(0)=-1
(so c_0=0, i.e. n>=1), the leading peel is `a(phi) = -1 + c_1 phi + O(phi^2)`,
**n=1 allowed** (Cassini bounds c_1 loosely: |c_1| phi^2 < 2.3e-5 at phi~1e-6 is
trivially satisfied for any sane c_1). The physical picture "departs only at the
extremes" is a STRONGER, optional choice (push c_n to high order / large onset
scale) — it is NOT forced by Cassini; Cassini permits a gentle linear peel from
phi=0. **(Tag: a(0)=-1 DERIVED; the order n and onset are CHOSEN/under-constrained,
Cassini-loose.)**

---

## 2. THE COMPOSITION FORK — number vs function (the heart)

The metric's exponential law came from composition/reciprocity (R1/R2/R3 behind
CANON C-2026-06-18-1): phi is ADDITIVE (combining depths adds phi), and dilations
COMPOSE — dilate by phi1 then phi2 = dilate by phi1+phi2. This is a functional
equation `D(phi1)·D(phi2) = D(phi1+phi2)`, whose continuous solution is forced to
`D = e^{k phi}` with CONSTANT k.

**The fork, cleanly:**
```
   IF mass-dilation OBEYS the same composition (m: dilate phi1 then phi2 = dilate phi1+phi2)
       => m(phi1)·... functional eqn => m ~ e^{a phi} with CONSTANT a
       => with the EP anchor a(0)=-1 => a = -1 EVERYWHERE
       => weight = 1, fingerprint const => UDT = GR locally.       [IN-STEP / "boring" branch]

   IF mass-dilation BREAKS simple composition
       => a is NOT forced constant => a(phi) can be a genuine FUNCTION
       => departs from -1 where composition breaks.                [UDT-departs-at-extremes branch]
```
**This is the real content of the reframe:** "a is a function" is EQUIVALENT to
"mass-dilation breaks the additive composition law the metric obeys." A constant a
is not a special case to argue against — it is what composition-respect FORCES.

**What would break composition? (OBSERVE, candidate, not derived):** the metric's
composition is scale-FREE (pure positional dilation, no length in it — consistent
with bare-gravity scale-invariance, CANON). Matter is different: a particle HAS an
intrinsic length (a Compton wavelength `lambda_C = hbar/(m c0)`, a rest scale).
Composition `D(phi1)D(phi2)=D(phi1+phi2)` is exact ONLY for a scale-free response.
An object with its OWN length responds to the LOCAL dilation depth nonlinearly
once the dilation becomes comparable to / probes that length — i.e. where
`e^{-2phi}` is large (the extremes: hadronic core, cosmic boundary). At small phi
the intrinsic scale is untouched and the response is effectively scale-free
(composition approximately holds => a~const~-1, GR). At large |phi| the intrinsic
scale enters => composition breaks => a(phi) departs.

**=> YES: the composition-breaking (function) branch is TIED to the matter having
an intrinsic scale.** This is the structural reason the deep a(phi) shape cannot
be a pure principle statement — it requires the OBJECT that carries the scale.
This is the same conclusion the matter-source MAP reached ("the decisive pin needs
a covariant rest-mass of an actual localized object"), now given a MECHANISM: the
object's intrinsic length is precisely what breaks composition and lets a run.
**(Tag: the fork structure DERIVED from the composition functional equation; the
intrinsic-scale mechanism is a CANDIDATE/OBSERVE, not derived — flag.)**

---

## 3. DOES a(phi) ESCAPE ABSORBABILITY? — the make-or-break — VERDICT: NO (still absorbs)

The twice-verified absorbability used a CONSTANT scalar weight. Re-examined here
for a POSITION-VARYING `a(phi)`, AND with the self-consistency that phi IS the
metric (this session's -1-vs-2 self-variation term, `+e^{-2phi}phi'^2`).

### 3a. The general-weight Bianchi tautology (script (A)) — EXACT ZERO for ANY W(phi)
Left side = standard Einstein tensor (P2). Contracted Bianchi `nabla_mu G^{mu nu}=0`
holds for ANY metric. For `G = kappa0 W(phi) T`:
```
   nabla_mu T^{mu nu} = -(d ln W/dphi)(partial_mu phi) T^{mu nu}    [exchange law, ANY W]
```
Define `T~ = W(phi) T`. Then (script, symbolic, ARBITRARY function W):
```
   nabla(W T) = W' T + W·nabla T = W' T + W·(-(W'/W) T) = 0    EXACTLY.
```
Script output: `nabla(W*T) = 0` for arbitrary `W(phi)`. The cancellation is
W'-against-W' STRUCTURAL — it never references whether `d ln W/dphi` is constant.
With `W = exp(∫(a(phi)+1)dphi)`, `d ln W/dphi = a(phi)+1` whatever its
phi-dependence; the tautology still holds.

> **CONCLUSION (3a): a POSITION-VARYING a(phi) is STILL ABSORBABLE. `T~ = W T` is
> covariantly conserved for ANY profile, so `G = kappa0 T~` relabels to ordinary GR
> with a constant coupling — exactly as in the constant-a case. The phi-dependence
> of `a` does NOT, by itself, escape absorbability.**

### 3b. Self-consistency (phi IS the metric) adds NO second weight (script (B))
Confirmed the banked identity `Box_g phi = -G^th_th` (sympy residual 0) on the
UDT metric. The th-th field equation is therefore
`Box_g phi = -kappa0 W(phi) T^th_th`. The weight on "matter-sources-phi" is the
SAME scalar `W(phi)`; the self-variation (the -1-vs-2 / `+e^{-2phi}phi'^2` term)
lives entirely in the `Box_g` operator on the GEOMETRY side, which is
exponent-free and is precisely what folds to zero in vacuum. **No SECOND,
independent weight is manufactured by self-consistency.** So combining
position-varying a(phi) WITH the metric-self-variation does NOT produce a
non-absorbable differential structure that a constant weight lacked. It routes
back to the same single (now phi-dependent) scalar weight, which 3a shows is
absorbable.

### 3c. HONEST verdict
> **a(phi) does NOT escape absorbability. It still absorbs.** The surviving
> non-absorbable object is the SAME one as in the constant case: the dimensionless
> ratio (matter ruler)/(metric ruler) `~ exp(-∫(a+1)dphi)`, which is physical ONLY
> when an INDEPENDENT matter ruler exists to compare against the metric ruler — and
> that ruler is the matter object's intrinsic scale (#2). With a generic T and no
> intrinsic scale, `T~ = W T` IS the source and there is nothing to compare, so it
> relabels to GR. **Making `a` a function is a physical-picture reframe, not a new
> mathematical escape.** (Recommend a blind verifier pass on 3a — the
> arbitrary-W conserved-T~ claim is load-bearing — before any banking.)

---

## 4. SNe BOUND on the departure ONSET (bound, not fit)

SNe match GR/LCDM out to z~2, i.e. phi up to ~1 (1+z = e^phi). The luminosity
distance `d_L = r(1+z)` and the Hubble-diagram shape are degenerate with absolute
magnitude M (the standard mu-vs-M degeneracy; `udt_validated_results.md`). Read as
a BOUND, not a fit:
```
   Through phi ~ 1, the matter ruler runs ~IN STEP with the metric ruler:
   (a(phi)+1) is observationally ~ 0 for 0 <= phi <~ 1.
   => any departure of a(phi) from -1 has its ONSET DEEPER than phi ~ 1.
```
This does NOT fit a value of a or c_n; it bounds the ONSET SCALE: the
composition-breaking (function) branch, if real, must keep `a(phi) ~= -1` through
phi~1 and turn on only beyond it — consistent with "departs only at the extremes"
(hadronic core has phi ~ -1 to -1.15 where e^{-2phi}~5-10; cosmic boundary phi up
to ~7 from CMB). **SNe says: the departure lives deeper than SNe reaches; it does
not say there IS one. (Tag: BOUND, derived from the SNe degeneracy; no value fit.)**

---

## 5. WHERE THE MATTER OBJECT BECOMES UNAVOIDABLE (exact point in the chain)

PRINCIPLE-LEVEL (settled WITHOUT an object), in order:
1. a(0) = -1 (EP anchor) — DERIVED. [#1a]
2. Cassini/SNe constraints on the low-order peel and the onset — DERIVED as
   (loose) bounds. [#1b, #4]
3. The composition fork: constant-a(=GR) vs function-a requires
   composition-breaking — DERIVED from the functional equation. [#2]
4. The absorbability of any scalar weight W(phi) — DERIVED (3a/3b): so the
   departure, if any, is NOT in the weight; it is in the ruler RATIO.

**THE EXACT HAND-OFF POINT:** the chain stops being principle-derivable the moment
it needs an INDEPENDENT MATTER RULER to make the ratio `exp(-∫(a+1)dphi)`
physical. That ruler IS the matter object's intrinsic scale (Compton length /
covariant rest mass). Concretely, the matter object becomes UNAVOIDABLE at the
junction of #2 and #3:
> To know (i) WHETHER composition breaks (a is a function vs constant) and
> (ii) the SHAPE of a(phi) where it breaks, you must have the object whose
> intrinsic length breaks composition and compute its covariant rest mass
> m(phi) — from which a(phi) = d(ln m)/dphi is read off directly. No
> generic-T, no principle statement, supplies an intrinsic length.

Everything UP TO "is the ruler running?" is principle. "What does the ruler do at
depth?" is the object. This matches the matter-source MAP's named decisive pin
(timelike-Killing energy vs Noether charge of an actual localized solution) —
the same gated, consequence-stage step.

---

## 6. PREMISE LEDGER (chose vs derived) + GR / fitted-quantity sneak-ins

| # | Item | chose / derived | GR-leak / fitted-leak risk |
|---|------|-----------------|----------------------------|
| Q1 | P2: standard Einstein tensor on the left (carried over) | **CHOSE** (unchanged from prior passes) | **PRIMARY GR-LEAK.** It is WHAT makes any scalar weight absorbable (Bianchi tautology). Native left-side law still unbuilt; firewalled to the gravity-sector push. |
| Q2 | a(0) = -1 | **DERIVED** from Sense-1 equivalence principle (no fifth force as phi->0) | the GR-locked anchor; forced |
| Q3 | Cassini does NOT force a(0)=-1 numerically (loose at solar phi) | **DERIVED** (script C; phi_solar~1e-6) | honest down-grade: anchor is EP, not Cassini |
| Q4 | leading allowed peel n=1: a = -1 + c_1 phi + ... | DERIVED order; c_1, onset CHOSEN/under-constrained | "departs only at extremes" is a CHOSEN stronger profile, not forced |
| Q5 | composition-respect => constant a => GR | **DERIVED** (functional equation D(phi1)D(phi2)=D(phi1+phi2)) | clean |
| Q6 | a a function <=> composition BREAKS <=> matter has intrinsic scale | fork DERIVED; intrinsic-scale mechanism CANDIDATE (OBSERVE) | the mechanism is a physical picture, not derived — flag |
| Q7 | scalar weight W(phi) absorbable for ANY profile (T~=W T conserved) | **DERIVED** (script A, exact 0); verifier recommended | the make-or-break; NEGATIVE for an escape |
| Q8 | self-consistency adds no 2nd weight (Box_g phi = -G^th_th) | **DERIVED** (script B, residual 0) | — |
| Q9 | SNe: (a+1)~0 through phi~1 => onset deeper than phi~1 | **DERIVED as a BOUND** from the d_L=(1+z)r / mu-M degeneracy | no value fit; bound only |
| Q10 | a(phi) departs (the function branch is realized) | **NOT established** — needs the object | the whole open question |

**Fitted-quantity sneak-ins:** NONE. No mu^2, no mu^2=pi/3, no Lambda, no
mass/ratio/wall/macro/SM number, no value of a or c_n inserted. The solar phi~1e-6
and SNe phi~1 are OBSERVED bounds used as bounds, not fits. Clean on the
fitted-leak axis. **The single GR-leak is Q1 (P2), carried over and firewalled.**

---

## 7. HONEST OVERALL READ (no narrated convergence)

- **a(phi) is NOT a new mathematical escape from GR-equivalence.** The make-or-break
  (3a/3b) is negative: a position-varying scalar weight absorbs by the SAME Bianchi
  tautology as the constant weight, for ANY profile, and self-consistency adds no
  second weight. Mathematically, "a as a function" relabels to GR just as "a as a
  number" did, UNLESS an independent matter ruler exists to make the ratio physical.
- **What the reframe DOES genuinely contribute (real, banked-pending-verifier):**
  (i) it correctly DERIVES a(0)=-1 from the equivalence principle (and exposes that
  Cassini is too loose at solar phi to do this — the anchor is EP, not Cassini);
  (ii) the COMPOSITION FORK cleanly separates the GR branch (composition-respecting
  => constant a => GR) from the UDT branch (composition-BREAKING => function a) and
  identifies the breaker as MATTER HAVING AN INTRINSIC SCALE; (iii) it pins, with a
  mechanism, exactly WHERE the principle stops and the OBJECT is required — the
  junction where the ruler ratio needs an independent matter ruler.
- **The payoff still waits on the matter object.** The reframe re-housed the open
  question with better structure (and a mechanism for why the object is needed), but
  did not move the binary `is a+1 ever nonzero?` off "needs the object." This is the
  SAME terminus as the matter-source MAP — convergent because it is genuinely the
  same dependency, not because of momentum.
- **Tripwire honesty:** this is now TWO MAP passes (matter-source, a-profile) both
  landing on "needs the covariant rest-mass of an actual localized object." That is
  not a refusal-run on a mechanism; it is a consistent CHARACTERIZATION that the
  principle-level work is COMPLETE and the next genuine step is the gated
  object-stage. A third principle-level re-housing would be the "one more thing"
  trap. The honest next move is PONDER with Charles: either (a) gate the object
  (covariant rest-mass pin), or (b) pivot to the firewalled gravity-sector / P2
  question (the only place the GR-leak lives), since on the MATTER side the verdict
  is stably "absorbable until the object speaks."

**NOT canon. MAP + OBSERVE only. Recommend a blind verifier on the script-(A)
arbitrary-W absorbability before any banking.**
