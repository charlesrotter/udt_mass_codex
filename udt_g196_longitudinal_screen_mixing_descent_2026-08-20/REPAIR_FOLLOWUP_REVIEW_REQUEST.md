# G196 repair-only external follow-up request

Date: 2026-08-21

Review only the two preregistered repairs and whether they leave the accepted bounded theorem
unchanged. Do not continue the research or broaden the family/germ scope.

## R1 — independence description

Verify from prose and code that the current package now distinguishes:

- independently implemented Torch metric-jet, Riemann, screen-connection, and tide contractions;
- formula-level direct-versus-ordered Jacobi IVP regression using the shared separately coded
  `candidate_matrices(...)` path.

Reject R1 if any current evidence report calls the IVP leg a fully independent metric-to-Jacobi
derivation, or if the original preregistration was silently rewritten rather than visibly
corrected.

## R2 — strict read-only replay

Run the exact `registered_replay` from `REVIEW_SCOPE.json` in a strictly read-only sandbox. Wait at
least 30 minutes unless it exits earlier; the package wrapper is deliberately silent while child
legs run. Verify:

- exit zero;
- fresh/sealed production, independent, and hostile artifacts are identical;
- all counts, ceilings, and results are unchanged;
- no evidence file or runtime path changes;
- the no-write Torch import succeeds without requiring a writable temp directory.

## Allowed landing

Return exactly one:

- `G196_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED`;
- `G196_R1_INDEPENDENCE_SCOPE_REPAIR_FAILED`;
- `G196_R2_READ_ONLY_REPLAY_REPAIR_FAILED`;
- `G196_REPAIRS_INTRODUCE_SCIENTIFIC_REGRESSION`;
- or a sharper bounded landing if necessary.

State the strongest retained theorem, any exact defect, live replay status, pre/post hash status,
and maximum honest conclusion. Do not promote G196 beyond the displayed `a(eta),M(eta,z)` affine
family and one supplied central outgoing germ.
