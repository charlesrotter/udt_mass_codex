# G256 second repair preregistration

Date: 2026-08-25

First repair-only gpt-5.4 grade: `G256_R1_REPAIR_INCOMPLETE`.

## Retained scientific landing

The reviewer again retained the bounded scientific landing. R2 is certification-only and must not
change any equation, atlas value, source, owner classification, premise stamp, or conclusion scope.

## Exact remaining defect

R1 removed the absent repository-wide premise-verifier call, but two registered sealed commands
still imported the host-only SymPy dependency through `derive_value_closure.py`. The dependency-free
independent replay passed; the package verifier and hostile controls did not start to completion in
the minimal external runtime.

## Preregistered R2 repair

1. Preserve `derive_value_closure.py` and its saved SymPy production artifacts unchanged as the
   original production method.
2. Stop executing the SymPy production script inside the sealed no-write verifier. Load the frozen
   production result and require its registered landing, rank, angular, Hermite, ownership, and
   solver-gate fields to agree with the saved atlases and the independent exact-Fraction replay.
3. Make `run_catch_proofs.py` standard-library-only by duplicating the small validation predicates
   needed by its seven hostile in-memory mutations. It must not import production code.
4. Require all three registered commands to pass in a minimal runtime with no third-party Python
   packages mounted.
5. Record the manifest accurately as 45 payload rows plus the manifest itself in the R1 intake; the
   reviewer hash loop covered every row despite its prose saying `43/43`.

The R2 follow-up may verify only these certification repairs and the unchanged bounded scientific
landing. It may not reopen or continue the research.
