# PREREGISTRATION — Fixed-metric reciprocal-plane selector theorem (constant-alpha family)

Date: 2026-07-28. Branch: `review/external-perspective-2026-07-28` (worktree from `0659101`;
`grok` untouched). Authorized by Charles ("Run the alpha selector theorem derivation")
following `udt_uniqueness_consumer_audit_2026-07-28/AUDIT_REPORT.md` F1 deliverable item 1.
CPU-only symbolic derivation (sympy) + numeric spot checks; no solve, no GPU, no canonization.

## Question (declared: METRIC-LED)

Within the registered stationary descended constant-alpha family (the higher-isometry
ownership audit's family), for a FIXED metric: does the inherited founded-pair certificate
select one of the two topology-supplied reciprocal planes, and exactly where does selection
fail? This asks WHAT THE FIXED METRIC DOES; it does not target a desired plane — a clean
refutation (both planes pass off the known witness stratum) is a fully successful outcome.

## Setting (inherited, exact)

`g = -u(c_E dt + alpha A)^2 + u^{-1} A^2 + q_B` on `R x S3`; `u = e^{-2phi} > 0`; `A` the
registered Hopf connection (curvature F nondegenerate on the base); `K` the stationary Killing
field; the two unoriented primitive free circle lines of the toric S3 are `{V, Y}` with
`A(V) = 1`, `f = A(Y)`; `H = Y - fV`, `b = q_B(H,H) > 0` on principal orbits; transverse
derivative `X`, `chi = X(phi)`, `X(u) = -2 chi u`, `X(f) = df`, `X(b) = db`.

## Premise ledger

| Premise | Tag |
|---|---|
| Family + registration (block-screen, stationary, descended, constant alpha, Hopf bundle) | CHOSE — inherited P06/P07/P14-class; every conclusion scoped to it |
| Candidate ruler set = the two free circle lines {V, Y} | DERIVED — parent R05 two-free-lines theorem (topology forces exactly two) |
| Clock generator = K | DERIVED-inherited — parent clock scan (family-wide); fixed-profile caveat noted: at fixed profile the clock-scan cancellation question is OPEN in the parent; this theorem CONDITIONS on clock=K and says so |
| Certificate C(P) for plane P = span(K,W): (i) |det G_P| constant on principal orbits (constant reciprocal area); (ii) K an eigenvector of D_P = G_P^{-1} X(G_P); (iii) eigenvalue pair exactly (-2chi, +2chi) (founded rates) | DERIVED-inherited — the parent founded-pair certificate + D1's clock/ruler eigenstructure; CERTIFICATE-RELATIVE (R09 caveat travels: full-response invariance is a different criterion and disagrees where df != 0) |
| df not identically 0 for the second line | TO BE DERIVED in-run (Cartan: independent free line projects nontrivially; F nondegenerate). If underivable, reported as a gap, not pinned |
| Principal orbits only (b > 0); caps excluded | THEORY — parent: D undefined at rank-dropping caps; cap gluing remains OPEN and is NOT claimed |

## Frozen theorem targets (to be proven exactly or refuted)

- **T1 (registered plane passes universally):** span(K,V) satisfies C for every metric of the
  family and every alpha: det G_KV = -c_E^2 exactly (constant), D_KV upper-triangular with
  K-eigenvalue -2chi and second eigenvalue +2chi.
- **T2 (second plane, K-eigenline leg):** K is an eigenvector of D_KY at a point iff
  alpha * df = 0 there; the off-eigenline component is exactly
  `-alpha c_E df u^2 / (b u + f^2)`.
- **T3 (second plane, area leg):** |det G_KY| = c_E^2 (b u + f^2) is constant iff
  `X(b u + f^2) = 0`.
- **T4 (Cartan):** for the second free line, df cannot vanish identically (derive; state the
  exact hypothesis used).
- **T5 (selector classification, the deliverable):** for a fixed metric on principal orbits:
  - if `alpha != 0`: C selects span(K,V) uniquely (span(K,Y) fails T2 on the open set where
    df != 0, nonempty by T4);
  - if `alpha = 0`: C selects span(K,V) uniquely iff `b u + f^2` is nonconstant; the
    EXCEPTIONAL STRATUM is exactly `{alpha = 0 and b u + f^2 constant}` (equivalently
    alpha*df == 0 and constant), on which BOTH planes satisfy C and this certificate is silent;
  - the parent's double-plane witness lies on the exceptional stratum (control: verify
    b u + f^2 = 1 there), and at its exchange-symmetric points selection is PROVABLY
    impossible (parent isometry); between "certificate silent" and "provably impossible" on
    the rest of the stratum remains OPEN and is not claimed.
- **T6 (secondary, if it falls out cheaply):** the constant-area leg for a general candidate
  line `W = mV + nY` at fixed metric — record what the algebra gives; no claim frozen.

## Falsifiers

- F-A: an admissible fixed metric with `alpha*df != 0` somewhere on which BOTH planes satisfy
  C (kills T5 branch 1).
- F-B: a generic `alpha = 0` metric (`b u + f^2` nonconstant) on which span(K,Y) satisfies C
  (kills T5 branch 2), or an exceptional-stratum metric on which C is NOT silent.
- F-C: an algebra error in T1-T3 (off-term, determinant, or rate formulas) found by the
  independent implementation or blind verifier.
- F-D: chart/coframe dependence of C (the certificate must be well-defined given (g, K, the
  line W, X) — if C's value depends on presentation choices beyond these, the theorem is void).

## Maximum conclusion (pre-committed ceiling)

A conditional fixed-metric plane-selection theorem with an exactly characterized exceptional
stratum, inside the registered constant-alpha family, on principal orbits, using the inherited
certificate, CONDITIONAL on clock=K — closing the parent's
`GENERIC_FIXED_METRIC_SELECTION_OPEN` for the topology-supplied two-candidate set. It selects
NO physical branch, alpha value, action, source, carrier, density law, dynamics, or mass; it
does not extend through caps; the R09 certificate-relativity and all inherited CHOSE stamps
travel. If a falsifier fires, the refutation is banked with equal standing.

## Method

1. Derivation agent: full sympy derivation of T1-T5 (+T6 if cheap), general symbols
   (u, f, b, chi, df, db, alpha, c_E free), no witness specialization except as the T5 control;
   numeric spot checks at random admissible parameter points; witness control (must land ON
   the exceptional stratum with both planes passing). Writes EXACT_DERIVATION.md +
   derive_alpha_plane_selector.py + DERIVATION_RESULT.json into this package.
2. Blind adversarial verifier (zero-context-framed): independent re-derivation, hunts F-A
   through F-D, quantifier slips, and the T4 hypothesis; verdict recorded.
3. Bank AUDIT_REPORT.md with scope stamps; review branch only.
