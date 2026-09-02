# G327 audit report — primitive axial Fourier tensor modes

Date: 2026-09-02
Grade: `EXTERNALLY_ACCEPTED_AFTER_R1_R2_R3_EVIDENCE_REPAIR`

## Bounded landing

```text
PRIMITIVE_AXIAL_TENSOR_MODE_CLOSES_AS_TWO_GAUGE_INVARIANT_POLARIZATIONS
__BESSEL_ZERO_TIME_BASIS__FINITE_AND_LOGARITHMIC_PAST_BRANCHES
__OSCILLATORY_T_MINUS_TWO_THIRDS_FUTURE_DECAY__NO_FULL_STABILITY_CLAIM
```

The first spatially varying tensor tile closes cleanly on every registered G324 compact Taub
quotient. The primitive axial harmonic carries two gauge-invariant transverse polarizations. Each
real phase and polarization has the exact time basis `J_0(z),Y_0(z)` with
`z=3 nu T^(4/3)/4`, for eight real constants in the complete declared eigenspace.

One branch is finite toward the past end and the other has logarithmic amplitude there. Both
oscillate and decay as `T^(-2/3)` toward the expanding end in the preregistered metric-relative
first-order phase-space norm. No branch was excluded by a boundary condition or merit test.

Production directly linearized the metric connection; the independent route inverted and
differentiated the full epsilon-dependent metric. All constraint and out-of-sector components
vanish exactly, the scalar variation is zero, and direct tidal components show the solutions are
local curvature-changing modes rather than gauge or lattice deformations. Six hostile mutations
are rejected.

## Four gates

1. **Preregistered:** `PASS`, commit `9bec301b`.
2. **Full bounded space:** `PASS_INTERNAL`, both polarizations, phases, and time solutions in the
   declared primitive axial tensor eigenspace.
3. **Independent:** `PASS_EXTERNAL`, implementation-distinct full-metric tensor reconstruction,
   fresh external scientific audit, and accepted repair-only replay.
4. **Premise audited:** `PASS_EXTERNAL`; all choices are visible and no new physical premise or
   imported equation was used.

## Fresh external review and evidence repairs

The fresh gpt-5.4 reviewer authenticated the 34-payload sealed intake and found no sign error,
missing in-sector degree of freedom, false Bessel identity, gauge defect, or scope promotion. It
returned `REFINE__G327_BOUNDED_LANDING` solely because the isolated host lacked SymPy, the bare
preregistration commit string was not an intake-local proof, and the aggregate verifier did not
literally execute its fourth registered command from the fresh copy.

Repairs R1--R3 were preregistered at commit `46f3aaaa`, then implemented without changing any
scientific source expression or generated scientific JSON value:

- a deterministic 6.6 MB intake-local archive supplies SymPy 1.13.1 and mpmath 1.3.0 with host user
  packages disabled;
- a dependency-free verifier authenticates the raw Git commit object, exact five-file changeset,
  and every preregistration blob at `9bec301bc265bf67afa5f8398f7557ccdabb855b`;
- the aggregate verifier executes all four registered commands in one fresh copy, with a narrow
  recursion sentinel on the nested fourth command, and records 73 outer assertions.

All three scientific artifacts remain byte-identical to the prerepair versions. The sealed
repair-only follow-up independently authenticated all 49 payloads, loaded SymPy and mpmath only
from the intake-local archive with host user packages disabled, recomputed the preregistration
commit and five blob IDs, ran all four registered commands literally in one writable ephemeral
copy, and verified that the nested recursion guard bypasses none of the scientific, integrity,
provenance, status, or scope gates. It returned:

```text
ACCEPT__G327_R1_R2_R3_REPAIRS__SCIENTIFIC_LANDING_UNCHANGED
```

The bounded result is therefore externally accepted after R1--R3 evidence repair.

## Boundary

This is one inhomogeneous sector, not the complete nonzero Fourier problem and not a linear or
nonlinear stability theorem. Scalar/vector sectors, other wavevector directions and harmonics,
full endpoint control, occupancy, history, scale, observation, matter/mass, and physical `X_max`
remain open. The metric, reciprocal kernel, angular sector, and adopted bounded equation are
unchanged.
