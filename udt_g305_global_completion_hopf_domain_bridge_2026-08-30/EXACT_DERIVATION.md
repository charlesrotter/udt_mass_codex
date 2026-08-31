# G305 exact derivation — global completion and Hopf-domain bridge

Date: 2026-08-30
Grade: `EXTERNALLY_VERIFIED_AFTER_PREREGISTERED_EVIDENCE_REPAIRS`

## Bounded landing

```text
POSITIVE_STANDARD_GLOBAL_COMPLETION_NATIVELY_SUPPLIES_COMPACT_S3_HOPF_DOMAIN
__STATIC_ZERO_IS_OBSERVER_HORIZON_NOT_MATERIAL_BOUNDARY
__EXPLICIT_HOPF_CLASS_PERSISTS_KINEMATICALLY_AND_IS_SCALE_BLIND
__TARGET_SECTION_ACTION_DYNAMICS_HISTORY_MAGNITUDE_MASS_AND_XMAX_REMAIN_OPEN
```

This is landing A from the pushed preregistration. It is a conditional theorem inside the G304
smooth-center constant-sector candidate family. It is not a UDT field equation or a selected
history.

## 1. Frozen G304 family

G304 left

\[
ds^2=-f(r)d\tau^2+\frac{dr^2}{f(r)}+r^2d\Omega_2^2,
\qquad
f(r)=1-\frac{R_0}{12}r^2,
\qquad d\tau=c_Edt,
\]

after smooth-center regularity removed the `b/r` mode. Set

\[
K=\frac{R_0}{12}.
\]

No value or sign is inserted below. Every sign is classified.

## 2. Positive sector: the static zero is not the end of the geometry

For `R0>0`, let `X=1/sqrt(K)=sqrt(12/R0)`. In five-dimensional flat space with signature
`(-++++)`, define

\[
\begin{aligned}
Y_0&=\sqrt{X^2-r^2}\sinh(\tau/X),\\
(Y_1,Y_2,Y_3)&=r\,\mathbf n(\theta,\varphi),\\
Y_4&=\sqrt{X^2-r^2}\cosh(\tau/X).
\end{aligned}
\]

The ambient constraint and induced metric are exactly

\[
-Y_0^2+Y_1^2+Y_2^2+Y_3^2+Y_4^2=X^2,
\]

\[
ds^2=-\left(1-\frac{r^2}{X^2}\right)d\tau^2
+\frac{dr^2}{1-r^2/X^2}+r^2d\Omega_2^2.
\]

The same connected hyperboloid has regular global coordinates

\[
Y_0=X\sinh(T/X),
\]

\[
(Y_1,Y_2,Y_3,Y_4)
=X\cosh(T/X)\,\mathbf\Omega_3,
\qquad \mathbf\Omega_3\in S^3,
\]

with induced metric

\[
\boxed{
ds^2=-dT^2+X^2\cosh^2(T/X)d\Omega_3^2.
}
\]

The static and global charts overlap through

\[
r=X\cosh(T/X)\sin\psi,
\qquad
\tanh(\tau/X)=\frac{\tanh(T/X)}{\cos\psi}.
\]

The static condition `r<X` is `Y_4^2>Y_0^2`; `r=X` is its null equality surface. The induced
global metric is regular there and continues to regions outside the chosen observer's static
chart. Therefore the G304 zero is a causal observer horizon in this completion, not a curvature
singularity, material wall, or edge of the complete geometry.

Every constant-`T` slice is an intrinsic compact `S3` without boundary. This conclusion uses the
standard connected simply connected completion stated in the preregistration. It does not classify
all possible quotients or topology-changing histories.

## 3. Zero and negative sectors

For `R0=0`, the standard completion is flat spacetime with spatial slices `R3`.

For `R0<0`, let `L=sqrt(-12/R0)`. In flat ambient signature `(--+++)`, set

\[
\begin{aligned}
Y_{-1}&=\sqrt{L^2+r^2}\cos(\tau/L),\\
Y_0&=\sqrt{L^2+r^2}\sin(\tau/L),\\
(Y_1,Y_2,Y_3)&=r\,\mathbf n.
\end{aligned}
\]

Then

\[
-Y_{-1}^2-Y_0^2+Y_1^2+Y_2^2+Y_3^2=-L^2
\]

and the induced metric is exactly

\[
ds^2=-\left(1+\frac{r^2}{L^2}\right)d\tau^2
+\frac{dr^2}{1+r^2/L^2}+r^2d\Omega_2^2.
\]

Writing `r=L sinh(rho)` gives

\[
ds^2=-\cosh^2\rho\,d\tau^2
+L^2\left(d\rho^2+\sinh^2\rho\,d\Omega_2^2\right).
\]

The ambient hyperboloid has periodic `tau`; the causally relevant standard cover unwraps it. Its
spatial slice is `H3`, diffeomorphic to `R3`, and is noncompact. This causal-cover choice is explicit
and is not derived from the reciprocal kernel.

Thus the bounded topology census is

| Sector | Standard spatial slice | Compact without boundary | Ordinary map class to `S2` |
|---|---|---:|---|
| `R0>0` | `S3` | yes | `[S3,S2]=Z` |
| `R0=0` | `R3` | no | trivial on the contractible domain |
| `R0<0` causal cover | `H3 ~= R3` | no | trivial on the contractible domain |

The zero/negative sectors can acquire Hopf classes only after an additional asymptotic/basepoint
condition permits one-point compactification `R3 union {infinity} ~= S3`, or after some other global
quotient/boundary premise. That is exactly the kind of supplied boundary used by the historical
fixed-box Hopfion. It is not metric-owned in the bounded standard completion.

## 4. Exact nontrivial Hopf witness on the positive slice

Use Hopf coordinates on the unit `S3`:

\[
z_1=\cos\eta\,e^{i\xi_1},
\qquad
z_2=\sin\eta\,e^{i\xi_2},
\]

with `0<=eta<=pi/2` and both angles of period `2 pi`. The explicit map

\[
\mathbf h(z_1,z_2)=
\left(
\sin 2\eta\cos(\xi_1-\xi_2),
\sin 2\eta\sin(\xi_1-\xi_2),
\cos 2\eta
\right)
\]

satisfies `|h|^2=1`. With

\[
A=\cos^2\eta\,d\xi_1+\sin^2\eta\,d\xi_2,
\]

the frozen orientation `deta wedge dxi1 wedge dxi2` gives

\[
A\wedge dA=-\sin(2\eta)\,
d\eta\wedge d\xi_1\wedge d\xi_2,
\]

and therefore

\[
\boxed{
H=\frac{1}{4\pi^2}\int_{S^3}A\wedge dA=-1.
}
\]

The sign reverses with orientation; nontriviality does not. Neither `X` nor `T` appears in this
integer. The same coordinate map can be carried through the explicit product slicing
`R_T x S3`, so its class is constant while the spatial radius

\[
a(T)=X\cosh(T/X)
\]

changes. This is exact kinematic persistence of a supplied map on a regular fixed-topology
continuation. It is not an equation saying that Nature populates the map, a dynamical conservation
law, or a stability theorem.

## 5. What the existing null/screen machinery hears

Every member of the centered family is constant curvature,

\[
R_{abcd}=K(g_{ac}g_{bd}-g_{ad}g_{bc}).
\]

For a null vector `k` and an orthonormal screen vector `e` with `g(k,e)=0`,

\[
R(e,k,e,k)=K\bigl(g(e,e)g(k,k)-g(e,k)^2\bigr)=0,
\]

and `R_ab k^a k^b=0`. The local null optical tidal matrix therefore does not distinguish the three
constant sectors. Likewise the full celestial direction screen remains `TS2` with Euler number

\[
\frac{1}{2\pi}\int_{S^2}F=2
\]

for every sign, including flat spacetime. G290 holonomy can evaluate supplied representative-metric
curvature on suitable loops, but its identities set neither sign nor magnitude. The new
discriminator is the global compact domain of the positive standard completion, not a hidden local
null-screen residual.

## 6. Exact gain and remaining gap

The positive completion removes one historical scaffold:

| Historical Hopf prerequisite | G305 status |
|---|---|
| compact spatial `S3` domain | `DERIVED_CONDITIONAL` in positive standard completion |
| artificial box and collapsed outer boundary | not needed in that sector |
| existence of nontrivial `S3 -> S2` classes | `DERIVED` mathematically |
| physical map/section | `OPEN` |
| fixed physical `S2` target | `OPEN` |
| frame-gauge-independent charge for the actual UDT field | `OPEN` |
| covariant action and time-live dynamics | `OPEN` |
| stability and backreaction | `OPEN` |
| physical history selection | `OPEN` |
| curvature magnitude, mass, or physical `X_max` | `OPEN` |

This is genuine consilience with G304: the same positive sector conditionally favored by the
working finite-ceiling premise is also the only member of the bounded standard-completion census
that supplies the old Hopf construction's compact domain without an extra boundary. It is not an
independent selection law, because both statements are consequences of the same positive global
geometry.

## 7. Evidence

- preregistration committed and pushed at `fc0ee889` before outcome files existed;
- 77 exact production assertions from direct ambient pullbacks, overlap identities, the Hopf map,
  normalized Hopf integral, null optical contraction, and sky Euler integral;
- 687 independent checks using no production import, including 24 finite-difference pullback cases,
  ambient constraints, positive chart overlap, negative global pullback/relation, explicit topology
  witnesses, maximum metric error below `3.6e-9`, and an independent midpoint Hopf integral;
- ten hostile cases making 11 direct computed-evidence or required-premise mutations, with named
  failures and a corrupted-baseline control;
- all three signs covered in the frozen centered standard-completion scope;
- no field equation, action, source, matter model, mass law, observation, fit, scale value,
  physical `X_max`, old fixed boundary, or protected package used.

Final external R3-completion follow-up returned `R3_COMPLETION_ACCEPTED`. The evidence repair changed
no metric, kernel, topology census, premise grade, or bounded scientific conclusion.
