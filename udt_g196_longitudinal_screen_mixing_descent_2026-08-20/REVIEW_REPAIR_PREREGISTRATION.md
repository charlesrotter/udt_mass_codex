# G196 external-review repair preregistration

Date: 2026-08-21

This freezes two bounded repairs before any repair edit or repair replay. Neither repair may alter
the metric family, candidate formulas, numerical census, tolerances, saved results, exact theorem,
or bounded scientific landing.

## R1 — independence-scope correction

Preserve the original preregistration as historical evidence, but append a dated correction and
update current evidence prose so that it states exactly:

- the Torch metric-jet, inverse-metric, Christoffel, Riemann, screen-connection, and tide
  contractions are implemented independently of the SymPy production script;
- the interval Jacobi IVP comparison is not an independent metric-to-Jacobi derivation;
- both the direct second-order IVP and ordered `L,K` IVP use coefficients from the same separately
  coded `candidate_matrices(...)` path, so their agreement is formula-level regression evidence.

R1 passes only if no current report or evidence-gate text calls the entire metric-jet/IVP leg fully
independent. The saved numerical results and their hashes must remain unchanged.

## R2 — Torch-import-safe no-write replay

In `G196_NO_WRITE=1` mode only, set Python's in-process `tempfile.tempdir` to the already declared
`TMPDIR` before importing Torch. This bypasses Python's writable-directory probe used by Torch's
optional serialization import; it does not create a temporary file or change any numerical code.
Normal evidence-producing execution remains unchanged.

R2 passes only if:

1. the registered no-write package replay exits zero when `TMPDIR`, `TMP`, and `TEMP` name an
   existing but non-writable directory;
2. no file is created or changed in that directory or in the evidence package;
3. the fresh production, independent, and hostile-control results remain byte-for-value identical
   to their sealed JSON artifacts;
4. all original counts and ceilings remain unchanged.

## Maximum repair conclusion

Passing R1 and R2 may close only the external review's evidence-description and replay-portability
defects. It may retain `G196_DIRECTIONAL_DESCENT_ACCEPTED_WITH_CAVEATS`; it cannot strengthen the
bounded family/germ theorem or remove its scientific caveats.

