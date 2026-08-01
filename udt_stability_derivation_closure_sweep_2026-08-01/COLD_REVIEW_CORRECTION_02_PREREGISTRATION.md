# Cold-review correction 02 preregistration

Date: 2026-08-01  
Trigger: fresh cold semantic review, before correction mutation

## Finding

`O05`, one compatible F02/F07 premise stack, is labeled `FORMAL_COMPATIBILITY_ONLY`. The inherited
joint-realization evidence grades this exact gate as partial: the separate modules have premise
stacks, but that does not supply one common compatible stack. `O01` remains the formal-module object.

## Frozen correction

Change exactly `O05` to `PARTIAL_CONSTRAINT_ONLY` and update only mechanically dependent Q01 and
overall status counts. Expected final census after corrections 01 and 02:

```text
DERIVED_SCOPED_OBSTRUCTION             3
FORMAL_COMPATIBILITY_ONLY              2
PARTIAL_CONSTRAINT_ONLY                4
UNDERDETERMINED_NO_NATIVE_OBJECT       6
NOT_APPLICABLE_AFTER_UPSTREAM_RESULT   0
```

The overall outcome, every other object status, and every readiness ruling remain unchanged.
