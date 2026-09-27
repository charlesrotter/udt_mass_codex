#!/usr/bin/env python3
"""Exercise actual builder validation on synthetic metadata in isolated scratch."""
import contextlib
import copy
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / "udt_repository_cleanup_2026-09-27/build_inventory.py"

def main():
    spec = importlib.util.spec_from_file_location("reviewed_cleanup_builder", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    scratch = Path(tempfile.mkdtemp(prefix="cleanup_builder_guard_"))
    root = scratch / "root"
    packet = root / "packet"
    (packet / "inventory").mkdir(parents=True)
    (root / "research/_registry").mkdir(parents=True)
    (packet / "BASELINE.json").write_text('{"HEAD":"synthetic_metadata_fixture"}\n')
    (root / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv").write_text("original_path\tcurrent_path\tpath_status\tfixed_base_blob_oid\tfixed_base_sha256\n")
    for name in ("review_a.md", "review_b.md"):
        (root / name).write_text("Synthetic guard fixture only; not a real review.\n")
    protected = module.PROTECTED[0] + "fixture.md"
    records = [dict(path=name, mode="100644", object_id="1" * 40, bytes="3")
               for name in ("candidate.md", "other.md", "AGENTS.md", protected)]
    module.ROOT = root
    module.PACKET = packet
    module.baseline_tree = lambda _: copy.deepcopy(records)
    columns = ["path", "disposition", "reason_id", "read_depth", "destination", "review_reference"]
    good = dict(path="candidate.md", disposition="ARCHIVE_REVIEWED", reason_id="R01",
                read_depth="FULL_CONTENT_REVIEW_SYNTHETIC", destination="archive/remaining_working_surfaces_2026-09-27/candidate.md",
                review_reference="review_a.md;review_b.md")

    def invoke(overrides, fields=columns):
        with (packet / "inventory/REVIEWED_OVERRIDES.tsv").open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
            writer.writeheader(); writer.writerows(overrides)
        with contextlib.redirect_stdout(io.StringIO()):
            module.build()

    invoke([good])
    results = {"valid_archive_metadata": "PASS"}

    def reject(name, replacement=None, *, fields=None, rows=None):
        trial = copy.deepcopy(good)
        if replacement:
            trial.update(replacement)
        try:
            invoke(rows if rows is not None else [trial], fields or columns)
        except (AssertionError, KeyError, ValueError) as error:
            results[name] = {"status": "REJECTED", "reason": str(error)}
            return
        raise AssertionError("builder false pass: " + name)

    reject("metadata_override_header", {"object_id": "0" * 40}, fields=columns + ["object_id"])
    reject("unknown_disposition", {"disposition": "ACCEPTED_PHYSICS"})
    reject("protected_payload_override", {"path": protected})
    reject("fixed_interface_override", {"path": "AGENTS.md"})
    reject("unknown_source", {"path": "not_in_baseline.md"})
    reject("duplicate_source", rows=[good, good])
    reject("duplicate_destination", rows=[good, good | {"path": "other.md"}])
    reject("destination_outside_archive", {"destination": "elsewhere/candidate.md"})
    reject("destination_traversal", {"destination": "archive/remaining_working_surfaces_2026-09-27/../candidate.md"})
    reject("absolute_destination", {"destination": "/tmp/candidate.md"})
    reject("metadata_only_archive", {"read_depth": "METADATA_ONLY_RETAIN_NO_SCIENTIFIC_REVIEW"})
    reject("single_review", {"review_reference": "review_a.md"})
    reject("duplicate_review", {"review_reference": "review_a.md;review_a.md"})
    reject("missing_review", {"review_reference": "review_a.md;missing.md"})
    reject("retained_destination_move", {"disposition": "RETAIN_ROOT_EVIDENCE_OR_DATA"})
    result = {"status": "PASS", "builder_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "scratch": str(scratch), "results": results,
              "scope": "Actual production build() guards, with only baseline_tree replaced by four synthetic metadata rows and ROOT/PACKET redirected. No scientific/protected content read. Review fixture files test existence only, not true reviewer independence."}
    (OUT / "BUILDER_GUARD_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
