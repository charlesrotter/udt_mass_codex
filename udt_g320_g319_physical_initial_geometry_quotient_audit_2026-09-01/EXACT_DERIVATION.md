# G320 exact derivation — physical initial geometry after representation quotient

Date: 2026-09-01
Grade: `EXTERNALLY_ACCEPTED_BOUNDED`

## Bounded landing

```text
G319_FREEDOM_NOT_PURE_REPRESENTATION__SCALE_FREE_INTRINSIC_CURVATURE_SEPARATES_LAWFUL_PROFILES__DECLARED_GAUGE_DUPLICATES_QUOTIENTED__NO_COMPLETE_MODULI_OR_PHYSICAL_DATA_SELECTION
```

This conclusion is restricted to the flat marked-`T^3`, one-coordinate, diagonal-TT, smooth
positive periodic, sign-definite `B!=0` G319 slice. It does not classify the full constraint
surface or choose physical initial data.

## 1. Compare physical data, not conformal coordinates

G319 uses the conformal presentation

\[
\gamma_{ij}=\psi^4\delta_{ij}.
\]

The physical initial datum is `(gamma,K)`, not the seed tuple. Two presentations are physically
equivalent only when a spatial diffeomorphism carries the complete pair:

\[
(\widehat\gamma,\widehat K)=(f^*\gamma,f^*K).
\]

Consequently, raw differences in `psi`, coordinate phase, the auxiliary vector `W`, or the
conformal seed cannot establish physical inequivalence. A scalar curvature invariant of the
reconstructed physical metric can.

## 2. Exact intrinsic separator

For a three-dimensional conformal metric `gamma=psi^4 delta`, with `psi=psi(x)`,

\[
{}^{(3)}R=-8\psi^{-5}\psi'',
\qquad
d\mu_\gamma=\psi^6\,dx\,dy\,dz.
\]

On a periodic torus, integration by parts gives

\[
\mathcal S[\psi]
:=\int_{T^3}{}^{(3)}R\,d\mu_\gamma
=-8\int_{T^3}\psi\psi''\,d^3x
=8\int_{T^3}(\psi')^2\,d^3x.
\tag{1}
\]

Both `Vol(gamma)` and `S[psi]` are spatial-diffeomorphism invariants. Under a common constant
rescaling `gamma -> ell^2 gamma`,

\[
\mathcal S\longmapsto \ell\mathcal S,
\qquad
\operatorname{Vol}^{1/3}\longmapsto \ell\operatorname{Vol}^{1/3}.
\]

Therefore

\[
\boxed{
Q_R[\psi]
=\frac{\mathcal S[\psi]}{\operatorname{Vol}(\gamma)^{1/3}}
}
\tag{2}
\]

is invariant under spatial diffeomorphisms and insensitive to an unattached common ruler scale.

## 3. Same values and volume, inequivalent geometry

Use the preregistered family

\[
\psi_n(x)=p+a\cos(nx),
\qquad
p=\frac32,
\qquad
a=\frac15,
\qquad n\in\mathbb N.
\tag{3}
\]

All members are positive. For every positive integer `n`, `cos(nx)` has the same value distribution
on the circle, so

\[
\operatorname{Vol}(\gamma_n)
=(2\pi)^3\left[
p^6+\frac{15}{2}p^4a^2+\frac{45}{8}p^2a^4+\frac5{16}a^6
\right]
\tag{4}
\]

is independent of `n`. But

\[
\int_{T^3}(\psi_n')^2d^3x
=(2\pi)^2\pi a^2n^2,
\]

and hence

\[
\boxed{Q_R[\psi_n]=n^2Q_R[\psi_1].}
\tag{5}
\]

No spatial diffeomorphism can carry `gamma_n` to `gamma_m` for `n!=m`, because it would have to
preserve `Q_R`. No conformal-seed rewrite can identify them either: a seed rewrite that represents
the same physical metric must preserve every invariant of that metric. G319 admits every positive
smooth periodic profile after a sufficiently large free `J0` is supplied. Equations (3)--(5)
therefore exhibit at least a countably infinite set of genuinely inequivalent physical initial
geometries in the registered G319 family.

This is not a complete quotient. Profiles related by translations, reflections, or other lawful
spatial diffeomorphisms remain equivalent, and G320 does not prove that every different-looking
profile defines a different moduli point.

## 4. Lawful G319 data, not merely intrinsic trial metrics

For the finite replay controls `n=1,2,3,4`, set only for diagnosis

\[
d=0,
\qquad
\Lambda=0,
\qquad
J_0=100.
\]

G319 gives

\[
Z=36(\psi')^2+J_0,
\qquad
B=\epsilon\psi^{-3}\sqrt Z,
\qquad
A=F/B,
\]

with `epsilon=+1` and `epsilon=-1`. The preregistered bound

\[
Z+\psi^6F
=36(\psi')^2+J_0+12\psi\psi''
\ge J_0-12an^2(p+a)>0
\]

holds for all four modes. Thus `B` never vanishes and `tau=(A+B)/2` has the selected branch sign.
Reconstructing `K` with the G319 formula gives maximum production residuals

```text
Hamiltonian       3.56e-15
momentum          1.78e-15
J0 drift          8.53e-14
```

over 16,384 points per mode and sign. The implementation-distinct verifier used different
`p,a,J0`, modes `1,3,5`, and 3,072 points; it rebuilt Christoffels and Ricci by index loops and
again obtained lawful physical data.

The finite controls do not prove the arbitrary-profile theorem. G319's compactness theorem does.
The controls prove that the registered invariant examples actually lie on the reconstructed
constraint surface and catch implementation/sign errors.

## 5. Representation controls

### Spatial isometries

For phase translations `psi_n(x-theta)` and reflections `psi_n(-x)`, production recomputed volume,
total scalar curvature, `Q_R`, and volume-weighted `tr(K)`, `tr(K^2)`, and `tr(K^3)`. All remained
equal within the registered numerical tolerance. These controls ensure that raw array differences
are not mistaken for physics.

### Conformal-seed covariance

For any positive `vartheta(x)`, set

\[
\widehat{\bar\gamma}=\vartheta^4\bar\gamma,
\qquad
\widehat\psi=\psi/\vartheta,
\qquad
\widehat{\bar A}^{ij}=\vartheta^{-10}\bar A^{ij}.
\]

Then

\[
\widehat\psi^4\widehat{\bar\gamma}=\psi^4\bar\gamma,
\qquad
\widehat\psi^{-10}\widehat{\bar A}^{ij}=\psi^{-10}\bar A^{ij}.
\]

With unchanged `tau`, the reconstructed physical `(gamma,K)` is identical. Production and the
independent verifier used different nonconstant `vartheta` controls. Their maximum pointwise
metric errors were `3.56e-15` and `1.78e-15`; physical trace-free tensor errors were `1.67e-16`
and `3.89e-16`. Different seed fields were correctly classified as the same physical datum.

## 6. What the extrinsic channel adds

The two signs reverse `K` while leaving the intrinsic metric and even contractions such as
`tr(K^2)` unchanged; odd contractions reverse. Mode changes also alter the volume-weighted
extrinsic contractions. These are useful physical characterizers of each reconstructed initial
datum, but they are not load-bearing for the inequivalence theorem: the intrinsic `Q_R` separator
already proves that the complete pairs cannot be diffeomorphic.

## 7. Exact meaning and open boundary

- `DERIVED_CONDITIONAL_IN_REGISTERED_SLICE`: equations (1)--(5).
- `DERIVED_CONDITIONAL_IN_REGISTERED_SLICE`: at least countably many inequivalent physical initial
  geometries occur within the G319 family.
- `QUOTIENTED_CONTROLS`: phase, reflection, auxiliary-vector kernel, and conformal-seed duplicates.
- `OPEN`: the complete moduli quotient of arbitrary G319 profiles.
- `OPEN_NOT_SELECTED`: which initial data are physically occupied and how they evolve globally.

Nothing here selects Nature's data, physical topology, history, population, source, matter/mass,
observation, scale, or physical `X_max`. The UDT metric, reciprocal kernel, angular cancellation,
and pair-readout interfaces are unchanged.
