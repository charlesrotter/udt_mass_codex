PASS_WITH_REQUIRED_CORRECTIONS

The bounded mathematics survives, but the independent-verification claims need tightening.

Required corrections:

1. Replace the verifier’s hardcoded zero dictionary at [verify_killing_plane_transition_independent.py](/home/udt-admin/udt_mass_codex/udt_killing_plane_strata_transition_audit_2026-07-28/verify_killing_plane_transition_independent.py:188) with an actual evaluation of its independently reconstructed twist at \(p=q=\kappa=0\), and verify \(D_X=0\) at \(\chi=0\). Regenerate the stored results and hashes.

2. The verifier currently assumes the lattice-preserving matrix form and samples it at [verify_killing_plane_transition_independent.py](/home/udt-admin/udt_mass_codex/udt_killing_plane_strata_transition_audit_2026-07-28/verify_killing_plane_transition_independent.py:207); it does not derive its necessity. Either add the universal-cover/lattice argument or downgrade [AUDIT_REPORT.md](/home/udt-admin/udt_mass_codex/udt_killing_plane_strata_transition_audit_2026-07-28/AUDIT_REPORT.md:81) from “reconstructs the lattice subgroup” to “checks representatives of the derived subgroup.” Likewise, its convex-path check is sampled regression evidence, while universal positivity rests on the analytic SPD-convexity argument.

3. [README.md](/home/udt-admin/udt_mass_codex/udt_killing_plane_strata_transition_audit_2026-07-28/README.md:15) names a nonexistent `FRESH_ADVERSARIAL_REVIEW_CORRECTED.md`; save this review there when banking or correct the navigation.

Evidence:

- Independent symbolic reconstruction gives
  \[
  D_X=
  \begin{pmatrix}
  -2\chi&-4\alpha\chi/c_E\\
  0&2\chi
  \end{pmatrix},
  \]
  with timelike eigenline \(K\), spacelike eigenline \(V-\alpha K/c_E\), norms \(-c_E^2e^{-2\phi}\) and \(e^{2\phi}\), and \(\det G=-c_E^2\).

- With \(A=c_E+\alpha\Omega\),
  \[
  a=-c_EAe^{-2\phi},\qquad
  b=\Omega e^{2\phi}-\alpha Ae^{-2\phi},
  \]
  all four twist components reproduce [EXACT_DERIVATION.md](/home/udt-admin/udt_mass_codex/udt_killing_plane_strata_transition_audit_2026-07-28/EXACT_DERIVATION.md:115):
  \[
  \begin{aligned}
  W^\flat\wedge dW^\flat={}&
  4c_E\Omega A p\,dt\wedge\sigma_3\wedge\sigma_1+
  4c_E\Omega A q\,dt\wedge\sigma_3\wedge\sigma_2\\
  &+\kappa ab\,dt\wedge\sigma_1\wedge\sigma_2+
  \kappa b^2\,\sigma_3\wedge\sigma_1\wedge\sigma_2 .
  \end{aligned}
  \]
  Thus \(K\) is only the unique timelike line without depth-mixed twist; generic contact twist remains.

- At \(d\phi=0=\kappa\), all four twist components and \(D_X\) vanish, leaving the founded clock unselected.

- Lifting an automorphism of \(\mathbb R\times S^1\) to \(\mathbb R^2\) and preserving its primitive kernel forces
  \[
  K\mapsto rK+bV,\qquad V\mapsto\epsilon V,
  \quad r\ne0,\ b\in\mathbb R,\ \epsilon=\pm1.
  \]
  Topology therefore fixes only the unoriented compact line.

- The analytic positive-metric path establishes nonzero rank-three points arbitrarily close to the descended endpoint, with both certificates selecting \(K\) at their respective strata. It does not establish simultaneous certification or a neighborhood theorem over every deformation direction. Along the particular analytic path, the identity theorem actually gives the stronger isolated-zero conclusion.

- Higher-isometry metrics and all macro/micro, action, carrier, source, density, dynamics, mass, and physical-branch claims remain explicitly open.

Evidence gates: preregistered at `0d6d83b`; scope appropriately bounded; mathematics independently reproduced, with the verifier caveats above; premises audited and the current premise verifier succeeded. The live verifier rerun reached its executed test command but could not run pytest because the read-only sandbox provides no writable temporary directory. No files were edited.