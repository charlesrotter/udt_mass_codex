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
