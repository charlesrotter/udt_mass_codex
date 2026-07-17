# Dispatch — independent verification of the UDT finite-cell boundary derivation

## Purpose

Independently determine whether current UDT premises force a finite-cell action and boundary mass
generator. This is an analytic audit. Do not run GPU numerics and do not choose an action because it
reproduces a desired mass formula.

## Hygiene and isolation

- Branch: grok.
- Read LIVE.md first; its CURRENT STATE wins.
- Remain pure to UDT. Standard geometric formalisms may be comparison/readout only.
- DATA-BLIND.
- Treat positional dilation as FOUNDING.
- Treat the \(S^2\) carrier as a historical WORKING POSIT now REOPENED, not as a permanently fixed
  founding truth. See UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md after the cold derivation
  is locked; do not use the existing carrier to select the geometric result.
- Treat existence/unattainability of one \(X_{\max}\) as a WORKING POSIT, while its independence,
  origin, and value remain OPEN. Do not import \(X_{\max}=2GM/c^2\) or any coefficient. See
  UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md after the cold derivation is locked.
- Do not read these until the independent derivation is locked:
  - UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md
  - verify_udt_finite_cell_boundary.py
  - verify_udt_finite_cell_boundary_out.txt
- The frozen, result-blind protocol is UDT_FINITE_CELL_BOUNDARY_MAP.md.

## Cold source packet

Read only:

1. CANON.md, especially C-2026-06-10-2, C-2026-06-18-1, C-2026-07-04-1, and
   C-2026-07-09-1/1a;
2. UDT_ELEGANT_FRAME.md;
3. SIMPLE_METRIC_MACRO.md;
4. simple_metric_L_wall_regularity_closure_results.md;
5. node05_seal_parity_regrade_results.md;
6. universe_cell_fold_jc_sigma_results.md;
7. native_geometric_action_results.md;
8. r1_route_fork_native_derivation.md;
9. d2c_gp_composite_conditions.md;
10. F2_matter_action_forcedness_results.md;
11. w_alg_verifier_scripts/UDT_H3_STATIC_MASS_BACKREACTION_DISPATCH.md;
12. hopfion_static_mass_results.md;
13. UDT_FINITE_CELL_BOUNDARY_MAP.md.

## Required derivation

### A. Boundary identity

Determine whether these are the same physical surface:

\[
\text{odd fold: }\phi=0,
\qquad
\text{WR-L wall: }A=1-r/X\to0,
\qquad A=e^{-2\phi}.
\]

Include causal-character and variation-class stamps. Keep the H3 numerical box separate.

### B. Off-shell quotient test

For

\[
L_P=\frac{Z}{2}\rho^2\phi'^2+2-2e^{-2\phi}\rho'^2+2\mu\rho\rho'\phi',
\]

\[
L_G=\frac{Z}{2}\rho^2\phi'^2+2-2\rho'^2+2\mu\rho\rho'\phi',
\]

apply the static depth mirror

\[
(\phi,\phi',\rho,\rho')\mapsto(-\phi,+\phi',\rho,-\rho').
\]

Compute \(I^*L-L\). Decide whether the defect vanishes or is a permissible local total derivative
on a neighborhood—not merely at the fixed surface. State exactly which \((G/P,Z,\mu)\) members
descend if the fold is an exact quotient.

### C. Variation-class separation

Derive independently:

1. the one-copy boundary term \(p_\phi\delta\phi+p_\rho\delta\rho+\delta B\);
2. its consequences for odd \(\phi\), even \(\rho\), \(\rho'=0\), and free \(\phi'\);
3. the matched-mirror momentum jumps.

Adjudicate whether the matched jump cancellation proves the one-copy or exact-quotient result.

### D. Endpoint and charge ambiguity

Derive moving-endpoint transversality with general \(B(q,b)\). Audit the transformations

\[
L\mapsto L+\frac{d}{dr}(\alpha\phi),
\qquad
L\mapsto L+\frac{d}{dr}(\gamma r).
\]

Track bulk equations, momenta, Hamiltonian, allowed boundary variations, and any proposed charge.
State what additional rule is needed to distinguish a physical boundary generator from an
improvement.

### E. WR-L compatibility

Insert

\[
\phi=-\frac{1}{2}\ln(1-r/X)
\]

into the live shift-clean radial action. Compute:

- \((r^2\phi')'\);
- near-wall action density;
- near-wall conjugate momentum;
- whether the action integral is finite.

Optionally test the narrow pure-kinetic inverse problem
\[
L=\frac{Z}{2}r^2W(\phi)\phi'^2
\]
without proposing the resulting \(W\) as UDT physics.

### F. Mass statement

Separate:

- the conjugate \(\phi\)-flux of the historical native-action family;
- the conditional H3 lapse flux
  \[
  \frac{2}{\kappa_g}\oint D_iN\,dS^i=2\int N\rho_4\,dV;
  \]
- the claim that either is native UDT mass.

Do not merge them without an explicit derived bridge.

## Adversarial attacks

Aim hardest at:

1. whether a finite depth shift could identify the odd fold and WR-L wall;
2. whether fixed-surface invariance is enough for a quotient action;
3. whether a derivative-dependent primitive defeats the quotient obstruction without adding
   boundary degrees of freedom or higher boundary data;
4. whether the one-copy and two-side variational problems are secretly equivalent;
5. whether a total-derivative improvement is physically inert once endpoints move;
6. whether the WR-L divergence is canceled by any already-recorded term;
7. whether the claimed smallest missing postulate is actually smaller or already present.

## Required output

Return:

1. a premise ledger;
2. all decisive equations;
3. verdicts for exact quotient, one-copy boundary, matched interface, horizon, and numerical box;
4. FORCED, ALLOWED-FAMILY, UNDERDETERMINED, or INCONSISTENT-SCOPE for the action and charge;
5. any refutation or correction;
6. a machine-readable JSON summary;
7. exact scripts and raw output for every symbolic check.

Do not edit LIVE.md or CANON.md, and do not bank a conclusion. Stop after the evidence package.
