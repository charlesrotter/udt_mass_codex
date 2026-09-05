# G350 preregistration execution note

Date: 2026-09-05

The preregistration and frozen executable sources were committed and pushed at `2b050a38` before
the first scientific execution.

The first production execution passed `120010/120010`. The first implementation-distinct exact-log
execution passed `35295/35295`. The first hostile execution caught `25/25` registered mutations.
No formula, alternative, tolerance, witness, source scope, or maximum conclusion was changed after
execution. No repair or retuning was required.

The first aggregate package replay passed `21/23`. Its two failures were documentary guards only:
the observer-weight check required a phrase not used verbatim in the lay report, and the registered-
command check counted the explanatory `UDT_NO_WRITE=1` sentence as a fifth command. The verifier was
repaired to recognize the unchanged lay statement and count command lines rather than raw token
occurrences. No scientific source, result, tolerance, or conclusion changed.
