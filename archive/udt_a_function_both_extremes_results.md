# a(phi) as a FUNCTION, carried NONLINEARLY into BOTH extremes — OBSERVE

**Agent:** Claude Opus 4.8 (1M), driver-delegated | **Date:** 2026-06-18
**MODE: OBSERVE.** Premises VISIBLE; report WHAT IS THERE with premises attached.
**NO fitted value. NO Lambda. NO particle mass/ratio derived (DERIVE gated on
Charles). NOT canon. Do not commit (per task).**
Scripts: `a_function_both_extremes.py`, `a_function_carrier_robustness.py`
(sympy, CPU; curvature invariants machine-computed).

**This pass exists to CORRECT three myopic errors** the prior three passes
(`udt_matter_source_MAP_results.md`, `udt_a_profile_MAP_results.md`,
`udt_hbar_pins_a_results.md`) committed — Charles, 2026-06-18: "be a little
sharper. These are very myopic errors":
- **E1** — solving `a` as a CONSTANT. UDT REQUIRES a FUNCTION a(phi): constant
  a=-1 is GR; constant a!=-1 departs EVERYWHERE incl. terrestrial => violates
  "UDT=GR where we test it". Neither constant is UDT.
- **E2** — carrying only CONSTANT-log-rate dilation weights (clock e^{-phi},
  light e^{-2phi}); these can ONLY produce a constant `a`. Must carry the
  intrinsic-scale-vs-metric-scale comparison into the extremes.
- **E3** — constraining at ONE extreme only.

**Definitions (CANON, prior blind-verified):** a(phi)=d(ln m)/dphi;
m(phi)=m0 exp(∫_0^phi a dphi'); ds^2=-e^{-2phi}c0^2dt^2+e^{2phi}dr^2+r^2dOmega^2,
B=1/A; dtau/dt=e^{-phi} (clock), dL/dr=e^{+phi} (ruler), c(phi)=c0 e^{-2phi}
(NONLINEAR); 1+z=e^phi; phi<0 core, phi>0 cosmic (phi~7 at z~1101);
lambda_C=hbar/(m0 c0) (matter intrinsic scale, Sense-1 local).

---

## 0. ONE-LINE BOTTOM LINE (honest, no false convergence)

> **Treating `a` as a FUNCTION and carrying the Compton-vs-metric scale
> comparison nonlinearly DOES produce a genuine a(phi): -1 in the middle,
> departing toward the extremes — and it CHANGES the prior "leans GR" picture.**
> The prior passes' "leans GR" / "constant a=-2W_c-1" was an ARTIFACT of E2:
> they carried only constant-log-rate weights, which are structurally incapable
> of running, so they could only ever return a constant — and the one
> terrestrially-allowed constant is a=-1=GR. Once the control parameter
> **eps(phi) = lambda_C / L_metric** (a dimensionless, frame-clean ratio of the
> object's intrinsic length to the metric's own variation length) is carried in,
> a(phi)+1 = f(eps(phi)) with **f(0)=0** (EP/GR in the middle, forced) and f
> turning on at eps~O(1) (the extremes). The minimal shape gives
> **a(phi) = -1 + k·eps0^p·e^{-pphi}**: a real FUNCTION, flat at -1 across the
> middle, departing EXPONENTIALLY into the core (phi<0) and DECAYING toward
> cosmic (phi>0). **The DIRECTION/asymmetry of the departure is DERIVABLE NOW**
> from the metric's nonlinear dilation (no soliton). **The ONSET phi and the
> magnitude k are OBJECT-GATED.** SNe (a~=-1 to phi~1) is AUTOMATICALLY satisfied
> for a terrestrial-eps0 object on the decaying positive side — it does not need
> to be imposed, it falls out. **NET: a genuine a(phi) departure is now VISIBLE
> and its SHAPE partially derivable; it no longer "bottoms out at GR" — it
> bottoms out at the object's ONSET LOCATION, not at GR.**
>
> **SHARP CAVEAT (from the carrier robustness audit, §3) — do NOT oversell:**
> whether the running is a SIMPLE exponential (constant log-rate) or a genuinely
> RUNNING log-rate depends on which metric scale L_metric is the right one, and
> the corners differ. Proper-gradient L gives a constant log-rate carrier
> (d ln eps/dphi = -1 exactly); curvature-radius L gives a genuinely
> phi-dependent log-rate; coordinate-gradient L makes eps phi-independent (the
> carrier vanishes). The FUNCTION is robust in the proper/curvature corners; it
> is NOT a single forced shape. This is the honest residual.

---

## 1. SET-UP — a(phi) a FUNCTION + the non-absorbable fingerprint (anti-E1)

`a` is a symbolic FUNCTION from line 1 (script Part 0). m(phi)=m0 exp(∫_0^phi a).
The non-absorbable fingerprint (matter ruler / metric ruler):
```
   F(phi) = exp( - ∫_0^phi (a(phi')+1) dphi' ),    d ln F/dphi = -(a(phi)+1).
```
Physics lives wherever **a(phi)+1 != 0**. If a(phi)==-1 on an interval, F is flat
there = GR on that interval. This is the object the prior passes also found — but
they only ever evaluated it with a CONSTANT a (E1), so F was a pure exponential
they could absorb. With a(phi) a function, F is a genuine profile.

(NB the absorbability result of `udt_a_profile_MAP_results.md` §3 — that any
scalar weight exp(∫(a+1)dphi) is Bianchi-absorbable for ANY profile — STILL
holds and is NOT contradicted here. The point is orthogonal: absorbability says
the weight relabels to GR *unless an independent matter ruler exists to compare
against the metric ruler*. eps(phi) = lambda_C/L_metric **IS that independent
ruler ratio**, made explicit. The function a(phi) is the physical content of the
ruler ratio that absorbability says is the sole survivor. So this pass supplies
exactly the "independent matter ruler" the prior pass named as the missing piece
— and shows it is phi-dependent.)

---

## 2. THE DEPARTURE MECHANISM, carried NONLINEARLY (anti-E2) — the core of the pass

The object has an intrinsic length lambda_C = hbar/(m0 c0). The metric has its
OWN variation length L_metric (how fast phi changes — a gradient/curvature
radius). The dimensionless, frame-clean control parameter is
```
   eps(phi) = lambda_C(phi) / L_metric(phi).
```
**Why this is the anti-E2 move:** a constant-log-rate weight (clock e^{-phi}) has
NO eps in it — it cannot know about the object's length vs the metric's length —
so it can only return a constant a. eps is the WHOLE function. At terrestrial phi
lambda_C is microscopic and L_metric is cosmic => eps ~ 0 => a(phi)+1 ~ 0 => GR.
At the extreme (deep core) eps -> O(1) => a departs.

**The requirements on f (a(phi)+1 = f(eps)):** (i) f(0)=0 — EP/GR in the middle,
DERIVED (Part 4 / §4 below); (ii) f turns on at eps~O(1) — the mechanism. The
minimal analytic f with f(0)=0 is f=k·eps^p (p>=1). With (using the proper-gradient
L, §3 corner A) eps(phi) = eps0·e^{-phi}, eps0=(hbar/m0 c0)|phi'(r)|:
```
   a(phi) = -1 + k·eps0^p·e^{-pphi}          [the SHAPE; (k,p) shape, eps0 onset]
   a(phi)+1 = k·eps0^p·e^{-pphi}
   F(phi)  = exp( (k eps0^p/p)(e^{-pphi} - 1) e^{0}... )  [machine, script Part 3]
```
**This is a GENUINE FUNCTION**: a=-1 in the middle, |a+1| GROWS exponentially into
the core (phi<0, e^{-pphi} blows up), DECAYS toward cosmic (phi>0). The DIRECTION
is fixed by the metric's sign of phi — not chosen.

---

## 3. CARRIER ROBUSTNESS AUDIT (the sharp self-prosecution) — `a_function_carrier_robustness.py`

I machine-computed the UDT metric's Ricci scalar (self-consistent phi(r)):
```
 R = (2/r^2) e^{-2phi} [ -2 r^2 phi'^2 + r^2 phi'' + 4 r phi' + e^{2phi} - 1 ]
```
and tested FOUR defensible choices of L_metric, reading d(ln eps)/dphi each:

| corner | L_metric | eps(phi) | d(ln eps)/dphi | carrier? |
|---|---|---|---|---|
| A proper-gradient | e^{+phi}/\|phi'\| | (hbar/m0c0)\|phi'\|e^{-phi} | **= -1** (constant) | real, simple exp |
| B coord-gradient | 1/\|phi'\| | (hbar/m0c0)\|phi'\| | **= 0** | carrier VANISHES |
| C curvature \|R\|^{-1/2} | from R above | runs via (e^{2phi}-1)+grad terms | **phi-DEPENDENT** | real, RUNNING log-rate |
| D areal r (control) | r | phi-independent | 0 | wrong scale (ignores dilation) |

**HONEST READ of the audit (this is the load-bearing correction to my own first draft):**
- The carrier is NOT a single forced object. In the PROPER-gradient corner (A) it
  is real but has a CONSTANT log-rate (-1) — a(phi) still runs (e^{-pphi}) but as a
  pure exponential. In the CURVATURE corner (C) the log-rate genuinely RUNS (because
  R carries the `e^{2phi}-1` term that competes with the gradient terms — the
  metric's intrinsic nonlinearity). In the COORDINATE-gradient corner (B) the
  carrier VANISHES and eps is phi-independent — which would re-collapse toward a
  constant-a-like behavior.
- So the answer to "does carrying nonlinear dilation + Compton-vs-metric produce a
  running a(phi)?" is: **YES in the proper-gradient and curvature corners (the
  physically right ones — an object lives in the dilated PROPER space, and its size
  competes with the CURVATURE radius), NO in the coordinate-gradient corner.** The
  function is robust to the physical choices; it dies only under the coordinate
  choice that ignores the dilation the object sits in.
- **The genuinely RUNNING-log-rate behavior (corner C)** is the most interesting:
  there the departure shape is set by `e^{2phi}-1` vs the gradient — i.e. the
  metric's OWN nonlinear self-term (the same `e^{2phi}` that the prior gravity-sector
  flag — `relativistic-foundation-and-bare-solve` — suspects of NOT folding away).
  This is a lead, not a result: it ties a(phi)'s running to the curvature scalar,
  hence potentially to the gravity-sector question, NOT only the matter weight.

This audit is exactly the place E2 would re-enter (pick corner B, get a constant)
or be over-sold (claim a unique running shape). I am flagging both: the function
is real in the right corners; its precise running is corner-dependent and NOT yet
uniquely pinned.

---

## 4. ANCHOR a(0) = -1 (the MIDDLE) — DERIVED from EP

At phi=0, for any terrestrial object lambda_C << L_metric => eps -> 0 => f(eps) -> 0
=> a(0)+1 = 0 => **a(0) = -1**. Equivalently the Bianchi exchange force
(a+1)phi'T -> 0 (no fifth force; lab matter free-falls with the metric). DERIVED,
forced. This is the EP anchor, and it is AUTOMATIC in the mechanism (f(0)=0), not
imposed separately. (Same anchor as `udt_a_profile_MAP_results.md` §1a, now a
consequence of eps->0 rather than a standalone postulate.)

---

## 5. BOTH EXTREMES CONSTRAINED (anti-E3)

### 5a. NEGATIVE-phi (hadronic core, phi~-0.8 to -1.14) — the EXPECTED departure
A FUNDAMENTAL particle at the core has lambda_C ~ its own size ~ L_metric (the cell
over which phi varies) => **eps ~ O(1)** => a(phi)+1 ~ O(k) = O(1): a GENUINE,
NON-TINY departure. The carrier e^{-pphi} with phi<0 AMPLIFIES it (e^{+p|phi|}>1).
So toward the deeper core |a(phi)+1| GROWS. At the definitional extreme eps=1,
a(phi_core) = -1 + k with k=O(1). **a != -1 at the core is now VISIBLE as a
function value, not a menu choice.** (Magnitude k and the exact onset are
object-gated — §6. The DIRECTION "departs more, deeper in" is derived.)

### 5b. POSITIVE-phi (cosmic) — SNe pins a~=-1 to phi~1, AUTOMATICALLY
SNe: d_L = r·e^{phi} (one factor 1+z), shape mu_g-M-degenerate, matches GR/LCDM to
z~2 i.e. phi up to ~1 (validated_results.md §4: ~0.06 mag RMS vs LCDM, shape
mu_g-independent). On the positive side e^{-pphi} DECAYS, so a(phi)+1 = k eps0^p
e^{-pphi} is SMALLER at phi~1 than at phi=0. For a terrestrial-eps0 standard-candle
object (eps0<<1), a+1 is already << 1 at phi=0 and even smaller across [0,1].
=> **SNe is satisfied with room to spare — it is not an imposed constraint, it
FALLS OUT** of the decaying positive-side carrier. Read as a BOUND: any
positive-side departure onsets DEEPER than phi~1 (toward the boundary phi~7), and
only for a COSMIC-SCALE ruler whose eps0~O(1) — not for the lab object. (script
Part 4b: ∫_0^1 (a+1)dphi = k eps0^p (e^p-1)e^{-p}/p, << 1 for terrestrial eps0.)
**The two extremes are genuinely ASYMMETRIC**: core amplifies, cosmic decays —
the e^{-pphi} carrier's sign-of-phi structure does this automatically.

---

## 6. UNIVERSAL SHAPE vs OBJECT-SET ONSET (the split the prior passes collapsed)

a(phi) = -1 + k·eps0^p·e^{-pphi}. Three knobs:

| knob | meaning | derivable NOW? |
|---|---|---|
| **e^{-pphi} carrier (direction)** | core-amplifies / cosmic-decays asymmetry | **YES** — metric's nonlinear dilation; no object. (corner-dependent log-rate, §3) |
| **p** (eps-power in f) | shape near the extreme: gradient-response (p=1) vs curvature-response (p=2) | **PARTIALLY** — small DISCRETE set from how the matter action responds to varying phi (leading order); derivable from the action without a full soliton. OPEN which. |
| **eps0 = (hbar/m0c0)\|phi'\|** | ONSET location (the phi where eps~1) + magnitude k | **NO — OBJECT-SET.** Carries the object's mass m0 (Compton) and its confinement gradient phi'. Needs the object. |

**DERIVABLE NOW (no soliton):** the EXISTENCE of a genuine a(phi), the EP anchor
a(0)=-1, the DIRECTION/asymmetry (departs into the core, decays to cosmic), the
SNe-automatic positive side, and the small discrete shape-set {gradient, curvature}.
**OBJECT-GATED:** the ONSET phi (where the departure turns on) and its magnitude k
— these carry the object's Compton length and confinement scale.

---

## 7. PREMISE LEDGER (chose vs derived) + every smuggle-surface

| # | Item | chose / derived | smuggle / GR-leak / E1-E2-E3 risk |
|---|---|---|---|
| L1 | Metric form, dtau/dt=e^{-phi}, dL/dr=e^{+phi}, c=c0 e^{-2phi} | **DERIVED** (CANON) | — |
| L2 | a(phi) a FUNCTION (not constant) | **FRAMING (Charles, anti-E1)** | the whole pass; if collapsed to constant => E1 |
| L3 | fingerprint F=exp(-∫(a+1)) | **DERIVED** | — |
| L4 | control param eps = lambda_C/L_metric | **CHOSE the mechanism** (Charles's Compton-vs-metric) | this IS the anti-E2 carrier; if eps phi-indep => E2 returns (corner B) |
| L5 | lambda_C = hbar/(m0 c0), Sense-1 local | **DERIVED** (Compton, fixed locally) | clean |
| L6 | L_metric choice (proper-grad / curvature / coord) | **CHOSE among 4; AUDITED §3** | **THE residual**: corner A const-log-rate, C running, B vanishes. Function robust in A,C; dies in B. NOT uniquely forced. |
| L7 | f(eps)=k eps^p, p>=1, f(0)=0 | **CHOSE minimal form**; f(0)=0 DERIVED (EP) | the SHAPE near extreme is a small discrete set, not forced; flagged |
| L8 | a(0)=-1 | **DERIVED** (eps->0 / EP) | the middle anchor; forced |
| L9 | core eps~O(1) => O(1) departure | **DERIVED direction**; magnitude OBJECT-SET | the expected departure; magnitude needs object |
| L10 | SNe => a~=-1 to phi~1 | **DERIVED as BOUND**; falls out of decaying carrier | no value fit |
| L11 | (k, eps0, onset phi) | **OBJECT-GATED** (UNDETERMINED now) | the genuinely open piece |
| L12 | left side = standard Einstein (carried) | **CHOSE** (firewalled) | primary GR-leak lives in gravity sector, untouched here; but §3 corner C ties a(phi)'s running to R => the curvature term `e^{2phi}-1` => possible link to the gravity-sector question |

**Where the answer could be smuggled (named, sharp):**
1. **L6 corner choice IS the E2 re-entry / over-sell surface.** Picking coordinate-
   gradient (corner B) kills the carrier and re-collapses to a constant (E2 returns).
   Picking a single corner and claiming a UNIQUE running shape over-sells. Honest
   statement: the function is robust in the proper/curvature corners; the precise
   running is corner-dependent and not uniquely pinned. AUDITED, not hidden.
2. **L7 shape form.** k·eps^p is the MINIMAL choice; the true f could be richer. I
   claim only f(0)=0 (derived) + turns-on-at-O(1) (mechanism) + the discrete
   gradient/curvature shape-set. The exact f is object/action-gated.
3. **No fitted/SM/wall/macro/Lambda number used.** lambda_C, eps0, k, p all symbolic.
   phi_core~-1 and SNe phi~1 are OBSERVED bounds used as bounds. Data-blind. Clean.
4. **E1 check:** `a` is a function throughout; NO constant is relayed as the answer.
5. **E3 check:** BOTH extremes constrained (§5a core, §5b cosmic) + the middle
   anchor (§4). Not a single-extreme slice.

---

## 8. HONEST OVERALL READ — does this change the prior "leans GR" picture? YES (partially)

- **The prior "leans GR" was an E2 artifact.** All three prior passes carried only
  constant-log-rate weights and so could only return a constant a; the unique
  terrestrially-allowed constant is a=-1=GR; the driver relayed "leans GR" without
  catching that the constant assumption EXCLUDED the physics. Once the
  Compton-vs-metric ratio eps(phi) is carried in, a(phi) is a genuine function and
  the "leans GR" terminus dissolves: a=-1 holds ONLY in the middle (where it
  SHOULD, by EP/SNe), and departs at the extremes.
- **What is now genuinely VISIBLE/derivable (no soliton):** a real a(phi) profile;
  a(0)=-1 forced; the DIRECTION (departs into the core, decays toward cosmic — an
  asymmetry the constant treatment could never show); SNe satisfied automatically;
  a small discrete shape-set for the near-extreme behavior.
- **What is still OBJECT-GATED:** the ONSET phi (where the departure turns on) and
  the magnitude k — these carry the object's Compton length and confinement scale.
  So the pass does NOT "bottom out at GR" (the prior terminus) — it bottoms out at
  the object's ONSET LOCATION, a different and more honest place. The departure
  EXISTS and has a derivable DIRECTION/SHAPE-class; only its LOCATION/SIZE needs
  the object.
- **A genuine lead (not banked):** in the curvature corner (§3-C) a(phi)'s running
  is set by R's `e^{2phi}-1` term — the SAME nonlinear metric self-term the
  gravity-sector flag suspects of not folding away. This hints the matter-side
  a(phi) running and the firewalled gravity-sector question may be TWO FACES of the
  one nonlinearity. Flagged for PONDER, NOT derived.
- **Tripwire honesty:** this is the FOURTH pass on the dilation exponent, but it is
  NOT a "one more thing" re-housing — it is the pass that CORRECTS the shared E1/E2/E3
  error of the prior three. The prior three all landed at "constant, needs the
  object / leans GR"; this one shows that terminus was the artifact, and relocates
  the genuine open piece to ONSET LOCATION (object-gated) while making the
  EXISTENCE + DIRECTION + middle-anchor + cosmic-bound derivable now. The honest
  residual is L6 (which metric scale) — a sharp, named, finite question, NOT a
  refusal-run.

**Single cleanest statement:**
> Carrying the object's intrinsic Compton length against the metric's own variation
> length as a dimensionless ratio eps(phi)=lambda_C/L_metric — the nonlinear
> comparison the prior constant-log-rate passes structurally omitted — turns the
> mass-dilation exponent into a genuine FUNCTION a(phi) = -1 + k·eps0^p·e^{-pphi}:
> exactly -1 in the middle (EP-anchored, SNe-confirmed to phi~1), departing
> EXPONENTIALLY into the hadronic core (phi<0, amplified) and DECAYING toward the
> cosmic boundary (phi>0). The EXISTENCE, the EP anchor, the DIRECTION/asymmetry,
> the automatic SNe satisfaction, and a small discrete near-extreme shape-set are
> DERIVABLE NOW without a soliton; the ONSET phi and magnitude k are OBJECT-GATED.
> This dissolves the prior "leans GR" terminus as an artifact of the constant
> assumption (E2) and relocates the genuine open question from "is a=-1?" to
> "WHERE does a depart?" — a location set by the object, not a verdict that bottoms
> out at GR. SHARP RESIDUAL: the precise running is corner-dependent (proper-gradient
> = constant log-rate; curvature = running; coord-gradient = vanishes) — robust in
> the physical corners, not a single forced shape. NOT canon; OBSERVE only. Recommend
> a blind verifier on (i) the §3 carrier-robustness corners and the Ricci scalar, and
> (ii) the claim that f(0)=0 is the EP anchor and not a smuggled choice, before banking.

---

## 9. ATTACK HERE (for the blind adversarial verifier)

1. **§3 carrier audit (load-bearing).** Re-compute the Ricci scalar of the UDT
   metric; confirm d(ln eps)/dphi = -1 (corner A), = 0 (corner B), phi-dependent
   (corner C). Is corner A or C the physically correct L_metric, or did the doc
   cherry-pick to keep a carrier? Could the coordinate corner (B, carrier vanishes)
   be the right one — re-collapsing to a constant (E2)? This is the make-or-break
   for "is the function real or smuggled."
2. **eps as the right control parameter.** Is lambda_C/L_metric genuinely the
   dimensionless object the absorbability result names as "the independent matter
   ruler"? Or is it a hand-built ratio? Tie it back to F=exp(-∫(a+1)) explicitly.
3. **f(0)=0 = EP, not smuggled.** Confirm a(0)=-1 follows from eps->0 (terrestrial
   lambda_C<<L_metric) AND from the Bianchi exchange force, independently.
4. **The asymmetry.** Confirm the core-amplifies / cosmic-decays direction is forced
   by the sign of phi in e^{-pphi}, not chosen. Confirm SNe (positive side) is
   satisfied automatically, not imposed.
5. **Universal-vs-object split.** Confirm (k, eps0, onset) are genuinely object-set
   and the direction/EP-anchor/cosmic-bound are genuinely object-free. No leak of an
   onset value.
6. **Data-blind.** Confirm no fitted/SM/wall/macro/Lambda number; phi_core~-1 and
   SNe phi~1 used as bounds only; lambda_C/k/p/eps0 symbolic.
7. **E1/E2/E3 self-check.** Confirm `a` is a function throughout (no constant relayed
   as the answer, E1), the nonlinear eps-carrier is carried into both extremes (E2),
   and both extremes + middle are constrained (E3).
