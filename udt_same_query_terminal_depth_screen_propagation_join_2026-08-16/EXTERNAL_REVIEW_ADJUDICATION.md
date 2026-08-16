# External review adjudication

Date: 2026-08-16
First-review landing: `CONDITIONAL_SAME_QUERY_DEPTH_JOIN_DERIVED`

## Accepted

The reviewer independently accepted the load-bearing regular-stratum result:

- terminal `phi_pair` is recovered exactly from the supplied regular pair metric;
- `B_j B_i^-1` contains `exp(Delta kappa) D(Delta phi)` after common-scale separation;
- composition, reversal, the `c_eff/c_E` normalization, and the G108 reparameterization are correct;
- the identification is a genuine conditional same-query join, not a renaming or a universal law.

## Registered repairs

1. Replaced the vacuous zero-rate booleans with explicit production and independent controls:
   `phi_pair(z)=z^2`, regular `W(z)=exp(z) I`, finite endpoint depth, zero local depth rate,
   nonzero screen-area rate, and equal depth on opposite sides of the turning point.
2. Added a genuine caustic control `W(z)=z I`, for which `det W(0)=0`, the optical trace is
   `2/z`, and the independent inverse fails at the singular point.
3. Corrected the malformed TeX in equation (7).
4. Refactored `verify_package.py` to replay in a temporary copy. Its default mode is now read-only;
   only the explicit local `--write-result` option updates the saved package-verification artifact.

These repairs strengthen evidence for the declared degeneracy boundaries. They do not enlarge the
regular-stratum conclusion or claim continuation through a turning point or caustic.

## Follow-up result

The sealed follow-up accepted all four repairs, found no central-algebra regression, and retained
`CONDITIONAL_SAME_QUERY_DEPTH_JOIN_DERIVED`. It identified one nomenclature drift between that
accepted primary landing and the package's longer internal label. The package now uses the accepted
primary landing consistently and carries the more specific ownership statement as a subordinate
clause. No additional external review is required for that editorial harmonization.
