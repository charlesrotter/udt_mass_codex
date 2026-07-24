# Verification report

The production and independent scripts are separate standard-library
implementations. The independent script imports no production audit module.

Final required gates:

- production exact controls: 20;
- frozen source identities: 35;
- candidates: 32;
- principle/object types: 15;
- completion classes: 12;
- injected adversarial failures caught: 20;
- native single-line selectors found: 0;
- reciprocal-swap gluing: mathematically valid but not selected.

Exact commands, Python/platform data, return codes, raw stdout/stderr hashes,
repository-wide tests, frozen manifests, navigation counts, and dirty-checkout
metadata are preserved in `RUN_ENVIRONMENT.json` and
`REPOSITORY_GATES.json`.

Semantic caveat: no fresh zero-context external model review was authorized.
The grade is therefore `VERIFIED-WITH-CAVEATS`, not canon or complete
scientific closure.

