# Codex instruction-chain rehearsal — 2026-09-05

## Scope and runtime

- Runtime: OpenAI Codex CLI `0.144.5`, model `gpt-5.6-sol`.
- Context: ephemeral, zero-context deployment probe with user configuration ignored.
- Sandbox: read-only; approval mode reported by the runtime as `never`.
- Web search: disabled.
- Repository writes: none.
- Claude Code: not invoked.
- Scientific packages and protected/untracked work: not inspected.

## Exact prompt

> Act as a zero-context deployment-instruction probe. Do not edit files, use network tools, run
> scientific work, or inspect protected/untracked work. Using the repository instructions
> automatically applicable here and only bounded read-only local inspection, report: (1) the exact
> primary method authority; (2) the shared on-disk instruction files it requires you to read and
> their role despite historical names; (3) whether Claude hooks are active, tested, or applicable
> in this deployment; and (4) the first and last items of the mandatory bounded startup read
> sequence. Do not execute fetch or pull in this deliberately read-only probe. Give exact evidence
> paths and identify anything not loaded.

## Exact final response

> 1. Primary method authority: `AGENTS.md`. It explicitly declares itself the primary method
> authority at line 6.
>
> 2. Required shared on-disk instructions:
>
>    - `CLAUDE.md`, specifically `How we work`, `DRIVER TRIGGERS`, and `Repo discipline`. Despite
>      its historical filename, it is shared Codex/ChatGPT method instruction—not evidence that
>      Claude is active and not scientific status.
>    - Task-triggered `.claude/skills/*/SKILL.md` protocols. Despite the directory name, these are
>      shared instructions in the Codex/ChatGPT startup chain. No skill protocol was triggered or
>      loaded for this deployment probe.
>
> 3. Claude hooks: inactive in this deployment. `AGENTS.md` says Codex/ChatGPT is active, Codex does
> not load `.claude/settings.json` or its hook, and live Claude-hook testing is not applicable or a
> Codex completion gate. `CLAUDE.md` further says testing is not marked passed. The retained
> configuration exists at `.claude/settings.json`, but I did not execute or test it.
>
> 4. Mandatory bounded startup sequence:
>
>    - First item: `LIVE.md`, only its `STARTUP_CURRENT` block; it overrides other status
>      descriptions.
>    - Last item, number 7: stop the startup read and give the orientation report. The final files
>      read immediately before that stop are `INDEX.md` and `MEMORY.md`, as compact pointers only.
>
> Inspection state: branch `grok`, HEAD `286ae71348242fb66e918a8c49fa47a081a45f47`, with existing
> tracked and untracked dirt. I did not fetch, pull, switch branches, or claim remote freshness.
>
> Not loaded or executed: `LIVE.md`, `HANDOFF.md`, `CURRENT_RESEARCH_PROGRAM.md`,
> `CURRENT_SCIENTIFIC_PREMISES.md`, its TSV registry, the premise verifier, `INDEX.md`, `MEMORY.md`,
> skill contents, the hook program, scientific packages, and all protected/untracked work.

Clickable file links emitted by the runtime were normalized to repository-relative code spans in
this record; wording is otherwise unchanged.

## Adjudication

`PASS_FOR_CURRENT_CODEX_INSTRUCTION_CHAIN_SCOPE`

The probe correctly identified `AGENTS.md` as primary, the historically named shared instructions
as explicit downstream reads, and Claude hooks as inactive/not applicable rather than passed. It
also reported the bounded startup endpoints and disclosed every intentionally omitted startup read.
This verifies instruction discovery and interpretation in the actual Codex deployment; it does not
claim that every future model response will obey every instruction.
