"""Reviewer-owned exact correspondence check; no scientific truth claim."""
import datetime
import hashlib
import json
import subprocess
from pathlib import Path, PurePosixPath

root = Path(__file__).resolve().parents[3]
here = Path(__file__).resolve().parent
package = root / "udt_positional_effect_assignment_2026-10-13"
freeze_path = package / "INTEGRATION_FREEZE.json"
freeze_bytes = freeze_path.read_bytes()
freeze = json.loads(freeze_bytes)
accepted = freeze["accepted_sha256"]
protected = (
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
    "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
    "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
)


def forbidden(name):
    p = PurePosixPath(name)
    return p.is_absolute() or ".." in p.parts or any(
        name == q or name.startswith(q+"/") for q in protected)


# Complete lexical exclusion precedes access to any accepted-map payload.
assert not [name for name in accepted if forbidden(name)], "PROTECTED_OR_UNSAFE_PATH"
paths = {}
for name in accepted:
    resolved = (root / name).resolve(strict=True)
    relative = resolved.relative_to(root).as_posix()
    assert not forbidden(relative), "PROTECTED_RESOLVED_PATH"
    assert resolved.is_file(), "NONFILE"
    paths[name] = resolved


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()


mismatches = [name for name, expected in accepted.items()
              if sha_file(paths[name]) != expected]
assert not mismatches, mismatches
prior = json.loads((package / "PRIOR_REVIEW_RECORD.json").read_text())["accepted_sha256"]
changed = sorted(name for name in prior if accepted.get(name) != prior[name])
added = sorted(set(accepted)-set(prior))
assert changed == sorted(freeze["changed_prior_files"]), "CHANGED_LIST"
assert added == sorted(freeze["new_files"]), "ADDED_LIST"
assert not set(prior)-set(accepted), "DROPPED_INHERITED_PATH"
candidate = json.loads((package / "CANDIDATE_FREEZE.json").read_text())["files_sha256"]
assert all(sha_file(root / name) == digest for name, digest in candidate.items())

central = (root / "UDT_DEVELOPMENT.md").read_text()
program = (root / "CURRENT_RESEARCH_PROGRAM.md").read_text()
opening = central.split("<!-- DEVELOPMENT_ORIENTATION_BEGIN -->", 1)[1].split(
    "<!-- DEVELOPMENT_ORIENTATION_END -->", 1)[0].strip()
generated = program.split("<!-- GENERATED_DEVELOPMENT_BEGIN -->", 1)[1].split(
    "<!-- GENERATED_DEVELOPMENT_END -->", 1)[0].strip()
assert opening == generated, "PROGRAM_EXCERPT"

baseline = json.loads((package / "BASELINE.json").read_text())
current_untracked = subprocess.check_output(
    ["git", "ls-files", "--others", "--exclude-standard", "-z"], cwd=root
).decode().split("\0")
current_unrelated = sorted(name for name in current_untracked if name and not
    name.startswith("udt_positional_effect_assignment_2026-10-13/"))
assert current_unrelated == sorted(baseline["unrelated_untracked_names_only"]), "UNRELATED_NAMES"
assert freeze_bytes == freeze_path.read_bytes(), "FREEZE_CHANGED_DURING_CHECK"

result = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "PASS", "context": "/root/pea_review_math",
    "freeze_sha256": hashlib.sha256(freeze_bytes).hexdigest(),
    "accepted_entries_checked": len(accepted), "mismatches": mismatches,
    "protected_exclusion_before_payload_access": True,
    "protected_payloads_read_or_hashed": False,
    "prior_entries": len(prior), "changed_prior_files": changed,
    "added_entries": len(added), "candidate_entries_unchanged": len(candidate),
    "unrelated_names_only_unchanged": len(current_unrelated),
    "generated_program_matches_central_opening": True,
    "script_sha256": sha_file(Path(__file__)),
    "scope": "Correspondence and routing, not corpus-wide scientific reproof or parent final gates",
}
with (here / "FINAL_MAP_CHECK.json").open("x") as stream:
    json.dump(result, stream, indent=2)
    stream.write("\n")
print(json.dumps(result, indent=2))
