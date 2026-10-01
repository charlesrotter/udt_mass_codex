# PSW1 tests-perspective finite anchor receipt

`SOURCE_FIRST.md` and `check_anchor.py` were frozen before execution in
`PRECHECK_FREEZE.json`. No other PSW1 proposal had been read. The parent granted
the shared CPU slot, which was explicitly released after this one run.

Exact command, from repository root:

```
python3 udt_time_live_production_survey_2026-10-01/capture.py --memory-mib 2048 udt_positional_selection_whiteboard_2026-10-01/tests/anchor python3 udt_positional_selection_whiteboard_2026-10-01/tests/check_anchor.py
```

Receipt `anchor.json` records return code 0, 0.45936122100101784 seconds,
48,588 KiB child maximum RSS, a 2,147,483,648-byte virtual-address cap,
no wall/CPU timeout and no forwarded signals. `anchor.stdout` reports 33 PASS
assertions under Python 3.10.12 and SymPy 1.13.1; stderr is empty.

The checks directly reconstruct the metric connection and Ric(U,U), verify
geodesic coordinate-fixed clocks for this specific supplied metric family,
test the shear difference, check the closed-form positive/negative null travel
relations and tick ratios, verify their small-L leading terms, and substitute
the isotropic vector into every conformal-Killing tensor component. Several
components vanish by the supplied symmetry; the check count is bookkeeping,
not a measure of scientific independence or scope.

The analytic argument in `SOURCE_FIRST.md` owns branch regularity, physically
matched initial separation/velocity, interpretation of the future return, the
sign inequalities and the distinction between the proposed endpoint-potential
condition and UDT's admitted premises. These are not established by assertion
count. No guard-mutation suite, numerical solution, data fit, raw TPS1 replay,
new full406 audit or independent general-data implementation was performed.
Cross-context challenge remains a separate next stage.

No failed run or source repair occurred in this finite check. The original
source-first bytes remain unchanged after the result. The known prior NCI1,
SGE1, FSL1 and TPS1 repairs remain attributed to their inspected sources.
