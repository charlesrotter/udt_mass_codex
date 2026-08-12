# External adjudication — G81 nonradial screen covariance

## Landing

`VERIFIED_WITH_CAVEATS`.

The fresh sealed `gpt-5.4` review found no blocking correctness issue and required no scientific
correction. It independently reconstructed the exact C1 frame, both rotations, the full tangent
reversal in the raw path arrays, the unrotated and rotated matrix equations, determinant/area
scaling, nonradial endpoint motion, and the nonzero off-diagonal response. It found no missing `Z`,
transpose, sign, inverse, basis placement, hidden diagonalization, or falsely radial control.

The maximum conclusion remains exactly

`DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS`.

For the two fixed controls on the supplied G79/G80 metric/query,

```text
D_reverse = Z transpose(D_forward)
D_reverse_AB = Z B transpose(D_forward) transpose(A).
```

C1 is genuinely angular: its receiver-frame direction is `(12,3,4)/13`; its endpoint is
approximately `(theta,psi)=(1.7493671390260097,0.23079074045919012)`; and its forward off-diagonal
norm is `1.1801666864663825e-3`.

## Binding caveats

1. The reviewer verified all `28/28` G81 package hashes and proved that the remaining nine manifest
   rows equal `SOURCE_MANIFEST.tsv`, but did not reopen those nine bytes because it interpreted them
   as outside its package subdirectory. They were actually included at the sealed intake root.
   Before transmission and again during adjudication, the live checkout independently verified all
   `37/37` payload hashes, including the nine exact frozen source bytes. This closes repository
   provenance locally but does not rewrite the reviewer’s stated evidence boundary.
2. The neighboring-ray replay is bounded independence. It replaces the production Riemann/Jacobi
   equation with locally rebuilt Christoffels and centered neighboring rays, but shares the fixed
   metric/profile, observer query, endpoints, rotations, and the DOP853 integrator family.

## Authority boundary

This is generic Jacobi/Wronskian screen covariance instantiated on two fixed UDT metric controls.
It is not a UDT-specific selector and does not select a physical profile, endpoint, scale, `Xmax`,
source, SNe/CMB observable, `cmb_temp`, action, matter, bootstrap closure, or future signal.

## Smallest next calculation

Without enlarging or retuning the control universe, replay fixed C1 once with an integrator family
other than DOP853. That is a method-independence closure, not a new physical search. Only after that
bounded check should the program open the already-deferred endpoint/`Xmax` curve or temperature
map.
