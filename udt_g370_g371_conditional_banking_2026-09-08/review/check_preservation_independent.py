"""Bounded independent integration checks; no author guard/science imports.

Prepared after the source-first seal and before direct new target intake.
Bytes, schema and actual rejected corruptions only; not scientific proof.
The existing run_capture helper owns resource/output preservation.
"""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[2]
BASE = "6eea4b90c59e5fd873d793c073b55ecab67d1992"
REGISTRY = "CURRENT_SCIENTIFIC_PREMISES.tsv"
NEW = {b"G370", b"G371"}
BANK = b"udt_g370_g371_conditional_banking_2026-09-08/BANKING_RECORD.md"
PRESERVE = ["udt_metric_source_reconstructibility_campaign_2026-09-08",
            "udt_source_metric_connection_campaign_2026-09-08",
            "udt_g367_g369_conditional_banking_2026-09-08",
            "CANON.md", "UDT_METRIC_KERNEL_DEVELOPMENT.md",
            "UDT_METRIC_KERNEL_COVERAGE.tsv"]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def assess_registry(data, baseline):
    failures = []
    lines = data.splitlines(keepends=True)
    cols = lines[0].rstrip(b"\r\n").split(b"\t")
    items = [line.rstrip(b"\r\n").split(b"\t") for line in lines[1:]]
    ids = [fields[0] for fields in items]
    if len(items) != 354 or len(set(ids)) != 354:
        failures.append("354 unique rows")
    if {item for item in ids if item in NEW} != NEW:
        failures.append("both new IDs")
    retained = b"".join(line for line in lines if line.split(b"\t", 1)[0] not in NEW)
    if retained != baseline:
        failures.append("all352 original bytes")
    for fields in items:
        if fields[0] not in NEW:
            continue
        if len(fields) != len(cols) or not all(fields):
            failures.append("new row schema")
            continue
        row = dict(zip(cols, fields))
        if row[b"controlling_source"] != BANK:
            failures.append("new source ownership")
        if b"BANKED_DERIVED_CONDITIONAL" not in row[b"current_status"]:
            failures.append("conditional banking status")
    return failures


baseline = git("show", BASE + ":" + REGISTRY)
current = (ROOT / REGISTRY).read_bytes()
assert len(baseline.splitlines()) == 353, "baseline registry must have352 data rows"
assert not assess_registry(current, baseline), assess_registry(current, baseline)

lines = current.splitlines(keepends=True)
old = next(line for line in lines[1:] if line.split(b"\t", 1)[0] not in NEW)
new_lines = [line for line in lines[1:] if line.split(b"\t", 1)[0] in NEW]
new_line = new_lines[0]
fixtures = {
    "alter_earlier_row": (current.replace(old, old.rstrip(b"\n") + b" CORRUPTION\n", 1), "all352 original bytes"),
    "remove_new_row": (current.replace(new_lines[-1], b"", 1), "both new IDs"),
    "duplicate_new_row": (current + new_line, "354 unique rows"),
    "new_source_displacement": (current.replace(BANK, b"unreviewed/source.md", 1), "new source ownership"),
    "unconditional_grade": (current.replace(new_line, new_line.replace(b"BANKED_DERIVED_CONDITIONAL", b"DERIVED"), 1), "conditional banking status"),
}
rejections = {}
for label, (mutant, expected) in fixtures.items():
    failed = assess_registry(mutant, baseline)
    assert expected in failed, (label, expected, failed)
    rejections[label] = failed

preserved = {}
archive_bytes = git("archive", "--format=tar", BASE, "--", *PRESERVE)
with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
    for member in archive:
        if not member.isfile():
            continue
        expected = archive.extractfile(member).read()
        actual = (ROOT / member.name).read_bytes()
        assert actual == expected, "changed protected-source bytes: " + member.name
        preserved[member.name] = digest(actual)

review = ROOT / PRESERVE[0] / "step_02/review"
failed_run = json.loads((review / "independent_initial.json").read_text())
success = json.loads((review / "independent_syntax_repaired.json").read_text())
assert failed_run["returncode"] == 1 and not failed_run["timeout"]
assert b"SyntaxError" in (review / "independent_initial.stderr").read_bytes()
assert success["returncode"] == 0 and not success["timeout"]
assert (review / "independent_product_check_initial_failed.py").read_bytes() != (
    review / "independent_product_check.py").read_bytes()

print(json.dumps({
    "status": "PASS", "meaning": "registry byte/schema preservation, original evidence correspondence and actual mutant rejection only",
    "python": sys.version, "baseline": BASE, "head": git("rev-parse", "HEAD").decode().strip(),
    "original_registry_sha256": digest(baseline), "current_registry_sha256": digest(current),
    "new_row_sha256": {line.split(b"\t", 1)[0].decode(): digest(line) for line in new_lines},
    "preserved_file_count": len(preserved), "preserved_file_sha256": preserved,
    "registry_actual_rejections": rejections, "RT2_syntax_failure_and_corrected_success_retained": True,
}, indent=2, sort_keys=True))
