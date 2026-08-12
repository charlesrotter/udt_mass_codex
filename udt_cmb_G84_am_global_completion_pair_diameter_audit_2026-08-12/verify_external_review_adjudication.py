#!/usr/bin/env python3
"""Verify the G84 sealed external review, chronology, and bounded claims."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def git(*args: str, text: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=text, check=False)


def eval_node(node: ast.AST, environment: dict[str, Fraction]) -> Fraction:
    if isinstance(node, ast.Expression):
        return eval_node(node.body, environment)
    if isinstance(node, ast.BinOp):
        left = eval_node(node.left, environment)
        right = eval_node(node.right, environment)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left**right
    if isinstance(node, ast.UnaryOp):
        value = eval_node(node.operand, environment)
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return value
    if isinstance(node, ast.Name):
        return environment[node.id]
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return Fraction(node.value, 1)
    raise TypeError(type(node))


def exact_q4(expression: str) -> Fraction:
    return eval_node(ast.parse(expression, mode="eval"), {"s": Fraction(4, 1)})


def main() -> None:
    result = json.loads((HERE / "EXTERNAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
    assert result["status"] == "VERIFIED_WITH_CAVEATS"
    assert result["scientific_corrections"] == 0
    assert len(result["binding_caveats"]) == 5
    assert result["maximum_conclusion"] == "BOUNDED_AM_SPATIAL_COMPLETION_AND_STATIONARY_DEPTH_COMPATIBILITY_ATLAS"
    assert digest(HERE / "REVIEW_MANIFEST.tsv") == result["sealed_manifest_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_RAW.md") == result["raw_review_sha256"]
    assert digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == result["review_transcript_sha256"]

    manifest = rows(HERE / "REVIEW_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest}) == 37
    for row in manifest:
        assert digest(ROOT / row["path"]) == row["sha256"], row["path"]

    preregistration = result["preregistration_commit"]
    calculation = result["calculation_commit"]
    parent = git("rev-parse", f"{calculation}^")
    assert parent.returncode == 0 and parent.stdout.decode().strip() == preregistration
    assert git("merge-base", "--is-ancestor", preregistration, calculation).returncode == 0
    assert git("show", "-s", "--format=%s", preregistration, text=True).stdout.strip() == "Preregister G84 AM global completion audit"
    assert git("show", "-s", "--format=%s", calculation, text=True).stdout.strip() == "Bank G84 AM global completion atlas"

    source_profiles = rows(ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv")
    am = [row for row in source_profiles if row["lapse_name"] == "AM"]
    assert len(am) == len({row["profile_id"] for row in am}) == 197
    values = {row["profile_id"]: exact_q4(row["q_of_s"]) for row in am}
    signs = Counter("zero" if value == 0 else "positive" if value > 0 else "negative" for value in values.values())
    assert signs == Counter({"positive": 104, "negative": 92, "zero": 1})
    assert [key for key, value in values.items() if value == 0] == ["G75_F01_AM"]
    assert min(abs(value) for value in values.values() if value != 0) == Fraction(1, 20)

    atlas = rows(HERE / "PROFILE_COMPLETION_ATLAS.tsv")
    assert len(atlas) == 197
    mismatches = 0
    for row in atlas:
        value = values[row["profile_id"]]
        rendered = str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
        mismatches += rendered != row["q_at_s_4_exact"]
    assert mismatches == 0

    geometry = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert geometry["physical_X_max_status"] == "OPEN"
    assert geometry["geometry"]["spatial_radius_over_R"] == "2"
    assert geometry["geometry"]["spatial_diameter_over_R"] == "2*pi"
    assert geometry["geometry"]["zero_mix_recentered_static_limit_over_R"] == "pi"
    assert geometry["geometry"]["zero_mix_frame_scope"] == "GLOBAL_ISOMETRY_ORBIT_OF_CENTRAL_GEODESIC_OBSERVERS"

    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    combined = raw + adjudication
    for token in (
        "VERIFIED_WITH_CAVEATS",
        "37/37",
        "central timelike-geodesic",
        "not a physical `X_max`",
        "104",
        "92",
        "1/20",
        "BOUNDED_AM_SPATIAL_COMPLETION_AND_STATIONARY_DEPTH_COMPATIBILITY_ATLAS",
    ):
        assert token in combined, token

    output = {
        "schema": "udt-cmb-g84-external-adjudication-verification-v1",
        "status": "PASS",
        "scientific_corrections": 0,
        "binding_caveats": len(result["binding_caveats"]),
        "sealed_intake_files": result["sealed_intake_files"],
        "sealed_payload_rows": len(manifest),
        "payload_hashes_verified_live": len(manifest),
        "preregistration_commit": preregistration,
        "calculation_commit": calculation,
        "chronology_verified": True,
        "profile_rows": len(am),
        "zero_q4_rows": signs["zero"],
        "nonzero_q4_rows": signs["positive"] + signs["negative"],
        "atlas_mismatches": mismatches,
        "physical_X_max_status": geometry["physical_X_max_status"],
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
