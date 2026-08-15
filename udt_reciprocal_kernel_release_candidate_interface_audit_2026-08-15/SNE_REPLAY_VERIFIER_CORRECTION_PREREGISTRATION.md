# Preregistration — exact-anchor verifier correction

Date: 2026-08-15
Parent: `SNE_REPLAY_PREREGISTRATION.md`

The first independent run correctly used the direct-Christoffel neighboring-ray method, but compared
its five exact fixed-redshift anchors with linear interpolation through the production values at the
observed Pantheon+ redshifts. At `z=2`, sparse observational sampling made the interpolation error
`6.50e-4`, exceeding the frozen `3e-4` method-agreement tolerance. This is a verifier implementation
error: the preregistered contract requires the two methods at the same fixed anchors.

Before rerun, replace only the production side of that comparison with exact evaluation of the saved
production Jacobi solution at `z=0.03,0.10,0.50,1.00,2.00`. Retain:

- the same complete geometry and query;
- the same direct-Christoffel neighboring-ray implementation;
- the same two finite-difference deltas;
- the same `3e-4` tolerance;
- the same SNe curve, offset, chi-square, and likelihood verifier;
- every original authority ceiling.

No outcome-dependent tolerance, geometry, endpoint, data selection, transfer premise, or physical
interpretation may change. If the exact same-anchor comparison still fails, the independent geometry
gate fails.
