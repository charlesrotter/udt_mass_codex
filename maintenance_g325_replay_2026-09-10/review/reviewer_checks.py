#!/usr/bin/env python3
"""Separate-context maintenance adversary; no scientific result derivation.

Run one bounded package at a time. All mutations occur in disposable copies.
Results retain exact subprocess argv, cwd, stdout/stderr, hashes, and replay JSON.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
REVIEW = Path(__file__).resolve().parent
BASELINE = "51f189679d4029d750e375be949f41e2f15420fa"
PACKAGES = {
    "g325": "udt_g325_g324_homogeneous_diagonal_linear_modes_2026-09-02",
    "g326": "udt_g326_g324_homogeneous_offdiagonal_linear_modes_2026-09-02",
}
ARTIFACTS = ("DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(value, reason):
    if not value:
        raise RuntimeError(reason)


def typed_equal(left, right):
    """Independent recursive oracle; does not use candidate serialization."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(typed_equal(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def leaves(value, path=()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from leaves(item, path + (key,))
    elif isinstance(value, list):
        for key, item in enumerate(value):
            yield from leaves(item, path + (key,))
    else:
        yield path, value


def replace(record, path, replacement):
    record = copy.deepcopy(record)
    node = record
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = replacement
    return record


def run(argv, cwd, *, extra_env=None):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if extra_env:
        env.update(extra_env)
    started = time.monotonic()
    process = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=40)
    return {"argv": argv, "cwd": str(cwd), "extra_env": extra_env or {},
            "returncode": process.returncode, "stdout": process.stdout,
            "stderr": process.stderr, "elapsed_seconds": time.monotonic() - started}


def package_preservation(package):
    paths = subprocess.check_output(["git", "ls-files", "--", package.name], cwd=ROOT, text=True).splitlines()
    records = []
    for relative in paths:
        current = (ROOT / relative).read_bytes()
        original = subprocess.check_output(["git", "show", f"{BASELINE}:{relative}"], cwd=ROOT)
        row = {"path": relative, "baseline_sha256": sha(original), "current_sha256": sha(current)}
        row["unchanged"] = current == original
        if Path(relative).name != "verify_package.py":
            require(row["unchanged"], f"Original package file changed: {relative}")
        records.append(row)
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package", choices=PACKAGES)
    args = parser.parse_args()
    package = ROOT / PACKAGES[args.package]
    verifier = package / "verify_package.py"
    before = package_preservation(package)
    spec = importlib.util.spec_from_file_location("reviewed_verifier", verifier)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = {"review_kind": "CHECKER_MAINTENANCE_NOT_SCIENTIFIC_REPROOF", "reviewer_model": "UNKNOWN",
              "baseline": BASELINE, "package": package.name, "python_version": sys.version,
              "harness_sha256": sha(Path(__file__).read_bytes()), "verifier_sha256": sha(verifier.read_bytes()),
              "original_package_files_before": before, "commands": [], "helper_case_count": 0,
              "helper_coverage": {}, "actual_replays": {}, "package_mutations": []}

    def probe(saved, replayed, runtime_keys, expected=None, malformed=False):
        result["helper_case_count"] += 1
        try:
            observed = module.compare_replay(saved, replayed, runtime_keys=runtime_keys)
        except (ValueError, TypeError, AttributeError):
            require(malformed, "Unexpected rejection of valid record")
            return
        require(not malformed, "Malformed metadata false pass")
        if expected is None:
            left = {k: v for k, v in saved.items() if k not in runtime_keys}
            right = {k: v for k, v in replayed.items() if k not in runtime_keys}
            expected = typed_equal(left, right)
        require(observed["exact_scientific_replay"] is expected, "Scientific replay disagrees with typed oracle")
        require(observed["exact_replay"] is typed_equal(saved, replayed), "Full-record equality disagrees with oracle")
        require(observed["runtime_provenance"] == {
            k: {"saved": saved[k], "replayed": replayed[k], "equal": saved[k] == replayed[k]}
            for k in runtime_keys}, "Provenance lost or inaccurately reported")

    for artifact in ARTIFACTS:
        saved = json.loads((package / artifact).read_text())
        keys = () if artifact == "CATCH_PROOF_RESULT.json" else ("python_version",)
        start = result["helper_case_count"]
        probe(saved, copy.deepcopy(saved), keys)
        probe(saved, dict(reversed(list(saved.items()))), keys)
        for path, old in leaves(saved):
            if path == ("python_version",):
                continue
            new = (not old) if isinstance(old, bool) else old + 1 if isinstance(old, (int, float)) else "REVIEW_MUTATED" if isinstance(old, str) else "REVIEW_NULL_CHANGED"
            probe(saved, replace(saved, path, new), keys, expected=False)
            if type(old) is int:
                probe(saved, replace(saved, path, float(old)), keys, expected=False)
                if old in (0, 1):
                    probe(saved, replace(saved, path, bool(old)), keys, expected=False)
            elif type(old) is bool:
                probe(saved, replace(saved, path, int(old)), keys, expected=False)
        for key in saved:
            if key in keys:
                continue
            missing = copy.deepcopy(saved)
            del missing[key]
            probe(saved, missing, keys, expected=False)
        extra = dict(saved, unexpected_scientific_field="REVIEW")
        probe(saved, extra, keys, expected=False)
        if keys:
            altered = dict(saved, python_version="REVIEW different Python build")
            probe(saved, altered, keys, expected=True)
            for bad in (None, True, 123, {}, [], "", " \n\t"):
                for side in (0, 1):
                    pair = [copy.deepcopy(saved), copy.deepcopy(saved)]
                    pair[side]["python_version"] = bad
                    probe(*pair, keys, malformed=True)
            for side in (0, 1):
                pair = [copy.deepcopy(saved), copy.deepcopy(saved)]
                del pair[side]["python_version"]
                probe(*pair, keys, malformed=True)
        else:
            probe(saved, dict(saved, python_version="REVIEW extra metadata forbidden"), keys, expected=False)
        result["helper_coverage"][artifact] = result["helper_case_count"] - start

    synthetic = {"python_version": "build-a", "nested": {"python_version": "scientific-a"}, "version": "v1", "runtime": "kept", "zero": 0}
    for path, replacement in ((("nested", "python_version"), "scientific-b"), (("version",), "v2"), (("runtime",), "changed"), (("zero",), False)):
        probe(synthetic, replace(synthetic, path, replacement), ("python_version",), expected=False)
    for nan in (float("nan"), float("inf"), float("-inf")):
        probe(synthetic, dict(synthetic, zero=nan), ("python_version",), malformed=True)

    with tempfile.TemporaryDirectory(prefix=f"review_{args.package}_", dir="/tmp") as temporary:
        scratch = Path(temporary) / "package"
        shutil.copytree(package, scratch, ignore=shutil.ignore_patterns(".review_runtime", "__pycache__"))
        replay_lines = (scratch / "REPLAY_COMMANDS.txt").read_text().splitlines()
        for line, artifact in zip(replay_lines, ARTIFACTS):
            command = run(shlex.split(line), scratch)
            result["commands"].append(command)
            require(command["returncode"] == 0, f"Actual producer failed: {artifact}")
            generated = scratch / ".review_runtime" / artifact
            saved = json.loads((package / artifact).read_text())
            replayed = json.loads(generated.read_text())
            excluded = () if artifact == "CATCH_PROOF_RESULT.json" else ("python_version",)
            left = {k: v for k, v in saved.items() if k not in excluded}
            right = {k: v for k, v in replayed.items() if k not in excluded}
            require(typed_equal(left, right), f"Actual science changed: {artifact}")
            differences = [k for k in saved.keys() | replayed.keys() if k not in saved or k not in replayed or not typed_equal(saved[k], replayed[k])]
            result["actual_replays"][artifact] = {"differing_top_level_fields": differences,
                "saved_sha256": sha((package / artifact).read_bytes()), "replayed_sha256": sha(generated.read_bytes()),
                "saved_record": saved, "replayed_record": replayed,
                "exact_scientific_replay_by_independent_recursive_oracle": True}

        # Reintroduce old comparison using exact baseline source; preserve its failure.
        original_verifier = subprocess.check_output(["git", "show", f"{BASELINE}:{package.name}/verify_package.py"], cwd=ROOT)
        (scratch / "verify_package.py").write_bytes(original_verifier)
        baseline = run(["python3", "-B", "-S", "verify_package.py"], scratch)
        result["commands"].append(baseline)
        require(baseline["returncode"] != 0 and "replay_exact:DERIVATION_RESULT.json" in baseline["stderr"], "Old bug did not go RED")
        (scratch / "verify_package.py").write_bytes(verifier.read_bytes())
        normal = run(["python3", "-B", "-S", "verify_package.py"], scratch)
        result["commands"].append(normal)
        require(normal["returncode"] == 0, "Candidate real aggregate failed")
        aggregate = json.loads(normal["stdout"])
        require(aggregate["exact_scientific_replay"] is True and aggregate["exact_replay"] is False, "Aggregate misreports equality")
        result["aggregate_result"] = aggregate

        # Each copied-package mutation exercises the live main() gate, not merely the helper.
        mutations = [
            ("DERIVATION_RESULT.json", "extra_field", lambda x: x.update(review_extra_field=1)),
            ("DERIVATION_RESULT.json", "count_int_to_float", lambda x: x.update(assertion_count=float(x["assertion_count"]))),
            ("DERIVATION_RESULT.json", "false_to_zero", lambda x: x.update(metric_changed=0)),
            ("DERIVATION_RESULT.json", "metadata_missing", lambda x: x.pop("python_version")),
            ("DERIVATION_RESULT.json", "metadata_null", lambda x: x.update(python_version=None)),
            ("INDEPENDENT_VERIFICATION.json", "count_int_to_float", lambda x: x.update(assertion_count=float(x["assertion_count"]))),
            ("INDEPENDENT_VERIFICATION.json", "extra_field", lambda x: x.update(review_extra_field=1)),
            ("INDEPENDENT_VERIFICATION.json", "metadata_empty", lambda x: x.update(python_version="")),
            ("CATCH_PROOF_RESULT.json", "count_int_to_float", lambda x: x.update(assertion_count=float(x["assertion_count"]))),
            ("CATCH_PROOF_RESULT.json", "metadata_injection", lambda x: x.update(python_version="REVIEW")),
        ]
        for artifact, label, mutate in mutations:
            path = scratch / artifact
            original = path.read_bytes()
            record = json.loads(original)
            mutate(record)
            path.write_text(json.dumps(record))
            command = run(["python3", "-B", "-S", "verify_package.py"], scratch)
            result["commands"].append(command)
            result["package_mutations"].append({"artifact": artifact, "mutation": label, "returncode": command["returncode"], "command_index": len(result["commands"]) - 1})
            require(command["returncode"] != 0, f"Package mutation false pass: {artifact}/{label}")
            path.write_bytes(original)
        for flags, env in ((["-O"], None), (["-OO"], None), ([], {"PYTHONOPTIMIZE": "1"})):
            command = run(["python3", "-B", "-S", *flags, "verify_package.py"], scratch, extra_env=env)
            result["commands"].append(command)
            require(command["returncode"] != 0 and "requires assertions enabled" in command["stderr"], "Optimized false pass")

    after = package_preservation(package)
    require(before == after, "Package bytes changed during review")
    result["original_package_files_after"] = after
    result["status"] = "PASS_MAINTENANCE_CHECKS_ONLY"
    output = REVIEW / f"{args.package}_reviewer_results.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "helper_case_count": result["helper_case_count"],
                      "commands": len(result["commands"]), "package_mutations": len(result["package_mutations"]),
                      "result": str(output), "verifier_sha256": result["verifier_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
