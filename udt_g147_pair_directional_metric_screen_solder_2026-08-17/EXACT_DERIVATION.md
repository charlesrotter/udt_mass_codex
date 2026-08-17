# G147 exact derivation — pair-directional / metric-screen solder

Date: 2026-08-17

## 1. Result

On one supplied regular calibrated pair query at nonzero relational position, **if** normalized
relation position is represented by the defined query-relative rest-space lift
`xi = rho n`, the directional sphere tangent and metric pair screen are the same positive
rank-two subspace of the ambient tangent space:

\[
T_{\boldsymbol\xi}S^2_{|\rho|}(R_u)=H_{\rm pair}.
\]

Thus no free solder coefficient occurs inside that conditional representation. The derivation does
not prove that the physical multidirectional position carrier is `R_u`, solder an independently
owned ball carrier into `R_u`, or identify screens belonging to distinct pair queries.

## 2. Query-owned orthonormal pair flag

Let a typed query supply a regular time-oriented calibrated immersion

\[
F:\Sigma^2\to(M^4,g)
\]

and at a marked point define

\[
J_0=F_*\partial_0,\qquad J_1=F_*\partial_1.
\]

The calibration owns a future timelike clock line `J_0` and an oriented transverse ruler class.
Write

\[
h_{ij}=g(J_i,J_j),\qquad h_{00}<0,\qquad \det h<0.
\]

Set

\[
T^2=-h_{00},\qquad \beta={h_{01}\over h_{00}},
\]

\[
u={J_0\over T},\qquad
r=J_1-\beta J_0.
\]

Then

\[
g(J_0,r)=h_{01}-{h_{01}\over h_{00}}h_{00}=0,
\]

and

\[
L^2=g(r,r)=h_{11}-{h_{01}^2\over h_{00}}
={\det h\over h_{00}}>0.
\]

Therefore

\[
n={r\over L}
\]

satisfies

\[
g(u,u)=-1,\qquad g(n,n)=1,\qquad g(u,n)=0.
\]

Because replacing `J_1` by `r` subtracts only a multiple of `J_0`,

\[
E_{\rm pair}=\operatorname{span}(J_0,J_1)=\operatorname{span}(u,n).
\]

The clock/ruler flag is query-owned. A bare Lorentzian two-plane has internal `O(1,1)` freedom and
does not select `u`; a change that changes the clock line is a different calibrated query, not a
gauge transformation in this theorem.

## 3. Conditional query-relative rest-space lift

The metric-defined rest space of the query clock is

\[
R_u=u^\perp.
\]

It is positive definite and rank three. The query ruler `n` lies in `R_u`. With the adopted bounded
pair position

\[
\rho=\tanh\phi_{\rm pair},\qquad \rho\ne0,
\]

define, as a `DEFINED / SUPPLIED_CONDITIONAL_QUERY_RELATIVE_LIFT`, the relation-ball coordinate

\[
\boldsymbol\xi=\rho n\in R_u.
\]

This is not derived as the physical three-position lift and is not a spacetime displacement,
exponential-map vector, proper length, or areal radius. It conditionally places the adopted scalar
position along the ruler direction owned by this query so the proposed common-carrier claim can be
typed and tested.

Inside the Euclidean space `R_u`, the radius-`|rho|` directional sphere is

\[
S^2_{|\rho|}(R_u)=\{v\in R_u:g(v,v)=\rho^2\}.
\]

Its tangent plane at `xi` is

\[
T_{\boldsymbol\xi}S^2_{|\rho|}(R_u)
=\{w:g(w,u)=0,\ g(w,\boldsymbol\xi)=0\}.
\]

Since `rho` is nonzero, the second condition is exactly `g(w,n)=0`. Hence

\[
T_{\boldsymbol\xi}S^2_{|\rho|}(R_u)
=\{w:g(w,u)=g(w,n)=0\}
=E_{\rm pair}^\perp
=H_{\rm pair}.
\]

The solder

\[
\sigma:T_{\boldsymbol\xi}S^2_{|\rho|}(R_u)\to H_{\rm pair}
\]

is therefore the identity inclusion on one subspace. It is automatically an isometry. This removes
no freedom from an independently owned position ball: soldering such an abstract carrier into
`R_u` while fixing only its radial axis retains an `O(2)` family. That freedom becomes ordinary
screen-frame gauge only after the common-carrier identification has been supplied.

## 4. Projector form

Writing `J=(J_0,J_1)`, the metric orthogonal projector onto the pair screen is

\[
P_H=I-J(J^TgJ)^{-1}J^Tg.
\]

The orthonormal flag gives

\[
P_{u,n}=I+u(u^Tg)-n(n^Tg).
\]

Since the two column pairs span the same nondegenerate plane,

\[
P_H=P_{u,n}.
\]

The production calculation verifies exact equality, rank two, idempotence, metric self-adjointness,
annihilation of `u,n`, and positive restriction.

## 5. Covariance and its boundary

Under an ambient basis change with old vector components `x=A x'`,

\[
g'=A^TgA,\qquad J'=A^{-1}J,
\]

and

\[
P'_H=A^{-1}P_HA.
\]

The induced pair metric is unchanged. Under a positive upper-triangular flag-preserving pair-domain
reparameterization

\[
R=\begin{pmatrix}a&b\\0&d\end{pmatrix},\qquad a,d>0,
\]

the clock line and oriented ruler quotient are preserved. Orthogonalization returns the same `u,n`,
and the screen projector is unchanged. This is not full calibrated-position covariance. In fact,

\[
{-\det h'\over(h'_{00})^2}
={d^2\over a^2}{-\det h\over h_{00}^2},
\]

so `phi_pair` and `rho` are not invariant unless the calibration is separately carried or `a=d`.
A general domain change with a nonzero lower-left entry also changes the clock line and therefore
changes the query flag; it is not gauge for this result.

No orientation or reversal theorem is claimed. The tangent screen is unchanged when `rho` changes
sign, so it forgets ordered-pair sign. An oriented solder would additionally require consistent
ambient, clock, and ruler orientation conventions.

## 6. Complete-coframe liveness witness

The preregistered rational witness uses

```text
B=[[2,1/2],[0,3]]
Q=[[1,1/3],[0,2]]
S=[[1/5,-1/7],[1/4,1/6]]
Y=I_2
Z=[[1/10,-1/8],[-1/12,1/9]]
rho=2/5
```

in

\[
E=\begin{pmatrix}B&0\\QS&Q\end{pmatrix},\quad
g=E^T\eta E,\quad
J=\binom YZ.
\]

All registered blocks are live in the tested witness. Scaling each one of `B,Q,S,Y,Z` separately
changes both the induced pair metric and the screen projector exactly. The induced pair metric has

\[
h_{00}=-{7619\over2025}<0,
\qquad
\det h<0,
\]

so the registered witness passes its untuned regularity gate. Both exact implementations return
the same screen projector and positive screen Gram matrix.

## 7. Degenerate and global boundaries

At `rho=0`, the radius-zero sphere has no intrinsic direction and its tangent is not a rank-two
position-owned screen. The supplied pair query still owns `H_pair`, but position alone no longer
reconstructs it. Null or degenerate pair planes likewise leave the theorem's domain.

For two different pair queries meeting at an intermediate observer, the two ruler directions may
define different tangent planes in that observer's rest sphere. G147 supplies each local plane but
does not identify them. A common middle-observer clock calibration, an allowed direction-space
path/carry, and orientation/order typing are still required before comparing positional angular
composition with metric `U_gamma`.

## Maximum conclusion

```text
CONDITIONAL_QUERY_RELATIVE_REST_SPACE_IDENTITY__PHYSICAL_THREE_POSITION_LIFT_AND_CROSS_QUERY_CARRY_OPEN
```

This proves only an identity inside the defined query-relative rest-space lift. The physical
three-position carrier and any residual `O(2)` solder from an independent carrier remain open. The
result does not select a multidirectional ball operation, derive a complete observer arrow, equate
a positional gyration with metric screen transport, or determine a physical query family, metric
history, `X_max`, proper length, dynamics, action, source, observations, bootstrap, matter, mass,
or global completion.
