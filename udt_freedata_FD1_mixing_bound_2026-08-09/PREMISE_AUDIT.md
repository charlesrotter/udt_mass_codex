# FD1 premise and completeness audit

Date: 2026-08-09
Status: final scoped premise audit; no canonization

## Premise ledger

| ID | premise used | exact status after FD1 |
|---|---|---|
| P1 | RA1 equatorial stationary `ds^2=-A dt^2+dr^2/A+r^2 dpsi^2+2h dt dpsi` in the areal/lock chart | `CHOSE`; bounded slice, not the complete UDT metric |
| P2 | `A=(1-r/R_w)^n` | data-conditioned `CHOSE`; P1 profile family, not native profile law |
| P3 | SNe-conditioned `inv_n=0.947 [0.9284,0.9658]` | prior `OBSERVED` lead with its redshift/anchor caveats; absolute `X_eff,R_w` cancel here |
| P4 | `h=h0(r/R_w)^2(1-r/R_w)^q` | `free-and-explored` registered center completion; no uniqueness claim |
| P5 | positive `hbar=h0/R_w`, sign reversal by angular orientation | sign convention `DERIVED`; `hbar=0` retained only as a continuum control |
| P6 | scalar `Box_g Psi=0` | metric-native probe `CHOSE`; not native UDT dynamics or source law |
| P7 | real `m=-1,0,+1` regular-center modes | bounded `CHOSE` slice; full sphere, higher `|m|`, complex modes open |
| P8 | Dirichlet and Neumann wall anchors | `free-and-explored`; full Robin circle and physical boundary completion open |
| P9 | Planck 2018 Results I TT extrema, Table 5 | external `OBSERVED` readout only; no Lambda-CDM parameter imported |
| P10 | affine `ell=a omega+b` comparison | `CHOSE`, two fitted continuous freedoms; decisive caveat, not metric-derived projection |
| P11 | `R_w=c=1` in computation | unit choice; primary outputs dimensionless |
| P12 | no source/population weights | deliberate background-only test; no `m` component silently removed |

Not used: strong CSN, EH/Bach/native action, GR field equations, a carrier, matter source, field
statistics, peak heights, polarization, absolute amplitude, baryon loading, Lambda-CDM parameters,
or a native mode-population law.

## What is exact or independently checked

- The radial quadratic pencil and Liouville weak form are direct consequences of P1 plus P6.
- In the registered `q=0` completion, the `m=+1/-1` split magnitude is exactly `2 hbar`; the full
  atlas reproduces it to `8.37e-12` absolute error.
- All 462 Phase-I rows were retained; both grids passed their internal real-spectrum, residual,
  asymptotic-join, and row-completeness gates.
- The independent Phase-I implementation used a different coordinate integrator and nonlinear
  symmetric eigenvalue roots. Its 54 mode checks drifted at most 1.39% from production and its raw
  residual was below `5.14e-9`.
- The independent Phase-II witness set drifted at most `0.4729%` from grid 240, with raw residual
  below `2.91e-10`.
- All 12 fixed strict-interior configurations passed independently and lie between the actual
  adjacent troughs. Each of the 8 outside family points remains outside under the controlling
  all-three-`n` family rule.

These are numerical/symbolic certifications of the stated conditional model, not native-physics
derivations.

## Preserved failures and their consequence

1. The first production atlas failed tail control; it was preserved and the asymptotic join was
   corrected by an explicit `A r^2/h^2 <= 1e-6` error ratio before the successful runs.
2. Exact transition-location refinement failed its frozen 10% grid-drift gate: maximum observed log
   drift `0.1360`. Precise window edges remain `OPEN`.
3. The first independent Phase-II validator demanded every individual outside `n` row remain
   outside and failed 8/10. Seven `q/qcrit=0.75` edge rows crossed the report-only 3.1% line. The
   preserved correction restores the original family logic: outside means not all three `n` samples
   are inside. Edge sensitivity remains evidence, not erased noise.
4. On every independently verified interior row, the one-scale map `ell=a omega` misses by at least
   `27.34%`. The affine offset is load-bearing. FD1 has not derived a native CMB projection or phase.

## Four banking gates

1. **Preregistered:** yes, controller committed at `ea05331b`; Phase I frozen before new TT trough
   data; every later correction/failure layer committed before its validating run.
2. **Full space or bounded scope justified:** yes for the exact 3 x 7 x 2 x 11 registered atlas;
   explicitly no claim outside that bounded slice.
3. **Independently verified on the load-bearing premise:** yes for strict interior existence,
   frequencies, residuals, and family semantics; no for exact transition locations.
4. **Every premise audited:** yes in this ledger; P1–P12 remain attached to every conclusion.

## Final scoped grade

```text
FD1-OPEN-COMPATIBILITY-WINDOW — VERIFIED-WITH-CAVEATS

Meaning:
strict open affine-comparison witnesses exist in the declared RA1 scalar slice;
exact window boundaries are OPEN;
the additive comparison offset is CHOSE and load-bearing;
one-scale native projection, source/population dynamics, and CMB explanation remain OPEN.
```

This is not eligible for `CANON.md` without Charles's explicit verdict.
