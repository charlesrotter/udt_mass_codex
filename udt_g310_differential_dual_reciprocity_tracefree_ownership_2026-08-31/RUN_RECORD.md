# G310 run record

## Production

```bash
python3 -S derive_ddr_tracefree.py --output DERIVATION_RESULT.json
```

Result: PASS, 14 exact checks. The 133-member rational Lorentz orbit has reciprocal shape rank nine;
the generator-only control has rank eight; the balance annihilator has nullity one and equals
`span(g_ab)`.

## Independent verification

```bash
python3 -S verify_ddr_independent.py --output INDEPENDENT_VERIFICATION.json
```

Result after preregistered R1/R2 repairs: PASS, 32 checks. A distinct constructive basis uses a
`5-12-13` spatial rotation and `5-3-4` rational boost to recover all three diagonal, three
spatial-cross, and three time-cross traceless directions. It then independently constructs and
row-reduces the Lorentz-pairing matrix, obtaining rank nine and nullspace `span(g_ab)`.

## Hostile mutations

```bash
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
```

Result: PASS, seven of seven mutations caught.

## Repository gates

Run before external review and banking:

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest -q
```

Results:

- premise verifier: PASS — 289-row registry and all reported startup/provenance guards;
- repository regression: PASS — 199 passed, one expected xfail in 137.14 seconds.

## External review and repairs

The fresh gpt-5.4 reviewer returned `G310_REPAIRABLE_DEFECTS`. It retained the bounded mathematics
but found that both scripts used `H/2` and that the separate verifier hardcoded rather than computed
the annihilator. The exact R1/R2 repair contract was committed and pushed at `71f45256` before the
repair implementation. Live repaired package replay passes; repair-only external follow-up remains
pending.

Post-repair repository gates:

- premise verifier: PASS — unchanged 289-row registry and all reported guards;
- repository regression: PASS — 199 passed, one expected xfail in 136.69 seconds.
