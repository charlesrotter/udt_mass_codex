#!/usr/bin/env python3
"""
solver_action.py -- THE SINGLE SOURCE-OF-TRUTH ACTION for the live solver (P2 of
SOLVER_INTEGRITY_UPGRADES_SPEC).  This module names EVERY term the operator implements,
its weight, its PROVENANCE, and the live code that realizes it -- in one place, so the
operator stops being a pile of hand-coded pieces where imports crept in.

*** SCOPE (Charles decision 2026-06-23): this is the a=-1 GR-BASELINE action that the
LIVE operator actually realizes -- NOT the derived e^{2phi}/a(phi)=e^{phi} theory. ***
The DERIVED action is wired at MIGRATION (the step that picks the curvature Branch G/P
fork, settles the matter weight, and swaps a(phi)=e^{phi} in); those open items are
recorded below as MIGRATION-DEFERRED and are tripwired by the P1 documented-gap xfails.

THE GR-BASELINE ACTION (DATA-BLIND; units L=sqrt(kappa/xi)=1):

    S = integral sqrt(-g) [ (1/(2 kap8)) R  +  L_m ]  d^4x ,   L_m = L2 + L4

  Euler-Lagrange:
    delta S / delta g^{mu nu} = 0   ->   G_{mu nu} = kap8 T_{mu nu}   (the field eqn the
        residual assembles: resE = G^mu_nu - kap8 T^mu_nu)
    delta S / delta Theta      = 0   ->   the matter field EOM (the sympy codegen matter_el_3d)

  WHAT P2 PROVES (machine precision) vs CHECKS (consistency):
    * matter STRESS T_{mu nu} == the exact Hilbert variation of L_m            [PROVEN, ~1e-15]
    * gravity G^mu_nu: two independent analytic engines agree (no drift);
        correctness vs truth anchored by P1 (de Sitter G=-Lam, Schwarzschild)  [PROVEN no-drift]
    * matter FIELD-EOM matter_el_3d (strong) == -autograd(action) (weak)       [CONSISTENCY ~0.4%,
        two routes converge with resolution; catches the codegen-bug class, NOT machine-precise]
    * residual assembles G - kap8 T with the production weight                 [REGRESSION LOCK]

PROVENANCE SPINE (shared with the P1 harness): this file REFERENCES the derivations; it
does not RE-ASSERT their numeric results.  Values (kap8, a(phi), xi, kap) are SOURCED
here from the live code / flagged FREE -- never hard-coded as a derived truth in a test.
"""

# ===========================================================================
# THE ACTION-TERM REGISTRY.  Every term: its weight, operator implementation, and a
# provenance TAG (DERIVED | FREE | IMPORTED | MIGRATION-DEFERRED) with evidence.  The
# P2 lint asserts every term carries a tag; the equality tests assert the live operator
# == the EL of these terms.
# ===========================================================================
ACTION_TERMS = [
    dict(
        name="gravity_curvature",
        symbol="(1/(2 kap8)) R",
        weight="1 (GR-baseline; a=-1)",
        tag="DERIVED",                     # the EL of sqrt(-g) R is the Einstein tensor G_{mu nu}
        operator="einstein_mixed_general / einstein_mixed_weyl (G^mu_nu)",
        evidence="EL of sqrt(-g)R = G_{mu nu} (textbook EH identity); the analytic engine is "
                 "machine-exact vs sympy (Stage-1) and exact on de Sitter/Schwarzschild (P1).",
        migration_note="DERIVED-THEORY weight is e^{2phi} on the GRADIENT-sector curvature ONLY; "
                       "the ANGULAR curvature refuses it -> Branch G/P fork UNRESOLVED (= the "
                       "phi-angular tension). MIGRATION resolves the fork. Tripwire: P1 "
                       "test_derived_a_phi_in_operator.",
    ),
    dict(
        name="matter_L2",
        symbol="-(xi/2) g^{ab} D_a n . D_b n",
        weight="1 (no metric weight; sqrt(-g) carries the geometry)",
        tag="DERIVED",                     # unique 2-derivative diffeo+SO(3) scalar (F2)
        operator="whole_metric_3d_matter.lagrangian L2 -> stress_tensor",
        evidence="F2_matter_action_forcedness: L2 is the UNIQUE 2-derivative diffeo+SO(3) scalar.",
        migration_note=None,
    ),
    dict(
        name="matter_L4",
        symbol="-(kap/4) |omega_H1|^2  (area-form / Skyrme stabilizer)",
        weight="1 (no metric weight)",
        tag="DERIVED",                     # native H1 area-form term (CANON C-2026-06-14-1)
        operator="whole_metric_3d_matter.lagrangian L4 -> stress_tensor",
        evidence="F2: a 4-derivative stabilizer is FORCED PRESENT by Derrick; the H1 area-form "
                 "natively privileges L4=|omega_H1|^2. CANON C-2026-06-14-1.",
        migration_note="MINIMAL-BUT-NOT-UNIQUE: the orthogonal 4-deriv invariant X^2 and the "
                       "6-deriv L6 are ADMISSIBLE (off by default). Switchable, tagged FREE.",
    ),
    dict(
        name="matter_couplings_xi_kap",
        symbol="xi, kap",
        weight="xi=kap=1.0 (live baseline)",
        tag="FREE",                        # F2: not fixed by principle; sourced at migration
        operator="stress_tensor(g, ginv, dn, xi=1.0, kap=1.0)",
        evidence="F2: the matter couplings are not fixed by the forcing principles; they only "
                 "move masses. Live baseline xi=kap=1 (units L=sqrt(kap/xi)=1).",
        migration_note="value SOURCED at migration; P1 test_matter_couplings_tagged tripwires the "
                       "untagged 1.0 in the live stress call.",
    ),
    dict(
        name="einstein_coupling_kap8",
        symbol="kap8  (in G = kap8 T)",
        weight="free dial (live callers pass 0.05)",
        tag="FREE",
        operator="residual_vector_p1(..., kap8=...)",
        evidence="kap8 enters as the gravity-matter coupling; round-gate DERIVED kap8=1 but the "
                 "live callers still pass 0.05 (un-migrated). P1 test_kap8_callers_tagged tripwires it.",
        migration_note="value SOURCED at migration (DERIVED kap8=1).",
    ),
    # ---- MIGRATION-DEFERRED terms (NOT in the GR-baseline operator; recorded so they are not
    # silently smuggled in to make a test pass) ----
    dict(
        name="dilaton_kinetic",
        symbol="X e^{2phi} (d phi)^2",
        weight="e^{2phi} (DERIVED weight) ; X (FREE coefficient)",
        tag="MIGRATION-DEFERRED",
        operator=None,                     # NOT in the a=-1 baseline operator
        evidence="native_dilation_weight_derivation: the e^{2phi} weight on (d phi)^2 is DERIVED "
                 "(R1/R2/R3); the coefficient X is FREE/UNFORCED (healthy window |X|>~1.7e5, large "
                 "NEGATIVE). Absent from the GR-baseline (phi not dynamic; a=-1).",
        migration_note="wired at migration; X tagged FREE.",
    ),
    dict(
        name="matter_weight",
        symbol="e^{2phi} in front of L_m",
        weight="e^{2phi} (UNTRACED)",
        tag="MIGRATION-DEFERRED",          # candidate smuggled import -- see below
        operator=None,
        evidence="UNTRACED: the e^{2phi} matter weight in SOLVER_INTEGRITY_UPGRADES_SPEC line 33 "
                 "appears NOWHERE in F2/scale-symmetry/CANON; the corpus matter action has NO such "
                 "factor. Inserting it CHANGES the matter field equations. FLAGGED as a candidate "
                 "smuggled import; the GR-baseline does NOT use it.",
        migration_note="must be DERIVED or DROPPED at migration -- do NOT add to pass a test.",
    ),
]


def term(name):
    for t in ACTION_TERMS:
        if t["name"] == name:
            return t
    raise KeyError(name)


# ===========================================================================
# THE SINGLE-SOURCE OPERATOR HOOKS.  The live operator pieces, re-exported HERE so the
# action file is the one place the action<->code mapping lives.  (Thin re-exports: the
# implementations stay in their validated modules; this names them as THE realization of
# the action terms above.)
# ===========================================================================
def matter_lagrangian(ginv, Gmn, xi=1.0, kap=1.0):
    """L_m = L2 + L4 (the matter action density).  Source: whole_metric_3d_matter.lagrangian."""
    import whole_metric_3d_matter as MAT
    return MAT.lagrangian(ginv, Gmn, xi, kap)


def matter_stress(g, ginv, dn, xi=1.0, kap=1.0):
    """T_{mu nu} = -2 delta(sqrt(-g) L_m)/delta g^{mu nu} / sqrt(-g)  (Hilbert variation of L_m).
    Source: whole_metric_3d_matter.stress_tensor (asserted == the autograd variation in P2)."""
    import whole_metric_3d_matter as MAT
    return MAT.stress_tensor(g, ginv, dn, xi, kap)


def gravity_operator_general(G, warps):
    """G^mu_nu = EL of sqrt(-g) R (the Einstein tensor).  Source: the analytic general engine."""
    from einstein_3d_general_eval import einstein_mixed_general
    return einstein_mixed_general(G, warps)
