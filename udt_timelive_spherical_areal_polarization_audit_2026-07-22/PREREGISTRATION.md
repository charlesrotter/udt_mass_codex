# UDT time-live spherical areal-polarization audit — preregistration

Date: 2026-07-22

Base: `066d1ee05c3ad144d28b096b4a4728cca06941fa`

Branch: `codex/udt-timelive-spherical-areal-polarization-audit-2026-07-22`

Mode: metric-led exact CPU kinematic audit; no action, EOM, ODE/PDE solve, GPU, carrier, source,
boundary selection, or physical-scale insertion

## Owner direction

Proceed from the metric. Macro observational frames are reciprocal, with no observer preferred by
the laws. No micro frame rule is imposed. If the complete metric supplies an invariant causal-role
change, retain it; if it does not, do not invent one.

## Whole question

In the complete spherically symmetric time-live metric

```text
g = h_ab(x) dx^a dx^b + R(x)^2 dOmega^2,
```

where `h_ab` is an arbitrary Lorentzian two-metric on the time–radial orbit space and `R(x)` is the
areal-radius scalar, does the angular sector itself provide a covariant clock/radial polarization?
If so:

- how does it behave with arbitrary time dependence and shift;
- does its causal character ever exchange while the full metric remains Lorentzian;
- does it recover the founded static reciprocal metric;
- does it give an invariant time-live meaning to `phi`;
- what occurs at a regular center and at an areal-null surface; and
- does it determine the complete time-live base metric, or does an independent clock/lapse factor
  remain?

This is a kinematic map. No outcome—ordinary polarization, null transition, causal-role exchange,
unique `phi`, or underdetermination—is preferred.

## Complete bounded family

The primary family retains every spherically symmetric metric degree of freedom:

```text
h = -N(T,r)^2 dT^2 + L(T,r)^2 [dr + beta(T,r)dT]^2,
N>0, L>0,
R=R(T,r)>0 away from centers.
```

Here `T=c_E t` may be used as a dimension-matched time coordinate. `N`, `L`, `beta`, and `R` remain
arbitrary `C^2` functions. The shift is not set to zero. Spherical symmetry supplies a round
**spacetime orbit**, not the conditional round-`S^2` matter carrier.

The coordinate-free calculations use only `h`, its volume form, and `R`.

## Premise ledger

| Item | Status | Use | Limit |
|---|---|---|---|
| The metric is the theory | `BINDING METHOD` | metric invariants precede dynamics | curvature identity is not EOM |
| Spherical time-live warped product | `BOUNDED CONDITIONAL FAMILY` | smallest complete dynamic extension of the static metric | not a universal micro geometry |
| Lorentzian orbit-space metric `h` | `DECLARED FAMILY` | retains lapse, radial factor, and shift | signature-change metrics outside primary family |
| Areal radius `R` | `DERIVED FROM SPHERE AREA` within spherical geometry | invariant angular-size scalar | requires a physical representative; not pre-scale CSN invariant by itself |
| Local base orientation/time orientation | `POSIT / OWNER MACRO ORIENTATION` | defines the Hodge-dual line and future branch | sign of the line is conventional |
| Macro observer reciprocity | `OWNER FOUNDING CLARIFICATION` | passive descriptions may change; laws privilege no observer | no GR EOM, equivalence principle, or micro inheritance |
| Static identity `R=r`, `X=A=exp(-2phi)` | `DERIVED CONDITIONAL CONTROL` | recovery gate | not assumed in time-live family |
| `phi_areal=-1/2 log X` on `X>0` | `CANDIDATE IDENTIFICATION TO TEST` | possible invariant extension of static `phi` | not preregistered as derived or valid across `X<=0` |
| Action, source, carrier, boundary, mass, `X_max`, physical micro scale | `OPEN / ABSENT` | exclusion gate | no selection or repair role |

## Metric-native objects to test

Define

```text
X = h^ab (partial_a R)(partial_b R),
K^a = epsilon^ab partial_b R,
```

where `epsilon^ab` is the contravariant orbit-space volume form. The audit will derive, rather than
assume, the orthogonality and norm identities of `K` and `grad R`.

The word “polarization” means only the causal assignment of these two metric-derived lines. It is
not boundary polarization, particle polarization, or a preferred law-frame.

## Exact algebra plan

1. Invert the full lapse/radial/shift base metric and derive `X` with every term retained.
2. Derive `K.grad R=0` and `K^2=-X` in arbitrary coordinates.
3. Classify the `X>0`, `X=0`, and `X<0` branches without using a field equation.
4. Derive the product of the two sphere-null expansions and its relation to `X`.
5. Derive the angular and mixed warped-product curvature motifs:
   `(1-X)/R^2` and `-(nabla_a nabla_b R)/R`.
6. Determine the bounded-curvature center condition and compare it to the preceding static result.
7. Recover the static reciprocal metric with `R=r`, `X=A=exp(-2phi)`.
8. Test whether `phi_areal=-1/2 log X` is coordinate invariant on `X>0`, what happens at `X=0`,
   and whether it has a real continuation to `X<0` without extra branch data.
9. Put the `X>0` base locally into orthogonal areal form
   `h=-F(T,R)^2 X dT^2+X^-1 dR^2` and determine whether `F` is fixed.
10. Exhibit exact same-`X` metrics with different `F` and curvature if the complete base metric is
    underdetermined.
11. Audit common-scale behavior and separate pre-scale from physical-representative statements.
12. Reconcile, without rewriting, the static frame-regime and prior time-live characteristic/flux
    packages.

## Candidate outcomes retained

- `ANGULAR_SECTOR_DERIVES_AREAL_CLOCK_RADIAL_LINES`;
- `NO_INTRINSIC_POLARIZATION`;
- `AREAL_POLARIZATION_CHANGES_CAUSAL_ROLE_AT_X_ZERO`;
- `FULL_METRIC_SIGNATURE_FLIPS`;
- `STATIC_RECIPROCAL_PHI_HAS_A_UNIQUE_TIME_LIVE_EXTENSION`;
- `AREAL_PHI_IS_CONDITIONAL_AND_AN_EXTRA_CLOCK_FACTOR_SURVIVES`;
- `REGULAR_CENTER_RETURNS_TO_X_ONE`;
- `TIME_LIVE_FAMILY_REMAINS_UNDERDETERMINED`.

## Certification and falsification

A genuine areal-role exchange requires the scalar `X` to change sign and the metric-derived lines to
exchange timelike/spacelike causal character. This does **not** count as a flip of the full metric
signature unless the four-metric inertia also changes.

The claim that the angular sector selects directions fails if two metrics with identical `h`, `R`,
orientation, and derivatives yield different lines. The claim that it selects the complete base
metric fails if an arbitrary function survives in exact orthogonal areal form or if two same-`X`
metrics have different curvature.

The candidate `phi_areal` is not promoted unless it is a scalar, exactly recovers the static
identity, and its domain/branch limitation is explicit. Static recovery alone does not establish
unique time-live ontology.

Regular-center conclusions require bounded orthonormal warped-product curvature, not a coordinate
component or one scalar contraction alone.

## Maximum conclusion

The audit may derive the invariant spherical areal polarization, classify its causal branches,
identify a metric-native role exchange, derive center conditions, and determine whether the founded
static `phi` and complete reciprocal clock normalization extend uniquely.

It may not call an `X=0` surface an event horizon, black hole, particle boundary, CMB, or physical
micro transition without the missing global/dynamical evidence. It may not adopt an action, source,
carrier, boundary condition, mass, absolute scale, ODE/PDE, GPU run, canon, or navigation change.
