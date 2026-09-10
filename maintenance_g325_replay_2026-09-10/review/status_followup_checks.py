#!/usr/bin/env python3
"""Bounded status-fidelity and G349 no-write replay; no source repair."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
REVIEW = Path(__file__).resolve().parent
BASELINE = "51f189679d4029d750e375be949f41e2f15420fa"
STATUS = ("LIVE.md", "HANDOFF.md", "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
          "MEMORY.md", "INDEX.md", "UDT_RESEARCH_ROADMAP.md")
PACKAGE = "udt_g349_finite_null_wavefront_patch_area_2026-09-04"
CANDIDATES = {
    "udt_g325_g324_homogeneous_diagonal_linear_modes_2026-09-02/verify_package.py":
        "5a272422a731404c119def22d3d92c2f8baf1fc5fd2cd183db1d00a956bc01b0",
    "udt_g326_g324_homogeneous_offdiagonal_linear_modes_2026-09-02/verify_package.py":
        "8d0e15db5a75f32f6d6cd0da2b1baae3d7fa33d48061043f75fd9bf208ebba9f",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def baseline(path):
    return subprocess.check_output(["git", "show", f"{BASELINE}:{path}"], cwd=ROOT)


def tracked_snapshot():
    paths = subprocess.check_output(["git", "ls-files", "--", PACKAGE], cwd=ROOT, text=True).splitlines()
    result = []
    for path in paths:
        original = baseline(path)
        current = (ROOT / path).read_bytes()
        require(original == current, f"G349 source/evidence changed: {path}")
        result.append({"path": path, "baseline_sha256": sha(original), "current_sha256": sha(current), "unchanged": True})
    return result


def main():
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    require(head == BASELINE, "Review baseline changed")
    records = {"baseline": BASELINE, "review_scope": "STATUS_FIDELITY_AND_G349_DOCUMENTATION_DIAGNOSIS_ONLY",
               "g349_preservation_before": tracked_snapshot(), "status_hashes": {}, "candidate_hashes": {},
               "unchanged_authority": [], "initial_review_sha256": sha((REVIEW / "REVIEW.md").read_bytes())}
    before = {path: sha((ROOT / path).read_bytes()) for path in STATUS}
    for path, expected in CANDIDATES.items():
        observed = sha((ROOT / path).read_bytes())
        require(observed == expected, f"Previously reviewed checker changed: {path}")
        records["candidate_hashes"][path] = observed
    for path in ("verify_current_scientific_premises.py", "CURRENT_SCIENTIFIC_PREMISES.tsv", "CANON.md",
                 "UDT_METRIC_KERNEL_DEVELOPMENT.md", "UDT_METRIC_KERNEL_COVERAGE.tsv"):
        original = baseline(path)
        current = (ROOT / path).read_bytes()
        require(original == current, f"Scientific authority changed: {path}")
        records["unchanged_authority"].append({"path": path, "sha256": sha(current), "unchanged": True})
    command = ["python3", "-B", "-S", f"{PACKAGE}/verify_package.py"]
    env = dict(os.environ, UDT_NO_WRITE="1", PYTHONDONTWRITEBYTECODE="1")
    start = time.monotonic()
    completed = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=40)
    records["g349_command"] = {"argv": command, "cwd": str(ROOT), "environment_overrides":
        {"UDT_NO_WRITE": "1", "PYTHONDONTWRITEBYTECODE": "1"}, "stdout": completed.stdout,
        "stderr": completed.stderr, "returncode": completed.returncode, "seconds": time.monotonic() - start}
    result = json.loads(completed.stdout)
    failed = [name for name, passed in result["checks"].items() if not passed]
    require(completed.returncode == 1, "G349 no longer reaches documented failure")
    require(result["checks_passed"] == 20 and result["checks_total"] == 21, "G349 check counts changed")
    require(failed == ["geometric_not_physical_union_scope"], "G349 has another failure")
    require(completed.stderr == "", "Unexpected diagnostic stderr")
    records["g349_result"] = result
    program = (ROOT / "CURRENT_RESEARCH_PROGRAM.md").read_text()
    program_before = baseline("CURRENT_RESEARCH_PROGRAM.md").decode()
    sentence = "G349 finite sheet area is not endpoint image-union; that needs supplied global preimages."
    require(sentence in program and sentence in program_before, "Scientific G349 sentence changed")
    require("geometric endpoint image-union" not in program and "physical image-union" not in program,
            "Literal gate cause changed")
    records["unchanged_g349_program_sentence"] = sentence
    records["literal_required_phrase_missing"] = True
    records["forbidden_physical_phrase_absent"] = True
    for path in STATUS:
        text = (ROOT / path).read_text()
        require("G349" in text and "documentation" in text, f"Actual blocker missing: {path}")
        if path != "UDT_RESEARCH_ROADMAP.md":
            require("Full365 NOT_PASSED" in text, f"Audit status strengthened: {path}")
        require("Full365 NOT_PASSED at G325" not in text, f"Stale blocker: {path}")
    records["g349_preservation_after"] = tracked_snapshot()
    require(records["g349_preservation_before"] == records["g349_preservation_after"], "G349 replay mutated originals")
    after = {path: sha((ROOT / path).read_bytes()) for path in STATUS}
    require(before == after, "Status text changed during review")
    records["status_hashes"] = after
    records["status_diff"] = subprocess.check_output(["git", "diff", BASELINE, "--", *STATUS], cwd=ROOT, text=True)
    records["tracked_changed_files"] = subprocess.check_output(["git", "diff", "--name-only"], cwd=ROOT, text=True).splitlines()
    require(set(records["tracked_changed_files"]) == set(STATUS) | set(CANDIDATES), "Unexpected tracked maintenance scope")
    work = ROOT / "maintenance_g325_replay_2026-09-10/WORK_RECORD.md"
    records["work_record_sha256"] = sha(work.read_bytes())
    full = ROOT / "maintenance_g325_replay_2026-09-10/full_after_g325_g326.json"
    records["author_full_audit_record"] = json.loads(full.read_text())
    records["author_full_audit_record_sha256"] = sha(full.read_bytes())
    records["status"] = "PASS_SCOPED_STATUS_REVIEW_FULL365_REMAINS_NOT_PASSED"
    (REVIEW / "status_followup_results.json").write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": records["status"], "g349_files_unchanged": len(records["g349_preservation_after"]),
                      "g349_passed": result["checks_passed"], "g349_total": result["checks_total"], "failed": failed}, indent=2))


if __name__ == "__main__":
    main()
