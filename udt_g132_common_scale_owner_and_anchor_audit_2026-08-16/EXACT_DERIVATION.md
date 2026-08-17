# G132 exact derivation — common scale, pair magnitude, and observational anchors

Date: 2026-08-16

## 1. Three different scale questions

The phrase “missing common scale” had begun to cover three mathematically different questions:

1. whether the founded reciprocal transformation contains an arbitrary common factor;
2. what information is discarded by keeping only `phi_pair` from a supplied pair metric;
3. what determines the functions and global size of a complete physical metric history.

They have different answers. The first has no internal common multiplier inside the stipulated
fixed-`K` reciprocal transformation. The second is retained by `kappa_pair` or the full pair
metric. The third remains open outside conditional branches and cannot be solved by dimensional
calibration alone.

## 2. The founded reciprocal transformation has no internal common-factor freedom

Let

\[
K=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
D(\phi)=\operatorname{diag}(e^{-\phi},e^{+\phi}).
\]

The founded exact dual-pair condition is

\[
D(\phi)^T K D(\phi)=K,
\qquad \det D(\phi)=1.
\]

If a positive common factor `A` is inserted,

\[
P_A=A D(\phi),
\]

then

\[
P_A^T K P_A=A^2K.
\]

Preserving the same fixed `K` therefore requires `A^2=1`, and positivity gives

\[
\boxed{A=1}.
\]

Thus an arbitrary common multiplier is not a freedom of the exact founded reciprocal
transformation. This does **not** make `K` an owner of the physical conformal scale of a complete
metric. A common scale can enter the coframe itself, a larger complete metric configuration, or a
separate calibration; none of those values is supplied by the `K` invariance equation.

After additionally declaring the founded Lorentzian quadratic readout in the identified calibrated
clock/ruler chart, the base metric is

\[
g_{\parallel}
=-e^{-2\phi}c_E^2dt^2+e^{2\phi}dr^2,
\qquad
\det g_{\parallel}=-c_E^2.
\]

For a positive conformal rescaling,

\[
\det(\Omega^2 g_{\parallel})=-\Omega^4c_E^2.
\]

If the rescaled base is required to remain in the same calibrated founded form, with the same
identified clock/ruler coordinates and the same observed `c_E`, its determinant must again be
`-c_E^2`. Hence `Omega^4=1` and positive `Omega=1`.

This is a conditional normalization theorem inside that same declared chart/readout type. It is
not a query-independent physical-scale theorem and does not select a complete nonspherical metric
history.

## 3. G131's conformal kernel is a projection kernel

For a supplied regular calibrated pair metric, write uniquely

\[
h=-T^2(dy^0+\beta,dy^1)^2+L^2(dy^1)^2,
\]

with

\[
T=e^{\kappa-\phi},\qquad L=e^{\kappa+\phi}.
\]

Then

\[
\det h=-e^{4\kappa},
\]

\[
\kappa_{\rm pair}=\frac14\log(-\det h),
\qquad
\phi_{\rm pair}=\frac14\log\frac{-\det h}{h_{00}^2},
\qquad
\beta_{\rm pair}=\frac{h_{01}}{h_{00}}.
\]

Under `h -> Omega^2 h`,

\[
\kappa_{\rm pair}\mapsto\kappa_{\rm pair}+\log\Omega,
\qquad
\phi_{\rm pair}\mapsto\phi_{\rm pair},
\qquad
\beta_{\rm pair}\mapsto\beta_{\rm pair}.
\]

Therefore `phi_pair` and `c_eff/c_E=exp(-2 phi_pair)` discard the common magnitude exactly, while
`kappa_pair` retains it.

The triplet is not merely suggestive. It reconstructs the complete calibrated pair metric:

\[
T^2=e^{2(\kappa-\phi)},\qquad
L^2=e^{2(\kappa+\phi)},
\]

\[
h=
\begin{pmatrix}
-T^2&-T^2\beta\\
-T^2\beta&L^2-T^2\beta^2
\end{pmatrix}.
\]

Equivalently, for arbitrary regular `h`,

\[
T^2=-h_{00},\qquad
\beta=\frac{h_{01}}{h_{00}},\qquad
L^2=h_{11}-\frac{h_{01}^2}{h_{00}}.
\]

Consequently, on a supplied rank-complete calibrated pair network, retaining the complete triplets
is equivalent to retaining all pair pullbacks. G129 then reconstructs the Lorentz metric uniquely
on the covered regular region, up to the ordinary isometry/diffeomorphism identification already
declared there.

This does **not** make `kappa_pair` query-independent. It is a calibrated state of the supplied
pair realization. It shows that the complete evaluator did not lose scale; the scalar-only G131
question deliberately did.

## 4. Metric volume and screen area

In four dimensions,

\[
\operatorname{vol}_{\Omega^2g}=\Omega^4\operatorname{vol}_g.
\]

Thus a supplied physical volume density fixes the conformal representative pointwise. But the
volume form is already computed from the full metric. Supplying it independently of the conformal
class is exactly supplying the missing scale datum; it is not a selector derived from the
conformal class.

The complete metric-orchestra chart similarly contains an angular common log-area variable
`sigma`, with

\[
\det E=e^\sigma,\qquad \sqrt{|\det g|}=e^\sigma
\]

in its dimension-matched coordinates. That variable is a genuine configuration direction, not a
gauge direction derived from Reciprocity. The existing kinematic chart does not select its
history.

## 5. Conditional areal-radius closure

On an identified spherical symmetry orbit,

\[
\mathcal A_{S^2}=4\pi R^2,
\qquad
R=\sqrt{\mathcal A_{S^2}/4\pi}.
\]

If `Omega` is constant on each orbit, then

\[
\widetilde{\mathcal A}_{S^2}=\Omega^2\mathcal A_{S^2},
\qquad
\widetilde R=\Omega R.
\]

Therefore an independently identified and calibrated orbit area supplies a scale datum on that
orbit. In the founded central-spherical metric

\[
ds^2=-e^{-2\phi}c_E^2dt^2+e^{2\phi}dr^2+r^2d\Omega_2^2,
\]

the angular coefficient defines `r` to be the areal radius of that metric. If a second conformally
related metric is additionally required to share the same identified and independently calibrated
orbit area or numerical areal label, it must obey `Omega^2 r^2=r^2`, hence `Omega=1` for `r>0`.
The shared calibrated area is the extra datum; writing an areal coordinate by itself does not
derive it from the conformal class.

This is strong but branch-conditional. A generic nonspherical metric does not supply `SO(3)`
orbits or a universal areal radius. The G119 screen theorem gives an analogous exact area readout
for its supplied central-spherical point-observer query; it is not a universal complete-history
scale datum.

## 6. What `c_E` and `G_obs` can calibrate

Use dimensions

\[
[c_E]=LT^{-1},\qquad [G_{\rm obs}]=L^3M^{-1}T^{-2}.
\]

There is no monomial `c_E^a G_obs^b` having dimensions of length. Mass neutrality requires
`b=0`; time neutrality then requires `a=0`; the length exponent is consequently zero.

Adding one further dimensionful observation changes the result.

For mass `M`, mass density `rho`, and energy density `epsilon`,

\[
[M]=M,\qquad [\rho]=ML^{-3},\qquad [\epsilon]=ML^{-1}T^{-2}.
\]

The unique monomial exponent solutions are

\[
\boxed{\ell_M=\frac{G_{\rm obs}M}{c_E^2}},
\]

\[
\boxed{\ell_\rho=\frac{c_E}{\sqrt{G_{\rm obs}\rho}}},
\]

\[
\boxed{\ell_\epsilon=\frac{c_E^2}{\sqrt{G_{\rm obs}\epsilon}}}.
\]

These are dimensional calibrators, not UDT equations. A native or explicitly conditional bridge
must still state which metric length, area, volume, boundary, or profile parameter is related to
one of them.

## 7. Why one or two anchors do not fix an arbitrary local field

For any real `a`, define

\[
\Omega_a(x)=\exp\bigl[a x^2(x-1)^2\bigr].
\]

Every member satisfies

\[
\Omega_a(0)=\Omega_a(1)=1,
\]

but

\[
\Omega_a(1/2)=e^{a/16}.
\]

Thus two exact point calibrations do not determine an arbitrary smooth conformal field. More
generally, finitely many scalar anchors can determine finitely many parameters only after a native
history equation, global completion rule, or explicitly declared finite-dimensional model has
reduced the functional freedom.

This does not weaken the observational-anchor proposal. It locates its proper role: observations
can calibrate or falsify a derived finite-dimensional history family; they cannot replace the law
that defines that family.

## 8. Type-separated landing

The strongest exact conclusion is

\[
\boxed{
\begin{aligned}
&\text{fixed-}K\text{ reciprocal transformation: no internal common multiplier;}\\
&\text{declared calibrated base readout: determinant normalized conditionally;}\\
&\text{terminal }\phi_{\rm pair}\text{ alone: common magnitude discarded;}\\
&(\kappa_{\rm pair},\phi_{\rm pair},\beta_{\rm pair})\text{: complete pair metric retained;}\\
&\text{independently calibrated spherical areal data: conditional scale datum;}\\
&\text{general complete history and its physical query network: still open.}
\end{aligned}}
\]

G131 therefore does not support reviving strong CSN or calling UDT physically scale-free. It
classifies the kernel of one reduced readout. `c_E` and `G_obs` remain legitimate observational
anchors; a mass/density/energy datum can form a dimensional length after a lawful bridge is supplied.
