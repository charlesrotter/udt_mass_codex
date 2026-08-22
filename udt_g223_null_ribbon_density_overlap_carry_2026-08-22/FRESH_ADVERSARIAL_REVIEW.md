# G223 fresh adversarial review

Date: 2026-08-22

Reviewer: external Codex `gpt-5.4`, fresh ephemeral high-reasoning context, web disabled,
read-only sealed intake.

Sealed intake: `/tmp/udt_g223_review_bz0x52MZ`

`REVIEW_SCOPE.json` SHA-256:
`881177079dcc0328f9e794acfa1406537813b1b44e6bd9a71217d79987487fcd`

## Primary landing

```text
ACCEPT_WITH_REPAIRS
```

The reviewer independently accepted the bounded scientific landing and found no load-bearing
mathematical defect. Its separate no-write SymPy replay confirmed:

- the coordinate-free mixed pairing and its nondegeneracy;
- affine-null metric congruence and inverse clock weight;
- area and triple-overlap laws;
- the same-geometry closedness counterexample;
- the local/global scalar classification;
- the positive-diagonal G214 comparison;
- the G216 cross-ribbon vertical-gluing boundary;
- the stated premise and conclusion ceiling.

## Required repairs

1. **R1 — actual read-only replay.** `verify_package.py` launches production scripts that rewrite
   deterministic evidence before comparing hashes. This is byte-stable in a writable tree but
   fails in a truly read-only intake. Add a check-only execution path and make the registered
   verifier use it.
2. **R2 — nonvacuous independent fiber test.** The independent local-fiber loop asserts only
   `density == density`. Replace it with a genuine exact-rational check of
   `s(lambda_2)-s(lambda_1)=a(lambda_2-lambda_1)` for an affine fiber potential.
3. **R3 — intake containment proof.** The seven frozen sources are copied at repository-relative
   paths inside the intake root, but the verifier does not explicitly reject absolute or parent
   escaping manifest paths. Add that containment check and record the layout in the review scope.

The repairs are evidentiary. The bounded scientific landing is unchanged and must not be promoted
before a repair-only follow-up accepts them.

