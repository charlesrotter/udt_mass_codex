"""Exercise the existing bounded Xmax documentary guard, not semantic completeness."""
import ast
import copy
from functools import lru_cache
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "c7f80d57920edb1aa06bfbd9cc1131367a01b460"
GUARD = ROOT / "verify_current_scientific_premises.py"
SOURCE = "udt_g163_xmax_dependency_reversal_audit_2026-08-18/AUDIT_REPORT.md"


@lru_cache(maxsize=2)
def xmax_nodes(baseline=False):
    source = (subprocess.check_output(["git", "show", f"{BASELINE}:verify_current_scientific_premises.py"],
                                     cwd=ROOT, text=True) if baseline else GUARD.read_text())
    tree = ast.parse(source)
    require = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "require")
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    positions = {target.id: i for i, n in enumerate(main.body) if isinstance(n, ast.Assign)
                 for target in n.targets if isinstance(target, ast.Name)}
    block = main.body[positions["xmax_controls"]:positions["adjudication"]]
    return ast.fix_missing_locations(ast.Module(
        body=copy.deepcopy([require, *block]), type_ignores=[]))


class XmaxMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="udt_xmax_guard_")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        for relative in ("AGENTS.md", "LIVE.md", "CURRENT_SCIENTIFIC_PREMISES.md", "INDEX.md", SOURCE):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)

    def replay(self):
        exec(compile(xmax_nodes(), str(GUARD), "exec"), {"ROOT": self.root})

    def test_current_control_block_passes(self):
        self.replay()

    def test_removed_limiting_qualification_fails(self):
        path = self.root / "LIVE.md"
        before = path.read_text()
        self.assertIn("asymptotic", before)
        path.write_text(before.replace("asymptotic", ""))
        with self.assertRaisesRegex(SystemExit, "control lacks Xmax limiting meaning: LIVE.md"):
            self.replay()

    def test_missing_source_pointer_fails(self):
        path = self.root / "INDEX.md"
        before = path.read_text()
        pointer = str(Path(SOURCE).parent) + "/"
        self.assertIn(pointer, before)
        path.write_text(before.replace(pointer, "missing_xmax_pointer/"))
        with self.assertRaisesRegex(SystemExit, "INDEX lacks controlling Xmax"):
            self.replay()

    def test_missing_controlling_source_fails(self):
        (self.root / SOURCE).unlink()
        with self.assertRaisesRegex(SystemExit, "controlling Xmax correction source missing"):
            self.replay()

    def test_actual_guard_block_unchanged(self):
        self.assertEqual(ast.dump(xmax_nodes()), ast.dump(xmax_nodes(baseline=True)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
