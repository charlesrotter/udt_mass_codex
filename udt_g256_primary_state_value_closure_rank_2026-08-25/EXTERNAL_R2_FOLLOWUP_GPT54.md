# G256 R2 repair-only follow-up — gpt-5.4

Sealed intake: `/tmp/udt_g256_r2_followup_j2rejex1`  
`REVIEW_MANIFEST.tsv` SHA-256:
`a538d8820421ead88b789bcf3d124f58eda407f1f9b3f1654617be5ca6301b76`  
Returned response SHA-256:
`0e7d9b38beadd5b36d86b776c30dbf79c9d3a7eef75134e46158667c45209e6c`

## Grade

`G256_R2_SELF_CONTAINED_REPLAY_ACCEPTED__SCIENTIFIC_LANDING_RETAINED`

## Verification

- All `47/47` sealed payload rows matched their recorded SHA-256 and byte count.
- All `18/18` scientific source hashes matched.
- The package verifier, independent exact-Fraction replay, and hostile controls all exited zero in
  a minimal external runtime with no third-party Python packages mounted.
- The reviewer confirmed that the only remaining SymPy import is in the preserved original
  production script, which the sealed replay does not execute.
- The retained outputs were anchored dimension `N-1`, 43 graph trials, 220 cycle checks, 100
  angular trials, 14 Hermite trials, zero owned nonidentity value laws, a gated solver, and seven of
  seven hostile catches.

No remaining defect was found within the R2 certification scope. The bounded scientific landing
was retained unchanged.
