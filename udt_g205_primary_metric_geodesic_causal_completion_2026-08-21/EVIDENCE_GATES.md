# G205 evidence gates

Date: 2026-08-21

## Preregistered

Pass. Scope, candidate landings, all-geodesic case split, optical test, trapping test, and
falsification contract were committed and pushed at `932155c1` before execution.

## Bounded completeness

Pass for the exact declared G204 family on `R x R3`: all three geodesic signs, radial/nonradial,
nonzero/zero energy, center, infinity, finite-radius imprisonment, optical completeness, global
hyperbolicity, finite Killing horizons, and circular-null strata. Nonspherical/time-live histories,
maximal conformal extension, and physical selection are excluded.

## Independent verification

Pass with bounded scope. An independent Hamiltonian/exact-rational implementation covers 10,000
distinct cases and 150,000 assertions without production imports or artifact reads. It verifies
the algebraic first-integral, zero-energy, acceleration, and trapping-polynomial core only. The
global completeness and Cauchy theorems are analytic proofs retained by fresh external review, not
independently mechanized results. Finite order checks do not own the all-odd-`n` quantifier.

## Premise audit

Pass at package level. The metric family is a supplied witness. Geodesics and optical geometry are
standard evaluators. No action, source, transfer, observations, fit, or `X_max` entered.

## Mechanical gates

- self-contained package replay: pass;
- live repository source-provenance replay: pass, seven hashes;
- fresh adversarial review: initial `REPAIR_REQUIRED_WITH_LANDING_RETAINED`;
- external repair-only follow-up: `REPAIRS_VERIFIED__LANDING_RETAINED`;
- premise registry/startup update: pass, 189 rows;
- repository tests: pass, 120 passed and one known xfail;
- protected local work remains untouched.
