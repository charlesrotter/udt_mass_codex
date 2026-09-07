# Serial-launch safeguard correction

Before candidate freeze, author_corrected was launched with a one-second tool
yield. The next mutant was launched before the yielded session was observed
complete. The saved capture intervals overlap by about0.042seconds
(14:30:03.496550UTC +1.225390820seconds versus14:30:04.680025UTC).
This batch did not meet the declared serial-launch safeguard; actual simultaneous
child instruction execution is not separately measured. Do not relabel it passed.
The per-child512MiB/60second caps remained in force, with about49MiB measured
RSS per child; no GPU or production solve was used. All original evidence remains.

Correction: serial_author, serial_mutant_harmonicity and serial_mutant_fixed_phase
were launched with ten-second tool yields, awaiting each completed result before
the next launch. Their recorded intervals do not overlap. Baseline passes16 groups;
both ACTUAL mutants exit1 at their intended guards. Each stdout is byte-identical
to its earlier counterpart (three cmp checks exit0). These are same-code regression
reruns, not independent review or scientific repairs. No resource cap increased.
