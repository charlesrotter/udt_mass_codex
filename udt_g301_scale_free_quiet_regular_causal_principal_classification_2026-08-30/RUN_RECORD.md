# G301 run record

Date: 2026-08-30

- Device: CPU
- Arithmetic: exact `fractions.Fraction`
- GPU: not used
- ODE/PDE solve: not used
- Grid or boundary: none
- Observations: none
- Source/action/matter/scale/`X_max`: none
- Production cases: 169 coefficient-grid + 7,880 generic inverse + 4,000 principal covector
- Production assertions: 27,829
- Independent cases: 12,000 random rational coefficient cases plus 3,000 homogeneity and 5,000
  principal controls
- Independent assertions: 49,609
- Full-space invariant-basis census: 20-dimensional algebraic curvature, 10-dimensional symmetric
  output, six Lorentz generators, 1,200 equivariance rows, 200 unknown map components, exact
  modular rank 198 under two primes, two exact independent null vectors, 53,605 assertions
- Output files: `DERIVATION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`,
  `INVARIANT_BASIS_VERIFICATION.json`, `CATCH_PROOF_RESULT.json`,
  `PACKAGE_VERIFICATION_RESULT.json`
- Stop condition: all preregistered coefficient strata classified or any exact assertion fails
- Fresh repair-only external review: `ACCEPT_REPAIRS`; all registered `python3 -S` replays passed
  from an ephemeral mirror of the sealed read-only intake
- Current 285-row premise verifier: pass
- Repository suite after startup compaction: 197 passed, 1 expected xfail
