# External review adjudication

The fresh sealed reviewer returned `PASS_WITH_CAVEATS`. Every scientific and numerical caveat is
accepted without qualification.

## Accepted result

The independent reconstruction confirms the primary statistic, correct marginal-covariance
operation, and secondary shape diagnostic. The review found no scientific numerical/type blocker
and no interpretation overreach in the stated conclusion ceiling.

## Portability repair

The review intake contained the exact public table and precision products, but the bundled replay
script defaulted to the scratch-disk data location. This did not affect the result: the reviewer
independently reconstructed the statistic from the intake-local copies.

For future sealed replays, `verify_independent.py` now accepts:

```text
--data-dir PATH
--check-only
```

Thus a read-only intake can run, from its root,

```bash
python3 package/verify_independent.py --data-dir data --check-only
```

without accessing the repository or writing an output file. This is an operational replication
repair only. It changes no preregistered value, source row, model formula, covariance operation,
threshold, result number, or conclusion.

## Final status

```text
VERIFIED_WITH_CAVEATS
__FROZEN_G99_P1_NOT_REJECTED_BY_DES_DOVEKIE
__LOW_CHI2_REFERENCE_WARNING
__MODEST_SECONDARY_SHAPE_SHIFT
```
