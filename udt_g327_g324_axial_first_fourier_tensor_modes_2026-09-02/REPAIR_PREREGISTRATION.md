# G327 external-review repair preregistration

Date: 2026-09-02
Trigger: fresh external verdict `REFINE__G327_BOUNDED_LANDING`

The fresh reviewer found no scientific defect in the bounded primitive axial tensor census. It
identified three evidence-chain defects. The following repairs are frozen before implementation.
They may not alter the metric, equation, perturbation sector, mode equation, solution basis,
endpoint classification, dimension count, curvature witness, or bounded scientific landing.

## R1 — self-contained exact runtime

Vendor the exact Python dependencies needed by the three registered symbolic programs into one
deterministic intake-local archive. Add an intake-local bootstrap that makes the archive importable
without internet, installation, repository access, protected-package access, or a host user site.
The corrected sealed intake must demonstrate all registered commands from a writable ephemeral
copy with the host user site disabled.

Acceptance:

- the archive contains the recorded SymPy 1.13.1 and its required mpmath dependency;
- the archive and bootstrap are included in and authenticated by the sealed manifest;
- a dependency-isolated probe reports SymPy 1.13.1 from the vendored archive;
- all registered replays complete without internet, installation, or access outside the intake.

Falsification: any registered computation still depends on an unsealed host package path, or fails
when the host user site is disabled.

## R2 — sealed preregistration ancestry proof

Add intake-local, manifest-authenticated evidence containing the raw G327 preregistration commit
object, its name-status change, and the exact preregistration tree entries. The verifier must
recompute the Git commit object identifier from the raw commit payload and require
`9bec301bc265bf67afa5f8398f7557ccdabb855b` exactly. It must also require that only the five frozen
preregistration files entered at that commit and authenticate their blob identifiers.

Acceptance: the corrected intake lets a reviewer validate the commit object and frozen file set
without repository access.

Falsification: the recomputed commit identifier, changed-file set, or registered blob identifiers
do not match the frozen proof.

This proves the content and Git ancestry marker carried by the repository. It is not an external
trusted timestamp or a claim that Git can prove human outcome blindness by itself.

## R3 — literal fourth-command replay

Strengthen `verify_package.py` so its outer run executes all four lines in
`REPLAY_COMMANDS.txt` from one fresh writable package copy. The fourth line must be invoked
literally. A narrowly scoped environment sentinel may tell that nested invocation not to recurse
again; it may not bypass scientific, source-integrity, provenance, or status gates. The outer run
must confirm the fourth command exits successfully and creates its declared ephemeral artifact.

Acceptance: the aggregate artifact records a successful literal fourth-command replay.

Falsification: the fourth line is merely string-checked, is not executed, recurses without bound,
or can pass after a source substitution.

## Maximum retained conclusion

If R1--R3 pass locally and a repair-only external reviewer accepts them, the original bounded
scientific landing may be upgraded only to externally accepted after evidence repair. No full
Fourier-spectrum, linear-stability, nonlinear-stability, endpoint-admissibility, occupancy,
history, scale, observation, matter/mass, or physical `X_max` conclusion follows.

