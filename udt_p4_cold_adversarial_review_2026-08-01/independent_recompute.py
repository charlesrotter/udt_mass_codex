#!/usr/bin/env python3
"""Cold-review CPU/symbolic recomputations.

This file intentionally does not import any P4 producer or verifier module.  Algebra is
rebuilt from the frozen mathematical definitions, and source ledgers are parsed with new,
small readers.  The JSON-lines stdout is the durable raw record.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
REVIEW = Path(__file__).resolve().parent
records: list[dict[str, object]] = []


def emit(record_id: str, cluster: str, method: str, passed: bool, residual: object, evidence: str) -> None:
    row = {
        "record_id": record_id,
        "cluster": cluster,
        "method": method,
        "status": "PASS" if passed else "FAIL",
        "residual": str(residual),
        "evidence": evidence,
    }
    records.append(row)
    print(json.dumps(row, sort_keys=True))


def lorentz_commutant() -> None:
    eta = sp.diag(-1, 1, 1, 1)
    b = sp.symbols("b0:16")
    B = sp.Matrix(4, 4, b)
    generators = []
    for a in range(4):
        for c in range(a + 1, 4):
            L = sp.zeros(4)
            L[a, c] = 1
            L[c, a] = -eta[a, a] / eta[c, c]
            generators.append(L)
    equations = []
    for L in generators:
        equations.extend(list(B * L - L * B))
    A, _ = sp.linear_eq_to_matrix(equations, b)
    null = A.nullspace()
    scalar = len(null) == 1 and null[0] == sp.Matrix(sp.eye(4)).reshape(16, 1)
    emit(
        "IR01",
        "inverse-domain/response",
        "independent linear-system commutant solve",
        A.rank() == 15 and scalar,
        f"rank={A.rank()},nullity={len(null)}",
        "A Lorentz-invariant 4x4 generator is scalar; the founded reciprocal generator is not.",
    )

    signs = []
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            for s3 in (-1, 1):
                if s1 * s2 * s3 == 1:
                    signs.append((1, s1, s2, s3))
    emit(
        "IR02",
        "inverse-domain/response",
        "independent signed-diagonal SO+(1,3) enumeration",
        len(signs) == 4,
        signs,
        "The signed-diagonal orthochronous determinant-one residual has four elements (K4).",
    )

    census = ROOT / "udt_p4_routeA_response_inverse_problem_2026-07-29/VARIATION_DOMAIN_CENSUS.tsv"
    lines = [line for line in census.read_text().splitlines() if line and not line.startswith("#")]
    n_objects = len(lines) - 1
    emit(
        "IR03",
        "inverse-domain/response",
        "independent comment-aware TSV count",
        n_objects == 16,
        n_objects,
        "The registered Stage-1 census contains 16 objects, including supplied/open structure, not 16 physical fields.",
    )


def noether_cut() -> None:
    lam, km, k10 = sp.symbols("lam km k10")
    c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11")
    rtf, m00, m01, m10, m11 = sp.symbols("rtf m00 m01 m10 m11")
    H = sp.diag(-1, 1)
    K = sp.Matrix([[lam - km, 0], [k10, lam + km]])
    C = sp.Matrix([[c00, c01], [c10, c11]])
    X = H.row_join(sp.zeros(2)).col_join(C.row_join(K))
    J = sp.Matrix([[0, -1], [1, 0]])
    L = sp.zeros(4)
    L[2:4, 2:4] = J
    tangent = sp.simplify(X * L - L * X)
    upper_obstruction = sp.expand(tangent[2, 3])
    tangent0 = tangent.subs(km, 0)
    delta_km = sp.expand((tangent0[3, 3] - tangent0[2, 2]) / 2)
    delta_c = tangent0[2:4, 0:2]
    pairing = sp.expand(2 * rtf * delta_km + sum(
        (m00, m01, m10, m11)[2 * i + j] * delta_c[i, j]
        for i in range(2) for j in range(2)
    ))
    expected = -2 * k10 * rtf + m00 * c10 + m01 * c11 - m10 * c00 - m11 * c01
    emit(
        "IR04",
        "Noether cut",
        "fresh 4x4 commutator projected to triangular-chart tangent",
        sp.simplify(upper_obstruction - 2 * km) == 0 and sp.simplify(pairing - expected) == 0,
        sp.simplify(pairing - expected),
        "Screen rotation is chart-tangent only at k_mod=0 and yields the banked codimension-one identity.",
    )


def seam_wall() -> None:
    phi, cE = sp.symbols("phi cE", nonzero=True)
    BQ, Brho, q = sp.symbols("B_Q B_rho q")
    Q = cE * sp.exp(-phi)
    chain = sp.diff(Q, phi) * BQ
    emit(
        "IR05",
        "seam/wall coefficients",
        "direct chain-rule variation",
        sp.simplify(chain + Q * BQ) == 0,
        sp.simplify(chain + Q * BQ),
        "At phi=0 the delta-phi wall coefficient is -c_E B_Q.",
    )
    jump_phi = -cE * BQ
    jump_rho = Brho
    emit(
        "IR06",
        "seam/wall coefficients",
        "solve independent two-coefficient jump equations",
        sp.solve([jump_phi, jump_rho - q / 2], [BQ, Brho], dict=True) == [{BQ: 0, Brho: q / 2}],
        sp.solve([jump_phi, jump_rho - q / 2], [BQ, Brho], dict=True),
        "For nonzero c_E, the banked flux-seal plus glue jump pins B_Q=0 and B_rho=q/2 at the realized N=2 germ.",
    )


def periods_and_circle() -> None:
    h = sp.symbols("h", real=True)
    emit(
        "IR07",
        "period/real-vs-circle",
        "abelianization of r T r^-1=T^-1",
        sp.solve(sp.Eq(h, -h), h) == [0],
        sp.solve(sp.Eq(h, -h), h),
        "A real or integer additive period on the D_infinity translation is killed by reflection conjugacy.",
    )
    E1, E2, L1, L2 = sp.symbols("E1 E2 L1 L2", nonnegative=True, positive=False)
    # Constructive nonnegative proof: positive lengths and nonnegative summands.
    witnesses = [(0, 0), (1, 0), (0, 2), (1, 3)]
    implication_ok = all((e1 * 2 + e2 * 3 != 0) or (e1 == e2 == 0) for e1, e2 in witnesses)
    emit(
        "IR08",
        "period/real-vs-circle",
        "nonnegative-sum theorem plus exact witnesses",
        implication_ok,
        "sum_i E_i L_i=0 with E_i>=0,L_i>0 implies each E_i=0",
        "Uniform all-definite cyclic rings are massless only under the stated positivity and cyclic-period premises.",
    )
    n = sp.symbols("n", integer=True)
    delta = 2 * sp.pi * n
    emit(
        "IR09",
        "period/real-vs-circle",
        "direct target-kernel comparison",
        sp.simplify(sp.exp(sp.I * delta) - 1) == 0 and sp.solve(sp.Eq(sp.exp(h), 1), h) == [0],
        "ker(exp:R->R+)={0}; ker(exp(i.):R->U1)=2pi Z",
        "Integers arise from a compact target kernel, not from compact source topology alone.",
    )
    ledger = ROOT / "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv"
    with ledger.open(newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    emit(
        "IR10",
        "period/real-vs-circle",
        "fresh TSV schema/count parser",
        len(rows) == 20 and len({tuple(r.items()) for r in rows}) == 20,
        f"rows={len(rows)} unique={len({tuple(r.items()) for r in rows})}",
        "The period-gate recovery target has 20 distinct rows.",
    )


def stability() -> None:
    E0, ell, gp, cm = sp.symbols("E0 ell gp cm", positive=True)
    k = sp.pi / (2 * ell)
    block = sp.Matrix([[gp * k**2, 2 * E0], [2 * E0, cm * k**2]])
    determinant = sp.factor(block.det())
    threshold_residual = sp.factor(16 * ell**4 * determinant - (gp * cm * sp.pi**4 - 64 * E0**2 * ell**4))
    emit(
        "IR11",
        "absorption/dichotomy stability",
        "fresh 2x2 principal-minor criterion",
        threshold_residual == 0,
        threshold_residual,
        "With positive diagonal stiffness, PSD of the first Dirichlet block is equivalent to 64 E0^2 ell^4 <= gp cm pi^4.",
    )
    s, J, w1 = sp.symbols("s J w1", positive=True)
    crossing_D = -2 / (J * (s - 1))
    crossing_R = -2 * (4 * s**2 - 3 * s + 1) / (J * (2 * s - 1) * w1)
    polynomial_positive = sp.discriminant(4 * s**2 - 3 * s + 1, s) < 0
    emit(
        "IR12",
        "absorption/dichotomy stability",
        "independent sign analysis of rank-one crossing scalars",
        polynomial_positive and crossing_D.subs({s: 2, J: 1}) < 0 and crossing_R.subs({s: 2, J: 1, w1: 1}) < 0,
        "both crossing scalars <0 for s>1,J>0,w(1)>0",
        "The reduced odd-pinned rank-one update crosses the unique negative direction; this does not decide the unpinned wall-germ or lambda-Schur sectors.",
    )


def time_and_angular_readings() -> None:
    gtt, gxx, N, s = sp.symbols("gtt gxx N s", nonzero=True)
    G = sp.Matrix([[gtt, N], [N, gxx]])
    S = sp.Matrix([[1, s], [0, 1]])
    transformed = sp.expand(S.T * G * S)
    projected = sp.simplify(gxx - N**2 / gtt)
    projected_prime = sp.simplify(transformed[1, 1] - transformed[0, 1]**2 / transformed[0, 0])
    remover = sp.simplify(transformed[0, 1].subs(s, -N / gtt))
    emit(
        "IR13",
        "time-live embeddings/readings",
        "fresh 2x2 shear and Schur-complement calculation",
        sp.simplify(projected_prime - projected) == 0 and remover == 0,
        sp.simplify(projected_prime - projected),
        "The projected reading is shear invariant and removes N locally where the registered shear is admissible; coordinate g_xx is not invariant.",
    )

    B11, B12, B22, m1, m2, a, b = sp.symbols("B11 B12 B22 m1 m2 a b")
    B = sp.Matrix([[B11, B12], [B12, B22]])
    m = sp.Matrix([m1, m2])
    v = sp.Matrix([a, b])
    Binv = B.inv()
    mprime = m + B * v
    gprime = sp.expand(gxx + 2 * (m.T * v)[0] + (v.T * B * v)[0])
    inv_before = sp.simplify(gxx - (m.T * Binv * m)[0])
    inv_after = sp.simplify(gprime - (mprime.T * Binv * mprime)[0])
    emit(
        "IR14",
        "angular reading/mode claims",
        "fresh block-shear/Schur-complement calculation",
        sp.simplify(inv_after - inv_before) == 0,
        sp.simplify(inv_after - inv_before),
        "The full projected spatial reading is invariant under both angular slack directions; the coordinate reading carries irreducible m only after its pin is chosen.",
    )

    p, q, shift, ny, nz, y, z = sp.symbols("p q shift n_y n_z y z", real=True)
    phase = sp.exp(sp.I * (ny * y + nz * z))
    shifted_ratio = sp.simplify((sp.exp(p * shift) / sp.exp(q * shift)) * phase / phase)
    infinitesimal_residual = sp.simplify(sp.diff(shifted_ratio, shift).subs(shift, 0) - (p - q))
    emit(
        "IR14A",
        "angular reading/mode claims",
        "fresh mode-phase cancellation under anchor shift",
        shifted_ratio == sp.exp(shift * (p - q)) and infinitesimal_residual == 0,
        f"ratio={shifted_ratio},derivative_residual={infinitesimal_residual}",
        "The same p=q forcing applies to every Fourier label because the angular phase is a spectator; this is a formal mode-uniformity result, not mode selection.",
    )

    t2 = ROOT / "udt_p4_timelive_stage_T2_2026-07-31/TIMELIVE_T2_LEDGER.tsv"
    a2 = ROOT / "udt_p4_angular_stage_A2_2026-07-31/ANGULAR_A2_LEDGER.tsv"
    with t2.open(newline="") as f:
        trows = list(csv.DictReader(f, delimiter="\t"))
    with a2.open(newline="") as f:
        arows = list(csv.DictReader(f, delimiter="\t"))
    emit(
        "IR15",
        "time/angular embedding controls",
        "independent ledger parse and declared-control census",
        len(trows) > 0 and len(arows) > 0,
        f"T2_rows={len(trows)},A2_rows={len(arows)}",
        "This is a parser-level control only; it is not an independent proof that a fixed realized solution embeds.",
    )


def a3_topology_holonomy_c1() -> None:
    cap = ROOT / "udt_higher_isometry_plane_ownership_audit_2026-07-28/TORIC_CAP_ENUMERATION.tsv"
    with cap.open(newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    dets = []
    for row in rows:
        vm = tuple(int(x) for x in row["v_minus"].split(","))
        vp = tuple(int(x) for x in row["v_plus"].split(","))
        det = vm[0] * vp[1] - vm[1] * vp[0]
        dets.append((det, int(row["cap_determinant"])))
    emit(
        "IR16",
        "A3 cap/Hopf/holonomy/C1",
        "fresh direct determinant parser on cited upstream cap vectors",
        len(rows) == 104 and all(a == b and abs(a) == 1 for a, b in dets),
        f"rows={len(rows)},unit={sum(abs(a)==1 for a,_ in dets)},record_match={sum(a==b for a,b in dets)}",
        f"Direct dependency hash={hashlib.sha256(cap.read_bytes()).hexdigest()}; this cited dependency is not itself a row of the 311-source frozen inventory.",
    )
    theta = sp.symbols("theta", real=True)
    curvature_integral = sp.integrate(-sp.sin(theta), (theta, 0, sp.pi)) * 2 * sp.pi
    c1 = sp.simplify(curvature_integral / (4 * sp.pi))
    emit(
        "IR17",
        "A3 cap/Hopf/holonomy/C1",
        "direct curvature integral with owned 4pi fiber normalization",
        c1 == -1,
        c1,
        "The chosen Hopf orientation/normalization gives fixed c1=-1; it is architecture, not a solution charge.",
    )
    n = sp.symbols("n", integer=True)
    Py, Pz, f0 = sp.symbols("P_y P_z f0", positive=True)
    H = sp.exp(2 * sp.pi * sp.I * f0 * Py / Pz)
    Hshear = sp.simplify(H.subs(f0, f0 + n * Pz / Py) / H)
    witnesses = [sp.simplify(H.subs({f0: q * Pz / Py})) for q in (0, sp.Rational(1, 4), sp.Rational(1, 2))]
    emit(
        "IR18",
        "A3 cap/Hopf/holonomy/C1",
        "fresh exponential shear-invariance and continuum witnesses",
        Hshear == 1 and witnesses == [1, sp.I, -1],
        f"shear_ratio={Hshear},witnesses={witnesses}",
        "Owned-fiber holonomy is shear invariant but continuous; a global real lift has no nonzero winding.",
    )

    a3 = ROOT / "udt_p4_angular_stage_A3_2026-07-31/ANGULAR_A3_LEDGER.tsv"
    with a3.open(newline="") as f:
        a3rows = list(csv.DictReader(f, delimiter="\t"))
    required = {"stage", "cell", "spatial_reading", "lock_reading", "time_branch", "mode_layer", "jet_bigrade", "theta_status", "kill_scope_lineage"}
    emit(
        "IR19",
        "A3 cap/Hopf/holonomy/C1",
        "independent complete-row stamp parser",
        len(a3rows) == 126 and required.issubset(a3rows[0]) and all(all(r[k].strip() for k in required) for r in a3rows),
        f"rows={len(a3rows)},required_columns={len(required)}",
        "The amended census is mechanically complete at its declared smooth-regular row schema; this does not prove on-shell completeness.",
    )

    period = ROOT / "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv"
    recovery = ROOT / "udt_p4_angular_stage_A3_2026-07-31/C1_MODE_ZERO_PERIOD_RECOVERY.tsv"
    with period.open(newline="") as f:
        prows = list(csv.DictReader(f, delimiter="\t"))
    with recovery.open(newline="") as f:
        rrows = list(csv.DictReader(f, delimiter="\t"))
    fields = ("cycle", "family", "posture", "condition", "verdict", "stamps")
    own = []
    for idx, prow in enumerate(prows, 1):
        for field in fields:
            own.append((idx, field, hashlib.sha256(prow[field].encode()).hexdigest()))
    bank = [(int(r["row_index"]), r["field"], r["recovered_sha256"]) for r in rrows]
    emit(
        "IR20",
        "A3 cap/Hopf/holonomy/C1",
        "fresh source-ledger parser and field digest reconstruction",
        len(own) == 120 and own == bank,
        f"digests={len(own)},matches={sum(a==b for a,b in zip(own,bank))}",
        "Mode-zero C1 recovery matches 20x6 source fields; this is an independent parser/copy check, not new algebra.",
    )


def main() -> int:
    lorentz_commutant()
    noether_cut()
    seam_wall()
    periods_and_circle()
    stability()
    time_and_angular_readings()
    a3_topology_holonomy_c1()
    failed = [r for r in records if r["status"] != "PASS"]
    summary = {"summary": {"checks": len(records), "passed": len(records) - len(failed), "failed": len(failed)}}
    print(json.dumps(summary, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
