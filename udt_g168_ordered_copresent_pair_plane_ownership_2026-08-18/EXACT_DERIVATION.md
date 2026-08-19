# G168 exact derivation — the local pair plane is the one-jet of the relation

Date: 2026-08-18

## 1. Exact type order

The bounded construction is

```text
local ordered co-present positional-comparison germ (u_A,s_AB)
+ primary UDT metric g
    -> orthogonal ruler r_AB
    -> local Lorentzian pair plane E_AB
    -> G167 blocks Y,Z
    -> complete pullback h_AB
    -> terminal reciprocal readout.
```

It is not

```text
two observer names -> metric-selected path -> externally attached kernel.
```

The local comparison germ is the one-jet needed to apply a metric: a calibrated future timelike
clock tangent (u_A\in T_pM) and a nonzero tangent (s_{AB}\in T_pM) representing the local
ordered positional variation toward B. It is a local differential datum of the relation, not a
curve between separated endpoints.

The founding reciprocal algebra does not manufacture this germ from two names. Its ownership is a
typing clarification of a **completed positional comparison**, not a new dynamics or path law.

## 2. Unique clock-orthogonal ruler

Let (g(u_A,u_A)<0). Among all representatives in the affine line

\[
s_{AB}+\operatorname{span}(u_A),
\]

there is exactly one clock-orthogonal vector:

\[
\boxed{
r_{AB}=s_{AB}-
\frac{g(u_A,s_{AB})}{g(u_A,u_A)}u_A .
}
\]

Indeed,

\[
g(u_A,r_{AB})=0.
\]

If (r'=s_{AB}+a u_A) is also orthogonal to (u_A), then

\[
0=g(u_A,s_{AB})+a g(u_A,u_A),
\]

so (a=-g(u_A,s_{AB})/g(u_A,u_A)). The ruler is therefore unique.

Because a Lorentzian metric of index one is positive definite on (u_A^\perp), every nonzero
(r_{AB}\in u_A^\perp) is spacelike. Hence

\[
\boxed{
E_{AB}=\operatorname{span}\{u_A,r_{AB}\}
      =\operatorname{span}\{u_A,s_{AB}\}
}
\]

is a nondegenerate Lorentzian two-plane. Its orthogonal complement is a positive two-dimensional
screen.

Writing

\[
U=g(u_A,u_A)<0,
\quad G=g(u_A,s_{AB}),
\quad S=g(s_{AB},s_{AB}),
\]

gives

\[
g(r_{AB},r_{AB})=S-\frac{G^2}{U}>0.
\]

In the raw basis ((u_A,s_{AB})),

\[
h=\begin{pmatrix}U&G\\G&S\end{pmatrix},
\qquad
\det h=U\left(S-\frac{G^2}{U}\right)<0.
\]

In the orthogonal basis ((u_A,r_{AB})), the same plane metric is diagonal. No ambient plane
selector, path, curvature eigenplane, or independent screen is required.

## 3. The primary metric determines all coefficients after the germ is supplied

For

\[
g=-c_E^2e^{-2\phi}dt^2+e^{2\phi}dr^2
  +r^2d\theta^2+r^2\sin^2\theta\,d\varphi^2,
\]

write the two germ tangents as columns of (J=(u_A,s_{AB})). Their base and angular components are

\[
Y=
\begin{pmatrix}
u^t&s^t\\
u^r&s^r
\end{pmatrix},
\qquad
Z=
\begin{pmatrix}
u^\theta&s^\theta\\
u^\varphi&s^\varphi
\end{pmatrix}.
\]

Therefore the G167 pullback is not missing another local assembly rule:

\[
\boxed{
h=Y^TB^T\eta_2BY+Z^TQ^TQZ,
}
\]

with metric-owned

\[
B=\operatorname{diag}(c_Ee^{-\phi},e^\phi),
\qquad
Q=\operatorname{diag}(r,r\sin\theta).
\]

Once ((u_A,s_{AB})) is supplied, (Y) and (Z) are simply its coordinate components. They are
not four additional physical functions.

A nonradial separation has nonzero angular entries in (Z), so the angular Gram term enters before
the terminal reciprocal readout. A central radial separation has (Z=0); in that special case its
scalar kernel is radial while angular response remains in the screen/Jacobi channels.

Under an angular coordinate change with Jacobian (K),

\[
Z\mapsto KZ,
\qquad
q_{S^2}\mapsto K^{-T}q_{S^2}K^{-1},
\]

and (Z^Tq_{S^2}Z) is unchanged. Positive rescaling of the raw separation tangent preserves its
line and normalized ruler direction. Pair-metric components transform covariantly; a terminal
readout remains tied to its declared calibration.

## 4. Exact rational witness

Take

\[
g=\operatorname{diag}\left(-\frac14,4,9,\frac{144}{25}\right),
\quad
u=(2,0,0,0),
\quad
s=\left(1,\frac12,\frac13,\frac14\right).
\]

Then

\[
g(u,u)=-1,
\qquad
g(u,s)=-\frac12,
\]

and the unique orthogonal ruler is

\[
r=\left(0,\frac12,\frac13,\frac14\right),
\qquad
g(r,r)=\frac{59}{25}.
\]

The raw and orthogonal pair metrics are

\[
h_{(u,s)}=
\begin{pmatrix}
-1&-1/2\\
-1/2&211/100
\end{pmatrix},
\qquad
h_{(u,r)}=
\begin{pmatrix}
-1&0\\
0&59/25
\end{pmatrix},
\]

and both have determinant (-59/25).

With

\[
B=\operatorname{diag}(1/2,2),
\quad Q=\operatorname{diag}(3,12/5),
\]

the germ supplies

\[
Y=\begin{pmatrix}2&1\\0&1/2\end{pmatrix},
\qquad
Z=\begin{pmatrix}0&1/3\\0&1/4\end{pmatrix},
\]

and the G167 block formula returns (h_{(u,s)}) exactly. Removing (Z) changes the pair metric.

## 5. Why bare observer labels still do not own the plane

In flat four-dimensional spacetime let

\[
A(\tau)=(\tau,0,0,0),
\qquad
B(\tau)=(\tau,1,0,0).
\]

For every real (a), the smooth timelike surface

\[
F_a(\tau,\sigma)
=\bigl(\tau,\sigma,a\sigma(1-\sigma),0\bigr),
\qquad 0\le\sigma\le1,
\]

has exactly the same boundary observers and the same boundary event pairing:

\[
F_a(\tau,0)=A(\tau),
\qquad
F_a(\tau,1)=B(\tau).
\]

But at A its separation tangent is

\[
\partial_\sigma F_a|_{\sigma=0}=(0,1,a,0).
\]

The planes for (a=0) and (a=1) are different. The induced metric remains Lorentzian:

\[
F_a^*\eta=-d\tau^2+
\left[1+a^2(1-2\sigma)^2\right]d\sigma^2.
\]

Therefore even observer labels plus a fixed boundary event pairing do not select a surface germ.
The local germ is the smallest datum that closes the local plane calculation. Supplying it is much
less than supplying an entire path or surface.

## 6. Reversal, coincidence, and relative motion

### Local orientation reversal

Inside one tangent space, (r_{AB}\mapsto-r_{AB}) preserves the unoriented plane and flips its
orientation. It does **not** by itself send the terminal reciprocal depth to its negative; signed
depth reversal belongs to the ordered reciprocal calibration.

Full observer reversal changes the base event from A to B. Comparing the A-side and B-side planes
then requires lawful calibration/transport. G168 does not invent that carry.

### Coincidence

At coincidence the separation tangent is zero and

\[
\operatorname{rank}(u_A,0)=1.
\]

The reciprocal scalar can have its coincidence value, but there is no direction-owned rank-two
plane. A limiting direction exists only when a pair germ is supplied. This is a genuine boundary,
not a failure of the regular theorem.

### Relative motion

B's velocity need not lie in the positional plane. In Minkowski coordinates,

\[
u_A=(1,0,0,0),
\quad r_{AB}=(0,1,0,0),
\quad v_B=(5/4,0,3/4,0)
\]

has (g(v_B,v_B)=-1), but (v_B\notin\operatorname{span}(u_A,r_{AB})). The local positional plane
is therefore not promoted into the complete relative-velocity kinematics of both observers.

## 7. Epistemic ownership

The exact result separates three levels:

1. **Bare labels ((A,B)):** insufficient.
2. **Typed local ordered co-present pair germ ((u_A,s_{AB})):** supplied by the completed local
   relation as a `WORKING` semantic clarification.
3. **Pair plane, orthogonal ruler, positive screen, and G167 (Y,Z):** `DERIVED` from the germ and
   metric.

Thus the local plane is not an additional physical history to be selected, and it is not an
arbitrary immersion menu. It is the tangent content of the relation being evaluated. What remains
open is which event/calibration germs form the physical global network and how distinct basepoints
carry their frames—not the local plane once a relation is present.

## Maximum conclusion

```text
ORDERED_COPRESENT_PAIR_GERM_OWNS_LOCAL_CALIBRATED_PAIR_PLANE
__BARE_LABELS_DO_NOT
__NO_PATH_REQUIRED
```

This does not derive a global event-pairing rule, path, pair surface, cross-query carry, physical
profile, `X_max`, dynamics, signalling, source, action, bootstrap, or general complete metric.
