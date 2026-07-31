# Stage T1 — CORRECTION LAYER (verifier round 1)

Date: 2026-07-31. Amendment agent record. The blind adversarial verifier returned
PASS-WITH-REQUIRED-AMENDMENTS (three amendments, none refuting; OT-1 stands; verdict +
attack script preserved in `AUDIT_REPORT.md` and `VERIFIER_INDEPENDENT_CHECK.py`, both
untouched by this layer). This page records what was WRONG, why it mattered, and exactly
what was changed. Nothing here alters the outcome class: OT-1 and the C-1 static-recovery
control are unaffected by all three amendments.

## AM-1 — an overstated residual-group claim (honesty error, derivation-level)

**What was wrong.** The package claimed "preserving the registered spatial row forces
ψ′ = 0" (check then named `T1p_registered_spatial_pin_kills_psi`) and "the full residual
group acts on N by sign only" via `T1r`, presenting the ψ-slack as fully frozen on the
registered chart. In fact the SPATIAL PIN ALONE gives ψ′ ∈ {0, −2N/g_tt}; the claimed
uniqueness silently used the shift-row equation as a SECOND pin — a pin on a varied field.
The second branch is a LAWFUL residual chart map on strata where 2Ne^{2φ}/c² is
t-independent: it preserves the clock row, the spatial row, and BOTH lock readings, and
flips N → −N (verifier attacks V5a/V5b).

**Fix (implemented).** New zero-residual checked steps `T1p2_spatial_pin_alone_two_branches`
and `T1p3_Z2_residual_branch_flips_N_stratum_conditional` (matching V5a/V5b); `T1p` renamed
`T1p_spatial_and_shift_pins_jointly_kill_psi` with an honest note; `T1r`'s note restated.
The residual-group claim now carries the stratum-conditional ℤ₂ ψ-branch everywhere it
appears: EXACT_DERIVATION §1.1 leg 3 + §1.2, ledger rows O16/O17/J10, results JSON.

**What survives.** Irreducibility-as-non-removability: the orbit of N under ALL residual
maps is {N, −N} — the new branch flips N's sign, it never removes N.

## AM-2 — an unstamped LOAD-BEARING fork (the important one)

**What was wrong.** The package derived the lock-reading fork (coordinate vs projected —
`T1k`/`T1l`/`T1m`) and, separately, the shift row's irreducibility (O17), presenting them
as independent facts. They are not independent: under a PROJECTED-reading spatial
registration (pin γ_xx, not g_xx), ψ′ = −N/g_tt is lawful wherever N/g_tt is t-independent
and REMOVES the shift entirely — the chart goes diagonal with g′_xx = γ_xx, clock row and
projected lock reading exactly preserved (verifier attack V5c). So O17's "N irreducible on
the registered chart" is CONDITIONAL on the COORDINATE-reading (i) spatial pin, and the
fork is not cosmetic: it decides whether the time-live domain has an irreducible shift
degree of freedom (coordinate reading) or the shift is pure gauge on the registered chart
(projected reading) — physical content for Stage T2.

**Fix (implemented).** New zero-residual checked step
`T1p4_projected_reading_pin_makes_N_removable` (matching V5c). The conditionality stamp is
now on O17 and every statement riding N's irreducibility (grep-audited): EXACT_DERIVATION
§1.1 legs 3–4, §1.2, §1.3 O17, TT-4 R_N bullet, §5.2; ledger O16/O17/R02/J10; results JSON
outcome class; DECISION_SURFACE items 2–3 and the T2 section. The fork is UPGRADED to
LOAD-BEARING in the ledger (O16 tag: LOAD-BEARING OPEN-FORK) and the decision surface.

**Not resolved (F-T4 honored).** Nothing in this package decides the fork, and no banked
structure genuinely constrains it: canon (CANON.md:186–217) states the reciprocal lock on
the diagonal stratum, where the two readings coincide identically (`C2a`), and is silent on
the shift-on extension; canon's own line is that DIAGONAL is a choice. Both branches travel
to Stage T2 with full stamps; deciding the reading is a registration choice owed to Charles
or a future derivation.

## AM-3 — bookkeeping inflation (~2) and a latent guard

**What was wrong.** (a) `G1` was appended AFTER the tally/JSON write: a G1 failure could
not flip the exit code (latent, harmless this run). (b) The guard enumeration in
EXACT_DERIVATION §5.4 listed G1 but omitted the actually-counted guard
`T3b_lorentzian_det_negative_diagonal`. (c) `C1b` (a literal copy of the banked class
table; the no-migration claim is ledger-derived, not computed) and `T4a` (compares two
self-authored lists; bank-faithfulness was certified only by the verifier's independent
V12) were graded SUBSTANTIVE — an inflation of ~2.

**Fix (implemented).** G1 is wired into the tally/JSON/exit path (JSON written,
round-tripped, G1 checked and COUNTED, JSON rewritten with final counts; a G1 failure now
exits nonzero). Guard enumeration reconciled (12 guards listed exactly, T3b_lorentzian
included). C1b and T4a re-graded GUARD/declaration-grade with amendment notes.

**Counts, old → new.** Old: "42 checks = 33 SUBSTANTIVE + 9 GUARD" (+1 latent G1 = 43
executed). Honest recount of the same content: 43 = 31 SUBSTANTIVE + 12 GUARD (matching
the verifier's ≈31 estimate). With the three amendment derivations (T1p2/T1p3/T1p4, all
substantive): **46 checks = 34 SUBSTANTIVE + 12 GUARD, 46/46 pass, exit 0, deterministic
(byte-identical reruns)**.

## Scope of this layer

Files changed: `derive_timelive_T1.py`, `TIMELIVE_T1_LEDGER.tsv`, `EXACT_DERIVATION.md`,
`DECISION_SURFACE_UPDATE.md`, regenerated `DERIVATION_STDOUT.txt` +
`timelive_T1_results.json`, this file (new). NOT touched: `PREREGISTRATION.md` (frozen),
`VERIFIER_INDEPENDENT_CHECK.py`, the verifier section of `AUDIT_REPORT.md`; the
pre-verifier derivation self-audit in `AUDIT_REPORT.md` still shows the OLD counts
(42/42, 33+9) and the old T1p/T1r wording — superseded by this layer, left as the honest
historical record of what the verifier caught. `VERIFIER_INDEPENDENT_CHECK.py` re-run
after all edits: 20/20 pass, exit 0 (its V11 ledger parse and V5 attacks remain valid
against the amended package). Nothing committed to git by this agent.
