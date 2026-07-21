# Preregistration Correction — Exact Independent Anchor Set

Date: 2026-07-21

This correction is committed before the builder or verifier is implemented or run. The original
preregistration requires an independent anchor set but does not enumerate it. The following exact set
controls that requirement:

- carriers:
  `R00_1,R05_1,R10_1,R15_1,R00_3,R05_3,R10_3,R15_3,V001,V006,V011,V016`;
- masks: `M0,M1,M3,M7,MF`;
- contexts: all eight registered bank/point contexts;
- total original anchors: `12 * 5 * 8 = 480`;
- nonlinear transformed anchors: both preregistered maps for all 480 originals, total `960`.

The independent verifier must implement its own phi-Hessian chain rule, curvature-generator
construction, algebra and gradient-orbit closure, bivector simplicity test, and nonlinear jet
transformation. It may read the builder's output rows only after computing each corresponding anchor.

For clarity, a reported *central block* is obtained from the center of the full operator commutant.
All real metric-self-adjoint minimal central projectors are retained. A `2+2` count includes every
rank-two union of minimal central blocks, modulo complementary duplication. Noncentral invariant
subspaces may be reported as an ambiguity, but cannot be promoted to a unique split.

No candidate family, tolerance, chart jet, maximum conclusion, or other requirement changes.
