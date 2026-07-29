# CORRECTION LAYER — P4 Route C Stage 1 (amendments A1 + A2, per VERIFIER_REPORT.md)

Date: 2026-07-28. Branch: grok. Amendment agent (post-verifier), applied against the
blind verifier's verdict **PASS WITH REQUIRED AMENDMENTS (verdict-preserving)**
(`VERIFIER_REPORT.md` §5–§6). Nothing here changes any check result, witness, component
verdict, or the OC1 outcome class — the amendments are documentation-level (A1) and
letter-level stamp compliance (A2), exactly as the verifier graded them.

## 1. Original claims (as they stood pre-amendment)

- **EXACT_DERIVATION.md, TC4 "Slice structure behind W-EXP" bullet:** the slice
  Bach-flat structure was stated as "a ONE-PARAMETER Bach-flat branch — **plus a
  discrete root pair `lambda = ±5√21/21, s = ∓2√21/7`**".
- **SECTOR_COMPARISON_LEDGER.tsv, SYSTEM row:** "...Bach admits the one-parameter
  branch 4 lambda s + s^2 + 4 = 0 **plus discrete roots (lambda = +/- 5 sqrt(21)/21,
  s = -/+ 2 sqrt(21)/7)**".
- **derive_routeC_stage1.py, `sys_rows` text:** the hand-written string generating the
  ledger SYSTEM row, same wording. The "plus discrete roots" sentence was hand-written
  and **check-free** — no zero-residual check backed it.
- **SECTOR_COMPARISON_LEDGER.tsv as a stand-alone file:** carried its INEQUIVALENT
  verdicts with **no conditionality stamps in-file** (stamps lived only in the JSON and
  EXACT_DERIVATION.md).

## 2. Verifier findings (cited from `VERIFIER_REPORT.md`)

- **A1 (refutation of the sub-claim, §5):** the "discrete root pair" is REFUTED AS
  STATED — the pair satisfies `4λs + s² + 4 = 0` exactly, i.e. it **lies ON the
  one-parameter branch** (a redundant `sp.solve` output at the points where the
  y-component's quotient also vanishes), and the quotient system has **no** common
  root (Gröbner basis `{s − 2λ, 3λ² + 1}`, no real solutions). The slice Bach-flat
  locus is the branch ALONE. Counter-computation preserved:
  `VERIFIER_INDEPENDENT_CHECK.py` V13c. No check, witness, or verdict depended on the
  refuted sentence; C17 (divisibility) itself is correct and was independently
  reproduced.
- **A2 (F-C6 letter gap, §3/§6):** the stand-alone TSV was the one deliverable carrying
  verdicts without in-file stamps — add the three stamps (domain CHOSE; strong-CSN
  CHALLENGED on the C2 side; CONDITIONAL_NOT_SELECTED on the EH side) via the
  generating script and regenerate.
- **N1 (note, §4/§6):** the two development-time check failures (documented only in the
  derivation agent's return) must be preserved in-package when AUDIT_REPORT.md is
  written. Done — `AUDIT_REPORT.md` "Development-time record (N1)".
- **Substantive convention-discriminator finding (§2, recorded as a finding worth
  keeping):** Einstein metrics **cannot pin the relative sign** of the two Bach terms
  (on Einstein members both terms vanish separately — Schwarzschild–de Sitter passes
  even with a wrong pairing); the decisive discriminator is **conformal covariance**
  `B[Ω²g] = Ω⁻²B[g]` (4D), which holds only for the correct `+½` pairing (V03b), plus
  the conformally-Einstein `r²·Schwarzschild` control. The package's tensor passes
  both, and recomputing in the opposite curvature sign convention gives exactly `−B` —
  same vanishing locus (V03a) — so all INEQUIVALENT/witness verdicts are
  convention-independent.
- **Confirmation record (§2):** full independent re-derivation — own metric build, own
  curvature/Weyl code, own Bach implementation; both 7-component restricted systems
  match the package files EXACTLY (V04b/V04c); W-EXP confirmed on a fully-independent
  engine with restriction-commutes-with-specialization on all 7 components (V11);
  direction A re-solved on all 7 components plus fresh verifier-chosen points (V08b);
  direction B re-solved with a deliberately different jet-preference order (V09); xx
  parity/coverage machinery independently re-derived (V10a–d); **28/28 independent
  checks, exit 0** (`VERIFIER_INDEPENDENT_STDOUT.txt`).

## 3. Changes made (this amendment pass)

1. **`derive_routeC_stage1.py`** —
   - `sys_rows` SYSTEM-row text corrected to: branch `4λs + s² + 4 = 0` **ALONE**, with
     the former pair identified as a redundant solver output lying ON the branch
     (pointing at the new check).
   - **New zero-residual check `C17b_pair_lies_on_branch`** (A1 made check-backed, not
     hand-written): both sign choices of the former "pair" are substituted into
     `4λs + s² + 4` and proven to give exactly zero.
   - **A2:** the TSV writer now emits three `#`-prefixed STAMP header lines (domain
     CHOSE / c2_side strong-CSN CHALLENGED / eh_side CONDITIONAL_NOT_SELECTED) from the
     script's `STAMPS` dict, keeping the TSV parseable (skip `#` lines).
2. **`EXACT_DERIVATION.md`** — TC4 slice bullet rewritten: branch ALONE, with the A1
   correction inline (pair lies ON the branch; C17b; verifier Gröbner basis cited);
   run record updated to the post-amendment count (33/33) with the pre-amendment 32/32
   noted.
3. **Regenerated deterministically by rerun:** `SECTOR_COMPARISON_LEDGER.tsv` (stamps
   header + corrected SYSTEM row; all seven per-component rows byte-identical to the
   verified originals), `routeC_stage1_results.json` (now 33 checks), and
   `DERIVATION_STDOUT.txt`.
4. **Rerun record:** `python3 derive_routeC_stage1.py` → **33/33 checks PASS, exit 0**
   (~48 s, single CPU process). A second rerun: JSON identical modulo `elapsed_s`, TSV
   byte-identical — determinism reconfirmed post-amendment.

## 4. Explicitly NOT changed (the verdict-preserving list)

- **The OC1 verdict** (exact INEQUIVALENCE with witnesses) — untouched.
- **All witnesses** — every per-component direction-A and direction-B witness set
  (including the xx even-parity/quadratic witnesses and their coverage intervals),
  W-FLAT, W-EXP (`s=1, λ=−5/4`), W-EXP-CF (`s=2, λ=−1`) — byte-identical.
- **All seven component verdicts** (tt, ty, tz, xx, yy, yz, zz: INEQUIVALENT) and the
  jet signatures — byte-identical ledger rows.
- **The TC6 re-grade** — CLOSED-for-this-pair (scoped); fork OPEN with narrowed
  conditions (CM0-C, KER-R kernel deformations, BDY-TD variants) — untouched.
- **The S26 re-stamp**, the TC5 boundary typing, the one-way containment statement,
  the C17 divisibility fact, and every pre-existing check C01–C18 — untouched (the
  amendment only ADDED C17b).
- `BACH_ODE_SYSTEM_FULL.txt` / `EH_ODE_SYSTEM_FULL.txt` — regenerated byte-identical.
