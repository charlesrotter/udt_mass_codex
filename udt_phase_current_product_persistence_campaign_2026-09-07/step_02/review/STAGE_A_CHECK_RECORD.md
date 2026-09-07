# Stage A exact-check record

source_first.json records exit0,1.553606558 seconds,53344KiB maximum RSS,
512MiB address-space,60-second CPU/wall limits, Python3.10.12, SymPy1.13.1.
All18 grouped exact controls passed; stderr is empty. No failed run or repair.
The full stdout contains independently assembled metrics, arbitrary covectors,
Ricci tensors, wave-commutator residuals, curvature and differentiated-curvature
terms, the initial scalar, and24 source SHA256 values. No PC2 author code or
output is imported or read. The capture wrapper is shared process plumbing.

Direct coordinate differentiation checks all16 slots of (A1) for a variable
curvature Ricci-flat harmonic metric and a variable-Ricci off-equation product
metric. All contracted differential-Bianchi identities also vanish exactly.
Changing the curvature sign or its factor2, or dropping the nonzero
differentiated-curvature term in the off-equation control, gives a nonzero
exact residual. These are algebraically changed-formula counterchecks, not
separate executable-author mutation runs or a completeness claim.

For H=x^3-3xy^2+u(x^2-y^2), the independent full ambient scalar is
q_rec=9/(4u^2+24ux+36x^2+36y^2). The complete spacelike-data formula agrees
exactly; omitting its normal subtraction fails. At u=0,x=1,y=0,c=2, N=36,
H+2c=5 and q_rec=1/4. A homogeneous flat scalar defect A=t has A(0)=0 but
nonzero normal derivative and is nonzero later, exposing an initial-value-only
uniqueness argument. These examples supplement the analytic full-data proof.

Not run: parent-only full audit, startup suite, old source suites, PDE production,
global or compact realization, protected payloads, external research, different
model/human review. Those omissions do not become passed checks. The Stage A
argument's conditional general PDE hypothesis remains explicit.
