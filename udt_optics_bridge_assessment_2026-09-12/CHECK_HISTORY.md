# OB1 construction/check history

Initial candidate and frame were written before author computation; hand formula exploration
was disclosed. First exact run13:49:29.150969UTC failed at forward_root_is_solution, exit1,
0.593926s. The direct original-null residual guards had passed. Python list membership was
comparing SymPy expression structure rather than algebraic equality of differently factored
roots. The saved initial code and full failed streams remain in checks/author_initial*.
The smallest repair compares simplify(candidate-root)==0 against the independently solved
roots. This is an implementation comparison repair; no mathematical candidate or tolerance
changed. Reverse-root guard received the same correction before rerunning. Later checks and
review must confirm the repair; the initial failure is not relabeled a pass.

Repaired author run13:50:02.705759UTC passed47 exact identity/diagnostic guards, exit0,
0.851592s,52100KiB, Python3.10.12/SymPy1.13.1. Six subsequent explicit computation mutants
(delay sign, detector clock factor, retained density, comparator ordering, wrapped alias
denial and omitted frequency errors) each exited1 at its named guard. Actual stdout/stderr,
argv and limits are preserved; checks/MUTATION_RESULTS.json is the summary. These include
finite control repetitions and are not47 independent theorems or an apparatus certification.
No candidate science changed. Initial candidate and repaired implementation are frozen for
the separate-context review; its source-first stage must not be described as blind discovery.
