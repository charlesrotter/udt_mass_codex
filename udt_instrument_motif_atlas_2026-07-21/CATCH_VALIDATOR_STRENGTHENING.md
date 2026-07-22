# Catch-Validator Strengthening Preregistration

Date: 2026-07-21

Status: `PREREGISTERED_BEFORE_STRENGTHENED_REPLAY`

The production K03/K04 edge catches and the independent K03/K04 edge/operator catches reject the
intended mutations, but their current implementations use catch-local count predicates rather than
the same fail-closed validators exercised by saved production data. This is an evidence-quality
defect, not an observed scientific discordance.

Before final banking:

1. create a reusable production edge validator that checks the exact 75 identities, one-bit
   direction, source/destination family identities, edge IDs, and added-instrument labels;
2. call that validator on the production edge registry and on missing/duplicate-edge catch inputs;
3. create a reusable production operator-count validator from the registered group keys, call it on
   every classified family, and pass a dropped-operator mutation through it;
4. independently construct and validate the exact 75-edge identity set in the independent verifier;
5. independently derive expected operator count from group keys and pass a dropped-operator mutation
   through that validator;
6. replay the full atlas and both independent verification layers without changing classifications,
   tolerances, inputs, premise labels, or maximum conclusion.

All pre-strengthening commits and outputs remain in Git history. No outcome may be retuned or
reclassified through this correction.
