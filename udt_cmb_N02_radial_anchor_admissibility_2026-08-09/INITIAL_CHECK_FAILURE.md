# Initial derivation-check failure

The first production run stopped at `K11_round_wall_limit_point=False`. The mathematical rows were
correct; the check incorrectly assumed the first three endpoint rows were the three round rows.
Rows are grouped by each `n`, so nonzero-mixing rows intervene.

The gate was repaired to select `family == R0_ROUND_P1`, require exactly three rows, and then test
their limit-point classifications. No candidate universe, formula, tolerance, or conclusion was
changed. The final run passes 20/20 keys. This failure is preserved because the original positional
assertion was a genuine false-pass/false-fail risk.
