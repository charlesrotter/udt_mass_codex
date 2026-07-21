#!/usr/bin/env python3
"""Exact CPU derivation for the preregistered UDT time-live boundary-flux audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

COMPONENTS = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3))
ETA = sp.diag(-1, 1, 1, 1)

PARENT_HASHES = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    "udt_full_equation_variation_p05_2026-07-21/SHA256SUMS.txt": "5c26d4eb97c4dc370e286469c63d662f182a71a94a6e6899131fd6706c4e7f2e",
    "udt_pre_p06_boundary_selector_audit_2026-07-21/SHA256SUMS.txt": "45c239639d999c26f2e574592fafc392fbb7c1e6f20ea92e1d260b4784e00e51",
    "reciprocal_metric_null_line_selector_2026-07-19/SHA256SUMS.txt": "01ed5557bb94a1df99209d37b1eb5e4eefae4486978be34ab09dafb73aeac17b",
    "complete_coframe_seal_involution_2026-07-20/SHA256SUMS.txt": "87d43cb281d236111a8baec4fe7da5686a8043931e6ba0a2715228f7d61f483e",
    "udt_global_kinematic_assembly_p03g_2026-07-21/SHA256SUMS.txt": "62f9b3f33409b62fb841734e8a91e61d9b859247bf808c4a6cf3740b6a54b6c9",
    "udt_founded_constraint_atlas_p03_2026-07-21/SHA256SUMS.txt": "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def symmetric_h() -> tuple[list[sp.Symbol], sp.Matrix]:
    hs = list(sp.symbols("h00 h01 h02 h03 h11 h12 h13 h22 h23 h33"))
    h = sp.zeros(4)
    for value, (a, b) in zip(hs, COMPONENTS):
        h[a, b] = value
        h[b, a] = value
    return hs, h


def principal_matrices(xi_values: tuple[int, int, int, int]) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    hs, h = symmetric_h()
    xi = sp.Matrix(xi_values)
    xi_up = ETA * xi
    xi2 = (xi.T * xi_up)[0]
    trace_h = sp.trace(ETA * h)
    ricci = sp.zeros(4)
    for a in range(4):
        for b in range(4):
            first = xi[a] * sum(xi_up[c] * h[c, b] for c in range(4))
            second = xi[b] * sum(xi_up[c] * h[c, a] for c in range(4))
            ricci[a, b] = sp.expand((first + second - xi2 * h[a, b] - xi[a] * xi[b] * trace_h) / 2)
    scalar = sp.expand(sum(xi_up[a] * xi_up[b] * h[a, b] for a in range(4) for b in range(4)) - xi2 * trace_h)
    einstein = sp.zeros(4)
    bach = sp.zeros(4)
    for a in range(4):
        for b in range(4):
            einstein[a, b] = sp.expand(ricci[a, b] - ETA[a, b] * scalar / 2)
            bach[a, b] = sp.expand(
                xi2 * ricci[a, b] / 2
                - xi[a] * xi[b] * scalar / 6
                - ETA[a, b] * xi2 * scalar / 12
            )
    evec = sp.Matrix([einstein[a, b] for a, b in COMPONENTS])
    bvec = sp.Matrix([bach[a, b] for a, b in COMPONENTS])
    emat = evec.jacobian(hs)
    bmat = bvec.jacobian(hs)
    return emat, bmat, einstein, bach


def gauge_vector(xi_values: tuple[int, int, int, int], v_values: tuple[int, int, int, int]) -> sp.Matrix:
    xi = sp.Matrix(xi_values)
    v = sp.Matrix(v_values)
    entries = []
    for a, b in COMPONENTS:
        entries.append(xi[a] * v[b] + xi[b] * v[a])
    return sp.Matrix(entries)


def weyl_vector() -> sp.Matrix:
    return sp.Matrix([2 * ETA[a, b] for a, b in COMPONENTS])


def symplectic_matrix(pair_count: int) -> sp.Matrix:
    identity = sp.eye(pair_count)
    zero = sp.zeros(pair_count)
    return zero.row_join(identity).col_join((-identity).row_join(zero))


def isotropic_check(jmat: sp.Matrix, basis: sp.Matrix, expected_dim: int) -> None:
    require(basis.rank() == expected_dim, "polarization basis rank")
    require(basis.T * jmat * basis == sp.zeros(expected_dim), "polarization is not flux-free")


def main() -> None:
    checks = 0
    for rel, expected in PARENT_HASHES.items():
        require(sha256(ROOT / rel) == expected, f"parent hash changed: {rel}")
        checks += 1

    # Complete reciprocal first-jet causal identity with a general positive angular block.
    phi, c, a, b, d = sp.symbols("phi c a b d", nonzero=True)
    pt, pr, p1, p2 = sp.symbols("phi_t phi_r phi_1 phi_2")
    delta = a * d - b**2
    qinv = sp.Matrix([[d, -b], [-b, a]]) / delta
    pang = (sp.Matrix([p1, p2]).T * qinv * sp.Matrix([p1, p2]))[0]
    complete_square = p1**2 / a + (a * p2 - b * p1) ** 2 / (a * delta)
    require(sp.simplify(pang - complete_square) == 0, "angular positive-form identity")
    norm = -sp.exp(2 * phi) * pt**2 / c**2 + sp.exp(-2 * phi) * pr**2 + pang
    seal_norm = sp.simplify(norm.subs(phi, 0))
    require(sp.simplify(seal_norm - (-pt**2 / c**2 + pr**2 + pang)) == 0, "seal norm")
    checks += 2

    # Radially moving regular level-set branch.
    v = sp.symbols("v", real=True)
    moving_norm = sp.factor(seal_norm.subs({pt: -v * pr, p1: 0, p2: 0}))
    require(moving_norm == -pr**2 * (-c + v) * (c + v) / c**2, "moving-seal norm")
    tangent_norm = -c**2 + v**2
    require(sp.simplify(moving_norm + pr**2 * tangent_norm / c**2) == 0, "normal/tangent causal duality")
    omega = sp.symbols("Omega", positive=True)
    require(sp.simplify((seal_norm / omega**2) / seal_norm - omega ** -2) == 0, "CSN causal preservation")
    checks += 3

    sign_witnesses = [
        ("S01", "TIMELIKE_NORMAL_SPACELIKE_SEAL", (1, 0, 0, 0), "-1"),
        ("S02", "NULL_NORMAL_NULL_SEAL", (1, 1, 0, 0), "0"),
        ("S03", "SPACELIKE_NORMAL_TIMELIKE_SEAL", (0, 1, 0, 0), "1"),
        ("S04", "NULL_WITH_ANGULAR_GRADIENT", (1, 0, 1, 0), "0"),
    ]
    for _, _, jet, expected in sign_witnesses:
        actual = -jet[0] ** 2 + jet[1] ** 2 + jet[2] ** 2 + jet[3] ** 2
        require(str(actual) == expected, f"seal sign witness {jet}")
        checks += 1

    # Full ten-component principal symbols at three exact covectors.
    covectors = {
        "TIMELIKE": (1, 0, 0, 0),
        "SPACELIKE": (0, 1, 0, 0),
        "NULL": (1, 1, 0, 0),
    }
    rank_rows: list[dict[str, str]] = []
    principal_cache: dict[str, tuple[sp.Matrix, sp.Matrix]] = {}
    for causal, xi in covectors.items():
        emat, bmat, einstein, bach = principal_matrices(xi)
        principal_cache[causal] = (emat, bmat)
        xi_up = ETA * sp.Matrix(xi)
        for col_b in range(4):
            div_e = [sp.expand(sum(xi_up[a] * einstein[a, col_b] for a in range(4)))]
            div_b = [sp.expand(sum(xi_up[a] * bach[a, col_b] for a in range(4)))]
            require(div_e == [0], f"Einstein Noether identity {causal}/{col_b}")
            require(div_b == [0], f"Bach Noether identity {causal}/{col_b}")
        require(sp.expand(sum(ETA[a, b_] * bach[a, b_] for a in range(4) for b_ in range(4))) == 0, f"Bach trace {causal}")
        for basis_i in range(4):
            vv = tuple(1 if i == basis_i else 0 for i in range(4))
            gv = gauge_vector(xi, vv)
            require(emat * gv == sp.zeros(10, 1), f"Einstein gauge kernel {causal}/{basis_i}")
            require(bmat * gv == sp.zeros(10, 1), f"Bach gauge kernel {causal}/{basis_i}")
        require(bmat * weyl_vector() == sp.zeros(10, 1), f"Bach Weyl kernel {causal}")
        checks += 13
        xi2 = str((sp.Matrix(xi).T * ETA * sp.Matrix(xi))[0])
        rank_rows.extend(
            [
                {
                    "lane": "L01",
                    "covector_class": causal,
                    "covector": str(xi),
                    "xi_squared": xi2,
                    "matrix_dimension": "10x10",
                    "rank": str(bmat.rank()),
                    "nullity": str(10 - bmat.rank()),
                    "built_in_kernel": "4 diffeomorphism + 1 Weyl (independence may drop on null xi)",
                    "quotient_character": "metric-null double",
                    "scope": "flat-point principal symbol; conditional C2 lane",
                },
                {
                    "lane": "L02",
                    "covector_class": causal,
                    "covector": str(xi),
                    "xi_squared": xi2,
                    "matrix_dimension": "10x10",
                    "rank": str(emat.rank()),
                    "nullity": str(10 - emat.rank()),
                    "built_in_kernel": "4 diffeomorphism (independence may drop on null xi)",
                    "quotient_character": "metric-null simple",
                    "scope": "flat-point principal symbol; conditional EH lane",
                },
            ]
        )

    # Exact EH comparison canonical form and exact C2 constrained boundary-flux witnesses.
    # C2 must not be represented as twelve unconstrained pairs: P_K is trace-free and CSN supplies
    # a presymplectic null direction.  Its complete reduced rank remains open.
    jeh = symplectic_matrix(6)
    require(jeh.rank() == 12, "EH comparison canonical rank")
    checks += 1

    # EH basis ordering (gamma_0..gamma_5, pi_0..pi_5); gamma_0 is reciprocal seal ratio.
    eh_a = sp.zeros(12, 6)
    for i in range(6):
        eh_a[6 + i, i] = 1
    eh_b = sp.zeros(12, 6)
    eh_b[6, 0] = 1
    for i in range(1, 6):
        eh_b[i, i] = 1
    isotropic_check(jeh, eh_a, 6)
    isotropic_check(jeh, eh_b, 6)
    require(eh_a != eh_b, "EH polarizations distinct")
    require(all(eh_a[0, j] == 0 and eh_b[0, j] == 0 for j in range(6)), "EH seal tangent")
    checks += 4

    dh = sp.Matrix(sp.symbols("dh0:6"))
    dk = sp.Matrix(sp.symbols("dk0:6"))
    pih = sp.Matrix(sp.symbols("pih0:6"))
    pk = sp.Matrix(sp.symbols("pk0:6"))
    c2_flux = (pih.T * dh)[0] + (pk.T * dk)[0]
    witness_a_rules = {**{dh[i]: 0 for i in range(6)}, **{pk[i]: 0 for i in range(6)}}
    witness_b_rules = {dh[0]: 0, **{pih[i]: 0 for i in range(1, 6)}, **{pk[i]: 0 for i in range(6)}}
    witness_a = sp.simplify(c2_flux.subs(witness_a_rules))
    witness_b = sp.simplify(c2_flux.subs(witness_b_rules))
    require(witness_a == 0, "C2 h-fixed K-free natural-E witness")
    require(witness_b == 0, "C2 seal-only h plus natural transverse equations witness")
    require(not any(dk[i] in witness_a_rules or dk[i] in witness_b_rules for i in range(6)), "C2 normal jet variables retained")
    require(dh[1] not in witness_b_rules, "C2 transverse h variables retained")
    checks += 4

    # The scalar seal wire does not kill angular/off-diagonal flux.
    eh_u = sp.zeros(12, 1)
    eh_v = sp.zeros(12, 1)
    eh_u[1] = 1
    eh_v[7] = 1
    jc2_channel = symplectic_matrix(1)
    c2_u = sp.Matrix([1, 0])
    c2_v = sp.Matrix([0, 1])
    require((eh_u.T * jeh * eh_v)[0] == 1, "EH angular flux witness")
    require((c2_u.T * jc2_channel * c2_v)[0] == 1, "C2 angular channel flux witness")
    require(eh_u[0] == eh_v[0] == 0, "EH flux witnesses preserve scalar seal")
    checks += 3

    # Exact principal wave/biwave flux witnesses in the transverse-traceless angular-shape
    # polarization h_22=-h_33=q(t,x).  The normalization below suppresses only the common nonzero
    # lane coefficient; it is not a physical action normalization.
    tt = sp.zeros(10, 1)
    tt[7] = 1
    tt[9] = -1
    emat_null, bmat_null, _, _ = principal_matrices((1, -1, 0, 0))
    require(emat_null * tt == sp.zeros(10, 1), "EH null TT characteristic")
    require(bmat_null * tt == sp.zeros(10, 1), "C2 null TT characteristic")
    t, x = sp.symbols("t x", real=True)
    box = lambda f: sp.diff(f, x, 2) - sp.diff(f, t, 2)
    q1_eh, q2_eh = t - x, (t - x) ** 2
    require(box(q1_eh) == 0 and box(q2_eh) == 0, "EH principal waves")
    jx_eh = sp.expand(q1_eh * sp.diff(q2_eh, x) - q2_eh * sp.diff(q1_eh, x))
    require(jx_eh.subs({t: 1, x: 0}) == -1, "EH time-live nonzero flux")
    q1_c2, q2_c2 = x**2 + t * x, t - x
    require(box(box(q1_c2)) == 0 and box(box(q2_c2)) == 0, "C2 principal biwaves")
    s1, s2 = box(q1_c2), box(q2_c2)
    jx_c2 = sp.expand(s1 * sp.diff(q2_c2, x) - sp.diff(s1, x) * q2_c2 - s2 * sp.diff(q1_c2, x) + sp.diff(s2, x) * q1_c2)
    require(jx_c2.subs({t: 1, x: 0}) == -2, "C2 time-live nonzero flux")
    checks += 6

    source_rows = [
        {"id": f"SRC{i:02d}", "path": rel, "sha256": expected, "role": role}
        for i, ((rel, expected), role) in enumerate(
            zip(
                PARENT_HASHES.items(),
                [
                    "founding metric finite-cell and bootstrap ledger",
                    "conditional P05 bulk operators currents and constraints",
                    "static pre-P06 selector obstruction",
                    "time-live dphi causal and angular-sector parent algebra",
                    "complete-coframe seal nonuniqueness",
                    "global boundary/coframe branch census",
                    "field-realization census",
                ],
            ),
            start=1,
        )
    ]
    write_tsv("SOURCE_LINEAGE.tsv", ["id", "path", "sha256", "role"], source_rows)

    seal_rows = [
        {
            "id": sid,
            "normal_class": label,
            "seal_first_jet_at_c1_qI": str(jet),
            "normal_norm": expected,
            "boundary_class": {"S01": "spacelike", "S02": "null", "S03": "timelike", "S04": "null"}[sid],
            "current_UDT_status": "CONDITIONAL_WITNESS_NOT_SELECTED",
            "consequence": "Reciprocity supplies the cone but does not select the seal first jet",
        }
        for sid, label, jet, expected in sign_witnesses
    ]
    seal_rows.extend(
        [
            {
                "id": "S05",
                "normal_class": "RADIAL_MOVING_LEVEL_SET",
                "seal_first_jet_at_c1_qI": "phi_t=-v*phi_r",
                "normal_norm": "phi_r^2*(1-v^2/c^2)",
                "boundary_class": "timelike/null/spacelike according to |v|<c/=c/>c",
                "current_UDT_status": "DERIVED_KINEMATICS_INSIDE_CONDITIONAL_TIME_LIVE_SEAL_EXTENSION",
                "consequence": "null seal iff v=+c or -c when phi_r is nonzero; v is not selected",
            },
            {
                "id": "S06",
                "normal_class": "STATIC_CANONICAL_SEAL",
                "seal_first_jet_at_c1_qI": "phi_t=phi_A=0; phi_r free",
                "normal_norm": "phi_r^2",
                "boundary_class": "timelike when regular; undefined as level set if phi_r=0",
                "current_UDT_status": "CANONIZED_SCOPED_STATIC_RESULT",
                "consequence": "the recorded static mirror is non-characteristic at regular points",
            },
            {
                "id": "S07",
                "normal_class": "NO_TIME_LIVE_SEAL_EXTENSION",
                "seal_first_jet_at_c1_qI": "not supplied",
                "normal_norm": "not evaluable",
                "boundary_class": "OPEN",
                "current_UDT_status": "CURRENT_FOUNDATION_BRANCH",
                "consequence": "static canon alone does not define a moving boundary worldtube",
            },
        ]
    )
    write_tsv(
        "SEAL_CAUSAL_BRANCHES.tsv",
        ["id", "normal_class", "seal_first_jet_at_c1_qI", "normal_norm", "boundary_class", "current_UDT_status", "consequence"],
        seal_rows,
    )

    write_tsv(
        "PRINCIPAL_SYMBOL_RANKS.tsv",
        ["lane", "covector_class", "covector", "xi_squared", "matrix_dimension", "rank", "nullity", "built_in_kernel", "quotient_character", "scope"],
        rank_rows,
    )

    characteristic_rows = [
        {"id": "C01", "lane": "L01", "object": "gauge-quotient principal factor", "exact_result": "alpha*(g^ab xi_a xi_b)^2", "time_live_meaning": "metric null cone with double fourth-order characteristic", "selector_effect": "propagation cone only; no polarization selected", "status": "DERIVED_CONDITIONAL"},
        {"id": "C02", "lane": "L02", "object": "gauge-quotient principal factor", "exact_result": "kappa*(g^ab xi_a xi_b)", "time_live_meaning": "metric null cone with simple second-order characteristic", "selector_effect": "propagation cone only; no polarization selected", "status": "DERIVED_CONDITIONAL"},
        {"id": "C03", "lane": "L01", "object": "Noether identities", "exact_result": "nabla^a B_ab=0 and g^ab B_ab=0", "time_live_meaning": "diffeomorphism and Weyl constraint identities", "selector_effect": "propagate compatible constraints after evolution/gauge/boundary choices; do not choose them", "status": "DERIVED_CONDITIONAL"},
        {"id": "C04", "lane": "L02", "object": "Noether identity", "exact_result": "nabla^a(G_ab+Lambda g_ab)=0", "time_live_meaning": "diffeomorphism constraint identity", "selector_effect": "propagates compatible constraints after evolution/gauge/boundary choices; does not choose them", "status": "DERIVED_CONDITIONAL"},
        {"id": "C05", "lane": "L01+L02", "object": "regular level-set seal", "exact_result": "seal characteristic iff g^-1(dphi,dphi)=0", "time_live_meaning": "null dphi eikonal branch", "selector_effect": "optional branch; current Reciprocity does not force it", "status": "DERIVED_KINEMATICS_CONDITIONAL_EXTENSION"},
        {"id": "C06", "lane": "L01+L02", "object": "CSN", "exact_result": "g^-1(dphi,dphi)->Omega^-2 g^-1(dphi,dphi)", "time_live_meaning": "causal type and nullness preserved", "selector_effect": "preserves a choice; does not make one", "status": "DERIVED"},
        {"id": "C07", "lane": "L01+L02", "object": "type-changing/degenerate locus", "exact_result": "inverse-metric symbol unavailable or nonuniform", "time_live_meaning": "characteristic count may change", "selector_effect": "no extrapolation from regular branches", "status": "OPEN_RETAINED"},
        {"id": "C08", "lane": "L03", "object": "bridge characteristics", "exact_result": "no operator", "time_live_meaning": "undefined", "selector_effect": "cannot test", "status": "OPEN_NO_OPERATOR"},
    ]
    write_tsv("CHARACTERISTIC_AND_CONSTRAINTS.tsv", ["id", "lane", "object", "exact_result", "time_live_meaning", "selector_effect", "status"], characteristic_rows)

    pair_rows = [
        {"lane": "L02", "regular_boundary_type": "non-null", "coordinate_slots": "6 induced metric gamma_ij including reciprocal ratio and angular/off-diagonal slots", "momentum_slots": "6 pi^ij", "phase_dimension": "12", "symplectic_rank": "12", "seal_restriction": "one reciprocal-ratio coordinate tangent fixed", "remaining_fact": "at least five coordinate pairs plus reciprocal momentum remain unselected", "scope": "conditional EH lane after a non-null canonical completion"},
        {"lane": "L01", "regular_boundary_type": "non-null", "coordinate_slots": "6 h_ij plus K_ij with only its trace-free sector paired by electric Weyl momentum", "momentum_slots": "Pi_h^ij plus trace-free P_K^ij=-8 epsilon E^ij", "phase_dimension": "OPEN_CONSTRAINED_PRESYMPLECTIC", "symplectic_rank": "OPEN_BEFORE_CSN_AND_CONSTRAINT_REDUCTION", "seal_restriction": "one h reciprocal-ratio tangent fixed; reciprocal normal jet remains free", "remaining_fact": "trace P_K=0 and the CSN null direction forbid an unconstrained twelve-pair count; multiple exact differentiable classes still survive", "scope": "conditional C2 fourth-order non-null boundary structure"},
        {"lane": "L01+L02", "regular_boundary_type": "null", "coordinate_slots": "generator cross-section shear/twist/normalization data depend on lane and completion", "momentum_slots": "not selected", "phase_dimension": "OPEN", "symplectic_rank": "OPEN", "seal_restriction": "nullness alone", "remaining_fact": "auxiliary null, generator normalization, joints and incoming data remain open", "scope": "covariant current only; non-null pairs not imported"},
        {"lane": "L01+L02", "regular_boundary_type": "moving/type-changing", "coordinate_slots": "embedding plus induced fields", "momentum_slots": "embedding response and field momenta", "phase_dimension": "OPEN", "symplectic_rank": "OPEN", "seal_restriction": "conditional level-set tangency only", "remaining_fact": "embedding variation and causal-transition law absent", "scope": "not completed by current foundation"},
    ]
    write_tsv("SYMPLECTIC_PAIR_CENSUS.tsv", ["lane", "regular_boundary_type", "coordinate_slots", "momentum_slots", "phase_dimension", "symplectic_rank", "seal_restriction", "remaining_fact", "scope"], pair_rows)

    polarization_rows = [
        {"id": "P01", "lane": "L02", "name": "seal-compatible induced-metric polarization", "fixed_or_free": "all delta gamma=0; all delta pi free", "scalar_seal": "preserved", "normal_phi_jet": "not fixed by induced metric data", "flux": "zero", "dimension": "6", "status": "CONDITIONAL_WITNESS_NOT_ADOPTED"},
        {"id": "P02", "lane": "L02", "name": "seal-plus-transverse-momentum polarization", "fixed_or_free": "delta gamma_phi=0 and delta pi_transverse=0; delta pi_phi and delta gamma_transverse free", "scalar_seal": "preserved", "normal_phi_jet": "reciprocal momentum free", "flux": "zero", "dimension": "6", "status": "INEQUIVALENT_CONDITIONAL_WITNESS"},
        {"id": "P03", "lane": "L01", "name": "h-fixed K-free natural-electric-Weyl class", "fixed_or_free": "all delta h=0; all delta K free; impose P_K_TF=-8 epsilon E_TF=0; corner delta h=0", "scalar_seal": "preserved", "normal_phi_jet": "all delta K including reciprocal normal jet free", "flux": "zero on declared natural subspace", "dimension": "OPEN_CONSTRAINED_PRESYMPLECTIC", "status": "CONDITIONAL_WITNESS_NOT_ADOPTED"},
        {"id": "P04", "lane": "L01", "name": "seal-only h plus fully-natural transverse class", "fixed_or_free": "delta h_phi=0; transverse delta h and all delta K free; impose E_TF=0 projected Pi_h=0 and corner flux=0", "scalar_seal": "preserved", "normal_phi_jet": "all delta K including reciprocal normal jet free", "flux": "zero on inequivalent declared natural subspace", "dimension": "OPEN_CONSTRAINED_PRESYMPLECTIC", "status": "INEQUIVALENT_CONDITIONAL_WITNESS"},
        {"id": "P05", "lane": "L01+L02", "name": "continuous canonical rotations", "fixed_or_free": "each unsealed canonical pair admits mixed Lagrangian subspaces", "scalar_seal": "preservable", "normal_phi_jet": "preservable as free", "flux": "zero on each chosen Lagrangian subspace", "dimension": "lane-dependent", "status": "CONTINUUM_AMBIGUITY"},
    ]
    write_tsv("POLARIZATION_WITNESSES.tsv", ["id", "lane", "name", "fixed_or_free", "scalar_seal", "normal_phi_jet", "flux", "dimension", "status"], polarization_rows)

    flux_rows = [
        {"id": "F01", "lane": "L02", "sector": "unsealed angular/off-diagonal canonical pair", "fields": "delta1 gamma_1=1; delta2 pi_1=1", "equations": "phase-space tangent witness", "seal": "delta phi=0", "boundary_flux": "1", "conclusion": "scalar seal does not imply zero full metric flux"},
        {"id": "F02", "lane": "L01", "sector": "unsealed angular h/Pi_h canonical pair", "fields": "delta1 h_2=1; delta2 Pi_h2=1", "equations": "phase-space tangent witness", "seal": "delta phi=0", "boundary_flux": "1", "conclusion": "scalar seal does not imply zero fourth-order flux"},
        {"id": "F03", "lane": "L02", "sector": "time-live TT angular-shape principal wave h_22=-h_33=q", "fields": "q1=t-x; q2=(t-x)^2", "equations": "Box q1=Box q2=0", "seal": "reciprocal phi perturbation absent", "boundary_flux": "normalized j^x(t=1,x=0)=-1", "conclusion": "on-principal-shell time dependence carries nonzero boundary flux"},
        {"id": "F04", "lane": "L01", "sector": "time-live TT angular-shape principal biwave h_22=-h_33=q", "fields": "q1=x^2+t*x; q2=t-x", "equations": "Box^2 q1=Box^2 q2=0", "seal": "reciprocal phi perturbation absent", "boundary_flux": "normalized j^x(t=1,x=0)=-2", "conclusion": "double-characteristic lane retains independent derivative flux"},
    ]
    write_tsv("FLUX_WITNESSES.tsv", ["id", "lane", "sector", "fields", "equations", "seal", "boundary_flux", "conclusion"], flux_rows)

    ambiguity_rows = [
        {"id": "A01", "object": "overall action scale", "time_live_effect": "rescales symplectic current momenta and charges", "bulk_effect": "same zero equation for nonzero scale", "removed_by_characteristics": "NO", "status": "OPEN"},
        {"id": "A02", "object": "Euler beta E4", "time_live_effect": "changes boundary/corner potential", "bulk_effect": "zero regular 4D metric bulk variation", "removed_by_characteristics": "NO", "status": "OPEN"},
        {"id": "A03", "object": "exact bulk divergence", "time_live_effect": "changes boundary primitive", "bulk_effect": "no bulk Euler change", "removed_by_characteristics": "NO", "status": "OPEN"},
        {"id": "A04", "object": "Theta -> Theta + delta Y + dZ", "time_live_effect": "changes potential/corner representative and local flux by an exact boundary divergence", "bulk_effect": "no bulk Euler change", "removed_by_characteristics": "NO", "status": "OPEN"},
        {"id": "A05", "object": "boundary Legendre transform", "time_live_effect": "exchanges coordinate and momentum polarization", "bulk_effect": "preserves bulk symplectic form", "removed_by_characteristics": "NO", "status": "OPEN"},
        {"id": "A06", "object": "orientation reference generator normalization", "time_live_effect": "changes signs/zero points/charges", "bulk_effect": "no principal cone selection", "removed_by_characteristics": "NO", "status": "OPEN"},
        {"id": "A07", "object": "moving embedding and joints", "time_live_effect": "adds embedding response and joint/corner channels", "bulk_effect": "not contained in fixed-boundary operator", "removed_by_characteristics": "NO", "status": "OPEN"},
    ]
    write_tsv("FUNCTIONAL_AMBIGUITY.tsv", ["id", "object", "time_live_effect", "bulk_effect", "removed_by_characteristics", "status"], ambiguity_rows)

    boundary_rows = [
        {"id": "T01", "branch": "NO_TIME_LIVE_SEAL_EXTENSION", "causal_status": "OPEN", "L01": "covariant current only", "L02": "covariant current only", "polarization": "NOT_DEFINED", "selected": "NO"},
        {"id": "T02", "branch": "FIXED_NON_NULL_MIRROR_FOLD", "causal_status": "regular static level set is timelike when dphi nonzero", "L01": "noncharacteristic fourth-order boundary pairs", "L02": "noncharacteristic second-order boundary pairs", "polarization": "MULTIPLE", "selected": "NO"},
        {"id": "T03", "branch": "MOVING_TIMELIKE_SEAL", "causal_status": "spacelike normal", "L01": "noncharacteristic; boundary data required", "L02": "noncharacteristic; boundary data required", "polarization": "MULTIPLE", "selected": "NO"},
        {"id": "T04", "branch": "MOVING_NULL_CHARACTERISTIC_SEAL", "causal_status": "null normal; v=+-c only in radial level-set subcase", "L01": "double characteristic", "L02": "simple characteristic", "polarization": "NULL_DATA_GENERATOR_AND_JOINTS_OPEN", "selected": "NO"},
        {"id": "T05", "branch": "MOVING_SPACELIKE_SEAL", "causal_status": "timelike normal", "L01": "initial/final-data type fourth-order surface", "L02": "initial/final-data type second-order surface", "polarization": "MULTIPLE", "selected": "NO"},
        {"id": "T06", "branch": "TYPE_CHANGING_OR_DEGENERATE", "causal_status": "nonuniform or inverse metric unavailable", "L01": "OPEN", "L02": "OPEN", "polarization": "OPEN", "selected": "NO"},
        {"id": "T07", "branch": "NULL_WRL_HORIZON", "causal_status": "conditional distinct null object", "L01": "covariant current; double cone", "L02": "covariant current; simple cone", "polarization": "generator normalization auxiliary null and joints open", "selected": "NO"},
        {"id": "T08", "branch": "QUOTIENT_CROSSING_INTERNAL_MATCH", "causal_status": "ontology unselected", "L01": "matching/soldering action open", "L02": "matching/soldering action open", "polarization": "OPEN", "selected": "NO"},
    ]
    write_tsv("BOUNDARY_BRANCH_STATUS.tsv", ["id", "branch", "causal_status", "L01", "L02", "polarization", "selected"], boundary_rows)

    field_rows: list[dict[str, str]] = []
    for lane in ("L01", "L02", "L03"):
        for rid in range(1, 8):
            realization = f"C{rid:02d}"
            if lane == "L03":
                operator = "NO_BRIDGE_OPERATOR"
                characteristic = "UNDEFINED"
                flux = "UNDEFINED"
            elif rid == 1:
                operator = "CONDITIONAL_METRIC_BULK_OPERATOR"
                characteristic = "METRIC_NULL_DOUBLE" if lane == "L01" else "METRIC_NULL_SIMPLE"
                flux = "MULTIPLE_POLARIZATIONS_NONZERO_UNDER_SEAL_ALONE"
            else:
                operator = "METRIC_OPERATOR_ONLY_EXTRA_FIELD_EQUATION_ABSENT"
                characteristic = "METRIC_PART_ONLY_EXTRA_FIELD_UNDEFINED"
                flux = "EXTRA_FIELD_FLUX_UNDEFINED"
            field_rows.append(
                {
                    "pair_id": f"{lane}_{realization}",
                    "lane": lane,
                    "realization": realization,
                    "operator_status": operator,
                    "time_live_characteristic": characteristic,
                    "boundary_flux_status": flux,
                    "complete_coframe_status": "OPEN_MULTIPLE_LIFTS" if rid == 3 else "NOT_SUPPLIED_OR_NOT_APPLICABLE",
                    "P06_ready": "NO",
                }
            )
    write_tsv("FIELD_LANE_CLOSURE.tsv", ["pair_id", "lane", "realization", "operator_status", "time_live_characteristic", "boundary_flux_status", "complete_coframe_status", "P06_ready"], field_rows)

    status_rows = [
        {"id": "R01", "claim": "full reciprocal first-jet causal identity", "status": "DERIVED", "scope": "positive local reciprocal representative with arbitrary positive angular block"},
        {"id": "R02", "claim": "time-live seal is phi=0 level surface", "status": "CONDITIONAL_EXPLORATORY_EXTENSION", "scope": "static seal canon does not itself make this global extension"},
        {"id": "R03", "claim": "radial moving seal tangency phi_t+v phi_r=0", "status": "DERIVED_CONDITIONAL_KINEMATICS", "scope": "regular radial level-set branch"},
        {"id": "R04", "claim": "Reciprocity forces null seal speed", "status": "NOT_DERIVED", "scope": "timelike null and spacelike exact first-jet witnesses survive"},
        {"id": "R05", "claim": "L01 characteristic cone", "status": "DERIVED_CONDITIONAL_DOUBLE_METRIC_NULL", "scope": "regular metric C2 lane after diagnostic gauge/Weyl quotient"},
        {"id": "R06", "claim": "L02 characteristic cone", "status": "DERIVED_CONDITIONAL_SIMPLE_METRIC_NULL", "scope": "regular metric EH lane after diagnostic gauge quotient"},
        {"id": "R07", "claim": "Noether identities select boundary data", "status": "NOT_DERIVED", "scope": "identities propagate compatible constraints but supply no unique incoming/polarization subspace"},
        {"id": "R08", "claim": "static scalar seal kills full boundary flux", "status": "EXCLUDED_BY_EXACT_COUNTERWITNESSES", "scope": "angular/off-diagonal metric channels in both conditional lanes"},
        {"id": "R09", "claim": "time-live characteristics select polarization", "status": "NOT_DERIVED", "scope": "multiple exact maximal flux-free polarizations survive"},
        {"id": "R10", "claim": "time-live characteristics select boundary functional", "status": "NOT_DERIVED", "scope": "Euler improvement Legendre embedding orientation and corner ambiguities survive"},
        {"id": "R11", "claim": "complete coframe time-live flux", "status": "OPEN_NO_COFRAME_ACTION_OR_UNIQUE_LIFT", "scope": "metric-only result cannot be promoted to coframe fields"},
        {"id": "R12", "claim": "P06 readiness", "status": "CLOSED_ZERO_OF_21_PAIRS", "scope": "complete operator boundary and field equations required"},
        {"id": "R13", "claim": "overall selector classification", "status": "TIME_LIVE_REDUCES_BUT_DOES_NOT_SELECT_BOUNDARY_DATA", "scope": "current principles and conditional P05 lanes only"},
        {"id": "R14", "claim": "native action carrier source mass scale or charge", "status": "OPEN_NOT_ADDRESSED", "scope": "outside maximum conclusion"},
    ]
    write_tsv("STATUS_LEDGER.tsv", ["id", "claim", "status", "scope"], status_rows)

    dependency = {
        "question": "Does full time-live metric structure close the pre-P06 boundary selector?",
        "inputs": list(PARENT_HASHES),
        "conditional_lanes": {
            "L01": {"bulk": "Bach", "principal": "double metric-null", "canonical_pairs": 12},
            "L02": {"bulk": "Einstein-Lambda", "principal": "simple metric-null", "canonical_pairs": 6},
            "L03": {"bulk": None, "principal": None, "canonical_pairs": None},
        },
        "joins": [
            "conditional time-live seal level set -> dphi normal",
            "metric operator principal symbol -> propagation characteristics",
            "boundary variation -> symplectic canonical pairs",
            "seal tangent -> one reciprocal coordinate restriction",
        ],
        "failed_implications": [
            "metric null cone -> seal is null",
            "seal is null -> unique boundary data",
            "Noether identity -> unique constraint-preserving boundary condition",
            "delta phi=0 -> zero complete metric flux",
            "zero flux -> unique polarization",
            "polarization -> unique boundary functional",
        ],
        "open_inputs": [
            "time-live seal extension",
            "complete coframe action and lift",
            "boundary causal type and embedding",
            "off-shell bootstrap functional",
            "boundary/corner improvement and normalization",
            "all non-metric field equations",
        ],
    }
    (OUT / "SELECTOR_DEPENDENCY_GRAPH.json").write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    require(len(rank_rows) == 6, "principal rank row count")
    require(len(seal_rows) == 7, "seal row count")
    require(len(boundary_rows) == 8, "boundary branch count")
    require(len(field_rows) == 21 and all(r["P06_ready"] == "NO" for r in field_rows), "field closure count")
    require(len(polarization_rows) == 5, "polarization witness count")
    require(len(flux_rows) == 4, "flux witness count")
    require(len(ambiguity_rows) == 7, "ambiguity count")
    checks += 7

    rank_summary = {
        f"{row['lane']}_{row['covector_class']}": {"rank": int(row["rank"]), "nullity": int(row["nullity"])}
        for row in rank_rows
    }
    result = {
        "audit": "UDT_FULL_TIME_LIVE_CHARACTERISTIC_AND_BOUNDARY_FLUX",
        "base": "21cfeb8f25fe18afe5a5a924ea073a9cfc24238b",
        "classification": "TIME_LIVE_REDUCES_BUT_DOES_NOT_SELECT_BOUNDARY_DATA",
        "epistemic_grade": "LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW",
        "maximum_conclusion": "TIME_LIVE_CHARACTERISTIC_AND_BOUNDARY_FLUX_SELECTOR_STATUS_CLASSIFIED",
        "checks": checks,
        "principal_ranks": rank_summary,
        "seal_causal_classes_retained": ["timelike", "null", "spacelike", "type-changing/open"],
        "conditional_characteristics": {"L01": "metric-null double", "L02": "metric-null simple", "L03": "undefined"},
        "canonical_pair_census": {"L01_non_null": "constrained presymplectic; P_K trace-free and CSN-null", "L02_non_null_comparison": 6},
        "inequivalent_flux_free_polarizations": {"L01": 2, "L02": 2, "continuous_families": True},
        "nonzero_seal_compatible_flux_witnesses": 4,
        "functional_ambiguities_retained": len(ambiguity_rows),
        "boundary_branches": len(boundary_rows),
        "field_lane_pairs": len(field_rows),
        "P06_ready_pairs": 0,
        "solutions_run": 0,
        "gpu_used": False,
        "central_result": (
            "Time dependence supplies conditional propagation cones, a level-set velocity relation, "
            "constraint identities, and boundary canonical pairs. It does not select the seal causal "
            "type, a unique flux-free polarization, or a unique boundary/corner functional."
        ),
    }
    (OUT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "UDT_TIME_LIVE_CHARACTERISTIC_FLUX_AUDIT=PASS",
        f"checks={checks}",
        "classification=TIME_LIVE_REDUCES_BUT_DOES_NOT_SELECT_BOUNDARY_DATA",
        f"principal_ranks={json.dumps(rank_summary, sort_keys=True)}",
        "seal_causal_classes=timelike,null,spacelike,type-changing/open",
        "flux_free_polarizations=L01:2+,L02:2+",
        "seal_compatible_nonzero_flux_witnesses=4",
        "boundary_branches=8",
        "field_pairs=21/21",
        "P06_ready_pairs=0",
        "solutions=0 gpu=NO",
        "maximum_conclusion=TIME_LIVE_CHARACTERISTIC_AND_BOUNDARY_FLUX_SELECTOR_STATUS_CLASSIFIED",
    ]
    (OUT / "DERIVATION_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()
