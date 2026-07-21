# UDT mixed-readout observational-anchor and sector-soldering audit

Date: 2026-07-20

## Result

The observational `c_E` anchor does **not** presently select or reject the conditional mixed
Lorentzian readout family. It also does not fix its modulus

```text
mu = B^2/(A^2 b^2) > 1.
```

The reason is now exact rather than verbal: current UDT authority calibrates the local clock/ruler
cone but does not identify the reciprocal eigen-coframe `q=(c dt,dr)` with the operational
orthonormal clock/ruler axes.

This is a bounded result about the constant symmetric `2x2` readout class. It is not a complete
metric, observer, action, or matter theorem.

## The invariant result

For

```text
H = [[A,B],[B,A b^2]],        L = diag(-1,1),
```

the simultaneous metric/operator pair has the scalar invariant

```text
I = tr(H^-1 L^T H L) = 2(1+mu)/(1-mu),
mu = (I-2)/(I+2).
```

Under any passive invertible basis change `q=S q'`, both objects transform:

```text
H' = S^T H S,        L' = S^-1 L S.
```

Exact symbolic reduction gives `I'=I`. Positive CSN rescaling also leaves it unchanged. Therefore
`mu` is not an artifact of keeping the reciprocal operator diagonal. Exact witnesses `mu=4` and
`mu=9` give `I=-10/3` and `I=-5/2`; they cannot be the same metric/reciprocity pair in different
bases.

This does not prove that `mu` is a new observable. It proves only that a valid equivalence cannot
erase it while retaining both the metric and reciprocal operator.

## The two c-anchor branches

### Strong: the reciprocal q axes are the measured axes

At the seal the q-chart null equation is

```text
A + 2 B v + A b^2 v^2 = 0,       v=dr/(c dt).
```

Symmetry under `v -> -v` forces `B=0`. The spatial-seal family then has
`det(H)=A^2 b^2>0`, so it is not Lorentzian. Consequently the strict `FIXED_Q_ANCHOR` premise rejects
the mixed Lorentz family.

The source audit classifies this premise as `pinned-by-HABIT`: the frozen packet calls q a
dimension-matched coframe pair but separately keeps local readout and slot identification
non-derived.

### Weak: an operational orthonormal frame exists

For the exact witness `A=1`, `B=-2`, `b=1`, a real basis `S` gives

```text
S^T H S = diag(-1,1).
```

The local null slopes are then exactly `v=+1` and `v=-1`, hence `+c` and `-c` after restoring the
observational unit. The reciprocal generator becomes

```text
S^-1 L S = [[0,-1/sqrt(3)],[-sqrt(3),0]].
```

The measured cone and reciprocal dilation therefore coexist, but their axes do not coincide. The
existence of this chart is a compatibility witness, not a physical soldering theorem.

## Spatial versus temporal mirror

The spatial seal remains exact: `F_b` relates `phi` and `-phi` and is an isometry of the mixed
family. A literal q-chart time reversal `diag(-1,1)` would flip the cross-term and force `B=0` if it
were imposed as an isometry.

In the exact orthonormal witness, however, the ordinary temporal reflection conjugates back to
`-F_1`, while the spatial reflection conjugates to `F_1`. These are not the literal q-chart time
flip. The canonized sector split says which sectors are governed by spatial and temporal mirrors,
but the current evidence does not supply the component/coframe soldering needed to identify the
owner-named coordinate `t` in this mixed readout. Temporal parity therefore neither selects nor
rejects the family here.

## Status

The preregistered outcome classes supported are:

- `OBSERVATIONAL_ANCHOR_LEAVES_MU_OPEN`;
- `MU_IS_INVARIANT_OF_METRIC_RECIPROCITY_PAIR`;
- `FIXED_Q_AND_ORTHONORMALIZABLE_ANCHOR_BRANCHES_DIVERGE`;
- `TEMPORAL_MIRROR_COMPONENT_SOLDERING_REMAINS_OPEN`; and
- `PHYSICAL_CLOCK_RULER_SOLDERING_RULE_ABSENT`.

Not supported are a unique `mu`, rejection by the current observational anchor, or a claim that
`mu` is a simultaneous-basis artifact.

## What remains open

The next missing object is a native map between the reciprocal eigen-coframe and operational
clock/ruler axes. The angular sector, finite-cell involution, CSN structure, or bootstrap may supply
it, but this audit does not assume that they do. Observer mechanics, action, field equations,
topology, scale selection, carrier, source, mass, and boundary completion were excluded.

## Evidence gates

1. **Preregistered:** yes, commit `4e7b126`, before source inspection and algebra.
2. **Full space or bounded scope:** complete in the real constant symmetric `2x2` mixed family;
   deliberately excludes complete four-dimensional/angular and dynamical completion.
3. **Independent verification:** standard-library rational recomputation of both pair invariants,
   a nontrivial simultaneous basis transform, anchor witnesses, tables, and fail-closed mutations.
4. **Premise audit:** exact owner meanings and non-derived readout/slot/observer stamps recorded in
   `SOURCE_LINEAGE.tsv` and `STATUS_LEDGER.tsv`.

Maximum conclusion:

`UDT_MIXED_READOUT_ANCHOR_SOLDERING_STATUS_CHARACTERIZED`.
