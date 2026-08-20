# G194 R5 implementation note

Date: 2026-08-20

The first local read-only package preflight completed the full 267-history write-free independent
verifier, then failed because `verify_package.py` also tried to rerun the old forward-AD equivalence
reference.  That reference necessarily enters the Torch path R5 was designed to remove.

R5 preregistered the forward-versus-reverse equivalence census in the ordinary writable banking
environment, followed by a genuinely read-only package replay.  The package driver was therefore
corrected to:

- rerun and identity-check the 384-comparison equivalence census during writable banking;
- seal its result and digest;
- rerun the write-free 267-history verifier and artifact-drift checker under read-only review;
- validate, but not rerun, the sealed forward-reference equivalence artifact there;
- report machine-readably whether the equivalence census was replayed in that invocation.

No formula, profile, seed, tolerance, scientific artifact, or outcome changed.
