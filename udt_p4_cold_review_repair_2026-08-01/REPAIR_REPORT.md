# P4 cold-review repair report

Date: 2026-08-01

Status: `PRIMARY-PASS-PENDING-SAME-SECOND-VERIFIER`

Base: `c9c8b3848a7ff85b7941e803bf87c0ff48b9f98c`

## Outcome

Both defects named by the cold review have been repaired without reopening its science:

1. P4-19 no longer identifies the order-four K4 chart group with the real points of U(1).
   It now states exactly that the screen-character image `{+1,-1}`, not K4 itself, is the
   real two-torsion of the gauge-spent screen U(1).
2. All 13 dependencies discovered after the review outcome are now in a forward immutable
   freeze: 7 `LOAD_BEARING` and 6 `SUPPORTING`. The record explicitly says
   `DISCOVERED_POST_OUTCOME_NOT_PREREGISTERED`; it does not rewrite the original 311-path
   preregistration.

The P4 scientific grade is unchanged: premise-scoped formal response/census evidence;
32 `RETAINED`, 148 `NARROWED`, 1 `CONTRADICTED`, and 1 `OPEN`. The fixed-realized on-shell
embedding question remains open. No response law, field, carrier, source, action, mass,
coupling, solution, or physical branch is adopted.

## Exact repair evidence

- Corrected summary SHA-256:
  `85f5b9e7ce6619ba0b286c71291a3eaee61779fcdb81980c0241d0e24a3b2bb8`.
- Dependency freeze SHA-256:
  `e74b025264d7f1d4bea3dbb383280bcaba76ea113d83114e507e498318f354ac`.
- Dependency manifest SHA-256:
  `58cf2290cf5e4add8597592a17bd7d188c0b4666c694f2a2ee83bac9fccdf6bb`.
- Original review overlay SHA-256 remains:
  `217b3146488b82d0135fa7bd5d4d7cf45063ac4a7d2f7e44796352b2ece55f90`.
- Original cold-review package tree remains:
  `d1254e1e018d55ead4b57696629163c3d0006db5`.
- Original 311-source inventory/manifest hashes remain
  `a7032b94d91218e64ebfb40d0d31375cdfd75cc297aafabcf33d6617f12a199e` and
  `f150650c940e2d942a455234726ad3e3ce72b20bd175573a65ca0aeea34e8d85`.

The primary repair verifier passes 12/12, including exercised catches for the old headline,
a missing dependency, a changed dependency hash, a false retroactive-preregistration promotion,
and a changed review tree. The 13-path checksum manifest validates.

Repository controls also pass:

- scientific premise guards: 18 premise guards, 9 startup controls, 754 candidate dispositions;
- tests: 70 passed, 1 expected xfail;
- no path outside `P4_ARC_SUMMARY_2026-07-31.md` and this new repair package changed;
- no P4 producer/evidence package, `LIVE.md`, `CANON.md`, current registry, GPU output, or
  repository organization changed.

## Four gates

1. Preregistered: **YES**, commit `9089c0f`, before either repair.
2. Full or bounded scope: **YES**, exactly one headline phrase plus all 13 discovered dependencies.
3. Independently verified: **PENDING** the same second cold verifier required by the review.
4. Every repair premise audited: **YES** at the primary-repair grade.

Maximum conclusion: the two cold-review presentation/provenance defects are repaired at the
primary grade. T4, stability-hypothesis exploration, adoption, new physics, canonization, and GPU
work remain unauthorized until the same second verifier closes this repair.
