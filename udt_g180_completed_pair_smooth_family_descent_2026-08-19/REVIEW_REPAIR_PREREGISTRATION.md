# G180 external-review repair preregistration

Date: 2026-08-19

The authorized fresh external review returned `G180_ACCEPTED_WITH_STATED_BOUNDS`. It independently
reconstructed the theorem, matched all nine frozen-source hashes after resolving them under the
sealed `sources/` directory, and reproduced the exact 20,000-family result. It found no scientific
or premise defect.

It did find two replay-packaging limitations:

1. `build_review_intake.py` placed frozen sources below `sources/` although the shipped replay
   scripts resolve repository-relative manifest paths from the intake root.
2. `run_catch_proofs.py` imported SymPy for one inequality that has a dependency-free exact-rational
   equivalent. The production symbolic derivation itself may continue to require SymPy; the sealed
   certification path must not.

Before inspecting any follow-up outcome, the registered repairs are exactly:

- preserve each frozen source at its original repository-relative path inside the sealed intake;
- replace the catch script's one SymPy comparison with the equivalent exact `Fraction` comparison;
- provide dependency-free `UDT_READ_ONLY_REPLAY=1` modes that compare recomputed independent and
  catch results to the banked artifacts without attempting to write into the sealed intake;
- require the corrected sealed intake to run the dependency-free independent replay, catch proof,
  package verifier, and intake verifier successfully without repository access;
- make no change to the theorem, premise grade, formulas, witnesses, source set, trial population,
  or maximum conclusion.

A follow-up review may return `G180_REPAIR_ACCEPTED` only if it verifies these repairs and retains
the original bounded landing. Any mathematical change or new scientific claim requires a new
preregistration rather than this repair path.
