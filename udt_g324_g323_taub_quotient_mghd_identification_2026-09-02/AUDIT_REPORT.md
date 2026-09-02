# G324 audit report — Taub quotient MGHD identification

Date: 2026-09-02
Status: `PASS_PENDING_EXTERNAL_ADVERSARIAL_REVIEW`

## Landing

```text
EXPLICIT_TAUB_QUOTIENTS_ARE_SMOOTH_MGHDS__REGISTERED_LATTICE_MODULUS_SURVIVES
```

## What was learned

The explicit G323 quotient is not merely a displayed globally hyperbolic portion of a potentially
larger smooth spacetime. Exact geodesic analysis shows that its expanding end has infinite proper-
time reach for every future timelike geodesic. The standard one-sided extension theorem therefore
rules out a future extension boundary. Any remaining smooth extension boundary must lie toward
`R=0`, but the invariant curvature `12 mu^2/R^6` diverges there and forbids a `C2` endpoint.

Consequently each explicit quotient is already the smooth maximal globally hyperbolic development
of its own fixed G322 datum. G323's primitive compact-lattice modulus therefore survives after the
initial marking is forgotten at the MGHD level.

## Evidence

- production: 29 exact/analytic assertions after source-evidence correction;
- independent: 30 exact tensor/interface assertions after source-evidence correction;
- hostile controls: 5/5 rejected;
- two independent curvature routes: Kasner identities and a direct exact Laurent-tensor engine;
- imported source boundary: Galloway--Ling--Sbierski one-sided extension theorem, explicitly typed
  as mathematical method;
- upstream global-development interface: the already-audited conditional G322 theorem.

The final exact counts are generated in the replayed JSON artifacts and must be checked by
`verify_package.py`; the prose count above is not a substitute for replay.

## Four gates

1. **Preregistered:** yes, commit recorded in `PREREGISTRATION_ANCESTRY.md`.
2. **Full bounded space:** yes for every member of the exact registered G323 Taub quotient family;
   no claim outside it.
3. **Independent:** yes, the independent verifier imports neither production code nor its result.
4. **Premise audited:** yes; both physical-premise ownership and imported theorem ownership remain
   explicit.

External adversarial verification remains required before banking.

## What did not change

No metric coefficient, reciprocal-kernel operator, angular-sector cancellation, field equation,
scale, observation, topology choice, or occupancy rule changed. The result closes one mathematical
continuation gap. It does not choose which allowed spacetime is physical.
