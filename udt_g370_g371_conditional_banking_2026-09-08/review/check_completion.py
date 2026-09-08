"""Focused post-audit completion correspondence, not a new scientific review."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "udt_g370_g371_conditional_banking_2026-09-08"
CHANGED = {"LIVE.md", "HANDOFF.md", "CURRENT_RESEARCH_PROGRAM.md"}
OLD = b"Promotion integration is PENDING the gates in its EXECUTION_RECORD.md."
NEW = (b"Promotion integration is COMPLETE: full354 audit and fresh fidelity PASS_WITH_CAVEATS.\n"
       b"Its EXECUTION_RECORD.md owns exact checks and preservation/publication history.")


def sha(data):
    return hashlib.sha256(data).hexdigest()


current_pins = {}
with (PKG / "INTEGRATION_FREEZE.tsv").open() as stream:
    for row in csv.DictReader(stream, delimiter="\t"):
        data = (ROOT / row["path"]).read_bytes()
        current_pins[row["path"]] = sha(data)
        if row["path"] in CHANGED:
            assert data.count(NEW) == 1 and OLD not in data, row["path"]
            data = data.replace(NEW, OLD, 1)
        assert sha(data) == row["sha256"], "change beyond three completion replacements: " + row["path"]

receipts = {"full354.stdout": "174fcdf678b58c4e642528611d0a4140362b720cd7e6a98370e98cd2f6f6dd10",
            "full354.stderr": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "full354.time": "81fb9a5d2da2ce9a7bf4931995862a5da5e9c790edd6e5581259448c203ed43e"}
for path, expected in receipts.items():
    assert sha((PKG / path).read_bytes()) == expected, path
assert b"PASS: 354-row premise registry" in (PKG / "full354.stdout").read_bytes()
assert "Exit status: 0" in (PKG / "full354.time").read_text()
capture = json.loads((PKG / "banking_checks_completion.json").read_text())
assert capture["returncode"] == 0 and not capture["timeout"]
assert (PKG / "banking_checks_completion.stdout").read_bytes() == (
    PKG / "review/author_guard_replay.stdout").read_bytes()
assert not (PKG / "banking_checks_completion.stderr").read_bytes()

print(json.dumps({"status": "PASS", "meaning": "three completion-only replacements and receipt correspondence; no full audit rerun",
                  "current_target_sha256": current_pins, "full354_receipt_sha256": receipts,
                  "parent_completion_guard_receipt": capture,
                  "initial_fidelity_report_sha256": sha((PKG / "review/ADVERSARIAL_REVIEW_INITIAL.md").read_bytes()),
                  "publication": "NOT_VERIFIED_BY_REVIEWER"}, indent=2, sort_keys=True))
