"""Bounded G349 wording and root diagnostic regression; not semantic proof."""
import ast
import copy
from functools import lru_cache
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "c7f80d57920edb1aa06bfbd9cc1131367a01b460"
PACKAGE = "udt_g349_finite_null_wavefront_patch_area_2026-09-04"
GUARD = ROOT / "verify_current_scientific_premises.py"


@lru_cache(maxsize=2)
def root_nodes(baseline=False):
    source = (subprocess.check_output(["git", "show", f"{BASELINE}:verify_current_scientific_premises.py"],
                                     cwd=ROOT, text=True) if baseline else GUARD.read_text())
    tree = ast.parse(source)
    require = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                   and node.name == "require")
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Name) and node.func.id == "require"
             and len(node.args) == 2
             and any(isinstance(part, ast.Constant) and isinstance(part.value, str)
                     and part.value.startswith("G349 dependency-free no-write replay failed")
                     for part in ast.walk(node.args[1]))]
    if len(calls) != 1:
        raise AssertionError("Expected exactly one actual root G349 replay guard")
    return require, calls[0]


def invoke_root_guard(result):
    """Execute the exact actual require() and G349 call, isolated from the long audit."""
    require, call = root_nodes()
    tree = ast.fix_missing_locations(ast.Module(
        body=[copy.deepcopy(require), ast.Expr(value=copy.deepcopy(call))], type_ignores=[]))
    exec(compile(tree, str(GUARD), "exec"), {"g349_replay": result})


class GuardMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="udt_guard_maintenance_")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.package = self.root / PACKAGE
        shutil.copytree(ROOT / PACKAGE, self.package,
                        ignore=shutil.ignore_patterns("__pycache__"))
        tree = ast.parse((self.package / "verify_package.py").read_text())
        hashes = next(ast.literal_eval(node.value) for node in tree.body
                      if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == "SOURCE_HASHES"
                              for target in node.targets))
        for relative in hashes:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
        self.program = self.root / "CURRENT_RESEARCH_PROGRAM.md"
        shutil.copy2(ROOT / "CURRENT_RESEARCH_PROGRAM.md", self.program)

    def replay(self):
        return subprocess.run([sys.executable, "-B", "-S", str(self.package / "verify_package.py")],
                              cwd=self.root, capture_output=True, text=True, timeout=30,
                              env=dict(os.environ, UDT_NO_WRITE="1", PYTHONDONTWRITEBYTECODE="1"))

    def expect_failed(self, gate):
        result = self.replay()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        record = json.loads(result.stdout)
        self.assertIs(record["all_passed"], False)
        self.assertIs(record["checks"][gate], False)
        return result

    def remove_geometric_qualification(self):
        before = self.program.read_text()
        self.assertIn("geometric endpoint image-union", before,
                      "Mutation requires the accepted baseline qualification")
        self.program.write_text(before.replace("geometric endpoint image-union", "endpoint image-union"))

    def test_current_qualified_program_and_real_package_pass(self):
        result = self.replay()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        record = json.loads(result.stdout)
        self.assertEqual(record["checks_passed"], 21)
        self.assertIs(record["all_passed"], True)

    def test_removed_geometric_qualification_fails(self):
        self.remove_geometric_qualification()
        self.expect_failed("geometric_not_physical_union_scope")

    def test_physical_identification_fails_even_with_geometric_phrase(self):
        self.assertIn("geometric endpoint image-union", self.program.read_text())
        self.program.write_text(self.program.read_text() + "\nG349 selects physical image-union.\n")
        self.expect_failed("geometric_not_physical_union_scope")

    def test_changed_scientific_check_count_fails(self):
        path = self.package / "DERIVATION_RESULT.json"
        record = json.loads(path.read_text())
        record["assertions"] -= 1
        path.write_text(json.dumps(record))
        self.expect_failed("production_44321_of_44321")

    def test_missing_scientific_record_fails(self):
        (self.package / "INDEPENDENT_VERIFICATION.json").unlink()
        result = self.replay()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("INDEPENDENT_VERIFICATION.json", result.stderr)

    def test_changed_scientific_source_hash_fails(self):
        path = self.package / "derive_finite_null_patch_area.py"
        path.write_text(path.read_text() + "\n# Deliberate source-correspondence mutation.\n")
        self.expect_failed("repaired_script_hashes")

    def test_root_acceptance_predicate_unchanged(self):
        self.assertEqual(ast.dump(root_nodes()[1].args[0]),
                         ast.dump(root_nodes(baseline=True)[1].args[0]))

    def test_root_reports_actual_stdout_failure(self):
        self.remove_geometric_qualification()
        result = self.expect_failed("geometric_not_physical_union_scope")
        self.assertEqual(result.stderr, "")
        with self.assertRaises(SystemExit) as caught:
            invoke_root_guard(result)
        message = str(caught.exception)
        self.assertIn("geometric_not_physical_union_scope", message)
        self.assertIn("exit 1", message)
        self.assertIn(result.stdout, message)

    def test_root_retains_stderr_and_rejects_wrong_count_token(self):
        failure = subprocess.CompletedProcess([], 2, "diagnostic stdout", "diagnostic stderr")
        with self.assertRaises(SystemExit) as caught:
            invoke_root_guard(failure)
        self.assertIn("diagnostic stdout", str(caught.exception))
        self.assertIn("diagnostic stderr", str(caught.exception))
        with self.assertRaises(SystemExit):
            invoke_root_guard(subprocess.CompletedProcess([], 0, '{"checks_total": 20}', ""))
        invoke_root_guard(subprocess.CompletedProcess([], 0, '{"checks_total": 21}', ""))


if __name__ == "__main__":
    unittest.main(verbosity=2)
