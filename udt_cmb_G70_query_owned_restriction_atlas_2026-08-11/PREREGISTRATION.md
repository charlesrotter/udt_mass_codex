# G70 complete-query-owned restriction and channel atlas — preregistration

Date: 2026-08-11

Base commit: `d43875adbfdc7a76e77afe3f10d3576635cf3ddc`

Mode: `MAP -> OBSERVE -> PONDER -> DERIVE`; metric-led saved-map algebra; CPU float64 plus exact
finite-dimensional identities; no ODE solve, eigenspectrum solve, fit, GPU work, source insertion,
or physical endpoint/profile selection

## Whole question

G69 established two facts in its frozen control universe: the complete three-channel geometry can
locally separate endpoint, lapse, and mixing controls, while an unrestricted positive-definite
source covariance can exactly compensate every invertible local `2 x 2` screen map. G70 asks:

> Which restrictions on source/state, endpoint/profile, or independently read channels are already
> owned by the complete typed UDT observation query and metric, and which merely make the inverse
> problem solvable after being supplied as additional assumptions?

The calculation must distinguish three logically separate statements:

1. an algebraic restriction can reduce the G69 degeneracy;
2. a declared observation channel can read the surviving geometric information;
3. UDT's current complete query or geometry actually owns that restriction or channel.

No algebraically successful control may be promoted to physics without passing item 3.

## Frozen bounded universe

Use only the `315` saved G69 screen maps and the same `15` preregistered sensitivity centers:

```text
shape in {PERSISTENT, TAPERED, SIGN_CHANGING}
x in {0.35, 0.50, 0.65, 0.80, 0.95}
parameters p=(endpoint x, lapse a, mixing epsilon)
```

Reconstruct no path and alter no G68/G69 artifact. Preserve the G69 midpoint, secant, parameter
spacing, column normalization, and numerical-rank thresholds:

```text
sigma_min/sigma_max >= 1e-6  -> FULL_RANK_OBSERVED
sigma_min/sigma_max <= 1e-8  -> RANK_DEFICIENT_OBSERVED
otherwise                    -> RANK_NUMERICALLY_UNRESOLVED
```

## Algebraic observation models

For a positive-definite local covariance `C`, define its symmetric matrix logarithm and the fixed
observer-screen coordinates

```text
A(C) = 1/2 log det(C),
S1(C) = 1/2[(log C)_00-(log C)_11],
S2(C) = (log C)_01.
```

`A` is the scalar area/amplitude channel and `(S1,S2)` is the smooth traceless shape/orientation
pair. These are analysis coordinates on the positive-definite cone, not new observables or source
physics.

Evaluate exactly these preregistered models:

1. `R00_UNRESTRICTED_SPD`: arbitrary positive-definite `C_src` for every map. Use the exact G69
   congruence theorem; geometry is profiled out of all covariance coordinates.
2. `R01_ISOTROPIC_UNKNOWN_AMPLITUDE`: `C_src=alpha I`, `alpha>0` free. Test only `(S1,S2)` from
   `C_obs=D D^T`; area is source-degenerate.
3. `R02_FIXED_SHAPE_UNKNOWN_AMPLITUDE`: `C_src=alpha C0`, with `alpha>0` free and each of the three
   frozen G69 positive-definite covariance shapes used separately as algebra controls. Test only
   `(S1,S2)`.
4. `R03_KNOWN_SOURCE_COVARIANCE`: use each frozen `C0` including its amplitude and test
   `(A,S1,S2)`.
5. `R04_UNKNOWN_AMPLITUDE_PLUS_CARRY`: append the saved endpoint azimuthal carry `psi` to the
   `R01` and `R02` shape pairs.
6. `R05_KNOWN_SOURCE_PLUS_CARRY`: append `psi` to `R03`; report rank without using a desired
   three-row subset.
7. `R06_TWO_FIXED_SHAPE_CHANNELS`: concatenate `(S1,S2)` for every unordered pair of distinct
   frozen source shapes, allowing an independent unknown amplitude in each channel.
8. `R07_UNRESTRICTED_SPD_PLUS_CARRY`: profile out covariance exactly as in R00 and retain only
   `psi`; its rank is at most one.

The source shapes, their amplitudes, and the availability of `psi` or multiple channels remain
`CHOSE_CONTROL` until separately owned. No result-dependent source shape may be introduced.

## Ownership census

Individually classify the following as `DERIVED`, `CHOSE_CONTROL`, `CONDITIONAL`, `POSIT`,
`OBSERVED`, or `OPEN`, with exact source citation:

- ordered observer-sky query and screen frame;
- screen Jacobi map `D`;
- endpoint surface as query input versus physical last-scattering selection;
- metric profile family versus physical profile selection;
- local source covariance and any isotropy, fixed-shape, shared-amplitude, or cross-channel rule;
- scalar TT access to area and shape;
- orientation-sensitive/azimuthal carry access;
- polarization or another independent source channel;
- conditional low-redshift SNe compatibility anchor;
- `X_max`, bootstrap, action, source law, and local signalling.

Symmetry of a metric control does not automatically impose the same symmetry on an unowned source
state. A query-supplied endpoint does not thereby become a physically selected endpoint.

## Certification and falsification

The package fails closed if:

1. any G69 cell or sensitivity center is omitted or duplicated;
2. any G68/G69 path is reintegrated or rewritten;
3. the matrix-log coordinates fail reconstruction or positive-definite domain checks;
4. rank is evaluated without the frozen column normalization and thresholds;
5. a two-output model is called rank three;
6. `psi` is silently treated as scalar-TT-owned;
7. a source symmetry or covariance is inferred from metric symmetry alone;
8. a query-input endpoint/profile is called physically selected;
9. the exact unrestricted-source congruence freedom is weakened without an explicit source owner;
10. an algebraically helpful control is promoted to a native UDT law;
11. an observational coefficient is fitted or chosen after inspection;
12. the protected native-on-shell draft is read, modified, or staged.

An independent implementation must reconstruct the matrix-log readouts and all finite-difference
ranks without importing the production builder. Exact dimensional rank ceilings and the G69
congruence theorem must be checked analytically.

## Allowed primary landings

Exactly one:

1. `QUERY_OWNS_IDENTIFIABILITY_RESTRICTION`;
2. `QUERY_OWNS_CHANNEL_BUT_NOT_SOURCE_RESTRICTION`;
3. `ALGEBRAIC_RESTRICTIONS_WORK__OWNERSHIP_REMAINS_OPEN`;
4. `NO_TESTED_RESTRICTION_RESTORES_LOCAL_RANK`;
5. `IDENTIFIABILITY_NUMERICALLY_UNRESOLVED`;
6. `TYPE_OR_EVIDENCE_FAILURE`.

Maximum conclusion: a bounded map of which declared restrictions recover which local parameter
directions, plus an evidence-led statement of whether current UDT owns any such restriction. G70
cannot select a physical source, endpoint, profile, last-scattering surface, spectrum, coefficient,
action, bootstrap law, `X_max` value, or signalling rule.
