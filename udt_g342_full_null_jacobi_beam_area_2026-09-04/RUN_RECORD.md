# G342 run record

Date: 2026-09-04
Python mode: `python3 -S`, standard library only
Device: CPU; no GPU process launched
Long solve: none

The initial production finite-axis miss is recorded verbatim in
`PREREGISTRATION_EXECUTION_NOTE.md`. The corrected production run passed `4720/4720`; the
implementation-distinct metric-curvature/RK run passed `2080/2080`; hostile controls passed
`10/10`. All registered replays use `UDT_NO_WRITE=1` and `PYTHONDONTWRITEBYTECODE=1`.

The authorized sealed external review authenticated 30 payloads, reproduced the registered
replays, independently reconstructed the load-bearing mathematics, and returned
`ACCEPT_G342_BOUNDED_FULL_NULL_JACOBI_BEAM_AREA` with no finding at any severity.

Before banking, the complete 325-row scientific-premise/startup verifier passed, and the full
repository suite passed 220 tests with one declared expected xfail.
