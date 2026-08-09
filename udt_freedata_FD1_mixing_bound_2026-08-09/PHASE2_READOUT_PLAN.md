# FD1 Phase-II readout implementation freeze

Date: 2026-08-09
Status: frozen after Phase-I commit `e7268d61`, before executing the Phase-II comparison

## Attributed data now opened

The only newly opened values are the TT extrema in Table 5 of Planck Collaboration,
*Planck 2018 results I*, A&A 641 A1 (2020),
<https://doi.org/10.1051/0004-6361/201833880>:

- peaks: `220.6, 538.1, 809.8, 1147.8, 1446.8, 1779, 2075`;
- troughs: `416.3, 675.5, 1001.1, 1290.0, 1623.8, 1919, 2241`.

The peak uncertainties are carried but are not used as a likelihood or exclusion test. Heights,
amplitudes, polarization, cosmological parameters, and source interpretations are not loaded.

## Frozen implementation rulings

1. The first seven ordered radial modes correspond to TT peaks 1 through 7, exactly as in RA2.
2. The authorized two-parameter comparison is implemented as one affine map from each row's
   computed `m=0` frequencies to multipole: `ell=a omega+b`. The same `a,b` map is then applied to
   the `m=+1,-1` partners. Both fitted freedoms are counted.
3. A projection-consistent one-scale `ell=a omega` fit is also reported as a diagnostic. It cannot
   replace the registered two-parameter comparison after outcomes are seen.
4. Only peaks 2 through 7 enter the primary basin conjunction because only they have a published
   trough on each side in this table. Peak 1 remains an edge diagnostic.
5. The primary condition is copied literally from the preregistration:
   `max(|ell_+-ell_0|,|ell_--ell_0|) <= B_k`. A stricter absolute check that both partners lie
   between the actual adjacent troughs is reported separately and cannot silently replace the
   registered condition.
6. `SPLITTING_ONLY` means the pair's half-separation is within every basin while at least one full
   displacement from `m=0` is not. This prevents a small odd-in-`m` split from hiding the even-in-`m`
   centrifugal displacement.
7. An open sampled interval requires at least two consecutive positive `hbar` grid points and must
   persist across all three SNe-conditioned `n` samples for the stated `q` stratum and wall anchor.
8. The historical RA2 `3.1%` maximum residual is report-only, exactly as preregistered. Joint
   intervals meeting it are listed, but no row is discarded for missing that line and the full
   residual surface is preserved.
9. No bisection, new grid, or transition refinement occurs in this first pass. Every observed
   transition will be identified first and only then checked under the registered convergence,
   cutoff, and independent-recomputation gates.

Maximum first-pass conclusion: an attributed morphology/shape map on the frozen atlas, with
candidate transition brackets. It is not yet a final FD1 classification, CMB prediction, source
law, or background selection.
