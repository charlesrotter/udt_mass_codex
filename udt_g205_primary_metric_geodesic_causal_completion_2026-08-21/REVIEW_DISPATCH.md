# G205 fresh adversarial review dispatch

Date: 2026-08-21

## Role

Act as a cold mathematical reviewer. Try to refute the landing; do not continue the research or
suggest downstream mechanisms.

## Required audit

1. Re-derive the timelike/null/spacelike first integrals from the full metric and check every sign.
2. Test whether the center, all `E!=0` outer geodesics, causal `E=0`, spacelike `E=0`, and
   finite-radius trapped/turning cases really exhaust maximal geodesics.
3. Check the compact-imprisonment ODE extension argument for hidden Lorentzian velocity failures.
4. Check optical completeness and the direct proof that `t=constant` slices are Cauchy. Do not
   accept global hyperbolicity from curvature decay alone.
5. Verify the circular-null condition, exact `a_crit(n)`, root count, and stability signs.
6. Audit terminology: finite Killing horizon, event horizon, asymptotic flatness, maximal extension,
   physical history, and `X_max` must remain distinct.
7. Run the registered no-write package replay and hunt circular or vacuous assertions.

## Required return

Return exactly one primary verdict:

- `VERIFIED_WITH_CAVEATS`;
- `REPAIR_REQUIRED_WITH_LANDING_RETAINED`;
- `LANDING_REFUTED`; or
- `EVIDENCE_INSUFFICIENT`.

List every mathematical error, evidence weakness, and overclaim. State the strongest surviving
landing and whether any repair changes the science.

## Restrictions

Read only the sealed intake. Do not edit files, continue the research, import observations, or
access repository material outside the intake.
