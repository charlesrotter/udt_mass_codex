# External Adversarial Review — G264

Disposition: `ACCEPT_WITH_REPAIRS`

I inspected only the sealed G264 intake package under `/review/udt_g264_negative_phi_native_selectivity_classification_2026-08-25` and did not continue the research program beyond that scope.

The bounded scientific landing survives. Re-deriving from the registered metric
`ds^2=-f(r)dt^2+dr^2/f(r)+r^2 dOmega^2` gives the same invariant structure claimed in the intake:

- `R = -f'' - 4 f'/r - 2(f-1)/r^2`
- `K = (f'')^2 + 4(f'/r)^2 + 4((f-1)/r^2)^2`

These formulas are internally consistent with the mixed Einstein channels claimed in the intake and
they reproduce standard checks such as Schwarzschild and Reissner-Nordstrom scalar flatness and the
constant-curvature `f=1+C r^2/L^2` representative.

I also checked the two required witness classes.

- Negative bump witness: `f=1+epsilon (r/L)^2 exp(-(r/L)^2)` stays `>1` for every finite `r>0`,
  has smooth-center expansion `f=1+(epsilon/L^2) r^2+O(r^4)`, hence finite center invariants
  `R(0)=-12 epsilon/L^2` and `K(0)=24 epsilon^2/L^4`, tends to `1` at infinity, and has
  static-slice radial metric bounded below by a positive Euclidean multiple, so the radial proper
  length to infinity diverges. This is a valid counterfamily against any sign-only exclusion.
- Power-law end: under the preregistered assumption `f ~ C (r/L)^alpha`, the curvature exponents are
  `alpha-2` for `R` and `2 alpha - 4` for `K`; the normalized static acceleration scales as
  `r^(alpha/2-1)`; radial proper length scales as `int r^(-alpha/2) dr`; spatial volume scales as
  `int r^(2-alpha/2) dr`. The reported thresholds `alpha=2` for curvature/acceleration/radial
  length and `alpha=6` for spatial volume are correct.
- Alpha-two representative: for `f=1+C r^2/L^2`, direct substitution gives
  `A_parallel=(r^2 f''-r f')/2 = 0` and `A_perp = 1-f+r f'/2 = 0` exactly, with
  `R=-12C/L^2`, `K=24C^2/L^4`, logarithmically divergent radial proper length, and finite
  nonzero normalized acceleration limit `sqrt(C)/L`.

I found no intake-local promotion of the conditional geometric classifiers into a field equation,
physical mass condition, history selector, or `X_max` theorem. The scope guards in
`MAP.md`, `PREREGISTRATION.md`, `STATUS_LEDGER.tsv`, `OWNERSHIP_ATLAS.tsv`, and
`AUDIT_REPORT.md` remain intact.

Defects:

1. The package overstates what the “independent verification” establishes.
   Evidence:
   [verify_independent.py](/review/udt_g264_negative_phi_native_selectivity_classification_2026-08-25/verify_independent.py:29)
   hardcodes the target scalar formula as `scalar_direct = -fpp - 4*fp/r - 2*(f-1)/r**2` and
   [verify_independent.py](/review/udt_g264_negative_phi_native_selectivity_classification_2026-08-25/verify_independent.py:41)
   hardcodes the target Kretschmann formula as
   `k_direct = fpp**2 + 4*(fp/r)**2 + 4*((f-1)/r**2)**2`. The script then checks algebraic
   consistency against equally hardcoded channel/sectional expressions and sampled witnesses, but it
   does not independently derive those formulas from the metric. That means Gate 3 language in
   [EVIDENCE_GATES.md](/review/udt_g264_negative_phi_native_selectivity_classification_2026-08-25/EVIDENCE_GATES.md:14)
   and the evidence wording in
   [AUDIT_REPORT.md](/review/udt_g264_negative_phi_native_selectivity_classification_2026-08-25/AUDIT_REPORT.md:31)
   are too strong if read as “second derivation from first principles.”
   Required repair:
   either downgrade the wording to “implementation-distinct consistency replay that is blind to
   production imports and saved results,” or strengthen `verify_independent.py` so it derives the
   curvature channels from the metric without embedding the target invariant formulas up front.

Bottom line:

- `phi<0` alone does not invalidate or select profiles of the primary metric.
- The smooth negative bump family is a valid finite counterfamily.
- The conditional power-law thresholds are correct.
- The `alpha=2` representative satisfies the claimed angular cancellation exactly.
- The landing should be banked only after the replay-independence wording or implementation is
  repaired.
