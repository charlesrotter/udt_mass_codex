# G303 exact derivation — nonlinear Cauchy and lawful-data classification

Date: 2026-08-30

## 1. Bounded landing

```text
BOTH_G301_CLASSES_HAVE_THE_SAME_LOCAL_CAUSAL_PRINCIPAL_SYSTEM
__TRACEFREE_DATA_ARE_THE_UNION_OVER_ONE_CONSTANT_SCALAR_DATUM
__WELLPOSEDNESS_DOES_NOT_SELECT
```

Status: `INTERNALLY_DERIVED_AND_IMPLEMENTATION_INDEPENDENTLY_VERIFIED_BOUNDED_LOCAL_CLASSIFICATION`.

This result is conditional on G301's candidate local metric-only lane. It does not adopt either
residual as UDT dynamics and does not select a realized history.

## 2. Frozen residual classes

G301 leaves

\[
\mathcal E^{(0)}_{ab}=R_{ab}=0
\]

and

\[
\mathcal E^{(T)}_{ab}=S_{ab}
=R_{ab}-\frac14R g_{ab}=0.
\]

Both equations act on the complete four-dimensional Lorentzian metric. Harmonic coordinates below
are a gauge method for exposing the PDE type, not preferred physical coordinates.

## 3. Exact nonlinear completion of the trace-free class

The contracted Bianchi identity is

\[
\nabla^aR_{ab}=\frac12\nabla_bR.
\]

Therefore

\[
\nabla^aS_{ab}=\frac14\nabla_bR.
\]

On a connected solution region, `S_ab=0` implies

\[
\nabla_bR=0.
\]

Define the solution datum

\[
\Lambda=\frac R4.
\]

Then `Lambda` is constant and the complete nonlinear equation is equivalently

\[
\boxed{R_{ab}=\Lambda g_{ab},\qquad d\Lambda=0.}
\]

No independent `Lambda` field or cosmological interpretation has been introduced. This is the
integrability completion of the frozen trace-free residual. The generic class is precisely its
`Lambda=0` sector.

The raw trace-free operator has nine algebraic output directions. The tenth direction is not a
free local metric mode: it is the connected-region constant above.

## 4. Cauchy constraints derived from the metric equations

Let `Sigma` be a spacelike slice with induced metric `gamma_ij`, unit normal `n`, second
fundamental form `K_ij`, spatial scalar curvature `R3`, and spatial derivative `D`. Set

\[
\mathcal H=R3+K^2-K_{ij}K^{ij},
\]

\[
\mathcal M^i=D_j(K^{ij}-\gamma^{ij}K).
\]

Gauss--Codazzi gives

\[
G_{ab}n^an^b=\frac12\mathcal H,
\qquad
G_{ab}n^a\gamma^{bi}=\mathcal M^i.
\]

For `R_ab=Lambda g_ab` in four dimensions, `R=4 Lambda` and

\[
G_{ab}=-\Lambda g_{ab}.
\]

Since `g(n,n)=-1` and `g(n,e_i)=0`, the constraints are exactly

\[
\boxed{\mathcal H=2\Lambda,\qquad \mathcal M^i=0.}
\]

Thus:

- generic Ricci-flat data obey `H=0` and `M=0`;
- trace-free data obey `M=0` and `H` spatially constant;
- without presupplying a value, the data determine `Lambda=H/2`;
- on a connected slice the same data cannot belong to two different `Lambda` sectors.

This is not an arbitrary profile. It is one number carried by each connected development.

## 5. Nonlinear principal and gauge propagation structure

In harmonic coordinates, the reduced Ricci tensor has principal part

\[
(R_{ab})_{\mathrm{principal}}
=-\frac12g^{cd}\partial_c\partial_dg_{ab}.
\]

For fixed constant `Lambda`, the term `Lambda g_ab` has no metric second derivatives. Hence the
Ricci-flat class and each **Bianchi-completed fixed-`Lambda` sector** have the same ten-component
metric principal operator and the same characteristic equation

\[
\boxed{g^{cd}\xi_c\xi_d=0.}
\]

The causal cone is therefore the supplied metric cone in both classes. The raw trace-free symbol
is the rank-nine output projection of this operator. Bianchi completion plus the initial-data value
of `Lambda` restores the full fixed-sector metric wave system; it does not add a propagating scalar.

The divergence of the harmonic-reduced equation gives the usual homogeneous wave equation for the
gauge-constraint covector, with curvature-dependent lower-order terms. Constancy of `Lambda`
prevents a source term. Vanishing gauge constraint and normal derivative on the initial slice are
therefore preserved by the reduced evolution.

Consequently, conditional on the imported standard harmonic-gauge quasilinear-wave and
gauge-constraint-propagation theorems, each fixed-`Lambda` constraint surface has a local smooth
development unique up to diffeomorphism. G303 verifies the hypotheses supplied by the two
residuals; it does not prove those general PDE theorems or global existence.

## 6. Exact lawful-data comparison

For a fixed initial three-manifold and a fixed value of `Lambda`, the functional data in both
classes are the same:

- six functions in `gamma_ij`;
- six functions in `K_ij`;
- four geometric constraints: `M_i=0` and `H=2 Lambda`;
- four coordinate freedoms, represented by lapse/shift or harmonic gauge data.

The trace-free class has no additional free function. Its data space is

\[
\boxed{\mathscr C_T=\bigsqcup_{\Lambda\in\mathbb R}\mathscr C_\Lambda,}
\]

where `C_Lambda` is the metric-data constraint surface `H=2 Lambda`, `M=0`. The generic class is

\[
\boxed{\mathscr C_0\subset\mathscr C_T.}
\]

If `Lambda` is not supplied before the data are given, the equivalent lawful-data statement is

\[
\boxed{\mathcal M_i=0,\qquad D_i\mathcal H=0,\qquad
\Lambda=\mathcal H/2.}
\]

Thus the union carries one constant per connected component. Spatial constancy is a compatibility
condition on the metric data, not an additional scalar function or normal-derivative datum.

The exact connected-graph replay gives rank `N` for `H_i=0` at `N` sampled points and rank `N-1`
for `H_i-H_0=0`. The one-dimensional nullspace is the constant vector. This finite certificate
tracks one connected modulus rather than a hidden function.

## 7. Reciprocal structure does not add a Cauchy equation

The completed pair pullback and reciprocal readouts evaluate any supplied evolved metric. The
registered chain is pointwise and definitional:

\[
h=F^*g=J^TgJ,
\quad m=\sqrt{-\det h},
\quad \Phi=-\frac12\log(-h_{00}),
\quad \delta_{AB}=\Phi_B-\Phi_A,
\quad \chi_{AB}=\tanh\delta_{AB}.
\]

`verify_kernel_no_evolution_residual.py` constructs these formulas at two generic endpoints and
computes their Jacobian with respect to an independent formal second-normal metric jet. Its exact
rank is zero. The formulas depend on the supplied pair-metric entries but generate no independent
normal-normal, normal-tangential, Cauchy, or evolution residual. This is a bounded dependency
theorem for the registered readouts, not a claim that no future UDT law could couple relations to
evolution.

G302's static family is a regression witness: its `R0` equals `4 Lambda`, and its Ricci-flat member
is the `Lambda=0` sector. G303 does not promote that static chart to the complete time-live theory.

## 8. Exact conclusion and remaining fork

Conditional use of the standard local causal well-posedness theorem does not select between the
Ricci-flat class and the Bianchi-completed fixed-`Lambda` sectors. It narrows the difference to one
question:

```text
Must the connected-region scalar datum be zero, or may lawful initial data set it?
```

Current postulates, reciprocal identities, and metric-causal propagation answer neither way.
This is a finite zero-mode/data fork, not the earlier unrestricted-profile underdetermination.

G303 does not derive a field equation, boundary law, source, mass, matter sector, observation,
physical query population, global completion, realized history, scale, or `X_max`.
