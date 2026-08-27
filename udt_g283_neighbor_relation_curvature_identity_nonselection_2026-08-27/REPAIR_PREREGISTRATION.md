# G283 external-review repair preregistration

Date: 2026-08-27

The fresh external reviewer accepted the bounded scientific landing and registered exactly three defects. The repairs below are evidence and packaging work only. They must not alter the witness family, derivation, source universe, scientific question, or landing.

## R1 — self-contained sealed replay

The intake builder currently excludes `build_review_intake.py`, although `verify_package.py` requires it. Include the builder in the sealed package so every registered replay command can pass from the intake copy.

Acceptance: a newly sealed intake contains the builder, all payload hashes/sizes and counts verify, and all five registered commands pass in an isolated writable replay copy.

## R2 — sealed preregistration chronology

The original package names preregistration commit `18100a3a` but the intake contains no object-level chronology evidence. Add a dependency-free chronology verifier and sealed raw Git commit-object payloads proving:

- full preregistration commit `18100a3a4a6721be4544cebe2e5e12cc84178167`;
- full outcome commit `98403a7485c9e72ffe30fa5571abb603a3b74668`;
- the outcome commit directly names the preregistration commit as its parent;
- the preregistration file's Git blob ID is `96d91d1143a84fa3bf6785bd17e239ed4ff44b73` and matches the sealed file;
- raw commit payloads recompute to the claimed Git object IDs without repository access.

Acceptance: the dependency-free verifier passes in the sealed replay and is required by `verify_preregistration.py` and `verify_package.py`.

## R3 — exact two-function trace-free proof

Replace the proxy `b != 0` test with an exact symbolic construction

```text
T_tf = [[p(u), q(u)], [q(u), -p(u)]]
```

and verify trace zero plus separate nonzero derivatives with respect to both independent symbolic placeholders. The result JSON must expose the two retained functions explicitly.

Acceptance: the production derivation and package verifier fail if either independent trace-free function is erased.

## Frozen landing

```text
ARBITRARY_SMOOTH_TIDAL_HISTORY_SURVIVES_OWNED_IDENTITIES
__VALUE_LAW_STILL_MISSING
```

No field equation, action, source, observation, fit, scale, physical population, history, or `X_max` may enter these repairs.
