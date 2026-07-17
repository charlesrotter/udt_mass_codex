# COLD DISPATCH — independently verify mutual-dilation resistance and carrier-emergence result

**Mode:** adversarial analytic verification, DATA-BLIND  
**Goal:** reproduce or refute the load-bearing claims with your own algebra and your own CAS.
Do not treat the supplied candidate as a desired answer.

## 0. Disclosure protocol

### Stage I — cold

Receive only:

1. this dispatch;
2. UDT_MUTUAL_DILATION_RESISTANCE_MAP.md;
3. CANON.md entries C-2026-06-18-1 and C-2026-07-09-1/1a;
4. simple_metric_hyperbolic_derive.md;
5. UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md;
6. UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md.

Do **not** receive the derivation-results report, verifier script/output, LIVE/HANDOFF, prior native
action conclusions, or the project owner’s preferred interpretation. Freeze and SHA-256 your full
Stage-I report and CAS before Stage II.

### Stage II — challenge

After Stage I is frozen, receive:

- UDT_MUTUAL_DILATION_RESISTANCE_DERIVATION_RESULTS.md;
- verify_udt_mutual_dilation_resistance.py;
- verify_udt_mutual_dilation_resistance_out.txt;
- UDT_NATIVE_ACTION_NONCOLD_DERIVATION_RESULTS.md;
- UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md;
- matter_carrier_provenance_audit_results.md.

Write a separate addendum. Do not overwrite the cold result. Name every revision and the exact
new information or error that caused it.

## 1. Binding physics rules

- Remain pure to UDT: the metric and stated positional-dilation structure are the theory.
- Do not import GR field equations, EH dynamics, ΛCDM, Standard Model physics, quantum mechanics,
  QED, fluids, Q-balls, boson stars, or textbook soliton mechanisms as derivations.
- Standard theories may be comparisons only.
- No fitted parameters, fudge factors, cutoffs, kernels, effective corrections, or invented
  couplings.
- Establish exact nonlinear algebra before controlled expansion.
- Distinguish FOUNDING, DERIVED, CHOSE, WORKING, OPEN, CONDITIONAL, POSIT, and OBSERVED.
- A passing CAS validates encoded algebra, not completeness, premise legitimacy, or physics.

## 2. Frozen inputs

\[
D_{AB}=e^{\Delta\phi_{AB}},\qquad D_{BA}=D_{AB}^{-1}.
\]

The working unattainable-distance branch has

\[
0\le u_{AB}=d_{AB}/X<1.
\]

The conditional hyperbolic-composition branch additionally has

\[
u_{AB}=\tanh|\Delta\phi_{AB}|.
\]

The candidate to test—not presume—is

\[
\Gamma_{AB}=\frac12(D_{AB}+D_{BA}),\qquad
\mathcal R=\Gamma-1.
\]

The \(S^2\) carrier is reopened. The live macro result remains WR-L:

\[
A=1-r/X.
\]

## 3. Required independent tasks

### A. Kinematic forcedness

1. Derive \(\Gamma\) from the reciprocal factors.
2. On the conditional hyperbolic branch, express it in \(u=d/X\).
3. Compute endpoint behavior and first two derivatives.
4. Determine whether reciprocity, regularity, positivity, and divergence uniquely select
   \(\mathcal R\). Supply at least one explicit counterfunction if not.
5. Keep separate the statements “invariant/readout,” “energy,” “inertia,” “mass multiplier,” and
   “source.”

### B. Exact graph variation

For a connected finite graph with symmetric positive weights, independently vary

\[
E_\phi=\sigma\sum_{a<b}w_{ab}
\left[\cosh(\phi_a-\phi_b)-1\right].
\]

Report:

- the full gradient;
- the Hessian quadratic form;
- all exact zero directions;
- whether any nonconstant stationary point exists;
- which conclusions change under an overall negative sign.

Do not infer stability from positivity without proving the stationary-point statement.

### C. Whole-scale and vector-cancellation test

For fixed relational constituents and weights, set \(d_{ab}\mapsto\lambda d_{ab}\). Derive
\(dE/d\lambda\) and \(d^2E/d\lambda^2\) for both overall signs. Decide whether an interior
\(0<\lambda<1/u_{\max}\) extremum exists.

Then independently test the claim that an isotropic vector-force cancellation can coexist with a
nonzero scale derivative. Use the exact identity between the scale variation and
\(\sum_a\mathbf r_a\cdot\mathbf F_a\). Do not use an undefined infinity-minus-infinity argument.

### D. Continuum/locality audit

Start from the exact bilocal expression

\[
E=\frac{\sigma}{2}\int d\mu(p)d\mu(q)\,
W(p,q)\left[\cosh(\phi(p)-\phi(q))-1\right].
\]

Independently determine:

- which measure, kernel, pair domain, and normalization are additional premises;
- the controlled small-separation expansion for a smooth \(\phi\);
- the scaling of second- and fourth-order moments with kernel range \(\ell\);
- whether one zero-range normalization retains both a finite \(L_2\) term and the nonlinear
  \(u\to1\) barrier without subtraction or tuning;
- whether a local covariant ansatz in \(g^{\mu\nu}\nabla_\mu\phi\nabla_\nu\phi\) is actually derived
  from a distance bound.

State clearly whether nonlocality is falsified or merely remains an unchosen possibility.

### E. Carrier-emergence census

Test at least these routes without assuming the answer:

1. scalar target \(\phi\in\mathbb R\) or \(u\in(-1,1)\);
2. normalized gradient \(\mathbf n=\nabla\phi/|\nabla\phi|\);
3. bilocal separation directions;
4. hyperbolic-angular state
   \[
   U=(\cosh\phi,\sinh\phi\,\mathbf n).
   \]

For each, audit global smoothness, target topology, R1 common-shift behavior, bilocality, and whether
a nontrivial topological particle sector and action are forced. Explicitly check

\[
\mathbf n\cdot(\nabla\times\mathbf n)
\]

for the normalized-gradient route. Do not reject or canonize the historical \(S^2\) carrier merely
because the derivation does not force it.

### F. WR-L versus hyperbolic distance chart

Keep the live areal variable \(y=r/X\) separate from \(u=x/X=\tanh\phi\). Derive their relation
through \(A=e^{-2\phi}\) and determine whether setting \(x=r\) is valid. Express the reciprocal
\(\Gamma\) directly on WR-L and check its wall limit.

### G. Global closure count

Determine whether

\[
X=\beta GM_{\rm total}/c^2,\qquad
c^2=\beta GM_{\rm total}/X
\]

are one equation or two. Audit whether the candidate defines \(M_{\rm total}\), \(\beta\), or a
second independent equation when \(c\) and \(X\) are both global outputs.

## 4. Required outputs

1. A premise ledger and fork map written before the algebra.
2. A standalone derivation with every conclusion labeled.
3. A fresh runnable SymPy script; do not copy the supplied verifier in Stage II.
4. Raw stdout/stderr.
5. A claim table with verdicts:
   **CONFIRMED**, **REFUTED**, **CONDITIONAL**, **UNDERDETERMINED**, or **NOT TESTED**.
6. The strongest counterexample to every uniqueness claim.
7. Exact SHA-256 hashes, Python/SymPy versions, timestamp, and exposure declaration.

## 5. Banking gate

Nothing becomes banked or canon from agreement alone. A surviving result still requires:

- both CAS implementations passing;
- reconciliation of any algebraic discrepancy;
- explicit confirmation that no extra balance term or carrier was inserted after seeing a failure;
- project-owner verdict on the physics wording and scope.

