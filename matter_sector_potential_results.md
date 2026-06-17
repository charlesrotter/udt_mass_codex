# Matter-Sector Phi-Angular Potential V — OBSERVE Results (E1–E5)

Date: 2026-06-17. Driver: Claude (Opus 4.8, 1M ctx). Mode: OBSERVE (pre-registered,
safeguarded). Branch: session-2026-06-17 (local). NOT canon. NEW file (append-never-edit).

Contract (frozen): `matter_sector_potential_PREREG.md` — obeyed exactly, no retuning.
Scripts (committed this push):
- `VERIF_matter_sector_potential_E1.py` — symbolic Jacobi/second-variation derivation (S1).
- `VERIF_matter_sector_potential_E2.py` — REAL hedgehog profile via scipy solve_bvp (S2).
- `VERIF_matter_sector_potential_E34.py` — V_eff + eigenproblem + S4 box-control trap-test.
Blind adversarial verifier: PENDING (verifier-before-record; attack-here block at end).

GOAL FRAME (per contract): emergent quantization — does the DERIVED matter guiding-wave
potential V give the wave INTRINSIC discrete modes (a native quantum face the metric sector
lacked)? NOT a mass hunt. Report what the math gives, desired or not.

---

## HEADLINE VERDICT: STRUCTURE-NEGATIVE (clean)

The DERIVED matter-sector potential V does **NOT** support intrinsic discrete bound modes.
Its angular/curvature contribution is **ATTRACTIVE (tachyonic), not a repulsive barrier**;
under the regular-core + finite-cell(seal) BC the spectrum is either (a) **BOX-CONTROLLED**
(omega^2 ~ 1/R^2, a wall artifact — fails S4) for the positive modes, or (b) a **depth-controlled
NEGATIVE omega^2 instability** from the attractive curvature term — never a stable discrete
bound tower. This is the SAME Friedrichs/box-control wall conjecture-A hit (LATER-4/5), now
reached INDEPENDENTLY from the matter side. The matter sector also lacks intrinsic trapping;
V is a depth-dependent dressing of the guiding wave, not a generator of discreteness.
Confidence 0.82. This CONFIRMS (does not change) the conjecture-A negatives for the matter sector.

---

## E1 — V FROM SCRATCH (S1): **MATCH** (with one flagged subtlety) — SUCCEEDS

Re-derived the L2 tangent-fluctuation operator FROM SCRATCH two ways (no keystone import):
(D1) moving-orthonormal-frame O(eta^2) expansion of L2 = -(xi/2) g^{mn} d_m n . d_n n;
(D2) textbook S^2 sigma-model second-variation (Jacobi / geodesic-deviation) operator. Both give

    J eta = - D^m D_m eta  -  K [ |grad n0|^2 eta  -  <eta, grad n0> grad n0 ],   K = Gauss(S^2) = 1,

with D_m the connection-covariant derivative carrying a tangent-bundle (U(1)) connection w_m.
The background curvature potential has MAGNITUDE |grad n0|^2 and a **NEGATIVE (attractive/tachyonic)
sign** on the transverse component.

`|grad n0|^2` on the static UDT metric (sympy, exact). FLAGGED SUBTLETY (load-bearing, S2/S5):
the corpus hedgehog `n=(sinTheta sin th cos(m ph), sinTheta sin th sin(m ph), cosTheta)`
(lepton_soliton_spectrum:31) is **not a unit S^2 vector** as written (|n|^2 = 1 - sin^2Theta cos^2 th).
No genuine unit S^2 field reproduces the corpus invariant `e^{-2phi}Theta'^2 + 2 sin^2Theta/r^2`
pointwise (that is the SU(2)/S^3 Skyrme |grad U|^2 form). The factor-2 angular piece arises only
in the SPHERE-REDUCED energy E2_r — the corpus' own derived background invariant. We therefore
use the reduced invariant `|grad n0|^2_reduced = e^{-2phi}Theta'^2 + 2 sin^2Theta/r^2` and TAG the
reduction. (Pointwise unit invariants computed for the record: suspension =
e^{-2phi}Theta'^2 + sin^2Theta/(r^2 sin^2 th); pure hedgehog Theta=theta = 2/r^2 — matches
angular_lagrangian X=2/r^2.) This S^2-texture vs S^3-Skyrme distinction is STATE_DERIVATION #51.

**COMPARE TO PRIOR keystone V ~ sin^2(Theta)/r^2 + e^{-2phi}Theta'^2 (+ connection): MATCH** in
structure — radial e^{-2phi}Theta'^2 + angular sin^2Theta/r^2 curvature term + the tangent-bundle
U(1) connection w_m. The ONLY refinement vs the prior verbal V: the curvature term's SIGN is
explicitly **attractive** (the keystone wrote it as a magnitude). VERDICT: SUCCEEDS (S1 satisfied;
V independently reproduced; sign and S^2/S^3 caveat surfaced).

## E2 — REAL PROFILE (S2): **SUCCEEDS**

Solved the REAL hedgehog Theta(r) from the corpus reduced field ODE (Theta'' = num/den, EL of
E2_r+E4_r; den = 2r^2(r^2 cos2Theta - 5r^2 - cos^2 2Theta + 4cos2Theta - 3)), NOT an ansatz.
- BCs: Theta(core)=pi, Theta(seal)=0 [DERIVED charge-1 hedgehog]. Finite cell r in [1e-3, 8] L
  [finite-cell canon]. Method: scipy solve_bvp, tol 1e-8.
- Flat (phi=0): monotone pi->0, half-twist r=0.69 L, max rms residual 1.0e-8
  (corpus width 0.648 L — agrees within solver/grid tolerance).
- Deep-phi (phi=-ln(r_int/r), p=1, phi_core~-7.9): twist pushed OUTWARD to r=2.1 L, residual 1e-8
  (matches corpus "deep-phi pushes twist outward", native_stabilizer:126). TWO real profiles in hand.
S2 satisfied: real EOM solutions, two backgrounds; E4 verdict re-run on both (below) -> robust.

## E3 — EFFECTIVE RADIAL OPERATOR: **NO REPULSIVE BARRIER** — the crux input

Static fluctuation eta ~ e^{-i omega t} Y_l u(r), g^{tt}=-e^{2phi} -> frequencies weighted by
e^{2phi}. The self-adjoint radial operator (DERIVED from the Jacobi operator on the metric):

    -(1/(e^{phi} r^2)) d_r( e^{-phi} r^2 d_r u ) + [ l(l+1)/r^2 + V_curv(r) ] u = omega^2 e^{2phi} u,
    V_curv(r) = - ( e^{-2phi} Theta'^2 + 2 sin^2Theta / r^2 )   (ATTRACTIVE).

Answer to the contract's E3 question ("genuine REPULSIVE near-core barrier?"): **NO.**
- The ONLY positive (repulsive) near-core term is the ordinary scalar centrifugal l(l+1)/r^2
  — present for ANY wave, not a matter-sector specialty. (This is MORE than conjecture-A's metric
  sector had: there the coupled operator carried l_eff=0 EXACTLY, no centrifugal at all, LATER-5.)
- The matter-sector curvature/winding dressing sin^2Theta/r^2 enters ATTRACTIVELY (the S^2 Jacobi
  curvature term is tachyonic), so it is a near-core WELL, not a barrier.
=> The "thing the metric sector lacked" (an intrinsic repulsive barrier) is STILL ABSENT here.

## E4 — MODE STRUCTURE + S4 BOX-CONTROL TRAP-TEST (CRUX): **BOX-CONTROLLED / TACHYONIC** — STRUCTURE-NEGATIVE

Regular-core + finite-cell(seal) Dirichlet eigenproblem, generalized SL (weight e^{2phi}),
finite differences. Convergence verified: omega0^2 stable to 6 digits N=1500->6000.
Box-control trap-test — seal radius R = {8, 25, 80, 250} (factor ~31, S4: >=4 values, factor>10):

| background / l | R=8 omega0^2 | R=25 | R=80 | R=250 | omega0^2 * R^2 | verdict |
|---|---|---|---|---|---|---|
| flat, l=1 | 2.313e-1 | 3.199e-2 | 3.154e-3 | 3.230e-4 | 14.8 -> 20.2 (const) | **BOX-CONTROLLED** |
| deep(p=1), l=1 | -2.989 | -2.720 | -2.183 | -1.519 | (omega0^2<0) | **TACHYONIC** (depth-set) |
| flat, l=0 (s-wave) | -5.040 | -4.988 | -4.818 | -4.335 | (omega0^2<0) | **TACHYONIC** (depth-set) |

Diagnostics (decisive):
- POSITIVE modes (flat l=1; all excited modes everywhere): omega^2 ~ 1/R^2, omega^2*R^2 -> ~20.2
  = 2 pi^2 (the box constant for the e^{2phi}=1 weight-2 problem) -> **pure wall artifact**,
  omega^2 -> 0 as R grows. FAILS S4. (Conjecture-A box constant was ~9 for its weight; same KIND.)
- NEGATIVE lowest modes (l=0 always; deep-phi): the attractive Jacobi well drives omega^2 < 0;
  |omega0^2| is DEPTH/profile-controlled and STABLE as R grows (flat l=0: -5.04 -> -4.33 over a
  31x box) — i.e. an INTRINSIC instability, NOT a bound tower (a tower needs a DISCRETE set of
  positive omega^2, not one tachyonic mode + a box-controlled continuum-in-the-box above it).
- TOGGLE confirmation (causal attribution): setting V_curv -> 0 REMOVES the negative eigenvalue
  entirely; all remaining modes are positive and box-scaling (flat l=0 off-mode: 0.00154 at R=80
  -> 0.000158 at R=250, ratio 9.8 = (250/80)^2 — exact 1/R^2). The negative omega^2 IS the
  attractive curvature term; the positive spectrum IS the box.
- CONTROL (+V_curv artificially repulsive): STILL box-controlled (omega^2*R^2 -> 20.2). Even a
  would-be repulsive barrier of this magnitude does NOT trap under the regular-core BC — the same
  regularity-kill conjecture-A's verifier proved (the wave must vanish where the well/barrier sits).

VERDICT E4: **STRUCTURE-NEGATIVE.** No intrinsic discrete bound tower. Positive modes box-controlled
(fail S4); the attractive curvature term gives a depth-controlled tachyonic instability, not
discreteness. The matter guiding wave has NO native trapped-mode quantum structure.

## E5 — QUANTUM-POTENTIAL EFFECT: depth-dependent dressing, no discreteness — PARTIAL/characterized

Per the keystone (B)/(C) (re-confirmed in E1), the TRUE quantum potential is
Q_true = -hbar^2 box_g R/R + V_curv (the dropped Jacobi term restored). Characterizing V_curv on
the real profiles:
- Lab depth (phi->0): V_curv is O(1) in the body (~6.5 at half-twist), diverges ~1/r^2 at the
  core; e^{-2phi} weight ~1. A modest, localized correction to the free Bohm potential — the
  flat-space guiding wave is essentially undressed away from the core.
- Hadronic depth (phi_core~-7.9, p=1): the radial-gradient piece e^{-2phi}Theta'^2 is amplified by
  e^{-2phi} ~ 7e6 at the core -> V_max ~ 3.8e9 (vs ~3.9e2 at lab). A HUGE depth-dependent dressing
  concentrated near the core, vanishing at the seal (Theta->0).
EFFECT ON QUANTUM STRUCTURE: V dresses the guiding wave strongly and depth-dependently, but (per
E4) gives it NO native discrete/quantum feature — it does not bind. So V's role in the Bohm
picture is a redshift-amplified core potential, not a quantizer. Consistent with the program's
standing result: the only native discreteness is TOPOLOGICAL (winding), not spectral.

---

## PREMISE LEDGER (chose / derived)

1. L2 second-variation = matter guiding-wave operator — **DERIVED** (E1, two methods).
2. Curvature term SIGN = attractive (K=+1 S^2) — **DERIVED** (Jacobi operator).
3. Hedgehog Theta(r) = solution of the corpus reduced field ODE — **DERIVED** (E2, two backgrounds,
   residual 1e-8).
4. Reduced invariant |grad n0|^2 = e^{-2phi}Theta'^2 + 2 sin^2Theta/r^2 — **DERIVED-as-reduced**,
   but **FLAGGED**: the pointwise unit S^2 field does NOT give the factor 2; this is the sphere-
   averaged energy invariant (S^2-texture vs S^3-Skyrme, #51). LOAD-BEARING for the angular term's
   coefficient (not for the box-control verdict, which holds for any positive multiple).
5. Core BC = Dirichlet (regularity: u finite, psi ~ r) — **CHOSEN-but-DERIVED-grade** (the physical
   regular branch; the alt u~1/r is the infinite-energy non-Friedrichs branch, ruled out as in
   conjecture-A). **THE load-bearing premise** (S4/contract): the exact rung conjecture-A turned on.
6. Seal BC = Dirichlet at finite R — **CHOSEN** (finite-cell canon); VARIED in the trap-test (S4).
7. Angular sector l = {0,1} scanned — **CHOSEN per mode** (low sector); both give the same KIND
   of verdict (box / tachyonic).
8. L4 (Skyrme term) DROPPED from the fluctuation operator — **DECLARED REDUCTION** (S3). Expected
   effect: L4 is the higher-derivative STABILIZER; it stiffens gradients and would RAISE positive
   eigenvalues and could regularize the core, but it adds positive-definite gradient energy — it
   cannot create a NEGATIVE-curvature TRAP where none exists, and cannot convert a 1/R^2 box mode
   into an R-independent intrinsic one (box-control is a BC/large-R fact, insensitive to a local
   core term). Bound: L4 affects core-region eigenvalues O(1), does not change the R->large
   scaling that defines the verdict. (Un-recomputed; flagged for the verifier.)
9. Eikonal / linearization — NONE used as a stated result; the operator is the exact second
   variation; the background is the exact EOM solution (S3 satisfied).

## CONFIDENCE: 0.82

High on the structural verdict (box-control + tachyonic, confirmed by convergence, the V_curv
toggle, the sign-flip control, and two independent backgrounds; it reproduces conjecture-A's wall
from a new direction). Held below 0.9 by: (i) premise 8 (L4 dropped, only bounded not recomputed);
(ii) premise 4 (the S^2/S^3 reduction — affects the angular coefficient, examined but not the
verdict); (iii) the FD discretization of a 1/r^2-singular operator near the core (convergence
checked to N=6000; not mpmath-anchored). None of these can manufacture an intrinsic positive
discrete tower out of a box-controlled / attractive structure.

## SINGLE MOST LOAD-BEARING PREMISE (flagged for the blind verifier)

**Premise 5 — the core boundary condition (Dirichlet/regularity) and the resulting box-vs-intrinsic
diagnosis.** This is the exact rung conjecture-A turned on: regular-core trapping is structurally
forbidden because the wave must vanish where the well sits, so any positive mode is the BOX, and
the only thing the attractive well can do is go tachyonic. Verifier should: (a) re-derive the
Jacobi V and its SIGN independently; (b) re-run the box-control trap-test (vary R) and confirm
omega^2*R^2 -> const for positive modes and depth-stable omega^2<0 for the curvature mode;
(c) test whether restoring L4 or an alternative (Robin/seal-physical) core BC changes the
intrinsic-vs-box verdict.

---

## NEGATIVES_REGISTRY ENTRY (proposed, premise-scoped)

NEGATIVE: "The DERIVED matter-sector L2 Jacobi potential V gives the matter guiding wave intrinsic
discrete bound modes." REFUTED (this run). PREMISE SET: L2 second-variation operator (L4 dropped,
bounded); real charge-1 hedgehog on flat + deep-phi backgrounds; regular-core + finite-cell Dirichlet
BC; angular l=0,1; FD eigensolve. The curvature term is attractive (tachyonic), positive modes are
box-controlled (~1/R^2). CONDITIONS-CHANGE triggers: a native repulsive angular barrier uncovered in
the angular Lagrangian (#49/monodromy reopening), a physical non-Dirichlet seal/core BC, or L4
recomputed into the fluctuation operator changing the large-R scaling.

## ATTACK-HERE (for the blind verifier)
- Re-derive J eta and the SIGN of the curvature term (is it -K|grad n0|^2, attractive? — the whole
  verdict hinges on it not being a barrier).
- Independently solve Theta(r) (any method) and re-run the R-scan; confirm box-control + tachyonic.
- Probe premise 8: put a representative L4-stiffening term in V_eff and check the R->large scaling.
- Probe premise 5: try the u~1/r (irregular) branch — does it bind intrinsically? (conjecture-A:
  yes but infinite-energy/unphysical — confirm the same here).
