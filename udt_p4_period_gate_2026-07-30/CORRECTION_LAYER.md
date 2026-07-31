# CORRECTION LAYER — P4 period gate (amendments AM-1 + AM-2, per VERIFIER_REPORT.md)

Date: 2026-07-30. Branch: grok. Finishing agent (post-verifier), applied against the
blind verifier's verdict **PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md`;
two REQUIRED amendments, **both bookkeeping** — no falsifier fired, no substantive
claim broken). **This layer is SLIM by construction: unlike the arc's prior
correction layers, NO computed claim, phrasing-level scope, verdict, ledger row, or
check needed amendment** — a first for the arc alongside Route D. The MIXTURE
outcome (OQ3 sector map + OQ4 no-quantization + Q-A no-selection) survived the
adversarial pass intact, including the hardest attacks on the two
owner-pleasing-adjacent legs (the quantization silence; the sector map).

## 1. The two amendments (both bookkeeping; both applied this pass)

- **AM-1 — `AUDIT_REPORT.md` was a promised deliverable (prereg §2 list, §5(5)) and
  did not yet exist.** Written this pass in house style (grade
  VERIFIED-WITH-AMENDMENT; TP table; composite verdict; family statuses; falsifier
  memorial; limits; verifier record).
- **AM-2 — `EXACT_DERIVATION.md` status line + hardening non-diffability.** The
  status line still read "DERIVATION-COMPLETE, blind verification pending"; updated
  to the verified status (pass recorded, amendments cited, post-amendment rerun
  cited). Added the one-sentence note that the three pre-bank check-hardenings
  (C3c/C5a/C2c) are NOT git-diffable — no earlier draft was ever committed, only
  the final script exists — and that the verifier audited the FINAL forms and
  certified them as the strong versions claimed (no soft `ask`, no vacuous
  disjunct anywhere in the final script).
- **Housekeeping consistency edit (same class, disclosed):**
  `DECISION_SURFACE_UPDATE.md`'s header parenthetical carried the same stale
  "blind verification pending"; synced to the verified status ("bookkeeping only,
  no row here changed"). No row, verdict, or proposal in that document was touched.

## 2. The verifier's strengthenings and attack record (cited from
`VERIFIER_REPORT.md`; independent artifact preserved as
`VERIFIER_INDEPENDENT_CHECK.py`, 14 groups, ALL PASS, exit 0)

- **The 2-cycle probe: OUT OF CONTRACT and doubly benign.** The binding R9 wording
  licenses periods over 1-cycles and loop holonomies only, so 2-form flux is out of
  contract; additionally (the verifier's own adjudication) the capped arena has
  H₂ = 0 (104/104 |det| = 1 ⇒ π₁ trivial), the lens class gives torsion H₂ ⇒ real
  periods vanish, and G13's F = dS is exact so its periods vanish identically.
- **The angular-compactness adjudication:** the toric angles ARE compact, but every
  1-cycle along them is capped-contractible or torsion; compactness reintroduces
  2πZ only through a circle-valued FIELD — none banked. The package's "one
  doorway" statement certified exactly right.
- **The second-route proof:** Hom(D∞, R) = 0 re-proven by the conjugation argument
  (h(γ) = h(rγr⁻¹) = h(γ⁻¹) = −h(γ)), independent of the package's
  generator-torsion route — the quotient theorem is now DOUBLY PROVEN; the
  integral corroboration adversarially extended to a transcendental profile
  (period still identically zero).
- **The independent closed form:** I_p(9/2)·a_F = −4 + π/6 + (2/3)atan 5 +
  (5/3)log 13 > 0 in exact closed form by an independent route, exceeding the
  package's piecewise lower bound (2/3)log(5/2) — the bound chain certified sound;
  the adversarial numeric corroboration locates the IVT root at A* ≈ 1.4129 ∈
  (1/2, 9/2) with E0 > 0. π − 4 confirmed equal to the banked Slice-2b
  `ADOPTED_Ip_signchange` c = 1 endpoint.
- **The SymPy defect reproduction:** `solveset(exp(I*t)−1, t, Reals)` returning the
  incomplete {0} REPRODUCED independently; the routed-around direct exact
  evaluation certified necessary and sound.
- **Attack record:** contract-first verified in git (6f093dc); rerun ×2
  byte-identical incl. against the banked artifacts; the 22+6 substantive/guard
  split audited by name and found honest; F-P3 hunted first (no unstamped claim);
  the hardest attacks fell on the silence leg (own cycle census from the binding
  spec; real-targets theorem re-checked target by target) and the sector leg (ring
  law, SOS forcing, 1-cell emptiness, crease conditions, realizability
  certificate — all re-derived on the verifier's own routes) — **both HELD**;
  F-P1..F-P7 all NOT FIRED / no contradiction.

## 3. Changes made (this finishing pass)

1. **`AUDIT_REPORT.md`** — written (AM-1).
2. **`EXACT_DERIVATION.md`** — status line updated to VERIFIED-WITH-AMENDMENT +
   the hardening non-diffability note appended to the honesty note (AM-2; two
   sentences total, exactly as the verifier specified).
3. **`DECISION_SURFACE_UPDATE.md`** — header status parenthetical synced
   (housekeeping, disclosed above).
4. **`CORRECTION_LAYER.md`** (this file) — written.
5. **Rerun record:** `python3 derive_period_gate.py` → **28/28, exit 0 = 22
   SUBSTANTIVE + 6 GUARDS, 0 failed**, run ×2 this pass: exit 0 both, stdout
   byte-identical across the two runs, and the regenerated `DERIVATION_STDOUT.txt`
   / `period_gate_results.json` / `PERIOD_LEDGER.tsv` byte-identical (sha256) to
   the banked pre-rerun copies — determinism reconfirmed post-amendment
   (3f1960b1… / 6f60eac3… / 0eb88666…). ~1 min wall, single CPU process, exact
   SymPy only.

## 4. Explicitly NOT changed (the verdict-preserving list — everything substantive)

- **The composite verdict** — MIXTURE OQ3 + OQ4: the sector map computed; NO
  quantization (with the derived structural reason and the one doorway); NO
  posture selection (Hom(D∞, R) = 0, doubly proven) — untouched.
- **The cycle census (TP-1)** — the per-posture × completion-branch table; the
  torsion vacuity; the live-cycle identification — untouched.
- **The derived period conditions (TP-2)** — the ring law Σ E0_i L_i = 0 with its
  mass-branch reading Σ M-WALL_i = 0; the field single-valuedness conditions; the
  whole-completion tie Σ E0_i I_p,i = 0 (the banked per-cell tie as its N = 1
  instance); the J11 twisted holonomy laws — untouched.
- **The three verdicts** — Q-A NO SELECTION; Q-B NO quantization; Q-C the six-row
  sector map (FORBIDDEN / EMPTY / PERMITTED-CONDITIONAL rows with the certified
  family-(i) crease witness) — untouched.
- **`PERIOD_LEDGER.tsv`** — all 20 rows byte-identical (regenerated by rerun,
  hash-identical); no row amended, none appended.
- **`period_gate_results.json` / `DERIVATION_STDOUT.txt`** — byte-identical
  (regenerated by rerun).
- **`derive_period_gate.py`** — not touched: all 28 checks as banked, 0 altered,
  0 relabeled, 0 added (no verifier-credited checks were required — the
  strengthenings are recorded in the verifier's own preserved artifact).
- **The honesty items** — the SymPy solver-path defect disclosure and the
  three-hardenings record (only ANNOTATED with the non-diffability sentence per
  AM-2; the claims themselves unchanged and verifier-certified).
- Also untouched: the ceiling (nothing adopted — no posture, census, pairing,
  completion branch; no spectrum claimed; no physics); all F-P3 stamps; the
  F-P7 characterized-only discipline; the candidate-family table (none dropped);
  the limits that travel; `PREREGISTRATION.md` (frozen) and `VERIFIER_REPORT.md` +
  `VERIFIER_INDEPENDENT_CHECK.py` (preserved verbatim).
