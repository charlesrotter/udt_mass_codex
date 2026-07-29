# R09 certificate adjudication — AUDIT REPORT (gate b)

Date: 2026-07-28. Branch: `grok`. Preregistration committed `ed01bda` BEFORE the derivation
ran. CPU-only symbolic derivation; no solve, no GPU, no canonization.

**GRADE: VERIFIED-WITH-CAVEATS** — blind adversarial pass (zero-context-framed,
same-session-spawned agent, not a hosted external model) returned **BANKABLE-AS-SCOPED after
one required wording fix**, which is applied (EXACT_DERIVATION.md §4.2 + CORRECTION_LAYER.md
C1). The verifier independently rebuilt the algebra from the metric (47/47), added a jet-free
direct η-space computation of the conflict witness, reran the script byte-identically
(73/73), and confirmed both falsifier records.

## Result first — the adjudication SPLITS on the founded-rates leg

- **C_full WITH the founded-rates leg: NO-CONFLICT.** The full-response criterion is EMPTY on
  every admissible member wherever the banked certificate selects: on the (T4-guaranteed)
  nonempty open set `df != 0`, `alpha != 0` kills D3-invariance pointwise, and at `alpha = 0`
  invariance forces a `db`-locus whose second restricted rate `mu = 2chi + n*df/z != +2chi`
  breaks the founded pair. The parent R09 caveat DOWNGRADES to: "the full criterion is empty
  where the founded certificate selects — no crowning conflict is possible in this family."
  Robust to adding a K-eigenline leg.
- **C_full WITHOUT the leg: CONFLICT — falsifier F-b1 FIRED (first-class).** Exact witness:
  `alpha = 0, f = cos 2eta, u = 2 + f` (principal-orbit admissible; b > 0 everywhere). The
  planes span(K,2V+Y) and span(K,−3V+Y) are D3-invariant at EVERY principal point (complete
  list `(m+3n)(m−2n) = 0`), while C_restricted crowns span(K,V) within the topology-supplied
  pair (`bu+f^2 = 6+f` nonconstant) and the invariant planes FAIL the area leg. The two
  criteria crown DIFFERENT planes; since K is an exact D3 eigenvector at `alpha = 0`, **the
  entire adjudication hinges on the founded-rates leg alone.**
- **Verifier-found strengthening (CORRECTION_LAYER C1):** on that witness, over the general
  (m,n) candidate class, C_restricted is itself not single-valued — span(K,V−2Y) also passes
  all three legs — and the two criteria's satisfier sets are DISJOINT. C_restricted's
  single-valuedness is proven only for the topology-supplied pair {V,Y} (P-SEL T5's scope).
- **Cap-closure corollary (record, conditional):** strict two-cap closure of the invariance
  ODE forces `bu = 1−f^2`, i.e. the exceptional stratum, where C_restricted is silent — the
  leg-free conflict is then admissibility-reading-dependent (principal-orbit admissible;
  dissolves under strict two-cap completeness). Both readings stated; neither adopted; the
  banked CONFLICT verdict stands for principal-orbit admissibility.

## Target outcomes

| Target | Outcome |
|---|---|
| T-b1 invariant-plane enumeration | PASS — exact closed forms `I1 = alpha*c_E*df*u*z/b`, `I2*bu = alpha^2*df*u^2*z^2 + u*n*z*(2b*chi−db) + df*(n^2*bu−z^2)`; per-stratum lists incl. the degenerate locus `db = 2b*chi` (every plane invariant, founded rates) |
| T-b2 adjudication | SPLIT as above; F-b1 FIRED (leg-free), NO-CONFLICT (with-rates) |
| T-b3 df=0 crowning agreement | AGREE everywhere realizable; agreement-in-silence at `{alpha=0, db=2b*chi}`; the `{alpha!=0, db=2b*chi}` pointwise case is formal (region-unrealizable by Cartan) |
| T-b4 rate spectra | recorded (founded on span(K,V) and on the degenerate locus; unfounded `2chi + n*df/z` on the db-locus planes) |

F-b2 (algebra vs parent): NOT FIRED — parent D3 entries reproduced independently twice
(derivation and verifier, the latter from the metric and by jet-free η-computation).

## Evidence

`derive_r09_adjudication.py`: 73/73 zero-residual checks + exact-rational spot points per
stratum, exit 0, deterministic; verifier rerun byte-identical; verifier independent scripts
47/47 + witness checks (see verifier record). `DERIVATION_RESULT.json` field
`C_restricted_status` carries the C1 reading correction (CORRECTION_LAYER.md).

## Limits

1. Family CHOSE (P06/P07/P14-class inheritance); clock = K conditional; principal orbits.
2. NO ownership criterion is adopted as THE definition — that adjudication is Charles's; this
   package only proves the compatibility structure and that the founded-rates leg is the
   load-bearing discriminator.
3. The leg-free CONFLICT is scoped to principal-orbit admissibility (see corollary).
4. C_restricted single-valuedness beyond the {V,Y} pair is OPEN (C1).
5. No physics, no alpha value, no branch, no canonization.

## Verifier record

Blind adversarial pass, 2026-07-28 (scratch scripts /tmp/scratch_verify_b/, independent
rebuild 47/47). Attack 1 (formulation + closed forms): CONFIRMED — the L-test is a
complement-free membership characterization, basis-correct; F-b2 stands NOT-FIRED. Attack 2
(conflict witness): CONFIRMED incl. jet-free η-space recomputation; found the C1 uniqueness
scope slip (required fix, applied) and the span(K,V−2Y) second passer; F-b1 STANDS. Attack 3
(no-conflict emptiness): CONFIRMED — quantifier frozen pre-use (C3), isolated-point escape
closed by T4 under identical admissibility. Attack 4 (cap corollary): CONFIRMED as record;
K06 gate vacuous as encoded (C2, cosmetic); no softening of F-b1. Attack 5 (rerun):
byte-identical, 73/73. Attack 6 (prose): within the preregistered ceiling; LIMITS complete.
Overall: **BANKABLE-AS-SCOPED** after C1 — applied above.
