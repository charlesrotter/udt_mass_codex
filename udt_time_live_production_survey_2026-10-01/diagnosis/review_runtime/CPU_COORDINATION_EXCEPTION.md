# Short operational CPU coordination departure

The runtime reviewer started the captured first-pair receipt/log/hash check at
2026-10-01 14:11:16.561433 UTC immediately after independently seeing the completed
GPU-controller receipt. The parent was still finishing authenticated assembly
while the original clock producer occupied the other CPU slot. The message
reserving that assembly slot arrived after the runtime check had been launched.

The extra check lasted 1.63276558 seconds and reached 64,052 KiB RSS (62.55 MiB),
with a 2 GiB address-space limit and no wall/CPU deadline. It used standard-library
JSON/log parsing and SHA-256 payload authentication, with no NumPy arrays, extra
GPU process, changed scientific criterion, or reported resource exhaustion.
This was nevertheless a departure from the maximum-two-CPU-check coordination
rule; its operational character does not erase the extra process. The parent
reported approximately 1.6 seconds of overlap with assembly and clock work.

The immutable receipt is `first_pair_operations_capture.json`; successful
results remain in `FIRST_PAIR_OPERATIONS.json`. The reviewer reported the
departure immediately and released the second slot to the mathematical reviewer.
Subsequent CPU checks require explicit slot allocation from the parent before
launch. No numerical result is strengthened by this exception or its disclosure.
