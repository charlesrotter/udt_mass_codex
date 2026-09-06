# P4 ROUTE B — STAGE 1 PREREGISTRATION: extension selection first (frozen before derivation)

Date: 2026-07-28. Branch: p4-routeB (off grok). Authorized: Charles approved the P4 MAP
(`udt_p4_variation_domain_map_2026-07-28/MAP.md`) and selected Route B (2026-07-28).
DERIVE authority: Route B ONLY — no response one-form, no action, no lambda adoption, no
census freeze, no completion-class choice, no physics. This document is committed BEFORE
the derivation runs; no retuning after.

## 0. Interrogation declaration

METRIC-LED and OBSERVING. The question is "which strata of the already-derived extension
class survive the already-derived constraint layers, and what exactly forces each
elimination/conditioning" — not "show stratum X wins". Outcome classes O1/O2/O3 (§5) are
all first-class; a moduli-family survival is an honest deliverable, not a failure.

## 1. The frozen question

Within the registered positive triangular chart, the complete-coframe extension class is
E02 (banked, `udt_founded_phi_complete_coframe_extension_audit_2026-07-25/`):

    X = [[H, 0], [C, K]],  H = diag(-1, 1) fixed (founded, G01/G02),
    K = [[a, b], [0, d]] (3 angular-generator params),
    C = [[s11, s12], [s21, s22]] (4 base-angular mixing params),

with strata E02 (7) ⊃ E03 det-one (6) ⊃ E04 transverse-invariant (4) / E05 no-mixing (3)
⊃ E06 spectator (0), and exact countermodels E07 (reciprocal-angular, generator
diag(-1,+1,-k,+k)) and E08 (shift-mixing, cross term s·(1−e^{−phi})) refuting
unconditional spectator uniqueness.

BANKED CONSTRAINT (input, not re-derived): the 18-family pointwise ACTIVE premise set has
ZERO selector rank on the 7 directions (`udt_complete_coframe_native_selector_audit_2026-07-26`).
Route B Stage 1 therefore classifies the strata ONLY under the constraint layers OUTSIDE
that exhausted set:

- **C1 — local-Lorentz equivariance / covariance of the strata.** The banked commutant
  facts (scalar-only centralizer; equivariance is the covariant form) are inputs. NEW
  question: under the induced action of the connected local Lorentz group on (K, C) in
  the registered chart, which strata are covariantly defined conditions and which are
  chart artifacts?
- **C2 — composition / transition-law closure (J07, J11).** At the Lie-algebra and
  finite one-parameter-subgroup level: which strata are closed under composition, and
  does the mixing block C compose as a cocycle (exact law for E08's s under
  concatenation)? What overlap/transition data would a global assignment require?
- **C3 — descent / reduced-holonomy conditional gates (assembly, no adoption).** The
  exact stratum-forcing map from the banked conditional facts: supplied SO(3) → forced
  diagonal member λ=+1; supplied SO+(1,2) → λ=−1; supplied reciprocal swap → λ=0 only in
  the extra diagonal subfamily (two mixing freedoms remain in the full class); holonomy
  centralizer dims (generic λ: 1; λ=±1: 3; λ=0: 1). Each gate stays CONDITIONAL on its
  supplied structure; cross-branch splices forbidden (banked: +1/−1 belong to different
  supplied global structures).
- **C4 — J-obligation compatibility typing.** Per stratum, for the extension-relevant
  obligations (J05, J06, J07, J10, J11, J13, J15 of
  `udt_joint_selector_provenance_audit_2026-07-28/JOINT_OPERATION_OBLIGATIONS.tsv`):
  satisfiable-in-principle vs structurally violated vs violated-only-if-imposed (e.g.
  imposing E06 spectator = J06's named false pass "spectator screen isotropy assumed").

## 2. Frozen targets

- **T1 (equivariance/covariance of strata).** Exact transformation law of (K, C) under
  the connected local Lorentz group in the registered chart; for each stratum
  E03/E04/E05/E06 decide: covariantly defined | chart-dependent (with the exact orbit
  computation). Input facts: scalar-only centralizer; so(1,3) perfect (no additive
  characters).
- **T2 (composition closure).** For each stratum: bracket/subalgebra status and finite
  composition closure of its one-parameter families; exact statement of what fails where
  it fails.
- **T3 (mixing cocycle).** The exact composition law of the E08 shift parameter s under
  concatenation of segments (and its generalization to the 4-param C block at first
  order); whether a consistent overlap assignment is possible pointwise or requires
  global data — stated as J07-typed requirements, not filled in.
- **T4 (transverse-seat reconciliation — the L2 clarification).** The E07 seat
  (a=−k, d=+k, reciprocal screen) and the isotropic seat (a=d=λ, the joint-audit lambda)
  are DISTINCT axes of the diagonal (a,d) plane. Map the (a,d)-plane (b=0, C=0 diagonal
  subfamily) completely: which banked results constrain which locus (det-one line
  a+d=0; volume-blind locus 1+2λ=0 at the orbit-volume level; swap-forced λ=0; ±1
  conditional points). Deliverable: the honest L2 modulus is identified exactly (which
  scalar(s), on which subfamily, with which banked pins) — resolving the MAP's "E07's k
  = the joint audit's lambda" seat-level equation into matrix-level precision.
- **T5 (conditional-gate assembly).** The stratum × supplied-reduction forcing table
  (C3), each cell cited to its banked source; no new conditional gates invented.
- **T6 (the L1/L2 re-tag).** Final ledger: L1 (stratum) and L2 (transverse modulus)
  re-tagged as DERIVED / CONDITIONAL(on cited supplied structure) / MODULUS-CARRIED,
  per the Stage-1 evidence only.

Deliverables: `derive_routeB_stage1.py` (exact SymPy, zero-residual checks, JSON +
stdout), `EXACT_DERIVATION.md`, `STRATUM_SURVIVAL_LEDGER.tsv` (stratum × constraint
layer → FORCED-OUT(identity) | CONDITIONAL(cite) | SURVIVES-WITH-MODULI(list) |
UNCONSTRAINED), `AUDIT_REPORT.md`, blind-verifier record + preserved independent script.

## 3. Falsifiers (frozen)

- **F-A (re-derivation masquerade).** Any claimed UNCONDITIONAL elimination whose
  forcing constraint belongs to the 18-family pointwise active set already proven
  rank-zero. Fires → that elimination is VOID and recorded as such.
- **F-B (bank contradiction).** Any claim of pointwise metric-only selection of a
  non-scalar generator (contradicts the joint-selector no-go structural theorem), or
  any unconditional spectator-uniqueness claim (contradicts E07/E08). Fires → halt,
  audit the derivation before anything is banked.
- **F-C (symbolic failure).** Any zero-residual SymPy check fails → recorded as-is;
  exit nonzero; no massaging.
- **F-D (quantifier slip).** Unique-in-subfamily promoted to unique-in-class (the E06
  scar: "unique ONLY in the stronger class"). Verifier hunts this explicitly on every
  uniqueness/forcing statement.
- **F-E (imposition).** Any acceptance criterion that filters by merit (expected
  shape/GR-likeness) rather than provenance/honesty. The ledger records eliminations by
  FORCING IDENTITY only.

## 4. Premise ledger (chose or derived — each tagged)

| Premise | Tag |
|---|---|
| Registered positive triangular chart | THEORY (banked E02 registration) — chart-covariance of strata is itself T1's question, NOT assumed |
| Fixed founded base generator H=diag(−1,1) | DERIVED (G01/G02) |
| Pointwise one-parameter extension scope | THEORY (E02 record scope stamp) — scope travels |
| Connected local Lorentz group as the gauge group | THEORY (requirement 7 / E11) |
| J01–J15 as obligations | THEORY (joint provenance audit 2026-07-28) |
| Banked reduced-holonomy conditional facts | DERIVED (07-27/28 audits; used as cited inputs, never adopted) |
| Zero pointwise active selector rank | DERIVED (07-26 selector audit; the reason Stage 1 uses only C1–C4) |
| SymPy/CPU, bounded, no GPU, no solves | Category-A conditioning (soundness check only) |
| NO action, source, carrier, density law, physical branch, alpha value | EXCLUDED (authority boundary — unchanged) |

## 5. Outcome classes and pre-committed ceiling

O1: one or more strata natively eliminated (a derivation, with the exact forcing
identity and the constraint layer named). O2: a stratified family survives with
explicit moduli — the moduli ledger IS the deliverable. O3: all reduction is
conditional-on-supplied-structure — the exact conditional map is the deliverable and
L1/L2 become explicitly-carried moduli. ALL THREE are first-class.

**Maximum-conclusion ceiling (pre-committed):** the strongest bankable statement is
"stratum/member X is eliminated or forced ONLY as scoped (registered chart, pointwise
one-parameter class, conditional on the cited supplied structure); L1/L2 re-tagged per
the final ledger." NO adoption of any supplied reduction, NO physics selection, NO
response one-form or action claims, regardless of what the algebra shows.

## 6. Method (same machinery as the selector theorem)

(1) This preregistration committed first. (2) Derivation agent writes the script +
EXACT_DERIVATION.md + ledger into the package; every symbolic check is a zero-residual
SymPy test; deterministic output. (3) Blind adversarial verifier (zero-context framing;
same-session-spawned — the not-a-hosted-external-model caveat travels per the
uniqueness-consumer META finding): independent re-derivation preserved in-package,
byte-identical production rerun, explicit F-A/F-B/F-D hunts, verdict framed as
ADJUDICATE not confirm. (4) AUDIT_REPORT.md banks grade + target-outcome table +
limits-that-travel + verifier record; CORRECTION_LAYER.md if the verifier requires
amendments. Anti-hang: pure symbolic CPU; no GPU; no numeric solves; single process.

## 7. Known flags carried in (from the recon pass, agent a89d906681d47f677)

- The "P4 evidence digest" is not a file; the fifteen-requirement checklist is cited as
  MAP.md §2 with per-item sources rebuilt where load-bearing.
- The 28-equation/12-completion negative-map counts are cited via HANDOFF.md's banked
  closure block (parent audits 07-24/25); background context only, not load-bearing here.
- The E07-k vs isotropic-λ seat mismatch is T4's explicit subject.
