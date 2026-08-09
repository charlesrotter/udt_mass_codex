# FD2 upstream correction final report — regular center changes the spectral picture

Date: 2026-08-09  
Landed status: `UPSTREAM_FD1_WITNESSES_WITHDRAWN — VERIFIED-WITH-CAVEATS`

## What was learned

FD2 could not honestly begin its observational profile inversion because its four inherited FD1
background witnesses were certified with a center discretization that does not represent the
regular `m=0` branch correctly.

The exact original radial equation, analytic Bessel controls, continuum flux shooting, and adaptive
collocation agree on the correction:

- Neumann `m=0` has an exact constant `omega=0` mode;
- the positive `m=0` roots shift by up to `113.9%` relative to like-indexed FD1 roots;
- the `m=+/-1` roots move by no more than `0.106%`;
- the corrected families interleave; same radial index does not produce the inherited nearly
  degenerate `m=-1,0,+1` triplet.

The attributed Planck readout retained all modes, both Neumann conventions, and the exact FD1 affine
and trough diagnostics. All six comparison rows are `SPLITTING_ONLY`. Zero rows retain full centered
multiplet containment, and zero rows put every carried component between the actual adjacent
troughs. The four backgrounds therefore do not survive as FD1 strict witnesses.

## What remains from the old picture

The corrected `m=0` ladders still project through the two-freedom affine map with a maximum
fractional residual of about `3.166%`–`3.180%`. The one-scale map still misses by at least `26.71%`.
Thus the generic scalar cavity comb remains a weak channel-level observation, with the additive
offset still load-bearing. It is not a full CMB spectrum or a native projection.

RA1's analytic wall endpoint classification is unchanged. The correction affects finite numerical
roots, center phase, overtone indexing, RA2's finite comb readout, and FD1's multiplet interpretation.

## FD2 disposition

The preregistered profile inversion did not run. Its blind low-order-FEM response atlases failed
their derivative-convergence gate, and the continuum refinement then exposed the upstream center
problem. Under the frozen contract:

```text
FD2 profile-response question: OPEN, NOT NEGATIVE.
Four inherited FD1 seed witnesses: WITHDRAWN.
Full corrected background atlas: REQUIRED before an all-channel FD2 continuation.
m=0-only profile characterization: possible only under a separately explicit channel-slice reframe.
```

No profile feature, matter-content structure, SNe compatibility result, source law, polarization
channel, native action, or CMB explanation is claimed.

## Numerical and independent gates

- Bessel `J0`/`J1` controls: maximum relative error `<6.96e-14`;
- 84 positive shooting roots and two exact Neumann zero modes;
- maximum shooting normalized wall residual `2.066e-11`;
- 84/84 adaptive-collocation roots successful;
- maximum shooting/collocation frequency disagreement `8.337e-11`;
- maximum collocation wall residual `1.310e-10`;
- six attributed comparison rows; all `SPLITTING_ONLY`;
- independent saved-artifact replay: 8/8 gates;
- six mutation catch-proofs: 6/6 rejected.

The failed first collocation return remains preserved. No tolerance was relaxed. No fresh external
zero-context semantic review was run in this turn; that prevents a stronger grade than
`VERIFIED-WITH-CAVEATS` despite the independent numerical methods.

## Premise and completeness audit

- Metric/probe: the same `CHOSE` stationary equatorial scalar `Box_g` slice.
- Center: regular/no-log branch from the exact radial equation; not a new boundary mechanism.
- Wall: both D/N anchors remain `free-and-explored`; no physical boundary selected.
- Projection: affine `ell=a omega+b` remains `CHOSE`, two fitted freedoms.
- Pairing: same-index `m` pairing is now explicitly a historical diagnostic, not a derived
  observational multiplet law.
- Complete sphere, higher `|m|`, vector/tensor probes, Robin walls, time-live backgrounds, source
  statistics, native dynamics, heights, polarization, profile law, and physical mode populations
  remain open.

This is one corrected spectral tile, not a complete solution-space census.

## Hashes

```text
8fe6c747b5f2629e6fbd4ddb44bd40452d39052a71adc1aa46cfbad1771ae567  center_spectrum_phase1.json
e2a9ac2bc01862b78394ce3111473ec18a1491fb256bc7624bf62f7923c73246  center_spectrum_phase2.py
a1d8c66091f2e7bf831ed54e28c2b68db9d5870ff73ddcd114b2bcc1cdba7722  center_spectrum_phase2.json
7bce3dac0c8d922d7b45985d40f129c0ae0457f8bab24168914ca34a2cf74433  verify_center_spectrum_correction.py
e5fd466b11d151634e1a296c178e3f3af41c459d99c4a5bdeef9debe2c58647b  center_spectrum_verification.json
```

## Next bounded decision

Do not resume the original FD2 inversion from the withdrawn four witnesses. The next scientific
choice is between:

1. a full corrected `(n,q,hbar,wall,m)` atlas to determine the actual all-channel background
   structure without assuming same-index triplets; or
2. an explicitly narrower `m=0` profile-response characterization, carrying the fact that other
   angular families and their observational populations are unresolved.

The first is the purer continuation. The second is cheaper but cannot answer the former multiplet
compatibility question.
