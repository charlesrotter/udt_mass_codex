# G125 correction record

Date: 2026-08-16

All six blind-review repairs were implemented without changing the bounded landing.

- The open inversion branch and its observer-vertex boundary closure are separated.
- Observed-range support and formal P1 continuation are separated.
- The score constraint is explicitly conditional on the complete G119/G120/catalog/P1 interface.
- The algebraic decomposition witnesses are called terminal allocations, not realized histories.
- Independent verification now has 13 checks, including a genuine signed-orientation control and a
  wrong-log-sign catch proof.
- Package verification now reruns both scripts in an isolated temporary directory and requires
  byte-identical regenerated JSON.

Post-repair gates: production 16/16; independent 13/13; six source hashes pass; isolated replay and
both byte comparisons pass.

The first bounded follow-up returned `FAIL` on one residual nomenclature defect: independent-code
variables and JSON checks still called the terminal allocations “stationary,” “screen,” and
“source” members. They were renamed to explicit terminal `phi`, screen-rate, and source-clock
allocations before the second follow-up.
