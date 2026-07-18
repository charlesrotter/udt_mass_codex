# Scientific-family migration rule

Date: 2026-07-18

Scope: R1H audit of the 32 proposed B02/B03 scripts. This rule does not
adjudicate the other 1,082 stable identities for migration and authorizes no
move.

## Rule

Filesystem/runtime independence is necessary but not sufficient for an
artifact to move independently. Migration closure must also include the
artifact's scientific family:

1. scripts and outputs introduced as one result-bearing commit family;
2. result, evidence, preregistration, and generated-output companions;
3. conceptual/operator and provenance companions required to interpret the
   script's calculation;
4. frozen, manifest-bound, permanent-control, and current-frontier companions;
5. runtime imports, reads, writes, generated outputs, tests, and current path
   pointers.

A script is independently move-safe only when moving it alone leaves every one
of those relationships intact and does not spatially split a coherent
scientific family from an immutable result, evidence, or provenance companion.
If complete closure contains an immutable-path artifact, a permanent control,
or another unauthorized companion, the partial script move is blocked. The
family is recorded as the atomic unit that would require a future dedicated
adjudication; it is not silently split or promoted to an executable batch.

This is a repository-provenance rule, not a physics judgment. Reference-only
Einstein/Misner–Sharp readouts remain disclosed as `REFERENCE_ONLY` and do not
demote native operator provenance. The two alpha-coupling scripts remain
`MIXED` because alpha enters their tested action/EOM.

## R1H application to B02/B03

The complete individual ledger is
[`B02_B03_SCIENTIFIC_FAMILY_CLOSURE.tsv`](B02_B03_SCIENTIFIC_FAMILY_CLOSURE.tsv).
All 32 candidates have no repository-local import and no runtime file I/O, but
each belongs to one of ten scientific families containing at least one
immutable result or provenance companion:

| Scientific family | Candidate rows | Load-bearing immutable companion class |
|---|---:|---|
| `SF01_THETA0_ACCUMULATION` | 9 | frozen theta0 result/table plus native-field provenance |
| `SF02_TWIN_LADDER_INVOLUTION` | 2 | frozen twin/accumulation results plus native-field provenance |
| `SF03_STABILITY_OPERATOR` | 5 | frozen stability/twin results plus native-field provenance |
| `SF04_ENERGY_ORIENTATION_READOUT` | 2 | frozen energy-orientation result plus native-field provenance; `CANON.md` is a control companion |
| `SF05_LEMMA_D_SEALING_AMPLITUDE` | 1 | frozen Lemma-D/Stage-C results plus native-field provenance |
| `SF06_PHI_ALPHA_COUPLING` | 2 | frozen phi-blindness result plus native-field provenance |
| `SF07_STAGE_D_FORECAST` | 1 | frozen Stage-D result/JSON plus native-field provenance |
| `SF08_HOMOGENEOUS_UNIVERSE_NEGATIVE` | 2 | frozen scoped-negative result plus native-field provenance |
| `SF09_REDSHIFT_OPTICS_N2` | 1 | frozen optics result and frozen-package-referenced geometry record |
| `SF10_UNIVERSE_CELL_FOLD_JC_SIGMA` | 7 | frozen fold/JC/sigma result plus native-field provenance |

Therefore every candidate is
`BLOCKED_IMMUTABLE_FAMILY_COMPANION`, with
`standalone_move_safe=NO`. The proposed B02 and B03 execution batches are
withdrawn. R1H does not invent replacement batches or claim that a future
whole-family migration is safe; such a migration would require new authority
and a separate closure audit covering every listed atomic-family path.

## Coverage and remaining open scope

R1H fully covers the preregistered 32-candidate slice and the exact 134-row R1G
override union. It does not freshly review the other 980 effective-registry
rows, which are explicitly `INHERITED_UNREVIEWED`. It does not reassess the
scientific claims in the frozen companions, change any operator provenance, or
test broader active/archive lane migration. This is one bounded repository
organization tile, not completion of the reorganization program.
