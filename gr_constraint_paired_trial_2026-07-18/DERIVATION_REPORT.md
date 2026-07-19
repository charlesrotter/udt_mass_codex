# GR-constraint paired trial — derivation report

Date: 2026-07-18
Branch: `codex/gr-constraint-paired-trial-2026-07-18`
Preregistration commit: `3e1d8a3`
Authority: bounded selector trial; not canonization

## Ruling

Yes: GR-origin constraints can be adopted one at a time as explicit trials and retained only while
they pass UDT compatibility and non-bundling tests. In this first paired trial:

- four dimensions remain `INHERITED`;
- bulk diffeomorphism covariance is `RETAIN_TRIAL_CONDITIONAL`; the full active diffeomorphism
  group compatible with the mirrored boundary is `UNRESOLVED_TRIAL`;
- unrestricted variation of every field a branch declares is `RETAIN_TRIAL` as a transparent
  off-shell discipline;
- the finite mirrored cell remains `CANONIZED_BINDING` and replaces GR's spatial-infinity boundary
  ontology;
- neither metric-only fields nor metric-plus-auxiliary-constraint fields are selected.

The preregistered top-level result is `BOTH_CONDITIONALLY_ADMISSIBLE`. This does not mean that two
complete UDT theories have been built. It is a bounded non-exclusion result: exact category-A
witnesses show both field censuses can inhabit the common bulk symmetry/CSN class and share a finite
reciprocal-cell root, while the current UDT foundation excludes neither. Covariance does not decide
between them. Neither witness is a nontrivial realized universe or a native action.

Locality, derivative order, invariant inventory, EH, `C^2`, source, normalization, and finite-cell
boundary completion were deliberately not adopted. A GR constraint earns no companions merely by
being familiar.

## T1 — bundle and provenance audit

The tested GR inheritance was split into independently reviewable statements:

| Candidate | Trial treatment | What was not bundled with it |
|---|---|---|
| Four-dimensional arena | `INHERITED` from the current UDT record | No field census, action, or dynamics |
| Diffeomorphism covariance | `TRIAL_CONDITIONAL` | No locality, metric-only ontology, derivative order, EH/Lovelock theorem, asymptotic charge, or source |
| Unrestricted variation | Applied only to every field declared within each branch | No assertion that the declaration itself is correct |
| Finite mirrored cell | Binding UDT arena | No GHY/ADM import and no completed finite-cell boundary action |

Pre-July-1 material was not used as affirmative physics. The post-July adjudication and selector
audit supply the controlling status: metric-only, multiplier, hard-constraint, and readout routes
remain live, while complete action and boundary charge remain open.

## T2 — exact multiplier reaction

For ordinary coordinates `x=(x,y)`, compare

```text
Branch A: S_0(x),                         delta x unrestricted
Branch B: S_B(x,lambda)=S_0(x)+lambda C(x), delta x and delta lambda unrestricted.
```

Branch A gives

```text
grad S_0 = 0.
```

Branch B instead gives the Karush-Kuhn-Tucker/Lagrange-multiplier equations

```text
grad S_0 + lambda grad C = 0,
C = 0.
```

The second term is the normal constraint reaction. Dropping it or the multiplier equation changes
the off-shell problem. Equality at a realized root requires more than `C=0`: the reaction must
vanish or a theorem must prove it redundant.

In a field theory the same structure is schematic:

```text
S_B[g,lambda] = S_0[g] + integral_cell sqrt(|g|) lambda C[g],
E_g[S_0] + H_C[lambda] = 0,
C[g] = 0,
```

where `H_C` is the metric reaction obtained from varying the entire constraint density, including
its integrations by parts and boundary terms. No particular UDT `C[g]` is supplied here.

## T3 — aligned and reactive exact witnesses

The aligned anchor is

```text
S_0=(x-1)^2+(y-2)^2,  C=x+y-3.
```

Both branches have the root `(1,2)`, and the constrained branch has `lambda=0`. This proves that a
constraint may be redundant at one realized root. It does not prove off-shell equivalence.

The reactive anchor is

```text
S_0=x^2+y^2,  C=x+y-1.
```

Unrestricted metric-only variation gives `(0,0)`, where `C=-1`. The constrained equations give

```text
(x,y,lambda)=(1/2,1/2,-1).
```

Here the nonzero multiplier is indispensable. Together the two anchors prevent the audit from
assuming either that every multiplier is physically active or that every multiplier is eliminable.
They are variational selector witnesses, not complete UDT universes.

## T4 — finite penalty and hard elimination are not Branch A

For positive finite `alpha`, the metric-only penalty action

```text
S_alpha=x^2+y^2 + alpha (x+y-1)^2/2
```

has

```text
x=y=alpha/[2(alpha+1)],
C=-1/(alpha+1),
alpha C=-alpha/(alpha+1).
```

Thus no finite positive `alpha` imposes the exact constraint. The constrained root and reaction are
recovered only in the singular `alpha -> infinity` limit. Calling that an exact finite elimination
would be false.

Substituting `y=1-x` before variation does recover the tangent root `x=1/2`, but this is variation on
the constrained submanifold. It is not Branch A's unrestricted variation of the original metric
coordinates. This is the same variation-domain distinction already exposed by the bootstrap audit.

## T5 — covariance does not select the field census

For a bulk diffeomorphism-invariant metric-only action, with
`E_g^{mu nu}=(1/sqrt|g|) delta S/delta g_{mu nu}`, the bulk Noether identity is, up to the declared
sign/index convention,

```text
2 nabla_mu E_g^{mu}{}_{nu} = 0.
```

For a covariant action containing an auxiliary scalar `lambda`, diffeomorphism variation instead
gives

```text
2 nabla_mu E_g^{mu}{}_{nu} = E_lambda nabla_nu lambda.
```

On the auxiliary equation `E_lambda=0`, the usual divergence identity is recovered. Covariance
therefore permits both field censuses; it does not select one. The runnable finite gauge analogue
`S=(u-v)^2`, invariant under `delta u=delta v`, verifies the corresponding two-field Noether
identity `E_u+E_v=0` exactly.

This is a bulk identity. It neither supplies a differentiable finite-cell action nor proves that the
unspecified constraint is a UDT law.

### Explicit four-dimensional bulk existence witness

To meet the preregistered outcome literally without promoting an action, let `M` be a finite
four-dimensional cell and write

```text
W[g] = C_abcd C^abcd,
S_A  = integral_M sqrt(|g|) W,
S_B  = integral_M sqrt(|g|) (1+lambda) W.
```

Both are bulk diffeomorphism-covariant. In four dimensions `w_W=-4`; choosing scalar
`w_lambda=0` makes both densities CSN-neutral. The flat reciprocal metric `phi=0` on the finite cell
has `W=0`. It is a stationary bulk root of A and, with any finite `lambda`, of B; varying `lambda`
supplies `W=0`. The runnable curvature-amplitude anchor represents `W` by `c^2` and verifies that
all A/B bulk first variations vanish at `c=0`.

This is a `CATEGORY_A_EXISTENCE_WITNESS_NOT_NATIVE_ACTION`. It uses one local fourth-order bulk
implementation only to prove the paired classes are nonempty; it does not adopt locality, fourth
order, or the `C^2` action for UDT. The root is the mathematically allowed trivial configuration,
not a model of the observed nontrivial universe. Its boundary/corner completion is still open.

Moreover, covariance of a bulk density does not determine the active gauge group on a manifold with
a mirrored boundary. That group may be restricted to boundary- and mirror-preserving
diffeomorphisms. Therefore “full finite-cell covariance” remains `UNRESOLVED_TRIAL` pending a
boundary embedding, allowed-data, corner, and generator analysis.

## T6 — Common-Scale Neutrality is compatible but nonselecting

In four dimensions `sqrt(|g|)` has common-scale weight `+4`. If, and only if, a candidate constraint
scalar transforms homogeneously with weight `w_C`, the term

```text
sqrt(|g|) lambda C
```

has weight zero when

```text
w_lambda = -4-w_C.
```

This shows that CSN does not generically exclude an auxiliary multiplier. It is only a weight
classification: local inhomogeneous transformation terms need their own audit, and neither `C` nor
the authority to introduce `lambda` has been derived.

## T7 — finite-cell completion stays open

The one-dimensional exact boundary anchor

```text
L = (q')^2/2 + lambda q'
```

gives

```text
E_q = -q''-lambda',
E_lambda = q',
endpoint variation = (q'+lambda) delta q.
```

The multiplier adds `lambda delta q` at the boundary. A covariant bulk constraint can therefore
change the finite-cell differentiability problem. Neither branch inherits GR's asymptotic or GHY
completion, and neither passes the native boundary gate merely because its bulk is covariant.

## T8 — “the metric is the theory” does not yet settle auxiliaries

The binding maxim excludes importing an independently physical mechanism in place of metric
geometry. Branch B assigns no particle, matter, carrier, or independently propagating ontology to
`lambda`; it treats it as off-shell constraint bookkeeping. The current final ledger explicitly
keeps metric-only, multiplier, and hard-constraint routes live. Therefore strengthening the maxim to
“only the metric may ever be varied” would be a new rule, not an interpretation already established
by the accepted record.

Conversely, this does not license Branch B. A multiplier becomes legitimate only if its constraint
and its role are derived from UDT. Nonpropagating does not mean law-neutral: the multiplier changes
the metric equation whenever its reaction is nonzero. The maxim leaves the auxiliary-bookkeeping
question unresolved.

## T9 — bootstrap remains nonselecting

The immediately prior verified derivation found that the current bootstrap statement is on-shell
closure/admissibility. It supplies no off-shell field census, constraint functional, or selection
map. It therefore selects neither A nor B and cannot be used to promote the trial covariance into a
complete action.

## T10 — iterative appropriateness ledger

| Selector | Trial ruling | Why now | Exact next rejection/selection test |
|---|---|---|---|
| Four dimensions | `INHERITED` | Existing comparison arena; not newly derived | A native dimensional-selection theorem could replace this inheritance |
| Diffeomorphism covariance | `RETAIN_TRIAL_CONDITIONAL` for the bulk; full finite-cell group `UNRESOLVED_TRIAL` | No bulk conflict found with Reciprocity or CSN; both branches admit its Noether identity | Derive boundary/mirror-preserving group and differentiable generators; reject or modify if a native law requires noncovariant preferred structure |
| Unrestricted variation of declared fields | `RETAIN_TRIAL` | Prevents silently dropping normal equations | Modify only with a derived restriction/selection theorem and an equivalence audit |
| Metric-only field census | `UNRESOLVED_TRIAL` | Compatible, but no premise excludes auxiliary bookkeeping | Select if UDT derives metric-only off-shell closure or excludes every auxiliary realization |
| Metric plus auxiliary constraint | `UNRESOLVED_TRIAL` | Compatible in form, but no native `C[g]` or authority exists | Select only by deriving the constraint and its multiplier role; reject if it imports physical mechanism or violates a foundation/boundary gate |
| Locality | `OPEN_NOT_ADOPTED` | Not tested and not implied by covariance | Separate future selector trial |
| Derivative order/action inventory | `OPEN_NOT_ADOPTED` | Would improperly bundle EH or `C^2` | Separate future selector trial after field/variation authority |
| Finite-cell boundary completion | `OPEN` | Both branches have unresolved boundary variations | Derive the differentiable action, allowed boundary data, corners, and generator |

## Smallest genuinely missing selector

The next missing object is the **native authority for the off-shell field/constraint census**:

```text
either a theorem that the metric-only configuration space is closed and excludes auxiliary varied
constraints, or a derived constraint functional C[g] whose exact enforcement requires one.
```

This is smaller and earlier than choosing EH, `C^2`, second order, a source, or a mass. Until that
authority exists, iterating on those later GR assumptions risks selecting an action by bundle rather
than by UDT foundation.

## Completeness map

| Criterion | Covered here | Still open |
|---|---|---|
| Fields | Exact A/B census comparison | Native census and auxiliary authority |
| Action terms | Generic multiplier structure only | Complete native invariant inventory and coefficients |
| Full equations | Every anchor variable is varied | Complete UDT field equations |
| Domain | Unrestricted declared-field variation versus constrained tangent reduction distinguished | Native off-shell domain selection |
| Boundary | Exact added endpoint term exhibited | Native finite-cell boundary/corner action and data |
| Topology | Finite cell retained | Full topology/corner classification |
| Dynamics | Reactive versus redundant constraints distinguished | Static/time-live native dynamics |
| Branches | Both selector branches retained | Global physical branches and uniqueness |
| Stability | Not used | Stability of any complete solution |
| Regime | Exact algebraic/variational selector scope | Physical approximation regime and errors |

## Authority boundary

The result is CPU-only, preregistered, carrier-free, density-normalization-free, and does not promote
an action. The July 1 provenance firewall remains binding. No research artifact, frozen package,
registry, `CANON.md`, or `grok` pointer is changed. Repository reorganization remains paused.
