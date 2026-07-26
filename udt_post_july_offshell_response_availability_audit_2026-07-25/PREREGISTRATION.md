# Post-July off-shell response availability audit — preregistration

Date: 2026-07-25

Base commit: `b5edb0744ee9c94223ed0b0c090b82c3994341e8`

Question type: `METRIC_LED_SOURCE_AVAILABILITY_AUDIT`.

This preregistration precedes candidate-family content adjudication. The
current frontier and its parent 28-family gate matrix were read to define the
question and freeze the candidate identities. This is therefore a source-led,
non-blind audit. No family closure, candidate gate outcome, or survivor count
has yet been generated.

## Whole question

Does any current post-July UDT scientific family already supply a complete
metric-native off-shell global-local response one-form on one coherent field,
finite-cell boundary, and global configuration space?

The response sought is an object of the form

```text
alpha[X; delta X]
```

defined away from solutions and paired with every admissible local, boundary,
corner, and global variation. This audit asks whether such an interface is
present. It does not invent or derive one.

## Frozen candidate universe

The primary universe contains exactly 30 families:

1. the 27 nonlegacy families `B01`–`B25`, `B27`, and `B28` in the parent
   `EQUATION_FAMILY_GATE_MATRIX.tsv`; and
2. the three scientific families added after the parent audit: `B29`
   global-local relational closure, `B30` founded-phi complete-coframe
   extension, and `B31` macro phi-angular-Xmax modulation.

`B26_LEGACY_PRE_JULY_BRANCHES` is frozen separately as a provenance-firewall
negative control. It may identify a missing gate or counterexample but cannot
supply affirmative UDT response physics.

The exact rows are frozen in `PREREGISTERED_CANDIDATE_UNIVERSE.tsv`. Generated
records from this audit cannot enter the candidate set. Candidate selection is
independent of the outcome.

Frozen registry/package hashes at the base commit:

```text
9ff6b8d1005964ee0721440779e07a78165b47a52a0bcac275b221733ce4fac1  udt_bootstrap_clock_angular_closure_audit_2026-07-24/EQUATION_FAMILY_GATE_MATRIX.tsv
7571a85c60da8edb7f5160063538d0f1261acb29380428eb2e46515530cc4872  udt_global_local_relational_closure_audit_2026-07-25/SHA256SUMS.txt
b9c09d4b661303fd091ecc6995ad62da3b81799f2e7771b43fb172725efc63d7  udt_founded_phi_complete_coframe_extension_audit_2026-07-25/SHA256SUMS.txt
c4cd2aee0db110d2f15aa56a1c14fa5a589cb2dc555b3003d8d179fc625c8342  udt_macro_phi_angular_xmax_extension_atlas_2026-07-25/SHA256SUMS.txt
```

## Six mandatory gates

A `COMPLETE_RESPONSE_SURVIVOR` must pass all six gates in one coherent family
or in an explicitly cited dependency closure whose field identities,
variation domain, boundary, and same-solution branch agree. Cross-branch
splicing is forbidden.

1. `G1_COMPLETE_VARIATION_DOMAIN`: declares every varied local field and the
   admissible boundary, corner, global, gauge, and topology variations.
2. `G2_OFF_SHELL_LOCAL_RESPONSE`: supplies a response pairing away from the
   solution set, not only an on-shell equation, invariant, root, or
   after-solution predicate.
3. `G3_TRACEFREE_ANGULAR_RESPONSE`: contains a native anisotropic/trace-free
   metric or screen response; a proper-volume trace alone fails this gate.
4. `G4_SAME_SOLUTION_MASS_VOLUME_DENSITY`: supplies a native mass functional
   and its variation together with proper-volume variation on the same metric
   solution. Observed density, an external mass, or a supplied-carrier energy
   does not pass.
5. `G5_FINITE_CELL_BOUNDARY_GLOBAL_VARIATION`: supplies differentiable seal,
   boundary, corner, gluing, and global-sector variation for the same
   response.
6. `G6_NATIVE_PROVENANCE`: the load-bearing response follows the July-1 native
   operator lineage. GR/EH, pre-July, supplied carrier, and other imported
   structures may be comparison readouts only.

Allowed per-gate values are exactly:

```text
PASS
CONDITIONAL
ABSENT
INCOMPATIBLE
OUT_OF_SCOPE
PROVENANCE_BLOCKED
```

Allowed final dispositions are exactly:

```text
COMPLETE_RESPONSE_SURVIVOR
PARTIAL_NATIVE_INTERFACE
CONDITIONAL_IMPORTED_OR_POSITED
ON_SHELL_ONLY
GEOMETRY_ONLY
PROVENANCE_BLOCKED
NO_RESPONSE_ROLE
```

No candidate may be a survivor if any gate is not `PASS`.

## Premise ledger

| Premise | Tag | Scope |
|---|---|---|
| exact C0/C1 reciprocal foundation | `pinned-by-THEORY` | founding kinematics only |
| July-1 native-field-equation boundary `f766478` | `pinned-by-THEORY` | ancestry and operator provenance, not calendar or filename |
| 30-family candidate universe | `free-and-explored` | complete frozen current registered family universe, excluding legacy control |
| six response gates | `pinned-by-THEORY` | current `LIVE`/global-local next-step contract |
| carrier `S2` | absent as authority | supplied carrier may only create a conditional gate |
| C-squared/Bach and EH | absent as native assumptions | conditional/comparison families only |
| total proper density value | free and not sampled | no density sweep or fitted value |
| action, source, boundary completion | open | audit checks availability; it does not choose them |
| finite-cell topology or angular lift | free and unselected | no branch ranking |
| CPU/GPU | CPU metadata and algebra only | no PDE, relaxation, or GPU process |

## Characterization, not filtering

The gates characterize what each family contains. They do not reject a family
for lacking a desired physical shape, particle, mass spectrum, or smooth lump.
Partial interfaces and incompatibilities remain recorded evidence. A candidate
that passes all gates must be reported even if it conflicts with the standing
bootstrap/Hopf picture.

## Falsification and certification contract

The verifier must reject:

1. a missing or duplicate primary family;
2. inclusion of a generated audit record as a candidate;
3. affirmative use of the `B26` pre-July control;
4. a survivor with any non-`PASS` gate;
5. a gate credited from a different incompatible branch or variation domain;
6. an on-shell equation, root set, density window, or invariant mislabeled
   off-shell;
7. volume variation mislabeled trace-free angular response;
8. supplied-carrier or external/observed mass mislabeled native mass;
9. a boundary value or gluing condition mislabeled a differentiable boundary
   variation;
10. comparison GR/EH structure mislabeled native operator provenance; or
11. a source hash, frozen package, or unrelated repository path change.

Every affirmative `PASS` must cite exact source lines or a machine-readable
source object. An `ABSENT` result is scoped to the frozen 30-family universe,
not a universal no-go theorem.

## Maximum allowed conclusion

The audit may report one of two outcomes:

- one or more precisely scoped complete response-interface survivors; or
- `NO_COMPLETE_RESPONSE_IN_FROZEN_30_FAMILY_UNIVERSE`, with every partial
  interface and exact missing arrow recorded.

It may not derive the bootstrap-to-local map, reconstruct an action, select a
carrier or topology, calculate density or `Xmax`, begin matter/time-live work,
launch GPU work, canonize, or reorganize the repository.

