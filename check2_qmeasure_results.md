# CHECK 2 — Q-MEASURE: What natural measure does UDT geometry put on configuration space, and where does the Born square sit against it?

**Mode:** OBSERVE (binding CLAUDE.md discipline). Question type: **METRIC-LED** —
"what measure does the derived UDT spatial metric induce on the localized
object's position, and how does standard curved-space continuity bookkeeping
place |psi|^2 against it?" NOT verdict-hunting; "Born survives" is not a target.
Absences/ill-posedness reported as first-class results.

**Date:** 2026-06-17. **Agent:** OBSERVE agent (Check-2 / Q-MEASURE).
**Files read (read-only):** CANON.md (C-2026-06-13-1 metric class; C-2026-06-10-1
R-areal; C-2026-06-10-2 finite-cell), STATE.md (lines 195-225: angular measure
`r^2 sin th BARE`, wave speeds c_r^2=e^{-4phi}, c_th^2=e^{-2phi}/r^2),
measure_fork_results.md (self-adjoint angular measure bare).

---

## 0. THE METRIC (derived anchor — not chosen here)

From CANON C-2026-06-13-1 (diagonal dilation-tie class), R-areal (rho=r a
theorem, C-2026-06-10-1), and the BARE 2-sphere (STATE.md:205, measure_fork):

    ds^2 = -e^{-2phi(r)} dt^2  +  e^{2phi(r)} dr^2  +  r^2 (dtheta^2 + sin^2 theta dphi_ang^2)

with c_eff = e^{-2phi}, g_tt g_rr = -1 (B=1/A). The dilation factor lives ONLY
in g_rr (radial). **The angular 2-sphere is bare r^2** — this is a derived
feature (the self-adjoint angular measure is r^2 sin th with no e^{2phi}
dressing; the e^{-2phi} sits in the stiffness, STATE.md:204-205), NOT a choice.
This single fact is what makes Part A's answer e^{phi}, not e^{3phi}.

---

## PART A — THE NATIVE SPATIAL MEASURE

Constant-t slice, induced 3-metric:

    g_spatial = diag( e^{2phi},  r^2,  r^2 sin^2 theta )
    det g_spatial = r^4 e^{2phi} sin^2 theta
    **sqrt(g_spatial) = e^{phi} * r^2 sin theta**            (exact, sympy-verified)

The proper-volume element is

    dV_proper = sqrt(g_spatial) d^3x = e^{phi} * (r^2 sin theta dr dtheta dphi_ang).

Separate the flat-space spherical Jacobian (r^2 sin theta) from the genuine
DILATION weight:

    **dilation weight  W(r) = e^{phi(r)}   (power +1 in phi).**

Stretch/compression vs coordinate volume:
- The radial direction is the ONLY stretched direction: proper radial length
  d(ell) = e^{phi} dr. The two angular directions are unstretched (bare r^2).
- So proper volume is stretched by exactly **e^{phi}** per coordinate volume,
  NOT e^{3phi}. A naive "all three directions dilate" guess (e^{3phi}) is WRONG
  here because the metric only dilates the radial leg.

Depth behavior (matter cell, phi < 0, inside-out, phi0 ~ -0.8 hadronic):
- phi -> 0 (lab / cell interface):  W = e^{phi} -> 1  (measure -> flat).
- phi0 = -0.8 (hadronic depth):     W = e^{-0.8} = **0.449** — proper volume is
  COMPRESSED to ~45% of coordinate volume deep in the well (matter cell digs
  DOWN in phi). [If one instead reads the universe/positive-phi half, W=e^{+phi}
  > 1, volume expanded; the matter object lives in the negative-phi half.]
- phi -> -inf (core endpoint / seal):  W = e^{phi} -> 0. The measure DEGENERATES
  to zero at the seal — flagged below as the load-bearing subtlety for typicality.

**This is the candidate natural measure:** d(mu) = e^{phi(r)} r^2 sin theta d^3x.

---

## PART B — WHERE THE BORN SQUARE SITS (exact curved-space continuity)

Standard curved-space probability conservation for a one-body density of the
collective coordinate X on the cell. The covariant continuity equation is

    d_t( sqrt(g) rho )  +  d_i( sqrt(g) rho v^i ) = 0,                 (*)

so the EQUIVARIANT (locally conserved, coordinate-integrable) object is the
COORDINATE density  N(X) := sqrt(g) rho ,  with  Integral N d^3x = 1 over the
cell. Here:

- rho == rho_proper is the PROPER (scalar) density: probability per unit PROPER
  volume,  dP = rho_proper dV_proper = rho_proper sqrt(g) d^3x.
- N = sqrt(g) rho_proper is the COORDINATE density: probability per unit
  COORDINATE volume,  dP = N d^3x.

These are exactly related by the dilation weight:

    **N(X) = sqrt(g) rho_proper(X) = e^{phi} r^2 sin theta * rho_proper(X).**
    (Dropping the universal flat Jacobian r^2 sin theta that QM shares,
     the load-bearing relation is  N_dil = e^{phi} rho_proper.)

Now place |psi|^2. The guiding-wave amplitude squared |psi|^2 is, in the
de Broglie–Bohm/pilot-wave construction, the density that the guidance flow
makes equivariant under (*) — i.e. |psi|^2 is whatever DENSITY is preserved by
the continuity equation written in the SAME variables psi obeys. UDT has not
yet fixed (Check-1) which variable the guiding equation is written in, so there
are two clean, mutually exclusive readings, and the bookkeeping forces the
sqrt(g) onto the OTHER one:

  Reading (B1) — psi a coordinate-scalar (flat-Born):
     |psi|^2 == N  (coordinate density). Then the PROPER density carries the
     INVERSE weight:  rho_proper = e^{-phi} |psi|^2 / (r^2 sin theta).
     Equilibrium "typical" coordinate distribution of X is exactly |psi|^2 d^3x.

  Reading (B2) — psi a proper/curved scalar (metric-Born):
     |psi|^2 == rho_proper (proper density). Then the COORDINATE (conserved)
     density carries the weight:  N = e^{phi} r^2 sin theta |psi|^2, and the
     typical coordinate distribution of X is e^{phi} |psi|^2 d^3x.

Exact summary relation (weight is e^{phi}, the Part-A measure):

    N(coordinate dens.) = e^{phi} (r^2 sin th) * rho_proper(proper dens.),
    and |psi|^2 is one of {N, rho_proper}; the sqrt(g)=e^{phi} weight always
    lands on whichever of those two is NOT identified with |psi|^2.

So the Born square does NOT live "against d^3x" or "against sqrt(g) d^3x"
unconditionally — it lives against whichever measure the GUIDANCE FLOW (Check-1)
makes equivariant. The bookkeeping is exact and unambiguous; the remaining
freedom is the scalar character of psi, which is a Check-1 input, not a
Check-2 result.

---

## PART C — IS THE WEIGHT OBSERVABLE OR ABSORBED?

A position measurement detects the object inside a coordinate region Omega and
reports a probability. The OBSERVED statistic is

    P(Omega) = Integral_Omega N(X) d^3x = Integral_Omega sqrt(g) rho_proper d^3x.

Key point: **P(Omega) is always the integral of the coordinate density N over
coordinate volume — there is no separate "proper-volume sampling" the detector
performs.** A detector occupies a coordinate region (a chart patch of the cell);
its count rate samples the conserved coordinate density N. Therefore:

- In reading (B1) (|psi|^2 = N): the detector measures Integral_Omega |psi|^2
  d^3x **exactly** — the e^{phi} weight is ABSORBED (it never appears; |psi|^2
  IS the coordinate density). Observed statistics are EXACTLY flat-Born,
  weight unobservable. Branch (i): cancellation/absorption.

- In reading (B2) (|psi|^2 = rho_proper): the detector measures
  Integral_Omega e^{phi} |psi|^2 (r^2 sin th) d^3x — the e^{phi} weight does
  NOT cancel. Observed statistics carry a depth-dependent **native deviation**:

      P_observed(Omega) = Integral_Omega e^{phi(r)} |psi|^2 d(coord vol)
                          ----------------------------------------------
                          Integral_cell e^{phi(r)} |psi|^2 d(coord vol)

  vs the flat-Born prediction Integral |psi|^2. The residual DEVIATION FACTOR
  multiplying |psi|^2 is

      **D(r) = e^{phi(r)}**   (relative to flat Born; normalized over the cell).

  Depth estimate of the deviation:
    - lab / interface, phi -> 0:   D = 1.000  (no deviation; Born exact).
    - hadronic depth phi0 = -0.8:  D = e^{-0.8} = **0.449** — a ~55% relative
      SUPPRESSION of detection probability per |psi|^2 at the bottom of the
      hadronic well relative to shallow regions. (For comparison the dilation
      observable e^{-2phi} ~ 4.95 there, i.e. the well is "deep" by the codex's
      own ~5x linearization-breaking measure; the Born deviation e^{phi} is the
      square-root-and-sign-flipped partner, ~0.45.)
    - core / seal, phi -> -inf:    D -> 0 (measure degenerates; see Part D-c).

**Which branch is physically true is NOT decidable inside Check-2.** It is fixed
by the SCALAR CHARACTER of the guiding wave psi (Check-1: is psi a coordinate
scalar or a curved/proper scalar under the UDT guidance equation?). Check-2's
honest output is: the geometry SUPPLIES a non-trivial weight e^{phi} that is
EITHER absorbed (B1) OR shows up as a falsifiable e^{phi} Born deviation (B2),
and the discriminator is a single Check-1 fact.

---

## PART D — HONEST VERDICT

The result is **conditional, with the condition sharply named** — not (a), not
(b) unconditionally, and partially (c) at the seal:

- It is **branch (a) FLAT-BORN if and only if** the UDT guidance flow makes the
  COORDINATE density equivariant (psi a coordinate scalar, |psi|^2 = N). Then
  the e^{phi} weight is absorbed and Born survives unmodified — a consistency
  result. This is the reading most consonant with the detector-samples-
  coordinate-volume fact in Part C.

- It is **branch (b) METRIC-CORRECTED if and only if** the guidance flow makes
  the PROPER density equivariant (psi a proper scalar, |psi|^2 = rho_proper).
  Then the native, falsifiable deviation is the explicit factor **D(r)=e^{phi(r)}**,
  depth-scaling as e^{phi} (suppression in the negative-phi matter well; ~0.45
  at hadronic phi0 = -0.8, -> 1 at the lab). This is a clean, single-power,
  derived prediction if (b) holds.

- There IS a genuine **branch-(c) ILL-POSEDNESS at the seal**: sqrt(g)=e^{phi}
  -> 0 as phi -> -inf at the core endpoint, so the natural measure DEGENERATES
  (vanishes) at the seal boundary of the matter cell. The total mass
  Integral_cell e^{phi} |psi|^2 d^3x is finite (the weight is bounded by 1 and
  vanishes at the core), so normalization is fine, but the measure is NOT
  uniform and pinches to zero at the seal — relevant for typicality below.

**Net:** the geometry does NOT leave the measure flat (Part A: a real e^{phi}
weight exists), and it does NOT spoil normalization, so this is not a trivial
"Born is automatic" nor a "setup is broken." It is a **clean fork whose selector
is a single Check-1 fact (the scalar character of the guiding wave)** — flat-Born
under coordinate-scalar guidance, a depth-scaling e^{phi} Born deviation under
proper-scalar guidance.

---

## TYPICALITY HALF (status, conditional on Check-1)

The finite closed cell (CANON C-2026-06-10-2: no spatial infinity, finite
mirrored domains, definite total measure) is FAVORABLE for making the typicality
argument rigorous: a definite finite total measure Integral_cell sqrt(g) d^3x
exists and is finite, so "typical relative to the natural measure" is well-defined
in principle — none of the usual non-compact/infinite-volume obstructions to
defining typicality apply. **Two visible obstructions remain, both honest:**
(1) the measure is NON-UNIQUE until Check-1 selects which density (N vs
rho_proper) the guidance flow preserves — the equilibrium/typical measure IS the
equivariant density, which Check-2 cannot fix alone; (2) the seal degeneration
(Part D-c: sqrt(g) -> 0 at the core) means the natural measure is non-uniform and
pinches at the seal boundary, so the typicality measure weights the seal region
to zero — whether that is benign (object simply unlikely to sit at the core) or a
boundary-condition pathology depends on the seal BC, which is also Check-1/
Check-3 structure. **Honest status:** the finite cell removes the infinity
obstruction to typicality (a real plus), but typicality rigor is CONDITIONAL on
(i) Check-1 fixing the equivariant density and (ii) the seal BC being benign. No
overclaim: Check-2 alone does not establish typicality.

---

## PREMISE LEDGER (chose / derived)

| # | Premise | chose / derived | note |
|---|---------|-----------------|------|
| 1 | ds^2 = -e^{-2phi}dt^2 + e^{2phi}dr^2 + r^2 dOmega^2 | **derived** | CANON C-2026-06-13-1 + R-areal C-2026-06-10-1 |
| 2 | 2-sphere is BARE r^2 (no e^{2phi} angular dressing) | **derived** | STATE.md:205, measure_fork_results.md (self-adjoint angular measure r^2 sin th bare) |
| 3 | sqrt(g_spatial) = e^{phi} r^2 sin theta; dilation weight e^{phi} (power +1) | **derived** | sympy det of premise 1; follows directly from 1+2 |
| 4 | Curved continuity d_t(sqrt(g) rho)+d_i(sqrt(g) rho v^i)=0; equivariant object = sqrt(g) rho | **derived** (standard covariant continuity) | not UDT-specific; standard curved-space QM bookkeeping, applied exactly |
| 5 | |psi|^2 equals EITHER N (coord dens) OR rho_proper (proper dens) | **chose (enumerated both)** | the actual selector is the scalar character of psi = Check-1 input; not fixed in Check-2 |
| 6 | Detector samples the COORDINATE density N over a coordinate region | **chose (physical modeling)** | a detector occupies a chart region; this is the standard reading but is a modeling premise, flagged |
| 7 | Matter object lives at phi<0 (inside-out cell, hadronic phi0~-0.8) | **derived** | CANON C-2026-06-10-2 + STATE.md:210-211 regime correction |
| 8 | Finite cell -> finite total measure (typicality well-posed in principle) | **derived** | CANON C-2026-06-10-2 |
| 9 | sqrt(g)->0 at seal (phi->-inf) — measure degenerates at core | **derived** | premise 3 at phi->-inf |

---

## CONFIDENCE

- Part A (sqrt(g)=e^{phi} r^2 sin th; weight e^{phi}, NOT e^{3phi}): **HIGH** —
  direct exact computation from the derived, canonized metric; the e^{phi}
  (radial-only dilation) vs e^{3phi} (naive) distinction is the key emergent fact
  and rests on the derived bare-2-sphere premise (#2).
- Part B (exact relation N = e^{phi} r^2 sin th rho_proper; |psi|^2 is one of the
  two): **HIGH** on the bookkeeping; the which-one is openly deferred to Check-1.
- Part C (deviation factor D=e^{phi}; 0.449 at hadronic depth): **HIGH**
  arithmetic, **MEDIUM** physical force — entirely conditional on premises 5+6.
- Part D verdict (conditional fork, selector = psi scalar character; genuine seal
  degeneration): **HIGH** as a conditional statement; deliberately NOT a single
  branch, because the math gives a fork, not a verdict.

## SINGLE MOST LOAD-BEARING PREMISE (flag for blind verifier)

> **Premise #5/#6 (joint): the identification of |psi|^2 with the COORDINATE
> density N (and the detector sampling coordinate volume) vs with the PROPER
> density rho_proper.** This single choice flips the verdict between branch (a)
> flat-Born (weight absorbed, unobservable) and branch (b) metric-corrected
> (observable e^{phi} deviation). Check-2 cannot decide it; it is fixed by the
> scalar character of the UDT guiding wave (Check-1: the variable in which the
> guidance/continuity equation is natively written). A verifier should (i)
> confirm sqrt(g)=e^{phi} r^2 sin th from the canonized metric independently,
> and (ii) confirm that NOTHING in Check-2 secretly fixes which density |psi|^2
> is — i.e. that the verdict is honestly a conditional fork, not a smuggled
> flat-Born.

---

## VERIFIER BLOCK — BLIND ADVERSARIAL PASS

**Date:** 2026-06-17. **Agent:** blind verifier (Opus 4.8 1M). **Method:** independent
sympy re-derivation of the spatial determinant and weight; independent reconstruction
of the medium-wave (LATER-4) conserved norm from VERIF_ceff_potential.py; cross-read of
CANON / STATE.md:204-205 / measure_fork_results.md (bare-2-sphere) and
quantization_check1_guiding_MAP.md (the guidance law). No data peeking.

### (A) MEASURE RE-DERIVATION — **SURVIVES.**
Independent sympy: det(g_spatial)=r^4 e^{2phi} sin^2 th, sqrt(g)=e^{phi} r^2 sin th,
weight W=e^{phi} (power +1). CONFIRMED exact. The load-bearing structural claim (BARE
2-sphere) is genuinely load-bearing AND genuinely backed: my counterfactual sympy with
e^{2phi}-dilated angular legs gives sqrt(g)=e^{3phi} r^2 sin th, so the power-1-vs-3
distinction hinges entirely on premise #2. That premise is corroborated by STATE.md:204-205
("self-adjoint measure is r^2 sin th BARE; e^{-2phi} in the stiffness") and the
measure_fork ruling. Reading is honest. (Cosmetic: Abs(sin th) on theta in [0,pi] = sin th.)

### (B) PART-B BOOKKEEPING — **PARTIAL.**
Covariant continuity and N=sqrt(g)*rho_proper as the coordinate-integrable/equivariant
object: standard and correct; the e^{phi} relation N = e^{phi} r^2 sin th rho_proper is
exact. The e^{phi} deviation algebra checks. HOWEVER the dichotomy |psi|^2 in {N,
rho_proper} is NOT manifestly complete: half-density / weighted-scalar conventions
(|psi|^2 = g^{1/4}-type) exist in curved QM and are a third bookkeeping. More concretely
(see C), the ONE wave UDT actually has — the LATER-4 medium-wave — carries a conserved
norm weight (P/f = 2r^2 e^{2phi}/(1+w)^2) that is NEITHER N (radial weight e^{phi} r^2)
NOR rho_proper: it differs from N by an extra e^{phi}. So the enumerated pair does not
provably exhaust the candidate densities. This is the doc's biggest gap, though it does
not break the conditional verdict (the doc explicitly defers the selector to Check-1).

### (C) FORK-COLLAPSE ATTACK — **FORK DOES NOT COLLAPSE (doc SURVIVES on this point).**
The attack hypothesis was that the LATER-4 medium-wave's own definition (psi=u*sqrt(P),
P=2r^2/(1+w)^2) pins the scalar character and forces branch (a) or (b) now. It does NOT,
for a decisive structural reason: the LATER-4 wave is the ripple OF THE METRIC SHAPE FIELD
w (an optical-cavity mode of the geometry), NOT a guiding/pilot wave for a localized
object's collective position X. quantization_check1_guiding_MAP.md is explicit: the
GUIDANCE LAW is UNBUILT ("the corpus has NOTHING here," Wall 3; ledger #5: "v proportional
to grad S — NEITHER chosen nor derived; UNBUILT"), and ledger #1 separates the medium-wave
from the guidance. Since the wave whose scalar character would decide the fork (the guiding
wave) does not yet exist, the fork is HONESTLY conditional on Check-1, exactly as claimed.
COLLATERAL FINDING (adversarial, recorded against premise B): had one (wrongly) treated the
existing LATER-4 wave as the guiding wave, its conserved norm weight P/f ~ r^2 e^{2phi}
matches NEITHER fork branch (off N by e^{phi}) — so that wave would land OUTSIDE the doc's
enumerated pair, not on (a) or (b). Either way the fork does not collapse to a branch; if
anything this strengthens "Check-2 cannot decide it" while denting the completeness of B.

### (D) SEAL ILL-POSEDNESS — **SURVIVES (benign, as claimed).**
e^{phi}->0 at the seal is structurally identical to the routine r^2->0 zero of the flat
spherical measure at the origin: a measure zero at a boundary. Weight is bounded in (0,1]
on phi in (-inf,0], so over the finite cell the total mass int e^{phi}|psi|^2 r^2 ... is
finite for any normalizable |psi|^2 (toy phi=log r gives int r^3 dr = 1/4, finite). No
divergence, no forbidden interior region; normalization is fine. The only real content is
that the natural measure is NON-UNIFORM and pinches at the seal (object cannot localize
exactly at the core) — correctly flagged as benign-but-relevant-for-typicality, with the
"is it pathological?" hook deferred to the seal BC (Check-1/3). Honest.

### (E) PREMISE / SMUGGLE AUDIT — **SURVIVES.**
No smuggled flat-Born and no smuggled deviation. The doc keeps both branches live, tags
the detector-samples-coordinate-volume step (#6) as a CHOSEN modeling premise, and never
asserts a single verdict. Premise #5 honestly carries the "chose (enumerated both)" tag.
"Geometry supplies a real e^{phi} weight; observability conditional on Check-1" is an
accurate characterization. The one residual is the (E)->(B) completeness gap above, which
the doc does not claim to have closed.

### VERDICT
- (A) SURVIVES · (B) PARTIAL · (C) SURVIVES — fork does NOT collapse · (D) SURVIVES · (E) SURVIVES.
- **Overall confidence the doc's verdict (conditional fork, weight=e^{phi}) is correct: 0.85.**
  The measure (e^{phi}, power +1) and the conditional-fork structure are solid; the deduction
  is honest and not verdict-hunting.
- **Single biggest weakness:** the |psi|^2 in {N, rho_proper} dichotomy (Part B) is asserted,
  not proven exhaustive — and the only concrete UDT wave (LATER-4) carries a weight (P/f ~
  e^{2phi}) lying OUTSIDE that pair. The fork may be a TRICHOTOMY-or-more once the guiding
  wave is actually built; the doc's two-branch framing could under-enumerate.
- **Fork-collapse (task C):** NO. The medium-wave is a metric-shape ripple, not the (unbuilt)
  particle-guidance wave, so it cannot pin psi's scalar character. The conditional fork is
  honest, NOT a smuggled flat-Born.
