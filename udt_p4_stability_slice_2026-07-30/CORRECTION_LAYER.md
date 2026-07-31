# CORRECTION LAYER — P4 stability slice (amendments A1 + A2, per VERIFIER_REPORT.md)

Date: 2026-07-31. Branch: grok. Finishing agent (post-verifier), applied against the
blind verifier's verdict **PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md`; two
REQUIRED amendments, **both bookkeeping-grade — no computed claim broken, no falsifier
fired**). The OS-4 mixed outcome (two UNSTABLE legs + the absorption theorem + the
dichotomy threshold + EMPTY-domain facts + passing controls) survived the adversarial
pass intact, including the F-S1 attacks on BOTH directions (the landed headline is the
anti-temptation direction and was attacked as hard as the stable-side legs).

## 1. The two amendments (both applied this pass)

- **A1 — scope propagation (bookkeeping).** The JSON verdict
  `S-i_crease_branch_free_fh_data` said "n-=1 exact" WITHOUT the "(reduced sector)"
  scope that ledger R05 and `EXACT_DERIVATION.md` correctly carried;
  `DECISION_SURFACE_UPDATE.md` item 1 ("index-1 UNSTABLE") likewise. Fixed in both
  places (and, consistency-disclosed, in the SB6 check detail + a joint-space sentence
  in `EXACT_DERIVATION.md` Stage B + ledger R05 stamps): the certified JOINT-space
  (fields+mu) statement is **index >= 1 exact; exactly-1 pending the lambda-Schur sign**
  (the same dilogarithmic obstruction as R06; the verifier's joint Galerkin hunt
  supports exactly-1 — cited as corroboration, NOT banked). **The UNSTABLE verdict
  itself is unconditional and unaffected by this amendment.**
- **A2 — label honesty (bookkeeping).** SB12's coded condition is an arithmetic
  identity true by construction (w·g·(kappa/(g w))·u == kappa·u); the real content
  (constrained minimization => the rank-one penalty g(int X)^2/J, tau = a_F^2 sigma/J)
  lives in the prose and was **independently verified by the verifier** (re-derivation
  + exact quadrature). Relabeled SUBSTANTIVE->GUARD with an honest in-script note.
  **The split becomes 30 SUBSTANTIVE + 6 GUARDS** (was 31+5); restated in
  `EXACT_DERIVATION.md`, the JSON (regenerated), and `AUDIT_REPORT.md`.

## 2. The verifier's strengthenings, ADOPTED as credited checks

- **E0<0 gap closure (credited): double-crease ∩ massive is EMPTY — now TOTAL** over
  both E0 signs. SB2 covered the definite class at E0>0; the verifier closed the E0<0
  leg (disc<0 with w>0 forces A>0, so the definite class has no E0<0 members).
  Recorded in `EXACT_DERIVATION.md` (SB2 paragraph), ledger R03, DECISION_SURFACE.
- **Rank-one crossing rule PROPERLY verified (credited; caveat RETIRED):** beyond the
  package's exact 2x2 toy — 8 random exact 5x5 matrices, rule exact each time, plus
  the analytic linear-crossing/interlacing argument. The "toy-verified" caveat is
  retired in `EXACT_DERIVATION.md` (Stage B + Limits (iii)) and annotated in SB11.
- **Joint-Galerkin index LEAD (named next-tile OPTION, noted NOT launched):** at the
  massive root s* ≈ 1.68102 (I_p=0 to 40 digits) the verifier's joint (fields+mu)
  Galerkin hunt gives n- = 1 at dims 13/17/21 — the lambda-Schur block appears NOT to
  add a second negative direction. Recorded in `DECISION_SURFACE_UPDATE.md` item 5 as
  a bounded-numeric contract option (the arc's FIRST numeric contract, separately
  preregistered) to close the lambda-Schur/index-exactly-1 gap. A LEAD, not a verdict.
- **The verifier's two own-script false-FAILs were ITS OWN bugs/tool limits**,
  disclosed in-script and resolved in the package's favor (duty F-S4/F-S6/F-S7 record:
  no package claim was wrong). Both disclosed derivation-side check-coding fixes (SA1
  cross-term over-count; SB10 closed-form slip) were verified on independent paths
  (polarization identity; direct exact quadrature) — sound.

## 3. Changes made (this finishing pass)

1. `derive_stability_slice.py` — SB12 kind->GUARD + honesty note (A2); SB11 detail:
   caveat-retirement credit; SB6 detail + the JSON verdict string: reduced-sector scope
   + joint-space statement (A1). No check CONDITION weakened or changed.
2. **Rerun record:** `python3 derive_stability_slice.py` -> **36/36, exit 0 = 30
   SUBSTANTIVE + 6 GUARDS, 0 failures**, run x2 this pass: exit 0 both, stdout and
   `stability_results.json` byte-identical across the two runs — deterministic
   post-amendment (sha256 `DERIVATION_STDOUT.txt` 53ba68fa…, `stability_results.json`
   e4814ed0…). ~4 s wall, single CPU process, exact SymPy only.
3. `EXACT_DERIVATION.md` — SB2 EMPTY-total credit; Stage-B joint-space sentence;
   crossing-rule caveat retired (x2); counts restated 30+6 with the A2 note; Limits
   (vii) verifier status OWED -> DELIVERED.
4. `STABILITY_LEDGER.tsv` — R03 stamp: EMPTY TOTAL credit; R05 stamp: joint-space
   clause. No verdict cell changed.
5. `DECISION_SURFACE_UPDATE.md` — header synced to verified status; item 1 S-i bullet
   rescoped per A1 + EMPTY-total credit; new item 5 = the named next-tile option.
6. `CORRECTION_LAYER.md` (this file) + `AUDIT_REPORT.md` — written.

## 4. Explicitly NOT changed (the verdict-preserving list — everything substantive)

- **The S-i free-fh-data UNSTABLE verdict** — index >= 1 exact instability on the joint
  space; exactly-1 in the reduced sector — UNSTABLE itself unconditional, untouched.
- **The odd-parity ABSORPTION theorem** — the odd f/bh pin exactly absorbs the unique
  negative direction; the zero-trace core POSITIVE (crossing scalar -2/(J(s-1)) < 0
  manifest, J cancels; free-p-trace version likewise) — untouched.
- **The S-ii no-jet UNSTABLE verdict** — unconditional, exact germ-independent witness,
  both E0 signs — untouched.
- **The jet-stiffness DICHOTOMY** — 64 E0^2 l^4 <= g_p c_m pi^4, exact threshold, both
  directions — untouched.
- **Double-crease EMPTY** — only STRENGTHENED (partial->TOTAL via the credited E0<0
  closure); the wall-trace derivation untouched.
- **Both controls PASS** (banked flat directions reproduced exactly) and **NV
  UNDEFINED-AT-LAYER typing** — untouched.
- **The OS-5 remainders** (free wall-germ curvature; the dilogarithmic lambda-Schur
  sign; the general-{I_p=0} member criterion R07), the germ-activation structure
  theorem SB16, chain inheritance SB17, all stamps/limits, `PREREGISTRATION.md`
  (frozen), `VERIFIER_REPORT.md` + `VERIFIER_INDEPENDENT_CHECK.py` (preserved
  verbatim) — untouched.
