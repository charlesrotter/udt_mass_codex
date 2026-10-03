# CPW1 exact-comparison implementation repair

The first conformal bookkeeping check failed at the intentionally incorrect
affine-rescaling negative control: SymPy factored its computed and expected
nonzero matrices differently. The original script, freeze and failed capture
remain unchanged. This is not a scientific negative result or a passed check.

The frozen one-case diagnostic independently expanded their difference to zero
and retained the nonzero derivative control(-25,-15,-20,0). The exact stdin
executed by the captured python3 - command is preserved in
checks/representation_diagnostic_stdin.py; it is a record, not a second run.

The repaired script changes only that matrix equality to componentwise expanded
difference=0. Equations, cases, normalization, countercontrol and resource bounds
are unchanged. The complete repaired run passed all six assertion groups in
three families,0.415s,48180KiB,Python3.10.12/SymPy1.13.1. Its source and original
version are bound by REPAIR_FREEZE. Fresh reviewers still must inspect the actual
repair and its scientific scope. No free-clock limiting theorem was computed.
