# Full corrected FD1 atlas — blind Phase-I report

Date: 2026-08-09  
Status: `VERIFIED-WITH-CAVEATS` in the declared scalar slice  
Observational peak/trough values loaded: **no**

## Result

The complete old FD1 census has been recomputed in the original regular radial field with the true
compactified wall endpoint.  The certified artifact contains 462 rows: 420 nonzero-mixing spectra,
42 zero-mixing continuum controls, and 10,080 positive roots.  The geometry is not a generally
aligned same-radial-index `m=-1,0,+1` triplet.  It is three interleaved angular ladders whose order
changes across the already frozen background freedom.

This is a correction of the scoped stationary equatorial scalar-probe atlas, not a native CMB model.

## What the blind atlas shows

- All 630 `(background,hbar,m)` Dirichlet/Neumann channel pairs strictly interlace.  This is a strong
  separated-wall spectral consistency check.
- The only same-index ordering motifs are `0,+1,-1` (1,489 positions), `+1,-1,0` (1,366), and
  `+1,0,-1` (505).  Positive hbar fixes the handed `+1` versus `-1` orientation, but does not fix
  where the scalar `m=0` ladder lies relative to them.
- `m=0` lies between the two rotating partners at only 505/3,360 same-index positions (15.0%).
  Only 44/420 rows have that ordering for all eight carried indices.
- Same-index displacement is never small in this census: minimum 6.08%, median 16.08%, 95th
  percentile 100.75%, maximum 213.15%.  This is a geometric statistic, not an observational test.
- The exact bounded-mixing identity survives: maximum q=0 splitting error is `1.8944e-12`.
- As `q/qcrit` approaches 1 from below, the finite optical wall length grows sharply.  Across the
  atlas it ranges from `0.9516` to `10860.0062`; the smallest positive frequency is `1.4465e-4`.
  The complete endpoint, rather than a finite cutoff, is essential in this corner.

## Regrade of the withdrawn transformed-field atlas

At identical rows and sorted radial order, absolute relative frequency changes are:

| channel | median | 95th percentile | maximum |
|---|---:|---:|---:|
| `m=-1` | 0.0385% | 0.778% | 3.272% |
| `m=0` | 12.496% | 115.768% | 589.059% |
| `m=+1` | 0.0435% | 0.863% | 12.061% |

Thus the upstream error was concentrated in the transformed `m=0` regular-center basis, exactly as
the four-witness correction indicated.  The rotating families were comparatively stable.  Any old
FD1 conclusion that used `m=0` as the center of a same-index observational multiplet remains
withdrawn pending an attributed readout on the corrected families.

## Numerical history and gates

The first complete run is preserved as a failure: 54 near-critical Dirichlet row/channel maxima
missed the wall-residual gate because the frozen absolute root tolerance was too loose for tiny
frequencies.  A strict replay of all 10,080 roots is also preserved; it exposed a factor-of-two
bookkeeping error and left three maxima just above gate.  A separately preregistered 24-root
ultrafine correction produced the certified artifact without changing a branch or scan cell.

Certified production:

- maximum normalized wall residual: `5.0948e-9` (`<2e-8` required);
- maximum q=0 split error: `1.8944e-12`;
- maximum all-root strict shift from the first complete atlas: `5.7209e-11`;
- maximum 24-root ultrafine shift: `1.0953e-15`.

Independent verification:

- 63 preregistered roots spanning all q strata, both walls, all n and hbar check values, all m,
  and low/middle/high radial order;
- maximum independent relative frequency difference `2.0633e-12`;
- maximum independent normalized residual `8.3473e-13`;
- split-chart drift `1.3840e-12`; center-radius drift `2.3537e-14`;
- flat-disk Bessel-control error `1.3678e-13`;
- 7/7 structural mutation catches and 10/10 verifier gates passed.

No fresh external zero-context semantic review was run, so the grade does not exceed
`VERIFIED-WITH-CAVEATS`.

## Premise and completeness audit

This result is conditioned on the `CHOSE` stationary equatorial areal/lock metric slice, the
data-conditioned `CHOSE/OBSERVED` P1 shape family, the sampled free mixing completion, scalar
`Box_g`, real frequencies, `m=-1,0,+1`, and the two free D/N wall representatives.  The regular
center and compact endpoint equations are derived within that slice.  `R_w=c=1` is a unit choice.

Not covered: full 4D/spherical nonseparable modes, higher `|m|`, the Robin wall family, complex
frequencies, time-live geometry, other profiles, source/statistical weights, amplitudes, heights,
polarization, native action/source, or physical mode populations.  No carrier, matter law, or CMB
explanation follows.

## Four evidence gates

1. Preregistered: yes, including both numerical correction layers before mutation.
2. Scope: the full frozen 462-row FD1 census, but only the declared scalar slice.
3. Independent verification: yes numerically and structurally; external semantic review absent.
4. Premises audited: yes above and in the preregistrations; no premise is promoted to native law.

## Next boundary

Freeze this blind Phase-I package before any observational readout.  Then rerun the already
registered affine comparison on the complete corrected families without assuming same-index
triplets are physical multiplets.  Stop again before FD2.
