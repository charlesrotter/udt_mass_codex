# G270 fresh external adversarial review

Date: 2026-08-26
Reviewer: external Codex `gpt-5.4`, high reasoning, zero-context, sealed read-only intake
Intake: `/tmp/udt_g270_review_mhgdqfco`
Scope SHA-256: `f5372cd46a427dc995159c973e4dce32b455f13e83b8ba723f146aeaeab14038`
Manifest SHA-256: `d6327dbab1eae8c230fa2fedd93e38a0900fd5760bb271a3a2aeb9f90c52b812`

Verdict: `ACCEPT_WITH_REPAIRS`

## Findings

1. The mutation gate exercised a hand-written claim dictionary, not either derivation
   implementation. It was a valid consistency check but was described too strongly as adversarial
   mutation assurance.
2. The smooth-ribbon automated checks covered the axis only. The written continuity argument for a
   regular off-axis neighborhood was sound, but the packaged automation did not directly exercise
   that neighborhood.

## Scientific adjudication

The reviewer accepted review items 1--8 without scientific repair:

- the intrinsic-versus-bilocal typing is coherent;
- the exact flat family supplies unit `U`, orthonormal `N=rk-U`, and the normalized null direction;
- `h_sigma` is independent of `w` and Lorentzian;
- completed normalization gives `m=1/r` and the constant `h_s`;
- `||W||^2=w^2` is the transported mismatch, not Jacobi area;
- the fixed-`r` planar/tilted pair separates intrinsic pullback from `W`;
- the smooth-ribbon construction is mathematically valid;
- the full supplied realization evaluates `W` without selecting a physical population or history.

Only evidence item 9 requires repair. The reviewer independently verified all 32 manifest entries
and ran the four registered no-write replays successfully with recorded artifacts unchanged.

