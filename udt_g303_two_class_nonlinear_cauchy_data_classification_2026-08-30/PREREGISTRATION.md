# G303 preregistration

Date: 2026-08-30
Question class: `METRIC_LED_BOUNDED_NONLINEAR_EVOLUTION_CLASSIFICATION`

## Frozen questions

For each surviving G301 residual class, determine:

1. its exact nonlinear differential consequences under the contracted Bianchi identity;
2. its reduced principal operator in harmonic coordinates;
3. its normal-normal and normal-tangential Cauchy constraints derived by Gauss--Codazzi;
4. the full lawful local initial-data family, including finite connected-region moduli;
5. whether local causal well-posedness or data burden selects one class;
6. whether completed reciprocal structure supplies any additional evolution equation.

No residual is adopted as UDT dynamics by this test.

## Preregistered candidate derivation

### Generic class

The generic G301 equivalence class is expected to reduce exactly to

\[
R_{ab}=0.
\]

On a spacelike slice with induced metric `gamma`, second fundamental form `K`, spatial scalar
curvature `R3`, and spatial derivative `D`, the expected constraints are

\[
R3+K^2-K_{ij}K^{ij}=0,
\qquad
D_j(K^{ij}-\gamma^{ij}K)=0.
\]

### Trace-free class

The exceptional class is expected to imply on each connected solution region

\[
dR=0,
\qquad
R_{ab}=\Lambda g_{ab},
\qquad
\Lambda=R/4=\text{constant}.
\]

Its expected Cauchy constraints are

\[
R3+K^2-K_{ij}K^{ij}=2\Lambda,
\qquad
D_j(K^{ij}-\gamma^{ij}K)=0.
\]

Equivalently, without presupplying `Lambda`, the Hamiltonian expression must be spatially constant;
its constant half-value is the connected-region datum.

### Principal causal structure

After harmonic reduction, both fixed-`Lambda` systems are expected to have principal part

\[
-\frac12g^{cd}\partial_c\partial_d g_{ab},
\]

with `Lambda g_ab` only lower order. If correct, standard quasilinear-wave local existence and
uniqueness applies conditionally to constraint-satisfying data, up to diffeomorphism. G303 will not
claim a new proof of the general PDE theorem; it will verify that both derived residuals meet the
same principal and constraint-propagation hypotheses.

## Preregistered landings

1. `BOTH_G301_CLASSES_HAVE_THE_SAME_LOCAL_CAUSAL_PRINCIPAL_SYSTEM__TRACEFREE_DATA_ARE_THE_UNION_OVER_ONE_CONSTANT_SCALAR_DATUM__WELLPOSEDNESS_DOES_NOT_SELECT`
   - both classes reduce to quasilinear metric wave systems after gauge fixing;
   - the generic class is the zero-scalar sector;
   - the trace-free class is the union over one connected-region constant;
   - local well-posedness and completed reciprocal evaluation do not select between them.
2. `TRACEFREE_CLASS_HAS_AN_ADDITIONAL_NONCONSTANT_OR_NONCAUSAL_MODE__GENERIC_CLASS_SELECTED_BY_WELLPOSEDNESS`
   - the exact nonlinear trace-free system carries a propagating scalar function, loses causal
     hyperbolicity, or fails constraint preservation.
3. `GENERIC_CLASS_FAILS_WHILE_TRACEFREE_CLASS_REMAINS_LOCALLY_WELLPOSED`
   - exact nonlinear reduction or constraint propagation refutes the generic class only.
4. `BOTH_CLASSES_REQUIRE_ADDITIONAL_UNOWNED_EVOLUTION_STRUCTURE`
   - neither frozen residual yields a closed local causal Cauchy system under the tested method.
5. `INTERNAL_CERTIFICATION_FAILURE`
   - algebra, provenance, independence, catch-proof, or replay gates fail.

Landing 1 would be a conditional local evolution/data classification, not a selected UDT equation
or physical history.

## Falsification contract

Landing 1 is falsified if any of the following occurs:

- `S_ab=0` does not force scalar curvature constant on connected regions;
- the trace-free class admits a nonconstant scalar mode compatible with all ten metric equations;
- either harmonic-reduced residual has a principal cone different from `g`;
- `Lambda` enters the principal symbol rather than lower order;
- direct Gauss--Codazzi projection gives different factors or signs from the registered constraints;
- constraint propagation requires a new physical field, source, action, or preferred slicing;
- trace-free lawful data require a free function beyond `gamma`, `K`, gauge, and one constant;
- completed reciprocal identities impose an additional nonidentity evolution constraint.

## Required exact and hostile checks

1. Re-derive the Bianchi identities for both residuals and reject a spacetime-varying `Lambda`.
2. Derive the constraint factors from normal projections and check the `Lambda=0` nesting.
3. Show that the trace-free data space is a disjoint/overlapping union over constant `Lambda`, not
   one fitted function.
4. Verify identical principal coefficient tensors for both branches at multiple exact Lorentzian
   metrics/covectors and reject Euclidean, sign-flipped, trace-dropped, and `Lambda`-derivative
   mutations.
5. Verify that reciprocal/kernel formulas are evaluators on evolved metrics and contribute no
   residual equation.
6. Characterize rather than reject data with nonzero constant Hamiltonian expression.

## Certification gates

- this preregistration is committed and pushed before production outcome files exist;
- exact symbolic or rational checks are used for identities and coefficient factors;
- an independent implementation imports no production function and uses a different route;
- hostile checks catch factor, sign, constancy, principal-symbol, nesting, and false-selection bugs;
- current 285-row premise registry and repository purity suite pass before banking;
- the conclusion remains scoped to a local boundary-free Cauchy slab and the frozen G301 lane;
- fresh zero-context adversarial review is required before externally verified status.

## Prohibited outcome-driven changes

No observational value, source, action, mass label, matter model, boundary, preferred sign,
distance attachment, `X_max`, protected work, or imported gravitational field equation may enter
after outcomes are seen.

