"""Scoped packaging/startup/preservation check; not scientific verification."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess
import sys

package = Path(__file__).resolve().parents[1]
repo = package.parent
sys.path.insert(0, str(repo))
from verify_current_scientific_premises import validate_startup_surface

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

launch = json.loads((package / "LAUNCH.json").read_text())
initial = json.loads((package / "CONSTRUCTION_MANIFEST.json").read_text())
core = ["AGENTS.md", "CLAUDE.md", "CANON.md", "founding.md",
        "CURRENT_SCIENTIFIC_PREMISES.md", "CURRENT_SCIENTIFIC_PREMISES.tsv",
        "verify_current_scientific_premises.py"]
changed_core = [n for n in core if sha(repo/n) != launch["source_sha256"][n]]
assert not changed_core, changed_core
preserved = {"WORK_ORDER.md": "INITIAL_WORK_ORDER.md",
             "DECISION_BRIEF.md": "INITIAL_DECISION_BRIEF.md"}
mismatches = []
for name, item in initial["files"].items():
    actual = package / preserved.get(name, name)
    if sha(actual) != item["sha256"] or actual.stat().st_size != item["bytes"]:
        mismatches.append(name)
assert not mismatches, mismatches
missing = [n for n in launch["preexisting_untracked_paths"] if not (repo/n).exists()]
assert not missing, missing
surfaces = ["LIVE.md", "HANDOFF.md", "CURRENT_RESEARCH_PROGRAM.md",
            "UDT_RESEARCH_ROADMAP.md", "INDEX.md", "MEMORY.md"]
def scoped(name):
    return name in surfaces or name.startswith(package.name + "/")
tracked = subprocess.check_output(["git", "diff", "--name-only", "HEAD"], cwd=repo, text=True).splitlines()
assert all(scoped(n) for n in tracked), tracked
staged = subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=repo, text=True).splitlines()
assert all(scoped(n) for n in staged), staged
assert not set(staged).intersection(launch["preexisting_untracked_paths"])
validate_startup_surface(repo)
subprocess.run(["git", "diff", "--check"], cwd=repo, check=True)
broken = []
for doc in package.rglob("*.md"):
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", doc.read_text()):
        if target.startswith(("http:", "https:", "#")):
            continue
        target = target.split("#", 1)[0].strip("<>")
        if target and not (doc.parent/target).exists():
            broken.append([str(doc.relative_to(package)), target])
assert not broken, broken
audit = json.loads((package / "checks/full_premise_surface_repair.json").read_text())
assert audit["returncode"] == 0 and not audit["timeout"]
assert (package / "review/RE_REVIEW.md").exists()
now = datetime.datetime.now(datetime.timezone.utc)
elapsed = (now - datetime.datetime.fromisoformat(launch["launch_utc"])).total_seconds()
files = [f for f in package.rglob("*") if f.is_file() and "__pycache__" not in f.parts]
size = sum(f.stat().st_size for f in files)
assert elapsed < 21600 and size < 2*1024**3
out = {"utc": now.isoformat(), "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(),
       "scope": "Final packaging/startup/preservation; no new scientific verification or protected-content reads",
       "initial_files_preserved": len(initial["files"]), "mutable_snapshot_mapping": preserved,
       "core_sources_unchanged": core, "preexisting_paths_present": len(launch["preexisting_untracked_paths"]),
       "preexisting_paths_staged": [], "tracked_changes_in_scope": tracked,
       "startup_surface_validator": "PASS", "git_diff_check": "PASS", "relative_package_links": "PASS",
       "full_audit": {k:audit[k] for k in ("returncode", "duration_seconds", "timeout")},
       "full_audit_scope": "Active-status inputs before final prose changes; scientific inputs unchanged, current startup surface checked here",
       "elapsed_seconds_at_check": elapsed, "package_files_at_check": len(files), "package_bytes_at_check": size,
       "surface_sha256": {n:sha(repo/n) for n in surfaces}, "script_sha256": sha(Path(__file__))}
(package/"checks/CLOSEOUT_CHECK.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps(out, indent=2))
