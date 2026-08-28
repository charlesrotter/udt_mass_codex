# G288 repair-only external follow-up request

Verify only preregistered repairs R1 through R5 and the unchanged bounded G288 landing.  Do not
continue the research.

Required checks:

1. Confirm `verify_independent.py` no longer uses a hard-coded coefficient table or the former
   closed-form random-case comparator, and that its registered coefficient map is obtained from
   full exact tensor evaluations on multiple amplitudes for each monomial.
2. Run the self-contained exact verifier and confirm both `c2` signs and both `c4` classes remain
   covered.
3. Run `run_hostile_recomputations.py`; verify that its baseline actually recomputes the tensors and
   that all four geometric mutations fail through nonzero verifier exits.
4. Confirm `run_catch_proofs.py` and `verify_package.py` are correctly described as artifact/semantic
   and integrity/provenance guards, not independent scientific derivations.
5. Confirm the SymPy dependency boundary is explicit and the standard-library replay is usable in
   the minimal reviewer environment.
6. Confirm the exact quadratic class now states sectional curvature `K=-C` in the registered
   convention.
7. Confirm no scientific equation, landing, scope, Planck-scale, physical-mass, history, source,
   observation, or `X_max` claim changed.

Return exactly one of `REPAIRS_ACCEPTED`, `REPAIRS_INCOMPLETE`, or `SCIENTIFIC_LANDING_CHANGED`,
followed by a concise defect list.
