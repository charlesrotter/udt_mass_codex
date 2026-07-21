# UDT mixed-readout observational-anchor and sector-soldering audit — preregistration

Date: 2026-07-20

Base: `a95d0c34d28f0c8ae53be0d8aea836aafa4ec48f`

Branch: `codex/udt-mixed-readout-anchor-soldering-audit-2026-07-20`

Mode: CPU-only exact `2x2` metric/operator-pair classification and provenance audit

## Whole question

The global coframe cocycle audit derived the conditional mixed Lorentzian readout family

```text
H0=[[A,B],[B,A b^2]],
g(phi)=P(phi)^T H0 P(phi),
P(phi)=diag(exp(-phi),exp(phi)),
B^2>A^2 b^2,
```

with exact reciprocal-seal closure. It left the invariant mixing modulus

```text
mu=B^2/(A^2 b^2)>1
```

and the physical clock/ruler soldering open.

This audit asks:

> Does the owner meaning of the observed terrestrial/solar `c` anchor, the exact
> dimension-matched pair `q=(c dt,dr)`, CSN, and the separate spatial-versus-temporal mirror sectors
> select, reject, or leave free the mixed readout and `mu`?

The audit must determine whether `mu` is a genuine invariant of the metric-plus-reciprocity pair or
only an artifact of keeping `P` diagonal while changing the readout.

## Objects that must remain distinct

1. a passive coordinate/basis change transforming the metric and reciprocal operator together;
2. an authorized local coframe gauge transformation preserving one physical metric;
3. a physical observer/frame transformation, for which UDT has not yet adopted SR/GR mechanics;
4. calibration by positive CSN rescaling;
5. the reciprocal eigen-directions of `P`;
6. the operational orthonormal clock/ruler axes used to measure local `c`;
7. the spatial-depth seal involution;
8. the temporal mirror acting on time-on/off-diagonal sectors.

No two items may be identified merely because a convenient chart makes them coincide.

## Premise treatment

| Object | Treatment |
|---|---|
| Observed terrestrial/solar `c` | `pinned-by-THEORY` as an observational anchor; exact source meaning to be audited |
| Reciprocal-c Identity and dual UDT Reciprocity | `pinned-by-THEORY` |
| `q=(c dt,dr)` | exact frozen dimension-matched formalization; physical slot meaning to be audited |
| `P(phi)=diag(exp(-phi),exp(phi))` | `DERIVED_CONDITIONAL` with frozen sign/unit and regularity stamps |
| Local Lorentzian readout and slot identification | retain their frozen `POSIT / CHOSE / CONDITIONAL` status |
| CSN | `pinned-by-THEORY` in pre-scale scope |
| Mixed readout family | `DERIVED_CONDITIONAL` in the constant real symmetric class |
| Static spatial seal `phi=0`, `delta phi=0`, normal `phi'` free | `pinned-by-THEORY` |
| Temporal mirror `t -> -t` for time-on/off-diagonal sectors | sector authority `pinned-by-THEORY`; executable component parity open unless sourced |
| Simultaneous diagonal clock/ruler anchor chart | `pinned-by-HABIT` unless the owner meaning requires it |
| Isotropic one-way local light speed in a declared anchor observer chart | `free-and-explored`; cannot be imported as an SR postulate |
| Angular sector, global cover, caps, topology, action, bootstrap, scale, carrier, source, mass | excluded |

## Exact tests

### A. Pair-equivalence classification

Write the infinitesimal reciprocal generator as

```text
L=diag(-1,1),       P(phi)=exp(phi L).
```

Under a passive basis change `q=S q_prime`, transform

```text
H -> S^T H S,
L -> S^-1 L S,
F -> S^-1 F S.
```

Derive scalar invariants of the pair `(H,L)`. Test whether two different `mu` values can be related
by any real invertible simultaneous basis change, not only by transformations commuting with `L`.

### B. Strong and weak `c`-anchor readings

Keep two branches until the source resolves them:

1. `FIXED_Q_ANCHOR`: the named `q=(c dt,dr)` axes themselves are the operational orthogonal
   clock/ruler axes at `phi=0`, with a symmetric local `c` cone in that chart;
2. `ORTHONORMALIZABLE_ANCHOR`: `c` fixes local clock/ruler calibration and the Lorentz cone, while
   the reciprocal eigenbasis may be oblique to the operational orthonormal frame.

For each branch derive the exact consequences for `B`, `mu`, and the transformed reciprocal
generator.

### C. Null-cone and calibration test

At `phi=0`, derive the two null slopes in the declared `q` chart and determine what is required for
the pair to be symmetric under `dr/(c dt) -> -dr/(c dt)`. Distinguish this chart statement from the
existence of a different orthonormal chart.

### D. Spatial and temporal mirror test

Test separately:

- the exact mixed spatial-seal involution;
- literal coordinate `t -> -t` in the fixed `q` chart;
- the conjugated temporal reflection in an orthonormal anchor basis.

Do not infer that a basis-conjugated reflection is the owner-named coordinate reversal without a
soldering rule.

### E. Counterwitnesses

Attempt at least:

- two inequivalent `mu` members satisfying the weak anchor and spatial mirror;
- a fixed-`q` anchor witness showing whether the mixed family survives;
- a transformed orthonormal witness proving whether the measured local `c` can coexist with a
  non-diagonal reciprocal generator;
- a temporal-parity witness exposing any unresolved slot interpretation.

## Falsification and certification contract

- The claim that `mu` is a basis artifact fails if an exact simultaneous-`GL(2,R)` scalar invariant
  reconstructs `mu`.
- The mixed family is rejected by the observational anchor only if the exact owner meaning requires
  the `FIXED_Q_ANCHOR` branch or every allowed anchor-preserving transformation fails.
- The mixed family is selected uniquely only if the current authority supplies an equation fixing
  `mu` or a type-correct equivalence removes it.
- A diagonalizable Lorentz metric is not by itself a physical soldering theorem.
- Literal coordinate time reversal and an abstract Lorentzian temporal reflection must not be
  silently identified.

## Frozen outcome classes

1. `OBSERVATIONAL_ANCHOR_REJECTS_MIXED_READOUT`
2. `OBSERVATIONAL_ANCHOR_SELECTS_UNIQUE_MU`
3. `OBSERVATIONAL_ANCHOR_LEAVES_MU_OPEN`
4. `MU_IS_SIMULTANEOUS_BASIS_ARTIFACT`
5. `MU_IS_INVARIANT_OF_METRIC_RECIPROCITY_PAIR`
6. `FIXED_Q_AND_ORTHONORMALIZABLE_ANCHOR_BRANCHES_DIVERGE`
7. `TEMPORAL_MIRROR_SELECTS_OR_REJECTS_MIXED_READOUT`
8. `TEMPORAL_MIRROR_COMPONENT_SOLDERING_REMAINS_OPEN`
9. `PHYSICAL_CLOCK_RULER_SOLDERING_RULE_ABSENT`
10. `AUDIT_INCONCLUSIVE`

Multiple scoped classes may apply.

## Authority boundary

No SR or GR observer mechanics, equivalence principle, imported ADM shift interpretation, action,
field equation, angular topology, bootstrap equation, scale selection, carrier, source, mass, GPU
work, startup-control edit, `CANON.md` edit, or canonization is authorized.

Maximum conclusion:

`UDT_MIXED_READOUT_ANCHOR_SOLDERING_STATUS_CHARACTERIZED`.
