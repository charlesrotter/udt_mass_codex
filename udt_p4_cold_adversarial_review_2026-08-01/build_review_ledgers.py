#!/usr/bin/env python3
"""Build the cold-review ledgers from explicit reviewer regrades.

The clauses below are deliberately finer than the 29 frozen headline bundles.  This
builder is review-owned; it never changes or imports a producer's verdict.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


META = {
    "P4-00": ("MAP-only variation-domain framing; owner clearances are operational facts", "MAP_ONLY; L1-L8 explicitly OPEN/CHOSE/THEORY", "a derived response, selected domain, action, or physics", "udt_p4_variation_domain_map_2026-07-28/MAP.md"),
    "P4-01": ("registered positive-triangular chart, pointwise one-parameter off-shell E02 family", "FOR_ALL_MEMBERS_OF_REGISTERED_CHART_CLASS; supplied reduction gates remain conditional", "global assignment, dynamics, or a selected extension", "udt_p4_routeB_extension_selection_2026-07-28/AUDIT_REPORT.md"),
    "P4-02": ("CHOSE stationary R x T2 local-toric comparison domain and the conditional C2/Bach versus EH+Lambda pair", "EQUATION_SET_INEQUIVALENCE; NOT_EMPTY_COMMON_SOLUTION_SET", "absence of all common solutions or a verdict on other actions/domains", "udt_p4_routeC_shared_static_sector_2026-07-28/AUDIT_REPORT.md"),
    "P4-03": ("typed Stage-1 registered domain; 16 census objects include fields, anchors, forks, gauge, and chart structure", "POSED_PROBLEM; POINTWISE_REGISTERED_CLASS; R11_PER_ROW_AND_STATUS_ROW_SEPARATE", "a metric-derived exhaustive physical field census or selected response law", "udt_p4_routeA_response_inverse_problem_2026-07-29/AUDIT_REPORT.md"),
    "P4-04": ("reference-map scope only", "MAP_ROWS_NOT_MATHEMATICAL_RESULTS", "independent validation of the imported GR techniques or any UDT answer", "udt_gr_analog_reconnaissance_2026-07-29/AUDIT_REPORT.md"),
    "P4-05": ("stationary registered chart, declared jet<=2 alphabet, off degeneration strata and cut by derived on-stratum identities", "EXACT_WITHIN_ORDER_BOUND; DEEPER_RESONANCE_NOT_EXHAUSTED", "all-jet/global/on-shell completeness or selection of the EH-form", "udt_p4_routeA_stage2_pointwise_reduction_2026-07-29/AUDIT_REPORT.md"),
    "P4-06": ("declared pointwise gate cut on R_PW", "BOUNDED_GATE_CENSUS; RESONANCE_CONTACTS_PENDING", "the queued resonance-locus census or whole-solution closure", "udt_p4_routeA_stage3_gate_cut_2026-07-29/AUDIT_REPORT.md"),
    "P4-07": ("fiberwise-quadratic p-unmixed stationary slice and integrated pairing branch", "EXISTENCE_WITHIN_REGISTERED_QUADRATIC_CLASS", "a universal solution atlas, physical mass, or pointwise-pairing result", "udt_p4_routeA_slice2_solution_legs_2026-07-29/AUDIT_REPORT.md"),
    "P4-08": ("registered full-cell response class with branch-labeled conditional mass definitions", "FULL_CELL_MEANS_CELL_PROFILE_WITHIN_DECLARED_RESPONSE_CLASS; MASS_IS_DEFINITIONAL", "physical mass ownership or all response/action classes", "udt_p4_routeA_slice2b_full_cell_2026-07-29/AUDIT_REPORT.md"),
    "P4-09": ("banked tangent dimensions, enumerated pairings, stationary jet<=2 footing", "REDUCTION_WITHIN_DECLARED_PAIRING_CLASS", "a metric derivation of the census choice or the unrun field-response exhaustion", "udt_p4_bookkeeping_forcing_2026-07-29/AUDIT_REPORT.md"),
    "P4-10": ("Route-B-analog class/coherence/cocycle/alphabet registration grade", "REGISTRATION_NOT_RESPONSE_EXHAUSTION; owner sign-off pending in source wording", "a selected field census, exhausted field-response space, or mass verdict", "udt_p4_routeD_field_registration_2026-07-29/AUDIT_REPORT.md"),
    "P4-11": ("P0/P1 seal and pairing ladders in the registered stationary chart", "PER_SECTOR_AND_PAIRING_BRANCH; epsilon_m supplied where stated", "a universal parity value or physical mass exclusion", "udt_p4_routeP_seal_parity_2026-07-29/AUDIT_REPORT.md"),
    "P4-12": ("field-census, P1-4D, quadratic-at-lock, E0!=0 and five explicitly listed cutting conditions", "WHEREVER_E0_NONZERO_WITHIN_NAMED_CLASS", "global constancy, dynamics, or a physical massive carrier", "udt_p4_gradient_seat_2026-07-29/AUDIT_REPORT.md"),
    "P4-13": ("typed R-A premise and explicitly separated banked versus unregistered completion classes", "CONDITIONAL_ON_R_A_AND_CLASS_SCOPE", "an adopted fold, universal selector, or class-independent collapse", "udt_p4_angular_completion_2026-07-30/AUDIT_REPORT.md"),
    "P4-14": ("documented canon provenance and Charles's explicit split-and-keep ruling", "PROVENANCE_CLASSIFICATION_NOT_NEW_DERIVATION", "derivation of G18 closure", "udt_mirror_canon_provenance_audit_2026-07-30/PROVENANCE_REPORT.md"),
    "P4-15": ("stationary seam, Branch-G-interior and exact three-premise Picard locus where invoked", "BRIDGE_ONLY_GENERAL; FOLD_ONLY_ON_NAMED_LOCUS", "unconditional closure/fold selection or other arenas", "udt_p4_seam_closure_derivation_2026-07-30/AUDIT_REPORT.md"),
    "P4-16": ("N=2 first-germ wall layer, per realized configuration and per discrete posture", "AT_REALIZED_GERM; POSTURE_CONDITIONAL", "N=4/higher germs, posture selection, corners, or dynamics", "udt_p4_boundary_action_gate_2026-07-30/AUDIT_REPORT.md"),
    "P4-17": ("registered completion-cycle census, stationary quadratic class, named postures/censuses/pairings", "REAL_TARGET_THEOREM_ON_BANKED_CENSUS; EXOTIC_COMPLETIONS_OPEN", "absence of integers for an added compact target or unregistered topology", "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md"),
    "P4-18": ("reduced stationary second variation, N=2, declared wall-germ and pairing branches; ell=1 normalization where stated", "SECTOR_STABILITY_NOT_FULL_DYNAMICAL_STABILITY", "full joint stability with unpinned germ curvature/lambda-Schur, time evolution, or a physical particle", "udt_p4_stability_slice_2026-07-30/AUDIT_REPORT.md"),
    "P4-19": ("registration test with an ADJOINED U(1) factor and REGISTERED-POSIT S1 field", "REGISTRATION_NOT_OWNERSHIP_OR_ADOPTION; K4_CHARACTERS_NOT_WHOLE_K4", "a native carrier, adopted field, or on-shell integer selection", "udt_p4_doorway_study_2026-07-31/AUDIT_REPORT.md"),
    "P4-20": ("IF-ADOPTED theta, six-class declared menu, banked N=2 completion/census/parity layers", "CONDITIONAL_MENU; C_THETA_DATA_NOT_BANKED_MASS_PARAMETER", "a selected coupling, particle spectrum, or unconditional mass quantization", "udt_p4_coupling_derivation_2026-07-31/AUDIT_REPORT.md"),
    "P4-21": ("authorized time-live MAP and premise ledger only", "MAP_AND_OWNER_RULING", "T1-T4 results merely from the map", "udt_p4_timelive_map_2026-07-31/TIME_LIVE_MAP.md"),
    "P4-22": ("time-live posing, registered chart, jets<=2, both lock readings, static controls", "POSED_DOMAIN_NOT_SOLVED_RESPONSE; SHIFT_STATUS_READING_CONDITIONAL", "a selected lock reading, integration-layer identity, or time-live solution", "udt_p4_timelive_stage_T1_2026-07-31/AUDIT_REPORT.md"),
    "P4-23": ("pointwise time-live module at unconditional layers, with stratum qualifiers and both readings", "FORMAL_MODULE_EMBEDDING_NOT_FIXED_REALIZED_SOLUTION", "integration-layer gauge closure, unique response, or on-shell coexistence", "udt_p4_timelive_stage_T2_2026-07-31/AUDIT_REPORT.md"),
    "P4-24": ("banked untwisted completion census; IF-ADOPTED theta layers; kinematic label grade", "UNTWISTED_NATIVE_CENSUS; PROVISIONAL_IF_ADOPTED_MARRIAGE", "twisted mapping-torus census, dynamics, state quantization, or mass cuts", "udt_p4_timelive_stage_T3_2026-07-31/AUDIT_REPORT.md"),
    "P4-25": ("cleared angular MAP only", "MAP_AND_OWNER_TORUS_FIRST_SEQUENCE", "an angular result before A1-A3", "udt_p4_angular_map_2026-07-31/ANGULAR_MAP.md"),
    "P4-26": ("angular-live posing on covariant metric rows, registered chart, both spatial readings", "POSED_DOMAIN; RESIDUAL_GROUP_WITH_AMENDMENTS", "a selected reading, KK ansatz, response law, or on-shell solution", "udt_p4_angular_stage_A1_2026-07-31/AUDIT_REPORT.md"),
    "P4-27": ("pointwise tri-graded jet<=2 module, unconditional layers plus named conditional character strata", "MODE_UNIFORM_FORMAL_MODULE; NOT_EACH_MODE_ON_SHELL", "mode selection, integration-layer closure, or realized angular-live solution", "udt_p4_angular_stage_A2_2026-07-31/AUDIT_REPORT.md"),
    "P4-28": ("frozen smooth-regular positive-metric target census across registered completion rows, linear time and theta absent", "CENSUS_COMPLETENESS_NOT_SOLUTION_SPACE_COMPLETENESS", "singular/distributional fields, exotic completions, completion joins, or angular-live on-shell coexistence", "udt_p4_angular_stage_A3_2026-07-31/AUDIT_REPORT.md"),
}


CLAIMS = {
    "P4-00": ["the P4 artifact is a MAP", "the variation-domain frame is stated whole", "premise rows L1-L8 are explicit", "Charles cleared staged B-to-A with C parallel"],
    "P4-01": ["the seven-parameter extension family survives all four tested constraint layers", "the residual signed-diagonal chart symmetry is exactly K4"],
    "P4-02": ["the comparison is C2/Bach versus EH+Lambda", "the pair shares no exact static equation sector", "the negative is confined to the registered comparison domain"],
    "P4-03": ["the inverse problem is posed", "the variation-domain census has 16 objects", "all R1-R15 requirements are formalized", "the primary tally is 8 pointwise, 2 whole-solution, and 4 global-completion, with R11 per-row", "no Lorentz-invariant generator member exists in the registered class", "the response must be treated as an equivariant family rather than an invariant fixed object"],
    "P4-04": ["the GR-analog map has 11 veins", "the GR-analog ledger has 26 rows", "a Category-A technique shortlist is identified", "RED-row answer imports such as exp(iS) quantization are banned"],
    "P4-05": ["R_PW is nonempty", "R_PW is exactly parametrized at the declared order and stratum scope", "R_PW is stratified", "a Noether identity occurs on k_mod=0", "k_mod=0 is the only codimension-one Noether cut found", "the conditional EH-form is a member of R_PW"],
    "P4-06": ["the declared gate cut on R_PW was performed", "the deeper resonance-locus census remains queued", "that census is a precondition before using locus-contacting candidates"],
    "P4-07": ["the quadratic-w atlas obeys exp(a_F p0)=(a_F^2 E0/2)x^2+w1 x+w0", "the integrated massive locus is I_p=0 with E0>0", "the bootstrap tie is 2 E0 I_p=0", "the bootstrap tie belongs to the integrated branch only"],
    "P4-08": ["a full-cell atlas is supplied within the declared class", "M-GEN equals M-DENS-proper equals 2 ell E0", "M-WALL equals a_F times M-GEN", "the mass branches are candidate definitions", "no mass definition is promoted to physical mass"],
    "P4-09": ["the constant-versus-field census fork reduces the integrated-versus-pointwise bookkeeping fork", "the reduction is a theorem on the declared tangent/pairing class", "the census fork remains free", "no banked source then decided the census fork"],
    "P4-10": ["the field-moduli class registers at Route-B-analog grade", "the package was the first P4 verdict with no required amendment", "the census fork becomes a pure domain-definition choice at class-registration level"],
    "P4-11": ["epsilon_lambda=-1 is derived on the named mirror-seal ladder", "constant lambda is then pinned to zero", "anchored pairing bifurcates", "the massive certificate fails on the P1-4D landing", "the computed triad certificate remains intact"],
    "P4-12": ["free lambda(x) rows force lambda=0 wherever E0 is nonzero on P1-4D", "constancy emerges on that named class", "a fields-census massive class survives only under five named cutting conditions"],
    "P4-13": ["the angular selector is conditional on typed premise R-A", "R-A identifies the fold with a point involution", "the fields-massive class collapses under R-A on the stated class", "R-A, a pointwise crease, and banked completeness are jointly unsatisfiable on the stated class"],
    "P4-14": ["the mirror record contains a derived seam bridge", "the closure promotion was ratified but never derived", "Charles ruled split-and-keep", "G17 finiteness was kept on its independent anchors", "G18 closure is an owner-ratified working proposal"],
    "P4-15": ["the phi=0 seam bridge is derived", "the seam forces only a data handshake", "closure remains free among named postures", "the fold is Picard-forced exactly on its full three-premise Branch-G locus"],
    "P4-16": ["the wall response is almost rigid at N=2", "the realized glue germ has B_rho=q/2", "the glue flux seal holds iff B_Q=0", "the remaining discriminator is the discrete posture", "the tested postures are quotient, two-sided, and open"],
    "P4-17": ["no integer quantization follows on the banked target census", "the live banked response/holonomy targets tested here are real", "an integer lattice requires a compact or circle-valued target kernel", "the missing compact target is the doorway", "the period gate selects no posture", "uniform all-definite cyclic rings are massless", "massive cyclic escape requires heterogeneity or an indefinite member", "a massive mixed crease-glue chain is certified conditionally"],
    "P4-18": ["the constants-census massive chain is unstable with free angular wall data in the reduced sector", "the odd-parity pin absorbs the unique reduced negative direction", "the jet-quadratic field lock sector is stable iff 64 E0^2 ell^4 <= g_p c_m pi^4", "the inequality is a conditional mass-size-stiffness relation", "the double-crease massive domain is empty at the banked layer"],
    "P4-19": ["the theory owns some doorway ingredients but not a compact field", "K4 itself equals the real points of the screen U1", "a new S1-valued field registers legally", "that field is REGISTERED-POSIT rather than adopted", "the first live winding equation is sum(c_i L_i)+sum(J_s)=2 pi n_w", "the carrier posit is only partially connected at its circle or phase layer"],
    "P4-20": ["six lawful coupling classes exist in the IF-ADOPTED menu", "the c_theta lattice cut is exact", "disjointness holds at both supplied crease-parity signs", "the certified massive chain carries no theta momentum at the banked N=2 layer", "every derived Z lattice is confined away from the certified massive chain", "E0 remains uncut everywhere in the declared menu", "the integers label completion sheets rather than particle states"],
    "P4-21": ["the time-live artifact is a MAP", "Charles cleared everything-on bounded-by-layer with controls only", "premise rows T-L1 through T-L8 are explicit", "the time-topology fork is carried three ways", "the owner-kernel correction is incorporated", "the staged program is T1 through T4"],
    "P4-22": ["the inverse problem is re-posed time-live", "the declared layer keeps all time-live fields on", "the native shift-row form is derived", "the canon clock pin is physically distinct from an ADM lapse pin when drift is nonzero", "there is no arbitrary free lapse on the locked leg", "K4 survives and the layered residual group grows", "R1-R15 are re-posed with zero posing-level breaks", "the temporal mirror parity assignment is derived at metric level", "the static response posing embeds tangentially", "C-1 static recovery is exact", "the lock-reading fork is load-bearing", "both lock readings are carried into T2"],
    "P4-23": ["the pointwise layer is re-run time-live", "shift equivariance still forces Q=c_E exp(-phi)", "bare t dependence is excluded from the invariant alphabet", "all three R_N slots survive as coordinate-branch physical-content components", "R_PW^T has the same unconditional module shape on both lock readings", "the lock fork changes the R_N reading rather than the pointwise module shape", "the lock decision is deferrable past the pointwise layer", "static R_PW embeds exactly as the formal static stratum", "the k_mod=0 identity extends verbatim", "the R_N sector adds no Noether term", "C-1 recovery is exact"],
    "P4-24": ["T3 gives a mixed bridge-test result", "no native integer appears on the banked untwisted time census", "massive implies non-uniform proper period on the named branch", "IF-ADOPTED epsilon_theta=+1 gives a provisional label-level marriage", "both conditional massive carriers can carry n_t labels on the named completion branches", "E0 and ell remain uncut by the time-winding labels", "epsilon_theta=-1 strengthens disjointness", "the twisted-identification or mapping-torus class is an open native-integer seat", "the marriage is kinematic and not an on-shell coexistence result"],
    "P4-25": ["the angular artifact is a MAP", "Charles cleared torus-first sequencing", "no banked negative already covers angular field dependence", "premise rows A-L1 through A-L9 are explicit", "A3 is posed as the line-branch integer census"],
    "P4-26": ["A1 re-poses the problem angular-live", "the covariant metric block is opened natively", "angular mixed rows are permitted rather than forced", "the opening is not a Kaluza-Klein ansatz", "K4 survives", "the amended residual-symmetry census includes the zeta slack", "the amended residual group has the stated semidirect tower rather than a direct product", "the spatial-reading fork makes m irreducible under the coordinate pin and removable under the projected pin", "both spatial readings are carried", "R1-R15 have zero posing-level breaks", "C-1 T1 recovery is exact", "C-2 transitive static recovery is exact", "17 registry entries are flagged for later scope review"],
    "P4-27": ["A2 runs the pointwise angular-live layer", "phi forcing is mode-uniform", "both R_m slots survive as coordinate-branch physical content", "the unconditional module parametrization is reading-independent", "R_PW^T embeds exactly at mode zero and m=0 at the banked layers", "the k_mod=0 identity extends verbatim", "the m sector adds no term to that identity", "R_PW^A is mode-uniform in form", "P3b is a conditional granted-mirror seat that reaches mode zero", "C-1 and C-2 controls recover exactly"],
    "P4-28": ["A3 has outcome class mixed-by-kind", "A3 is verified-with-caveats", "the amended census has 126 rows", "the census covers torus, registered two-cap S3, and all smooth regular detail by target contraction", "fixed mode, presentation, Hopf, and base integers survive", "continuous owned-fiber holonomy survives", "no solution-dependent native integer is found in the declared smooth census", "no declared integer cuts either conditional massive carrier's banked parameters", "the carrier-to-two-cap-S3 completion joins remain open", "nonzero angular-live on-shell coexistence remains open"],
}


RETAIN_IF = {
    "P4-04": set(CLAIMS["P4-04"]),
    "P4-06": set(CLAIMS["P4-06"]),
    "P4-14": set(CLAIMS["P4-14"]),
    "P4-21": set(CLAIMS["P4-21"]),
    "P4-25": set(CLAIMS["P4-25"]),
}
for uid in ("P4-08", "P4-10", "P4-13", "P4-17", "P4-19", "P4-20", "P4-22", "P4-24", "P4-28"):
    RETAIN_IF.setdefault(uid, set()).update(c for c in CLAIMS[uid] if any(w in c for w in ("no mass definition", "remains queued", "open", "carried", "not adopted", "rather than particle", "C-1", "C-2", "flagged")))


QROWS = [
    ("Q1", "Does the inverse-problem domain follow without silent alphabet/pairing/posture/census choices?", "NARROWED", "Only the reciprocal anchor, chart constraints, and some transformation laws are derived; the 16-object domain explicitly carries CHOSE/OPEN alphabet, pairing, posture, census, completion, and variation forks.", "EXISTENTIAL_DOMAIN_POSING_NOT_UNIQUE_METRIC_DERIVATION"),
    ("Q2", "Do static, time-live, and angular-live spaces embed exactly without a formal-family/fixed-metric quantifier change?", "OPEN", "The banked package controls and this cold parser regression recover the formal pointwise module pullbacks exactly; this is not a cold different-method proof, and no fixed realized time/angular-live on-shell metric family was constructed, so solution-level embedding remains open.", "FORMAL_MODULE_FOR_ALL_MEMBERS; BANK_CONTROL_PLUS_COLD_PARSER_REGRESSION; FIXED_REALIZED_SOLUTION_OPEN"),
    ("Q3", "Do mass branches and stability results survive full premise stacks?", "NARROWED", "The algebra survives only as conditional mass definitions and reduced-sector Hessian results; full dynamical stability, unpinned wall-germ curvature, lambda-Schur closure, and physical mass ownership remain open.", "CONDITIONAL_DEFINITIONS_AND_SECTOR_STABILITY_ONLY"),
    ("Q4", "Is real-character versus circle-integer distinction a theorem of the admitted domain?", "NARROWED", "Yes for the explicitly admitted targets: real additive kernels give no lattice and an S1 target gives 2pi Z; which compact transition/field targets belong to the physical domain remains a topology/ownership choice.", "TARGET_KERNEL_THEOREM; TARGET_OWNERSHIP_OPEN"),
    ("Q5", "Does A3 exhaust torus, full-sphere, and fine-detail layers without steering?", "NARROWED", "A3 exhausts its 126-row smooth-regular registered census and its target-contraction argument is all-mode/all-finite-jet; singular fields, exotic completions, transitive dependency freeze, completion joins, and on-shell solution space are not exhausted.", "FROZEN_SMOOTH_CENSUS_ONLY"),
    ("Q6", "Are coordinate/projected forks shape-neutral through A2 and where distinguishable?", "RETAINED", "Fresh Schur-complement algebra confirms identical unconditional pointwise module coordinates; they differ already in interpretation of N and m as physical content versus chart-slack, and can become equation-distinguishable only at integration/on-shell layers.", "UNCONDITIONAL_POINTWISE_MODULE; CONDITIONAL_STRATA_STAMPED"),
    ("Q7", "Which claims are independent and which share derivation/implementation?", "NARROWED", "Package verifiers usually use separate scripts but share the same frozen definitions, symbolic conventions, generated ledgers, and same-session context; cold checks independently confirm selected algebra, while many completeness/embedding checks remain parser or replay evidence.", "METHOD_BY_METHOD_INDEPENDENCE_NOT_PACKAGE_LABEL"),
    ("Q8", "Does nuclear scoping remain separated?", "RETAINED", "The governing correction separates banked structural theorems, textbook/SEMF reimplementation, and conditional identifications; the ladder is CONSISTENCY-DEMO and the a_F-lambda test remains unresolved, not a prediction.", "CORRECTION_LAYER_PRECEDENCE; NO_NUCLEAR_PROMOTION"),
]


# Clause-specific premise reconstruction.  Every exploded package clause receives
# the source byte hash, a literal source-clause stamp, and the full package-local
# conditions that control the claim.  These are intentionally more exact than the
# package-wide META summaries and are not claims of physical adoption.
PREMISE_DETAIL = {
    "P4-00": "MAP_ONLY; L1-L8 retain their OPEN/CHOSE/THEORY labels; owner clearance is operational, not a response/action/physics derivation",
    "P4-01": "positive triangular registered chart; pointwise one-parameter off-shell E02 family; seven-parameter extension only inside the supplied reduction gates; signed-diagonal residual group K4; global assignment, dynamics, action and physical selection open",
    "P4-02": "CHOSE stationary local-toric R x T2 domain; conditional C2/Bach and EH+Lambda actions; strong-CSN inactive; vacuum equations; all real Lambda compared; equation-set inequivalence does not imply an empty common-solution set; other actions/domains open",
    "P4-03": "registered pointwise Stage-1 class; 16 objects include nonfields/anchors/forks/gauge/chart data; equivariance modulo K4; R1-R15 posed with R11 per-row plus status row; global/whole-solution layers and action selection open",
    "P4-04": "reference MAP only; GR techniques are comparison tools; RED answer imports banned; no UDT equation, action, response or field ownership inferred",
    "P4-05": "stationary registered response chart; jet order <=2; polynomial-formal moduli alphabet; degeneration strata off and derived cut identities on; k_mod=0 Noether cut; deeper resonances, global/on-shell closure and EH-form selection open",
    "P4-06": "pointwise R_PW gate only; declared gate predicates applied; resonance-contact census pending; no global, integration-layer or on-shell solution closure",
    "P4-07": "stationary BASE-READY representative fiberwise-quadratic p-unmixed slice; jet order <=2; P1 integrated pairing only; real a_F and a_F!=0 for nontrivial quadratic branch; ell>0; E0>=0 definite and E0>0 on named massive locus; I_p=0; bootstrap is a WORKING lens; mass is conditional",
    "P4-08": "stationary BASE-READY full-cell profiles inside declared response class; arbitrary L_E plus quadratic exhaustiveness only in that class; P1 integrated/pointwise and P2 branches separated; definite/indefinite signs retained; ell>0; M-GEN/M-DENS/M-WALL are conditional definitions, not physical mass",
    "P4-09": "stationary jet<=2 tangent bookkeeping; constant-versus-field census and integrated-versus-pointwise pairings kept distinct; reduction holds only in the enumerated tangent/pairing class; census ownership remains open",
    "P4-10": "Route-B-analog field/moduli class, coherence, cocycle and alphabet registration only; census is a domain-definition choice at this grade; response exhaustion, action and physical field selection absent",
    "P4-11": "registered stationary P0/P1 seal and pairing ladders; epsilon_lambda=-1 derived; constant lambda then zero on named ladder; epsilon_kmod=-1 only where P2 states it; epsilon_m is supplied; BASE and BR-M branches separated; P1-4D a_F=0 certificate fails while P1-triad a_F=1 certificate remains",
    "P4-12": "FIELD census; Route-D promoted-moduli jet alphabet; stationary P1-4D with a_F(0)=0; generic g_p!=0 and Delta_G=g_f*g_h-g_x^2!=0; E0=L_fh!=0; p=0 with affine f,h; free lambda forced to zero only on named class; five cutting conditions include supplied wall slope, locked-row vanishing, M-WALL=0 and open completion/canon choices; P1-triad remains separate",
    "P4-13": "typed premise R-A is supplied conditionally; banked and unregistered completion classes separated; fold/point involution and collapse statements hold only on stated class; no fold, topology, action or selector adopted",
    "P4-14": "provenance audit only; derived seam bridge separated from owner-ratified G18 proposal; G17 anchors independent; no new closure or action derivation",
    "P4-15": "stationary phi=0 seam; Branch-G equations on both interior sides; rho'(r_s)=0 and the full named C1/Picard regularity locus required for fold uniqueness; rho'!=0 branch does not fold; bridge is general but posture/closure remains free",
    "P4-16": "N=2 first-germ boundary-action layer at each realized seam and discrete posture; c_E!=0 where divided; B_rho=q/2; glue-flux seal iff B_Q=0; quotient/two-sided/open postures carried separately; N>=4, corners, dynamics and posture selection open",
    "P4-17": "registered stationary quadratic completion-cycle census; all named postures/cycles/pairings carried; real additive target has no integer lattice; compact/circle target is an added doorway; uniform all-definite cyclic ring uses E_i>=0 and L_i>0 and is massless; heterogeneous/indefinite and mixed-chain escapes are conditional; exotic completions open",
    "P4-18": "reduced stationary second variation only; N=2 wall-germ and pairing branches; ell=1 normalization only where stated; positivity uses E0>0, g_p>0 and c_m>0 on named sector; odd-parity pin and lambda-Schur/wall-curvature qualifications retained; sector Hessian is not dynamical or particle stability",
    "P4-19": "REGISTERED-POSIT S1-valued theta field and ADJOINED U(1), neither owned nor adopted; K4 character image {+1,-1}, not K4 itself, is real two-torsion; cyclic winding n_w in Z depends on the added circle target; no on-shell integer selection",
    "P4-20": "IF-ADOPTED theta only; six declared coupling classes; c_theta lattice data are not a banked mass parameter; N=2 completion/census/parity layers retained; supplied epsilon signs and coupling terms are branch-conditional; E0 remains free; integers label completion sheets, not particle states; no coupling/action adopted",
    "P4-21": "authorized time-live MAP only; T-L1 through T-L8 retain their labels; controls-only and three topology forks carried; T1-T4 sequence is programmatic, not a result or adoption",
    "P4-22": "time-live posing in registered jet<=2 chart; all fields on; both lock readings and static controls carried; shift row native; clock pin differs from ADM lapse pin when drift nonzero; temporal mirror parity is metric-level; C-1 is parser/regression control, not an on-shell solution",
    "P4-23": "pointwise time-live formal module at unconditional layers; stratum qualifiers and both lock readings retained; Q=c_E*exp(-phi); bare t excluded; three R_N slots are coordinate-branch content only under named reading; static embedding is formal module/bank-control grade; integration gauge, uniqueness and on-shell coexistence open",
    "P4-24": "banked untwisted completion census plus IF-ADOPTED theta layers; epsilon_theta=+1 is provisional label-level marriage and epsilon_theta=-1 is disjointness branch; E0 and ell uncut; twisted mapping-torus class open; winding is kinematic, not dynamics/state quantization/on-shell coexistence",
    "P4-25": "cleared angular MAP only; A-L1 through A-L9 retain labels; torus-first sequence is operational; no angular result, field/action selection or solution follows from the map",
    "P4-26": "angular-live posing on covariant metric rows; registered chart; coordinate-pin and projected spatial readings both carried; angular mixed rows permitted but not forced; no KK ansatz; K4 and amended zeta-slack semidirect residual group; C-1/C-2 are recovery controls; no response or on-shell solution",
    "P4-27": "pointwise tri-graded angular jet order <=2 formal module; unconditional layers plus named conditional character strata; both readings; R_N/R_m coordinate-branch semantics retained; mode-uniform form does not mean each mode is on shell; C-1/C-2 are bank-control/parser grade; integration closure open",
    "P4-28": "frozen smooth-regular positive-metric target census across registered torus/two-cap-S3 rows; linear time and theta absent; 126-row census; fixed architecture integers and continuous holonomy separated from solution-dependent integers; singular/distributional fields, exotic completions, joins and angular-live on-shell coexistence open",
}


ACTION_CELLS = {
    "P4-02": "conditional C2/Bach and EH+Lambda action pair explicitly compared; neither action selected",
    "P4-07": "no native action selected; reduced conditional action/ODE and integrated response pairing are explicitly used",
    "P4-08": "no native action selected; cell-energy first integral and conditional action-derived mass definitions are explicitly used",
    "P4-16": "no global action or posture selected; seam functional B and its N=2 first variation are explicitly active",
    "P4-18": "no complete action selected; reduced second variation/Hessian and wall-germ Hessian sectors are explicitly tested",
    "P4-20": "no coupling or action selected; IF-ADOPTED theta coupling classes and coupling terms are explicitly tested",
}


OVERLAY_CLASS = {
    "archive/horizon_cmb_correspondence.md": "SUPPORTING",
    "archive/udt_validated_results.md": "SUPPORTING",
    "c2_finite_cell_boundary_variation_2026-07-20/AUDIT_REPORT.md": "LOAD_BEARING",
    "grok/quarantine_free_DA/macro_sector_fork_resolution.md": "SUPPORTING",
    "legacy/root_oneoffs_2026-07-01/native_phi_sign_mirror_bridge_audit.py": "LOAD_BEARING",
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md": "LOAD_BEARING",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": "LOAD_BEARING",
    "native_action_stage1_2026-07-18/arm_B/cold_output/D0_D5.md": "SUPPORTING",
    "udt_common_scale_neutrality_provenance_audit_2026-07-24/AUDIT_REPORT.md": "SUPPORTING",
    "udt_founded_phi_complete_coframe_extension_audit_2026-07-25/AUDIT_REPORT.md": "LOAD_BEARING",
    "udt_higher_isometry_plane_ownership_audit_2026-07-28/PREREGISTRATION.md": "SUPPORTING",
    "udt_higher_isometry_plane_ownership_audit_2026-07-28/TORIC_CAP_ENUMERATION.tsv": "LOAD_BEARING",
    "udt_joint_selector_provenance_audit_2026-07-28/JOINT_OPERATION_OBLIGATIONS.tsv": "LOAD_BEARING",
}


CONDITION_TRIGGERS = {
    "SIGN": ("epsilon", "parity", "sign", "definite", "indefinite", "odd", "negative direction", "nonzero", "K4"),
    "POSITIVITY": ("E0", "mass", "stable", "positiv", "definite", "energy", "inequality"),
    "NORMALIZATION": ("ell", "π", "q/2", "2 E0", "2 pi", "64 E0", "M-GEN", "M-WALL", "winding equation"),
    "BRANCH": ("branch", "locus", "landing", "slice", "reading", "sector", "stratum", "static", "massive", "lock", "triad", "full-cell", "mode zero"),
    "BOUNDARY_GERM": ("wall", "seam", "glue", "germ", "boundary", "crease", "cap", "fold"),
    "PAIRING": ("pairing", "integrated", "pointwise", "P1", "P2", "census fork"),
    "POSTURE": ("posture", "quotient", "two-sided", "open", "cycle", "chain"),
    "TOPOLOGY": ("K4", "torus", "S1", "U1", "circle", "winding", "integer", "topolog", "Hopf", "cap", "S3", "completion", "cycle", "holonomy", "lattice"),
}

CONDITION_VALUES = {
    "SIGN": {
        "P4-01": "signed-diagonal residual group has exactly the four K4 elements listed in the anchored source excerpt",
        "P4-07": "a_F is real and a_F!=0 only for the nontrivial quadratic branch; E0>0 only on the named massive locus",
        "P4-08": "definite and indefinite response branches remain separate",
        "P4-11": "epsilon_lambda=-1 derived; epsilon_kmod=-1 only on P2 where stated; epsilon_m supplied; a_F=0 on P1-4D and a_F=1 on P1-triad",
        "P4-12": "E0!=0 is a nonvanishing branch condition, not an unconditional sign or positivity assertion",
        "P4-16": "c_E!=0 wherever the glue-flux equation is divided",
        "P4-17": "all-definite and indefinite members remain distinct",
        "P4-18": "the odd-parity pin is branch-specific; positivity signs are E0>0, g_p>0, c_m>0 only on the tested sector",
        "P4-19": "K4 character values are {+1,-1}; the order-four K4 group itself does not embed in U(1)",
        "P4-20": "both supplied crease-parity signs are carried; theta status is IF-ADOPTED",
        "P4-24": "epsilon_theta=+1 provisional-marriage branch and epsilon_theta=-1 disjointness branch remain separate",
        "P4-22": "temporal metric parity flips the shift row; coframe-layer and stratum qualifications remain explicit",
        "P4-26": "K4 characters, angular mirror signs and reading-conditional slack transformations remain source-scoped",
        "P4-28": "fixed signed characteristic data are architecture labels, not solution-dependent integer cuts",
    },
    "POSITIVITY": {
        "P4-07": "ell>0; E0>=0 on the definite class and E0>0 on the named massive locus",
        "P4-08": "ell>0; mass labels are conditional definitions on their named sign branches",
        "P4-11": "massive-locus positivity certificate requires a_F!=0; it is uncertified at the P1-4D a_F=0 landing",
        "P4-12": "E0=L_fh!=0 and generic g_p!=0, Delta_G!=0; this is nonvanishing, not universal positivity",
        "P4-13": "the R-A collapse forces E0=0 only on the stated conditional completion/crease class",
        "P4-17": "E_i>=0 and L_i>0 only in the uniform all-definite cyclic theorem",
        "P4-18": "E0>0, g_p>0 and c_m>0 on the named PSD sector; no full dynamical stability",
        "P4-20": "E0 remains uncut by the declared coupling menu",
        "P4-24": "E0 and ell remain uncut by time-winding labels",
        "P4-28": "positive-metric smooth-regular target census only; no carrier-parameter cut",
    },
    "NORMALIZATION": {
        "P4-07": "exp(a_F p0)=(a_F^2 E0/2)x^2+w1*x+w0 and ell>0 as source-normalized",
        "P4-08": "M-GEN=M-DENS-proper=2*ell*E0 and M-WALL=a_F*M-GEN are definitions",
        "P4-16": "B_rho=q/2 at the realized N=2 glue germ",
        "P4-17": "real targets have no lattice; a compact circle would introduce a 2*pi normalization only conditionally",
        "P4-18": "ell=1 only where stated; retain the exact 64*E0^2*ell^4 <= g_p*c_m*pi^4 coefficient",
        "P4-19": "sum(c_i L_i)+sum(J_s)=2*pi*n_w with n_w integer only for the adjoined circle target",
        "P4-20": "retain the source c_theta lattice units; they do not normalize or cut E0",
        "P4-24": "proper-period and theta-label normalizations are branch-specific and kinematic",
        "P4-28": "E0, ell and moduli retain their banked definitions and remain uncut by the declared integer census",
    },
    "BRANCH": {
        "P4-01": "registered positive-triangular pointwise off-shell E02 family only",
        "P4-02": "CHOSE stationary local-toric R x T2 comparison family only",
        "P4-05": "stationary jet<=2 response class with degeneration strata off and k_mod=0 cut on",
        "P4-06": "five pairing branches x three strata x two G3 cells; deeper resonance cells remain census-required",
        "P4-07": "P1 integrated pairing and named quadratic massive locus only",
        "P4-08": "P1 integrated/pointwise and P2 branches remain distinct",
        "P4-11": "BASE, BR-M, P1-4D and P1-triad ladders remain distinct",
        "P4-12": "P1-4D locked class only; P1-triad remains separate",
        "P4-13": "R-A conditional stated class only",
        "P4-15": "Branch-G interior on both sides plus the full Picard locus",
        "P4-17": "registered cyclic/acyclic, definite/indefinite and mixed-chain branches only",
        "P4-18": "reduced stationary N=2 sector and named wall/pairing branches only",
        "P4-20": "six IF-ADOPTED coupling classes across all carried posture/census/pairing/parity branches; none selected",
        "P4-22": "both time-lock readings carried; no reading selected",
        "P4-23": "both lock readings at formal pointwise module grade; fixed on-shell branch absent",
        "P4-24": "untwisted native and IF-ADOPTED theta branches; mapping torus open",
        "P4-25": "angular map carries torus-first staging and all named premise forks without launching or selecting a branch",
        "P4-26": "coordinate-pin and projected spatial readings both carried",
        "P4-27": "both readings and all formal modes; mode-uniform form is not per-mode on-shell existence",
        "P4-28": "registered smooth torus/two-cap-S3 census branches only",
    },
    "BOUNDARY_GERM": {
        "P4-07": "integrated cell branch only; boundary realization not selected",
        "P4-08": "cell/wall definitions remain branch-labeled; no complete boundary action",
        "P4-12": "supplied wall slope, locked-row vanishing and M-WALL=0 are among five cuts",
        "P4-13": "fold/crease is conditional on R-A and the stated completion class",
        "P4-14": "derived seam bridge is separated from the underived closure promotion; no boundary closure is inferred",
        "P4-15": "phi=0 seam, rho'(r_s)=0 and C1/Picard regularity required for the fold",
        "P4-16": "realized N=2 first germ only; N>=4 and corners open",
        "P4-17": "named completion-cycle boundary data only",
        "P4-18": "N=2 wall-germ Hessian only; free higher-germ curvature remains open",
        "P4-20": "banked N=2 crease/completion layer only",
        "P4-28": "registered regular two-cap data only; joins remain open",
    },
    "PAIRING": {
        "P4-03": "P1/P2/P3 pairings are enumerated and none adopted in the typed inverse-problem domain",
        "P4-07": "P1 integrated pairing; pointwise pairing explicitly excluded",
        "P4-08": "P1 integrated/pointwise and P2 definitions remain separate",
        "P4-09": "constant/field census and integrated/pointwise pairing forks remain free",
        "P4-10": "field-class registration does not select a pairing or exhaust the response on the promoted-field branch",
        "P4-11": "anchored pairing bifurcation retained per named seal ladder",
        "P4-12": "P1-4D pairing and field-census cuts only",
        "P4-13": "P1-4D field-census collapse is conditional on R-A and the stated completion/crease class",
        "P4-17": "only enumerated cycle/pairing census",
        "P4-18": "declared reduced pairing branches only",
        "P4-23": "coordinate physical-content and projected chart-slack pairings are both carried; integration identity remains typed",
        "P4-27": "angular formal module retains the banked pairing/reading branches; no mode or pairing is selected",
    },
    "POSTURE": {
        "P4-13": "no fold/completion posture adopted",
        "P4-15": "closure remains free among named postures",
        "P4-16": "quotient, two-sided and open postures tested separately; none selected",
        "P4-17": "all registered postures carried; period gate selects none",
        "P4-18": "posture-dependent wall-germ qualifications retained",
        "P4-20": "completion/crease postures inherited conditionally; none adopted",
        "P4-24": "time-topology/completion postures are conditional, none adopted; marriage remains label-grade",
        "P4-26": "N=2 angular wall postures are typed and carried; none selected at posing grade",
        "P4-28": "all registered completion/posture rows are censused; no posture or completion join adopted",
    },
    "TOPOLOGY": {
        "P4-01": "K4 is the residual signed-diagonal chart group only",
        "P4-03": "K4 is a residual chart quotient; boundary/completion labels remain typed and unselected",
        "P4-13": "banked and unregistered completion classes separated",
        "P4-17": "real additive targets versus added compact/circle target; exotic completions open",
        "P4-19": "only the K4 character image {+1,-1}, not K4, is U(1) real two-torsion; S1 is adjoined REGISTERED-POSIT",
        "P4-20": "integer lattices belong to IF-ADOPTED completion sheets, not particle states",
        "P4-21": "time topology is carried as line/circle/finite-cell branches; none adopted in the map",
        "P4-22": "time-topology fork remains typed-not-enumerated and no topology branch is adopted",
        "P4-24": "untwisted census only; twisted mapping-torus class open",
        "P4-25": "torus-first is sequencing only; full-sphere and angular integer questions remain staged, not selected",
        "P4-26": "angular-live residual group and torus chart only; no completion selected",
        "P4-27": "mode labels are formal module labels, not topology-selected states",
        "P4-28": "torus and registered two-cap S3 smooth census; fixed topology integers and continuous holonomy separated; joins open",
    },
}


# Curated source-local evidence anchors.  Claim indices are one-based positions in
# CLAIMS[uid].  A shared group is deliberate only when one self-contained excerpt
# states several clauses and their controlling conditions together.
PACKAGE_SOURCE_ANCHORS = {
    "P4-00": [
        ("map_scope", "udt_p4_variation_domain_map_2026-07-28/MAP.md", 1, 6, "states the frame whole", (1, 2)),
        ("premise_ledger", "udt_p4_variation_domain_map_2026-07-28/MAP.md", 54, 65, "L1 | Which extension stratum", (3,)),
        ("owner_sequence", "udt_p4_variation_domain_map_2026-07-28/MAP.md", 100, 109, "B (extension classification)", (4,)),
    ],
    "P4-01": [
        ("survival_and_k4", "udt_p4_routeB_extension_selection_2026-07-28/AUDIT_REPORT.md", 17, 39, "L1 (extension stratum): MODULUS-CARRIED", (1, 2)),
    ],
    "P4-02": [
        ("pair_scoped_inequivalence", "udt_p4_routeC_shared_static_sector_2026-07-28/AUDIT_REPORT.md", 18, 42, "INEQUIVALENT on every one of the seven independent components", (1, 2, 3)),
    ],
    "P4-03": [
        ("posed_domain", "udt_p4_routeA_response_inverse_problem_2026-07-29/AUDIT_REPORT.md", 21, 41, "The typed variation domain 𝒟", (1, 2, 3, 4)),
        ("equivariant_family", "udt_p4_routeA_response_inverse_problem_2026-07-29/AUDIT_REPORT.md", 61, 72, "No Lorentz-invariant member exists in the class", (5, 6)),
    ],
    "P4-04": [
        ("map_counts_shortlist", "udt_gr_analog_reconnaissance_2026-07-29/AUDIT_REPORT.md", 15, 22, "26 rows, 11 veins", (1, 2, 3)),
        ("import_ban", "udt_gr_analog_reconnaissance_2026-07-29/AUDIT_REPORT.md", 24, 40, "Answer imports (F-G1)", (4,)),
    ],
    "P4-05": [
        ("rpw_structure", "udt_p4_routeA_stage2_pointwise_reduction_2026-07-29/AUDIT_REPORT.md", 30, 67, "ℛ_PW = the character-matched module space CUT BY", (1, 2, 3, 4, 5)),
        ("eh_member", "udt_p4_routeA_stage2_pointwise_reduction_2026-07-29/AUDIT_REPORT.md", 82, 92, "stationary restriction): INSIDE the jet ≤ 2 class", (6,)),
    ],
    "P4-06": [
        ("gate_cut", "udt_p4_routeA_stage3_gate_cut_2026-07-29/AUDIT_REPORT.md", 22, 41, "The gates partition ℛ_PW", (1,)),
        ("resonance_queue", "udt_p4_routeA_stage3_gate_cut_2026-07-29/AUDIT_REPORT.md", 111, 130, "queued deeper resonance-census tile", (2, 3)),
    ],
    "P4-07": [
        ("quadratic_atlas", "udt_p4_routeA_slice2_solution_legs_2026-07-29/AUDIT_REPORT.md", 28, 41, "The SIGN-STAMPED emergence", (1,)),
        ("integrated_bootstrap", "udt_p4_routeA_slice2_solution_legs_2026-07-29/AUDIT_REPORT.md", 43, 61, "The emergent tie", (2, 3, 4)),
    ],
    "P4-08": [
        ("full_cell", "udt_p4_routeA_slice2b_full_cell_2026-07-29/AUDIT_REPORT.md", 23, 48, "Full-cell structure (TE1)", (1,)),
        ("mass_definitions", "udt_p4_routeA_slice2b_full_cell_2026-07-29/AUDIT_REPORT.md", 91, 100, "M-GEN = 2ℓE at full generality", (2, 3)),
        ("none_promoted", "udt_p4_routeA_slice2b_full_cell_2026-07-29/AUDIT_REPORT.md", 3, 9, "labeled mass-definition branches, none promoted", (4, 5)),
    ],
    "P4-09": [
        ("census_reduction", "udt_p4_bookkeeping_forcing_2026-07-29/AUDIT_REPORT.md", 22, 48, "R2 REDUCES to the census fork", (1, 2)),
        ("fork_open", "udt_p4_bookkeeping_forcing_2026-07-29/AUDIT_REPORT.md", 94, 105, "census fork OPEN", (3, 4)),
    ],
    "P4-10": [
        ("registration", "udt_p4_routeD_field_registration_2026-07-29/AUDIT_REPORT.md", 25, 38, "The field-moduli census REGISTERS", (1,)),
        ("no_amendment", "udt_p4_routeD_field_registration_2026-07-29/AUDIT_REPORT.md", 13, 23, "PASS with NO required amendments", (2,)),
        ("domain_choice", "udt_p4_routeD_field_registration_2026-07-29/AUDIT_REPORT.md", 101, 115, "stands as a PURE domain-definition choice", (3,)),
    ],
    "P4-11": [
        ("parity_ladder", "udt_p4_routeP_seal_parity_2026-07-29/AUDIT_REPORT.md", 38, 55, "ε_λ = −1 DERIVED", (1,)),
        ("constant_cut", "udt_p4_routeP_seal_parity_2026-07-29/AUDIT_REPORT.md", 94, 102, "constants λ = k_mod = 0 pinned", (2,)),
        ("pairing_bifurcation", "udt_p4_routeP_seal_parity_2026-07-29/AUDIT_REPORT.md", 59, 78, "The anchored-pairing bifurcation", (3, 4, 5)),
    ],
    "P4-12": [
        ("lock_emergence", "udt_p4_gradient_seat_2026-07-29/AUDIT_REPORT.md", 30, 49, "The lock-emergence theorem, fully stamped", (1, 2)),
        ("five_conditions", "udt_p4_gradient_seat_2026-07-29/AUDIT_REPORT.md", 51, 63, "The five cutting conditions", (3,)),
    ],
    "P4-13": [
        ("ra_selector_and_collapse", "udt_p4_angular_completion_2026-07-30/AUDIT_REPORT.md", 28, 63, "The selector chain under R-A", (1, 2, 3, 4)),
    ],
    "P4-14": [
        ("bridge_not_closure", "udt_mirror_canon_provenance_audit_2026-07-30/PROVENANCE_REPORT.md", 86, 104, "The underived step is the PROMOTION", (1, 2)),
        ("owner_split", "udt_mirror_canon_provenance_audit_2026-07-30/CORRECTION_LAYER.md", 89, 101, "Charles ruled", (3,)),
        ("finiteness_anchors", "udt_mirror_canon_provenance_audit_2026-07-30/CORRECTION_LAYER.md", 91, 96, "still multiply-anchored", (4,)),
        ("g18_status", "P4_ARC_SUMMARY_2026-07-31.md", 39, 42, "G18 closure = owner-ratified proposal", (5,)),
    ],
    "P4-15": [
        ("bridge_only", "udt_p4_seam_closure_derivation_2026-07-30/AUDIT_REPORT.md", 26, 32, "BRIDGE-ONLY is what banked structure derives", (1, 2, 3)),
        ("picard_fold", "udt_p4_seam_closure_derivation_2026-07-30/AUDIT_REPORT.md", 34, 42, "The conditional fold, on its FULL premise set", (4,)),
    ],
    "P4-16": [
        ("n2_wall_family", "udt_p4_boundary_action_gate_2026-07-30/AUDIT_REPORT.md", 28, 60, "OW2 — the wall response is a FAMILY", (1, 2, 3, 4, 5)),
    ],
    "P4-17": [
        ("real_target_no_lattice", "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md", 33, 56, "NO QUANTIZATION (Q-B = NO)", (1, 2, 3, 4)),
        ("no_posture_selection", "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md", 57, 65, "NO POSTURE SELECTION", (5,)),
        ("mass_sector_map", "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md", 66, 90, "THE SECTOR MAP", (6, 7, 8)),
    ],
    "P4-18": [
        ("stability_composite", "udt_p4_stability_slice_2026-07-30/AUDIT_REPORT.md", 32, 69, "Outcome class: OS-4", (1, 2, 3, 4, 5)),
    ],
    "P4-19": [
        ("doorway_composite", "udt_p4_doorway_study_2026-07-31/AUDIT_REPORT.md", 29, 79, "K₄ itself, order 4, does NOT embed in the circle", (1, 2, 3, 4, 5, 6)),
    ],
    "P4-20": [
        ("six_class_menu", "udt_p4_coupling_derivation_2026-07-31/EXACT_DERIVATION.md", 26, 77, "class-level six-member menu unchanged", (1,)),
        ("ctheta_lattice", "udt_p4_coupling_derivation_2026-07-31/EXACT_DERIVATION.md", 84, 106, "the θ-momentum is LATTICE-CUT", (2, 6)),
        ("massive_disjointness", "udt_p4_coupling_derivation_2026-07-31/EXACT_DERIVATION.md", 196, 210, "the certified massive family carries NO c_θ lattice", (3, 4, 5)),
        ("sheet_not_state", "udt_p4_coupling_derivation_2026-07-31/EXACT_DERIVATION.md", 154, 164, "never particle states", (7,)),
    ],
    "P4-21": [
        ("map_only", "udt_p4_timelive_map_2026-07-31/TIME_LIVE_MAP.md", 1, 8, "map-only; no compute; nothing launched", (1,)),
        ("premises_and_rulings", "udt_p4_timelive_map_2026-07-31/TIME_LIVE_MAP.md", 68, 145, "EVERYTHING-ON, bounded by LAYER", (2, 3, 4, 5)),
        ("staged_program", "udt_p4_timelive_map_2026-07-31/TIME_LIVE_MAP.md", 147, 165, "Stage T4 — the massive candidates time-live", (6,)),
    ],
    "P4-22": [
        ("scope", "udt_p4_timelive_stage_T1_2026-07-31/EXACT_DERIVATION.md", 1, 15, "EVERYTHING-ON per owner ruling", (1, 2)),
        ("shift_and_clock", "udt_p4_timelive_stage_T1_2026-07-31/EXACT_DERIVATION.md", 22, 42, "THE SHIFT ROW'S NATIVE FORM", (3, 4, 5)),
        ("k4", "udt_p4_timelive_stage_T1_2026-07-31/EXACT_DERIVATION.md", 93, 116, "K₄ SURVIVES VERBATIM", (6,)),
        ("requirements", "udt_p4_timelive_stage_T1_2026-07-31/EXACT_DERIVATION.md", 149, 207, "the requirement set re-posed (R1–R15", (7, 8)),
        ("static_control", "udt_p4_timelive_stage_T1_2026-07-31/EXACT_DERIVATION.md", 315, 330, "C-1: static recovery", (9, 10)),
        ("lock_fork", "udt_p4_timelive_stage_T1_2026-07-31/AUDIT_REPORT.md", 149, 161, "both-ways-undecided is CORRECT", (11, 12)),
    ],
    "P4-23": [
        ("pointwise_outcome", "udt_p4_timelive_stage_T2_2026-07-31/EXACT_DERIVATION.md", 250, 255, "Outcome class: OU-1", (1,)),
        ("phi_and_bare_t", "udt_p4_timelive_stage_T2_2026-07-31/EXACT_DERIVATION.md", 22, 49, "shift-equivariance ALONE forces Q", (2, 3)),
        ("rn_survival", "udt_p4_timelive_stage_T2_2026-07-31/EXACT_DERIVATION.md", 100, 125, "all three R_N slots SURVIVE", (4,)),
        ("reading_map", "udt_p4_timelive_stage_T2_2026-07-31/EXACT_DERIVATION.md", 127, 158, "Same depth, both branches", (5, 6, 7)),
        ("static_embedding", "udt_p4_timelive_stage_T2_2026-07-31/EXACT_DERIVATION.md", 162, 180, "EMBEDS EXACTLY", (8,)),
        ("noether", "udt_p4_timelive_stage_T2_2026-07-31/EXACT_DERIVATION.md", 190, 207, "The k_mod = 0 identity EXTENDS VERBATIM", (9, 10)),
        ("c1", "udt_p4_timelive_stage_T2_2026-07-31/EXACT_DERIVATION.md", 211, 224, "C-1: static recovery", (11,)),
    ],
    "P4-24": [
        ("amended_native_layer", "udt_p4_timelive_stage_T3_2026-07-31/AUDIT_REPORT.md", 147, 173, "massive ⇒ non-uniform", (1, 2, 3)),
        ("driver_conditions", "udt_p4_timelive_stage_T3_2026-07-31/AUDIT_REPORT.md", 175, 202, "the marriage's full premise stack", (4, 5, 6, 7, 8, 9)),
    ],
    "P4-25": [
        ("map_only", "udt_p4_angular_map_2026-07-31/ANGULAR_MAP.md", 1, 8, "map-only; no compute; nothing launched", (1,)),
        ("torus_first", "udt_p4_angular_map_2026-07-31/ANGULAR_MAP.md", 164, 175, "Torus-first", (2,)),
        ("kill_scope", "udt_p4_angular_map_2026-07-31/ANGULAR_MAP.md", 64, 82, "THE BANKED KILLS", (3,)),
        ("premise_rows", "udt_p4_angular_map_2026-07-31/ANGULAR_MAP.md", 88, 125, "A-L1. The angular-extended presentation", (4,)),
        ("a3_pose", "udt_p4_angular_map_2026-07-31/ANGULAR_MAP.md", 131, 149, "THE WINDING/CYCLE CENSUS ANGULAR-LIVE", (5,)),
    ],
    "P4-26": [
        ("metric_opening", "udt_p4_angular_stage_A1_2026-07-31/EXACT_DERIVATION.md", 20, 60, "The x-angular mixed row", (1, 2, 3, 4)),
        ("residual_group", "udt_p4_angular_stage_A1_2026-07-31/EXACT_DERIVATION.md", 82, 140, "K₄ SURVIVES VERBATIM", (5, 6, 7)),
        ("spatial_fork", "udt_p4_angular_stage_A1_2026-07-31/EXACT_DERIVATION.md", 158, 170, "irreducibility rides the NEW spatial-reading fork", (8, 9)),
        ("requirements", "udt_p4_angular_stage_A1_2026-07-31/EXACT_DERIVATION.md", 173, 230, "the requirement set re-posed (R1–R15", (10,)),
        ("controls_and_registry", "udt_p4_angular_stage_A1_2026-07-31/EXACT_DERIVATION.md", 286, 313, "10 → 17 candidate entries", (11, 12, 13)),
    ],
    "P4-27": [
        ("pointwise_scope", "udt_p4_angular_stage_A2_2026-07-31/AUDIT_REPORT.md", 158, 178, "ℛ_PW^A parametrized per branch × mode", (1,)),
        ("forcing_and_rm", "udt_p4_angular_stage_A2_2026-07-31/AUDIT_REPORT.md", 64, 81, "φ-forcing mode-uniformity", (2, 3, 9)),
        ("mode_uniform_module", "udt_p4_angular_stage_A2_2026-07-31/EXACT_DERIVATION.md", 179, 197, "surviving space is MODE-UNIFORM", (4, 8)),
        ("mode_zero_embedding", "udt_p4_angular_stage_A2_2026-07-31/EXACT_DERIVATION.md", 201, 212, "EMBEDS EXACTLY as the mode-zero stratum", (5,)),
        ("angular_identity", "udt_p4_angular_stage_A2_2026-07-31/EXACT_DERIVATION.md", 240, 252, "The k_mod = 0 identity EXTENDS VERBATIM", (6, 7)),
        ("controls", "udt_p4_angular_stage_A2_2026-07-31/AUDIT_REPORT.md", 90, 93, "C-1 PASS, C-2 PASS", (10,)),
    ],
    "P4-28": [
        ("mixed_verdict", "udt_p4_angular_stage_A3_2026-07-31/AUDIT_REPORT.md", 15, 27, "OB3-3 MIXED-BY-KIND", (1, 5, 6, 7)),
        ("verified_status", "udt_p4_angular_stage_A3_2026-07-31/AUDIT_REPORT.md", 3, 13, "VERIFIED-WITH-CAVEATS", (2, 3)),
        ("massive_carriers", "udt_p4_angular_stage_A3_2026-07-31/AUDIT_REPORT.md", 29, 34, "Neither gains a variable native integer", (8, 9, 10)),
        ("smooth_scope", "udt_p4_angular_stage_A3_2026-07-31/AUDIT_REPORT.md", 154, 166, "The full frozen smooth regular scope was run", (4,)),
    ],
}


CROSS_SOURCE_ANCHORS = {
    "Q1": ("P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md", 31, 32, "silently choose a response alphabet"),
    "Q2": ("P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md", 33, 34, "quantifier change from a formal family"),
    "Q3": ("P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md", 35, 36, "complete premise stacks"),
    "Q4": ("P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md", 37, 38, "chosen topology/transition class"),
    "Q5": ("P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md", 39, 40, "without steering toward integers"),
    "Q6": ("P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md", 41, 42, "physically distinguishable"),
    "Q7": ("P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md", 43, 44, "different-method recomputation"),
    "Q8": ("P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md", 45, 46, "conditional identifications"),
    "D-001": ("udt_p4_cold_adversarial_review_2026-08-01/TRANSITIVE_DEPENDENCY_OVERLAY.tsv", 1, 14, "NON_RETROACTIVE_POST_OUTCOME_DEPENDENCY_RECORD"),
    "D-002": ("P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md", 10, 13, "shared framing, vocabulary, or code lineage"),
}


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, delimiter="\t", fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def completeness_cells(uid: str, scope: str, limit: str) -> dict[str, str]:
    """Ten contract-required completeness cells, repeated on every exploded claim."""
    fields_by_arc = {
        "P4-00": "maps phi/coframe/moduli/boundary/completion choices; selects none",
        "P4-01": "E02 generator H,C,K and moduli lambda,k_mod,k10,C",
        "P4-02": "u,alpha,A,q_B on CHOSE stationary metric family",
        "P4-03": "16 objects including fields plus anchors/forks/gauge/chart labels",
        "P4-04": "no UDT field census; reference-map rows only",
        "P4-05": "stationary response slots through jet order 2",
        "P4-06": "R_PW survivors; deeper resonance fields not exhausted",
        "P4-07": "quadratic p0/w slice and integrated moduli rows",
        "P4-08": "full cell profiles within declared response class",
        "P4-09": "constant versus promoted moduli tangent directions",
        "P4-10": "promoted lambda,k_mod,k10,C fields and local jets",
        "P4-11": "seal-dressed moduli and pairing branches",
        "P4-12": "promoted moduli jets plus p,f,bh rows",
        "P4-13": "screen/fold completion data and response rows",
        "P4-14": "no new fields; premise provenance only",
        "P4-15": "phi,rho seam germs on stationary branches",
        "P4-16": "phi,rho and first wall germs B_Q,B_rho",
        "P4-17": "banked response fields, moduli, wall germs on completion cycles",
        "P4-18": "reduced perturbations v_p,v_f,v_h,v_lambda and wall germs",
        "P4-19": "owned U1 transition/circle structures plus proposed S1 field theta",
        "P4-20": "IF-ADOPTED theta blocks/jets coupled to banked response alphabet",
        "P4-21": "maps lapse/shift/time topology fields; selects none",
        "P4-22": "time-live phi,f,bh,N_i,moduli,boundary slots",
        "P4-23": "time-live pointwise response slots including three R_N",
        "P4-24": "native time cycles plus IF-ADOPTED theta time dependence",
        "P4-25": "maps angular fields/modes/mix rows; selects none",
        "P4-26": "angular-live covariant metric rows including N_i and m_y,m_z",
        "P4-27": "angular-live response slots including R_N,R_m and tri-graded jets",
        "P4-28": "smooth regular native metric/response targets; theta absent",
    }
    eq_by_arc = {
        "P4-00": "none solved; inverse problem framed",
        "P4-01": "pointwise equivariance, commutators, cocycles",
        "P4-02": "restricted vacuum Bach and EH+Lambda component equation sets",
        "P4-03": "R1-R15 conditions posed; no response equations solved",
        "P4-04": "no equations adjudicated; import map",
        "P4-05": "pointwise equivariance/Noether cuts; no whole-solution equations",
        "P4-06": "gate predicates on R_PW; resonance ideals incomplete",
        "P4-07": "reduced quadratic ODE/integrated row",
        "P4-08": "cell energy ODE and branch-definition integrals",
        "P4-09": "pairing/tangent localization theorem",
        "P4-10": "class connection/cocycle/alphabet registration, not response solve",
        "P4-11": "mirror parity equations on named ladders",
        "P4-12": "pointwise moduli-row forcing on named class",
        "P4-13": "conditional involution/selector equations",
        "P4-14": "provenance comparisons; no new field equations",
        "P4-15": "seam handshake, ODE uniqueness on Branch-G locus",
        "P4-16": "first-variation wall jump/natural-boundary equations",
        "P4-17": "real period and holonomy equations",
        "P4-18": "reduced second-variation operators and 2x2 mode blocks",
        "P4-19": "topology/target kernels and registration laws",
        "P4-20": "conditional theta response/menu and period equations",
        "P4-21": "none solved; time-live program framed",
        "P4-22": "posing identities and metric transformations, not response solve",
        "P4-23": "pointwise module/Noether equations; integration identity typed only",
        "P4-24": "cycle/period census; kinematic, no dynamics",
        "P4-25": "none solved; angular program framed",
        "P4-26": "metric transformation/posing identities, not response solve",
        "P4-27": "pointwise module/Noether identities; integration closure absent",
        "P4-28": "topological/target contraction census; no on-shell equations",
    }
    boundary_live = uid in {"P4-07", "P4-08", "P4-11", "P4-12", "P4-13", "P4-15", "P4-16", "P4-17", "P4-18", "P4-20", "P4-24", "P4-28"}
    topology_live = uid in {"P4-13", "P4-14", "P4-15", "P4-16", "P4-17", "P4-19", "P4-20", "P4-21", "P4-24", "P4-25", "P4-26", "P4-27", "P4-28"}
    stability_live = uid == "P4-18"
    return {
        "fields_covered_or_dropped": fields_by_arc[uid],
        "action_terms_covered_or_dropped": ACTION_CELLS.get(uid, "no action selected; no action term is used in this clause set"),
        "equations_covered_or_dropped": eq_by_arc[uid],
        "domain_covered_or_dropped": scope,
        "boundary_covered_or_dropped": "named N=2/seam/completion boundary data carried" if boundary_live else "boundary/corner realization not adjudicated",
        "topology_covered_or_dropped": "named registered completion/topology branches carried; exotic/unregistered classes open" if topology_live else "global topology/completion not adjudicated",
        "dynamical_character_covered_or_dropped": "off-shell/pointwise or kinematic; no physical time evolution or on-shell dynamics",
        "branches_covered_or_dropped": "declared census/pairing/posture/reading branches carried; no branch adopted",
        "stability_covered_or_dropped": "reduced second-variation sectors only; joint/dynamical stability open" if stability_live else "stability not tested in this unit",
        "regime_and_limits": limit,
    }


def clause_condition_profile(uid: str, clause: str) -> str:
    fields = []
    lowered = clause.lower()
    for category, triggers in CONDITION_TRIGGERS.items():
        active = any(trigger.lower() in lowered for trigger in triggers)
        value = CONDITION_VALUES.get(category, {}).get(uid)
        if active:
            if not value:
                raise RuntimeError(f"{uid}: missing curated {category} premise for clause {clause!r}")
            fields.append(f"{category}={value}")
        else:
            fields.append(f"{category}=NOT_LOAD_BEARING_FOR_THIS_CLAUSE")
    fields.append(f"ACTION_FIELD_ADOPTION_STATUS=all DERIVED/CHOSE/OPEN/CONDITIONAL/POSIT labels retained; no action, field, carrier, mass, coupling, dynamics or physics adopted; excluded={META[uid][2]}")
    return "; ".join(fields)


def source_excerpt_fields(uid: str, clause_index: int) -> dict[str, str]:
    matches = []
    for group, path, start, end, token, indices in PACKAGE_SOURCE_ANCHORS[uid]:
        if clause_index in indices:
            matches.append((group, path, start, end, token))
    if len(matches) != 1:
        raise RuntimeError(f"{uid} clause {clause_index}: expected one curated source anchor, got {len(matches)}")
    group, path, start, end, token = matches[0]
    source = ROOT / path
    lines = source.read_bytes().splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        raise RuntimeError(f"{uid}:{group}: invalid source range {start}-{end} for {path}")
    excerpt = b"".join(lines[start - 1:end])
    if token.encode("utf-8") not in excerpt:
        raise RuntimeError(f"{uid}:{group}: exact anchor token absent from curated excerpt: {token!r}")
    digest = hashlib.sha256(excerpt).hexdigest()
    return {
        "source_path": path,
        "source_start_line": str(start),
        "source_end_line": str(end),
        "source_anchor_token": token,
        "source_excerpt_sha256": digest,
        "shared_source_premise_id": f"{uid}:{group}",
        "source_provenance_class": "PREREGISTERED_SOURCE_INVENTORY",
        "source_stamp_id": f"{uid}:{group}:{digest[:12]}",
    }


def cross_source_excerpt_fields(uid: str) -> dict[str, str]:
    path, start, end, token = CROSS_SOURCE_ANCHORS[uid]
    source = ROOT / path
    lines = source.read_bytes().splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        raise RuntimeError(f"{uid}: invalid source range {start}-{end} for {path}")
    excerpt = b"".join(lines[start - 1:end])
    if token.encode("utf-8") not in excerpt:
        raise RuntimeError(f"{uid}: exact anchor token absent from curated excerpt: {token!r}")
    digest = hashlib.sha256(excerpt).hexdigest()
    provenance = "NON_RETROACTIVE_REVIEW_OVERLAY" if uid == "D-001" else "PREREGISTERED_SOURCE_INVENTORY"
    return {
        "source_path": path,
        "source_start_line": str(start),
        "source_end_line": str(end),
        "source_anchor_token": token,
        "source_excerpt_sha256": digest,
        "shared_source_premise_id": f"{uid}:governing_anchor",
        "source_provenance_class": provenance,
        "source_stamp_id": f"{uid}:governing_anchor:{digest[:12]}",
    }


def clause_premise(uid: str, clause: str, quant: str) -> tuple[str, str, str]:
    condition_profile = clause_condition_profile(uid, clause)
    stack = f"SCOPE={PREMISE_DETAIL[uid]}; {condition_profile}; QUANTIFIER={quant}"
    semantic_id = "SEM:" + hashlib.sha256(stack.encode("utf-8")).hexdigest()[:16]
    required = "||".join((
        "SCOPE=",
        "SIGN=", "POSITIVITY=", "NORMALIZATION=", "BRANCH=", "BOUNDARY_GERM=", "PAIRING=", "POSTURE=", "TOPOLOGY=",
        "ACTION_FIELD_ADOPTION_STATUS=", f"QUANTIFIER={quant}",
    ))
    return semantic_id, stack, required


def build_claims() -> list[dict[str, str]]:
    frozen = {r["unit_id"]: r for r in csv.DictReader((OUT / "FROZEN_REVIEW_UNITS.tsv").open(), delimiter="\t")}
    rows: list[dict[str, str]] = []
    seq = 0
    for uid in [f"P4-{i:02d}" for i in range(29)]:
        scope, quant, limit, evidence = META[uid]
        for clause_index, clause in enumerate(CLAIMS[uid], start=1):
            seq += 1
            grade = "RETAINED" if clause in RETAIN_IF.get(uid, set()) else "NARROWED"
            replacement = (
                f"Within {scope}, the clause is retained: {clause}; it does not establish {limit}."
                if grade == "RETAINED"
                else f"The evidence supports '{clause}' only within {scope}; it does not establish {limit}."
            )
            if uid == "P4-19" and clause == "K4 itself equals the real points of the screen U1":
                grade = "CONTRADICTED"
                replacement = "The source proves only that the screen-character image {+1,-1} is the real two-torsion of U(1); the order-four K4 group itself does not embed in that circle."
            semantic_premise_id, premise_stack, required_premise_tokens = clause_premise(uid, clause, quant)
            source_fields = source_excerpt_fields(uid, clause_index)
            row = {
                "claim_id": f"MC-{seq:03d}", "unit_id": uid, "package": frozen[uid]["package"],
                "unit_kind": "PACKAGE_HEADLINE_CLAUSE", "source_clause": clause,
                "semantic_premise_id": semantic_premise_id, "required_premise_tokens": required_premise_tokens,
                "premise_stack": premise_stack, "quantifier_guard": quant, "regrade": grade,
                "replacement_sentence": replacement, "evidence": evidence,
                "completeness_limit": limit, "falsifier_disposition": "NO_F1_F2_F10; scope controlled under F3-F9",
            }
            row.update(source_fields)
            row.update(completeness_cells(uid, scope, limit))
            rows.append(row)
    for uid, question, grade, answer, quant in QROWS:
        seq += 1
        premise_stack = "all 29 P4 packages plus frozen controls"
        row = {
            "claim_id": f"MC-{seq:03d}", "unit_id": uid, "package": "P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md",
            "unit_kind": "CROSS_CUTTING_QUESTION", "source_clause": question,
            "semantic_premise_id": "SEM:" + hashlib.sha256(premise_stack.encode()).hexdigest()[:16],
            "required_premise_tokens": "all 29 P4 packages||frozen controls",
            "premise_stack": premise_stack,
            "quantifier_guard": quant, "regrade": grade, "replacement_sentence": answer,
            "evidence": "MECHANICAL_CLAIM_REGRADES.tsv; INDEPENDENT_RECOMPUTATION_LEDGER.tsv; SHARED_CODE_CIRCULARITY_MAP.tsv",
            "completeness_limit": "maximum is evidence regrade; no new physics", "falsifier_disposition": "cross-cutting adjudication",
        }
        row.update(cross_source_excerpt_fields(uid))
        row.update({
            "fields_covered_or_dropped": "cross-cutting audit of declared fields; no field adopted",
            "action_terms_covered_or_dropped": "all actions remain conditional/unselected",
            "equations_covered_or_dropped": "selected algebra recomputed; unrun integration/on-shell equations remain open",
            "domain_covered_or_dropped": "all frozen package domains compared without merging them",
            "boundary_covered_or_dropped": "posture and N=2 limits kept explicit",
            "topology_covered_or_dropped": "real/circle/torus/S3 distinctions kept explicit",
            "dynamical_character_covered_or_dropped": "formal, off-shell, kinematic, and dynamical claims separated",
            "branches_covered_or_dropped": "all named census/pairing/posture/reading branches retained",
            "stability_covered_or_dropped": "sector Hessian claims separated from physical/dynamical stability",
            "regime_and_limits": "maximum is evidence regrade; no new physics",
        })
        rows.append(row)
    discoveries = [
        ("D-001", "The frozen 311-source inventory is transitively complete for every load-bearing dependency.", "NARROWED", "It freezes every package byte, but direct cited dependencies such as TORIC_CAP_ENUMERATION.tsv and JOINT_OPERATION_OBLIGATIONS.tsv are outside the 311 rows; their current base bytes were read and separately hashed, so transitive source closure is not manifest-complete."),
        ("D-002", "Every banked package is independently verified in the strong later-context sense.", "NARROWED", "Most packages have separate verifier scripts and adversarial amendments, but the records explicitly say same-session-spawned and not hosted-external; they are useful partial independence, not this later cold review's independence grade."),
    ]
    for did, clause, grade, replacement in discoveries:
        seq += 1
        premise_stack = "cold-review provenance and completeness layer"
        row = {
            "claim_id": f"MC-{seq:03d}", "unit_id": did, "package": "DISCOVERED_LOAD_BEARING_CLAIM",
            "unit_kind": "DISCOVERED_LOAD_BEARING_CLAIM", "source_clause": clause,
            "semantic_premise_id": "SEM:" + hashlib.sha256(premise_stack.encode()).hexdigest()[:16],
            "required_premise_tokens": "cold-review provenance||completeness layer",
            "premise_stack": premise_stack,
            "quantifier_guard": "TRANSITIVE_DEPENDENCY_AND_ON_SHELL_SCOPE", "regrade": grade,
            "replacement_sentence": replacement, "evidence": "INDEPENDENT_RECOMPUTATION_RAW.jsonl; SOURCE_INVENTORY.tsv; A3 EXACT_DERIVATION.md",
            "completeness_limit": "review cannot promote absent transitive freeze or absent solutions", "falsifier_disposition": "F3/F5/F8 caught and scoped",
        }
        row.update(cross_source_excerpt_fields(did))
        row.update({
            "fields_covered_or_dropped": "dependency/provenance claim; no field result",
            "action_terms_covered_or_dropped": "none",
            "equations_covered_or_dropped": "source closure/independence only",
            "domain_covered_or_dropped": "frozen source universe versus direct cited dependencies",
            "boundary_covered_or_dropped": "not applicable",
            "topology_covered_or_dropped": "cap dependency included only as direct citation",
            "dynamical_character_covered_or_dropped": "not applicable",
            "branches_covered_or_dropped": "no branch adoption",
            "stability_covered_or_dropped": "not applicable",
            "regime_and_limits": "review cannot promote incomplete transitive freeze",
        })
        rows.append(row)
    return rows


def build_premise_audit(claims: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    frozen = list(csv.DictReader((OUT / "FROZEN_REVIEW_UNITS.tsv").open(), delimiter="\t"))
    for unit in frozen:
        uid = unit["unit_id"]
        subset = [r for r in claims if r["unit_id"] == uid]
        if uid.startswith("P4-"):
            scope, quant, limit, evidence = META[uid]
            labels = "DERIVED/CHOSE/OPEN/CONDITIONAL carried from package; no label promoted"
        else:
            q = next(x for x in QROWS if x[0] == uid)
            scope, quant, limit, evidence = "all frozen packages", q[4], q[3], "cross-cutting ledgers"
            labels = "cross-cutting regrade only"
        rows.append({
            "unit_id": uid, "package": unit["package"], "exploded_claim_count": str(len(subset)),
            "clause_source_stamp_count": str(sum(bool(r.get("source_stamp_id")) for r in subset)),
            "source_anchor_group_count": str(len({r.get("shared_source_premise_id", "") for r in subset})),
            "semantic_premise_profile_count": str(len({r.get("semantic_premise_id", "") for r in subset})),
            "clause_source_stamps": "|".join(r.get("source_stamp_id", "") for r in subset),
            "shared_source_premise_ids": "|".join(sorted({r.get("shared_source_premise_id", "") for r in subset})),
            "semantic_premise_ids": "|".join(sorted({r.get("semantic_premise_id", "") for r in subset})),
            "source_anchor_ranges": "|".join(sorted({f"{r.get('source_path', '')}:{r.get('source_start_line', '')}-{r.get('source_end_line', '')}" for r in subset})),
            "domain_and_premises": scope, "quantifier_guard": quant, "epistemic_labels": labels,
            "excluded_or_open_scope": limit, "primary_evidence": "machine-local ranges in source_anchor_ranges",
            "audit_result": "PASS_SOURCE_LOCAL_ANCHORED_WITH_LEGITIMATE_SHARED_GROUPS" if subset and all(r.get("source_excerpt_sha256") for r in subset) else "FAIL_MISSING_SOURCE_LOCAL_ANCHOR",
        })
    return rows


def build_recompute_ledger() -> list[dict[str, str]]:
    rows = []
    for line in (OUT / "INDEPENDENT_RECOMPUTATION_RAW.jsonl").read_text().splitlines():
        obj = json.loads(line)
        if "record_id" not in obj:
            continue
        method = obj["method"]
        parser_or_regression = {"IR03", "IR06", "IR10", "IR15", "IR19", "IR20"}
        grade = "INDEPENDENT_PARSER_OR_REGRESSION" if obj["record_id"] in parser_or_regression else "GENUINELY_DIFFERENT_METHOD"
        rows.append({
            "record_id": obj["record_id"], "cluster": obj["cluster"], "independence_label": grade,
            "method_or_command": f"python3 {OUT.name}/independent_recompute.py :: {method}",
            "status": obj["status"], "residual_or_count": obj["residual"], "evidence_and_limit": obj["evidence"],
            "raw_output": "INDEPENDENT_RECOMPUTATION_RAW.jsonl",
        })
    return rows


def build_dependency_overlay() -> list[dict[str, str]]:
    second = json.loads((OUT / "SECOND_VERIFIER_RESULTS.json").read_text())
    overlay = second["source_freeze"]["overlay"]
    if {entry["path"] for entry in overlay} != set(OVERLAY_CLASS):
        raise RuntimeError("second-verifier overlay path set changed")
    rows = []
    for entry in overlay:
        rows.append({
            "overlay_date": "2026-08-01",
            "overlay_status": "NON_RETROACTIVE_POST_OUTCOME_DEPENDENCY_RECORD",
            "path": entry["path"],
            "sha256": entry["sha256"],
            "base_sha256": entry["base_sha256"],
            "base_byte_identical": str(entry["base_byte_identical"]).upper(),
            "cited_by_count": str(entry["cited_by_count"]),
            "cited_by": "|".join(entry["cited_by"]),
            "classification": OVERLAY_CLASS[entry["path"]],
            "classification_reason": (
                "directly controls a checked premise, algebra input, or source-ledger row"
                if OVERLAY_CLASS[entry["path"]] == "LOAD_BEARING"
                else "provenance or contextual support; not used as a cold load-bearing algebra input"
            ),
        })
    return rows


def build_shared_map() -> list[dict[str, str]]:
    frozen = {r["unit_id"]: r for r in csv.DictReader((OUT / "FROZEN_REVIEW_UNITS.tsv").open(), delimiter="\t")}
    map_only = {"P4-00", "P4-04", "P4-14", "P4-21", "P4-25"}
    high_parser = {"P4-03", "P4-05", "P4-22", "P4-23", "P4-24", "P4-26", "P4-27", "P4-28"}
    rows = []
    for i in range(29):
        uid = f"P4-{i:02d}"
        pkg = frozen[uid]["package"]
        if uid in map_only:
            grade = "MAP_OR_PROVENANCE_ONLY"
            risk = "No independent algebra is implied by the package headline."
            verifier = "none or document/provenance audit"
        elif uid in high_parser:
            grade = "PARTIAL_INDEPENDENCE_PLUS_PARSER_REPLAY"
            risk = "Separate script, but shared conventions/source tuples/generated schemas; recovery/count controls are not independent algebra."
            verifier = "in-package VERIFIER_* script(s), same-session record"
        else:
            grade = "PARTIAL_DIFFERENT_IMPLEMENTATION"
            risk = "Separate symbolic construction, yet identical source premises and same-session context; no external model/method family."
            verifier = "in-package VERIFIER_INDEPENDENT_CHECK.py, same-session record"
        rows.append({
            "unit_id": uid, "package": pkg, "producer": "derive_*.py or source document",
            "verifier": verifier, "shared_inputs": "package preregistration; banked conventions; cited source tuples",
            "shared_expressions_or_parsers": "same mathematical identities; JSON/TSV schemas; producer replay where recorded",
            "independence_grade": grade, "circularity_risk": risk,
            "cold_review_disposition": "Cold script recomputed selected mandatory clusters; un-recomputed clauses remain premise-scoped, not upgraded.",
        })
    rows.extend([
        {"unit_id": "X-SHARED-01", "package": "static response chain P4-03/05/06/22/23/27", "producer": "successive inheritance", "verifier": "successive in-package scripts", "shared_inputs": "same 16-object census and R1-R15 definitions", "shared_expressions_or_parsers": "same K4 characters and k_mod=0 identity", "independence_grade": "DEPENDENT_CHAIN_WITH_LOCAL_RECOMPUTATIONS", "circularity_risk": "Exact embedding can mean schema equality rather than existence of a fixed realized solution.", "cold_review_disposition": "NARROWED to formal pointwise module embedding."},
        {"unit_id": "X-SHARED-02", "package": "mass/stability chain P4-07/08/17/18/20/24/28", "producer": "mass definitions inherited downstream", "verifier": "package-local", "shared_inputs": "quadratic atlas; pairing/census/posture; labeled mass definitions", "shared_expressions_or_parsers": "E0, ell, I_p, M-GEN/M-WALL", "independence_grade": "DEPENDENT_PREMISE_CHAIN", "circularity_risk": "A downstream survival claim cannot establish physical mass ownership.", "cold_review_disposition": "NARROWED to conditional definitions and reduced sectors."},
        {"unit_id": "X-SHARED-03", "package": "A3 cap dependency", "producer": "A3 parser over TORIC_CAP_ENUMERATION.tsv", "verifier": "A3 verifier parses same upstream table", "shared_inputs": "104 upstream cap-vector rows", "shared_expressions_or_parsers": "determinant and primitivity", "independence_grade": "ALGEBRA_INDEPENDENT_BUT_DATA_SHARED", "circularity_risk": "The upstream cap file is direct-cited but absent from the 311-row source freeze.", "cold_review_disposition": "104/104 recomputed from base bytes; transitive-freeze gap reported."},
        {"unit_id": "X-SHARED-04", "package": "A3 C1 recovery", "producer": "20-row period ledger", "verifier": "field-digest reconstruction", "shared_inputs": "same period ledger", "shared_expressions_or_parsers": "120 field digests", "independence_grade": "PARSER_COPY_CHECK_ONLY", "circularity_risk": "Proves faithful recovery, not the period algebra itself.", "cold_review_disposition": "Labeled regression; real/circle algebra recomputed separately."},
    ])
    return rows


def main() -> None:
    for uid, clauses in CLAIMS.items():
        anchored = [idx for _, _, _, _, _, indices in PACKAGE_SOURCE_ANCHORS[uid] for idx in indices]
        if sorted(anchored) != list(range(1, len(clauses) + 1)) or len(anchored) != len(set(anchored)):
            raise RuntimeError(f"{uid}: curated anchor coverage is not exact: {anchored}")
    overlay = build_dependency_overlay()
    write_tsv(OUT / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv", overlay, list(overlay[0]))
    claims = build_claims()
    write_tsv(OUT / "MECHANICAL_CLAIM_REGRADES.tsv", claims, list(claims[0]))
    premise = build_premise_audit(claims)
    write_tsv(OUT / "PREMISE_QUANTIFIER_AUDIT.tsv", premise, list(premise[0]))
    recompute = build_recompute_ledger()
    write_tsv(OUT / "INDEPENDENT_RECOMPUTATION_LEDGER.tsv", recompute, list(recompute[0]))
    shared = build_shared_map()
    write_tsv(OUT / "SHARED_CODE_CIRCULARITY_MAP.tsv", shared, list(shared[0]))
    counts = Counter(r["regrade"] for r in claims)
    package_counts = {f"P4-{i:02d}": sum(r["unit_id"] == f"P4-{i:02d}" for r in claims) for i in range(29)}
    package_claims = [r for r in claims if r["unit_kind"] == "PACKAGE_HEADLINE_CLAUSE"]
    anchor_sizes = Counter(r["shared_source_premise_id"] for r in package_claims)
    result = {
        "review_base": "2e93a621aeeee0a0844543068363d0ba94094357",
        "review_units": 37,
        "source_inventory_rows": 311,
        "mechanical_claim_rows": len(claims),
        "regrades": dict(sorted(counts.items())),
        "package_claim_counts": package_counts,
        "cross_cutting_units_covered": 8,
        "discovered_claims": 2,
        "independent_recomputations": {
            "total": len(recompute), "passed": sum(r["status"] == "PASS" for r in recompute),
            "genuinely_different_method": sum(r["independence_label"] == "GENUINELY_DIFFERENT_METHOD" for r in recompute),
            "independent_parser_or_regression": sum(r["independence_label"] == "INDEPENDENT_PARSER_OR_REGRESSION" for r in recompute),
            "q2_footing": "banked package controls plus cold parser regression; not a cold different-method proof",
        },
        "amendment_status": "PRIMARY_SOURCE_LOCAL_ANCHOR_AMENDMENT_PENDING_SAME_SECOND_VERIFIER_CLOSURE",
        "source_local_premise_anchors": {
            "package_clause_rows": len(package_claims),
            "anchored_package_clause_rows": sum(bool(r["source_excerpt_sha256"]) for r in package_claims),
            "source_anchor_groups": len(anchor_sizes),
            "legitimate_shared_anchor_groups": sum(size > 1 for size in anchor_sizes.values()),
            "single_clause_anchor_groups": sum(size == 1 for size in anchor_sizes.values()),
            "semantic_premise_profiles": len({r["semantic_premise_id"] for r in package_claims}),
            "note": "Counts are semantic/source-anchor counts; no uniqueness claim is manufactured from claim IDs or row indices.",
        },
        "completeness_validation": {"cells_per_claim": 10, "claim_rows": len(claims), "action_bearing_rows_corrected": 26},
        "transitive_dependency_overlay": {
            "date": "2026-08-01", "status": "NON_RETROACTIVE", "rows": len(overlay),
            "load_bearing": sum(r["classification"] == "LOAD_BEARING" for r in overlay),
            "supporting": sum(r["classification"] == "SUPPORTING" for r in overlay),
        },
        "falsifier_events": {
            "F1": 0, "F2": 0, "F3": "caught_scope_narrowings", "F4": "formal_vs_realized_embedding_caught",
            "F5": "parser/replay relabeled", "F6": "mass definitions kept conditional", "F7": "K4/U1 overstatement contradicted",
            "F8": "all ten criteria mapped", "F9": "nuclear remains CONSISTENCY-DEMO", "F10": 0,
        },
        "maximum_conclusion": "Accumulated P4 algebra survives selected different-method checks, but the arc must be read as a premise-scoped formal response/census chain; one headline group-identification is contradicted and broad architecture/mass/embedding/completeness wording is narrowed.",
        "smallest_next_step": "STOP_REPAIR_FIRST: freeze transitive load-bearing dependencies and replace the K4=real-points headline before any adoption/T4; then rerun the cold verifier on the repaired review package.",
    }
    (OUT / "REVIEW_RESULTS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"claims": len(claims), "package_anchors": len(package_claims), "anchor_groups": len(anchor_sizes), "semantic_profiles": len({r["semantic_premise_id"] for r in package_claims}), "regrades": counts, "premise_rows": len(premise), "recomputations": len(recompute), "shared_rows": len(shared), "overlay_rows": len(overlay)}, default=dict, sort_keys=True))


if __name__ == "__main__":
    main()
