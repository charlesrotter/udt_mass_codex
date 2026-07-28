# Complete screen-response finite-cell branch atlas

Date: 2026-07-28

Status: `VERIFIED-WITH-CAVEATS` — exact CPU/SymPy derivation plus a non-importing independent
implementation in the same warm context; no fresh adversarial model.

## What was learned

The historical-method lead survived contact with the current complete-branch library, but in a
more informative form than “replace lambda with four numbers.”

1. The complete local screen response really has four independent slots: area/trace, rotation, and
   two shears.
2. The registered complete homogeneous controls realize pure rotation after a conditional Hopf
   pair is supplied.  They do not realize area or shear response.
3. The complete twisted reciprocal `S3` family realizes isotropic area response plus rotation.
   For nonconstant depth it also forces pair-screen mixing somewhere.
4. Neither shear component appears in the 30 explicitly evaluable registered response rows.
5. That absence is not a metric no-go.  The twisted coframe gave both angular legs the same
   `exp(lambda phi)` weight, which algebraically freezes shear in the depth response.  The three
   arbitrary-geodesic Jacobi rows remain explicitly `UNDETERMINED`, and a general screen matrix has
   not been constructed.

The new practical distinction is therefore:

```text
observed current response vocabulary = trace + rotation + pair-screen mixing,
ambient complete screen vocabulary   = trace + rotation + two shears,
missing shear status                 = open / ansatz-frozen, not rejected.
```

## Census and coverage

- fixed-base source records: 5,939;
- direct load-bearing sources: 16;
- completion classes: 12 (`FC01`–`FC12`, taxonomy only unless an actual metric is supplied);
- fixed Q configurations: 4;
- W witnesses/controls: 6;
- C parameter strata: 8;
- branch/path response rows: 52, all unique;
- registered parent rows represented: 30;
- exact-zero shear rows: 30;
- generic Jacobi shear rows left open: 3;
- mixing/mismatch rows retained: 8;
- preregistered catch-proofs passed: 28/28;
- ten completeness criteria stamped: 10/10.

## Evidence gates

1. Preregistered: **yes**, commits `a41bdd4` and `4df5607` froze the scope and source universe.
2. Full space: **full fixed registered source/branch universe**, not the space of arbitrary metrics
   or unregistered solutions.
3. Independent verification: **yes with caveat** — non-importing implementation and direct frozen
   source/hash replay; no fresh adversarial model.
4. Premise audit: **yes** — every branch keeps its on-shell, pair, orientation, path, and
   completeness stamps.

## What did not happen

No branch, value of `lambda`, screen orientation, action, equation, source, carrier, boundary,
density, bootstrap, scale, particle, force, gauge group, or prediction was selected.  No GPU,
ODE/PDE, time-live, matter, canonization, or repository-reorganization work was performed.

## Ruling

`MIXED_MULTIPLE_OUTCOMES` within the registered branch library.

The result is useful because it identifies a concrete source of apparent underdetermination: the
current complete branch ansätze do not yet exercise the whole angular response space.  The next
metric-led question is not “which physics should the shear produce?” but whether a complete regular
finite-cell coframe with a general positive screen matrix exists and what response motifs it
actually realizes.
