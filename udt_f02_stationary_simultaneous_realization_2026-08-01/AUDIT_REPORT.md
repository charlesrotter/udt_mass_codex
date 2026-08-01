# F02 stationary simultaneous-realization audit

Date: 2026-08-01  
Preregistration commit: `5e0c437`  
Mode: CPU-only exact algebra; no GPU or new physics

## Result first

```text
CONDITIONAL_NONPERIODIC_F02_DIRICHLET_HESSIAN_SECTOR_POSITIVITY_WITNESS_EXISTS
```

One exact F02 local background simultaneously satisfies the complete background Euler rows, the
corrected generic landing conditions, a supplied nonperiodic open/acyclic posture, and the
registered jet-quadratic Dirichlet-sector inequality. This is not a completed stationary solution
or global/physical realization. The witness is

```text
ell=1, g_p=g_f=g_h=c_m=1, g_x=0,
p=lambda=h=0, f=x/2, E0=1/8.
```

It lies strictly inside the tested nonnegative sector because `64 E0^2 ell^4=1<pi^4`. Its three
agreeing inherited candidate readings are `1/4`; `M_WALL=0` still dissents. No reading is promoted.

## What was actually closed

- The jet-quadratic response term is present in both the background field equations and Hessian;
  it is not pasted onto a no-jet solution after the fact.
- Its complete background lambda row vanishes because the registered term is quadratic in the
  lambda jet at the locked background.
- All four fields are varied jointly in the Hessian. No depth or response coordinate is frozen.
- The acyclic branch is explicit: `f(1)-f(-1)=1`, so the witness cannot be silently reclassified as
  a one-cell cyclic member, where single-valuedness would remove it.
- The exact Fourier-mode determinant reproduces the banked inequality and verifies the witness.

Primary details and source anchors are in `EXACT_DERIVATION.md`; all inherited conditions and open
scopes are in `CONDITION_LEDGER.tsv`.

## What remains open

This is not a completed stationary object or a native stable-matter result. The P4 fields census and response remain conditional;
`c_m` is not selected; open/acyclic completion is supplied rather than physically derived; the
`p=0` whole-cell background's canon admissibility remains open. The calculation has no time-live
equation, nonlinear stability theorem, complete Hessian, carrier, source, bootstrap return, native
mass definition, or species interpretation. Supplying the fold-realization premise `R-A` would
collapse the affine slopes and remove this nonzero member.

## Why F02 was tested first

`PRIORITY_COMPARISON.tsv` applies the preregistered workflow criteria. F02 was the only live gate
that combined an already realized conditional geometry-only nonzero branch with a finite test of
existing simultaneous conditions and no additional carrier/action posit. This is an operational
ordering, not a physical ranking and not a UDT theorem.

## Evidence status

- primary exact calculation: 10/10 checks;
- independent non-importing reconstruction: four Euler rows, Fourier determinant, completion
  discriminator, 10/10 mutation catches;
- six load-bearing sources frozen by SHA-256;
- external algebra checks: Euler/Hessian `PASS`; mode positivity `PASS`;
- external scope audit: `FAIL` on the broader stationary-witness wording; required narrowing to
  nonperiodic Dirichlet-Hessian-sector positivity applied; closure `CLOSED-PASS`;
- repository premise, frozen-manifest, and test gates: pending final replay.

## Four gates before bank

1. Preregistered: yes, commit `5e0c437`.
2. Full or bounded: full over the declared stationary F02 affine landing plus open/acyclic posture
   and registered Dirichlet jet sector; no claim beyond it.
3. Independent: local non-importing reconstruction passes; external algebra passes and the scope
   narrowing is independently closed `CLOSED-PASS`.
4. Premises: explicitly separated in `CONDITION_LEDGER.tsv`; final repository replay pending.

Maximum conclusion: one conditional nonperiodic F02 local background with a positive registered
Dirichlet Hessian sector. Native stable mass remains open.
