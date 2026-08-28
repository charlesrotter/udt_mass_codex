# G285 external repair-only follow-up request

Review mode: fresh read-only repair-only follow-up.

The first external review returned `ACCEPT_WITH_REPAIRS`, found no scientific defect, retained the
bounded G285 landing, and accepted every G280--G284 regrade. Verify only the preregistered repairs
in `REPAIR_PREREGISTRATION.md`:

1. R1 regrades the new G285 computations and counts as source-bounded type-schema adjudication and
   an implementation-distinct type-schema census. They no longer claim to independently recompute
   the already reviewed G280--G284 witness geometry.
2. R2 makes `verify_package.py` require those repaired labels, reject restoration of the overgraded
   package status, replay all four registered computations in an ephemeral copy, and retain the
   broken-replay mutation catch.

Run registered commands or bounded repair checks only in a writable ephemeral copy. Confirm or
reject each repair and state whether the accepted scientific landing remains unchanged. Do not
reopen the scientific question, propose a new law, edit evidence, or continue the research.
