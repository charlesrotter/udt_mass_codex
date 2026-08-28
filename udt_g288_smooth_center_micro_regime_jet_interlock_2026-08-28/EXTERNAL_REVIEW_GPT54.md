# G288 external adversarial review — gpt-5.4

Date: 2026-08-28
Verdict: `PASS_WITH_REPAIRS`

## Scientific landing

The reviewer independently reconstructed the current primary metric geometry and retained the exact
bounded G288 landing:

```text
PARTIAL_CENTER_INTERLOCK_ONLY
__QUADRATIC_NEGATIVE_PROFILE_GERM_IS_ZERO_TIDE_CONSTANT_CURVATURE
__ANGULAR_TIDE_BEGINS_AT_INDEPENDENT_QUARTIC_JET
__NO_PLANCK_SCALE_OR_HISTORY_SELECTED
```

The reviewer separately recovered the scalar curvature, Riemann-square, Weyl-square, null-screen
channels, both signs of `c2`, the `c4=0` and `c4!=0` cases, and the exact quadratic family.  It also
retained the distinctions between geometric areal mass aspect and physical mass, and between
coordinate radial-null slope and locally normalized null speed.

## Required repairs

1. **Moderate, evidence grade only.**  The independent verifier reconstructs the tensor geometry,
   but then compares parts of it with a pre-entered coefficient formula and a hard-coded expected
   coefficient table.  Replace those targets with coefficient maps obtained from the independent
   tensor route itself.
2. **Moderate, evidence grade only.**  `run_catch_proofs.py` mutates saved result strings and
   booleans.  Regrade it as an artifact/semantic replay guard and add a true recomputing hostile
   harness for the geometric mutations.
3. **Moderate, evidence grade only.**  `verify_package.py` is principally an integrity and
   provenance aggregator, not an independent scientific recomputation.  State that distinction
   explicitly.
4. **Minor, evidence grade only.**  The SymPy production route could not run in the reviewer's
   minimal environment.  Make the standard-library exact route the registered self-contained
   scientific replay and mark the SymPy route's dependency explicitly.
5. **Minor, wording only.**  State the sign of the quadratic family's sectional curvature:
   `K=-C` in the registered Riemann convention.

None of these findings changes the bounded scientific result.  No Planck scale, physical mass,
source, history, `X_max`, or observation was selected.

## Reviewer-proposed next question

After repairing certification, test whether the quadratic zero-angular-tide tangent survives in a
general static-spherical areal metric with independent `A(r)` and `B(r)`, or whether it depends on
the primary reciprocal restriction `B=1/A`.  This is only a proposed future question.
