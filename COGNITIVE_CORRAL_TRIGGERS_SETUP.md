# Cognitive corral: current runtime implementation

`AGENTS.md` is the primary method authority. This document describes the reminder implementation;
it does not supply scientific premises, decide merit, or enlarge permissions.

## What the implementation can and cannot do

The active layers are distinct:

1. `AGENTS.md`: primary method and permissions boundary.
2. `CLAUDE.md`: compact Claude runtime adapter.
3. `.claude/skills/*/SKILL.md`: expanded procedures used only when triggered.
4. `.claude/hooks/corral_trigger.py`: nonblocking event reminders.
5. repository tests: mechanical checks within their declared coverage.

A hook message proves only that the named hook event ran and returned context. It does not prove all
instructions loaded, that the model obeyed them, that a permission is enforced, or that science is
valid. Claude hook behavior does not prove Codex hook integration; Codex follows `AGENTS.md` manually
unless its own runtime exposes and verifies an equivalent facility.

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

## Claude hook configuration

Project settings are in `.claude/settings.json`. The dispatcher reads a JSON object from stdin and
returns documented `hookSpecificOutput.additionalContext`; it never executes a scientific command
or rewrites tool input. Nonblocking reminders are not permission gates.

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

- Locally inspected Claude Code runtime on 2026-09-05: `2.1.201`.
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

Configuration-schema review and direct dispatcher tests establish portable behavior. A real CLI
session is required to claim deployed hook loading. If authentication or runtime access prevents
that test, record it as untested without blocking unrelated repository work.

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
