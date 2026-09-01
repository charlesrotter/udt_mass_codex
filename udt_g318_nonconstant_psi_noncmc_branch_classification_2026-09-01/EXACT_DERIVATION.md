# G318 exact derivation — nonconstant-conformal non-CMC branch classification

Date: 2026-09-01
Scope: positive sign-definite constant-ratio, flat marked `T^3`, diagonal-TT, one-coordinate subspace

## 1. Bounded landing

```text
NONCONSTANT_PSI_FORCES_A_POWER_LAW_NONCMC_INTERLOCK
__G317_DIRECT_FORM_IS_OBSTRUCTED
__POSITIVE_PERIODIC_TIDAL_BRANCH_EXISTS
__NO_PHYSICAL_DATA_SELECTION
```

Status before external review:
`INTERNALLY_DERIVED_AND_IMPLEMENTATION_DISTINCT_VERIFIED_BOUNDED`.

G318 frees G317's constant conformal factor in one declared separability family. The exact
interlock survives, but not unchanged: the momentum constraint forces a power relation between
mean curvature and conformal geometry. Some exponent/sign classes are obstructed, while an
`n=-2` class contains positive nonconstant periodic solutions. Those periodic witnesses have
nonzero initial Weyl tide. This is not a general non-CMC theorem or physical-data selector.

## 2. Active equation and ownership

Universal Reciprocity/DDR and both G312 premises are owner-adopted provisionally, not derived or
canonized. In their bounded regular local metric-only vacuum arena,

\[
R_{ab}=\Lambda g_{ab},\qquad d\Lambda=0.
\]

G315 supplies the physical constraints, and G316 rewrites them by the conditional conformal
method. The flat torus, diagonal TT seed, one-coordinate dependence, sign-definite `tau`, and
constant-ratio separability used here are all chosen diagnostic restrictions. The autonomous-ODE
phase portrait is imported mathematical method only.

## 3. Exact vector reorganization

Let

\[
\bar\gamma_{ij}=\delta_{ij},\qquad \psi=\psi(x)>0,
\]

\[
\bar A_{TT}^{ij}=\operatorname{diag}
(\alpha,-\alpha/2+d,-\alpha/2-d),
\qquad W=w(x)\partial_x.
\]

Put `u=w'` and

\[
v=\frac32\alpha+2u.
\]

Then

\[
\bar A_{TT}+\bar L W
=\operatorname{diag}
\left(\frac23v,-\frac13v+d,-\frac13v-d\right),
\]

\[
|\bar A_{TT}+\bar L W|^2=\frac23v^2+2d^2,
\]

and the vector constraint becomes

\[
\boxed{v'=\psi^6\tau'.}
\]

Now classify the constant-ratio separability family

\[
v=k\psi^6\tau.
\]

Substitution gives

\[
(k-1)\tau'+6k\frac{\psi'}{\psi}\tau=0.
\]

For `k != 1` and sign-definite `tau`, integration is exact:

\[
\boxed{
\tau=C\psi^n,\qquad k=\frac{n}{n+6},\qquad n\ne-6.
}
\]

Because `v` is periodic, the constant TT mean and longitudinal derivative are

\[
\boxed{
\alpha=\frac23\langle v\rangle,
\qquad
w'=\frac12\left(v-\langle v\rangle\right),
}
\]

with `w` still free up to its additive translation/conformal-Killing kernel.

## 4. Why G317 does not survive unchanged

G317's reconstructed physical form had

\[
K^i{}_j=\operatorname{diag}(\tau,q,-q).
\]

In the present notation this is `k=1`, so the vector constraint reduces to

\[
6\psi^5\psi'\tau=0.
\]

Consequently, on any interval where `psi'` and sign-definite nonzero `tau` are both present, the
unchanged G317 form is obstructed. This is not a regression of G317; its theorem assumed constant
`psi`. It shows that activating the frozen conformal degree of freedom forces the other channels
to rearrange.

## 5. Physical reconstruction and scalar equation

For the power branch,

\[
\boxed{\gamma_{ij}=\psi^4\delta_{ij},}
\]

\[
\boxed{
K^i{}_j=\operatorname{diag}
\left(
\frac{n+2}{n+6}\tau,
\frac{2}{n+6}\tau+q,
\frac{2}{n+6}\tau-q
\right),
\quad q=d\psi^{-6},\quad \tau=C\psi^n.
}
\]

The trace is exactly `tau`. The physical momentum constraint reduces to

\[
\left(\frac{n+2}{n+6}-1\right)\tau'
+\left(6\frac{n+2}{n+6}-2\right)
\frac{\psi'}{\psi}\tau=0,
\]

which vanishes identically for `tau=C psi^n`.

The spatial scalar curvature is

\[
{}^{(3)}R=-8\psi^{-5}\psi''.
\]

The direct Hamiltonian constraint and the conformal scalar equation independently reduce to

\[
\boxed{
-8\psi''
+\frac{8(n+3)}{(n+6)^2}C^2\psi^{2n+5}
-2d^2\psi^{-7}
-2\Lambda\psi^5=0.
}
\]

This is the surviving nonlinear interlock. It links the conformal geometry, curvature profile,
TT difference, and connected scalar, but it does not choose their data.

## 6. Exact periodic obstruction classes

Integrating the scalar equation around the marked periodic coordinate removes the Laplacian term.
Every remaining power of positive `psi` has a positive integral. Therefore:

- if `n<-3`, `n!=-6`, `C!=0`, and `Lambda>=0`, all surviving integrated terms have the same
  nonpositive sign and at least one is strictly negative: no positive periodic member exists;
- at `n=-3` the `C` coefficient vanishes. If `d` or nonnegative `Lambda` is nonzero, the same
  integral obstruction applies; if both vanish, `psi''=0`, so periodicity makes `psi` constant;
- `n=0` is the CMC boundary;
- for `n>-3` the sign obstruction disappears, but existence is not automatic.

These statements classify only the registered power family. Negative `Lambda`, sign-changing
`tau`, nonseparable data, and other omitted sectors can behave differently.

## 7. Positive periodic `n=-2` family

For `n=-2`,

\[
\tau=C\psi^{-2},
\qquad
K^i{}_j=\operatorname{diag}
\left(0,\frac12\tau+q,\frac12\tau-q\right),
\qquad q=d\psi^{-6},
\]

and

\[
\boxed{
\psi''=\frac{C^2}{16}\psi
-\frac{d^2}{4}\psi^{-7}
-\frac{\Lambda}{4}\psi^5.
}
\]

It has the exact first integral

\[
\boxed{
I=-4(\psi')^2+\frac{C^2}{4}\psi^2
+\frac{d^2}{3}\psi^{-6}-\frac{\Lambda}{3}\psi^6.
}
\]

Equivalently, `psi''=-V'(psi)` with

\[
V(\psi)=-\frac{C^2}{32}\psi^2
-\frac{d^2}{24}\psi^{-6}
+\frac{\Lambda}{24}\psi^6.
\]

A positive equilibrium `p` satisfies

\[
C^2p^8-4d^2-4\Lambda p^{12}=0.
\]

Its linear center frequency is

\[
\boxed{\omega^2=\frac{C^2}{4}-3d^2p^{-8}.}
\]

Thus, whenever

\[
C^2p^8>12d^2,
\qquad
\Lambda=\frac{C^2p^8-4d^2}{4p^{12}}>0,
\]

`V` has a strict local minimum. The standard one-dimensional autonomous phase portrait then gives
a neighborhood of closed positive energy curves: smooth nonconstant periodic solutions surrounding
`p`. This is a theorem about the registered ODE, not a numerical fit.

If a base orbit has natural period `P`, then

\[
\psi(x)=\Psi(\kappa x),\quad
(C,d,\Lambda)=(\kappa C_0,\kappa d_0,\kappa^2\Lambda_0),
\quad \kappa=P/(2\pi)
\]

is an exact member with marked coordinate period `2 pi`. This covariance attaches no physical
ruler: the parameters and marked period remain uncalibrated construction data.

## 8. Initial Weyl tide

For `gamma=psi^4 delta`, the mixed spatial Ricci eigenvalues are

\[
{}^{(3)}R^x{}_x=-4\psi^{-5}\psi''+4\psi^{-6}(\psi')^2,
\]

\[
{}^{(3)}R^y{}_y={}^{(3)}R^z{}_z
=-2\psi^{-5}\psi''-2\psi^{-6}(\psi')^2.
\]

Using the `n=-2` ODE, the electric Weyl tensor is

\[
\boxed{
E^i{}_j=\operatorname{diag}(E_x,-E_x/2,-E_x/2),
}
\]

\[
\boxed{
E_x=4\psi^{-6}(\psi')^2-\frac{C^2}{4}\psi^{-4}
+d^2\psi^{-12}+\frac{\Lambda}{3}
=-I\psi^{-6}+\frac43d^2\psi^{-12}.
}
\]

A direct covariant curl gives the only independent orthonormal magnetic component

\[
\boxed{
B_{\hat y\hat z}=B_{\hat z\hat y}=-4d\frac{\psi'}{\psi}\psi^{-8}.
}
\]

For `d=0`, the small center orbits lie below the zero-energy barrier and have `I>0`; hence `E_x`
is nonzero. For `d!=0`, every nonconstant orbit has nonzero magnetic tide wherever `psi'!=0`.
Therefore the registered positive periodic family is genuinely tidal. This does not prove that
all nonconstant-`psi` data in omitted sectors are tidal.

## 9. Solution-space meaning

The result is both an obstruction and an opening:

- the constant-`psi` G317 response cannot be bolted onto varying conformal geometry;
- the momentum equation makes `tau` and `psi` turn together by an exact power law in the selected
  separability family;
- the scalar equation divides the exponent/sign space into obstructed and admitted sectors;
- an admitted periodic sector exists and carries true Weyl curvature;
- `psi` orbit, `C`, `d`, `n`, `Lambda`, TT mean, and translation kernel remain unselected.

The metric and reciprocal kernel are unchanged. No physical initial data, history, topology,
population, scale, source, matter/mass law, observation, fit, or physical `X_max` is selected.
