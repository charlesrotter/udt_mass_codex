# Fresh source-first adversarial review

## Independence protocol

A fresh adversarial context read only the seven preregistration inputs and all
sixteen frozen cited sources. It froze its algebraic rulings and complete
twelve-by-nine gate matrix before reading `ALGEBRA_RESULT.json`, the production
gate matrix, verifiers, or reports. It made no file edits and ran no GPU work.

The later production comparison changed 26 gate cells conservatively. No
change altered the maximum conclusion or created a complete survivor. The
review also found a thirteenth distinct source family, added through the
preregistered append-only route. The effective matrix is frozen in
`CONNECTOR_GATE_MATRIX.tsv` and its exact 117 gate values are enforced by
`verify_connector_audit.py`.

## Independent algebraic ruling

For

```text
J(delta X,delta O)
 = (A_X delta X+A_O delta O, -R_X delta X+delta O),
```

the reviewer independently derived

```text
ker J = {(x,R_X x): x in ker(A_X+A_O R_X)}.
```

This needs the lower identity block and a common differentiated root/domain;
it does not require `A_X` to be invertible. In finite square controls,
`det J=det(A_X+A_O R_X)`.

Exact countercontrols independently establish that feedback can create or
remove a kernel, a root does not determine its derivative, and a singular
linearization does not determine nonlinear branch existence. In particular,
`x^2+lambda^2=0` and `x^2-lambda^2=0` have the same zero linearization at the
origin but respectively an isolated real root and two crossing real branches.

## Source-first physical rulings

- `G4` is `ABSENT` for all thirteen candidates. None of the cited evidence gives
  one complete same-branch `(g,phi,matter,boundary)` witness.
- `G9` is `ABSENT` for all thirteen. No cited source gives a noncircular physical
  bootstrap selector.
- `C01` is exact algebraic architecture, but its physical `A`, `R`, common
  domain, and boundary realization are uninstantiated. This follows directly
  from S01 lines 49-52 and 241-249.
- `C02` has a metric-native local clock-tidal kernel. Its parallelism and
  descent remain conditional, while both feedback arrows are absent (S02
  lines 20-54 and 80-90).
- `C03` has a genuine trace-free curvature response and global integral type,
  but UDT has not selected that functional or its global-to-local use (S01
  lines 85-93).
- `C04` is trace-only through volume unless the missing native mass response
  supplies more structure; its moving-boundary domain is conditional (S01
  lines 64-93 and 178-191).
- `C05-C07` are conditional toric/holonomy/topological structures. They do not
  supply a physical selector or complete response (S09 lines 78-98 and
  126-159, together with S10, S12, and S14).
- `C08-C09` give exact local metric structures, with global persistence or
  local-to-global use only conditional. They do not furnish a complete
  branch.
- `C10` is stricter than a merely missing arrow: its global-to-local use is
  `PROVENANCE_BLOCKED`. A moving endpoint gives a response only after a
  boundary functional is specified; it cannot derive that functional (S11
  lines 33-66 and 163-191).
- `C11` gives conditional local pair-depth and global diameter types, but no
  complete physical observer-pair branch.
- `C12` is absent at every gate. Native energy and mass are named requirements,
  not existing metric-native response objects.
- `C13` is the append-only general Levi-Civita curvature-holonomy family. S13
  derives a bounded local irreducible/flat curvature-algebra dichotomy but no
  closed-loop theorem, realization law, or bootstrap arrow.

The reviewer identified `C06` holonomy as the nearest conditional mathematical
two-arrow model. It is not a physical bootstrap closure because the character,
line, caps, same complete branch, and physical use are unselected.

## Minimum missing object

The independent minimum is one metric-native differentiable coupled closure
section `(A,R)` on a single complete, gauge-quotiented finite-cell
configuration branch. It must include the native energy/mass/curvature
observables actually used, moving boundary/corner/gluing data, native dual
pairing and normalization, the physical metric-ontology branch, global
descent, and nonlinear regularity/continuation data.

Owner “optimization” remains mutual two-arrow tuning. Requiring a scalar
objective would add a premise.

## Production corrections caused by the review

The review required and the package now contains:

1. the general kernel-graph statement with common-domain and same-root scope;
2. wording limited to the *linearized* kernel condition;
3. a genuinely non-gradient full-rank vector closure, replacing an accidental
   gradient example;
4. repaired independent same-root and boundary-domain controls, with
   scientific algebra separated from artifact-integrity checks;
5. scalar-curvature wording limited to algebraic Ricci trace and pointwise
   trace-free response; and
6. the append-only C13 curvature-holonomy census correction.

The persistence/stability safeguard remains explicitly open; it is not counted
as a computed control.

## Review verdict

```text
VERIFIED-WITH-CAVEATS
EXACT_COUPLED_NONTRIVIALITY_SKELETON
NO_COMPLETE_METRIC_NATIVE_BOOTSTRAP_CONNECTOR
```

This is a bounded current-source result, not a universal no-go theorem and not
a matter-emergence derivation.
