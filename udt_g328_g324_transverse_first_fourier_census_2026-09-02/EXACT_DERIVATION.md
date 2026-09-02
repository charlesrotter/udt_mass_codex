# G328 exact derivation — primitive transverse Fourier census

Date: 2026-09-02
Status: `INTERNAL_VERIFIED_PENDING_EXTERNAL_REVIEW`

## 1. Bounded question and ownership

On a fixed registered G324 quotient, let the primitive Fourier covector point along the expanding
`y` circle. Classify the complete first variation of

\[
S_{ab}:=R_{ab}-\frac14R g_{ab}=0
\tag{1}
\]

modulo all smooth quotient-periodic infinitesimal diffeomorphisms in that eigenspace.

The background is

\[
g_0=-dT^2+a^2dX^2+b^2(dy^2+dz^2),
\qquad
a=C_1T^{-1/3},\quad b=C_\perp T^{2/3}.
\tag{2}
\]

Equation (1) is active only through Charles's owner-provisional Universal Reciprocity / DDR and
G312 premises. It is not rederived or promoted here. G328 changes neither the UDT metric nor the
reciprocal kernel.

## 2. Full perturbation and parity split

Let `k=2 pi/L_y>0` and use `exp(i k y)` as shorthand for the two real phases. The complete
ten-component perturbation splits under `z -> -z` into

\[
h_{03}=bN,\qquad h_{13}=abH_o,\qquad h_{23}=b^2Q
\tag{3}
\]

in the odd block, and

\[
\begin{aligned}
h_{00}&=-2A,&h_{01}&=aB,&h_{02}&=bC,\\
h_{11}&=2a^2U,&h_{12}&=abV,&h_{22}&=2b^2W,&h_{33}&=2b^2Z
\end{aligned}
\tag{4}
\]

in the even block. Every displayed amplitude is a function of `T`, and the common Fourier factor
is suppressed. The two blocks contain all `3+7=10` symmetric metric components. Production
directly differentiates all spacetime Ricci components in both blocks. The independent route uses
the spatial Gauss--Codazzi equations and reconstructs the constraints separately.

## 3. Why the connected scalar disappears only for nonzero modes

On a Ricci-flat background the exact first-variation Bianchi identity is

\[
\nabla^a\delta S_{ab}=\frac14\nabla_b\delta R.
\tag{5}
\]

Both symbolic routes verify (5) component by component. On shell, the `y` component gives

\[
ik\,\delta R=0.
\tag{6}
\]

Because `k>0`, `delta R=0`, and (1) becomes `delta R_ab=0` in this tile. This conclusion must not
be transferred to `k=0`: G325's connected constant-scalar mode remains intact.

## 4. Complete periodic gauge image

For

\[
\xi=(P,G_X,G_y,G_z)e^{iky},
\tag{7}
\]

the exact Lie derivative of (2) gives

\[
\begin{array}{lll}
A=P',&B=aG_X',&C=bG_y'-ikP/b,\\
U=-P/(3T),&V=ik(a/b)G_X,&W=2P/(3T)+ikG_y,\\
Z=2P/(3T),&N=bG_z',&Q=ikG_z,
\end{array}
\tag{8}
\]

while `H_o` has zero gauge image. The even combination

\[
\boxed{H_e=2U+Z}
\tag{9}
\]

also has zero gauge image.

Every perturbation can be put in synchronous gauge on a compact interval inside `T>0` by solving

\[
P'=A,\qquad G_X'=B/a,\qquad G_z'=N/b,
\qquad G_y'=C/b+ikP/b^2.
\tag{10}
\]

All coefficients are smooth there. The integration constants are retained and audited below; no
solution is lost by (10).

## 5. Odd block

Direct linearization gives the momentum constraint

\[
i bQ'+kN=0
\tag{11}
\]

and the gauge-invariant master equation

\[
\boxed{
H_o''+\frac1T H_o'
+\left(\nu^2T^{-4/3}-\frac1{T^2}\right)H_o=0,
\qquad \nu=\frac{k}{C_\perp}.
}
\tag{12}
\]

In synchronous gauge `N=0`, (11) makes `Q` constant. The remaining odd equation is then
identically satisfied. A constant residual `G_z` shifts `Q` by `ikG_z` and removes it. Therefore
(12) is the complete odd physical quotient; it is not a tensor ansatz imposed before solving.

## 6. Even vector block

The `B,V` equations contain the exact constraint

\[
TV'+V-\frac{ikT^{1/3}}{C_\perp}B=0.
\tag{13}
\]

In synchronous gauge `B=0`, this gives `V=c_X/T`. The other equation is then redundant. A
constant residual `G_X` produces exactly this solution and removes it. The block carries no
physical mode.

## 7. Even scalar/tensor block

Set `A=C=0` by (10). The momentum constraint is

\[
U'+Z'-\frac UT=0.
\tag{14}
\]

Using (9), equation (14) becomes

\[
U'+\frac UT=H_e'.
\tag{15}
\]

The `XX` equation determines

\[
W'=3TU''+3U'-\frac UT+3\nu^2T^{-1/3}U.
\tag{16}
\]

After (14)--(16), the `zz` equation reduces exactly to

\[
\boxed{
H_e''+\frac1T H_e'+\nu^2T^{-4/3}H_e=0.
}
\tag{17}
\]

Calling the left side `E`, the remaining independent-looking time and longitudinal equations are
respectively `3T E'+4E` and `3T E'+5E`. Thus they propagate rather than add data.

For a supplied `H_e`, equation (15) has one homogeneous constant `U=c_U/T`, and (16) has one
further constant. At `H_e=0` their exact form is

\[
U=\frac{c_U}{T},\qquad
W=-\frac{2c_U}{T}-9\nu^2c_UT^{-1/3}+c_W.
\tag{18}
\]

These are precisely the residual synchronous `P,G_y` gauge images. Consequently (17) is the
complete even physical quotient.

## 8. Exact representatives and curvature witnesses

One completely fixed representative of the even family is

\[
A=-3H_e,\quad
C=-\frac{3iC_\perp T^{2/3}}{k}H_e',\quad
U=H_e,\quad Z=-H_e,
\quad B=V=W=0.
\tag{19}
\]

For the odd family take `N=Q=0` with only `h_13=abH_o`. Production substitutes (19) and the odd
representative into every one of the sixteen matrix positions of `delta R_ab`; all vanish exactly
on (12) or (17). The gauge conditions `U+Z=W=V=Q=0` have an invertible residual-gauge matrix for
`k>0`, so these representatives have no same-mode gauge remainder.

There are also direct intrinsic-curvature witnesses. Let `delta Ric^(3)` be the first variation of
the Ricci tensor of the constant-`T` spatial slice. Exact differentiation gives

\[
\boxed{
2\frac{\delta R^{(3)}_{XX}}{a^2}
+\frac{\delta R^{(3)}_{zz}}{b^2}
=\frac{k^2}{b^2}H_e
}
\tag{20}
\]

and

\[
\boxed{
\frac{\delta R^{(3)}_{Xz}}{ab}
=\frac{k^2}{2b^2}H_o.
}
\tag{21}
\]

The right sides use the gauge invariants (9) and `H_o`; hence the displayed curvature responses
cannot be periodic gauge images.

## 9. Exact time bases and endpoint classification

Set

\[
\zeta=3\nu T^{1/3}.
\tag{22}
\]

Equations (17) and (12) become Bessel equations of order zero and three:

\[
H_e=A_eJ_0(\zeta)+B_eY_0(\zeta),
\tag{23}
\]

\[
H_o=A_oJ_3(\zeta)+B_oY_3(\zeta).
\tag{24}
\]

Their `T`-Wronskian is

\[
W_T=\frac{2}{3\pi T}\ne0.
\tag{25}
\]

No branch is discarded. As `T -> 0+`, the even branches are finite and logarithmic, while

\[
J_3(\zeta)\sim\frac9{16}\nu^3T,
\qquad
Y_3(\zeta)\sim-\frac{16}{27\pi\nu^3}T^{-1}.
\tag{26}
\]

As `T -> infinity`, all four branches oscillate with relative amplitude proportional to
`zeta^(-1/2)=T^(-1/6)`. This is a mode-amplitude classification, not an endpoint boundary rule or
a full stability estimate.

## 10. Count, extension, and landing

There are two masters, two time constants per master, and two real spatial phases:

\[
\boxed{2\times2\times2=8}
\tag{27}
\]

real physical constants in the primitive transverse eigenspace, plus four arbitrary gauge
functions before quotienting. The calculation depends only on `k>0`, so replacing `k` by any
nonzero transverse harmonic leaves the classification form unchanged.

The preregistered landing is

```text
PRIMITIVE_TRANSVERSE_FOURIER_SECTOR_CLOSES_MODULO_PERIODIC_GAUGE
__TWO_PHYSICAL_MODE_FAMILIES__EXACT_BRANCH_CLASSIFICATION
__NO_FULL_STABILITY_CLAIM
```

Still open: oblique covectors, simultaneous modes, a uniform estimate over all harmonics and the
whole MGHD, nonlinear coupling and stability, endpoint admissibility, other topologies and
backgrounds, physical occupancy, observations, matter/mass, scale, history selection, and physical
`X_max`. No metric, reciprocal-kernel, angular-sector, or field-equation formula changed.
