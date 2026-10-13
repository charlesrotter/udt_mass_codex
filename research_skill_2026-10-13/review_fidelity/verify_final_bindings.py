"""Bounded method/copy verification; never open inherited scientific payloads."""
import difflib
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[2]
out = Path(__file__).resolve().parent
package = root / "research_skill_2026-10-13"
protected = (
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/",
    "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/",
    "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/",
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/",
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


freeze_path = package / "INTEGRATION_FREEZE.json"
freeze_bytes = freeze_path.read_bytes()
freeze = json.loads(freeze_bytes)
prior_path = root / freeze["prior_review_record"]
prior_bytes = prior_path.read_bytes()
prior = json.loads(prior_bytes)
accepted = freeze["accepted_sha256"]
old = prior["accepted_sha256"]
added = sorted(set(accepted) - set(old))
removed = sorted(set(old) - set(accepted))
changed = {
    name: {"before": old[name], "after": accepted[name]}
    for name in sorted(set(old) & set(accepted)) if old[name] != accepted[name]
}
unchanged = sum(accepted.get(name) == digest for name, digest in old.items())
assert sha(prior_bytes) == freeze["prior_review_record_sha256"]
assert added == sorted(freeze["added"])
assert removed == freeze["removed"] == []
assert changed == freeze["inherited_changed"]
assert unchanged == freeze["inherited_unchanged_count"]
assert set(changed) == {"AGENTS.md", "HANDOFF.md", "LIVE.md", "UDT_RESEARCH_OPERATING_PLAN.md"}

hash_names = added + sorted(changed)
assert not any(name.startswith(protected) for name in hash_names)
hash_mismatches = []
for name in hash_names:
    data = (root / name).read_bytes()
    if sha(data) != accepted[name]:
        hash_mismatches.append(name)
assert not hash_mismatches, hash_mismatches

pins = read_json(package / "INITIAL_TRIAL_PINS.json")
for name, digest in pins.items():
    path = Path(name)
    assert path.is_relative_to(Path("/tmp/udt-research-skill-2026-10-13"))
    assert sha(path.read_bytes()) == digest, name
copies = read_json(package / "TRIAL_CORRESPONDENCE.json")
for row in copies["outputs"]:
    src = Path(row["original"])
    assert src.is_relative_to(Path("/tmp/udt-research-skill-2026-10-13"))
    data = src.read_bytes()
    assert data == (root / row["saved"]).read_bytes(), row["saved"]
    assert sha(data) == row["sha256"] == accepted[row["saved"]]

fixture_count = 0
for case in ("case_a", "case_b", "case_c"):
    for name in ("TASK.md", "NOTEBOOK.md"):
        saved = package / "fixtures" / case / name
        original = f"/tmp/udt-research-skill-2026-10-13/{case}/{name}"
        assert sha(saved.read_bytes()) == pins[original]
        fixture_count += 1

initial_skill = (package / "INITIAL_SKILL.md").read_text()
final_skill = (root / ".agents/skills/goal-directed-research/SKILL.md").read_text()
skill_diff = "".join(difflib.unified_diff(initial_skill.splitlines(True),
                                        final_skill.splitlines(True),
                                        fromfile="INITIAL_SKILL.md", tofile="final SKILL.md"))
assert (package / "INITIAL_OPENAI.yaml").read_bytes() == (
    root / ".agents/skills/goal-directed-research/agents/openai.yaml").read_bytes()
actual_diff = subprocess.check_output(
    ["git", "diff", "--no-ext-diff", "--binary", "HEAD", "--", *sorted(changed)], cwd=root
)
assert actual_diff == (package / "FINAL_TRACKED_DIFF.patch").read_bytes()

original_check = read_json(package / "trials/case_a/check.stdout.json")
replay_check = read_json(package / "checks/case_a_replay.stdout")
replay = read_json(package / "checks/case_a_replay.json")
for name in ("status", "checks", "first_derivative", "second_derivative", "arithmetic", "scope"):
    assert original_check[name] == replay_check[name], name
assert original_check["status"] == "PASS"
assert len(original_check["checks"]) == 6 and all(original_check["checks"].values())
assert replay["command"] == ["python3", "research_skill_2026-10-13/trials/case_a/check.py"]
assert replay["returncode"] == 0
assert replay["wall_timeout_seconds"] is None and replay["cpu_timeout_seconds"] is None
assert replay["address_space_bytes"] == 2 * 1024 ** 3
for stream in ("stdout", "stderr"):
    assert sha((package / f"checks/case_a_replay.{stream}").read_bytes()) == replay[f"{stream}_sha256"]

b_manifest = read_json(package / "trials/case_b/manifest.json")
for name, digest in b_manifest["artifacts"].items():
    assert sha((package / "trials/case_b" / name).read_bytes()) == digest

result = {
    "status": "PASS",
    "scope": "Method/artifact bindings only; no scientific payload read or new scientific check",
    "freeze_sha256": sha(freeze_bytes),
    "prior_record_sha256": sha(prior_bytes),
    "accepted_map_count": len(accepted),
    "prior_map_count": len(old),
    "unchanged_inherited_map_entries": unchanged,
    "changed_inherited_count": len(changed),
    "added_count": len(added),
    "removed_count": len(removed),
    "current_added_changed_hashes_checked": len(hash_names),
    "current_hash_mismatches": hash_mismatches,
    "protected_payloads_read_or_hashed": False,
    "inherited_scientific_payloads_read_or_hashed": False,
    "original_input_hashes_checked": len(pins),
    "exact_original_output_copies_checked": len(copies["outputs"]),
    "saved_raw_fixture_hashes_checked": fixture_count,
    "original_case_b_internal_artifact_hashes_checked": len(b_manifest["artifacts"]),
    "final_tracked_diff_matches_current_HEAD_diff": True,
    "initial_to_final_skill_diff": skill_diff,
    "ui_metadata_byte_unchanged": True,
    "case_a_six_exact_comparisons_and_derivative_arrays_match_replay": True,
    "case_a_replay_receipt": {
        key: replay[key] for key in ("command", "returncode", "duration_seconds",
                                     "wall_timeout_seconds", "cpu_timeout_seconds", "address_space_bytes")
    },
    "limits": [
        "Inherited hashes were compared between review maps, not recalculated from scientific files.",
        "Copied-file identity does not prove initial chronology or independent authorship.",
        "Case A replay is same-code regression; original timeout history remains unchanged.",
        "No final normal/maintenance/full406 gate or publication executed or attested.",
    ],
}
(out / "FINAL_BINDING_CHECKS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: result[k] for k in (
    "status", "freeze_sha256", "accepted_map_count", "unchanged_inherited_map_entries",
    "current_added_changed_hashes_checked", "original_input_hashes_checked",
    "exact_original_output_copies_checked", "saved_raw_fixture_hashes_checked",
    "initial_to_final_skill_diff")}, indent=2))
