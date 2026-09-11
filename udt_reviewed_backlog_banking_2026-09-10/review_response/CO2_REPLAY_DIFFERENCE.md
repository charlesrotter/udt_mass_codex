# CO2 output correspondence

The unchanged CO2 source script returned0 and all original scientific assertions
passed. Its full stdout differs from the saved output in exactly one JSON field:
`python`, which reports the build date June22 versus August31 of Python3.10.12;
both report GCC11.4.0. Every other field, including all design values, source
hashes, tolerances, controls and finite stress comparisons, is exactly equal.
Both raw outputs and the first strict byte-comparison failure are retained.

check_added_correspondence.py performs the bounded explicit comparison after
this difference was exposed. Its allowed one-field comparison is not a blind
prediction and is not a waiver of any scientific/source change. The supplied
rotation remains shared; this replay does not certify independent astrometry.
No original script, saved result or expectation is rewritten to pretend full
stdout byte identity. Seven other added replay outputs are byte-identical.
