# Full corrected FD1 spectral atlas — preregistration

Date: 2026-08-09  
Mode: `OBSERVE`, Phase I blind geometry followed only after freezing by an attributed comparison  
Parent correction: `udt_freedata_FD2_profile_inversion_2026-08-09/UPSTREAM_CORRECTION_FINAL_REPORT.md`

## Whole question and maximum conclusion

Recompute the complete frozen FD1 scalar-probe census after removing the transformed-field
regular-center error.  Characterize the positive real spectra and their branch relationships in
the declared stationary equatorial metric slice.  Do not seek a CMB pattern and do not use peak or
trough values in Phase I.

The maximum Phase-I conclusion is a bounded spectral atlas for this scalar slice.  After that atlas
is committed and hashed, the already registered FD1 affine comparison may be rerun as an attributed
readout.  Neither phase may claim a native CMB source, mode population, action, boundary selection,
polarization law, or full UDT dynamics.  FD2 profile inversion remains stopped.

## Frozen census

- `inv_n = {0.9658, 0.9470, 0.9284}`, with `n=1/inv_n`;
- `q/qcrit = {-2,-1,0,0.25,0.50,0.75,0.95}`, `qcrit=(2-n)/2`;
- `hbar = {0,0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5,1}`;
- wall representatives `D,N`;
- scalar angular channels `m=-1,0,+1`;
- eight positive roots per nonzero-mixing channel;
- 42 zero-mixing limit controls and 420 nonzero-mixing rows, total 462.

Every nonzero row is retained.  Divergence, interleaving, wall sensitivity, crossings, and numerical
failure are classifications, not rejection criteria.  Neumann `m=0` also carries its exact constant
zero mode separately; it is not counted among the eight positive roots.

## Equation and endpoint correction

The frozen metric/probe slice is

```text
ds^2 = -A dt^2 + dr^2/A + r^2 dpsi^2 + 2 h dt dpsi,
A=(1-r)^n, h=hbar r^2 (1-r)^q, R_w=c=1,
Psi=exp(-i omega t + i m psi) R(r).
```

With `p=sqrt(A(A r^2+h^2))`, solve the original-field flux system

```text
F=p R',
dR/dy = u F/p,
dF/dy = u(A m^2 - 2 h m omega - r^2 omega^2)R/p,
u=1-r=exp(-y).
```

Use the regular/no-log center branch: `R~r^|m|`; for `m=0`, `R=1+O(r^2)`.
At the wall impose `R=0` for D or `F=0` for N.  For every `hbar>0`, compactify the complete
`y in [0,infinity)` endpoint using `t=u^delta`,
`delta=min(1-(n+2q)/2, 1-n/2)`.  The factored equations must be evaluated at `t=0` without a
finite-wall cutoff or a harmonic-tail substitution.

## Premise ledger

| premise | status |
|---|---|
| stationary equatorial areal/lock metric slice | `CHOSE`, inherited RA1/FD1 bounded slice |
| P1 profile and three `inv_n` values | data-conditioned `CHOSE/OBSERVED`; not a native profile law |
| mixing completion and all sampled `q,hbar` values | `free-and-explored` on the frozen grid |
| scalar `Box_g` probe | `CHOSE` metric-native diagnostic, not UDT dynamics |
| real positive frequency, `m=-1,0,+1` | `CHOSE` bounded channel census |
| regular/no-log center | pinned by the exact radial equation |
| D and N wall data | `free-and-explored`; neither selected physically |
| `R_w=c=1` | unit choice; atlas outputs are dimensionless |
| numerical tolerances, scan mesh, compactification split | solver controls, checked for soundness |

`hbar=0` is retained only as the RA1 limit-point continuum control.  It must not be solved first or
promoted to the physical system.  CSN, a carrier, action, matter/source statistics, amplitudes,
peak heights, and mode-population weights are not used.

## Numerical and certification contract

1. Production: CPU float64 two-chart original-variable shooting.  Integrate from the center to
   `y=1`, then in `t=u^delta` exactly to `t=0`.  Use DOP853 with `rtol=2e-10`, `atol=2e-12` for
   scans and `rtol=2e-11`, `atol=2e-13` for roots.
2. Scan every positive-frequency boundary function on a mesh whose step is at most `0.12`; expand
   the upper bound until at least eight sign-changing roots exist for both walls.  Refine with
   Brent (`xtol=rtol=1e-11`).  Tangential roots are not expected for separated regular scalar
   channels; the verifier must nevertheless check phase/root counts and fail closed on ambiguity.
3. Per-root normalized wall residual must be `<2e-8`; frequencies must be positive and strictly
   ordered.  Exact Neumann `m=0,omega=0` must replay directly.
4. The exact `q=0` relation `|omega(+1)-omega(-1)|=2 hbar` must hold at matched radial order with
   maximum error `<2e-8`.
5. Analytic flat-disk controls must reproduce the first eight Bessel `J_0`/`J_1` D/N roots with
   maximum relative error `<2e-9`.
6. A preregistered independent subset spans all seven q strata, both walls, all three n samples,
   `hbar={0.001,0.05,1}` and all m channels.  It is checked with an independently coded endpoint
   propagator/root condition at tighter tolerances.  Maximum relative frequency disagreement is
   `<2e-7` and normalized wall residual `<2e-7`.
7. Endpoint robustness: the same subset is rerun with split `y={0.7,1.4}`; maximum relative drift
   `<2e-8`.  Center robustness uses `r0={1e-6,1e-8}`; drift `<2e-8`.
8. Phase I contains no Planck peak/trough values and is committed before any attributed readout.

If full production is throughput-obstructed, preserve the partial output and report obstruction;
do not loosen tolerances or shrink the census after seeing results.

## Blind classifications to report

- endpoint/wall spectral existence and exact zero modes;
- ordered branch spacings, interleaving, pair splitting, and displacement surfaces;
- q-stratum, hbar, n, and wall dependence;
- crossings or ordering changes by continuous frequency order (no assumed observational triplet);
- comparison with the withdrawn finite-element atlas only as a numerical regrade after the corrected
  values are frozen.

No blind row is labeled good/bad by Planck resemblance.

## Completeness stamp and stop boundary

Covered: the full previously frozen FD1 parameter census in one stationary equatorial scalar slice,
with the corrected center and complete compactified endpoint.

Not covered: full 4D/spherical nonseparable geometry, higher `|m|`, Robin wall family, complex modes,
time-live backgrounds, other profile families, source/statistical weights, vector/polarization
channels, native action/source, or physical mode selection.

After the corrected atlas, independent checks, optional attributed FD1 readout, reports, hashes,
tests, commit, and push: **STOP before restarting FD2**.
