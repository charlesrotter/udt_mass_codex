# G311 run record

Date: 2026-09-01

## Regime

- regular local four-dimensional Lorentz metric;
- all locally realizable orthonormal timelike--spacelike pair germs;
- exact arithmetic for rank/projector checks;
- exact dependency-free time-live countermetric reconstruction from metric two-jets;
- conditional G301 Cauchy classification only after the response boundary is stated.

## Outcomes

- production exact checks: 24 passed;
- independent dependency-free exact checks: 14 passed;
- shared-code hostile regression mutations: 6/6 caught;
- exact current-premise/startup verifier: `PASS` (293 rows);
- full repository regression suite: `211 passed, 1 known matter-sector xfail`;
- no GPU, numerical grid, tolerance, observation, fit, or long solve used.

## Data and choice ledger

- rational rotations and boosts: `MATHEMATICAL_METHOD`, changed in the independent implementation;
- Lorentz signature `(-,+,+,+)`: `CHART/METHOD`, no physical preferred frame;
- four spacetime dimensions: `CURRENT_UDT_COMPLETE_METRIC_ARENA`;
- Universal Reciprocity/DDR: `OWNER_ADOPTED_PROVISIONAL_POSTULATE__NOT_DERIVED__NOT_CANON`;
- G301 response formula: `CONDITIONAL`, never used in the unconditional projector theorem;
- FLRW-form countermetric parameter `b=1,t=0`: `MATHEMATICAL_WITNESS`, not fitted physics;
- sources, action, matter, mass, scale, observation, boundary, physical `X_max`: `OMITTED`.

## External review and registered repairs

- fresh external verdict: `G311_REPAIRABLE_DEFECTS`;
- bounded scientific landing: independently upheld without scientific defect;
- R1: undeclared SymPy dependency removed; independent replay now runs under `python3 -S`;
- R2: aggregate sealed replay no longer accesses repository paths or Git history;
- R3: hostile harness graded `SHARED_CODE_REGRESSION_NOT_INDEPENDENT_CONFIRMATION`;
- repair-only external follow-up: `G311_ACCEPTED_WITH_RESPONSE_CONSTITUTION_BOUNDARY`;
- remaining registered defects: none.
