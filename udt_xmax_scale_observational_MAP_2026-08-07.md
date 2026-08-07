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
