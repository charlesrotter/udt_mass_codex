# External Adversarial Review: G327

## Findings

1. **Evidence defect: the four-command replay does not reproduce on this host under the sealed review constraints.** The scope forbids installs and repository/package access ([REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:2), [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:9), [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:11)), while the registered replay requires `python3` plus SymPy ([REPLAY_COMMANDS.txt](/intake/REPLAY_COMMANDS.txt:1), [RUN_RECORD.md](/intake/RUN_RECORD.md:16)). I authenticated the intake and then ran the four registered commands literally from a writable copy under `/work/g327_external_review.cB4Ke4`. Commands 1-3 each failed immediately with `ModuleNotFoundError: No module named 'sympy'`. Command 4 failed because it reruns command 1 internally. This is an evidence-only reproducibility failure, not a mathematical refutation, but it blocks external replay exactly as requested.

2. **Evidence defect: preregistration ancestry is asserted, not authenticated, inside the sealed intake.** The package verifier treats preregistration ancestry as the presence of the string `9bec301b` in the audit report ([verify_package.py](/intake/verify_package.py:126), [verify_package.py](/intake/verify_package.py:131)). I found no sealed prereg artifact, detached prereg hash, or append-only registry proof inside `/intake` that would let an external reviewer validate that ancestry without forbidden repository access. The intake therefore preserves the claim of preregistration, but not an independently auditable proof of that claim.

3. **Evidence defect: the banked aggregate verifier does not itself replay the fourth registered command from a fresh copy.** It checks that line 4 is textually present ([verify_package.py](/intake/verify_package.py:138), [verify_package.py](/intake/verify_package.py:149)) and it replays only the first three registered commands in a temporary copy ([verify_package.py](/intake/verify_package.py:151), [verify_package.py](/intake/verify_package.py:167)). That is weaker than the external instruction to run all four lines literally. I did run line 4 literally; it failed here because SymPy is unavailable.

## Authentication and Boundary

I verified the detached seal against the manifest and every listed payload. `python3 -S /intake/verify_review_intake.py` passed and reported `payload_count: 34`, `read_only_payloads: true`, and the manifest SHA256 `cbd12db48f2663f49dad86d1204fa7cc1267e999557aeef689cb8133728cb1bc`. A direct permission scan found no writable files under `/intake`.

Within the sealed intake, source provenance is internally coherent: upstream dependency files are enumerated in [SOURCE_SCOPE.tsv](/intake/SOURCE_SCOPE.tsv:1) and included under `sources/`, and those payloads are themselves covered by the review manifest. What is not independently sealed is the claimed upstream repository ancestry of the preregistration marker.

## Scientific Assessment

I did **not** find a bounded mathematical refutation of the declared primitive axial transverse-tracefree sector.

The background metric is the LRS Kasner form with exponents `(-1/3, 2/3, 2/3)` ([EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:22), [sources/udt_g324_g323_taub_quotient_mghd_identification_2026-09-02/EXACT_DERIVATION.md](/intake/sources/udt_g324_g323_taub_quotient_mghd_identification_2026-09-02/EXACT_DERIVATION.md:45)), and the cited source explicitly records `Ric=0` ([sources/udt_g324_g323_taub_quotient_mghd_identification_2026-09-02/EXACT_DERIVATION.md](/intake/sources/udt_g324_g323_taub_quotient_mghd_identification_2026-09-02/EXACT_DERIVATION.md:50)). That matters because both derivation scripts linearize `R_ab-(R/4)g_ab` as `delta R_ab-(delta R/4)g_ab` ([derive_axial_tensor_modes.py](/intake/derive_axial_tensor_modes.py:86), [derive_axial_tensor_modes.py](/intake/derive_axial_tensor_modes.py:94), [verify_independent.py](/intake/verify_independent.py:79), [verify_independent.py](/intake/verify_independent.py:88)); the omitted `-(R/4) delta g_ab` term is harmless only because the background scalar vanishes.

The gauge claim survives adversarial inspection inside the declared sector. For a legal periodic same-mode infinitesimal diffeomorphism, the `yz` block of `L_xi g_0` receives only the time-shift trace term and no transverse-tracefree part ([EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:55), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:72)). A vector field with linear `y` or `z` dependence could fake a tensor shear locally, but it would violate the fixed compact quotient periodicity and is therefore not a legal gauge vector in the declared problem.

The closure and ODE also check out. In LRS Bianchi I form, the tensor mode with wave covector along `X` has friction `H_X+H_y+H_z=(-1/3+2/3+2/3)/T=1/T` and gradient term `k_1^2/a_X^2 = (k_1^2/C_1^2) T^{2/3} = nu^2 T^{2/3}`, matching the claimed operator. That agrees with both sealed derivations that all off-sector and constraint components vanish and only the `yy-zz` and `yz` tensor equations remain ([EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:82), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:115), [derive_axial_tensor_modes.py](/intake/derive_axial_tensor_modes.py:109), [derive_axial_tensor_modes.py](/intake/derive_axial_tensor_modes.py:122), [verify_independent.py](/intake/verify_independent.py:107), [verify_independent.py](/intake/verify_independent.py:120)).

The Bessel reduction is correct. With `z=(3/4) nu T^(4/3)`, one has `z' = nu T^(1/3)` and `(z''+z'/T)/(z')^2 = 1/z`, so the mode equation becomes `h_zz + z^{-1} h_z + h = 0`, i.e. the order-zero Bessel equation. The basis `J_0(z), Y_0(z)` and transformed Wronskian `T W_T = 8/(3 pi)` are therefore correct ([EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:123), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:153), [derive_axial_tensor_modes.py](/intake/derive_axial_tensor_modes.py:208), [derive_axial_tensor_modes.py](/intake/derive_axial_tensor_modes.py:235)).

I found no defect in the dimension count, curvature witness, or endpoint/norm claims within the declared scope. Two polarizations times cosine/sine phases times two time solutions gives eight real constants ([EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:155), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:171)). The on-shell transverse tidal witness is not the zero operator ([EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:173), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:189)). Near `T -> 0+`, `J_0` is finite and `Y_0` is logarithmic; for `T -> infinity`, both the amplitude and the normalized derivative term in the declared norm decay like `z^{-1/2} ~ T^(-2/3)` ([EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:191), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:220)). I also saw no improper promotion to the full Fourier spectrum, stability theorems, occupancy, scale, matter/mass, observation, or `X_max`; the intake repeatedly keeps those open ([COMPLETENESS_MAP.md](/intake/COMPLETENESS_MAP.md:5), [COMPLETENESS_MAP.md](/intake/COMPLETENESS_MAP.md:11), [AUDIT_REPORT.md](/intake/AUDIT_REPORT.md:41), [PREMISE_LEDGER.tsv](/intake/PREMISE_LEDGER.tsv:10)).

## Required Repairs

Scientific:
- None required for the bounded primitive axial tensor census itself. I found no sign error, missing in-sector degree of freedom, false Bessel identity, or hidden promotion within the stated scope.

Evidence-only:
- Vendor the exact replay runtime or provide a dependency-free external verifier so the four literal commands can be rerun under the sealed no-install review constraints.
- Seal the preregistration ancestry with an intake-local artifact or detached registry proof instead of a bare commit string mention.
- Strengthen `verify_package.py` so a fresh copied package also executes the fourth registered command, not just the first three.

REFINE__G327_BOUNDED_LANDING
