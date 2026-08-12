# G84 fresh cold adversarial review

Date: `2026-08-12`

Reviewer: fresh read-only Codex context `/root/g84_cold_adversary`

Landing: `VERIFIED-WITH-CAVEATS`

## Reproduced load-bearing claims

The reviewer independently reproduced:

- the `x=2 sin(chi)` refactor and round minimal doubled spatial candidate of radius `2R`;
- sectional curvature `1/(4R^2)`, scalar curvature `3/(2R^2)`, injectivity radius `2piR`, and
  diameter `2piR`;
- the zero-mixing constant-curvature Lorentzian embedding and transitive central-geodesic observer
  isometry orbit;
- the recentered stationary laws
  `phi(s)=-log cos[s/(2R)]` and `c_eff/c_E=cos[s/(2R)]^2` on `0<=s<piR`;
- the conditional common center-to-static-horizon distance `piR` on that observer class;
- all `197` exact AM rows, with one `q(4)=0` row and `196` nonzero rows, zero atlas
  mismatches, `104` positive and `92` negative nonzero values, and minimum nonzero
  `|q(4)|=1/20`;
- the axial fixed-set degeneracy of the analytic mixed continuation and the stronger
  symmetry-preserving bifurcation obstruction when `h_H=4q(4)` is nonzero.

The exact profile census was recomputed with standard-library rational arithmetic rather than the
production SymPy path.

## Corrections required and incorporated

1. The round `S^3` is the preregistered **minimal doubled, simply connected candidate**. The local
   metric does not establish uniqueness among possible global topologies or identifications.
2. The former antipodal zero-depth example compared equal lapse magnitudes across opposite static
   patches, where the displayed static Killing field reverses global time orientation. It was
   therefore not one valid future-directed stationary pair query. The banked counterexample now
   stays wholly within the north static patch: at `chi=pi/4`, equal-latitude pairs have zero lapse
   depth while their spatial distance ranges continuously from `0` to `piR`.
3. The packaged mutation tests are regression locks, not independent proofs of the mathematics.
   The embedding reconstruction, exact rational census, and invariant fixed-set calculation carry
   the adversarial evidential load.

## Scope that did not close

No physical `X_max`, topology, profile, or scale is selected. The result does not cover arbitrary
accelerated observers, the `196` mixed profiles beyond the declared stationary-axisymmetric
bifurcate extension class, time-live completions, symmetry-breaking completions, a physical
pair-separation owner, a CMB observable, source, action, matter, or bootstrap closure.

The surviving maximum conclusion is:

`BOUNDED_AM_SPATIAL_COMPLETION_AND_STATIONARY_DEPTH_COMPATIBILITY_ATLAS`.
