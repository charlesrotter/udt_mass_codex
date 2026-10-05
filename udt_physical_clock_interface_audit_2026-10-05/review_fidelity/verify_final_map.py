"""Read-only frozen-byte correspondence check; not semantic review."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import resource
import subprocess

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
root = Path.cwd().resolve()
package = Path("udt_physical_clock_interface_audit_2026-10-05")
freeze_path = package / "INTEGRATION_FREEZE.json"
freeze = json.loads(freeze_path.read_text())
expected = freeze["accepted_sha256"]
protected = [
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
    "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
    "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
]
def prohibited(name):
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts:
        return True
    if any(name == pref or name.startswith(pref + "/") for pref in protected):
        return True
    resolved = (root / name).resolve()
    if not resolved.is_relative_to(root):
        return True
    rel = resolved.relative_to(root).as_posix()
    return any(rel == pref or rel.startswith(pref + "/") for pref in protected)

# Complete path rejection precedes opening any mapped payload.
bad_paths = [x for x in expected if prohibited(x)]
if bad_paths:
    print(json.dumps({"status":"FAIL", "reason":"protected/unsafe path", "paths":bad_paths}))
    raise SystemExit(1)

def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024**2), b""):
            h.update(block)
    return h.hexdigest()

mismatches = []
for name, want in expected.items():
    got = digest(root / name)
    if got != want:
        mismatches.append({"path":name,"expected":want,"actual":got})

changed = subprocess.check_output(["git","diff","--name-only"],text=True).splitlines()
central = Path("UDT_DEVELOPMENT.md").read_text()
program = Path("CURRENT_RESEARCH_PROGRAM.md").read_text()
def block(text, start, end):
    return text.split(start,1)[1].split(end,1)[0].strip()

same_excerpt = block(central,"<!-- DEVELOPMENT_ORIENTATION_BEGIN -->","<!-- DEVELOPMENT_ORIENTATION_END -->") == block(program,"<!-- GENERATED_DEVELOPMENT_BEGIN -->","<!-- GENERATED_DEVELOPMENT_END -->")
insert = (package / "CENTRAL_INSERT.md").read_text().strip()
checks = {
    "no_protected_paths_opened":not bad_paths,
    "all_frozen_hashes_match":not mismatches,
    "changed_inherited_exact":sorted(changed)==sorted(freeze["changed_inherited"]),
    "generated_orientation_exact":same_excerpt,
    "reviewed_insert_present_exactly_once":central.count(insert)==1,
    "freeze_hash_matches_parent_dispatch":digest(freeze_path)=="664a2e96fa48d8a12ca38e64befd73c263dd30cb2e023a0ea0059bbf49c9f606",
}
result = {
    "status":"PASS" if all(checks.values()) else "FAIL",
    "scope":"Version correspondence only; separate FINAL_REVIEW owns semantics",
    "freeze_sha256":digest(freeze_path),
    "accepted_count":len(expected),
    "head":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
    "checks":checks,
    "mismatches":mismatches,
    "changed_inherited":changed,
}
print(json.dumps(result,indent=2))
raise SystemExit(0 if result["status"]=="PASS" else 1)
