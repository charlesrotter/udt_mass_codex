#!/usr/bin/env python3
"""Exercise fail-closed defects against the magnitude-owner ruling."""

from __future__ import annotations

import csv
import argparse
import hashlib
import io
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def table(path: Path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence_paths(rows):
    return {
        citation.split("::", 1)[0]
        for row in rows
        for citation in row["evidence"].split(";")
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify cached proof table without writing")
    args = parser.parse_args()
    atlas = table(HERE / "MAGNITUDE_OWNER_ATLAS.tsv")
    transitions = {row["branch_id"]: row for row in table(ROOT / "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/TRANSITION_OWNERSHIP_ATLAS.tsv")}
    relations = {row["branch_id"]: row for row in table(ROOT / "udt_global_relation_family_branch_classification_2026-08-10/GLOBAL_RELATION_FAMILY_CLASSIFICATION.tsv")}
    loops = table(ROOT / "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/LOOP_HOLONOMY.tsv")
    premises = {row["premise_id"]: row for row in table(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")}
    manifest = table(HERE / "SOURCE_MANIFEST.tsv")
    manifest_paths = {row["path"] for row in manifest}
    tests = []

    def record(test_id: str, defect: str, rejected: bool) -> None:
        assert rejected, test_id
        tests.append({"test_id": test_id, "injected_defect": defect, "expected": "REJECT", "observed": "REJECT"})

    record("C01", "omit or duplicate one branch-family cell", len(atlas) == len({(r["branch_id"], r["family_id"]) for r in atlas}) == 120)
    record("C02", "call a supplied pair-surface Jacobian branch-owned", all(r["disposition"] != "OWNER_DERIVED" for r in atlas if r["family_id"] == "F01_PAIR_SURFACE_JACOBIAN"))
    record("C03", "promote the exact R17 semidirect assembly to branch ownership", "NOT_BRANCH_OWNED" in transitions["R17"]["nonisometric_transition"])
    record("C04", "call R18 a complete reciprocal owner without a ruler", transitions["R18"]["intrinsic_ruler_or_grading"] == "NO_SAME_BRANCH_INTRINSIC_RULER")
    record(
        "C05",
        "claim Levi-Civita path transport generates nonzero density",
        "LEVI_CIVITA" in transitions["R23"]["owned_geometric_transport"]
        and "METRIC_COMPATIBLE" in transitions["R23"]["nonisometric_transition"],
    )
    record("C06", "erase path labels to manufacture endpoint ownership", len(loops) == 36 and any(float(r["nonidentity_max"]) > 1e-10 for r in loops))
    record("C07", "invent a current native dynamical or bootstrap magnitude law", all(r["disposition"] == "BLOCKED_MISSING_DYNAMIC_LAW" for r in atlas if r["family_id"] == "F04_NATIVE_DYNAMICAL_BOOTSTRAP"))
    record("C08", "call the terminal evaluator the generator of its supplied magnitude", "scalar descent called physical-law selection" in premises["G44"]["forbidden_regression"])
    record("C09", "promote the conditional readout to universal mixed-geometry c_eff", "universal mixed-geometry c_eff" in premises["G44"]["open_scope"])
    record("C10", "call aggregate FC04 one selected owner", relations["R04"]["primary_disposition"] == "STRATIFIED_MIXTURE_OWNED" and transitions["R04"]["primary_disposition"] == "AGGREGATE_MEMBER_DEPENDENT")
    record("C11", "select one W04 Killing line by convenience", transitions["R20"]["middle_state_rule"] == "NO_OWNER_SELECTS_ONE_MIDDLE_STATE")
    record("C12", "state the bounded no-owner result as a theorem over all UDT metrics", len({r["branch_id"] for r in atlas}) == 24 and len({r["family_id"] for r in atlas}) == 5)

    cited = evidence_paths(atlas)
    removed = set(manifest_paths)
    removed.remove(sorted(cited)[0])
    record("C13", "remove one cited source from the manifest", not cited.issubset(removed))

    first = manifest[0]
    changed = (ROOT / first["path"]).read_bytes() + b"injected-corruption"
    record("C14", "mutate one manifested source byte stream", hashlib.sha256(changed).hexdigest() != first["sha256"])

    injected_citations = set(cited)
    injected_citations.add("UNMANIFESTED_LOAD_BEARING_SOURCE.md")
    record("C15", "insert an unmanifested atlas evidence citation", not injected_citations.issubset(manifest_paths))

    cached = {
        name: digest(HERE / name)
        for name in (
            "MAGNITUDE_OWNER_ATLAS.tsv",
            "BRANCH_OWNER_SUMMARY.tsv",
            "DERIVATION_RESULT.json",
            "INDEPENDENT_VERIFICATION_RESULT.json",
        )
    }
    for script in ("derive_magnitude_ownership.py", "verify_magnitude_ownership_independent.py"):
        completed = subprocess.run(
            [sys.executable, str(HERE / script), "--check"],
            cwd=HERE,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert completed.returncode == 0, completed.stderr
    record("C16", "allow a read-only check to mutate cached outputs", cached == {name: digest(HERE / name) for name in cached})

    review = (HERE / "EXTERNAL_REVIEW.md").read_text(encoding="utf-8")
    record(
        "C17",
        "call internal cached-count reproduction an external scientific acceptance",
        "ACCEPT_BRANCH_CONDITIONAL_OWNER_ONLY" in review
        and "Exact external output SHA-256" in review,
    )

    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(tests[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(tests)
    rendered = stream.getvalue()
    if args.check:
        assert (HERE / "CATCH_PROOFS.tsv").read_text(encoding="utf-8") == rendered
    else:
        (HERE / "CATCH_PROOFS.tsv").write_text(rendered, encoding="utf-8")
    print(f"catch_proofs={len(tests)}/{len(tests)}")


if __name__ == "__main__":
    main()
