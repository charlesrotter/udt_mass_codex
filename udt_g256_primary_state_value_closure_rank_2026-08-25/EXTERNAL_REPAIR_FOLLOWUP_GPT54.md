# G256 first repair-only follow-up — gpt-5.4

Sealed intake: `/tmp/udt_g256_repair_followup_vrg_sfkg`  
`REVIEW_MANIFEST.tsv` SHA-256:
`69916960eb0fb8b7d8b86edba8ae8c74d50dabe74bbe1d822201b5b5d3e5c33c`  
Returned response SHA-256:
`81d49422fa92ff3aad8b71c76b2293487ee2166db74935ed3453ea60341b7f42`

## Grade

`G256_R1_REPAIR_INCOMPLETE`

## What passed

- The reviewer hash loop returned `REVIEW_MANIFEST_OK` for all 45 payload rows and
  `SOURCE_MANIFEST_OK` for all 18 scientific sources. Its prose incorrectly summarized the first
  count as `43/43`; the loop itself traversed the complete manifest.
- The source inspection confirmed that R1 removed the repository-external premise-verifier call.
- The dependency-free independent replay passed all graph, cycle, angular, Hermite, owner, and
  solver-gate checks and retained the scientific landing.

## Remaining certification defect

The external runtime did not contain SymPy. `verify_package.py` still executed the SymPy production
script, and `run_catch_proofs.py` imported it. Those two registered commands therefore exited one
with `ModuleNotFoundError`, while the independent standard-library replay exited zero.

The reviewer explicitly retained the bounded scientific landing and classified the problem as
packaging/runtime self-containment rather than a scientific defect.
