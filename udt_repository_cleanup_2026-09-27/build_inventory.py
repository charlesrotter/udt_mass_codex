"""Maintenance dispositions of the exact baseline Git tree; no science regrading.

Reads Git path/object metadata, the old relocation table by known input paths,
and reviewed disposition overrides. Never opens protected/untracked payloads.
Default preservation is explicitly metadata-only, not a source/content audit.
"""
import collections
import csv
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKET = Path(__file__).resolve().parent
PROTECTED = (
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/",
    "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/",
    "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/",
)
CURRENT = set("AGENTS.md LIVE.md HANDOFF.md INDEX.md MEMORY.md README.md CLAUDE.md CURRENT_RESEARCH_PROGRAM.md CURRENT_SCIENTIFIC_PREMISES.md CURRENT_SCIENTIFIC_PREMISES.tsv UDT_RESEARCH_ROADMAP.md UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md research/README.md research/_registry/README.md".split())
FOUNDATION = set("CANON.md PROVENANCE.md founding.md UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md".split())
FIXED = set("CODEX_STARTUP_REHEARSAL_2026-07-17.md codex_rehearsal_final.md codex_rehearsal_transcript.txt STATE.md HANDOFF_ARCHIVE.md UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md UDT_SCIENTIFIC_FRONTIER_2026-07-19.md PURSUIT_CHARTER_2026-07-04.md UDT_ELEGANT_FRAME.md SIMPLE_METRIC_MACRO.md PROBLEM_STATEMENT.md CODEX_ZERO_CONTEXT_STARTUP_REHEARSAL_2026-07-19.md CODEX_ZERO_CONTEXT_STARTUP_REHEARSAL_PREREG_2026-07-19.md INFLIGHT_STATE.md".split())
METHOD = set("STRUCTURE_HYGIENE.md HYGIENE_HEADER_TEMPLATE.md CROSS_MODEL_VERIFY.md COGNITIVE_CORRAL_TRIGGERS_SETUP.md".split())
OVERRIDE_KEYS = {"path", "disposition", "reason_id", "read_depth", "destination", "review_reference"}
DISPOSITIONS = {"EXCLUDE_PROTECTED", "RETAIN_MAINTAINED_NAVIGATION", "RETAIN_FOUNDATIONAL_SOURCE",
                "RETAIN_FIXED_ROOT_INTERFACE", "RETAIN_METHOD_AND_TESTS", "RETAIN_EXISTING_ARCHIVE",
                "RETAIN_REORGANIZATION_PROVENANCE", "RETAIN_ORGANIZED_EVIDENCE",
                "RETAIN_CODE_OR_CONFIGURATION", "RETAIN_ROOT_EVIDENCE_OR_DATA",
                "RETAIN_COHERENT_PACKAGE", "RETAIN_REVIEWED_DEPENDENCY", "ARCHIVE_REVIEWED"}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def baseline_tree(commit):
    records = []
    for item in git("ls-tree", "-r", "-l", "-z", commit).decode().split("\0"):
        if not item:
            continue
        meta, name = item.split("\t", 1)
        mode, kind, oid, size = meta.split()
        records.append(dict(path=name, mode=mode, object_id=oid, bytes=size))
    assert len(records) == len({r["path"] for r in records}), "duplicate Git path"
    return records


def default_disposition(name):
    if name.startswith(PROTECTED):
        return "EXCLUDE_PROTECTED", "P01"
    if name in CURRENT:
        return "RETAIN_MAINTAINED_NAVIGATION", "C01"
    if name in FOUNDATION:
        return "RETAIN_FOUNDATIONAL_SOURCE", "C02"
    if name in FIXED:
        return "RETAIN_FIXED_ROOT_INTERFACE", "C03"
    if name in METHOD or name.startswith((".claude/", "tests/")):
        return "RETAIN_METHOD_AND_TESTS", "C04"
    if name.startswith("archive/"):
        return "RETAIN_EXISTING_ARCHIVE", "H01"
    if name.startswith(("research/_registry/", "reorganization_")):
        return "RETAIN_REORGANIZATION_PROVENANCE", "H02"
    if name.startswith("research/"):
        return "RETAIN_ORGANIZED_EVIDENCE", "E01"
    if "/" not in name:
        if Path(name).suffix.lower() in (".py", ".sh", ".toml", ".ini", ".cfg") or name.startswith("."):
            return "RETAIN_CODE_OR_CONFIGURATION", "E02"
        return "RETAIN_ROOT_EVIDENCE_OR_DATA", "E03"
    return "RETAIN_COHERENT_PACKAGE", "E04"


def build():
    baseline = json.loads((PACKET / "BASELINE.json").read_text())
    records = baseline_tree(baseline["HEAD"])
    names = {r["path"] for r in records}
    # A set of known baseline names is the lookup input, never a frontier dump.
    old = {}
    with (ROOT / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv").open() as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["original_path"] in names:
                old[row["original_path"]] = row
    override_file = PACKET / "inventory/REVIEWED_OVERRIDES.tsv"
    overrides = {}
    if override_file.exists():
        with override_file.open() as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            assert set(reader.fieldnames) == OVERRIDE_KEYS, "override fields may not replace immutable Git metadata"
            destinations = set()
            for row in reader:
                assert row["path"] in names and row["path"] not in overrides
                assert not row["path"].startswith(PROTECTED), "protected override"
                assert row["path"] not in CURRENT | FOUNDATION | FIXED | METHOD, "protected interface override"
                assert row["review_reference"] and row["read_depth"]
                assert row["disposition"] in DISPOSITIONS, "unknown disposition"
                dest = row["destination"]
                assert dest and dest not in destinations, "missing or duplicate destination"
                assert not Path(dest).is_absolute() and ".." not in Path(dest).parts, "unsafe destination"
                if row["disposition"] == "ARCHIVE_REVIEWED":
                    assert dest.startswith("archive/remaining_working_surfaces_2026-09-27/"), "archive destination required"
                    assert dest not in names, "archive destination collides with baseline"
                    assert row["read_depth"].startswith("FULL_CONTENT_REVIEW"), "archive requires full content review"
                    refs = row["review_reference"].split(";")
                    assert len(refs) >= 2 and len(set(refs)) == len(refs), "archive requires distinct review references"
                    assert all((ROOT / ref).is_file() for ref in refs), "missing review reference"
                else:
                    assert dest == row["path"], "retained destination must stay fixed"
                destinations.add(dest)
                overrides[row["path"]] = row
    fields = ["path", "mode", "object_id", "bytes", "disposition", "reason_id", "read_depth", "destination", "old_ledger_status", "review_reference"]
    totals = collections.Counter()
    groups = collections.defaultdict(collections.Counter)
    for row in records:
        name = row["path"]
        disposition, reason = default_disposition(name)
        row.update(disposition=disposition, reason_id=reason,
                   read_depth="METADATA_ONLY_RETAIN_NO_SCIENTIFIC_REVIEW",
                   destination=name, old_ledger_status=old.get(name, {}).get("path_status", "NOT_IN_OLD_SNAPSHOT"),
                   review_reference="inventory/DISPOSITION_RULES.md")
        if name in overrides:
            row.update({k: v for k, v in overrides[name].items() if k in OVERRIDE_KEYS and k != "path"})
        totals[row["disposition"]] += 1
        groups[name.split("/")[0] if "/" in name else "(root)"][row["disposition"]] += 1
    out = PACKET / "inventory"
    for filename, selected in (("TRACKED_DISPOSITIONS.tsv", records), ("ROOT_DISPOSITIONS.tsv", [r for r in records if "/" not in r["path"]])):
        with (out / filename).open("w") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
            writer.writeheader(); writer.writerows(selected)
    with (out / "PACKAGE_DISPOSITIONS.tsv").open("w") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["group", "tracked_paths", "disposition_counts"])
        for name, counts in sorted(groups.items()):
            writer.writerow([name, sum(counts.values()), json.dumps(dict(sorted(counts.items())), sort_keys=True)])
    summary = dict(baseline=baseline["HEAD"], tracked_paths=len(records),
                   root_paths=sum("/" not in r["path"] for r in records), groups=len(groups),
                   dispositions=dict(sorted(totals.items())), reviewed_overrides=len(overrides),
                   scope="Exact baseline metadata census plus individually reviewed overrides; not content/proof review of every file or a complete dynamic dependency graph.")
    (out / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    build()
