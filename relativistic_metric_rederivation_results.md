# Relativistic Re-Derivation of the Bare UDT Metric Structure

**Mode:** careful DERIVE + cross-check (NOT exploration). Gated/foundation-securing,
authorized by Charles 2026-06-18. **Category-A, DATA-BLIND**: derive from stated
first principles only; import nothing; no mass/ratio/wall numbers used anywhere.

**Script:** `relrederiv_checks.py` (sympy, CPU). All symbolic claims below are
machine-verified by that script unless tagged ANALYTIC (functional-equation prose).

**Constructor:** Claude Opus 4.8 (1M), 2026-06-18. Verifier-before-record: an
ATTACK HERE block is provided; a blind adversarial pass is required before this
result is treated as banked.

---

## 0. The owner's postulates, verbatim (the ONLY postulates for this derivation)

> "Two properties follow directly from the SR and GR analogs: the dilation depends
> only on differences in phi, so no position is geometrically privileged; and
> dilations compose consistently across intermediate positions. Together these
> requirements uniquely determine the functional form of the metric -- it is
> derived, not assumed. A mutual symmetry condition -- each observer sees the
> other's clock run slow, with neither position preferred -- forces a structural
> identity between the metric components."

Labelled:
- **(R1)** dilation depends only on DIFFERENCES in phi (no privileged position /
  position-translation symmetry of the dilation).
- **(R2)** dilations COMPOSE consistently across intermediate positions
  (transitivity / one-parameter group).
- **(R3)** MUTUAL RECIPROCITY: each position sees the other's clock run slow,
  neither preferred.

These are treated as the complete and only premise set for the metric-STRUCTURE
derivation. UDT is an extension of GR that MUST remain relativistic; R1-R3 are the
relativistic-kinematic content that fixes the form before any field equation or
matter source is introduced.

---

## PART 1 — THE DIAGONAL RESULT

### 1a. Functional equation → unique exponential clock-rate law

**Setup (DERIVED from the metric, given the local-clock postulate of relativity).**
Proper time at a position is `dtau = sqrt(-g_tt) dt / c` (the GR/SR clock-rate
reading of the line element along a fixed worldline). Define the *clock-rate
function* of position-scalar phi:

```
f(phi) := sqrt( -g_tt(phi) / c^2 )      (assumed > 0; a real clock rate)
```

The dilation one observer at phi_A assigns to a clock at phi_B is the ratio
`D(phi_A, phi_B) = f(phi_B) / f(phi_A)`.

**Impose R1.** "Depends only on differences" means `D` is a function of
`phi_B - phi_A` alone: `D(phi_A,phi_B) = g(phi_B - phi_A)` for some single-variable
`g`. (This is exactly the statement that shifting all phi by a constant leaves every
physical dilation unchanged — the additive gauge freedom of phi; see 1c.)

**Impose R2.** Composition through any intermediate phi_C:
```
D(phi_A,phi_C) * D(phi_C,phi_B) = D(phi_A,phi_B)
=>  g(phi_C - phi_A) * g(phi_B - phi_C) = g(phi_B - phi_A).
```
Writing x = phi_C - phi_A, y = phi_B - phi_C (so x+y = phi_B - phi_A):
```
g(x) * g(y) = g(x + y)        (Cauchy/Abel exponential functional equation)
```

**Regularity premise (NAMED, not papered over):** `g` is continuous (equivalently:
monotone, or merely measurable/bounded-on-an-interval — any one of these standard
regularity conditions suffices) and `g > 0`. This is the one premise BEYOND R1-R2
needed for uniqueness; it is the relativistic requirement that the dilation vary
smoothly/monotonically with potential, not a physics choice of any value.

**Unique solution (ANALYTIC + machine-verified that exp solves it).** The positive
continuous solutions of the multiplicative Cauchy equation are exactly
`g(x) = exp(k x)` for a single real constant k. (Proof: set h = ln g; then
h(x)+h(y)=h(x+y) is additive Cauchy, whose continuous/monotone/measurable solutions
are h(x)=kx; hence g=exp(kx). Pathological non-measurable Hamel-basis solutions are
the ONLY alternatives and are excluded by the regularity premise.) Script confirms
`g(x)g(y) - g(x+y) = 0` and `g(0)=1` (composition forces the identity dilation).

Therefore `f(phi)^2 = -g_tt/c^2 = exp(2 k phi)`, i.e.
```
g_tt = - exp(2 k phi) c^2.
```

**Pin the convention constant k.** UDT *defines* phi by
`phi := -(1/2) ln(-g_tt/c^2)`. Substituting the derived form:
```
phi = -(1/2) ln( exp(2 k phi) ) = -k phi   =>   k = -1.
```
Script solves this and returns `k = -1`. So
```
g_tt = - exp(-2 phi) c^2.                          [DIAGONAL TIME RESULT]
```

**DERIVED vs CONVENTION (1a):**
- DERIVED: the *exponential functional form* `-g_tt/c^2 = exp(2k phi)` (forced by
  R1+R2 + regularity).
- CONVENTION: k = -1 — fixed by the chosen *definition* of phi (sign/normalization
  of the potential). It carries no physical content; any other nonzero k is the same
  physics with phi rescaled. (The MAGNITUDE |k|=1 is also convention: it is absorbed
  into the units/normalization of phi by that same definition.)
- ASSUMED (regularity): `g` continuous/monotone and positive.

### 1b. Reciprocity R3 → structural identity g_tt g_rr = -c^2

**Setup.** The radial proper-length element is `dL = sqrt(g_rr) dr`. Define the
length/ruler dilation factor `h(phi) := sqrt(g_rr(phi))`.

**The SR/GR reciprocity property invoked (named, ANALOG not import).** In SR the
Lorentz boost relating two inertial frames satisfies *mutual reciprocity*: each
frame sees the other's clock dilated by gamma and the other's ruler contracted by
1/gamma, with neither frame preferred — the time-dilation factor and the
length factor are exact reciprocals (the boost is its own inverse up to sign of
velocity; gamma_time x (1/gamma)_length = 1). R3 is the positional-dilation ANALOG
of precisely this property: the time-rate factor a position assigns and the
length factor are reciprocal, with neither position preferred.

**Impose R3.** "Each sees the other's clock run slow, neither preferred" =
the time and length dilation factors are mutual reciprocals at every phi:
```
f(phi) * h(phi) = 1      for all phi
=>  sqrt(-g_tt/c^2) * sqrt(g_rr) = 1
=>  (-g_tt/c^2) * g_rr = 1
=>  g_tt * g_rr = -c^2.                              [STRUCTURAL IDENTITY]
```
With g_tt = -exp(-2 phi) c^2 this gives
```
g_rr = -c^2 / g_tt = exp(2 phi) = e^{-2k phi}.       [DIAGONAL RADIAL RESULT]
```
Script confirms `g_tt g_rr = -c^2` and `sqrt(-g_tt/c^2) sqrt(g_rr) = 1` exactly.

**DERIVED vs ASSUMED (1b):**
- DERIVED: `g_tt g_rr = -c^2` (i.e. B = 1/A) — forced by R3 reciprocity, given the
  1a exponential form. **No matter source, no action, no field equation used.**
- ASSUMED (analog premise, NAMED): that R3 is the faithful positional analog of SR
  boost reciprocity — i.e. that the relevant length factor is `sqrt(g_rr)` and that
  the mutual-inverse pairing is between g_tt and g_rr. This is an analog *choice of
  what reciprocity means*, owner-stated, not an import of an SR result.

### 1c. Assembled bare diagonal form + gauge check

```
g_tt = - e^{-2 phi} c^2 ,   g_rr = e^{+2 phi} ,   g_tt g_rr = -c^2.
```
- No matter source assumed; no action extremized; no field equation used. Pure
  relativistic kinematics (R1+R2+R3) + the phi-definition convention.
- **phi is physical only up to an additive constant** (only DIFFERENCES matter):
  the entire construction entered through `g(phi_B - phi_A)`, so phi -> phi + const
  leaves every dilation `D` invariant. **R1 IS this gauge freedom**, verified: the
  derivation never used an absolute phi, only differences. (Consequence: there is no
  preferred zero of phi and no preferred position — exactly R1.)

---

## PART 2 — BEYOND THE DIAGONAL SLICE (what relativity forces vs leaves free)

This is the real re-establishment value. The corpus chain (S58-009, sec 1.0)
SMUGGLES static spherical symmetry at step 1 ("GR + static spherical symmetry ->
two-function ansatz"). We ask what R1+R2+R3 *actually* force starting from a
GENERAL metric, with no symmetry assumed.

### 2a. What R1+R2+R3 force on a general g_{mu nu}(t,r,theta,psi)

Start from a fully general metric (10 independent components, no Killing vectors,
no diagonality). R1-R3 are statements about a *scalar* phi and the *clock-rate* and
*reciprocal length* dilations. Carefully, they constrain ONLY the following, and
leave the rest free:

1. **R1+R2 fix the FUNCTIONAL DEPENDENCE of the proper-time rate on phi, not which
   coordinate carries it.** They force `sqrt(-g_tt)` (the local clock rate along the
   chosen time direction) to be `c exp(k phi)` *as a function of phi*. They say
   NOTHING about r-, theta-, psi-dependence except through phi(x). They do NOT force
   g_tt to be static (phi may depend on t), NOR spherical (phi may depend on
   theta,psi). They constrain the **t-t block's magnitude-vs-phi law**, full stop.

2. **R3 reciprocity ties the time dilation to ONE conjugate length dilation — the
   one along the direction in which phi varies (the gradient direction).** The
   physical content of "each sees the other's clock slow, neither preferred" is a
   statement about the line connecting two positions of different phi, i.e. the
   *gradient direction* of phi. So R3 forces the reciprocal tie between g_tt and the
   metric component ALONG grad(phi). In the spherical slice grad(phi) = phi'(r) r-hat,
   so the tie is g_tt <-> g_rr. **In general, R3 ties g_tt to g_{nn}, n = grad(phi)/|grad phi|** — it does NOT, by itself, tie the
   angular (transverse-to-gradient) components or the off-diagonal components.

3. **What is therefore LEFT FREE by R1+R2+R3 alone:**
   - the transverse (angular) block — any 2-metric on surfaces of constant phi
     (e.g. r^2 dOmega^2 is a CHOICE, not forced; an ellipsoidal or sheared
     transverse metric is equally allowed by R1-R3);
   - the shift/off-diagonal components g_{ti}, g_{ij} (i,j != gradient direction) —
     rotation/frame-dragging-type terms are NOT excluded by R1-R3;
   - the t-dependence of phi (NON-STATIONARY phi is allowed: R1-R3 are
     instantaneous/local kinematic statements, silent on d/dt);
   - the radial gauge / areal-vs-isotropic chart choice;
   - the global topology / domain (finite-cell vs infinite is not addressed here).

**KEY FINDING (Part 2a):** R1+R2+R3 are NOT equivalent to "static + spherical +
diagonal." They force exactly two things and no more:
   (i) the **exponential clock-rate law** `g_tt = -e^{2k phi} c^2` as a function of phi;
   (ii) the **reciprocal tie** `g_tt g_{nn} = -c^2` along the gradient of phi.
Everything else — angular structure, off-diagonal terms, time dependence, chart,
topology — is FREE and was, in the old chain, fixed by an UNSTATED symmetry choice
(static spherical symmetry), not by relativity.

This is exactly the "whole before slice" tripwire: the diagonal static spherical
result is the gradient-aligned, transverse-isotropic, stationary *corner* of the
relativity-forced structure, not its entirety.

### 2b. The BARE metric structure (locked vs free)

Adopt coordinates with the "1" direction along grad(phi) (always possible locally).
What relativity (R1-R3) LOCKS:

```
g_tt    = - e^{2k phi(x)} c^2            (k = -1 by convention)  [LOCKED, exponential law]
g_{tt} * g_{(grad)(grad)} = -c^2          (reciprocal tie along grad phi) [LOCKED]
```

What remains FREE (the solution space for the NEXT stage — Einstein eqs + finite-cell/seal):
```
- the 2-metric on constant-phi surfaces (the angular/transverse block), incl. its
  area element r^2 dOmega^2 if one CHOOSES spherical;
- all off-diagonal/shift components g_{0i}, g_{ij} not along grad phi
  (frame-dragging / rotation / shear);
- the t-dependence of phi (stationary vs non-stationary);
- the chart (areal vs isotropic radial gauge);
- the global domain/topology.
```

When one *additionally* CHOOSES static + spherical + diagonal + areal-r (four
choices, none forced by R1-R3), the locked content collapses to the familiar
```
ds^2 = - e^{-2 phi(r)} c^2 dt^2 + e^{+2 phi(r)} dr^2 + r^2 dOmega^2.
```
That `r^2 dOmega^2` and the staticity are the SMUGGLED content; only the
`e^{-2phi}`/`e^{+2phi}` pair and their product `-c^2` are relativity-forced.

---

## PART 3 — CROSS-CHECK + SMUGGLE-AUDIT against the corpus

### 3a. Reproduces the canonical form

Script PART 3a confirms, for `A=e^{-2phi(r)}, B=e^{+2phi(r)}`:
- `A*B = 1` identically ⇒ `(AB)' = 0` identically;
- the full 4D Einstein-tensor computation gives `G^t_t - G^r_r = 0` for the locked
  form WITHOUT any matter assumption;
- `g_tt g_rr = -c^2` and the diagonal form
  `ds^2 = -e^{-2phi}c^2 dt^2 + e^{+2phi}dr^2 + r^2 dOmega^2`
  are exactly the canonical UDT metric (matches sec 1.0 step 4 and CANON
  C-2026-06-10-1 areal reading). ✔ Reproduced.

### 3b. Is B = 1/A genuinely source-free / kinematic? — YES.

**This is the headline.** In our derivation, `g_tt g_rr = -c^2` (B=1/A) drops out of
**R3 reciprocity alone** (Part 1b): no stress tensor, no `T^t_t = T^r_r`, no
asymptotic flatness, no field equation. The Einstein-tensor identity
`G^t_t - G^r_r = -(AB)'/(rAB^2)` is then a CONSISTENCY check, not the origin: with
AB=1 already forced by R3, `(AB)'=0` is automatic and `G^t_t = G^r_r` follows for
free (script confirms G^t_t - G^r_r = 0 identically). So:

> **B=1/A is relativistic-kinematic (R3), upstream of all dynamics. The
> matter-source derivation C-2026-06-14-1 (angular sector gives T^t_t=T^r_r) is
> DOWNSTREAM and is a CONSISTENCY requirement, not the cause:** matter must RESPECT
> the relativistically-forced tie (its stress must satisfy T^t_t=T^r_r so the
> Einstein equations don't contradict the kinematically-fixed AB=1), it does not
> CREATE the tie. C-2026-06-14-1's value is that the angular sector is *compatible*
> with — and dynamically sustains — the kinematic tie inside matter; the refinement
> (radial-twist EOS softening, p_r+rho>0) is then the statement that a realized
> interior departs from the *idealized* reciprocal slice, which is consistent
> because once phi varies in a sourced interior the simple two-position reciprocity
> picture is the exterior/idealized limit (see Part 2: the tie is exact along
> grad phi for a clean potential; a twisting body adds transverse structure).

### Smuggle-audit: assumptions the old chain (sec 1.0) made

| Old-chain assumption (S58-009 sec 1.0) | This derivation |
|---|---|
| Step 1: **static spherical symmetry** (two-function SSS ansatz) | **DROPPED.** Not forced by R1-R3; it is 4 independent CHOICES (static, spherical, diagonal, areal-r). Relativity forces only the exponential law + the gradient-direction reciprocal tie (Part 2). |
| Step 2: positional-dilation as a POSTULATE giving A=e^{-2phi} | **DERIVED** here from R1+R2 (Cauchy FE) + the phi-definition convention. Demoted from postulate to consequence. |
| Step 3: `(AB)'=0` from **matter T^t_t=T^r_r (or vacuum) + asymptotic flatness** | **DROPPED as the ORIGIN.** B=1/A comes from R3 reciprocity (kinematic), upstream of any T and of asymptotic flatness. The Einstein identity becomes a downstream consistency check (auto-satisfied). Asymptotic flatness NOT needed for the tie (it is only needed later to pick the Schwarzschild *vacuum solution*, step 5 — a separate question about phi(r), not about the form). |
| Step 5: Schwarzschild vacuum limit via asymptotic flatness | Untouched/orthogonal: this is solving `G^theta_theta=0` for phi(r) (the FREE content of Part 2b), not part of forcing the bare form. |

**What we DERIVE that the old chain assumed:** the metric FORM (exponential +
reciprocal tie) from pure relativity, and B=1/A as kinematic.
**What we can DROP:** static sphericity as a *prerequisite for the form*; the
T^t_t=T^r_r matter constraint and asymptotic flatness as the *cause* of B=1/A.
**What we must still NAME as a premise:** the regularity of g (1a), and the analog
identification of R3 with SR boost reciprocity (1b).

---

## PREMISE LEDGER (chose vs derived)

| # | Item | Status | Note |
|---|---|---|---|
| P1 | Proper time `dtau = sqrt(-g_tt) dt/c` | DERIVED (GR/SR line-element reading) | standard relativistic clock postulate |
| P2 | Dilation depends only on phi-differences (R1) | OWNER POSTULATE | = additive gauge freedom of phi |
| P3 | Dilations compose (R2) | OWNER POSTULATE | one-parameter group / transitivity |
| P4 | g continuous/monotone & >0 (regularity) | **ASSUMED (named)** | the one extra premise for FE uniqueness; excludes non-measurable Hamel solutions |
| P5 | Exponential form `-g_tt/c^2 = e^{2k phi}` | DERIVED | from P2+P3+P4 (Cauchy FE) |
| P6 | k = -1 | **CONVENTION** | from definition `phi := -(1/2)ln(-g_tt/c^2)`; no physics |
| P7 | Mutual reciprocity (R3) | OWNER POSTULATE | SR/GR boost-reciprocity ANALOG (not import) |
| P8 | Reciprocity acts as `f·h = 1` with h=sqrt(g_rr) | **ASSUMED (named)** | the analog identification: which length factor pairs with the clock factor |
| P9 | `g_tt g_rr = -c^2` (B=1/A) | DERIVED | from P5+P7+P8; KINEMATIC, source-free |
| P10 | Static / spherical / diagonal / areal-r | **CHOICE (not forced)** | the four smuggled choices; collapse the locked structure to the familiar diagonal form |
| P11 | matter T^t_t=T^r_r; asymptotic flatness | DOWNSTREAM consistency, not used to force the form |

Nothing imported. No data, no mass/ratio/wall numbers used.

---

## REGIME / SCOPE STAMP

- **Scope:** the BARE METRIC FORM only — what relativistic kinematics (R1-R3) lock
  vs leave free, BEFORE any field equation, matter source, action, BC, chart, or
  topology is chosen.
- **Holds:** for any metric admitting a scalar phi with a clock-rate and a
  gradient-aligned reciprocal length dilation. Locks (i) exponential clock law,
  (ii) reciprocal tie along grad phi. Silent on (free) angular block, off-diagonal/
  shift terms, time-dependence of phi, chart, topology.
- **Does NOT determine:** phi(x) itself (needs Einstein eqs / the FREE content), the
  angular structure, non-stationary content, the finite-cell/seal closure. Those are
  the next stage's solution space (Part 2b).
- **Premises that, if revised, void this:** P4 (regularity) and P8 (the R3 analog
  identification). If R3 is read differently (e.g. tying g_tt to a transverse rather
  than gradient component), the tie changes — flag in NEGATIVES_REGISTRY if revisited.

---

## ATTACK HERE (for the blind adversarial verifier)

1. **FE uniqueness:** Is the jump from `g(x)g(y)=g(x+y)` to `g=exp(kx)` airtight
   GIVEN P4? Confirm the only escape is dropping regularity (non-measurable
   solutions). Check g>0 is actually used (it is: to take log).
2. **k=-1 is convention, not physics:** verify that any nonzero k gives identical
   physics under phi-rescaling, and that the value -1 follows ONLY from the stated
   definition of phi. Try to find a hidden physical input.
3. **R3 → B=1/A (the headline):** Is `f·h=1` the *only* faithful reading of "each
   sees the other's clock slow, neither preferred"? Could R3 instead give
   `g_tt = g_rr` (same-sign) or a different pairing? Attack P8 hardest — this is
   where a smuggled choice would hide. Does the SR-boost-reciprocity analogy
   genuinely yield reciprocal (inverse), not equal, factors?
4. **Part 2 (the real claim):** Is it TRUE that R1-R3 leave the angular block and
   off-diagonal terms free? Try to derive a constraint on g_{theta theta} or g_{tphi}
   from R1-R3 alone. If you can, Part 2's "what's free" is wrong. Conversely confirm
   the old chain's spherical symmetry is genuinely an independent assumption.
5. **Source-free claim (3b):** Verify NO step in 1a/1b used a stress tensor, action,
   or Einstein equation. Confirm `(AB)'=0` and `G^t_t-G^r_r=0` are CONSEQUENCES of
   the already-forced AB=1, not its source. Check the script's Einstein computation
   independently (recompute G^t_t-G^r_r).
6. **Stationarity:** confirm R1-R3 do not force d(phi)/dt = 0 (non-stationary phi
   allowed) — important for the closed-time frontier.
7. **Data-blind / import check:** confirm no mass, ratio, or wall number, and no
   SM/GR result, was imported as a *value*. (GR is used only for the line-element
   clock reading and as the downstream field equation, both relativistic structure,
   not imported numbers.)

---

## THE SINGLE CLEANEST STATEMENT

> Given relativity's local clock reading `dtau ∝ sqrt(-g_tt) dt`, three kinematic
> requirements — that positional dilation depend only on phi-DIFFERENCES (R1),
> COMPOSE across intermediate positions (R2), and be MUTUALLY RECIPROCAL with no
> position preferred (R3) — together with the single regularity premise that the
> dilation vary continuously, FORCE the metric's two radial dials to take the
> exponential reciprocal form `g_tt = -e^{-2phi}c^2`, `g_rr = e^{+2phi}`, with
> `g_tt g_rr = -c^2`. The exponential is the unique solution of the composition
> (Cauchy) equation; the reciprocal tie B=1/A is the unique consequence of
> mutual reciprocity. Both are **derived from relativity, not assumed, and both are
> source-free kinematics** — upstream of any matter, action, or field equation.
> Static spherical diagonality is an ADDED choice, not part of the derivation.

---

## BLIND VERIFIER VERDICT — 2026-06-18 (verifier agent ad75fef845c31a128)

**STANDS-CONDITIONALLY** on the premises the doc already names (P4 regularity; P8/P7 the
reciprocity slot-identification). Independent re-derivation from R1+R2+R3 in sympy; no
circular or silently-smuggled step found. Axis-by-axis:

- A (exponential uniqueness) CONFIRMS — and STRENGTHENS: R1 + mere differentiability ALONE
  forces (log f)'=const => f=exp(kphi); R2 is then automatic (so R1,R2 not strictly
  independent — harmless over-count). P4 (continuity/monotonicity/measurability — any one) is
  PHYSICALLY MANDATORY for a clock rate, NOT a smuggled convenience. Exponential is unique.
- B (reciprocity -> B=1/A) STANDS-CONDITIONALLY — the one genuine load. "Each sees the other's
  clock slow, neither preferred" does NOT by itself force B=1/A: the "equal-time-factors"
  reading gives g_tt g_rr = -c^2 e^{-4phi} (NOT constant, no clean tie); the "time x length
  inverse" reading gives B=1/A. The inverse-vs-equal choice is ESSENTIALLY FORCED once exp law
  + the phi->-phi "swap the two positions = neither preferred" symmetry is accepted (e^{-x}=1/e^{x}).
  But the SLOT identification — that the conjugate-to-time direction is the radial / phi-GRADIENT
  direction (not a transverse one) — is an IRREDUCIBLE ANALOG CHOICE (P8). So B=1/A is forced by
  R3-as-read-by-P7/P8, not by relativity in the abstract. NO circularity (P8 assumes the pairing,
  from which B=1/A follows — it does not assume B=1/A). The doc's LEDGER is honest (P8 tagged
  ASSUMED, scope void-if-revised); only the HEADLINE PROSE overstates — read "R3 forces B=1/A" as
  "R1+R2+R3-as-read-by-P7/P8 forces B=1/A". [Prose-calibration note, not a defect in the result.]
- C (forced-vs-free, the prize) CONFIRMS exactly: no under-claim (R1 is silent on transverse
  geometry — no isotropy/g_thth constraint follows) and no over-claim (reciprocity transverse to
  grad phi is VACUOUS — along constant-phi the difference is 0, dilation = identity, tie = 1).
  So angular block, off-diagonals/shift, time-dependence (non-stationary phi allowed), chart, and
  topology are GENUINELY FREE. Static + spherical + diagonal + areal-r = four independent CHOICES,
  not consequences. (The old chain smuggled all four.)
- D (source-free) CONFIRMS: independent Christoffel/Ricci/Einstein for general A(r),B(r) gives
  G^t_t - G^r_r = -(AB)'/(rAB^2), = 0 for B=1/A at ARBITRARY A, no stress tensor/action/field
  equation/asymptotic-flatness used. So B=1/A is the INPUT (kinematic, from R3) and G^t_t=G^r_r is
  the DOWNSTREAM consequence. C-2026-06-14-1 (angular-source -> T^t_t=T^r_r) is genuinely DOWNSTREAM
  consistency, not the cause of the tie.
- E (convention) CONFIRMS: any nonzero k is identical physics; k=-1 follows ONLY from the
  definition phi:=-(1/2)ln(-g_tt/c^2). phi->phi+const leaves all dilations invariant, and R1 IS
  that gauge freedom.
- F (relativity preserved) CONFIRMS: Lorentzian signature for all real phi, finite local light
  speed, regular Minkowski tangent space — local Lorentz invariance intact. UDT stays relativistic.

NET (bankable, foundation): UDT's bare metric structure is DERIVED from "remain relativistic":
(1) the exponential dilation law g_tt=-e^{-2phi}c^2 (R1, essentially clean); (2) the reciprocal
tie g_tt g_rr=-c^2 / B=1/A, SOURCE-FREE/kinematic, from reciprocity along the phi-GRADIENT
direction — modulo the one natural slot-identification P8 (the dilation-gradient direction is the
one paired with time). Everything else — angular shape, off-diagonals, time-dependence, chart,
topology — is FREE (the solution-space DOF); sphericity/staticness/diagonality/areal-r are CHOICES.
B=1/A is relativistic-UPSTREAM of the matter-source canon C-2026-06-14-1. Verifier files:
verify_relrederiv_independent.py, verify_relrederiv_reciprocity_deep.py. CANONIZATION = Charles's call.
