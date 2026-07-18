#!/usr/bin/env python3
"""Finite algebra for the Stage-II carrier-covariance source audit.

This checks only the encoded chain rule for a generic position-weighted
static completion in a reciprocal representative.  It does not choose the
weights, measure, time sector, field representation, variation domain, or a
physical source convention.
"""

import sympy as sp


phi = sp.symbols("phi", real=True)
x2_parallel, x2_transverse = sp.symbols("x2_parallel x2_transverse")
x4_parallel, x4_transverse = sp.symbols("x4_parallel x4_transverse")
w2p = sp.Function("w2p")(phi)
w2t = sp.Function("w2t")(phi)
w4p = sp.Function("w4p")(phi)
w4t = sp.Function("w4t")(phi)

# The reciprocal lapse/longitudinal determinant cancels in the suppressed
# product measure.  Contractions carrying one longitudinal inverse metric
# receive exp(-2 phi); purely transverse contractions do not.
rho_completion = (
    sp.exp(-2 * phi) * (w2p * x2_parallel + w4p * x4_parallel)
    + w2t * x2_transverse
    + w4t * x4_transverse
)

derived = sp.expand(sp.diff(rho_completion, phi))
expected = (
    sp.exp(-2 * phi)
    * (
        (sp.diff(w2p, phi) - 2 * w2p) * x2_parallel
        + (sp.diff(w4p, phi) - 2 * w4p) * x4_parallel
    )
    + sp.diff(w2t, phi) * x2_transverse
    + sp.diff(w4t, phi) * x4_transverse
)
assert sp.simplify(derived - expected) == 0
print("PASS generic position-weight chain rule")

# Constant weights are one choice, not a covariance theorem.  In that choice
# the reciprocal constrained variation selects only longitudinal channels.
constant_weights = {
    w2p: 1,
    w2t: 1,
    w4p: 1,
    w4t: 1,
    sp.diff(w2p, phi): 0,
    sp.diff(w2t, phi): 0,
    sp.diff(w4p, phi): 0,
    sp.diff(w4t, phi): 0,
}
constant_source = sp.simplify(expected.subs(constant_weights).subs(phi, 0))
assert sp.simplify(constant_source + 2 * (x2_parallel + x4_parallel)) == 0
print("PASS constant-weight constrained variation is directional")

# Explicit admissible weight parameters change all four source coefficients.
a2p, a2t, a4p, a4t = sp.symbols("a2p a2t a4p a4t")
weighted = rho_completion.subs(
    {
        w2p: sp.exp(a2p * phi),
        w2t: sp.exp(a2t * phi),
        w4p: sp.exp(a4p * phi),
        w4t: sp.exp(a4t * phi),
    }
)
weighted_source_at_zero = sp.expand(sp.diff(weighted, phi).subs(phi, 0))
expected_weighted = (
    (a2p - 2) * x2_parallel
    + a2t * x2_transverse
    + (a4p - 2) * x4_parallel
    + a4t * x4_transverse
)
assert sp.simplify(weighted_source_at_zero - expected_weighted) == 0
print("PASS chosen weights change the source coefficients")
print("LIMIT: algebra does not select weights or certify a physical source law")
