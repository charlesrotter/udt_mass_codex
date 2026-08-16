# G111 audit report — nonflat complete-metric replay

Date: 2026-08-16

Status: `BLIND_VERIFIED_WITH_REPAIRS`

## Learned

The G110 reconstruction is not a flat-space artifact. On the complete nonflat R17 control family,
one supplied observer exponential simultaneously produces:

- a regular pair block and terminal `phi_pair` series;
- an independent rank-two celestial Jacobi block;
- mixed pair/angular contractions;
- nontrivial angular expansion and shear.

All 192 metric controls and 1,152 direction controls survive. Every optical tidal matrix is
nonzero, every pair-screen leading vector is nonzero, and 1,088 controls have nonzero cubic sky
shear. Reversing the twist changes a retained optical trace by as much as `4.451081856984935`, so
the twist sector is not silently erased.

## Raw gates

- exact symbolic metric/coframe/connection/Riemann identities: pass;
- complete census: `192` metric and `1152` directional controls;
- maximum symbolic optical-symmetry residual: `5.55e-17`;
- maximum mixed compatibility residual: `0`;
- independent exact exterior-form replay: all `64` brackets, `64` connection coefficients, and
  `256` Riemann components agree componentwise;
- supplementary independent finite-difference replay: all `1152` rows pass;
- largest independent sky determinant residual: `1.3483e-5` against `2e-4`;
- largest independent pair quadratic residual: `6.7743e-7` against `2e-5`;
- seven hostile catch proofs: pass.

The exact comparison uses a separate exterior-form construction and component hashes. The
finite-difference moving-frame replay remains supplementary because its tolerances were not frozen
in the preregistration.

## Correction caught before acceptance

The first implementation incorrectly treated ordered second derivatives in a noncommuting frame as
independent. Exact pair exchange and Bianchi checks rejected it. The repaired six-jet construction
obeys the Maurer--Cartan relations and all identities. See `CORRECTION_RECORD.md`.

## Not learned

This calculation does not select the R17 family, `phi(q)=epsilon q0`, a physical history, a global
observer query, endpoint occupancy, source weights, SNe, BAO, CMB, flux, bootstrap, or `X_max`.
It validates the geometry evaluator only on the preregistered bounded family.

## Blind-review repair

The first blind return was `REPAIRS_REQUIRED`. It accepted the core geometry but found that the
original harness did not meet F03 or F10 literally. The repair adds an implementation-distinct
exact componentwise Cartan replay, executable same-`W`/Riemann/vertex mutations, exact normalization
residuals, and an independently formed mixed coefficient. Bounded follow-up returned
`REPAIRS_VERIFIED` with no remaining failure.
