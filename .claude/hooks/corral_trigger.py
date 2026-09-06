#!/usr/bin/env python3
"""Nonblocking UDT method reminders for supported Claude Code hook events.

This dispatcher never grants permission, blocks a tool, or certifies scientific compliance. It
reports malformed input visibly and injects context only for recognized events. Command matching is
advisory and intentionally narrower than a shell-security parser.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path
from typing import Any


SESSION_SOURCES = {"startup", "resume", "clear", "compact", "fork"}
AGENT_TOOLS = {"Task", "Agent"}
SHELL_SEPARATORS = {";", "&&", "||", "|", "&", "\n"}
WRAPPERS = {"env", "sudo", "command", "time", "nice", "nohup"}
INTERPRETERS = {"python", "python3", "pypy", "pypy3", "bash", "sh"}
FALLBACK_SOLVER_WORDS = re.compile(
    r"(?:^|[_-])(solve|solver|derive|scan|relax|evolve|residual)(?:[_-]|\.|$)"
)
DEFAULT_METADATA = ".claude/guardrail_work_order_metadata.json"


def _write(payload: dict[str, Any]) -> int:
    json.dump(payload, sys.stdout, sort_keys=True)
    return 0


def _context(event: str, text: str) -> int:
    return _write(
        {
            "hookSpecificOutput": {
                "hookEventName": event,
                "additionalContext": text,
            }
        }
    )


def _diagnostic(reason: str) -> int:
    return _write(
        {
            "systemMessage": (
                "UDT corral hook input was not processed; no guardrail-health claim is made: "
                + reason
            )
        }
    )


def _tokens(command: str) -> list[str]:
    if not isinstance(command, str):
        return []
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|\n")
        lexer.whitespace_split = True
        lexer.commenters = ""
        return list(lexer)
    except (TypeError, ValueError):
        return []


def _segments(command: str) -> list[list[str]]:
    result: list[list[str]] = []
    # Newlines delimit ordinary shell commands. This remains an advisory parser; it does not claim
    # to reproduce quoted multiline shell syntax.
    for line in command.splitlines() or [command]:
        current: list[str] = []
        for token in _tokens(line):
            if token in SHELL_SEPARATORS or set(token) <= {";", "&", "|"}:
                if current:
                    result.append(current)
                    current = []
                continue
            current.append(token)
        if current:
            result.append(current)
    return result


def _command_words(segment: list[str]) -> list[str]:
    words = list(segment)
    while words:
        first = Path(words[0]).name
        if "=" in words[0] and not words[0].startswith(("=", "-")):
            words.pop(0)
            continue
        if first in WRAPPERS:
            words.pop(0)
            while words and words[0].startswith("-"):
                option = words.pop(0)
                takes_value = (
                    (first == "env" and option in {"-u", "--unset", "-C", "--chdir"})
                    or (first == "sudo" and option in {"-u", "--user", "-g", "--group", "-h", "--host", "-p", "--prompt", "-C", "--chdir"})
                    or (first == "nice" and option in {"-n", "--adjustment"})
                )
                if takes_value and words:
                    words.pop(0)
            while first == "env" and words and "=" in words[0] and not words[0].startswith("="):
                words.pop(0)
            continue
        break
    return words


def _is_git_commit(command: str) -> bool:
    for segment in _segments(command):
        words = _command_words(segment)
        if not words or Path(words[0]).name != "git":
            continue
        args = words[1:]
        index = 0
        while index < len(args):
            token = args[index]
            if token in {"-C", "-c", "--config-env", "--git-dir", "--work-tree"}:
                index += 2
                continue
            if token.startswith(("--config-env=", "--git-dir=", "--work-tree=")):
                index += 1
                continue
            break
        if index < len(args) and args[index] == "commit":
            return True
    return False


def _metadata(data: dict[str, Any]) -> dict[str, Any]:
    supplied = data.get("guardrail_metadata")
    if "guardrail_metadata" in data:
        if not isinstance(supplied, dict):
            return {"metadata_error": "inline guardrail_metadata must be an object"}
        return _validated_metadata(supplied)
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
    metadata_path = os.environ.get("UDT_WORK_ORDER_METADATA", DEFAULT_METADATA)
    path = Path(metadata_path)
    if not path.is_absolute():
        path = project / path
    try:
        resolved = path.resolve()
        resolved.relative_to(project / ".claude")
        loaded = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return {"metadata_error": "declared work-order metadata unavailable or invalid"}
    if not isinstance(loaded, dict):
        return {"metadata_error": "metadata is not an object"}
    return _validated_metadata(loaded)


def _validated_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    names = metadata.get("solver_entrypoints", [])
    if not isinstance(names, list) or not all(
        isinstance(item, str) and item.strip() for item in names
    ):
        return {"metadata_error": "solver_entrypoints must be a list of nonempty strings"}
    for key in ("resource_budget", "stop_conditions"):
        if key in metadata and not isinstance(metadata[key], (str, int, float, list, dict)):
            return {"metadata_error": f"{key} has unsupported metadata type"}
    return metadata


def _invoked_target(segment: list[str]) -> str | None:
    """Return only the directly executed file/module token, never arbitrary arguments."""
    words = _command_words(segment)
    if not words:
        return None
    executable = Path(words[0]).name
    if executable not in INTERPRETERS:
        return executable
    args = words[1:]
    index = 0
    while index < len(args):
        token = args[index]
        if token == "-m" and index + 1 < len(args):
            return args[index + 1]
        if token in {"-c", "--command"}:
            return None
        if token in {"-W", "-X"} and index + 1 < len(args):
            index += 2
            continue
        if token.startswith("-"):
            index += 1
            continue
        return Path(token).name
    return None


def _solver_match(command: str, metadata: dict[str, Any]) -> tuple[str | None, bool]:
    names = metadata.get("solver_entrypoints", [])
    declared = {Path(item).name for item in names}
    for segment in _segments(command):
        target = _invoked_target(segment)
        if target is None:
            continue
        basename = Path(target).name
        if basename in declared or target in names:
            return basename, True
        if FALLBACK_SOLVER_WORDS.search(basename.lower()):
            return basename, False
    return None, False


def dispatch(data: Any) -> dict[str, Any] | None:
    """Return a structured hook response, or None for a valid unmatched event."""
    if not isinstance(data, dict):
        return {"diagnostic": "top-level JSON must be an object"}
    event = data.get("hook_event_name")
    if event is None:
        return {"diagnostic": "hook_event_name is missing"}
    if not isinstance(event, str):
        return {"diagnostic": "hook_event_name must be a string"}

    if event == "SessionStart":
        source = data.get("source", "unknown")
        if not isinstance(source, str):
            return {"diagnostic": "SessionStart source must be a string"}
        support = "recognized" if source in SESSION_SOURCES else "unrecognized"
        return {
            "event": event,
            "text": (
                f"UDT corral reminder loaded for SessionStart source={source!r} ({support}). "
                "This proves only that this hook event ran. AGENTS.md is the primary method "
                "authority; follow its bounded startup and report any unverified loading or checks."
            ),
        }

    if event == "SubagentStart":
        agent_type = data.get("agent_type", "unknown")
        return {
            "event": event,
            "text": (
                f"UDT subagent reminder loaded for agent_type={agent_type!r}. AGENTS.md is the "
                "primary method authority. Stay inside the dispatched scope; method instructions "
                "supply no physics; separate exploration, verification, and promotion; preserve "
                "protected paths and report review independence honestly."
            ),
        }

    if event != "PreToolUse":
        return None

    tool = data.get("tool_name")
    tool_input = data.get("tool_input", {})
    if not isinstance(tool, str):
        return {"diagnostic": "PreToolUse tool_name must be a string"}
    if tool_input is None:
        tool_input = {}
    if not isinstance(tool_input, dict):
        return {"diagnostic": "PreToolUse tool_input must be an object"}

    if tool in AGENT_TOOLS:
        return {
            "event": event,
            "text": (
                "UDT agent-launch reminder: state the authorized question, quantifier, regime, "
                "retained choices, exclusions, and maximum conclusion. Targeted bounded questions "
                "are allowed; hidden answer-fitting and silent physical premises are not."
            ),
        }

    if tool != "Bash":
        return None
    command = tool_input.get("command", "")
    if not isinstance(command, str):
        return {"diagnostic": "Bash tool_input.command must be a string"}

    metadata = _metadata(data)
    match, declared_match = _solver_match(command, metadata)
    reminders = []
    if metadata.get("metadata_error"):
        reminders.append(
            "UDT metadata diagnostic: " + str(metadata["metadata_error"]) + "."
        )
    if _is_git_commit(command):
        reminders.append(
            "UDT commit reminder: a commit preserves work but does not promote science. Record "
            "evidence type, scope, premises, review state, and authorized paths; use the "
            "evidence-appropriate freeze rather than a blanket preregistration claim."
        )
    if match:
        budget = metadata.get("resource_budget", "not supplied")
        stops = metadata.get("stop_conditions", "not supplied")
        match_type = "declared" if declared_match else "undeclared solver-like"
        reminders.append(
                f"UDT solver reminder for {match_type} entrypoint {match!r}: preserve admitted equations; "
                f"state physical choices and numerical controls; budget={budget!r}; "
                f"stop_conditions={stops!r}; keep one GPU process and certify against the original "
                "residual. An undeclared match requires an active work-order declaration before a "
                "scientific launch. This reminder is advisory, not permission enforcement."
        )
    if reminders:
        return {"event": event, "text": " ".join(reminders)}
    return None


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return _diagnostic(f"malformed JSON ({exc.__class__.__name__})")
    result = dispatch(data)
    if result is None:
        return 0
    if "diagnostic" in result:
        return _diagnostic(str(result["diagnostic"]))
    return _context(str(result["event"]), str(result["text"]))


if __name__ == "__main__":
    raise SystemExit(main())
