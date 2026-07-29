# BLIND VERIFIER REPORT — P4 Route C Stage 1 (shared exact static sector)

Verifier: blind adversarial verifier, **same-session-spawned** (zero-context framing; the
standing caveat travels: this is NOT a hosted external model — an in-repo agent of the same
session lineage). Date: 2026-07-28. Contract adjudicated against: `PREREGISTRATION.md`
(committed at dfb39ac, BEFORE the derivation artifacts existed — contract-first confirmed in
git). Framing: ADJUDICATE, not confirm; refutation and pass were both first-class outcomes.

Independent artifacts written by this verifier (preserved in-package):
`VERIFIER_INDEPENDENT_CHECK.py` (own curvature engine + own Bach implementation + own
witness re-solves), `VERIFIER_INDEPENDENT_STDOUT.txt` (transcript).

## VERDICT: **PASS WITH REQUIRED AMENDMENTS** (verdict-preserving; listed exactly in §6)

The OC1 headline — all 7 independent restricted components INEQUIVALENT for the
(C2/Bach, EH+Λ) pair on the declared CHOSE domain, witnesses in both directions, every real
Λ covered — is CONFIRMED by full independent re-derivation. The two amendments are
documentation-level; neither touches any check, witness, or the verdict.

## 1. Rerun (Duty 1) — PASS

- `python3 derive_routeC_stage1.py`: exit 0, 32/32 checks PASS, 48.0 s single CPU process.
- Outputs byte-identical to the committed artifacts: `BACH_ODE_SYSTEM_FULL.txt`,
  `EH_ODE_SYSTEM_FULL.txt`, `SECTOR_COMPARISON_LEDGER.tsv` identical; `routeC_stage1_results.json`
  identical modulo the `elapsed_s` field; `DERIVATION_STDOUT.txt` identical modulo timestamps.
- Purity: exact SymPy only — grep found no floats, no randomness, no numpy, no evalf/.n(),
  no network imports. Deterministic (two runs identical).

## 2. Independent re-derivation (Duty 2) — PASS on every load-bearing claim

Own construction (not a copy): metric rebuilt from the TC1 census by expanding the one-forms
`-u(c_E dt + αA)² + u⁻¹A² + W(dx² + bh dy²)` myself; own Christoffel/Riemann/Ricci/Weyl code;
own Bach implementation `B_ab = ∇^c∇^d C_acbd + ½ R^cd C_acbd`.

**Engine validation & the sign/normalization attack surface (resolved):**
- Schwarzschild: Ricci=0, Weyl≠0, Bach=0 (V01). Non-Bach-flat control metric: B≠0 (V02).
- Finding worth recording: **Einstein metrics cannot pin the relative sign** of the two Bach
  terms (on Einstein members Cotton = 0 and R^cd C_acbd = Λ·tr C = 0, so both terms vanish
  separately — Schwarzschild–de Sitter passes even with the wrong pairing). The decisive
  discriminator is **conformal covariance**: B[Ω²g] = Ω⁻²B[g] (4D) holds for the +½ pairing
  and FAILS for the mixed −½ pairing; likewise r²·Schwarzschild (conformally-Einstein,
  non-Einstein) is Bach-flat only with the correct pairing (V03b). The package's tensor
  passes both ⇒ it is the genuine conformally-covariant Bach tensor.
- Convention-independence of the verdicts: recomputing in the opposite Riemann/Ricci sign
  convention (with its matching pairing sign) gives exactly −B — same vanishing locus (V03a).
  INEQUIVALENT/witness verdicts are therefore convention-independent.

**Full-system cross-check (strongest single check):** my independently recomputed restricted
Bach and EH+Λ systems match the package's `BACH_ODE_SYSTEM_FULL.txt` and
`EH_ODE_SYSTEM_FULL.txt` EXACTLY, all 7 components, same normalization (V04b/V04c). Mixed
x-row vanishing, Bach symmetry/trace-freeness, det g = −c_E²·bh·e^{4λφ} all reproduced.

**Witnesses (Duty 2b — all exceeded the required minimum):**
- **W-EXP** (φ=x, bh=e^{2x}, f=0, α=0, λ=−5/4), checked with the fully-independent engine on
  the concrete member metric built by me from the census: Bach ≡ 0 (all 16 components),
  Weyl ≠ 0 (genuinely non-conformally-flat), trace-free Ricci ≠ 0; the four diagonal EH legs
  would demand Λ = {−7/4, −1, 1/4, 1} simultaneously ⇒ fails EH+Λ for EVERY Λ including 0
  (V11a/V11b). The load-bearing decisive witness is CONFIRMED. Restriction-commutes-with-
  specialization verified on ALL 7 components, not just tt (V11c — stronger than C16b).
- **W-FLAT**: B ≡ 0, E = Λg ≠ 0 ∀Λ≠0 (V07). **W-EXP-CF**: Weyl ≡ 0, Bach ≡ 0, non-Einstein
  ∀Λ (V12).
- **Direction A re-solved on all 7 components** (not just 2): B_comp=0 with E_comp≠0, two
  witnesses with distinct exceptional Λ* each ⇒ every real Λ covered (V08). Also re-solved
  with a fresh verifier-chosen parameter/jet set (different primes, not in the package) on
  tt and yz — witnesses exist there too; the inequivalence is not an artifact of the
  package's chosen points (V08b).
- **Direction B re-solved on all 6 non-xx components with a deliberately DIFFERENT low-jet
  preference order** (fresh witnesses, not the package's): E_comp=0 at symbolic Λ (Λ-free
  linear coefficients and denominators verified), B_comp≠0, Λ-numerators gcd-coprime (V09).
- **xx even-parity/quadratic construction** (named attack surface — resolved): E_xx identity
  `E_xx|_{p0=0} = [4Λh0+(α²−1)f1²−4h0p1²]/(4h0)` verified zero-residual, λ and h1 confirmed
  absent (V06b); B_xx f-jet parity verified (V10a); the three witnesses' validity intervals
  INDEPENDENTLY re-derived from f1²≥0 (slope sign of 4h0/(1−α²)) = [0,∞), (−∞,1], (−∞,4] —
  union covers all real Λ (V10b); root cross-coverage redone with exact real-root isolation;
  the gcd-degree-0 criterion is sound over Q (a shared algebraic root would force a common
  factor) (V10c). Extra rigor: the α=2,3 witness points have g_zz = q < 0, but the metric is
  still Lorentzian (−,+,+,+) — the (t,z) block determinant is −c_E² < 0 identically — so
  they are genuine domain members (V10d).
- Jet-order split confirmed: every Bach component carries 3rd/4th jets; no EH component
  exceeds 2nd jets (V06a).

**Bach-flat branch & λ-seat (Duty 2d):** reproduced independently — off-diagonal Bach
vanishes on the exponential slice, every deweighted diagonal component is x-free and
divisible by (4λs+s²+4) (V13a); at λ=0, s²+4 has no real root AND the quotient system has no
common real root (Gröbner basis {s−2λ, 3λ²+1}) ⇒ no Bach-flat member on the slice at λ=0
(V13b). Scoping VERIFIED: both C17/C18 and the EXACT_DERIVATION bullet stamp the claim
SCOPED to the exponential subfamily — it is not stated family-wide. EH slice rigidity
independently re-solved: no (s,Λ) roots at k=1; flat member only with Λ=0 (V15).

**Containment (Duty 2e):** Einstein ⇒ Bach-flat spot-verified with my tensors on three
members (the flat in-domain member; Schwarzschild; de Sitter static patch with Λ=3/L²)
(V14, V01, V07). The package correctly FLAGS it as Category-A, slice-verified-only, NOT
re-proven on the full ansatz — no over-claim.

Final independent run: 28/28 checks PASS, exit 0, 48.7 s (`VERIFIER_INDEPENDENT_STDOUT.txt`).
Transparency: the first version of my own script had two test-DESIGN bugs (a mixed-pairing
probe on a Ricci-flat metric, where the pairing term vanishes identically; and a naive
expectation that the "discrete pair" be a quotient-system root). Both were my errors,
diagnosed and replaced with the decisive tests above; no package computation was at fault.

## 3. Falsifier hunts (Duty 3)

- **F-C1 (restrict-then-vary): CLEAN.** Both covariant tensors are unrestricted variational
  outputs evaluated on the ansatz afterwards. The Bach provenance citation is ACCURATE:
  `c2_finite_cell_boundary_variation_2026-07-20/AUDIT_REPORT.md` states verbatim "The
  unrestricted bulk equation is proportional to the Bach tensor" (line 29); the EH output is
  standard Category-A. The TC5 quotes (`P^abcd = 2 C^abcd`, "Current UDT premises select
  none of them", conformally-flat zero charge) all verified verbatim against the 07-20
  audit; J07/J08 wording verified verbatim against the 07-21 jet-matching atlas.
- **F-C2 (static-energy false pass): CLEAN.** The verdict rests on all seven components
  individually — including the lapse row tt, the momentum rows ty/tz, and the radial
  constraint xx — each with its own two-directional witnesses, plus system-level witnesses.
  No static-energy or E2+E4 shortcut anywhere.
- **F-C4 (quantifier slips, both directions): CLEAN — this was the sharpest hunt.**
  Condition 2 of the 07-18 record reads verbatim "one declared variation domain and the same
  exact finite-cell static equations on both" — EQUATION-equality. The subfamily-refutes-
  superset asymmetry is applied exactly to equation-sharing (valid: equal equation sets on a
  superset restrict to equal sets on the subfamily; they are unequal there), NOT to
  solution-set notions. The package does NOT conflate equation-inequivalence with an empty
  shared-solution sector: it states the one-way containment (every Einstein member is
  Bach-flat — so shared SOLUTIONS exist one-way) separately and explicitly says "shares
  solutions one-way is NOT the same exact equations". Inequivalence is stamped pair-scoped
  and domain-scoped; TC6 explicitly lists surviving alternatives (CM0-C, KER-R kernel
  deformations, BDY-TD variants) — NOT "route dead". No promotion of agreement occurred
  (none was found).
- **F-C5 (imposition/merit): CLEAN.** Every acceptance criterion is an exact algebraic
  identity or witness-existence check (provenance/honesty class); no solution filtered for
  shape; no spatial-infinity normalization appears anywhere (the EH-H3 stamp says NOT used,
  and it is not).
- **F-C6 (conditionality laundering): CLEAN in JSON + EXACT_DERIVATION (stamps at head,
  restated in TC4/TC6 and carried by the S26 re-stamp), with ONE letter-level gap — the
  stand-alone TSV ledger carries verdicts with no stamps in-file (amendment A2).
- S26 row dependency quoted accurately against
  `native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv` row S26 ("Native
  branch adoption or shared-sector theorem plus normalization"); the re-stamp narrows only
  the second leg, scoped — correct.

## 4. Contract compliance (Duty 4)

- TC1–TC6 all addressed; census table complete with chose-or-derived tags; λ seat symbolic
  throughout; Λ symbolic, never fitted; FULL family computed (no THROUGHPUT-LIMITED fallback
  needed — confirmed by rerun timing).
- TC5 is typed-only: jet-order requirements, corner/charge structure, J07/J08 classes, the
  BDY-TD threat — and explicitly "No boundary law is chosen here". Confirmed.
- Pre-registered outcome ceiling respected: no shared-sector theorem, no mass statement, no
  normalization, no candidate promoted/demoted as physics.
- The two development-time check failures are documented only in the derivation agent's
  return (not visible to this verifier) and in no in-package file. Adjudication by
  independent re-derivation: every final banked claim is mathematically confirmed, so
  whatever failed during development did not survive into the record — consistent with
  implementation-not-math. AUDIT_REPORT.md (the prereg-named deliverable, to be written
  after this pass) should preserve that failure record explicitly (note N1).

## 5. Refuted sub-claim (documentation-level, verdict-preserving)

The "**plus a discrete root pair λ = ±5√21/21, s = ∓2√21/7**" wording (EXACT_DERIVATION TC4
slice bullet; SECTOR_COMPARISON_LEDGER.tsv SYSTEM row; hand-written, not check-backed) is
REFUTED AS STATED: the pair satisfies 4λs+s²+4 = 0 exactly — it lies ON the one-parameter
branch (it is a redundant `sp.solve` output at the points where the y-component's quotient
also vanishes), and the quotient system has NO common root (Gröbner basis {s−2λ, 3λ²+1}, no
real solutions). The Bach-flat locus on the slice is the branch ALONE. Counter-computation:
`VERIFIER_INDEPENDENT_CHECK.py` V13c. No check, witness, or verdict depends on this
sentence; C17 itself (divisibility) is correct and independently reproduced.

## 6. Required amendments (exact list)

- **A1.** In `EXACT_DERIVATION.md` (TC4, "Slice structure behind W-EXP" bullet) and the
  `SECTOR_COMPARISON_LEDGER.tsv` SYSTEM row (and the hand-written `sys_rows` text in
  `derive_routeC_stage1.py` that generates it): delete or reword "plus a discrete root
  pair λ = ±5√21/21, s = ∓2√21/7" — the pair lies on the branch (see §5). Suggested wording:
  "the branch alone (a solver-output pair at λ=±5√21/21, s=∓2√21/7 lies ON it)".
- **A2.** F-C6 letter-compliance for the stand-alone ledger: add the three stamps (domain
  CHOSE; strong-CSN CHALLENGED on the C2 side; CONDITIONAL_NOT_SELECTED on the EH side) as
  a header comment line or column to `SECTOR_COMPARISON_LEDGER.tsv` (via the generating
  script, then regenerate), so the verdict-bearing TSV carries its stamps in-file.
- **N1 (note, not a defect).** When `AUDIT_REPORT.md` is written, record the two
  development-time check failures and their implementation-level resolution in-package.

## 7. Scope of this verification (limits that travel)

Same-session-spawned verifier (not a hosted external model). The comparison domain remains
CHOSE; both candidates remain conditional (strong-CSN CHALLENGED / CONDITIONAL_NOT_SELECTED);
the negative is pair-scoped and domain-scoped; conditions 1, 3–6 of the 07-18 fork are
untouched by Stage 1 — nothing here discharges them. This report verifies the mathematics
and the honesty of the record; it selects no physics.

---

## AMENDMENT CLOSURE (same blind verifier, 2026-07-28 — adversarial re-check, not confirmation)

**Closure verdict: CLOSED.** All amendments applied correctly, check-backed, and
verdict-preserving; no new defect found.

1. **Rerun:** `python3 derive_routeC_stage1.py` → exit 0, **33/33** checks PASS, 48.0 s.
   New check `C17b_pair_lies_on_branch` PASSES (both sign choices of the former "pair"
   substituted into 4λs+s²+4, zero-residual) — my V13c refutation is now check-backed in
   the derivation itself. Rerun outputs byte-identical to the committed amended artifacts
   (TSV and both ODE-system files identical; JSON identical modulo `elapsed_s`; stdout
   identical modulo timestamps). JSON diff vs the pre-amendment run I verified: exactly
   ONE added check (C17b), zero removed, zero changed top-level fields (witness data,
   jet signatures, slice polys, stamps, scope all identical).
2. **A1:** the "plus discrete roots" claim is gone/corrected in all three places
   (EXACT_DERIVATION.md TC4 slice bullet; ledger SYSTEM row; script `sys_rows` text).
   The corrected statement — branch **ALONE**, pair lies ON the branch, quotient-system
   Gröbner basis {s−2λ, 3λ²+1} with no real solutions — matches my V13c computation
   exactly. `BACH/EH_ODE_SYSTEM_FULL.txt` unchanged from the versions I verified.
3. **A2:** `SECTOR_COMPARISON_LEDGER.tsv` now opens with three `#`-prefixed STAMP header
   lines (domain CHOSE; c2_side strong-CSN CHALLENGED; eh_side CONDITIONAL_NOT_SELECTED),
   matching the script's `STAMPS` dict; the file parses cleanly (9 data rows × 7 columns
   skipping `#` lines). The seven per-component verdict rows AND the column header are
   **byte-identical** to the pre-amendment rows I verified; only the SYSTEM-row wording
   changed (the A1 correction), as claimed.
4. **N1:** `AUDIT_REPORT.md` "Development-time record (N1)" preserves both development
   failures with resolutions consistent with implementation-not-math, and both
   resolutions are visible in the final structure (the failed W-EXP point at s=2, λ=−1 is
   exactly the conformally-flat member banked as W-EXP-CF/C16c, which I independently
   verified; the xx linear-solve failure is exactly why the quadratic/parity construction
   exists, which I independently verified V10a–d). The verifier-record section represents
   my findings faithfully: 28/28 independent checks, fully-independent Bach engine,
   conformal-covariance convention discriminator (with the Einstein-metrics-cannot-pin-
   the-sign finding), fresh direction-B witnesses at a different jet order, A1/A2,
   PASS-WITH-REQUIRED-AMENDMENTS verdict-preserving, and the same-session/not-hosted
   caveat at both the grade line and the verifier record.
5. **CORRECTION_LAYER.md did-NOT-change list HOLDS:** verified by byte comparison against
   my pre-amendment snapshots — OC1 verdict, all witnesses, all seven component verdicts
   and jet signatures (byte-identical ledger rows), TC6 re-grade, S26 re-stamp, TC5
   typing, containment statement, C01–C18 all unchanged; both ODE-system files
   byte-identical; the only deltas are C17b, the SYSTEM-row wording, the TSV stamp
   header, and the documentation corrections.

Caveat travels: same-session-spawned blind verifier, not a hosted external model.
Nothing committed to git by the verifier.
