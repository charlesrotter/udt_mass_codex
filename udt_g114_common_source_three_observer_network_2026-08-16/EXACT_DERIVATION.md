# G114 exact derivation — common-source three-observer network

Date: 2026-08-16

## 1. Typed common-source query

Let `(M,g)` be a supplied smooth time-oriented Lorentz four-manifold. For `i=A,B,C`, supply a
properly calibrated observer worldline `z_i(tau_i)` and a time-dependent normalized celestial field
`k_i(tau_i,n_i)`. Define the conditional observer exponential

\[
F_i(\tau_i,\lambda_i,n_i)
=\operatorname{Exp}_{z_i(\tau_i)}[\lambda_i k_i(\tau_i,n_i)].
\]

Supply one marked source event `s`, preferably as a marked event on a source worldline `q(sigma)`.
The branch set is the complete exponential preimage

\[
\mathcal B_i(s)=\{(\tau_i,\lambda_i,n_i):F_i(\tau_i,\lambda_i,n_i)=s\}.
\]

Every member is retained with its path, cut, and caustic label. The metric and query derive this set
conditionally; neither `c_E` nor terminal depth selects one member.

For one branch `b_i`, the full differential remains

\[
dF_i=(T_i,K_i,J_{i1},J_{i2}),
\]

with distinct terminal pair block `h_parallel,i`, angular Jacobi block `D_i`, and mixed block. The
terminal reciprocal readout is

\[
\phi_i=\frac14\log\frac{-\det h_{\parallel,i}}{(h_{\parallel,i})_{00}^2}.
\]

This number remains a readout of branch `b_i`; three readable numbers are not automatically one
edge cocycle.

## 2. Full Jacobi phase carrier

Choose a parallel screen on branch `b_i`. The transverse Jacobi equation is

\[
D_{K_i}^2J+\mathcal R_iJ=0,
\]

where the optical tidal operator `R_i` is symmetric on the positive screen. In phase coordinates

\[
X_i=\binom{J}{\Pi},\qquad \Pi=D_{K_i}J,
\]

the equation is first order,

\[
\frac{dX_i}{d\lambda_i}
=A_iX_i,
\qquad
A_i=\begin{pmatrix}0&I\\-\mathcal R_i&0\end{pmatrix}.
\]

For

\[
\Omega=\begin{pmatrix}0&I\\-I&0\end{pmatrix},
\]

symmetry of `R_i` gives

\[
A_i^T\Omega+\Omega A_i=0.
\]

Therefore the fundamental phase propagator `P_i` obeys

\[
P_i^T\Omega P_i=\Omega,
\qquad \det P_i=1.
\]

It is invertible wherever the smooth Jacobi initial-value problem exists, including ordinary
caustics where the position block `D_i` is singular. For the exact isotropic control at
`lambda=pi`,

\[
P(\pi)=-I_4,
\qquad D(\pi)=\sin(\pi)I_2=0.
\]

Thus inverse-`D` filtering deletes a regular phase state. The full `(J,D_KJ)` carrier is the correct
compositional object.

## 3. What the common source supplies

A bare event supplies neither a rest frame nor a cross-ray screen comparison. If the query supplies
a source worldline with unit tangent `U_s`, each ray tangent can be normalized at the source by

\[
\omega_i=-g(K_i,U_s)>0,
\qquad \widehat K_i=K_i/\omega_i.
\]

The source-rest screen is then

\[
\mathcal S_i^s=\{v\in T_sM:g(v,U_s)=g(v,\widehat K_i)=0\}.
\]

It is canonically the tangent plane at direction `n_i=widehat K_i-U_s` of the round source
celestial sphere determined by `(g_s,U_s)`. A transported null-screen representative can be
projected into this source-rest representative by adding a multiple of `K_i`; this preserves the
screen-quotient metric.

The source worldline therefore derives:

1. the three endpoint screen fibers;
2. a common source celestial sphere;
3. its metric Levi-Civita connection.

It does not select a path between different points `n_i` on that sky. For a supplied source-sky
path `xi_ji`, parallel transport gives

\[
Q_{ji}:\mathcal S_i^s\longrightarrow\mathcal S_j^s.
\]

Its phase lift is

\[
C_{ji}=Q_{ji}\oplus Q_{ji}.
\]

This form uses source-normalized derivative coordinates. In each ray's native affine phase
coordinates, write `Pi_i=D_{K_i}J` and `widehat Pi_i=Pi_i/omega_i`. Then the same junction is

\[
C_{ji}^{\rm native}
=\operatorname{diag}\left(Q_{ji},\frac{\omega_j}{\omega_i}Q_{ji}\right),
\]

and

\[
(C_{ji}^{\rm native})^T\Omega C_{ji}^{\rm native}
=\frac{\omega_j}{\omega_i}\Omega.
\]

Thus the native-affine junction is generally conformally symplectic, while its
source-normalized representation is symplectic. The frequency factors telescope around every
closed observer loop. The exact rational verification includes unequal `omega_A,omega_B,omega_C`;
the simpler `Q+Q` witness is its matched-calibration special case.

This is a metric-derived comparison conditional on `U_s`, affine/source covector calibration, and
the path label. At antipodes or around
loops, retaining path labels is essential. A finite common source-frame trivialization is another
legal query choice; it gives exact descent locally but is not a globally selected celestial frame.

Source emission transfer, polarization state, occupancy, amplitude, and branch weights are not
contained in `C_ji` and remain `OPEN`.

## 4. Exact carried observer edges

Let the endpoint phase coordinates and propagators include the explicitly declared source
normalization above. Let

\[
P_i:V_i\longrightarrow E_i
\]

carry the observer-i initial phase fiber to its source endpoint phase fiber. For a correctly typed
source junction

\[
C_{ji}:E_i\longrightarrow E_j,
\]

define

\[
R_{ji}=P_j^{-1}C_{ji}P_i:V_i\longrightarrow V_j.
\]

This is a mathematical comparison of full phase states. It is not a signal sent backward through
observer `j`, and it is not yet an identification of physical point-observer beams.

For composable junction paths,

\[
R_{kj}R_{ji}=P_k^{-1}C_{kj}C_{ji}P_i.
\]

If

\[
C_{ki}=C_{kj}C_{ji},
\]

then `R_ki=R_kj R_ji`. Reversal is exact when `C_ij=C_ji^-1`.

For the based observer triangle `A -> B -> C -> A`,

\[
R_{AC}R_{CB}R_{BA}
=P_A^{-1}(C_{AC}C_{CB}C_{BA})P_A.
\]

Thus the observer loop is conjugate to the source-junction holonomy. In a supplied common source
trivialization `B_i:E_i->E_0`,

\[
C_{ji}=B_j^{-1}B_i
\]

and the loop is identity. With path-labelled source-sky transport, nonidentity is lawful holonomy,
not an associativity failure or a missing scalar.

Endpoint frame changes conjugate the based loop. Independent changes of the three source endpoint
representatives cancel exactly between `P_i` and `C_ji`. Hence identity, rank from identity,
spectrum, and conjugacy class are representation-covariant.

## 5. The new compatibility condition

The full four-dimensional phase edge always exists once `C_ji` is supplied, but a point observer
does not populate the whole phase fiber. Its angular vertex data satisfy

\[
J(0)=0,
\qquad D_KJ(0)=v,
\]

so the physical vertex variations occupy the two-dimensional Lagrangian plane

\[
L_i^0=\{0\}\oplus\mathcal S_i^{\rm obs}\subset V_i.
\]

Their source image is

\[
\Lambda_i=P_iL_i^0\subset E_i.
\]

After source calibration, two observer beams describe the same two-dimensional infinitesimal
source pattern only if the relevant source boundary rule identifies their image planes. The
strong matched-beam condition is

\[
C_{ji}\Lambda_i=\Lambda_j.
\]

More generally, the surviving common variation dimension is

\[
d_{ji}=\dim(C_{ji}\Lambda_i\cap\Lambda_j)\in\{0,1,2\}.
\]

This dimension is representation-invariant. An invertible source-frame change sends both planes
through the same bijection and preserves their intersection dimension; observer endpoint frame
changes merely reparameterize `L_i^0` before `P_i`. Hence `d_ji` belongs to the supplied
metric/query/branch/source-junction geometry, not to the chosen matrices.

Only on the `d_ji=2` stratum does `R_ji` restrict to a full two-dimensional sky-to-sky map between
the point-observer vertex planes. `d_ji=1` carries one common variation; `d_ji=0` carries none.

This is a metric/query compatibility invariant, not a new field equation. It is also not a
physical selector until the source boundary state or transfer rule says which endpoint phase
planes must match.

The exact rational witness in this package has:

```text
full phase loop: identity
pairwise vertex-image intersection dimensions: 0,0,0
```

Therefore full phase descent does not imply physical beam alignment. A separately constructed
aligned control has all three source image planes equal, proving that the matched stratum is
nonempty and is a genuine restriction rather than an algebraic impossibility.

This is the strongest new result of G114.

## 6. A fixed source event versus a source family

One marked source event organizes the central rays but does not itself provide a nontrivial
two-dimensional source image. A variation that keeps a nonconjugate endpoint fixed has no generic
two-dimensional angular family. To compare resolved sky patterns, polarization, or finite beams,
the query must additionally supply a source screen, source surface/worldtube germ, covectors, or an
equivalent boundary subspace.

That datum is not an appended observer-response score. It states what source variation the metric
is being asked to propagate. Once supplied, the metric owns its branchwise propagation and the
intersection test above.

## 7. Reciprocal scalar channel

Each branch supplies a terminal `phi_i`, but a scalar through-source edge

\[
\delta_{ji}=\phi_i-\phi_j
\]

is exact only when the three terminal pair readouts have been placed in one common reciprocal
calibration local system with reversal and middle-state carry. Local `c_E` normalization fixes
units; it does not by itself prove that independently reconstructed pair blocks are that one
system.

If the common reduction is supplied or derived, triangle scalar periods vanish identically. If the
complete source junction mixes the reciprocal and angular channels, a scalar projection must be
derived from that owned reduction; it may not be imposed after the full calculation.

## 8. Landing

The bounded result is

```text
COMMON_SOURCE_FULL_PHASE_NETWORK_DERIVED_CONDITIONALLY
__SOURCE_WORLDLINE_DERIVES_ENDPOINT_SKY_BUNDLE_AND_CONNECTION
__CROSS_RAY_COMPARISON_REMAINS_PATH_LABELLED
__FULL_PHASE_CARRY_SURVIVES_JACOBI_CAUSTICS
__OBSERVER_LOOP_IS_CONJUGATE_TO_SOURCE_JUNCTION_HOLONOMY
__FULL_PHASE_DESCENT_DOES_NOT_FORCE_PHYSICAL_BEAM_ALIGNMENT
__BEAM_INTERSECTION_RANK_IS_A_METRIC_QUERY_COMPATIBILITY_INVARIANT
__SCALAR_RECIPROCAL_DESCENT_REQUIRES_COMMON_CALIBRATION_REDUCTION
__PHYSICAL_HISTORY_SOURCE_TRANSFER_OCCUPANCY_WEIGHTS_AND_SELECTION_REMAIN_OPEN
```

No observation, fit, action, bootstrap, `X_max`, matter, mass, source law, or signalling result
follows.
