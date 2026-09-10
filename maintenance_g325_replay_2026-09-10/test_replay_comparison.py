"""Maintenance-only catch proofs; no new scientific assertions or dependencies."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [ROOT / "udt_g325_g324_homogeneous_diagonal_linear_modes_2026-09-02",
            ROOT / "udt_g326_g324_homogeneous_offdiagonal_linear_modes_2026-09-02"]
ARTIFACTS = ("DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
             "CATCH_PROOF_RESULT.json")


def module_for(package):
    spec = importlib.util.spec_from_file_location("replay_verifier", package / "verify_package.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReplayComparisonTests(unittest.TestCase):
    def test_real_replays_and_provenance(self):
        for package in PACKAGES:
            with self.subTest(package=package.name):
                run = subprocess.run([sys.executable, "-S", str(package / "verify_package.py")],
                                     capture_output=True, text=True, timeout=30)
                self.assertEqual(run.returncode, 0, run.stderr)
                report = json.loads(run.stdout)
                self.assertIs(report["exact_scientific_replay"], True)
                self.assertEqual(set(report["replay_records"]), set(ARTIFACTS))
                for artifact, record in report["replay_records"].items():
                    self.assertIs(record["exact_scientific_replay"], True)
                    if artifact == "CATCH_PROOF_RESULT.json":
                        self.assertEqual(record["runtime_provenance"], {})
                    else:
                        metadata = record["runtime_provenance"]["python_version"]
                        saved = json.loads((package / artifact).read_text())
                        self.assertEqual(metadata["saved"], saved["python_version"])
                        self.assertEqual(metadata["replayed"], sys.version)
                        self.assertEqual(metadata["equal"], metadata["saved"] == sys.version)

    def test_only_declared_top_level_metadata_may_differ(self):
        for package in PACKAGES:
            compare = module_for(package).compare_replay
            saved = {"python_version": "build A", "result": 7, "nested": {"python_version": "x"}}
            replayed = copy.deepcopy(saved)
            replayed["python_version"] = "build B"
            result = compare(saved, replayed, runtime_keys=("python_version",))
            self.assertIs(result["exact_scientific_replay"], True)
            self.assertIs(result["exact_replay"], False)
            self.assertEqual(saved["python_version"], "build A")
            self.assertEqual(replayed["python_version"], "build B")
            replayed["nested"]["python_version"] = "y"
            self.assertIs(compare(saved, replayed, runtime_keys=("python_version",))
                          ["exact_scientific_replay"], False)

    def test_missing_empty_or_malformed_runtime_rejected(self):
        for package in PACKAGES:
            compare = module_for(package).compare_replay
            good = {"python_version": "build A", "result": 7}
            for bad in ({"result": 7}, {"python_version": None, "result": 7},
                        {"python_version": " ", "result": 7},
                        {"python_version": 3, "result": 7}):
                for saved, replayed in ((good, bad), (bad, good)):
                    with self.subTest(package=package.name, bad=bad, saved_bad=saved is bad):
                        with self.assertRaises(ValueError):
                            compare(saved, replayed, runtime_keys=("python_version",))

    def test_every_real_scientific_field_is_compared(self):
        for package in PACKAGES:
            compare = module_for(package).compare_replay
            for artifact in ARTIFACTS:
                saved = json.loads((package / artifact).read_text())
                runtime = () if artifact == "CATCH_PROOF_RESULT.json" else ("python_version",)
                for key in saved:
                    if key in runtime:
                        continue
                    for action in ("mutate", "remove"):
                        with self.subTest(package=package.name, artifact=artifact, key=key, action=action):
                            changed = copy.deepcopy(saved)
                            if action == "mutate":
                                changed[key] = {"MUTATED": saved[key]}
                            else:
                                del changed[key]
                            self.assertIs(compare(saved, changed, runtime_keys=runtime)
                                          ["exact_scientific_replay"], False)
                changed = dict(saved, unexpected_metadata="must not be ignored")
                self.assertIs(compare(saved, changed, runtime_keys=runtime)
                              ["exact_scientific_replay"], False)

    def test_bool_integer_float_not_equated(self):
        for package in PACKAGES:
            compare = module_for(package).compare_replay
            for value in (True, 1.0):
                self.assertIs(compare({"result": 1}, {"result": value}, runtime_keys=())
                              ["exact_scientific_replay"], False)

    def test_order_irrelevant_and_nonfinite_rejected(self):
        for package in PACKAGES:
            compare = module_for(package).compare_replay
            self.assertIs(compare({"a": 1, "b": 2}, {"b": 2, "a": 1}, runtime_keys=())
                          ["exact_scientific_replay"], True)
            with self.assertRaises(ValueError):
                compare({"result": float("nan")}, {"result": float("nan")}, runtime_keys=())

    def test_aggregate_rejects_changed_record_in_each_artifact(self):
        for package in PACKAGES:
            for artifact in ARTIFACTS:
                with self.subTest(package=package.name, artifact=artifact):
                    with tempfile.TemporaryDirectory(prefix="udt_replay_mutation_") as scratch:
                        target = Path(scratch) / "package"
                        shutil.copytree(package, target, ignore=shutil.ignore_patterns(".review_runtime", "__pycache__"))
                        path = target / artifact
                        result = json.loads(path.read_text())
                        # No explicit earlier value guard owns this added field: replay must catch it.
                        result["unexpected_scientific_result"] = 1
                        path.write_text(json.dumps(result))
                        run = subprocess.run([sys.executable, "-S", str(target / "verify_package.py")],
                                             capture_output=True, text=True, timeout=30)
                        self.assertNotEqual(run.returncode, 0)
                        self.assertIn("replay_scientific_exact:" + artifact, run.stderr)

    def test_old_whole_record_comparison_reintroduces_false_failure(self):
        for package in PACKAGES:
            with self.subTest(package=package.name):
                with tempfile.TemporaryDirectory(prefix="udt_old_replay_guard_") as scratch:
                    target = Path(scratch) / "package"
                    shutil.copytree(package, target, ignore=shutil.ignore_patterns(".review_runtime", "__pycache__"))
                    path = target / "DERIVATION_RESULT.json"
                    result = json.loads(path.read_text())
                    result["python_version"] = "synthetic different build for catch proof"
                    path.write_text(json.dumps(result))
                    verifier = target / "verify_package.py"
                    before = verifier.read_text()
                    changed = before.replace('gate(comparison["exact_scientific_replay"],',
                                             'gate(comparison["exact_replay"],')
                    self.assertNotEqual(before, changed)
                    verifier.write_text(changed)
                    run = subprocess.run([sys.executable, "-S", str(verifier)],
                                         capture_output=True, text=True, timeout=30)
                    self.assertNotEqual(run.returncode, 0)
                    self.assertIn("replay_scientific_exact:DERIVATION_RESULT.json", run.stderr)

    def test_optimized_execution_refused(self):
        for package in PACKAGES:
            run = subprocess.run([sys.executable, "-O", "-S", str(package / "verify_package.py")],
                                 capture_output=True, text=True, timeout=30)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("requires assertions enabled", run.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
