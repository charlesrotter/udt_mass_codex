# G316 exact derivation — lawful constraint-data construction

Date: 2026-09-01
Scope: bounded regular local G312--G315 metric-only vacuum arena

## 1. Bounded landing

```text
CONFORMAL_CONSTRUCTION_MAPS_A_LAWFUL_SUBSET_WITH_NONTRIVIAL_SOLVABILITY_AND_CORNER_GAUGE_BOUNDS
__NO_PHYSICAL_DATA_SELECTION
```

Status before external review: `INTERNALLY_DERIVED_AND_IMPLEMENTATION_DISTINCT_VERIFIED_BOUNDED`.

G316 gives one practical mathematical chart for constructing data that satisfy G315. It does not
derive which seed fields, topology, connected scalar, or null sheets Nature supplies.

## 2. Active equation and ownership

Universal Reciprocity/DDR and both G312 premises are owner-adopted provisionally, not derived or
canonized. Inside their registered regular local metric-only scale-free vacuum arena,

\[
R_{ab}=\Lambda g_{ab},\qquad d\Lambda=0
\]

on each connected region. G315 derived the spacelike constraints

\[
{}^{(3)}R+\frac23\tau^2-A_{ij}A^{ij}=2\Lambda,
\qquad
D_jA^{ij}-\frac23D^i\tau=0.
\]

The conformal method used below is a `CONDITIONAL_IMPORTED_MATHEMATICAL_METHOD`: it is a
presentation of these active constraints, not another UDT field equation.

## 3. Exact conformal construction

Choose a positive conformal factor `psi` and write, in three spatial dimensions,

\[
\gamma_{ij}=\psi^4\bar\gamma_{ij},\qquad \psi>0.
\]

Split the second fundamental form into trace and trace-free parts,

\[
K_{ij}=A_{ij}+\frac13\tau\gamma_{ij},
\qquad A^i{}_i=0,
\]

and assign the contravariant trace-free part the standard weight

\[
A^{ij}=\psi^{-10}\bar A^{ij}.
\]

Because lowering two indices contributes `psi^8`,

\[
A_{ij}=\psi^{-2}\bar A_{ij},
\qquad
A_{ij}A^{ij}=\psi^{-12}|\bar A|_{\bar\gamma}^2.
\]

The scalar curvature transforms as

\[
{}^{(3)}R
=\psi^{-5}\left(-8\bar\Delta\psi+\bar R\psi\right).
\]

Now decompose the conformal trace-free tensor into a supplied transverse-traceless part and a
longitudinal correction,

\[
\bar A^{ij}=\bar A_{TT}^{ij}+(\bar L W)^{ij},
\]

\[
(\bar L W)^{ij}
=\bar D^iW^j+\bar D^jW^i
-\frac23\bar\gamma^{ij}\bar D_kW^k,
\qquad
\bar D_j\bar A_{TT}^{ij}=0.
\]

Substitution into the Hamiltonian constraint and multiplication by `psi^5` gives

\[
\boxed{
-8\bar\Delta\psi+\bar R\psi
-|\bar A_{TT}+\bar L W|_{\bar\gamma}^2\psi^{-7}
+\left(\frac23\tau^2-2\Lambda\right)\psi^5=0.
}
\]

The conformal divergence identity for a trace-free tensor is

\[
D_jA^{ij}=\psi^{-10}\bar D_j\bar A^{ij},
\]

whereas

\[
D^i\tau=\psi^{-4}\bar D^i\tau.
\]

Therefore the momentum constraint is

\[
\boxed{
\bar D_j(\bar L W)^{ij}
=\frac23\psi^6\bar D^i\tau.
}
\]

The powers `-7`, `5`, and `6` are forced by this three-dimensional tensor bookkeeping; they are
not fitted coefficients.

## 4. What is seed, solved, gauge, and output

One conformal construction begins with:

- a supplied conformal metric `bar gamma_ij` on a supplied topology;
- a supplied transverse-traceless tensor `bar A_TT^ij`;
- a supplied mean-curvature field `tau`;
- a supplied or lawfully inferred connected constant `Lambda`;
- supplied boundary or asymptotic conditions when the slice is not compact without boundary.

It then solves the coupled elliptic system for positive `psi` and `W`. Only after both equations
hold does it reconstruct lawful physical data `(gamma_ij,K_ij)`.

Lapse and shift are absent because they are evolution gauge, not constraint seeds. Constant mean
curvature, conformal flatness, compactness, roundness, and any sign are optional mathematical
subcases, not UDT consequences.

This decomposition also has representation redundancy: conformally related seed tuples can encode
the same physical data. It is therefore not a unique global coordinate system on the full
constraint surface.

## 5. Vector solvability and conformal-Killing degeneracy

On a compact slice without boundary, define the vector operator

\[
(\bar\Delta_LW)^i=\bar D_j(\bar L W)^{ij}.
\]

For smooth vector fields `X,W`, integration by parts gives

\[
\int X_i(\bar\Delta_LW)^i\,d\bar\mu
=-\frac12\int(\bar L X)_{ij}(\bar L W)^{ij}\,d\bar\mu.
\]

If `X` is a conformal-Killing field, `bar L X=0`. Hence a necessary Fredholm compatibility
condition for a source `J^i` is

\[
\int X_iJ^i\,d\bar\mu=0
\]

for every conformal-Killing field. When a solution exists, `W+X` is another solution and produces
the same `bar L W`. This is nonuniqueness of the auxiliary vector, not additional physical data.

For constant mean curvature, `bar D tau=0`, the source vanishes. The vector and scalar equations
decouple, but this convenient lane does not cover generic non-CMC data.

## 6. Exact scalar existence and nonexistence controls

Set

\[
C=\frac23\tau^2-2\Lambda.
\]

For constant coefficients and constant `psi`, the scalar equation becomes

\[
\bar R\psi-|\bar A|^2\psi^{-7}+C\psi^5=0.
\]

This produces exact controls.

### 6.1 Balanced TT control

If `bar R=0`, `|bar A|^2=a^2>0`, and `C>0`, then

\[
\psi^{12}=\frac{a^2}{C}
\]

gives a positive constant solution. The executable control uses `a^2=4096`, `C=1`, `psi=2`.

### 6.2 Integrated no-solution control

On a compact slice without boundary, `int bar Delta psi=0`. If `bar R=0`, `a^2>0`, and `C<=0`,
the remaining integrand

\[
-a^2\psi^{-7}+C\psi^5
\]

is strictly negative for every positive `psi`. Its integral cannot vanish. Thus this registered
seed class has no positive solution.

### 6.3 Pure-scalar constant controls

If `bar A=0` and `bar R=R_0` and `C` are constant, a nonzero constant solution requires

\[
\psi^4=-\frac{R_0}{C}>0.
\]

Opposite signs admit the registered constant roots. If instead `R_0=C=0`, every positive constant
`psi` solves the scalar equation. That continuum is an unfixed conformal/homothetic freedom; it is
not a derived physical ruler or `X_max`.

These examples prove both existence and nonexistence occur inside the same construction. They do
not replace the full global conformal-method solvability literature, which depends on conformal
class, zeros of coefficients, boundary conditions, topology, regularity, and non-CMC coupling.

## 7. Reconstruction of G315 controls

At `psi=1` the scalar equation exactly reconstructs:

1. round positive bounce: `bar R=6`, `tau=0`, `bar A=0`, `Lambda=3`;
2. flat positive slicing: `bar R=0`, `tau^2=9`, `bar A=0`, `Lambda=3`;
3. positive product time-symmetric data: `bar R=6`, `tau=0`, `bar A=0`, `Lambda=3`;
4. Berger-`S3` data: `bar R=7/2`, `tau^2=15/4`, `bar A=0`, `Lambda=3`.

Each satisfies

\[
{}^{(3)}R+\frac23\tau^2-A^2=2\Lambda.
\]

Their different spatial geometries remain different lawful data. Reconstruction is a regression
and sign check, not a population rule.

## 8. Exact null-corner gauge map

Let two smooth null hypersurfaces intersect at a spacelike screen `S`, and cross-normalize their
null normals by

\[
g(\ell,k)=-1.
\]

This leaves the local boost gauge

\[
\ell'=e^f\ell,\qquad k'=e^{-f}k.
\]

The screen metric is unchanged. The null second fundamental forms, expansions, and shears carry
opposite boost weights:

\[
\theta_{(\ell)}',\sigma^{(\ell)'}_{AB}
=e^f\theta_{(\ell)},e^f\sigma^{(\ell)}_{AB},
\]

\[
\theta_{(k)}',\sigma^{(k)'}_{AB}
=e^{-f}\theta_{(k)},e^{-f}\sigma^{(k)}_{AB}.
\]

Consequently,

\[
\theta_{(\ell)}\theta_{(k)},
\qquad
\sigma^{(\ell)}_{AB}\sigma_{(k)}^{AB}
\]

are boost invariant.

With the convention

\[
\omega_A=-k_bq_A{}^c\nabla_c\ell^b,
\]

the normal-bundle connection transforms as

\[
\omega_A' = \omega_A+D_Af,
\]

so its curl is invariant. The active mixed projection

\[
R_{ab}\ell^ak^b=-\Lambda
\]

is also boost invariant.

Cross-normalization therefore does not install a clock, ruler, physical distance, or scale. The
same-null Raychaudhuri hierarchy transports data from a corner along one sheet; it cannot generate
the independent shear/corner information on the transverse sheet. Two-sheet compatibility remains
a real part of the characteristic data problem.

## 9. Meaning of the result

G315 changed the old “missing phi profile” problem into constrained metric initial data. G316 now
shows how one may construct a substantial lawful subset of those data and where that construction
can fail or be nonunique.

The chain is

```text
supplied conformal seeds + connected Lambda + boundary/topology choices
    -> solve coupled constraint equations, if solvable
    -> lawful (gamma,K)
    -> conditional local metric development
    -> supplied observer/event germ and complete pair pullback
    -> reciprocal/projective readout
```

It is not

```text
arbitrary seeds -> automatically physical universe.
```

No physical history, topology, population, scalar magnitude, scale, source, matter/mass law,
observation, fit, or physical `X_max` is selected. Metric, reciprocal kernel, angular cancellation,
and observational interfaces are unchanged.
