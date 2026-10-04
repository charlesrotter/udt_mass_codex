# CPR1 final integration repair: explicit orientation

The math reviewer caught a lost hypothesis in the condensed central text.
INITIAL_CANDIDATE.md fixes Omega>0 as an orientation convention. The first
central integration stated only Omega²>0 while using beta=Omega*a/sqrt(f(a))
in a sign-dependent bound. If Omega were negative, that bound would require
|Omega| instead. The central text now explicitly carries Omega>0, matching
its unchanged source. No physical orientation or new premise is privileged.

The first freeze SHA256485911723d9eb2b19842e4df0e3117a7556ff0208c791ae5ba42c6aaab84c494
and its central text, insertion and graph are preserved in integration_repair/.
This is a hypothesis-restoration repair, not a changed equation or tightened
physical claim. The typed review graph pins this record. Both final reviewers
re-read the actual repaired text and exact replacement map before attestation.
No numerical rerun is needed: code used the positive square root throughout;
initial candidate, numerical outcomes and source meanings are unchanged.
