# Curvature split audit run record

Date: 2026-08-12  
Branch: `grok`  
Base before preregistration: `2f64ae45`  
Question preregistration: `0e36e507`  
Control preregistration: `1907dbbf`  
Hardware: CPU only

## Commands

```text
python3 udt_curvature_principal_split_ownership_audit_2026-08-12/derive_founding_symbolic.py
python3 udt_curvature_principal_split_ownership_audit_2026-08-12/derive_curvature_split_atlas.py
python3 udt_curvature_principal_split_ownership_audit_2026-08-12/verify_curvature_split_independent.py
python3 udt_curvature_principal_split_ownership_audit_2026-08-12/verify_package.py
python3 udt_curvature_principal_split_ownership_audit_2026-08-12/run_catch_proofs.py
python3 udt_curvature_principal_split_ownership_audit_2026-08-12/verify_repository_gates.py
```

The production tensor route uses Torch automatic differentiation. The independent route is a
separate NumPy fourth-order finite-difference implementation. No ODE, GPU, fit, action, source,
bootstrap selector, or physical history calculation was run.

## Final output identities

```text
75565a06a9d99d845141cbfa2ccaa61a9bc3b3e45d19e6b253d2737eb9ebb301  FOUNDING_SYMBOLIC_RESULT.json
e7234b2eff7180e612118ace2d5f114ee90d393ce183c93cc9873597f206e9c6  CURVATURE_SPLIT_ATLAS.tsv
46b90e47423e95a6a448d68c9adb6d76daef67402639c36b14d55cbebd269ee7  DERIVATION_RESULT.json
320e22c68c1f79fd19403bc7977bd875fa4ec61b4fa97fc100ac1e718b3caedf  PRODUCTION_CURVATURE_TENSORS.npz
50a816bf663fc9dda672fc1e0dc4179e7999565f97fae12261403ced5f23a06e  INDEPENDENT_COMPARISON.tsv
57c193166228acb1fe0d9a26093dd9804780f2c67a1a451d19f89eb7b6227fb2  INDEPENDENT_VERIFICATION.json
da2b1ce0bfacedda98abeead3dcd31eaabddb6b01c238e38dfc7d0127354c7e1  INDEPENDENT_CURVATURE_TENSORS.npz
db1abb0e65c4d75d09cc19eca4f00800aeebc07ba03b81ab19ff3f3f0e8fd472  PACKAGE_VERIFICATION.json
18462157e9b062fb1059ee733aebe1a19cf8a4dd7c2c99e2c4e309834fb2c8c1  CATCH_PROOF_RESULT.json
8b3aefd86af935c8724d492e96d5d4f2918fe4cfa7199624ea8ef997c16f974c  REPOSITORY_GATES.json
```

Repository gates pass with `83` premise guards, six frozen manifests / `133` frozen package paths,
`1,114` current registry paths, `101` resolved frontier targets, and tests
`103 passed, 1 xfailed`. The seven protected stopped-draft paths remained untracked and unread.
