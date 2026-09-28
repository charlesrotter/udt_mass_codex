"""Read-only provenance checks for this packet; not scientific verification.

Run from the repository root. Emits JSON to stdout; does not overwrite evidence.
Historical pins are checked against their explicit preserved version, never
silently treated as current. No unrelated untracked payload is read.
"""
import csv
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parent
PREFIX = PACKET.name + "/"
BASE = "df71211c11fde4b123d1e71e2028cc571719ea68"
checks = {}


def require(label, condition):
    if not condition:
        raise AssertionError(label)
    checks[label] = True


def sha(data):
    return hashlib.sha256(data).hexdigest()


def data(rel):
    return (ROOT / rel).read_bytes()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def document(rel):
    return json.loads((PACKET / rel).read_text())


require("branch_grok", git("branch", "--show-current").decode().strip() == "grok")
baseline_roadmap = git("show", BASE + ":UDT_RESEARCH_ROADMAP.md")
for row in csv.DictReader((PACKET / "SOURCE_PINS.tsv").open(), delimiter="\t"):
    content = baseline_roadmap if row["path"] == "UDT_RESEARCH_ROADMAP.md" else data(row["path"])
    require("parent_source:" + row["path"], sha(content) == row["sha256"])

for rel, key in [("canonical/SOURCE_PINS.json", "local_file_sha256"),
                 ("review/SOURCE_FIRST_FREEZE.json", "source_sha256"),
                 ("review/SOURCE_FIRST_FREEZE.json", "artifact_sha256"),
                 ("review/DIRECT_REVIEW_RECORD.json", "artifact_sha256"),
                 ("review/DIRECT_REVIEW_RECORD.json", "input_sha256")]:
    for name, expected in document(rel)[key].items():
        require(rel + ":" + key + ":" + name, sha(data(name)) == expected)
for name, expected in document("canonical/INITIAL_MANIFEST.json")["files"].items():
    require("canonical_initial:" + name, sha((PACKET / "canonical" / name).read_bytes()) == expected)
for name, expected in document("review/FOCUSED_REVIEW_RECORD.json")["reviewed_sha256"].items():
    # The reviewer explicitly reviewed a draft closeout; preserve that byte object.
    actual = (PACKET / "CLOSEOUT_REVIEW_INPUT.md").read_bytes() if name == PREFIX + "CLOSEOUT.md" else data(name)
    require("focused_review:" + name, sha(actual) == expected)

insertion = (PACKET / "ROADMAP_INSERT.md").read_text()
marker = "## Two-path equation investigation — 2026-09-27\n"
expected_roadmap = baseline_roadmap.decode().replace("Updated: 2026-09-27 UTC.", "Updated: 2026-09-28 UTC.", 1).replace(marker, insertion + "\n" + marker, 1)
require("roadmap_exact_reviewed_insertion_and_date_only", data("UDT_RESEARCH_ROADMAP.md").decode() == expected_roadmap)
changed = set(git("diff", BASE, "--name-only").decode().splitlines())
require("existing_tracked_changes_limited_to_roadmap", all(x == "UDT_RESEARCH_ROADMAP.md" or x.startswith(PREFIX) for x in changed))
prior = set(document("BASELINE.json")["pre_existing_untracked_paths"])
current = {x for x in git("ls-files", "--others", "--exclude-standard", "-z").decode().split("\0") if x and not x.startswith(PREFIX)}
require("52_unrelated_untracked_names_preserved_without_payload_reads", len(prior) == 52 and prior == current)

for left, right in [("PARENT_CHECKS.json", "parent.stdout.json"),
                    ("canonical/CHECK_RESULT.json", "canonical/check.stdout.txt")]:
    require("raw_result_correspondence:" + left, (PACKET / left).read_bytes() == (PACKET / right).read_bytes())
require("parent_56_pass", document("PARENT_CHECKS.json")["count"] == 56 and document("PARENT_CHECKS.json")["status"] == "PASS")
require("canonical_34_pass", document("canonical/CHECK_RESULT.json")["check_count"] == 34 and document("canonical/CHECK_RESULT.json")["status"] == "PASS")
for rel, count in [("review/source_first_checks.stdout.json", 10), ("review/direct_checks.stdout.json", 29)]:
    result = document(rel)
    require("review_counts:" + rel, result["passed"] == result["total"] == count)
failed = document("review/initial_failed_direct_checks.stdout.json")
require("failed_review_output_retained", failed["passed"] == 28 and failed["total"] == 29 and (PACKET / "review/initial_failed_direct_checks.stderr.txt").stat().st_size > 0)
for rel in ["parent.stderr.txt", "canonical/check.stderr.txt", "review/source_first_checks.stderr.txt", "review/direct_checks.stderr.txt", "premise_verifier.stderr.txt"]:
    require("successful_stderr_empty:" + rel, (PACKET / rel).stat().st_size == 0)
execution = document("PREMISE_VERIFIER_EXECUTION.json")
require("full_premise_execution_pass", execution["exit_code"] == 0 and execution["timeout"] is False)
premise_text = (PACKET / "premise_verifier.stdout.txt").read_text()
require("full_premise_stdout_406_pass", "406" in premise_text and "PASS" in premise_text)

json_count = 0
link_count = 0
for path in PACKET.rglob("*"):
    if not path.is_file() or path.name in {"PACKAGING_CHECKS.json", "MANIFEST.json"}:
        continue
    if path.suffix == ".json":
        json.loads(path.read_text())
        json_count += 1
    if path.suffix in {".md", ".py", ".tsv"}:
        raw = path.read_bytes()
        require("LF_and_no_trailing_whitespace:" + str(path.relative_to(PACKET)), b"\r" not in raw and all(line.rstrip(b" \t") == line for line in raw.splitlines()))
    if path.suffix == ".md":
        for target in re.findall(r"\[[^\]]+\]\(([^\s)]+)\)", path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            require("local_link:" + str(path.relative_to(PACKET)) + ":" + target, (path.parent / target.split("#")[0]).exists())
            link_count += 1

print(json.dumps({"status": "PASS", "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "command": "python3 udt_response_selection_methods_2026-09-27/verify_package.py > udt_response_selection_methods_2026-09-27/PACKAGING_CHECKS.json 2> udt_response_selection_methods_2026-09-27/packaging.stderr.txt",
    "baseline_head": BASE, "observed_head": git("rev-parse", "HEAD").decode().strip(),
    "json_files_parsed": json_count, "local_links_checked": link_count, "checks": checks,
    "limits": "Byte/provenance and packaging regression only; no scientific recomputation, promotion, remote sync, commit or push certification. Manifest is generated and checked separately after this result is frozen."}, indent=2))
