# Preserved author-check correction — one same-premise repair

Initial scientific candidate remains unchanged, SHA1a2a8439f2591631fd52e92b6c1c45c8a6e4e8e60a59c5e4b8642045cd2d5571.
Initial author script/outputs are preserved in commit ee213282; its actual
run reported494 assertions, rc0,1.360s. Do NOT call all494 exact supporting
checks: some denominator probes used Python integer division and therefore
floating point, and the final numeric-inequality "anchor corruption" assertion
was vacuous as verification evidence. This is a checking defect, not a failed
scientific theorem. Parent identified it after the passing run.

Correction: explicitly sympify all four input values before those divisions;
remove the vacuous assertion and its supporting-evidence label. The existing
script is edited in place; original source and raw outputs remain in Git.
The wrong-Green-sign and removed-sphere-term controls remain narrowly labeled
formula checks, not an exhaustive mutation suite. No mathematical claim,
premise, norm, tolerance or result scope changes. Rerun uses a new output stem,
author_checks_corrected, never overwrites the initial evidence. Focused review
of this repair is included in the step1 review budget (one repair used).
