# G195 no-write evidence-repair preregistration

Date: 2026-08-20

The fresh external review returned `G195_INDEPENDENCE_OR_EVIDENCE_GATE_FAILS`. It accepted the
bounded mathematical theorem and found one evidence-packaging defect: the intake did not expose a
completed package-level no-write replay artifact.

## R1 — freeze and expose the registered no-write replay

Run the existing registered command from the repository package without changing the scientific
implementation:

```bash
G195_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 \
python3 udt_g195_antisymmetric_screen_rotation_boundary_2026-08-20/verify_package.py --no-write
```

Capture its stdout outside the package, require exit status zero, parse it as one JSON object, and
preserve that exact object inside the package as `NO_WRITE_REPLAY_RESULT.json`. The frozen object
must report all of the following:

- `status: PASS`;
- `no_write_replay: true`;
- 266 independent histories and 5,059 assertions;
- 18 hostile catches;
- fresh artifact identity and hostile stale-artifact detection;
- unchanged registered error values and bounded pending-review grade.

After adding the frozen artifact, rerun the same no-write verifier with stdout captured outside the
package. It must again exit zero, return the same registered result, and prove that every package
evidence digest—including the frozen replay artifact—remained unchanged during execution.

## Frozen scientific content

No mathematical or census repair is authorized. The coframe, arbitrary functions, supplied germ,
connection, tide, ordered factorization, exact Gram proof, production result, independent result,
profiles, seed, counts, tolerances, hostile catches, and bounded landing are frozen.

## Follow-up gate

Build a fresh sealed intake containing the original review record, this preregistration, the frozen
no-write replay result, and the unchanged evidence. Request a repair-only external review limited to
R1 and the retained bounded theorem. Banking remains prohibited until that reviewer runs or audits
the registered replay and returns an accepting repair verdict.

Maximum repair conclusion: the visible no-write evidence gate closes. The scientific conclusion
may not be strengthened.
