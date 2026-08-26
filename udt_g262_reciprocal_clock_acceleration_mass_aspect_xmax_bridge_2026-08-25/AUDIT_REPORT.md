# G262 audit report — clock, acceleration, mass-aspect, and Xmax bridge

Date: 2026-08-25
Grade: `VERIFIED_INTERNALLY_WITH_CAVEATS__EXTERNAL_REVIEW_PENDING`

## Primary landing

```text
ONE_METRIC_STATE_HIERARCHY_DERIVED
__COVECTOR_ENERGY_PAIRING_CONDITIONAL
__LOCAL_REST_MASS_PHYSICAL_TOTAL_MASS_XMAX_VALUE_AND_HISTORY_LAW_OPEN
```

## Result

On the full primary static-spherical metric, one lapse `N=exp(-phi)` owns an exact hierarchy:

\[
d\tau=Ndt,
\qquad
a_{\hat r}=N',
\qquad
\mu=\frac r2(1-N^2),
\]

\[
\mathcal E_0=-2\mu',
\qquad
\mathcal E_1=-r\mu'',
\qquad
A_\parallel+A_\perp=2\mu'-r\mu''.
\]

Thus time, static acceleration, spherical compactness/mass-aspect geometry, curvature, and the
angular trace are interlocked descriptions of one metric state. None is a post-readout correction.

On a supplied endpoint-exact pair,

\[
q_{os}=\frac{d\tau_s}{d\tau_o}=e^{-(\phi_s-\phi_o)}=\frac1{Z_{so}}.
\]

After the separate G95 physical-carrier-covector identification,

\[
\frac{E_o}{E_s}=q_{os}.
\]

For the working normalized pair coordinate `chi=tanh(delta)`,

\[
q=\sqrt{\frac{1-\chi}{1+\chi}}.
\]

The `chi` endpoint therefore gives reciprocal zero/infinity pair-energy limits. It does not imply
infinite local rest mass. In the same static chart a zero lapse gives the distinct geometric limit
`mu/r -> 1/2`.

## What was accomplished

- the user's time/acceleration/gravity/mass intuition becomes one exact bounded metric hierarchy;
- the angular orchestra is retained and rewritten as mass-aspect derivatives;
- the existing conditional energy-redshift theorem is joined to the same clock factor with correct
  arrow typing;
- the Xmax relationship is made exact without inserting a numerical scale or profile;
- local rest mass, remote energy, geometric mass aspect, and physical total mass are separated.

## What was not accomplished

Every identity holds for arbitrary positive `f`. Both preregistered profiles `f0=1` and
`fa=1+a r^2/(1+r^2)` satisfy the complete hierarchy while having distinct metric data. Therefore
the hierarchy does not propagate or select `phi` values.

A generic positive mass factor depending only on clock ratio becomes `F(q)=q^w` only after a new
mass-composition/regularity premise; the physical object and weight remain open. G95 conditionally
realizes the `w=1` numerical factor only for a supplied transported covector energy readout.

The geometric attachment `M_ref=c_E^2 mu/G_obs` remains a GR/Misner--Sharp comparison, not native
UDT matter. No source, action, boundary, total mass, numerical Xmax, or history law was derived.

## Evidence

- preregistration and pre-execution type repair were separately committed and pushed;
- 19 arbitrary-function symbolic checks pass;
- independent standard-library exact-Fraction replay passes 10,003 assertions over 1,000 cases;
- 10/10 applied sign, factor, direction, and ownership mutations are rejected;
- current 244-row premise registry verification passes;
- no observations, fits, GPU, protected package, GR field equation, or particle model entered.

## Maximum conclusion

G262 derives a cohesive static-spherical metric hierarchy and narrows the missing bridge to a
physical source/mass feedback or another nonidentity dynamics generator. It does not derive a
local rest-mass dilation law, normalized physical mass, `Xmax`, or the valued history.
