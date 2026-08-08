# MAP — observational constraints on the x_max SCALE (SNe + BAO, UDT-native ontology)

Date: 2026-08-07. Branch: grok. MODE: MAP ONLY — no compute, no data touched, nothing runs.
Charles's go ("Ok, let's map") with his binding ontology rule and his hypothesis, both recorded in
§0. This is the SCALE side of the structure/scale split (`udt_xmax_pair_question_MAP_2026-08-06.md`
is the STRUCTURE side; O1 pending there). Parallel lanes; sequencing = Charles's call (CP3).

## 0. Owner rulings and hypothesis (2026-08-07, recorded verbatim-intent)

- **ONTOLOGY RULE (binding for this lane):** "It's important that we not import any assumptions
  from LCDM of what BAO is. It's just observations we are matching with a completely different
  ontology." BAO enters as RAW OBSERVATIONS ONLY — a clustering feature in galaxy surveys at some
  characteristic angular/redshift separation. NO acoustic story, NO sound-horizon value, NO
  comoving-coordinate conversion, NO expansion-based processing.
- **OWNER HYPOTHESIS (tagged: direction, not evidence — hypothesis discipline applies):** "BAO
  could be exactly a manifestation of phi+orchestra, maybe even the deferred mu portion, with UDT
  giving structure between observation frames." Carried as the ORIGIN question (§3), strictly
  SEPARATED from the validator (§2): matching observations does not require an origin story;
  deriving one would be a later, separately-gated win. Verifiers aim hardest at anything that
  would confirm this hypothesis.

## 1. The goal, stated whole

Use SNe (existing data on disk) and BAO (new validator) to put honest, likely-loose constraints on
a RANGE of x_max — profile-conditional, stated as ranges-with-conditions, never one number. What
this buys beyond the number: through the dimensional lead x_max ~ G*M_total/c^2, an X range implies
an M_total range — the kernel's two posits (finite distance, finite mass-energy) getting their
first joint observational handle (translation labeled as riding the dimensional lead, not derived).

**The two levels (from the 08-07 discussion):**
- SHAPE: does the profile's redshift-distance relation match the data's shape? (SNe: already banked
  at chi2/dof=0.91 for the L-profile, conditional on P-opt. BAO would be an INDEPENDENT shape test
  — different physics, different systematics: candles vs a ruler.)
- SCALE: the absolute X. SNe alone float the magnitude offset (X degenerate with candle
  calibration); pinning X needs the EXTERNAL ANCHOR (the standard-candle absolute calibration —
  the "amount" that turns exchange rates into lengths, per the 08-07 c/G discussion). At low z, 2X
  plays the role of c/H0, so the answer lands at the few-Gpc order — arithmetic of the model form,
  NOT a result; a number exists only after a preregistered run.

## 2. The validator design (what would be BUILT; nothing here runs)

**V-SNe (mostly exists; rebuild clean):** the Pantheon+ machinery exists but its scripts were
archived with the retired shape-fit lane (`archive/xmax_history_root_2026-08-06/`). Path: a FRESH,
small, preregistered fit (the model is one line per profile) rather than resurrecting archived
code (F-LEGACY; a point-of-use re-grade of the archived script is the legal alternative if
preferred). Two modes: offset-free (shape only) and anchored (absolute X, with the anchor's
premise carried).

**V-BAO (genuinely new — and the ontology rule bites hard here):** the standard published "BAO
measurements" are heavily ΛCDM-processed: (a) redshifts are converted to distances using a
FIDUCIAL ΛCDM cosmology before correlation functions are computed; (b) "reconstruction" moves
galaxies using ΛCDM-gravity displacement fields; (c) quoted D_V/r_d values are fit with ΛCDM
templates and calibrated by the acoustic r_d. ALL THREE are forbidden imports here. The native
design: work in OBSERVABLE space — the feature as an angular separation theta_BAO(z) and a
redshift separation dz_BAO(z), per redshift bin, from the least-processed products available
(pre-reconstruction angular correlation measurements exist in the literature; which products are
clean enough is the M1 recon question). UDT side: a chosen profile (+X) plus ONE nuisance
parameter ell = the feature's native length, maps ell -> predicted theta_BAO(z), dz_BAO(z).
- SHAPE-ONLY use: the z-EVOLUTION of theta_BAO tests the profile with ell free (no calibration
  needed, no origin story needed).
- COMBINED use: with the SNe anchor, the same fits bound X (and incidentally measure ell in
  physical units — itself a new UDT-native datum).
- **P-STATIC-RULER premise (tagged):** "the feature has the SAME native length at every z." In a
  static universe this is the natural reading (nothing stretches it — arguably cleaner than the
  comoving-ruler premise ΛCDM needs), but it is a PREMISE, tagged and carried, not a fact.

**Combination deliverable:** the X-range table — per profile-class, per probe, per anchor-status —
plus the implied M_total range (labeled).

## 3. The ORIGIN question (Charles's hypothesis — separated, gated, NOT in the validator)

Could the BAO feature be native phi+orchestra structure — "UDT giving structure between observation
frames" — possibly touching the deferred mu channel? Recorded as an exploratory question X-BAO-ORIGIN
with honest notes: (a) any native derivation of a LENGTH faces the 08-07 exchange-rate fact — c and
G supply no amount, so a native ell must tie to an existing amount (x_max/M_total itself, or a
discreteness scale if one ever emerges from the mu seed); a derived ell/x_max RATIO would be the
natural dimensionless target. (b) mu is currently COUPLING-INERT and unquantized (banked); nothing
may be assumed from it. (c) This question is METRIC-LED only if posed as "what characteristic
scales does the orchestra put between observation frames?" — posed as "can the orchestra make BAO?"
it is TEMPLATE-LED and must be declared as such. GATE: separate MAP + Charles's go; nothing in this
lane depends on it; the validator treats ell as a free nuisance regardless of origin.

**SIBLING HYPOTHESIS X-CMB-ANISO (Charles, 2026-08-07, recorded verbatim-intent; direction, not
evidence; same quarantine):** "if you look at 'the effort-like sticks are supposed to diverge'
[the O3 rapidity-role rows: z/depth/d_L divergent at the wall for every profile] toss in some
angular sector modulation and you might end up with CMB anisotropies." Honest notes at recording:
(a) the machinery this lands on is exactly the DEFERRED mu/mixing channel (the clock->screen
angular channel entering lambda_t, tabled 08-06) — currently COUPLING-INERT and unquantized;
nothing may be assumed from it. (b) Banked kinematic-layer facts that BEAR on it, scoped: O1 Q3
found the mu-direction WALL-PROTECTIVE (mixing RAISES the lambda_t floor — i.e. angular data can
modulate how the divergence is approached per direction, the right SHAPE for direction-dependent
redshift), while the anti-hunch datum says PURE rotation composes additively (no modulation
without genuine mixing). (c) Any CMB contact must be built FORWARD — the old CMB anchor is canon
C-2026-08-06-2 (symbolic ln(T_emit/T_CMB), interpretation-conditional, from the ARCHIVED assembly
lane; standalone repair stands, lane does not). (d) METRIC-LED posing only: "what angular
structure does the orchestra put on the divergent rows near the wall?" — posed as "can the
orchestra make the CMB power spectrum?" it is TEMPLATE-LED and must be declared. GATE: separate
MAP + Charles's go; NOT in any validator; M2/M3 must not import it.

## 4. Premise ledger (data provenance grades — the anti-import gate for this lane)

- Pantheon+ light-curve magnitudes vs z (on disk, `Data/`) — NATIVE-OBSERVABLE.
- The candle absolute calibration (M_B / local ladder) — EXTERNAL-ANCHOR (its own premise chain:
  geometry + standard-candle physics; largely cosmology-model-independent but not zero; travels
  with any absolute X).
- The BAO feature's EXISTENCE at some (theta, dz)(z) — NATIVE-OBSERVABLE (a bump in a correlation
  function).
- "Same native length at all z" — PREMISE (P-STATIC-RULER, natural-in-static, tagged).
- The feature's ORIGIN — OPEN (owner hypothesis recorded §3; no origin needed for matching).
- FORBIDDEN-IMPORTS (F-IMPORT-LCDM): the acoustic/sound-horizon story; the r_d value; any
  comoving-coordinate or fiducial-cosmology conversion; ΛCDM template fits; reconstruction-based
  products. The M1 recon must audit each candidate dataset's processing chain against this list.
- The profile menu (§5 CP1) — CHOSE, fixed BEFORE any run (F-SHOP).
- x_max ~ G*M_total/c^2 — DIMENSIONAL LEAD (08-06, Charles-confirmed frame); used only to
  translate X-ranges into M_total-ranges, labeled.

## 5. Catch-points for Charles (cheap catches, the point of a MAP)

- **CP1 — the profile menu for the RANGE.** Ranges are profile-conditional, so the menu must be
  fixed up front. Proposed (each tagged CHOSE, you ratify/edit): the L-profile (the banked
  conditional lead); the H-profile ((X-r)/(X+r), the finite-proper alternative from the 08-05
  copresence probe); the exponential asymptote class. Alternative: wait for O2/O3 (the pair-lane
  measure table + approach classes) to supply a PRINCIPLED family first — cleaner, slower.
- **CP2 — the separation.** Validator-with-ell-as-nuisance now; origin question later and gated.
  Confirm that split matches your intent (your hypothesis is recorded, not smuggled into the build).
- **CP3 — sequencing vs O1.** Scale lane and structure lane are independent. Which first, or
  parallel? (M1, the data recon, is cheap and could run while O1 is pondered.)
- **CP4 — the anchor.** Absolute X requires accepting the candle calibration as the external
  amount. Without it: shape-only (still valuable — two independent shape tests). Acceptable?
- **CP5 — data acquisition.** Pantheon+ is on disk. Clean BAO products are NOT; M1 must find and
  fetch them (needs your OK for external data acquisition, and the processing-chain audit is the
  make-or-break of the whole BAO leg).

## 6. Work menu (bounded, gated per step on Charles's go; nothing runs from this map)

1. **M1 — data-provenance recon (cheap, read/lit only):** inventory candidate BAO products by
   processing level against the forbidden-import list; report which (if any) are clean enough,
   with the exact contamination each carries. Also: confirm Pantheon+ disk state.
2. **M2 — validator build (preregistered):** V-SNe fresh fit + V-BAO observable-space matcher;
   frozen profile menu; falsifiers wired (F-IMPORT-LCDM, F-SHOP, F-ANCHOR, F-SCOPE, F-STEER).
3. **M3 — runs:** shape tests; anchored X-ranges per profile; the range table.
4. **M4 — the M_total translation + a consilience note (labeled as riding the dimensional lead).**
X-BAO-ORIGIN (§3) is NOT on this menu; it gets its own map only on your explicit go.

**CANDIDATE FUTURE STEPS (recorded 2026-08-07 on Charles's in-run reflections; direction, not
evidence; each gated on its own go; NOTHING here touches the frozen M3 run 523f4aca):**

- **M3-AUDIT — per-shell selection-function forensics (if outliers survive tonight's weight-variant
  comparison).** Charles's framing (binding for this step): investigate what DESI did to NORMALIZE
  the data (mask, fiber-assignment/collision gaps, target-selection transitions, imaging-weight
  maps) — the SURVEY's own layers — as the outlier suspects, NOT a physics mechanism. This is
  "mismatch -> solver" applied to a third party's pipeline: the outlier's provenance is a
  selection/systematics question first. Concrete open lead already visible: the 8.8-deg LRG
  outlier sits at z 0.95-1.00, at the sample's selection-edge thinning — a shell-boundary x
  selection-transition interaction is a known broad-power mimic. STILL LCDM-free (DESI's
  normalization != LCDM model assumptions; F-IMPORT-LCDM intact). Preregistered if run.

- **M3b — additional pre-recon surveys averaged/cross-checked in (Charles: "BAO surveys are all over
  the place; average in a few more").** M1 already graded the shelf: BOSS DR12 pre-recon (~5 GiB,
  clean-enough) = the natural DECORRELATED cross-check (different telescope/target/imaging =>
  systematics independent of DESI; an independent ~2.3-deg thread at overlapping z would outweigh
  more DESI statistics; its absence = a systematics verdict). eBOSS usable with care (mixed
  _rec/raw directory trap). Published theta_BAO compilations = cross-check-only (small fiducial
  corrections). NOT averaged into 523f4aca (frozen); a separate preregistered leg after the
  current verdict.

- **NEW ANCHOR CANDIDATES beyond SNe/BAO/CMB (Charles's 10-month go-to trio; asked for peers/
  betters). Shortlist, graded:**
  - **Standard sirens (GW) — the cleanest anchor available.** Absolute distance from waveform
    physics ALONE (no ladder, no light-curve standardization, no BBC bias layer) + host-galaxy
    redshift => pristine d(z) points. Few events, growing. BONUS native test: GW170817 bounds
    |c_GW - c_light|/c < ~1e-15 — a sharp consistency test for how c_eff treats the tensor vs
    optical sectors (metric-led: "does the orchestra force the two speeds equal?").
  - **Alcock-Paczynski ratio — anchor-FREE, and possibly already in hand.** theta / Delta z at the
    SAME z cancels the ruler length entirely => pure-shape, no external calibration; the radial
    trichotomy (grow/constant/decay) survives the division. Our transverse+radial BAO legs already
    compute both halves; if the radial leg gets traction this is ruler-free profile discrimination
    for free — arguably the purest observable in the program. Elevate at M4/M3b if radial survives.
  - **Time-delay lensed quasars — geometric absolute distances** (measured delays + lens model);
    moderate cleanliness (lens-model premise); a third-party check on the candle anchor.
  - **Standing cheap consistency notes (banked mentally, no discrimination but no vulnerability):**
    UDT passes the Tolman surface-brightness (1+z)^-4 test automatically (forced by the banked
    d_L/d_A, zero freedom); SNe light-curve time-stretching is native (clock ratio IS 1+z) — a
    test some static-universe models fail and UDT passes by construction. (These are NOT anchors;
    they are non-vulnerabilities worth knowing when the picture is challenged.)
  - JWST angular sizes already parked as V-ANGSIZE above.

**CANDIDATE FUTURE LEG (recorded 2026-08-07 on Charles's question "would higher-z JWST data
help?"; NOT on the M2/M3 menu — F-SHOP; own MAP + go required): V-ANGSIZE, the JWST angular-size
floor test.** Rides the banked O2/O3 cell d_A = r -> R_w FINITE at the wall (class i): objects of
fixed proper size STOP SHRINKING on the sky as z grows (floor angle ~ size/R_w), monotone
theta(z) decline to a floor — qualitatively distinct from LCDM's d_A turnover. JWST high-z
angular sizes are the natural probe; the honest blocker is the RULER premise (galaxy intrinsic
size evolution is a severe systematic; would need its own tagged premise, the sibling rigor of
P-STATIC-RULER). Blending sparse JWST high-z SNe into V-SNe was considered and declined (tiny N,
contaminated standardization layer, mid-stream freeze violation; DESI QSO shells already carry
the high-z shape discrimination). Direction, not evidence; nothing in M2/M3 depends on this.

## 7. Falsifiers

- **F-IMPORT-LCDM (primary):** any acoustic/r_d/comoving/fiducial/template/reconstruction leakage
  — fires per dataset; a leg riding a contaminated product is void unless the contamination is
  quantified and shown negligible for the shape being used.
- **F-SHOP:** the profile menu is frozen pre-run; no post-hoc additions; ranges reported for the
  whole menu including failures.
- **F-STEER:** the owner hypothesis (BAO = orchestra/mu) is recorded direction; the validator must
  be origin-agnostic by construction; any design choice that only makes sense under the hypothesis
  fires.
- **F-ANCHOR:** every absolute number carries the anchor premise visibly.
- **F-SCOPE:** deliverables are profile-conditional RANGES with conditions attached; no single
  "the value of x_max"; no mass claim beyond the labeled M_total translation.

## CP RULINGS (Charles, 2026-08-07)

- **CP1 = the cleaner/slower way:** the profile menu comes from the pair lane's O2/O3 (the measure
  table + approach classes), NOT declared ad hoc. CONSEQUENCE: the structure lane (O1 -> O2 -> O3)
  is now the CRITICAL PATH for this lane's fitting steps (M2/M3 wait on it). Only M1 (data recon)
  is independent.
- **CP2 = YES:** the validator/origin split stands; the validator is origin-agnostic (ell free);
  X-BAO-ORIGIN stays separately gated.
- **CP3:** resolved by CP1's ruling (structure lane first; M1 in parallel). [Charles asked for a
  lay explanation — given in-session.]
- **CP4 = YES:** the candle absolute calibration is accepted as the external anchor (its premise
  chain travels with every absolute number).
- **CP5 = YES:** data acquisition authorized; astroquery permitted; disk budget ~100 GiB; DESI DR1
  already on disk at `/media/udt-admin/ScratchDisk/Data/desi_dr1`. M1 is GO: inventory-first
  (the on-disk DESI DR1, then the wider product landscape), audit processing chains against the
  forbidden-import list; NO bulk downloads at recon stage (metadata/small catalogs only).

**CP5 AMENDMENT (Charles, 2026-08-07):** disk budget raised to ~500 GiB IF NECESSARY, using the
scratch disk (`/media/udt-admin/ScratchDisk`, 3.4 TB free) as the storage location for acquired data.

## M1 COMPLETE (2026-08-07): BAO leg VIABLE-NATIVELY (recon report; single-agent, spot-verify at M2)

`udt_xmax_scale_observational_M1_recon_2026-08-07/RECON_REPORT.md`. On-disk DESI DR1 (30 GiB) =
PRE-reconstruction LSS catalogs, 9.75M galaxies, continuous z 0.01-3.5 (BGS/LRG/ELG/QSO). Audit for
angular correlations in thin z-shells: RA/DEC/Z + completeness/zfail/imaging weights = CLEAN
(cosmology-free; WEIGHT_SYS over-correction caveat -> run with/without); NX + WEIGHT_FKP =
CONTAMINATED-AVOIDABLE (fiducial-LCDM columns -- simply never read them; native dN/dz replacement);
the FATAL layers (reconstruction, templates, r_d, fiducial distance conversion) are ABSENT from
these files. Landscape: BOSS DR12 pre-recon (~5 GiB) as optional cross-check; eBOSS mixed-directory
hazard (explicit non-rec file choice required); the published theta_BAO literature series carries a
small fiducial projection correction (0.28-1.44%, removable) -> cross-check grade only; published
D/r_d tables + Ly-alpha = use for nothing. Honest risk named: thin-shell S/N (DR1 may give a
low-significance feature per shell -- an honest outcome, not contamination). Pantheon+ confirmed on
disk (1701 rows + full cov).

**NEW CATCH FOR THE SNe LEG (flagged for M2's prereg, and a caveat on the banked 0.91):** the
Pantheon+ ledger shows `zHD` carries peculiar-velocity/flow-model corrections (raw zCMB/zHEL
available) and **`m_b_corr` carries fiducial-cosmology BBC bias corrections** — i.e. the standard
magnitude column itself has a LCDM-adjacent processing layer. M2's V-SNe prereg must choose columns
deliberately (raw-er columns vs corrected, with the contamination quantified) and the banked
0.91's column choice gets a point-of-use note. Recon findings are single-agent: spot-verify the
load-bearing ones at M2 prereg time.

## M2 COMPLETE (2026-08-07): M2-BUILT — both validators built, synthetic-gated, blind-verified

`udt_xmax_scale_observational_M2_build_2026-08-07/` (prereg f9a64ecf committed BEFORE the build).
D1: exact native predictions, 52/52 sympy checks (n=1 reproduces banked z(z+2)); load-bearing
low-z degeneracy derived (all profiles collapse to one X_eff at leading order; menu separates at
second order with disjoint c2 ranges; fitters parametrized (X_eff, 1/shape) accordingly); radial
Dz_BAO trichotomy derived (P1 grows/P2 constant/P3 decays — a clean M3 discriminator if S/N
permits). D2 V-SNe: 4 frozen modes, full-cov chi2, injection-recovery gate PASS (27/27 + coverage;
the gate CAUGHT and fixed an interval-collapse bug — Category-A, disclosed); M1's column claims
verified on-file; M2_GUARD blocks real fits (pytest-proven). D3 V-BAO: blacklist machine-wired
(NX/WEIGHT_FKP/_rec unreadable), frozen shells/bins, LS + jackknife, model-free bump machinery
(full-window search, null-mock trials calibration), end-to-end mock recovers planted theta(z) and
joint (ell/X_eff) at truth n=1.6; M1 spot-verify all claims hold. BLIND VERIFIER (fresh context):
CLEAN-AMENDED — re-ran everything byte-identical; live purity attacks held; 2/3 mutation probes
caught, the miss (weight-drop invisibility) closed by a new catch-proven test; all amendments
applied (A1-A7; incl. smoke-output redaction restoring the F-PEEK letter). F-PEEK CLEAN: no
real-data verdict number exists anywhere in the package. **M2 is a TOOLING milestone, not a
physics result — nothing about the sky is claimed.**

**M3 GATE ITEMS (for Charles, owed at M3 prereg):** (1) shell-floor interpretation — per-cap as
built (drops all ELG/QSO SGC shells) vs cap-combined pair counts with a per-tracer floor (option
now BUILT, default OFF; driver recommendation = combine); (2) randoms depth — Charles ruled
FOUR-file; (3) cross-shell look-elsewhere machinery MUST be wired in the M3 prereg before
any significance claim (verifier A4); (4) radial leg = attempt-only (S/N risk); (5) the
diagonal-jackknife-covariance caveat conditions M3 significances (self-consistent for M2 only).

## M3 COMPLETE (2026-08-08): M3-RANGES(SNe) + detection(BAO) — verified LEADS (blind pass in)

`udt_xmax_scale_observational_M3_runs_2026-08-07/` (prereg 523f4aca; RESULTS_VERIFIER_REPORT.md:
SNe SUSTAINED, BAO SUSTAINED, audit-amendment SUSTAINED; every number reproduced bit-identically;
four-check complete; same-session verifier — external bar travels). HEADLINES:
- **V-SNe:** P1 (finite-radius power-law wall) fits (chi2/dof 0.92); P2/P3 (infinite-radius
  walls) fail structurally (chi2/dof ~3.2) — the data separate the O2/O3 classes. n ~ 1.056
  with **n=1 (P-opt/L) excluded at 2.82 sigma** (zCMB primary; the zHD flow-corrected column
  STRENGTHENS to 3.89 sigma — direction verifier-corrected). Anchored: X_eff = 2086 [2059,
  2113] Mpc; R_w ~ 2.2 Gpc (F-ANCHOR premise travels). BBC-contamination on shape = 0.0044
  (quarter of the interval half-width) — the point-of-use number on the banked 0.91.
- **V-BAO:** the frozen detection criterion MET both weight variants (global trials-corrected
  p < 1/300 vs 0.01) — a coherent angular feature in the raw catalogs, zero LCDM anywhere;
  the strong cluster (LRG 0.70-1.10, QSO 0.95-1.25, mostly 2.3-2.4 deg) weight-variant stable
  to ~1%. HONEST LIMITS: joint single-ruler parametrization variant-unstable -> NO BAO-alone
  X-range; thread magnitudes near the SNe-fitted curve (ell ~ 70 Mpc-scale) BUT drift
  direction opposite the predicted fall (~1-1.5 bins) — not over-read; outliers (worst 3.8x)
  -> M3-AUDIT/M3b. Radial estimator UNBUILT (triggers: 9 sys / 8 nosys) — OWED.
NEXT GATES on Charles: M4 (M_total translation); M3-AUDIT; M3b (BOSS); the radial build (the
AP-ratio prize). No banked negative registry changes; all leads same-session-verified only.

**GPU AMENDMENT (2026-08-07, Charles's ruling "refactor for GPU + four-file"): applied, verified,
honest outcome recorded.** Exact float64 GPU pair-count backend built (bin-identical to CPU;
equivalence test proven non-vacuous — catches ONE misbinned pair; float32 and weight-drop
mutations catch-proven; all gates re-pass on GPU). MEASURED HONESTY: for the 4-file run the GPU
brute path is ~3.8x SLOWER than the CPU tree (165.6 GPU-hr vs 43.5 CPU-hr, DR-once convention;
the tree touches only ~4% in-window pairs, brute touches all) — GPU kept as the independent
cross-check backend (different algorithm, same counts = a soundness bonus), CPU tree = the M3
workhorse. PROPOSED M3 SHAPE (needs prereg + Charles): 4 random files with SPLIT-AVERAGED RR
(per-file RR averaged, no cross-file pairs — linear not quadratic cost, ~13 CPU-hr total; a
standard estimator convention, frozen explicitly, never slipped in); GPU spot-check on a shell
subset; look-elsewhere wired; radial attempt-only; cap-combine per Charles's ruling. Focused
verifier pass: CLEAN-AMENDED; provenance nits B1/B2/B3 closed (all shipped numbers regenerable
by shipped code).
