# G193 external-review repair preregistration

Date: 2026-08-20

The fresh external `gpt-5.4` review returned `G193_ACCEPTED_WITH_REPAIRS`.  It accepted the bounded
scientific landing and identified two evidence-banking defects.  These repairs are frozen before
altering any implementation or claim.

## R1 — sealed replay temp safety

The exact registered `--no-write` replay must execute from a fresh sealed intake.  The first intake
was physically read-only and reviewed under a read-only sandbox; Torch's import chain could not
locate any writable temporary directory and failed before mathematical execution.

Repair contract:

- the corrected intake will retain read-only evidence files;
- it will contain one empty, package-local runtime directory excluded from scientific artifacts;
- the registered replay will set `TMPDIR`, `TMP`, and `TEMP` to that runtime directory for child
  processes;
- the review launcher may use a workspace-write sandbox, while filesystem permissions keep all
  evidence files and directories read-only except that runtime directory;
- the package verifier must prove the runtime directory is empty before and after the replay;
- no scientific artifact may change during `--no-write` replay.

R1 passes only if a fresh sealed external reviewer runs the exact registered command successfully.

## R2 — independence wording

The existing verifier independently reconstructs metric jets and Riemann tides at preregistered
points, then independently solves the direct and factorized matrix IVPs using the closed-form tide.
That is a strong two-leg consistency replay, but it is not an end-to-end metric-derived tide at every
adaptive IVP evaluation.

Repair contract:

- narrow all evidence descriptions to `independent metric-jet/Riemann spot checks plus an
  independently implemented formula-driven matrix-IVP replay`;
- explicitly state that full metric-to-Jacobi propagation over the entire interval remains absent;
- do not reduce any registered history count, assertion count, tolerance, or hostile catch;
- do not alter the theorem, family, equations, saved numeric artifacts, or conclusion scope.

No additional end-to-end solver is introduced in this repair.  The accepted exact proof remains
load-bearing; the numerical replay remains corroborative and is described at its exact strength.

## R3 — optional portability hardening

The reviewer noted exact JSON identity is stricter than tolerance-based portability.  G193 retains
exact artifact identity because the current deterministic environment reproduces it and because it
is a strong stale-artifact guard.  This optional suggestion is recorded but not activated.

## Maximum repair conclusion

At most this repair may close the sealed-replay packaging gate and align the evidence language with
the actual independent implementation.  It may not alter or strengthen the bounded G193 theorem.
