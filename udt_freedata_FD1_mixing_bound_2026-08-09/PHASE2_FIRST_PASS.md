# FD1 Phase-II first-pass return

Date: 2026-08-09
Status: `OBSERVED`, attributed first-pass map; transition refinement and independent verification pending

## Data and ordering

Phase I was independently verified, committed, and pushed at `e7268d61` before any new trough value
was opened. The Phase-II formulas and exact attributed table were then frozen at `9342737c` before
this comparison was executed.

Source: Planck Collaboration, *Planck 2018 results I*, A&A 641 A1 (2020), Table 5,
<https://doi.org/10.1051/0004-6361/201833880>.

No peak height, polarization datum, cosmological parameter, source model, or likelihood enters.

## First-pass result

All 7/7 execution keys passed over the 420 nonzero-mixing rows:

- `170` `FULL_CENTERED_MULTIPLET_CONTAINMENT`;
- `170` `SPLITTING_ONLY`;
- `80` `BASIN_MISMATCH`.

The split-only population confirms the preregistered warning: a small `+m/-m` separation does not
guarantee that the entire pair stays near the `m=0` comb, because the even-in-`m` centrifugal shift
can move both partners.

Using the preregistered two-parameter affine comparison and the report-only historical RA2 3.1%
line, four sampled joint neighborhoods persist across all three SNe-conditioned `n` values:

| `q/qcrit` | wall | consecutive sampled `hbar` values |
|---:|:---:|:---|
| `0.75` | D | `0.002, 0.005, 0.01, 0.02` |
| `0.75` | N | `0.005, 0.01, 0.02` |
| `0.95` | D | `0.2, 0.5` |
| `0.95` | N | `0.2, 0.5` |

All 51 individual rows in these joint neighborhoods also pass the stricter diagnostic requiring
both `m=+1,-1` lines to lie between the actual adjacent troughs. Thus the registered centered-basin
condition is not hiding an absolute-trough failure at these witnesses.

## Decisive caveat: the fitted offset matters

The open-window label is conditional on P10's registered affine map `ell=a omega+b`. Across the 51
joint rows, the affine maximum fractional residual ranges from `0.0249468` to `0.0309860`.

The separately frozen one-scale diagnostic `ell=a omega`—the more literal form of RA2's statement
that common projection factors cancel—has maximum fractional residuals from `0.257110` to
`0.317913` over those same rows. Therefore:

- the first pass does find an open **two-parameter morphology compatibility** region;
- it does **not** establish a native one-scale projection from the computed frequency ladder to the
  observed TT comb;
- the additive offset is a spent continuous comparison freedom and must not be redescribed as a
  derived CMB phase or source effect.

The historical 3.1% line remains report-only. It was not used to delete any row; the complete
residual surface, including maxima up to `0.0900209`, is preserved.

## What remains before landing FD1

1. bisect the entry/exit brackets of the four joint neighborhoods without changing any threshold;
2. rerun every load-bearing transition at finer grid and 10x/100x smaller asymptotic joins;
3. recompute the transition witnesses with the independent ODE-coordinate/nonlinear-root method;
4. audit whether the affine-offset convention is merely the preregistered empirical comparison or
   can be confused with the metric projection dictionary;
5. run repository premise and test gates.

Until those steps complete, the first-pass label is a candidate
`FD1-OPEN-COMPATIBILITY-WINDOW`, not the banked FD1 verdict.

## Hashes

```text
117b447bd0a9be7701be43a177ffd7bf184eecf8592585790c104dae5d7d5605  phase2_comparison.json
c5b3748981b2016def1a51b84ce85d43f0113c63689d3cd6a61d21a309f280c1  phase2_run_output.txt
```
