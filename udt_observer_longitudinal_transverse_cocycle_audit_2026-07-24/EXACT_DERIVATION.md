# Exact derivation: observer longitudinal/transverse path cocycle

## 1. Typed inputs

Fix one supplied Lorentzian metric branch, a directed path `gamma:p->q`,
endpoint observer tangents `u_p,u_q`, and a screen basis along the path.
Nothing in this derivation selects the observers, event pairing, or path
type.

For a null tangent `k`, the endpoint-measured frequency is

`omega=-g(u,k)`.

With the direction convention frozen in the preregistration correction,

`Q_gamma = omega_q/omega_p`.

For static rest observers in

`g=-N^2 c_E^2 dt^2+h`,

the conserved coordinate energy gives `omega=E/N`, hence

`Q_pq=N_p/N_q`.

If `p->q->r` uses the same intermediate observer/event,

`Q_pr=Q_pq Q_qr`.

Therefore

`delta_gamma=log Q_gamma`

is additive, and the already derived reciprocal matrix

`S(delta)=diag(exp(-delta),exp(delta))`

obeys

`S(delta_qr) S(delta_pq)=S(delta_pr)`.

This proves a metric endpoint-clock cocycle given the typed path and
observers. It does **not** prove that `delta_gamma` is the native
observer-pair depth appearing in the founding UDT reciprocal postulate.

## 2. Why the angular-size map alone does not compose

Let `xi` be a two-component transverse separation and let
`eta=D xi/d lambda`. The metric Jacobi equation is

`D^2 xi/d lambda^2 + T(lambda) xi = 0`,

where the screen tidal matrix `T` is symmetric and comes from the supplied
metric curvature.

The vertex Jacobi map `J_gamma` is only the map from an initial angular
kick `eta_p` to final separation `xi_q` when `xi_p=0`. It is the upper-right
block of the complete evolution matrix.

In constant sectional curvature `K=1/b^2`,

`J(L)=b sin(L/b) I_2`.

For `b=1` and two segments of length `pi/3`,

`J(2pi/3)=sqrt(3)/2`,

while

`J(pi/3)J(pi/3)=3/4`.

The difference `sqrt(3)/2-3/4` is nonzero. Thus the angular-size/Jacobi
block is not a path cocycle.

## 3. The smallest composable transverse object

Retain the complete first-order state

`Y=(xi,eta)`.

It obeys

`dY/d lambda = A(lambda)Y`,

with

`A = [[0,I],[-T,0]]`.

For

`Omega=[[0,I],[-I,0]]`,

symmetry of `T` gives exactly

`A^T Omega + Omega A = 0`.

The fundamental matrix `M_gamma` is therefore symplectic:

`M_gamma^T Omega M_gamma=Omega`,

and in particular it is invertible. Uniqueness of the first-order initial
value problem gives

`M_(q->r) M_(p->q)=M_(p->r)`,

with matched intermediate data, and

`M_(q->p)=M_(p->q)^-1`.

Writing

`M=[[A,B],[C,D]]`,

the vertex Jacobi map is `B`, and the correct block concatenation law is

`B_pr=A_qr B_pq + B_qr D_pq`,

not `B_pr=B_qr B_pq`.

## 4. Caustics do not destroy the full cocycle

For a round branch the one-screen propagator is

`M_K(L) = [[cos(L/b), b sin(L/b)],`

`          [-sin(L/b)/b, cos(L/b)]]`.

The two-screen result is its tensor product with `I_2`.

At the antipode `L=pi b`,

`B=0`

but

`M_K=-I`.

The projected angular-area map is singular at the caustic, while the
complete transverse state propagator remains invertible with determinant
one. At the cut locus there are multiple geodesic paths; the metric gives a
set of path-labelled propagators, not a unique path-independent operator.

## 5. Screen-frame covariance

If the screen bases at the endpoints are rotated by `R_p,R_q`, lift them to
phase space as

`G_p=diag(R_p,R_p)`, `G_q=diag(R_q,R_q)`.

Then

`M_pq -> G_q M_pq G_p^-1`.

For two adjacent segments the intermediate factors cancel exactly:

`(G_r M_qr G_q^-1)(G_q M_pq G_p^-1)`

`=G_r M_pr G_p^-1`.

Thus the cocycle is geometric and endpoint-frame covariant. A particular
matrix representation is not itself frame independent.

## 6. Reducible longitudinal/transverse assembly

On the same path and with the same intermediate event data, define

`C_gamma = S(log Q_gamma) direct_sum M_gamma`.

Both blocks compose, so

`C_qr C_pq=C_pr`.

This is a real metric-derived path-groupoid cocycle. It is a **reducible
direct sum**: the calculation supplies no off-diagonal solder, mixing law,
or theorem that identifies `log Q` with the founding UDT pair depth. Full
coframe parallel transport is another composable metric object, but its type
is distinct from both the endpoint readout and the deviation propagator.

## 7. Exact branch controls

### B19 round `S3_b`

The complete ultrastatic branch has `Q=1`, so `S=I`. The transverse
propagator is exact and pathwise global. At the antipode the projected
Jacobi block vanishes while the full propagator remains invertible. This is
a complete transverse witness with a trivial clock block, not the desired
nontrivial reciprocal solder.

### Homogeneous squashed `S3`

The off-shell complete control is also ultrastatic, hence `Q=1`. A
path-labelled transverse fundamental matrix exists for every supplied
geodesic. The explicit cut/area atlas and on-shell selection remain open.

### Local WR-L residual

In proper radial distance `D`,

`N=1-D/(2X)`,

`R=D-D^2/(4X)`,

`K_rad=1/(2XR)`.

The exact identity

`R''+K_rad R=0`

shows that `R` is the centered vertex Jacobi solution. For a centered start,

`Q=1/N=exp(phi)`.

Thus WR-L has a local common-path witness with nontrivial clock and
transverse blocks. It remains centered, locally residual, center-irregular
if the center is included, and lacks a complete all-observer recentering.

### Temporal-`phi` slice family

The transverse propagator exists pathwise if a complete positive level
geometry is supplied. Its physical clock solder and complete branch remain
open.

### Constant-curvature static countercontrol

Both blocks exist inside its static patch. The clock patch ends before the
completed round spatial diameter, and the control is not a registered UDT
branch.

### Universal physical UDT

No registered branch simultaneously supplies:

1. completeness;
2. arbitrary-observer recentering;
3. a nontrivial reciprocal clock block;
4. one typed event/path rule;
5. the founding-depth solder.

The universal operator therefore remains `OPEN`.

## 8. Exact status

- Metric transverse phase-space path cocycle:
  `DERIVED_GIVEN_METRIC_PATH`.
- Endpoint clock ratio cocycle:
  `DERIVED_GIVEN_OBSERVERS_PATH_AND_EVENTS`.
- Reducible direct-sum cocycle:
  `DERIVED_REDUCIBLE_GIVEN_COMMON_PATH_DATA`.
- Vertex Jacobi map as a standalone cocycle:
  `REJECTED_GENERICALLY`.
- Founding reciprocal depth equal to `log Q`:
  `CONDITIONAL`.
- One irreducible native UDT observer representation:
  `OPEN`.
- Complete nontrivial universal all-observer realization:
  `OPEN`.

No action, source, carrier, topology, boundary completion, density,
bootstrap law, physical `X_max`, signal ontology, or empirical fit was used
or derived.
