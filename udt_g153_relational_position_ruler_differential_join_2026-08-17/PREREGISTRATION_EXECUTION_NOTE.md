# G153 preregistration execution note

Date: 2026-08-17

The preregistered task required the full first differential while leaving the `X_max` realization
open. The first implementation wrote only the constant-`X_max` subcase. A self-audit identified the
omitted product-rule term before adversarial review or banking.

The production derivation, independent witness, exact report, premise ledger, and lay report were
therefore corrected to use

\[
d\rho=\tanh\phi\,dX_{\max}
+X_{\max}\operatorname{sech}^2\phi\,d\phi.
\]

The constant-`X_max` expression is retained only as a labelled conditional subcase. This repair does
not alter the preregistered question or maximum conclusion; it enforces its declared no-shortcut
scope.
