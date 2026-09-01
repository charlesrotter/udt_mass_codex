# G317 exact derivation — coupled non-CMC data family

Date: 2026-09-01
Scope: constant-`psi`, flat marked `T^3`, diagonal-TT, one-coordinate subspace of G316

## 1. Bounded landing

```text
EXACT_NONCMC_COUPLED_TORUS_FAMILY_EXISTS_WITH_ZERO_TIDE_AND_TIDAL_SUBBRANCHES
__CONSTANT_PSI_CLASSIFICATION_FORCES_LAMBDA_MINUS_Q_SQUARED
__NO_PHYSICAL_DATA_SELECTION
```

Reviewed status: `EXTERNALLY_ACCEPTED_BOUNDED__NO_SCIENTIFIC_DEFECT`.

G317 proves a genuine non-CMC family exists inside the G315 constraints and classifies the entire
registered ansatz. It is not a general non-CMC theorem and does not select initial data.

## 2. Active equation and premise boundary

Universal Reciprocity/DDR and both G312 premises are owner-adopted provisionally, not derived or
canonized. In their bounded regular local metric-only vacuum arena,

\[
R_{ab}=\Lambda g_{ab},\qquad d\Lambda=0.
\]

G315 gives

\[
{}^{(3)}R+\frac23\tau^2-A_{ij}A^{ij}=2\Lambda,
\qquad
D_jA^{ij}-\frac23D^i\tau=0.
\]

G316's conformal construction is a `CONDITIONAL_IMPORTED_MATHEMATICAL_METHOD`, not a new UDT law.
The flat torus, constant conformal factor, diagonal TT tensor, and one-coordinate dependence below
are all `CHOSE_BOUNDED_DIAGNOSTIC_SLICE`.

## 3. Registered non-CMC ansatz

On a flat marked torus with dimensionless `2 pi` periodic coordinates, let

\[
\bar\gamma_{ij}=\delta_{ij},\qquad \psi=p>0,
\]

\[
\tau=\tau(x),\qquad \tau'\not\equiv0,
\]

\[
\bar A_{TT}^{ij}=\operatorname{diag}(\alpha,\beta,\gamma),
\qquad \alpha+\beta+\gamma=0,
\]

and

\[
W=w(x)\partial_x.
\]

The constant diagonal tensor is trace-free and divergence-free on the flat seed. Define

\[
\mu=\frac1{2\pi}\int_0^{2\pi}\tau(x)\,dx,
\qquad
d=\frac{\beta-\gamma}{2}.
\]

The longitudinal tensor and its divergence are

\[
(\bar L W)^{ij}
=\operatorname{diag}\left(\frac43w',-\frac23w',-\frac23w'\right),
\]

\[
\bar D_j(\bar L W)^{xj}=\frac43w''.
\]

## 4. Exact vector solution and its kernel

The momentum equation becomes

\[
2w''=p^6\tau'.
\]

After one integration,

\[
w'=\frac{p^6}{2}\tau+c.
\]

Periodicity of `w` requires the mean of `w'` to vanish, fixing

\[
c=-\frac{p^6}{2}\mu.
\]

Therefore

\[
\boxed{w'=\frac{p^6}{2}(\tau-\mu).}
\]

Every smooth periodic `tau` admits such a periodic `w`. Adding a constant to `w` is a translation
conformal-Killing field and leaves `bar L W` unchanged. This is auxiliary nonuniqueness, not an
extra physical field.

For a Fourier presentation

\[
\tau=\mu+\sum_{n\ge1}(a_n\cos nx+b_n\sin nx),
\]

one exact primitive is

\[
w=\frac{p^6}{2}\sum_{n\ge1}
\left(\frac{a_n}{n}\sin nx-\frac{b_n}{n}\cos nx\right)+w_0.
\]

No Fourier coefficient is fitted or selected.

## 5. Complete scalar classification inside the ansatz

Write

\[
\beta=-\frac\alpha2+d,
\qquad
\gamma=-\frac\alpha2-d.
\]

Substitution of the vector solution into the scalar equation and division by `p^5` gives exactly

\[
\mathcal F(x)=
\left(\frac43\mu-2\alpha p^{-6}\right)\tau(x)
-\frac23\mu^2+2\alpha p^{-6}\mu
-\left(\alpha^2+\beta^2+\gamma^2\right)p^{-12}
-2\Lambda.
\]

Because `tau` is nonconstant, the coefficient of `tau(x)` must vanish. Hence

\[
\boxed{\alpha=\frac23p^6\mu.}
\]

Using

\[
\alpha^2+\beta^2+\gamma^2=\frac32\alpha^2+2d^2,
\]

the remaining constant equation becomes

\[
\boxed{\Lambda=-d^2p^{-12}.}
\]

Define

\[
q=d p^{-6}.
\]

Then the necessary and sufficient conditions are

\[
\boxed{
\bar A_{TT}^{ij}=p^6\operatorname{diag}
\left(\frac23\mu,q-\frac13\mu,-q-\frac13\mu\right),
\qquad
\Lambda=-q^2.
}
\]

Thus the TT mean channel, varying longitudinal channel, and connected scalar do interlock. They are
not independent knobs inside this exact family. But the equations retain arbitrary `tau(x)`, `p`,
and `q`; they do not choose their values.

The result `Lambda=-q^2` belongs only to this ansatz. It is not a global UDT sign theorem and does
not conflict with G304's positive result in a different static smooth-center finite-ceiling branch.

## 6. Direct physical reconstruction

The total conformal trace-free tensor is

\[
\bar A_{TT}+\bar L W
=p^6\operatorname{diag}
\left(\frac23\tau,q-\frac13\tau,-q-\frac13\tau\right).
\]

After conformal reconstruction,

\[
\boxed{\gamma_{ij}=p^4\delta_{ij},}
\]

\[
\boxed{K^i{}_j=\operatorname{diag}(\tau(x),q,-q).}
\]

The physical trace and norm are

\[
K=\tau,
\qquad
K_{ij}K^{ij}=\tau^2+2q^2.
\]

Because the spatial metric is flat,

\[
{}^{(3)}R+K^2-K_{ij}K^{ij}
=-2q^2=2\Lambda.
\]

The momentum tensor `K^{ij}-gamma^{ij}K` is diagonal. Its `xx` entry vanishes identically; its
`yy` and `zz` entries depend only on `x`, while their divergence differentiates them in `y` and
`z`. Therefore

\[
D_j(K^{ij}-\gamma^{ij}K)=0.
\]

This direct check rules out a conformal-only circular pass. For every nonconstant profile the
vector source `p^6 tau'` and the longitudinal correction are nonzero somewhere, so the family is
genuinely non-CMC and coupled.

## 7. Zero-tide and tidal subclasses

For Einstein data, the electric Weyl tensor on the slice is

\[
E^i{}_j={}^{(3)}R^i{}_j+K K^i{}_j-K^i{}_kK^k{}_j
-\frac23\Lambda\delta^i{}_j.
\]

The exact diagonal result is

\[
\boxed{
E^i{}_j=\operatorname{diag}
\left(
\frac23q^2,
\tau q-\frac13q^2,
-\tau q-\frac13q^2
\right).
}
\]

It is trace-free. In the registered data the only spatial derivative of `K` is `D_xK_{xx}`;
antisymmetry kills it in the magnetic curl, so

\[
B_{ij}=0
\]

on the initial slice.

Two subclasses are therefore exact:

1. `q=0`: `Lambda=0` and `E=B=0`. Conditional on the already-caveated local uniqueness theorem,
   this is a locally flat development represented by non-CMC slicing data. No global flat torus
   completion is asserted.
2. `q!=0`: `E^x{}_x=2q^2/3` is nonzero everywhere, so the family has a genuine invariant electric
   tidal channel. It is not merely slicing gauge.

Under `q -> -q`, swapping the marked `y` and `z` axes interchanges the last two entries of `K` and
`E`. The sign of `q` is therefore not selected in this axis-symmetric diagnostic family.

## 8. Solution-space meaning

The exact family retains:

- an arbitrary smooth periodic nonconstant function `tau(x)`;
- a positive marked-slice size parameter `p`;
- a continuous transverse parameter `q`;
- the additive conformal-Killing constant in `w`;
- zero-tide and nonzero-tide subclasses.

This is substantial interlocking, but not uniqueness. It shows how the constraint equations turn
some apparently independent seed components into linked quantities. It does not supply a physical
population or actualization law.

Nonconstant `psi`, nonflat conformal geometry, nondiagonal TT tensors, general coordinate
dependence, boundaries, asymptotics, low regularity, global completion, and the rest of the full
constraint surface remain open.

## 9. Maximum conclusion

G317 is the first exact non-CMC family in this construction lane where the vector source is active
and the scalar equation closes only after the longitudinal and TT channels are combined. It also
separates non-CMC coordinate slicing from genuine tide by a metric-invariant Weyl calculation.

No physical initial data, history, topology, scalar magnitude, scale, source, matter/mass law,
observation, fit, or physical `X_max` is selected. The metric, reciprocal kernel, angular
cancellation, and observational interfaces are unchanged.
