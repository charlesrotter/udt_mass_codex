# G311 repair preregistration

Date: 2026-09-01

External verdict: `G311_REPAIRABLE_DEFECTS`.

The reviewer found no scientific defect in the two-level G311 landing. These repairs are frozen
before changing any affected implementation or evidence language. They may not alter the scientific
question, theorem, counterresponse, or bounded conclusion.

## R1 — dependency-free independent verifier

Replace the undeclared SymPy dependency with a standard-library-only implementation that remains
independent of `derive_covariant_response.py`. It must independently reconstruct:

- rank nine of the reciprocal tangent span;
- the one-dimensional response annihilator spanned by the metric;
- the conformally flat, non-Einstein time-live countermetric at `b=1,t=0`, including nonzero
  trace-free Ricci and zero Weyl;
- the conditional G301 degree count.

The replacement must run under `python3 -S`, reproduce a saved machine-readable result, and share
no production imports.

Falsification: any changed scientific value, nonzero Weyl component, rank other than nine, response
annihilator other than the metric line, or hidden non-standard dependency fails R1.

## R2 — intake-self-contained aggregate replay

Remove every repository and Git-history access from the registered sealed aggregate replay. The
intake verifier must use only files inside its own package plus a writable temporary directory.
Repository-only premise and regression gates may remain documented as upstream banking gates, but
must be explicitly outside the sealed replay and must not be invoked by it.

The frozen preregistration commit and parent remain evidence recorded in
`PREREGISTRATION_ANCESTRY.md`; this repair does not rewrite that historical claim.

Falsification: any registered sealed command that resolves a path above the package, invokes Git,
or requires an undeclared external dependency fails R2.

## R3 — hostile-harness evidence grade

Keep the hostile mutation harness as useful shared-code regression evidence, but remove every claim
that it is implementation-independent confirmation. The dependency-free independent verifier is
the separate implementation evidence; the hostile harness only proves that specified mutations are
caught by the production machinery.

Falsification: any package ledger, report, or verifier that grades the hostile harness as independent
confirmation fails R3.

## Retained landing

```text
FULL_COVARIANT_RECIPROCITY_CLOSES_RESPONSE_SHAPE_ONLY__RESPONSE_CONSTITUTION_REMAINS_OPEN
```

Strongest retained conditional landing:

```text
G301_FAITHFUL_BRANCH_GIVES_EINSTEIN_SPACE_DYNAMICS
```

Neither landing may be strengthened during repair. A fresh repair-only external follow-up is
required before G311 can be graded `G311_ACCEPTED_WITH_RESPONSE_CONSTITUTION_BOUNDARY`.
