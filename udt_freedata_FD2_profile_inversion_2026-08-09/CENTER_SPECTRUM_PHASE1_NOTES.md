# Upstream center-spectrum correction — blind Phase-I return

Date: 2026-08-09  
Status: blind numerical correction passes all preregistered analytic/shooting/collocation gates

## Result

The inherited low-order covariant FEM did not correctly resolve the regular `m=0` center phase. The
correction is sharply localized:

- all 56 `m=+/-1` positive roots move by at most `0.001058` relative to like-indexed FD1 values;
- the 28 `m=0` positive roots move by as much as `1.13869`;
- each Neumann `m=0` background also carries the exact `omega=0`, constant-`R` mode that FD1 did not
  preserve;
- the analytic endpoint classification remains untouched.

Representative central-`n` roots:

| q/qcrit | wall | hbar | channel | first three positive roots |
|---:|:---:|---:|:---:|---|
| 0.75 | D | 0.01 | m=0 | 0.0175433, 0.0526258, 0.0876971 |
| 0.75 | D | 0.01 | m=-1 | 0.0351783, 0.0703651, 0.1055274 |
| 0.75 | D | 0.01 | m=+1 | 0.0351275, 0.0702228, 0.1052998 |
| 0.75 | N | 0.01 | m=0 positive-only | 0.0350855, 0.0701633, 0.1052267 |
| 0.75 | N | 0.01 | m=+/-1 | interleaved near 0.0176, 0.0527, 0.0879 |
| 0.95 | D | 0.5 | m=0 | 0.0212548, 0.0637588, 0.1062466 |
| 0.95 | N | 0.5 | m=0 positive-only | 0.0425082, 0.0850054, 0.1274816 |

The old "same radial index gives a nearly degenerate m=-1,0,+1 triplet" picture is therefore not a
certified continuum property. In the corrected regular-center problem, the `m=0` and `|m|=1`
families generally interleave because they carry different center phases. Whether observational
projection groups any of them is a separate question and cannot be repaired by relabeling modes to
improve a fit.

## Numerical gates

- unit-disk Dirichlet `J0` roots: maximum relative error `6.87e-14`;
- unit-disk Neumann positive `J1` roots: maximum relative error `6.95e-14`;
- exact Neumann zero mode: present;
- 84/84 positive roots found and ordered;
- maximum shooting normalized wall residual: `2.066e-11`;
- adaptive collocation success: 84/84;
- maximum shooting/collocation relative frequency disagreement: `8.337e-11`;
- maximum collocation normalized wall residual: `1.310e-10`.

The first collocation attempt is preserved separately; it failed only because an `r0^-|m|`
normalization inflated the outer solution. The preregistered physical Frobenius scaling correction
passes without changing any tolerance.

## Scope and consequence

This is a solver correction, not CMB evidence. Before any FD2 profile inversion can resume, the four
inherited FD1 witnesses must undergo the frozen attributed readout with both Neumann conventions
reported. Until then:

```text
RA1 endpoint classification: unchanged.
RA2 finite numerical comb: OPEN_RECHECK_REQUIRED.
FD1 multiplet compatibility: OPEN_RECHECK_REQUIRED.
FD2 observational inversion: sealed.
```

## Hashes

```text
14355a70666d0a77d31ca9febc94204750158204df813869476c451243cd691f  center_spectrum_phase1.py
8fe6c747b5f2629e6fbd4ddb44bd40452d39052a71adc1aa46cfbad1771ae567  center_spectrum_phase1.json
99da4d4383d39b421a3802c878f05d416dfbcb2ebb31a6d00fe8c871746eebe0  center_spectrum_phase1_failed_collocation.json
```
