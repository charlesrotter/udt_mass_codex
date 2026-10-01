# Repair checker adapter history

The first prelaunch specs-only execution of `check_repair.py` failed safely:
it applied the old survey-artifact path guard to shared source files under TDS
and TPP, outside the TPS1 package. That guard is intentionally narrow for fields
and cannot authenticate the larger admitted source closure. The first adapter
is retained under `initial_adapter/` and `repair_readiness_run.*` preserves the
failure. No repair fields existed and no scientific result was emitted.

The corrected adapter authenticates every manifest source SHA-256 within the
repository; field/spec paths still use the narrow unchanged guard. The new
`repair_readiness_corrected_run.*` succeeds, recording `REPAIR_READINESS.json`
against the corrected prelaunch dispatch/manifest/map. Five in-memory defects
(initial substitution, threshold loosening, mesh change, absent CFL halving,
wrong step halving) were rejected. No frozen original source was changed.

The adapter authorship is this mathematical review context; the parent must
separately inspect it before use. It calls the unchanged independent TPS1
case checker, records that reuse, and compares the new explicitly named triple
against unchanged original thresholds. It supports only first pair or all26,
preserves every case report, and authenticates any already computed report.
This is operational adaptation, not a new equation checker or independent
general-data time integrator. The original65/13 split is never rewritten.
