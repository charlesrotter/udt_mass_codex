# Native Derivation of UDT's Universal Dilation-Weight on the Action

**Mode:** METRIC-LED, OBSERVING NOT TARGETING (declared up front). Gated DERIVE,
authorized by the foundational-assumptions audit (F0-F8), 2026-06-21.
**Category-A, DATA-BLIND**: derive from the relativistic principle (R1-R3) only;
import no mechanism, no conformal-weight table, no mass/ratio/wall number.

**Constructor:** Claude Opus 4.8 (1M), agent for udt_mass_codex, 2026-06-21.
**Scripts (new, this push, nothing committed):** `/tmp/dilation_weight*.py`
(sympy, CPU, analytic). All symbolic claims below are machine-checked by those
scripts unless tagged ANALYTIC.

**Verifier-before-record:** an ATTACK HERE block is provided at the end; a blind
adversarial pass is required before this result is treated as banked.

---

## 0. DECLARED FRAMING (binding discipline)

- **Question type:** METRIC-LED — "what weight does UDT's own relativistic
  principle FORCE on each piece of the action?" NOT template-led, NOT
  verdict-hunting. I did not steer the weight toward a GR-departure (richer
  physics) NOR toward plain-GR (Cassini-safe). I report what the rule forces and,
  where it under-determines, I say so.
- **TWO-PLAYER (Charles 2026-06-21):** phi and the metric are INDEPENDENT
  dynamical players. phi is NOT slaved to g_tt. Every step below keeps phi as an
  independent field; the corpus's slaving (phi = -1/2 ln(-g_tt)) is NOT used.
- **Principle 7:** I do NOT default to the Einstein-Hilbert R-term as "the"
  gravity action. I ask what invariance the principle demands and let the weighted
  curvature object emerge. I interrogate the "folds away / reduces to standard"
  steps — and indeed one of them (the angular-curvature term) does NOT fold away,
  which is the central finding.
- **The lever (Charles-blessed):** R1 applied to the ACTION = invariance under the
  GLOBAL constant shift phi -> phi + lambda. NOT full local Weyl (that washes phi
  out — wrong). NOT dropped (that gives back plain EH — wrong). The constant mode
  of phi is gauge; the VARYING part stays physical.

---

## 1. THE GROUND TRUTH (verified by reading the corpus)

Metric form, areal / gradient-aligned slice
(`relativistic_metric_rederivation_results.md:149,238`):
```
g_tt = - e^{-2 phi} c^2 ,   g_rr = e^{+2 phi} ,   angular = r^2 dOmega^2 ,
g_tt g_rr = -c^2  (R3 reciprocity, B=1/A).
```
**Induced transformation under phi -> phi + lambda (lambda CONSTANT):**
```
g_tt    -> e^{-2 lambda} g_tt          (the (t) clock factor)
g_rr    -> e^{+2 lambda} g_rr          (the radial / gradient ruler)
angular block r^2 dOmega^2  -> UNCHANGED   (phi-free)
sqrt(-g) = c r^2 sin(theta)  -> UNCHANGED   (phi-free; the dilation factors CANCEL
                                             under B=1/A; verified script 1)
```
This is **NOT** a uniform conformal rescaling. It acts on the (t,r) "gradient
block" only; the transverse/angular block and the measure are inert. Every weight
below is derived from THIS actual induced transformation — no textbook conformal
weight is imported. (CRITICAL FACT verified: `em_forcing_results.md:171`,
script 1 reproduces sqrt(-g)=c r^2 sin(theta), invariant.)

**KEY SILENCE (verified `relativistic_metric_rederivation_results.md`):** R1-R3 as
written pin only the metric FORM (exponential clock law + reciprocal tie). They say
nothing directly about the action/weight/curvature/rest-mass. The task is to extend
the principle's OWN logic (R1 = only depth DIFFERENCES are physical) to the action.

---

## 2. PREMISE LEDGER (chose vs derived)

| # | Premise / choice | Status |
|---|---|---|
| P1 | Metric form g_tt=-e^{-2phi}c^2, g_rr=e^{2phi}, angular r^2dOmega^2 | DERIVED (R1-R3, corpus, verified) |
| P2 | R3 reciprocity B=1/A => measure phi-free | DERIVED (corpus, re-verified script 1) |
| P3 | **R1-on-the-action = invariance under GLOBAL phi->phi+const** | **CHOSE (interpretive; the Charles-blessed lever). FLAGGED VISIBLE.** |
| P4 | phi is an INDEPENDENT player (not slaved) | CHOSE (Charles ruling 2026-06-21) |
| P5 | "Universal" = ONE invariance RULE applied to every term (Premise 2, Charles) | CHOSE (owner premise) |
| P6 | Regularity of weights (continuous/monotone) so R2 -> pure exponential | ASSUMED (named; same as the metric derivation's regularity premise) |
| P7 | Areal chart, gradient-aligned, static SSS slice for the explicit R computation | CHOSE (CANON C-2026-06-18-1 slice; used only to EXHIBIT, the shift-algebra is chart-independent) |
| P8 | Cassini |gamma-1|<2.3e-5 (weak-field LOCAL probe only) | observational input (labeled local probe) |
| D1 | Kinetic weight = e^{+2 phi} | **DERIVED (R1, script 1)** |
| D2 | Rest-mass weight a(phi) = e^{+ phi} | **DERIVED (R1, script 2)** |
| D3 | Curvature: gradient-sector weight e^{+2phi}; transverse/angular curvature NOT homogenizable by any single power | **DERIVED (R1, scripts 3-5) — the central finding** |
| D4 | R2 forces EXPONENTIAL form of every weight, does NOT fix exponent | DERIVED (ANALYTIC, Cauchy equation) |
| D5 | R3 (B=1/A) SOURCES the kinetic exponent +2 (= 2x rest-mass +1) | DERIVED (script 6) |

---

## 3. R1 DERIVATION — the weight on each piece (sympy-checked)

**Reading of R1-on-the-action (VISIBLE interpretive step P3):** "only depth
DIFFERENCES are physical" => the action integral must be UNCHANGED when every phi
is shifted by the same constant lambda. The constant mode of phi is pure gauge;
the varying part is physical. Method: for each term, compute its bare shift-weight
(the power of e^{lambda} it picks up), then the required weight W(phi) is the EXACT
INVERSE of that bare shift-weight. This is ONE rule (P5).

### (i) Depth-field kinetic term  ->  weight e^{+2 phi}  [DERIVED, script 1]
Bare kinetic scalar = g^{rr}(d_r phi)^2 = e^{-2 phi}(phi')^2 (since g^{rr}=1/g_rr).
Under the shift: phi' unchanged (lambda constant), g^{rr} -> e^{-2lambda} g^{rr}.
So the bare scalar -> e^{-2lambda} x itself. sqrt(-g) invariant. Required weight
must supply e^{+2lambda}:  **W_kin(phi) = e^{+2 phi}**. Then
```
sqrt(-g) * e^{2phi} * g^{rr}(phi')^2 = sqrt(-g) * (phi')^2   (script 1: = (phi')^2),
```
manifestly shift-invariant (no phi prefactor remains).

### (iii) Particle rest-mass coupling a(phi)  ->  weight e^{+ phi}  [DERIVED, script 2]
Point-particle action S_m = - integral m c^2 a(phi) dtau, dtau = sqrt(-g_tt)/c dt =
e^{-phi} dt for a static particle. Under the shift dtau -> e^{-lambda} dtau. For
m a(phi) dtau invariant, need a(phi) -> e^{+lambda} a(phi):  **a(phi) = e^{+ phi}**,
power +1. Check (script 2): a(phi) dtau ~ e^{phi} e^{-phi} = 1 (phi-free, invariant).

**The +2 vs +1 anisotropy (REAL, not a slip):** the kinetic term couples to the
FULL inverse metric g^{rr} ~ e^{-2phi} (TWO metric powers); the rest-mass couples to
sqrt(-g_tt) ~ e^{-phi} (ONE clock power). The exponent of the weight = the number
of metric/clock factors the term carries. SAME rule, different exponent because
different tensorial valence. This is exactly the anisotropy the brief warned about —
derived natively, not imported.

### (ii) Curvature term  ->  THE CENTRAL FINDING: R is INHOMOGENEOUS under the shift
[DERIVED, scripts 2-5]. The Ricci scalar of the actual UDT metric (computed from
scratch, script 2):
```
R = e^{-2phi}[ -4 phi'^2 + 2 phi'' + 8 phi'/r ]  +  2/r^2  -  (2/r^2) e^{-2phi}.
        \________ gradient (t,r) sector ________/    \__ angular __/  \_ frame _/
```
Decompose by shift-weight (script 3):
- **A** (derivative piece, e^{-2phi}) -> e^{-2lambda} A
- **B** = 2/r^2 (the transverse / angular curvature, phi-FREE) -> **SHIFT-INVARIANT**
- **C** = -(2/r^2)e^{-2phi} -> e^{-2lambda} C

**R carries TWO different shift-weights at once (0 and -2lambda).** Because
sqrt(-g) is invariant, **no single power weight W_R=e^{k phi} can make sqrt(-g) W_R R
shift-invariant.** Trying W_R = e^{+2phi} (the kinetic weight) homogenizes A and C
(ratio 1 under shift, script 3) but leaves B picking up e^{+2lambda} (script 3).

Explicitly (scripts 4-5), the weighted density is
```
sqrt(-g) e^{2phi} R = 2c sin(theta)[ -2 r^2 phi'^2 + r^2 phi'' + 4 r phi' + e^{2phi} - 1 ],
```
and under the shift only the **e^{2phi}** term moves:
```
L(phi+lambda) - L = 2c sin(theta) (e^{2lambda}-1) e^{2phi}     (script 4).
```
After integration by parts in r (boundary dropped, script 5) the shift-invariant
BULK is:
```
L_bulk = 2c sin(theta)[ -2 r^2 (phi')^2 + 2 r phi' + e^{2phi} - 1 ].
```
- The **-2 r^2 (phi')^2** is the NATIVE KINETIC INVARIANT — it is precisely the
  e^{2phi}-weighted kinetic term of (i), confirming the SAME e^{2phi} weight on
  geometry and on the depth-field. Geometry and kinetic share ONE weight: the
  universal rule holds for them.
- The **e^{2phi}** survivor is the ANGULAR / transverse curvature (the 2/r^2 = the
  intrinsic curvature of the constant-phi 2-spheres re-expressed through the frame).
  It is NOT shift-invariant: it acts as an intrinsic POTENTIAL V(phi) ~ e^{2phi}
  that gives phi a PREFERRED depth scale — which is exactly what R1 forbids.

**THE FORK (reported explicitly, not silently resolved):** R1-on-the-action lands
cleanly on the kinetic and gradient-curvature weight = e^{2phi}, but it CANNOT
simultaneously honor the angular-curvature term with the same single power. Two
honest branches:
- **Branch G (gauge the constant mode strictly):** keep only the manifestly
  shift-invariant remnant (native kinetic (phi')^2 + gradient-sector curvature);
  the bare e^{2phi} angular-potential is NOT an allowed term of a strictly
  R1-invariant action. This is the clean two-player scalar-tensor theory of Sec 5.
- **Branch P (keep the angular curvature as a physical potential):** accept that
  the transverse curvature is a real geometric source that DOES distinguish a depth
  scale (the angular block is phi-free, so it legitimately breaks the global shift
  — the cell SIZE r is physical). Then R1-on-the-action is OBSTRUCTED by the
  anisotropy: the angular sector is the one place a depth scale can legally enter.
  **This is structurally aligned with Charles's standing hunch that discreteness /
  scale comes from the phi-ANGULAR interaction** — here the angular curvature is
  exactly the term R1 cannot wash out.

The brief's instruction "locate exactly where the constant-shift demand lands" is
answered: it lands FULLY on kinetic + gradient-curvature (weight e^{2phi}) and is
OBSTRUCTED by the angular-curvature term, because the angular block is phi-free.
The obstruction is not a failure of the derivation — it is the native statement
that UDT's anisotropy prevents a single universal conformal weight, and isolates
the angular sector as the carrier of any physical depth scale.

---

## 4. R2 AND R3 CROSS-CHECKS + FORK ANALYSIS (Charles's explicit instruction)

**R2 (consistent composition / one-parameter group), script 6.** A weight that is
itself built from clock/ruler dilations must compose by the SAME Cauchy functional
equation that forced g_tt: g(x)g(y)=g(x+y) => exp. The rest-mass weight a(phi) IS
literally a dilation factor on dtau, so R2 FORCES it to be a PURE EXPONENTIAL
e^{k_m phi} (no polynomial / no admixture). R2 does the same to the kinetic weight.
**R2 REFINES the FORM (every weight must be pure exponential) but does NOT fix the
EXPONENT.** No conflict with R1: R1 supplies the exponents (+2, +1), R2 confirms
they sit in pure exponentials. **CONFIRMS R1, does not over-determine the exponent.**

**R3 (reciprocity, B=1/A), script 6.** R3 is UPSTREAM of the kinetic exponent: it
is precisely B=1/A that makes g^{rr}=e^{-2phi}, which is WHY the bare kinetic scalar
carries e^{-2phi} and the weight must be e^{+2phi}. R3 also explains the +2-vs-+1
factor: the kinetic couples to the full inverse metric (two phi powers), the
rest-mass to sqrt(-g_tt) (one phi power). **R3 SOURCES (consistently over-determines)
the kinetic exponent and EXPLAINS the anisotropy. CONFIRMS R1; no conflict.**

**Net fork status:**
- The EXPONENTS (kinetic +2, rest-mass +1, gradient-curvature +2) are
  CONFIRMED by all three (R1 fixes, R2 confirms exponential form, R3 sources). NOT
  a fork — pinned.
- The fork is elsewhere and is TWO-FOLD:
  (a) the angular-curvature obstruction (Branch G vs Branch P above) — R1/R2/R3
      do not resolve whether the angular potential is gauged away or kept physical;
  (b) the dimensionless RATIO X of kinetic-to-curvature weight (Sec 5) — R1/R2/R3
      fix that BOTH terms wear e^{2phi}, but NOT their relative coefficient.
  Both forks are reported, neither is silently picked.

---

## 5. CONSEQUENCE 1 — BIRKHOFF / does vacuum still freeze?  [script 9]

The clean (Branch G) invariant two-player action is
```
S = integral sqrt(-g) [ f(phi) R + X f(phi) g^{munu} d_mu phi d_nu phi ],
    f(phi) = e^{+2 phi},  phi an INDEPENDENT player.
```
Metric variation gives the scalar-tensor structure
```
f(phi) G_munu + (g_munu box - nabla_mu nabla_nu) f(phi) = (1/2) T^phi_munu.
```
The coefficient on R is NON-CONSTANT (f=e^{2phi}). Computed from scratch (script 9):
```
box f = 2 phi'' + 4 phi'/r   != 0  for any non-constant phi.
```
So the (g box - nabla nabla)f terms SURVIVE in vacuum.

**BIRKHOFF VERDICT: vacuum != GR.** With a NON-CONSTANT derived weight AND phi an
INDEPENDENT player, the static round vacuum is NOT automatically frozen to
Schwarzschild: the f-derivative terms couple phi's profile back into the metric
equation. Structured / non-static vacuum is ADMITTED. This is robust to the exact
power — ANY non-constant f gives a surviving box f (corpus claim CONFIRMED,
script 9). **This DEPARTS from the current classical-continuum headline**, which was
established on the SLAVED / EH-frozen reading. With the derived weight and two
players, the classical metric does MORE than freeze to a continuum.

(Honest caveat: "does more" = admits non-trivial vacuum coupling; whether that
yields DISCRETE structure is a SEPARATE solver question, not claimed here. This is
the structural door, not a spectrum.)

---

## 6. CONSEQUENCE 2 — CASSINI / PPN gamma  (weak-field LOCAL probe)  [scripts 7-8]

Map the Branch-G action to Brans-Dicke form. The BD scalar is the curvature weight
Phi_BD = f = e^{2phi}; dPhi_BD = 2 e^{2phi} dphi, so the BD kinetic
-(omega/Phi)(dPhi)^2 = -4 omega e^{2phi}(dphi)^2 matches our +X e^{2phi}(dphi)^2 at
```
omega = - X / 4 ,    gamma = (1+omega)/(2+omega) = (X-4)/(X-8)   (script 8).
|gamma - 1| = 4 / |X - 8|.
```
- gamma -> 1 requires |omega| -> infinity, i.e. a LARGE native kinetic coefficient.
- Cassini |gamma-1| < 2.3e-5 forces |X - 8| > 1.74e5, i.e. |X| >~ 1.7e5 (script 8).

**RE-GRADE OF THE OLD f(phi)R CASSINI DEATH (honest):** the gamma=9 death carried
premise set {f = c0^4 e^{-8phi}/16piG (exponent -8), NO bare kinetic term, phi
SLAVED, static-SSS} (`gravity_sector_local_reduction_results.md:21-26,196-198`).
The NATIVE two-player theory differs on THREE of those premises:
1. **Exponent:** derived weight is e^{+2phi}, NOT e^{-8phi}. (The -8 came from
   f = c0^4 e^{-8phi}/16piG, an EH-frame slaved construction, not from R1.)
2. **Bare kinetic term:** the native theory HAS one INTRINSICALLY — it is the
   shift-invariant remnant (Sec 3, the -2r^2(phi')^2 term), with coefficient X.
   The death's premise A6 ("no bare kinetic term") is FALSE for the native theory.
3. **phi independent, not slaved:** the death used phi=-1/2 ln g_tt; we forbid it.

The death's own L7 noted that a bare kinetic X(dphi)^2 with X >~ 40000 forces
gamma->1 — there it was a POSITED rescue mechanism (rightly flagged Principle-1).
**Here that kinetic term is NOT posited: R1 forces its PRESENCE.** But R1/R2/R3 do
NOT fix its COEFFICIENT X.

**CASSINI VERDICT: UNDETERMINED at the kinematic (R1-R3) level — NOT a death, NOT a
pass.** gamma is a one-parameter family gamma(X)=(X-4)/(X-8). Large |X| (>~1.7e5)
clears Cassini; small X fails. R1/R2/R3 pin the EXPONENT (e^{2phi}) but leave the
 kinetic-to-curvature RATIO X free, so they cannot decide Cassini. The honest
status is "the native weight is Cassini-COMPATIBLE for a range of X, Cassini-failing
for another; the principle does not select X." I did NOT target "passes."

This is a genuinely different verdict from the f(phi)R gamma=9 death: that death's
gamma=9 was an O(1) FIXED number with no free coefficient (no bare kinetic, fixed
exponent). The native theory has a free X precisely because the bare kinetic term is
intrinsic. The f(phi)R death is RE-GRADED to "f(phi)R-branch only" (its premise set
is not the native two-player premise set); it does not transfer to the derived
theory.

---

## 7. WHAT IS FORCED vs WHAT IS OPEN (crisp summary)

**FORCED (pinned by R1, confirmed by R2/R3):**
- Kinetic weight on the depth field: **e^{+2 phi}**.
- Rest-mass coupling: **a(phi) = e^{+ phi}** (power +1).
- Gradient-sector curvature weight: **e^{+2 phi}** (SAME as kinetic — geometry and
  depth-field share one weight; the universal rule holds on this sector).
- The UNIVERSAL RULE itself: weight each term by the EXACT INVERSE of its own bare
  constant-shift weight (= demand global-shift invariance). ONE rule; exponent per
  term = number of metric/clock factors it carries (+2, +1, +0). "Same depth-law" =
  same INVARIANCE PRINCIPLE, not literally same power.
- R2 forces every weight to be a PURE EXPONENTIAL (no polynomial admixture).
- R3 (B=1/A) SOURCES the +2 kinetic exponent and explains the +2-vs-+1 anisotropy.
- BIRKHOFF: with the non-constant weight + two independent players, **vacuum != GR**
  (box f survives). The classical metric does MORE than freeze to a continuum
  (structural door; robust to the exact power).

**OPEN / UNDER-DETERMINED (reported, not forced):**
- **The angular-curvature obstruction (the deepest fork):** R1 CANNOT homogenize the
  transverse/angular curvature (phi-free angular block) with the same single power.
  Branch G (gauge it away -> clean shift-invariant scalar-tensor) vs Branch P
  (keep e^{2phi} as a physical potential that the anisotropy LEGITIMATELY admits,
  carrying a depth scale in the angular sector). R1/R2/R3 do not decide. **Branch P
  is structurally aligned with the phi-angular discreteness hunch** — the angular
  sector is exactly where a depth scale can enter.
- **The kinetic-to-curvature ratio X:** R1/R2/R3 fix that BOTH wear e^{2phi} but not
  their relative coefficient. gamma = (X-4)/(X-8) is a one-parameter family.
- **CASSINI: UNDETERMINED** — Cassini-compatible for |X|>~1.7e5, failing for small
  X. The principle does not select X. (Old f(phi)R gamma=9 death RE-GRADED to
  f(phi)R-branch-only; does not transfer — different exponent, intrinsic bare
  kinetic, phi unslaved.)
- Whether the admitted non-trivial vacuum yields DISCRETE structure (a spectrum) is
  a separate SOLVER question, not addressed here.

**One-line headline:** the relativistic principle's constant-shift demand FORCES
the universal weight e^{+2phi} on the depth-field kinetic term and on the
gradient-sector curvature, and a(phi)=e^{+phi} on rest-mass (one rule, valence-set
exponents; R2/R3 confirm) — but it is OBSTRUCTED by UDT's anisotropy at the
angular-curvature term, which it cannot wash out, leaving (i) a clean-vs-physical
fork on that angular potential and (ii) the kinetic/curvature ratio X free, so that
Birkhoff is BROKEN (vacuum != GR, classical metric does more) while Cassini is
UNDETERMINED rather than dead.

---

## 8. ATTACK HERE (for the blind verifier — required before banking)

1. **The R1-on-the-action reading (P3).** Is "invariance under global phi->phi+const"
   the right native extension of R1, or a smuggled frame? Check it is NOT secretly
   full local Weyl (it is not: lambda is constant; the varying part of phi stays
   physical, and the angular obstruction PROVES phi is not washed out).
2. **The induced transformation.** Re-verify g_tt->e^{-2lambda}g_tt, g_rr->e^{+2lambda}g_rr,
   angular & measure invariant (script 1). A sign error here flips every exponent.
3. **The kinetic exponent.** Is g^{rr}(phi')^2 the right bare kinetic scalar, and
   does e^{+2phi} really homogenize it (script 1)? Check the +2 is not a doubled +1.
4. **The R inhomogeneity (the central claim).** Re-derive R (script 2) and the
   A/B/C decomposition (script 3). Is the e^{2phi} survivor genuinely the angular
   curvature, or an IBP / chart artifact? Try isotropic chart: does the obstruction
   persist, or is it areal-chart-specific? (Chart-robustness NOT yet checked — flag.)
5. **The IBP boundary term (script 5).** I dropped it. Could the boundary term
   restore shift-invariance of the angular piece, dissolving Branch P? Check.
6. **rest-mass +1.** dtau uses only sqrt(-g_tt); is the static-particle restriction
   hiding a velocity-dependent weight for moving particles? Check a geodesic, not
   just a static worldline.
7. **The BD mapping / gamma(X).** Re-verify omega=-X/4 and gamma=(X-4)/(X-8)
   (script 8). Is the BD identification legitimate given phi is independent (not the
   slaved case that gave gamma=9)?
8. **X really free?** Does any deeper consistency (unitarity, sign of kinetic energy,
   ghost-freedom) constrain X and thereby pin Cassini? Not checked here — flag.

---

## 9. VERIFICATION & REVISIONS (2026-06-21) — verifier-before-record

Two independent agents were run concurrently: a BLIND ADVERSARIAL VERIFIER (saw this
doc; recomputed Ricci, Christoffels, box f, the BD map, the shift-algebra from
scratch — its Ricci code cross-chart-validated to 1e-12; agent `aa01430609f471615`)
and a BLIND INDEPENDENT RE-DERIVATION (did NOT read this doc; agent `af91bb6b7fdf512b6`).
**They converge: every symbolic claim was reproduced exactly; no fatal refutation.**
Verdict: **SUPPORTED-WITH-REVISIONS.** The revisions below are now part of the record.

**Confirmed as stated (bank):** kinetic weight e^{+2phi} (D1); a(phi)=e^{+phi} static
(D2); R inhomogeneous, obstruction at the angular 2/r^2 (D3 — the central finding);
R2->pure-exponential / R3->sources-+2 (D4/D5); Birkhoff broken, vacuum != GR, box f =
2phi''+4phi'/r robust to the power (Sec 5); BD map omega=-X/4, gamma=(X-4)/(X-8)
(Sec 6). The IBP boundary term does NOT dissolve Branch P (the e^{2phi} survivor is a
derivative-free potential IBP cannot remove — attack item 5 resolved).

**REVISIONS (elevated from footnote to load-bearing; add to the premise ledger):**
- **R1/D3 — name the orbit-area premise.** The angular obstruction is chart-ROBUST
  (verifier confirmed: S=int sqrt(-g) W R is coordinate-invariant and phi->phi+const
  is a chart-independent field-space map; recomputed in a phi-mixing chart, exact
  match) — BUT it rests on the shift acting **at fixed SO(3)-orbit area** (the areal
  radius is the invariant orbit-area label). That is physically the right choice (the
  invariant orbit-sphere area does not rescale under the depth shift while the (t,r)
  block does — that statement IS chart-independent), but it is a PREMISE, now named:
  **P7' — "the constant-depth shift acts at fixed invariant orbit-area" [CHOSE,
  physically justified].** The "angular sector is special" conclusion survives.
- **D2 — a(phi)=e^{+phi} is STATIC-ONLY (headline restriction).** For a moving
  worldline the three blocks scale e^{-2λ}/e^{+2λ}/1 and NO single a(phi) restores
  invariance (same anisotropy obstruction). The terrestrial cross-check PASSES and is
  banked: the observable m c^2 a(phi) dtau/dt = m c^2 e^{phi} e^{-phi} = m c^2 is
  **depth-independent** — a(phi)=e^{+phi} is exactly the NO-ANOMALY value, so a
  *function* e^{phi} does NOT conflict with the constant-a!=-1 terrestrial warning
  (it is the depth-flat choice). [[myopic-errors-dilation-exponent]] satisfied.
- **Sec 6 / X — add the GHOST constraint (attack item 8, now done).** No-ghost
  (Einstein-frame health, 2omega+3>0) requires X < O(1); Cassini requires |X|>1.7e5.
  These coexist ONLY at large **NEGATIVE** X: large positive X is a GHOST (forbidden),
  large negative X is HEALTHY and gives gamma->1 (gamma-1 ~ -2e-5 at X=-2e5, clears
  Cassini). So X is **not** a two-sided free family — it is **one-sided** (large
  negative), and a healthy Cassini-passing window DOES exist. Cassini is COMPATIBLE
  (not dead, not unconditionally undetermined): the theory is healthy + Cassini-safe
  for X large negative, and what remains open is what (if anything) FIXES X within
  that healthy window.

**DEEPENING from the independent re-derivation (new, beyond this doc):** the SAME
anisotropy that obstructs the angular curvature ALSO obstructs the **time-live
kinetic** sector — g^{tt} ~ e^{+2phi} and g^{rr} ~ e^{-2phi} carry OPPOSITE
shift-weight (the reciprocity g_tt g_rr = -c^2), so once d_t phi != 0 no single
uniform kinetic weight invariantizes both. The depth scale enters precisely via the
sectors that REFUSE the uniform weight — the **angular AND the time** sectors. The
phi-angular tension is thus a hard SYMMETRY obstruction in the action (not only in
the solutions), and it extends to phi-time. [[everything-on-solver-build]]'s
time-live carrier and [[frontier-time-live-native-matter]] connect here.
