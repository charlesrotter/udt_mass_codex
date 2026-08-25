#!/usr/bin/env python3
"""Extract source-native landing and ceiling sections for the G255 audit.

This is deliberately non-semantic: it selects named Markdown sections and does
not classify their scientific content.  Classification is performed against
CLASSIFICATION_CONTRACT.tsv after this extract is frozen.
"""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
SLOT_CENSUS = PKG / "SLOT_CENSUS.tsv"
OUT = PKG / "PRIMARY_CLAIM_EXTRACTS.tsv"

LANDING_KEYS = (
    "primary landing",
    "landing",
    "bounded landing",
    "current landing",
    "primary result",
    "result",
    "current grade",
    "consensus landing",
)

CEILING_FRAGMENTS = (
    "maximum conclusion",
    "ceiling",
    "what remains open",
    "what was not learned",
    "scope boundary",
    "exact boundary",
    "caveat",
    "scientific grade",
    "bounded scientific statement",
)


def sections(text: str) -> list[tuple[str, str]]:
    hits = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    result: list[tuple[str, str]] = []
    for i, hit in enumerate(hits):
        start = hit.end()
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        result.append((hit.group(1).strip(), text[start:end].strip()))
    return result


def compact(value: str) -> str:
    value = value.replace("\t", " ").replace("\r", "")
    return "\\n".join(line.rstrip() for line in value.splitlines()).strip()


def main() -> None:
    with SLOT_CENSUS.open(newline="", encoding="utf-8") as handle:
        slots = list(csv.DictReader(handle, delimiter="\t"))

    rows: list[dict[str, str]] = []
    for row in slots:
        report_rel = row["primary_report"]
        report = ROOT / report_rel
        raw = report.read_bytes()
        text = raw.decode("utf-8")
        parsed = sections(text)

        landing = ""
        landing_heading = ""
        for heading, body in parsed:
            lowered = heading.casefold()
            if any(lowered == key or lowered.startswith(f"{key} ") for key in LANDING_KEYS):
                landing_heading = heading
                landing = body
                break
        if not landing:
            raise RuntimeError(f"no landing/result section: {report_rel}")

        ceiling_parts = [
            f"[{heading}]\n{body}"
            for heading, body in parsed
            if any(fragment in heading.casefold() for fragment in CEILING_FRAGMENTS)
        ]
        rows.append(
            {
                "slot": row["slot"],
                "report": report_rel,
                "report_sha256": hashlib.sha256(raw).hexdigest(),
                "landing_heading": landing_heading,
                "landing_extract": compact(landing),
                "ceiling_extracts": compact("\n\n".join(ceiling_parts)) or "NONE",
            }
        )

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"{OUT}\t{len(rows)}")


if __name__ == "__main__":
    main()
