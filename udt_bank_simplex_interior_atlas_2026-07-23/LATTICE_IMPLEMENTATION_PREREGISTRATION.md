# Lattice implementation preregistration

Date: 2026-07-23

Parents: `PREREGISTRATION.md` and `NUMERIC_SCOPE_CORRECTION_PREREGISTRATION.md`

Status: `FROZEN_BEFORE_L1_L2_PRODUCTION_RUN`

## Process and resources

- one foreground CPU process;
- NumPy float64;
- no GPU process;
- no concurrent solve;
- 20-minute production timeout;
- estimated raw sign storage below 280 MB before compression;
- point batches at most 4,096 and group batches at most 64;
- deterministic output names; a pre-existing output aborts unless byte-identical replay mode is
  explicitly requested.

The GPU is unnecessary for this bounded lattice map. CPU float64 keeps production and independent
matrix replay on the same disclosed platform while 80-decimal interval anchors provide the separate
precision control.

## Frozen node classification

For each sheet and resolution, let

```text
tau = 64 * eps_float64 * max(1, max_node_abs_s).
```

Nodes are classified:

```text
POSITIVE          s > +tau
NEGATIVE          s < -tau
NUMERICALLY_ZERO  otherwise.
```

`NUMERICALLY_ZERO` nodes are retained and make a component/root class unresolved unless their sign
is separately certified at high precision. No tolerance will be changed after the production run.

Root locations used for shape diagnostics are linear sign-transition interpolants inside the
bracketing lattice interval. They are noncertifying and must not be described as exact roots.

## Frozen lattice adjacency

Two simplex nodes are adjacent exactly when their integer barycentric triples differ by `(+1,-1,0)`
up to permutation. Base nodes at neighboring `u` indices are adjacent when their barycentric triple
is identical.

The `t=1` repetitions of the simplex apex configuration are identified for component reasoning and
never counted as distinct configurations. Barycentric triples are the authority; the rectangular
`(r,v)` parameterization is only an evaluation coordinate.

## Stop conditions

Stop without a banked topology class if:

- either level does not finish for all 768 sheets;
- any sheet has a numerically-zero node not resolved by the registered precision controls;
- L1 and L2 qualitative classes disagree;
- the independent full-matrix route disagrees on any node sign or transition class;
- raw arrays, hashes, source identities, edge controls, or repository gates fail.

The maximum conclusion remains the corrected bounded lattice conclusion.
