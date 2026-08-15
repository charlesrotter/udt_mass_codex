# External-review adjudication — native radiative current and energy ownership

Date: 2026-08-15

## Accepted landing

```text
VERIFIED_WITH_CAVEATS
__GEOMETRIC_RESPONSE_AND_PHASESPACE_TRANSPORT_ONLY
__PHYSICAL_TRANSFER_OPEN
__EPSILON_ONE_OVER_Z_ONLY_AFTER_ONE_CARRIER_COVECTOR_IDENTIFICATION
```

The sealed 24-file intake had `REVIEW_SCOPE.json` SHA-256
`3804ebceee666d3b2d3514ea312adbd4cf9df15b7cc888c3926f43f373d13bcb`. The fresh external
reviewer was restricted to that intake, read-only operation, and no network access.

## What survived

- The full Lorentz, four-dimensional screen, pair-normal, and toric/Hopf connection homes remain
  correctly separated. Only the conditional four-dimensional screen reduction is an in-scope 4D
  Abelian home.
- `F=dA`, `dF=0`, `J3=d(*F)`, and `dJ3=0` form a valid Maxwell-shaped response complex, but the
  two closedness statements are identities and `J3` is defined response, not physical radiative
  cargo or a source-free field equation.
- The reviewer independently reproduced `A=t^2 dx`, for which `d(*F)` is nonzero, and the flat
  phase-space witness with zero Hamiltonian divergence but `X_H(x^0)=-p_0`.
- Phase-volume preservation does not select or populate a collisionless distribution.
- `epsilon=1/Z` is conditional on identifying a physical carried covector `p=C k_flat` and energy
  `E_u=-p(u)`. The normalization cancels, so no absolute normalization or `hbar` is required for
  that ratio.
- `eta=1` still requires a physically identified conserved carrier measure/distribution and zero
  side flux. A full Maxwell action is sufficient machinery but is not necessary for this narrow
  transparent-propagation closure and is not derived here.

## Accepted evidentiary repair

`verify_package.py` is explicitly a package-consistency gate over saved outputs, tables, and status
text. It is not counted as an independent mathematical derivation. The evidence layers are:

1. the primary SymPy derivation;
2. the implementation-distinct standard-library exact-Fraction replay;
3. the fresh sealed reviewer's independent reconstruction and no-write reruns; and
4. the package verifier, used only to fail closed on record consistency.

No scientific equation or status changed under this repair.

## Four gates

1. Preregistered: **PASS**.
2. Full or bounded: **PASS only for the declared regular local candidate-home and transfer-ownership question**.
3. Independently verified: **PASS WITH CAVEATS** by the exact-Fraction replay and fresh sealed reconstruction; the package verifier is consistency-only.
4. Premises audited: **PASS** for the declared geometry, connection, carrier, energy, current, action, and excluded global/singular scopes.

## Maximum conclusion

The metric supplies conditional geometric response and null phase-space transport structure. It
does not yet supply physical radiative cargo or transparent-transfer closure. The next decision is
whether to continue seeking a metric-owned carrier law or explicitly introduce the minimal
transparent null-carrier premise; neither is adopted by this audit.
