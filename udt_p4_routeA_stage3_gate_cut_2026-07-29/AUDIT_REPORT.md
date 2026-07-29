# P4 Route A Stage 3 (Slice 1) — AUDIT REPORT (the candidate-free gate cuts on ℛ_PW, TC1–TC6)

Date: 2026-07-29. Branch: `grok`. Preregistration (`PREREGISTRATION.md`) committed at
dbc114f BEFORE the derivation artifacts existed (contract-first confirmed in git by
the verifier). CPU-only exact-SymPy derivation; no solve, no GPU, no candidate, no
canonization, no physics selected.

**GRADE: VERIFIED-WITH-AMENDMENT** — blind adversarial pass (zero-context-framed,
same-session-spawned agent, **not a hosted external model**; caveat travels) returned
**PASS-WITH-REQUIRED-AMENDMENTS** with one SUBSTANTIVE amendment and three lesser ones
(A1: the anchored-log forcing quantifier **REFUTED AS PHRASED** by an in-family
counter-construction — corrected to the exact iff condition, with the verifier's
counterexample adopted as zero-residual checks; A2: both F-S3-class catches
memorialized here; A3: the bare-φ/anchored-log reconciliation line added; A4: three
guard-grade checks reclassified in the split), all applied and check-backed
(`CORRECTION_LAYER.md`; 3 new zero-residual checks; rerun **52/52, exit 0 = 33
substantive + 19 citation guards**, deterministic ×3). The refutation does NOT touch
the outcome class or any partition computation: the refuted strand was one
TC1 prose/detail claim whose underlying computations were correct; the corrected
statement is strictly narrower.

## Result first — the joint gate-cut map is the principal deliverable

**The gates partition ℛ_PW as a populated composite map (`GATE_CUT_LEDGER.tsv`): 30
composite cells = 5 pairing branches (P1-4D, P1-triad, P2, P3-bulkP2, P3-bulkP1) × 3
strata (GENERIC, KMOD0, RES-CNEQ0) × 2 G3-cells — 20 adjudicated composite cells, ALL
witness-nonempty; 10 RES-CNEQ0 cells CENSUS-REQUIRED (resonance rule); + 4
known-object OBSERVATION rows.** Outcome class **OS1** (no gate empties ℛ_PW at the
declared scope; no rigid collapse). **The L6 response-vs-action fork is now a COMPUTED
pairing-relative partition, not a decision:** LOCALLY-EXACT vs NONVARIATIONAL is a
computed cut, pairing-RELATIVE (the e^{−a_F p0} bijection intertwines the P1 and P2
partitions — isomorphic-but-distinct; cell membership of a fixed tuple is
pairing-relative, witnessed by W1/W2′/ω changing cells off the T4 blindness loci; W3
is NV with PROVEN branch-independence), with **both cells populated under every
enumerated branch and both first-class**. Per row the ledger carries: the G3 condition
set, G1 type (GENERIC = DETERMINED-type, no identity assumed; KMOD0 =
CONSTRAINED-balanced, one algebraic identity ↔ one gauge direction; RES-CNEQ0 =
CENSUS-REQUIRED), G5 status (N=2 self-pairable-typed at jet ≤ 2; N=3/4
extension-required; parity-halving; NV = no-bulk-forced-slots), G6 type
(vanishing-by-torsion for closed forms on K₄-torsion cycles; needs-completion-data;
J07/J11 classification-required [F-S7]), witnesses, open forks, and Slice-2 duties.

**The corrected anchored-log statement (A1, verifier-derived, adopted exactly):**
under the two ENUMERATED λ-dependent P1 volume instances (both da_F/dλ = 2), the LE
cell's λ-slot is forced nonzero — carrying the log(c_E/Q) dependence via the a_F′·p0
term — **IFF ∂λ(W_F·R_a) ≢ 0 for some field slot a; in particular for every
λ-INDEPENDENT nonzero field sector** (where the forcing is real and the generated
witness R_λ = 2p0·L̃₀ stands); NOT "whenever the field sector is nonzero"
(counterexample on record: R_a = e^{−2λp0}(p2,f2,h2), moduli slots zero, fully LE
under P1-4D, zero λ-slot, no log — verifier V10b, banked as
`A1_V10b_counterexample_LE_zero_lambda_slot` with the iff and sub-case checks). The
log is alphabet-legal at supplied c_E — anchored exactly as Stage-2's (c_E/Q)^a
alphabet entries are (no bare-φ readmission; A3 reconciliation in
`EXACT_DERIVATION.md` §1.2.6). Forced STRUCTURE inside the LE cell, not an obstruction.

## Target outcomes

| Target | Outcome |
|---|---|
| TC1 Helmholtz partition | PASS-WITH-AMENDMENT — condition system proven = Fréchet self-adjointness + necessity on the generic EL image (sufficiency = banked bicomplex statement, Category-A cited, witness-instantiated); pairing-dependence map computed (condition (i) pairing-independent across the anchored family; exact (ii)/(iii)/H4/H5 shifts; the intertwining bijection; T4 blindness consistency; P3 bulk inheritance); witnesses W1/W2′/W3/ω verifier-reproduced; W3 branch-independence attacked and SURVIVED; **A1**: the anchored-log quantifier corrected to the exact iff condition (3 new `A1_*` checks); four-corner transversality on KMOD0 witnessed |
| TC2 integrability typing | PASS — GENERIC = DETERMINED-type (no pointwise identity, recomputed; no Bianchi-type identity assumed); KMOD0 = CONSTRAINED-type balanced (the banked identity = one row dependency ↔ the L23 gauge direction; algebraic NOT differential); RES-CNEQ0 CENSUS-REQUIRED; no existence claim (F-S6 clean, verifier-confirmed "balanced is a COUNT") |
| TC3 boundary census | PASS — N=2: slots = 0-jet traces, 1-jet momenta, self-pairable at wall grade 2 (banked trace-jet rule); N=4: third-jet momenta → structurally unable within jet ≤ 2, typed extension REQUIRED (scope stamp correct everywhere — never "excluded"); parity-halving derived, parities SUPPLIED-tagged; anchored-φ wall rule recomputed; NV cell = no bulk-forced slots; corners typed-only; Route C TC5 instances reproduced verbatim |
| TC4 period typing | PASS — K₄ all-torsion recomputed; vanishing-by-torsion scoped to CLOSED forms on TORSION cycles in every occurrence; completion cycles need L4 data (branch-uniform type); J07/J11 mixing rows CLASSIFICATION-REQUIRED with the F-S7 flag carried on every row; no banked G6 claim rests on the MODEL-KNOWLEDGE row |
| TC5 joint gate-cut map | PASS — the 30-cell composite map above; 20 adjudicated witness-nonempty + 10 CENSUS-REQUIRED; OS1; known-object rows observations-only |
| TC6 Slice-2 surface | PASS — `SLICE2_SURFACE.md`: a HANDLE, not a launch (verifier-confirmed: no leg run, no fork decided); per-cell remaining work + cross-cell tiles + the may-not-inherit list; the LE×KMOD0 anchored-log echo now carries the A1-corrected condition |

## Known-object locations (OBSERVATIONS ONLY — nothing selected)

ω-shape: LE under P2/P3-bulkP2/P1-with-λ-independent-a_M; NV under P1 with a_M = 2λ
(computed; banked stratum stamps cited — off RES-CNEQ0, on-stratum witness for KMOD0).
EH-form (stationary restriction): variational w.r.t. its metric-volume (P1-4D-type)
pairing BY CONSTRUCTION of its action (Route C banked; GR-as-reference lane); the
RESTRICTED system's G3 status under the enumerated pairings NOT adjudicated (R12
restrict-vs-vary caveat; Slice-2 cost item). Bach-form: typed jet-3/4 class, outside
the exhaustive layer; G5 EXTENSION-REQUIRED at jet ≤ 2 (derived); order-4 condition
machinery anchored (2-field instance). CM0-C-type nonvariational members: the NV cell
is their home CLASS (banked; none instantiated).

## Falsifier record (A2 — the memorial)

**F-S1/F-S2/F-S4/F-S5/F-S6/F-S7: clean (verifier-hunted). F-S3: TWO instances of the
NAMED error class fired and were cured — memorialized here per A2:**

1. **The derivation's SELF-CATCH (pre-verifier):** an earlier draft of the W2 witness
   claimed "W2 (the field sector alone) is LE under P1" — a field-sector-only gloss
   (the field-only tuple with zero moduli slots FAILS H4(λ)). Caught during
   derivation; the shipped package carried only the corrected form (W2′ = field
   sector + the λ-slot 2p0·L̃₀), verifier-verified correct AND complete (the full
   tuple needs ONLY the λ-slot). The catch itself was memorialized nowhere until this
   report — that omission is what A2 cures.
2. **The verifier's CATCH (A1):** the anchored-log forcing claim "…whenever the field
   sector is nonzero" — an F-S3-class quantifier slip ("whenever/all" missing its
   exact condition) — REFUTED by the in-family V10b counter-construction; restated as
   the exact iff condition at every occurrence (script ×2, JSON ×2, stdout,
   EXACT_DERIVATION §1.2.6, the SLICE2_SURFACE echo, the ledger H4 text) and banked
   as three zero-residual `A1_*` checks.

**Method observation (recorded as directed):** this is the **THIRD external catch of
the named stratum-blind/quantifier-gloss error class** in this arc (Stage-2 round-1
A1: the R7(b) vacuity, a class-wide-vs-per-member stratum gloss; Stage-2 closure C3:
"only genuine cut = k_mod = 0", a stratum-blind uniqueness gloss one level down;
Stage-3 A1: the anchored-log "whenever", a quantifier missing its exact condition).
The recurring shape is unchanged: an all/whenever/only claim written one level below
the last verified stratum/condition. **The named-falsifier mechanism worked as
designed — F-S3 was pre-registered as the class to hunt FIRST, the verifier hunted it
first, and found it**; the derivation-side self-catch (item 1) shows the discipline
beginning to internalize, but the external catch was still needed. Standing
corrective (Stage-2's, re-affirmed): stamp every universal claim with the exact
condition/stratum at which it was actually proven.

## LIMITS THAT TRAVEL

1. **Exhaustive layer** = jet ≤ 2 in the varied fields, registered positive
   triangular chart, registered stationary one-parameter presentation, off-shell,
   polynomial/formal in the (k10, C) moduli, BASE branch (BR-A carries the same
   theorems at jet ≤ 2; BR-M/BR-CE typed NOT-EXHAUSTED). **Jet 3/4: typed via the
   order-4 self-adjointness anchor (2-field instance) only — TYPED-NOT-EXHAUSTED**
   (the Bach-side class lives here; "extension required", never "excluded").
2. **Pairing branches ENUMERATED, NOT adopted (F-S2):** every G3 statement carries
   its pairing-branch label or a PROOF of branch-independence (W3); P1's volume and
   per-slot weights and P2's distributional class remain OPEN supplied structure.
3. **Strata carried:** GENERIC / KMOD0 adjudicated (their identity content banked
   and exhaustive at codim 1); **all 10 RES-CNEQ0 composite rows CENSUS-REQUIRED**
   (resonance rule; blocked on the queued deeper resonance-census tile); nonemptiness
   is WITNESS-LEVEL, not a full-cell census; corners typed-only.
4. **Slice-1 only — no solution-dependent leg run (F-S6):** no solution of 𝓡 = 0, no
   R5/R14, no gate 2, no gate-1 on-shell leg, no gate-4 current leg, no completion
   class (L4), no boundary-data choice (BR-B); sufficiency of the Helmholtz
   conditions = the banked bicomplex statement (Category-A, cited) + witness
   instantiation.
5. **No member selected, no physics (F-S1; ceiling respected):** known-object rows
   are observations; the full ℛ = ℛ_PW ∩ {WS/GC} could still be empty, a point, or a
   family (J15); adjudication stays with Charles.
6. **F-S7:** the twisted-H¹ analog row is MODEL-KNOWLEDGE — flag carried on every
   J07/J11-typed row; no banked G6 claim rests on it; a source check is owed before
   any load-bearing use.
7. **Verifier caveat**: same-session-spawned blind verifier, not a hosted external
   model.

## Evidence

`derive_routeA_stage3.py`: **52/52 checks, exit 0 = 33 substantive zero-residual
exact-SymPy checks + 19 citation guards** (49 pre-amendment — all surviving with math
and pass conditions unchanged (2 substantive detail strings amended, 3 kind-relabels
per A4) — + 3 new `A1_*` checks), ~61 s, single CPU process, deterministic (three
consecutive post-amendment runs: JSON sha256 a0371b62…3ccd, ledger sha256
652535b3…eb8a, stdout sha256 4f497a71…b7e6 — all byte-identical; full hashes in
`CORRECTION_LAYER.md` §3). `GATE_CUT_LEDGER.tsv` (34 rows = 30 composite + 4
observation), `routeA_stage3_results.json` (`amendments`, amended `check_split` and
`falsifier_record`), `DERIVATION_STDOUT.txt` — regenerated post-amendment.
`EXACT_DERIVATION.md` (A1/A3/A4-amended), `SLICE2_SURFACE.md` (A1-amended echo),
`CORRECTION_LAYER.md` (the amendment record), `PREREGISTRATION.md` (the frozen
contract).

## Verifier record

Blind adversarial pass, 2026-07-29 (zero-context framing; same-session-spawned;
**not a hosted external model** — caveat travels). Independent artifacts preserved
in-package (`VERIFIER_INDEPENDENT_CHECK.py`, `VERIFIER_INDEPENDENT_STDOUT.txt`):
**29/29 independent checks, exit 0**, own constructions throughout — independent jet
machinery and adjoint-comparison route; the condition system, the P1-4D shifts, all
four witnesses, the intertwining bijection (V4), the four-corner transversality with
the exact Stage-2 identity match (V5), the boundary census by own integration by
parts (V6/V7/V11), and the TC2/TC4 typing (V8/V9) all REPRODUCED; **the W3
branch-independence claim attacked and SURVIVED** (symbolic-a_F exponential defect,
nowhere zero; no moduli-slot rescue); **the V10b adversarial counter-construction
REFUTED the anchored-log quantifier as phrased** (the one broken claim — found by
hunting F-S3 FIRST, per contract). **Contract-first VERIFIED in git**
(PREREGISTRATION.md sole content of dbc114f; artifacts later-stamped).
Byte-identical rerun (49/49 pre-amendment). Verdict framing: ADJUDICATE, not
confirm. **A1 required, A2 required, A3 recommended, A4 minor — all four applied
and check-backed this pass** (`CORRECTION_LAYER.md`; rerun 52/52, exit 0,
deterministic ×3). Same-verifier closure per contract §6 remains OWED on the
restatements before the driver banks.

## SLICE-2 SURFACE (pointer — stated as a handle, NOT launched)

`SLICE2_SURFACE.md` (TC6) is the binding surface: per-cell remaining work for the 20
adjudicated cells (the WS legs R5/R14, gate 2, gate-1 on-shell, gate-4 currents —
all solution-dependent; gate-5 per-candidate wall depth; gate-6 completion/holonomy
data), the four gating forks (L4/BR-C, BR-B, L8/BR-A, the pairing supply), the
RES-CNEQ0 census blocker, and the cross-cell derivation tiles (P3 wall-block
symmetry, general-arena corners, restricted-EH G3 status, jet-3/4 parametrization if
a 4th-order candidate is declared). Slice 2 inherits NOTHING as decided; it requires
its own preregistration and Charles's go — nothing is launched by this report.
