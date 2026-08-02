#!/usr/bin/env python3
"""Extract content-based evidence from every frozen audit report.

This is a screening aid only.  It never assigns a scientific verdict from a
filename or from a keyword count; every potential object remains queued for
source-level adjudication.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
BASE = "156b8a57d2e4ce65a588e5f7c2d82d0bd1f88334"

FEATURES = {
    "rank1_object": re.compile(r"rank[- ]one|rank\s*1|eigenline|line projector", re.I),
    "projector": re.compile(r"\bprojector|\bprojection", re.I),
    "holonomy": re.compile(r"\bholonomy|parallel subbundle|preserved subspace", re.I),
    "dphi": re.compile(r"d\s*phi|dphi|\\mathrm\{d\}\\phi", re.I),
    "killing": re.compile(r"Killing (?:line|plane|field|vector)", re.I),
    "toric": re.compile(r"\btoric|torus action|circle action|dual systole", re.I),
    "involution": re.compile(r"\binvolution|fixed set|seam eigenspace", re.I),
    "spectral": re.compile(r"spectral projector|eigenbivector|simple eigenvalue|eigenspace", re.I),
    "global_completion": re.compile(r"complete (?:global|finite[- ]cell|branch|cell)|global (?:completion|descent|gluing)", re.I),
    "local_only": re.compile(r"local stratum|local or pointwise|bounded local|pointwise|local-only", re.I),
    "offshell": re.compile(r"off[- ]shell", re.I),
    "full_holonomy": re.compile(r"full (?:so\(1,3\)|Lorentz|six-dimensional holonomy|irreducible curvature)", re.I),
    "degeneracy": re.compile(r"degener|causal[- ]type change|null or zero|wall crossing", re.I),
    "global_open": re.compile(r"global (?:extension|completion|descent|closure).*OPEN|global .*remain[s]? open", re.I),
    "carrier_conditional": re.compile(r"carrier.*(?:POSIT|CONDITIONAL)|S\^?2.*(?:POSIT|CONDITIONAL)|carrier remains conditional", re.I),
}


def read_tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def frozen_blob(oid: str) -> str:
    out = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=ROOT)
    return out.decode("utf-8", "replace")


def clean(value: str, limit: int = 800) -> str:
    return " ".join(value.replace("\t", " ").split())[:limit]


def section_excerpt(text: str) -> str:
    lines = text.splitlines()
    starts = []
    for index, line in enumerate(lines):
        if re.match(r"^##+\s+(Result first|Result|Conclusion|Maximum conclusion|Ruling|Verdict)\b", line, re.I):
            starts.append(index + 1)
    start = starts[0] if starts else 0
    body = []
    for line in lines[start:]:
        if body and line.startswith("##"):
            break
        stripped = line.strip()
        if stripped and not stripped.startswith("```"):
            body.append(stripped)
        if len(" ".join(body)) >= 800:
            break
    return clean(" ".join(body))


def status_excerpt(text: str) -> str:
    for line in text.splitlines()[:30]:
        if re.search(r"\bStatus\s*:", line, re.I):
            return clean(line)
    return "NOT_EXPLICIT_IN_TOP_30_LINES"


def triage(features: dict[str, int]) -> str:
    object_signal = sum(features[name] > 0 for name in (
        "rank1_object", "projector", "holonomy", "dphi", "killing", "toric", "involution", "spectral"
    ))
    if object_signal >= 2 and (features["global_completion"] or features["holonomy"]):
        return "MANUAL_SIX_GATE_REVIEW"
    if object_signal >= 1:
        return "MANUAL_SUPPORT_OR_LOCAL_REVIEW"
    return "CONTEXT_ONLY_SCREEN"


def main() -> int:
    output = []
    for row in read_tsv("AUDIT_REPORT_UNIVERSE.tsv"):
        text = frozen_blob(row["git_blob"])
        counts = {name: len(pattern.findall(text)) for name, pattern in FEATURES.items()}
        output.append({
            "path": row["path"],
            "top_group": row["top_group"],
            "git_blob": row["git_blob"],
            "sha256": row["sha256"],
            "first_commit_date": row["first_commit_date"],
            "status_excerpt": status_excerpt(text),
            "result_excerpt": section_excerpt(text),
            **counts,
            "triage_route": triage(counts),
            "scientific_disposition": "PENDING_SOURCE_ADJUDICATION",
        })
    fields = [
        "path", "top_group", "git_blob", "sha256", "first_commit_date", "status_excerpt", "result_excerpt",
        *FEATURES, "triage_route", "scientific_disposition",
    ]
    target = PKG / "REPORT_EVIDENCE_EXTRACT.tsv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    routes = {route: sum(r["triage_route"] == route for r in output) for route in sorted({r["triage_route"] for r in output})}
    result = {
        "base": BASE,
        "reports": len(output),
        "triage_routes": routes,
        "report_evidence_extract_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "status": "PASS",
    }
    (PKG / "REPORT_EVIDENCE_EXTRACT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
