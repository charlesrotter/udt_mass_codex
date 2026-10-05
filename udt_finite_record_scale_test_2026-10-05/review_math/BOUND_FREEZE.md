# Independent bound-check freeze

Before running: exact rational arithmetic only, no incidence cases, no fits.
Check each conservative constant in SOURCE_FIRST.md and the incidence root
bracket for the entire declared compact box. Counterchecks increase x to 1e-4
and increase the proposed accuracy to eta=1e-6; each must fail the corresponding
derived bound. These counterchecks test this certificate, not actual failure
of the physical model. Independent script, no import of parent candidate code.

CPU only, 2GiB virtual memory, one BLAS thread, no wall/CPU timeout, capture.py.
Expected output small JSON with exact rational strings and floating display.
Maximum conclusion: the analytic inequalities are arithmetically sound under
their stated hypotheses; no sampled arithmetic can substitute for the proof.
