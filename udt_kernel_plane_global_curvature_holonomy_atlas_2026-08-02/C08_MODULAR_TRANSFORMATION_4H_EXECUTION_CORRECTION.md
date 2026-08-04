# C08 four-hour continuation — execution-environment correction

Date: 2026-08-04
Base before correction: `273cb386`
Status: `PREREGISTERED_ENVIRONMENT_CORRECTION_BEFORE_PRODUCTION`

## Disclosed failed launch gate

The first invocation of the committed four-hour supervisor did not open the C08 production input.
Its nontrivial toy stopped in `tasks.lib::startTasks_child` because the managed sandbox disables the
localhost socket that Singular's four-worker modular implementation uses for interprocess
communication:

```text
? ERROR opening socket
int port = system("reserve", 1);
open: Error for link ... localhost:0
```

The fail-closed toy consequently reported a zero final identity and the Python assertion stopped the
driver before production. The failed-gate artifacts are preserved as:

```text
C08_TRANSFORMATION_4H_TOY_STDOUT.txt  0cb971207d4897ebd87ff8dd00eb5822b0229b5e2b76a333f06186293d4ffd79
C08_TRANSFORMATION_4H_TOY_STDERR.txt  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

This supplies no algebraic result. No Singular production process remained after the assertion.

## Preregistered correction

The retry may run the exact committed command outside the managed network namespace solely so that
Singular can create its localhost SSI worker links. It does not require or authorize internet or
remote-host access. The polynomial input, modular method, callbacks, four worker count, one-thread
setting, exact identities, four-hour wall limit, 64-GiB aggregate-RSS ceiling, 32-GiB
available-memory floor, 8-GiB swap ceiling, and maximum conclusion remain unchanged.

The supervisor will preserve the failed toy files and write the corrected-environment toy to new
`C08_TRANSFORMATION_4H_RETRY_TOY_*` paths. It must refuse to overwrite either the old two-hour
production evidence or any four-hour production artifact. A failed corrected-environment toy stops
the program again; no further retry is authorized.

This is an execution-environment correction, not a mathematical or resource retuning. The four-hour
clock begins only after the corrected toy passes and immediately before the C08 production process
starts.
