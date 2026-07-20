#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
EXPECTED={"RAW_HOMOTOPY_PATHS_COMPLETE_LEDGER.json":"1a8da008545be0a65d9f25899219a9334e4afd0692d5ef1bb7b67b95a817b2e8","HOMOTOPY_COMPLETE_LEDGER_TRANSCRIPT.txt":"defc668e5ef55919081f1e92d43a011878bcee97a5f1f2934563eb1f4a0e389f","RAW_HOMOTOPY_PATHS_INCOMPLETE_LEDGER.json":"05583c69d82ed8afb713fa17094a790b7c30146012f4616ef32ed22d5f57586c","HOMOTOPY_INCOMPLETE_LEDGER_TRANSCRIPT.txt":"b3bde058d0b4c1890e166f629647bb8e20b96d51d02b0dcf89d829b3895c15e4"}
def main():
 for name,expected in EXPECTED.items():
  observed=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
  if observed!=expected:raise AssertionError(f"sha256:{name}:{observed}")
 a=json.loads((HERE/"RAW_HOMOTOPY_PATHS_COMPLETE_LEDGER.json").read_text());b=json.loads((HERE/"RAW_HOMOTOPY_PATHS_INCOMPLETE_LEDGER.json").read_text());key=lambda r:{(p["path_id"],p["status"],(p.get("endpoint") or {}).get("classification")) for p in r["paths"]}
 if len(key(a))!=51 or key(a)!=key(b) or a["status_counts"]!={"ENDPOINT_REACHED":29,"PATH_TIME_LIMIT":22}:raise AssertionError("identity regression")
 print(json.dumps({"result":"PASS","identity_rows":51,"round_endpoints":29,"unresolved":22,"hashes":EXPECTED},sort_keys=True))
if __name__=="__main__":main()
