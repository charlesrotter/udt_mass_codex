#!/usr/bin/env python3
"""Altered-copy proof that the G263 repair closes the registered evidence escapes."""

from __future__ import annotations

import argparse
import copy
import csv
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path
from types import ModuleType


REVIEWER_ESCAPE_NAMES = (
    "shared_scalar_story_corrupted",
    "pair_contrast_replaced_with_padding",
    "positive_end_angular_corrupted",
    "negative_end_angular_corrupted",
    "pair_delta_reversal_weakened",
)


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expect_assertion(action, name: str) -> None:
    try:
        action()
    except AssertionError:
        return
    raise AssertionError(f"mutation escaped: {name}")


def run() -> dict[str, object]:
    package = Path(__file__).resolve().parent
    repo = package.parent
    catch_module = load_module("g263_catches", package / "run_catch_proofs.py")
    verifier_module = load_module("g263_package_verifier", package / "verify_package.py")
    derivation = json.loads((package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))

    direct_mutations = {
        "shared_scalar_story_corrupted": lambda d: d["separation"].update(shared="shared scalar inversion never happens"),
        "pair_contrast_replaced_with_padding": lambda d: (
            d["symbolic_checks"].remove("pair_contrast_even"),
            d["symbolic_checks"].append("bogus_placeholder_check"),
        ),
        "positive_end_angular_corrupted": lambda d: d["asymptotic_constant_jet"].update(
            phi_to_positive_infinity="N->0; mu/r->1/2; Aparallel->999; Aperp->999"
        ),
        "negative_end_angular_corrupted": lambda d: d["asymptotic_constant_jet"].update(
            phi_to_negative_infinity="N->infinity; mu/r->-infinity; Aparallel->999; Aperp->999"
        ),
        "pair_delta_reversal_weakened": lambda d: d["operations"].update(
            R_pair="endpoint swap at fixed ambient metric; delta stays the same except in examples"
        ),
    }
    caught: dict[str, bool] = {}
    for name, mutate in direct_mutations.items():
        candidate = copy.deepcopy(derivation)
        mutate(candidate)
        expect_assertion(lambda candidate=candidate: catch_module.validate(candidate), name)
        caught[name] = True

    with tempfile.TemporaryDirectory(prefix="g263_repair_catch_") as raw:
        temp_repo = Path(raw)
        temp_package = temp_repo / package.name
        shutil.copytree(package, temp_package)
        with (package / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                source = repo / row["path"]
                destination = temp_repo / row["path"]
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)

        sealed_path = temp_package / "SEALED_REPLAY_RESULT.json"
        sealed = json.loads(sealed_path.read_text(encoding="utf-8"))
        sealed["assertion_count"] -= 1
        sealed_path.write_text(json.dumps(sealed, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        expect_assertion(
            lambda: verifier_module.verify(temp_package, require_repair_catch=False),
            "sealed_replay_evidence_corrupted",
        )
        caught["sealed_replay_evidence_corrupted"] = True

        shutil.copy2(package / "SEALED_REPLAY_RESULT.json", sealed_path)
        catch_path = temp_package / "CATCH_PROOF_RESULT.json"
        catch_data = json.loads(catch_path.read_text(encoding="utf-8"))
        catch_data["caught_count"] -= 1
        catch_path.write_text(json.dumps(catch_data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        expect_assertion(
            lambda: verifier_module.verify(temp_package, require_repair_catch=False),
            "mutation_evidence_corrupted",
        )
        caught["mutation_evidence_corrupted"] = True

    if tuple(name for name in REVIEWER_ESCAPE_NAMES if not caught.get(name)):
        raise AssertionError("reviewer escape coverage incomplete")
    return {
        "status": "PASS",
        "caught_count": len(caught),
        "caught": caught,
        "qualification": "altered_copy_evidence_guard_not_scientific_proof",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
