# Fresh-context subject invocations

All four subjects were new Codex CLI processes. They used the existing ChatGPT
authentication route only to contact Codex, ordinary user configuration, no
resume or fork, `--ephemeral`, approval policy `never`, and disabled web search.
The controller captured each JSONL event stream through a PTY and supplied the
corresponding `R*_PROMPT.txt` as standard input. No authentication value is
recorded here or in the prompts.

The first R1 launch incorrectly placed `-a never` after `exec`; the CLI rejected
it before model launch. Its exact error is retained in `R1_LAUNCH_ERROR.txt`.
The corrected subject argument vectors were:

```text
/home/udt-admin/.local/bin/codex -a never exec --ephemeral -m gpt-5.6-sol -c web_search="disabled" -s read-only -C /tmp/udt_cold_start_r1_UnGMhL/repo --color never --json -o /home/udt-admin/udt_mass_codex/tests/cold_start_rehearsal_2026-09-06/R1_FINAL.md -

/home/udt-admin/.local/bin/codex -a never exec --ephemeral -m gpt-5.6-sol -c web_search="disabled" -s read-only -C /tmp/udt_cold_start_r2_yoRucn/repo --color never --json -o /home/udt-admin/udt_mass_codex/tests/cold_start_rehearsal_2026-09-06/R2_FINAL.md -

/home/udt-admin/.local/bin/codex -a never exec --ephemeral -m gpt-5.6-sol -c web_search="disabled" -s workspace-write -C /tmp/udt_cold_start_r3_wco5ez/repo --color never --json -o /home/udt-admin/udt_mass_codex/tests/cold_start_rehearsal_2026-09-06/R3_FINAL.md -

/home/udt-admin/.local/bin/codex -a never exec --ephemeral -m gpt-5.6-sol -c web_search="disabled" -s workspace-write -C /tmp/udt_cold_start_r4_ZjQOSR/repo --color never --json -o /home/udt-admin/udt_mass_codex/tests/cold_start_rehearsal_2026-09-06/R4_FINAL.md -
```

R1 and R2 were deliberately read-only. R3 and R4 used writable disposable
clones because the current premise verifier requires temporary scratch. The
base configuration supplied `model_reasoning_effort="xhigh"`, the default
OpenAI provider, and disabled Codex memory. The current installation was the
standalone Codex CLI 0.144.5 at all four launches.

The transcripts are `R1_TRANSCRIPT_RETRY.txt`, `R2_TRANSCRIPT.txt`,
`R3_TRANSCRIPT.txt`, and `R4_TRANSCRIPT.txt`. They include fresh thread IDs,
prompts, commands, results, and a single completed turn each.
