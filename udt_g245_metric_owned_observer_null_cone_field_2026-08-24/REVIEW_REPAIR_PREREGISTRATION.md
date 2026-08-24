# G245 external-review repair preregistration

Date: 2026-08-24

The fresh sealed GPT-5.4 review returned
`G245_REPAIRABLE_EVIDENCE_OR_TYPING_DEFECT`. It found no scientific objection or overclaim and
requested only two replay-packaging clarifications.

Before applying those repairs, freeze the following repair-only scope:

1. **R1 — self-contained premise replay.** Add the exact repository premise verifier to
   `SOURCE_MANIFEST.tsv` and therefore to the next sealed intake. Update the package verifier's
   expected source count from five to six. Do not change any scientific result or classification.
2. **R2 — distinguish repository smoke testing.** Keep `python3 -m pytest -q` in `COMMANDS.md`, but
   label it as an optional repository-only smoke test that is not part of the sealed evidentiary
   replay. Do not change any scientific result or classification.
3. Preserve the original review verbatim and add a concise review summary that distinguishes the
   packaging defect from the accepted mathematical adjudication.
4. Rebuild a fresh sealed intake and request only a repair-verification follow-up. The follow-up may
   not continue the research or revisit observational outcomes.

Repair success requires:

- the exact premise verifier to be present in the sealed scope and hash correctly;
- all five registered commands before the optional pytest line to execute in the sealed intake;
- all saved G245 outputs and the bounded scientific landing to remain byte-identical;
- the follow-up reviewer to accept R1 and R2 without introducing a new scientific claim.

Maximum post-repair grade:

```text
G245_ACCEPTED_WITH_STATED_BOUNDS
```
