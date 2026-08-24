# G249 exact derivation — reciprocal/angular absolute-scale ownership

Date: 2026-08-24

## 1. Two meanings of calibration

The founded conversion has type

\[
c_E\in \mathsf L\,\mathsf T^{-1}.
\]

Reciprocal depth and redshift are dimensionless:

\[
\delta_{AB}=-\log r_{AB},
\qquad
r_{AB}=\frac{d\tau_B}{d\tau_A},
\qquad
\phi=\log(1+z).
\]

Therefore `c_E` fixes how a supplied clock interval is expressed as a ruler interval, but it is not
itself a clock interval or a ruler length. A monomial made only from `c_E` has dimensions

\[
[c_E^a]=\mathsf L^a\mathsf T^{-a}.
\]

To have area dimensions would require simultaneously (a=2) and (-a=0), which is impossible.
Dimensionless functions of (phi) or (z) do not alter this result. An absolute time, length, mass
with an additional dimensional law, or another dimensional datum is required to manufacture an
absolute area.

## 2. Exact primary-metric scale family

Write (x^0=c_Et). Let (F(s)>0) be any supplied dimensionless profile and let
(ell>0) be a dimensional scale. The primary static-spherical metric family is

\[
g_\ell
=-F(r/\ell)(dx^0)^2+F(r/\ell)^{-1}dr^2+r^2d\Omega^2.
\]

Set

\[
u=\frac{x^0}{\ell},
\qquad
s=\frac r\ell.
\]

Then exactly

\[
\boxed{
g_\ell=\ell^2\bar g,
\qquad
\bar g=-F(s)du^2+F(s)^{-1}ds^2+s^2d\Omega^2.
}
\]

The same observed (c_E) appears in every member through (x^0=c_Et). It has not been changed or
set to one. The entire dimensionless presentation potential

\[
\bar\phi(s)=-\frac12\log F(s)
\]

is also identical in every member. At corresponding static observer events,

\[
r_{AB}
=\frac{e^{-\bar\phi(s_B)}}{e^{-\bar\phi(s_A)}},
\qquad
\delta_{AB}=\bar\phi(s_B)-\bar\phi(s_A)
\]

are independent of (ell). Positive constant homothety also preserves time orientation and null
cones. The metrics are not thereby declared gauge-equivalent: their absolute lengths, areas, and
curvature scales differ.

## 3. Full Jacobi scaling

Let (\bar\gamma(\sigma)) be a source-clock-normalized null branch of (\bar g). For
(g_\ell=\ell^2\bar g), unit clocks and normalized null tangents scale as

\[
U_\ell=\ell^{-1}\bar U,
\qquad
k_\ell=\ell^{-1}\bar k,
\qquad
\lambda=\ell\sigma.
\]

An orthonormal screen basis similarly scales by (ell^{-1}). Since a constant metric homothety
leaves the Levi-Civita connection unchanged while the normalized arguments rescale, the screen
tidal matrix obeys

\[
\boxed{
\mathcal T_\ell(\lambda)
=\ell^{-2}\bar{\mathcal T}(\lambda/\ell).
}
\]

If the dimensionless Jacobi map solves

\[
\bar{\mathcal D}''+\bar{\mathcal T}\bar{\mathcal D}=0,
\qquad
\bar{\mathcal D}(0)=0,
\qquad
\bar{\mathcal D}'(0)=I,
\]

then

\[
\boxed{
\mathcal D_\ell(\lambda)
=\ell\bar{\mathcal D}(\lambda/\ell)
}
\]

has the same vertex data and satisfies the scaled equation. Uniqueness of the matrix IVP makes this
the complete scaled solution, not an ansatz.

Consequently, on the regular rank-two screen,

\[
\boxed{
A_\ell(\lambda)=\ell^2\bar A(\lambda/\ell),
\qquad
C_\ell(\lambda)=\bar C(\lambda/\ell).
}
\]

The absolute area changes, while the unit-determinant shape and all dimensionless reciprocal clock
ratios are retained. The same block scaling follows from the full phase map by conjugating with
(\operatorname{diag}(\ell I_2,I_2)): the upper-right Jacobi block scales by (\ell), while the
full phase remains symplectic.

## 4. Consequence for the G248 interlock

G248 gives, branchwise,

\[
d\mu_{AB}=\frac{r_{AB}}{A_{AB}}d\tau_A.
\]

At corresponding dimensionless branch points,

\[
r_{AB,\ell}=\bar r_{AB},
\qquad
\left(\frac rA\right)_\ell
=\ell^{-2}\left(\frac rA\right)_{1}.
\]

Thus the interlock is genuinely scale-sensitive. It can measure or constrain an absolute scale once
an absolute incidence/area datum is supplied. It does not make the scale disappear or derive its
numerical value from a dimensionless clock ratio.

For corresponding dimensionless source intervals, (d\tau_{A,\ell}=\ell d\bar\tau_A), so the
full one-dimensional coarea density scales as (ell^{-1}). This typing does not turn it into a
probability, flux, or detector measure.

## 5. Why a value of phi does not determine normalized angular response

In the primary metric, G201 gives the dimensionless local angular amplitudes

\[
A_\parallel=e^{-2\phi}(2p^2+p-q),
\qquad
A_\perp=1-e^{-2\phi}(1+p),
\]

where (p=r\phi') and (q=r^2\phi''). At the same value (phi=0),

\[
(p,q)=(0,0)
\quad\Rightarrow\quad
(A_\parallel,A_\perp)=(0,0),
\]

while

\[
(p,q)=(1,0)
\quad\Rightarrow\quad
(A_\parallel,A_\perp)=(3,-1).
\]

Therefore equal redshift depth does not fix even the normalized local angular response. The missing
information is not an external angular coefficient: it is the first two jets of the same metric
history and, for finite propagation, the complete tidal history along the labelled branch.

## 6. What a complete dimensionless history does fix

Once the following are supplied:

1. the complete dimensionless metric history (\bar g);
2. one source-clock-normalized labelled null branch;
3. the G188 vertex conditions;

the Jacobi IVP uniquely fixes (\bar{\mathcal D}(\sigma)), (\bar A(\sigma)), and
(\bar C(\sigma)). No angular fit coefficient survives.

Writing (\bar A) as a single-valued function of (\phi) requires an additional mathematical
condition: (phi(\sigma)) must be injective on the declared branch interval. At a turning point or
across multiple route labels, the lawful object is the parametric or branch-labelled relation

\[
(\phi(\sigma),\bar A(\sigma),\bar C(\sigma)),
\]

not an artificially single-valued (A(\phi)).

## 7. Conditional one-anchor closure

Suppose the dimensionless history and branch are already fixed and (\bar A(\sigma_*)>0). One
independent absolute area anchor (A_*) would determine

\[
\boxed{
\ell=\sqrt{\frac{A_*}{\bar A(\sigma_*)}}.
}
\]

Equivalently, an independently supplied absolute time (T_*) can be converted to a length
(c_ET_*). Redshift supplies frequency or clock ratios, not that absolute interval. This is a
conditional calibration theorem, not an observational fit and not a claim that the dimensionless
history has already been selected.

## 8. Landing

```text
CE_AND_RECIPROCAL_REDSHIFT_FIX_DIMENSIONLESS_CLOCK_RATIOS_NOT_ABSOLUTE_LENGTH
__POSITIVE_HOMOTHETY_PRESERVES_COMPLETE_DIMENSIONLESS_PHI_HISTORY_CAUSAL_STRUCTURE_AND_NORMALIZED_SHAPE_WHILE_JACOBI_AREA_SCALES_AS_LENGTH_SQUARED
__PHI_VALUE_ALONE_DOES_NOT_FIX_NORMALIZED_ANGULAR_RESPONSE
__FULL_DIMENSIONLESS_METRIC_AND_BRANCH_FIX_NORMALIZED_JACOBI_RESPONSE_CONDITIONALLY
__ONE_INDEPENDENT_DIMENSIONFUL_ANCHOR_REMAINS_FOR_ABSOLUTE_SCALE
```

This is a bounded ownership theorem. It does not select the physical history, assign the anchor,
fit a numerical scale, aggregate branches, cross caustics, or derive source/detector physics or an
observational prediction.
