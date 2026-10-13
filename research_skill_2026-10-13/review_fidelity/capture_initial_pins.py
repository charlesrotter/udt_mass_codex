"""Capture only the authorized RSK1 method-review source pins and actual diff."""
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[2]
out = Path(__file__).resolve().parent
names = [
    "AGENTS.md", "CLAUDE.md", "UDT_RESEARCH_OPERATING_PLAN.md", "LIVE.md",
    "HANDOFF.md", ".agents/skills/goal-directed-research/SKILL.md",
    ".agents/skills/goal-directed-research/agents/openai.yaml",
    "research_skill_2026-10-13/WORK_ORDER.md",
    "research_skill_2026-10-13/EVALUATION_PLAN.md",
    "research_skill_2026-10-13/INITIAL_SKILL.md",
]
tracked = ["AGENTS.md", "HANDOFF.md", "LIVE.md", "UDT_RESEARCH_OPERATING_PLAN.md"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=root)


sources = {name: (root / name).read_bytes() for name in names}
head = git("rev-parse", "HEAD").decode().strip()
diff = git("diff", "--no-ext-diff", "--binary", "HEAD", "--", *tracked)
(out / "INITIAL_TRACKED_DIFF.patch").write_bytes(diff)
for name, data in sources.items():
    if (root / name).read_bytes() != data:
        raise RuntimeError(f"Source changed during pin capture: {name}")
manifest = {
    "review_stage": "INITIAL_METHOD_FIDELITY_REVIEW_NOT_FINAL_ATTESTATION",
    "reviewer_context": "/root/skill_trial_b",
    "model": "inherited model; exact identifier not independently verified",
    "prior_exposure": ["initial skill", "Case B source packet and own outputs"],
    "evaluation_plan_exposure": "first read in this integration review",
    "sibling_review_or_parent_outcome_exposure_before_initial_save": False,
    "parent_startup": "attributed synchronized grok at 60c273ef",
    "independently_read_current_HEAD": head,
    "source_sha256": {name: digest(data) for name, data in sources.items()},
    "initial_and_current_skill_byte_identical": sources[names[5]] == sources[names[9]],
    "tracked_diff_command": "git diff --no-ext-diff --binary HEAD -- " + " ".join(tracked),
    "tracked_diff_sha256": digest(diff),
    "report_sha256": digest((out / "INITIAL_REPORT.md").read_bytes()),
    "source_files_stable_during_pin_capture": True,
    "limits": [
        "Only current LIVE/HANDOFF blocks received content review.",
        "CLAUDE and operating-plan method sections were reviewed; full hashes pin versions only.",
        "No final map, gate completion, remote sync, scientific truth or promotion is attested.",
        "Checksums establish byte correspondence only.",
    ],
}
(out / "INITIAL_PINS.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"head": head, "sources_pinned": len(sources),
                  "initial_skill_identical": manifest["initial_and_current_skill_byte_identical"],
                  "diff_sha256": digest(diff)}, indent=2))
