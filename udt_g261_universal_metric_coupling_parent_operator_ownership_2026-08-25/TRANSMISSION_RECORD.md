# G261 external-review transmission record

Date: 2026-08-25

## Authorized sealed intake

- path: `/tmp/udt_g261_review_vxh45vmq`
- total files: 30
- manifest entries: 29
- `REVIEW_SCOPE.json` SHA-256:
  `ce062b2f0a0f04ad4f486132b2e97f71275954b5ffb146b0ec3700e1e00aaa70`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `fc5c23ea3cd6b453d15809e2019396a3ec2309c2d652a5e54f566245c11f68b2`

The hashes were rechecked unchanged after review.

## Isolation

The external Codex `gpt-5.4` reviewer received only the sealed intake mounted read-only, a writable
ephemeral runtime/copy, and read-only authentication-file use solely to launch it. The repository,
observational outcomes, protected packages, and internet search were not exposed. The reviewer was
instructed not to edit evidence or continue the research.

Two launcher attempts failed before model execution because obsolete command-line flags were used.
The successful isolated launch used the current standalone Codex binary. This mechanical retry did
not change the intake.

## Mechanical verification

- all 29 manifest hashes and byte counts: pass;
- registered replay in writable ephemeral copy: pass;
- regenerated outputs versus sealed packaged outputs: byte-identical;
- reviewer disposition: `ACCEPT_WITH_REPAIRS`.

The raw substantive return is preserved in `EXTERNAL_REVIEW_GPT54.md`. Repairs R1--R4 were frozen
before implementation in `REPAIR_PREREGISTRATION.md`; repair-only external follow-up remains
required.

## Repair-only follow-up

- sealed intake: `/tmp/udt_g261_review_0383z1d6`
- total files: 34
- manifest entries: 33
- `REVIEW_SCOPE.json` SHA-256:
  `e924e63e892597682746f8052928b4c65abeddf0e3998a9bde520066681b0b57`
- `REVIEW_MANIFEST.tsv` SHA-256:
  `ee2bec4a8c7c97593d67d1f862763ee95b468307723b13aa220314e6ee849c0f`

The first follow-up launcher stopped before model execution because the intake is intentionally not
a Git repository. The second and third stopped before substantive review because the filesystem
sandbox lacked the host resolver target. The successful launch added only the resolver files and
shared network access for the model API; the intake remained read-only and the repository,
observational outcomes, and protected packages remained absent.

The reviewer verified all 33 manifest rows, ran only the four registered commands in a writable
ephemeral copy, and found all five regenerated durable outputs byte-identical to the sealed
versions. Disposition: `ACCEPT_REPAIR`; exact remaining R1--R4 defects: none. The bounded scientific
landing is unchanged.
