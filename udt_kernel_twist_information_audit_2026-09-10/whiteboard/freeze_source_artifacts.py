#!/usr/bin/env python3
"""Hash only the explicitly consulted unprotected sources and own whiteboard files."""
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
paths = [
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/AUDIT_REPORT.md",
    "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXACT_DERIVATION.md",
    "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXTERNAL_REVIEW_ADJUDICATION.md",
    "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/STATUS_LEDGER.tsv",
    "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/AUDIT_REPORT.md",
    "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/EXACT_DERIVATION.md",
    "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/AUDIT_REPORT.md",
    "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/EXACT_DERIVATION.md",
    "udt_g182_completed_pair_two_sided_carry_classification_2026-08-19/AUDIT_REPORT.md",
    "udt_g182_completed_pair_two_sided_carry_classification_2026-08-19/EXACT_DERIVATION.md",
    "udt_g220_covariant_null_clock_arrow_timelive_lift_2026-08-22/EXACT_DERIVATION.md",
]
with (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").open() as handle:
    rows = list(csv.reader(handle, delimiter="\t"))
selected = [row for row in rows[1:] if row[0] in {"G89", "G176", "G179", "G182", "G220"}]
if len(selected) != 5:
    raise ValueError("Expected exactly the five consulted scientific registry rows")
with (HERE / "FROZEN_SOURCE_ROWS.tsv").open("w") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerows([rows[0], *selected])


def manifest(entries, output):
    with output.open("w") as handle:
        handle.write("path\tbytes\tsha256\n")
        for path in entries:
            payload = path.read_bytes()
            handle.write(f"{path.relative_to(ROOT)}\t{len(payload)}\t{hashlib.sha256(payload).hexdigest()}\n")


manifest([ROOT / name for name in paths], HERE / "SOURCE_MANIFEST.tsv")
artifact_files = [path for path in sorted(HERE.iterdir())
                  if path.is_file() and path.name != "ARTIFACT_MANIFEST.tsv"]
manifest(artifact_files, HERE / "ARTIFACT_MANIFEST.tsv")
print(json.dumps({"source_count": len(paths), "selected_registry_rows": len(selected),
                  "artifact_count": len(artifact_files),
                  "meaning": "Byte correspondence only; not truth, independence or chronology"}))
