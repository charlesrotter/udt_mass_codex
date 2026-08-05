#!/usr/bin/env python3
"""Fail-closed verifier for the native-law order architecture audit."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table_text(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))


def table(path: Path) -> list[dict[str, str]]:
    return table_text(path.read_text(encoding="utf-8"))


def validate(
    program: str,
    report: str,
    arch_text: str,
    joint_text: str,
    evidence_text: str,
    nav_texts: dict[str, str],
) -> None:
    architectures = table_text(arch_text)
    assert len(architectures) == 2
    by_arch = {row["architecture"]: row for row in architectures}
    assert len(by_arch) == 2 and set(by_arch) == {"R_FIRST", "A_FIRST"}
    assert by_arch["R_FIRST"]["current_ruling"] == "ADMISSIBLE_WORKING_PRIORITY_NOT_DERIVED"
    assert by_arch["R_FIRST"]["next_priority"] == "FIRST_BOUNDED_TEST"
    assert by_arch["A_FIRST"]["current_ruling"] == "ADMISSIBLE_CONDITIONAL_NOT_SELECTED"
    assert by_arch["A_FIRST"]["next_priority"] == "RETAIN_AS_ALTERNATIVE"

    joints = table_text(joint_text)
    assert len(joints) == 10
    objects = [row["object"] for row in joints]
    assert len(objects) == len(set(objects))
    assert {row["status"] for row in joints} >= {
        "OPEN", "OPEN_WITH_LAW", "OPEN_NATIVE__F04_CONDITIONAL",
        "OPEN_DOWNSTREAM_OPTION", "OPEN_CONDITIONAL_OPTION",
    }

    evidence = table_text(evidence_text)
    assert len(evidence) == 15
    assert [row["id"] for row in evidence] == [f"E{i:02d}" for i in range(1, 16)]
    assert any(row["id"] == "E04" and row["status"] == "DERIVED_PARTIAL_KINEMATIC" for row in evidence)
    for row in evidence:
        assert (ROOT / row["source"]).is_file(), row["source"]

    required_program = (
        "Law-order `NOT_DERIVED`",
        "Response-first is the priority",
        "Action-first remains admissible",
        "Strong local Common-Scale Neutrality is an inactive",
        "Einsteinian `c_E` and observed `G_obs` are active dimensional calibration anchors",
        "`X_max` is the working frame-shared observer-pair positional-dilation asymptote",
        "F04` is a genuine full-3D Hopf-capable model with settled static finite-box stability only",
        "Co-presence means membership in one complete solution",
        "Failure would sharply limit the current response-first foothold to boundary kinematics",
        "not launched by the present audit",
    )
    for token in required_program:
        assert token in program, token
    forbidden_program = (
        "response-first is derived",
        "action-first is selected",
        "bootstrap return is derived",
        "source is a required substrate substance",
        "physical mass is derived",
        "strong local CSN is active",
        "UDT is scale-free",
        "X_max is a variational boundary",
        "F04 is native unconditional stability",
        "general observer-pair depth law is derived",
        "action is impossible",
    )
    lowered = program.lower()
    for token in forbidden_program:
        assert token.lower() not in lowered, token

    required_report = (
        "THREE_JOINTS_FORM_ONE_ORDERED_CLOSURE_CHAIN",
        "LAW_ORDER_NOT_DERIVED",
        "ACTION_FIRST_REMAINS_ADMISSIBLE_CONDITIONAL",
        "COMPLETE_NATIVE_RETURN_REMAINS_OPEN",
        "partial-correspondence conormal response audit",
        "VERIFIED-WITH-CAVEATS",
    )
    for token in required_report:
        assert token in report, token

    for name in ("LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md"):
        text = nav_texts[name]
        assert "CURRENT_RESEARCH_PROGRAM.md" in text, name
        assert "udt_native_law_order_architecture_audit_2026-08-05" in text, name


def main() -> None:
    program = (ROOT / "CURRENT_RESEARCH_PROGRAM.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    arch_text = (HERE / "ARCHITECTURE_COMPARISON.tsv").read_text(encoding="utf-8")
    joint_text = (HERE / "JOINT_DEPENDENCY.tsv").read_text(encoding="utf-8")
    evidence_text = (HERE / "EVIDENCE_LEDGER.tsv").read_text(encoding="utf-8")
    nav_texts = {
        name: (ROOT / name).read_text(encoding="utf-8")
        for name in ("LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md")
    }
    validate(program, report, arch_text, joint_text, evidence_text, nav_texts)

    sources = table(HERE / "SOURCE_INVENTORY.tsv")
    assert len(sources) == 23
    assert sum(row["immutability"] == "IMMUTABLE_SOURCE" for row in sources) == 21
    assert sum(row["immutability"] == "MUTABLE_NAVIGATION_CONTROL" for row in sources) == 2
    for row in sources:
        path = ROOT / row["path"]
        assert path.is_file(), row["path"]
        if row["immutability"] == "IMMUTABLE_SOURCE":
            assert digest(path) == row["sha256_at_preregistered_base"], row["path"]

    premise = subprocess.run(
        ["python3", "verify_current_scientific_premises.py"], cwd=ROOT, text=True,
        capture_output=True, timeout=60, check=False,
    )
    assert (
        premise.returncode == 0 and "PASS: 27 premise guards" in premise.stdout
    ), premise.stdout + premise.stderr

    mutations = []

    def caught(name: str, **changes: str) -> None:
        args = {
            "program": program,
            "report": report,
            "arch_text": arch_text,
            "joint_text": joint_text,
            "evidence_text": evidence_text,
            "nav_texts": dict(nav_texts),
        }
        args.update(changes)
        try:
            validate(**args)
        except (AssertionError, KeyError):
            mutations.append(name)
            return
        raise AssertionError(f"mutation escaped: {name}")

    caught("C01", arch_text=arch_text.replace("ADMISSIBLE_WORKING_PRIORITY_NOT_DERIVED", "DERIVED"))
    caught("C02", arch_text=arch_text.replace("ADMISSIBLE_CONDITIONAL_NOT_SELECTED", "SELECTED"))
    caught("C03", program=program + "\nBootstrap return is derived.\n")
    caught("C04", program=program + "\nSource is a required substrate substance.\n")
    caught("C05", program=program + "\nPhysical mass is derived.\n")
    caught("C06", program=program + "\nStrong local CSN is active.\n")
    caught("C07", program=program + "\nUDT is scale-free.\n")
    caught("C08", program=program + "\nX_max is a variational boundary.\n")
    caught("C09", program=program + "\nF04 is native unconditional stability.\n")
    caught("C10", program=program + "\nGeneral observer-pair depth law is derived.\n")
    caught("C11", program=program.replace("not launched by the present audit", "launched by the present audit"))
    caught("C12", program=program + "\nAction is impossible.\n")
    caught("C13", arch_text="\n".join(line for line in arch_text.splitlines() if not line.startswith("R_FIRST\t")) + "\n")
    caught("C14", arch_text=arch_text + next(line for line in arch_text.splitlines() if line.startswith("A_FIRST\t")) + "\n")
    caught("C15", evidence_text="\n".join(line for line in evidence_text.splitlines() if not line.startswith("E04\t")) + "\n")
    nav_mut = dict(nav_texts)
    nav_mut["LIVE.md"] = nav_mut["LIVE.md"].replace("CURRENT_RESEARCH_PROGRAM.md", "MISSING_PROGRAM.md")
    caught("C16", nav_texts=nav_mut)
    assert mutations == [f"C{i:02d}" for i in range(1, 17)]

    result = {
        "schema": "udt.native_law_order_architecture_audit.v1",
        "status": "PASS",
        "architectures": len(table_text(arch_text)),
        "joint_rows": len(table_text(joint_text)),
        "evidence_rows": len(table_text(evidence_text)),
        "source_rows": len(sources),
        "immutable_sources": 21,
        "navigation_controls": 5,
        "premise_guards": 27,
        "mutation_catches": len(mutations),
        "external_semantic_review": "NOT_TRANSMITTED",
        "grade": "VERIFIED_WITH_CAVEATS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
