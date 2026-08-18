# G158 exact derivation — the supplied complete coframe is a (3+3+4) semidirect machine

Date: 2026-08-18

## 1. Exact bounded object

On the oriented regular gauge used by the complete-metric witness, let

\[
B,Q\in B^+(2),\qquad S\in\operatorname{Mat}(2,\mathbb R),
\]

where $B^+(2)$ is the positive-diagonal upper-triangular group. Define

\[
E(B,Q,S)=
\begin{pmatrix}
B&0\\
QS&Q
\end{pmatrix}.
\]

This is the ten-coordinate gauge-fixed complete coframe chart:

- three base clock/ruler coordinates in $B$;
- three positive-screen coordinates in $Q$;
- four base-to-screen mixing coordinates in $S$.

The theorem is conditional on a supplied common trivialization that makes matrix multiplication
typed. A coframe at one event is not automatically a physical arrow to a coframe at another event.

The factorization is unique. For a structured matrix $E$,

\[
B=E_{BB},\qquad Q=E_{QQ},\qquad S=Q^{-1}E_{QB}.
\]

The Jacobian from the ten coordinates to the ten structured entries is

\[
\det J=(\det Q)^2=q_{00}^2q_{11}^2>0.
\]

Thus this is a genuine ten-dimensional regular chart, not a list with a hidden algebraic ratio.

## 2. Exact finite composition

For chronological multiplication $E_2E_1$, direct block multiplication gives

\[
\boxed{
B_{21}=B_2B_1,
\qquad
Q_{21}=Q_2Q_1,
\qquad
S_{21}=S_1+Q_1^{-1}S_2B_1.
}
\]

The identity is $(I,I,0)$, and

\[
\boxed{
(B,Q,S)^{-1}
=
(B^{-1},Q^{-1},-QSB^{-1}).
}
\]

Closure and unique factorization make associativity the ordinary associativity of matrix
multiplication.

Write

\[
H(B,Q)=\operatorname{diag}(B,Q),
\qquad
N(S)=\begin{pmatrix}I&0\\S&I\end{pmatrix}.
\]

Then $E=H N$, the mixing subgroup is additive,

\[
N(S_2)N(S_1)=N(S_2+S_1),
\]

and base/screen frames act on it by

\[
\boxed{
H(B,Q)N(S)H(B,Q)^{-1}=N(QSB^{-1}).
}
\]

Therefore the regular gauge-fixed complete-coframe matrices are a semidirect product. The four
mixing components are not independent ornaments: the base and screen frames rescale and shear how
mixing is carried.

## 3. The $3+3+4$ channel structure

G157 uniquely writes the base block as

\[
B=e^\sigma D(\delta)U(\mu).
\]

The positive screen block has the mathematically analogous decomposition

\[
Q=e^\tau A(\psi)U(\nu),
\]

where $\tau$ is screen log-area scale, $\psi$ is screen anisotropy, and $\nu$ is screen shear in
the chosen triangular gauge. Both triangular blocks have their own three-channel semidirect law.
The four entries of $S$ then transform through the exact two-sided action above.

No equation makes

\[
(\sigma,\delta,\mu,\tau,\psi,\nu,S_{00},S_{01},S_{10},S_{11})
\]

proportional to one scalar parameter. Composition coordinates the instruments; it does not impose
fixed volume ratios.

## 4. Determinant characters see only two notes

The determinant is

\[
\boxed{\det E=\det B\,\det Q.}
\]

Therefore $\log\det B$ and $\log\det Q$ are separate additive characters, while every entry of
$S$ is invisible to them. In the logarithmic triangular coordinates,

\[
\log\det E=2\sigma+2\tau.
\]

Consequently a total-volume condition would constrain only one combination of base and screen
scale. It would not fix reciprocal depth, either shear, screen anisotropy, or any mixing entry.
This is why determinant closure cannot substitute for complete carry closure.

## 5. $Y,Z$ are query data acted on by the group

For a supplied pair realization

\[
J=\begin{pmatrix}Y\\Z\end{pmatrix},
\]

the complete pair coframe is

\[
V=EJ=
\begin{pmatrix}
BY\\
Q(SY+Z)
\end{pmatrix}.
\]

If $E_1$ is followed by $E_2$, the action satisfies

\[
E_2(E_1J)=(E_2E_1)J
\]

with exactly the $(B_{21},Q_{21},S_{21})$ law above. Thus $J$ is representation/query data. Its
eight displayed entries are not eight more coordinates of the ambient ten-dimensional group.

Under a pair-domain reparameterization $A\in GL(2)$,

\[
J\mapsto JA,
\qquad
h=J^TE^T\eta EJ\mapsto A^ThA.
\]

The pair metric transforms covariantly as $h\mapsto A^ThA$. Terminal `phi_pair` and
`c_eff/c_E` are not invariant under arbitrary $GL(2)$: they require the supplied calibrated
clock/ruler coordinates or matched carry. Covariance does not choose that query or calibration.

## 6. The time-live score already inside the coframe

For a smooth supplied path $E(\lambda)$, define the right- and left-trivialized logarithmic
velocities

\[
\Omega_R=\dot E E^{-1},
\qquad
\Omega_L=E^{-1}\dot E.
\]

Direct differentiation gives the exceptionally sparse right score

\[
\boxed{
\Omega_R=
\begin{pmatrix}
\dot B B^{-1}&0\\
Q\dot S B^{-1}&\dot Q Q^{-1}
\end{pmatrix}.
}
\]

The equivalent left score is

\[
\boxed{
\Omega_L=
\begin{pmatrix}
B^{-1}\dot B&0\\
\dot S+Q^{-1}\dot Q S-SB^{-1}\dot B&Q^{-1}\dot Q
\end{pmatrix}.
}
\]

These are two frame conventions for the same supplied coframe motion. Under a live left coframe
change $E'=\Lambda(\lambda)E$,

\[
\Omega_R'
=\dot\Lambda\Lambda^{-1}+\Lambda\Omega_R\Lambda^{-1}.
\]

The inhomogeneous term shows that score components and their ratios are gauge-presentation data,
not observables. The current premises do not promote either logarithmic velocity, entry by entry,
into a gauge-independent observable.

For the pair coframe $V=EJ$,

\[
\boxed{
\dot V=\Omega_RV+E\dot J.
}
\]

This is the clean split that earlier selection language obscured:

1. $\Omega_RV$ is change of the supplied complete metric/coframe;
2. $E\dot J$ is change of the supplied observer query/immersion.

The heard pair metric obeys

\[
\dot h
=2\operatorname{sym}\!\left[V^T\eta(\Omega_RV+E\dot J)\right].
\]

Thus one supplied time-live history already carries a changing score. No fixed ratios or extra
post-processing mixer are required. What remains open is the law or legitimate data determining
$E(\lambda)$, $J(\lambda)$, and the physical meaning of $\lambda$.

## 7. Generic changing score versus fixed-generator scaffolding

For any smooth regular endpoint-frame family $E(\lambda)$, relative transitions

\[
C_{ji}=E_jE_i^{-1}
\]

automatically telescope:

\[
C_{21}C_{10}=C_{20}.
\]

The registered polynomial witness changes every $B,Q,S$ sector and passes this identity. Its base
right-score blocks are

\[
(\Omega_R)_{BB}(0)=
\begin{pmatrix}1&0\\0&0\end{pmatrix},
\qquad
(\Omega_R)_{BB}(1)=
\begin{pmatrix}\tfrac12&\tfrac34\\0&1\end{pmatrix}.
\]

They are not scalar multiples, so no reparameterization turns this witness into one fixed score
direction. It also fails $E(2)=E(1)^2$. This proves changing balance only for a supplied kinematic
witness in the registered gauge; it does not select a physical history.

A constant right score

\[
\Omega_R=X
\]

would instead impose

\[
E(\lambda)=e^{\lambda X}E(0).
\]

Writing $X=\begin{psmallmatrix}A&0\\M&C\end{psmallmatrix}$, the component conditions are

\[
\dot B B^{-1}=A,
\qquad
\dot Q Q^{-1}=C,
\qquad
Q\dot S B^{-1}=M.
\]

This fixed-generator path is a legitimate special ansatz, not the generic consequence of
composition. A varying $\Omega_R(\lambda)$ is the natural general history.

## 8. Landing and ownership boundary

`GAUGE_FIXED_COMPLETE_COFRAME_SEMIDIRECT_SCORE_DERIVED__TEN_CHANNEL_REGULAR_GROUP_CLOSES__BASE_AND_SCREEN_BPLUS2_CHANNELS_ACT_ON_FOUR_MIXING_COMPONENTS__Y_Z_ARE_QUERY_REPRESENTATION_DATA_NOT_GROUP_COORDINATES__CHANGING_BALANCE_ALLOWED__PHYSICAL_CARRY_HISTORY_SCORE_AND_GLOBAL_COMPLETION_OPEN`

Premise-stamped meaning:

- `DERIVED_CONDITIONAL`: the ten-channel group, composition, inverse, action, and logarithmic
  velocities on the supplied regular triangular gauge;
- `DERIVED_CONDITIONAL`: the split $\dot V=\Omega_RV+E\dot J$;
- `OPEN`: physical cross-query carry, the functions $E(\lambda),J(\lambda)$, regime calibration,
  and global/singular completion;
- not derived: fixed ratios, observed loud--quiet--loud behavior, $X_{\max}$, action, source,
  bootstrap, matter, mass, or signalling.

All ten gauge-fixed coframe channels in the registered oriented regular
$B^+(2)\times B^+(2)\times\operatorname{Mat}(2)$ chart therefore form one lawful coupled machine.
Its score can change with regime; full coframe-gauge restoration and quotient classification remain
excluded, and the algebra does not yet write the physical composition played by the Universe.
