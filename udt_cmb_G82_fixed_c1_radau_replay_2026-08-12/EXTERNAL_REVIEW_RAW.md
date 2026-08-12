**Landing**

`VERIFIED_WITH_CAVEATS`.

Within the 27-file sealed intake, G82 does honestly replay the frozen G81 `C1_FULL_ANGULAR` control with `Radau` and supports only `G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY`. I verified all `26/26` payload hashes from [REVIEW_MANIFEST.tsv](/tmp/udt_g82_review_EfMKGy/REVIEW_MANIFEST.tsv:1), confirmed the G82 control row matches the G81 C1 row exactly in direction, screens, and rotations ([G81 CONTROL_UNIVERSE.tsv](/tmp/udt_g82_review_EfMKGy/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/CONTROL_UNIVERSE.tsv:3), [G82 CONTROL_UNIVERSE.tsv](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/CONTROL_UNIVERSE.tsv:2)), and confirmed the code replaces G81’s integrator with `solve_ivp(..., method="Radau")` while reusing G81’s downstream machinery ([replay_fixed_c1_radau.py](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/replay_fixed_c1_radau.py:41), [replay_fixed_c1_radau.py](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/replay_fixed_c1_radau.py:83), [replay_fixed_c1_radau.py](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/replay_fixed_c1_radau.py:95), [verify_nonradial_neighboring_rays.py](/tmp/udt_g82_review_EfMKGy/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/verify_nonradial_neighboring_rays.py:173), [verify_nonradial_neighboring_rays.py](/tmp/udt_g82_review_EfMKGy/udt_cmb_G81_nonradial_screen_covariance_2026-08-12/verify_nonradial_neighboring_rays.py:181)).

**Corrections/Caveats**

- No scientific correction to the saved G82 numerical result is required.
- One documentation caveat is real: [PREREGISTRATION.md](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/PREREGISTRATION.md:5) declares base `e36752ed5e01d45f46812cb154415683a353030f`, while [AUDIT_REPORT.md](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/AUDIT_REPORT.md:41) says preregistered at commit `88afa190`. The intake does not let me reconcile that, so I can verify only the sealed preregistration text boundary, not the claimed committed boundary.
- The hostile catch suite is useful but not complete on its face. Its explicit mutations cover 15 cases ([run_catch_proofs.py](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/run_catch_proofs.py:29), [CATCH_PROOF_RESULTS.json](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/CATCH_PROOF_RESULTS.json:2)), but it does not explicitly mutate partial tangent reversal, omitted `Z`/transpose/`A`/`B`, or changed endpoint/profile/deltas. In this sealed intake those routes are still materially constrained by the verified file hashes and the six-row source boundary in [SOURCE_MANIFEST.tsv](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/SOURCE_MANIFEST.tsv:1), but the catch harness alone does not directly demonstrate them.
- I did not credit the wider-repository claims in `REPOSITORY_GATES.json` as evidence for this review, because [verify_repository_gates.py](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/verify_repository_gates.py:45) plainly depends on paths and tests outside the sealed intake.

**Independently Recomputed Load-Bearing Numbers**

From the saved G82 matrices in [DERIVATION_RESULT.json](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/DERIVATION_RESULT.json:1) and the frozen G81 C1 matrices:

- `Radau vs DOP853` relative differences:
  `forward = 8.12971690308621e-12`
  `reverse = 9.459627107202695e-12`
  `rotated = 9.176648809164132e-12`
  `max = 9.459627107202695e-12`
- `Unrotated reciprocity residual = 1.139757402684705e-08`
- `Rotated covariance residual = 1.1582146620151037e-08`
- `Area reciprocity residual = 1.2229577572853145e-08`
- `Max coarse/fine FD relative change = 3.449865616964161e-08`
- `Z = 1.145643923738985`
- `Endpoint return max abs = 3.1179280077925364e-13`
- `Rotated endpoint return max abs = 2.068091520517762e-13`
- `Frequency product error = 2.4424906541753444e-15`
- `Max endpoint null abs = 6.183942247162122e-14`

All of those sit far below the preregistered `2e-4` gate ([PREREGISTRATION.md](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/PREREGISTRATION.md:53), [DERIVATION_RESULT.json](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/DERIVATION_RESULT.json:69)).

**Reproducibility Status**

Exact packaged CLI rerun in this sealed environment is `not permitted`: it fails on the first attempted write to `DERIVATION_RESULT.json` because the filesystem is read-only ([replay_fixed_c1_radau.py](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/replay_fixed_c1_radau.py:146)). I therefore cannot count an exact rerun as completed evidence.

I did complete two weaker but relevant checks:
- Independent algebraic recomputation from saved matrices matched the saved verifier values exactly, consistent with [INDEPENDENT_VERIFICATION.json](/tmp/udt_g82_review_EfMKGy/udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/INDEPENDENT_VERIFICATION.json:1).
- Executing the same numerical code path with writes suppressed in-process produced rendered JSON bytes identical to the sealed `DERIVATION_RESULT.json` (`2972` bytes, exact match). I treat that as supportive, but not as a literal exact packaged rerun.

**Exact Evidence Boundary**

Evidence I do claim:
- All 26 manifest-listed payload hashes inside the intake.
- The sealed preregistration text and status.
- Exact G81/G82 control-row identity.
- The G82 implementation path, including actual `Radau` use and absence of hidden DOP853 fallback in the reviewed code path.
- Independent recomputation from saved matrices.
- Saved-artifact verifier and catch-harness behavior as sealed files.

Evidence I do not claim:
- Existence or chronology of the declared preregistration commit beyond the text inside the intake.
- Independent validation of repository-wide facts asserted by `REPOSITORY_GATES.json`.
- Any physical profile, endpoint, scale, `Xmax`, SNe/CMB observable, `cmb_temp`, source, action, matter, bootstrap closure, signalling law, or future signal.

**Maximum Justified Conclusion**

`G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY`.

Nothing in this intake justifies promotion beyond that one frozen-control integrator-family sensitivity check. The scientific ceiling remains `DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS`.