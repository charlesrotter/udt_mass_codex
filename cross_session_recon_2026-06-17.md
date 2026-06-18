# Cross-session recon — mining origin/session-2026-06-17 (quantization-emergence fork)

Recon only; we KEEP main (branch NOT merged). A parallel session diverged from the SAME point
(commit 49292cf) and pursued the OTHER fork: how does quantization/the quantum face EMERGE from the
UDT metric (pilot-wave / waves-in-the-dilation-medium / eigenvalue-spectrum / Bell). Read read-only via
`git show origin/session-2026-06-17:<file>`. Its own HANDOFF says "nothing this session is CONCLUSIVE"
— treat as provisional leads; several pieces are blind-verified there (not re-verified by us). Recon
agent a3d3d20abc5d73d7f. This doc = the DISTILLED usable findings for our (main) line.

## THE FINDING THAT REDIRECTS US (high value)
*** A SINGLE-CELL FLUCTUATION / "vibration-notes" EIGENVALUE SOLVER WILL NOT GIVE THE LEPTON MASS
FAMILY AS RATIOS — it is BOX-CONTROLLED. *** Confirmed 4x there (metric sector, L2-only matter,
WITH-L4 shallow, WITH-L4 deep at the EXACT coefficient): every fluctuation mode in every sector
(l=0,1,2) has omega^2 ~ 1/R^2 -> 0 as the finite cell grows; the absolute frequency is set by the
CELL WALL, only the ratio-SHAPE is intrinsic, and that shape is just the box's own integer ladder
(the #44 breathing tower = the box's modes). => the "eigenvalue/standing-wave spectrum of one cell"
route (our fork B as naively conceived) is ALREADY RUN and box-controlled. Their escape (CONVERGENT
with our line): native discreteness is TOPOLOGICAL (winding) or in the NON-STATIONARY / CLOSED-TIME
sector, NOT the static fluctuation spectrum.

SHARPENING for the lepton GENERATIONS (e/mu/tau, SAME charge, different mass): our winding catalog
gives CHARGE diversity (m=1,2,3 charge sectors), NOT same-charge generations; the depth axis (#54/#56
super-exponential M(p)) is the same-charge family but a CONTINUUM with no static selector; and the
single-cell breathing spectrum is box-controlled. => the generation selector is most likely the
CLOSED-TIME / non-stationary sector (the #57 time-selector done properly), not static-spectral and
not winding-charge. Both sessions independently point here.

## REUSABLE TOOLS / RECIPES (if we do spectral/fluctuation work)
- deep_phi_mode_sign_results.md: the EXACT native l=0 Sturm-Liouville Hessian of the reduced action
  (closed forms P kinetic, Q potential, R_mix, exact breathing weight
  W=(2pi/3)[2kappa(sin^4 Th+sin^2 Th)+r^2 xi(sin^2 Th+2)] e^{3phi}); l=0,1,2 generalized eigenproblem
  H u = omega^2 W u (with_L4_fluctuation_results.md). REUSE rather than rebuild.
- NUMERICS PITFALL (documented, verified there): float64 is GARBAGE in deep-phi (the e^{phi} span
  wrecks conditioning); use mpmath, log-grid x=ln r, dps>=50. (Relevant to ANY deep-phi spectral solve;
  cf. our own large-grid conditioning troubles.)
- METHOD TRAPS they hit: (i) "representative coefficients" INVERT the physics — a wrong coeff flipped
  the deep-phi sign and manufactured a spurious intrinsic unstable mode (later fully retracted); use the
  EXACT native coefficient. (ii) Dropping L4 produces spurious tachyons — the native stabilizer is
  essential to the QUANTUM structure too.

## CONVERGENCES with our main line (strengthen our banked findings)
- "No presumed quantum sector" — both lines independently conclude discreteness is geometric/topological.
- Mass is native (our milestone) + native U(1) photon — they list these among their positives.
- BOX-CONTROL of the single-cell spectrum — agrees with our "single cell is not the catalog" and our
  "m>=2 absolute masses not grid-convergeable" (both say absolute scales aren't pinned by one cavity).
- QCD/angular overlap: both keep q=1/3, N=3 as the surviving overlap.

## TENSIONS to flag (hold loosely; surface to Charles)
1. OBJECT IDENTITY: their MAP says the native single-cell soliton is a self-gravitating GLOBAL-MONOPOLE
   O(3) degree-texture (Barriola-Vilenkin class, target S^2, pi_2=Z; computed Hopf number = 0) — NOT a
   Skyrme baryon / Hopfion. This TENSIONS our Phase-3/3b reading of the winding objects as "Skyrme B=2
   torus analog." Possibly different objects (their single-cell texture vs our matter-winding catalog),
   but the "Skyrmion" framing should be held loosely; the texture/global-monopole class may be the
   correct identification. WORTH a careful reconciliation before leaning on the QCD-baryon analogy.
2. phi-angular DYNAMICAL resonance DEAD (~0.8): Charles's founding prime-suspect (phi x angular ->
   discreteness) fails as a DYNAMICAL RESONANCE. Scoped: untested as topology / closed-time. Our hunch
   memory still flags phi-angular as the discreteness suspect — this scopes it down.
3. Fermion must be POSTULATED (Berry phase 0, no native double-cover, su(3) kinematic not gauge): a
   re-derivation of the wall, but on the SM-analog line we SHELVED 2026-06-15 (observation-led). Not new.
4. #51 (the corpus hedgehog is NOT pointwise unit): caps confidence on EVERY matter-sector coefficient
   on both lines — a source-level issue flagged for the workstation (us).

## PILOT-WAVE ARCHITECTURE (their claimed picture; conditional, not derived)
particle = m=1 global-monopole texture; guiding wave = smooth tangent fluctuation of the SAME n-field;
nonlocality = the seal (c_eff=e^{-2phi}->inf at the cell boundary); Born = finite-cell typicality vs the
native config-space measure. UDT can HOST a relativistic KG-Bohm pilot wave (guidance law, Bohm quantum
potential, Schrodinger slow-limit) — BUT conditional on a PARKED rest-clock/hbar input, and the
clock->wave step is GENERIC relativity, not UDT-native. de Broglie CLOCK is ABSENT (verified): the static
texture has no native rest-energy clock ("hbar is input" and "no native rest clock" are the SAME gap).
Born is a clean FORK (native spatial measure e^{phi} r^2 sin th; flat-Born iff the guiding wave is a
coordinate scalar, else an e^{phi} deviation). Check 3 (Bell/seal, "the sharpest falsifier") is
PRE-REGISTERED but NOT RUN.

## NET — what we USE
1. REDIRECT fork B: do NOT build a single-cell fluctuation-spectrum solver for lepton ratios (box-
   controlled, already run). If we pursue the spectrum/quantum route, target the CLOSED-TIME /
   non-stationary sector (#57 done properly) or the topological/winding axis (our catalog).
2. If we ever do deep-phi spectral work, reuse their exact operator + mpmath-log-grid-dps>=50 recipe and
   heed the representative-coefficient + drop-L4 traps.
3. Reconcile the OBJECT IDENTITY (global-monopole texture vs Skyrmion) before leaning on QCD-baryon analogy.
4. Bell/seal (Check 3) is unrun and orthogonal to our solver — a separate future falsifier.

## AUDIT of the box-control claim (2026-06-17) — CONFIRMED to our standards
Charles flagged that the parallel session may not share our safeguards. Adversarial audit
(agent a0c2d1dcae12a52fe, read-only on branch + independent re-derivation/re-run) VERDICT:
**BOX-CONTROL HOLDS; the redirect is SAFE.**
- Operator = genuine exact 2nd variation of the native reduced energy (L2+L4, full xi,kappa, correct
  weight W~e^{3phi}); NOT a representative coefficient, L4 kept. Reproduced independently.
- BC is NOT the artifact (the key risk): re-ran with a FREE (Neumann) seal -> still box-controlled
  (omega^2*R^2 ~ const). Dirichlet is conservative (raises eigenvalues, can't hide a negative). So the
  1/R^2 scaling is a property of the OPERATOR, not the wall.
- 1/R^2 MEASURED, reproduced to all printed digits: omega^2*R^2 = 57.7/55.6/53.5/50.9 at R=8/16/32/64.
- The interim "intrinsic unstable deep-phi mode" (omega^2~-0.55) RETRACTION is CORRECT (it was a
  representative-coefficient/weight mis-normalization). Pre-registered + blind-verified there (conf 0.82),
  category-A clean (only chosen value xi=kappa=1, ratio-robust).
- GENUINE CAVEAT (both sessions share it): premise #51 -- the hedgehog carrier is NOT pointwise-unit
  (|n|^2 = 1 - sin^2 Theta cos^2 theta), so the well's coefficients rest on that carrier; a true unit map
  gives a different energy (65.7 vs corpus 4.74). Caps confidence <0.9. Does NOT undermine the box-control
  redirect, but MUST be closed before building any DERIVE on this fluctuation operator.
NET: the warning is trustworthy. Single-cell fluctuation spectrum is box-controlled (audited) -> do not
build a lepton-mass-family solver on it; discreteness is topological/winding or closed-time/non-stationary.

## FOUR-CLUSTER AUDIT (2026-06-17) — remaining branch claims, graded + bring-over decisions
Four parallel adversarial audits (agents a9b561.../addbb6.../a28510.../af42e1...; read-only on branch +
independent re-derivation). Verdicts:

### A. OBJECT IDENTITY / TOPOLOGY (agent a9b561)
- Branch claim "single-cell soliton = global-monopole O(3)/S^2 degree-texture (pi_2=Z, Hopf=0), NOT a
  Skyrme baryon": HOLDS *for the BRANCH's carrier* (the non-unit 3-vector, target S^2) — VERIFIED
  (rests on crux1_statistics_topology blind-verified 2026-06-15).
- *** CONFLICT with cluster D (important, do NOT bank an object-identity correction): *** the BRANCH
  analyzed an S^2 (non-unit 3-vector) field; our MAIN line's soliton+catalog use the UNIT S^3 (SU(2)/
  Skyrme) 4-vector (cluster D, confirmed |n|^2=1 to 4e-17). DIFFERENT CARRIER FIELDS -> different
  topological class (branch S^2/pi_2 texture vs main S^3/pi_3 Skyrme-class). So "it's a texture not a
  Skyrmion" is about the BRANCH field and does NOT correct main; our "Skyrme B=2" reading is defensible
  for the S^3 object. OPEN RECONCILIATION ITEM: pin the precise carrier + topological class of main's
  ACTUAL catalog object (S^3/pi_3 vs S^2/pi_2). Hold "Skyrme B=2 torus" loosely but do NOT replace with
  "texture." Branch multicell-tiling-dead + relational-winding-no-catalog: HOLD as PROVISIONAL, static-
  scoped, premise-laden, single-pass (branch's own HANDOFF: "nothing conclusive").

### B. de BROGLIE CLOCK ABSENT (agent addbb6) — SCOPED, HOLDS
- "Static texture has no native rest-energy clock; only native clock is spin-tied omega=J/Lambda_3
  (Lambda_3 native)": HOLDS but SCOPED to the STATIC ansatz (by construction). Single-pass (verifier
  pending there); de Broglie eikonal machinery independently re-derived + strengthened (worldline-INDEP).
- IMPACT: SUPPORTS our closed-time/non-stationary selector plan (green light, not wall): the moment the
  closed-time sector supplies a carrier omega_clock, the native de Broglie wave follows for free. Soften
  the branch's "whole wave-face = one missing input" (over-collapses static->all).

### C. PILOT-WAVE / SCHRODINGER / BORN (agent a28510)
- Guidance law + Schrodinger slow-limit: SCOPED — mostly GENERIC relativity (any curved KG metric) with
  hbar + flowing phase PARKED as inputs; only the e^{-4phi}/e^{2phi} factors are UDT-native. HOSTING/
  consistency, NOT emergence. Do NOT port as "native QM."
- box_g "identically" claim: REFUTED (their own verifier caught it). Corrected operator =
  D^m D_m eta + K|grad n0|^2 eta; the dropped Jacobi term K|grad n0|^2 IS the phi-angular coupling (the
  discreteness prime-suspect) — interesting to OBSERVE, not bury.
- Born native measure sqrt(g_spatial)=e^{phi} r^2 sin th (radial-only dilation, power +1, NOT e^{3phi}):
  HOLDS — the ONE genuinely UDT-native result in this cluster (independently reproduced). Fork is honest
  but under-enumerated (a 3rd branch e^{2phi}=KG charge density exists).

### D. phi-ANGULAR RESONANCE + #51 (agent af42e1) — the load-bearing cluster
- phi-angular resonance "DEAD ~0.8": SCOPED, weaker than billed. Mechanism is "TOO STRONGLY coupled ->
  broadband parametric runaway selects nothing" (not "too weak"). Retires Charles's founding suspect
  ONLY in the dynamical/parametric form, ONE channel (centrifugal-breathing), under FORCED premise C1
  (Lambda_3(b)=(1+b)^2), single-pass, NO blind verifier, ALREADY downgraded to PROVISIONAL by Charles
  (branch LATER-14). => provisionally weakened in one form, NOT genuinely retired; topological/closed-
  time forms untouched.
- matter-sector V box-control + "tachyon = L4-drop (Derrick) artifact": HOLDS (consistent with our
  box-control audit; branch's own verifier walked back the tachyon overclaim -> "L2-only box-controlled;
  WITH-L4 untested").
- *** #51 (non-unit carrier) — the worry RESOLVED FOR OUR LINE: *** the corpus 3-vector IS genuinely
  non-unit (|n|^2 = 1 - sin^2 Theta cos^2 theta, independently confirmed); the obvious unit fixes are
  singular (1/sinth pole) or profile-free. BUT the correct unit field = the S^3 (SU(2)/Skyrme) 4-vector,
  and OUR MAIN LINE ALREADY USES IT: the milestone soliton (radial_Bfree/whole_metric_solve_3D), the
  winding catalog (full3d_spectral/winding_catalog_map, |n|^2=1 to 4e-17), and CANON C-2026-06-14-1
  (unit monopole n=x/r) are UNAFFECTED. #51 is QUARANTINED to the SHELVED single-cell fluctuation-V line.
  *** CORRECTION to this doc's earlier "#51 caps every matter-sector coefficient on BOTH lines": it does
  NOT threaten main. We do NOT need to close #51 for the soliton/catalog/canon (already closed there via
  the S^3 4-vector). #51 only caps the branch's matter-sector-V coefficients. ***

## BRING-OVER DECISIONS (what we PORT to main vs leave)
PORT (as scoped records/registry negatives):
- The #51 RESOLUTION (above) — high value: removes the cross-line worry; main uses the unit S^3 carrier.
- Scoped PROVISIONAL negatives -> NEGATIVES_REGISTRY (each with premise set, cross-session/UNVERIFIED-here):
  phi-angular dynamical-resonance dead (one channel, forced C1); static texture no native rest clock
  (supports closed-time selector); static multicell tiling + relational-winding give no catalog.
- The Born NATIVE MEASURE e^{phi} (radial-only) — as a scoped reusable geometric fact.
- The de Broglie eikonal machinery is native+exact (worldline-indep) — reusable capability note; the
  closed-time sector supplying omega_clock would complete it.
LEAVE / do NOT port as results:
- pilot-wave "native host" + Schrodinger "native" HEADLINES (hosting/consistency, not emergence).
- the box_g "identically" claim (refuted) — if referenced, use the CORRECTED operator (+ note the dropped
  K|grad n0|^2 = phi-angular suspect).
- "object is a texture not a Skyrmion" as a CORRECTION to main (it's about the branch's S^2 field; main is
  S^3) — record as an OPEN reconciliation item instead.
NET: nothing merged; main keeps the unit-S^3 soliton/catalog (unaffected by #51); the closed-time selector
remains the pointed-to lepton-generation route, now with a native de Broglie machinery waiting for a carrier.
