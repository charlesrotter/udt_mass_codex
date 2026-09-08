# Proportional packaging parser correction

The initial assembly check exited1 at nonempty_CF1_freeze,0.261754s/no timeout,
because its parser accepted only CF2's indented hash/filename format, not CF1's
existing bullet filename/SHA256 format. assembly_initial.* and the exact initial
script are preserved. The separate fidelity reviewer independently identified
the same issue. The smallest fix parses BOTH declared frozen formats; no sealed
file, hash requirement, scientific equation, candidate, review or test is altered.
This is a packaging correction, not a CF1/CF2 scientific repair or extra step.
Earlier buffered check results were not emitted and are not claimed as preserved
original output. The corrected complete run uses a distinct capture stem.
