# G115 evidence gates

## Gate 1 — preregistered

Yes. `PREREGISTRATION.md` was committed and pushed at `5c3f19ba` before the confirmatory production,
independent verification, catch proofs, or verdict documents were created. The disclosed pilot
algebra is not counted as a preregistered discovery.

## Gate 2 — full or bounded

Bounded and justified: complete smooth central spherical metric two-jet, arbitrary time dependence,
one central outgoing radial-null observer query, and exact finite-dimensional source-boundary
classification. Higher radial order, nonspherical modes, finite-radius/global branches, dynamics,
and observations are excluded.

## Gate 3 — independently verified

The production route uses SymPy series, direct Christoffel contraction, pullback/Schur algebra, and
exact source-boundary ranks. The independent executable route uses numerical metric derivatives,
RK4 affine geodesics, a separately integrated null graph, coefficient recovery, and selected direct
subspace ranks. It independently checks the main terminal/frequency distinction, affine coefficient,
null pullback, and rank examples; it does not independently integrate the Jacobi system or rebuild
the Schur, areal, and QW formulas. Its caustic and rank controls are explicit finite matrices, and
the catch proofs reuse the saved numerical witness. A fresh zero-context adversarial reviewer
independently reconstructed the remaining algebra and returned `VERIFIED_WITH_CAVEATS`.

The preregistered direct Riemann reconstruction was not implemented; the optical coefficient is
checked through direct Christoffels/geodesic propagation and blind algebra instead. This unclosed
method gate is retained as a caveat rather than silently counted as passed.

## Gate 4 — premises audited

Yes for the bounded claim: `c_E`, residual gauge, regularity, metric jets, observer branch, active
versus passive celestial drift, source congruence, source types, phase boundary, and every excluded downstream interpretation are
listed in `TYPE_AND_PREMISE_LEDGER.tsv`. The repository-wide verifier passes all 102 premise rows;
the repository suite passes 90 tests with one documented xfail.
