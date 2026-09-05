# G348 exact derivation — generic Lorentzian null-screen area theorem

Date: 2026-09-04
Grade: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Bounded landing

```text
GENERIC_METRIC_NULL_SCREEN_AREA_THEOREM_CLOSES_WITH_SINGULAR_STRATA
__LEVI_CIVITA_QUOTIENT_CONNECTION_SELF_ADJOINT_TIDE_AND_SYMPLECTIC_FLOW
__SOURCE_FREQUENCY_SQUARED_DIRECTIONAL_AREAS_AND_GENERIC_OBSERVER_COVARIANCE
__WRONSKIAN_FORCES_CONJUGATE_ZERO_ORDER_EQUAL_TO_KERNEL_DIMENSION
__TYPE_I_GENERATOR_INVERSE_SCALAR_AND_STATIONARY_SEWING_ARE_CHARTWISE
__NO_LIGHT_DISTANCE_POPULATION_HISTORY_SCALE_OR_XMAX_SELECTED
```

G348 selects preregistered alternatives `A`, `Q1`, `J1`, `R1`, `A1`, `O1`, `C1`, `X1`, `S1`,
`W1`, and `P1`. The result is conditional on a supplied smooth Lorentzian metric, supplied regular
affine null geodesic, endpoints, observers, and path label. It does not use the owner-provisional
field equation and therefore selects no UDT spacetime or history.

## 1. Intrinsic quotient screen and connection

Let `(M,g)` be a smooth time-oriented four-dimensional Lorentzian manifold with signature
`(-,+,+,+)`. Let `gamma` be an affinely parameterized future null geodesic with nonzero tangent
`k`, so

\[
 g(k,k)=0,\qquad \nabla_k k=0.
\tag{1}
\]

At every point define

\[
 Q_k=k^\perp/\operatorname{span}(k).
\tag{2}
\]

The restriction of `g` to `k^perp` has radical exactly `span(k)`. For example, choose any future
unit timelike vector `u` and write `k=omega(u+s)`, where `s` is unit spacelike in `u^perp`. If
`X=a u+x` lies in `k^perp`, then `x dot s=a` and

\[
 g(X,X)=|x-a s|^2\geq0,
\tag{3}
\]

with equality exactly when `X` is proportional to `k`. Thus (2) has a positive-definite rank-two
metric `q` independent of the auxiliary observer.

For any quotient section represented by `X in k^perp`, define

\[
 {D[X]\over d\lambda}=[\nabla_kX].
\tag{4}
\]

This is well defined. Replacing `X` by `X+f k` changes its derivative by `f'k`, which vanishes in
the quotient. Also `nabla_k X` remains orthogonal to `k`, and metric compatibility gives

\[
 {d\over d\lambda}q([X],[Y])
 =q(D[X],[Y])+q([X],D[Y]).
\tag{5}
\]

No independently supplied screen carry is needed: (4) is the Levi-Civita quotient connection.

## 2. Metric curvature and the complete Jacobi phase flow

With curvature convention

\[
 R(X,Y)Z=\nabla_X\nabla_YZ-\nabla_Y\nabla_XZ-\nabla_{[X,Y]}Z,
\tag{6}
\]

define the quotient tidal endomorphism

\[
 \mathcal T[X]=[R(X,k)k].
\tag{7}
\]

It is independent of the representative because `R(k,k)=0`, lies in the quotient because its
inner product with `k` vanishes, and is self-adjoint by the Riemann symmetries:

\[
 q(\mathcal T[X],[Y])=q([X],\mathcal T[Y]).
\tag{8}
\]

The transverse class of a connecting Jacobi field obeys

\[
 {D^2x\over d\lambda^2}+\mathcal T x=0.
\tag{9}
\]

Put `v=Dx/dlambda` and use the metric musical map `p=v^flat` for canonical momentum. The
metric-vector presentation `(x,v)` and canonical presentation `(x,p)` are equivalent; only the
latter has covector momentum components under arbitrary screen coordinates. For two solutions,
with `p=v^flat` and `r=(Dy/dlambda)^flat`, their quotient Wronskian is

\[
 \Omega((x,p),(y,r))=r(x)-p(y).
\tag{10}
\]

Differentiating (10), using (9), metric compatibility, and (8), gives `dOmega/dlambda=0`.
Consequently the complete rank-four fundamental map

\[
 \binom{x_1}{p_1}=M_{10}\binom{x_0}{p_0},\qquad
 M_{10}=\begin{pmatrix}A_{10}&B_{10}\\C_{10}&D_{10}\end{pmatrix}
\tag{11}
\]

is symplectic. It is the fundamental solution of a regular linear ODE, hence exists uniquely and
is invertible throughout every regular metric/geodesic segment, including conjugate endpoints.
It obeys

\[
 M_{20}=M_{21}M_{10},\qquad M_{01}=M_{10}^{-1}.
\tag{12}
\]

In metric-adjoint notation, the inverse of a symplectic block matrix gives

\[
 \boxed{B_{01}=-B_{10}^{*}},\qquad
 \boxed{|\det B_{01}|=|\det B_{10}|}.
\tag{13}
\]

Equations (4)--(13) are coordinate-free and use no special spacetime solution.

## 3. Directional infinitesimal angular areas

Let `u_i` be any future unit timelike endpoint observers and

\[
 \omega_i=-g(k,u_i)>0.
\tag{14}
\]

A fixed-frequency projective-null variation has initial momentum covector
`p_0=omega_0 q_0 theta_0`. Holding the source position fixed gives

\[
 x_1=B_{10}\,\omega_0q_0\theta_0.
\tag{15}
\]

Pairing the component determinant with the two endpoint metric area coefficients yields

\[
 \boxed{
 \mathscr A_{1\leftarrow0}
 =\omega_0^2|\det B_{10}|\sqrt{\det q_1\det q_0}},
\tag{16}
\]

\[
 \boxed{
 \mathscr A_{0\leftarrow1}
 =\omega_1^2|\det B_{01}|\sqrt{\det q_0\det q_1}}.
\tag{17}
\]

In orthonormal quotient frames the metric determinant factor is one. From (13),

\[
 \boxed{
 {\mathscr A_{1\leftarrow0}\over\mathscr A_{0\leftarrow1}}
 =\left({\omega_0\over\omega_1}\right)^2}.
\tag{18}
\]

This is an infinitesimal metric-area statement. No finite light bundle, emission, detector,
brightness, flux, luminosity, probability, or observational distance is present.

## 4. Coordinate and affine covariance

Under arbitrary passive endpoint coordinates

\[
 x_i'=R_ix_i,\qquad p_i'=R_i^{-T}p_i,
\tag{19}
\]

the typed objects obey

\[
 B_{10}'=R_1B_{10}R_0^T,\qquad
 q_i'=R_i^{-T}q_iR_i^{-1}.
\tag{20}
\]

The determinant of `B` and the metric area coefficients in (16) acquire reciprocal factors, so
both directional areas are endpoint-`GL(2)` scalars.

Under a common positive affine rescaling `k->a k`, derivative units change by `p->a p`. Therefore

\[
 M'_{10}=S_aM_{10}S_a^{-1},\qquad
 S_a=\operatorname{diag}(I_2,aI_2),\qquad B'_{10}=a^{-1}B_{10}.
\tag{21}
\]

Both endpoint frequencies gain `a`, while the two-dimensional determinant gains `a^-2`. Equations
(16)--(18) are affine invariant.

## 5. Arbitrary endpoint observers

For any future unit timelike observer `u`, its screen is the unique representative of (2)
orthogonal to `u`. If `v` is another such observer, the representative change is

\[
 I_{v\leftarrow u}X=X+{g(X,v)\over\omega_v}k.
\tag{22}
\]

It is an isometry of the quotient metric. Differentiating the normalized celestial direction gives

\[
 \theta_v={\omega_u\over\omega_v}I_{v\leftarrow u}\theta_u,
 \qquad
 d\Omega_v=\left({\omega_u\over\omega_v}\right)^2d\Omega_u.
\tag{23}
\]

Thus, for independent endpoint replacements and
`D_i=omega_(v_i)/omega_(u_i)>0`,

\[
 \boxed{\mathscr A'_{1\leftarrow0}=D_0^2\mathscr A_{1\leftarrow0}},\qquad
 \boxed{\mathscr A'_{0\leftarrow1}=D_1^2\mathscr A_{0\leftarrow1}}.
\tag{24}
\]

Only the source factor enters because the target observer changes the quotient representative by
an isometry. This proves that G347's observer law is pointwise general, not Taub/Kasner-specific.

## 6. Conjugate points, rank loss, and the Wronskian transversality theorem

Fix the source endpoint and metric-identify initial covectors with vectors. Let `B(lambda)` be the
corresponding Jacobi tensor; in a parallel orthonormal quotient frame it has

\[
 B(\lambda_0)=0,\qquad DB(\lambda_0)=I.
\tag{25}
\]

The conserved Wronskian of its columns is

\[
 B^*DB-(DB)^*B=0.
\tag{26}
\]

At a conjugate endpoint `lambda_*`, let `V=ker B(lambda_*)`. If both `Bv=0` and `DBv=0`, uniqueness
for (9) makes the corresponding Jacobi field identically zero, contradicting (25) unless `v=0`.
Thus `DB` is injective on `V`.

For `v in V` and arbitrary `w`, (26) gives

\[
 q(DBv,Bw)=q(Bv,DBw)=0.
\tag{27}
\]

Therefore

\[
 DB: \ker B\longrightarrow(\operatorname{im}B)^\perp
\tag{28}
\]

is injective. The domain and codomain have the same dimension, so it is an isomorphism. In bases
adapted to the kernel and image, the lost directions of `B` cross zero linearly. Hence

\[
 \boxed{\operatorname{ord}_{\lambda_*}\det B=\dim\ker B}.
\tag{29}
\]

This proves preregistered alternative `X1`: higher-order degenerate metric-Jacobi crossings cannot
occur on the stated regular positive quotient bundle.

In four spacetime dimensions there are exactly three strata:

| Rank of `B` | Kernel dimension / determinant order | Directional area | Oriented sign |
|---|---:|---|---|
| 2 | 0 | positive | constant on the connected regular interval |
| 1 | 1 | zero | flips across the simple conjugate crossing |
| 0 | 2 | zero | does not flip across the transverse double crossing |

At coincidence, `B=(lambda-lambda_0)I+O((lambda-lambda_0)^3)`, so the vertex is the rank-zero,
order-two identity boundary. A noncoincident multiplicity-two conjugate point has the same order
classification but is not coincidence.

The full `M` never loses rank at any of these crossings. What fails is only the projection from
initial screen slope to final screen position.

## 7. Orientation and endpoint-chart limits

The positive metric area uses `|det B|` and requires no screen orientation. A signed determinant
requires orientations of both endpoint quotient spaces. With compatible transported orientations,
(13) preserves the sign on reversal because the screen dimension is two:

\[
 \det(-B^*)=(-1)^2\det B=\det B.
\tag{30}
\]

Reversing exactly one supplied endpoint orientation reverses the signed coefficient. Therefore a
universal positive **oriented** determinant is false, even though the orientation-free areas are
nonnegative.

On the rank-two stratum, the type-I endpoint generator exists because `B^-1` exists. The G345
inverse determinant scalar is finite there and

\[
 \sqrt{\mathscr A_{1\leftarrow0}\mathscr A_{0\leftarrow1}}
 ={1\over\widehat\Delta_{10}}.
\tag{31}
\]

At rank loss, both directional areas vanish. The type-I generator and finite G345 scalar are
undefined; `widehat Delta` diverges in the limiting chart while its reciprocal tends to zero.
Calling this a singular spacetime or deleting the ray would be false: the phase map (11) remains
regular and a different canonical endpoint chart may be used.

## 8. Composition and stationary sewing across strata

The full symplectic composition (12) holds across every rank stratum. If and only if the three
position blocks used below are invertible, symplectic block algebra gives

\[
 H_1=B_{21}^{-1}B_{20}B_{10}^{-1},
\tag{32}
\]

\[
 |\det B_{20}|=|\det H_1|\,|\det B_{21}|\,|\det B_{10}|.
\tag{33}
\]

Equations (32)--(33) reproduce G344--G347's stationary generator and directional-area sewing on
each rank-two chart. If any required `B` is singular, that formula is not globally extended by
wishful cancellation; one returns to the everywhere-regular full map (12) or changes generating
chart. Thus preregistered `W1`, not global bare sewing `W2`, holds.

## 9. Exact witnesses and computational evidence

In a parallel quotient frame, every self-adjoint tide has a Hamiltonian phase generator

\[
 L(\lambda)=\begin{pmatrix}0&I\\-\mathcal T(\lambda)&0\end{pmatrix}.
\tag{34}
\]

The production route composed exact constant-tide Hamiltonian steps with changing, noncommuting
symmetric tides. It passed `39542/39542` checks across 420 profiles, arbitrary endpoint `GL(2)`
frames including reflections, affine scales, reversal, area laws, stationary joins, and arbitrary
finite endpoint observers.

The exact constant-tide witnesses were:

- `T=diag(1,-1)` at length `pi`: rank one, a simple determinant zero, and a sign flip;
- `T=I` at length `pi`: rank zero, a double determinant zero, and no sign flip;
- length zero: the rank-zero identity boundary with a regular full phase map;
- `T=diag(-1,-4)`: a nonconjugate hyperbolic branch with positive determinant.

The first production execution returned `39541/39542` because one supplemental diagnostic falsely
equated finite-offset magnitudes on opposite sides of `sin(L)sinh(L)`. The recorded execution note
replaced only that assertion with centered first- and second-derivative checks at unchanged
tolerance; no theorem, formula, sample, alternative, or maximum conclusion changed.

The implementation-distinct route integrated 150 smooth noncommuting symmetric tidal profiles by
direct RK4, reconstructed observers with a rapidity chart, and passed `9759/9759`. Its maximum
phase composition error was `2.377154029176154e-12`, and all other smooth phase, Wronskian,
reversal, observer, and crossing errors were smaller than the preregistered tolerances. It imports
neither production nor G343--G347 code.

Fresh external `gpt-5.6-sol` review authenticated all 33 sealed payloads, reproduced the registered
`18/18` no-write aggregate and all three underlying replays, and independently reconstructed the
quotient, symplectic, crossing, observer, area, and chartwise-sewing arguments. It found no
mathematical defect or required repair and returned
`ACCEPT_G348_GENERIC_NULL_SCREEN_AREA_THEOREM`. Its nonblocking evidence caveats remain explicit:
the checksum and Git chronology evidence is documentary rather than externally signed; the hostile
mutation checker is a tautological contract guard; and text-token gates are not mathematical proof.

## 10. Ownership and remaining boundary

This is a general differential-geometric consequence of a supplied Lorentzian metric and its
Levi-Civita connection. It is metric-derived but not uniquely diagnostic of UDT, and it adds no
field equation. The owner-provisional trace-free response equation is not used.

Every metric, geodesic, endpoint, observer, orientation, and path label remains supplied. The
result does not select a physical ray or observer population, sum paths, evolve a finite bundle,
or define emission, detection, light transfer, brightness, flux, luminosity, probability, or
observational distance. It supplies no history, occupancy, topology, stability, matter/mass,
physical scale, `X_max`, or canon.
