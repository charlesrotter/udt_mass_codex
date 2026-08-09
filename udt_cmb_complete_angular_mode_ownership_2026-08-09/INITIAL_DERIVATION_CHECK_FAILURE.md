# Initial derivation-check failure

Date: 2026-08-09

The first preregistered exact run stopped with 22/26 keys true. The determinant, inverse, full
operator, equatorial/full-volume mismatch, generic nonseparability witness, symmetry breaking,
center powers, general-screen counterexample, and source manifest all already passed.

The four failures were checker defects, not changed physical premises or equations:

1. `K04` used a Python stride selecting coordinate indices `(t,theta)` rather than the intended
   `(t,psi)` metric block. It is repaired with an explicit matrix extraction.
2. `K09` compared `sqrt(r^2)` directly to `r` while the symbolic radius lacked a positivity
   assumption. It is repaired as the exact squared-volume identity on the stated regular chart.
3. `K22` asked SymPy to integrate an over-general symbolic integer Fourier difference and received
   an unevaluated conditional form. It is repaired by the preregistered concrete equal/unequal
   character controls.
4. `K26` searched a semantic phrase across a Markdown line break. It is repaired by whitespace
   normalization before the exact phrase check. The second run showed that the report's controlling
   wording is actually `absent mode weights` plus `physical population rule`, rather than the
   paraphrase used by the initial predicate; the predicate was narrowed to those two literal source
   anchors. All 25 algebraic/source-identity keys passed on that second run.

No candidate, equation, result threshold, or maximum conclusion was changed after inspection.

The independent verifier's first invocation also stopped before arithmetic because its validator
looked for the paraphrase `extra r`, while the machine payload says `equals r times`. The validator
was changed to the literal payload wording; no evidence value or acceptance condition changed.
After the document-census checks were added, `V20` likewise stopped on a Markdown line break inside
`C1 is CHOSE`; after whitespace normalization it exposed that the second predicate was a paraphrase
rather than the document's literal `selects no preferred m and no amplitude`. `V20` now checks the
two literal scope anchors.
