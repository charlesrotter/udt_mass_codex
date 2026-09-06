# Same-premise check repair — focused re-review pending

The initial candidate argument and its five-file freeze manifest are unchanged.
The initial script remains check_exact.py in the parent directory. This separate
repaired script adds only the explicit record-feasibility guard, reject_nonzero
mutation and identifying docstring. Source formulas, classes and controls are
unchanged; no scientific theorem or premise repair occurred.

Actual repaired baseline: PASS,17 guard groups/1887 assertions, same625 records,
same182 constructions/443 rejections. All4 original mutants retain their expected
first failures; the new actual reject_nonzero mutant exits1 at
record_feasibility_not_silently_discarded. Exact commands/streams are retained.
The declared finite grid and threshold-relative guard are not a completeness
proof over arbitrary real records. Initial reviewer independent mathematics
and exact checks remain distinct from this author regression.

This consumes1/1 allowed Step05 repair/focused re-review cycles. No conclusion
about repaired verification is final until focused review completes. The initial
false-pass execution/review history is preserved separately and not relabeled.
