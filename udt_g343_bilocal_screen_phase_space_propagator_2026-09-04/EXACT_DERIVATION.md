# G343 exact derivation — bilocal screen phase-space propagation

Date: 2026-09-04
Grade: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Bounded landing

```text
FULL_BILOCAL_PHASE_SPACE_PROPAGATOR_CLOSES__EXACT_COMPOSITION_SYMPLECTICITY
__COMMON_AFFINE_INVERSE_AND_SOURCE_NORMALIZED_FREQUENCY_RECIPROCITY
__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED
__NO_LUMINOSITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED
```

G343 selects preregistered alternatives `A`, `C1`, `W1`, `R1`, `P1`, and `Q1`. This is an exact
geometric result on one supplied G341/G342 spacetime and its supplied labelled null rays. The
metric, completed-pair kernel, angular sector, and provisional equation are unchanged.

## 1. Exact ray in a dimensionally typed projective chart

Use

\[
 g=-dT^2+a(T)^2dX^2+b(T)^2(dY^2+dZ^2),
 \qquad a=C_XT^{-1/3},\quad b=C_\perp T^{2/3},\quad T>0.
\tag{1}
\]

G341 supplies the invariant direction parameter

\[
 \lambda={C_Xp_\perp\over C_\perp|p_X|}.
\tag{2}
\]

Because `lambda` has the same dimension as `T`, a regular direction chart must compare it with an
event time rather than add unlike momentum components. Mark any supplied reference event `T_*` on
the same ray and write

\[
 \rho={T_*^2\over T_*^2+\lambda^2}\in[0,1],
 \qquad \nu=\left.{dT\over ds}\right|_{T_*}>0,
\tag{3}
\]

where `s` is one affine parameter held fixed along the full ray. Define

\[
 H(T)=\sqrt{\rho T^2+(1-\rho)T_*^2}.
\tag{4}
\]

Then the fixed-affine ray rate and metric-derived parallel-screen tide are

\[
 \boxed{\alpha(T)={dT\over ds}
 =\nu T_*^{-1/3}T^{-2/3}H(T)},
\tag{5}
\]

\[
 \boxed{\mathcal T=\operatorname{diag}(-q,+q)},\qquad
 \boxed{q(T)={2\nu^2T_*^{4/3}(1-\rho)\over3T^{10/3}}\ge0}.
\tag{6}
\]

Equation (6) is the G342 curvature tide rewritten in the regular chart. The independent verifier
rebuilt it from the coordinate metric two-jet, Christoffels, and Riemann tensor rather than defining
it from the propagator.

## 2. Two exact scalar bases

The two screen components obey

\[
 \ddot\xi_\parallel-q\xi_\parallel=0,
 \qquad
 \ddot\xi_Z+q\xi_Z=0,
\tag{7}
\]

where a dot is `d/ds`. Direct substitution gives one everywhere-positive solution in each sector:

\[
 y_\parallel(T)=T^{-1/3}H(T),
 \qquad y_Z(T)=T^{2/3}.
\tag{8}
\]

Their affine logarithmic derivatives are

\[
 \mu_\parallel={\dot y_\parallel\over y_\parallel}
 =\alpha\left({\rho T\over H^2}-{1\over3T}\right),
 \qquad
 \mu_Z={\dot y_Z\over y_Z}={2\alpha\over3T}.
\tag{9}
\]

Reduction of order is exact because

\[
 {ds\over y_\parallel^2}
 ={T_*^{1/3}\over\nu}{T^{4/3}\over H^3},dT,
 \qquad
 {ds\over y_Z^2}
 ={T_*^{1/3}\over\nu}{T^{-2/3}\over H},dT.
\tag{10}
\]

For arbitrary positive endpoints define the signed integrals

\[
 I_\parallel(T_1,T_0)
 =\int_{T_0}^{T_1}{u^{4/3}\over H(u)^3},du,
 \qquad
 I_Z(T_1,T_0)
 =\int_{T_0}^{T_1}{u^{-2/3}\over H(u)},du,
\tag{11}
\]

and the bilocal position blocks

\[
 \boxed{B_j(T_1,T_0)
 ={T_*^{1/3}\over\nu}y_j(T_1)y_j(T_0)I_j(T_1,T_0)}.
\tag{12}
\]

They are positive for `T_1>T_0`, vanish only at coincident endpoints, and obey

\[
 \boxed{B_j(T_0,T_1)=-B_j(T_1,T_0)}
\tag{13}
\]

in the same parallel screen basis and affine gauge.

## 3. Complete four-by-four propagator

For either scalar sector put `r_j=y_j(T_1)/y_j(T_0)`. The exact two-by-two phase-space map is

\[
 M_j(T_1,T_0)=
 \begin{pmatrix}A_j&B_j\\C_j&D_j\end{pmatrix},
\tag{14}
\]

\[
 \boxed{
 A_j=r_j-\mu_j(T_0)B_j,
 \qquad
 D_j=r_j^{-1}+\mu_j(T_1)B_j,
 }
\tag{15}
\]

\[
 \boxed{
 C_j=\mu_j(T_1)r_j-\mu_j(T_0)D_j.
 }
\tag{16}
\]

In state order `(xi_parallel,xi_Z,dot_xi_parallel,dot_xi_Z)`, assemble

\[
 \boxed{
 M(T_1,T_0)=
 \begin{pmatrix}
 A_\parallel&0&B_\parallel&0\\
 0&A_Z&0&B_Z\\
 C_\parallel&0&D_\parallel&0\\
 0&C_Z&0&D_Z
 \end{pmatrix}.}
\tag{17}
\]

No screen component is deleted. The zeros follow from the metric's transverse axial reflection in
the G341 parallel screen; an implementation-distinct direct-curvature calculation confirmed the
off-diagonal tide is zero.

## 4. Wronskian, symplecticity, and composition

Let

\[
 Q_j(T)={T_*^{1/3}\over\nu}\int^T w_j(u),du,
\tag{18}
\]

where the two weights are the integrands in (11). An exact unit-Wronskian fundamental basis is

\[
 F_j(T)=
 \begin{pmatrix}
 y_j&y_jQ_j\\
 \mu_jy_j&\mu_jy_jQ_j+y_j^{-1}
 \end{pmatrix},
 \qquad \det F_j=1.
\tag{19}
\]

Equations (14)--(16) are exactly

\[
 M_j(T_1,T_0)=F_j(T_1)F_j(T_0)^{-1}.
\tag{20}
\]

Consequently

\[
 \boxed{M(T_2,T_0)=M(T_2,T_1)M(T_1,T_0)}
\tag{21}
\]

for every positive endpoint triple on the same ray with the same affine gauge and path label.
Also `A_jD_j-B_jC_j=1`. With

\[
 J=\begin{pmatrix}0&I_2\\-I_2&0\end{pmatrix},
\tag{22}
\]

the full result is

\[
 \boxed{M^TJM=J},\qquad \boxed{\det M=1}.
\tag{23}
\]

This is preservation of the canonical screen Wronskian. It is geometric phase-space transport,
not a statistical, quantum, or electromagnetic assertion.

## 5. Reference-event covariance and the absence of a hidden scale

Choose another supplied point `T_*'` on the same ray while keeping `lambda` and the affine tangent
fixed. The converted coordinates are

\[
 \rho'={T_*'^2\over T_*'^2+\lambda^2},
 \qquad \nu'=\alpha(T_*').
\tag{24}
\]

Substitution in (4)--(17) leaves `alpha`, `q`, and the complete propagator invariant:

\[
 \boxed{M(T_1,T_0;T_*,\rho,\nu)
 =M(T_1,T_0;T_*',\rho',\nu')}.
\tag{25}
\]

Production tested (25) across all mixed, near-axis, and exact principal cases; the maximum relative
error was `1.7763568394002505e-14`. The independent implementation obtained
`1.2434497875801753e-14`. Thus `T_*` is a chart reference, not a selected scale.

The first discarded implementation hid `T_*=1` and was not banked. The preserved execution note
records that dimensional failure and the subsequent old-chart conversion repair.

## 6. Affine gauge and endpoint-normalized reciprocity

If the same affine tangent is rescaled by `nu -> a nu`, define

\[
 S_a=\operatorname{diag}(I_2,aI_2).
\tag{26}
\]

Then

\[
 \boxed{M_{a\nu}=S_aM_\nu S_a^{-1}}.
\tag{27}
\]

This is a change of derivative units: `A,D` are invariant, `B` scales by `a^{-1}`, and `C` scales
by `a`. In one common affine gauge endpoint reversal is simply

\[
 \boxed{M(T_0,T_1)=M(T_1,T_0)^{-1}}.
\tag{28}
\]

Now let each endpoint separately choose unit normal-observer frequency. The required reference
frequencies are

\[
 \nu_i={T_*^{1/3}T_i^{2/3}\over H(T_i)}.
\tag{29}
\]

For a ray normalized at endpoint `0`, the metric frequency ratio at endpoint `1` is

\[
 \alpha_{01}={\omega(T_1)\over\omega(T_0)}={\nu_0\over\nu_1}.
\tag{30}
\]

Put `a=nu_1/nu_0=alpha_01^{-1}`. The separately normalized reverse map is not the bare inverse in
unchanged derivative units; it is the typed conjugate

\[
 \boxed{
 M^{[1]}(T_0,T_1)
 =S_a\,[M^{[0]}(T_1,T_0)]^{-1}S_a^{-1}.}
\tag{31}
\]

In particular its position block obeys

\[
 \boxed{B^{[1]}(T_0,T_1)
 =-\alpha_{01}\,[B^{[0]}(T_1,T_0)]^T.}
\tag{32}
\]

The factor in (32) is not a repair or new optical law. It is forced by resetting the affine
derivative unit at the opposite endpoint and is the same metric frequency ratio already present in
G340/G342. Multiplying independently source-normalized vertex maps without (31) is ill typed.

## 7. Recovery of G342 and both principal limits

Set `T_*=T_0` and `nu=1`. Then

\[
 \rho={T_0^2\over T_0^2+\lambda^2},
\tag{33}
\]

and the two entries of the position block in (17) reduce exactly to G342's
source-normalized widths. The production old-chart comparison reached a maximum relative difference
of `9.662469068589168e-16` after the dimensionally required factor in (33) was restored.

On the longitudinal family `rho=1`, `q=0` and both scalar maps are the free propagator

\[
 \boxed{M_\parallel=M_Z=
 \begin{pmatrix}1&\Delta s\\0&1\end{pmatrix}},
 \qquad
 \Delta s={3T_*^{1/3}\over2\nu}
 (T_1^{2/3}-T_0^{2/3}).
\tag{34}
\]

On the transverse family `rho=0`, put `kappa_perp=nu T_*^{2/3}`. Two exact bases are

\[
 (T^{-1/3},T^2)\quad\hbox{for the parallel-screen sector},
 \qquad
 (T^{2/3},T)\quad\hbox{for the azimuthal sector},
\tag{35}
\]

with affine derivative `d/ds=kappa_perp T^{-2/3}d/dT`. Their fundamental matrices have nonzero
constant Wronskians and reproduce (14)--(17) exactly. Both principal phase spaces therefore retain
rank four. The maximum production principal-limit difference was
`3.228398296572961e-14`.

## 8. Compact path labels

Each supplied compact-lattice lift `L` determines its own invariant `lambda_L`, direction chart,
arrival point, parallel screen, and propagator

\[
 M_L(T_1,T_0).
\tag{36}
\]

Equation (21) composes segments of that same lifted ray. It does not identify, sum, weight, or
select distinct lifts. Quotient multiplicity remains path-labelled, exactly as in G340--G342.

## 9. Evidence and ownership

The corrected production route passed `8888/8888` checks. Its maximum composition,
symplectic, common-affine reversal, reference-event covariance, G342 recovery, and principal-limit
relative errors were respectively
`1.3247134512261843e-14`, `8.881784197001252e-16`,
`5.684341886080802e-14`, `1.7763568394002505e-14`,
`9.662469068589168e-16`, and `3.228398296572961e-14`.

An implementation-distinct verifier rebuilt the coordinate metric two-jet and screen curvature,
integrated the full first-order phase-space equation in log time by RK4, and compared it with a
separately assembled unit-Wronskian basis. It imported neither production nor G341/G342 code and
passed `2960/2960`. Its maximum curvature, ODE-map, composition, reversal, symplectic, and
reference-event covariance errors were `3.039235529911366e-15`,
`1.4629478184424727e-12`, `8.048941603813503e-12`,
`9.734435479913373e-12`, `6.439293542825866e-15`, and
`1.2434497875801753e-14`. Thirteen hostile mutations were all caught by the baseline validator.

This is a metric-native geometric propagator conditional on the supplied spacetime, ray, endpoint
basis, affine gauge, and compact path label. It does not provide luminosity, electromagnetic
transfer, emission, detection, observational distance, physical route or population, topology or
occupancy selection, generic stability, matter/mass, a physical scale, `X_max`, or canon.

Fresh external `gpt-5.4` review authenticated all 29 sealed payloads, replayed the registered
`19/19` package gates, ran a separate scratch reconstruction, found no issue at any severity, and
returned `ACCEPT_G343_BOUNDED_BILOCAL_SCREEN_PHASE_SPACE_PROPAGATOR`. The bounded grade is therefore
`EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`.
