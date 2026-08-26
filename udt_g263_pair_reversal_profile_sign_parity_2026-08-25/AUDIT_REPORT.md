# G263 audit report — pair reversal and signed-profile parity

Date: 2026-08-25
Grade: `EXTERNALLY_REVIEWED_WITH_REPAIRS_ACCEPTED__NO_REMAINING_R1_R2_R3_DEFECT`

## Primary landing

```text
PAIR_ARROW_REVERSAL_IS_EXACT_RECIPROCAL_INVOLUTION
__WHOLE_PROFILE_SIGN_CONJUGATION_IS_A_DISTINCT_METRIC_INVOLUTION
__SCALAR_DEPTH_INVERSION_SHARED_BUT_COMPLETE_CHANNEL_PARITIES_MIXED
```

## Result first

The earlier phrase “arbitrary positive profiles” meant arbitrary real `phi` on the regular branch
`f=exp(-2phi)>0`; it did not exclude negative `phi`.

G263 distinguishes two operations:

- swapping the endpoints of one supplied observer pair reverses `delta` while leaving the ambient
  metric fixed;
- changing the sign of the entire profile sends `f` to `1/f` and generally produces a different
  metric history.

The two operations can produce the same scalar depth inversion, but they are not the same full
geometric operation. Lapse, acceleration, geometric mass aspect, residuals, and angular channels
contain mixed even and odd profile-sign parts. The geometric mass aspect is not physical mass.

## Strong separator

G201's exact zero-tide family `f=1+C r^2` is sent by profile conjugation to
`f=1/(1+C r^2)`. Its conjugate angular channels are nonzero away from `Cr^2=0`. Therefore profile
sign conjugation does not preserve angular quietness and cannot be identified with endpoint-pair
reversal.

## Evidence

- preregistered and pushed at `43cf54d3` before outcome algebra;
- 10 frozen source hashes;
- 31 exact symbolic identities;
- 1,000 implementation-distinct rational cases spanning both signs of `phi`;
- 29,000 exact standard-library assertions;
- dependency-free sealed replay: 38,010 exact assertions over 1,000 cases, including shared scalar
  inversion, areal-sphere protection, both profile signs, and the zero-tide separator;
- 17/17 applied artifact mutations rejected, including all five fresh-review escape probes;
- 7/7 disposable altered-copy guards rejected the five reviewer escapes and corrupted evidence;
- fresh external review accepted the bounded scientific landing and requested evidence-only repairs;
- repair-only external follow-up: `ACCEPT_REPAIR`, no remaining R1-R3 defect;
- no observations, fits, GPU, source, action, physical-mass model, or protected input.

## Four gates

1. Preregistered: yes.
2. Full or bounded: exact local primary static-spherical second-jet classification only.
3. Independently verified: implementation-distinct algebra and fresh adversarial algebra yes;
   evidence repairs independently accepted.
4. Premises audited: yes; profile conjugation remains a diagnostic, not a physical symmetry.

## Maximum conclusion

The same pair has a native reversal-even reciprocal magnitude and reversal-odd direction. The two
signed whole-profile sectors are generally geometrically inequivalent and may behave very
differently. No universal angular loudness, valued history, mass/source law, or physical selection
is derived.

The repairs change no scientific formula or landing. The standard-library replay is exact algebra,
not an epistemically independent physical derivation. The preregistered repair-only follow-up
accepted R1-R3 with no remaining scoped defect.
