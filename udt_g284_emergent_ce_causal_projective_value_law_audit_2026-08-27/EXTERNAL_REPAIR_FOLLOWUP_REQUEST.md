# G284 external repair-only follow-up request

Review mode: fresh read-only repair-only follow-up.

The first external review returned `ACCEPT-WITH-REPAIRS`, found no scientific defect, and retained
the bounded G284 landing unchanged. Verify only the preregistered repairs in
`REPAIR_PREREGISTRATION.md`:

1. R1 replaces the registered SymPy-dependent derivation with a standard-library exact replay that
   retains all three arbitrary smooth tidal functions and the same 20 exact claims. The former
   SymPy implementation is supplemental only.
2. R2 makes `verify_package.py` execute all four registered recomputations with `python -S` in an
   ephemeral copy containing the exact frozen sources, and reject an artifact-level broken replay.

Run the registered commands or bounded repair checks only in a writable ephemeral copy. Confirm or
reject each repair and state whether the accepted bounded scientific landing remains unchanged.
Do not reopen the scientific question, propose a new law, edit evidence, or continue the research.
