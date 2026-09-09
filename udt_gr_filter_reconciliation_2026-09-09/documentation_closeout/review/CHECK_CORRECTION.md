# Reviewer receipt-inspection correction

2026-09-09. `documentary_correspondence.{json,stdout,stderr}` preserves an
actual failed diagnostic, not a source defect. The new reviewer's inspection
script initially asserted the literal shorthand `'47/47'` appeared in the
saved G351 subprocess stdout. Its actual output is structured JSON with
`checks_passed: 47`, `checks_total: 47`, 47 true named checks, no failed
checks, and `all_passed: true`.

The exact replaced source line was:

```python
assert '47/47' in utility['g351_replay']['stdout']
```

The correction parses that saved JSON and checks its numeric fields,
named-check count/values, failures and all-passed flag. No historical
receipt, guard, test, scientific source or pass gate was modified. The
failed capture remains; the corrected execution uses a separate capture.
This is documentary receipt inspection, not a new independent G351 replay.
