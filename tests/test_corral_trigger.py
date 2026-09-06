import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".claude/hooks/corral_trigger.py"
SETTINGS = ROOT / ".claude/settings.json"


def load_hook():
    spec = importlib.util.spec_from_file_location("corral_trigger", HOOK)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


HOOK_MODULE = load_hook()


def run_hook(raw: str):
    completed = subprocess.run(
        [sys.executable, str(HOOK)],
        input=raw,
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
    )
    return completed, json.loads(completed.stdout) if completed.stdout else None


def context(result):
    return result["hookSpecificOutput"]["additionalContext"]


def test_malformed_and_non_object_inputs_are_visible_nonblocking_diagnostics():
    for raw in ("{", "null", "[]", "1", "{}"):
        completed, result = run_hook(raw)
        assert completed.returncode == 0
        assert "systemMessage" in result
        assert "no guardrail-health claim" in result["systemMessage"]


def test_all_configured_session_sources_report_only_event_loading():
    for source in ("startup", "resume", "clear", "compact", "fork"):
        result = HOOK_MODULE.dispatch({"hook_event_name": "SessionStart", "source": source})
        message = result["text"]
        assert source in message
        assert "only that this hook event ran" in message
        assert "all guardrails active" not in message.lower()
        assert "passed" not in message.lower()


def test_subagent_context_carries_primary_authority_and_scope():
    result = HOOK_MODULE.dispatch(
        {"hook_event_name": "SubagentStart", "agent_type": "Explore"}
    )
    assert "AGENTS.md is the primary method authority" in result["text"]
    assert "dispatched scope" in result["text"]


def test_pretool_validation_and_unknown_events():
    assert "diagnostic" in HOOK_MODULE.dispatch(
        {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": 4}
    )
    assert "diagnostic" in HOOK_MODULE.dispatch(
        {"hook_event_name": "PreToolUse", "tool_name": 7, "tool_input": {}}
    )
    assert HOOK_MODULE.dispatch({"hook_event_name": "Unknown"}) is None


def test_git_commit_variants_match_but_quoted_examples_do_not():
    positives = (
        "git commit -m test",
        "/usr/bin/git commit -m test",
        "git -C /tmp/project commit -m test",
        "git -c user.name=test commit -m test",
        "env FLAG=1 git --work-tree=/tmp/project commit -m test",
        "env -u FLAG git commit -m test",
        "sudo -u nobody git commit -m test",
        "nice -n 5 git commit -m test",
        "echo x\ngit commit -m test",
    )
    for command in positives:
        result = HOOK_MODULE.dispatch(
            {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command}}
        )
        assert "commit reminder" in result["text"]
    for command in ('echo "git commit"', 'python3 -c "print(\'git commit\')"'):
        result = HOOK_MODULE.dispatch(
            {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command}}
        )
        assert result is None


def test_solver_fallback_is_direct_only_and_declared_metadata_reports_budget():
    base = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "python3 solve.py"},
    }
    message = HOOK_MODULE.dispatch(base)["text"]
    assert "undeclared solver-like" in message
    assert "requires an active work-order declaration" in message
    for command in ('echo "solve.py"', 'rg solve.py README.md', 'python3 -c "print(\'solve.py\')"'):
        probe = dict(base)
        probe["tool_input"] = {"command": command}
        assert HOOK_MODULE.dispatch(probe) is None
    base["tool_input"] = {"command": "python3 compute.py"}
    base["guardrail_metadata"] = {
        "solver_entrypoints": ["compute.py"],
        "resource_budget": "10 seconds",
        "stop_conditions": ["residual failure", "timeout"],
    }
    message = HOOK_MODULE.dispatch(base)["text"]
    assert "compute.py" in message
    assert "declared entrypoint" in message
    assert "10 seconds" in message
    assert "permission enforcement" in message


def test_commit_and_solver_reminders_are_both_retained():
    data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "python3 solve.py && git commit -m result"},
        "guardrail_metadata": {"solver_entrypoints": ["solve.py"]},
    }
    message = HOOK_MODULE.dispatch(data)["text"]
    assert "commit reminder" in message
    assert "solver reminder" in message


def test_metadata_errors_are_visible_alone_and_alongside_commit(monkeypatch, tmp_path):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(ROOT))
    monkeypatch.setenv("UDT_WORK_ORDER_METADATA", str(tmp_path / "outside.json"))
    base = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": "echo ok"}}
    assert "diagnostic" in HOOK_MODULE.dispatch(base)["text"]
    base["tool_input"] = {"command": "git commit -m test"}
    message = HOOK_MODULE.dispatch(base)["text"]
    assert "metadata diagnostic" in message.lower()
    assert "commit reminder" in message


def test_malformed_inline_metadata_is_not_silently_ignored():
    base = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "echo ok"},
        "guardrail_metadata": {"solver_entrypoints": "solve.py"},
    }
    assert "solver_entrypoints must be a list" in HOOK_MODULE.dispatch(base)["text"]


def test_default_metadata_loads_and_actual_solver_like_entrypoints_warn(monkeypatch):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(ROOT))
    monkeypatch.delenv("UDT_WORK_ORDER_METADATA", raising=False)
    for command in (
        "python3 p1_residual_general_einstein.py",
        "python3 udt_uncompressed_pair_kernel_reconstruction_2026-08-14/derive_uncompressed_pair_evaluator.py",
    ):
        result = HOOK_MODULE.dispatch(
            {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command}}
        )
        assert "solver reminder" in result["text"]
        assert "undeclared" in result["text"]


def test_settings_declares_supported_routes_and_exec_form():
    settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    hooks = settings["hooks"]
    assert hooks["SessionStart"][0]["matcher"] == "startup|resume|clear|compact|fork"
    assert hooks["SubagentStart"][0]["matcher"] == ".*"
    assert hooks["PreToolUse"][0]["matcher"] == "Task|Agent|Bash"
    for groups in hooks.values():
        for group in groups:
            for hook in group["hooks"]:
                assert hook["type"] == "command"
                assert hook["command"] == "python3"
                assert hook["args"] == ["${CLAUDE_PROJECT_DIR}/.claude/hooks/corral_trigger.py"]
