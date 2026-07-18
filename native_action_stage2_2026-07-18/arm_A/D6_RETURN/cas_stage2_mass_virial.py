#!/usr/bin/env python3
"""Finite algebra for the Stage-II three-part mass/virial accounting.

This verifies bookkeeping after the EH mass premise and finite-domain virial
balance are supplied.  It cannot establish either premise, the boundary
surface theorem, numerical convergence, or the controlled infinite-volume
limit.
"""

import sympy as sp


E2, E4, B_boundary, W_res = sp.symbols(
    "E2 E4 B_boundary W_res", real=True
)
E_carrier = E2 + E4
M0 = 2 * E4

virial_substitution = {E4 - E2: B_boundary + W_res}
accounting_defect = sp.expand(M0 - (E_carrier + B_boundary + W_res))
assert sp.simplify(accounting_defect.subs(E4, E2 + B_boundary + W_res)) == 0
print("PASS finite-domain identity: M0 = E_carrier + B_boundary + W_res")

# At an exact critical point only the residual is removed; the boundary term
# remains unless a separate boundary theorem or limit removes it.
critical_defect = sp.simplify((M0 - E_carrier).subs(E4, E2 + B_boundary))
assert sp.simplify(critical_defect - B_boundary) == 0
print("PASS exact critical point leaves the boundary contribution")

# In a separately premised controlled limit with both terms zero, the usual
# whole-space mass/energy equality follows algebraically.
closed_limit = sp.simplify(
    (M0 - E_carrier).subs(E4, E2 + B_boundary + W_res).subs(
        {B_boundary: 0, W_res: 0}
    )
)
assert closed_limit == 0
print("PASS separately premised zero-boundary/zero-residual closure")
print("LIMIT: algebra does not prove EH sourcing, a surface theorem, or a limit")
