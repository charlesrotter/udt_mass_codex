#!/usr/bin/env python3
"""
Cognitive-corral PreToolUse hook dispatcher (Part B of COGNITIVE_CORRAL_TRIGGERS_SETUP.md).

Fires from the HARNESS at structural tool-call moments -- agent launch, a solver run, a git commit --
so the corral triggers fire even when the driver did NOT recognize it was at a fork (it supplies,
mechanically, the external signal Charles's challenge currently supplies).

NON-BLOCKING: injects a PAUSE + HONESTY/PROVENANCE reminder; it never vetoes the action and it NEVER
judges MERIT (is the answer the right shape / a lump / the expected mass). A hook injects a required
procedure; it does not parse, score, or gate the driver's answer (CLAUDE.md governing limit).

Confirmed against Claude Code v2.1.173 (claude-code-guide, 2026-06-27): a PreToolUse hook injects
non-blocking context by printing {"hookSpecificOutput": {"hookEventName": "PreToolUse",
"additionalContext": "..."}} to stdout and exiting 0.  STDIN carries tool_name and tool_input.command.
Cross-platform: pure python, no bash-isms (runs on the Linux workstation and the Windows box).
"""
import json
import sys

# Solver entrypoints whose appearance in a Bash command means "a solve is about to run".
SOLVER_ENTRYPOINTS = (
    "continuation_solve", "newton_solve_p1", "migration_convergence_guard", "check_winding",
    "seed_round_native", "branchGP", "x_continuation", "jacobian_p1", "residual_vector_p1",
)


def _inject(text, event="PreToolUse"):
    out = {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}
    if event == "SessionStart":
        out["continue"] = True
    json.dump(out, sys.stdout)
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)                       # never block on a parse error -- silent pass

    # SessionStart: print a banner whose PRESENCE proves the hooks loaded (Part B is live), and
    # whose text prompts the startup self-check (Part A auto-load recite + the gate).  If this banner
    # is ABSENT at the top of a session, the corral hooks did NOT load -- the loud failure signal.
    if data.get("hook_event_name", "") == "SessionStart":
        _inject(
            "✓ CORRAL GUARDRAILS ACTIVE (DRIVER-TRIGGER hooks loaded). STARTUP SELF-CHECK: "
            "(1) read LIVE.md FIRST; (2) confirm the `## DRIVER TRIGGERS` section AUTO-LOADED -- recite "
            "the 6 triggers / the allowed-lane clause from context (Part-A check); (3) run "
            "WORK IS ON THE `grok` BRANCH (git checkout grok if not; LIVE.md/HANDOFF/MEMORY/INDEX on grok = the frontier); then "
            "`python3 -m pytest tests/` (grok: ~69 passed / 1 xfailed / 1 FAILED; the 1 fail = a pre-existing "
            "hygiene-header doc gap on some simple_metric_* docs, NOT a code failure -- a higher pass count is fine). If this banner is the ONLY "
            "corral signal you see (triggers not in context), rely on the hooks + note Part-A as failing.",
            event="SessionStart")

    tool = data.get("tool_name", "") or ""
    cmd = ((data.get("tool_input") or {}).get("command") or "")

    if tool in ("Task", "Agent"):
        _inject(
            "DRIVER TRIGGER (agent launch) -- OBSERVING or TARGETING? Check this agent's question vs the "
            "SM-template list (lump / mass / particle / spectrum): if it targets a desired answer, STOP and "
            "reframe to 'what is there'. State the REGIME the agent solves and the FREE choices it holds "
            "fixed (static / diagonal / branch G-or-P / grid / frozen rows). [CLAUDE.md ## DRIVER TRIGGERS #2,#3]"
        )

    if tool == "Bash":
        if "git commit" in cmd:
            _inject(
                "DRIVER TRIGGER (banking a result) -- verifier-before-record: confirm ALL FOUR before you "
                "commit -- pre-registered? full-space (or bounded slice justified)? blind-verified on the "
                "LOAD-BEARING premise? every forced premise audited? If any is missing, this is a "
                "PROVISIONAL / a LEAD, not a result -- say so in the message; do NOT write cured / proven / "
                "confirmed / dead / no-go without the four. [CLAUDE.md ## DRIVER TRIGGERS #4]"
            )
        if any(k in cmd for k in SOLVER_ENTRYPOINTS):
            _inject(
                "DRIVER TRIGGER (solver run) -- BOUND the grid (Nr<=16/24), SINGLE process, NO nohup, no "
                "`| grep` (block-buffers -> no live progress; write straight to file). Chose-or-derived: tag "
                "every FREE PHYSICS constant this solve rides (X, xi, kap, branch, kap8). Conditioning params "
                "(grid, tol, continuation step, preconditioner) are CATEGORY-A -- they need convergence/"
                "soundness, NOT metric-derivation; they do not trip chose-or-derived. [CLAUDE.md ## DRIVER "
                "TRIGGERS #5 + ANTI-HANG]"
            )

    sys.exit(0)                           # no match -> silent


if __name__ == "__main__":
    main()
