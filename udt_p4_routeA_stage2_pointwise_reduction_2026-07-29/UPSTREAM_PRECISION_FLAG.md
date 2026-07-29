# UPSTREAM PRECISION FLAG — class-wide vs per-member stabilizer glosses (DRAFT; NOT APPLIED)

Date: 2026-07-29. Origin: Route A Stage 2 amendment A1 (`VERIFIER_REPORT.md` §2b +
A1(v); `CORRECTION_LAYER.md`). Status: **DRAFT for the driver's review — no upstream
file has been edited by the amendment agent.** The driver applies these as separate
visible edits (and flags NEGATIVES_REGISTRY-style CONDITIONS-CHANGED bookkeeping if
any consumer leaned on the glosses). **Round-2 note (closure C7):** both proposed
edits were ENDORSED by the closure verifier and are kept; only the resonance
DESCRIPTION below is adjusted so it does not imply the named C = 0 strata exhaust
the resonance content (per the closure consistency note and the C3 correction).

## What was found

The blind verifier's counter-computation (adopted and extended in this package's
`A1_*`/`A1R2_*` checks) established: the banked rank-6/empty-nullspace stabilizer
computation is the **CLASS-WIDE** stabilizer ("[B,X] tangent to the class for EVERY
class member"). The **PER-MEMBER** stabilizer jumps on strata: on the codim-1
stratum k_mod = 0 the screen rotation L23 is tangent to the registered class
([L23,X] = [[0,0],[J·C, k10·diag(1,−1)]] ≠ 0), inducing the exact pointwise Noether
identity −2k10·r_tf + m00c10 + m01c11 − m10c00 − m11c01 = 0 there; the remaining
rank-drop locus is confined (codim-1-exhaustively, minor-ideal proof) to the
eigenvalue-resonance locus λ∓k_mod ∈ {±1} — which carries BOTH the four named
C = 0 strata (identities auto-satisfied in the declared class) AND higher-codim
C ≠ 0 sub-varieties with further genuine identities (round-2 example: the shear
identity −c10·r_sh − k10·m10 = 0 on {λ−k_mod = −1, c00 = c01 = 0}; the named
strata do NOT exhaust the resonance content; deeper stratification
TYPED-NOT-EXHAUSTED). **The upstream COMPUTATIONS are correct**; two banked
interpretation-layer GLOSSES state the class-wide fact as if it were per-member.

## Proposed edit 1 — Stage-1 `udt_p4_routeA_response_inverse_problem_2026-07-29/POSED_INVERSE_PROBLEM.md` §1.4

CURRENT (§1.4, "What a tangent vector IS"):

> A tangent vector at a configuration is the equivalence class (mod infinitesimal gauge;
> on the registered chart, mod nothing continuous — the quotient is discrete K₄):

PROPOSED REPLACEMENT:

> A tangent vector at a configuration is the equivalence class (mod infinitesimal gauge;
> on the registered chart the CLASS-WIDE continuous stabilizer is trivial, so at GENERIC
> members this is mod nothing continuous and the quotient is discrete K₄ — SCOPE NOTE
> (Stage-2 A1): per-MEMBER continuous gauge directions exist on the degeneration strata
> of the moduli (k_mod = 0: the screen rotation, with an exact pointwise Noether
> identity; the eigenvalue-resonance locus λ∓k_mod ∈ {±1}, whose sub-varieties —
> including C ≠ 0 ones — carry further exact identities; the named C = 0 strata do not
> exhaust the resonance content) — see
> `udt_p4_routeA_stage2_pointwise_reduction_2026-07-29/EXACT_DERIVATION.md` §2):

## Proposed edit 2 — Route B `udt_p4_routeB_extension_selection_2026-07-28/EXACT_DERIVATION.md` T1(b), registered-class bullet

CURRENT:

> - Registered class (fixed H block, zero upper-right, K lower-triangular): infinitesimal
>   stabilizer **trivial** (`T1_registered_chart_infinitesimal_stabilizer_trivial`).

PROPOSED REPLACEMENT:

> - Registered class (fixed H block, zero upper-right, K lower-triangular): infinitesimal
>   stabilizer **trivial** (`T1_registered_chart_infinitesimal_stabilizer_trivial`).
>   SCOPE NOTE (Route A Stage-2 A1): this is the CLASS-WIDE stabilizer (tangency for
>   every class member); PER-MEMBER stabilizers jump on strata — on k_mod = 0 the screen
>   rotation span(L23) (the same L23 that survives on the relaxed block form, next
>   bullet) is tangent at the member, giving an exact pointwise Noether identity; see
>   `udt_p4_routeA_stage2_pointwise_reduction_2026-07-29/EXACT_DERIVATION.md` §2.

## Proposed edit 2b — same gloss in the Route B script/JSON headline (secondary, same package)

`derive_routeB_stage1.py` (results-dict string, ~line 489) and
`routeB_stage1_results.json` ("equivariance_law", ~line 413):

CURRENT (fragment):

> connected structure-preserving stabilizer of the registered chart class is trivial;

PROPOSED (fragment; if the driver prefers not to touch the frozen JSON, the MD scope
note of edit 2 suffices — the JSON is a generated artifact of a banked run):

> connected structure-preserving stabilizer of the registered chart class is trivial
> (CLASS-WIDE; per-member stabilizers jump on strata — Route A Stage-2 A1);

## Not proposed

- No change to any Route B computation, check, or the K₄ exhaustiveness result (all
  verified correct; the finite-orbit argument is unaffected — the finite screen
  rotations exit the class, only the INFINITESIMAL member-tangency jumps).
- No change to Stage-1's forced items F-RA1..F-RA4 (their statements do not rest on
  the per-member reading).
- No registry entry is created here; whether the glosses' consumers need a
  CONDITIONS-CHANGED flag is the driver's call (the only identified downstream
  consumer was THIS package's pre-amendment R7(b) claim, now amended).
