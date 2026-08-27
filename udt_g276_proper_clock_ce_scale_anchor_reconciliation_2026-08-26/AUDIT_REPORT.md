# G276 audit report — proper-clock / `c_E` scale reconciliation

Date: 2026-08-26

## Landing

`VERIFIED-WITH-CAVEATS`

One independently calibrated positive proper-clock record on the exact modeled timelike segment
has homothety weight \(+1\) and conditionally fixes G275's single remaining scale:

\[
\ell=\frac{c_E\tau_*}{\bar C}.
\]

`c_E` then carries the attached time into a length and hence into the W5 representative
\(x=\ell\chi\). `c_E` alone, the dimensionless \(M=\operatorname{sech}\delta\) and
\(\chi=\tanh\delta\), scale-invariant increment ratios, and metric self-evaluation do not fix
\(\ell\).

## Evidence

- Preregistration was committed and pushed at `e5fddc76` before implementation.
- The production derivation passed 22 exact symbolic and typed checks.
- An implementation-distinct standard-library verifier passed 20,000 exact-rational cases and
  300,003 assertions without importing production code or reading production output.
- It rejected 20,000 inconsistent second records, 20,000 metric-generated self-records, and 20,000
  same-segment identity mismatches.
- Eight hostile controls passed: six implementation mutations and two typed-scope overclaims.
- No observational values, fits, new kernel mechanisms, metric modifications, history, operational
  distance, or `X_max` selection entered.

## Interpretation

Charles's tape-measure intuition is conditionally correct. A calibrated clock interval plus `c_E`
is a physical length attachment. The exact epistemic split is:

- `OBSERVED`: `c_E` is the clock/ruler conversion;
- `SUPPLIED`: one independent same-segment clock record \(\tau_*\);
- `DERIVED_CONDITIONAL`: the unique scale \(\ell=c_E\tau_*/\bar C\);
- `OPEN`: which record, segment, global history, distance protocol, and boundary Nature realizes.

This is a reconciliation of already-owned G252 and G275 results, not an added mechanism.

## Four gates

1. preregistered: **PASS**;
2. full bounded space: **PASS** for positive constant homotheties and identified positive timelike
   segments;
3. independently verified: **PASS**;
4. premises audited: **PASS**, with the supplied independent-clock and supplied-history caveats.

The result is not canon and has not yet received fresh external adversarial review.
