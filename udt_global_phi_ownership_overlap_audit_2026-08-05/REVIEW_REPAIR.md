# Adversarial-review repair

Date: 2026-08-05

The fresh `gpt-5.4` review returned `ACCEPTED_WITH_REPAIRS`. It accepted the local factorization,
overlap/coboundary, scalar, affine/reversal, query, path, premise, and termination claims. It found
one concrete harness defect: both variable-reference seam checks compared a constructed expression
to the identical expression, and verifier catch `C14` merely flipped that stored boolean.

## Repair

Both implementations now construct separate endpoint data:

```text
E_-, bar_theta_-, theta_-=E_- bar_theta_-,
E_+, bar_theta_+, theta_+=E_+ bar_theta_+,
L_seam=theta_+ theta_-^-1,
R_seam=bar_theta_+ bar_theta_-^-1.
```

They then apply unequal endpoint shifts `K_- != K_+`, reconstruct the shifted endpoint reference
coframes independently, and verify all of:

```text
R'_seam = K_+^-1 R_seam K_-,
R'_seam != R_seam,
E_+ = L_seam E_- R_seam^-1,
E'_+ = L_seam E'_- (R'_seam)^-1,
theta'_-=theta_-,
theta'_+=theta_+.
```

The saved witness now contains the distinct before/after reference seam matrices and the unchanged
physical transition. Verifier catch `C14` mutates the saved after-seam to equal the before-seam and
requires the witness guard to reject it.

## Post-repair exact counts

- production: 54/54 checks;
- independent standard-library reconstruction: 46/46 checks;
- verifier: 32/32 checks;
- exercised mutations: 16/16 rejected.

No premise, candidate route, source set, classification, or conclusion wording changed.
