# G264 packaging-repair-only external follow-up request

Verify only the sealed-replay packaging repair preregistered in
`PACKAGING_REPAIR_PREREGISTRATION.md` and the unchanged bounded G264 landing.

Required checks:

1. Copy the sealed `replay_root/` to a writable ephemeral directory.
2. From its G264 package, rerun every command in `REGISTERED_REPLAY_COMMANDS.md`.
3. Confirm `verify_package.py` resolves exactly seven frozen sources using only `replay_root/`, with
   no repository, Git, network, or protected-package access.
4. Confirm the missing-manifest, altered-source, and missing-source attacks all fail closed.
5. Confirm the previously accepted R1--R3 repairs and the scientific landing are unchanged.

Return `ACCEPT_PACKAGING_REPAIR` or `REJECT_PACKAGING_REPAIR`. Do not edit evidence files, change
the scientific question, or continue the research.

