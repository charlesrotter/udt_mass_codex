# Preregistration — intrinsic defect, monodromy, and kernel-plane transport atlas

Date: 2026-08-02  
Branch: `grok`  
Preregistration base: `b58cdabd66be0a3e5c0b571b52fa4be5d91d38dc`

## Whole question

On the unchanged stationary, off-shell, complete `R x S3` ensemble, classify the intrinsic
transport data carried by the metric-derived projective line

```text
L_W=span(N),  N_flat=star(T_flat wedge W),
W=dPhi_contact wedge dSigma_contact,
```

after its exact continuation across the generic equatorial zero sheet. Determine:

1. whether the continued real line bundle has nontrivial projective `Z2` monodromy;
2. what local transverse turning occurs around every regular part of the three-circle defect graph;
3. what link data occur at the two shared poles and six equatorial crossings;
4. the induced metric connection and holonomy of the real line;
5. the induced Lorentzian connection of `E_W=span(T,N)` and whether its local holonomy data depend
   on the registered metric branch; and
6. which apparent winding data are orientation/frame conventions rather than intrinsic classes.

This is metric-led and outcome-neutral. It does not target a charge, particle, carrier, Hopf map,
nontrivial winding, quantization, or preferred branch.

## Frozen candidate and defect universe

All 18 parent candidates remain in `CANDIDATE_BINDING.tsv`. The full transport calculation is
performed only on the six parent-certified intrinsic nonzero candidates

```text
C04, C08, C09, C10, C16, C17.
```

The nine intrinsic-zero, two projector-blocked, and one degenerate candidates remain controls and
may not acquire a transport line.

The exact parent obstruction graph is fixed:

```text
D=C03 union C13 union C23,
C03: q1=q2=0,
C13: q0=q2=0,
C23: q0=q1=0.
```

The extended domain is `M=S3\D`. The equatorial sheet `q3=0` away from its six axis intersections
is in `M`; it is not deleted again. No profile, `lambda`, shear, twist value, point, loop family,
radius, or topology may be added or removed after outcome.

## Four different transport notions — kept separate

### A. Projective monodromy

The line gives a map from each loop in `M` to `RP2`. Its intrinsic line-bundle monodromy is the
class in `pi1(RP2)=Z2`, equivalently the first Stiefel-Whitney class `w1(L_W)`. A visually repeated
turn inside an `RP1` subset is not automatically nontrivial in `RP2`.

### B. Local transverse vector turning

At a regular defect edge, linearize a nonzero representative in the oriented normal plane. If the
normal derivative has rank two, its normalized image may have a local vector index. The signed
index is reported only relative to explicitly registered domain/image orientations; orientation or
representative reversal must remove any claim that the sign is canonical. The magnitude may remain
intrinsic if proved invariant.

### C. Projected connection of the real line

For a local unit representative `n`, define

```text
nabla^L_X n = Pi_L(nabla_X n).
```

This is not the same as ambient turning `(I-Pi_L)nabla_X n`. A global unit lift would make the
metric line connection trivial while leaving ambient turning nonzero or singular. Both outcomes
are retained.

### D. Induced Lorentzian connection of the kernel plane

On `E_W=span(T,n)`, use the projected Levi-Civita connection. In the orthonormal frame `(T,n)`, its
`so(1,1)` one-form is

```text
omega_E(X)=g(n,nabla_X T).
```

The production route must independently derive whether the parent screen-projected clock two-form
implies

```text
omega_E=(q_T/2)(n3 theta2-n2 theta3),
Omega_E=d omega_E.
```

This displayed formula is a preregistered test, not an accepted result. Since `SO+(1,1)` is
abelian, infinitesimal and contractible-loop holonomy is controlled by `Omega_E`; finite path
integrals are not inferred from point samples.

Full four-dimensional Levi-Civita holonomy is a different tangent-bundle object. It may be used as
a consistency check but may not be called defect-line holonomy.

## Exact loop and link universe

`LOOP_UNIVERSE.tsv` freezes:

- all six regular graph edges (the north/south arc of each great circle);
- the six equatorial axis crossings, which are regular points of `D` after the equatorial sheet is
  filled;
- the north and south pole links, each an `S2` punctured by six incident rays;
- the candidate five-generator first-homology class of the graph complement, to be verified; and
- the seven inherited exact stereographic anchors for regression, with p1 and p2 frozen for exact
  connection-curvature evaluation.

Regular-edge results must be derived for a symbolic base point, not extrapolated from one sample.
Pole-link claims must retain all six punctures. No loop is accepted or rejected because it looks
particle-like or has a desired winding.

## Registered algebraic and differential tests

1. Rebuild the parent factorization `N=q3 L_g f` up to a globally nonzero scalar and define the
   candidate lift `N_tilde=L_g f` on `M`.
2. Prove or refute that `N_tilde` is globally nonzero on `M`. Only such a proof may set `w1=0`.
3. Recompute every regular-edge transverse derivative, its rank, and its orientation-dependent
   determinant.
4. Recompute the quadratic pole-link leading map and every puncture meridian.
5. Distinguish the `RP2` loop class from any `RP1` traversal or oriented-image-plane index.
6. Derive the projected real-line connection and ambient turning separately.
7. Derive `omega_E` from the registered metric and `F_T`, then compute exact `Omega_E` components at
   p1 and p2 for all six candidates. These points establish only local existence/difference, not a
   global nowhere-zero theorem.
8. Test branch equality/difference using exact expressions, not decimal thresholds.
9. Reverse orientation and all representative signs; rotate the screen coframe; verify which data
   are invariant, conjugated, sign-reversed, or convention-dependent.

## Controls, certification, and falsification

- exact CPU/SymPy algebra only; no GPU, fitting, ODE/PDE, relaxation, or time evolution;
- source blobs are frozen before calculation;
- all objects in `OBJECT_UNIVERSE.tsv` receive a status;
- every mutation in `FALSIFICATION_CONTRACT.tsv` is exercised and typed honestly;
- a fresh read-only adversarial implementation must rebuild the global lift, monodromy, regular
  edge and pole-link data, and kernel-plane connection formula without importing production code;
- any uncomputed finite-loop integral remains `OPEN/PATH_DEPENDENT`, never supplied from curvature
  samples.

## Maximum allowed conclusion

At most: a verified bounded topological/connection/turning atlas for the intrinsic line and kernel
plane on the frozen stationary profile ensemble, including any exact triviality, nontriviality,
singularity, or branch dependence actually proved.

No topological charge, quantization, carrier, Hopf section, particle, force, substrate ontology,
preferred branch, field equation, dynamics, action, source, boundary, density/bootstrap value,
`X_max`, matter, mass, stability, phenomenology, or canonization may follow.
