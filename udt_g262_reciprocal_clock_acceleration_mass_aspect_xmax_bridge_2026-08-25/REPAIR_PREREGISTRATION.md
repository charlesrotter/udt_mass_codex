# G262 external-review repair preregistration

Date: 2026-08-25

External verdict: `ACCEPT_WITH_REPAIRS`.

The bounded scientific landing is frozen. These repairs may correct reporting scope and external
runtime disclosure only. They may not promote the raw wall flux to mass, import a boundary action,
identify a generator or normalization, select `Xmax`, add a source/history law, or continue the
research.

## R1 — retain the pre-existing raw wall lapse flux

Amend the G262 report, exact derivation, lay report, status/ownership surfaces, and package verifier
to acknowledge the already-sealed exact WR-L raw wall lapse flux

\[
\Phi_{\rm wall}=-2\pi X.
\]

Preserve its exact ownership: this is a metric flux on the supplied WR-L representative, not a
native mass, normalized charge, global `Xmax` law, or source/history equation. A physical mass or
charge interpretation still requires a complete action or generator, normalization, reference,
orientation, and boundary prescription.

**Pass:** every blanket statement that G262 found no boundary-side value relation is narrowed, and
the flux is included without promotion.

**Fail:** the package omits the flux, calls it physical mass/charge, or uses it to choose a history,
`Xmax`, or a normalization.

## R2 — disclose external replay scope

Record that the external reviewer reran the dependency-free exact-Fraction replay, mutation harness,
and package verifier successfully, but could not rerun the SymPy production derivation because
SymPy was absent in its isolated runtime. Preserve the locally saved SymPy result and the
implementation-distinct dependency-free replay as separate evidence.

**Pass:** the external gate is not described as a live reproduction of the SymPy derivation.

**Fail:** the package claims the reviewer reran SymPy or hides the runtime limitation.

## Maximum repair landing

```text
REPAIRS_IMPLEMENTED__BOUNDED_SCIENTIFIC_LANDING_UNCHANGED
__EXTERNAL_REPAIR_FOLLOWUP_REQUIRED
```

No repair can establish a local rest-mass dilation law, normalized physical UDT mass, a source,
numerical or global `Xmax`, or a valued-history equation.
