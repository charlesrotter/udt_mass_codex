# P03G global kinematic assembly atlas — preregistration

Date: 2026-07-21

Base: `c89708eec3e415e4f0a052d93c02ab4ad1088512`

Branch: `codex/udt-global-kinematic-assembly-p03g-2026-07-21`

Registered stage: `P03G / PRE_DYNAMICS_GLOBAL_KINEMATIC_ASSEMBLY`

Maximum conclusion:
`CURRENT_GLOBAL_KINEMATIC_ASSEMBLY_CONDITIONS_AND_OPEN_BRANCHES_CHARACTERIZED`

## Why this stage is inserted before P04

P03 completed the registered **point-local** founded-constraint census. It did not establish that
the local configurations patch across a complete finite cell. Proceeding directly to P04 would ask
Charles to choose a dynamics lane while cover, transition, seal-lift, topology, degeneracy, and
global-coframe compatibility data remain uncounted in the current atlas.

P03G is therefore a preregistered, law-neutral correction to the execution order. It does not edit
the frozen P00--P03 packages or claim that the later P11 global-solution stage has been performed.
P11 remains downstream of a selected dynamics and actual solutions. P03G asks only what is required
to turn point-local **kinematic configurations** into global finite-cell configurations before any
law of motion is selected.

## Frozen parent evidence

- `SHA256(P01/SHA256SUMS.txt) = b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad`
- `SHA256(P02/SHA256SUMS.txt) = c56390eb26b80c54a3c3a09f4800086c8dbc00b5bfd40b2038e264e85bec8938`
- `SHA256(P03/SHA256SUMS.txt) = b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be`
- `SHA256(complete-map/SHA256SUMS.txt) = 1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38`
- `SHA256(global-cocycle/SHA256SUMS.txt) = 1297e8f6773f863f426d66f6c4915741a742c1ee13230abf2b066421de49b04b`
- `SHA256(static-seal/SHA256SUMS.txt) = 704b084548a212eabcfb1ac051e89234a7fd91bbeaf7f70abcc28bf63edc7a3b`
- `SHA256(complete-seal/SHA256SUMS.txt) = 3a6cc83e40fe95951b19f37b68b1167a3683cf4f02c0fbf1f52f54d95db99b66`

These packages are read-only inputs. Their records may be cited, not rewritten.

## Whole question

Given the frozen P02/P03 local atlas and the already audited transition and seal algebra, what
additional data must be supplied for local UDT configurations to assemble over a complete finite
cell, which compatibility relations already constrain those data, and which global kinematic
branches remain open before any dynamics is loaded?

This is an assembly atlas, not a search for a preferred topology, action, field equation, solution,
particle, mass, boundary condition, or familiar geometric law.

## Exact bounded regime

- CPU-only exact algebra, deterministic ledgers, and finite witness checks.
- Point-local parent space is the frozen P02/P03 atlas; no local stratum will be deleted.
- Existing derived transition identities may constrain overlaps and closed cocycles.
- Existing seal results may constrain only the exact fields and tangents they audited.
- Covers, incidence/nerve data, transition components, continuous transition moduli, signed-field
  patching, seal lifts, tangent polarizations, caps, degeneracies, and connection branches remain
  explicit independent axes unless an exact cited relation joins them.
- The topology census is deliberately bounded to the alternatives already present in current UDT
  evidence plus an explicit `OTHER_UNENUMERATED` branch. It is not a classification of all
  manifolds, bundles, or singular completions.
- No ODE, PDE, action, variation, evolution, relaxation, empirical target, or comparison readout is
  loaded.

## Question provenance

`METRIC-LED / OBSERVING`: inventory how the complete metric/coframe data can be patched and sealed.
Acceptance is based on coverage, exact compatibility, and preservation of open branches, never on
whether an assembly resembles GR, supports matter, or yields a desired equation.

## Premise ledger fixed before evaluation

| item | tag | permitted role |
|---|---|---|
| UDT metric/coframe configuration | `pinned-by-THEORY` | object whose local realizations are assembled |
| Common-Scale Neutrality | `pinned-by-THEORY` | local positive common-scale equivalence and its overlap bookkeeping |
| dual Reciprocity | `pinned-by-THEORY` | internal reciprocal character; spacetime realization remains conditional |
| finite mirrored cell/no spatial infinity | `pinned-by-THEORY` | demands a complete-cell assembly and boundary accounting, not a topology or field equation |
| global `X_max` | `OPEN_GLOBAL_OUTPUT` | may label a completed cell only after its global meaning is derived |
| cover, nerve, overlap incidence | `free-and-explored` | not supplied by the local metric |
| transition group and cocycle | `PARTLY_DERIVED` | exact audited reciprocal `G/F` algebra; actual cocycle and cover remain free |
| global signed `phi` | `free-and-explored` | existence, zero set, and monodromy must be checked rather than assumed |
| full coframe soldering | `CONDITIONAL_BRANCH` | cannot be inferred from the audited two-channel character alone |
| static seal | `PARTLY_DERIVED` | `phi=0`, parity-preserving `delta phi=0`, normal derivative free |
| complete seal involution/polarization | `OPEN` | no unique lift or full boundary phase space is supplied |
| topology, caps, periods, quotient, no-cap | `free-and-explored` | retain all cited alternatives and an unenumerated remainder |
| degeneracy/type change/interior signature change | `free-and-explored` | retained; regular inverse-metric diagnostics do not cover closure |
| independent connection/torsion | `CONDITIONAL_BRANCH` | retained separately from Levi-Civita metric branch |
| action, equation, source, carrier, mass, charge, scale selection | `EXCLUDED_FROM_P03G` | no role in classification or acceptance |

No numerical physical value, topology, orientation, chart atlas, seal lift, cap, connection,
boundary polarization, or global representative will be fixed by habit.

## Frozen assembly-axis universe

P03G must account for all of these axes without ranking them:

1. local field realization (`C01`--`C07` from P03);
2. cover/nerve and overlap incidence;
3. reciprocal transition component (`G`, `F`) and continuous modulus;
4. closed-path cocycle product, reversal parity, and global obstruction/class;
5. CSN representative changes and global representative existence;
6. signed-`phi` existence, zero set, and possible sign holonomy;
7. coframe soldering and angular lift;
8. static-seal scalar condition and complete boundary tangent/polarization;
9. cap/topology/no-cap and unenumerated topology remainder;
10. regular, degenerate, type-changing, and singular completion;
11. Levi-Civita versus independent connection/torsion branch; and
12. global scale, `X_max`, physical representative, mass/volume, and bootstrap closure status.

Generated records may refine these axes into named branches, but may not remove an axis or rank a
branch after outcomes are visible.

## Registered outputs

- `P03G_PROTOCOL_CORRECTION.md`
- `ASSEMBLY_INPUT_REGISTRY.tsv`
- `GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv`
- `COVER_AND_COCYCLE_BRANCHES.tsv`
- `SEAL_LIFT_AND_TANGENT_BRANCHES.tsv`
- `TOPOLOGY_AND_COMPLETION_BRANCHES.tsv`
- `LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv`
- `GLOBAL_COUNTERMODEL_LEDGER.tsv`
- `UNCOUNTED_GLOBAL_MODULI.tsv`
- `ASSEMBLY_DEPENDENCY_GRAPH.json`
- `STATUS_LEDGER.tsv`
- deterministic generator, independent verifier, corruption catches, reports, commands,
  repository gates, and SHA-256 manifest

## Falsification and certification contract

P03G fails closed if any of the following occurs:

1. a point-local P02/P03 configuration is discarded merely because no global completion has yet
   been supplied;
2. a local reciprocal transformation group is promoted to an actual global cocycle or cover;
3. closed-cocycle parity is mistaken for a selected global `Z2` class;
4. a two-channel reciprocal character is promoted to a complete four-dimensional coframe
   transition law;
5. the static `phi` seal wire is promoted to a complete seal involution or boundary polarization;
6. a listed cap witness is promoted to the unique topology, or the bounded witness list is called
   exhaustive;
7. regular inverse-metric calculations are used to erase degenerate/type-changing completions;
8. CSN is used to select a physical representative or scale;
9. `X_max`, total mass, volume, density, or bootstrap closure is assigned without a complete global
   solution and native matter definition;
10. an action, equation, solution goal, GR template, particle criterion, or merit score enters the
    assembly logic;
11. any frozen parent package changes; or
12. generated tables fail deterministic replay, independent reconstruction, or an exercised
    corruption catch.

The verifier will mutate each load-bearing claim class and require failure, including missing axes,
promoted local-to-global claims, collapsed transition parity, lost continuous moduli, false seal
completion, false topology exhaustiveness, deleted degeneracy, hidden dynamics tokens, and parent
hash drift.

## Maximum allowed interpretation

P03G may report the currently derived compatibility conditions and the data still required for a
global finite-cell kinematic assembly. It may not claim existence, uniqueness, physical selection,
on-shell status, global solution completeness, topology selection, a dynamics law, or bootstrap
closure.

P03G stops after banking and verification. P04, P11, ODE/PDE work, GPU work, comparison, canonization,
or repository reorganization requires a new explicit dispatch.
