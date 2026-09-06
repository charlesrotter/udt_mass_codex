import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def normalized(relative: str) -> str:
    return " ".join(read(relative).split()).lower()


def test_one_primary_method_authority_and_no_science_from_method():
    agents = normalized("AGENTS.md")
    adapters = (
        "CLAUDE.md",
        "CROSS_MODEL_VERIFY.md",
        "STRUCTURE_HYGIENE.md",
        "COGNITIVE_CORRAL_TRIGGERS_SETUP.md",
    )
    assert "primary working-method authority" in agents
    assert "method instructions" in agents and "do not supply scientific" in agents
    for relative in adapters:
        text = normalized(relative)
        assert "agents.md" in text
        assert "primary" in text
        assert "scientific premise" in text or "science" in text


def test_codex_is_active_and_claude_named_files_remain_shared_not_live_hooks():
    agents = normalized("AGENTS.md")
    claude = normalized("CLAUDE.md")
    setup = normalized("COGNITIVE_CORRAL_TRIGGERS_SETUP.md")
    metadata = json.loads(read(".claude/guardrail_work_order_metadata.json"))
    assert "codex/chatgpt is the active development deployment" in agents
    assert "shared instructions in the active codex/chatgpt startup chain" in agents
    assert "not evidence that claude code is the active deployment" in claude
    assert "inactive compatibility infrastructure" in agents
    assert "not applicable" in agents
    assert "not_applicable" in setup and "not passed" in setup
    assert "claude hooks are retained inactive compatibility" in metadata["runtime_scope"].lower()


def test_bounded_discovery_approximation_quantifier_and_solver_permissions():
    combined = " ".join(
        normalized(path)
        for path in (
            "AGENTS.md",
            "CLAUDE.md",
            ".claude/skills/no-shortcuts/SKILL.md",
            ".claude/skills/solution-space-not-imposition/SKILL.md",
            ".claude/skills/solver-first/SKILL.md",
        )
    )
    for required in (
        "bounded discovery",
        "controlled approximation",
        "first variation",
        "targeted bounded",
        "counterexample",
        "finite diagnostic",
        "stop",
    ):
        assert required in combined
    for obsolete in (
        "never use approximations",
        "do not linearize",
        "solve everything before",
        "any targeting is forbidden",
    ):
        assert obsolete not in combined


def test_numerical_validity_is_not_aesthetic_and_finite_search_is_scoped():
    agents = normalized("AGENTS.md")
    claude = normalized("CLAUDE.md")
    solution = normalized(".claude/skills/solution-space-not-imposition/SKILL.md")
    assert "numerical validity is not aesthetic" in claude
    assert "unfamiliar appearance" in agents
    assert "finite failed search" in claude
    assert "nonexistence" in claude
    assert "convergence" in solution


def test_evidence_specific_freeze_review_and_dependency_impact():
    agents = normalized("AGENTS.md")
    verifier = normalized(".claude/skills/verifier-before-record/SKILL.md")
    review = normalized("CROSS_MODEL_VERIFY.md")
    assert "evidence-appropriate freeze" in agents
    assert "mathematical discovery" in verifier
    assert "observations: freeze" in agents and "numerics: freeze" in agents
    assert "source-first" in review
    assert "defective step" in review and "strongest surviving" in review
    assert "positive and negative descendants" in agents


def test_counterfactual_conditional_review_and_stable_id_guards_are_explicit():
    agents = normalized("AGENTS.md")
    assert "counterfactual remains explicitly unadopted" in agents
    assert "excluded from accepted dependencies" in agents
    assert "unproved dependency" in agents
    assert "conditional candidate chain" in agents
    assert "packaging-only repair" in agents
    assert "reuse sound existing utilities" in agents
    assert "stable premise/result ids" in agents
    assert "source versions" in agents


def test_resource_limits_are_declared_not_stale_hardware_constants():
    active = " ".join(
        normalized(path)
        for path in (
            "AGENTS.md",
            "CLAUDE.md",
            ".claude/skills/no-shortcuts/SKILL.md",
            ".claude/skills/solver-first/SKILL.md",
            "COGNITIVE_CORRAL_TRIGGERS_SETUP.md",
        )
    )
    assert "resource budget" in active
    assert "one gpu process" in active
    assert "nr<=16/24" not in active
    assert "69 passed" not in active


def test_decision_packet_is_lay_assessable_and_does_not_treat_approval_as_proof():
    agents = normalized("AGENTS.md")
    claude = normalized("CLAUDE.md")
    assert "lay packet" in agents
    assert "approval is authority, not proof" in agents
    assert "the change" in claude
    assert "alternatives" in claude
    assert "count against" in claude


def test_behavior_case_set_was_frozen_with_required_and_held_back_cases():
    payload = json.loads(read("tests/guardrail_behavior_cases.json"))
    assert payload["frozen_before_revised_runtime_evaluation"] is True
    cases = payload["cases"]
    identifiers = {case["id"].lower() for case in cases}
    assert len(cases) >= 18
    assert len(identifiers) == len(cases)
    assert {case["set"] for case in cases} == {"required", "held_back"}
    for required in (
        "hidden_action",
        "controlled_approximation",
        "first_variation",
        "failed_finite_search",
        "upstream_change",
        "protected_input",
        "data_tuned_promotion",
    ):
        assert required in identifiers
    rubric = payload["adjudication"]
    assert {"missed_substantive_defect", "unnecessary_block", "repeat_permission"} <= set(rubric)
