# Full corrected spectral atlas — final report

Date: 2026-08-09  
Landed status: `CORRECTED_FULL_SCALAR_ATLAS_VERIFIED_WITH_CAVEATS__OLD_FD1_MULTIPLET_WINDOW_WITHDRAWN`

## Outcome

The entire old 462-row FD1 census has been replaced by an original-field, regular-center,
exact-endpoint atlas.  It contains 420 nonzero-mixing rows, 42 zero-limit controls, and 10,080
positive roots.  The corrected geometry is three interleaved angular ladders, not a generally
centered same-index `m=-1,0,+1` multiplet.

The old FD1 `OPEN-COMPATIBILITY-WINDOW` conclusion is withdrawn for the complete frozen census, not
only for its four named witnesses.  Under the identical historical same-index Planck-basin
diagnostic, all 630 corrected convention rows are either `SPLITTING_ONLY` (503) or
`BASIN_MISMATCH` (127); zero have full-centered containment.

This does not refute a CMB role for the resonator.  It removes an unjustified multiplet
interpretation and exposes the missing object cleanly: a native rule for which angular ladders and
radial modes carry observable power.

## Blind geometry

- all 630 D/N channel pairs strictly interlace;
- q=0 exact splitting error: `1.8944e-12`;
- 505/3,360 same-index positions place `m=0` between the rotating partners;
- only 44/420 rows do that for all eight indices;
- same-index displacement: minimum 6.08%, median 16.08%, 95th percentile 100.75%;
- optical wall length spans `0.9516` to `10860.0062` across the frozen freedom;
- certified maximum normalized wall residual: `5.0948e-9`.

Relative to the withdrawn transformed-field atlas, median frequency changes are 0.0385% (`m=-1`),
12.496% (`m=0`), and 0.0435% (`m=+1`).  The error was concentrated in the old `m=0`
`sqrt(r)R` center representation.

## Attributed readout

The Planck Table 5 positions were opened only after blind commit `2ef02737`.  Each ladder was then
fit separately with the inherited two-parameter affine map, while both Neumann zero conventions and
all 24 positive lines were retained.

- rows crossing the old 3.1% comparison marker: `m=0` 4/630, `m=-1` 63/630, `m=+1` 78/630;
- best maximum fractional residuals: 3.083%, 2.570%, and 2.251%, respectively;
- median line count per published trough basin under any ladder anchor: 3;
- the earlier six central-witness readouts reproduce to `4.34e-11` relative.

These are attributed compatibility/crowding statistics, not predictions.  The two fitted affine
freedoms, generic cavity-comb character, absent mode weights, absent source statistics, and absent
polarization law all travel.

## Numerical correction history

Both failed production returns are preserved.  The first complete atlas failed its wall-residual
gate in 54 near-critical Dirichlet row/channels.  A strict all-root replay exposed a factor-of-two
root-count typo and left three channel maxima just above gate.  Separately preregistered stricter
root certification changed no branch: the largest all-root shift was `5.7209e-11`, and the final
24-root correction moved a frequency by at most `1.0953e-15`.

Independent blind verification reproduced 63 preregistered roots to `2.0633e-12` relative, passed
flat Bessel controls at `1.3678e-13`, and fired 7/7 mutation catches.  Independent attributed replay
passed 7/7 gates.  No external zero-context semantic review was run; status therefore remains
`VERIFIED-WITH-CAVEATS`.

## Premises and what remains open

The atlas is conditioned on the `CHOSE` stationary equatorial scalar `Box_g` slice, the
data-conditioned P1 shape family, sampled mixing completion, real `m=-1,0,+1`, and free D/N wall
representatives.  It does not cover the full 4D sphere, higher `|m|`, Robin data, complex modes,
time-live geometry, alternative profiles, vector/polarization channels, source statistics, native
action/source, or a physical population rule.

FD2 remains `OPEN_NOT_RESTARTED`.  Its old four witness seeds are withdrawn, and the full atlas does
not select a replacement background.  Restarting FD2 now would require an explicit rule for which
ladder/profile family is being characterized; choosing the four best standalone affine rows would
be template-led post-selection.

## Four evidence gates

1. Preregistered: yes, including all numerical corrections and attributed-readout protocol.
2. Scope: complete frozen FD1 census in the declared scalar slice; broader geometry remains open.
3. Independent verification: yes, separate numerical replay and attributed semantic/count replay;
   no external zero-context review.
4. Premises audited: yes; no scalar probe, wall datum, pairing, or affine fit is promoted to native
   UDT physics.

## Stop boundary

Stop here.  Do not restart FD2, assign source weights, choose a surviving ladder, run polarization,
or make a CMB prediction without a new explicit dispatch.
