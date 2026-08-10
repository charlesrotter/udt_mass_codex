# Cold external review dispatch

Audit this package and only the exact source files listed in `SOURCE_MANIFEST.tsv` as a read-only
adversary. Reconstruct the load-bearing algebra rather than trusting the verdict.

## Required questions

1. Is `D_X=P_H nabla_X` globally and correctly typed as a metric connection on the normal bundle
   of the supplied pair foliation for all four directions?
2. Independently reproduce the four connection coefficients and all six curvature components,
   enforcing the noncommuting scalar-jet identities.
3. Test the special-role atlas: `lambda=-1` clock contraction, `lambda=0` horizontal coefficients
   and Hopf-basic metric, `lambda=1` first-gradient cancellation, and absence of generic complete
   flatness.
4. Adversarially audit the distinction between the Hopf Ehresmann connection, the projected normal
   connection, ambient Lorentz transport, and the still-open physical non-isometric observer map.
5. Check the path-groupoid identity/composition/reversal claim and gauge/`O(2)` statements.
6. Check the vertical-contraction algebra and the conclusion that no supplied lambda yields
   generic base-curvature descent. Identify any missing invariance or holonomy condition.
7. Audit the global `R x S3 -> S2` and chart/finite-cell claims for overstatement.
8. Hunt circular verification, assigned formulas, silently frozen jets, branch selection, and
   scope inflation.

Return exactly one primary verdict: `VERIFIED_AS_STATED`, `VERIFIED_WITH_CORRECTIONS`,
`TYPE_FAILURE`, `ALGEBRA_FAILURE`, `GLOBAL_OVERSTATEMENT`, or a more precise landing. State the
maximum defensible claim and every remaining open ownership seam.

Do not edit files, continue the research, inspect anything outside the sealed intake, or inspect
the protected curvature-atlas contents.
