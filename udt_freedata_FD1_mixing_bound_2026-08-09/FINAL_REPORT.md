# FD1 final report — background mixing versus the CMB multiplet kill-switch

Date: 2026-08-09
Landed status: `FD1-OPEN-COMPATIBILITY-WINDOW — VERIFIED-WITH-CAVEATS`

## What was learned

RA2's large-doublet warning is real at its old `h0=1/2` witness, but it is not generic across the
background freedom already present in the metric slice. The complete preregistered atlas contains
strict neighborhoods where all three carried components, `m=0,+1,-1`, remain within the published
TT peak basins without setting either `|m|=1` population to zero.

The independent strict-interior witnesses are:

| `q/qcrit` | wall | `hbar` | minimum affine margin below 3.1% | minimum centered basin margin | minimum actual-trough margin | minimum one-scale mismatch |
|---:|:---:|---:|---:|---:|---:|---:|
| 0.75 | D | 0.01 | 0.002107 | 46.73 | 59.60 | 28.91% |
| 0.75 | N | 0.01 | 0.001981 | 49.72 | 61.66 | 27.34% |
| 0.95 | D | 0.5 | 0.004679 | 10.81 | 18.22 | 29.08% |
| 0.95 | N | 0.5 | 0.004765 | 17.42 | 23.14 | 28.07% |

Each row persists across all three SNe-conditioned `n` samples. Strict positive margins plus the
continuous finite-dimensional pencil establish a local open neighborhood around each witness; this
does not certify the neighborhood's exact edge.

The atlas also contains `170` `SPLITTING_ONLY` rows. That is the clean technical lesson behind the
earlier warning: suppressing the odd-in-`m` `+/-` split is not enough. The even-in-`m` centrifugal
term can move both partners away from the `m=0` comb.

## What failed or remains conditional

- **Exact edges:** `OPEN`. Two `q/qcrit=0.75` exit locations exceeded the preregistered 10% grid-drift
  gate (11.45% and 13.60%). No precise `hbar` bound is claimed.
- **Invariant mixing bound:** not derived. `hbar` is a chart/realization coefficient, not an invariant
  `mu`; FD1 reports dimensionless multiplet geometry first.
- **Native projection:** not derived. The authorized affine map `ell=a omega+b` uses two fitted
  freedoms. Removing the additive offset produces a 27–32% mismatch on the verified witnesses.
- **CMB physics:** not derived. Peak heights, amplitudes, damping, polarization, excitation weights,
  and the even/odd pattern still require background profile structure and/or a source/coupling law.
- **Complete geometry:** not covered. Full sphere, higher `|m|`, Robin boundary completion,
  time-live backgrounds, other profiles, and native dynamics remain open.

## Scientific interpretation

FD1 removes one false dichotomy. The CMB comb does not force either “mixing must vanish” or “a source
must hide every rotating mode.” Within this conditional scalar slice, decaying-wall mixing can make
the whole low-`|m|` multiplet geometrically compatible with the observed basins.

That is a background-freedom result, not a CMB explanation. The strongest honest statement is:

```text
The RA2 multiplet kill-switch is conditional on the chosen mixing realization.
Background geometry can avoid it in open affine-comparison neighborhoods.
UDT has not yet derived which neighborhood, the projection offset, or the mode powers.
```

## Evidence gates

- Phase-I atlas: 462 rows, two grids, all internal gates passed.
- Independent Phase I: 8/8 gates passed.
- Phase-II first pass: 7/7 gates passed; complete row surface retained.
- Boundary refinement: 4/5, failure preserved; exact edges not certified.
- First independent Phase II: 8/10, over-strong outside-row failure preserved.
- Corrected frozen family-semantics audit: 6/6 gates and 7/7 catch-proofs passed.
- Current premise verifier: 28 premise guards passed.
- Repository tests: `78 passed, 1 xfailed` (documented baseline).

## Next justified step

Return to the background-freedom fork, not source invention. FD2 should characterize whether
data-allowed structure in the radial profile can account for the alternating position residuals
while remaining jointly consistent with the SNe profile evidence. It must be data-first and
profile-characterizing: no bump may be inserted merely to manufacture the alternation. Heights and
power allocation remain explicitly source-side.

No GPU is justified for that first bounded derivation.
