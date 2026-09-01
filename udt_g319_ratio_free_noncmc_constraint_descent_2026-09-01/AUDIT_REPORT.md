# G319 internal audit report

Date: 2026-09-01

## Result

```text
RATIO_FREE_REGULAR_STRATUM_HAS_EXACT_QUADRATURE_AND_ARBITRARY_POSITIVE_PERIODIC_PSI__B_ZERO_REMAINS_A_COMPATIBILITY_STRATUM__G318_POWER_OBSTRUCTIONS_ARE_ANSATZ_SCOPED__NO_PHYSICAL_DATA_SELECTION
```

## Audit findings

1. The reduction was performed without the G318 constant-ratio assumption.
2. The global first integral was derived without dividing by `B`.
3. The regular reconstruction was checked in both sign branches.
4. Compact positivity requires both the radicand and `B^2+F` to be positive; positivity of the
   radicand alone was not used to infer the sign of `tau`.
5. Direct physical Hamiltonian and momentum constraints agree with the conformal reduction.
6. The independent verifier reconstructs the connection and Ricci scalar by index loops and does
   not import production code or read production output.
7. G318 embeds exactly and remains unchanged inside its declared ansatz.
8. The exceptional zero/crossing stratum is retained as open global compatibility work.
9. `J0` is a free constraint constant. It is not an observational anchor, physical scale, history,
   or `X_max`.
10. The metric and reciprocal kernel are unchanged.

## External adversarial review

The fresh external reviewer authenticated all 33 sealed payloads, reproduced all five generated
artifacts byte-for-byte, independently rederived the regular-stratum quadrature and compactness
theorem, and found no scientific defect. It returned
`G319_ACCEPTED__RATIO_FREE_REGULAR_QUADRATURE_AND_ANSATZ_SCOPE_UPHELD`. It explicitly retained the
global `B=0` crossing classification as open.

## Numerical role

The load-bearing arbitrary-profile conclusion is proved by compactness. The eight Fourier rows in
`PROFILE_ATLAS.tsv` are finite replay controls, not evidence from sampling that substitutes for the
proof. Their maximum direct Hamiltonian residual is below `1.7e-14`; the independent set uses six
different controls and has maximum direct residual below `6.7e-15`.

## Remaining scope

This audit does not cover the full constraint surface, nonflat seeds, nondiagonal tensors,
multidimensional profiles, sign-changing `tau`, every global `B=0` crossing, evolution, stability,
physical topology, observations, sources, matter/mass, scale, or physical history.
