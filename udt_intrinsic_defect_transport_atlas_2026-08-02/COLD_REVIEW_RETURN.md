# Fresh adversarial review return

Grade: **PASS_WITH_CAVEATS**

The reviewer independently reconstructed the load-bearing algebra before reading the production
script and made no repository edits.

It reproduced:

- the two-vertex/six-edge defect graph and
  `H1(S3 minus D;Z) isomorphic to H^1(D;Z) isomorphic to Z^5`;
- `det(L_g)=1/(F^2 u)>0`, the global nonzero lift, `w1=0`, and trivial projective meridians;
- all three symbolic regular-edge matrices and determinants `3q0^2,2q1^2,-6q2^2` on `S3`;
- vector-index magnitude one, two local `RP1` traversals, and trivial `RP2` class;
- the pole leading map `s(2yz,3xz,-xy)` and exactly six link punctures;
- flat projected real-line connection versus distinct `1/rho` ambient turning;
- the pre-cancellation kernel-plane formula

  ```text
  omega_E=-n(phi)theta0-(t0/2)(n3theta2-n2theta3),
  t0=-2a/(sqrt(u)F),
  ```

  and its reduction to the preregistered formula because
  `i_n(dphi wedge dSigma)=0` forces `n(phi)=n(Sigma)=0`;
- a separate coordinate-Christoffel value for `C08/p1` to better than `2e-61`;
- all 12 point-curvature certificates, four distinct registered screen/`lambda` coordinate triples
  at each point, and exact `4x/5x` twist scaling.

The review caught and required repair of:

1. an early draft `OBJECT_STATUS.tsv` whose row count was correct but whose object identities had
   shifted relative to the preregistered universe;
2. a vacuous first mutation harness that flipped per-gate booleans instead of mutating evidence and
   claims;
3. Alexander-duality, leading-turn, anchored-frame, and sampled-coordinate wording;
4. the distinction between consistent screen-`O(2)` invariance and the inhomogeneous transformation
   of a connection under an arbitrary `SO(1,1)` frame change.

The production record and verifier were repaired before banking. The caveats are remaining scope,
not algebra failures: the global zero set of `Omega_E`, finite kernel-plane holonomies, pole turning
asymptotics, and full Levi-Civita holonomy remain open. Nothing derives charge, carrier, Hopf
structure, substrate physics, or a preferred branch.
