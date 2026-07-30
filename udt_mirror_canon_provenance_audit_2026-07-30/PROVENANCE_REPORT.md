# Mirrored-cell / seal canon — provenance audit

Date: 2026-07-30. Auditor: provenance recon agent (read-only; no repo file edited).
**AMENDED 2026-07-30** per the blind audit (`AUDIT_VERIFIER_REPORT.md`, verdict
PASS-WITH-REQUIRED-AMENDMENTS, amendments A1-A6). The origin narrative is corrected
throughout (the mirror wording pre-exists the fork doc; the record at adoption was not
silent); the corrected central finding is at §1.1. See `CORRECTION_LAYER.md` for what the
correction changed vs what survived.
Trigger (owner, 2026-07-30, verbatim): "That is not something I could have come up with. I
probably agreed to something the previous AI proposed... if it's leading us somewhere, great,
it's a working premise. But if it's blocking, we should be careful."
House template: `udt_common_scale_neutrality_provenance_audit_2026-07-24/` (strong-CSN re-grade
to CHALLENGED_OWNER_POSTULATE_NOT_DERIVED + consumer map). This audit is documentary only: every
claim cites the banked file; nothing is re-derived here.

---

## 1. The canon record, exact

### 1.1 C-2026-06-10-2 — the finite-cell canon (the root entry)

CANON.md:27-50, verbatim:

> ## C-2026-06-10-2: The finite-cell canon
>
> **Statement:** Dilation is monotone on a finite domain terminated by a
> physical boundary, mirrored across phi -> -phi. The universe is a finite
> cell ([0, r_CMB], phi: 0 -> ln(1101) at the CMB boundary); matter cells
> are finite inside-out cells (phi: 0 at the interface -> -infinity at the
> core endpoint). There is no spatial infinity.
>
> **Forces:**
> - The open-domain threshold theorems lose their premise globally: [...]
> - The matter cell's finite domain and its phi=0 interface are PHYSICAL
>   structure (the mirror of the CMB boundary), not a hand-placed wall.
> [...]
>
> **Provenance:** macro_sector_fork_resolution.md (legacy CG finite-domain
> Class A closure, lines 846-859; current dispatches, Theory Rule 5).
> Canonized by Charles 2026-06-10.

**Origin trace (CORRECTED per amendment A1).** The cited provenance doc is
`grok/quarantine_free_DA/macro_sector_fork_resolution.md` (2026-06-10, an AI recon/synthesis
document). The mirror wording does NOT originate there. Its first banked appearance is
`negative_phi_native_geometry.md` §235 "phi-sign mirror bridge audit" (+ §236, lines
~16668-16745), in the INITIAL repo snapshot commit `691e04a` (2026-06-10), which PRECEDES the
fork doc's commit `64e8fd1` — exact φ→−φ statements ("phi -> -phi swaps the positive-phi and
negative-phi radial/time weights"; "g_AB = r² ω_AB is unchanged by phi -> -phi"; "at phi = 0,
f = 1"), a script (`native_phi_sign_mirror_bridge_audit.py`), and the banked verdict "**The
two-sided bridge is native at the level of metric geometry.**" The fork doc's
"as-if-already-available" posture (flagged below) almost certainly points to §235. Within the
fork doc itself the wording appears in two places:

- Lines 87-89 (as an observation/analogy, not a derivation):
  > The mirror statement on the matter side (phi -> -phi, inside-out):
  > monotone decrease into the cell, terminated by the core endpoint. Both
  > sides are finite cells with monotone dilation — the same canon, mirrored.
- Lines 127, 135-137 (as an explicit AI PROPOSAL to Charles):
  > ## Canonization recommendation (Charles decides)
  > [...]
  > 2. **Replace the growth canon with the finite-cell canon**: monotone
  >    dilation on a finite domain with a physical boundary, mirrored across
  >    phi -> -phi.

The doc's own basis for FINITENESS is quoted at lines 72-84: "Per current canon (Theory Rule 5,
static universe): 'the domain ends at the cosmological boundary; there is no beyond.'" and the
distilled line 84: "MONOTONE GROWTH ON A FINITE DOMAIN TERMINATED BY A PHYSICAL BOUNDARY." The
doc gives NO derivation of the reflection/mirror step — it is introduced by the phrase "The
mirror statement on the matter side" as if already available (available = the banked §235
bridge symmetry), then folded into the recommended canon wording. **The record therefore
shows: bridge symmetry banked pre-fork (AI-era, §235) → the fork doc PROMOTES the bridge to a
CLOSURE clause (the underived step, in the same doc that recommended canonization) →
Charles-RATIFIED same day in compound.** The owner's 2026-07-30 recollection ("I probably
agreed to something the previous AI proposed") MATCHES the written record — indeed §235 is
also previous-AI-era work.

**CORRECTED CENTRAL FINDING (amendment A2; supersedes the original "record is silent"
sentence).** The record at adoption was NOT silent on the reflection. It contained, same-day:

- a DERIVED bridge symmetry — §235's native φ→−φ bridge audit (script + verdict "The
  two-sided bridge is native at the level of metric geometry"), banked in the initial
  snapshot `691e04a`;
- the record's own bridge-vs-closure distinction — `weld_two_sided_results.md:39-41` (commit
  `8cb335d`, 2026-06-10): "**Exterior mirroring is NOT USED** anywhere in the banked chain:
  the phi -> -phi mirror (section 235) is a sign/bridge statement at the phi=0 surface, not a
  mirrored profile in r";
- a mirror DISCUSSION — the horizon-CMB ponder note `archive/horizon_cmb_correspondence.md`
  §3 ("φ = 0 is the unique fixed point of the exact φ → −φ symmetry ... either a triviality
  or a derivation seed — this note does not decide which") and §5 audit target 2 (does the
  inside-out mirror map the BH dissolution-shell structure onto the matter-cell interface
  shell quantitatively?). Note the note's "Origin: Charles's realization" concerns the
  horizon-CMB correspondence; the mirror content is the note's own, AI-authored.

What remains true — and is now the finding: **(i) no CLOSURE derivation exists anywhere in
the record. The underived step is the PROMOTION of the banked seam-bridge symmetry into a
closure clause ("cells close by reflection") — the fork doc crossed the very line the
adoption-day record drew (weld :39-41: a sign/bridge statement at the φ=0 surface, NOT a
mirrored profile in r). (ii) No OWNER quote or discussion of the reflection exists (Charles's
quoted realization concerns the horizon-CMB correspondence, not the mirror). (iii) The
compound sign-off never separately surfaced the mirror clause.**

**The bridge-vs-closure split is decision-relevant:** it parallels the setwise-vs-pointwise /
R-A structure in the banked angular completion (§3.2) — in both cases the DERIVED content
(the seam bridge; the setwise crease) is strictly WEAKER than the point-involution/closure
reading the consumers ride.

The 2026-06-10 macro evidence on the table (Pantheon+ chi2/dof 0.94, DESI BAO, the C2 rho=r
theorem, the finite-domain Class A closure) all bears on FINITENESS and the areal reading —
none of it touches reflection-CLOSURE. [SEE §1.1a: the legacy Class A closure crease is the
one pre-canon antecedent of a mirror-like structure; it is same-doc-legacy, not independent.]

**Founding-intent annotation (CANON.md:66-74 + PROVENANCE.md:31-35,55-58):** the origin prompts
(Grok, 2025-08-12) contain finiteness — Prompt 2: "the redshift will increase asymptotically as
you approach the universe boundary" — and CANON records this as matching C-2's finite-cell
intent "directly", explicitly graded "Recorded as provenance/consilience, not as evidence."
The prompts contain NO mirror/reflection statement.

### 1.1a The cited antecedents: Class A closure and Theory Rule 5 (both finiteness-only)

CANON C-2's provenance cites "legacy CG finite-domain Class A closure, lines 846-859" and
"current dispatches, Theory Rule 5". Both were checked; **neither contains a mirror**:

- `udt_canonical_geometry.md:846-859` defines "**Class A — Finite-Domain (Boundary-Closed)
  Completion**": ":849 The scalar field φ(r) is defined on a finite interval r ∈ [0, r_*]";
  ":851 An explicit outer boundary condition is imposed at r=r_* (Dirichlet, Neumann, or
  Robin), derived from self-adjointness or stated as a modeling assumption"; ":856 No claim is
  made that r_* represents physical infinity." No mirror/reflection anywhere in the cited span.
- **Theory Rule 5** is a Charles-authored founding rule (verbatim at
  `archive/udt_validated_results.md:27904`): "UDT is STATIC. ... Lab inputs only: {m_proton, c,
  G, ℏ} + direct observations {T_CMB, T_starlight}" — invoked by the fork doc only for
  finiteness (`macro_sector_fork_resolution.md:73-75`: "'the domain ends at the cosmological
  boundary; there is no beyond.'"). It anchors finiteness/staticness; it does not contain or
  support the mirror.

**Session record of the adoption:** the fork doc self-labels "Status: SYNTHESIS + CANONIZATION
RECOMMENDATION — not canonical until Charles signs off. Created: 2026-06-10"
(`grok/quarantine_free_DA/macro_sector_fork_resolution.md:8-9`). `STATE.md:1838-1840`:
"Awaiting Charles's sign-off on: R-areal canon, finite-cell canon, program redirect ..." — the
sign-off list names "finite-cell canon" as one item and does NOT separately name the mirror.
The only ratification language on record is the stamp `CANON.md:50`: "Canonized by Charles
2026-06-10." **The record contains no Charles quote proposing, discussing, or specifically
endorsing the reflection component** — it entered as one clause inside a ratified compound.
No record exists of the mirror clause ever being separately surfaced to Charles.

### 1.2 C-2026-07-02-1 — Δφ clarification (zero at the CMB fold)

CANON.md:235-253 (relevant verbatim): "The finite-cell canon C-2026-06-10-2's wording ... is
CLARIFIED (not retracted): the physical content is the DIFFERENCE Δφ = φ(CMB fold) − φ(core) =
ln(1101) ... The blind-verified fold derivation (universe_cell_fold_jc_sigma_results.md: the odd
fold φ→−φ pins φ = 0 AT the CMB fold) fixes the canonical convention ... **Provenance:** fold JC
derivation + blind verification (agents a15ecc62590d15bd4 / a18115fe9d95cfb84) ...
**Charles-authorized 2026-07-02.**"

**Origin verdict:** DERIVED-GIVEN-THE-MIRROR. The fold JC derivation is real, CAS-checked and
blind-verified — but it takes the odd mirror AS INPUT from canon
(`universe_cell_fold_jc_sigma_results.md:14`: "**Odd fold (outer, r_s; canon φ→−φ)**"). It
derives the CONSEQUENCES of the fold (φ(r_s)=0 pin, ρ'(r_s)=0, φ' free ⇒ flux seal q), not the
fold's existence.

### 1.3 C-2026-07-03-3 — matter-core wording clarified (even fold at finite depth)

CANON.md:326-343 (relevant verbatim): the φ→−∞ core "was an early exploratory description ...
Charles had let it go long before this derivation (Charles, 2026-07-03: 'I let go of negative
phi to infinity a long time ago')"; the derived replacement is an "**EVEN MIRROR FOLD at FINITE
depth** — φ'(0) = ρ'(0) = f_r(0,θ) = 0 as natural boundary conditions from stationarity alone";
"The finite-cell content of C-2026-06-10-2 — finite mirrored domains, no spatial infinity —
STANDS unchanged." Provenance: `microphysics_E1_composite_closure_results.md` (CAS 24/24;
blind verifier 8/8 HOLD). Canonized by Charles 2026-07-03.

**Origin verdict:** the EVEN (inner) fold is the one mirror component with a stationarity-alone
derivation on record — `universe_cell_fold_jc_sigma_results.md:37-40`: "**Even fold (inner,
r_c):** exact symmetry of both branches; stationarity ALONE (no smoothness needed) pins
φ'(r_c)=ρ'(r_c)=0". Note this derives the inner fold's BCs as NATURAL boundary conditions —
i.e. the even "mirror" at the core is equivalent to ordinary regularity/free-endpoint
conditions, and does not by itself support the OUTER odd reflection (the identification of a
mirror partner across the seal).

### 1.4 C-2026-07-04-1 — seal-involution sector split

CANON.md:367-398 (relevant verbatim): "the durable mirror-fold canon (seal = same-minus MIRROR
FOLD; C-2026-06-10-2 'mirrored across φ→−φ') is CLARIFIED by localizing WHICH involution acts
on WHICH sector: STATIC fields ... governed by the SPATIAL depth mirror σ_φ ... ⇒ **Dirichlet
φ(r_s)=0** ... TIME-ON / rotating / off-diagonal fields are governed by the temporal mirror
t→−t ... It is NOT a new mechanism and NOT an overturn — it makes explicit which involution the
banked fold-JC derivation already used ... **Correction folded in:** the pre-foundation
`seal_junction_condition_results.md` (2026-06-21) assigned φ EVEN→Neumann via t→−t; that is
WRONG ... **Canonized (as a CLARIFICATION) by Charles 2026-07-04.**"

**Origin verdict:** DERIVED-GIVEN-THE-MIRROR (blind-verified re-grade, doc
`node05_seal_parity_regrade_results.md`). Like C-2026-07-02-1, it allocates and corrects the
involution's ACTION; the EXISTENCE of the mirror involution is inherited from C-2026-06-10-2
at every link of the 06-21 → 07-04 seal chain. Traced quotes:

- `seal_junction_condition_results.md:6` (2026-06-21): "sigma-ODD / time-on sector, for BOTH
  candidate involutions. NOT canon."; `:50-52`: "the canon seal (C-2026-06-10-2) is a
  **spatial/radial** boundary (mirrored across φ→−φ at the φ=0 interface). But the W6
  *involution acting at that crease* is read as **time-reversal**." — the doc only tests WHICH
  involution (σ1 = t→−t vs σ2 = P×T) and its parities; never derives that a mirror exists.
- `node05_seal_parity_regrade_results.md:38-40` (2026-07-04): "**This RE-LOCALIZES, it does not
  contradict, the canon.** Canon's primary wording is 'mirrored across φ→−φ' (CANON.md:30); the
  fold-JC derivation ALREADY used φ→−φ to pin the static fields."; premise tags `:73-75`: "odd
  φ→−φ identification DERIVED within the pointwise class (class = CHOSE, loophole probed);
  φ(r_s)=0 DERIVED given φ-continuity (continuity posture CHOSE-cited, **canon-anchored
  C-2026-06-10-2**)."
- STATE.md has no 2026-07-04 lab-log block for this canonization (the only 2026-07-04 hit is a
  superseded charter reference at STATE.md:2); the adoption record is CANON.md + the node05
  doc. No session-level discussion of the mirror's existence at the 07-04 clarification is on
  record — consistent with its "clarification, not overturn" framing.

### 1.5 Related but not part of the compound (noted for completeness)

- CANON.md:135,173 (C-2026-06-14-1): "eta-seal coupling", "eta=1/18 is a seal/boundary object"
  — legacy-era seal VOCABULARY inside a superseded-arc entry; not the mirror premise.
- CANON.md:289-325 (C-2026-07-03-2): the ladder/fold-pair soft mode — uses "fold-pair" as a
  mode label on the mirrored-cell structure; downstream consumer, not origin.

---

## 2. The compound premise, split

The canon sentence "Dilation is monotone on a finite domain terminated by a physical boundary,
mirrored across phi -> -phi" bundles THREE separable claims:

### 2a. FINITENESS (no spatial infinity; cells are finite)

MULTIPLY-ANCHORED — the only component with independent, later, derivation-grade support:

1. **Founding intent** (PROVENANCE.md:31-35, Prompt 2 verbatim): "the redshift will increase
   asymptotically as you approach the universe boundary" — owner-originated (2025-08-12),
   pre-AI-development. Graded consilience-not-evidence in CANON.md:66-74, but it establishes
   finiteness as OWNER-ORIGINATED in intent.
2. **The WR-L macro arc (2026-07-09, canon C-2026-07-09-1/1a)** — CANON.md:420-470: finite
   proper room ℓ=∫dr/√A<∞ is a Charles-ACCEPTED AXIOM of the WR-L package ("I have no problem
   with those conditions"), and the selected A=1−r/X gives "the causal ceiling ... finite proper
   distance". IMPORTANT PRECISION (C-2026-07-09-1a item 2, verbatim): "**Horizon, not hard edge
   of space.** ... a causal / Schwarzschild-type horizon at finite proper distance: infinite
   optical reach, z→∞, with a **trapped interior beyond** r=X (signature flip). Wording: 'ends
   at x_max' means causal horizon at finite proper distance with interior beyond, **not a wall
   of space**." So the strongest current finiteness anchor is a CAUSAL-HORIZON finiteness
   (finite proper room, wall as horizon), which is not identical to — and mildly reshapes —
   C-2's "physical boundary / no beyond" wording. [Independence from the mirror: §2a-i below.]
3. **The fold-JC arc's own finiteness teeth** (`universe_cell_fold_jc_sigma_results.md`,
   NEGATIVES_REGISTRY.md:129-146): vacuum impossible + two-mirror rigidity + the flux-seal
   survivor — derived within the finite-cell frame (these support the frame's fruitfulness, not
   its truth; they are conditional on it).
4. **Legacy antecedents, finiteness-only:** the CG Class A finite-domain definition
   (`udt_canonical_geometry.md:846-859`, §1.1a) and Charles's Theory Rule 5 (STATIC / "no
   beyond", `archive/udt_validated_results.md:27904`).

**2a-i. WR-L independence check (confirmed):** exhaustive grep of both WR-L records
(`simple_metric_L_wall_regularity_closure_results.md`,
`simple_metric_WR_L_external_triple_blind_audit_results.md`) finds NO occurrence of "mirror",
"φ→−φ", "reflection", or "C-2026-06-10"; the only canon cited is C-2026-07-09-1. Finiteness
driver verbatim: `simple_metric_L_wall_regularity_closure_results.md:20` "Wall package: ∞
optical, finite proper, finite G^θ_θ at wall | **WR-L axioms** — **Charles accepts**
(2026-07-09)"; `:168` "only finite proper room kills α=2"; `:169` "α=1 wall = causal horizon +
interior beyond r=X, not hard edge of space". The WR-L finiteness anchor is therefore fully
independent of the mirror clause.

**2a-ii. The 07-18 adjudication's finite-cell requirements** (mirror-free):
`native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md:118-123` requires
"the same exact **finite-cell** static equations", "compatible nontrivial **finite-cell**
solutions and global Xmax/proper-density closure";
`UDT_NATIVE_ACTION_FINAL_ADJUDICATION_RETURN_2026-07-18.md:31-32`: "The complete native action,
off-shell variation domain, native carrier-to-dilation source, **differentiable finite-cell
boundary action**, and normalized boundary charge/mass are **OPEN**." No "mirror" / "φ→−φ" /
"reflection" token appears in the adjudication requirements — its gates are finiteness-side
(boundary action, Xmax closure) and do not touch reflection.

**Verdict 2a: finiteness is multiply-anchored** (owner intent 2025-08-12; the macro data stack
06-10; Theory Rule 5; the Charles-accepted WR-L finite-proper-room axiom 2026-07-09,
triple-blind audited and mirror-independent; the 07-18 adjudication gates) — though its
sharpest current form is "causal horizon with interior beyond", not "hard edge".

### 2b. MIRROR-CLOSURE (cells close by REFLECTION; the fold; φ→−φ identification)

The CLOSURE reading is single-sourced to the 2026-06-10 fork-doc PROMOTION (the bridge
SYMMETRY beneath it pre-exists, derived, in §235 — corrected origin, §1.1). The record's own
adoption-day split marks the line the promotion crossed — `weld_two_sided_results.md:39-41`
(2026-06-10), verbatim:

> **Exterior mirroring is NOT USED** anywhere in the banked chain: the phi -> -phi mirror
> (section 235) is a sign/bridge statement at the phi=0 surface, not a mirrored profile in r.

Every later appearance is one of:

- **Assumed-from-canon:** the fold-JC derivation takes it as input
  (`universe_cell_fold_jc_sigma_results.md:14` "canon φ→−φ"); the seal chain (06-21 → 07-04)
  allocates which involution acts where but never derives that an involution closes the cell.
- **Explicitly flagged as the assumption it is** — the sharpest in-record statement, fold-JC doc
  lines 31-33, verbatim:
  > Independent-partner glue (NOT mirror-image) gives no ρ'-pin — that configuration IS the
  > banked embedded case; the mirror-image assumption = the "closed cell, nothing beyond"
  > premise. Fork recorded, consistent.
  I.e. the banked derivation ITSELF records mirror-image-vs-independent-partner as an open
  FORK, with the mirror leg riding the "nothing beyond" reading of C-2 — the reading that the
  WR-L precision (2a item 2: "interior beyond", horizon-not-wall) has since softened.
- **Re-read as definitional by the current arc:** Route P package,
  `udt_p4_routeP_seal_parity_2026-07-29/EXACT_DERIVATION.md:46`, verbatim:
  > Mirror on the depth field | ε_φ = −1. **Provenance, re-read exactly: not derived from
  > deeper structure — it is the canon's DEFINING wording of the finite-cell mirror**
  > ("mirrored across φ→−φ" is what the fold IS). C-2026-07-04-1 (node05, blind-verified)
  > DERIVES which involution governs which sector ... | **CANON** (definitional) + **DERIVED**
  > (sector localization, BC consequence — banked)
  (The task brief attributed this finding to the angular-completion package; the exact locus is
  the ROUTE P package's TP1 seal-record table, echoed at
  `udt_p4_routeP_seal_parity_2026-07-29/AUDIT_REPORT.md:86`.)
- **Partially derived structure NEAR it (not of it):** (i) the even INNER fold = natural BCs
  from stationarity alone (§1.3) — but that is core regularity, not reflection-closure; (ii)
  the odd fold is an exact bulk symmetry of Branch G though NOT of Branch P
  (`universe_cell_fold_jc_sigma_results.md:20-23`) — a suggestive consilience ("P|G-seal"),
  recorded as a PONDER-tag, not a derivation.

**Verdict 2b (corrected chain, A2): reflection-CLOSURE has NO derivation anywhere in the
record.** Its full provenance chain is: pre-handover bridge-symmetry observation
(`negative_phi_native_geometry.md` §235, initial snapshot 691e04a — DERIVED, bridge-scoped
only) → fork-doc PROMOTION of the bridge to a CLOSURE clause
(macro_sector_fork_resolution.md:87-89 analogy; :135-137 recommendation — the underived step,
crossing the weld :39-41 line) → Charles ratification in compound (CANON C-2026-06-10-2) →
everything since assumes it. The closure promotion is exactly the class the owner named on
2026-07-30: OWNER-RATIFIED-PROPOSAL (the bridge beneath it is derived).

### 2c. The entangled THIRD component: seal-value / parity conditions (ε_φ=−1 wording)

CONFIRMED. ε_φ = −1 (φ odd under the fold) is not a separate result: it IS the canon's wording
("mirrored across φ→−φ" — the sign is inside the definition). Exact locus of the current arc's
own finding: `udt_p4_routeP_seal_parity_2026-07-29/EXACT_DERIVATION.md:46` ("not derived from
deeper structure — it is the canon's DEFINING wording"), echoed AUDIT_REPORT.md:86
("canon-definitional + derived sector localization"). What IS derived downstream of it
(blind-verified): the sector split (σ_φ static / t→−t time-on), Dirichlet φ(r_s)=0, the flux
seal q=Zρ_s²φ', ρ'(r_s)=0 (three independent routes). So the layer-structure is:
[canon-definitional: a mirror exists AND φ is odd under it] → [derived: which involution, which
BC, the flux seal]. A challenge to 2b automatically challenges the ε_φ=−1 SIGN; it does NOT by
itself void the JC machinery, which would survive as conditional structure on any fold that
exists.

---

## 3. The consumer map

Per-consumer table with exact loci in `CONSUMER_LEDGER.tsv`. Fall-hardness is assessed against
a hypothetical re-grade of the MIRROR-CLOSURE clause (not finiteness) to CHALLENGED, using each
package's OWN premise typing (no re-derivation here). Tags: FALLS (void without the premise) /
DEGRADES-TO-CONDITIONAL (survives with a premise stamp) / UNAFFECTED (finiteness-only or
independent).

### 3.1 Route P — `udt_p4_routeP_seal_parity_2026-07-29` (ea5d8a3) — **FALLS**

Premise ladder `EXACT_DERIVATION.md:56-72`: P0 (CANON) ":56 the fold is a Z₂ identification and
flips depth, φ→−φ"; P1 (DERIVED transcription X ↦ −JXJ⁻¹); P2 (TYPED, NOT derived) ":67-72
chart-representability — the mirror acts ON the registered class (member-to-member) ... on that
alternative ε_m is UNDEFINED on the banked footing." ε_λ=−1 ":133 needs only P0+P1;
dressing-INDEPENDENT"; ε_kmod=−1 ":134 DERIVED under P2 ... CONSTRAINED without P2" (chart-escape
witness in-package). Every parity IS the sign of a field under the fold's action — no fold, no ε.
The λ=0 / k_mod=0 constant-census pins (the det-one/E07 landing) go with it. Rides
MIRROR-CLOSURE entirely; finiteness plays no role in the parity engine.

### 3.2 Angular completion — `udt_p4_angular_completion_2026-07-30` (5978573) — **FALLS**
(core), with its E0-collapse conditional INVERTING

Typed premise R-A `EXACT_DERIVATION.md:60`: "the completed fold's screen block is realized by
(descends from) a point involution of the banked toric arena ... TYPED, NOT DERIVED. **Without
R-A all S-B/S-D conclusions are VOID and silence stands.** R-A ⟹ P2 (strictly stronger)."
Joint unsatisfiability `:22-24,:128`: "{R-A, R-C-pointwise, banked-complete membership} jointly
unsatisfiable — under R-A with the pointwise crease reading, NO banked complete member realizes
the canon fold" (escapes: ¬R-A / setwise crease / register a new class). The E0-collapse ("in
EVERY realized outcome E0=0", AUDIT_REPORT.md:50-53) is conditional on R-A; challenging the
mirror makes ¬R-A the live branch — i.e. the massive-landing SURVIVAL branch. Note the package
already PROVED the strictest mirror reading incompatible with the registered arena (the joint
unsatisfiability) — the trigger for this audit.

### 3.3 Gradient seat — `udt_p4_gradient_seat_2026-07-29` (f521222) — **DEGRADES-TO-CONDITIONAL
→ FALLS for the λ/k_mod legs**

Inputs `EXACT_DERIVATION.md:67-68,84`: "banked odd-parity forcing (Route P ea5d8a3, premise
ladder P0+P1(+P2)): λ(x), k_mod(x) mirror-odd, wall values vanish; f/bh parities SUPPLIED";
the lock-at-zero step `:150-153`: "A mirror-odd field's wall value solves v = −v ⟹ v = 0";
E0 condition `:208-210`: "either definite supplied parity on both fields collapses E0 to 0."
The lock-emergence theorem's parity lever inherits Route P's ladder ("the ladder travels"), so
its λ/k_mod odd-forcing falls with Route P; the f/bh legs were SUPPLIED (carried both ways)
and are unaffected as suppositions. The jet-extension/atlas machinery itself is mirror-free.

### 3.4 Slice-2 / Slice-2b — `udt_p4_routeA_slice2_solution_legs_2026-07-29`,
`udt_p4_routeA_slice2b_full_cell_2026-07-29` — **DEGRADES-TO-CONDITIONAL**

Both tag the mirror instance honestly: `EXACT_DERIVATION.md:68` (both) "Mirror parity instance
ε_φ = −1 (spatial mirror, static sector) | THEORY-cite (CANON C-2026-06-10-2 /
C-2026-07-04-1)". What rides it: Slice-2 ":250-257 odd p0-trace forces the intercept 0 at each
wall"; Slice-2b ":178 the v_p SLOT is parity-killed", ":269 canon ε_φ = −1 kills the v_p slot".
The massless theorem has separate E0-census support; the parity-specific cuts (v_p slot-kill,
wall-intercept-zero, canon-parity trace loci) would need a CONDITIONAL-ON-MIRROR stamp, and the
wall-density cut count would reopen. Not void.

### 3.5 Reduction theorem — `udt_p4_bookkeeping_forcing_2026-07-29` (38577c9) — **UNAFFECTED**
(its S3 lever was already conditional)

`EXACT_DERIVATION.md:61`: "CANON ... ε_φ = −1 instance | CANON cite; **moduli parities ε_m NOT
derived — SUPPLIED**"; the S3 lever `:149`: "PERMITS-BOTH-CONDITIONAL — an exact lever awaiting
SUPPLIED data ... **the depth mirror is not representable in-class by generator negation ...
canon derives ε_φ = −1 only**." The reduction (R2 ≡ census fork) does not need the mirror; only
a future parity RESOLUTION of the fork would. Already flagged both-ways.

### 3.6 Stage-1 census — `native_action_stage1_2026-07-18/arm_B/cold_output/D0_D5.md` —
**DEGRADES-TO-CONDITIONAL (datum only); verdicts UNAFFECTED**

":61 Static phi odd parity at seal; phi|_Σ = 0, normal derivative free | CANONIZED / BINDING
INPUT"; ":431 Boundary functional is uniquely fixed by finite-cell parity | UNDERDETERMINED |
Parity fixes phi|_Σ, not B[φ]." The mirror yields only the boundary datum φ|_Σ=0 — already
UNDERDETERMINED for the boundary functional; the census's OPEN verdicts do not change. The
separate finiteness input ("no asymptotic infinity", :29) stands on §2a anchors.

### 3.7 Fold-JC / seal chain banked results (2026-07-02 → 07-04) —
**DEGRADES-TO-CONDITIONAL (they are theorems GIVEN the fold)**

`universe_cell_fold_jc_sigma_results.md` (φ(r_s)=0, ρ'(r_s)=0, flux seal q as output, budget
identity, E_m(r_c)=2 critical closure) and `node05_seal_parity_regrade_results.md` /
C-2026-07-04-1 (sector split, Dirichlet correction): all derived GIVEN the odd fold; each would
survive as conditional structure on any fold that exists. The fold-JC doc itself recorded the
escape fork (`:31-32` independent-partner glue = the banked embedded case, no ρ'-pin). The
even-INNER-fold results (stationarity-alone natural BCs) are mirror-independent and UNAFFECTED.

### 3.8 Broad sweep (~130 July report files matching mirror|fold|seal|crease)

Majority cite "finite mirrored cell / no spatial infinity" as finiteness backdrop only —
UNAFFECTED (e.g. `finite_cell_completion_atlas`, `finite_cell_reciprocal_survival_density`,
`global_reciprocal_closure/persistence`, `xmax_*`, most `reciprocal_*`/`coframe_*` audits).
Additional reflection-load-bearing members (DEGRADES-TO-CONDITIONAL unless noted):
`udt_complete_seal_fixed_set_selector_audit_2026-07-21` (involution fixed-locus is the object);
`udt_free_global_seal_transversality_audit_2026-07-21` (fold geometry);
`udt_involutive_exchange_branch_availability_audit_2026-07-24`; the 07-20 coframe
seal-involution completion trio (`clock_ruler_soldering_selector`,
`mixed_readout_anchor_soldering`, `complete_lift_mu_closure` — the MULTIPLE_COMPLETIONS bank
that Route P and the angular completion cite as the smallest missing object).

**Added per amendment A5 — four further DEGRADES-class consumers (missed in the first
sweep):**

- `udt_p4_routeA_stage3_gate_cut_2026-07-29` — ε_φ = −1 THEORY-cited wall parity
  (EXACT_DERIVATION.md:59, :227 — the `TC3_mirror_canon_parity_instance` guard; f/bh parities
  SUPPLIED, carried both ways). DEGRADES-TO-CONDITIONAL.
- `udt_p4_routeA_stage2_pointwise_reduction_2026-07-29` — mirrored-parity wall data handed to
  Stage 3 as a CANON boundary component (STAGE3_HANDOFF.md:68). DEGRADES-TO-CONDITIONAL.
- `udt_p4_routeA_response_inverse_problem_2026-07-29` — the R6 finite-cell boundary gate
  CONDITIONS on the mirrored-cell parity + sector split (POSED_INVERSE_PROBLEM.md:194;
  SIX_GATE_SPECS.md:143) — a forward decision-surface/spec consumer (POSED; nothing banked on
  it yet). DEGRADES (spec-conditioned).
- `finite_cell_seal_boundary_phase_join_2026-07-20` — the mirror-fold + temporal-seal clause
  rows enter as CANONIZED inputs (PREREGISTRATION.md:43, :64-66); the package's own strongest
  challenge (AUDIT_REPORT.md:47-66) already records that K_ij=0 is NOT derived from the word
  "mirror". DEGRADES-TO-CONDITIONAL.

**Sweep scope (stated per A5):** the §3.8 sweep is scoped to JULY report files; June-era
SUPERSEDED consumers (w6, phase1_geon, phase2a/2b) fall outside its stated scope —
acceptable given supersession, but stated here explicitly.

### Tally

FALLS: 2 (Route P; angular completion core — with its E0-collapse conditional inverting to the
survival branch; unchanged by amendment A5). DEGRADES-TO-CONDITIONAL: 9+ (gradient-seat
λ/k_mod legs; Slice-2; Slice-2b; fold-JC/seal chain incl. C-2026-07-02-1 and C-2026-07-04-1
content; Stage-1 parity datum; the 07-20/07-21 involution-object audits; plus the A5
additions: stage-3 gate cut, stage-2 pointwise-reduction handoff, response-inverse-problem R6
spec, seal-boundary-phase-join). UNAFFECTED: the reduction theorem, the even-inner-fold
results, and the large finiteness-only population. **This week's census-fork decision surface
is the maximal exposure: the constant-sector pins (λ=0, k_mod=0) and the R-A-conditional
E0-collapse — the exact cuts on Charles's desk — all ride the challenged clause.**

---

## 4. The re-grade options (typed; no recommendation — the owner rules)

Full two-sided costs in `REGRADE_OPTIONS.md`. One line each:

- **(a) KEEP as working premise** — append-annotate CANON: mirror-closure =
  OWNER-RATIFIED-PROPOSAL (CHOSE-class), tag travels on every consumer; everything stands but
  visibly conditioned, and the banked joint-unsatisfiability remains an untyped tension.
- **(b) CHALLENGE** (strong-CSN-style) — re-grade to
  CHALLENGED_OWNER_RATIFIED_PROPOSAL_NOT_DERIVED; CONDITIONS-CHANGED stamps per the ledger
  (Route P + angular core FALL; six-plus consumers degrade to conditional; the ¬R-A branch —
  the massive-landing survival branch — becomes live; the arena incompatibility dissolves).
- **(c) SPLIT-AND-KEEP** — declare C-2026-06-10-2 a compound: finiteness retained at its own
  stronger multi-anchor provenance (§2a), mirror-closure re-tagged separately, ε_φ=−1 tagged
  canon-definitional; surfaces the "no beyond" vs "interior beyond" reconciliation question.
- **(d) DERIVABILITY candidates located** (not derived here): the WR-L signature-flip/macro↔micro
  seam; the Branch-G exact odd-fold symmetry (P|G-seal consilience); the fold-vs-independent-
  partner ρ'(r_s)=0 discriminator; the OPEN 07-18 finite-cell boundary-action gate as the named
  derivation site; the banked §235 bridge audit (the derived seam-bridge whose PROMOTION is the
  gap) and the horizon note's §5 audit target 2 (A3 additions) — with the angular completion's
  unsatisfiability inherited as falsifier.
