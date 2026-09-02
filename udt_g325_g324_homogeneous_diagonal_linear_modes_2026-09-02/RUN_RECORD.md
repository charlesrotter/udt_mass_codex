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

## Exact replay

Run the four commands in `REPLAY_COMMANDS.txt`. The first three write only beneath
`.review_runtime`; the fourth checks exact equality with the banked artifacts and document gates.
