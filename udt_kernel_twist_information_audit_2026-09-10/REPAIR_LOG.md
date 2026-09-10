# Preserved construction check repair

Before fresh review, author_01 actually exited 1 at 21:28:38 UTC. The shift-erasure
negative control constructed a 3x3 zero matrix where the shift record was a 3x1 vector.
SymPy raised ShapeError. The original source is checks/INITIAL_check_candidate.py
(SHA-256 1cf29c543298fded3b439d8cc50d2aee80484b98bd806f24b5e5e2bb712b826f).
The original stdout, stderr and exact run metadata are preserved. That run is not a PASS;
the program had not emitted its diagnostic report.

R1 changes only zeros(3) to zeros(3,1) in that control. Candidate equations, comparison
maps and source files are unchanged. The next actual run and later fresh review own
their results; no success is inferred from this repair note.
