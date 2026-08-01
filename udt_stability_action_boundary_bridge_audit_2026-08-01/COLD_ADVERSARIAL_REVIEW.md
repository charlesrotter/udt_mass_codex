# Cold adversarial review

Date: 2026-08-01  
Context: fresh delegated review; no package edits, commits, or pushes by reviewer  
Final grade: `PASS_AFTER_REGISTERED_REPAIRS`

## Independent verdict

The primary outcome stands:

`PARTIAL_ANALOGIES_ONLY__F01_BOUNDARY_BRIDGE_OPEN`

The reviewer independently found no exact field, background, tangent, trace-domain,
boundary-one-form, boundary-Hessian, or second-germ map from C2/Bach, EH, or the proposed
two-stage route into F01.

## Reproduced evidence

- all 275 frozen source identities and SHA-256 values match base `3d136a8`;
- all 36 route gates were independently audited;
- C2/Bach: 9 blocks, 1 conditional analogy, 2 conditional premises, and currently inactive
  without explicitly reauthorized strong local CSN;
- EH: 10 blocks, 1 conditional analogy, 1 conditional premise;
- two-stage bridge: 12 blocks;
- the only P4/F01 `conditional-EH` occurrence is an object-identity warning, not a map;
- independent variation gives `Theta2 = u' v` and `Theta4 = u'' v' - u''' v`;
- adding `d(kappa u^2/2)/dx` preserves the bulk Euler equation while shifting the boundary
  one-form by `kappa u v` and the boundary Hessian by `kappa v^2`;
- corrected primary verifier passes 5/5 computed controls and 16/16 exercised catches;
- six frozen manifests, 127 members/133 package paths, current-premise verifier, and
  70 passed/1 xfailed all reproduce.

## Repairs found and closed

The initial cold pass found three evidence defects:

1. omitted current G04/G10 stamps and an obsolete `CURRENT` label on the July-18 selector audit;
2. a literal pattern that omitted the `EH` abbreviation;
3. tautological verifier controls that did not compute the variational identities.

The repair contract was transparently committed at `d06d5b7`. The final cold rerun confirmed the
corrected route applicability, literal census, SymPy calculations, and false-control mutation catch.

## Maximum conclusion

The registered action routes cannot presently supply F01's missing boundary germ. This is not a
universal no-action theorem, an action selection, a physical boundary derivation, or a stable-matter
result.

