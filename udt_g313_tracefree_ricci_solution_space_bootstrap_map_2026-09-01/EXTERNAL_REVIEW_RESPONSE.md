G313_REPAIRABLE_DEFECTS__SCIENTIFIC_LANDING_RETAINED

Findings, ordered by severity:

- Medium: [derive_solution_space.py](/intake/package/derive_solution_space.py:177) claims to verify the G309 round-cosh branch equation, but the code only checks the hyperbolic identity `cosh^2-sinh^2=1`. It never evaluates the actual G309 residual `Q[a]=aa''-a'^2-1` derived in [EXACT_DERIVATION.md](/intake/sources/udt_g309_strengthened_chain_history_selection_audit_2026-08-31/EXACT_DERIVATION.md:136). This is a vacuous evidence check relative to the stated target.
- Medium: [verify_independent.py](/intake/package/verify_independent.py:40) independently checks product curvature invariants, but it does not independently verify the explicit positive product metric’s full claimed package properties: `Ric=Lambda g` from that Lorentzian metric and compact `S1 x S2` Cauchy topology, both asserted in [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:62). The independent product-witness replay is therefore incomplete.
- Low: The Local Metric Sufficiency versus global-bootstrap separation is only lightly executable. [derive_solution_space.py](/intake/package/derive_solution_space.py:198) reduces it to a toy topology distinction, and [verify_independent.py](/intake/package/verify_independent.py:114) reports the compatibility result without an independent derivation. The substantive argument is in prose in [ADOPTION_RECORD.md](/intake/sources/startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md:25) and [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:169).
- Low: [SOURCE_SCOPE.tsv](/intake/package/SOURCE_SCOPE.tsv:4) omits the cited `G307`/`G308` source reports even though [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:185) invokes `G305--G308` collectively. The current registry and `LIVE.md` summary still support the nonselection reading, but direct file-level audit of those two gates is unavailable inside this intake.

Scientific verdict after fresh read-only review:

The landing survives. Independently, the 4D contracted Bianchi completion is correct: from `S_ab=R_ab-(R/4)g_ab=0`, one gets `(1/4)∇_b R=0`, hence on each connected regular region `R=4Lambda` and `Ric_ab=Lambda g_ab` [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:14). The positive `dS2 x S2` product witness is a valid non-round Einstein witness with nonzero Weyl invariant and compact `S1 x S2` Cauchy slices [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:62). The Berger `(1,1,3/2)` data give Ricci eigenvalues `(-1/2,-1/2,9/2)` and satisfy the fixed-`Lambda=3` Hamiltonian constraint with `h^2=5/12`, but only G303-conditional local development follows [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:91), [AUDIT_REPORT.md](/intake/sources/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/AUDIT_REPORT.md:17). The Ricci-flat plane-wave and constant-homothety controls are also sound [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:130).

W5/W6/Hopf/relation premises do not reject the nonround witnesses; they characterize or condition the round branch without selecting it [AUDIT_REPORT.md](/intake/sources/udt_g304_global_cell_constant_sector_discriminator_2026-08-30/AUDIT_REPORT.md:28), [EXACT_DERIVATION.md](/intake/sources/udt_g309_strengthened_chain_history_selection_audit_2026-08-31/EXACT_DERIVATION.md:69), [LIVE.md](/intake/sources/LIVE.md:41). The adoption record’s type separation between a whole-history admissibility predicate and a forbidden hidden local-memory variable is coherent [ADOPTION_RECORD.md](/intake/sources/startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md:25).

Explicit answers:
- The round cosh branch is not unique.
- The scalar magnitude is not selected.
- No nonidentity bootstrap/admissibility predicate is already owned.
- The metric/kernel/angular sector did not change.

All four registered replay commands passed in a writable `/work` copy.