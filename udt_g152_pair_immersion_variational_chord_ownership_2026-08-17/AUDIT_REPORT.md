# G152 audit report — pair-immersion variational chord ownership

Date: 2026-08-17
Grade: `VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_PASS`

## Result

For one supplied smooth regular calibrated timelike pair immersion,

\[
J_1=\beta T u+Ln,
\qquad
r=J_1-\beta J_0=Ln,
\qquad
\xi=\rho n,
\]

with

\[
\rho=X_{\max}\tanh\phi_{\rm pair}
=X_{\max}\frac{L-T}{L+T}.
\]

The immersion owns `J1`, and its pullback metric owns the orthogonal ruler `r`. It does not
automatically identify either with the working reciprocal chord `xi`.

For orientation \(\epsilon=\pm1\), ruler equality is exactly

\[
\xi=\epsilon r
\iff
\rho=\epsilon L
\iff
T=L\frac{X_{\max}-\epsilon L}{X_{\max}+\epsilon L}.
\]

Equivalently, if this identification is supplied,

\[
X_{\max}^{(\epsilon)}
=\epsilon L\frac{L+T}{L-T}.
\]

Coordinate equality additionally requires \(\beta\equiv0\) on the comparison neighborhood.

For \(f=\rho/L\), exact normalized-clock carry is

\[
[u,\xi]
=L\,u(f)n
+f\left[J_1(\log T)-u(\beta T)\right]u.
\]

Thus a nonzero chord is connecting exactly when \(u(f)=0\) and
\(J_1(\log T)-u(\beta T)=0\). Exact counterexamples prove that magnitude equality and connecting
carry do not imply one another.

## Interpretation

This closes the local ownership question from G151. The pair immersion supplies the ingredients and
an exact test; terminal reciprocity alone does not force the test to pass. If a coherent physical
family is later shown to satisfy ruler equality, constancy of the displayed candidate across that
family is a necessary test for a universal `X_max`. It is not sufficient by itself and no value is
derived here.

## Evidence

- preregistration: commit `09a45aa3`;
- production exact algebra: `derive_variational_ownership.py`;
- independent Lie-bracket replay: `verify_variational_ownership_independent.py`;
- package gate: `VERIFICATION_RESULT.json`;
- fresh adversarial result: `FRESH_ADVERSARIAL_REVIEW.md` (`PASS`, no repair).

## Maximum conclusion

```text
PAIR_IMMERSION_OWNS_COORDINATE_AND_ORTHOGONAL_VARIATIONS_BUT_NOT_THEIR_IDENTIFICATION_WITH_WORKING_XI__
EXACT_MAGNITUDE_SHIFT_LAPSE_AND_COMMUTATOR_CONDITIONS_CLASSIFIED__
UNIVERSAL_XMAX_WOULD_REQUIRE_CANDIDATE_CONSTANCY_ACROSS_THE_SUPPLIED_FAMILY__
PHYSICAL_IDENTIFICATION_QUERY_HISTORY_DYNAMICS_XMAX_VALUE_AND_COMPLETION_OPEN
```
