# G250 banking replay record

Date: 2026-08-24

Final-tree gates run from repository root:

1. `python3 verify_current_scientific_premises.py`
   - PASS: G242--G250 extended startup/premise guards.
   - PASS: exact 233-row registry and current bounded startup route.
2. `python3 udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/verify_package.py`
   - PASS: 26/26 checks; no failed checks.
   - Replayed production 4,096 cases, independent 12,000 cases / 24,010 assertions, and 23/23
     hostile mutations without persistent output.
3. `python3 -m pytest -q`
   - PASS: 155 passed, 1 expected xfail.
   - The xfail is the pre-existing matter-sector HABIT-pin gate, unrelated to G250.

The active startup files satisfy their enforced line, word, and maximum-line-length limits. No
scientific conclusion, observational value, protected payload, or unrelated working-tree path was
introduced by this integration.
