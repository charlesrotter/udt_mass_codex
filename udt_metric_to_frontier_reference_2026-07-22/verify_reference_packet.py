#!/usr/bin/env python3
"""Fail-closed verifier for the UDT metric-to-frontier reference packet."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


EXPECTED_STATUS = {
    "C001": "FOUNDING",
    "C002": "FOUNDING",
    "C003": "FOUNDING",
    "C004": "CANONIZED_BINDING_STATIC_SCOPE",
    "C005": "WORKING",
    "C010": "DERIVED",
    "C011": "DERIVED_CONDITIONAL",
    "C012": "CONDITIONAL",
    "C020": "UNIQUE_CONDITIONAL",
    "C021": "CONDITIONAL",
    "C022": "OPEN",
    "C030": "OBSERVED_BOUNDED",
    "C031": "OBSERVED_BOUNDED",
    "C032": "DERIVED_REGISTERED_GEOMETRIC_IDENTITY",
    "C033": "OBSERVED_BOUNDED",
    "C034": "OBSERVED_BOUNDED",
    "C040": "OBSERVED_BOUNDED_TAXONOMY",
    "C041": "OPEN_NOT_SELECTED",
    "C050": "EXACT_CONDITIONAL",
    "C051": "CONDITIONAL_DERIVED_FIBER",
    "C052": "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
    "C060": "UNIQUE_CONDITIONAL",
    "C061": "DERIVED_CONDITIONAL",
    "C070": "DERIVED_DIMENSIONAL_SCOPE",
    "C071": "DERIVED_CONDITIONAL",
    "C072": "OBSERVED_OR_EXTERNAL_ANCHOR",
    "C073": "OPEN_POTENTIAL_FUTURE_SELECTOR",
    "C080": "OPEN",
    "C090": "WORKING",
}


EXPECTED_JOIN_STATUS = {
    "J01": "OPEN",
    "J02": "OPEN",
    "J03": "WORKING_NEXT_QUESTION",
    "J04": "OPEN",
    "J05": "OPEN",
    "J06": "OPEN",
    "J07": "OPEN",
    "J08": "OPEN",
    "J09": "OPEN",
    "J10": "OPEN",
    "J11": "OPEN",
    "J12": "OPEN",
    "J13": "OPEN",
}


def validate_sources(source_rows: list[dict[str, str]]) -> None:
    require(len(source_rows) == 16, "source count")
    require(len({row["source_id"] for row in source_rows}) == 16, "source id uniqueness")
    require(len({row["path"] for row in source_rows}) == 16, "source path uniqueness")
    for row in source_rows:
        path = ROOT / row["path"]
        require(path.is_file(), f"missing source {row['path']}")
        require(digest(path) == row["sha256"], f"source hash {row['path']}")
        require(row["immutability_status"] in {"REFERENCE_PINNED_ROOT_SOURCE", "FROZEN_PACKAGE_SOURCE"}, "source status")
        if row["immutability_status"] == "FROZEN_PACKAGE_SOURCE":
            manifest = path.parent / "SHA256SUMS.txt"
            require(manifest.is_file(), f"missing source manifest {row['path']}")
            entries = {}
            for line in manifest.read_text(encoding="utf-8").splitlines():
                if not line:
                    continue
                hash_value, relative = line.split("  ", 1)
                entries[relative.lstrip("*").removeprefix("./")] = hash_value
            require(path.name in entries, f"source absent from manifest {row['path']}")
            require(entries[path.name] == row["sha256"], f"source manifest hash {row['path']}")


def validate_claims(claims: list[dict[str, str]], source_rows: list[dict[str, str]]) -> None:
    require(len(claims) == len(EXPECTED_STATUS), "claim count")
    require({row["claim_id"] for row in claims} == set(EXPECTED_STATUS), "claim identity coverage")
    require(len({row["claim_id"] for row in claims}) == len(claims), "duplicate claim")
    sources = {row["path"] for row in source_rows}
    for row in claims:
        require(row["status"] == EXPECTED_STATUS[row["claim_id"]], f"claim status {row['claim_id']}")
        evidence = row["evidence_source"]
        require(evidence in sources or evidence == f"{HERE.name}/REFERENCE.md", f"claim evidence {row['claim_id']}")
        require((ROOT / evidence).is_file(), f"claim evidence target {row['claim_id']}")
        require(bool(row["indispensable_premises"]), f"empty claim premises {row['claim_id']}")
        require(bool(row["remaining_open_scope"]), f"empty claim scope {row['claim_id']}")


def validate_joins(joins: list[dict[str, str]]) -> None:
    require(len(joins) == len(EXPECTED_JOIN_STATUS), "join count")
    require({row["join_id"] for row in joins} == set(EXPECTED_JOIN_STATUS), "join identity coverage")
    require(len({row["join_id"] for row in joins}) == len(joins), "duplicate join")
    for row in joins:
        require(row["status"] == EXPECTED_JOIN_STATUS[row["join_id"]], f"join status {row['join_id']}")
        require(bool(row["missing_object"]), f"missing join object {row['join_id']}")
        require(bool(row["prohibited_shortcut"]), f"missing shortcut guard {row['join_id']}")
        require(bool(row["bounded_next_test"]), f"missing next test {row['join_id']}")


def markdown_links() -> int:
    count = 0
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for source in (HERE / "REFERENCE.md", HERE / "EXTERNAL_REVIEW_PACKET.md", HERE / "PREREGISTRATION.md"):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.split("#", 1)[0]
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            require(source.parent.joinpath(target).resolve().exists(), f"broken link {source.name}:{target}")
            count += 1
    return count


def validate_reference(text: str) -> None:
    required = [
        "REFERENCE_DRAFT__EVIDENCE_LINKED__NO_NEW_PHYSICS",
        "GLOBAL_QUOTIENT_SELECTION_OPEN",
        "configuration-space subspaces; it is not physical time evolution",
        "orderly `phi` solo, not the full angular orchestra",
        "Neither result derives the carrier",
        "density is an output returned to the same fixed point",
        "This is `WORKING`, not evidence that such a structure exists",
        "Rediscovering only the universal Hodge split is a negative",
        "No item after the cold audit is authorized merely by this reference",
    ]
    for phrase in required:
        require(phrase in text, f"missing reference guard {phrase}")
    forbidden = [
        "NATIVE_CARRIER_EMERGENCE_DERIVED",
        "GLOBAL_QUOTIENT_SELECTED",
        "COMPLETE_NATIVE_ACTION_DERIVED",
        "DENSITY_NATIVE_SELECTOR_DERIVED",
    ]
    for phrase in forbidden:
        require(phrase not in text, f"forbidden promotion {phrase}")


def validate_navigation() -> int:
    required = {
        "LIVE.md": "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
        "HANDOFF.md": "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
        "INDEX.md": "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
        "README.md": "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
        "research/README.md": "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
        "AGENTS.md": "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
    }
    for path, pointer in required.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        require(pointer in text, f"navigation pointer {path}")
    live = (ROOT / "LIVE.md").read_text(encoding="utf-8")
    require(live.index("CURRENT STATE (2026-07-22") < live.index("CURRENT STATE (2026-07-20"), "LIVE current ordering")
    require("Four cold role-separated reviews of the synthesis are pending" in (ROOT / "HANDOFF.md").read_text(encoding="utf-8"), "handoff review status")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    require("Further repository reorganization is" in readme and "**PAUSED**" in readme, "reorganization pause")
    return len(required)


def run_catches(source_rows, claims, joins, reference_text) -> list[dict[str, str]]:
    catches: list[dict[str, str]] = []

    def exercise(catch_id, description, validator) -> None:
        caught = False
        try:
            validator()
        except AssertionError:
            caught = True
        require(caught, f"catch did not fire {catch_id}")
        catches.append({"catch_id": catch_id, "mutation": description, "result": "PASS_MUTATION_REJECTED"})

    bad_sources = deepcopy(source_rows)
    bad_sources[0]["sha256"] = "0" * 64
    exercise("C01", "corrupt one source hash", lambda: validate_sources(bad_sources))
    duplicate_claims = deepcopy(claims)
    duplicate_claims[-1]["claim_id"] = duplicate_claims[0]["claim_id"]
    exercise("C02", "duplicate a claim identity", lambda: validate_claims(duplicate_claims, source_rows))
    promoted_hopf = deepcopy(claims)
    next(row for row in promoted_hopf if row["claim_id"] == "C050")["status"] = "DERIVED"
    exercise("C03", "promote conditional Hopf compatibility", lambda: validate_claims(promoted_hopf, source_rows))
    promoted_particle = deepcopy(claims)
    next(row for row in promoted_particle if row["claim_id"] == "C052")["status"] = "SETTLED"
    exercise("C04", "erase particle premise scope", lambda: validate_claims(promoted_particle, source_rows))
    missing_evidence = deepcopy(claims)
    next(row for row in missing_evidence if row["claim_id"] == "C032")["evidence_source"] = "missing.md"
    exercise("C05", "remove transport evidence target", lambda: validate_claims(missing_evidence, source_rows))
    exercise("C06", "drop one open join", lambda: validate_joins(joins[:-1]))
    promoted_join = deepcopy(joins)
    next(row for row in promoted_join if row["join_id"] == "J05")["status"] = "DERIVED"
    exercise("C07", "promote quotient to carrier join", lambda: validate_joins(promoted_join))
    exercise("C08", "remove physical-time guard", lambda: validate_reference(reference_text.replace("configuration-space subspaces; it is not physical time evolution", "configuration-space subspaces")))
    exercise("C09", "remove universal-Hodge falsifier", lambda: validate_reference(reference_text.replace("Rediscovering only the universal Hodge split is a negative", "The universal Hodge split is sufficient")))
    exercise("C10", "promote density architecture", lambda: validate_reference(reference_text + "\nDENSITY_NATIVE_SELECTOR_DERIVED\n"))
    return catches


def main() -> None:
    source_rows = rows("SOURCE_MANIFEST.tsv")
    claims = rows("CLAIM_DEPENDENCY_LEDGER.tsv")
    joins = rows("OPEN_JOIN_LEDGER.tsv")
    reference_text = (HERE / "REFERENCE.md").read_text(encoding="utf-8")
    validate_sources(source_rows)
    validate_claims(claims, source_rows)
    validate_joins(joins)
    link_count = markdown_links()
    validate_reference(reference_text)
    navigation_files = validate_navigation()
    catches = run_catches(source_rows, claims, joins, reference_text)
    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    result = {
        "schema": "udt-metric-to-frontier-reference-verification-1.0",
        "status": "PASS_INTERNAL_REFERENCE_CONSISTENCY",
        "source_rows": len(source_rows),
        "claim_rows": len(claims),
        "open_join_rows": len(joins),
        "markdown_links": link_count,
        "navigation_files": navigation_files,
        "catch_proofs": len(catches),
        "external_reviews": "PENDING_AFTER_IMMUTABLE_REFERENCE_COMMIT",
        "scientific_changes": 0,
        "maximum_conclusion": "EVIDENCE_BACKED_SYNTHESIS_AND_RANKED_NEXT_QUESTIONS_ONLY",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
