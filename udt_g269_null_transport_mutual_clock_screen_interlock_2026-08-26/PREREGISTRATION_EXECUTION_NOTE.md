# G269 preregistration execution note

Date: 2026-08-26
Preregistration commit: `c79f29e6`

The first production invocation stopped before writing `DERIVATION_RESULT.json` on two control-
expression transcription errors:

1. the reversal-depth zero test used `-log(1/r)+log(r)` instead of the intended
   `-log(1/r)-log(r)`;
2. the displayed off-planar witness value at `r=2,w=1` was transcribed as `2/7`; direct substitution
   into the preregistered formula `M=2r/(1+r^2+r^2w^2)` gives `4/9`.

Both corrections are arithmetic/sign repairs inside frozen tests. They change no domain,
alternative, premise, falsifier, or maximum conclusion. No result artifact existed before the
repair.
