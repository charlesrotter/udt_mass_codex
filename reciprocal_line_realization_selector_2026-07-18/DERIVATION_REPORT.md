# Reciprocal internal-pair/spacetime-line realization selector — derivation report

Date: 2026-07-18  
Branch: `codex/reciprocal-line-realization-selector-2026-07-18`  
Required parent: `9e08bccaf6a2ad9d7b464850560bc5f01d8349bf`  
Preregistration commit: `9dd9d9f`

## Result

The preregistered outcome is:

```text
NO_UNIVERSAL_LOCAL_METRIC_ONLY_SELECTOR_REALIZATION_MAP_OPEN
```

The internal reciprocal conversion pair remains `DERIVED_KINEMATIC` under its exact premise stamps.
It is not yet a spacetime line field. No universal pointwise or finite-order local natural rule can
select a time/parallel line pair from one metric in the preregistered unrestricted Lorentz class: at
a flat metric jet, the full Lorentz stabilizer fixes the metric but fixes no one-dimensional
subspace. The current UDT off-shell domain remains open and supplies no derived restriction that
excludes this jet; a later justified restricted domain would be a separately conditional route.

This is a bounded naturality theorem. Curvature eigendirections on nondegenerate strata, an
independently derived scalar gradient, a static Killing field, a separately supplied spacetime
endomorphism, and finite-cell/nonlocal constructions remain conditional or open. Their present
failure to close does **not** derive a required auxiliary field or full coframe.

The smallest genuinely missing object is a native realization/reduction **rule class** connecting
the internal comparison labels to ordered causal spacetime line/projector data, including its
diffeomorphism and Common-Scale laws, degeneracy handling, and finite-cell/global compatibility.
Full reciprocal metric realization additionally needs weights, relative normalization, and the
meaning/preservation of the pairing. The current foundation supplies neither layer, so the
variation domain and two-stage C-squared/EH bridge remain open.

## T1 — provenance and type census

C1 uses

```text
q=(c dt,dr)^T,
P(phi)=diag(exp(-phi),exp(phi))
```

as one faithful dimension-matched formalization of the internal dual conversion pair. Its status
ledger explicitly retains the local Lorentzian quadratic readout, CSN representative, sign/unit of
`phi`, and reciprocal spatial-slot identification as separately non-derived. The accepted prior
selector therefore calls this pair an internal comparison and not a derived global spacetime
coframe.

The type gap matters. For provisional bookkeeping only, let `E -> M` denote what an internal
rank-two comparison bundle with labeled conversion lines would have to be. C1 does **not** derive
this smooth bundle, its transition functions, or a global coframe: it supplies the algebraic
faithful representation in adapted temporal/radial coframe notation. Spacetime line data live in
`TM` or `T*M`. Matching the number of components does not define a bundle map. A realization could
use a rank-two injection or two projectors such as

```text
s: E -> T*M,
s(E_time)=L_time,
s(E_length)=L_parallel,
```

together with causal character, covariance, CSN behavior, degeneracy and branch rules, and
global/boundary compatibility. That suffices for line selection. Carrying the complete reciprocal
metric readout additionally requires weights, relative normalization, and a rule for the internal
pairing. A full tetrad is sufficient but stronger than either minimal layer.

## T2 — pointwise Lorentz-isotropy theorem

Suppose a pointwise diffeomorphism-natural rule `F` assigns a line `F(g) subset V` to each Lorentz
inner product on a four-dimensional vector space. At

```text
eta=diag(-1,1,1,1),
```

naturality requires `F(eta)` to be invariant under every member of the stabilizer `O(1,3)`.

Invariance under the full spatial rotation subgroup first forces any invariant line to be the time
axis: no nonzero spatial vector spans a line invariant under every rotation, and a vector with both
time and spatial parts also fails. But the exact boost

```text
Lambda(beta) = [[cosh(beta),sinh(beta),0,0],
                [sinh(beta),cosh(beta),0,0],
                [0,0,1,0],
                [0,0,0,1]]
```

satisfies `Lambda^T eta Lambda=eta` and sends

```text
e0 -> (cosh(beta),sinh(beta),0,0).
```

The real zero set of the wedge minor `sinh(beta)` is exactly `{0}`. Thus every nonzero real boost
moves the image outside `span(e0)`. Hence
the standard Lorentz representation has no invariant one-dimensional subspace. No natural
pointwise metric-only timelike, spacelike, or null line selector exists. `S0` is
`REFUTED_IN_CLASS`.

## T3 — universal finite-jet extension

A universal finite-order local natural selector on the unrestricted Lorentz class, evaluated on a
flat metric jet, must also be fixed by the flat jet's Lorentz isotropy. Every curvature tensor and
every finite covariant derivative of curvature vanishes there. The same no-invariant-line result
therefore applies.

The current ledger explicitly leaves the globally trivial `phi identically 0` representation
mathematically allowed, but `phi=0` by itself does not prove flatness. More importantly, the UDT
off-shell domain is `OPEN`: it supplies no native restriction excluding the independent flat
SR-continuity anchor from the preregistered unrestricted Lorentz class. Observed nonzero dilation in
the realized universe does not itself provide such a domain theorem.

This closes only universal smooth finite-order metric-only selection in S1. A curvature
construction defined on a justified generic open stratum, a future native domain that excludes the
flat jet, and a nonlocal/global construction are not covered.

## T4 — coframe and reciprocal-endomorphism challenges

### A metric does not uniquely factor into a coframe

If `g=e^T eta e`, then for every local Lorentz transformation `Lambda`,

```text
(Lambda e)^T eta (Lambda e)=e^T eta e.
```

The executable boost above supplies two distinct coframes with the same metric. Thus the phrase
“metric coframe” does not select the internal time/length labels without a Lorentz-gauge reduction,
projector, or other native rule.

### Strongest declared endomorphism

Grant a spacetime two-plane and endomorphism

```text
D=diag(exp(-phi),exp(phi)).
```

For `phi != 0`, its distinct eigenvalues select two eigenlines. A valid causal use must additionally
declare its spacetime embedding, suitable self-adjointness/causal eigendata, and transformation law.
The endomorphism is precisely extra/derived structure whose origin is at issue. At `phi=0`, `D=I`;
every line is an eigenline pointwise. Surrounding data or derivatives might continue the lines, but
that is a new branch/continuation rule. The candidate is `CONDITIONAL_STRUCTURED`, not universal
closure.

## T5 — curvature, gradient, and Killing challenges

### Curvature eigenlines

A Ricci, Weyl-derived, or other curvature endomorphism can select a line on a declared stratum with
a unique real simple eigenvalue of the required causal type. That is a genuine metric-only,
derivative route on that stratum. It fails to be universal at flat, conformally symmetric, or
eigenvalue-degenerate configurations, and it needs an operator choice, CSN law, branch ordering,
regularity, and continuation across degeneracy. Current Reciprocity selects none of these. Status:
`CONDITIONAL_STRATIFIED`.

More strongly, generic four-dimensional Weyl principal-null or Cartan-invariant constructions can
select finite line sets or frames on suitable algebraically nondegenerate strata. They still require
ordering and axis reconstruction and fail or branch at type-O/flat and other degenerate loci. Their
existence is an explicit reason not to extend the S1 no-go beyond its universal full-domain scope.

### Gradient of reciprocal depth

If an independently defined spacetime scalar `phi` were supplied, `g^{-1}(d phi)` would define a
direction wherever nonzero. Current `phi=(1/4)log(b/a)` is instead a conditional readout **after**
the paired spacetime slots exist. Using its gradient to define those slots is circular unless a
separate spacetime definition of `phi` is derived. Regions where `d phi=0` leave no direction; these
include the globally trivial `phi identically 0` branch, not a mere zero level set whose normal
derivative may be nonzero. Status:
`CIRCULAR_OR_EXTRA_FIELD`.

### Static Killing line

A selected hypersurface-orthogonal timelike Killing line can supply the time direction in a static
sector. Staticity is not a universal consequence, and symmetric metrics can have multiple Killing
directions. A Killing field for `g` need not remain Killing for `Omega^2 g` unless the scale is
constant along its flow; otherwise a conformal-Killing formulation or selected representative is
required. Normalization remains CSN/representative data. The route does not extend to the time-live
domain without a new theorem. Status: `CONDITIONAL_SECTOR_ONLY`.

## T6 — Common-Scale Neutrality

Under `g -> Omega^2 g`,

```text
g(v,v) -> Omega^2 g(v,v).
```

The null cone and the causal type of a nonzero vector are preserved. An already-declared line
distribution is also unchanged as a subbundle, while a unit vector representative rescales. Thus a
conformal class can carry a selected causal line without assigning its absolute normalization, but
it does not choose one line among the Lorentz cone or among spatial directions. Time orientation, if
separately supplied, selects a cone component rather than a unique timelike line.

A supplied two-dimensional Lorentzian plane is a strongest conformal counterexample: its induced
conformal structure carries an unordered pair of null lines. But the plane itself, ordering, and
reconstruction of the reciprocal time/parallel axes are not selected by the four-dimensional
conformal metric. This is a valid S3 ingredient, not an S0/S1 universal line pair.

## T7 — finite-cell boundary challenge

For a declared smooth spatial mirror hypersurface, the metric/conformal geometry supplies a normal
**line** at the seal; changing the representative changes a unit normal but not the line. In current
C1 this conclusion is limited to the binding static-`phi` seal structure already using a normal
derivative. The orthogonal tangent hyperplane is three-dimensional and does not supply a unique time
line.

Nor does a seal normal determine a unique bulk parallel line among unrestricted smooth extensions.
In a sufficiently small boundary collar `u >= 0`, let `x` be spacelike tangential and choose
`epsilon` bounded so the examples retain the desired causal character. Compare

```text
N0 = partial_u,
N1 = partial_u + epsilon u (L-u) partial_x.
```

Both equal the boundary normal at `u=0`, but at `u=L/2` they differ by
`epsilon L^2/4 partial_x`. Infinitely many such smooth extensions exist. A geodesic-normal,
spectral, variational, or other nonlocal extension might be selected, but C1 supplies none; a metric
representative, caustics/cut loci, topology, corners, and global branches would then need audit.
The example does not challenge uniqueness inside an additional fully specified extension
prescription.

The seal-normal route is therefore `CONDITIONAL_BOUNDARY_LOCAL`; its bulk extension is
`UNDERDETERMINED`.

## T8 — realization-map closure

The least missing object is not automatically a full coframe or an independently physical
auxiliary field. It is a native realization/reduction rule class. Minimal ordered line selection
and full reciprocal metric realization should not be conflated; across the two layers the audit
exposes seven facets:

1. internal domain and spacetime codomain;
2. diffeomorphism and CSN transformation law;
3. ordered causal line/projector selection;
4. weights, relative normalization, and preservation/meaning of the internal pairing for the full
   metric readout;
5. handling of globally trivial/critical and other eigen/gradient degeneracies;
6. finite-cell boundary-to-bulk compatibility;
7. global existence, topology, continuity, and branch selection.

A rule could be a bundle injection, a pair of projectors, a derived endomorphism, a boundary/nonlocal
construction, or a restriction to a justified sector. The theorem does not choose among them.

## T9 — action and variation implications

The selector result does not determine whether any eventual line data are dependent readout,
gauge-fixed geometry, independent varied fields, or boundary/global functionals. Therefore it does
not select the off-shell variation domain and cannot decide between:

- conditional pre-scale `C^2`/Bach variation;
- conditional post-scale EH variation; or
- a two-stage bridge.

Those branches retain their accepted statuses. No carrier, native matter source, finite-cell
differentiable action, charge, or mass follows.
The possible shared-static-source route also remains `OPEN`; a line selector alone supplies none of
its common-action, generator, normalization, solution, or controlled-limit obligations.

## T10 — bounded completeness map

| Criterion | Covered here | Still open |
|---|---|---|
| Fields | Internal pair distinguished from spacetime data | Native realization and field/variation status |
| Naturality | S0 and universal S1 closed by Lorentz isotropy | Generic-stratum, nonlocal, boundary selectors |
| CSN | Cone/line versus normalization separated | Native transformation/representative rule |
| Degeneracy | Flat and globally trivial/critical branches exposed | Continuation and global branch theorem |
| Boundary | Seal-local normal and extension nonuniqueness | Complete boundary geometry/action and bulk rule |
| Topology | No topology assumed | Global line/coframe existence and sectors |
| Action/equations | No dynamics inferred | Complete action, Ward identities, source |
| Stability | Not used | Stability of any completed realization |
| Regime | Exact local theorem plus bounded candidates | Material/post-scale matching |

## Mechanical result

`derive_reciprocal_line_selector.py` verifies 11 exact algebraic anchors with SymPy 1.13.1: the
boost preserves `eta`; the real zero set of `sinh(beta)` is `{0}`, so every nonzero real boost moves
the rotation-fixed time line; Lorentz-related coframes give the same metric; the reciprocal
eigenvalue gap vanishes exactly at `phi=0`; conformal rescaling preserves the null cone; flat
curvature and constant-`phi` gradient fixtures are degenerate; and two boundary-normal extensions
agree at the seal while differing in the bulk.

The finite-jet conclusion is the analytic naturality/isotropy proof in T3. The executable flat-jet
anchor checks its Lorentz stabilizer and zero curvature data; it does not pretend to enumerate all
natural differential operators.

The result is CPU-only, carrier-free, and action-free. It changes no frozen source, research
artifact, current registry, or navigation control, and it does not update `grok`.
