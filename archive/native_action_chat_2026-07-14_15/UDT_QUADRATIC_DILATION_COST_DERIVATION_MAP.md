# Deriving quadratic dilation cost from existing UDT premises — MAP

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic DERIVE + countermodel audit; DATA-BLIND |
| Repository | `grok` at `64af120`; unrelated dirt preserved |
| Driver | DISCLOSED NON-COLD; prior action and reciprocal-resistance audits visible |
| User instruction | Attempt derivation first; do not add a postulate to make it work |
| GPU | Not used or requested |
| Banking | Forbidden pending fresh independent verification |

## 0. Exact question

Starting from the existing UDT foundation, determine whether one can derive

\[
\boxed{
\text{an exact quadratic local cost for nonuniform positional dilation, and specifically the
quadratic WR-L inverse functional.}
}
\]

Three claims must remain separate:

1. the tangent space of dilation states has an invariant quadratic line element;
2. the local field action is linear in that quadratic scalar;
3. the resulting radial action is the WR-L functional
   \[
   \mathcal I_0[A]
   =\frac12\int dr\left[r(A')^2+\frac{(A-1)^2}{r}\right].
   \]

Deriving one does not automatically derive the next.

## 1. Frozen existing premises

| Input | Status |
|---|---|
| Positional dilation | FOUNDING |
| R1: comparisons depend on depth differences | FOUNDING |
| R2: regular composition makes depth additive and residual multiplicative | DERIVED with recorded regularity |
| \(D=e^{\Delta\phi}\), \(A=e^{-2\phi}\) | DERIVED/defined with convention |
| R3: mutual reciprocity | FOUNDING; spatial-slot implementation conditional as recorded |
| Metric is the theory | Binding UDT research rule |
| Universal unattainable \(X\) | WORKING POSIT; origin/value OPEN |
| Exact pair invariant \((D+D^{-1})/2=\cosh\Delta\phi\) | DERIVED algebraic readout |
| Action existence, locality, field-space metric, measure, derivative order | OPEN |
| Orthogonal additivity of overlapping local gradients | Not an existing premise |
| “Choose lowest polynomial degree” | Not an existing premise |
| WR-L \(A=1-r/X\) | DERIVED under residual re-centering plus wall regularity |

The owner's statement that positional-dilation cost should parallel SR/acceleration dilation is
treated as a direction to derive, not permission to import an SR energy formula.

## 2. Required derivations

### Q1 — dilation-state geometry

Classify smooth positive quadratic line elements on the one-dimensional additive depth group that
are invariant under

\[
\phi\mapsto\phi+C,
\qquad
\phi\mapsto-\phi.
\]

Express the result in \(\phi\), \(A\), and \(B=1-A\).

### Q2 — full local cost

After choosing a base metric and measure, classify local first-gradient scalar costs

\[
S_F=\int d\mu\,F(Y),
\qquad
Y=\mathcal G^{ab}\partial_a\phi\partial_b\phi.
\]

Determine whether R1/R2/R3 force \(F(Y)\propto Y\).

### Q3 — reciprocal pair route

For a symmetric local kernel, take the controlled zero-range limit of

\[
\cosh(\phi(x+y)-\phi(x))-1.
\]

Track every assumption, the surviving quadratic coefficient, and the error order.  Determine
whether the exact finite-distance barrier survives the local limit.

### Q4 — WR-L comparison

Pull the invariant depth norm back to the reciprocal static metric under each clearly stated
measure/variation choice.  Compare its Euler equation directly with WR-L and with
\(\mathcal I_0[A]\).  No weak-depth approximation may be used at the wall.

### Q5 — exact selector theorem

Test whether exact additivity of costs for orthogonal local dilation gradients would force
\(F(Y)=\kappa Y\).  Determine whether that additivity is already a UDT theorem or would be the
smallest new principle.

## 3. Predeclared verdicts

- **DERIVED-EXACT:** follows from the frozen existing premises without adding action structure.
- **CONDITIONAL-DERIVED:** follows only after a named premise such as a Riemannian field-space cost,
  a local zero-range kernel, or orthogonal additivity.
- **LEADING-ORDER ONLY:** quadratic term is controlled near uniform dilation, but higher nonlinear
  terms remain allowed.
- **NOT DERIVED:** an explicit counterfunctional satisfies every frozen premise.

Do not call a tangent-space quadratic form a full nonlinear action.  Do not call a quadratic local
limit valid at the WR-L wall unless the error is uniformly controlled there.

## 4. Stop rules

1. One allowed nonlinear \(F(Y)\) defeats exact action uniqueness.
2. If the invariant state-space norm is \(d\phi^2\), do not replace it by \(dA^2\) globally without
   proving equivalence.
3. If a result depends on an even/isotropic kernel, locality limit, or nondegenerate Hessian, label
   that premise.
4. Do not use an observed mass to select a function.
5. Do not proceed to numerics unless a unique full nonlinear functional and boundary problem
   survive.

## 5. Deliverables

- `UDT_QUADRATIC_DILATION_COST_DERIVATION_RESULTS.md`
- `verify_udt_quadratic_dilation_cost.py`
- `verify_udt_quadratic_dilation_cost_out.txt`
- `UDT_QUADRATIC_DILATION_COST_VERIFY_DISPATCH.md`

