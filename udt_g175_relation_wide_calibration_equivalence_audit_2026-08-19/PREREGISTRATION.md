# G175 preregistration — relation-wide calibration equivalence

Date: 2026-08-19
Mode: metric-led exact type, covariance, and equivalence classification
Frozen source commit: `6df732bd`

## Question

Does the primary metric plus reciprocal `c_E` calibration at observer A uniquely extend the ruler
calibration along one supplied regular pair relation, or does only a fully supplied calibrated pair
map own that relation-wide tape?

## Preregistered primary landings

Exactly one will be selected:

1. `A_LOCAL_CALIBRATION_DOES_NOT_OWN_RELATION_WIDE_CARRY__ONE_SUPPLIED_CALIBRATED_PAIR_MAP_DOES__ENDPOINT_DEPTH_FIXES_ONLY_CONSTANT_UNIT_CLASS`:
   smooth positive recalibrations can agree with the entire A germ yet change B depth; one supplied
   relation-wide coordinate remains sufficient; equality of every endpoint difference holds iff
   two densities differ by one positive constant on each connected tape.
2. `PRIMARY_METRIC_AND_A_CALIBRATION_UNIQUELY_EXTEND_THE_RULER`: an existing metric identity uniquely
   fixes the calibration away from A without adding a path, connection, affine structure, or
   transport rule.
3. `RECIPROCAL_CE_STRUCTURE_UNIQUELY_EXTENDS_THE_RULER`: the founding reciprocal character and
   `c_E`, rather than a metric normalization, forbid every nonconstant recalibration that agrees at
   A.
4. `TYPE_OR_REGULARITY_FAILURE`: the proposed comparison does not preserve the same bounded input
   type or leaves the regular stratum.

## Exact derivation contract

1. Start from one connected regular G174 tape with auxiliary coordinate `sigma`, spatial tensor
   entry `H>0`, and positive density `m=|ds/dsigma|`.
2. Derive the exact effect of `n=fm`, `f>0`, on the calibrated metric, terminal scalar, and every
   endpoint-relative depth.
3. Construct a smooth `f` equal to one on an open neighborhood of A but nonunit at B. Preserve the
   same ambient metric, pair image, rank, orientation, and all A-local calibration data.
4. Prove or refute: two positive densities produce identical directed depths for every endpoint
   pair on a connected tape iff their ratio is constant.
5. Distinguish a supplied global ruler coordinate from a local A germ. Do not call the former
   derived merely because it is sufficient.
6. Classify the pointwise metric-unit choice `m=sqrt(H)` separately. Determine whether it is a
   derived normalization option and whether calling it the carried A-ruler requires an additional
   premise.
7. Audit `c_E`: identify exactly which time/ruler unit relation it fixes and whether any active
   equation determines a spatial derivative or continuation of `m`.
8. Preserve G170 same-class reversal/telescoping, G171 pair relativity, and G173/G174 tensor and
   calibrated-germ results.

## Values, charts, and omitted sectors

- connected static, time-orthogonal, spherical, `r>0` regular tape: `CHOSE_BOUNDED_CLASS`;
- `H`, positive `m`, and positive smooth `f`: `FREE_AND_CHARACTERIZED`;
- A anchor neighborhood: fixed identically under the counterfamily;
- omitted: time-live shift, nonspherical/micro ambient mixing, center/null/cut/focal/topology
  strata, path/connection/Jacobi/holonomy, global completion, `X_max`, observations, radiative
  transfer, action, source, matter, bootstrap, mass, and signalling.

## Certification and falsification contract

- exact symbolic derivation and equivalence proof;
- independent standard-library rational replay over at least 10,000 regular endpoint pairs;
- at least 1,000 anchored counterfamilies with `f=1` at A and `f_B!=1`;
- at least 14 semantic/mutation catches, including silently selecting pointwise unit normalization,
  confusing local and relation-wide calibration, and calling sufficiency derivation;
- all eight frozen source hashes verified at commit `6df732bd`;
- current premise verifier and full regression suite pass;
- fresh adversarial review before final `VERIFIED` grade.

Landing 1 is falsified by an active source-owned equation that uniquely determines `f=1` throughout
the connected tape from A-local data. Landings 2 or 3 are falsified by one regular smooth anchored
counterfamily satisfying every active gate.

## Maximum conclusion

At most G175 may classify calibration equivalence and relation-wide sufficiency on the bounded
static pair family. It cannot select the physical ruler, path, connection, pair population,
completion, or downstream physics.
