# Cognitive corral: Codex deployment and retained compatibility

`AGENTS.md` is the primary method authority. This document describes the reminder implementation;
it does not supply scientific premises, decide merit, or enlarge permissions.

Codex/ChatGPT is the active development deployment. Its effective chain is `AGENTS.md`, followed by
the exact `CLAUDE.md` sections and task-triggered `.claude/skills/` reads required there. Those
shared files retain historical names. Claude Code hooks are not active in this deployment; their
configuration is preserved as inactive compatibility infrastructure and live testing is
`NOT_APPLICABLE`, not passed.

## What the implementation can and cannot do

The instruction and compatibility layers are distinct:

1. `AGENTS.md`: primary method and permissions boundary.
2. `CLAUDE.md`: shared expanded method instructions with a historical filename.
3. `.claude/skills/*/SKILL.md`: shared procedures read only when triggered.
4. `.claude/hooks/corral_trigger.py`: inactive Claude-compatibility reminders in the Codex deployment.
5. repository tests: mechanical checks within their declared coverage.

A hook message, when that compatibility runtime is used, proves only that the named event returned
context. It does not prove all instructions loaded, model obedience, permission enforcement, or
science. Codex does not use the Claude hook as its instruction-chain proof.

## Current method reminders

- **Approach:** compare the least-imposed exact route and a controlled approximation. The latter is
  allowed with parameter, domain, error support, and propagated limits.
- **Mismatch:** run a frozen finite solver diagnostic, then report implementation defect, bounded
  incompatibility, or remaining numerical ambiguity.
- **Scope:** respect quantifiers. Targeted witnesses and counterexamples are legitimate; hidden
  answer-fitting and unjustified generalization are not.
- **Promotion:** separate exploratory checkpoint, candidate verification, review, owner adoption,
  and canon.
- **Choices:** tag physical premises and solver controls accurately.
- **Native/imported:** known mathematics is an allowed method; a known physical equation cannot be
  relabeled native merely because it helps.

## Inactive Claude compatibility configuration

Project settings are in `.claude/settings.json`. The dispatcher reads a JSON object from stdin and
returns documented `hookSpecificOutput.additionalContext`; it never executes a scientific command
or rewrites tool input. These files are retained and unit-tested for compatibility, but they are not
loaded by the active Codex deployment. Nonblocking reminders are not permission gates.

The intended event coverage is:

| Event | Local purpose |
|---|---|
| `SessionStart` (`startup`, `resume`, `clear`, `compact`, and compatible `fork`) | Report the actual source and remind the model of the bounded startup authority. |
| `SubagentStart` | Supply the essential authority/scope/promotion boundary to a child context. |
| `PreToolUse` (`Task`, `Agent`, `Bash`) | Add an advisory prompt at agent launch, recognized solver launch, or Git commit. |

Unknown events and valid unmatched tool calls are silent successes. Malformed JSON, non-object JSON,
and structurally invalid matched events return a visible hook-input diagnostic and never a healthy
banner. Null and missing optional fields are handled without traceback.

Command recognition is deliberately conservative. The parser tokenizes ordinary shell syntax and
recognizes executable tokens or configured script basenames. It avoids matching harmless quoted
examples such as `echo "git commit"`. It is not a universal shell parser or a security boundary.
Entrypoints and budgets come from declared task/work-order metadata when supplied. The repository
default metadata authorizes no solver. A narrow executable-name fallback warns on directly invoked
`solve`, `derive`, `scan`, `relax`, or `evolve` scripts when no entrypoint was declared; it does not
inspect arbitrary arguments and is advisory rather than complete coverage.

## Runtime facts and schema basis

- Active development runtime on 2026-09-05: Codex/ChatGPT.
- Locally installed but inactive Claude Code compatibility runtime: `2.1.201`.
- Official hooks reference checked on 2026-09-05:
  `https://code.claude.com/docs/en/hooks`.
- Official project-memory and subagent references checked on 2026-09-05:
  `https://code.claude.com/docs/en/memory` and
  `https://code.claude.com/docs/en/sub-agents`.

The official schema places nonblocking context under
`hookSpecificOutput.additionalContext` with the matching `hookEventName`. `SessionStart` is context
only and supports startup/resume/clear/compact/fork. Project hooks run in subagents according to
current documentation, but child receipt remains a deployment behavior to exercise rather than
assume on the installed runtime.

Configuration-schema review and direct dispatcher tests establish portable compatibility behavior.
No live Claude session is required for this Codex deployment, and none is claimed. If Claude becomes
active again, its deployed hook loading would need a new runtime test before being called tested.

## Testing contract

`tests/test_corral_trigger.py` covers:

- startup/resume/clear/compact/fork source handling;
- subagent context;
- Task/Agent/Bash matches and ordinary command variants;
- harmless quoted examples and unmatched events;
- malformed, non-object, null, missing, and unknown input;
- path/config handling and no stale pass-count claim.

`tests/test_guardrail_policy.py` statically checks that permission and protection language is
present and internally compatible. Actual model behavior requires the separately frozen blinded
evaluation cases; passing either finite check is evidence only for that scope, not a guarantee of
future conduct.

## Enforced versus advisory

| Control | Classification |
|---|---|
| Filesystem/network/user approval boundary | Runtime-enforced when the active runtime reports it. |
| Scientific-premise/startup verifier | Static repository check in its declared scope. |
| Import scanner | Conservative static dependency report; cannot certify native physics. |
| Corral hook | Advisory context only. |
| Adversarial review | Evidence about a specified candidate and exposure, not permission enforcement. |

No hook may weaken filesystem, network, credential, protected-path, scientific-premise, or canon
boundaries. No copied test count or historical failure exemption is a health signal.
