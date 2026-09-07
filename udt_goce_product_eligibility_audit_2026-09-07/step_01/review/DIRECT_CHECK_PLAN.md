# Direct-review check freeze

Candidate pinned before this check:
`dc9614726e856f39bfffcb4fa3a314336b178603afdc8eb9cfe98d09e15906ac`.

Question: do TN3397 equations 6–10 and Algorithm 16 use incompatible meanings
for the same arm-length symbols, and is the final trace identity correctly
bounded to that written algorithm?

Scope: exact symbolic 3-by-3 symmetric gradient matrix and antisymmetric
rotation matrix; positive symbolic half-separations. Reconstruct acceleration
differences from the note's matrix equation, then compute both reconstruction
conventions. This differs from the author's scalar Fraction loop. Rotation and
off-diagonal terms are included to challenge an accidental zero-rotation-only
pass. An arbitrary rational witness is a diagnostic, never a flight input.

Expected alternatives: symbolic identities hold under the stated conventions;
a mismatch is exposed; or implementation/resource failure leaves the check
unresolved. No physical calibration, observations, nuisance model or accepted
source is changed. Maximum conclusion concerns the displayed document only.

Use pre-read existing run_capture.py, serial children, 512 MiB, 60 s CPU/wall.
Preserve control and failed mutant outputs. Also rerun the author's exact
control and changed-factor guard as same-code regression, not independence.
No tests of source calibration, pipeline execution or empirical errors.
