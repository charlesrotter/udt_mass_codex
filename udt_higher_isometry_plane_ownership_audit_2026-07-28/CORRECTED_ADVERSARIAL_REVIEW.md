PASS_WITH_CAVEATS

The corrected bounded conclusion is supportable. The package now explicitly separates family-wide coefficientwise robustness, fixed-profile constancy, universal selection, and full-orbit versus restricted-plane response. Generic fixed-metric uniqueness remains `OPEN`.

Exact replay:

- Production: 135/135 checks; 31 symbolic and 104 cap bases.
  - stdout: `1d65b56d5e9511bc349a9ae8bb1e1d54f9ab52349e4fca3b0d38b889bd72d30d`
  - stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Independent: 292/292 checks; 232 cap bases, all with exactly two free unoriented lines.
  - stdout: `a3808e1a41a27c6a3235c8d0b919f9714219d04b46f44691c63e383b787d580b`
  - stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Frozen sources: 26/26; identity SHA-256 `e85ad7db71c6041a1690973ba932a59db973253fdfedc3e40dd1a60b5977a482`.
- Mutation catches: 32/32, including reintroductions of generic fixed-metric promotion.
- Premise verifier: PASS.
- Repository tests: 70 passed, 1 expected failure.

All six listed initial-artifact hashes match `CORRECTION_LAYER.md`. The preserved review begins `REFUTED` and currently hashes to `21e99ac850291d189aaf578a47c238094e08d866dfa7c5c785e04408b25102cc`.

R01/R02 and `D3` are correctly restricted to principal orbits `b>0`; cap limits explicitly have `b=0` and do not use an invertible orbit Gram matrix. The smooth nonconstant-depth double-plane countercontrol and exactly-two-free-circle theorem remain valid. The response-degeneracy atlas is openly incomplete. No downstream physical selection is claimed.

Caveats:

1. `CORRECTION_LAYER.md` publishes no expected hash for `FRESH_ADVERSARIAL_REVIEW.md`, so its byte identity cannot be verified against that layer—only its presence, verdict, content, and current hash.
2. R07 still says `smooth_nonconstant_depth_and_round_controls_retain_multiple_planes`, although the constant-depth round row is explicitly unverified. The exact R06 countercontrol independently supports R07, but the surplus “round controls” wording should carry no evidentiary weight.
3. `verify_audit.py` regenerates artifacts before validating them and does not itself compare raw streams with `RUN_ENVIRONMENT.json`; its mutations mainly test fail-closed labels. Independent temporary-directory hash comparison supplies the missing replay check. In isolation, the verifier stopped exactly at `corrected_review_exists`.

Maximum supportable conclusion: within the bounded stationary descended higher-isometry family, universal unique plane selection is refuted by the exact smooth nonconstant-depth countercontrol. The principal-orbit algebra, toric two-free-line theorem, and family-identity robustness of `span(K,V)` are derived. Generic fixed-metric selection and the complete response-degeneracy atlas remain open. No physical branch, macro/micro assignment, carrier, action, source, density/bootstrap law, dynamics, or mass emergence is derived.