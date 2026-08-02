# Preregistration — broader-coframe exact/harmonic response audit

Date: 2026-08-02  
Base: `aef26451c9006a7bb43a9faed9c2533cb7a8053b`  
Mode: metric-led exact CPU audit; no fit, density scan, action, matter, or GPU work

## Whole question

The preceding FC07 audit separated the founded exact depth form `dphi` from the primitive harmonic
base form `alpha` in a stationary, torus-invariant, lower-triangular coframe. This audit asks two
bounded questions without presupposing a desired bridge:

1. Does that separation remain a theorem when the spatial metric, screen dependence, and
   upper-right ruler/screen mixing are released?
2. What exact, first-derivative one-form responses are already available when the founded depth
   scalar `phi` and the metric angular log-area scalar `sigma=log(D/D0)` are allowed to act jointly?

“Available” means constructible and covariantly typed inside the stated family. It does not mean
selected as a UDT law, equation, source, or bootstrap return.

## Bounded regime

The audit has three deliberately separate layers.

### U — universal compact-Hodge layer

- any connected, compact, oriented, boundaryless Riemannian spatial three-cell `(Sigma,q)` with
  `b1=1`;
- arbitrary smooth single-valued scalars `phi` and `sigma`;
- the exact/coexact/harmonic Hodge decomposition of one-forms;
- no chosen coordinates, monodromy, action, or field equation.

### X — explicit upper-right FC07 controls

- the registered `M_MINUS_IDENTITY` mapping torus, with normalized base coordinate `s` and fiber
  coordinates `(y1,y2)`;
- the positive spatial coframe

  ```text
  eta1 = ds + c,
  eta2 = dy1,
  eta3 = dy2,
  q = eta1^2 + eta2^2 + eta3^2;
  ```

- two globally descending, non-torus-invariant upper-right controls: an exact connection
  `c=dpsi` and a mean-zero coexact/nonclosed connection
  `c=epsilon sin(2 pi y1) dy2`;
- exact descent, determinant, Hodge, closure, and cohomology tests.

These controls falsify universal statements but do not exhaust all upper-right coframes, all four
FC07 monodromies, full clock/screen upper-right mixing, or all complete spacetime metrics.

### O — minimal depth/angular “orchestra” layer

- the established oriented screen-split family where `D=sqrt(det h)>0` is a global scalar density
  under the supplied unimodular descent;
- `sigma=log(D/D0)`, with arbitrary constant reference `D0>0` retained only to type the logarithm;
- the complete first-derivative, field-degree-at-most-one scalar-built response basis

  ```text
  dphi, dsigma, phi dphi, sigma dsigma,
  phi dsigma + sigma dphi,
  lambda = (phi dsigma - sigma dphi)/2.
  ```

- arbitrary smooth finite `phi` and positive `D`, including base-only and genuinely
  non-torus-invariant controls.

The basis restriction is a bounded algebraic census, not a claim that connection/curvature permits
no higher-order or nonpolynomial response.

## Physical-choice ledger

The detailed ledger is `PREMISE_LEDGER.tsv`.

- Founded `phi`, the reciprocal clock/ruler pair, observer-frame Reciprocity as naturality, and
  observed `c_E` are `pinned-by-THEORY` in their registered scopes.
- The compact Hodge theorem is mathematics, not a physical selector.
- The FC07 topology, stationary slice, explicit upper-right controls, screen split, response degree,
  and `D0` are `CHOSE` bounded controls.
- `phi`, `D`, and the upper-right one-form are free-and-explored inside those controls.
- Strong CSN remains inactive. Mirror completion, J07/J11, `X_max` closure, bootstrap density,
  action, carrier, source, scale closure, and time-live dynamics are excluded/open.

## Preregistered candidate outcomes

The audit preserves all of these outcomes:

1. universal exact/harmonic orthogonality survives every broadened metric;
2. upper-right structure breaks the pointwise ruler/harmonic line ownership while leaving only a
   cohomological relation;
3. the minimal two-scalar basis supplies no non-exact response;
4. exactly one minimal alternating cross-sector response survives modulo exact forms;
5. one or more responses exist but are split-relative, unselected readouts rather than laws;
6. no broadened response licenses density bracketing.

## Certification and falsification contract

The primary derivation must:

1. prove `Pi_H(df)=0` for arbitrary smooth `f` and arbitrary compact boundaryless `q`;
2. prove the same for every single-scalar response `F(phi)dphi` admitting a scalar primitive;
3. derive, rather than assume, the exact/exact-plus-cross classification of the complete registered
   six-element minimal response basis;
4. test reference shifts `phi -> phi+A` and `sigma -> sigma+B` and distinguish exact changes from
   harmonic changes;
5. derive `d lambda` and exhibit both a nonzero base-loop harmonic witness and a non-torus local
   curl witness;
6. verify global descent and positive nondegeneracy of both upper-right FC07 controls;
7. verify the exact control gives an exact ruler deviation and the nonclosed control gives a
   non-harmonic ruler even when the primitive harmonic base form remains `ds`;
8. separate cohomology, Hodge projection, pointwise projector ownership, and physical selection;
9. retain the no-selection and no-density outcomes unless a current premise supplies an equation.

An independent implementation may use only the standard library and direct exterior-calculus,
Fourier, and matrix identities; it must not import the primary derivation. Exercised semantic
catch-proofs must reject at least:

- an exact one-form assigned a nonzero harmonic projection;
- a single-scalar integrating-factor identity promoted to a bridge;
- the alternating cross response deleted from the minimal basis;
- a reference shift treated as a physical change;
- a nonclosed upper-right ruler called harmonic;
- the upper-right witness claimed for all FC07 monodromies or all coframes;
- a split-relative screen scalar called fully frame-independent;
- an available response called a selected UDT equation;
- a density scan launched from a readout without a return equation.

## Maximum allowed conclusion

At most this audit may derive universal compact-Hodge obstructions, exact upper-right countercontrols,
and a bounded minimal cross-sector response motif already constructible from metric scalars. It may
say whether the preceding separation and ownership claims are robust, weakened, or refined.

It may not derive or select a complete coframe, field equation, action, source, carrier, bootstrap
fixed point, density window, `X_max`, mass, stability theorem, or physical branch. No density scan,
GPU work, time-live solve, canonization, or repository reorganization is authorized.
