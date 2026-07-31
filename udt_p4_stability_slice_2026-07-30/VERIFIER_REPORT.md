# Blind adversarial verifier report — P4 stability slice

Verifier: blind adversarial agent, **same-session-spawned** (zero prior task context; NOT a hosted
external model — that caveat travels with this record). Date: 2026-07-31.
Independent script: `VERIFIER_INDEPENDENT_CHECK.py` (this dir; exit 0, 0 failures on final form).

## VERDICT: PASS-WITH-REQUIRED-AMENDMENTS (2 amendments, both bookkeeping-grade; no computed claim broken)

## Duty 0 — rerun / contract / hygiene
- Contract-first CONFIRMED in git: `PREREGISTRATION.md` committed at 942d1f6 (2026-07-30 22:51)
  before every derivation artifact (files dated 07-31 01:23-01:25).
- Rerun: exit 0, 36/36, 3.6 s single CPU process; `DERIVATION_STDOUT.txt` and
  `stability_results.json` **byte-identical** on rerun (deterministic).
- Substantive/guard split audited: exactly 5 `kind="GUARD"` rows (SB6, SB15, SB16, SB17, SD5) —
  labels honest; the verdict-assembly rows are guards, their computational legs are substantive.
  EXCEPTION → Amendment A2 (SB12, below).
- No floats / numeric eigensolvers / GPU in the derivation script (`eigenvals` only on the exact
  2×2 toy). Forbidden-content greps clean: no dynamics adopted for NV, no posture/census/pairing
  adoption, no hopfion results (method-shape citations only).

## Duties 1–8 — independent re-derivations (all in `VERIFIER_INDEPENDENT_CHECK.py`)
1. **Reduced operator, exact basis, index-1 count (V0–V2, V4, V8):** re-derived from the banked
   atlas on my own path. Energy relation, fh completion, depth total-derivative, L·v1=L·v2=0,
   Wronskian = a_F²E0² — all zero-residual. Crease-branch footing re-derived against the banked
   C6b coefficients (w1=2A−√(2A), w0=1+A−√(2A) ⟺ wB at s=√(2A); A*∈(1/2,9/2) ⟺ s∈(1,3) — the
   cited interval is genuine). Sturm legs SOUND as used: w ≥ 1/2 > 0 (regular problem, computed),
   vt2 = solution vanishing at the crease with exactly ONE interior zero x2=2/s−1 (exact roots),
   vt2(1)≠0 and no Dirichlet/Robin kernel — oscillation gives n−=1 as an upper AND lower bound.
   Galerkin(6) hunts at s=3/2, 2, 5/2: Dirichlet n−=1, Robin n−=1 (no missed direction found;
   no over-count). UNDER-count hunt against the banked slot census: no wrongly excluded direction
   at the banked layer (w rides p; k_mod/k10/C vacuous — verified; jet≤2/N=2/4th-order typed out).
2. **Absorption crossing (V5, V6, V8, V9):** resolvents re-derived independently by variation of
   parameters (my own α, β solve — matches −1/s³, 1/(s(s−1)), 2/(s(2s−1))); criterion closed forms
   confirmed by DIRECT exact quadrature at s=3/2, 2, 5/2 (J computed exactly, atan closed form) —
   the J-cancellation is real: 1+τ⟨g,φ_D⟩ = −2/(J(s−1)) and the Robin analog, both < 0 for EVERY
   s>1 (4s²−3s+1 has discriminant −7), so uniformity over the transcendental A* HOLDS. The rank-one
   crossing rule verified properly, beyond their toy: 8 random exact 5×5 matrices, rule exact every
   time; plus the analytic argument (linear crossing function, single root, interlacing). Galerkin
   hunts confirm the penalized forms are nonnegative (n−=0) at all spot s.
3. **S-ii unconditional witness (V11–V12b):** assembly re-derived (two-parameter Hessian; also
   proved the script's single-ε form equals the full joint Hessian by polarization, V1). Witness
   recomputed: Q = −g_p π²/ℓ exact; sin(πx/ℓ) is exactly odd about BOTH walls with all traces zero
   (germ-independent) — admissible under the banked mirror-odd moduli forcing; both E0 signs.
4. **Dichotomy (V13):** per-mode 2×2 re-derived; mode basis sin(nπ(x+ℓ)/2ℓ) verified orthogonal in
   both metrics AND wall-odd for every n (it IS the right basis for the banked all-traces-zero
   sector — the verdict is honestly scoped "in-this-sector"); threshold 64E0²ℓ⁴ ≤ g_p c_m π⁴
   confirmed BOTH directions (stable-side spot all dets > 0; unstable-side n=1 det < 0 explicit).
5. **Double-crease EMPTY vs period gate:** REFINES, not contradicts — the period-gate quotient row
   is about periods (all identically vanish; no cut); this is a wall-trace fact. The C6a witness
   w=x²/2+1/2 has I_p·a_F = π−4 ≠ 0 (not on the massive locus), consistent. Also closed the E0<0
   gap myself: disc<0 with w>0 forces A>0, so E0<0 has no definite-class members — EMPTY is total.
6. **Controls (V14, V15):** re-run independently; both PSD with kernel exactly the banked flat
   directions (μ and k_mod absent from the form; triad: arbitrary odd v_λ, v_kmod). PASS.
7. **Disclosed check-coding fixes:** both final forms verified on independent paths — SA1 by the
   polarization identity (V1), SB10 by direct exact quadrature (V6). Sound.
8. **OS-5 obstructions:** genuine exactness obstructions, not throughput — (i) the second germ is
   unpinned at the banked N=2 wall layer (matches the boundary-action gate: "N=2 is exactly the
   first germ"; SB16's δ²-activation is the honest consequence); (ii) C = a_F′²E0∫p̄² involves
   ∫(log w)² → dilogarithmic at transcendental A*; numerics were contract-forbidden (TS-3).
   NOTE (lead, not a verdict): my joint Galerkin hunt at the massive root s* ≈ 1.681 (I_p = 0
   solved to 40 digits) gives joint (fields+μ) n− = 1 at dims 13/17/21 — the λ-Schur block appears
   NOT to add a second negative direction; a future bounded-numeric contract could close this.

## Falsifier hunts (duty 9)
- **F-S3 first:** all ledger rows carry candidate/posture/census/pairing/chain-vs-single/jet-layer/
  perturbation-space stamps. Clean.
- **F-S1 both directions:** attacked the UNSTABLE verdicts as hard as the stable-side ones (the
  landed headline is the anti-temptation direction; I hunted a wrongly-included direction that
  would fake instability — none: every negative witness is banked-admissible; and a wrongly-excluded
  one that would hide extra instability — none found; Galerkin counts match the exact counts).
- **F-S2 both directions:** no fixed-background Hessian (μ computed jointly — V1); no invented
  constraint (crease Dirichlet = banked posture fact; odd pin = SUPPLIED branch, carried both ways;
  zero-mean of v_f′ is a derived consequence of zero traces). The one F-S2-flavored soft spot is the
  JSON's unscoped index claim → Amendment A1.
- **F-S4/F-S6/F-S7:** clean (no dynamics/adoption/hopfion; no bank contradiction — period gate,
  wall gate, C6a/C6b, tie all re-checked; no symbolic failure; my two own-script false-FAILs were
  MY bugs/tool limits, disclosed in-script).
- **F-S5:** controls reproduced independently. Run valid.

## Contract compliance (duty 10)
TS-1..TS-5 all met; §4 ceiling respected (no candidate crowned, no posture decided, no dynamics).
Minor style note (not a violation): `DECISION_SURFACE_UPDATE.md` uses "the great pruner cut…" /
"surviving-stability corners" — tied to computed verdicts and inside the ceiling, but near it.

## REQUIRED AMENDMENTS
- **A1 (scope propagation, bookkeeping):** `stability_results.json` verdict
  `S-i_crease_branch_free_fh_data` says "n-=1 exact" WITHOUT the "(reduced sector)" scope that the
  ledger (R05) and `EXACT_DERIVATION.md` correctly carry; `DECISION_SURFACE_UPDATE.md` item 1
  ("index-1 UNSTABLE") likewise. On the JOINT space (fields+μ) the certified statement is
  **index ≥ 1 exact; exactly-1 pending the λ-Schur sign** (the same dilogarithmic obstruction as
  R06; my hunt supports exactly-1 at s*). Add the scope in both places. UNSTABLE itself is
  unconditional and unaffected.
- **A2 (label honesty, bookkeeping):** SB12's coded condition is an arithmetic identity true by
  construction (w·g·(κ/(g w))·u ≡ κu); the real content (constrained minimization ⇒ penalty
  g(∫X)²/J) lives in the detail prose. Relabel SB12 SUBSTANTIVE→GUARD (split becomes 30+6) or add
  a genuine check of the minimum value. The underlying math is CORRECT (verified independently:
  penalty and τ = a_F²σ/J re-derived; quadrature-confirmed).

## Scope notes that must travel (already in the record; confirmed accurate)
Verdicts are at: quadratic class, banked ℓ=1 CHOSE normalization, s∈(1,3), germ-Hessian-flat
realized wall responses, N=2 wall layer, no dynamics. NV UNDEFINED-AT-LAYER is honest typing.

## AMENDMENT CLOSURE (same blind verifier, 2026-07-31)

**Verdict: CLOSED.**
- Rerun of the amended `derive_stability_slice.py`: exit 0, 36/36 = 30 substantive + 6 guards;
  deterministic (rerun stdout byte-identical to the banked `DERIVATION_STDOUT.txt`; JSON counts
  {30,6,0} consistent). Full diff vs my pre-amendment snapshot inspected: ONLY detail strings,
  the SB12 kind SUBSTANTIVE->GUARD, and JSON verdict text changed — **no check CONDITION altered**.
- A1 installed at all five sites (JSON verdict, SB6 detail, DECISION_SURFACE item 1,
  EXACT_DERIVATION Stage-B, ledger R05 stamps column): joint-space statement "index >= 1 exact,
  exactly-1 pending the lambda-Schur sign"; UNSTABLE unconditional; my joint hunt cited as
  corroboration-not-banked everywhere it appears. Note: R05 carries the joint scope in the
  STAMPS column while the verdict column reads "n-=1 EXACT (reduced sector)" — acceptable
  (the verdict is itself scoped); not a defect.
- A2: SB12 relabeled GUARD with the honesty note; split restated 30+6 in script summary, JSON,
  and records.
- Credits accurate: E0<0 closure -> EMPTY TOTAL at R03/SB2-adjacent text (EXACT_DERIVATION +
  ledger, marked credited); crossing-rule toy caveat retired with the proper-verification
  citation (SB11 detail); joint-Galerkin lead = DECISION_SURFACE item 5, named next-tile,
  NOT launched. CORRECTION_LAYER "explicitly NOT changed" list verified against the diff —
  holds. AUDIT_REPORT records my two disclosed own-bugs faithfully.
- No new defect found.
