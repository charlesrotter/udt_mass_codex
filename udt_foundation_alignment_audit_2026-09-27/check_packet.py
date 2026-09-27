"""Packet correspondence and preservation checks, not scientific certification."""
import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def table(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def check_rows(candidate, current, families):
    ids = [r["premise_id"] for r in candidate]
    expected = {r["premise_id"]: r for r in current}
    assert len(ids) == len(set(ids)) == len(expected), "ID count/uniqueness"
    assert set(ids) == set(expected), "ID membership"
    members = {}
    for family in families:
        group = family["premise_ids"].split(";")
        assert len(group) == int(family["count"]), "family count"
        for pid in group:
            assert pid not in members, "family overlap"
            members[pid] = family["family_id"]
    assert set(members) == set(expected), "family membership"
    for row in candidate:
        pid = row["premise_id"]
        assert all(row[k] == value for k, value in expected[pid].items()), "exact current field"
        assert row["editorial_family"] == members[pid], "family assignment"
        assert row["packet_read_depth"] in {
            "INHERITED_CWA1_DISPOSITION__NOT_NEW_PROOF_REVIEW",
            "CURRENT_BANKING_RECORD_READ__FULL_CANDIDATE_AND_RAW_EVIDENCE_NOT_REREVIEWED"}, "review depth"


def main():
    baseline = json.loads((HERE / "BASELINE.json").read_text())
    current = table(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    rows = table(HERE / "candidate/REGISTRY_COVERAGE.tsv")
    families = table(HERE / "candidate/FAMILY_ROUTING.tsv")
    check_rows(rows, current, families)
    caught = []
    mutants = []
    mutants.append(("dropped row", rows[:-1]))
    mutants.append(("duplicated row", rows + [rows[0]]))
    for key, value in [("epistemic_label", "PROMOTED_BY_AUDIT"),
                       ("open_scope", "CLOSED_BY_AUDIT"),
                       ("editorial_family", "F99"),
                       ("packet_read_depth", "ALL_PROOFS_REVIEWED")]:
        variant = copy.deepcopy(rows)
        variant[0][key] = value
        mutants.append(("changed " + key, variant))
    for name, mutant in mutants:
        try:
            check_rows(mutant, current, families)
        except AssertionError:
            caught.append(name)
        else:
            raise AssertionError("uncaught mutant: " + name)
    command = ["git", "status", "--porcelain=v1", "--untracked-files=all"]
    status = subprocess.check_output(command, cwd=ROOT, text=True).splitlines()
    outside = [line for line in status if line[3:].strip('"') != HERE.name
               and not line[3:].strip('"').startswith(HERE.name + "/")]
    assert sorted(outside) == sorted(baseline["preexisting_status_lines"]), "outside path/status preservation"
    for name, key in [("CURRENT_SCIENTIFIC_PREMISES.tsv", "registry_sha256"),
                      ("Mass creates gravity.txt", "lecture_sha256")]:
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == baseline[key], name
    pins = table(HERE / "SOURCE_READ_LEDGER.tsv")
    for pin in pins:
        path = Path(pin["path"])
        assert not path.is_absolute() and ".." not in path.parts
        assert path.parts[0] not in {
            "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
            "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
            "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
            "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02"}
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == pin["sha256"], str(path)
    result = dict(status="PASS", registry_rows=len(rows), exact_fields_per_row=len(current[0]),
                  editorial_families=len(families), negative_controls_rejected=caught,
                  source_pins=len(pins), outside_status_lines=len(outside),
                  preexisting_untracked_content_identity="NOT_CLAIMED; only authorized lecture hashed",
                  scientific_claim="NONE; correspondence and local preservation only")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
