# G125 blind review — raw bounded return

Verdict: `PASS_WITH_REPAIRS`

The reviewer independently reproduced both machine artifacts byte-for-byte and accepted the
inversion, junction sign, unchanged luminosity curve, decomposition nonuniqueness, and `X_max`
guard.

Required repairs:

1. State the inversion domain as `0<R<R_inf`; `R=0,Z=1` is its continuous boundary closure.
2. Separate exact validity of the frozen functional family from observational support limited to
   the evaluated SNe range; the formal `R->R_inf` limit is extrapolation.
3. Do not call equation (5) a constraint on any live UDT history. It applies only after the same
   G119 query, G120 imported transfer, processed-release frequency slot, and frozen P1 curve are
   supplied, and is not independent evidence for G124.
4. Rename the `(a,b)` witnesses as terminal allocations, not stationary/screen/source realized
   histories.
5. Replace a vacuous orientation comparison with a signed `K=+q` versus `K=-q` control and add a
   wrong-screen-log-sign mutation.
6. Make package verification rerun both implementations in isolation and byte-compare the outputs,
   rather than trusting saved JSON booleans.
