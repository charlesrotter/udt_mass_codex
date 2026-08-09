# FD2 continuum refinement — upstream regular-center spectral failure

Date: 2026-08-09  
Status: Phase-I refinement stopped before any TT/SNe FD2 inversion

The preregistered continuum flux-shooting method did not reproduce the inherited FD1 spectrum. On
the first central-`n`, `q/qcrit=0.75`, `D`, `hbar=0.01` background, the first seven regular-center
roots are displaced by as much as `0.4718` relative to FD1. On the corresponding Neumann background,
the inherited first positive frequency could not be bracketed as the first continuum positive root.

The exact radial equation explains why this is an upstream issue rather than an FD2 motif effect:

```text
-(pR')' = omega^2 wR                         (m=0),
p=sqrt(A D), w=r^2/p,
R bounded/no-log at r=0.
```

For the Neumann wall, `R=constant`, `omega=0` is therefore an exact mode on every registered
background. The FD1 FEM reports a small positive first mode instead. Its `v=sqrt(r)R` representation
requires the regular `m=0` branch `v~sqrt(r)` at the center, while the piecewise-linear trial space
with the first node removed resolves that singular-but-covariantly-regular shape only very slowly.

A diagnostic analytic control makes the risk concrete. For `A=1`, `h=0`, unit outer radius and a
Dirichlet wall, the exact regular `m=0` frequencies are the zeros of `J_0`:

```text
2.40482556, 5.52007811, 8.65372791, 11.79153444, ...
```

The inherited covariant linear-FEM construction gives, even at 1,600 nodes,

```text
2.56709463, 5.69937366, 8.84283424, 11.98790972, ...
```

and converges slowly toward the analytic answer. The earlier FD1 "independent" verifier changed the
metric-coordinate integrator and eigenvalue extraction but rebuilt the same piecewise-linear
covariant matrices and imposed the same center representation. It was independent of code, not of
this center-discretization premise.

Consequences, pending the preregistered correction audit:

- RA1's analytic endpoint/limit-point/limit-circle classification is not challenged by this finding.
- The finite numerical frequencies, overtone indexing, RA2 comb projection, and FD1 multiplet
  compatibility are `OPEN_RECHECK_REQUIRED`.
- The four FD1 backgrounds cannot yet seed FD2 as verified spectral witnesses.
- No Planck or Pantheon+ FD2 inversion has been run.

The failed continuum program is preserved as `derive_phase1_continuum.py`; its failure is not a
physical profile result.

