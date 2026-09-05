# G351 exact derivation — conserved label measure

Date: 2026-09-05
Status: `DERIVED_CONDITIONAL_ON_OWNER_ADOPTED_PROVISIONAL_PREMISE`

## 1. Supplied geometric data

Let `Lambda` be the measurable label space of one supplied future-null family. For each supplied
cut `i`, G348--G349 provide a labelled map

```text
X_i: Lambda -> Sigma_i
```

and, on the screen-rank-two stratum, a positive metric sheet-area Jacobian `J_i`. A supplied
future-timelike endpoint observer measures positive metric frequency `omega_i`. Hence

```text
A_ji=J_j/J_i,
R_ji=omega_j/omega_i.
```

This geometry is unchanged by G351.

## 2. New premise and its exact type

`OWNER_ADOPTED_PROVISIONAL_PREMISE`:

> On a source-free segment of a populated labelled null family, physical carried content is a
> finite nonnegative additive measure `mu` on label space, and the same `mu` is used at every cut.

The premise supplies neither `mu` nor which labels are populated. It is a constitutive conservation
statement for any supplied populated measure. It is not derived from metric geometry, Universal
Reciprocity/DDR, the G312 response constitution, or G350.

The measure at cut `i` is its mathematical pushforward

```text
mu_i=(X_i)_* mu.
```

This equation is meaningful even when `X_i` loses rank or is many-to-one.

## 3. Absolutely continuous regular-cut density

An arbitrary finite `mu` need not have an ordinary density. On a regular local label chart, take
its Lebesgue decomposition relative to label-coordinate measure:

```text
dmu=dmu_ac+dmu_s,
dmu_ac=s(lambda) dlambda,
dArea_i=J_i(lambda) dlambda,
```

with `J_i>0`. All regular sheet-area measures are mutually absolutely continuous with label
measure, so `mu_s` remains singular there. The Radon--Nikodym density of only the absolutely
continuous part relative to metric sheet area is

```text
n_i=dmu_ac/dArea_i=s/J_i.
```

For the same retained label at two regular cuts, the division-free Radon--Nikodym chain rule is

```text
n_j=A_ji^-1 n_i                                           (1)
```

almost everywhere. On nonzero-density support this is equivalently
`n_j/n_i=J_i/J_j=A_ji^-1`. Zero density obeys (1) but cannot identify an exponent by itself. Thus,
for any nonzero absolutely continuous regular density component, the owner-adopted conservation
premise fixes the area weight to `-1`. The singular measure component has no ordinary density and
no ordinary density exponent `q`. This is division of one supplied conserved measure component by
derived metric sheet area; it is not a new metric equation.

A decisive counterexample to the overbroad density statement is `mu=delta_(1/2,1/2)` on the
two-dimensional label chart `[0,1]^2` with regular constant area Jacobians `J_i=1` and `J_j=2`.
The singleton has zero metric area at both cuts but positive `mu`; no finite ordinary density can
represent the full measure.

## 4. Arbitrary observer weight remains

Let `w` be the declared endpoint frequency weight of a measured component `C`, and fix one common
positive reference frequency `omega_*`. By definition of that transformation type,

```text
C_i=(omega_i/omega_*)^w n_i
```

so arbitrary real powers act only on a dimensionless ratio. Equation (1) gives, on nonzero support,

```text
C_j/C_i=(omega_j/omega_i)^w (n_j/n_i)
       =R_ji^w A_ji^-1.                                  (2)
```

Equivalently,

```text
C_i J_i / (omega_i/omega_*)^w=s(lambda)                  (3)
```

is cut-independent. The premise and geometry do not choose `w`. Relabelling `w` as the G350
frequency exponent `p`, the conditional family is

```text
T_ji^(p)=R_ji^p A_ji^-1,        p in R.                  (4)
```

## 5. Uniqueness of the area exponent inside G350

Take an arbitrary G350 character with frequency exponent `a` and area exponent `q`:

```text
T_ji=R_ji^a A_ji^q.
```

If it is to represent a nonzero absolutely continuous component of declared observer weight `w`
whose label measure obeys (3), then

```text
(C_j J_j / (omega_j/omega_*)^w)/(C_i J_i / (omega_i/omega_*)^w)
  =T_ji A_ji R_ji^-w
  =R_ji^(a-w) A_ji^(q+1)
  =1                                                       (5)
```

for every independent positive `(R,A)` in G350's declared full abstract domain. Setting `A=1`
forces `a=w`; setting `R=1` forces `q=-1`. Therefore

```text
a=w,    q=-1.                                             (6)
```

Only `q` is numerically fixed because `w`, hence `a=p`, remains an arbitrary declared observer
type. A zero component provides no exponent witness, and a singular component has no ordinary
density exponent. This proof does not assert that one universe realizes every abstract ratio; it
inherits G350's explicitly chosen classification domain.

## 6. Identity, sewing, reversal, and observer covariance

For three regular cuts,

```text
R_ki=R_kj R_ji,
A_ki=A_kj A_ji.
```

Therefore

```text
T_ki^(p)=T_kj^(p) T_ji^(p).
```

At identity `R=A=1`, `T=1`. Reversal sends `(R,A)` to `(R^-1,A^-1)` and therefore sends `T` to
`T^-1`.

Under independent finite endpoint observer-frequency recalibrations

```text
omega_i -> D_i omega_i,
```

the component is typed by

```text
C_i -> D_i^p C_i.
```

The same fixed `omega_*` is used at both endpoints. Then (3) remains unchanged. Covariance checks a
supplied `p`; it cannot choose one.

## 7. Caustics and many-to-one endpoints

At a caustic `J_i` can vanish while the labelled null family and its phase-space evolution remain
regular. The pointwise density `n_i=s/J_i` may diverge, and the Radon--Nikodym derivative relative
to two-dimensional image area may cease to exist as an ordinary finite function. G351 does not
remove that singularity or extend `A^-1` as a finite pointwise scalar.

The conservation premise nevertheless remains well-defined because the full `mu` lives on
`Lambda`, not on the image-area chart. Its pushforward `(X_i)_*mu` is a finite measure and may
acquire singular parts. A singular part can already be present before a caustic; G351 assigns no
ordinary density exponent to it.
If several labels reach one endpoint, pushforward retains their multiplicity. G349's geometric
image-union area discards that multiplicity and therefore cannot replace the carried measure.

Measure additivity states only

```text
mu(E union F)=mu(E)+mu(F)   for disjoint label sets E,F.
```

It supplies no phase, cancellation, interference, detector resolution, or physical rule for
combining distinct path families.

## 8. Sources and zero content

If `mu=0` on a label set, every pushforward and every regular density is zero there. Conservation
cannot populate a ray, create an emission profile, or determine a nonzero normalization. Nonzero
initial/source measure is supplied data. A source/sink balance law would be a separate premise.

## 9. Exact landing

```text
OWNER_PROVISIONAL_SOURCE_FREE_LABEL_MEASURE_CONSERVATION
__NONZERO_ABSOLUTELY_CONTINUOUS_REGULAR_DENSITY_AREA_WEIGHT_Q_EQUALS_MINUS_ONE
__OBSERVER_WEIGHT_P_REMAINS_ARBITRARY
__T_P_EQUALS_R_TO_P_A_INVERSE_WITH_IDENTITY_SEWING_REVERSAL_AND_COVARIANCE
__FULL_FINITE_MEASURE_REMAINS_DEFINED_THROUGH_CAUSTIC_RANK_LOSS_WHILE_POINTWISE_DENSITY_NEED_NOT
__SINGULAR_MEASURE_PART_HAS_NO_ORDINARY_DENSITY_EXPONENT
__SOURCE_POPULATION_CROSS_LABEL_PHYSICS_LIGHT_DISTANCE_HISTORY_SCALE_XMAX_AND_CANON_REMAIN_OPEN
```

This is a premise-conditioned theorem about the full conserved measure and its nonzero absolutely
continuous regular-density component, not a native light, energy, flux, luminosity, or
observational-distance law. The metric, reciprocal kernel, angular sector, and owner-adopted
bounded response equation are unchanged.
