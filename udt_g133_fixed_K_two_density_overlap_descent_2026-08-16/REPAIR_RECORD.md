# G133 repair record

## Production output serialization

The first production run completed the symbolic checks but failed while serializing SymPy Boolean
objects to JSON. The script was repaired to convert every check result to a native Python Boolean
before constructing the output object.

This repair changed no equation, witness, tolerance, candidate, or landing. The pre-review repaired
route passed 25/25 exact checks.

## Independent evidence hardening

Before external review, the independent route's area-weight and two-form controls were strengthened
from assigned exact values to separately constructed four-dimensional Lorentz Gram calculations.
The endpoint calibration check now constructs two distinct pair metrics and explicitly recharts one
endpoint. The pre-review strengthened route passed 24/24 and did not import the production code.

## Fresh external-review evidence repairs

The fresh reviewer returned `PASS_WITH_REPAIRS` and retained the mathematical landing. It correctly
found that the original direct-overlap check had first defined `J_AC=J_BC J_AB`, and that the
production endpoint-trivialization check merely asserted a known nonzero logarithm.

The production implementation now:

- declares the A-to-C affine overlap map independently from the two-step composite;
- differentiates both constructions and compares their Jacobians and induced metrics;
- rejects a deliberately corrupted direct-overlap Jacobian and metric;
- constructs an explicit second endpoint metric, recharts only that endpoint, and verifies the
  squared density-ratio factor and the half-log-determinant shift in `Delta kappa`.

The independent Fraction implementation now declares the direct A-to-C Jacobian literally rather
than computing it from the product, and includes the same corrupted-overlap rejection. Corrected
counts are 29/29 production and 25/25 independent. No premise, tolerance, conclusion, or physical
claim changed.
