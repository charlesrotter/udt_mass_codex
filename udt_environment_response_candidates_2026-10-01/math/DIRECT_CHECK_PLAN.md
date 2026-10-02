# ERC1 exposed candidate check plan

Source-first seals and results remain unchanged. This stage follows reading the
parent INITIAL_DERIVATION, NUMERICAL_PLAN, original check_candidates.py and frozen
output summaries. The parent disclosed its combined Ric+Q assertion weakness;
reviewer confirmed it before receiving notice of the bounded repair. No other
reviewer's result has been supplied. Model/independence limits are unchanged.

The core equations and first-variation interpretation agree with the sealed
independent derivation (the parent interchanges the names Phi and Psi, explicitly).
The exact flat-event expansion will be recomputed by repeatedly differentiating
the ODE as polynomial algebra, through fifth order. This check follows exposure
to the parent claimed cubic result and is not a blind discovery.

Independently recompute all eight already-saved finest-tolerance histories at
their 32/64/128 grids, without importing any parent code or launching another
survey. Use saved a(t) alone, an 11-point polynomial differentiator with weights
from exact Vandermonde inversion, through derivative order four. Construct
H=a'/a, R=6(a''/a+H^2), R' and R'' directly and evaluate E00-Lambda and
Eii/a^2+Lambda. Compare the separately saved H/R and constraint. This gives a
different reconstruction than the parent's nine-point differentiation of H;
both remain sampled floating diagnostics, not interval/PDE certification.
Acceptance for finest absolute tensor residual is 1e-7, declared before this
recomputation. Report all grid errors and roundoff growth rather than imposing
an unobserved asymptotic convergence rate.

Reconstruct null arrivals from a-only quintic interpolation, numerical quadrature
of 1/a and bracketed root solving, at the parent's L=1/4,1,2; compare arrival,
echo and infinitesimal proper-period ratios with saved parent query records at
1e-7 absolute tolerance. This method does not use the evolved eta or parent
dense solution. Independently report flat-event cubic errors at L=1/8,1/16,1/32.
They are diagnostic small-distance remainders, not finite pulse-period ratios.

Check parent freeze hashes, mapping the original checker to its preserved
check_candidates_initial.py if the authorized repair is already in place.
Record files actually checked. Use existing TPS1 capture, CPU only, 2 GiB virtual
memory, one BLAS thread, no elapsed/CPU cutoff and manual interruption; stop on
nonfinite data, unreadable shapes or a failed fixed gate. Preserve failures.
