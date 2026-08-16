# G104 random-reference typing clarification

Date: 2026-08-15

This clarification was recorded after the preregistered algebra ran and before external semantic
review or any BAO/CMB outcome exposure.

The preregistration used the shorthand `mask-only randoms` for the branch in which the random
reference omits a hypothetical physical UDT one-point modulation. That shorthand is too narrow.
Official survey randoms can encode footprint, angular and radial selection, completeness, vetoes,
and other registered observational selection information.

The invariant distinction used by the derivation is therefore:

```text
q = registered survey selection reference,
p = physical observed one-point measure,
p != q only if a separately derived physical modulation is absent from q.
```

The exact identity

```text
p tensor p - p tensor q - q tensor p + q tensor q
  = (p-q) tensor (p-q)
```

is unchanged. No source, fixture, coefficient, operator, or conclusion ceiling changes. The result
landing uses `SELECTION_REFERENCE_MISMATCH` rather than `MASK_ONLY_SELECTION_MISMATCH`. Historical
preregistration wording remains frozen as the audit trail.

This clarification does not assert that such a physical modulation exists or that any mismatch in
real data is UDT rather than survey systematics. That ownership remains `OPEN`.
