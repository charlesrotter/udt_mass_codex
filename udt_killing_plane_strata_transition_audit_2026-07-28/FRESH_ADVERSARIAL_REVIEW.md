`PASS_WITH_REQUIRED_CORRECTIONS`

The central Gram-response and transition results survive, but the preregistered certification is incomplete.

Required corrections:

1. The “full twist” claim must include all four components. With \(u=e^{-2\phi}\), \(A=c_E+\alpha\Omega\),

\[
a_\Omega=-c_EAu,\qquad
b_\Omega=\Omega/u-\alpha Au,
\]

and \(d\phi=p\sigma_1+q\sigma_2\),

\[
\begin{aligned}
W_\Omega^\flat\wedge dW_\Omega^\flat
={}&4c_E\Omega A p\,dt\wedge\sigma_3\wedge\sigma_1\\
&+4c_E\Omega A q\,dt\wedge\sigma_3\wedge\sigma_2\\
&+\kappa a_\Omega b_\Omega\,dt\wedge\sigma_1\wedge\sigma_2\\
&+\kappa b_\Omega^2\,\sigma_3\wedge\sigma_1\wedge\sigma_2 .
\end{aligned}
\]

The implementation checks only the first two components ([derive_killing_plane_transition.py](/home/udt-admin/udt_mass_codex/udt_killing_plane_strata_transition_audit_2026-07-28/derive_killing_plane_transition.py:116)). Therefore the report must say that \(K\) is the unique timelike line with no depth-mixed twist component—not that its full twist vanishes. Generally both \(K\) and the ruler retain contact-twist components.

2. Add the missing constant-depth, \(\kappa=0\) control. When \(d\phi=0=\kappa\), every constant Killing direction is twist-free and \(D_X=0\); neither certificate selects a founded clock. Existing S07 covers only nonconstant depth ([SELECTOR_STRATA.tsv](/home/udt-admin/udt_mass_codex/udt_killing_plane_strata_transition_audit_2026-07-28/SELECTOR_STRATA.tsv:8)).

3. Explicitly classify lattice-preserving automorphisms. For the primitive compact generator,

\[
K\mapsto rK+bV,\qquad V\mapsto\epsilon V,
\quad r\neq0,\ b\in\mathbb R,\ \epsilon=\pm1.
\]

This confirms that topology fixes the compact line \(V\), but not one noncompact helix. Generic \(GL(2,\mathbb R)\) covariance is algebraically stronger but does not replace the preregistered global lattice classification.

4. Scope the intrinsic claim to the registered \((K,V)\) plane. Higher-isometry metrics may contain additional Killing planes or compact circles; selection of the tested plane is explicitly open in [PREMISE_LEDGER.tsv](/home/udt-admin/udt_mass_codex/udt_killing_plane_strata_transition_audit_2026-07-28/PREMISE_LEDGER.tsv:9). Either exclude such metrics by requiring the full Killing algebra to be exactly two-dimensional, or classify them separately.

5. Downgrade the independent-verification claim until the missing checks are implemented. The verifier:

- reads the old nonzero endpoints but does not independently reconstruct the analytic transition;
- validates T03 by comparing a stored conclusion string ([verify_killing_plane_transition_independent.py](/home/udt-admin/udt_mass_codex/udt_killing_plane_strata_transition_audit_2026-07-28/verify_killing_plane_transition_independent.py:239));
- does not check the two contact-twist components or lattice automorphisms;
- hardcodes frozen/tests/navigation as true ([verify_killing_plane_transition_independent.py](/home/udt-admin/udt_mass_codex/udt_killing_plane_strata_transition_audit_2026-07-28/verify_killing_plane_transition_independent.py:218)).

Those mutation gates are semantic ledger guards, not independent mathematical or repository verification. F20 must be marked pending or replaced by actual commands.

Strongest surviving bounded conclusion:

Within the stationary, constant-\(\alpha\), block-screen \( \mathbb R\times S^3 \) family, conditional on the registered descended Killing plane, a nonconstant Gram map defines

\[
D_X=G^{-1}X(G)
=
\begin{pmatrix}
-2X\phi & -4\alpha X\phi/c_E\\
0 & 2X\phi
\end{pmatrix},
\]

whose unique timelike and spacelike eigenlines are respectively

\[
K,\qquad V-\frac{\alpha}{c_E}K.
\]

Their norms are \(-c_E^2e^{-2\phi}\) and \(e^{2\phi}\), and the lines extend globally across critical points from any regular point on a connected base. The analytic positive-metric path establishes continuous adjacency to the old rank-three configurations and selection of the same \(K\), but not simultaneous full descent and rank-three certification.

No macro/micro assignment, mass emergence, carrier, action, source, density law, dynamics, or physical branch is derived. No repository files were edited.