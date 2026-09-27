"""Snapshot adapter for the existing CWA1 coverage; no scientific regrading.

The old build/check programs encode 397 rows and their historical source snapshot.
Reuse their tables without rerunning or modifying those historical programs.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "candidate"
OLD = ROOT / "udt_accepted_work_consolidation_2026-09-12"


def read(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    current = read(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    old = read(OLD / "REGISTRY_COVERAGE.tsv")
    by_id = {r["premise_id"]: r for r in old}
    assert len(current) == 406 and len(old) == 397
    assert len({r["premise_id"] for r in current}) == 406 and len(by_id) == 397
    pairs = [("term", "term"), ("epistemic_label", "epistemic_label_exact"),
             ("active_use", "active_use_exact"), ("controlling_source", "controlling_source_exact")]
    added, changed, rows = [], [], []
    for r in current:
        pid = r["premise_id"]
        if pid in by_id:
            prior = by_id[pid]
            for now_key, old_key in pairs:
                if r[now_key] != prior[old_key]:
                    changed.append([pid, now_key])
            family = prior["family_id"]
            depth = "INHERITED_CWA1_DISPOSITION__NOT_NEW_PROOF_REVIEW"
            inherited = prior["inspection_disposition"]
        else:
            added.append(pid)
            family = "F23"
            depth = "CURRENT_BANKING_RECORD_READ__FULL_CANDIDATE_AND_RAW_EVIDENCE_NOT_REREVIEWED"
            inherited = "NOT_IN_CWA1"
        rows.append(dict(r, editorial_family=family, packet_read_depth=depth,
                         inherited_inspection_disposition=inherited))
    removed = sorted(set(by_id) - {r["premise_id"] for r in current})
    assert not removed and not changed
    assert set(added) == {f"G{i}" for i in range(415, 424)}
    write(OUT / "REGISTRY_COVERAGE.tsv", rows)
    routing = {
        "F01": "Foundation ownership; separate the carrier/action lane before any detailed use",
        "F02": "Angular comparison controls; do not select native profiles",
        "F03": "Prior pair/empirical controls; protected payloads excluded",
        "F04": "Relation-to-metric and scale typing; reused when testing physical assignment",
        "F05": "Core completed-pair construction and normalization controls",
        "F06": "Clock/direction/null/screen attachment and reconstruction",
        "F07": "Directed/mutual clocks, projective position, angular/GR limits and scale",
        "F08": "Observation provenance and imported-transfer limits",
        "F09": "History/co-presence/causality; W5/W6 later authority retained",
        "F10": "Native response-class membership gap; GR filter overlay essential",
        "F11": "Conditional geometry/development arena; reuse only with supplied-data hypotheses",
        "F12": "Optical geometry and area attachment; no physical transfer identity",
        "F13": "Provisional measure/clock readouts and nonselection boundaries",
        "F14": "Conditional phase/recipe constraints; physical content not selected",
        "F15": "Optional source branch PAUSED; not an automatic foundations dependency",
        "F16": "Conformal compatibility limits; no selected absolute scale",
        "F17": "Line-fibre and tidal controls; topology/mass entry authorities required for that lane",
        "F18": "Conditional nonlinear geometry, not a native selected universe",
        "F19": "Response/correspondence gap and tested limits",
        "F20": "Directional-clock and kernel interfaces",
        "F21": "Measurement design/benchmark controls; physical eligibility remains separate",
        "F22": "Initial evolution and retained-density distinctions",
        "F23": "Conditional whole-event signal chain; possible reuse for linked observables",
    }
    families = read(OLD / "FAMILY_MAP.tsv")
    families.append(dict(family_id="F23", count="9", premise_ids=";".join(sorted(added)),
                         topic="Conditional signal-chain additions G415–G423",
                         retained_gain="Conditional clock, duration, direction, area and benchmark joins",
                         scope_limit="Supplied geometry/query/protocol; no native physical identification or field law",
                         account_sections="NOT_IN_OLD_ACCOUNT",
                         inspection="Current banking-record scope only; not full proof/raw-evidence review"))
    for f in families:
        f["audit_relevance_editorial"] = routing[f["family_id"]]
        f["archive_disposition"] = "NOT_CLASSIFIED_FOR_RELOCATION"
    write(OUT / "FAMILY_ROUTING.tsv", families)
    summary = dict(current_count=len(current), inherited_count=len(old), added_ids=sorted(added),
                   removed_ids=removed, changed_in_four_compared_fields=changed,
                   compared_fields=[a for a, _ in pairs], family_count=len(families),
                   all_nine_current_fields_copied=True,
                   full_historical_row_byte_identity="NOT_TESTED_BY_THIS_FOUR_FIELD_COMPARISON",
                   source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in [ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv",
                                            OLD / "REGISTRY_COVERAGE.tsv", OLD / "FAMILY_MAP.tsv"]},
                   interpretation="Correspondence/coverage only; no new grades or blanket scientific review")
    (OUT / "COVERAGE_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("current_count", "inherited_count", "added_ids", "removed_ids", "changed_in_four_compared_fields", "family_count")}))


if __name__ == "__main__":
    main()
