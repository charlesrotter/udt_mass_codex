# G307 repair preregistration

Date: 2026-08-31
Trigger: fresh external verdict `G307_REPAIRABLE_DEFECTS`

The external reviewer found no scientific defect and retained the exact bounded G307 landing. The
following repairs are frozen before implementation. They may improve portability and evidence
independence only; they may not change the question, member census, ownership boundary, metric, or
reciprocal kernel.

## R1 — sealed-layout source resolution

Repair `build_review_intake.py` so each frozen dependency resolves uniquely in either repository
layout or sealed-intake layout. Repository sources may appear at `ROOT/path`; sealed sources at
`ROOT/frozen_sources/path`; current premise files at `ROOT/name` or `ROOT/frozen_current/name`.
Missing and ambiguous layouts must be rejected. A writable copy of the repaired sealed intake must
run the builder successfully.

## R2 — independent reconstruction from `(p,v)`

Extend the implementation-independent verifier so it does not start only from the already chosen
`route +/- screen` operators. For every random regular `(p,v)` it must:

- construct the left and right imaginary-quaternion evaluation maps independently;
- verify each map is an isometry and hence injective;
- solve for the unique left and right coefficients from `(p,v)` by projection onto those maps;
- compare those independently solved coefficients with `v conjugate(p)` and
  `conjugate(p) v`;
- reconstruct both full operators and verify that they coincide with the independently built
  route/screen operators.

At least 30,000 independent nonvacuous checks must pass with maximum error below `2e-10` and no
production import.

## R3 — direct mathematical hostile mutations

Retain the semantic result-field guards, but add direct algebraic mutations that would corrupt the
load-bearing theorem. At minimum catch:

- wrong quaternion order in left reconstruction;
- wrong quaternion order in right reconstruction;
- a broken route-plane sign;
- same rather than opposite transverse screen turn;
- omission of the positive-radius `1/a` factor;
- point-only false uniqueness;
- route-only false chirality selection;
- orientation reversal without twist-sign reversal.

Each direct mutation must be exercised on a noncommuting exact witness and fail for the registered
reason. Merely mutating JSON is insufficient for these cases.

## R4 — command and premise-audit typing

Clarify that the four package evidence commands and repaired intake builder are sealed replays.
The whole-repository premise verifier and pytest are repository-only gates recorded by hash/result;
they are not promised as self-contained sealed commands. Include the frozen premise guide and
registry as before without claiming the complete repository verifier can run from the intake.

## Certification contract

- R1 passes from repository and freshly copied sealed layouts; missing/ambiguous sources rejected.
- R2 supplies at least 30,000 checks, exact member counts, and the existing tolerance.
- R3 catches all registered direct mathematical and semantic mutations.
- All original production outputs and the exact landing remain unchanged.
- `python3 -S verify_package.py`, the current premise verifier, and repository regression pass.
- Maximum grade before repair-only external follow-up:
  `INTERNALLY_REPAIRED_AFTER_EXTERNAL_SCIENTIFIC_SUPPORT__FOLLOWUP_PENDING`.

Any scientific change, member-count change, ownership promotion, or kernel/metric change fails the
repair and requires a new preregistered question.
