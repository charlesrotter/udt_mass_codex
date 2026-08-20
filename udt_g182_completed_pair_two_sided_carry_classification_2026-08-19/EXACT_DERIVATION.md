# G182 exact derivation — completed-pair two-sided carry

Date: 2026-08-19

## 1. Domain and typing

Take two supplied one-sided completed pair families whose finite endpoints are to be identified.
On each punctured side,

\[
h_\pm=-T_\pm^2(d\tau_\pm+B_\pm dx_\pm)^2+T_\pm^{-2}dx_\pm^2,
\qquad x_\pm>0,
\]

where `x_±=0` is the approached endpoint. G181 supplies the bounded antecedent

\[
T_\pm\to T_{\pm0}\in(0,\infty),
\qquad B_\pm\to B_{\pm0}\in\mathbb R.
\]

A two-sided question additionally needs a supplied seam identification: common endpoint, common
clock unit and time orientation, clock-origin translation, and a relative ruler orientation. These
are carry data, not a new metric coefficient. The main theorem is stated in the resulting retained
calibration. A smooth clock shear would change the event-pairing calibration and hence `B`; it is a
different supplied query, not an invisible deletion of the shift.

No branch, event, path, or global realization is selected here.

## 2. One signed completed ruler

Choose outward one-sided rulers and define

\[
s=-x_-\quad(s<0),
\qquad
s=x_+\quad(s>0).
\]

With the same carried clock coordinate on both sides, the left coefficients in the signed chart are

\[
T_L(s)=T_-(-s),
\qquad
B_L(s)=-B_-(-s),
\]

while

\[
T_R(s)=T_+(s),
\qquad
B_R(s)=B_+(s).
\]

Therefore their raw outward-coordinate jets obey

\[
\boxed{T_+^{(j)}(0)=(-1)^jT_-^{(j)}(0)},
\]

\[
\boxed{B_+^{(j)}(0)=(-1)^{j+1}B_-^{(j)}(0)}.
\]

The extra sign for `B` comes from the directed ruler one-form. A time-orientation reversal on one
side contributes one further sign to the carried shift. Physical same-time-orientation carry uses
the displayed law. A constant clock-origin translation changes nothing.

## 3. Necessary and sufficient metric matching theorem

In the common signed chart,

\[
h_{00}=-T^2,
\qquad
h_{0s}=-T^2B,
\qquad
h_{ss}=T^{-2}-T^2B^2.
\]

The forward map `(T,B) -> h` is smooth for `T>0`. On the determinant-minus-one Lorentzian stratum
its inverse is

\[
\boxed{T=\sqrt{-h_{00}}},
\qquad
\boxed{B=\frac{h_{0s}}{h_{00}}}.
\]

It follows immediately that, for every finite nonnegative integer `k`,

\[
\boxed{
h_L\text{ and }h_R\text{ form one }C^k\text{ completed pair metric}
\iff
j_0^k(T_L,B_L)=j_0^k(T_R,B_R).
}
\]

Equality of every one-sided jet gives the `C^infinity` version. The limiting determinant remains
`-1`, so the joined metric is nondegenerate and Lorentzian.

This theorem is in the supplied carried calibration. If the branch clocks have not been identified,
the statement has not yet been typed. If an arbitrary domain shear is allowed, it can regrade `B`,
but then it changes the calibrated event pairing rather than proving carry of the original pair.

## 4. Scalar carry is strictly weaker

The completed reciprocal scalar is

\[
\Phi=-\log T.
\]

Since `T>0`, `T -> Phi` is a smooth bijection. Thus

\[
\boxed{\Phi\text{ joins }C^k\iff T\text{ joins }C^k.}
\]

It says nothing about `B`. For example, `T_L=T_R=1`, `B_L=0`, and `B_R=1` give the same
`Phi=0` on both sides while the metric coefficients jump. Reciprocal-depth carry is therefore not
full pair-metric carry.

## 5. Pair-metric carry is strictly weaker than immersion carry

Let a supplied ambient coframe and pair tangent be

\[
V=E(F)J,
\qquad
h=V^T\eta_4V.
\]

The Gram map `V -> h` is not injective. Ambient Lorentz transformations, including ordinary screen
rotations, can change `V` while preserving `h`. Consequently a perfectly smooth intrinsic pair
metric does not determine how the realized pair surface passes through the seam.

In a common smooth ambient chart, a piecewise pair map is `C^k` exactly when its endpoint values and
all coordinate derivatives through order `k` agree. Equivalently, after the endpoint value is
matched, its full tangent `J=dF` must have matching jets through order `k-1`. With a common smooth
invertible ambient coframe, the same information is carried by the jets of `V=EJ`.

Thus for `k>=1`,

\[
\boxed{
F\text{ joins }C^k
\iff
F_L(0)=F_R(0)
\text{ and }
j_0^{k-1}V_L=j_0^{k-1}V_R
}
\]

in the supplied common chart/coframe. The equivalent invariant formulation uses the metric's
Levi-Civita covariant tangent jets. This is a matching test on supplied germs, not a path law.

## 6. Exact flat counterexamples

In Minkowski space take

\[
F(\tau,s)=(\tau,X(s),Y(s),0).
\]

Every unit-speed spatial curve gives

\[
F^*g=-d\tau^2+ds^2.
\]

Three different failures survive this identical completed metric:

1. **Cusp:** left tangent `(1,0)`, right tangent `(-1,0)`. The map is continuous but not `C^1`.
2. **Direction rotation:** left tangent `(1,0)`, right tangent `(0,1)`. Again the metric is unchanged
   and the map is not `C^1`.
3. **Higher-jet mismatch:** use the straight line on the left and, on the right,

   \[
   X(s)=\frac{\sin(\kappa s)}{\kappa},
   \qquad
   Y(s)=\frac{1-\cos(\kappa s)}{\kappa}.
   \]

   Position and tangent match at zero, so the joined map is `C^1`, but the right acceleration is
   `(0,kappa)` while the left acceleration is zero. It is not `C^2`. Both induced metrics are
   exactly flat to all orders.

These examples prove that no scalar or intrinsic two-metric condition can replace full germ jets.

## 7. Primary spherical tangent and stall parity

For the time-orthogonal primary family,

\[
m^2=v^2+e^{-2\phi}r^2b^2.
\]

This is the squared magnitude of the complete spatial pair tangent in the completed density. It does
not retain its radial/angular direction. Equal `m` values can arise from different `(v,b)` vectors,
so two-sided tangent carry requires equality of the normalized full tangent, not only equality of
its quadratic magnitude.

The G181 radial stall admits an exact two-sided parity classification. Set `phi=0` and

\[
r(q)=r_0+a q^p,
\qquad a\ne0,
\qquad p\ge2.
\]

Then

\[
m=|ap|\,|q|^{p-1},
\qquad
s(q)=|a|\,\operatorname{sgn}(q)|q|^p.
\]

If `p` is odd,

\[
r=r_0+\operatorname{sgn}(a)s,
\]

so the stall is removable through the two-sided completed immersion. If `p` is even,

\[
r=r_0+\operatorname{sgn}(a)|s|,
\]

so the completed pair metric is still exactly flat but the radial realization has a cusp. Hence
one-sided tape removal plus pair-metric carry does not decide two-sided immersion carry; the missing
bit is the carried tangent direction already contained in the complete germ.

## 8. Landing and ceiling

```text
TWO_SIDED_PAIR_METRIC_CARRY_CLASSIFIED__FULL_GERM_JETS_REQUIRED_FOR_IMMERSION_CARRY
```

G182 supplies a necessary-and-sufficient matching theorem for two **supplied** completed branches in
one supplied carried calibration. It sharply separates scalar, intrinsic-metric, and full-immersion
carry. It does not select branches or events, identify a physical singularity, or cover null,
cut/focal, topology-changing, winding, global-completion, `X_max`, observational, dynamical, action,
source, matter, bootstrap, or signalling questions.
