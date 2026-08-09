# Preserved first derivation failure

The first post-preregistration implementation successfully wrote the complete 256/512-point
numerical matrix and block tables, then failed to reach the certification/result stage. It asked
SymPy to rediscover the same low-order associated-Legendre polynomial integrals separately for
every matrix pair. The process remained in those exact integrations and was interrupted after the
redundancy was identified.

This was a computational-method failure, not a failed scientific gate. No matrix outcome was used
to alter the registered `B` grid, basis, tolerance, selection rule, or maximum conclusion.

The repair replaces repeated integration with the exact normalized associated-Legendre recurrences

```text
x p_l = a_l p_(l+1)+a_(l-1)p_(l-1),
(1-x^2)p'_l = (l+1)a_(l-1)p_(l-1)-l a_l p_(l+1),
```

so the first derivative matrices follow by finite exact matrix products. The preregistered
first-order `Delta ell=0,2` falsification gate is unchanged.

The first completed repaired run then exposed two marginal numerical failures in the original
double-precision Gauss-Legendre implementation: the largest round-limit error was
`2.5011104298755527e-11` and the largest 256/512 disagreement was
`2.1998403099132702e-11`, both above the preregistered `2e-11` gate. The gate was not widened.
The numerical repair refines the same registered Gauss-Legendre nodes by long-double Newton steps,
recomputes their weights from the Legendre derivative, and evaluates the associated-Legendre basis
by its exact three-term recurrence with long-double accumulation. The quadrature orders and all
scientific inputs remain unchanged.
