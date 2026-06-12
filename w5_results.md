# W5 — The Untruncated Species: Results (Arms 1 + 2, verifier-adjudicated)

Date: 2026-06-12. Driver: Claude. Declaration: W5 section of
w_stiffness_push_declaration.md. Arm 1 (UNCOVER): w5_arm1_*.py 47/47
+ w5_arm1_results.md (committed UNVERIFIED by the arm — this doc and
the verifier records supersede its wording where amended). Arm 2
(SOLVE): w5_arm2_*.py suite (sym 21/21, gates 6/6, 934-row catalog,
coupled, frame). Blind verifiers, independent machinery: VW5-1 =
agent a7d7ad6ed8656bd5b (w5_arm1_verifier{1,2,3}.py: 18/18, 20/20,
16/16); VW5-2 = agent ab4f2486105fb651f + sub-verifiers
(w5_arm2_verifier1_sym.py 19/19, verifier2_units, verifier3_fresh/
arclen/kcprobe, verifier4_locus, verifier5_hygiene,
verifier6_coupled_premise). All committed arm scripts rerun clean.
HYPOTHESIS-GRADE labels binding on all kappa != 0 physics.

## HEADLINE — THE PAIRING REVERSAL (VW5-1's central finding)

Arm 1 recorded the phi-angular pairing as dead ("[(1-f) + 4 w_thth]
acquires no EL channel in any equation at any q at this order").
THE VERIFIER REVERSED IT: on the C1-q* branch, the reduced f-equation
at O(kappa) carries a NONZERO w_thetatheta coefficient —
  c_f-row[w_thth]|_{w=0} =
    -8 f r^3 f_r^3 f_theta^2 (2f + r f_r) sin(theta) / (Delta_w^2 P)
— entering through the member Arm 1's carrier bookkeeping missed:
E_f[C1] carries q-JETS, the branch response q* enters with D_theta q*,
and dq*/dw_theta != 0. Established four independent ways (substituted-
density variation at exact rationals; member-product equality;
representative-unambiguity; closed form). EVEN in f_theta (vs S_rtheta
odd), vanishes on spherical as f_theta^2, diverges as 1/Delta_w^2.
THE W2 PAIRING'S w_thth IS EL-VISIBLE — the clock/shape direction has
a derived dynamical channel on the q* branch. Charles's phi-angular
hunch acquires its first derived equation-level entry, found by
machinery attacking a negative (hypothesis discipline working as
designed). Arm 1's w-channel theorem is untouched (E_w[C1] is
q-jet-free); only the f-row statement is reversed.

## The -2/f origin (Arm 1 + VW5-1, amended scope)

- Third + fourth independent proofs of E_w[species] = EL_w[W_wave]
  - (2/f) dL_C1/dw. Stronger (Arm 2, VW5-2-confirmed): D_alg =
  -(2/f) L_C1ang AS DENSITIES at all w — the untruncated w-potential
  is (1 - 2 kappa/f) L_C1ang + beta D_cell, one global factor.
- WEIGHT-STRIPPING identity: the species' algebraic w-channel = C1's
  angular density x (-2 e^{2 phi}) — postulate weight stripped,
  curvature weight installed, localized in the single f_theta^2 slot
  (VW5-1 completeness census closed; div-V invisibility closed
  symbolically both channels).
- Tie-deformation: all contamination ∝ (a+b), vanishing exactly on
  the unimodular line g_TT g_rr = -1 (the postulate's pairing), where
  the tadpole scales as pure a^2 clock-tie content. VW5-1 census
  correction: a third (linear-f_theta) contamination slot exists,
  also ∝ (a+b) — the unimodular verdict survives.
- GUARDRAIL WORDING (VW5-1 adjudication, binding): "only the -2 is
  EH-specific" is supported WITHIN EH on the power-law tie family;
  the cross-action universal ("any curvature-grade scalar carries
  this channel") is UNPROVEN (R^2: existence only). The guardrail is
  sharpened to one number's provenance, NOT softened beyond that.

## The q*-branch adjudication (Arm 1 + VW5-1, symbolic grade)

- c[w_thth] = 0 IDENTICALLY at all q in all three EL channels of the
  density; the wave cone dr/dT = +-f is q-invariant; the w-row of the
  reduced branch EL is {c[w_rr] = 4 f r^2 sin P/Delta_w, c[w_rtheta] =
  S_rtheta = -16 f r^2 sin f_r f_theta^3/(P Delta_w), c[w_thth] = 0}
  (closed symbolically; supersonic flip computed) — NO pure angular
  SL well; bands cannot become lines via the w-row alone.
- BUT with the f-row w_thth door (the headline) the coupled 2D mixed
  operator {w-row + f-row + S_rtheta + the q_TT dynamical channel} is
  the OPEN bands-vs-lines question — NOT settled at the coupled
  level. This is W6's named object.
- The Delta_w divergence is REAL STRUCTURE (not chart image): the
  q-elimination Hessian L_qq|_{q*} = P^4 sin/(4 r^2 Delta_w^3)
  diverges and flips sign across the surface — the static
  q-elimination itself breaks down there; the unreduced three-field
  EL is finite. One locus, now triply characterized (W3 turning
  surface, W4 dressing zero, W5 elimination breakdown).

## The solve map (Arm 2 + VW5-2 sub-verifiers, amendments folded)

- CONVENTION ERRATUM OF RECORD (VW5-2 confirmed analytically + by
  code inspection + numerically): the committed W4-B suite coded
  geo.c = member weld momentum (0.184/0.283/0.091) where the exact
  constant is c = 2. Every banked W4 B-side kappa is member-unit:
  kappa_banked = kappa_true c_m/2. TRUE-unit W4 edges: kc
  0.767/0.180/0.198, ks 1.453/0.343/0.377. The ratio is exactly
  invariant. CONSILIENCE: the fix reconciles W4's "two kappa_c
  families" — the A-side pencil and B-side Rayleigh are the same
  operator (<= 0.4% on all three members). w4_results.md's absolute
  B-side kappa numbers carry this erratum (append-only: recorded
  here and in the registry, not edited there).
- THE RATIO RE-GRADE (VW5-2 fresh-member + kcprobe): the
  domain-graded break is REAL and reproduces on three fresh members
  (full-domain ratios 1.47-1.64 member-dependent; window ratios
  1.838-1.850 (t5) and 1.876-1.880 (t1) member-independent); the ks
  folds are GENUINE saddle-nodes (arc-length verified). BUT the
  window kc' values are NEWTON-FROM-ZERO BASIN-SWITCH artifacts
  (>= 3 coexisting ON equilibria below the claimed edge; the edge is
  solver-dependent), and under the convention-robust dynamic in-band
  criterion the universal window value moves 1.84 -> ~2.12 —
  MEMBER-INDEPENDENCE IS THE ROBUST INVARIANT; the specific constant
  is convention-graded. Flip-overlap mechanism: binary yes (break
  iff overlap), quantitative ranking no. Full-domain edges carry ~1%
  ray-grid error (Nu 24->48).
- W4's D_cell-ON exact statics DIES untruncated (v = 0 static on
  neither branch; ON residual kappa-free) — every shaped cell
  self-dresses; the ON-branch algebraic equilibrium e^{3v} =
  1 - 2 kappa/f exists where f > 2 kappa.
- Continuity corrected: the truncation difference vanishes at
  kappa -> 0, NOT kappa -> infinity; the kappa -> infinity limit is
  a kappa-FREE system (free wave + flipped repulsive C1 force).
- THE LOCUS NULLS UPHELD under sharpened attack (Agmon distance:
  no forbidden region, no trapping at any probed kappa; eigenvalue
  count: no new branch, spectra match species-off to < 0.034 of a
  spacing; pinning: bounded oscillation, no attraction of f to
  2 kappa). Language amendment (VW5-2-4): the "drifts away" reading
  was a diagnostic artifact — the coupled cell executes a bounded
  oscillation about the static dressed cell; the no-pinning negative
  carries the premise "4-mode library-frame slice ansatz,
  weld-anchored IVP" (cannot represent a pinned surface even in
  principle).
- THE COUPLED RENORMALIZATION WAS AN ARTIFACT (VW5-2-6 premise test,
  decisive): claim 6's O(kappa) cell renormalization (max f/f_b up
  to 2.35) and the kappa < 0 slice divergence are BARE-D_alg
  artifacts — the species' true f-EL content vanishes at w = 0
  (Arm 1's E_f map, reconciled exactly); with the subtracted f-force
  the v = 0 cell is undressed to 3.4e-8 and the coupled runs (R1+:
  kappa = +1, t5, both branches probed) march durable and bounded
  with flat pinning. Durable coupled shaped matter STANDS; the
  renormalization story does not.
- HYGIENE RE-SCOPES (VW5-2-5): ON-branch band headline survives on
  energy-valid rows; OFF-branch evolution headlines for |kappa| < 3
  rest on energy-invalid (amp = 0.01) rows — rescoped pending a
  higher-precision pass; GROW rows are 54 (not "2 outliers"),
  essentially all energy-invalid, Radau coverage partial; 135 RING
  rows carry lowest-FFT-bin frequencies (unmeasured periods — any
  frequency claim excludes freq < 2); the five BREATHER rows are all
  energy-invalid (not banked-quality).
- FRAME: W4's frame-mixing premise was a LABEL ARTIFACT (sign-flip
  label swap; everything ran consistently diagonal-frame). First
  genuine Class-B q* f-flow: NEVER SEALS from M1 weld data (f -> 2e4
  by t = 10) — first-class structural finding, scoped (M1, weld
  data, t <= 10).
- Box control NOT rescued untruncated (t1 -> t5 still 31-34%):
  scale autonomy remains unestablished; the seal treatment still
  owns the notes.

## Registry actions (appended this commit)

- #28 AMENDED (within the entry's CONDITIONS-CHANGED protocol): the
  q*-branch is now adjudicated at the w-row level (no pure angular
  well — the bands verdict survives there), but the COUPLED 2D mixed
  operator (w-row + the NEW f-row w_thth door + S_rtheta + dynamical
  delta-q) is open: bands-vs-lines is NOT settled at the coupled
  level. The truncation flag clears for the q = 0 class.
- NEW #29: the f = 2 kappa locus nulls (no trapping, no new states,
  no pinning) — premise-scoped (q = 0 diagonal class; frozen-f or
  4-mode slice back-reaction; Nu = 24 (+48 spot); ell <= 3
  backgrounds; subtracted-species coupled runs at probed kappa).
- ERRATA OF RECORD: the W4-B member-unit kappa convention; the W4
  "two kappa_c families" reconciliation; the W5 Arm-2 bare-D_alg
  coupled artifacts; Arm-1's pairing death (REVERSED) and its
  "f_max 6.8-33" locus numbers (true 14.1-58.4).

## Where this leaves the program (the W6 frame)

The locus hope died honestly; the discreteness gap did not move at
the w-row level — but the verifier chain converted W5's deaths into
the sharpest open object yet: THE COUPLED 2D BRANCH OPERATOR on the
q* class, carrying (i) the f-row w_thth door — the first derived
EL-visible entry of the phi-angular pairing (the hunch's species),
(ii) the mixed S_rtheta coupling, (iii) the Delta_w
elimination-breakdown surface, and (iv) the dynamical delta-q
channel. Bands-vs-lines — the angular discreteness question — now
lives exactly there. W6 = pose and solve that coupled operator
(uncover its exact structure first; then the solution-space sweep on
trust windows). The kappa question remains open alongside it (the
member-independent window invariant survives re-grading; its
convention-robust value ~2.12 awaits derivation; the -2/f provenance
is narrowed to one EH-specific number on the unimodular tie line).
