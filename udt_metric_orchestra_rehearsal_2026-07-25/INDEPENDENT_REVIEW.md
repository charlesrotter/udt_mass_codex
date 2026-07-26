# Fresh source-first adversarial review

Verdict: `PASS-WITH-CAVEATS`.

## Independence protocol

The reviewer first read only the preregistration packet and every one of its
ten manifest-cited frozen sources.  Before seeing any production script,
generated table, verifier, report, or package manifest, it froze
`ADVERSARIAL_PRERULING.md`:

```text
SHA-256 36a02a336120397f4092c1199ca53e59c2de9795ea5ac78b1b14595152ea6a49
bytes   8934
```

All ten source Git-blob, SHA-256, and size identities independently matched.
The reviewer made no repository edits and did no GPU work.

## Scientific findings

The determinant, volume, normalized angular metric, general depth norm,
torus-invariant `dphi` norm, connection curvature, scalar Hessian, and
second-jet formulas agree with the frozen expectations.

A separate SymPy `diffgeom` Ricci route—not the package's metric-jet Ricci
contraction—exactly reproduced eight load-bearing first-rate controls spanning:

- `phi` to angular shape;
- angular shape to connection;
- connection to connection; and
- exact absence of a direct neutral-point `phi` to connection edge.

That route also reproduced all 240 Ricci pure-second-jet entries exactly.  The
original frozen scratch script is preserved byte-identically as
`ADVERSARIAL_DIFFGEOM_SCRATCH.py`:

```text
SHA-256 ce417c0e73ec4c671bea7b14d4cc5aafff0b01b9c3e2f4e431ba907016850440
```

`verify_orchestra_diffgeom.py` is its repository-relative fail-closed replay.

Exact connection-gauge reduction passed.  The four raw `S` amplitudes reduce
to two gauge-invariant curvature channels `F1,F2`.  The resulting six-node
graph `{phi,sigma,alpha,k,F1,F2}` remains connected, with no direct `phi-F`
edge.  This rules out the simplest concern that raw gauge multiplicity alone
created the observed connectivity.

The package correctly leaves the reverse `A` arrow, action, source, carrier,
density, boundary functional, physical branch, and bootstrap closure open.

## Corrections caused by review

1. Raw `frozenset` formatting initially made two catch-proof rows depend on
   Python hash order.  Sorted serialization now gives identical replays under
   different hash seeds.
2. Reports now distinguish Ricci response from complete Riemann/Weyl
   curvature.
3. The independent 20 checks are separated into 15 numerical/geometric
   controls and five schema/integrity checks.
4. A stale sentence below the scalar-curvature formula was removed; no formula
   changed.

## Remaining caveats

- The connected graph is a neutral-point, torus-invariant, chosen-chart
  Ricci-component result, not a frame-independent physical coupling theorem.
- The full 2,560-entry reconstruction uses independent numerical metric jets
  but a structurally similar coordinate Ricci contraction.  The `diffgeom`
  route independently secures the load-bearing connectivity controls and all
  240 pure second-jet entries, not every first-rate table cell by a third exact
  implementation.
- No on-shell or globally completed branch is established.

## Final bounded grade

```text
VERIFIED-WITH-CAVEATS
EXACT_TYPED_PARTIAL_R_GEOM_AND_COMMON_DOMAIN_CROSS_RESPONSE_ATLAS_ONLY
```

This is a bounded geometric response atlas, not physical closure or selection.
