# G332 external-review repair preregistration

Date: 2026-09-03
Trigger: fresh external verdict
`ACCEPT_WITH_REPAIRS__G332_SCIENTIFIC_LANDING_RETAINED`

The fresh reviewer retained the exact bounded constraint-existence result and identified one sealed
replay path defect plus one tensor-typing clarification. The following repairs are frozen before
implementation. They may not change the supplied G331 metric family, the unit-Killing witness, the
Hamiltonian or momentum equations, either square-root branch, the arbitrary fixed finite connected
`Lambda`, or the bounded scientific landing.

## R1 — dependency-free sealed source resolution

Repair `verify_package.py` so each `SOURCE_MANIFEST.tsv` row resolves against the repository root
during repository replay and against the sealed `sources/` subtree during intake replay. Preserve
all source-count, existence, byte-count, and SHA-256 checks; never fall back from a missing sealed
source to a repository path.

Acceptance:

- all four registered commands pass in one fresh writable copy of the corrected sealed intake;
- all three generated JSON artifacts reproduce byte-for-byte;
- all 12 sealed sources retain their registered sizes and SHA-256 digests;
- no repository, network, host package, or unsealed dependency is used by the replay.

Falsification: any source check is skipped or weakened, any sealed path escapes its intake, or the
aggregate verifier still requires a path outside the corrected sealed copy.

## R2 — explicit tensor index convention

State in `EXACT_DERIVATION.md` that the momentum calculation uses the contravariant tensor
`P^ij = K^ij - tau gamma^ij`; the later unindexed formula is its covariant version after lowering
both indices. Retain `xi^i xi^j` in the former and `xi_flat tensor xi_flat` in the latter.

Acceptance: the derivation is type-consistent without changing any coefficient, sign, trace
inversion, eigenvalue, residual, or conclusion.

Falsification: the repair conflates vector and covector products, changes the witness, or promotes
the construction beyond bounded initial-data existence.

## Maximum retained conclusion

If R1 and R2 pass locally and a repair-only external reviewer accepts them, G332 may be graded only
as an externally accepted `DERIVED_CONDITIONAL` existence theorem on the complete supplied G331
positive-weight family. It remains neither a full `K` census nor an evolution, stability, occupancy,
matter/mass, scale, physical `X_max`, or canon result.
