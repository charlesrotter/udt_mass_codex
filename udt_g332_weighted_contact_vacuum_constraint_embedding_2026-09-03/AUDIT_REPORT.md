# G332 audit report — weighted-contact vacuum-constraint embedding

Date: 2026-09-03
Status: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Bounded landing

```text
EXACT_IRREGULAR_WEIGHTED_CONTACT_VACUUM_CONSTRAINT_DATA_EXIST
__INITIAL_CONSTRAINTS_DO_NOT_FORCE_HOPF_ORBIT_RIGIDITY
__EXISTENCE_IS_NOT_A_FULL_K_CENSUS_OR_DYNAMIC_STABILITY
```

## Result

Every smooth compact three-metric with a global unit Killing field admits the following exact
active-constraint construction for any fixed finite connected `Lambda`. With `R` its scalar
curvature, choose a constant `C` large enough that

```text
R+2C^2-2Lambda > 0
```

globally, and set

```text
b = -C +/- sqrt[2(R+2C^2-2Lambda)],
K = ((C-b)/2) gamma + b xi_flat tensor xi_flat.
```

Unit-Killing identities solve the complete momentum constraint; the displayed square root solves
the Hamiltonian constraint. Applying the theorem to G331 gives exact smooth vacuum-constraint data
for the full positive-weight family, including irrational unequal weights with generic nonclosed
dense Ricci-eigenline orbits.

The active constraints therefore impose no Hopf-circle orbit rigidity on these initial data. The
construction is an existence witness within the unrestricted symmetric extrinsic-curvature space,
not a full classification of that space.

## Evidence

- preregistration committed and pushed at `352837d9` before outcome execution;
- one covariant proof over the complete compact unit-Killing class;
- 642 exact standard-library production checks across 80 direct coordinate cases;
- 65 implementation-distinct exact checks across 64 different coordinate cases, with no production
  import or production-result read;
- nine hostile mutations caught;
- equal, rational-unequal, and irrational-unequal orbit classes retained analytically;
- both square-root signs, both signs of `C`, arbitrary fixed finite `Lambda`, and the zero-radicand
  boundary retained;
- fresh hostile external review independently retained the theorem and requested only sealed-path
  and tensor-typing repairs;
- repair-only external follow-up accepted both preregistered repairs after a dependency-free
  four-command replay with 91 aggregate gates;
- no carrier, action, source, matter, mass, observation, fit, absolute scale, physical `X_max`, or
  protected local work.

## Four banking gates

1. **Preregistered:** yes, `352837d9`.
2. **Full bounded space:** yes for existence on the complete G331 positive-weight family; no for a
   census of every `K`, general nearby metrics, or evolution.
3. **Independent:** yes internally by an implementation-distinct direct reconstruction and
   externally by hostile analytic rederivation, unsampled spot checks, and sealed replay.
4. **Premises:** audited in `PREMISE_LEDGER.tsv`; the response equation remains owner-provisional
   and the constraints remain conditional on it.

Maximum current grade:

```text
DERIVED_CONDITIONAL__EXTERNALLY_ACCEPTED_BOUNDED
```

## Open boundary

The immediate next question is dynamic: conditional local development exists per the already
imported Cauchy theorem, but it remains unknown whether the Ricci eigengap
and irregular orbit type persist, bifurcate, or disappear. That is not yet stability and must not be
collapsed into another restricted symmetry tile. Occupancy, topology selection, matter/mass,
absolute scale, physical `X_max`, and canon remain open.
