# G309 run record

## Production

```bash
python3 -S derive_strengthened_history_audit.py --output DERIVATION_RESULT.json
```

Result: PASS, 13 exact algebra/flatness checks plus the registered high-precision witness. At
`X=1`, `epsilon=0.1`, `T=1`, the deformation has
`Q=-0.1122170734375668...` and `R=12.7896011305518...`, versus base `Q=0`, `R=12`.

## Independent verification

```bash
python3 -S verify_strengthened_history_independent.py --output INDEPENDENT_VERIFICATION.json
```

Result: PASS, 28 checks. Maximum base trace-free gap `2.220446049250313e-16`; maximum deformed gap
`0.13333930068074173`; maximum sampled scalar-curvature difference from 12
`1.7723697334331678`.

## Hostile mutations

```bash
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
```

Result: PASS, four of four mutations caught.

## Repository gates

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest -q
```

Results: current 289-row premise registry PASS; `199 passed, 1 xfailed in 137.51s`.

These two results are repository provenance gates. They are not package-local commands and are not
promised as replayable by a reviewer restricted to a sealed intake.

The first production attempt was interrupted after an unnecessary full symbolic expansion proved
slow. The exact logarithmic-derivative identity was then used; it changed no preregistered witness,
formula, or conclusion.

During the first sealed-intake replay, the saved result unexpectedly showed the older 17-check
count. The pre-optimization process had survived its visible interruption and completed late,
overwriting only the saved representation. Repair `3344ef0e` preregistered regeneration from the
current source, an exact 13-check package gate, and pre-seal package verification. Independent and
hostile outputs, formulas, numerical witnesses, and the scientific landing did not change.

The fresh external reviewer accepted the bounded scientific landing with stated caveats and
independently reproduced the load-bearing witness. Its production replay exposed a missing-SymPy
portability defect. Repair `4280cb5d` preregistered replacement of that replay by a dependency-free
exact polynomial/flatness implementation, live-versus-saved equality in the package verifier, and
the repository-versus-sealed replay wording above. No scientific claim changed.

The repair-only follow-up ran all four registered commands under `python3 -S` in a fresh ephemeral
copy and returned `G309_REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`.
