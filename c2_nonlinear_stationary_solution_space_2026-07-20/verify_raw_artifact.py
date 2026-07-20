#!/usr/bin/env python3
"""Freeze and replay the expensive official solve artifacts without rerunning them."""
from __future__ import annotations
import hashlib,json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
EXPECTED={
 "RAW_ATTEMPTS.json":"0671c58e9684390ce82fa136dc9d2986337efcf5edc63453ecabe3b802197d55",
 "SOLVE_TRANSCRIPT.txt":"af583a6e3a00a7b6bdba6fcb4bfb337c8a60e27539a2138a1d0ac72f2b1be2b7",
}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 for name,expected in EXPECTED.items():
  observed=digest(HERE/name)
  if observed!=expected:raise AssertionError(f"sha256:{name}:{observed}")
 raw=json.loads((HERE/"RAW_ATTEMPTS.json").read_text())
 if raw["result"]!="COMPLETE_WITHIN_BUDGET" or raw["coverage"]!={"attempted":198,"planned":198,"stopped_by_global_budget":False}:raise AssertionError("coverage")
 counts=Counter(a["status"] for a in raw["attempts"])
 if counts!={"SOLVE_RESIDUAL_PASS":147,"NO_RESIDUAL_DECREASING_NEWTON_STEP":51}:raise AssertionError("status census")
 final=json.loads((HERE/"SOLVE_TRANSCRIPT.txt").read_text().splitlines()[-1])
 if final!={"attempted":198,"clusters":6,"planned":198,"result":"COMPLETE_WITHIN_BUDGET","status_counts":{"NO_RESIDUAL_DECREASING_NEWTON_STEP":51,"SOLVE_RESIDUAL_PASS":147}}:raise AssertionError("transcript terminus")
 print(json.dumps({"result":"PASS","attempts":198,"certified":147,"unresolved":51,"hashes":EXPECTED},sort_keys=True))
if __name__=="__main__":main()
