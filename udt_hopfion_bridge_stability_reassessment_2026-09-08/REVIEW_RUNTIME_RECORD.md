# Review runtime, not scientific evidence

The collaboration tool rejected the attempted new HB1 reviewer with 'agent
thread limit reached'; two older completed contexts were still retained.
No old context was reused or called fresh. The existing CLI0.153.4 was inspected;
its local configuration says gpt-6-astra/xhigh. No model/configuration changed.
OpenAI Docs skill was used to check the supported noninteractive mechanism:
https://learn.chatgpt.com/docs/non-interactive-mode (retrieved2026-09-08).

Exact initial command, from the repository root:

    timeout 2700 codex exec --ephemeral --sandbox workspace-write --json --output-last-message /home/udt-admin/udt_mass_codex/udt_hopfion_bridge_stability_reassessment_2026-09-08/step_01/review/CLI_LAST_MESSAGE.md 'Read and follow udt_hopfion_bridge_stability_reassessment_2026-09-08/REVIEW_RUNTIME_DISPATCH.md. Fresh HB1 source-first adversarial review only. No resume or fork.'

First ordinary-sandbox invocation exited1 before a context started: read-only
filesystem blocked in-process app-server initialization. Scoped escalation of
the same command then started thread01a081ce-43c9-7292-ad15-c2bc13a36ba5,
terminal session38534. The REVIEWER retained workspace-write sandbox controls;
no dangerous bypass, resume or fork. Maximum2700s invocation inside total4h.
Substantive review may not exceed its45min dispatch. Configured identity is not
backend model attestation; different-model review is UNTESTED unless actual
evidence establishes it. No separate external review service or install used.

The parent polled JSON events while doing useful banking/source work. One poll
had95904 tokens of events and was truncated; therefore a complete raw CLI event
transcript is NOT preserved/claimed. The independent review artifacts and their
explicit source-first/late-exposure record own the auditable scientific review.
Selected event messages and thread-start/exit observations are not a complete
trace. Source-first requirements SHA256
b825527f4be0dfdf7b22b4d8792bb7b4e0aad785509bcedb26f9987c11788952
was emitted before author candidate exposure. Main read its detailed contents
only after freezing HB1. Main candidate hash is recorded in step_01/CANDIDATE_FREEZE.md.

Reviewer STARTUP_DEVIATION.json preserves its actual redundant audit exit1
'G351 dependency-free no-write replay failed:' with no detail, combined rather
than separate streams, and no measured duration. This omission/failure is not
repaired or relabeled. Its failed read-only fetch/pull and no-op checkout are
also recorded. Successful parent356/358 audits are separate receipts. Later
review dispatches must put reuse/no-shared-Git instructions directly in the
initial prompt before task-file reading, to avoid the redundant root startup.

HB1 reviewer invocation finished with exit0 and a saved VERIFIED-WITH-CAVEATS
final message. For HB2 a NEW ephemeral invocation was started16:38UTC with
the same existing configuration and workspace-write controls, after scoped
initialization escalation. Its direct initial prompt explicitly forbids
duplicate shared Git/startup audit before reading step_02/REVIEW_DISPATCH.md.
HB2 thread01a081e2-f777-7673-b61b-9aca409f2ccc, terminal session61501,
timeout2700s. HB1 had exited before HB2 launch; only one alternate reviewer
process active at a time. No resume/fork or model switch. Exact HB2 command
will be retained in its execution evidence; the scientific result is still open.
