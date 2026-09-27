#!/usr/bin/env python3
"""Independent metadata audit; no production classifier imports or payload reads."""
import collections
import copy
import csv
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "udt_repository_cleanup_2026-09-27"
OUT = Path(__file__).resolve().parent
BASE = "8aac11e13a2311347771e11f507f4f2042ea02a2"
PROTECTED = (
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/",
    "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/",
    "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/",
)
ALLOWED = {
    "EXCLUDE_PROTECTED", "RETAIN_MAINTAINED_NAVIGATION", "RETAIN_FOUNDATIONAL_SOURCE",
    "RETAIN_FIXED_ROOT_INTERFACE", "RETAIN_METHOD_AND_TESTS", "RETAIN_EXISTING_ARCHIVE",
    "RETAIN_REORGANIZATION_PROVENANCE", "RETAIN_ORGANIZED_EVIDENCE",
    "RETAIN_CODE_OR_CONFIGURATION", "RETAIN_ROOT_EVIDENCE_OR_DATA",
    "RETAIN_COHERENT_PACKAGE", "ARCHIVE_REVIEWED",
}

def table(name):
    with (PACKET / "inventory" / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))

def baseline():
    payload = subprocess.check_output(["git", "ls-tree", "-r", "--long", "-z", BASE], cwd=ROOT)
    result = {}
    for record in payload.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, kind, oid, size = meta.decode().split()
        assert kind == "blob"
        result[path.decode()] = (mode, oid, size)
    return result

def validate(rows, root_rows, package_rows, expected):
    paths = [row["path"] for row in rows]
    assert len(paths) == len(set(paths)), "duplicate inventory path"
    assert set(paths) == set(expected), "exact baseline path membership"
    destinations = set()
    for row in rows:
        path = row["path"]
        assert (row["mode"], row["object_id"], row["bytes"]) == expected[path], "baseline metadata drift"
        assert row["disposition"] in ALLOWED, "unknown disposition"
        assert all(row.get(key) for key in ("reason_id", "read_depth", "review_reference", "destination")), "missing disposition basis"
        dest = PurePosixPath(row["destination"])
        assert not dest.is_absolute() and ".." not in dest.parts, "unsafe destination"
        assert row["destination"] not in destinations, "duplicate destination"
        destinations.add(row["destination"])
        if path.startswith(PROTECTED):
            assert row["disposition"] == "EXCLUDE_PROTECTED", "protected disposition"
            assert row["read_depth"] == "METADATA_ONLY_RETAIN_NO_SCIENTIFIC_REVIEW", "protected read depth"
        if row["disposition"] == "ARCHIVE_REVIEWED":
            assert row["destination"].startswith("archive/remaining_working_surfaces_2026-09-27/"), "archive prefix"
            assert row["destination"] not in expected, "baseline destination collision"
            assert row["read_depth"].startswith("FULL_CONTENT_REVIEW"), "archive review depth"
            refs = row["review_reference"].split(";")
            assert len(refs) >= 2 and len(refs) == len(set(refs)), "independent review references"
            assert all((ROOT / ref).is_file() for ref in refs), "review reference absent"
        else:
            assert row["destination"] == path, "retained destination moved"
    wanted_roots = [row for row in rows if "/" not in row["path"]]
    assert root_rows == wanted_roots, "root projection mismatch"
    counts = collections.defaultdict(collections.Counter)
    for row in rows:
        name = row["path"]
        group = name.split("/", 1)[0] if "/" in name else "(root)"
        counts[group][row["disposition"]] += 1
    observed = {row["group"]: row for row in package_rows}
    assert len(observed) == len(package_rows) and set(observed) == set(counts), "package membership mismatch"
    for name, group_counts in counts.items():
        row = observed[name]
        assert int(row["tracked_paths"]) == sum(group_counts.values()), "package count mismatch"
        assert json.loads(row["disposition_counts"]) == dict(group_counts), "package disposition mismatch"
    return {"tracked_paths": len(rows), "root_paths": len(root_rows), "groups": len(counts),
            "dispositions": dict(collections.Counter(row["disposition"] for row in rows))}

def main():
    expected = baseline()
    rows = table("TRACKED_DISPOSITIONS.tsv")
    roots = table("ROOT_DISPOSITIONS.tsv")
    groups = table("PACKAGE_DISPOSITIONS.tsv")
    result = validate(rows, roots, groups, expected)
    cases = {}

    def catch(name, mutate):
        copies = copy.deepcopy((rows, roots, groups))
        mutate(*copies)
        try:
            validate(*copies, expected)
        except (AssertionError, KeyError, ValueError) as error:
            cases[name] = {"status": "REJECTED", "reason": str(error)}
            return
        raise AssertionError("negative control falsely passed: " + name)

    catch("missing_path", lambda a, b, c: a.pop())
    catch("duplicate_path", lambda a, b, c: a.append(copy.deepcopy(a[0])))
    catch("same_count_path_substitution", lambda a, b, c: a[0].update(path="invented.txt"))
    for field, bad in (("mode", "100755"), ("object_id", "0" * 40), ("bytes", "-1")):
        catch("baseline_" + field + "_mutation", lambda a, b, c, f=field, v=bad: a[0].update({f: v}))
    catch("unknown_disposition", lambda a, b, c: a[0].update(disposition="ACCEPTED_PHYSICS"))
    catch("retained_path_moved", lambda a, b, c: a[0].update(destination="elsewhere.txt"))
    catch("destination_traversal", lambda a, b, c: a[0].update(destination="../escape.txt"))
    catch("destination_collision", lambda a, b, c: a[1].update(destination=a[0]["destination"]))
    protected_index = next(i for i, row in enumerate(rows) if row["path"].startswith(PROTECTED))
    catch("protected_override", lambda a, b, c: a[protected_index].update(disposition="RETAIN_COHERENT_PACKAGE"))
    catch("root_projection_omission", lambda a, b, c: b.pop())
    catch("package_count_mutation", lambda a, b, c: c[0].update(tracked_paths="0"))
    result.update(status="PASS", baseline=BASE, negative_controls=cases,
                  limitations="Independent exact metadata accounting and finite guard tests; does not prove scientific content review or dynamic dependency closure.",
                  inventory_sha256=hashlib.sha256((PACKET / "inventory/TRACKED_DISPOSITIONS.tsv").read_bytes()).hexdigest(),
                  builder_sha256=hashlib.sha256((PACKET / "build_inventory.py").read_bytes()).hexdigest())
    (OUT / "INDEPENDENT_INVENTORY_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
