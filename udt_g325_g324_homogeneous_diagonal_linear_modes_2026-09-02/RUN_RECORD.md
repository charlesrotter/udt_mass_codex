# G325 run record

Date: 2026-09-02

## Environment

- Python: `3.10.12`
- external Python packages: none (`python3 -S`)
- GPU: not used
- long/background process: none

## Chronology

1. Preregistration committed and pushed as `3875663f` before production execution.
2. Production exact ODE/mode calculation passed.
3. The first independent tensor replay stopped because the verifier expression class lacked value
   equality. Equality was implemented; no scientific formula changed.
4. A vacuous production assertion was removed before evidence banking.
5. The first hostile replay correctly refused a proposed “wrong scalar coefficient” control:
   multiplying the whole scalar mode only renames its free amplitude. The invalid control was
   replaced by a wrong *relative directional shape*, which the equation must reject.
6. Production, independent direct tensor, and all five repaired hostile controls then passed.
7. The fresh sealed external reviewer independently rederived the six-constant solution and
   accepted the bounded census. It identified one further non-load-bearing tautological production
   assertion.
8. Repair R1 was preregistered at commit `28e28742`, applied at commit `ec760b87`, and removed that
   assertion without changing the metric, equation, solution, mode count, or classifications.
9. The repair-only reviewer authenticated all 33 payloads, ran the four registered commands
   literally, found all three regenerated JSON artifacts byte-identical to the banked artifacts,
   confirmed the direct independent Lie-derivative witness remained, and accepted R1 plus the
   unchanged bounded landing.

## Exact replay

Run the four commands in `REPLAY_COMMANDS.txt`. The first three write only beneath
`.review_runtime`; the fourth checks exact equality with the banked artifacts and document gates.
