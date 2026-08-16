# G126 evidence gates

1. **Preregistered:** commit `33ff75f4`, before executable evaluation.
2. **Bounded scope:** exact central-spherical screen, ideal reference projection, processed-depth
   chain rule, and banked R5 output type only; no observational arrays opened.
3. **Production:** 15/15 exact symbolic checks pass.
4. **Independent:** 12/12 standard-library Fraction checks pass without importing production code.
5. **Source integrity:** ten source hashes frozen, including R2's exact estimator/window
   preregistration; package replay passed before review and must pass again after repairs.
6. **Premise/startup audit:** 113-row verifier passes; full repository suite passes 90 tests with
   one expected xfail; startup files remain within their fixed bounds.
7. **Blind review:** initial `PASS_WITH_REPAIRS`; all six repairs registered and implemented; fresh
   follow-up `PASS`, including independent reruns and byte identity.

Current maximum status:
`BLIND_VERIFIED_WITH_REPAIRS__NO_CURRENT_R5_TO_K_OR_PHASE_BRIDGE`.
