# UDT global coframe cocycle and finite-cell tangent audit — preregistration

Date: 2026-07-20

Base: `c8d337fb06b90126756483af86f105e2fbb4eabb`

Branch: `codex/udt-global-coframe-cocycle-audit-2026-07-20`

Mode: CPU-only exact algebra, topology/cocycle census, and boundary-tangent audit

## Whole question

The global reciprocal-closure audit isolated the first missing mathematical layer as a possible
`GLOBAL_COMPLETION_MAP`. This audit tests the sharpest metric-only part of that lead:

> Given only the exact reciprocal local coframe, founding CSN equivalence, and the canonized
> finite-cell sector split, do involution, overlap/corner cocycle consistency, regularity, and global
> orientation force a unique complete coframe lift and allowed boundary tangent space?

The audit is `METRIC_LED`. It does not add an action and does not assume that a globally attractive
completion is physical.

## Bounded configuration class

The audit will retain the exact local reciprocal block and enumerate all real full-coframe lifts that
obey the registered algebraic involution and reciprocal-character requirements. It will then add, in
order and without silently merging them:

1. positive-CSN physical-readout compatibility where a readout is source-authorized;
2. normal, angular, and time-on extensions;
3. cocycle consistency on double and triple overlaps;
4. corner compatibility of commuting or noncommuting seal generators;
5. orientation preservation or reversal, recorded rather than preselected;
6. regularity at any caps that can be stated without choosing open topology or periods;
7. the induced fixed and anti-fixed boundary tangent subspaces;
8. compatibility with the exact conditional bare-`C2` boundary phase-space slots, without adopting
   `C2` as the native action.

Where the global chart cover, topology, cap structure, periods, or corner incidence are not supplied,
the audit must parameterize alternatives rather than choose one.

## Premise treatment

| Object | Treatment |
|---|---|
| Exact reciprocal local coframe and `phi` character | `pinned-by-THEORY`, with frozen premise stamps |
| Common-Scale Neutrality | `pinned-by-THEORY` in its pre-scale equivalence scope |
| Finite mirrored domains and no spatial infinity | `pinned-by-THEORY` in the exact canonized scope |
| Static spatial seal `phi=0`, `delta phi=0`, normal `phi'` free | `pinned-by-THEORY` |
| Separate temporal mirror/time-on sector | `pinned-by-THEORY` as a sector split; its action is open |
| Physical full-coframe slot/readout map | `free-and-explored` |
| Normal/angular/time-on lift | `free-and-explored` |
| Angular caps, periods, topology, twist, and chart cover | `free-and-explored` |
| Global orientation | `free-and-explored` unless exact source authority fixes it |
| Boundary polarization and corner completion | `free-and-explored` |
| Static seal / WR-L horizon / global `X_max` identification | excluded; no silent join |
| `C2` action | `UNIQUE-CONDITIONAL` only in the frozen pre-scale class; diagnostic phase space only |
| EH route | excluded from the derivation |
| Bootstrap placement and physical scale | excluded from the derivation |
| Carrier, source, matter, and mass | excluded from the derivation |

## Exact tests

### A. Full-block involution census

Reproduce the complete-seal family and classify each full lift by:

- square equal to identity;
- reciprocal-character inversion;
- determinant and orientation character;
- compatibility with every source-authorized quadratic readout;
- fixed and anti-fixed subspace dimensions.

### B. Cocycle and corner equations

For transition/seal maps `T_i`, test exactly:

```text
T_i^2 = I
T_ij T_jk T_ki = I
T_i T_j = T_j T_i               when the declared corner is order-independent
(T_i T_j)^m = I                  when a finite corner angle/order m is declared
```

No value of `m`, corner angle, cap, period, or incidence graph may be assumed merely because it is
standard.

### C. Boundary tangent equations

At a fixed seal, derive the linearized eigenspaces

```text
delta e = +T delta e             fixed/Dirichlet-compatible sector
delta e = -T delta e             anti-fixed/parity sector
```

and compare them with the actual scoped `delta phi=0`, normal-derivative-free rule. Determine whether
the complete tangent space is unique before an action or polarization is chosen.

### D. Global inequivalence

Two completions count as inequivalent when they differ by an invariant not removable by an allowed
positive CSN rescaling and source-authorized coframe gauge transformation, including orientation
character, fixed-subspace dimensions, angular holonomy/conjugacy class, or boundary tangent data.

## Falsification and certification contract

The unique-completion lead fails in the audited class if either:

1. at least two inequivalent full lifts survive every requirement that can be stated from current
   authority; or
2. a load-bearing cocycle, corner, or regularity equation cannot be posed without first choosing an
   open topology, chart cover, period, physical readout, or boundary polarization.

A unique algebraic reciprocal `2x2` block is not enough. A unique result must include the full
normal/angular/time-on lift and the complete legal boundary tangent space.

## Frozen outcome classes

1. `UNIQUE_GLOBAL_COFRAME_AND_TANGENT_COMPLETION_IN_AUDITED_CLASS`
2. `MULTIPLE_GLOBAL_COMPLETIONS_SURVIVE`
3. `COCYCLE_CONSISTENCY_REDUCES_BUT_DOES_NOT_SELECT`
4. `GLOBAL_COCYCLE_CANNOT_BE_POSED_WITHOUT_OPEN_TOPOLOGY_OR_COVER`
5. `BOUNDARY_TANGENT_SPACE_REMAINS_POLARIZATION_DEPENDENT`
6. `CURRENT_DATA_DEFINE_ONLY_LOCAL_OR_SECTORWISE_INVOLUTIONS`
7. `AUDIT_INCONCLUSIVE`

Multiple negative/partial classes may apply.

## Fail-closed gates

- Do not treat a chosen `O(1,1)` readout as source-authorized merely because it makes the algebra
  elegant.
- Do not call two lifts equivalent using a gauge transformation that current UDT has not authorized.
- Do not impose an `S2`, torus, Hopf fibration, round cap, angular period, or corner group by habit.
- Do not infer a complete boundary polarization from `delta phi=0`.
- Do not infer a global cocycle from pairwise involution alone.
- Do not promote conditional `C2` boundary slots into the native UDT action.
- Do not identify the static seal with the WR-L horizon or global `X_max`.
- Do not infer bootstrap, scale, action, carrier, source, or mass closure.

Maximum positive conclusion:

`UDT_GLOBAL_COFRAME_COCYCLE_STATUS_CHARACTERIZED`.

No startup-control edit, `CANON.md` edit, GPU work, repository
reorganization, or canonization is authorized.
