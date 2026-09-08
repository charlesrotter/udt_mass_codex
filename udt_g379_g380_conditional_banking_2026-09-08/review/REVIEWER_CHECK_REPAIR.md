# Reviewer-only correspondence harness resource correction

The initial independent correspondence run began 2026-09-08T22:12:08.107032 UTC
and exited 1 after 0.090971668 seconds, no timeout, maximum RSS 31,320 KiB.
Its original script is check_correspondence_initial_failed.py; original empty
stdout, stderr and receipt remain correspondence_initial.*.

The subprocess reading the baseline assembly_corrected.stderr Git blob exited
128 because Git tried mapping a packed-object file beyond the inherited 512 MiB
address-space limit. This is a Git resource failure, not a failed byte equality
or a scientific result. The completed partial check dictionary was still in
memory and not printed when the subprocess raised; those initial partial
results are not represented as preserved stdout.

The finite diagnostic is to reduce per-command Git packed-object window and
cache limits to 16 MiB and 64 MiB, retaining the same 512 MiB/60-second capture
budget and one library thread. A read-only probe of the exact failed blob with
those Git options succeeded. No repository configuration was changed.

The corrected script adds only those two per-command options and an exception
hook that prints any partial dictionary before subsequent unexpected failure.
All correspondence assertions and scientific/source bytes remain unchanged.
The complete replay uses a fresh output stem and is a new execution, not a
recovered original stream. This reviewer implementation correction consumes
no author-science repair and does not alter the grouped documentation repair.
