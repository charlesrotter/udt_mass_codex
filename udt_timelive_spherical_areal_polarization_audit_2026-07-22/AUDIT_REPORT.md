# UDT time-live spherical areal-polarization audit

Date: 2026-07-22

Base: `066d1ee05c3ad144d28b096b4a4728cca06941fa`

Preregistration commit: `90217f71e27769686ab13b9cc460772c88ec5cb1`

Mode: exact CPU metric algebra; no action, EOM, ODE/PDE, GPU, carrier, source, boundary selection,
physical scale, or navigation change

Grade: `VERIFIED-WITH-CAVEATS`; an independent standard-library rational tensor implementation
passes, while no fresh external-model semantic review was authorized

## Result first

For the complete spherically symmetric time-live warped product

```text
g = h_ab dx^a dx^b + R(x)^2 dOmega^2,
h = -N(T,r)^2 dT^2 + L(T,r)^2 [dr + beta(T,r)dT]^2,
```

the angular sector defines the coordinate scalar and oriented areal dual

```text
X   = h^ab (partial_a R)(partial_b R),
K^a = epsilon^ab partial_b R.
```

Exact algebra with lapse, radial factor, time dependence, and shift retained gives

```text
X = R_r^2/L^2 - (R_T-beta R_r)^2/N^2,
K.grad R = 0,
K^2 = -X.
```

Thus a supplied spherical physical geometry contains a solution-specific clock/radial
polarization wherever `dR` is non-null. The sign of `X` gives an exact causal-role atlas:

| condition | `grad R` | `K` | full regular metric |
|---|---|---|---|
| `X>0` | spacelike | timelike | Lorentzian |
| `X=0` | null | null and collinear | Lorentzian |
| `X<0` | timelike | spacelike | Lorentzian |

The `X<0` branch is therefore a genuine exchange of the two **areal** causal roles. It is not a
full signature flip, preferred law-observer, or derived microscopic regime. The metric family has
inertia `(-,+,+,+)` at every regular point because `det(h)=-N^2L^2<0` and the angular orbit is
positive.

## Null and curvature identities

For base null vectors normalized by `ell.n=-1`, the sphere expansions obey

```text
theta_ell theta_n = -2X/R^2.
```

This is kinematic. It does not select trapping dynamics or attach global horizon meaning to an
`X=0` surface.

Direct coordinate Riemann reconstruction gives the warped-product motifs

```text
angular sectional curvature = (1-X)/R^2,
mixed base-angular curvature = -(nabla_a nabla_b R)/R.
```

Consequently, bounded orthonormal warped curvature at a regular areal center, together with bounded
base curvature, requires

```text
X = 1 + O(R^2),
nabla_a nabla_b R = O(R).
```

This covariantly extends the preceding static result. It does not determine global topology or say
that a matter core must be a spherical center.

## Static recovery and the domain of `phi`

For the founded static reciprocal control

```text
R=r,
h=diag(-A,A^-1),
A=exp(-2phi)>0,
```

the time-live scalar becomes exactly

```text
X=A=exp(-2phi).
```

Therefore

```text
phi_areal = -(1/2)log X
```

is a coordinate scalar on `X>0` and exactly matches the founded static `phi`. That establishes a
strong candidate extension, not unique ownership: it diverges at `X=0`, and on `X<0` a real
logarithm needs `log|X|` plus separate sign-branch data. The original positive reciprocal character
alone does not prescribe that continuation.

## Exact underdetermination of the complete time-live metric

Where `X>0`, an orthogonal areal chart puts the general orbit metric locally into

```text
h = -F(T,R)^2 X dT^2 + X^-1 dR^2,
F>0.
```

The areal scalar fixes the displayed reciprocal amplitudes but does not fix `F`. This surviving
factor cannot be discarded as pure notation. At `X=1`, compare

```text
F=1,
F=exp(qR).
```

The first four-metric is flat, while the second has scalar curvature

```text
scalar curvature = -2q^2 - 4q/R.
```

The independent exact rational control `R=2`, `F=9`, `F'=3`, `F''=1` gives `scalar curvature=-8/9`,
while the same-`X` flat control gives zero. Hence `X`, the local areal lines, and the conditional
`phi_areal` do not determine the complete geometry. `F` represents remaining clock-normalization
and threading geometry; whether registered UDT structure selects it remains open.

## Common-scale scope

Under a local common rescaling of a selected representative,

```text
h -> Omega^2 h,
R -> Omega R,
```

the areal scalar gains derivative-of-`Omega` terms:

```text
X' = X + 2R <dR,d log Omega>_h + R^2 <d log Omega,d log Omega>_h.
```

Constant common scaling preserves `X`; general local scaling does not. The areal polarization is
therefore a property of a selected physical spherical representative, not an invariant of the
entire pre-scale local-CSN class. This does not refute Common-Scale Neutrality; it distinguishes its
pre-material calibration role from post-selection areal geometry.

## Relation to prior work

- The static frame/center result is retained and covariantly extended: static `X=A`, a regular center
  has `X->1`, and the recorded WR-L wall is an `X=0` boundary of the static polarization chart.
- The no-universal-subbundle result is retained: these lines are supplied by a particular spherical
  solution, not fixed in all metrics by law.
- The prior characteristic/flux package remains distinct: it classified conditional action
  principal symbols and boundary flux, while this audit uses no action or EOM.
- The conditional carrier `S^2` is not involved. The round spheres here are spacetime symmetry
  orbits and do not derive a matter carrier or section.

## Verification

Eleven exact post-firewall sources are frozen in `SOURCE_LINEAGE.tsv`. The production SymPy route
passes 23/23 exact checks. A separate implementation using only `Fraction` arithmetic rebuilds the
shift-complete inverse, causal branches, null expansion identity, generic warped metric two-jets,
angular and mixed Riemann blocks, center Laurent controls, same-`X` lapse counterfamily, and local
common-scale control. It passes 22/22 exact checks and 18/18 exercised corruption catches.

## Four evidence gates

1. **Preregistered:** yes; commit `90217f7` precedes production algebra and adjudication.
2. **Full or bounded:** complete for arbitrary `C^2` spherical kinematics with Lorentzian two-base,
   positive round symmetry orbits, and all lapse/radial/shift/areal functions retained. It excludes
   nonspherical geometry, degenerate/signature-changing metrics, dynamics, and physical scale.
3. **Independently verified:** yes for the load-bearing inverse, branch, curvature, center,
   underdetermination, source, and ledger claims. No fresh external-model semantic review was
   authorized.
4. **Premises audited:** representative, symmetry, orientation, chart, CSN, static recovery, `phi`
   domain, global meaning, matter, dynamics, scale, and micro limitations are explicit.

## Stop line

No event horizon, particle boundary, CMB surface, micro transition, action, source, carrier,
boundary functional, mass, `X_max`, physical scale, ODE/PDE, GPU run, canon, or navigation change is
selected.

Maximum conclusion:

```text
SPHERICAL_ANGULAR_GEOMETRY_DERIVES_SOLUTION_SPECIFIC_TIME_LIVE_AREAL_CLOCK_RADIAL_LINES;
THESE_LINES_EXCHANGE_CAUSAL_ROLES_AT_X_ZERO_WHILE_THE_FULL_METRIC_REMAINS_LORENTZIAN;
STATIC_PHI_HAS_A_CONDITIONAL_X_POSITIVE_AREAL_EXTENSION;
THE_COMPLETE_TIME_LIVE_METRIC_REMAINS_OPEN_BECAUSE_CLOCK_THREADING_F_IS_NOT_SELECTED.
```
