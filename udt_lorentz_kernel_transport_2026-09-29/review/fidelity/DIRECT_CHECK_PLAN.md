# Independent direct-stage check plan

Exposure: source-first seal and correction already preserved; INITIAL_CANDIDATE.md
(sha256 600c261ec1662d8a8315034ef362f78563e7c8a193a2ca8fecad2d119ea46d52)
and CANDIDATE_FREEZE.json now read. No author check code/output or other reviewer
assessment read. Parent reports30 exact checks; not treated as evidence here.

Independently compute Levi-Civita Christoffels from the full general metric
h=[[-T^2,-T^2 b],[-T^2 b,L^2-T^2 b^2]] with symbolic smooth positive T,L and b.
Transform the coordinate connection using dual-frame matrix from the coframe
inverse; compare both independent components with equation(5). Independently
compute coordinate Ricci scalar from Christoffel derivatives/products and compare
with equation(9), retaining T,L,b dependence and derivatives. Verify null
frequency derivative directly using coordinate geodesic transport and proper
clock covector, without entering the claimed frame transport equation. Test a
nonconstant nonzero-shift/nonconstant-T/nonconstant-L analytic example and the
flat Milne timing control; compare reciprocal sector curvature and basis change.

This is source-preserving symbolic verification inside the authorized restricted
Lorentz2 domain. Positivity is a domain hypothesis, not checked by unconstrained
symbol cancellation. No claim of native selection. CPU one thread,60s/512MiB
via existing capture runner. Preserve any failure, no overwrites. Check count
will be reported from actual stdout. Analytic inference and scope review remain
separate from finite examples and symbolic regressions. No author implementation
imports; Python/SymPy only. No full-source or full406 audit by this reviewer.
