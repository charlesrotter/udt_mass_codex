"""Bounded documentary correspondence checks; not scientific validation."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path.cwd()
archive = root / "archive/roadmap_history_2026-09-28"
launch = json.loads((archive / "LAUNCH.json").read_text())
baseline = launch["head"]
maintained = ["LIVE.md", "HANDOFF.md", "CURRENT_RESEARCH_PROGRAM.md", "MEMORY.md", "INDEX.md", "UDT_RESEARCH_ROADMAP.md"]
git_prefix = ["git", "-c", "core.preloadIndex=false", "-c", "grep.threads=1"]
def git(*args):
    return subprocess.check_output([*git_prefix, *args], text=True).strip()
def before(path):
    return subprocess.check_output([*git_prefix, "show", baseline + ":" + path])
def sha(data):
    return hashlib.sha256(data).hexdigest()

checks = []
def record(name, passed, detail=None):
    checks.append({"name": name, "passed": bool(passed), "detail": detail})

record("branch", git("branch", "--show-current") == "grok")
record("review_baseline_head", git("rev-parse", "HEAD") == baseline)
changed = git("diff", "--name-only", baseline).splitlines()
record("tracked_edit_scope", set(changed) == set(maintained), changed)
immutable = {p: h for p, h in launch["source_sha256"].items() if p not in maintained}
pins = [{"path": p, "expected": h, "actual": sha((root / p).read_bytes())} for p, h in immutable.items()]
record("immutable_launch_pins", all(x["expected"] == x["actual"] for x in pins), pins)
snapshot = archive / "UDT_RESEARCH_ROADMAP_before_consolidation.md"
record("archive_byte_identity", snapshot.read_bytes() == before("UDT_RESEARCH_ROADMAP.md"), sha(snapshot.read_bytes()))
old_program = before("CURRENT_RESEARCH_PROGRAM.md").decode()
program = (root / "CURRENT_RESEARCH_PROGRAM.md").read_text()
record("founding_program_opening_unchanged", old_program.split("## Architecture")[0] == program.split("## Current next gate")[0])
old_inventory = old_program.split("## Architecture", 1)[1].split("## Current next gate", 1)[0].rstrip()
new_inventory = program.split("## Architecture", 1)[1].rstrip()
record("program_architecture_and_dependency_inventory_unchanged", old_inventory == new_inventory)
old_roadmap = snapshot.read_text()
roadmap = (root / "UDT_RESEARCH_ROADMAP.md").read_text()
new_quotes = re.findall(r"^> .+$", roadmap, flags=re.M)
old_quotes = re.findall(r"^> .+$", old_roadmap, flags=re.M)
record("three_verbatim_owner_quotes", len(new_quotes) == 3 and all(x in old_quotes for x in new_quotes))
heading = "## Owner direction clarification — emergence question, 2026-09-13"
old_emergence = old_roadmap.split(heading, 1)[1].split("This current direction qualifies", 1)[0]
new_emergence = roadmap.split(heading, 1)[1].split("This continuing direction controls", 1)[0]
record("emergence_direction_substantive_text_unchanged", old_emergence == new_emergence)
for name in ["LIVE.md", "HANDOFF.md"]:
    text = (root / name).read_text()
    record(name + "_one_current_block", text.count("<!-- STARTUP_CURRENT_BEGIN -->") == 1 and text.count("<!-- STARTUP_CURRENT_END -->") == 1)
record("current_next_gate_heading", program.count("## Current next gate") == 1)
prior = set(launch["prior_untracked_paths"])
current_untracked = set(git("ls-files", "--others", "--exclude-standard").splitlines())
record("prior_untracked_pathnames_present", prior <= current_untracked, {"count": len(prior), "missing": sorted(prior-current_untracked)})
record("no_new_untracked_paths_outside_archive", all(p.startswith("archive/roadmap_history_2026-09-28/") for p in current_untracked-prior))

targets = []
for name in maintained + ["archive/roadmap_history_2026-09-28/README.md"]:
    source = root / name
    text = source.read_text()
    for m in re.finditer(r"\[[^\]\n]+\]\(([^\s)]+)(?:\s+\"[^\"\n]*\")?\)", text):
        target = m.group(1).strip("<>")
        if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target):
            continue
        path, _, anchor = target.partition("#")
        resolved = source.parent / (path or source.name)
        targets.append({"source": name, "target": target, "kind": "markdown", "exists": resolved.exists(), "anchor": anchor or None})
    if name in maintained:
        for target in re.findall(r"`([^`\n]+)`", text):
            if "/" in target and re.fullmatch(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*/?", target):
                targets.append({"source": name, "target": target, "kind": "code_path", "exists": (root / target).exists()})
record("all_current_literal_local_targets_exist", all(x["exists"] for x in targets), targets)
record("no_local_markdown_anchors_need_resolution", all(not x.get("anchor") for x in targets))
locator = (archive / "README.md").read_text().split("## Historical section locator", 1)[1]
locators = re.findall(r"^- (.+)$", locator, re.M)
historical_headings = re.findall(r"^#{1,6} (.+)$", old_roadmap, re.M)
record("archive_section_locator", all(x in historical_headings for x in locators), {"count": len(locators), "missing": [x for x in locators if x not in historical_headings]})
inbound = subprocess.run([*git_prefix, "grep", "-n", "-F", "UDT_RESEARCH_ROADMAP.md#", "--", "*.md", ":!udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/**", ":!udt_native_onshell_timelive_reset_owner_audit_2026-08-10/**", ":!udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/**", ":!udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/**"], capture_output=True, text=True)
record("no_tracked_inbound_roadmap_anchors", inbound.returncode == 1 and not inbound.stdout and not inbound.stderr)
whitespace = subprocess.run([*git_prefix, "diff", "--check"], capture_output=True, text=True)
record("diff_whitespace", whitespace.returncode == 0, whitespace.stdout + whitespace.stderr)

reviewed_paths = maintained + ["archive/roadmap_history_2026-09-28/README.md", "archive/roadmap_history_2026-09-28/WORK_RECORD.md", "archive/roadmap_history_2026-09-28/LAUNCH.json"]
result = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "baseline": baseline, "python": sys.version, "checks": checks, "reviewed_sha256": {p: sha((root / p).read_bytes()) for p in reviewed_paths}, "limits": "Literal local target and locator checks only; no renderer/link-network check, scientific reproof, full 406-row replay or protected-payload read."}
print(json.dumps(result, indent=2))
raise SystemExit(0 if all(x["passed"] for x in checks) else 1)
