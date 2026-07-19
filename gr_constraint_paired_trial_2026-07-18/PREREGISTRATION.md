# GR-constraint paired trial — preregistration

Date: 2026-07-18  
Branch: `codex/gr-constraint-paired-trial-2026-07-18`  
Required parent: `378eac0ae0b615f4e64828d50bbe5d7d027393c1`  
Mode: CPU-only selector/variational algebra; no GPU and no repository reorganization

## Exact paired question

With four dimensions retained as `INHERITED`, full diffeomorphism covariance adopted only as a
`TRIAL`, and the finite mirrored cell retained as binding, does UDT select between:

- `A_METRIC_ONLY`: the metric is the sole independent off-shell field and is varied unrestrictedly;
- `B_METRIC_PLUS_CONSTRAINT`: the metric and an auxiliary multiplier/constraint field are varied
  unrestrictedly, with the auxiliary field carrying no presumed particle or matter ontology?

This is an observing selector comparison. It does not target EH, `C^2`, a mass, a carrier, or a
preferred equation. Locality, derivative order, invariant inventory, bootstrap placement, source,
normalization, and boundary completion remain open in both branches.

## Frozen sources

The July 1 provenance firewall remains binding. Affirmative inputs and SHA-256 values are:

| Source | SHA-256 |
|---|---|
| `bootstrap_variation_selector_2026-07-18/SHA256SUMS.txt` | `cad3c4f0dccc1599c5b4ff48c6adafa32fb64b590e4ef4f0f6e20e5e96de9bed` |
| `bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md` | `05a84a7bfeca3d78c628a3a6a343463db11497d66c5889ac0590655728d056f9` |
| `bootstrap_variation_selector_2026-07-18/STATUS_LEDGER.tsv` | `d271b483a02e0732bbab7f597b59827810586894ea29a8717f3cfff3c87949e6` |
| `UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md` | `4bb0da9098da0a9970602e2449615eef151796b0d7fe7a9978f4b66145748a34` |
| `UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md` | `db4a426b021e375fa4bca0d870aaf973de319de3b08072195d001a056630832d` |
| `native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv` | `70cab9d5e10b03e0e3418129b67155e01d9f805c4397c69ef8795c4d2aaa5dfd` |

No source or frozen package may be modified.

## Common trial assumptions and explicit non-assumptions

Common to A and B:

1. four-dimensional arena: `INHERITED`, not derived;
2. diffeomorphism covariance: `TRIAL_CONDITIONAL`, not bundled with Einstein equations;
3. finite mirrored cell: binding global arena; spatial infinity is not reintroduced;
4. CSN and Reciprocity: unchanged foundations;
5. unrestricted variation of every field declared by that branch.

Not assumed: locality, metric-only truth, a particular constraint, second- or fourth-order equations,
EH, Lovelock, `C^2`, a cosmological term, a carrier, matter source, GHY/ADM structure, `G`, density
normalization, or a bootstrap selection map.

## Preregistered outcomes

Exactly one top-level outcome will be assigned:

1. `A_METRIC_ONLY_SELECTED` — exact UDT premises exclude every auxiliary-constraint realization.
2. `B_CONSTRAINT_SELECTED` — an exact UDT premise requires an auxiliary varied constraint and the
   metric-only branch cannot represent it without changing the declared variation problem.
3. `BOTH_CONDITIONALLY_ADMISSIBLE` — explicit models show both field censuses can satisfy the common
   trial assumptions, while neither is selected.
4. `A_INCONSISTENT`, `B_INCONSISTENT`, or `NEITHER_ADMISSIBLE` — a branch conflicts with an exact
   premise under every implementation in its declared class.
5. `OPEN` — the bounded algebra cannot establish compatibility or exclusion.

No expected outcome is forced.

## Load-bearing tests

### T1 — provenance and bundle audit

Separate covariance from locality, metric-only fields, unrestricted metric variation, derivative
order, EH/Lovelock, asymptotic boundary data, and matter. A familiar GR bundle may not enter as one
premise.

### T2 — exact multiplier/KKT equations

For a generic finite-dimensional anchor `S_0(x)` and constraint `C(x)=0`, independently derive

```text
grad S_0 + lambda grad C = 0,
C = 0.
```

Show why this is not the same off-shell problem as unrestricted metric-only variation
`grad S_0=0`.

### T3 — redundant and reactive constraint cases

Construct two exact anchors:

- an aligned case where the metric-only root already satisfies `C=0` and the multiplier reaction
  vanishes;
- a reactive case where the constrained root differs and the multiplier supplies a nonzero normal
  reaction.

The comparison must characterize both; it may not choose only the convenient case.

### T4 — penalty/elimination challenge

Test whether replacing a multiplier by a finite metric-only penalty `alpha C^2/2` enforces `C=0`.
If exact equivalence occurs only in a singular `alpha -> infinity` limit, record that limit rather
than calling the auxiliary field eliminated.

### T5 — covariance/Noether field-census test

Audit the general covariance identity for metric-only and metric-plus-scalar/multiplier actions.
Determine whether covariance alone excludes auxiliary fields. No GR equation may be assumed.

### T6 — CSN weight test

For a constraint scalar of common-scale weight `w_C`, test whether assigning the multiplier weight
`-4-w_C` can make `sqrt(|g|) lambda C` weight zero in four dimensions. This is only a weight
classification; the actual constraint and multiplier authority remain open.

### T7 — finite-cell boundary test

Record the additional boundary variation introduced by `lambda C[g]`. Neither branch passes
finite-cell completion merely because its bulk is covariant.

### T8 — “the metric is the theory” interpretation audit

Distinguish physical propagating ontology from auxiliary off-shell bookkeeping. Determine whether the
binding maxim excludes all multipliers or only independently physical nonmetric mechanisms. Do not
strengthen the final accepted field-census ledger without evidence.

### T9 — bootstrap compatibility

Apply the verified prior result: current bootstrap is an on-shell closure/admissibility principle and
does not select the field census. No branch may claim bootstrap support beyond that scope.

### T10 — iterative appropriateness ruling

Grade each common/branch selector separately as `RETAIN_TRIAL`, `REJECT_TRIAL`, or
`UNRESOLVED_TRIAL`, with the exact next falsifier. Compatibility is not derivation.

## Acceptance and falsification

- A branch is selected only if all alternatives are excluded by exact affirmative UDT premises, not
  by simplicity or familiarity.
- Branch B fails if its multiplier is secretly assigned matter ontology, an untagged scale, a fitted
  density, or a constraint chosen to manufacture a desired solution.
- Branch A fails as an equivalent replacement for B if it drops the normal reaction or uses only a
  finite penalty while claiming exact `C=0`.
- Covariance is rejected as a useful trial if it contradicts Reciprocity, CSN, or the finite-cell
  arena; mere non-selection does not count as contradiction.
- A shared realized root does not establish off-shell equivalence.

## Verification contract

The derivation and independent verifier may not import one another. The verifier must independently
rederive T2–T6, validate both T3 cases, exercise corrupt fixtures for a missing multiplier equation,
a discarded reactive case, a false finite-penalty equivalence, a wrong CSN weight, a bundled EH
promotion, and an overstated selector status. Two fresh reviewers must separately attempt to select A
or B and to find a hidden GR bundle.

Repository tests must match the documented baseline. All six frozen manifests and 133 package paths,
the prior bootstrap-selector package, current paths/frontier, and the original 54-path dirty checkout
metadata must remain unchanged; dirty contents stay unread.

## Maximum conclusion

This trial may retain, reject, or leave unresolved the individual GR-origin constraints only within
the bounded selector scope. It cannot derive or canonize a complete action, alter existing C2/EH
statuses, adopt a carrier/source/mass, update `grok`, resume reorganization, or use GPU work.
