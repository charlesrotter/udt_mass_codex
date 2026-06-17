# PRE-REGISTRATION (frozen): examine the DERIVED matter-sector phi-angular potential V

STATUS: pre-registration, committed BEFORE the run. Derivation track, LOCAL branch
session-2026-06-17 ONLY. NOT canon. Frozen model + safeguards + success/failure + premise
ledger fixed here; no retuning after the run.

PROVENANCE: the keystone derivation (check1_wall3_keystone_results.md + verifier block,
2026-06-18) found that the FULL native matter field's tangent-fluctuation operator is the
JACOBI/geodesic-deviation operator (NOT free box_g), carrying a DERIVED background potential
V ~ K[|grad n0|^2] ~ sin^2(Theta)/r^2 + e^{-2phi} Theta'^2 (+ a tangent-bundle U(1) connection).
This is the matter-field guiding-wave equation's own potential. We examine WHAT IT DOES.

GOAL-CORRECT: emergent quantization (the quantum structure of the guiding wave) -- NOT a mass
hunt (LATER-15). V is examined as "what it does to the QUANTUM structure" (the quantum potential;
whether the matter wave has discrete modes = a quantum face), not as a route to mass ratios.

SAFEGUARDS (Charles, 2026-06-18 -- this machine lacks the workstation's auto-audit; replicate
manually, binding):
S1. RE-DERIVE V FROM L2 INDEPENDENTLY -- do NOT import the keystone/verifier V; derive the
    quadratic fluctuation (second-variation) operator of L2 around the hedgehog from scratch,
    state it exactly, THEN compare to the prior V.
S2. REAL BACKGROUND, NO ANSATZ -- obtain Theta(r) by actually solving the hedgehog field ODE on
    this machine (state ODE + BCs + finite-cell termination + numerical method). If a
    representative analytic profile is used for a first look, FLAG it and show the verdict is
    ROBUST to the profile (vary it).
S3. NO approximation/linearization as a stated result (charter principle 2). The fluctuation
    operator is the exact second variation (legitimate); the BACKGROUND must be the real solution;
    any further reduction is DECLARED and bounded.
S4. TRAP-TEST vs conjecture-A box-control (LATER-4/5): any "discrete mode" MUST be tested for
    box-control -- vary the cell/wall size R and report whether eigenvalues are INTRINSIC
    (depth-controlled, stable as R grows) or BOX-CONTROLLED (~1/R^2, a wall artifact). Box-control
    is a first-class NEGATIVE, not discreteness.
S5. Every value/BC/sign/chart tagged chose/derived. Absences reported as results.
    VERDICT-HUNTING GUARD: bound modes / "native discreteness" is the DESIRED answer; report the
    exact mode structure even if it is box-controlled or empty.
S6. INDEPENDENT BLIND VERIFIER re-derives V again + re-runs the box-control trap-test after.

## FROZEN MODEL

- Action: native matter L2 (S^2 sigma-model) [+ note L4] on the static UDT metric
  ds^2=-e^{-2phi}dt^2+e^{2phi}dr^2+r^2 dOmega^2. Background = the degree-1 hedgehog n0 (profile
  Theta(r), n0 = (sin Theta cos(m phi_ang)... ) per the corpus's exact hedgehog ansatz -- cite).
- Fluctuation: tangent perturbation eta (2 real components = 1 complex on the S^2 tangent plane),
  the matter guiding wave. Operator = exact second variation of L2.
- Sources to cite for exact forms: native_stabilizer_results.md, angular_lagrangian_results.md,
  lepton_soliton_spectrum_results.md, whole_metric_full_solve_results.md.

## PRE-REGISTERED QUESTIONS + OUTCOMES (no retuning)

E1 -- V FROM SCRATCH: independently derive the L2 second-variation operator; state V exactly;
   compare to the prior V ~ sin^2(Theta)/r^2 + e^{-2phi}Theta'^2 (+ connection). MATCH or DIFFER?
E2 -- REAL PROFILE: solve the hedgehog ODE for Theta(r) with stated BCs + finite cell. Report it.
E3 -- EFFECTIVE RADIAL OPERATOR: with angular-harmonic decomposition, give V_eff(r) for the
   matter fluctuation (include the sigma-model centrifugal sin^2(Theta)/r^2 and e^{-2phi}Theta'^2,
   the connection, and the angular eigenvalue). Is there a genuine REPULSIVE near-core barrier
   (the thing conjecture-A's METRIC sector lacked)?
E4 -- MODE STRUCTURE (the test): under regularity-at-core + finite-cell/seal BC, does V_eff support
   DISCRETE BOUND modes? Run S4's box-control trap-test (vary R). Report: intrinsic-discrete /
   box-controlled / no bound modes. THIS IS THE CRUX -- report honestly.
E5 -- QUANTUM-STRUCTURE EFFECT: what does V do to the Bohm quantum potential (Q -> box_g R/R + V)?
   Characterize the correction and whether it gives the guiding wave a native discrete/quantum
   feature, at lab depth (phi->0) vs hadronic depth.

## SUCCESS / FAILURE (frozen, all first-class)

- STRUCTURE-POSITIVE: V_eff has a genuine repulsive barrier giving INTRINSIC (not box-controlled)
  discrete bound modes that survive S4 -- a native quantum feature in the matter sector that the
  metric sector lacked. (Would CONDITIONS-CHANGE the conjecture-A negatives for the matter sector.)
- STRUCTURE-NEGATIVE: box-controlled (fails S4) OR no barrier OR no bound modes -- the matter
  sector ALSO lacks intrinsic trapping; V is a depth-dependent dressing only. A clean negative.
- PARTIAL: barrier present but binding marginal / regularity-killed / profile-dependent.

## PREMISE LEDGER (frozen; chose/derived)

1. L2 second-variation operator = the matter guiding-wave operator -- DERIVED.
2. Hedgehog background Theta(r) = solution of its field ODE -- DERIVED (to be solved here);
   if representative profile used, CHOSEN+flagged+robustness-checked (S2).
3. Finite-cell / seal BC + regularity-at-core -- the BCs are LOAD-BEARING (conjecture-A turned on
   exactly the core BC). Tag each chose/derived; test sensitivity.
4. Angular eigenvalue / harmonic sector -- CHOSEN per mode; scan the low sector.
5. L4 -- noted; if dropped from the fluctuation operator, FLAGGED as a declared reduction + its
   expected effect bounded.

LOAD-BEARING PREMISE flagged for the blind verifier: the core boundary condition (S4/premise 3)
and whether any discreteness is intrinsic vs box-controlled -- the exact rung conjecture A turned on.
