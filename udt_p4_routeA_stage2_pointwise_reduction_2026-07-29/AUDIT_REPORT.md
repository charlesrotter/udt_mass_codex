# P4 Route A Stage 2 — AUDIT REPORT (the pointwise reduction ℛ_PW, TB1–TB6)

Date: 2026-07-29. Branch: `grok`. Preregistration (`PREREGISTRATION.md`) committed at
b741add BEFORE the derivation artifacts existed (contract-first confirmed in git by
the verifier). CPU-only exact-SymPy derivation; no solve, no GPU, no candidate, no
canonization, no physics selected.

**GRADE: VERIFIED-WITH-AMENDMENTS (two rounds)** — blind adversarial pass
(zero-context-framed, same-session-spawned agent, **not a hosted external model**;
caveat travels) returned **PASS-WITH-REQUIRED-AMENDMENTS** with one SUBSTANTIVE
amendment and two minor ones
(A1: the R7(b) "pointwise-vacuous" claim was **REFUTED AS STATED** — a class-wide vs
per-member stabilizer conflation; corrected to GENERIC vacuity + exact stratum
Noether identities, with the verifier's counter-computation adopted and extended;
A2: the check headline overcounted — now split substantive vs citation-guard;
A3: the E12 null-slot statement stamped chart-δK-convention-relative), all applied
and check-backed (`CORRECTION_LAYER.md`; 14 new zero-residual checks; round-1 rerun
67/67, exit 0). The same verifier's **AMENDMENT CLOSURE** pass then returned
**NEW-DEFECT** on ONE A1-extension headline (C3: "the ONLY genuine new cut is the
k_mod = 0 identity" — refuted on C ≠ 0 resonance sub-varieties; the same error class
as the original refutation, one level down), everything else CLOSED; the C3 fix is
applied and check-backed (round 2: 8 new `A1R2_*` zero-residual checks; rerun
**75/75, exit 0 = 67 substantive + 8 citation guards**, deterministic;
`CORRECTION_LAYER.md` §5). Neither refutation overturns the outcome class: OB1
survives on corrected witnesses (verifier-established both rounds), and the refuted
claims' replacements are themselves POSITIVE structural findings — the first
nontrivial pointwise Noether content of the response problem, now including a
shear-slot cut on the resonance locus.

## Result first — the corrected parametrization is the principal deliverable

**ℛ_PW = the character-matched module space CUT BY the stratum Noether identities on
the degeneration strata** — a STRICT SUBSET of the pre-amendment claim on the
codimension-1 stratum k_mod = 0. Exactly:

- **Off the degeneration strata** (generic moduli): per-component character-matched
  functions of the graded alphabet (dims 10/13/16) with the exhibited module bases
  (ranks 1/5/4/4 over the 11-generator invariant ring) — unchanged, verifier-reproved
  to degree 8 + all-degree.
- **On k_mod = 0** (the reciprocal-isotropy locus; codim 1; K₄-stable): the exact
  pointwise Noether identity **−2·k10·r_tf + m00·c10 + m01·c11 − m10·c00 − m11·c01
  = 0** (χ_a-graded; gauge direction = the screen rotation L23, whose tangency
  obstruction at general members is exactly 2k_mod; ONE scalar relation cutting the
  on-stratum restrictions of (R_kmod, R_C); r_tr, r_sh, r_nl drop out).
- **On the resonance locus** (the ONLY other rank-drop loci — the codim-1 layer
  exhaustively confined to λ∓k_mod ∈ {±1} by the Gröbner minor-ideal proof;
  R2-CORRECTED): **k_mod = 0 is the only CODIMENSION-1 genuine cut; the resonance
  rank-drop locus consists of higher-codim sub-varieties, generically with C ≠ 0,
  whose identities ARE further genuine cuts.** The four named C = 0 strata carry
  derived identities involving only mixing components, AUTOMATICALLY satisfied by
  every character-matched member of the declared polynomial/formal class (all
  χ_b/χ_c generators vanish at C = 0) — but these do NOT exhaust the resonance
  content: on the C ≠ 0 sub-variety {λ−k_mod = −1, c00 = c01 = 0} (codim 3,
  K₄-stable) the nullspace is the mixed boost L02 and the exact identity
  **−c10·r_sh − k10·m10 = 0** cuts the SHEAR slot (the character-matched member
  R_c10 = c10 violates it — NOT auto-satisfied). The FULL deeper stratification is
  TYPED-NOT-EXHAUSTED (derived examples + method, not a census).
- **Verdict OB1** (nonempty; R2 per-witness stratum stamps): on k_mod = 0 the
  witnesses are the ω-shape AND the corrected trace-free witness
  (r_tf, m00) = (c01·c10, 2·k10·c01) (character-matched, R_kmod ≢ 0 — the
  k_mod-DETERMINED branch stays nonempty ON the stratum); the ω-shape is an
  on-stratum witness for k_mod = 0 ONLY (it VIOLATES the C ≠ 0 shear identity —
  scoped off those sub-varieties); the corrected witness ALSO vanishes on the found
  C ≠ 0 stratum (survives the new cut); the pre-amendment constant witness
  (r_tf = 1) violates the k_mod = 0 identity and is retained only OFF-stratum
  (scoped); field-sector members (all moduli components zero) pair to zero with
  every gauge direction on EVERY stratum — the all-strata nonemptiness carrier.

## Target outcomes

| Target | Outcome |
|---|---|
| TB1 building-block alphabet | PASS — graded alphabet with zero-residual character/shift assignments; anchored-exponent exclusion VERIFIED and UPGRADED by the verifier (forced by shift-equivariance + banked D3 absorption ALONE, via the orbit-space argument — stronger provenance than the power-family check) |
| TB2 equivariance reduction | PASS-WITH-AMENDMENT (two rounds) — module bases computed and verifier-reproved (degree 8 + all-degree Davenport-style); **R7(b) A1-AMENDED**: class-wide triviality correct but not per-member; now generic vacuity + the stratum identities (13 round-1 `A1_*` checks: all-member minor proof, L23 direction, identity, K₄ grading, witnesses, named resonance strata, codim-1 confinement; + 8 round-2 `A1R2_*` checks: the C ≠ 0 sub-variety shear identity, its K₄ grading, genuine-cut and witness re-scoping computations, all-strata field-sector coverage) |
| TB3 slot/seat reduction | PASS — unique slot decomposition, component pairings, slot theorem, character-graded transport all verified; A3 convention note added (against δ(K+Kᵀ): (4r_tr, 4r_tf, r_sh+r_nl); isomorphic component space; no math changes) |
| TB4 residual space | PASS-WITH-AMENDMENT (two rounds) — parametrization now stated CUT BY the stratum identities (ledger gains three STRATUM-IDENTITY constraint rows: kmod0, named C=0 resonance, R2 shear; R_kmod/R_C/R_k10 rows reference the cuts); fork table and jet-3/4 typing unchanged; stratum identities order-independent (verifier-confirmed) |
| TB5 pointwise verdict | **OB1 stands (both rounds)** — nonemptiness re-witnessed with per-witness stratum stamps (ω-shape: k_mod = 0 only; corrected trace-free witness: k_mod = 0 + survives the shear cut; constant witness: off-stratum; field-sector members: ALL strata); located objects unchanged except the ω scope stamp; exclusion fences unchanged |
| TB6 Stage-3 handoff | PASS-WITH-AMENDMENT — gate-1/gate-4 notes corrected: the R7(b) input is "generically vacuous + stratum identities" and the gates must CARRY the strata; the no-Bianchi-TYPE-assumption warning STANDS (the identities are algebraic pointwise, not differential) |

## Located objects (OBSERVATIONS ONLY — nothing selected)

ω = k10·dk10: INSIDE off the C ≠ 0 resonance sub-varieties (χ_a sector; satisfies
the k_mod = 0 identity — an on-stratum witness THERE — but violates the C ≠ 0
resonance shear identity; R2 per-witness stratum stamps). EH-form
(stationary restriction): INSIDE the jet ≤ 2 class (Route C TC3 cited; anchored
Q-powers recomputed). Bach-form: OUTSIDE jet ≤ 2, INSIDE the typed jet-3/4
extension. CM0-C-type nonvariational members: NOT excluded pointwise (Helmholtz is
gate 3). **A1 OBSERVATION (recorded with scope stamps):** the k_mod = 0 identity is
the FIRST nontrivial pointwise Noether content of the response problem — it ties the
forced trace-free slot r_tf to the mixing kernel M exactly on the
reciprocal-isotropy locus. Factual cross-thread note: the identity's gauge direction
is the screen rotation (the twist/angular direction).

## Falsifier record

**F-B1..F-B6: two F-B3-class items fired (one per round) and were cured; the rest
clean.** F-B1
(candidate smuggle/selection): CLEAN — observational language throughout; no member
selected; no gate run (verifier prose hunt clean; the corrected witnesses are
structural exhibits, not selections). F-B2 (silent fork freeze): CLEAN — six
branches carried/labeled; BR-B/BR-C independence graded genuine by the verifier.
F-B3 (jet-order/scope slip): **two F-B3-CLASS SCOPE SLIPS, both verifier-caught and
amended** — (round 1) the R7(b) vacuity over-claim (a generic-stratum truth stated
unqualified), AMENDED (A1) with the counter-computation embodied as zero-residual
checks; (round 2) the "only genuine cut = k_mod = 0" headline (the same error class
one level down: a stratum-blind uniqueness gloss over the C ≠ 0 resonance
sub-varieties), caught by the closure verifier's counter-computation, AMENDED
(A1-R2) likewise; all other exhaustive claims carried correct stamps. F-B4 (bank
contradiction): CLEAN as to usage — the finding indicts upstream interpretation
GLOSSES (Stage-1 POSED §1.4; Route B T1 headline), routed to the driver via
`UPSTREAM_PRECISION_FLAG.md` (draft; not applied). F-B5 (symbolic failure): NOT
FIRED — 75/75, exit 0 (pre-amendment 53/53; round-1 67/67). F-B6 (equivariance by
fiat): NOT FIRED
— every equivariant space carries its computed basis (verifier-reproved).

## LIMITS THAT TRAVEL

1. **Exhaustive layer** = jet ≤ 2 in the varied fields, registered positive
   triangular chart, registered stationary presentation, one-parameter, off-shell,
   polynomial/formal in (k10, C) (smooth extension = Schwarz-type, Category-A,
   cited). Jet 3/4, BR-M, BR-CE: TYPED, NOT-EXHAUSTED. Wall/corner slot depth:
   example-typed (Route C TC5).
2. **The structural layer is order-independent** — equivariance reduction, character
   modules, slot structure, exclusions, AND the A1 stratum identities
   (moduli-sector, jet-blind; verifier-confirmed).
3. **A1 scope (rounds 1+2)**: field-sector vanishing of the stratum identities is
   DERIVED on the registered stationary presentation (chart scalars carry no frame
   index); general arenas TYPED. The resonance auto-satisfaction holds for the four
   NAMED C = 0 strata within the declared polynomial/formal class; the C ≠ 0
   resonance sub-varieties carry FURTHER genuine cuts (one derived example — the
   shear identity); the FULL deeper stratification is TYPED-NOT-EXHAUSTED (codim-1
   layer exhaustive by the Gröbner proof; deeper layers = derived examples + the
   per-branch method, not a census).
4. **Registered chart**; the K₄ residual is the chart's exact discrete gauge; the
   stratum identities live on the chart's degeneration strata.
5. **Stage-2 bank pending; nothing here selects a member.** ℛ_PW nonempty says
   NOTHING about closure on a solution (R5), cell differentiability (R6), periods
   (R9), R14/R15, or global existence (J07/J11): the full ℛ = ℛ_PW ∩ {WS/GC} could
   still be empty, a point, or a family (J15). No action, no equations of motion,
   no modulus value, no physics; adjudication stays with Charles.
6. **Verifier caveat**: same-session-spawned blind verifier, not a hosted external
   model.

## Evidence

`derive_routeA_stage2.py`: **75/75 checks, exit 0 = 67 substantive zero-residual
exact-SymPy checks + 8 citation guards** (A2 split; 53 pre-amendment + 13 `A1_*` +
1 `A3_*` + 8 round-2 `A1R2_*`, with `PW2_R7b_noether_pointwise_vacuous` REPLACED by
the corrected per-member form), < 2 s, single CPU process, deterministic (three
consecutive round-2 runs: JSON sha256 fb07909a…48b6, ledger sha256 f6d4c6a2…1d06,
stdout sha256 83a423c8…4d68 — all byte-identical; round-1 shas in
`CORRECTION_LAYER.md` §3). `RESIDUAL_SPACE_LEDGER.tsv` (44 data rows; three
STRATUM-IDENTITY constraint rows — kmod0, named C=0 resonance, R2 shear; corrected
header stamp), `routeA_stage2_results.json` (`amendments` incl. `A1_R2`,
`check_split_A2`, `stratum_noether_identities_A1` incl. `Cneq0_subvarieties_R2`),
`DERIVATION_STDOUT.txt` — regenerated post-round-2. `EXACT_DERIVATION.md`
(A1/A2/A3 + round-2 amended), `STAGE3_HANDOFF.md` (round-2-amended gates),
`CORRECTION_LAYER.md` (the amendment record, §5 = round 2),
`UPSTREAM_PRECISION_FLAG.md` (draft upstream edits — NOT applied; resonance
phrasing round-2-adjusted).

## Verifier record

Blind adversarial pass, 2026-07-29 (zero-context framing; same-session-spawned;
**not a hosted external model** — caveat travels). Independent artifacts preserved
in-package (`VERIFIER_INDEPENDENT_CHECK.py`): **33/33 independent checks, exit 0**,
own constructions — orbit-space anchoring derivation (an UPGRADE: the general
exclusion forced by shift-equivariance + D3 absorption alone), degree-8 +
all-degree module reproof, slot/convention cross-check, Route C jet signatures
independently re-read, jet-3/4 attack surface, AND the adversarial
counter-computation that REFUTED the R7(b) vacuity as stated (pointwise stabilizer
rank drop on k_mod = 0; the exact stratum identity; the witness violation).
**Contract-first VERIFIED in git** (PREREGISTRATION.md sole content of b741add;
artifacts later-stamped). Byte-identical rerun (53/53 pre-amendment). Verdict
framing: ADJUDICATE, not confirm — the refutation was found by hunting the
package's own strongest claim. **A1–A3 required**, all applied and check-backed
(round-1 rerun 67/67, exit 0; `CORRECTION_LAYER.md`). The verifier additionally
confirmed: OB1 survives the refutation; the stratum identities are order-independent;
the upstream glosses (Stage-1 §1.4, Route B T1) are generic-only statements whose
COMPUTATIONS are correct — flagged, not indicted.

**Closure record (same blind verifier, 2026-07-29; probe
`VERIFIER_CLOSURE_PROBE.py`, runs clean).** Verdict: **NEW-DEFECT**, scoped to ONE
A1-extension headline; everything else CLOSED. C1 rerun CLOSED (67/67 deterministic;
count reconciliation 53 − 1 + 13 + 1 + 1 = 67 verified; 40 survivors byte-equal, 8
guard relabels, 4 annotation-only, PW5_verdict strengthened — math unchanged). C2
A1 core + extensions (a)(b)(d) CLOSED, independently verified (own `sp.rem` minor
divisibility — 36/36; own Gröbner confinement incl. the attack check that bare
(k00−k11) is NOT in the ideal; the corrected witness's identity/characters/
nonvanishing). **C3 NEW-DEFECT:** "the ONLY genuine new cut is the k_mod = 0
identity" REFUTED — the k00 = −1 slice of the minor ideal has 7 branches incl. two
with generic C ≠ 0; on {λ−k_mod = −1, c00 = c01 = 0} the nullspace is L02 with the
exact identity −c10·r_sh − k10·m10 = 0 (a SHEAR-slot cut), violated by the
character-matched member R_c10 = c10 and by the ω-shape witness; OB1 not threatened
(field-sector members + the corrected witness survive). **RESOLVED this round:**
the corrected statement installed at every occurrence the closure listed
(EXACT_DERIVATION §2 + stamps, ledger header + resonance row, STAGE3_HANDOFF
gate rows, this report, JSON resonance_note/verdict/scope-stamp/check-detail); the
counter-computation adopted as the 8 `A1R2_*` checks; the ω witness re-scoped
per-stratum; a shear STRATUM-IDENTITY ledger row added; the deeper stratification
stamped TYPED-NOT-EXHAUSTED. C4 (A2/A3) CLOSED; C5 handoff CLOSED except the C3
phrase (fixed this round); C6 correction-layer accurate with one wording nit (fixed
— the precise 40/8/4 accounting); C7 upstream flag ENDORSED, both edits, with the
consistency note applied (the resonance phrasing no longer implies the named C = 0
strata exhaust the resonance content). **Pattern note (quoted as a METHOD
observation, verifier's closing):** "One inference overreached — the same error
CLASS as the original refutation (a stratum-blind uniqueness gloss), one level
down: 'only genuine cut = k_mod = 0' fails on C ≠ 0 resonance sub-varieties." The
recurring failure shape is a UNIQUENESS/EXHAUSTIVENESS gloss written one level
below the last verified stratum — the corrective is to stamp every uniqueness claim
with the codimension/stratum level at which it was actually proven (done here:
"only CODIMENSION-1 cut", deeper layers TYPED-NOT-EXHAUSTED).

## STAGE-3 SURFACE (updated; stated as a handle — NOT launched)

Stage 3 = the WS/GC gates ON ℛ_PW per `STAGE3_HANDOFF.md` (rounds-1+2-amended):
gate 1/4 inputs now carry "generically vacuous + explicit stratum identities on the
degeneration strata (k_mod = 0 — the only CODIMENSION-1 genuine cut; the four named
C = 0 resonance strata auto-satisfied in the declared class; the C ≠ 0 resonance
sub-varieties carry FURTHER genuine cuts — derived shear example; deeper
stratification TYPED-NOT-EXHAUSTED)" — gates must CARRY the strata, must NOT assume
continuous-identity-freedom on them, must NOT assume the derived examples exhaust
the deeper resonance content, and must still NOT assume Bianchi-type differential
identities anywhere (that warning stands). Candidates touching the k_mod = 0
stratum must respect the r_tf–M tie; candidates touching the found C ≠ 0
sub-variety must respect the r_sh–m10 tie (per-branch identity computation for any
other deeper stratum contact). Requires its own preregistration and Charles's go;
nothing is launched by this report.
