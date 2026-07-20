#!/usr/bin/env python3
"""Fast integrity replay for already completed expensive continuation verification."""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = {
    "RAW_EXTENDED_PATHS.json": "c784c6aeb0c8d122bf7f485708c5c132fdcf8a90c3ea3320f66702812db9fa2b",
    "SUMMARY_RESULT.json": "9b4aa3ac88ff8b24db69a12350fd4a41bb30376117409badafebfd941fce0fa4",
    "VERIFICATION_RESULT.json": "2ced18ada4d4e900787acee244374d812ce2d77be9b144c909b2df86980f2313",
    "REPLAY_CHECKPOINT.json": "4a90b086dcd61463db9063460aaa08dda61a2362f09e72642f87060e6f2a70a1",
    "CATCH_PROOFS.tsv": "273d92eaedd3ecbbaf054cded7e5e855e79dde08bc0e521378fb03abdc798a6c",
    "PATH_STATUS_LEDGER.tsv": "d065a2d40b9c8a16d6f92a7632a20ef54ecde0589aa62d20d0675e76cabe90e6",
    "STATUS_LEDGER.tsv": "d8c13e3599b343a860ebb588da1361295f2148d358e1459a8e36c8f83a545dda",
    "COMPLETENESS_MAP.tsv": "4850bbfe191eba83897411f92917d8e37ead73ff30cd3b42f87975c9f167aac9",
}
SOURCE_EXPECTED = {
    "c2_failed_basin_homotopy_2026-07-20/RAW_HOMOTOPY_PATHS_COMPLETE_LEDGER.json": "1a8da008545be0a65d9f25899219a9334e4afd0692d5ef1bb7b67b95a817b2e8",
    "c2_failed_basin_homotopy_2026-07-20/continue_failed_basins.py": "30e343535d447c35f2457d7121e5e8fe8c67ea33c10b7210a0a7f2cb56cc0a80",
    "c2_failed_basin_homotopy_2026-07-20/full_bach.py": "a6bd3294b1ad1fabfb0325bda67fded8b491fcb5793b6a912e9f238f3e2e9973",
    "c2_nonlinear_stationary_solution_space_2026-07-20/stationary_c2_engine.py": "c5f06e9be433a3f90179fa6f66957eef8cf76e7aad39921fd2b484335a189b4a",
    "c2_nonlinear_stationary_solution_space_2026-07-20/explore_stationary_space.py": "36c07e153f96ad3980b8131792c2d06fafbadfd4014c717fe1534fed9e9c264b",
    "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md": "df0171eb83d75ad175727a8db541df8500b7826edf6059ae63a52f1a1ba15bea",
    "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv": "de154fbb7787759864786c04186a26a4605c447d362112bb482acee064d457e4",
    "stability_branch_follow_256_DECISION.md": "9806bc8f61b94109080699f00d8a758f1afc935db18a11f07dbe7365a61811d5",
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    root = HERE.parent
    assert all(digest(HERE / name) == expected for name, expected in EXPECTED.items())
    assert all(digest(root / name) == expected for name, expected in SOURCE_EXPECTED.items())
    summary = json.loads((HERE / "SUMMARY_RESULT.json").read_text())
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text())
    checkpoint = json.loads((HERE / "REPLAY_CHECKPOINT.json").read_text())
    assert summary["result"] == verification["result"] == "PASS"
    assert summary["counts"] == {"accepted_states": 3919, "bounded_open": 15, "cumulative_registered_starts": 198, "cumulative_round": 177, "paths": 22, "reduced_artifacts": 6, "rejected_steps": 1, "round_endpoints": 1}
    assert verification["counts"] == {"accepted_states": 3919, "bounded_open": 15, "catch_proofs": 14, "groups": 5, "paths": 22, "reduced_artifacts": 6, "round_endpoints": 1}
    assert checkpoint["raw_sha256"] == EXPECTED["RAW_EXTENDED_PATHS.json"] and checkpoint["groups"] == verification["groups"]
    with (HERE / "CATCH_PROOFS.tsv").open(newline="", encoding="utf-8") as handle:
        catches = list(csv.DictReader(handle, delimiter="\t"))
    assert len(catches) == 14 and all(row["result"] == "PASS" for row in catches)
    with (HERE / "SOURCE_LINEAGE.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 8 and {row["path"]: row["sha256"] for row in sources} == SOURCE_EXPECTED
    print(json.dumps({"result": "PASS", "artifact_hashes": len(EXPECTED), "source_hashes": len(SOURCE_EXPECTED), "groups": 5, "catch_proofs": 14}, sort_keys=True))

if __name__ == "__main__":
    main()
