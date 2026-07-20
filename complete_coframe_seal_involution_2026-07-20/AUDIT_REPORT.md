# Complete-Coframe Seal-Involution Audit

Date: 2026-07-20

Base: `5b1b57297bcceb5f8806b1ee238ac2ed2ccfcee3`

Preregistration commit: `02bdf20`

Mode: CPU-only exact real algebra, complete-sector extension census, and provenance audit

## Result

`MULTIPLE_COMPLETIONS`

UDT's reciprocal character has an exact depth-reversing involution, but the current foundation does
not derive one complete physical coframe action of the finite-cell seal.

For every nonzero real `b`,

```text
F_b = [[0,b],[1/b,0]],
F_b D(phi) F_b^-1 = D(-phi),
F_b^2 = I.
```

This is the full constant real `2x2` family. In the conditionally chosen diagonal clock/radial
readout `eta=diag(-1,1)`, however,

```text
F_b^T eta F_b = diag(1/b^2,-b^2),
```

which cannot equal `Omega^2 eta` for any positive real common-scale factor. The balanced raw swap is
therefore an anti-isometry of that readout, not a physical Lorentz reflection.

If the founded off-diagonal dual pairing `K=[[0,1],[1,0]]` is **additionally chosen** as a
null-coordinate Lorentz metric, every `F_b` is an exact `O(1,1)` reflection. A Hadamard basis change
makes the structure familiar: `K` becomes diagonal Lorentz form, `D(phi)` becomes a standard boost,
and the balanced swap becomes a spatial reflection. The algebra is exact; the physical
identification is not supplied by the source, which calls `K` a faithful dual-pairing
formalization.

Even after making that choice, the completion is nonunique. On an isotropic angular two-plane the
identity, minus identity, and a continuous family of axis reflections are inequivalent coframe
involutions. Conditional Hopf circle exchange is another witness but imports its already disclosed
representation and topology premises. The temporal mirror supplies sector authority without an
executable parity for all rotating/off-diagonal data. Positive Common-Scale Neutrality preserves a
gauge direction; it does not select one extension.

The canonical field-dependent map `T(phi)=D(-phi)D(phi)^-1` does match the two reciprocal
representatives and obeys `T(-phi)T(phi)=I`. It is generically not conformal-Lorentzian in the
diagonal readout, so it is a tautological transport identity rather than the missing physical
symmetry.

## What was learned

- The earlier raw-swap obstruction was not an arithmetic accident; it extends to the full constant
  real inverting family in the diagonal readout.
- The reciprocal algebra already has the structure of a boost plus reflection in a null-basis
  Lorentz realization. This is a strong conditional geometric clue.
- The clue does not identify the reciprocal pairing as the physical metric, nor does it determine
  the angular, normal, time-on, global, or boundary-tangent completion.
- At least two inequivalent complete algebraic coframe witnesses survive, and in fact continuous
  families survive. Native uniqueness is therefore unavailable from the registered premises.

## Boundary consequence

No complete fixed/anti-fixed tangent decomposition follows. The durable static conclusion remains
only that the odd scalar depth has `phi=0` at the seal while its normal derivative is free. The
audit does not pin `delta h`, `delta K`, corner data, boundary charge, or a physical polarization.

## Evidence grade and limits

The result is `VERIFIED-WITH-CAVEATS`: preregistered; full for the declared constant real block and
isotropic angular involution classes; independently reconstructed with source/hash and mutation
catches; all premises audited. No fresh different-model external review was authorized. The result
does not select an action, carrier, boundary functional, topology, representative, `X_max`, total
mass, or particle mass, and no nonlinear or GPU solve was run.

The smallest genuinely missing object is a source-authorized physical quadratic readout/slot map
together with a complete normal-angular-time-on lift of the seal involution. Global-solution
admissibility may eventually select among the surviving conditional families, but that must be
tested comparatively rather than assumed.
