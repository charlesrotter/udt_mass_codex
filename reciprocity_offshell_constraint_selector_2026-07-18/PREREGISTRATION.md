# Reciprocity off-shell constraint selector — preregistration

Date: 2026-07-18
Branch: `codex/reciprocity-offshell-constraint-selector-2026-07-18`
Required parent: `7b0e07fcad2ffdee94bcc1acda582d7ebab074d0`
Mode: CPU-only exact geometry/variational selector audit; no GPU or repository reorganization

## Observing question

Does the current post-July UDT foundation express Reciprocity as a nontrivial, diffeomorphism- and
Common-Scale-Neutrality-compatible off-shell constraint `C[g]=0` of the metric alone? Or is the
displayed reciprocal product identity a representative/coframe readout or gauge choice until extra
off-shell structure is derived?

The run observes the available structures. It does not target metric-only closure, a multiplier, a
preferred action, or a desired equation.

## Whole frame and bounded classes

The audit keeps five candidate classes distinct:

1. `L0_METRIC_ONLY_ORDER_ZERO`: a local algebraic natural scalar of one Lorentz metric, with no
   derivatives, reference tensor, coframe, vector, scalar, foliation, or volume form;
2. `L1_ADAPTED_REPRESENTATIVE`: the component relation
   `(-g_tt/c^2) g_parallel_parallel=1` after a paired coframe and CSN representative are chosen;
3. `L2_STRUCTURED_COVARIANT`: a scalar constructed from the metric plus declared time/parallel
   vectors, projectors, coframe, clock, or reference volume;
4. `L3_DERIVATIVE_METRIC_ONLY`: curvature or other derivative natural scalars of the metric;
5. `L4_GLOBAL_BOUNDARY`: a nonlocal or finite-cell construction selecting directions or scale.

Only L0 could close the requested local algebraic metric-only question without additional
structure. L2-L4 remain legitimate challenges and must be classified rather than silently excluded.
No result in L0 is a theorem about every derivative, nonlocal, boundary, or enlarged-field theory.

## Frozen affirmative sources

The July 1 provenance firewall remains binding. The following post-July/current sources are frozen:

| Source | SHA-256 |
|---|---|
| `UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md` | `6e977717ca028cabaa198dd14a6a97b3b15740e45485d0ab735f3df0326df192` |
| `UDT_NATIVE_ACTION_COLD_PACKET.md` | `d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0` |
| `UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md` | `b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003` |
| `UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md` | `4bb0da9098da0a9970602e2449615eef151796b0d7fe7a9978f4b66145748a34` |
| `UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md` | `db4a426b021e375fa4bca0d870aaf973de319de3b08072195d001a056630832d` |
| `native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv` | `70cab9d5e10b03e0e3418129b67155e01d9f805c4397c69ef8795c4d2aaa5dfd` |
| `gr_constraint_paired_trial_2026-07-18/SHA256SUMS.txt` | `8d5c617d9bb611f67b15524b34271de7f121ea9a71fa14d8e131cf85bc2c63a2` |
| `gr_constraint_paired_trial_2026-07-18/DERIVATION_REPORT.md` | `952b29705023c0626896db75b7a60173d6c78e3e00a8321d826a53b606557316` |
| `gr_constraint_paired_trial_2026-07-18/STATUS_LEDGER.tsv` | `ba26cad7d04d7492c206e3fe11a7cd10ab226c01663bef5edee4b166c2f08809` |

The final ledger controls any stronger wording in an earlier source: the Lorentzian readout, CSN
representative, full metric, and reciprocal slot identification remain conditional/chosen, and the
off-shell domain remains open.

## Premise and non-premise ledger

Common inputs:

- positional dilation, Reciprocal-c, dual UDT Reciprocity, and CSN retain their current founding
  statuses;
- `uv=1` and the reciprocal exponential comparison retain their exact derived premise stamps;
- four dimensions remain inherited for this comparison;
- bulk diffeomorphism covariance remains a conditional trial, not a derived UDT premise;
- the finite mirrored cell is binding, while its complete boundary group/action remains open;
- the trivial `phi=0` configuration remains mathematically allowed although realized nonzero
  dilation is observed.

Not assumed: a canonical time vector, radial/parallel vector, foliation, coframe field, reference
metric, background volume form, representative-selection map, locality outside L0-L3, derivative
order, action, source, carrier, density normalization, boundary completion, or global constraint.

## Preregistered outcomes

Exactly one top-level outcome will be assigned:

1. `NATIVE_METRIC_ONLY_CONSTRAINT_DERIVED`: an exact current premise yields a nontrivial covariant,
   CSN-compatible `C[g]` and excludes the readout/gauge alternatives.
2. `NO_L0_CONSTRAINT_REPRESENTATIVE_IDENTITY_IS_GAUGE_READOUT`: the order-zero natural-scalar class
   is closed by theorem, while the component product is a chart/coframe/CSN-representative condition;
   derivative, structured, or global routes remain separately open.
3. `AUXILIARY_NATIVE_CONSTRAINT_REQUIRED`: an exact current premise derives extra fields and a
   multiplier/hard constraint, with alternatives excluded.
4. `OPEN`: the bounded tests cannot close L0 or classify the representative identity.
5. `INCONSISTENT`: the exact current premises contradict each other within the audited scope.

No expected outcome is forced. A no-go outside L0 or a required auxiliary field cannot be inferred
from failure to find a candidate.

## Load-bearing tests

### T1 — provenance and field census

Audit the exact status of the paired coframe, Lorentzian readout, CSN representative, spatial-slot
identification, covariance, and finite-cell boundary structure. No conditional object may become an
off-shell field by typography.

### T2 — chart transformation of the component product

For `g=diag(-a c^2,b)` in an adapted two-coordinate block, apply independent coordinate rescalings.
Test whether `a b=1` is a scalar statement without carrying a coframe/vector pair.

### T3 — CSN decomposition

Independently derive

```text
a = exp(2 sigma-2 phi),
b = exp(2 sigma+2 phi),
sigma = (1/4) log(a b),
phi   = (1/4) log(b/a).
```

Under `g -> Omega^2 g`, test `sigma -> sigma+log(Omega)` and `phi -> phi`. Determine whether
`a b=1` fixes the calibrational coordinate `sigma` rather than constraining reciprocal depth.

### T4 — order-zero natural-scalar theorem

Use the transitive `GL(4)` action on Lorentz inner products of fixed signature to test whether any
nonconstant diffeomorphism-natural scalar can be made algebraically from one metric at a point.
Explicitly separate scalars from densities such as `sqrt(|det g|)`.

### T5 — strongest structured covariant candidate

Introduce explicit time/parallel vectors or a coframe only as a challenge. Test the scalar norms,
their CSN weights, and the invariant depth ratio. Record every extra field, normalization, and
degeneracy; do not call it metric-only.

### T6 — readout, hard restriction, and multiplier comparison

Write the exact scale/depth variables. For a CSN-invariant pre-scale action independent of `sigma`,
compare unrestricted quotient/readout, hard gauge `sigma=0`, and a multiplier `lambda sigma`.
Determine whether the multiplier has a physical normal reaction or only fixes gauge. Then introduce
a `sigma`-dependent corrupt fixture and verify that it is a CSN violation rather than native
reactivity.

### T7 — derivative and curvature challenge

Attempt the strongest derivative metric-only replacement. Test whether a curvature scalar can be
equivalent to the pointwise component product by using flat metrics in differently scaled charts.
Do not infer that all derivative/nonlocal constructions are impossible.

### T8 — finite-cell/global challenge

Audit whether the mirror supplies a bulk time/parallel two-plane, normalization, or representative,
and whether a boundary-selected/nonlocal construction remains open.

### T9 — “metric is the theory” and bootstrap

Determine only what the accepted current wording establishes. Do not turn metric-led physical
ontology into an unstated metric-only off-shell theorem, or bootstrap closure into a local
constraint.

### T10 — selector ruling and completeness map

Classify each route as `DERIVED`, `CONDITIONAL`, `GAUGE/READOUT`, `OPEN`, or `REFUTED_IN_CLASS`, state
the exact next falsifier, and identify all uncovered completeness criteria.

## Acceptance and falsification

- The L0 no-go fails if a nonconstant order-zero diffeomorphism-natural scalar of one Lorentz metric
  exists without background structure.
- The gauge/readout classification fails if the component product is invariant under arbitrary
  chart changes and local common scaling without carrying a paired frame/representative.
- An L2 construction does not count as metric-only; its extra structure must be derived before it
  can count as native.
- A derivative scalar that vanishes on one reciprocal metric is insufficient; equivalence requires
  both directions across the declared class.
- A physical multiplier reaction is not native pre-scale evidence if it arises only after inserting
  forbidden `sigma` dependence.
- No conclusion may exclude L2-L4 merely because L0 closes negatively.

## Verification contract

The derivation and verifier may not import one another. The verifier must independently rederive
T2-T7 and exercise corrupt fixtures for: treating the component product as a scalar; losing the CSN
shift; accepting a nonconstant order-zero invariant; hiding a preferred vector/coframe; treating a
density as a scalar; converting gauge fixing into physical reaction; accepting a one-way curvature
implication as equivalence; and overstating the conclusion beyond L0. Two fresh read-only reviewers
must separately attempt a covariant counterexample and audit the variational/boundary interpretation.

Repository tests must match the documented baseline. The six frozen packages and 133 paths, prior
selector packages, current paths/frontier, and the original 54-path dirty checkout metadata must
remain unchanged; dirty contents stay unread.

## Maximum conclusion

This run may close only the local order-zero metric-only constraint class and classify the displayed
representative identity. It cannot derive a complete action, universally select readout/hard/
multiplier implementations, exclude derivative or global constructions, adopt a source/carrier,
update `grok`, resume repository reorganization, canonize a result, or use GPU work.

