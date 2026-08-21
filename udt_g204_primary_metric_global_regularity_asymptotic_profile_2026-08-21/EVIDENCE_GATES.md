# G204 evidence gates

Date: 2026-08-21

## Preregistered

Pass with explicit repair. Original scope was committed at `ea91f45e`. The first witness failed the
strong smooth-center gate; the failure and sole even-areal repair were committed at `785b0447`
before repair evaluation.

## Bounded completeness

Pass for the declared static-spherical positive-areal branch, center limits, registered controls,
outer curvature asymptotics, radial spatial length, and radial-null affine reach. No completion or
downstream physics is classified.

## Independent verification

Pass. Independent exact-rational profile jets and orthonormal sectional-curvature reconstruction
cover 10,000 distinct cases and 160,010 assertions without production imports or artifact reads.

## Premise audit

Pass at package level. Global regularity is a conditional geometric gate, not an equation of
motion. The repair family is a witness, not a physical profile. The outer limit is not `X_max`.

## Mechanical gates

- package replay: pass (`all_pass=true`; byte-stable no-write replay);
- 188-row premise registry update and full premise verifier: pass;
- repository tests: 119 passed, 1 expected xfail;
- diff check: pass;
- protected local work remains untouched.
