# Bootstrap variation-domain selector derivation — preregistration

Date: 2026-07-18  
Branch: `codex/bootstrap-variation-selector-2026-07-18`  
Required parent: `3f0d716bd07f9c9f5d8438638bdced28a7b45bda`  
Mode: CPU-only symbolic/logical derivation; no GPU and no repository reorganization

## Exact question

Does the existing UDT global-bootstrap working principle select where fundamental variation occurs,
or derive a two-stage bridge between a pre-scale CSN-compatible law and a post-scale physical law?

This is an observing question, not a request to obtain `C^2`, EH, a carrier, or a mass. All outcomes
below are admissible.

## Frozen affirmative sources

The July 1, 2026 provenance firewall is binding. Pre-July-1 material may identify a failure or
counterexample but cannot supply affirmative UDT physics. The affirmative input set and pre-run
SHA-256 values are:

| Source | SHA-256 |
|---|---|
| `UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md` | `ce14075bad1ff4b6ea9b41e35dc6b63dfc5a9ae13478bd57c80b1502f33fb540` |
| `UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md` | `4bb0da9098da0a9970602e2449615eef151796b0d7fe7a9978f4b66145748a34` |
| `UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md` | `db4a426b021e375fa4bca0d870aaf973de319de3b08072195d001a056630832d` |
| `UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md` | `6a835388e8f7a82a4bb4b9496f99c4a5e4181f5e5ccb2637641a1b4346922cc6` |
| `native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv` | `70cab9d5e10b03e0e3418129b67155e01d9f805c4397c69ef8795c4d2aaa5dfd` |
| `native_action_final_adjudication_2026-07-18/LAY_DECISION_TREE.md` | `cac9da7f47d529eccb06615a25e5158a14a8ffa6b33739fb5b21152758da961a` |
| frozen final-adjudication package manifest | `57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33` |

No frozen package or source above may be modified.

## Preregistered outcomes

Exactly one top-level result will be assigned, without forcing the expected count or direction:

1. `PRE_SCALE_SELECTED`: bootstrap forces fundamental variation on `[g]_CSN` before representative
   selection and excludes post-scale-first realizations.
2. `POST_SCALE_SELECTED`: bootstrap derives a physical representative/scale before fundamental
   variation and excludes pre-scale-first realizations.
3. `TWO_STAGE_BRIDGE_DERIVED`: bootstrap derives both a representative-selection rule and a
   dynamical matching rule connecting the pre- and post-scale laws.
4. `UNDERDETERMINED`: the exact bootstrap principle is compatible with at least two inequivalent
   variation placements, or supplies selection without the independent matching theorem.

An outcome may be `OPEN` if the exact sources do not support a theorem and the countermodels do not
close the relevant implication.

## Load-bearing tests

### T1 — semantic/off-shell audit

Classify every clause of the bootstrap source as an on-shell realized-solution condition, an
off-shell variational rule, a representative-selection map, or a matching rule. No intent may be
silently promoted across those categories.

### T2 — variation/restriction commutator

For a general functional `S(x,y)` and section `y=f(x)`, verify

```text
d S(x,f(x))/dx = S_x + S_y f'(x).
```

Restrict-then-vary and vary-then-restrict are equivalent only under an explicit condition such as
`S_y f'=0`. This test must be runnable symbolic algebra.

### T3 — selector-level countermodels

Construct at least two explicit logical models sharing:

- a pre-scale CSN quotient variable;
- a common-scale/representative variable;
- the same global bootstrap closure and narrow-window admissibility predicate;
- at least one common realized solution;

while placing variation on different sides of representative selection. These are logical
countermodels to a selector implication, not complete UDT universes. They may establish
underdetermination but cannot provide affirmative UDT dynamics.

### T4 — conformal-weight anchor

In four dimensions, independently confirm under constant common scaling that `sqrt(|g|) C^2` has
weight zero while `sqrt(|g|) R` has weight two. State explicitly that constant-weight algebra is an
anchor, not the full local Weyl/boundary derivation.

### T5 — principal-order bridge test

Test whether selecting a representative or dimensionful scale alone can turn a fourth-order
principal polynomial `a k^4` into a second-order polynomial `b M^2 k^2` for all `k`. A derived bridge
requires more than representative selection if the identity fails.

### T6 — global-condition placement

Separate three inequivalent uses of bootstrap:

1. an after-solution admissibility predicate;
2. an off-shell constraint varied with a multiplier;
3. a representative-selection map applied before a post-scale action.

No equivalence may be assumed without an explicit theorem.

### T7 — strongest bridge contract

Attempt the strongest bridge consistent with the sources. Record every independently required item:
selection-map existence, uniqueness and differentiability; field/variation map; controlled regime;
principal-operator matching; boundary/corner matching; source and normalization matching. A bridge is
not derived if any load-bearing item is inserted rather than obtained.

## Falsification and acceptance

- `PRE_SCALE_SELECTED` or `POST_SCALE_SELECTED` fails if an inequivalent placement satisfies every
  exact bootstrap clause without adding a forbidden local density coupling.
- `TWO_STAGE_BRIDGE_DERIVED` fails if representative selection leaves the local invariant inventory,
  derivative order, source, or boundary generator independently free.
- `UNDERDETERMINED` is accepted only if the countermodels satisfy the exact selector premises and the
  independent verifier reproduces their common closure and inequivalent placement.
- Any proof that depends on a carrier, fitted density, GR field equation, spatial infinity, or
  unrecorded scale is rejected.

## Verification contract

The derivation implementation and independent verifier must not import one another. The verifier must
rederive T2–T5, parse the premise/status ledgers, check source hashes, exercise catch-proofs for a
false restrict/vary equivalence, a missing countermodel closure, a false order bridge, and an
overstated status, and leave the frozen inputs unchanged. SymPy is pinned only as a CPU algebra tool.

Repository tests must reproduce the documented baseline. The original 54-path dirty checkout is
checked by metadata only; its contents remain unread.

## Maximum conclusion

This bounded derivation may select the logical placement of variation only if the existing bootstrap
principle actually forces it. Otherwise it may identify the smallest missing off-shell object and a
conditional bridge contract. It cannot canonize an action, adopt a carrier, derive a source or mass,
start GPU work, update `grok`, or resume repository reorganization.
