#!/usr/bin/env python3
"""Bounded actual-G349 guard probes; no new scientific derivation or full audit.

Uses the prior maintenance review's command capture helper. Fixture mutations
are disposable and never touch accepted evidence. Stdout is the full record.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
PACKAGE = "udt_g349_finite_null_wavefront_patch_area_2026-09-04"
BASELINE = "c7f80d57920edb1aa06bfbd9cc1131367a01b460"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def demand(value, message):
    if not value:
        raise RuntimeError(message)


def assignment_to(node, name):
    return isinstance(node, ast.Assign) and any(
        isinstance(target, ast.Name) and target.id == name for target in node.targets
    )


def root_g349_block(source):
    tree = ast.parse(source)
    main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
    start = next(i for i, node in enumerate(main.body) if assignment_to(node, "g349"))
    end = next(i for i, node in enumerate(main.body) if assignment_to(node, "g350"))
    nodes = main.body[start:end]
    gates = [node for node in nodes if isinstance(node, ast.Expr)
             and isinstance(node.value, ast.Call)
             and any(isinstance(child, ast.Name) and child.id == "g349_replay"
                     for child in ast.walk(node.value.args[0]))]
    demand(len(gates) == 1, "Ambiguous root G349 replay acceptance")
    expected = ast.parse('g349_replay.returncode == 0 and \'"checks_total": 21\' in g349_replay.stdout', mode="eval").body
    demand(ast.dump(gates[0].value.args[0]) == ast.dump(expected), "Root acceptance predicate changed")
    helper = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "require")
    compiled = compile(ast.Module(body=[helper] + nodes, type_ignores=[]), "<actual-root-G349-statements>", "exec")
    return compiled, gates[0], helper, (nodes[0].lineno, nodes[-1].end_lineno)


def main():
    helper = ROOT / "maintenance_g325_replay_2026-09-10/review/reviewer_checks.py"
    spec = importlib.util.spec_from_file_location("prior_review_capture", helper)
    capture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(capture)
    source = (ROOT / "verify_current_scientific_premises.py").read_text()
    code, diagnostic_gate, require_node, line_span = root_g349_block(source)
    program = (ROOT / "CURRENT_RESEARCH_PROGRAM.md").read_text()
    demand("geometric endpoint image-union" in program, "Candidate program is not ready")
    with (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").open() as stream:
        row = next(row for row in csv.DictReader(stream, delimiter="\t") if row["premise_id"] == "G349")

    package = ROOT / PACKAGE
    protected_paths = [path for path in package.rglob("*") if path.is_file() and "__pycache__" not in path.parts]
    before = {str(path.relative_to(ROOT)): sha(path) for path in protected_paths}
    result = {"kind": "MAINTENANCE_ONLY_NOT_SCIENTIFIC_REPROOF", "model": "UNKNOWN",
              "baseline": BASELINE, "python_version": sys.version,
              "root_acceptance_expression_unchanged": True,
              "root_statement_line_span": line_span, "source_hashes": {
                  "harness": sha(Path(__file__)), "capture_helper": sha(helper),
                  "verify_current_scientific_premises.py": sha(ROOT / "verify_current_scientific_premises.py"),
                  "CURRENT_RESEARCH_PROGRAM.md": sha(ROOT / "CURRENT_RESEARCH_PROGRAM.md"),
                  "CURRENT_SCIENTIFIC_PREMISES.tsv": sha(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")},
              "accepted_package_before": before, "cases": [], "root_checks": []}

    with tempfile.TemporaryDirectory(prefix="g349_maintenance_review_", dir="/tmp") as directory:
        scratch = Path(directory)
        copied = scratch / PACKAGE
        shutil.copytree(package, copied, ignore=shutil.ignore_patterns("__pycache__"))
        verifier_tree = ast.parse((copied / "verify_package.py").read_text())
        source_hashes = next(ast.literal_eval(node.value) for node in verifier_tree.body
                            if assignment_to(node, "SOURCE_HASHES"))
        for relative, expected in source_hashes.items():
            original = ROOT / relative
            demand(sha(original) == expected, f"Accepted dependency mismatch before test: {relative}")
            destination = scratch / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, destination)
        fixture_program = scratch / "CURRENT_RESEARCH_PROGRAM.md"
        fixture_program.write_text(program)

        def root_probe(label, expected_pass, message_tokens=()):
            namespace = {"ROOT": scratch, "Path": Path,
                         "hashlib": hashlib, "json": json, "os": os,
                         "sys": sys, "subprocess": subprocess, "by_id": {"G349": row}}
            message = ""
            try:
                exec(code, namespace)
                passed = True
            except SystemExit as exc:
                passed = False
                message = str(exc)
            demand(passed is expected_pass, f"Actual root G349 block unexpected result: {label}")
            for token in message_tokens:
                demand(token in message, f"Diagnostic omits {token}: {label}")
            child = namespace.get("g349_replay")
            result["root_checks"].append({"label": label, "passed": passed, "message": message,
                "child": None if child is None else {"argv": child.args, "cwd": str(copied),
                    "returncode": child.returncode, "stdout": child.stdout, "stderr": child.stderr,
                    "extra_env": {"UDT_NO_WRITE": "1", "PYTHONDONTWRITEBYTECODE": "1"}}})

        def package_probe(label, text, expected_failed):
            fixture_program.write_text(text)
            command = capture.run([sys.executable, "-B", "-S", str(copied / "verify_package.py")],
                                  copied, extra_env={"UDT_NO_WRITE": "1"})
            observed = json.loads(command["stdout"])
            failed = sorted(key for key, value in observed["checks"].items() if not value)
            demand(failed == sorted(expected_failed), f"Unexpected package gates: {label}: {failed}")
            demand(command["returncode"] == (1 if expected_failed else 0), f"Exit mismatch: {label}")
            result["cases"].append({"label": label, "failed_checks": failed,
                                    "program_sha256": sha(fixture_program), "command": command})

        package_probe("qualified_candidate", program, [])
        root_probe("qualified_candidate", True)
        missing = program.replace("geometric endpoint image-union", "endpoint image-union")
        package_probe("geometric_qualification_removed", missing, ["geometric_not_physical_union_scope"])
        root_probe("geometric_qualification_removed", False,
                   ("geometric_not_physical_union_scope", '"checks_passed": 20', "exit 1", "STDOUT:", "STDERR:"))
        physical = program.replace("geometric endpoint image-union", "physical image-union")
        package_probe("qualification_replaced_by_physical_union", physical, ["geometric_not_physical_union_scope"])
        package_probe("physical_union_phrase_appended", program + "\nphysical image-union is established.\n",
                      ["geometric_not_physical_union_scope"])

        # An inherited literal-guard limitation; this is deliberately not a pass claim.
        contradiction = program + "\nG349 establishes physical light transfer and detector content.\n"
        package_probe("token_preserving_physical_overclaim_LIMITATION", contradiction, [])

        result_path = copied / "DERIVATION_RESULT.json"
        original_result = result_path.read_bytes()
        record = json.loads(original_result)
        record["assertions"] += 1
        result_path.write_text(json.dumps(record))
        package_probe("saved_production_count_corrupted", program, ["production_44321_of_44321"])
        root_probe("saved_production_count_corrupted", False, ("G349 production evidence changed",))
        result_path.write_bytes(original_result)

        evidence = copied / "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md"
        original_evidence = evidence.read_bytes()
        evidence.write_bytes(original_evidence + b"\nREVIEW ONLY CORRUPTED EVIDENCE\n")
        package_probe("frozen_external_evidence_corrupted", program, ["frozen_external_repair_evidence"])
        root_probe("frozen_external_evidence_corrupted", False,
                   ("frozen_external_repair_evidence", "exit 1", "STDOUT:", "STDERR:"))
        evidence.write_bytes(original_evidence)

        # Synthetic failed-child outputs test only the unchanged diagnostic gate,
        # supplementing the actual child-process failures above.
        gate_code = compile(ast.Module(body=[require_node, diagnostic_gate], type_ignores=[]), "<actual-root-replay-gate>", "exec")
        for label, child, expected_pass in (
            ("nonzero_despite_success_looking_stdout", subprocess.CompletedProcess([], 7, '{"checks_total": 21}', "REAL STDERR SENTINEL"), False),
            ("zero_without_expected_total", subprocess.CompletedProcess([], 0, "missing expected total", ""), False),
        ):
            try:
                exec(gate_code, {"g349_replay": child})
                passed, message = True, ""
            except SystemExit as exc:
                passed, message = False, str(exc)
            demand(passed is expected_pass, f"Diagnostic gate weakened: {label}")
            demand(child.stdout in message and child.stderr in message, f"Captured stream lost: {label}")
            demand(f"exit {child.returncode}" in message, f"Exit status lost: {label}")
            result["root_checks"].append({"label": label, "passed": passed, "message": message,
                "child": {"returncode": child.returncode, "stdout": child.stdout, "stderr": child.stderr},
                "synthetic_diagnostic_only": True})

        package_probe("restored_fixture", program, [])

    after = {str(path.relative_to(ROOT)): sha(path) for path in protected_paths}
    demand(before == after, "Accepted G349 package mutated during review")
    result["accepted_package_unchanged_during_review"] = True
    result["limitations"] = [
        "Literal documentation predicate can pass a token-preserving physical overclaim; no semantic completeness claimed.",
        "Actual G349 root statements were isolated from the full verifier; this is not a full365 run.",
        "Existing numerical producers were replayed by the actual package checker; no independent mathematical re-proof.",
        "Fresh context and separately written fixture probes do not establish a different runtime model."]
    result["status"] = "PASS_BOUNDED_MAINTENANCE_WITH_RECORDED_LIMITATION"
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
