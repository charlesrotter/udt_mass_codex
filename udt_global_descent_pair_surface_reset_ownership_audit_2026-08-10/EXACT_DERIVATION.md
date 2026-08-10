# Exact derivation — global descent ownership

## 1. Typed chain

For observer objects `Q_A,Q_B,Q_C`, a descended relation requires composable arrows

```text
J_AB : Q_A -> Q_B,
J_BC : Q_B -> Q_C,
J_AC = J_BC J_AB.
```

If the target state carried to `B` is `Q_B^car` while the state reconstructed intrinsically from the
metric is `Q_B^int`, composition with an independently built second leg requires a typed morphism

```text
M_B : Q_B^car -> Q_B^int.
```

Associativity of matrix multiplication proves composition only when the middle object already
matches. It neither proves `Q_B^car = Q_B^int` nor selects `M_B`.

## 2. R17 pair-surface correction

On each supplied regular stationary R17 member, the complete dual frame contains commuting fields
`T` and `Z`. Hence

```text
[T,Z] = 0 in span(T,Z),
```

and Frobenius gives an integrable distribution

```text
E = span(T,Z).
```

The recorded global completion is `R x S3`, with `Z` tangent to Hopf circles. Thus maximal leaves of
`E` are `R x S1`, parametrized by the Hopf base `S2`. This is a global foliation family on the
declared regular configurations. It does not select one leaf for arbitrary cross-leaf endpoints or
one winding/path within a leaf.

The angular screen `H=E^perp` is a positive rank-two normal bundle. It is nonintegrable in four
dimensions and restricts to the contact plane on each spatial `S3`; this does not invalidate the
integrability of `E`.

## 3. R17 path carry and reset

Metric projection of the Levi-Civita connection supplies a path functor `U_gamma` on the normal
bundle. For composable supplied paths,

```text
U_(gamma_2 o gamma_1) = U_gamma_2 U_gamma_1,
U_(gamma^-1) = U_gamma^-1.
```

Its curvature is generally nonzero, so loop return may be nonidentity. This is lawful path-labelled
holonomy, not failed associativity.

At a middle observer the carried and intrinsic projector triples are generically different. The
pinned middle-morphism audit derives the alignment set

```text
Iso_H(X_car,X_int)
```

as a nonempty `SO(2)` bitorsor. Balanced bitorsor composition is exact, so projector alignment itself
does not require an arbitrary representative. But a unique calibration-bearing map is not selected;
the continuous screen stabilizer supplies equally valid representatives. The atlas therefore assigns
R17:

- `OWNED_EXACT` to complete witness, pair foliation, and its recorded global regularity;
- `PATH_LABELLED_HOLONOMY` to overlap/direct-composite/holonomy axes;
- `OWNED_EXACT` to the full carried/intrinsic projector-alignment bitorsor and its balanced composition;
- `OPEN_OWNER` to calibration-bearing reset and complete selector;
- `CONDITIONAL_AFTER_QUERY` to terminal reciprocal readout.

## 4. R18 clock-only descent

R18 supplies one global nonvanishing timelike Killing field `K`. The same `K` is evaluated at every
endpoint, so its norm ratio is an endpoint coboundary and the middle clock state is literally shared.
Consequently its clock-only overlap, identity carry, and direct/composite endpoint descent are exact.

The same source states that R18 contains no intrinsic ruler. Therefore the exact clock chain cannot
be promoted to a reciprocal pair surface or terminal complete-pair law. `D06=OWNED_EXACT` is scoped
to the identity carry of the shared clock object, not a derived complete reciprocal reset.

## 5. Other constructive structures

- R23: exact Levi-Civita path arrows on the complete coframe, with holonomy retained; the owned arrow
  is metric-compatible and contains no non-isometric calibration magnitude.
- R24: global set-valued shortest-line projector with equivariant transport and tie-wall exchanges;
  the set is owned while one member and a reciprocal density are not.
- R13/R14: path holonomy is registered only after an unowned pair/query orientation is supplied.
- R19: exact isometric path/holonomy control with no owned pair state.
- R04: aggregate member dependence is recorded without inheriting one member's apparatus panel.

## 6. Landing

No `D10` cell is `OWNED_EXACT`. The strongest bounded negative is therefore

```text
NO_COMPLETE_DESCENT_SELECTOR_IN_PINNED_CORPUS.
```

This is not a no-go theorem outside the pinned stationary/static corpus.

The missing joint is no longer “does R17 have any pair surface?” It is whether a still-unseen
on-shell/global-completion rule owns the pair-leaf/path query and the calibration descent from the
carried projector state into the intrinsic middle state. Nothing in this audit establishes that such
a rule exists or requires a new postulate.
