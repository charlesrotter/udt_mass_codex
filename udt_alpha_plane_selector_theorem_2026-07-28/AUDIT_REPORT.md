# Fixed-metric reciprocal-plane selector theorem — AUDIT REPORT

Date: 2026-07-28. Branch: `review/external-perspective-2026-07-28` (worktree at `0659101`;
`grok` untouched). Preregistration: `PREREGISTRATION.md` (committed `6ca0297` BEFORE the
derivation ran). CPU-only symbolic derivation; no solve, no GPU, no canonization.

**GRADE: VERIFIED-WITH-CAVEATS** — blind adversarial pass (zero-context-framed,
same-session-spawned agent, NOT a hosted external model; the distinction stated per the
uniqueness-consumer audit's META finding) returned **BANKABLE-AS-SCOPED**: fully independent
re-derivation (52 checks) including a **4D coordinate model with no jet formalism**, four
covariance checks, byte-identical deterministic rerun, and a demonstration that the one
corrected auxiliary identity genuinely fails in its uncorrected form. No preregistered
falsifier fired.

## Theorem (as proven, exactly scoped)

Within the registered stationary descended constant-`alpha` family, on principal orbits
(`b > 0`), conditional on clock = K, using the inherited founded-pair certificate C
(constant reciprocal area; K an eigenvector of the plane-restricted response; rates exactly
`(-2chi, +2chi)`), for the two topology-supplied candidate planes `{span(K,V), span(K,Y)}`:

- **`alpha != 0`:** C selects `span(K,V)` uniquely. `span(K,V)` passes for every member and
  every alpha (`det G_KV = -c_E^2` exactly; `D_KV = [[-2chi, -4 alpha chi/c_E],[0, +2chi]]`);
  `span(K,Y)` fails the K-eigenline leg wherever `df != 0` via the exact fully-general
  off-eigenline component `-alpha c_E df u^2/(b u + f^2)`, and `df != 0` on a nonempty set is
  DERIVED (Cartan; see T4 below) — in fact at every principal point under (H1)-(H5), a
  strengthening verified sound but NOT load-bearing (the theorem needs only "somewhere").
- **`alpha = 0`:** C selects `span(K,V)` uniquely iff `b u + f^2` is nonconstant along X. The
  rate leg and the area leg collapse to the SAME scalar condition `X(b u + f^2) = 0` — so the
  **exceptional stratum is exactly `{alpha = 0 and b u + f^2 constant}`**. On it, BOTH planes
  satisfy C and this certificate is silent. The parent's double-plane witness lies on it
  (`b u + f^2 = 1` exactly, both planes passing, verified twice); at its exchange-symmetric
  points selection is provably impossible (parent isometry); on the rest of the stratum the
  question remains OPEN.

This closes the parent's `GENERIC_FIXED_METRIC_SELECTION_OPEN` for the topology-supplied
two-candidate set, as a necessary-and-sufficient classification with an exact exceptional
stratum — certificate-relative, clock-conditional, family-scoped.

## Target outcomes

| Target | Outcome |
|---|---|
| T1 registered plane passes universally | PASS (exact, all alpha) |
| T2 K-eigenline iff `alpha*df = 0`; off-term exact | PASS (fully general in the family) |
| T3 area leg iff `X(b u + f^2) = 0` | PASS |
| T4 `df` not identically zero for the second line | **DERIVED-WITHIN-REGISTRATION** (verifier's grade, adopted): the Lie-derivative chain deriving `L_Y A = 0` from the registered isometries is a genuine derivation — the parent registration does NOT contain it and the parent had *hypothesized* bundle preservation — but its hypotheses (H1)-(H5) are themselves registration/CHOSE. Pointwise strengthening sound, non-load-bearing. |
| T5 selector classification | PASS — the theorem above |
| T6 general line `mV + nY` | RECORD ONLY: `det = -c_E^2((m+nf)^2 + n^2 b u)` (alpha drops out); `X(det) = -c_E^2(2 m n df + n^2 X(b u + f^2))`; no claim |

Falsifiers: F-A/F-B excluded by proven iffs; F-C — one incident on an AUXILIARY control
(outside T1-T6): the parent §6 identity `det D_KY + 4chi^2 = alpha^2 u^2 df^2` is
witness-scoped; the general stratum form carries `1/(b u + f^2)` (verifier exhibited a numeric
point where the unscoped form fails; parent text correct in its witness context). Documented in
the script header and EXACT_DERIVATION.md §6. F-D — no presentation dependence under four
independent transformation checks (W-rescale, X-rescale, K-rescale, Y-sign); the certificate
uses only `g(K,K), g(K,W), g(W,W), X`.

## Evidence

- `derive_alpha_plane_selector.py`: 37/37 zero-residual sympy checks + 7/7 seeded numeric
  points, exit 0, deterministic (`DERIVATION_RESULT.json`, `DERIVATION_STDOUT.txt`).
- `INDEPENDENT_REDERIVE.py` (blind verifier's script, preserved): 52/52 checks incl. the 4D
  coordinate model, re-run in-package (`INDEPENDENT_STDOUT.txt`, exit 0, no failures).
- Verifier rerun of the derivation script: stdout and JSON **byte-identical**.
- Witness control: exceptional-stratum landing + both-planes-pass verified by two independent
  methods (jet formalism; direct `d/d eta`).

## Limits (travel with every use of this result)

1. Family CHOSE (block-screen, stationary, descended, constant alpha, registered Hopf bundle —
   P06/P07/P14-class inheritance). 2. Clock = K CONDITIONAL (the parent's fixed-profile clock
   question is untouched). 3. Certificate-relative (R09: the full-response criterion is a
   different, disagreeing criterion; this theorem does not adjudicate between certificates).
4. Principal orbits only; caps (`b -> 0`) excluded; cap gluing OPEN. 5. Exceptional-stratum
   remainder (non-exchange-symmetric members) OPEN. 6. At constant depth (`chi = 0`) the
   founded rates are degenerate (the K-eigenline leg still discriminates for `alpha != 0` —
   verifier's note — but "founded-rate" language has no content there). 7. The pointwise
   `df != 0` strengthening is an observation, not load-bearing. 8. **No physics selected**: no
   physical branch, alpha value, action, source, carrier, density law, dynamics, or mass. The
   theorem says: IF the universe is a fixed member of this family off the exceptional stratum,
   THEN the founded certificate picks the reciprocal plane uniquely — which member, and whether
   this family is realized, remain entirely open.

## Verifier record

Blind adversarial pass, 2026-07-28 (scripts preserved: `INDEPENDENT_REDERIVE.py`; scratch
rerun byte-identical). Attacks: independent re-derivation (jet + 4D non-jet model) —
CONFIRMED, no F-C; T4 grading — DERIVED-WITHIN-REGISTRATION (adopted above); T5 quantifiers —
CONFIRMED, strengthening sound and correctly quarantined; F-D covariance — does not fire
(four checks, two beyond the derivation's own); witness + incident — CONFIRMED, uncorrected
auxiliary form demonstrated to fail; script determinism — byte-identical; prose audit — all
scope stamps present, conclusions within the preregistered ceiling; two conservative
under-claims noted (LIMITS #6; leg-(ii) quantifier reading), no action forced. Overall:
**BANKABLE-AS-SCOPED**.
