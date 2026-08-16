# Blind-review adjudication

The `REPAIRS_REQUIRED` return is accepted in full.

## Repairs implemented

1. `verify_nonflat_exact.py` independently derives the coframe structure from exterior forms and
   compares all `64` bracket, `64` connection, and `256` Riemann components exactly against the
   production component record. It imports no production implementation.
2. `run_catch_proofs.py` now executes actual false same-`W`, wrong vertex, wrong Riemann contraction,
   normalization, twist-erasure, jet-sign, control-drop, rank, and selection mutations.
3. Production evaluates null/screen and Jacobi-vertex residuals exactly.
4. The mixed coefficient is formed a second way as `nabla_K U + [U,K]` and compared with
   `nabla_U K`, rather than subtracting one expression from itself.
5. The finite-difference moving-frame replay is explicitly supplementary. The exact exterior-form
   comparison now carries preregistered F03.

No physical claim, control, tolerance, profile, or observational input was changed. A bounded
follow-up must verify these exact repairs before the package can be banked.
