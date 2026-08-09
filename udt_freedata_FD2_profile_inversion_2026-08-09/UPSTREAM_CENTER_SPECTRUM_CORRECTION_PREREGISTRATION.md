# Upstream center-spectrum correction preregistration — gate before FD2 resumes

Date: 2026-08-09  
Scope: bounded correction of the four FD1 strict-interior witness families; no full-atlas claim

## Question

Does a center-regular continuum realization of the exact radial scalar equation sustain any of the
four FD1 spectral witnesses that were meant to seed FD2, once the exact Neumann zero mode and the
regular center phase are represented without the inherited piecewise-linear `v` bias?

This is solver correction, not new physics. The metric, probe, walls, profile, mixing, Planck readout,
and affine comparison remain exactly those already ledgered.

## Frozen tests

1. **Analytic center controls.** Reproduce unit-disk `m=0` Dirichlet `J_0` zeros to relative error
   `<1e-8`; reproduce the exact Neumann `omega=0`, constant-`R` mode; reproduce the center indices
   `R~r^|m|` for `m=+/-1`.
2. **Continuum roots.** Use the original radial flux system—not the transformed linear-FEM trial
   space—for `m=-1,0,+1`, seven nonnegative ordered modes, on all four FD1 backgrounds at central
   `1/n=0.9470`. Retain the Neumann zero mode as mode zero and also report the first seven positive
   modes separately. Propagate the frozen asymptotic tail analytically. Require normalized wall
   residual `<1e-8`.
3. **Method independence.** Check every continuum root with an independently assembled high-order
   Chebyshev or adaptive-collocation realization in the original `R,F` variables. A repeated shooting
   run is not independent.
4. **Attributed readout.** Only after roots are frozen, apply the same Planck Table-5 positions,
   diagonal errors, and affine `ell=a omega+b` comparison. Report both conventions explicitly:
   Neumann ladder including its exact zero and the seven-positive ladder excluding it. No convention
   may be selected because it fits better.
5. **Multiplet check.** Carry all `m=-1,0,+1` partners and repeat the exact FD1 centered/actual-trough
   basin diagnostics. No source weight may remove a component.
6. **Cross-`n` check.** Any surviving central-`n` witness is rerun at both registered SNe interval
   endpoints before it can seed FD2.

## Frozen landings

- `UPSTREAM_WITNESS_SURVIVES_CONTINUUM_CORRECTION`: at least one exact convention/background remains
  an open strict multiplet witness across all three `n` values. FD2 may resume only on those survivors.
- `UPSTREAM_FD1_WITNESSES_WITHDRAWN`: none survives. FD2 stops; a separately preregistered full
  corrected atlas is required before profile inversion.
- `CENTER_CONVENTION_PHYSICALLY_OPEN`: the continuum mathematics is sound but the registered
  observer/center condition does not select whether the Neumann zero mode belongs to the compared
  ladder. Both readouts remain conditional; no favorable convention is adopted.
- `NUMERICALLY_OPEN`: shooting and independent collocation disagree beyond the frozen tolerance.

Maximum conclusion is a bounded numerical regrade of the four witnesses. It cannot alter the RA1
endpoint classification, select a physical wall condition, validate CMB physics, or derive a native
projection/source/profile law.
