"""Read-only correspondence checks; not scientific proof or publication gate."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

P = Path(__file__).resolve().parent
ROOT = P.parent
BASE = "3b11eb2f2bf1d96182a9b9095d672349c308d6c9"
checks = {}


def require(label, ok):
    if not ok:
        raise AssertionError(label)
    checks[label] = True


def obj(name):
    return json.loads((P/name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


require("branch", git("branch", "--show-current").decode().strip() == "grok")
baseline_roadmap = git("show", BASE+":UDT_RESEARCH_ROADMAP.md")
for name, entry in obj("SOURCE_PINS.json")["local_files"].items():
    actual = hashlib.sha256(baseline_roadmap).hexdigest() if name == "UDT_RESEARCH_ROADMAP.md" else digest(ROOT/name)
    require("source:"+name, actual == entry["sha256"])
for name, expected in obj("review/SOURCE_FIRST_FREEZE.json")["source_sha256"].items():
    require("review_source:"+name, digest(ROOT/name) == expected)
for record, key in [("INITIAL_FREEZE.json", "files"), ("review/DIRECT_REVIEW_RECORD.json", "input_sha256")]:
    for name, expected in obj(record)[key].items():
        require(record+":"+name, digest(P/name) == expected)

# Focused record is checked separately against the preserved draft closeout
# and current final candidate, brief and insertion; its shape is reviewer-owned.
require("reviewed_draft_closeout_preserved", digest(P/"CLOSEOUT_REVIEW_INPUT.md") == "1e0acbc330bb0edc11486ffeb2a3c52f4871eec749f5b3ba9c6038b9491118de")
require("final_candidate", digest(P/"CANDIDATE.md") == "571e016a282dfe1a67a5bf6ff91376ec17ee703b79fd297a65b7c9ca2a61000c")
require("final_brief", digest(P/"DECISION_BRIEF.md") == "722962826039c26455db628a124a0e992d26a0aaa53c596fe4eb46d05b404f54")
require("reviewed_insertion", digest(P/"ROADMAP_INSERT.md") == "3b75df6811f877c8c2ab36e0129d1b01a6772efbcd67d18a64d0b9af083d62ba")
insertion = (P/"ROADMAP_INSERT.md").read_text()
marker = "## Response-selection methods — 2026-09-27\n"
require("roadmap_only_reviewed_insertion", (ROOT/"UDT_RESEARCH_ROADMAP.md").read_text() == baseline_roadmap.decode().replace(marker, insertion+"\n"+marker, 1))
for name, count in [("construction.stdout.json",50),("review/source_first_checks.stdout.json",47),("review/direct_checks.stdout.json",12)]:
    result = obj(name)
    require("exact_result:"+name, result["status"] == "PASS" and result["count"] == count)
for name in ["construction.stderr.txt","review/source_first_checks.stderr.txt","review/direct_checks.stderr.txt","premise_verifier.stderr.txt"]:
    require("empty_stderr:"+name, (P/name).stat().st_size == 0)
audit = obj("PREMISE_VERIFIER_EXECUTION.json")
require("current_premise_execution", audit["exit_code"] == 0 and audit["timeout"] is False)
require("full406_raw_pass", "PASS: 406-row premise registry" in (P/"premise_verifier.stdout.txt").read_text())
before = set(obj("BASELINE.json")["pre_existing_untracked_paths"])
after = {x for x in git("ls-files","--others","--exclude-standard","-z").decode().split("\0") if x and not x.startswith(P.name+"/")}
require("52_unrelated_path_names_preserved_without_payload_reads", len(before) == 52 and before == after)
changed = git("diff",BASE,"--name-only").decode().splitlines()
require("only_authorized_changes", all(x == "UDT_RESEARCH_ROADMAP.md" or x.startswith(P.name+"/") for x in changed))
for path in P.rglob("*"):
    if not path.is_file() or path.name in {"PACKAGING_CHECKS.json","MANIFEST.json"}:
        continue
    if path.suffix == ".json":
        json.loads(path.read_text())
    if path.suffix in {".md",".py"}:
        raw = path.read_bytes()
        require("whitespace:"+str(path.relative_to(P)), b"\r" not in raw and all(line.rstrip(b" \t") == line for line in raw.splitlines()))
    if path.suffix == ".md":
        for target in re.findall(r"\[[^\]]+\]\(([^\s)]+)\)",path.read_text()):
            if "://" not in target and not target.startswith("#"):
                require("link:"+str(path.relative_to(P))+":"+target, (path.parent/target.split("#")[0]).exists())
print(json.dumps({"status":"PASS","utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "command":"python3 udt_metric_derivation_response_bridge_2026-09-28/verify_package.py > udt_metric_derivation_response_bridge_2026-09-28/PACKAGING_CHECKS.json 2> udt_metric_derivation_response_bridge_2026-09-28/packaging.stderr.txt",
    "baseline_head":BASE,"checks":checks,"limits":"Correspondence/regression only. Review-focused pins and final manifest independently rechecked by parent; no proof, adoption, remote, commit or push certification."},indent=2))
