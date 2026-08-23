# G230 repair record

Date: 2026-08-23

## R1 — ceiling guard test line wrapping

The first focused test searched for one literal sentence across a Markdown line break and failed
despite the intended ceiling being present. The test now normalizes whitespace before matching the
sentence. This was a verifier defect only; no scientific formula, result, or landing changed.

## R2 — independent omitted-term diagnostics

The first independent output recorded only commutator residuals for the connection-product-only
and covariantization-only controls. The covariantization term alone correctly supplies the
antisymmetric commutator for the frozen witness, but it fails differentiated Bianchi. The output
was expanded to record both constraint families, preventing that valid structural fact from being
misread as evidence that the connection-product term is optional. The full calculation and landing
were unchanged.

## R3 — explicit lower-gate residuals for the counterexample

The first production boolean inferred that the nonzero-curvature, zero-`D`, zero-`E` witness passed
G227/G228 from its typed basis and the homogeneity of differential Bianchi. A fresh geometry review
correctly requested direct machine assertions. Production and the independent full-21-slot replay
now calculate the G227 algebraic-Bianchi residuals, the complete G228 zero-`D` residuals, the G230
zero-`E` differentiated-Bianchi residuals, and the nonzero G230 commutator residual explicitly.
This strengthens certification without changing the witness, ranks, formulas, or landing.

## R4 — structured history-promotion hostile

The preregistration required a hostile catch against promoting pointwise fourth-order realization to
a finite-region field or physical history. The first suite relied on prose ceiling guards and did
not count a structured positive-overclaim mutation. A scope record with separate finite-region,
value-generation, and physical-history fields is now checked; flipping the history field is caught.
The hostile suite increases from eight to nine valid catches. No scientific result changed.

## R5 — frozen-source verification across startup promotion

The preregistered source manifest includes `LIVE.md` and the premise registry as they existed at
commit `3808e397`. Those files must change when G230 is promoted, so comparing only against current
working-tree bytes would incorrectly invalidate the frozen pre-outcome source record. Source
verification now accepts current bytes when unchanged and otherwise verifies the exact blob at the
preregistration commit with `git show`. Preregistration hashes remain current-file checks. This is a
provenance repair; the source manifest, scientific code, ranks, identities, and landing are
unchanged.
