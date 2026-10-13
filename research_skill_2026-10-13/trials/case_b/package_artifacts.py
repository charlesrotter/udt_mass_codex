"""Preserve the supplied proposal and bind this case's artifacts; no research probe."""
import hashlib
import json
import platform
from pathlib import Path

case = Path(__file__).resolve().parent.parent
output = case / "output"
source_names = [
    "TASK.md",
    "NOTEBOOK.md",
    "AGENTS.md",
    "UDT_RESEARCH_OPERATING_PLAN.md",
    ".agents/skills/goal-directed-research/SKILL.md",
]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


source_bytes = {name: (case / name).read_bytes() for name in source_names}
copy_path = output / "INITIAL_PROPOSAL.md"
if copy_path.exists():
    if copy_path.read_bytes() != source_bytes["NOTEBOOK.md"]:
        raise RuntimeError("Existing initial proposal differs; preserving it.")
else:
    copy_path.write_bytes(source_bytes["NOTEBOOK.md"])

for name, content in source_bytes.items():
    if (case / name).read_bytes() != content:
        raise RuntimeError(f"Input changed during packaging: {name}")

artifact_names = [
    "INITIAL_PROPOSAL.md",
    "NOTEBOOK.md",
    "CANDIDATE.md",
    "RETURN.md",
    "package_artifacts.py",
]
manifest = {
    "status": "CANDIDATE_FOR_REVIEW",
    "command": f"python3 {output / 'package_artifacts.py'}",
    "python_version": platform.python_version(),
    "sources": {name: sha256(data) for name, data in source_bytes.items()},
    "artifacts": {
        name: sha256((output / name).read_bytes()) for name in artifact_names
    },
    "checks": {
        "initial_proposal_byte_identical": copy_path.read_bytes()
        == source_bytes["NOTEBOOK.md"],
        "inputs_unchanged_during_packaging": True,
    },
    "research_cpu_probes_used": 0,
    "fresh_review_performed": False,
    "publication_performed": False,
    "limits": [
        "Hashes establish correspondence only, not truth or review.",
        "The manifest excludes itself to avoid self-referential hashing.",
        "Preservation comparison covers the packaging operation; original reads"
        " and tool edits are recorded in the conversation.",
        "No real repository state was independently checked by this scoped agent.",
    ],
}
(output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"status": manifest["status"], "checks": manifest["checks"],
                  "source_count": len(source_names),
                  "hashed_artifact_count": len(artifact_names)}, indent=2))
