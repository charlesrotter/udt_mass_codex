# CMF1 construction record

The initial parent exact-check script failed at parse time: one extra closing
parenthesis in the synthetic trace-sample serializer. The complete original
script and exact.stderr/stdout/receipt are preserved. Removing that parenthesis
changes no calculation, candidate claim, tolerance or saved scientific result;
none had been produced. check_feasibility.py is the repaired implementation.
This is a construction defect, not an adversarial scientific repair.

The initial full406 startup verifier completed with exit0 in exec session85023
and its full PASS output was returned in the tool transcript. It was launched
directly with bounded Git mapping environment, not through capture.py; no
separate startup stdout file or resource/timing receipt is claimed. A captured
full406 audit will be run on final integrated bytes at banking.
