# Twisted reciprocal S3 full Killing-algebra audit — preregistration

Date: 2026-07-27

Base: `c239adceadad0464da6bf43ab7980a8aa3c2108d`

Question type: **METRIC-LED COMPLETE SYMMETRY-STRATUM CENSUS**.

## Whole question

For the already registered complete stationary twisted coframe on `R x S3`, does the metric itself
select exactly one timelike Killing line in any complete regular configuration, and can such a
configuration also carry the previously derived nonconstant clock depth and nonzero twist ruler?

The full Killing vector is allowed to have arbitrary time-dependent and spatially dependent
components. Finding the displayed coordinate field `partial_t`, or checking only the inherited
`SU(2)`/`U(1)` action, is not a uniqueness proof.

## Exact bounded family

The audited family is

```text
d sigma_3 = kappa sigma_1 wedge sigma_2,
tau = c_E dt + a sigma_3,
theta_0 = exp(-phi) tau,
theta_1 = R exp(phi) sigma_3,
theta_2 = R exp(lambda phi) sigma_1,
theta_3 = R exp(lambda phi) sigma_2,
g = -theta_0^2 + theta_1^2 + theta_2^2 + theta_3^2,
```

with `phi` any registered smooth scalar on `S3`, `c_E,R>0`, and real `a,lambda`; `kappa` is the
nonzero Maurer-Cartan normalization. The strict spacelike-slice condition is retained:

```text
R^2 exp(2 phi) - a^2 exp(-2 phi) > 0.
```

This is a configuration-space audit, not an equation-of-motion or branch-selection calculation.

## Premise stamps

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

## Frozen strata

Every row of `KILLING_STRATUM_UNIVERSE.tsv` must receive an outcome. In particular the audit retains:

- generic nonconstant `phi`;
- constant `phi`;
- nonconstant `phi` with a continuous stabilizer;
- twist-free and nonzero-twist configurations;
- generic and enhanced-symmetry `lambda`/shape cases;
- causal-slice degeneration and boundary cases;
- local curvature-invariant rank certificates and their global-extension requirement.

The audit may refine a row, but may not delete a stratum after outcomes are seen.

## Required derivation

1. Write the general Killing field without assuming stationarity, split preservation, or membership
   in a known group action.
2. Derive exact consequences of the Killing equation and/or an intrinsic curvature-invariant rank
   certificate that applies to the full Killing algebra.
3. Prove every claimed uniqueness result on an open set and justify its extension to the complete
   connected metric; an isolated-point or coordinate-asymmetry observation is insufficient.
4. Exhibit exact nonunique controls for constant or continuously symmetric profiles.
5. Check global smoothness/descent, Lorentz signature, and the strict spatial-slice inequality for
   every complete witness.
6. Separate `dim Kill(g)=1` from merely finding one timelike Killing field. On compact `S3`, any
   independent spatial Killing field produces additional timelike linear combinations with
   `partial_t` for sufficiently small coefficient.
7. Recheck nonconstant Killing norm and nonzero twist in the same configuration. Cross-branch
   splicing is forbidden.
8. Classify `a=0`, constant-profile, continuous-stabilizer, and enhanced angular-symmetry limits.

## Category-A computational choices

Charts, rational sample coefficients, local expansion points, finite Taylor order, and exact
symbolic elimination order may be chosen for a witness or catch proof. They are computational
controls only. No chosen coefficient, `phi`, `lambda`, chart, or topology is promoted to physical
selection.

## Certification contract

`FULL_KILLING_LINE_UNIQUE_EXACT` requires either a complete solution of the unrestricted Killing
equations or an intrinsic certificate that annihilates every Killing field transverse to the
stationary line on a nonempty open set, followed by a valid connected/global extension argument.

`SAME_BRANCH_RECIPROCAL_PAIR_WITNESS` additionally requires one complete smooth profile with strict
slice inequality, nonconstant stationary norm, and nonzero twist. Existence does not establish that
UDT selects that configuration or profile.

If only conditional criteria or local jets are established, the result remains `OPEN` or
`VERIFIED-WITH-CAVEATS`; it may not be upgraded by genericity language alone.

## Premise audit and excluded scope

`phi`, `a`, and `lambda` are free-and-explored configuration data. `c_E` is the observational scale
anchor already present in the metric; `R` and the global profile are not selected here. No action,
variation, EOM, source, carrier, boundary functional, density, bootstrap closure, mass, `X_max`,
dynamics, signalling law, or observational fit is authorized.

## Maximum conclusion

At most:

```text
FULL_KILLING_ALGEBRA_OF_REGISTERED_TWISTED_CONFIGURATION_STRATA_CLASSIFIED;
EXISTENCE_OR_NONEXISTENCE_OF_A_COMPLETE_SAME_BRANCH_UNIQUE_K_DEPTH_TWIST_WITNESS_ESTABLISHED
ONLY_TO_THE_EXACT_CERTIFIED_SCOPE;
NO_PHYSICAL_PROFILE_OR_DYNAMICAL_BRANCH_SELECTED.
```

Stop before action work, physical selection, density/bootstrap work, GPU work, canonization, or
startup-control edits.
