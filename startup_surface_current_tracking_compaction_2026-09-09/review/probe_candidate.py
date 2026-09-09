"""Review-only actual guard probes; scientific sources are never modified."""

import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
REVIEW = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import verify_current_scientific_premises as guard

spec = importlib.util.spec_from_file_location("review_startup_tests", ROOT / "tests/test_startup_surface.py")
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)
scratch = REVIEW / "probe_fixture_initial"
assert not scratch.exists(), "preserve prior review fixture"
scratch.mkdir()
suite._startup_copy(scratch)
guard.validate_startup_surface(scratch)
print(json.dumps({"baseline": "PASS", "fixture": str(scratch)}), flush=True)

target = scratch / "LIVE.md"
original = target.read_text()
probes = [
    ("reversed_rescaling_exponent", "Lambda_hat=a^2 Lambda", "Lambda_hat=a^-2 Lambda"),
    ("joint_development_reduced_to_reconstruction", "joint evolution under an", "algebraic reconstruction under an"),
    ("measurement_prerequisite_reversed", "not a blanket prerequisite", "a blanket prerequisite"),
    ("discussion_stop_removed", "no new campaign is authorized", "a new campaign is authorized"),
]
for label, old, new in probes:
    assert old in original, (label, "fixture text absent")
    suite._replace(target, old, new)
    try:
        guard.validate_startup_surface(scratch)
    except SystemExit as exc:
        outcome = {"probe": label, "outcome": "CAUGHT", "message": str(exc)}
    else:
        outcome = {"probe": label, "outcome": "FALSE_PASS"}
    print(json.dumps(outcome), flush=True)
    target.write_text(original)
guard.validate_startup_surface(scratch)
print(json.dumps({"restored_fixture": "PASS"}), flush=True)

owned = {
    "LIVE.md", "HANDOFF.md", "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
    "MEMORY.md", "INDEX.md", "verify_current_scientific_premises.py", "tests/test_startup_surface.py",
}
changed = subprocess.check_output(["git", "diff", "--name-only", "15425bf61726d67a7a9b9473fb70cd881bde3687"], cwd=ROOT, text=True).splitlines()
assert set(changed) <= owned, changed
print(json.dumps({"tracked_change_scope": "PASS", "changed": changed}), flush=True)
for line in (REVIEW / "source_pins.stdout").read_text().splitlines():
    expected, relative = line.split(maxsplit=1)
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    baseline = subprocess.check_output(["git", "show", "15425bf61726d67a7a9b9473fb70cd881bde3687:" + relative], cwd=ROOT)
    assert actual == expected == hashlib.sha256(baseline).hexdigest(), relative
print(json.dumps({"ten_pinned_inputs_unchanged_from_baseline": "PASS"}), flush=True)
for relative in ("CANON.md", "UDT_METRIC_KERNEL_DEVELOPMENT.md", "UDT_METRIC_KERNEL_COVERAGE.tsv"):
    actual = (ROOT / relative).read_bytes()
    baseline = subprocess.check_output(["git", "show", "15425bf61726d67a7a9b9473fb70cd881bde3687:" + relative], cwd=ROOT)
    assert actual == baseline, relative
print(json.dumps({"canon_fixed_manuscript_and_coverage_unchanged": "PASS"}), flush=True)
