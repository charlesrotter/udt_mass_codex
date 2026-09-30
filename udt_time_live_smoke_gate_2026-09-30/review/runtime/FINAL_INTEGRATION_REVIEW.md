# Final SMK1 runtime integration review — ACCEPT_WITH_LIMITS

The repaired checkpoint/runtime implementation and its final operational routing
are acceptable within the tested engineering scope. R1 (partial commit-marker
publication) and R2 (invalid endpoint restart false pass) were independently
reproduced before repair and are closed by the separately preserved repaired
review. Their original failing evidence remains intact. No scientific grade,
premise, native-dynamics selection or broader-solver claim is strengthened.

Reviewer `/root/smk_runtime` is an actual separate conversation context with the
same inherited model; different-model independence is not claimed. Parent startup
and full-premise evidence are attributed, not independently replayed here. The
reviewer inspected the small runtime source, designed and ran CPU fault tests,
then reviewed repaired source and operational records. Production output and
parent conclusions were visible before the final saved-artifact checks. Numerical
evolution was not independently implemented or rerun on a GPU. All reviewer
writes remain under review/runtime; no protected payload was accessed.

The exact source review is preserved in REPAIRED_REVIEW.md and its manifest.
Nine CPU repair checks passed in 0.9284 seconds at 377476 KiB peak RSS. Actual
save-path interruption before publication recovers the earlier checkpoint;
interruption after publication exposes the completed new checkpoint. Marker
overwrite and corrupt committed payloads are refused. Diagnostics remain
ineligible. Invalid and nonfinite-derived endpoint residuals reject before
completion, while a valid endpoint completes. These are fault-injection and
control-flow checks, with explicitly CPU-mocked CUDA entry points where stated.

A final independent direct read of saved checkpoint arrays, without the producer
loader, verified metadata/payload hashes and identical raw float64 bytes across
uninterrupted, resumed, SIGTERM-resumed and SIGKILL-resumed endpoints. All have
shape [3,5,32] and state-byte SHA-256
`ac31b18262fe9a8515c5f7e8e31ab79c1e1fdedcfc5d804c0e5daea45463c61a`.
NumPy spectral differentiation across the saved valid checkpoints gives maximum
momentum residual `6.074456215809931e-11`, agreeing with the parent-recorded
`6.074456909699322e-11` within floating-point implementation differences and
well below the frozen 2e-6 limit. All 18 stdout/stderr hash pairs match the parent
result. The uninterrupted log records torch 2.5.1+cu121, Tesla V100-PCIE-32GB,
float64, completion at t=4 / step 600, and 42496 bytes peak Torch allocated memory.
These log checks inspect evidence of parent-owned GPU execution; they do not
claim this reviewer independently launched those processes.

Final exact binding: all 1351 paths in FINAL_INTEGRATION_FREEZE.json match their
SHA-256 entries, checked by streaming 126086067 bytes in 0.0851 seconds. All 643
previous paths remain bound; only AGENTS.md, HANDOFF.md and LIVE.md differ from
their previous bindings. The 708 added entries are completed package inputs.
No protected path occurs in this map. At audit time the branch is grok, HEAD
622d1700d91705320ee17e79ed5fd92bc174d752; the tracked delta is exactly those three
operational files. The final freeze hash is
`64349bc75e15559b2e66b2775046b3169d142fa89a71e4bdd33a589948131a6b`.
Hash correspondence is not historical scientific re-proof.

The exact AGENTS change makes short end-to-end checks mandatory before
multi-hour runs and explicitly requires new checks for changed solvers or
dimensions. LIVE/HANDOFF retain the broader exploration objective, the bounded
smoke return, the requirement for a specified solver and representative load
measurement, and a written production dispatch before longer runs. They do not
treat SMK1 as transferable certification. WORK_RECORD.md accurately preserves the
initial failed review, repaired operational result, limits, parent/reviewer
division of work and unchanged scientific dependencies. The final rounding and
spacing repairs were inspected; no further substantive objection remains.

Exact additional CPU commands (each exited 0 within the declared budget):

```sh
timeout 180s python3 udt_time_live_smoke_gate_2026-09-30/review/runtime/saved_runtime_check.py > udt_time_live_smoke_gate_2026-09-30/review/runtime/saved_runtime_check.stdout 2> udt_time_live_smoke_gate_2026-09-30/review/runtime/saved_runtime_check.stderr
timeout 180s python3 udt_time_live_smoke_gate_2026-09-30/review/runtime/final_binding_check.py > udt_time_live_smoke_gate_2026-09-30/review/runtime/final_binding_check.stdout 2> udt_time_live_smoke_gate_2026-09-30/review/runtime/final_binding_check.stderr
```

Those completed post-freeze reviewer outputs are bound separately in
FINAL_ATTESTATION.json. Its accepted_sha256 map is exactly the final integration
map and does not fold final outputs back into their own input freeze.

Remaining limits: the lock is cooperative; the local hard-link publication
semantics are assumed; no all-interruption or power-loss guarantee, multi-hour
drift/throughput certificate, general three-dimensional solver validation,
production-memory sizing or continuum theorem is supplied. The original
scientific checks and premises remain inherited at their unchanged scope. The
parent's final full 406-row audit and normal binding checks remain parent-owned
completion gates; this attestation does not claim to have run them.
