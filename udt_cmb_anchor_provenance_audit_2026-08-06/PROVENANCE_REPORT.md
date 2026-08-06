# CMB anchor Δφ = ln(1101) — provenance audit

Date: 2026-08-06. Auditor: provenance recon agent (read-only; no canon/registry edit; no
compute beyond arithmetic checks). Target: **canon C-2026-07-02-1** and specifically the
VALUE Δφ = ln(1101). Charles-directed 2026-08-06 under the binding 2026-07-30 rule (canon
ratified-proposals are working premises; track origination; provenance-audit before ruling
atop a blocking one). House template: `udt_mirror_canon_provenance_audit_2026-07-30/`
(PROVENANCE_REPORT structure imitated). This audit is documentary only: every claim cites
the banked file; nothing is re-derived here.

---

## 1. The canon record, exact

### 1.1 C-2026-07-02-1 (CANON.md:235-253) — what it canonized

CANON.md:237-244, verbatim (emphasis in original):

> **Statement:** The finite-cell canon C-2026-06-10-2's wording "the universe is a finite cell
> ([0, r_CMB], phi: 0 -> ln(1101) at the CMB boundary)" is CLARIFIED (not retracted): the
> physical content is the DIFFERENCE Δφ = φ(CMB fold) − φ(core) = ln(1101) (1+z = e^Δφ). The
> blind-verified fold derivation (universe_cell_fold_jc_sigma_results.md: the odd fold φ→−φ pins
> φ = 0 AT the CMB fold) fixes the canonical convention: **φ(CMB fold) = 0, interior running
> φ: −ln(1101) → 0.**

**The entry canonizes BOTH:** (i) the FORM (the anchor is a Δφ statement; the zero sits at
the CMB fold — this is the blind-verified, derived part), AND (ii) the VALUE — ln(1101)
appears twice inside the canonical statement itself ("= ln(1101) (1+z = e^Δφ)";
"interior running φ: −ln(1101) → 0"). The value is not quarantined outside the statement.

The provenance section (CANON.md:249-252) cites ONLY the fold-JC derivation + blind
verification (agents a15ecc62590d15bd4 / a18115fe9d95cfb84) and "operated as Δφ by Charles
from the T2 ruling onward". **It contains no trace of where ln(1101) itself comes from.**

### 1.2 What was surfaced to Charles at canonization time (2026-07-02)

The 07-02 work surfaced the CONVENTION question, not the value's provenance.
`universe_cell_fold_jc_sigma_results.md:42-46`:

> **Anchor bookkeeping:** Δφ = −φ_c ⇒ **φ_c = −ln(1101)**. ...
> **CANON-GAUGE FLAG (Charles to adjudicate):** canon C-2026-06-10-2 words the cell as
> φ: 0 → ln(1101); the fold pins the zero AT the CMB fold ⇒ interior runs −ln(1101) → 0. In
> Branch P the shift is PHYSICAL (e^{−2φ} source) — the canon phrasing must be re-read as a Δφ
> statement or the two conflict.

And the premise table, `:107`: "φ_c = −ln(1101) | DERIVED from anchor + fold pin;
CANON-GAUGE FLAG raised". I.e. the VALUE entered the 07-02 derivation as "the anchor" — an
INPUT taken from canon C-2026-06-10-2 wording — and only the zero-location (gauge) question
was flagged for adjudication. **No 07-02 document (fold-JC results, the ladder-arc LIVE
snapshot `archive/LIVE_universe_cell_ladder_arc_2026-07-02.md`, `relay_claudeai_2026-07-02.md`)
traces ln(1101) to its empirical source or tags it as an interpretation-conditional import.**
The value's provenance was NOT surfaced at canonization; it rode through inside quoted canon
wording. (Same pattern as the mirror-clause finding of the 2026-07-30 audit: a clause
ratified in compound without separate surfacing.)

---

## 2. Origination trace (earliest record)

### 2.1 The value pre-exists this repo: legacy D1 closure, 2026-03-07

Earliest in-repo appearance: the initial snapshot commit `691e04a3` (2026-06-10) already
carries it in BOTH legacy corpus docs (verified via `git grep "1101" 691e04a3`):

- `udt_canonical_geometry.md` §10.6 (lines 1467-1500), headed "**D1 Algebraic Closure ...
  Status: CLOSED (2026-03-07) — algebraic, no free parameters.**" The originating passage,
  `udt_canonical_geometry.md:1469-1477` verbatim:

  > **(A) Redshift definition** (from §1.3):
  > $$1 + z = e^{\Delta\phi} \implies \Delta\phi = \ln(1 + z_{\mathrm{CMB}})$$
  > where $z_\mathrm{CMB} = T_\text{starlight}/T_\mathrm{CMB} - 1$ from two direct
  > observations: $T_\mathrm{CMB} = 2.725$ K (microwave background monopole) and
  > $T_\text{starlight} \approx 3000$ K (recombination surface temperature). No ΛCDM input —
  > just two thermometers.
  > At $z_{\mathrm{CMB}} \approx 1100$:
  > $$\Delta\phi = \ln(1101) = 7.003974$$

- `archive/udt_validated_results.md:987-996` records the same "D1 algebraic closure chain
  (2026-03-07)", step 1 verbatim: "CMB redshift: $z_\mathrm{CMB} = T_\text{starlight}/
  T_\mathrm{CMB} - 1 \approx 1100$ (two observed temperatures) $\implies \Delta\phi =
  \ln(1101) = 7.003974$".

- The D1-item ledger, `archive/udt_validated_results.md:1317`: "D1 | **Cosmological Δφ
  boundary condition** | **CLOSED (ALGEBRAIC, 2026-03-07).**"

So the value FIRST entered the record in the LEGACY pre-handover corpus on 2026-03-07 (D1
closure), months before this repo existed. It entered THIS repo verbatim in the initial
snapshot (2026-06-10) and entered CANON the same day inside the finite-cell canon wording.

### 2.2 The chain into canon

1. **Legacy D1 closure (2026-03-07)** — CG §10.6, quoted above. AI-era session work.
2. **Fork doc (2026-06-10)** — `grok/quarantine_free_DA/macro_sector_fork_resolution.md:71-72`
   quotes the legacy value as established fact: "The macro phi grows monotonically from
   phi(0)=0 to phi(r_CMB) = ln(1101) = 7.003974 at r_CMB = 9.164 Gpc — and the domain ENDS
   there." (An AI recon/synthesis doc; the same doc whose canonization recommendation
   produced C-2026-06-10-2 — see the 2026-07-30 mirror audit §1.1.)
3. **C-2026-06-10-2 (canonized 2026-06-10)** — CANON.md:30-31: "The universe is a finite
   cell ([0, r_CMB], phi: 0 -> ln(1101) at the CMB boundary)". The value is inside the
   ratified compound wording; no separate surfacing of its provenance on record.
4. **C-2026-07-02-1 (canonized 2026-07-02)** — clarifies the FORM (Δφ, zero at fold),
   restates the VALUE (§1.1-1.2 above); provenance section silent on the value's source.

### 2.3 WHO originated it

**AI-ASSEMBLED FROM OWNER-SUPPLIED THERMOMETERS.** Split precisely:

- **Owner-originated (Charles):** (a) the INPUT LIST — Theory Rule 5 is a Charles-authored
  founding rule (`archive/udt_validated_results.md:27904`): "UDT is STATIC. ... Lab inputs
  only: {m_proton, c, G, ℏ} + direct observations {T_CMB, T_starlight}" — T_CMB and
  T_starlight are Charles's own named observational inputs; (b) the CMB ONTOLOGY —
  PROVENANCE.md:61-62: "**The CMB-as-thermalized-starlight (recycling) ontology** of the
  macro work traces to Prompt 1 verbatim" (founding Grok prompts, 2025-08-12).
- **AI-originated (legacy sessions):** the FORMULA z_CMB = T_starlight/T_CMB − 1, the
  specific value T_starlight ≈ 3000 K with its "recombination surface temperature" label
  (CG:19 input table), the rounding to z = 1100, and the assembled anchor Δφ = ln(1101) =
  7.003974 (the 2026-03-07 D1 closure). The founding prompts contain NO temperature value
  and no 1100/1101 (grep of PROVENANCE.md: no hit for 1100/1101/3000).
- **Ratification:** the value entered canon inside two Charles-ratified compounds
  (C-2026-06-10-2, C-2026-07-02-1), in both cases without its empirical provenance being
  separately surfaced (§1.2, §2.2). This is exactly the class Charles named on 2026-07-30:
  an OWNER-RATIFIED-PROPOSAL riding owner-supplied raw inputs.

### 2.4 In-record self-audit trail (the legacy corpus already flagged the edges)

The legacy record itself audited this number more than once — relevant to grading:

- `archive/udt_validated_results.md:27892` (S53 G-F-4 verification): "z_CMB = 1100 IS
  canonically derived via the algebraic identity z = T_starlight/T_CMB − 1 = **1099.92** at
  CG §1.3 / §10.6 ... The §230/§231/§236/S53-001 NEGATIVE chain's empirical inheritance is
  **at the BAO-anchor / mass→length-route ... layer specifically**, not at the z_CMB layer."
- `archive/udt_validated_results.md:6705-6712` (Session 29): T_*/T_CMB = 3000/2.725 =
  1100.917 vs canonical z=1100 exactly — a logged ppm-level discrepancy, plus the standing
  annotation that reproducing r_CMB from φ(r_CMB)=ln(1101) is a "**2BO-compatibility
  consistency check**, NOT an independent prediction" (the identity defines r_CMB).
- `archive/udt_validated_results.md:6925`: "φ(r_CMB) = ln(1101) reproduction |
  **CONSISTENCY-CHECK** (inversion of defining identity)".
- The D1 closure's leg (B) (Misner-Sharp + Machian c²=2GM/r_*, CG:1479-1493) is a
  CONSISTENCY companion, not an independent derivation of the value — and its r_* = 9.164
  Gpc "inherits from BAO-constrained parameters" per the S53 audit
  (`archive/udt_validated_results.md:27896`). The Δφ VALUE rides leg (A) (the temperature
  ratio) alone.

**Arithmetic checks (this audit's only compute):** 3000/2.725 − 1 = 1099.917;
ln(1101) = 7.003974 ✓; ln(1100.917) = 7.003898 (Δ ≈ 1×10⁻⁵ relative); ΛCDM's fitted
z_* ≈ 1089-1090 would give ln(1091) ≈ 6.9949 — ~0.13% below the canon value. So the canon
number is NOT the Planck fit; it is the rounded two-thermometer ratio.

---

## 3. What the number assumes — 1101 = 1 + z_CMB decomposed at source

The record does NOT derive z ≈ 1100 natively; it assembles it from the two-thermometer
identity (§2.1). Ingredient tags:

### (a) "The CMB is light emitted at a ~3000 K surface" (the interpretation) —
**LEGACY-INTERPRETATION-IMPORT**

The identification of T_starlight with a "recombination surface temperature" (CG:19,
CG:1471; `archive/udt_validated_results.md:6697` "recombination/starlight") imports the
standard last-scattering reading of the CMB. Charles's founding recycling ontology
(CMB-as-thermalized-starlight, Prompt 1 — owner-NATIVE as an ontology) does NOT supply the
3000 K value; the number is taken from the recombination picture in every banked appearance.
The CG input table's label "Direct observation" (CG:19) is an overclaim at source: the
emission-surface temperature is inferred through the interpretation, not directly observed
(what is directly observed is T_CMB = 2.725 K, tag NATIVE-COMPATIBLE direct datum).

### (b) T_emit ≈ 3000 K (Saha/atomic physics) — **SHARED-PHYSICS, conditional on (a)**

Given (a), the ~3000 K figure is hydrogen-ionization/Saha physics — atomic, largely
model-independent, not a ΛCDM fit. But it load-bears ONLY through (a): without the
emission-surface interpretation there is no in-record derivation of any T_emit.

### (c) The temperature-ratio redshift applied in UDT's STATIC frame — **NATIVE**

This leg the record DOES justify natively; it does not silently carry the expansion-era
mapping: (i) the redshift law 1+z = e^{Δφ} is metric-derived (CG §1.3:118 "Redshift
(between points): 1+z = e^{φ(r₂)−φ(r₁)}"); (ii) the blackbody-to-blackbody temperature
scaling is derived in-frame — CG:1671: "Local matter-emitted Planck at T_proper = T₀e^φ
redshifts (Gate S1 / §1.6.2 Tolman) to the observed CMB blackbody at T₀"; CG:1700 "Tolman
T_obs = T_proper e^{−φ}"; CG:2075 (the −3 Tolman scalar-transport weight). So
T_emit/T_obs = 1+z is a native static-dilation Tolman relation here, with the semiclassical
Planck-spectrum route derived at CG:1666-1671 (blackbody itself remains a Theory-Rule-5
observational input, CG:1520 — honest in-record).

### (d) Planck/ΛCDM-fitted numbers — **NOT USED**

z = 1100 is the rounded two-thermometer ratio (1099.92 → 1100; §2.4), not the ΛCDM-fitted
z_* ≈ 1090 (~1% away). The in-record S53 audit explicitly localizes the legacy corpus's
empirical inheritance at the BAO/length-anchor layer, NOT the z_CMB layer
(`archive/udt_validated_results.md:27892`). Residual CHOSE flags: the rounding
1099.92 → 1100 → "1101 exactly" (ppm-level, logged in-record at :6705-6712), and the
choice T_starlight := 3000 K exactly.

**Net:** the VALUE ln(1101) = [NATIVE redshift/Tolman machinery] applied to [an imported
emission-surface interpretation (a)] carrying [shared atomic physics (b)]. The load-bearing
import is (a) alone. No Planck/ΛCDM fit rides it.

---

## 4. The consumer map

Sweep by a dedicated recon agent (grep "1101" + ~15-line context per hit, all known
mentioning files + SNe/Pantheon check). Operational test for VALUE-RIDING: would changing
z_CMB / ln(1101) change the banked numbers or conclusions?

### 4.1 VALUE-RIDING (7) — banked numeric tables shot to carry Δφ = ln(1101)

| file | load-bearing loci | what rides |
|---|---|---|
| universe_cell_T3_closure_results.md | :17, R3 roots ~:39-50 | shoots from φ_c=−ln(1101); banked roots a*, q, ρ_s, r_s scale with the value |
| cascade_stageB_results.md | :31 + B2 table | per-rung q/L/ρ_s table computed carrying Δφ=ln(1101) |
| ladder_theorems_AB_C_results.md | :17, :40, :42 | q=Z·Δφ·B⁻¹, slope ln(1101)/B, amplifier √1101≈33.2, F2 numeric test |
| microphysics_E0_ambient_tables.md | :32,:49,:65,:82,:98,:117,:133 | ambient tables banked at φ_c=−7.00397 |
| microphysics_E1_composite_closure_results.md | :184, :265 | plateau (φ,ρ,U)≈(−7.004,1,2) banked; bracket selected via the anchor |
| stageD_sweep_results_raw.md | :72, :115 | 20-rung sweep computed at the φ_c=−ln(1101) pin |
| stageD_frozen_forecast.md | :18, :78 | x_c=1/1101 banked anchor drives the forecast table |

All 7 are constructive interior-cell/cascade solver outputs (the 07-02→07-04 ladder arc):
their NUMBERS move if the value moves; their structural theorems (existence, budget
identities, amplifier LAW e^{Δφ/2}) are form-level and survive re-anchoring.

### 4.2 FORM-ONLY (10)

universe_cell_fold_jc_sigma_results.md (:42,:45,:107 — JC/budget identities
value-independent; the value is anchor bookkeeping only); cascade_characterization_miniMAP;
ladder_lemmaD_sealing_amplitude_results (:36 — the anchor CANCELS from a_seal; x_c=1/1101
gives <0.2% corrections); F7_scale_bridge_native_results (:193,:217,:220 — proves the
dimensionless 7.004 cannot pin a length); native_readout_map_depth_size_results (:38,:129 —
φ_c kept FREE, "OUT OF SCOPE, not imported"); flux_sealed_universe_cell_miniMAP;
stability_filter_miniMAP (:26 — primary index anchor-free); simple_metric_cascade_C2_C5_J1
(:149,:170 "not 1101 inside derivation"); simple_metric_mass_xmax_cascade (:186,:230);
microphysics_reentry_omega_reframe_MAP (:204 — the anchor "cancels out of it").

### 4.3 SIGN-ONLY (1)

universe_cell_vacuum_impossibility_results.md (:111 — no gradient between two φ'=0
mirrors; holds for any Δφ > 0).

### 4.4 QUOTE-ONLY (6)

derived_background_and_phi_coupling_DESIGN (:4,:55,:90-91 — data-blind spec that FORBIDS
grabbing 1101); macro_universe_native_MAP (:38,:63 "Do NOT fit 1101/7.004");
ponder_emergence_directions_2026-07-04 (:48); simple_metric_pantheon_xmax_fit_results
(:53,:158 — 1101 listed "Not free", z=1100 only a downstream x/X≈0.999998 sanity check);
udt_p4_seam_closure_derivation_2026-07-30/EXACT_DERIVATION.md (:29 — asserts ln(1101) does
NOT appear) + VERIFIER_REPORT.md (:51 — forbidden-content grep).

**SNe/WR-L/macro:** the Pantheon x_max fit does NOT ride the value (held fixed as "Not
free", never a fit input; only a downstream kinematic check). No SNe/Pantheon results file
uses z_CMB=1100 as a numeric fit input. The WR-L macro arc rides C-2026-07-09-1, not this
anchor.

### 4.5 ALREADY-RESCOPED (10) — the 2026-08-06 stamps, CONFIRMED

- `udt_global_cell_assembly_MAP_2026-08-06.md:127-135` — "ANCHOR RE-SCOPE (2026-08-06,
  Charles-directed)": datum = "some Delta phi > 0"; "The value ln(1101) is a SEPARATE
  flagged premise riding the standard CMB last-scattering interpretation (legacy import
  ...). No row verdict depends on the value; only quantitative witnesses do."
- `udt_global_cell_assembly_step2_2026-08-06/` (PREREGISTRATION :11; DERIVATION_NOTES
  :262-264 — IVT existence holds for any Δφ>0, the 1101-specific threshold flagged
  value-conditional; both ADVERSARIAL_REVIEWs — sign-argument level, LEAD/UNBANKED).
- `udt_two_mirror_rigidity_regrade_2026-08-06/` (REGRADE_REPORT :141-146 — explicit
  re-scope: datum → "some Δφ>0", the value "load-bearing NOWHERE"; both reviews concur).
- `NEGATIVES_REGISTRY.md:176,:862` — "value-independent ... specific ln(1101) a separate
  flagged premise; 7.004 FREE".

### Tally

**VALUE-RIDING: 7** (all in the 07-02→07-04 interior-cell/cascade ladder arc) |
FORM-ONLY: 10 | SIGN-ONLY: 1 | QUOTE-ONLY: 6 | ALREADY-RESCOPED: 10. Every
impossibility/existence/amplifier CONCLUSION on record is value-independent; the exposure
is confined to banked numeric TABLES (roots, rungs, ambients, forecasts) that would need
re-shooting (or an anchor-parameterized re-statement) under any value change.

---

## 5. Rewording options for Charles (proposed, NOT ruled; house precedents:
C-2026-07-30-1 split reading, C-2026-08-06-1 chart-scoped rewording)

### Option (i) — SPLIT-AND-KEEP (mirror-audit precedent)

Keep the Δφ FORM + fold-zero convention as canon (the blind-verified, derived part of
C-2026-07-02-1 — untouched). DEMOTE the VALUE ln(1101) to a flagged working number:
**INTERPRETATION-CONDITIONAL (rides import (a), the ~3000 K emission-surface reading;
temperature-ratio machinery itself native per §3c; no Planck/ΛCDM fit)**. The tag travels
to every VALUE-RIDING consumer.
**Consumer impact:** nothing FALLS — the value is an anchor DATUM, not a derived theorem;
FORM/SIGN consumers unchanged; VALUE-RIDING results gain a conditionality stamp and stand.
Cheapest option; matches what the 2026-08-06 assembly-MAP re-scope already did locally.

### Option (ii) — VALUE-OPEN rewording

Replace the value inside the canon statement with: "Δφ_cell > 0, value open. Candidate
anchors: CMB-interpretation ln(1101) ≈ 7.004 (conditional on the emission-surface reading);
a T_starlight-based native anchor; other native anchor TBD." This matches Charles's current
working-anchor list (C-2026-07-30-1 owner clarifications: m_proton, ħ, T_CMB or
T_starlight) and the recycling ontology's owner-native standing (Prompt 1).
**Consumer impact:** stronger than (i): every quantitative witness that used 7.004 (E0/E1
ambient tables, cascade √1101 amplitude laws, assembly Step-2 existence witness ε*, any SNe
cross-tie) becomes anchor-parameterized (results re-stated as functions of Δφ); sign/form
results untouched; assembly Step 3 must treat the SNe L-lead as the primary native datum
(the MAP already orders this). More re-stating work than (i), buys a clean native frontier.

### Option (iii) — DERIVE-THE-ANCHOR lane (the option-(d) analog)

Keep the value as a working premise (per (i)) AND authorize a named derivation push: derive
the emission temperature natively from Charles's own recycling ontology (CMB-as-thermalized-
starlight, Prompt 1) — does the UDT medium/thermalization sector pin ~3000 K (or another
T_emit) without the recombination import? The native Tolman machinery (§3c) is already in
place; the ONLY missing native leg is T_emit. Success converts the import into a
derivation; failure leaves (i)'s tag honest.
**Consumer impact:** none immediate; sets the closure site.

### Option (iv) — sub-variant of (i)/(ii): un-round to the symbolic ratio

Wherever the value is kept, state it as Δφ = ln(T_emit/T_CMB) with T_emit tagged
conditional, retiring the double rounding 1099.92 → 1100 → "1101 exactly" (§2.4, a
CHOSE-class ppm wrinkle the legacy record itself logged). Zero consumer cost at current
precision; removes a false-exactness signal from canon wording.

**What this audit does NOT propose:** retracting the fold-zero convention or the Δφ form —
both are blind-verified derived structure; the audit finds the value, and only the value,
riding an unsurfaced interpretation import.

---

END OF REPORT (verifier pass owed before any canon action; this package is documentary and
uncommitted per the audit charter).

## OWNER PROVENANCE CORRECTION (Charles, 2026-08-06)

Charles corrects the origination narrative: **the starlight-temperature anchor PREDATES the
recycling picture and the Planck-blackbody interpretation** in his own idea history. T_starlight as
an anchor is the older element; the recycling ontology and the CMB-as-blackbody reading came later.
The report's framing "the T_starlight language belongs to the recycling picture" is therefore
reversed in his history. Ruling executed same day: options (1)+(4) — see canon C-2026-08-06-2.
