"""Exact diagnostic of two printed conventions, not a processor implementation."""
from fractions import Fraction as F
import json
import sys

mutant = '--drop-algorithm-factor-two' in sys.argv
v = tuple(map(F, (2, 3, 5)))  # FREE diagnostic numbers, not observations
h = tuple(map(F, (1, 2, 3)))  # FREE half-separations in arbitrary units
ad = tuple(-x*y for x, y in zip(v, h))  # TN3397 eq6 with eq7/9
intro = tuple(-x/y for x, y in zip(ad, h))  # eq10, diagonal, zero rotation
factor = F(1) if mutant else F(2)  # printed Algorithm16 coefficient
same_symbol = tuple(-factor*x/y for x, y in zip(ad, h))
full_separation = tuple(-factor*x/(2*y) for x, y in zip(ad, h))
print(json.dumps(dict(mutant=mutant, gradient=list(map(str, v)),
    half_separations=list(map(str, h)), differences=list(map(str, ad)),
    intro=list(map(str, intro)), algorithm_same_symbol=list(map(str,same_symbol)),
    algorithm_full_separation=list(map(str,full_separation))),sort_keys=True),flush=True)
assert intro == v, 'introductory definitions recompute original gradient'
assert same_symbol == tuple(2*x for x in v), 'printed two-convention mismatch'
assert full_separation == v, 'full pair separation resolves this comparison only'
print('PASS: 3 exact diagnostic assertions; not flight-processing validation')
