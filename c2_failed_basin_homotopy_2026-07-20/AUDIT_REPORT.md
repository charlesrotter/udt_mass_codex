# Conditional C2 Failed-Basin Homotopy Audit

Date: 2026-07-20

Base: `33eaed961d4601019ee59df5ee8aa59fdc105353`

Preregistration: `a7736ea`; implementation freeze: `1e8d1f9`; complete-ledger correction: `e015cf7`

Mode: CPU float64 pseudo-arclength continuation in the conditional stationary toric `C^2` tile

## Result

`29_OF_51_FORMERLY_UNRESOLVED_PATHS_NOW_CERTIFIED_ROUND; 22_REMAIN_UNRESOLVED`.

Every one of the 51 exact direct-Newton failures was traced with the artificial equation

`F(q) - lambda F(q0) = 0`.

Twenty-nine paths crossed `lambda=0`, were solved against the unchanged stationarity equation, and
passed both the raw `1e-9` and higher-order/doubled-grid `1e-7` gates.  Every endpoint is the same
round gauge-fixed orbit; the largest endpoint coefficient norm is
`3.553635345703164e-11`.

Twenty-two paths reached their registered 180-second limit at positive `lambda`.  Their smallest
final `lambda` is `0.11787904611236555`.  They remain unresolved.  Time-limited continuation is not
evidence that a branch is absent.

## What changed from the parent census

- All 14 former order-two failures now reach the round endpoint.
- Order four splits into 15 certified round endpoints and 22 unresolved paths.
- Single-sector starts split into 19 round and four unresolved; the four unresolved starts are the
  order-four lapse pair in the even and odd-shift sectors.
- Mixed starts split into ten round and 18 unresolved.
- Seven paths reverse the sign of their `lambda` tangent at least once.  These are folds of an
  artificial solver homotopy, not physical time evolution or new UDT structure.

No nonround reduced endpoint appeared.  The registered direct Bach promotion gate was therefore not
triggered.  Its round bulk anchor passes, while the primitive-cap boundary remains explicitly open.

## Complete-ledger correction

The first official run produced the same 29/22 result but retained norms rather than every
intermediate coefficient vector.  It is preserved byte-for-byte.  Before rerunning, a correction
committed full accepted/rejected state logging without changing a numerical or physical control.
The authoritative return reproduces the status and endpoint class of all 51 identities exactly.
Wall-clock-limited paths may contain a different final accepted point; their classification does not
change.

## Independent gates

- All 1,764 accepted homotopy states were recomputed from their saved coefficient vectors.  The
  maximum raw homotopy residual is `9.970122505364998e-10`; stored and recomputed norms agree exactly
  at recorded precision.
- Centered finite differences of the reduced action independently reproduce selected automatic
  stationarity gradients with maximum scaled error `7.303861194432221e-8`.
- The direct all-component Bach implementation gives maximum round bulk residual
  `5.919487592309094e-9` at the edge of its conditioned interior interval and about `2.9e-15` at the
  midpoint.
- The preserved first return and complete-ledger rerun have identical 51-row status/endpoint identity
  sets.
- Source identities, tables, endpoint gates, and 20 fail-closed mutations pass.

## Interpretation and evidence grade

The round stationary metric is now supported by more than the original direct Newton basin: an
artificial continuation repairs 29 starts that previously stalled, including every order-two
failure.  This materially strengthens the bounded broad-round-basin observation.

It is not a uniqueness theorem.  Twenty-two order-four paths remain open, and the calculation still
omits physical cap/boundary completion, endpoint-singular functions, higher and nonpolynomial modes,
nontoric topology, unrestricted metric components, genuine time dependence, alternative actions,
carrier/source emergence, scale, `X_max`, and mass.

Grade: `VERIFIED-WITH-CAVEATS`.  The test was preregistered; the complete 51-path finite census was
run twice at identity level; load-bearing saved states and gradients were independently recomputed;
and every premise was audited.  No fresh different-model review was authorized.

Maximum conclusion:

`FAILED_BASIN_HOMOTOPY_CHARACTERIZED_IN_CONDITIONAL_STATIONARY_TORIC_C2_TILE; BROAD_ROUND_BASIN_STRENGTHENED; UNIQUENESS_OPEN`.
