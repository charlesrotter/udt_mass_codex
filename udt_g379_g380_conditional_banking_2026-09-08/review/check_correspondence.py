"""Independent byte/source correspondence for CF banking; no scientific proof."""
import csv
import datetime
import hashlib
import io
import json
from pathlib import Path
import platform
import subprocess
import sys

REVIEW = Path(__file__).resolve().parent
PACKAGE = REVIEW.parent
ROOT = PACKAGE.parent
BASE = "b1dda6724fae599f9684b5f3f03d421221569fe5"
CF = "udt_closed_fibre_persistence_campaign_2026-09-08"
INTEGRATION = [
    "AGENTS.md", "LIVE.md", "HANDOFF.md", "CURRENT_RESEARCH_PROGRAM.md",
    "CURRENT_SCIENTIFIC_PREMISES.md", "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "INDEX.md", "MEMORY.md", "verify_current_scientific_premises.py",
]

def git(*args):
    return subprocess.check_output(
        ["git", "-c", "core.preloadIndex=false", "-c", "index.threads=1",
         "-c", "core.packedGitWindowSize=16m", "-c", "core.packedGitLimit=64m", *args],
        cwd=ROOT, timeout=10)

def digest(data):
    return hashlib.sha256(data).hexdigest()

checks = {}
original_exception_hook = sys.excepthook
def preserve_partial_checks(exc_type, exc, traceback):
    print(json.dumps({"status": "INTERRUPTED", "checks": checks,
                      "exception": str(exc)}, indent=2), flush=True)
    original_exception_hook(exc_type, exc, traceback)
sys.excepthook = preserve_partial_checks

def check(name, condition):
    checks[name] = bool(condition)
    if not condition:
        print(json.dumps({"status": "FAILED", "checks": checks}, indent=2), flush=True)
        raise AssertionError(name)

check("observed_branch_grok", git("branch", "--show-current").strip() == b"grok")
raw = (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()
baseline = git("show", BASE + ":CURRENT_SCIENTIFIC_PREMISES.tsv")
old = b"".join(line for line in raw.splitlines(keepends=True)
               if line.split(b"\t", 1)[0] not in (b"G379", b"G380"))
check("all_361_prior_rows_and_header_byte_identical", old == baseline)
rows = list(csv.DictReader(io.StringIO(raw.decode()), delimiter="\t"))
old_rows = list(csv.DictReader(io.StringIO(baseline.decode()), delimiter="\t"))
ids = [row["premise_id"] for row in rows]
check("exactly_two_distinct_additions", len(rows) == len(set(ids)) == 363
      and len(old_rows) == 361
      and set(ids) - {row["premise_id"] for row in old_rows} == {"G379", "G380"})

manifest = PACKAGE / "SOURCE_EVIDENCE_SHA256SUMS"
entries = [line.split(maxsplit=1) for line in manifest.read_text().splitlines()]
members = git("ls-tree", "-r", "--name-only", BASE, "--", CF).decode().splitlines()
check("149_manifest_members_equal_original_git_tree", len(entries) == 149
      and len({name for _, name in entries}) == 149
      and set(members) == {name for _, name in entries})
payloads = {}
for expected, name in entries:
    data = (ROOT / name).read_bytes()
    check("original_git_and_manifest:" + name,
          data == git("show", BASE + ":" + name) and digest(data) == expected)
    payloads[name] = expected

pin_path = ROOT / CF / "step_02/SOURCE_PINS_SHA256SUMS"
pins = [line.split(maxsplit=1) for line in pin_path.read_text().splitlines()]
check("25_distinct_dependency_pins", len(pins) == len({name for _, name in pins}) == 25)
dependencies = {}
for expected, name in pins:
    historical = name in ("CURRENT_SCIENTIFIC_PREMISES.tsv", "verify_current_scientific_premises.py")
    data = git("show", BASE + ":" + name) if historical else (ROOT / name).read_bytes()
    check("dependency_pin:" + name, digest(data) == expected)
    dependencies[name] = {"sha256": expected, "bytes_from": BASE if historical else "live"}

changed = git("diff", BASE, "--name-only").decode().splitlines()
check("tracked_change_scope", all(name in INTEGRATION or name.startswith(PACKAGE.name + "/")
                                   for name in changed))
for name in ("CANON.md", "UDT_METRIC_KERNEL_DEVELOPMENT.md", "UDT_METRIC_KERNEL_COVERAGE.tsv"):
    check("fixed_payload:" + name, (ROOT / name).read_bytes() == git("show", BASE + ":" + name))
check("only_count_changed_in_method_authority", (ROOT / "AGENTS.md").read_bytes()
      == git("show", BASE + ":AGENTS.md").replace(b"361-row exact registry", b"363-row exact registry"))

receipt_stems = ["prebank_361", "focused_initial"]
if "--postbank" in sys.argv:
    receipt_stems.append("postbank_363")
receipts = {}
for stem in receipt_stems:
    path = PACKAGE / (stem + ".json")
    record = json.loads(path.read_text())
    stdout = (PACKAGE / (stem + ".stdout")).read_bytes()
    stderr = (PACKAGE / (stem + ".stderr")).read_bytes()
    check("receipt_success:" + stem, record["returncode"] == 0
          and record.get("timeout", False) is False
          and record["cwd"] == str(ROOT))
    if "stdout" in record:
        check("embedded_streams_match:" + stem, record["stdout"].encode() == stdout
              and record["stderr"].encode() == stderr)
    if stem in ("prebank_361", "postbank_363"):
        count = "361" if stem == "prebank_361" else "363"
        check("full_audit_scope:" + stem, (count + "-row premise registry").encode() in stdout
              and record["command"] == ["python3", "-B", "verify_current_scientific_premises.py"]
              and record["address_space_bytes"] == 2 * 1024 ** 3
              and record["cpu_wall_limit_seconds"] == 900)
    receipts[stem] = {"record_sha256": digest(path.read_bytes()),
                      "stdout_sha256": digest(stdout), "stderr_sha256": digest(stderr),
                      "returncode": record["returncode"],
                      "duration_seconds": record["duration_seconds"],
                      "timeout_field": record.get("timeout", "NOT_PRESENT; successful returncode recorded")}

replay_path = REVIEW / "guard_replay.stdout"
if replay_path.exists():
    check("same_code_guard_stdout_byte_identical", replay_path.read_bytes()
          == (PACKAGE / "focused_initial.stdout").read_bytes())
    check("same_code_guard_stderr_byte_identical", (REVIEW / "guard_replay.stderr").read_bytes()
          == (PACKAGE / "focused_initial.stderr").read_bytes())

source_routes = [
    "udt_shared_readout_metric_constraint_campaign_2026-09-06/step_03/CANDIDATE_ARGUMENT.md",
    "udt_shared_readout_metric_constraint_campaign_2026-09-06/step_03/REVIEW_RECORD.md",
    "udt_shared_readout_metric_constraint_campaign_2026-09-06/step_03/review/PHASE_B_ADVERSARIAL_REVIEW.md",
    "udt_g357_g360_conditional_banking_2026-09-07/BANKING_RECORD.md",
    "udt_g367_g369_conditional_banking_2026-09-08/BANKING_RECORD.md",
    "udt_source_metric_connection_campaign_2026-09-08/step_01/CANDIDATE_INITIAL.md",
    "udt_source_metric_connection_campaign_2026-09-08/step_01/REVIEWED_RESULT.md",
    "udt_source_metric_connection_campaign_2026-09-08/step_01/review/ADVERSARIAL_REVIEW_INITIAL.md",
    "udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/AUDIT_REPORT.md",
    "udt_g349_finite_null_wavefront_patch_area_2026-09-04/AUDIT_REPORT.md",
    "udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/AUDIT_REPORT.md",
    "udt_g352_clock_rate_carried_measure_readout_2026-09-05/AUDIT_REPORT.md",
]
packet = INTEGRATION + [PACKAGE.name + "/" + name for name in
    ("BANKING_RECORD.md", "NEXT_CAMPAIGN_PROPOSAL.md", "WORK_ORDER.md",
     "EXECUTION_RECORD.md", "SOURCE_EVIDENCE_SHA256SUMS", "check_banking.py")]
versions = {name: digest((ROOT / name).read_bytes()) for name in packet + source_routes}
print(json.dumps({
    "status": "PASS_CORRESPONDENCE_ONLY", "base": BASE,
    "recorded_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "head": git("rev-parse", "HEAD").decode().strip(),
    "python": platform.python_version(), "git": git("--version").decode().strip(),
    "checks": checks, "registry_rows": len(rows), "old_registry_sha256": digest(old),
    "source_manifest_sha256": digest(manifest.read_bytes()), "original_payloads": payloads,
    "dependency_pins": dependencies, "packet_and_planning_source_pins": versions,
    "parent_receipts_authenticated_not_rerun": receipts,
    "protected_payloads": "NOT_INSPECTED", "science_reproof": False,
    "different_model_human_formal": "UNTESTED",
}, indent=2), flush=True)
