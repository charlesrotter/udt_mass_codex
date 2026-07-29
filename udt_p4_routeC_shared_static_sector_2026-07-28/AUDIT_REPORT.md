# P4 Route C Stage 1 — AUDIT REPORT (shared exact static sourced sector, TC1–TC6)

Date: 2026-07-28. Branch: `grok`. Preregistration (`PREREGISTRATION.md`) committed at
dfb39ac BEFORE the derivation artifacts existed (contract-first confirmed in git by the
verifier). CPU-only exact-SymPy derivation; no solve, no GPU, no canonization, no
physics selected.

**GRADE: VERIFIED-WITH-AMENDMENT** — blind adversarial pass (zero-context-framed,
same-session-spawned agent, **not a hosted external model**; caveat travels) returned
**PASS WITH REQUIRED AMENDMENTS (verdict-preserving)** with two amendments (A1: a
check-free "discrete root pair" sentence refuted as stated — the pair lies ON the
branch; A2: the stand-alone ledger lacked in-file stamps), both applied and
check-backed (`CORRECTION_LAYER.md`; new zero-residual check C17b; stamps now emitted
into the TSV by the generating script). All load-bearing deliverables — the seven
component verdicts, every witness in both directions, the system witnesses, the TC6
re-grade, the S26 re-stamp — verified independently with no changes.

## Result first — OC1: the two conditional actions do NOT share the exact static sector

**Pair-scoped: (C2/Bach, EH+Λ) only.** On the declared comparison domain — **CHOSE**
(the registered stationary family `g = −u(c_E dt + αA)² + u⁻¹A² + q_B`, `u = e^{−2φ}`,
with its `R×T²` stratum in the local toric chart; the stamp travels on every
conclusion) — the restricted vacuum equation sets of the two CONDITIONAL candidates are
**INEQUIVALENT on every one of the seven independent components**, with exact witnesses
in BOTH directions per component (every real Λ covered), plus system-level witnesses
(W-FLAT, W-EXP, W-EXP-CF).

Scope stamps (all travel; F-C6):

- Domain: **CHOSE** (registered stationary family + `R×T²` stratum, local toric chart).
- C2/Bach side: `UNIQUE_CONDITIONAL_ONLY_IF_STRONG_CSN_RETAINED`; strong CSN
  `CHALLENGED_OWNER_POSTULATE_NOT_DERIVED` (G04/G10) — an INACTIVE conditional branch.
- EH+Λ side: `CONDITIONAL_NOT_SELECTED` (G11); EH-H3 spatial-infinity normalization NOT
  used anywhere.
- **Equation-sharing sense**: the verdict adjudicates condition 2 of the 07-18 record in
  its verbatim sense — "one declared variation domain and the same exact finite-cell
  static equations on both" — EQUATION-equality, and the pre-registered
  subfamily-refutes-superset asymmetry is applied to equation-sharing only.
- **One-way solution containment stated separately**: every Einstein member is Bach-flat
  (standard 4D fact, cited as Category-A mathematics, **slice-verified-only** — NOT
  re-proven on the full ansatz), so shared SOLUTIONS exist one-way; "shares solutions
  one-way" is NOT "the same exact equations". No conflation (verifier F-C4 hunt: CLEAN).

## Target outcomes

| Target | Outcome |
|---|---|
| TC1 census | PASS — domain + varied-field census stated with chose-or-derived tags; λ seat SYMBOLIC throughout (never frozen); `det g` consistency with the plane-audit A01 (C01) |
| TC2 Bach restriction | PASS — full-vary-then-restrict (F-C1 clean); 7 independent components (trace-free, symmetric, mixed x-row vanishes); every component carries 3rd/4th jets; full system in `BACH_ODE_SYSTEM_FULL.txt`; verifier's independent engine matches EXACTLY |
| TC3 EH+Λ restriction | PASS — same 7 components, Λ symbolic never fitted; contracted Bianchi exact (C07); no component above 2nd jets; full system in `EH_ODE_SYSTEM_FULL.txt`; exact independent match |
| TC4 comparison verdict | **OC1 — all 7 components INEQUIVALENT**, two-directional witnesses each, every real Λ covered; PROPORTIONAL/IDENTICAL excluded by the witness pairs; A1-amended slice wording (branch alone, C17b) |
| TC5 boundary typing | PASS (typed only) — 2-jet wall + 3rd-derivative momenta + trace-free-Weyl corner structure (Bach) vs 1-jet wall + K-momenta + Hayward corners (EH); J07/J08 classes; BDY-TD threat quoted; **no boundary law chosen**; all quotes verified verbatim by the verifier |
| TC6 route re-grade | **CLOSED-for-this-pair (scoped)**; fork OPEN with narrowed conditions; S26 second unlock leg re-stamped (below) |

## The 07-18 fork re-grade (scoped)

**CLOSED-for-this-pair (scoped):** for the (C2/Bach conditional, EH+Λ conditional) pair
on the declared CHOSE domain — and, by the pre-registered subfamily-refutes-superset
asymmetry, on any static domain class containing it — condition 2 cannot be satisfied.
**The fork itself remains OPEN with narrowed conditions:** a shared-static-sector
theorem, if it exists, must come from a DIFFERENT pair — the unwritten **CM0-C**
nonvariational completion (recorded exclusion), a **KER-R kernel deformation** of a
completed base action (actions differing by terms in the static kernel), or **BDY-TD
boundary-primitive variants** of one bulk action (bulk sector shared trivially;
condition 4 then the whole fight). NOT "route dead" (F-C4 respected). Conditions 1,
3–6 of the 07-18 record are untouched by Stage 1.

**S26 re-stamp (re-stamped, NOT discharged; no mass claim):** the S26 conditional row's
second unlock leg ("shared-sector theorem plus normalization") is re-stamped
`SHARED-SECTOR-THEOREM: UNAVAILABLE-VIA-THE-(C2/Bach, EH+Λ)-PAIR-ON-THE-REGISTERED-
DOMAIN (Stage-1 witnesses; scoped)`. The leg survives only through a different
pair/completion; the first leg (native branch adoption) is untouched. S26 remains
CONDITIONAL.

## REPORTED OBSERVATIONS (structural, not verdicts; scope stamps attached)

1. **The Bach-flat branch requires the λ seat unfrozen.** On the exponential slice
   (`φ=kx`, `bh=e^{2sx}`, `f=0`, `α=0`, `k=1` gauge) the Bach-flat locus is the
   one-parameter branch `4λs + s² + 4 = 0` ALONE (A1-corrected; C17/C17b), which
   forces `λs = −(s²+4)/4 < 0` — **a frozen λ=0 seat admits NO Bach-flat member on the
   slice** (verifier V13b: Gröbner-confirmed). **SCOPED to the exponential subfamily**;
   a structural datum for the G08-open λ seat, not a selection.
2. **Reciprocal-lock rigidity.** The registered `u`/`u⁻¹` reciprocal lock on the (t,z)
   legs makes the restricted 2nd-order EH+Λ system RIGID on this slice (no roots at
   k=1; flat member only, with Λ=0 — C18, verifier V15), while the 4th-order Bach
   system is not. Same slice scope stamp; reported, not adjudicated.

## Development-time record (N1 — preserved per the verifier's note)

Two intermediate check failures occurred during development; both were diagnosed as
**check-implementation issues, not mathematics**, and their resolutions became part of
the final record:

1. The originally chosen W-EXP point (`s=2, λ=−1`) failed the "Weyl ≠ 0" leg — because
   that branch point is CONFORMALLY FLAT (Bach vanishes trivially there). Resolution:
   it became the separate witness **W-EXP-CF** (C16c, the trivially-Bach-flat
   non-Einstein member), and **W-EXP moved to `s=1, λ=−5/4`** (C16, genuinely
   non-conformally-flat Bach-flat). The domain in fact contains both witness types —
   the failure enriched the record.
2. The xx direction-B witness initially failed under the generic linear-jet solve — no
   jet enters `E_xx` linearly at `p0=0`. Resolution: the exact **quadratic/parity
   construction** (E_xx identity + B_xx f-jet parity + `f1²` substitution with
   validity-interval coverage), which became the banked C15_xx machinery.

The verifier (report §4) could not see the development transcript; it adjudicated by
full independent re-derivation — every final banked claim confirmed, "consistent with
implementation-not-math" — and required this in-package preservation (N1).

## Falsifier record

**F-C1..F-C6 all clean in the final run.** F-C1 (restrict-then-vary): NOT FIRED — both
covariant tensors are unrestricted variational outputs evaluated afterwards; Bach
provenance citation verified verbatim. F-C2 (static-energy false pass): NOT FIRED —
verdict rests on all seven components individually incl. lapse tt and momentum ty/tz.
F-C3: NOT FIRED — 33/33 zero-residual checks, exit 0 (pre-amendment 32/32). F-C4
(quantifier slip, both directions): NOT FIRED — equation-sharing sense exact; one-way
containment stated separately; pair-scoped, not "route dead". F-C5 (imposition): NOT
FIRED — provenance/honesty criteria only; no spatial-infinity normalization anywhere.
F-C6 (conditionality laundering): one LETTER-LEVEL gap found by the verifier (the
stand-alone TSV carried no in-file stamps) = **A2, cured** (stamps now
script-generated into the TSV header). **A1 was a documentation-level refutation** — a
hand-written, check-free sentence ("plus a discrete root pair") refuted by the
verifier's Gröbner computation (the pair lies ON the branch); **now check-backed**
(C17b proves the pair satisfies the branch equation with zero residual). No check,
witness, or verdict was touched by either amendment.

## LIMITS THAT TRAVEL

1. **The domain is CHOSE.** Every conclusion is scoped to the registered stationary
   family (+ its `R×T²` stratum, local toric chart); the inequivalence extends UPWARD
   to supersets (subfamily refutes superset) but says nothing about disjoint domains.
2. **Both candidates are conditional.** Strong-CSN CHALLENGED (C2 side, inactive
   branch); CONDITIONAL_NOT_SELECTED (EH side). Neither is promoted or demoted as
   physics by this result.
3. **Pair-scoped negative.** Other pairs, the CM0-C completion, KER-R kernel
   deformations, and BDY-TD variants are untouched; the 07-18 fork stays OPEN with
   narrowed conditions. Conditions 1, 3–6 undischarged.
4. **Vacuum equations only; source side typed-only.** No carrier adopted (G09 posit);
   the non-equivalent source identities remain separate typed rows.
5. **Containment is slice-verified-only.** "Einstein ⇒ Bach-flat" cited as Category-A
   mathematics, verified on slice members only, NOT re-proven on the full ansatz.
6. **No adoption ceiling enforced.** No action adopted, no mass, no normalization, no
   boundary law, no branch, no α value — the pre-committed maximum-conclusion ceiling
   was respected (verifier-confirmed).
7. **Verifier caveat.** The blind verifier is same-session-spawned, not a hosted
   external model.

## Evidence

`derive_routeC_stage1.py`: **33/33** zero-residual exact-SymPy checks (32 original +
C17b from A1), exit 0, ~48 s single CPU process, deterministic (JSON identical modulo
`elapsed_s`, TSV byte-identical across reruns; no floats/randomness/network).
`routeC_stage1_results.json`, `SECTOR_COMPARISON_LEDGER.tsv` (A2: three in-file STAMP
header lines; A1: corrected SYSTEM row), `BACH_ODE_SYSTEM_FULL.txt`,
`EH_ODE_SYSTEM_FULL.txt`, `DERIVATION_STDOUT.txt` — all regenerated post-amendment.
`EXACT_DERIVATION.md` (A1-amended), `CORRECTION_LAYER.md` (the amendment record).

## Verifier record

Blind adversarial pass, 2026-07-28 (zero-context framing; same-session-spawned; **not a
hosted external model** — caveat travels). Independent artifacts preserved in-package
(`VERIFIER_INDEPENDENT_CHECK.py`, `VERIFIER_INDEPENDENT_STDOUT.txt`): **28/28
independent checks, exit 0**, with a **fully-independent Bach engine** (own metric
build from the census, own Christoffel/Riemann/Ricci/Weyl code, own
`B_ab = ∇^c∇^d C_acbd + ½R^cd C_acbd`). Both full 7-component restricted systems match
the package files EXACTLY. **W-EXP confirmed** on the independent engine
(restriction-commutes-with-specialization on all 7 components). **Convention-
independence PROVEN**: Einstein metrics cannot pin the Bach pairing sign (both terms
vanish separately there); the decisive discriminator is conformal covariance
`B[Ω²g] = Ω⁻²B[g]` (4D), which the package tensor satisfies (and the opposite curvature
convention gives exactly −B — same vanishing locus). **Fresh direction-B witnesses
re-solved at a different jet order** (deliberately different low-jet preference; the
inequivalence is not an artifact of the package's chosen points), plus fresh
direction-A points at verifier-chosen primes. Duty-2 adjudications: full-system match
CONFIRMED; xx parity/coverage machinery CONFIRMED; slice branch + λ=0 emptiness
CONFIRMED (Gröbner); one sub-claim REFUTED-AS-STATED (→ **A1**); F-C6 letter gap
(→ **A2**). Verdict: **PASS WITH REQUIRED AMENDMENTS (verdict-preserving)**; A1+A2
applied and check-backed this pass (rerun 33/33, exit 0; `CORRECTION_LAYER.md`).
