# Lovelock/Navarro theorem scope used by G259

Date checked: 2026-08-25

This is a faithful local scope statement, not a new UDT premise and not a reproduction of either
paper. It makes the one external mathematical classification used by G259 auditable inside a sealed
intake.

Primary sources:

- José Navarro, [“On second-order, divergence-free tensors,” Theorem 5.3](https://arxiv.org/abs/1306.4354).
- Alberto Navarro and José Navarro, [“Lovelock's theorem revisited”](https://arxiv.org/abs/1005.2386).

## Faithful theorem statement

Fix a smooth manifold of dimension `n` and the bundle of pseudo-Riemannian metrics of one fixed
signature. Consider smooth natural two-contravariant tensor constructions whose value at a point
depends only on the metric two-jet there and whose metric covariant divergence vanishes identically.
Navarro's Theorem 5.3 states that this real vector space has the Lovelock tensors

```text
L_0, ..., L_m,  with 2m <= n-1,
```

as a basis. Here `L_0` is the inverse metric and `L_1` is proportional, with a convention-dependent
nonzero factor, to the contravariant Einstein tensor. The theorem itself establishes that the
two-index basis tensors are symmetric; its refined statement does not need symmetry to be imposed
separately.

For `n=4`, the bound permits only `m=0,1`. Lowering both indices with the metric is a natural
isomorphism and turns the basis into `g_ab` and `G_ab`, with constant real coefficients. Therefore
the exact theorem-level conclusion used in G259 is

```text
E_ab = a G_ab + b g_ab.
```

The theorem does not say that UDT's physical parent operator belongs to this class. It classifies
the class only after its hypotheses are supplied.

## Hypothesis map

| Theorem item | G259 declaration | Premise-ledger row | Ownership in G259 |
|---|---|---|---|
| Smooth pseudo-Riemannian metrics with fixed signature and dimension | four-dimensional Lorentz metric arena | `four_dimensions` | `DECLARED_ARENA` |
| Smooth natural construction under local diffeomorphisms | diffeomorphism-natural metric operator | `diffeomorphism_naturality` | `ACCEPTANCE_REQUIREMENT` |
| Two tensor indices | rank-two parent operator | `rank_two_symmetry` | `NEW_PREMISE_CANDIDATE`; symmetry is explicit but theorem-redundant |
| Dependence only on the metric two-jet | local through second metric differential order | `locality`, `second_order` | `NEW_PREMISE_CANDIDATE` |
| Metric covariant divergence vanishes for every supplied metric | identity divergence freedom | `divergence_free` | `NEW_PREMISE_CANDIDATE` |
| Real vector-space classification | coefficients multiplying `L_0,L_1` are constants | `Lovelock_classification` | `MATHEMATICAL_METHOD` conclusion |
| Four-dimensional truncation | only `L_0,L_1` survive | `four_dimensions`, `Lovelock_classification` | `MATHEMATICAL_THEOREM` |

## Points not assumed by the theorem

- No separate polynomial or quasilinear hypothesis is inserted by G259. In Navarro's proof,
  polynomial dependence on second metric derivatives follows from naturality plus identity
  divergence freedom.
- No field equation, action, source, coupling, boundary condition, observer population, or UDT
  value law is supplied by the classification.
- The theorem does not remove the metric term. G259 removes it only afterward by conditionally
  requiring the flat quiet vacuum member to satisfy the candidate equation.
- The theorem includes the identically zero linear combination. Treating a parent equation as a
  nonidentity restriction requires the separate explicit `a != 0` gate after `b=0`.
- The theorem is insensitive to the overall nonzero normalization of `G_ab`; that normalization is
  absorbed into `a` and does not affect the vacuum zero set.

## Exact G259 ceiling after applying the theorem

The source theorem supports only this conditional implication:

```text
declared operator class + four dimensions
    -> E_ab = a G_ab + b g_ab
flat quiet vacuum member
    -> b = 0
nonidentity parent-equation gate a != 0
    -> zero(E) = zero(G)
```

Neither class membership nor the nonidentity physical parent law is derived from F1--F4, W1, or
W3. Source/history ownership remains open.
