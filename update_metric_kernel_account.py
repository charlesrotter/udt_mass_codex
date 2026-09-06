#!/usr/bin/env python3
"""Generate/check the metric-kernel manuscript coverage sidecar.

The scientific registry remains the only status owner. This file stores editorial roles,
manuscript locations, current and last-reviewed controlling-source hashes, and an intentionally
bounded dependency map. Ordinary regeneration preserves the last-reviewed hash and invalidates
changed rows plus descendants. Only an explicit review record tied to the new source bytes can
advance that binding. A missing dependency entry means not recorded here, never independence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv"
SIDECAR = ROOT / "UDT_METRIC_KERNEL_COVERAGE.tsv"
SCIENTIFIC_SNAPSHOT = "f23199e4a47aaf83acb9ea7d1ad382cd814159c2"
REGISTRY_SHA256 = "3743533cfe1cc6a047e11cf182d90561c100727fc506aca3c5ff7a33779b2c3f"
REVIEWED_MANUSCRIPT_VERSION = "FIRST_COMPLETE_EDITION_2026-09-05"
REVIEWED_MANUSCRIPT_SHA256 = "3b625d8f43620a37c99d9f4f0fdc9390c3a12306b1da87281c143ce84d40a81e"


ROLE_IDS = {
    "MAIN_ARGUMENT": """G01 G02 G129 G130 G134 G135 G137 G145 G166 G167 G176 G179 G180 G188 G201 G204 G205 G211 G213 G215 G216 G220 G221 G222 G226 G227 G229 G231 G244 G245 G246 G247 G250 G252 G269 G270 G272 G274 G275 G276 G282 G293 G295 G296 G301 G310 G311 G312 G313 G315 G316 G319 G321 G322 G324 G333 G334 G335 G336 G337 G350 G351 G352 W5 W6""".split(),
    "SUPPORTING_LEMMA": """G05 G06 G07 G19 G24 G28 G35 G37 G39 G40 G43 G44 G46 G47 G48 G49 G51 G53 G54 G57 G58 G59 G60 G62 G64 G87 G89 G107 G108 G109 G110 G114 G115 G116 G119 G123 G124 G127 G128 G133 G138 G139 G141 G142 G143 G144 G147 G148 G149 G151 G152 G153 G156 G157 G158 G159 G160 G161 G168 G169 G170 G172 G173 G174 G175 G182 G184 G186 G187 G199 G200 G206 G207 G208 G209 G210 G214 G217 G219 G223 G224 G225 G228 G230 G248 G260 G263 G266 G268 G271 G288 G290 G292 G294 G303 G304 G305 G306 G307 G308 G317 G318 G323 G325 G326 G327 G328 G329 G330 G331 G332 G338 G339 G340 G341 G342 G343 G344 G345 G346 G347 G348 G349""".split(),
    "BOUNDARY_RESULT": """G04 G08 G11 G12 G14 G16 G20 G21 G22 G23 G25 G26 G27 G36 G38 G41 G42 G45 G50 G52 G55 G56 G61 G63 G90 G94 G95 G96 G98 G113 G121 G122 G126 G131 G132 G136 G146 G150 G154 G155 G162 G163 G165 G181 G183 G202 G203 G233 G235 G249 G251 G254 G256 G259 G261 G262 G264 G265 G267 G273 G277 G280 G281 G283 G284 G285 G286 G287 G289 G297 G298 G299 G300 G309 G314 G320""".split(),
    "CONTROL_ONLY": """G03 G65 G66 G74 G75 G77 G78 G79 G80 G81 G82 G91 G92 G93 G97 G99 G101 G102 G103 G104 G105 G106 G111 G112 G117 G118 G120 G125 G140 G177 G178 G189 G190 G191 G192 G193 G194 G195 G196 G198 G212 G218 G234 G236 G237 G238 G239 G240 G241 G242 G243 G253 G255 G257 G258 G278 G279""".split(),
    "OUTSIDE_SCOPE": "G09 G10 G13 G15 G17 G18 G29 G30 G31 G32 G33 G34".split(),
    "SUPERSEDED_HISTORICAL": "G76 G171".split(),
}


DEPENDENCIES = {
    "G02": ["G01"], "G130": ["G129"], "G134": ["G129"], "G137": ["G135"],
    "G145": ["G129", "G137"], "G166": ["G01", "G02"], "G167": ["G166"],
    "G176": ["G167"], "G179": ["G176"], "G180": ["G179"], "G188": ["G179"],
    "G215": ["G176", "G171"], "G216": ["G215"], "G220": ["G216"],
    "G221": ["G220"], "G222": ["G221", "G188"], "G226": ["G188", "G222"],
    "G227": ["G226"], "G229": ["G227", "G228"],
    "G231": ["G227", "G228", "G229", "G230"], "G244": ["G188"],
    "G245": ["G244"], "G246": ["G220", "G222", "G245"],
    "G247": ["G246", "G226"], "G250": ["G249"], "G252": ["G249", "G250"],
    "G269": ["G268"], "G270": ["G269", "G176"], "G272": ["G269"],
    "G274": ["G272"], "G275": ["W5", "G274"], "G276": ["G275", "G252"],
    "G277": ["G276"], "G278": ["G277"], "G279": ["G278"],
    "G280": ["W5", "G188"], "G281": ["G277", "G278", "G279", "G280"],
    "G282": ["G176", "G188"], "G295": ["W6", "G293"],
    "G296": ["G286", "G295"], "G301": ["G296"], "G310": ["G301"],
    "G311": ["G310"], "G312": ["G301", "G311"], "G313": ["G312"],
    "G314": ["G313"], "G315": ["G313"], "G316": ["G315"],
    "G317": ["G316"], "G318": ["G317"], "G319": ["G318"],
    "G320": ["G319"], "G321": ["G320"], "G322": ["G321"],
    "G323": ["G320", "G322"], "G324": ["G323", "G322"],
    "G325": ["G324"], "G326": ["G324"], "G327": ["G324"],
    "G328": ["G324"], "G329": ["G324"], "G330": ["G313"],
    "G331": ["G330"], "G332": ["G331", "G315", "G316"],
    "G333": ["G332", "G176"], "G334": ["G333"], "G335": ["G334"],
    "G336": ["G335"], "G337": ["G336"], "G338": ["G324", "G176"],
    "G339": ["G338"], "G340": ["G324", "G176"], "G341": ["G340"],
    "G342": ["G341"], "G343": ["G342"], "G344": ["G343"],
    "G345": ["G340", "G344"], "G346": ["G342", "G345"],
    "G347": ["G346"], "G348": ["G343", "G346", "G347"],
    "G349": ["G348"], "G350": ["G348", "G349"], "G351": ["G350"],
    "G352": ["G351", "G350"],
}


ROLE_NOTES = {
    "MAIN_ARGUMENT": "Body-level construction or response/readout obligation; exact source limits retained.",
    "SUPPORTING_LEMMA": "Supporting typing, covariance, existence, or witness material consolidated by dependency.",
    "BOUNDARY_RESULT": "Accepted nonselection, limitation, or open-interface result retained against overclaim.",
    "CONTROL_ONLY": "Regression, comparison, provenance, or empirical control; not a construction input.",
    "OUTSIDE_SCOPE": "Accepted row belongs to a carrier/action/finite-cell/CMB/micro branch outside this edition.",
    "SUPERSEDED_HISTORICAL": "Explicit historical or reclassified row retained for provenance, not current construction.",
}


FIELDS = [
    "premise_id", "role", "manuscript_anchor", "documentation_status",
    "scientific_snapshot", "controlling_source", "source_sha256",
    "reviewed_source_sha256", "source_review_id", "source_section",
    "upstream_ids", "dependency_type", "claim_polarity", "scope_note",
    "reviewed_manuscript_version",
]

SOURCE_CHANGED_STATUS = "SOURCE_CHANGED__FIDELITY_REVIEW_REQUIRED"
UPSTREAM_CHANGED_STATUS = "UPSTREAM_SOURCE_CHANGED__DEPENDENCY_REVIEW_REQUIRED"
SOURCE_REVIEW_SCHEMA = "udt-metric-kernel-source-review-1.0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def role_map() -> dict[str, str]:
    result: dict[str, str] = {}
    for role, ids in ROLE_IDS.items():
        for premise_id in ids:
            if premise_id in result:
                raise ValueError(f"duplicate disposition: {premise_id}")
            result[premise_id] = role
    return result


BODY_ANCHORS = {
    "G01": "Sections 2-3",
    "G02": "Sections 2-3",
    "W5": "Section 4.10",
    "W6": "Sections 4.10 and 5.1",
    **{f"G{number}": "Section 4.9" for number in range(129, 146)},
    **{f"G{number}": "Section 4" for number in (166, 167, 176, 177, 178, 179, 180)},
    "G188": "Section 4.10",
    **{f"G{number}": "Section 4.11" for number in (201, 204, 205)},
    **{f"G{number}": "Section 4.9" for number in range(211, 217)},
    **{
        f"G{number}": "Section 4.10"
        for number in (217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231)
    },
    **{f"G{number}": "Section 8.5" for number in (236, 237)},
    **{f"G{number}": "Section 4.10" for number in range(244, 253)},
    "G269": "Sections 4.10 and 6.2",
    **{f"G{number}": "Section 4.10" for number in range(270, 277)},
    **{f"G{number}": "Section 8" for number in range(277, 282)},
    "G282": "Section 5.1",
    "G293": "Section 5.1",
    "G295": "Section 5.1",
    "G296": "Section 5.1",
    "G298": "Section 6.2",
    "G301": "Section 5.2",
    "G310": "Section 5.3",
    "G311": "Section 5.3",
    "G312": "Section 5.4",
    **{f"G{number}": "Section 5.5" for number in range(313, 315)},
    **{f"G{number}": "Section 5.6" for number in range(315, 317)},
    **{f"G{number}": "Section 5.7" for number in range(317, 321)},
    **{f"G{number}": "Section 5.8" for number in range(321, 325)},
    **{f"G{number}": "Section 5.9" for number in range(325, 330)},
    **{f"G{number}": "Section 5.10" for number in range(330, 338)},
    **{f"G{number}": "Section 6" for number in range(338, 350)},
    **{f"G{number}": "Section 7" for number in range(350, 353)},
}


def anchor_for(premise_id: str) -> str:
    """Return a curated body anchor; unmapped rows are dispositioned in Appendix A."""
    return BODY_ANCHORS.get(premise_id, "Appendix A")


def documentation_status(role: str, anchor: str) -> str:
    if anchor != "Appendix A":
        return "FIDELITY_REVIEWED"
    if role in {"OUTSIDE_SCOPE", "SUPERSEDED_HISTORICAL"}:
        return "DISPOSITION_RECORDED"
    return "CONSOLIDATED_IN_COVERAGE_MAP"


def claim_polarity(role: str) -> str:
    return {
        "MAIN_ARGUMENT": "POSITIVE_OR_CONDITIONAL",
        "SUPPORTING_LEMMA": "POSITIVE_OR_CONDITIONAL",
        "BOUNDARY_RESULT": "NEGATIVE_OR_LIMIT",
        "CONTROL_ONLY": "CONTROL",
        "OUTSIDE_SCOPE": "NONE",
        "SUPERSEDED_HISTORICAL": "HISTORICAL",
    }[role]


def registry_rows() -> list[dict[str, str]]:
    if sha256(REGISTRY) != REGISTRY_SHA256:
        raise ValueError("registry bytes differ from the fixed scientific snapshot")
    with REGISTRY.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sidecar_rows() -> list[dict[str, str]]:
    if not SIDECAR.is_file():
        raise ValueError("coverage sidecar missing; reviewed source bindings cannot be inferred")
    with SIDECAR.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _previous_bindings(previous_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    bindings: dict[str, dict[str, str]] = {}
    for row in previous_rows:
        premise_id = row["premise_id"]
        reviewed_hash = row.get("reviewed_source_sha256") or row.get("source_sha256")
        review_id = row.get("source_review_id") or row.get("reviewed_manuscript_version")
        if not reviewed_hash or not review_id:
            raise ValueError(f"missing reviewed-source binding: {premise_id}")
        bindings[premise_id] = {
            "reviewed_source_sha256": reviewed_hash,
            "source_review_id": review_id,
        }
    return bindings


def _validate_review_record(
    review_record: dict[str, object],
    output: list[dict[str, str]],
    changed_ids: set[str],
    affected_ids: set[str],
) -> tuple[str, set[str]]:
    if review_record.get("schema") != SOURCE_REVIEW_SCHEMA:
        raise ValueError("source review record schema mismatch")
    review_id = review_record.get("review_id")
    if not isinstance(review_id, str) or not review_id.strip():
        raise ValueError("source review record needs a nonempty review_id")
    if review_record.get("scientific_snapshot") != SCIENTIFIC_SNAPSHOT:
        raise ValueError("source review record scientific snapshot mismatch")
    manuscript_hash = sha256(ROOT / "UDT_METRIC_KERNEL_DEVELOPMENT.md")
    if review_record.get("manuscript_sha256") != manuscript_hash:
        raise ValueError("source review record is not tied to the current manuscript bytes")
    if manuscript_hash != REVIEWED_MANUSCRIPT_SHA256:
        raise ValueError("fixed-snapshot manuscript changed; source review cannot rebind it")
    sources = review_record.get("sources")
    if not isinstance(sources, dict) or not sources:
        raise ValueError("source review record needs exact changed-source hashes")
    expected_sources = {
        row["controlling_source"]: row["source_sha256"]
        for row in output
        if row["premise_id"] in changed_ids
    }
    if sources != expected_sources:
        raise ValueError("source review record does not match every changed source version")
    covered = review_record.get("covered_premise_ids")
    if not isinstance(covered, list) or not all(isinstance(item, str) for item in covered):
        raise ValueError("source review record needs covered_premise_ids")
    covered_ids = set(covered)
    if covered_ids != affected_ids:
        raise ValueError("source review must cover exactly the changed rows and their descendants")
    return review_id, covered_ids


def build_rows(
    previous_rows: list[dict[str, str]] | None = None,
    review_record: dict[str, object] | None = None,
) -> list[dict[str, str]]:
    roles = role_map()
    rows = registry_rows()
    if previous_rows is None:
        previous_rows = sidecar_rows()
    bindings = _previous_bindings(previous_rows)
    registry_ids = {row["premise_id"] for row in rows}
    if set(roles) != registry_ids:
        raise ValueError(
            f"disposition mismatch: missing={sorted(registry_ids-set(roles))}, "
            f"extra={sorted(set(roles)-registry_ids)}"
        )
    if set(bindings) != registry_ids:
        raise ValueError("coverage sidecar reviewed-source bindings do not match the registry")
    output = []
    for row in rows:
        premise_id = row["premise_id"]
        role = roles[premise_id]
        source = ROOT / row["controlling_source"]
        if not source.is_file():
            raise ValueError(f"controlling source missing: {row['controlling_source']}")
        upstream = DEPENDENCIES.get(premise_id, [])
        binding = bindings[premise_id]
        output.append(
            {
                "premise_id": premise_id,
                "role": role,
                "manuscript_anchor": anchor_for(premise_id),
                "documentation_status": documentation_status(role, anchor_for(premise_id)),
                "scientific_snapshot": SCIENTIFIC_SNAPSHOT,
                "controlling_source": row["controlling_source"],
                "source_sha256": sha256(source),
                "reviewed_source_sha256": binding["reviewed_source_sha256"],
                "source_review_id": binding["source_review_id"],
                "source_section": "Registry controlling source; exact hypotheses remain source-owned",
                "upstream_ids": ";".join(upstream),
                "dependency_type": "SCIENTIFIC" if upstream else "NOT_RECORDED_IN_CENTRAL_MAP",
                "claim_polarity": claim_polarity(role),
                "scope_note": ROLE_NOTES[role],
                "reviewed_manuscript_version": REVIEWED_MANUSCRIPT_VERSION,
            }
        )

    changed_ids = {
        row["premise_id"]
        for row in output
        if row["source_sha256"] != row["reviewed_source_sha256"]
    }
    affected_ids = descendants(output, changed_ids)
    if review_record is not None:
        if not changed_ids:
            raise ValueError("no changed source version is awaiting review")
        review_id, covered_ids = _validate_review_record(
            review_record, output, changed_ids, affected_ids
        )
        for row in output:
            if row["premise_id"] in changed_ids:
                row["reviewed_source_sha256"] = row["source_sha256"]
            if row["premise_id"] in covered_ids:
                row["source_review_id"] = review_id
        changed_ids = set()
        affected_ids = set()

    for row in output:
        premise_id = row["premise_id"]
        if premise_id in changed_ids:
            row["documentation_status"] = SOURCE_CHANGED_STATUS
        elif premise_id in affected_ids:
            row["documentation_status"] = UPSTREAM_CHANGED_STATUS
    return output


def render(rows: list[dict[str, str]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def descendants(rows: list[dict[str, str]], changed_ids: set[str]) -> set[str]:
    downstream: dict[str, set[str]] = {}
    for row in rows:
        for upstream in filter(None, row.get("upstream_ids", "").split(";")):
            downstream.setdefault(upstream, set()).add(row["premise_id"])
    affected = set(changed_ids)
    frontier = list(changed_ids)
    while frontier:
        current = frontier.pop()
        for child in downstream.get(current, set()):
            if child not in affected:
                affected.add(child)
                frontier.append(child)
    return affected


def stale_after_source_changes(
    rows: list[dict[str, str]], current_source_hashes: dict[str, str]
) -> set[str]:
    changed = {
        row["premise_id"]
        for row in rows
        if current_source_hashes.get(row["premise_id"], row["source_sha256"])
        != row["source_sha256"]
    }
    return descendants(rows, changed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the generated sidecar")
    parser.add_argument(
        "--record-review",
        type=Path,
        help="write only after validating a review record tied to changed source bytes",
    )
    args = parser.parse_args()
    if args.write and args.record_review:
        parser.error("--write and --record-review are mutually exclusive")
    review_record = None
    if args.record_review:
        review_record = json.loads(args.record_review.read_text(encoding="utf-8"))
        if not isinstance(review_record, dict):
            raise ValueError("source review record must be a JSON object")
    rendered = render(build_rows(review_record=review_record))
    if args.write or args.record_review:
        SIDECAR.write_text(rendered, encoding="utf-8")
        print(f"WROTE {SIDECAR.name}")
        return 0
    if not SIDECAR.is_file() or SIDECAR.read_text(encoding="utf-8") != rendered:
        print("STALE UDT_METRIC_KERNEL_COVERAGE.tsv")
        return 1
    print("PASS metric-kernel coverage sidecar current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
