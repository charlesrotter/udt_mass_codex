# G212 exact derivation — what the missing “history” is and is not

Date: 2026-08-22

## Landing

```text
RANK_COMPLETE_VALUED_COMPLETED_PAIR_NETWORK_CAN_BE_THE_METRIC_STATE
__NO_SECOND_HISTORY_SELECTOR_IS_NEEDED_AFTER_FAITHFUL_RECONSTRUCTION
__CURRENT_RECIPROCITY_COMPATIBILITY_AND_CAUSAL_IDENTITIES_DO_NOT_GENERATE_NETWORK_VALUES_FROM_FINITE_ANCHORS
__TWO_GENERIC_COMPLETED_CLOCKS_RECONSTRUCT_THE_G211_SCALAR_MODES_POINTWISE
__UNIVERSAL_SCALAR_PAIR_LAW_DOES_NOT_FORCE_CONSTANT_CURVATURE
__FULL_ALL_GERM_TWO_JET_ISOTROPY_FORCES_A_SPACE_FORM_ONLY_CONDITIONALLY
```

The result is a reconciliation, not a new history law. G129--G130 already proved that a smooth,
compatible, rank-ten network of known full pair pullbacks and its values is equivalent to one
Lorentz metric on the covered regular region. G176 and G211 now sharpen what the completed
reciprocal data hear. They do not change the distinction between reconstruction of supplied values
and prediction of those values.

## 1. The three different questions

Let a local completed pair relation include its embedding/calibrated germ, auxiliary pullback,
reciprocal ruler density, completed pullback, endpoint calibration, branch label, and any requested
screen/transport outputs.

Three questions must not be merged:

1. **Local reconstruction:** do sufficiently many pair relations determine the metric germ?
2. **Global descent:** do compatible local reconstructions define one metric/network state?
3. **Finite-data prediction:** do the founding identities generate all numerical relation values
   from finitely many constants or anchors?

G129 answers question 1 conditionally at rank ten and question 2 on a declared regular compatible
cover. It does not answer question 3. Calling the full valued network the state removes the false
need for another selector between that network and `g`; it does not compress infinite-dimensional
state data into a few constants.

## 2. Pointwise scalar tomography after G211

In the supplied G211 split, write a clock tangent as

\[
J_i=\alpha_i\partial_t+v_i,
\qquad
w_i=v_i+\alpha_i b.
\]

Define known germ coefficients

\[
C_i=f\alpha_i^2>0,
\qquad
S_i=h_A(w_i,w_i)\ge0.
\]

On the regular completed-clock stratum,

\[
e^{-2\Phi_i}
=e^{2\Omega}\left(C_i-e^{2q}S_i\right).
\]

Put

\[
x=e^{2\Omega},
\qquad
y=e^{2\Omega+2q},
\qquad
R_i=e^{-2\Phi_i}.
\]

Two completed clocks give the exact linear system

\[
\boxed{
\begin{pmatrix}
C_1&-S_1\\
C_2&-S_2
\end{pmatrix}
\binom{x}{y}
=
\binom{R_1}{R_2}.
}
\]

Its determinant is

\[
\Delta=C_2S_1-C_1S_2.
\]

If `Delta` is nonzero and the reconstructed `x,y` are positive, then

\[
x=\frac{-S_2R_1+S_1R_2}{\Delta},
\qquad
y=\frac{-C_2R_1+C_1R_2}{\Delta},
\]

and therefore

\[
\boxed{
\Omega=\frac12\log x,
\qquad
q=\frac12\log\frac yx.
}
\]

Two differently bearing completed clocks can therefore reconstruct both G211 scalar modes at one
germ. Two Eulerian/static clocks have `S_1=S_2=0` and are rank deficient. Equivalently, a fully
calibrated causal cone determines `q`, after which one generic completed clock determines `Omega`.

This is a real narrowing: changing channel ratios across a sweep can reconstruct the evolving
frame point by point. But it consumes function-valued pair observations along that sweep. It is
tomography, not propagation from finitely many anchors.

## 3. What exact composition actually gives

On a matched thin endpoint family, suppose a real depth obeys

\[
\delta(A,C)=\delta(A,B)+\delta(B,C),
\qquad
\delta(B,A)=-\delta(A,B).
\]

Choose a reference observer `O` and define

\[
\varphi(A)=\delta(O,A).
\]

Then

\[
\boxed{\delta(A,B)=\varphi(B)-\varphi(A).}
\]

Conversely every function `varphi` defines such a cocycle. Composition therefore produces an
endpoint potential on a matched family; it does not determine the potential's profile.

G171 is stricter than this control. Generic independently realized physical pair germs need not
share one observer-only endpoint readout, so arbitrary triangle additivity is not a primary-metric
identity. It returns only on its exact matched-germ/readout subfamily. Thus even endpoint-potential
descent is conditional, not the missing universal history equation.

## 4. Exact arbitrary-function counterfamily

Take arbitrary smooth real functions `Omega(x)` and `q(x)` and set, on a regular interval,

\[
g=e^{2\Omega(x)}
\left[-dt^2+e^{2q(x)}(dx^2+dy^2+dz^2)\right].
\]

For the coordinate pair surface `F(t,x)=(t,x,0,0)`, the auxiliary pullback is

\[
h_x=-e^{2\Omega}dt^2+e^{2\Omega+2q}dx^2.
\]

G176 gives

\[
m=T L_x=e^{2\Omega+q},
\qquad
ds=m\,dx.
\]

The completed pair becomes

\[
\boxed{
h_s=-e^{2\Omega}dt^2+e^{-2\Omega}ds^2,
\qquad
\Phi=-\Omega.
}
\]

The relative mode `q` changes the physical tape map `s(x)`; the common mode `Omega` changes the
completed depth. Both functions are arbitrary. The pair surface is integrable, the metric is
Lorentzian, and the completed reciprocal determinant is `-1` for every choice.

An equivalent pair-level control starts with arbitrary smooth `Phi(s)`:

\[
h_\Phi(s)=D(\Phi(s))^T\eta_2D(\Phi(s)).
\]

With

\[
C_{ab}=D(\Phi(a))^{-1}D(\Phi(b)),
\]

one has

\[
C_{ab}^Th(a)C_{ab}=h(b),
\quad
C_{ab}C_{bc}=C_{ac},
\quad
C_{ba}=C_{ab}^{-1}
\]

for every smooth `Phi`. Even compatible flat reciprocal carry proves exactness, not a rate law.

Finite calibration anchors cannot remove this functional freedom. A smooth deformation multiplied
by sufficiently high powers of `(x-x_i)` can preserve any finite set of registered anchor jets
while changing the relation elsewhere.

## 5. Why standard geometry does not supply the rate

- `nabla g=0` and zero torsion solve for the Levi-Civita connection of a supplied metric.
- The first Cartan equation solves for connection forms from a supplied coframe.
- The second Cartan equation defines curvature.
- Bianchi identities hold for every Levi-Civita curvature.
- Gauss--Codazzi--Ricci identities relate data of a supplied immersion and ambient metric.
- Along a one-dimensional family, pulled-back curvature two-forms vanish automatically.
- Frobenius may restrict a supplied plane distribution, but the coordinate counterfamily above is
  integrable for arbitrary `Omega,q`.

These become nonidentity restrictions only after an extra curvature value, holonomy reduction,
parallel subbundle, symmetry, boundary, or source condition is supplied. None is currently owned as
the UDT history bridge.

If a canonical additive separation `r` and a basepoint-independent law

\[
\delta(A,B)=F(r_B-r_A)
\]

were separately owned, smooth composition would give Cauchy's equation and `F(r)=k r`. Current UDT
does not own that additive separation or translation-invariant all-observer calibration, and
defining `r=delta` would make the statement tautological.

## 6. The strongest symmetry bridge and its ownership

The same terminal scalar law about every observer does not imply the same metric germ. Scalar pair
readouts have blind sectors. Spherical symmetry about one selected center also leaves arbitrary
radial profiles.

A much stronger conditional statement does close the local geometry:

> At every event, the complete coincidence two-jet of every normalized timelike--spacelike pair
> germ is equivalent under an isotropy group transitive on the relevant orthonormal two-frames.

Then every nondegenerate sectional curvature at the event is equal, so

\[
R_{abcd}=K(p)(g_{ac}g_{bd}-g_{ad}g_{bc}).
\]

In connected dimension at least three, the contracted Bianchi identity gives `dK=0`. Hence the
metric is locally a constant-curvature space form.

For the primary static spherical ansatz

\[
ds^2=-f(r)c_E^2dt^2+\frac{dr^2}{f(r)}+r^2d\Omega_2^2,
\]

the independent orthonormal sectional curvatures include

\[
K_{t\theta}=K_{r\theta}=-\frac{f'}{2r},
\qquad
K_{\theta\varphi}=\frac{1-f}{r^2},
\qquad
K_{tr}=-\frac{f''}{2}.
\]

Equality gives

\[
r f'=2(f-1),
\]

and regular-center calibration gives

\[
\boxed{
f(r)=1-Kr^2,
\qquad
\phi(r)=-\frac12\log(1-Kr^2).
}
\]

This leaves one continuous local modulus `K`, plus its sign/flat case. One direct curvature or
length anchor could calibrate nonzero `K`. `c_E` and `G_obs` alone do not form a length without a
lawfully identified mass/density/energy datum and bridge.

The all-germ isotropy premise is not owned by current UDT. Reciprocity does not assert an isometry
group, equality of directional coincidence two-jets, a canonical geodesic tape, or local two-point
homogeneity. Spatial isotropy about comoving observers is also insufficient: an FLRW-type metric
can have arbitrary lapse and scale factor. Promoting the space-form control would therefore add
scaffolding rather than reveal a currently derived law.

## 7. Resolution and next gate

The phrase “missing history” bundled a false problem with a real one:

- **False extra problem:** after a rank-complete valued completed-pair network is supplied and
  shown globally compatible, no second metric-history selector is required. The network is a valid
  relational representation of the state and `g` is its reconstruction.
- **Real open problem:** current premises do not generate the numerical network valuation or a
  finite-dimensional separation flow from a few anchors.

The next native calculation is not another search for a history mechanism. It is the already
identified determinant-one spatial-remainder census followed by a finite multidirectional
completed-pair rank test. That test asks whether G176-completed relations, including their ruler
density and non-scalar channels, retain the rank-ten metric information that G129 required.

If the completed network is rank complete, the local germ/history bridge is reconstructive and
closed in its bounded domain. Any later finite-anchor prediction claim must then state and test a
separate genuine compression principle rather than calling evaluator compatibility a law.

## Standard comparison references

- Greenwood and Leistner, *Lorentzian homogeneous structures with indecomposable holonomy*,
  <https://arxiv.org/abs/2404.17470>.
- Fels and Renner, *Non-reductive Homogeneous Pseudo-Riemannian Manifolds of Dimension Four*,
  <https://arxiv.org/abs/math/0406147>.

These references support the caution that homogeneity and weaker Lorentzian isotropy conditions do
not generally imply constant curvature. The space-form implication used above is also proved
directly from full curvature isotropy and Bianchi.
