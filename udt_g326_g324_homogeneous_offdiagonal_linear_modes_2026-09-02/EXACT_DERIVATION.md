# G326 exact derivation — homogeneous off-diagonal modes around G324

Date: 2026-09-02
Status: `INTERNAL_VERIFIED_PENDING_EXTERNAL_REVIEW`

## 1. Bounded question

On every registered compact G324 Taub quotient, classify the complete spatially homogeneous
off-diagonal synchronous first variation of

\[
S_{ab}:=R_{ab}-\frac14R g_{ab}=0.
\tag{1}
\]

The background in proper time and fixed quotient coordinates is

\[
g_0=-dT^2+\sum_{i=1}^3 C_i^2T^{2p_i}(dx^i)^2,
\qquad
(p_1,p_2,p_3)=\left(-\frac13,\frac23,\frac23\right).
\tag{2}
\]

Let

\[
g_{ij}=\epsilon k_{ij}(T)+O(\epsilon^2),\qquad i<j,
\tag{3}
\]

with `k_12`, `k_13`, and `k_23` arbitrary before solving. Diagonal modes are absent from this
sector and were classified separately in G325.

## 2. Direct matrix-metric equation

For any homogeneous spatial metric matrix `gamma(T)` in synchronous gauge, set

\[
K=\frac12\dot\gamma,
\qquad
\theta=\operatorname{tr}(\gamma^{-1}K).
\]

A direct Christoffel calculation gives

\[
R_{00}
=-\frac12\operatorname{tr}(\gamma^{-1}\ddot\gamma)
+\frac14\operatorname{tr}(\gamma^{-1}\dot\gamma\gamma^{-1}\dot\gamma),
\tag{4}
\]

\[
R_{0i}=0,
\qquad
R_{ij}=\frac12\ddot\gamma_{ij}
+\frac14\operatorname{tr}(\gamma^{-1}\dot\gamma)\dot\gamma_{ij}
-\frac12(\dot\gamma\gamma^{-1}\dot\gamma)_{ij}.
\tag{5}
\]

Every trace in (4) contains one background-diagonal and one first-order off-diagonal factor, so
its off-diagonal first variation vanishes. The diagonal components likewise receive no term linear
in one `k_ij`. Hence

\[
\delta R_{00}=\delta R_{0i}=\delta R_{ii}=0,
\qquad
\boxed{\delta R=0}.
\tag{6}
\]

There is therefore no new connected-scalar mode in this sector. Linearizing (5) for each `i<j`
gives the decoupled Euler equation

\[
\boxed{
\ddot k_{ij}
+\frac{1-2(p_i+p_j)}{T}\dot k_{ij}
+\frac{4p_ip_j}{T^2}k_{ij}=0
}.
\tag{7}
\]

The independent verifier reconstructs the complete Christoffel, Riemann, Ricci, scalar, and
trace-free tensors without importing (7).

## 3. Complete solution

For `k=T^m`, the characteristic polynomial is

\[
F_{ij}(m)=m^2-2(p_i+p_j)m+4p_ip_j
=(m-2p_i)(m-2p_j).
\tag{8}
\]

Thus

\[
k_{12}=A_{12}C_1^2T^{-2/3}+B_{12}C_2^2T^{4/3},
\tag{9}
\]

\[
k_{13}=A_{13}C_1^2T^{-2/3}+B_{13}C_3^2T^{4/3}.
\tag{10}
\]

The transverse roots coincide because `p_2=p_3`. Differentiating the power solution with respect
to `m` supplies the indispensable repeated-root solution:

\[
k_{23}=T^{4/3}\left[L_{23}+2C_2C_3q_\times
\log\frac{T}{T_{\rm ref}}\right].
\tag{11}
\]

Changing `T_ref` shifts `L_23` and creates no additional constant. Equations (9)--(11) are the
general solutions of three second-order equations, so the sector has exactly six integration
constants.

## 4. Five cover-coordinate modes become quotient-lattice modes

On the universal cover let

\[
\xi^a=A^a{}_b x^b,
\tag{12}
\]

with constant `A`. Then

\[
(\mathcal L_\xi g_0)_{ij}
=(g_0)_{jj}A^j{}_i+(g_0)_{ii}A^i{}_j.
\tag{13}
\]

The two solutions in each of (9) and (10) are obtained independently from `A^1{}_2`, `A^2{}_1`,
`A^1{}_3`, and `A^3{}_1`. The constant term in (11) is obtained from the one combination

\[
C_2^2A^2{}_3+C_3^2A^3{}_2.
\tag{14}
\]

The orthogonal combination is the infinitesimal transverse rotation, a Killing generator of the
locally LRS cover, and has zero metric image. The off-diagonal image of constant linear cover
changes therefore has rank five.

These vectors do not descend as infinitesimal gauge on the fixed quotient. If `x^b` has period
`L_b`, then

\[
\xi^a(x^b+L_b)-\xi^a(x^b)=A^a{}_bL_b.
\tag{15}
\]

A nonzero affine generator is not single-valued on `T3`; the connected tangent of the discrete
lattice-automorphism group is also zero. The five modes are consequently locally isometric cover
changes but globally distinct fixed-quotient lattice/frame attachments. They are not local
curvature modes, not legal fixed-quotient gauge, and not an observed ruler scale.

Including G325's three diagonal lattice constants, the complete constant-linear cover map has rank
eight and the single transverse-rotation kernel. Thus the registered homogeneous family carries
eight lattice/frame moduli at first order.

## 5. The logarithmic mode is local shear

Normalize the logarithmic coefficient as in (11). The direct Riemann reconstruction gives the
off-diagonal mixed tidal operator on the background transverse orthonormal plane:

\[
\boxed{
\delta E^{\hat y}{}_{\hat z}
=\delta E^{\hat z}{}_{\hat y}
=-\frac{q_\times}{3T^2}
}.
\tag{16}
\]

The constant transverse lattice mode gives zero in this mixed tidal channel. More generally, G325's
diagonal shear `q_+` and the new cross shear assemble as

\[
\delta E_{\perp}^{\rm TF}
=-\frac{1}{3T^2}
\begin{pmatrix}
q_+ & q_\times\\
q_\times & -q_+
\end{pmatrix}.
\tag{17}
\]

The transverse eigenvalue split is therefore

\[
\frac{2}{3T^2}\sqrt{q_+^2+q_\times^2}.
\tag{18}
\]

This is an intrinsic curvature change, not Lie transport: the background tidal operator is
degenerate on the transverse plane, so its commutator with an infinitesimal transverse basis change
vanishes, whereas (16) does not. Equivalently, (11)'s logarithmic term is the cross component of a
tangent to the exact matrix-Kasner family.

The two components `(q_+,q_cross)` are linearly independent in the fixed marked quotient problem.
The local background `O(2)` isotropy rotates them, so they are not two independent unmarked scalar
magnitudes; their invariant local magnitude is the square root in (18). A generic fixed lattice
does not make that continuous cover rotation into quotient gauge.

## 6. Residual gauge and combined census

A quotient-legal homogeneous synchronous residual vector has constant time component plus spatial
translations. The time translation produces G325's diagonal `1/T` mode; spatial translations are
Killing and produce no metric perturbation. Periodic nonzero Fourier generators do not preserve the
homogeneous sector, and affine spatial generators fail (15). Therefore G326 adds no legal gauge
mode.

Combining the complete decoupled diagonal and off-diagonal sectors gives exactly twelve integration
constants in the fixed marked synchronous problem:

| Class | Dimension |
|---|---:|
| residual time-origin gauge | 1 |
| quotient lattice/frame moduli | 8 |
| local Kasner-shear components | 2 |
| connected scalar-curvature variation | 1 |
| total | 12 |

This is a linear solution-space count, not a physical population or probability count.

## 7. Time behavior and bounded validity

On every compact interval `0<T_min<=T<=T_max<infinity`, the perturbation is controlled by choosing
`epsilon` so that the normalized cross-terms remain small. Globally:

- the `T^-2/3` and `T^4/3` cover modes have normalized amplitudes proportional to `T^-1` or `T`
  in the mixed axial/transverse planes;
- the transverse lattice mode has constant normalized amplitude;
- the local cross shear has logarithmic normalized amplitude and is not uniformly small at either
  logarithmic endpoint.

The lattice modes have exact finite quotient deformations beyond their nonuniform linear
representation, but that does not make the chosen diagonal quotient uniformly stable. No endpoint-
uniform, full linear, or nonlinear stability statement follows.

## 8. Bounded landing

```text
HOMOGENEOUS_OFFDIAGONAL_MODES_CLOSE_AS_FIVE_QUOTIENT_LATTICE_MODULI
__ONE_LOCAL_TRANSVERSE_KASNER_SHEAR__NO_NEW_GAUGE_OR_SCALAR_MODE
__NO_FULL_STABILITY_CLAIM
```

Together G325 and G326 close the complete spatially homogeneous synchronous first variation of the
registered G324 background. Every nonzero Fourier mode, general inhomogeneous gauge, nonlinear mode
coupling, endpoint-uniform control, other quotient/topology, physical occupancy, scale, matter/mass,
observation, history selection, and physical `X_max` remain open. No UDT metric, reciprocal-kernel,
angular-sector, or adopted field-equation formula changed.
