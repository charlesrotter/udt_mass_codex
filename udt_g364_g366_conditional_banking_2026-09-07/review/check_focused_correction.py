"""Independently authenticate the one exposure-wording correction; no writes."""
import hashlib
import json
import pathlib

root = pathlib.Path(__file__).resolve().parents[2]
bank = "udt_g364_g366_conditional_banking_2026-09-07"
original = (root / bank / "diagnostics/BANKING_RECORD_INITIAL.md").read_bytes()
current = (root / bank / "BANKING_RECORD.md").read_bytes()
before = b"parameter-diagnostic and SOS/commutator hints"
after = b"parameter-diagnostic and SOS method hints"
assert original.count(before) == 1 and before not in current
assert current == original.replace(before, after), "change exceeds requested correction"
assert hashlib.sha256(original).hexdigest() == (
    "3ff6eb0245b805e5e50a41a6e2bfd906c8af2fdfaaf3b9aecd50a87e83d7490f")
remaining = []
for line in (root / bank / "DIRECT_REVIEW_SHA256SUMS.stdout").read_text().splitlines():
    digest, relative = line.split(maxsplit=1)
    data = original if relative == bank + "/BANKING_RECORD.md" else (root / relative).read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest, relative
    if relative != bank + "/BANKING_RECORD.md":
        remaining.append(relative)
assert len(remaining) == 15
audit = json.loads((root / bank / "CLEAN_PREMISE_AUDIT.json").read_text())
assert audit["exit_code"] == 0 and not audit["timeout"] and audit["stderr"] == ""
assert "PASS: 349-row premise registry" in audit["stdout"]
print(json.dumps({
    "status": "PASS",
    "only_difference": [before.decode(), after.decode()],
    "original_bank_sha256": hashlib.sha256(original).hexdigest(),
    "corrected_bank_sha256": hashlib.sha256(current).hexdigest(),
    "other_frozen_targets_identical": remaining,
    "audit_inspected_not_rerun": {
        "file": bank + "/CLEAN_PREMISE_AUDIT.json",
        "sha256": hashlib.sha256((root / bank / "CLEAN_PREMISE_AUDIT.json").read_bytes()).hexdigest(),
        "exit_code": audit["exit_code"], "elapsed_seconds": audit["elapsed_seconds"],
        "maxrss_kib": audit["maxrss_kib"],
    },
    "scientific_rederivation": "NOT_PERFORMED",
}, indent=2))
