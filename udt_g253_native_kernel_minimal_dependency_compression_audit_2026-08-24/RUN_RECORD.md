# G253 run record

Date: 2026-08-24

All commands were run from `/home/udt-admin/udt_mass_codex`.

## Production replay

```text
manifest sources: 21
nodes: 17
edges: 12
typed graphs: 3
exact rational trials: 4096
formula assertions: 21510
founded-depth samples: 513
unsupported edges: 0
```

## Independent replay

```text
independent trials: 12000
independent assertions: 49602
source assertions: 15
production module imported: false
production output read: false
```

## Hostile replay

All 23 registered mutations were caught, including P1, G116, G189, `X_max`, fit, outcome,
protected-input, post-readout-orchestra, `phi`-only angular, scale-rewrites-depth, and
working-premise-promotion mutations, plus missing, mismatched, and conflicting dual-layout source
failures. Matching repository and sealed source layouts pass as two positive controls.

## External review and repair

The fresh `gpt-5.4` review verified all 45 sealed payload hashes and retained the bounded scientific
landing, but returned `REPAIRS_REQUIRED` because the registered production, independent, and package
replays could not resolve scientific sources under the sealed `sources/` prefix. The repair was
preregistered before implementation. The production, independent, and package verifiers now use a
hash-aware, fail-closed resolver for repository and sealed layouts. Local no-write production and
independent outputs remain unchanged.

A fresh 50-file sealed replay at `/tmp/udt_g253_review_mjtlwrd8` passed all four registered commands.
Production and independent outputs remained identical to the stored scientific results, the 23-case
hostile result matched its stored result, and `verify_package.py` returned `PACKAGE_PASS`.

Because this replay record itself changes the package payload, the repair-only review builder must
produce one final fresh seal. External repair-only follow-up remains pending.

## Repository gates

`verify_current_scientific_premises.py` exited zero:

```text
PASS: 235-row premise registry and current startup/premise guards
```

The full suite returned:

```text
157 passed, 1 xfailed in 62.37s
```

The xfail is the registered matter-sector habit-pin gate and is unrelated to G253.
