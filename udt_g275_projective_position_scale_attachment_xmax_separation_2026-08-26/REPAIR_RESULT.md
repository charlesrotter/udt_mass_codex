# G275 repair result

Date: 2026-08-26

Preregistration: commit `18f84136`

## Landing

`EXTERNALLY_REVIEWED__R4_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`

The external reviewers retained the exact G275 theorem. R1--R4 change certification only.

## R1 — explicit nonrecursive manifest and containment

`REVIEW_SCOPE.json` now records both the total physical file count and the manifest-entry count.
It states explicitly that `REVIEW_MANIFEST.tsv` lists every physical file except itself because a
cryptographic self-hash would be recursive. The sealed package verifier reconstructs the complete
physical path set, proves that the listed set is exactly the physical set minus the manifest,
checks containment, and checks every listed byte count and SHA-256.

Fresh ephemeral mutations adding an unlisted file or changing a listed payload are rejected.

## R2 — sealed verifier fails closed

Inside a sealed review root, frozen sources resolve only from the intake's exact `sources/` copies.
A missing or mismatched source fails immediately. The historical Git fallback remains available
only in repository mode so the preregistered source snapshot remains replayable after live startup
documents change.

An ephemeral test changes a sealed source while lawfully refreshing only its outer review-manifest
entry. The inner source hash fails, and a fake `git` marker proves no Git fallback was invoked.

## R3 — executable mutation/scope ledger

The prior pre-baked predicates were replaced with actual operators and hostile alternatives for:

1. homothety leakage into projective state;
2. screen deletion;
3. vector-only composition despite hidden spatial carry;
4. per-anchor scale proliferation;
5. automatic `X_max=ell` on a finite populated domain;
6. treating an empty population as a zero supremum;
7. attaching a pure length from `c_E` alone;
8. recovering scale from a zero-weight datum.

The independent verifier now exercises an actual nonempty-domain supremum function: an empty domain
raises, while a populated zero-state domain has supremum zero. The exact original independent
assertion count remains 340,006.

## Scientific non-change

The exact bounded landing, 26 production checks, 20,000-case independent census, active-screen and
frame-carry coverage, absence of observational inputs, and all stated open boundaries are unchanged.

## R4 — sealed repair-harness replay

The first repair-only follow-up found that `verify_review_repairs.py` could not launch from inside
the sealed intake because the builder looked only at the intake root or Git. R4 was preregistered at
`a16436e3`. The builder now resolves exact frozen sources from `package/sources/` first and fails
closed in sealed mode. The repair verifier recognizes an existing sealed root, treats it as the
immutable source for ephemeral copies, exercises a sealed builder replay, and—when launched from
the repository—launches its own registered `--no-write` command from the fresh sealed intake. A
fake-Git tripwire proves neither sealed route invokes Git. The scientific landing is unchanged.

The final repair-only `gpt-5.4` follow-up independently reran the sealed verifier and a bounded
repository-mode simulation made only from intake files. Both returned zero, every hostile tamper
gate passed, and the fake-Git marker remained absent. Its verdict was
`R4_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`; no blocking defect remains within R4 scope.
