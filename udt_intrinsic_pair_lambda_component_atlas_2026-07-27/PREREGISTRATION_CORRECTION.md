# Preregistration correction — numerical Torch cross-method tolerance

Date: 2026-07-27

Parent preregistration: `6df7f07`

Status: **CORRECTION BEFORE INDEPENDENT TORCH REPLAY**.

The preregistration froze five Torch holdout values and required a preregistered tolerance but
omitted the numerical tolerance. Use the exact tolerance already audited in the parent independent
full-Riemann/autodiff verifier:

```text
|D_Torch - D_exact| <= 2e-9 * max(1, |D_exact|).
```

This tolerance is copied without retuning from
`udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/verify_intrinsic_pair_independent.py`.
It is frozen before any of the five newly preregistered Torch holdouts are evaluated.

The exact polynomial, exact roots, and exact interval census remain controlling. The Torch replay is
a cross-implementation geometry check only. The original `PREREGISTRATION.md` remains unchanged as
historical evidence.
