# Development notes

The final derivation and verifier pass.

One implementation-level false failure occurred while writing the symbolic scale-rank check. SymPy
represented `X*(1-alpha*gamma)` as the algebraically equal `-X*(alpha*gamma-1)`. The check was
corrected to simplify their difference to zero. No equation, coefficient, premise, branch, or
expected physical outcome changed.

The candidate census initially named `bootstrap_variation_selector_2026-07-18/AUDIT_REPORT.md`,
while the tracked report is `DERIVATION_REPORT.md`. The preregistered source family was preserved and
the exact tracked path corrected before the census ran successfully.

No tolerance, fitted parameter, new physical boundary condition, or post-outcome source was added.

