# Exposed saved-artifact recomputation freeze

Reviewer's parent-code/results exposure is now declared. This check imports no
parent module and does not run its root solver. It reuses the saved three central
70-digit incidences as data, then integrates the original r-coordinate ray and
receiver integrals, rather than the parent's inverse-radius quadrature. It also
contracts the original outgoing metric components, independently reconstructs
Z and the limiting product, and checks the saved finite-step errors for reported
threshold/convergence compliance. It does not independently reconstruct the
unsaved satellite incidence states or certify their derivative errors.

Six finite recomputations: three saved (E,R) cases at 50 and 90 decimal digits,
the same two precisions as the reviewer's initial controls. The source values are
free-and-explored parent examples; no new physical choices or fits. Original
incidence residual and relative Z/product errors must be below 1e-40 at 50
digits and 1e-62 at 90 digits. Quadrature partitions are [a,2a,10a,R] after removing
duplicates and [R,2R,10R,infinity] for the tail. No numeric repair or tolerance
change is authorized by this freeze; failures are retained first.

Python/mpmath only, one process, CPU, 2 GiB address limit, one BLAS thread,
no wall/CPU timeout, grid or GPU. Total reviewer finite cases after this check
will be 43 including the earlier 37, within the 100-case ceiling. Outputs,
commands, input hashes, stdout and stderr are preserved in review_fidelity.
