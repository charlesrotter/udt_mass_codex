"""Run the new persistent tests against the preserved defective verifier, without edits.

Expected pytest failure in the 11 guards that reread. The original review file and live
implementation remain unchanged. This is a catch-proof, not a scientific replay.
"""
from pathlib import Path
import importlib.util
import sys
import pytest

repo = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo))
source = Path(__file__).resolve().parent / "review/INITIAL_verify_current_scientific_premises.py"
name = "verify_current_scientific_premises"
spec = importlib.util.spec_from_file_location(name, source)
module = importlib.util.module_from_spec(spec)
sys.modules[name] = module
spec.loader.exec_module(module)
raise SystemExit(pytest.main([
    "--noconftest", "-q", str(repo / "tests/test_ti2_banking.py"),
    "-k", "test_historical_guard_never_rereads_a_substituted_registry",
]))
