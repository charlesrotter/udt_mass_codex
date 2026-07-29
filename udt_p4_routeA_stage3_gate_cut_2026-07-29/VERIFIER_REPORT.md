# BLIND VERIFIER REPORT — P4 Route A Stage 3 (Slice 1): the candidate-free gate cuts on ℛ_PW

Date: 2026-07-29. Verifier: blind adversarial verifier, **same-session-spawned** (zero-context
agent in the same Claude Code session — NOT a hosted external model; the independence caveat
travels with every use of this report). Framing: ADJUDICATE, not confirm. Contract:
`PREREGISTRATION.md` (verified contract-first in git: commit dbc114f contains ONLY the
preregistration, committed 2026-07-29 09:38, before every derivation artifact, all of which are
still uncommitted working-tree files). Independent script preserved:
`VERIFIER_INDEPENDENT_CHECK.py` (29/29 own-construction checks, exit 0, ~7 s;
`VERIFIER_INDEPENDENT_STDOUT.txt`).

## VERDICT: PASS-WITH-REQUIRED-AMENDMENTS

The rerun is byte-identical and exact; the condition system, the pairing-relative partition,
the intertwining bijection, all four witnesses, the four-corner transversality, the boundary
census, and the typing tables were independently re-derived and REPRODUCED; the falsifier
record is clean EXCEPT one F-S3-class quantifier slip in the anchored-log forcing claim, which
I refuted by an in-family counter-construction (A1 below). The refuted phrasing is one strand
of TC1 prose/detail-strings; the computations behind it are correct and the corrected statement
is strictly narrower — amendment, not demolition.

## Duty 1 — rerun, determinism, contract-first, check-split audit

- `python3 derive_routeA_stage3.py`: exit 0, ~61 s, single CPU process. 49/49.
- `routeA_stage3_results.json` and `GATE_CUT_LEDGER.tsv` byte-identical to the committed-tree
  copies (sha256 9d0c97d8…, c58894c5…); stdout byte-identical to `DERIVATION_STDOUT.txt`.
- Exact SymPy only: no floats, no randomness, no network, no time-dependence (the only
  `import os` is for output paths).
- Contract-first: VERIFIED in git (dbc114f = preregistration alone; artifacts written
  10:09–10:12, after).
- **Check-split audit (33 substantive + 16 guards):** the 16 guards are honestly labeled
  in-script, in stdout (`[guard]`), and in the JSON. HOWEVER, 3 of the 33 "substantive" checks
  are guard-grade in computational content:
  1. `TC4_torsion_period_vacuous` — `solve(2P=0)` is trivial arithmetic; the torsion-period
     argument lives in the detail string.
  2. `TC1_no_empty_adjudicated_cell` — a re-aggregation of booleans already checked upstream.
  3. `TC2_kmod0_identity_is_row_dependency` — its `dep_vec − IDENT` leg compares an expression
     to itself re-typed (tautological); the nullspace leg repeats `S0`; the load-bearing
     content (R_kmod = 2·r_tf) is a Stage-2 CITATION (which I verified independently, V5).
  Honest substantive count ≈ 30. See amendment A4.

## Duty 2 — independent re-derivation (own constructions, `VERIFIER_INDEPENDENT_CHECK.py`)

**(a) Pairing-relative variationality (attacked hardest): REPRODUCED; attacks failed.**
Own jet machinery and adjoint comparison (different data layout and construction route):
- Conditions = Fréchet self-adjointness; necessity on the generic EL image under P2 (V1);
  non-vacuity of my checker verified on a known-NV probe (V1b).
- P1-4D branch: condition (i) weight-cancels (pairing-independent across the anchored family);
  condition (ii) shifts by exactly −2·a_F·p1·∂R/∂u″ (V2).
- Witnesses all reproduced (V3): W1 LE(P2)/NV(P1-4D) with defect −4λp1e^{2λp0} vanishing
  exactly at the T4 blindness locus λ=0; W2 field sector = p2 + λ(p1²−f1²−h1²) LE(P1)/NV(P2)
  with the field-only tuple FAILING H4(λ) (the package's self-corrected statement is CORRECT);
  the generated λ-slot is exactly 2p0·L̃₀; ω-shape LE(P2)/NV(P1, a_M=2λ).
- The intertwining bijection: e^{±a_F p0} touches only (λ, p0), both K₄-inert; exactly
  invertible; R ↦ W_F R sends the P1 partition onto the P2 partition (V4). Isomorphic-but-
  distinct is right (distinctness witnessed by W1/W2 changing cells off the blindness loci).
- **W3 branch-independence attacked and SURVIVED:** Hi1(p,p) = 2e^{a_F p0} for SYMBOLIC
  a_F(λ) — an exponential, nowhere zero on any real branch; and the failing condition is
  field-field, involving no moduli component, so no choice of moduli slots can rescue W3
  (V3_W3_*). The "proven branch-independence" claim is genuine.

**(b) The anchored-log forcing: REFUTED AS PHRASED — the one broken claim (amendment A1).**
The claim (script details `TC1_H4_witness_lambda_slot_contains_log` /
`TC1_both_volumes_same_dlambda` context, JSON `pairing_dependence_map`, EXACT_DERIVATION
§1.2.6, echoed in SLICE2_SURFACE §2 LE×KMOD0): the LE cell's λ-slot carries forced
log(c_E/Q)-dependence "**whenever the field sector is nonzero**."
Counter-construction (V10b, in the package's own working class — the generic L̃ of its H4/H5
checks depends smoothly on all moduli, and the banked alphabet is "polynomial/FORMAL in the
moduli, smooth in the rest" with anchored (c_E/Q)^a forms admitted, moduli-dependent exponents
precedented by the banked e^{φX} closed forms):
take L̃ = e^{−2λp0}·L̃₀, so the generated action S = W_F·L̃ = L̃₀ is λ-independent. The member
R_a = e^{−2λp0}(p2, f2, h2), ALL moduli slots ZERO, then satisfies every LE condition under
P1-4D ((i)–(iii), H4 for every modulus, H5 — all checked zero-residual) with a NONZERO,
genuinely λ- and p0-dependent field sector and NO log anywhere.
The TRUE statement (verified V10a/V10c): the λ-row reads E_a(W_M R_λ) = ∂λ(W_F R_a) =
W_F[∂λR_a + a_F′·p0·R_a]; the λ-slot is forced nonzero **iff ∂λ(W_F R_a) ≢ 0 for some a** —
in particular for EVERY λ-independent nonzero field sector (where the forcing and its log
factor are real; the generated witness R_λ = 2p0L̃₀ stands). This is exactly the F-S3 error
class: an "whenever/all" quantifier missing its exact condition. The claim IS correctly framed
as forced structure (not an obstruction, not a selection) — the framing duty passes; only the
quantifier is overbroad.

**(c) Transversality: REPRODUCED (V5).** All four (G3-cell × identity-cut) corners on KMOD0
under P2 populated exactly as the ledger says; the violating corner violates only where
k10 ≠ 0 — scope stamp correct.

**(d) Boundary census: REPRODUCED (V6, V7, V11).** Own integration by parts: N=2 slots =
0-jet traces with 1-jet momenta (self-pairable at wall grade 2 under the banked trace-jets ≤
grade−1 rule); N=4 pairs {v, v′} and the v-momentum contains 3rd jets → wall grade 4 →
structurally unable within jet ≤ 2. Parity-halving reproduced. The Route C TC5 instances
(1-jet wall + K-momenta vs 2-jet wall + 3rd-normal-derivative momenta; Hayward vs
trace-free-Weyl corners) match the Route C bank verbatim. **The scope stamp is correct
everywhere I hunted: "typed jet-3/4 extension required / NOT-EXHAUSTED" — never "Bach class
excluded"** (script, EXACT_DERIVATION §3, ledger G5 column, JSON). P3 bulk inheritance:
reproduced with a DIFFERENT interior-supported variation pair (note: my first pair was
x↔1−x-symmetric, which gives zero defect trivially — my construction error, fixed with an
asymmetric pair; the package's pair is asymmetric and correct).

**(e) The self-caught F-S3 instance (W2 "LE under P1" was field-sector-only):** the
RESTATEMENT is correct and complete — I verified the field-only tuple fails exactly H4(λ) and
that the full W2′ needs ONLY the λ-slot (H4 for every other modulus holds with zero slots,
since L̃₀ carries no other moduli dependence). HOWEVER the catch itself is memorialized
nowhere in the package (no AUDIT_REPORT.md yet; the prose presents only the corrected form).
See amendment A2.

**(f) TC2/TC4 typing: REPRODUCED (V8, V9, V5b).** Generic stabilizer rank 6 (no pointwise
identity, GENERIC scope); k_mod=0 nullspace dim 1 (one algebraic identity ↔ one gauge
direction — "balanced" is a COUNT, not a solvability claim; F-S6 clean); the row dependency
with R_kmod = 2·r_tf, R_C = M is EXACTLY the banked Stage-2 identity
(PW3_component_pairings mapping verified — F-S4 clean); no Bianchi-type identity assumed
anywhere (disclaim carried in script, prose, ledger — matches the STAGE3_HANDOFF warning);
K₄ all-torsion recomputed and the vanishing-by-torsion statement scoped to CLOSED forms on
TORSION cycles in every occurrence; F-S7 flags present on every J07/J11-typed row and both
ledger G6 texts — no banked G6 claim rests on the twisted-H¹ MODEL-KNOWLEDGE row (the torsion
vacuity is own-computed; everything else is an obligation TAG or cites the banked Route B T3
cocycle type).

## Duty 3 — falsifier hunts (F-S3 first)

- **F-S3:** ONE instance found = the anchored-log "whenever" (A1; details above). Otherwise
  clean across the 34 ledger rows, EXACT_DERIVATION, and SLICE2_SURFACE: the ledger header
  carries the global scope stamp; "no pointwise identity" is stratum-scoped; "exhaustive
  layer" = the banked jet ≤ 2 designation; "all witness-nonempty" is scoped witness-level;
  "pairing-independent" claims are scoped to the enumerated anchored family.
- **F-S1:** clean. No member selected/privileged/ranked; the four known-object rows are
  observations; SLICE2_SURFACE does not pre-rank (its "potentially harder than LE" is a cost
  shape of the VERIFICATION work per cell, with both cells kept first-class).
- **F-S2:** clean. Every G3 statement carries its pairing label; W3's branch-independence is
  a genuine proof (re-derived symbolically).
- **F-S4:** clean on everything checked: the k_mod=0 identity, the R_kmod = 2r_tf slot
  mapping, the T4 blindness loci (λ=0 / λ=−1/2 vs exponents 2λ / 1+2λ), the Route C TC5
  instances, the resonance shear-identity example, the wall-alphabet rule, the amended cut
  structure (k_mod=0 the only codim-1 cut; C≠0 sub-varieties CENSUS-REQUIRED). One noted
  TENSION, flagged not broken: Stage-2's "bare φ excluded" headline vs Stage-3's
  "anchored-depth log alphabet-legal at supplied c_E" (`J0_anchored_relabeling`) — reconciled
  by the same anchored/supplied-c_E reading Stage-2 itself uses to admit (c_E/Q)^a; a
  one-line reconciliation note would close it (A3).
- **F-S6:** clean. TC2's "balanced" = a count; TC3's "CAN self-pair" = slot-availability
  typing; no existence/closure/current/mass claim anywhere.
- **F-S7:** clean (see 2f).

## Duty 4 — contract compliance

- TC1–TC6 all addressed (TC6 = `SLICE2_SURFACE.md`, a handle not a launch — verified: no leg
  run, no fork decided).
- **Resonance rule:** all 10 RES-CNEQ0 composite rows are CENSUS-REQUIRED with G5/G6
  DEFERRED; none adjudicated (verified row-by-row).
- **Slice-1 boundary:** nothing from the OUT list run — no solution of 𝓡=0, no gate-2
  sector selection, no R5/R14, no gate-4 current leg, no completion class, no boundary-data
  choice, no pairing adopted.
- **Ceiling:** respected — the strongest claim made is exactly the pre-committed maximum
  (the partition map, per branch and stratum, with CENSUS-REQUIRED cells and open forks; the
  L6 fork = the computed partition); OS1 is the honest outcome class (OS2/OS3 correctly not
  triggered at the declared witness-level scope).
- Deliverables: `AUDIT_REPORT.md` (contract §3) is not yet present — consistent with the
  contract's §6 ordering (audit after the verifier round), but it is OWED before commit and
  must absorb A2.
- Anti-hang: 61 s single process, pure CPU — bounded, full declared scope, honestly stamped.

## REQUIRED AMENDMENTS

- **A1 (required — the load-bearing one).** Restate the anchored-log forcing with its exact
  condition everywhere it appears (script detail strings at lines ~395 and ~1140, the JSON
  `pairing_dependence_map` entry and check detail, `EXACT_DERIVATION.md` §1.2.6, and the
  SLICE2_SURFACE §2 LE×KMOD0 echo): the λ-slot is forced (and log-carrying via the a_F′·p0
  term) **iff ∂λ(W_F R_a) ≢ 0 for some field slot** — in particular for every λ-INDEPENDENT
  nonzero field sector; NOT "whenever the field sector is nonzero" (in-family counterexample
  on record: `VERIFIER_INDEPENDENT_CHECK.py` V10b — R_a = e^{−2λp0}(p2,f2,h2), moduli slots
  zero, fully LE under P1-4D, zero λ-slot, no log).
- **A2 (required).** When `AUDIT_REPORT.md` is written, memorialize BOTH the derivation's
  self-caught W2 field-only gloss (currently only the corrected form appears) and this
  verifier-caught anchored-log quantifier slip, as F-S3-class catches.
- **A3 (recommended).** Add a one-line reconciliation of Stage-2's "bare φ excluded" with
  Stage-3's anchored-depth-log legality (the supplied-c_E anchored reading), so the F-S4
  tension is closed in-file.
- **A4 (minor).** Reclassify or footnote the three guard-grade "substantive" checks
  (`TC4_torsion_period_vacuous`, `TC1_no_empty_adjudicated_cell`,
  `TC2_kmod0_identity_is_row_dependency`); the honest substantive count is ~30/33.

Same-verifier closure per contract §6: after A1/A2 edits, this verifier (or its successor
with this report) should confirm the restatements and the byte-identity of a rerun.
NOT committed by the verifier (per instruction).

---

# AMENDMENT CLOSURE (same verifier, 2026-07-29 — adjudicated, not confirmed)

## VERDICT: CLOSED

All four amendments verified applied, check-backed, and verdict-preserving. No new defect
found under attack.

1. **Rerun: PASS.** `derive_routeA_stage3.py` exit 0, ~60 s, **52/52 = 33 substantive + 19
   guards**; JSON/ledger/stdout byte-identical to the shipped artifacts (sha256 a0371b62…,
   652535b3…, 4f497a71… — matching `CORRECTION_LAYER.md` §3). All 49 pre-amendment check
   NAMES survive (set-compared programmatically); exactly the 3 `A1_*` checks added;
   arithmetic reconciles (30 + 3 new = 33 substantive; 16 + 3 reclassified = 19 guards).
2. **A1: CLOSED.** The three new checks are genuine zero-residual instantiations of my
   derivation, ATTACKED and sound: `A1_V10b_counterexample_LE_zero_lambda_slot` rebuilds my
   V10b member exactly (S = W_F·L̃ = L̃₀ enforced symbolically; field-field conditions via
   the package's own Helmholtz machinery; H4 over ALL seven moduli with zero slots; the
   field sector verified ≡ e^{−2λp0}p2 and genuinely λ- and p0-dependent);
   `A1_anchored_log_iff_condition` proves the zero-slot H4(λ) residual identity on the
   GENERIC member with SYMBOLIC a_F and instantiates BOTH directions (counterexample side
   all-zero; W1's p-row forcing side nonzero) — the iff logic is sound (residual = 0 ⇒
   zero slot admissible = not forced; residual ≠ 0 ⇒ any LE completion needs R_λ ≠ 0);
   `A1_lambda_independent_sector_forcing_real` = my V10c. The corrected statement is
   installed and matches my derivation exactly at EVERY occurrence I had listed — script
   ×2 (the `TC1_H4_witness_lambda_slot_contains_log` detail and the JSON-map text), JSON ×2
   (`pairing_dependence_map` + check detail) plus the `field_moduli_H4` line and the new
   `amendments` block, stdout, `EXACT_DERIVATION.md` §1.2.6 (fully restated; scope stamps:
   the two enumerated λ-dependent P1 instances, jet ≤ 2, stationary presentation, BASE
   branch), the `SLICE2_SURFACE.md` §2 LE×KMOD0 echo (the iff carried into the
   candidate-declaration duty), and the ledger LE-row H4 text. **Grep-verified: every
   remaining "whenever" string in the package is a negated quotation (NOT '…'), a memorial
   of the catch (AUDIT_REPORT/CORRECTION_LAYER), or a verifier artifact.** Bonus:
   `TC1_W2_LE_P1_NV_P2` and §1.2.3 now tie the field-only H4(λ) failure to the iff
   condition — correct.
3. **A2/A3/A4: CLOSED.** A2 — both F-S3 catches memorialized in `AUDIT_REPORT.md`'s
   falsifier record AND `EXACT_DERIVATION.md` §6, with the third-catch method observation
   (Stage-2 A1 / Stage-2 C3 / Stage-3 A1 — the recurring one-level-below-verified shape;
   accurately recorded, incl. that the named-falsifier mechanism worked as designed). A3 —
   the reconciliation line is present in §1.2.6 (echoed in the JSON and AUDIT_REPORT) and
   is correctly anchored: log(c_E/Q) legality via the SAME supplied-c_E anchored reading as
   Stage-2's (c_E/Q)^a entries, explicitly no bare-φ readmission, the Stage-2 anchoring
   rule cited. A4 — kind-relabel ONLY, verified against my in-context pre-amendment copy:
   the three checks' pass conditions and detail strings are byte-identical; only the
   guard-set membership changed (with an honest in-code comment recording the
   reclassification).
4. **CORRECTION_LAYER's did-NOT-change list: VERIFIED by comparison.** OS1 unchanged; the
   partition/condition system, all witnesses (W3's branch-independence condition
   `expand(z1−2·WF)==0` untouched), the four-corner transversality (`four_corner`
   untouched), the boundary census + scopes (N=4 "typed extension required", never
   "excluded"), TC2/TC4 typing conditions, the 30-cell map (recounted: 20
   ADJUDICATED-NONEMPTY + 10 CENSUS-REQUIRED; ZERO RES-CNEQ0 rows adjudicated), the 4
   observation rows, and the 20 ledger F-S7 flags all unchanged; the only ledger delta is
   the LE-rows' H4 conditions text, as claimed.
5. **AUDIT_REPORT.md: FAITHFUL** to my findings — contract-first-in-git, the 29/29
   independent record, the W3 attack survival, V10b + the iff adoption, the A1–A4
   disposition, the bare-φ tension resolved via A3, the same-session-spawned /
   not-a-hosted-external-model caveat carried, the ceiling/F-S1/F-S6 limits intact, and
   Slice-2 stated as a handle, not a launch.

Residual notes (non-blocking): AUDIT_REPORT's "deterministic ×3" rests on the amendment
agent's three-run record — I independently confirmed determinism on my own rerun
(byte-identical); the F-S7 source-check duty and the RES-CNEQ0 census blocker remain open
Slice-2/queued items, correctly carried. NOT committed by the verifier (per instruction).
