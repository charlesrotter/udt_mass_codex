# G256 evidence gates

1. **Preregistered:** PASS. Commit `6a5cfb91` froze the question, three landings, exclusions,
   falsifiers, and maximum conclusion before outcome production.
2. **Full space or bounded scope:** PASS WITH BOUNDS. Arbitrary finite connected scalar networks and
   arbitrary finite primary value/first/second jets are covered by general proofs. Singular strata,
   nonscalar transport, sources, topology, and boundaries are explicitly excluded.
3. **Independent verification:** PASS. The standard-library exact-Fraction replay imports no
   production code and reads no production result.
4. **Premise audit:** PASS WITH EXPLICIT LOCATION. The repository-local 238-row premise verifier
   passed before sealing. The self-contained sealed replay checks the exact 18-source hashes and
   owner census; it does not invoke the repository-wide verifier.
5. **Hostile mutation catches:** PASS, 7/7, through a standard-library-only validation path after
   R2; no production module is imported by the sealed hostile replay.
6. **Fresh external review:** PASS AFTER R2. The original
   review found no scientific defect. The R1 follow-up confirmed the external root-script call was
   removed and retained the landing, but exposed a remaining host-only SymPy dependency. R2 removes
   third-party dependencies from all registered sealed replays without changing production
   evidence or the scientific result. The R2 follow-up verified 47/47 payloads, 18/18 sources, and
   all three registered commands at exit zero; no remaining certification defect was found.

Current grade: `EXTERNALLY_VERIFIED_WITH_CAVEATS__R2_SELF_CONTAINED_REPLAY_ACCEPTED`.
