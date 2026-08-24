# G250 exact derivation — absolute-scale anchor type and ownership

Date: 2026-08-24

## 1. The remaining object is one scale orbit

G249 considers one already supplied dimensionless metric history and one matched regular branch,
with

\[
g_\ell=\ell^2\bar g,\qquad \ell>0.
\]

The normalized reciprocal and angular response are fixed by \(\bar g\) and the branch. The only
question here is how an independent observation may identify one member of this one-dimensional
homothety orbit.

Let a scalar metric quantity on the same identified query object have constant homothety weight
\(w\):

\[
Q_\ell=\ell^w\bar Q.
\]

The phrase “same identified query object” is load-bearing. It may mean the same observer-clock
interval, event, screen, orbit, labelled null branch point, spatial region, or spacetime region,
depending on the type of \(Q\).

## 2. One-anchor theorem

If \(w=0\), then \(Q_\ell=\bar Q\) for every \(\ell\), so \(Q\) cannot distinguish members of the
scale orbit.

If \(w\ne0\), \(\bar Q\ne0\), and an independently calibrated observation \(Q_*\) is attached to
the same object with \(Q_*/\bar Q>0\), then

\[
\boxed{\ell=\left(\frac{Q_*}{\bar Q}\right)^{1/w}}
\]

is the unique positive scale. For negative \(w\), this means the corresponding positive inverse
root. The sign condition is automatic for an exact positive homothety of one nonzero real scalar,
but it is an independent falsification condition for measured data.

This proves conditional calibration of \(\ell\). It does not select \(\bar g\), the observer
population, the branch, or the query object to which the observation is attached.

## 3. A second anchor is a test, not another scale

For two matched quantities,

\[
Q_{1*}=\ell^{w_1}\bar Q_1,\qquad
Q_{2*}=\ell^{w_2}\bar Q_2,
\]

one scale exists only if

\[
\boxed{
\left(\frac{Q_{1*}}{\bar Q_1}\right)^{w_2}
=
\left(\frac{Q_{2*}}{\bar Q_2}\right)^{w_1}.
}
\]

Thus the first lawful nonzero-weight anchor calibrates \(\ell\). Every additional independent
anchor checks the dimensionless history, branch matching, and measurement bridge. It is not a
license to add one fitted scale per channel.

## 4. Direct metric anchor classes

Under constant positive homothety, the preregistered direct classes have the following weights:

| Matched quantity | Weight |
| --- | ---: |
| proper-time interval | \(+1\) |
| length or vertex-normalized Jacobi amplitude | \(+1\) |
| screen or spherical-orbit area | \(+2\) |
| spatial three-volume | \(+3\) |
| spacetime four-volume | \(+4\) |
| nonzero scalar curvature or normalized tidal eigenvalue | \(-2\) |
| nonzero quadratic curvature scalar | \(-4\) |

Each is a `CONDITIONAL_ANCHOR_CLASS`: it can calibrate the one G249 scale only after its geometric
object is matched and its absolute value is independently calibrated. Metric volume computed from
the same unknown metric is not an independent anchor. Zero curvature cannot calibrate \(\ell\),
because every member of the homothety orbit then returns zero.

## 5. Weight-zero and conversion-only data

The following do not change along the G249 scale orbit:

- reciprocal depth, redshift, and clock ratios;
- causal cones;
- the unit-determinant Jacobi shape;
- any other dimensionless normalized metric response.

The observed constant \(c_E\) has dimensions \(LT^{-1}\). It converts one supplied absolute clock
interval to a length, but it is not itself that interval. The observed \(G_{\rm obs}\) has
dimensions \(L^3M^{-1}T^{-2}\) and has no active native placement law in the bounded metric chain.

No monomial in \(c_E\) and \(G_{\rm obs}\) alone has dimensions of length. If

\[
c_E^aG_{\rm obs}^b\sim L,
\]

mass neutrality gives \(b=0\), time neutrality then gives \(a=0\), and the resulting length
exponent is zero rather than one.

## 6. Mass, density, and energy-density candidates

Exact dimensional linear algebra reproduces the unique monomial exponent solutions already
bounded by G132 and G202:

\[
\boxed{\ell_M\sim\frac{G_{\rm obs}M}{c_E^2}},
\]

\[
\boxed{\ell_\rho\sim\frac{c_E}{\sqrt{G_{\rm obs}\rho}}},
\qquad
\ell_\epsilon\sim\frac{c_E^2}{\sqrt{G_{\rm obs}\epsilon}}.}
\]

These are `DIMENSIONALLY_ELIGIBLE_NEEDS_ATTACHMENT`, not direct scale owners. Dimensional analysis
does not determine which mass, density, or energy density is relevant, where it lives in the
observer network, which metric length it equals, or the dimensionless proportionality. Choosing
that identification merely because it supplies a desired scale would add scaffolding.

## 7. Observational anchors already in the repository

### Current G236/G237 SNe state

The current dual-SNe state is explicitly relative. One additive offset per release removes the
absolute magnitude and distance-scale zero point. It can constrain dimensionless shape after its
stated processing and transfer assumptions; it cannot calibrate \(\ell\).

### Historical G99 scale

G99 contains a dimensionful `X_eff`, but its premise ledger makes that normalization conditional
on external \(M_B\), P1, and imported luminosity transfer. G197 excludes those objects from native
kernel construction. G99 therefore remains a historical conditional external cross-check. It may
not be promoted to the native G249 anchor without separately reauthorizing and auditing its
transfer bridge.

No G99 numerical value enters G250.

## 8. Type-separated landing

```text
ONE_MATCHED_NONZERO_HOMOTHETY_WEIGHT_ANCHOR_CONDITIONALLY_FIXES_THE_SINGLE_G249_SCALE
__ADDITIONAL_INDEPENDENT_ANCHORS_TEST_THE_SUPPLIED_DIMENSIONLESS_HISTORY_RATHER_THAN_ADD_SCALE_PARAMETERS
__CE_GOBS_RECIPROCAL_REDSHIFT_AND_RELATIVE_SNE_STATE_DO_NOT_FIX_ABSOLUTE_SCALE
__MASS_DENSITY_ENERGY_COMPOSITES_ARE_DIMENSIONAL_CANDIDATES_ONLY_UNTIL_A_METRIC_ATTACHMENT_LAW_IS_SUPPLIED
__G99_XEFF_REMAINS_HISTORICAL_TRANSFER_CONDITIONAL_NOT_NATIVE_G249_INPUT
__NO_ANCHOR_VALUE_HISTORY_PROFILE_OR_OUTCOME_SELECTED
```

This result closes the anchor **type** question, not the observational calibration. It neither
chooses an anchor nor supplies its measured value.
