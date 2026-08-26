# G266 exact derivation — covariant mutual pair even-channel ownership

Date: 2026-08-26

## Landing

```text
CANONICAL_REVERSAL_EVEN_TRACE_CHANNEL_DERIVED_ON_SUPPLIED_TIMELIVE_RELATION
__NONTRIVIAL_COMPOSITION_REQUIRES_THE_ODD_COMPANION
__SECH_PHYSICAL_PROJECTION_DISTANCE_FUNCTIONAL_AND_HISTORY_SELECTION_OPEN
```

This is preregistered alternative B. The result is conditional on one supplied regular calibrated
time-live observer relation. It neither adopts the recovered mutual-distance premise nor selects a
metric history.

## 1. Covariant signed input

G220 gives, on one supplied regular future-null incidence,

\[
r_{AB}=\frac{d\tau_B}{d\tau_A}
=\frac{k_A\!\cdot U_A}{k_B\!\cdot U_B}>0,
\qquad
\delta_{AB}=-\log r_{AB}.
\]

The ratio is invariant under a common affine rescaling of the null generator. Mathematical reversal
of this same correspondence gives

\[
r_{BA}=r_{AB}^{-1},
\qquad
\delta_{BA}=-\delta_{AB}.
\]

A later causal return is a different incidence relation and is not asserted to be this inverse.

## 2. The canonical even and odd channels

On the completed reciprocal two-channel representation,

\[
D_{AB}=\begin{pmatrix}r_{AB}&0\\0&r_{AB}^{-1}\end{pmatrix}.
\]

Within this determinant-one two-leg reciprocal kernel on the supplied relation, the primitive
reversal-even conjugacy invariant is its trace, so define

\[
\boxed{
\Gamma_{AB}=\frac12\operatorname{Tr}D_{AB}
=\frac12\left(r_{AB}+r_{AB}^{-1}\right)
=\cosh\delta_{AB}.
}
\]

The signed companion is

\[
\boxed{
\Xi_{AB}=\frac12\left(r_{AB}^{-1}-r_{AB}\right)
=\sinh\delta_{AB}.
}
\]

Then

\[
\Gamma_{AB}^2-\Xi_{AB}^2=1,
\]

\[
\Gamma_{BA}=\Gamma_{AB},
\qquad
\Xi_{BA}=-\Xi_{AB},
\]

and the two directed legs are recovered exactly:

\[
r_{AB}=\Gamma_{AB}-\Xi_{AB},
\qquad
r_{AB}^{-1}=\Gamma_{AB}+\Xi_{AB}.
\]

Thus the even channel is not an added instrument. It is already the trace invariant of the same
reciprocal representation that contains the directional clock/ruler legs. Other smooth
reversal-even scalar readouts formed only from this kernel may still be arbitrary functions of
`Gamma`; trace naturality does not choose their physical interpretation. This classification does
not cover arbitrary physical scalars constructed from the complete ambient metric.

## 3. Why the even channel cannot compose alone

For composable supplied relations, `r_AC=r_BC r_AB` and
`delta_AC=delta_AB+delta_BC`. Therefore

\[
\boxed{
\Gamma_{AC}
=\Gamma_{AB}\Gamma_{BC}+\Xi_{AB}\Xi_{BC},
}
\]

\[
\boxed{
\Xi_{AC}
=\Xi_{AB}\Gamma_{BC}+\Gamma_{AB}\Xi_{BC}.
}
\]

The mutual and directional channels are interlocked. Dropping `Xi` destroys nontrivial
composition.

There is also a short no-go theorem. Let `m(delta)>0` be continuous and multiplicative,

\[
m(\delta_1+\delta_2)=m(\delta_1)m(\delta_2).
\]

Then `m(-delta)=m(delta)^{-1}`. If the same scalar is reversal-even,
`m(-delta)=m(delta)`, positivity gives

\[
\boxed{m(\delta)=1.}
\]

So a nontrivial mutual magnitude cannot be an independent one-dimensional multiplicative
character. It must remain joined to the signed companion inside the full reciprocal kernel.

## 4. Conditional mutual clock projection

If one additionally declares that physical mutual clock rate is the inverse of the reciprocal
trace magnitude, then

\[
\boxed{
M_{AB}=\Gamma_{AB}^{-1}
=\frac{2r_{AB}}{1+r_{AB}^2}
=\operatorname{sech}\delta_{AB}.
}
\]

This expression is covariant on the supplied G220 relation, positive, at most one, and invariant
under reversal. No fitted coefficient or external response function is involved.

But the inverse-clock interpretation is not selected by F1--F4, W1, or W4. Those premises derive
`Gamma`; they do not say whether the physical mutual readout is `Gamma`, `Gamma^-1`, or another
function of `Gamma`. Accordingly `sech(delta)` remains a particularly simple proposed projection,
not an adopted result.

## 5. The simplest spacetime biscalar cannot be the distance

For the null incidences used by G220, Synge's world function obeys

\[
\sigma(A,B)=0
\]

for every separation along the branch. Its scalar value therefore cannot distinguish nontrivial
pair depths. Endpoint derivatives of `sigma` do encode the null tangent and hence the signed clock
arrow, but that is relation data, not a new scalar distance value.

Radar distance requires an emission-reflection-reception protocol. Pair-surface ruler distance
requires a supplied pair germ. Both are lawful metric constructions, but neither is selected by a
single one-way null incidence.

## 6. Three natural distance attachments agree locally and then separate

The remaining ownership issue can be shown sharply in the primary static spherical metric

\[
ds^2=-f(R)c_E^2dt^2+\frac{dR^2}{f(R)}+R^2d\Omega^2,
\qquad
\delta(R)=\phi(R)-\phi(R_0),
\qquad
f=e^{-2\phi}.
\]

Let `x=R-R0`, `sqrt(f(R0))=y0`, and explore the same simple statement

\[
d\delta=\kappa\,ds,
\]

where `kappa` is a freely explored positive inverse length. The primary metric has already fixed
`R` as the invariant areal-radius descriptor through the angular orbit area. That geometric fact
does not declare `Delta R`, static-slice ruler length, or optical length to be the physical mutual
distance. Supplying each of those three attachments in turn gives three exact controls.

### Areal-radius attachment

Here `R` is already a metric-owned areal scalar, while the further identification `ds=dR` as the
physical mutual-distance increment is `FREE_AND_EXPLORED`. With that identification,

\[
\boxed{f_{\rm areal}=y_0^2e^{-2\kappa x}.}
\]

### Static-slice proper separation

With `ds=dR/sqrt(f)`,

\[
\boxed{f_{\rm slice}=(y_0-\kappa x)^2.}
\]

### Optical null separation

With `ds=dR/f`,

\[
\boxed{f_{\rm opt}=y_0^2-2\kappa x.}
\]

All three profile families are derived only after their physical distance attachment is supplied.
At a unit-calibrated anchor
`y0=1`, they have the same value and first derivative,

\[
f(0)=1,
\qquad
f'(0)=-2\kappa,
\]

but distinct second derivatives,

\[
\boxed{
f_{\rm areal}''(0)=4\kappa^2,
\quad
f_{\rm slice}''(0)=2\kappa^2,
\quad
f_{\rm opt}''(0)=0.
}
\]

This explains why the missing distinction can hide in a local calibration: the three attachments
agree through first order and separate exactly where curvature/angular second-jet information
begins to matter. Since areal radius is an invariant spherical scalar, these different functions of
`R` are not mere radial-coordinate relabellings inside the marked areal branch.

## 7. Ownership result

The present premises derive a stronger and simpler kernel statement than G265 alone:

- the reversal-even trace magnitude `Gamma=cosh(delta)` is canonical inside the determinant-one
  reciprocal kernel on a supplied relation;
- it and the signed companion are inseparable under nontrivial composition;
- `sech(delta)` is the simplest inverse-trace clock projection, but remains physically unadopted;
- null incidence alone does not own a nonzero separation scalar;
- several metric-constructed distance controls agree locally and produce inequivalent histories;
  the areal control uses an already-owned geometric descriptor, but its promotion to physical
  mutual distance is no more derived than the other two attachments.

Therefore current premises reject no admitted history. The remaining bridge is no longer “find an
even function.” It is to own one operational two-point distance protocol and its relation to the
already-derived trace channel, or to derive that ownership from a richer physical pair semantics.
