# G75 external-review correction preregistration

Date: 2026-08-11

Base: `43de3554`

External landing: `VERIFIED_WITH_CAVEATS`.

## Frozen correction scope

Preserve the G75 derivation, 49-row shape atlas, 591-row profile atlas, and all preregistered
scientific conclusions unchanged. The reviewer independently reconstructed the complete frozen
quadratic family with zero row mismatches and confirmed Cartesian center smoothness and Lorentz
signature.

Apply only these evidence-strength repairs:

1. preserve the exact external review and transcript;
2. state explicitly that `verify_profile_family_independent.py` is a partial independent replay,
   while the fresh external implementation is the independent load-bearing reconstruction;
3. extend the local replay to check exact root identities, distinct-root counts, extrema, behavior
   labels, and stratum labels;
4. extend hostile catches so algebraic-field mutations fail even when aggregate counts are
   preserved;
5. update the G75 audit/status records and current startup navigation to
   `VERIFIED_WITH_CAVEATS` without promoting the bounded family to physical CMB physics.

## Frozen non-actions

- Do not alter any row of `SHAPE_ATLAS.tsv` or `PROFILE_ATLAS.tsv`.
- Do not rank or select a profile.
- Do not start a sky solve, fit, source model, scale selection, `X_max`, bootstrap, action, matter,
  ODE/PDE, geodesic, Jacobi, or GPU work.
- Do not read, stage, or modify the protected stopped native-on-shell draft.

## Certification contract

The correction is acceptable only if the strengthened replay and every hostile mutation pass, the
review manifest still hashes exactly, all 49/591 atlas rows remain byte-identical, repository gates
remain at baseline, and the protected draft metadata is unchanged.
