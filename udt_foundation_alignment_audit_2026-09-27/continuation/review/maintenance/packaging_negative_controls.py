"""Isolated metadata controls through the actual maintenance checker.

No scientific implementation runs, and no authoritative metadata is modified.
ROOT and PREFIX remain those initialized by the actual checker; only PACKET is
redirected to copied metadata. A successful positive run precedes each failure.
"""
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
PACKET = OUT.parents[1]
SPEC = importlib.util.spec_from_file_location("actual_integrity_checker", PACKET / "check_integrity.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
FIXTURE = Path(tempfile.mkdtemp(prefix="udt_packaging_metadata_review_"))
FIXTURE_NAMES = [
    "BASELINE.json", "archive/ARCHIVE_MANIFEST.tsv",
    "review/science/SOURCE_PINS.tsv", "initial_candidate/FREEZE.json",
    "initial_candidate/ATTACHMENT_CANDIDATE.md",
]
ORIGINALS = {name: (PACKET / name).read_bytes() for name in FIXTURE_NAMES}


def restore():
    for name, data in ORIGINALS.items():
        destination = FIXTURE / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)


def rewrite_table(name, mutate):
    path = FIXTURE / name
    reader = csv.DictReader(io.StringIO(path.read_text()), delimiter="\t")
    fields = reader.fieldnames
    rows = list(reader)
    rows = mutate(rows)
    with path.open("w") as handle:
        writer = csv.DictWriter(handle, fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def wrong_commit(rows):
    rows[0]["source_commit"] = "0" * 40
    return rows


def duplicate_pin(rows):
    rows[1]["path"] = rows[0]["path"]
    return rows


def main():
    CHECKER.PACKET = FIXTURE
    results = []
    cases = [
        ("wrong_archive_source_commit", "archive/ARCHIVE_MANIFEST.tsv", wrong_commit, "archive source commit mismatch"),
        ("empty_source_pins", "review/science/SOURCE_PINS.tsv", lambda rows: [], "source"),
        ("duplicate_source_pin_path", "review/science/SOURCE_PINS.tsv", duplicate_pin, "source"),
    ]
    for label, path, mutate, expected in cases:
        restore()
        positive = CHECKER.run()
        assert positive["status"] == "PASS"
        assert positive["reviewer_source_pins_checked"] == 41
        rewrite_table(path, mutate)
        try:
            CHECKER.run()
        except AssertionError as exc:
            diagnostic = str(exc)
            assert expected.lower() in diagnostic.lower(), (label, diagnostic)
            results.append({"case": label, "positive_control": "PASS", "negative_control": "REJECTED", "diagnostic": diagnostic})
        else:
            raise AssertionError("False pass: " + label)
    preserved = all((PACKET / name).read_bytes() == data for name, data in ORIGINALS.items())
    assert preserved
    record = {
        "status": "PASS", "scope": "Three isolated metadata defects through actual checker; no scientific replay",
        "python": sys.version, "checker_sha256": hashlib.sha256((PACKET / "check_integrity.py").read_bytes()).hexdigest(),
        "fixture": str(FIXTURE), "actual_root": str(CHECKER.ROOT), "actual_prefix": CHECKER.PREFIX,
        "authoritative_fixture_inputs_unchanged": preserved, "cases": results,
    }
    (OUT / "PACKAGING_NEGATIVE_CONTROLS.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
