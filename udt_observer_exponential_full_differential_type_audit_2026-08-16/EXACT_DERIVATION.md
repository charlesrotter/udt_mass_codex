# Exact derivation — observer-exponential full differential

Date: 2026-08-16

Status: `BLIND_VERIFIED_WITH_CAVEATS__REPAIRS_VERIFIED`

## 1. Bounded correction

G93 evaluates a supplied complete coframe and a two-column pair realization. G108 then
conditionally identifies the screen block of those same two columns with a rank-two angular
Jacobi map, and G109 uses terminal `phi_pair` as its local propagation coordinate.

This audit type-checks that identification for the metric-natural point-observer construction. It
does not select a physical metric history, source, transfer law, branch weight, or observation.

## 2. One complete observer relation

Let `(M,g)` be a supplied smooth time-oriented Lorentz manifold, let `z(tau)` be a supplied observer
worldline with unit tangent `u`, and let `n` label the observer's celestial directions. The query
must also supply a time-dependent celestial trivialization `k(tau,n)`; one direction at one event
does not determine how its label is carried along the observer. For the conditional null
observer-sky query, normalize

\[
g(k,k)=0,\qquad g(k,u)=-1
\]

in `c_E`-calibrated clock/ruler units and define

\[
F(\tau,\lambda,n)=\operatorname{Exp}_{z(\tau)}[\lambda k(\tau,n)].
\tag{1}
\]

The full differential has four distinct columns,

\[
dF=(T,K,J_1,J_2)
  =(F_{,\tau},F_{,\lambda},F_{,1},F_{,2}).
\tag{2}
\]

For any complete coframe representative `E`, define

\[
\mathcal V=E\,dF=(V_\parallel,V_\angle),
\qquad
\mathcal H=F^*g=\mathcal V^T\eta\mathcal V.
\tag{3}
\]

The block decomposition is

\[
\mathcal H=
\begin{pmatrix}
h_\parallel&C\\
C^T&h_\angle
\end{pmatrix},
\tag{4}
\]

where `h_parallel` comes from `(T,K)`, `h_angle` comes from `(J_1,J_2)`, and `C` retains their mixed
coupling. The individual `E` and `dF` representatives are not separately physical: any exact
refactorization that preserves `E dF` preserves (3).

## 3. Terminal reciprocal block

On

\[
(h_\parallel)_{00}<0,\qquad \det h_\parallel<0,
\]

the terminal A-calibrated pair decomposition remains

\[
h_\parallel=-T_{\rm pair}^2(dy^0+\beta\,dy^1)^2
             +L_{\rm pair}^2(dy^1)^2,
\]

\[
\phi_{\rm pair}
=\frac12\log\frac{L_{\rm pair}}{T_{\rm pair}}
=\frac14\log\frac{-\det h_\parallel}{(h_\parallel)_{00}^2},
\tag{5}
\]

\[
\frac{c_{\rm eff}^{(\rm pair)}}{c_E}=e^{-2\phi_{\rm pair}}.
\tag{6}
\]

Thus G93 and the terminal portion of G109 survive. Equation (6) remains an inter-observer
calibration readout, not a local signal speed.

## 4. Angular Jacobi block is a different map

Let `(e_1,e_2)` be a parallel orthonormal screen along one ray. The angular Jacobi map is

\[
\mathcal D_{AB}=g(e_A,J_B),
\qquad
\mathcal D:T_nS^2\longrightarrow\mathcal S.
\tag{7}
\]

By contrast, the G93 pair-screen block is

\[
W_{\parallel,Ai}=g(e_A,(T,K)_i),
\qquad
W_\parallel:T_{(\tau,\lambda)}\Sigma_\parallel
             \longrightarrow\mathcal S.
\tag{8}
\]

Equations (7) and (8) have different domain bundles. Independent changes of pair coordinates and
sky coordinates act on their right by independent `GL(2)` matrices. Equal matrix size cannot
identify them. A literal equality requires an extra solder

\[
T_{(\tau,\lambda)}\Sigma_\parallel\longrightarrow T_nS^2,
\]

which the natural observer exponential does not supply.

There is a stronger intrinsic obstruction on every canonical null observer ray. A screen vector is
orthogonal to the ray tangent `K`, hence

\[
g(e_A,K)=0.
\]

Therefore

\[
W_\parallel=(\operatorname{screen}T,0)
\tag{9}
\]

has rank at most one. Its rank-two determinant, area, inverse, and Riccati stratum are empty on this
point-observer subclass. G108's algebraic pair-screen area identity remains true as an identity,
but its regular rank-two realization is inapplicable here. The Jacobi/Riccati algebra instead
belongs to the distinct angular map (7).

## 5. Exact flat catch proof

In Minkowski space, choose a local celestial chart

\[
n(a,b)=(\sqrt{1-a^2-b^2},a,b)
\]

and

\[
F(\tau,\lambda,a,b)
=(\tau+\lambda,\lambda n(a,b)).
\tag{10}
\]

At `a=b=0`, the pair columns give

\[
h_\parallel=
\begin{pmatrix}-1&-1\\-1&0\end{pmatrix},
\qquad
\det h_\parallel=-1,
\qquad
\phi_{\rm pair}=0.
\tag{11}
\]

Their transverse screen projection is

\[
W_\parallel=0,
\tag{12}
\]

whereas the angular columns give

\[
\mathcal D=\lambda I_2.
\tag{13}
\]

For every `lambda>0`, (12) has rank zero and (13) has rank two. Therefore G108's literal same-`W`
soldering is not the canonical point-observer sky construction.

The full pullback remains regular away from the vertex:

\[
F^*\eta=
\begin{pmatrix}
-1&-1&0&0\\
-1&0&0&0\\
0&0&\lambda^2&0\\
0&0&0&\lambda^2
\end{pmatrix}.
\tag{14}
\]

The coordinate degeneration at `lambda=0` is precisely the collapse of all sky directions at one
observer event, not a failure of the relation.

## 6. Vertex data and metric propagation

Because every angular direction starts at the same observer event,

\[
\mathcal D(0)=0.
\]

The derivative `D_lambda^perp D(0)` is the sky-tangent-to-screen basis-identification map. It is
fixed by unit-sky calibration and `g(k,u)=-1`, and is written

\[
D_\lambda^\perp\mathcal D(0)=I_2
\tag{15}
\]

only in matched orthonormal sky and parallel-screen bases, up to passive `O(2)`. Hence a
point-observer query has no independent initial screen
amplitude. This statement does not apply to an extended source or a general finite beam.

Since all four columns derive from one `F`, mixed partials commute and torsion freedom gives

\[
\nabla_KJ_A=\nabla_{J_A}K.
\tag{16}
\]

With `\nabla_K K=0`, curvature supplies

\[
(D_\lambda^\perp)^2\mathcal D
+\mathcal R_\perp\mathcal D=0.
\tag{17}
\]

Thus the pair and angular blocks are coupled by one immersion and one metric, without being the
same block.

## 7. Full expansion, shear, and caustics

Where `det(D) != 0`, the covariant optical matrix is

\[
\mathfrak B_\lambda
=(D_\lambda^\perp\mathcal D)\mathcal D^{-1}.
\tag{18}
\]

Its trace is screen-area expansion and its symmetric trace-free part is shear. The analytic control

\[
\mathcal D=\operatorname{diag}(\sin\lambda,\lambda),
\qquad
\mathcal R_\perp=\operatorname{diag}(1,0)
\tag{19}
\]

has nonzero shear and exactly satisfies (17). Therefore the correction retains the full `2x2`
orchestra; it does not impose isotropy.

For positive isotropic screen curvature,

\[
\mathcal D=\sin\lambda\,I_2.
\]

At `lambda=pi`, the second-order Jacobi map and its derivative remain finite while `det(D)=0` and
the Riccati matrix diverges. The caustic is a branch event of the exponential map, not a failure to
be filtered out.

## 8. Corrected G109 join

On a common branch of the one full relation, terminal depth and sky propagation share `lambda` but
come from distinct blocks. Wherever

\[
\dot\phi_{\rm pair}\ne0,
\]

the lawful depth-parameterized optical matrix is

\[
\mathfrak B_\phi
=\frac{\mathfrak B_\lambda}{\dot\phi_{\rm pair}},
\qquad
a_{\rm eff}=\frac12\operatorname{tr}\mathfrak B_\phi
=\frac{1}{2}\frac{d\log|\det\mathcal D|}{d\phi_{\rm pair}}.
\tag{20}
\]

This is a chain rule joining distinct blocks of the same `F`; it is not their identification.

The flat control has

\[
\dot\phi_{\rm pair}=0,
\qquad
\frac{d}{d\lambda}\log|\det\mathcal D|=\frac2\lambda.
\]

Therefore terminal reciprocal depth is not a universal propagation coordinate. On such an
interval, (18) remains the regular description while (20) is undefined.

## 9. What became scaffolding

- `E/J` and `S/Z` redistributions that leave `E dF` fixed are representative freedom.
- The observer and requested channel are measurement inputs, not a physical selector the metric
  owes.
- For the point-observer query, arbitrary `J`, arbitrary initial screen amplitude, and a preferred
  local branch cease to be independent inputs: `dF`, (15), and the exponential initial-value
  problem determine them.
- The observer's time-dependent celestial trivialization remains query data; it controls `F_tau`
  and must not be inferred from one isolated direction.
- Global endpoint comparisons may have several exponential preimages. Their set is metric-derived;
  source occupancy and observational weights are not.
- The physical complete metric history remains genuinely supplied and open.

## 10. Bounded landing

```text
OBSERVER_EXPONENTIAL_FULL_DIFFERENTIAL_RECONSTRUCTION_DERIVED_CONDITIONALLY
__TERMINAL_PAIR_AND_SKY_JACOBI_ARE_DISTINCT_BLOCKS
__POINT_VERTEX_SCREEN_DATA_FIXED_UP_TO_GAUGE
__LOCAL_BRANCH_ATLAS_METRIC_DERIVED
__G108_G109_LITERAL_SAME_W_SOLDERING_REQUIRES_REGRADING
__PHYSICAL_METRIC_HISTORY_GENERAL_QUERY_GLOBAL_WEIGHTS_AND_SOURCES_OPEN
```

This is a type correction and local geometric reconstruction. It is not a history-selection law or
an observational prediction.
