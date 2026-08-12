# First curvature-derivative intrinsic-distribution atlas — preregistration

Date: 2026-08-12  
Branch: `grok`  
Question class: **METRIC-LED MAP**  
Computation class: CPU third-jet differential-invariant atlas; no ODE, GPU, action, source, or fit

## Whole question

The completed pointwise-curvature audit showed that Weyl/Ricci curvature recovers the registered
reciprocal/angular `2+2` split on only a proper subset of the tested complete metric jets. This
follow-up asks what intrinsic distributions and endomorphisms are supplied by the **first covariant
derivative of curvature**, without presuming that the registered split is the answer.

The audit has two symmetric obligations:

1. map every intrinsic subspace produced by the declared derivative objects; and
2. compare those subspaces with the registered pair/screen split only afterward.

Agreement, an alternative plane, rank zero/one, rank three/four, irreducibility, degeneracy, and
numerical uncertainty are all valid returns. No combination coefficient may be fitted or chosen
after outcomes.

## Exact bounded arena

Evaluate every **distinct** local metric jet from the prior curvature atlas:

- all 42 G63 `p/q/r` jets: 27 R17 and 15 complete time-live;
- all 1,176 distinct G85 A03/A04 profile-control jets;
- the three distinct G85 A05 shift-supported-taper control jets.

Total: exactly **1,221 distinct jets**. The 196 repeated A05 source identities remain provenance in
the parent atlas but are not repeated as independent derivative calculations. The zero-shift
Kruskal-local A05 subcase remains `INSUFFICIENT_OWNED_JET` and receives no invented third jet.

All points, amplitudes, profiles, and controls remain those frozen by the parent package. They are
bounded off-shell controls, not physical histories or UDT constants.

## Declared metric-natural objects

### A. Scalar-polynomial-invariant gradient distribution

At each point construct the following seven real scalar invariants:

```text
R,
tr(S^2), tr(S^3),
Re tr(Q^2), Im tr(Q^2),
Re tr(Q^3), Im tr(Q^3),
```

where `S=Ric^a_b` and `Q` is the self-dual Weyl bivector endomorphism. Their traces are frame
invariant on the oriented/time-oriented regular stratum. Compute all seven covariant gradients and
the metric-raised distribution

```text
D_SPI = span{ grad(I_A) }.
```

Only the span is used; no scalar normalization or weighted sum is introduced. Record rank,
signature when nondegenerate, and its projector when rank two. This seven-invariant family is
declared and bounded; it is not advertised as the complete scalar polynomial invariant algebra.

### B. Covariant-derivative Gram endomorphisms

Construct separately

```text
K_Riem_ab = (nabla_a R_cdef)(nabla_b R^cdef),
K_Ric_ab  = (nabla_a Ric_cd)(nabla_b Ric^cd),
K_Weyl_ab = (nabla_a C_cdef)(nabla_b C^cdef).
```

No linear combination of these tensors is allowed. For each mixed endomorphism `g^-1 K`, record
its real/complex spectrum, Jordan/rank diagnostics, whether it preserves the registered pair and
screen, and whether disjoint pair/screen spectra give an intrinsic spectral projector. Also record
whether the three endomorphisms jointly preserve the registered split and the dimension of their
generated matrix algebra as a diagnostic, not as a physical selector.

### C. Result comparison

For a rank-two `D_SPI`, classify whether its Lorentzian plane equals the registered pair plane,
equals its screen complement, or defines an alternative intrinsic plane. For each `K`, registered
split ownership requires block preservation plus a preregistered spectral gap. A full simple
eigenframe does not by itself choose one grouping into a physical `2+2` split.

## Numerical gates

Production uses float64 automatic differentiation of the supplied metric through third order.
Independent verification uses a separately coded finite-difference curvature-derivative route.

- metric signature: exactly one negative eigenvalue;
- covariant-derivative tensor identities and contractions: relative residual `<= 2e-8` production;
- production/independent derivative-Gram tensor agreement: relative Frobenius error `<= 5e-3`;
- scalar-gradient subspace principal-angle defect: `<= 2e-3` between routes;
- normalized numerical rank threshold: `1e-7`, with a fivefold unresolved band;
- registered block-preservation residual: `<= 2e-6`;
- spectral ownership gap: `>= 2e-5 * max(1, ||g^-1 K||)`;
- a quantity within a fivefold threshold band is `NUMERICALLY_UNRESOLVED`.

The independent finite-difference ladder and any stratified high-precision anchors must be fixed in
a second committed control preregistration before derivative outcomes are evaluated.

## Per-object landing classes

The SPI distribution returns one of:

- `SPI_RANK2_REGISTERED_PAIR`
- `SPI_RANK2_REGISTERED_SCREEN`
- `SPI_RANK2_ALTERNATIVE_PLANE`
- `SPI_RANK0_OR_1_UNDERDETERMINED`
- `SPI_RANK3_OR_4_NO_INTRINSIC_2PLANE`
- `SPI_DEGENERATE_OR_NUMERICALLY_UNRESOLVED`

Each derivative Gram tensor returns one of:

- `DERIVATIVE_GRAM_OWNS_REGISTERED_SPLIT`
- `DERIVATIVE_GRAM_PRESERVES_WITHOUT_GAP`
- `DERIVATIVE_GRAM_DEFINES_ALTERNATIVE_SPECTRAL_STRUCTURE`
- `DERIVATIVE_GRAM_DEGENERATE`
- `NUMERICALLY_UNRESOLVED`

## Package landing classes

Exactly one package landing is allowed:

1. `FIRST_DERIVATIVE_CONCOMITANTS_OWN_REGISTERED_SPLIT_ON_ALL_PRIOR_MISALIGNED_JETS`
2. `FIRST_DERIVATIVE_CONCOMITANTS_OWN_REGISTERED_SPLIT_ON_A_PROPER_SUBSET`
3. `FIRST_DERIVATIVE_CONCOMITANTS_SUPPLY_ALTERNATIVE_INTRINSIC_DISTRIBUTIONS`
4. `NO_TESTED_FIRST_DERIVATIVE_CONCOMITANT_RECOVERS_REGISTERED_SPLIT`
5. `FIRST_DERIVATIVE_ATLAS_NUMERICALLY_OR_JET_UNRESOLVED`

The package may use landing 2 or 3 only with exact counts and must retain overlaps between owner and
alternative-structure classes rather than forcing a single story per jet.

## Falsification and conclusion ceiling

The optimistic derivative-owner lead is falsified as universal by any robust prior-misaligned jet
on which none of the declared derivative objects owns the registered split. It is supported only on
the exact strata where ownership passes both implementations.

Even a universal positive result may conclude only local third-jet recovery of the registered
split in this bounded witness arena. A negative result is scoped to the seven SPI gradients and
three derivative-Gram tensors. Neither result selects a physical history, query, realization,
coframe, observer, action, source, bootstrap law, global section, `X_max`, SNe/CMB profile, or
dynamical equation.

