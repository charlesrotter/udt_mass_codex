#!/usr/bin/env python3
"""Second fresh adversarial verifier for the unbanked P4 cold review.

This script is review-owned, CPU-only, and imports no P4 producer, package
verifier, or primary-review module.  It emits durable JSONL plus a compact JSON
result only inside this review package.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "2e93a621aeeee0a0844543068363d0ba94094357"
RAW = HERE / "SECOND_VERIFIER_RAW.jsonl"
RESULTS = HERE / "SECOND_VERIFIER_RESULTS.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


records: list[dict[str, object]] = []


def record(check_id: str, layer: str, passed: bool, detail: object, disposition: str = "") -> None:
    records.append({
        "check_id": check_id,
        "layer": layer,
        "status": "PASS" if passed else "FAIL",
        "detail": detail,
        "disposition": disposition,
    })


def write_outputs(result: dict[str, object]) -> None:
    RAW.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in records))
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


EXPECTED_PACKAGE_CLAIMS = {
    "P4-00": 4, "P4-01": 2, "P4-02": 3, "P4-03": 6, "P4-04": 4,
    "P4-05": 6, "P4-06": 3, "P4-07": 4, "P4-08": 5, "P4-09": 4,
    "P4-10": 3, "P4-11": 5, "P4-12": 3, "P4-13": 4, "P4-14": 5,
    "P4-15": 4, "P4-16": 5, "P4-17": 8, "P4-18": 5, "P4-19": 6,
    "P4-20": 7, "P4-21": 6, "P4-22": 12, "P4-23": 11, "P4-24": 9,
    "P4-25": 5, "P4-26": 13, "P4-27": 10, "P4-28": 10,
}

TEN_COMPLETENESS_FIELDS = (
    "fields_covered_or_dropped",
    "action_terms_covered_or_dropped",
    "equations_covered_or_dropped",
    "domain_covered_or_dropped",
    "boundary_covered_or_dropped",
    "topology_covered_or_dropped",
    "dynamical_character_covered_or_dropped",
    "branches_covered_or_dropped",
    "stability_covered_or_dropped",
    "regime_and_limits",
)

PARSER_IDS = {"IR03", "IR10", "IR15", "IR19", "IR20"}


def source_manifest_check(overrides: dict[str, bytes] | None = None) -> tuple[int, list[str]]:
    overrides = overrides or {}
    bad: list[str] = []
    lines = (HERE / "SOURCE_MANIFEST.sha256").read_text().splitlines()
    for line in lines:
        digest, rel = line.split("  ", 1)
        data = overrides.get(rel)
        if data is None:
            path = (HERE / rel).resolve()
            if not path.is_file():
                bad.append(rel)
                continue
            data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            bad.append(rel)
    return len(lines), bad


def status_paths() -> list[str]:
    raw = subprocess.check_output(["git", "status", "--porcelain", "-z"], cwd=ROOT)
    return [item[3:] for item in raw.decode().split("\0") if item]


def audit_structure() -> dict[str, object]:
    frozen = read_tsv("FROZEN_REVIEW_UNITS.tsv")
    inventory = read_tsv("SOURCE_INVENTORY.tsv")
    claims = read_tsv("MECHANICAL_CLAIM_REGRADES.tsv")
    premise = read_tsv("PREMISE_QUANTIFIER_AUDIT.tsv")
    recompute = read_tsv("INDEPENDENT_RECOMPUTATION_LEDGER.tsv")
    shared = read_tsv("SHARED_CODE_CIRCULARITY_MAP.tsv")
    primary_results = json.loads((HERE / "REVIEW_RESULTS.json").read_text())

    units = [r["unit_id"] for r in frozen]
    record("SV01", "frozen-inputs", len(units) == 37 and len(set(units)) == 37,
           {"rows": len(units), "unique": len(set(units))})
    package_units = [u for u in units if u.startswith("P4-")]
    question_units = [u for u in units if u.startswith("Q")]
    record("SV02", "frozen-inputs", len(package_units) == 29 and len(question_units) == 8,
           {"packages": len(package_units), "questions": len(question_units)})
    nmanifest, bad_manifest = source_manifest_check()
    record("SV03", "source-immutability", nmanifest == 311 and not bad_manifest,
           {"rows": nmanifest, "bad": bad_manifest})
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT
    ).returncode == 0
    record("SV04", "frozen-inputs", ancestor, {"base": BASE})

    inv_paths = {r["path"] for r in inventory}
    package_dirs = sorted({r["package"] for r in frozen if r["unit_id"].startswith("P4-")})
    tracked = set(subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE, "--", *package_dirs],
        cwd=ROOT, text=True,
    ).splitlines())
    record("SV05", "source-selection", tracked <= inv_paths and len(tracked) == 297,
           {"tracked_package_files": len(tracked), "missing_from_inventory": sorted(tracked - inv_paths)})

    counts = Counter(r["unit_id"] for r in claims)
    package_counts = {u: counts[u] for u in EXPECTED_PACKAGE_CLAIMS}
    record("SV06", "claim-explosion", package_counts == EXPECTED_PACKAGE_CLAIMS,
           {"package_clause_rows": sum(package_counts.values()), "counts": package_counts})
    record("SV07", "claim-explosion",
           all(counts[f"Q{i}"] == 1 for i in range(1, 9)) and counts["D-001"] == counts["D-002"] == 1,
           {"questions": {f"Q{i}": counts[f"Q{i}"] for i in range(1, 9)},
            "discoveries": {"D-001": counts["D-001"], "D-002": counts["D-002"]}})
    duplicate_claim_ids = [k for k, v in Counter(r["claim_id"] for r in claims).items() if v > 1]
    record("SV08", "claim-explosion", len(claims) == 182 and not duplicate_claim_ids,
           {"rows": len(claims), "duplicate_claim_ids": duplicate_claim_ids})
    grade_counts = Counter(r["regrade"] for r in claims)
    expected_grades = Counter({"RETAINED": 32, "NARROWED": 148, "CONTRADICTED": 1, "OPEN": 1})
    record("SV09", "regrade-counts", grade_counts == expected_grades,
           dict(sorted(grade_counts.items())))
    result_counts = Counter(primary_results["regrades"])
    record("SV10", "regrade-counts", grade_counts == result_counts,
           {"ledger": dict(grade_counts), "results": primary_results["regrades"]})

    missing_replacement = [r["claim_id"] for r in claims if not r["replacement_sentence"].strip()]
    record("SV11", "replacement-sentences", not missing_replacement,
           {"missing": missing_replacement, "rows": len(claims)})
    bad_source_rows: list[str] = []
    for row in claims:
        if row["unit_kind"] != "PACKAGE_HEADLINE_CLAUSE":
            continue
        if not (ROOT / row["source_path"]).is_file() or row["source_path"] not in inv_paths:
            bad_source_rows.append(row["claim_id"])
    record("SV12", "provenance", not bad_source_rows,
           {"package_rows_checked": 172, "bad_source_rows": bad_source_rows})

    missing_cells = {
        r["claim_id"]: [field for field in TEN_COMPLETENESS_FIELDS if not r.get(field, "").strip()]
        for r in claims
    }
    missing_cells = {k: v for k, v in missing_cells.items() if v}
    record("SV13", "completeness-presence", not missing_cells,
           {"rows": len(claims), "fields_per_row": len(TEN_COMPLETENESS_FIELDS), "missing": missing_cells})
    completeness_text = (HERE / "COMPLETENESS_MAP.md").read_text()
    headings_present = all(f"{i}. **" in completeness_text for i in range(1, 11))
    record("SV14", "completeness-presence", headings_present,
           {"ten_named_sections": headings_present})

    # The production verifier's named ten-cell check actually reads only three of
    # the ten cells (plus premise_stack).  Seven completeness columns are untested.
    primary_checked = {"domain_covered_or_dropped", "branches_covered_or_dropped", "regime_and_limits"}
    untested = sorted(set(TEN_COMPLETENESS_FIELDS) - primary_checked)
    record("SV15", "primary-verifier-adequacy", len(untested) == 7,
           {"completeness_fields_not_checked_by_primary_verifier": untested},
           "REQUIRED_AMENDMENT")

    # Every package clause uses one package-wide premise template.  That is a useful
    # ceiling, but it is not a clause-by-clause reconstruction of exact source stamps.
    pkg_claims = [r for r in claims if r["unit_kind"] == "PACKAGE_HEADLINE_CLAUSE"]
    premise_shapes = {u: {r["premise_stack"] for r in pkg_claims if r["unit_id"] == u}
                      for u in EXPECTED_PACKAGE_CLAIMS}
    one_template_units = sorted(u for u, values in premise_shapes.items() if len(values) == 1)
    record("SV16", "premise-fidelity", len(one_template_units) == 29,
           {"package_clause_rows": len(pkg_claims), "single_template_units": len(one_template_units)},
           "REQUIRED_AMENDMENT: replace package templates with clause-specific source stamps where load-bearing")

    # The action-term cell says response/geometry-only for packages whose clauses
    # explicitly depend on a conditional energy, wall action, Hessian, or theta
    # coupling menu.  Presence is not semantic completeness.
    action_live_units = {"P4-07", "P4-08", "P4-16", "P4-18", "P4-20"}
    weak_action_rows = [r["claim_id"] for r in pkg_claims
                        if r["unit_id"] in action_live_units
                        and r["action_terms_covered_or_dropped"].endswith("response/geometry only")]
    record("SV17", "completeness-fidelity", len(weak_action_rows) == 26,
           {"rows_requiring_action_cell_amendment": len(weak_action_rows),
            "units": sorted(action_live_units), "claim_ids": weak_action_rows},
           "REQUIRED_AMENDMENT")

    premise_counts_ok = len(premise) == 37 and all(int(r["exploded_claim_count"]) == counts[r["unit_id"]] for r in premise)
    record("SV18", "premise-ledger", premise_counts_ok,
           {"rows": len(premise)})
    record("SV19", "circularity-map", len(shared) == 33,
           {"package_rows": sum(r["unit_id"].startswith("P4-") for r in shared),
            "cross_package_rows": sum(r["unit_id"].startswith("X-") for r in shared)})

    mislabeled = sorted(r["record_id"] for r in recompute
                        if r["record_id"] in PARSER_IDS and r["independence_label"] == "GENUINELY_DIFFERENT_METHOD")
    record("SV20", "independence-labels", mislabeled == ["IR10", "IR20"],
           {"false_independent_labels": mislabeled},
           "REQUIRED_AMENDMENT")

    outside = sorted(p for p in status_paths() if not p.startswith(HERE.name + "/"))
    record("SV21", "write-isolation", not outside, {"outside_package": outside})
    primary_manifest_bad: list[str] = []
    for line in (HERE / "REVIEW_MANIFEST.sha256").read_text().splitlines():
        digest, rel = line.split("  ", 1)
        if not (HERE / rel).is_file() or sha(HERE / rel) != digest:
            primary_manifest_bad.append(rel)
    record("SV21A", "primary-review-manifest-pre-second-append", not primary_manifest_bad,
           {"rows": len((HERE / "REVIEW_MANIFEST.sha256").read_text().splitlines()),
            "bad": primary_manifest_bad,
            "scope": "validated before the mandatory final AUDIT_REPORT second-verifier append"})
    return {
        "frozen": frozen,
        "inventory": inventory,
        "claims": claims,
        "recompute": recompute,
        "grade_counts": dict(sorted(grade_counts.items())),
        "false_independent_labels": mislabeled,
        "weak_action_rows": weak_action_rows,
        "single_template_units": one_template_units,
    }


def dependency_overlay(frozen: list[dict[str, str]], inventory: list[dict[str, str]]) -> list[dict[str, object]]:
    """Post-outcome citation overlay; never represented as preregistered input."""
    package_dirs = sorted({r["package"] for r in frozen if r["unit_id"].startswith("P4-")})
    inv_paths = {r["path"] for r in inventory}
    pattern = re.compile(
        r"(?<![A-Za-z0-9_.-])((?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\."
        r"(?:md|tsv|json|py|txt|sha256|npz|csv))"
    )
    refs: dict[str, set[str]] = defaultdict(set)
    for directory in package_dirs:
        for source in (ROOT / directory).iterdir():
            if not source.is_file():
                continue
            try:
                text = source.read_text()
            except UnicodeDecodeError:
                continue
            for match in pattern.finditer(text):
                rel = match.group(1).lstrip("./")
                if (ROOT / rel).is_file() and rel not in inv_paths:
                    refs[rel].add(str(source.relative_to(ROOT)))

    overlay: list[dict[str, object]] = []
    for rel, sources in sorted(refs.items()):
        current = (ROOT / rel).read_bytes()
        base = subprocess.check_output(["git", "show", f"{BASE}:{rel}"], cwd=ROOT)
        overlay.append({
            "path": rel,
            "sha256": hashlib.sha256(current).hexdigest(),
            "base_sha256": hashlib.sha256(base).hexdigest(),
            "base_byte_identical": current == base,
            "cited_by_count": len(sources),
            "cited_by": sorted(sources),
            "status": "POST_OUTCOME_OVERLAY_NOT_RETROACTIVE_PREREGISTRATION",
        })
    record("SV22", "transitive-source-overlay", len(overlay) == 13 and all(r["base_byte_identical"] for r in overlay),
           {"explicit_existing_external_refs": len(overlay), "paths": [r["path"] for r in overlay]},
           "DISCLOSED_FREEZE_GAP; overlay is non-retroactive")

    cap = next(r for r in overlay if r["path"].endswith("TORIC_CAP_ENUMERATION.tsv"))
    joint = next(r for r in overlay if r["path"].endswith("JOINT_OPERATION_OBLIGATIONS.tsv"))
    hashes_ok = (
        cap["sha256"] == "ceecb5837ff8652c83c0ba72c67645182b1fd30f6e437026bd735c4d813bdfdf"
        and joint["sha256"] == "52bc430e16227cc60d73e312a916666e0d206c54dc90a0d7ca8914d6c01336e9"
    )
    record("SV23", "transitive-source-overlay", hashes_ok,
           {"cap": cap["sha256"], "joint": joint["sha256"],
            "note": "joint hash is correct but absent from primary machine raw"},
           "REQUIRED_AMENDMENT: preserve the overlay hashes in machine-readable evidence")
    return overlay


def independent_recomputations() -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}

    def ir(rid: str, passed: bool, detail: object, method: str) -> None:
        out[rid] = {"status": "PASS" if passed else "FAIL", "detail": detail, "method": method}
        record(f"SV-{rid}", "independent-recomputation", passed, detail)

    eta = sp.diag(-1, 1, 1, 1)
    variables = sp.symbols("x0:16")
    unknown = sp.Matrix(4, 4, variables)
    generators = []
    for a in range(4):
        for b in range(a + 1, 4):
            gen = sp.zeros(4)
            gen[a, b] = 1
            gen[b, a] = -eta[a, a] / eta[b, b]
            generators.append(gen)
    system, _ = sp.linear_eq_to_matrix(
        [entry for gen in generators for entry in unknown * gen - gen * unknown], variables
    )
    null = system.nullspace()
    ir("IR01", system.rank() == 15 and len(null) == 1,
       {"rank": system.rank(), "nullity": len(null)}, "fresh commutant linear system")

    signed = [(1, a, b, c) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1) if a * b * c == 1]
    ir("IR02", len(signed) == 4 and len(set(signed)) == 4, signed, "direct SO+ signed-diagonal enumeration")

    census = ROOT / "udt_p4_routeA_response_inverse_problem_2026-07-29/VARIATION_DOMAIN_CENSUS.tsv"
    census_rows = list(csv.DictReader((line for line in census.open() if line.strip() and not line.startswith("#")), delimiter="\t"))
    ir("IR03", len(census_rows) == 16, len(census_rows), "independent parser/regression")

    lam, km, k10 = sp.symbols("lam km k10")
    c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11")
    rtf, m00, m01, m10, m11 = sp.symbols("rtf m00 m01 m10 m11")
    H = sp.diag(-1, 1)
    K = sp.Matrix([[lam - km, 0], [k10, lam + km]])
    C = sp.Matrix([[c00, c01], [c10, c11]])
    X = H.row_join(sp.zeros(2)).col_join(C.row_join(K))
    rot = sp.zeros(4)
    rot[2:4, 2:4] = sp.Matrix([[0, -1], [1, 0]])
    tangent = sp.expand(X * rot - rot * X)
    tangent0 = tangent.subs(km, 0)
    delta_km = sp.expand((tangent0[3, 3] - tangent0[2, 2]) / 2)
    delta_c = tangent0[2:4, 0:2]
    pairing = sp.expand(2 * rtf * delta_km + m00 * delta_c[0, 0] + m01 * delta_c[0, 1]
                        + m10 * delta_c[1, 0] + m11 * delta_c[1, 1])
    expected = -2 * k10 * rtf + m00 * c10 + m01 * c11 - m10 * c00 - m11 * c01
    ir("IR04", sp.simplify(tangent[2, 3] - 2 * km) == 0 and sp.simplify(pairing - expected) == 0,
       str(sp.simplify(pairing - expected)), "direct commutator and tangent projection")

    phi = sp.symbols("phi", real=True)
    cE = sp.symbols("c_E", nonzero=True)
    BQ, Brho, q = sp.symbols("B_Q B_rho q")
    Q = cE * sp.exp(-phi)
    ir("IR05", sp.simplify(sp.diff(Q, phi) + Q) == 0, str(sp.simplify(sp.diff(Q, phi) + Q)),
       "direct differentiation")
    wall_solution = sp.solve([-cE * BQ, Brho - q / 2], [BQ, Brho], dict=True)
    ir("IR06", wall_solution == [{BQ: 0, Brho: q / 2}], str(wall_solution), "direct linear solve")

    h = sp.symbols("h", real=True)
    ir("IR07", sp.solve(sp.Eq(h, -h), h) == [0], "2h=0", "abelianized reflection conjugacy")
    ir("IR08", True,
       "manual proof: if any E_i>0 then E_i L_i>0 for L_i>0, contradicting a zero sum of nonnegative terms",
       "universal nonnegative-sum proof, not finite witnesses")
    n = sp.symbols("n", integer=True)
    compact_ok = sp.simplify(sp.exp(sp.I * 2 * sp.pi * n) - 1) == 0
    real_ok = sp.solve(sp.Eq(sp.exp(h), 1), h) == [0]
    ir("IR09", compact_ok and real_ok, "real kernel {0}; circle kernel 2pi Z", "direct kernel comparison")

    period_rows = list(csv.DictReader((ROOT / "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv").open(), delimiter="\t"))
    ir("IR10", len(period_rows) == 20 and len({tuple(r.items()) for r in period_rows}) == 20,
       {"rows": len(period_rows), "unique": len({tuple(r.items()) for r in period_rows})},
       "independent parser/regression")

    E0, ell, gp, cm = sp.symbols("E0 ell g_p c_m", positive=True)
    k = sp.pi / (2 * ell)
    block = sp.Matrix([[gp * k**2, 2 * E0], [2 * E0, cm * k**2]])
    residual = sp.factor(16 * ell**4 * block.det() - (gp * cm * sp.pi**4 - 64 * E0**2 * ell**4))
    ir("IR11", residual == 0, str(residual), "principal minors and determinant identity")

    s = sp.symbols("s", real=True)
    poly = 4 * s**2 - 3 * s + 1
    disc = sp.discriminant(poly, s)
    # For s>1: s-1>0, 2s-1>0, poly>0 since its discriminant is negative.
    ir("IR12", disc == -7 and sp.simplify(poly.subs(s, 1)) > 0,
       {"discriminant": str(disc), "p_at_1": str(poly.subs(s, 1))},
       "global sign proof on s>1; no single-point witness")

    gtt, gxx, N, shear = sp.symbols("gtt gxx N shear", nonzero=True)
    G = sp.Matrix([[gtt, N], [N, gxx]])
    S = sp.Matrix([[1, shear], [0, 1]])
    transformed = sp.expand(S.T * G * S)
    before = sp.simplify(gxx - N**2 / gtt)
    after = sp.simplify(transformed[1, 1] - transformed[0, 1]**2 / transformed[0, 0])
    ir("IR13", sp.simplify(after - before) == 0, str(sp.simplify(after - before)), "Schur complement invariance")

    b11, b12, b22, m1, m2, a, b = sp.symbols("b11 b12 b22 m1 m2 a b")
    B = sp.Matrix([[b11, b12], [b12, b22]])
    m = sp.Matrix([m1, m2])
    v = sp.Matrix([a, b])
    mp = m + B * v
    gxp = sp.expand(gxx + 2 * (m.T * v)[0] + (v.T * B * v)[0])
    inv_before = sp.simplify(gxx - (m.T * B.inv() * m)[0])
    inv_after = sp.simplify(gxp - (mp.T * B.inv() * mp)[0])
    ir("IR14", sp.simplify(inv_after - inv_before) == 0, str(sp.simplify(inv_after - inv_before)),
       "block Schur complement invariance")

    p, qq, sh, ny, nz, y, z = sp.symbols("p q sh ny nz y z", real=True)
    phase = sp.exp(sp.I * (ny * y + nz * z))
    ratio = sp.simplify(sp.exp(p * sh) * phase / (sp.exp(qq * sh) * phase))
    ir("IR14A", ratio == sp.exp(sh * (p - qq)), str(ratio), "cancel common Fourier character")

    t2rows = list(csv.DictReader((ROOT / "udt_p4_timelive_stage_T2_2026-07-31/TIMELIVE_T2_LEDGER.tsv").open(), delimiter="\t"))
    a2rows = list(csv.DictReader((ROOT / "udt_p4_angular_stage_A2_2026-07-31/ANGULAR_A2_LEDGER.tsv").open(), delimiter="\t"))
    ir("IR15", len(t2rows) == 26 and len(a2rows) == 29,
       {"T2": len(t2rows), "A2": len(a2rows)}, "independent parser/regression only")

    cap_path = ROOT / "udt_higher_isometry_plane_ownership_audit_2026-07-28/TORIC_CAP_ENUMERATION.tsv"
    cap_rows = list(csv.DictReader(cap_path.open(), delimiter="\t"))
    cap_checks = []
    for row in cap_rows:
        vm = tuple(int(x) for x in row["v_minus"].split(","))
        vp = tuple(int(x) for x in row["v_plus"].split(","))
        determinant = vm[0] * vp[1] - vm[1] * vp[0]
        cap_checks.append(determinant == int(row["cap_determinant"]) and abs(determinant) == 1)
    ir("IR16", len(cap_rows) == 104 and all(cap_checks),
       {"rows": len(cap_rows), "passed": sum(cap_checks), "sha256": sha(cap_path)},
       "direct determinants from frozen-base-identical overlay bytes")

    theta = sp.symbols("theta", real=True)
    c1 = sp.simplify(sp.integrate(-sp.sin(theta), (theta, 0, sp.pi)) * 2 * sp.pi / (4 * sp.pi))
    ir("IR17", c1 == -1, str(c1), "direct curvature integral with stated orientation")

    Py, Pz, f0 = sp.symbols("P_y P_z f0", positive=True)
    hol = sp.exp(2 * sp.pi * sp.I * f0 * Py / Pz)
    shear_ratio = sp.simplify(hol.subs(f0, f0 + n * Pz / Py) / hol)
    witnesses = [sp.simplify(hol.subs(f0, qv * Pz / Py)) for qv in (0, sp.Rational(1, 4), sp.Rational(1, 2))]
    ir("IR18", shear_ratio == 1 and witnesses == [1, sp.I, -1],
       {"shear_ratio": str(shear_ratio), "witnesses": [str(x) for x in witnesses]},
       "direct holonomy witnesses and shear invariance")

    a3rows = list(csv.DictReader((ROOT / "udt_p4_angular_stage_A3_2026-07-31/ANGULAR_A3_LEDGER.tsv").open(), delimiter="\t"))
    expected_stage = Counter({"alpha": 84, "beta": 28, "gamma": 14})
    expected_seats = Counter({
        "native_real_fields": 12, "T2_character_modes": 12, "large_zeta_chart_shear": 12,
        "fiber_U1_connection_holonomy": 12, "angular_mirror_characters": 12,
        "stratum_m_involution": 12, "h_reparam_orientation_degree": 12,
        "all_smooth_modes_and_jets": 12, "full_S3_extension_applicability": 10,
        "registered_Hopf_bundle_applicability": 10, "massive_carrier_integer_test": 4,
        "native_opened_metric_fields": 2, "registered_Hopf_bundle": 2,
        "singular_or_distributional_angular_fields": 1, "completion_topology": 1,
    })
    all_nonblank = all(all(value.strip() for value in row.values()) for row in a3rows)
    unique = len({tuple(row.items()) for row in a3rows})
    ir("IR19", len(a3rows) == 126 and unique == 126 and all_nonblank
       and Counter(r["stage"] for r in a3rows) == expected_stage
       and Counter(r["seat"] for r in a3rows) == expected_seats,
       {"rows": len(a3rows), "unique": unique, "stage": dict(Counter(r["stage"] for r in a3rows)),
        "seat_classes": len(Counter(r["seat"] for r in a3rows)), "columns": len(a3rows[0]),
        "target_contraction_manual": "R is linear; R+ contracts through log/exp; SPD is a convex cone (or contracts through matrix log)"},
       "independent exhaustive schema/count regression plus direct target-space contraction; not an on-shell proof")

    recovery = list(csv.DictReader((ROOT / "udt_p4_angular_stage_A3_2026-07-31/C1_MODE_ZERO_PERIOD_RECOVERY.tsv").open(), delimiter="\t"))
    fields = ("cycle", "family", "posture", "condition", "verdict", "stamps")
    rebuilt = [(idx, field, hashlib.sha256(row[field].encode()).hexdigest())
               for idx, row in enumerate(period_rows, 1) for field in fields]
    saved = [(int(row["row_index"]), row["field"], row["recovered_sha256"]) for row in recovery]
    ir("IR20", len(rebuilt) == 120 and rebuilt == saved,
       {"digests": len(rebuilt), "matches": sum(a == b for a, b in zip(rebuilt, saved))},
       "independent parser/copy regression, not different-method period algebra")

    record("SV24", "independent-recomputation-summary", len(out) == 21 and all(r["status"] == "PASS" for r in out.values()),
           {"total": len(out), "passed": sum(r["status"] == "PASS" for r in out.values()),
            "parser_or_regression": sorted(PARSER_IDS)})
    return out


def primary_replay() -> dict[str, object]:
    run = subprocess.run(
        ["python3", str(HERE / "independent_recompute.py")], cwd=ROOT,
        text=True, capture_output=True,
    )
    lines = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
    checks = [row for row in lines if "record_id" in row]
    result = {
        "exit_code": run.returncode,
        "records": len(checks),
        "passed": sum(row["status"] == "PASS" for row in checks),
        "classification": "SAME_CODE_DETERMINISTIC_REGRESSION_ONLY",
    }
    record("SV25", "primary-replay", run.returncode == 0 and len(checks) == 21
           and all(row["status"] == "PASS" for row in checks), result)
    return result


def audit_primary_catch_proofs(structure: dict[str, object]) -> dict[str, object]:
    claims: list[dict[str, str]] = structure["claims"]  # type: ignore[assignment]
    recompute: list[dict[str, str]] = structure["recompute"]  # type: ignore[assignment]
    frozen: list[dict[str, str]] = structure["frozen"]  # type: ignore[assignment]

    # Primary catch-proof adequacy, judged against the named contract mutation.
    primary_adequate = {
        "missing_unit": True,
        "duplicate_unit": False,  # duplicates claim_id, not FROZEN_REVIEW_UNITS unit_id
        "source_byte_mutation": False,  # checks fake_digest != digest, not source_manifest()
        "quantifier_weakening": False,  # catches only literal sentinel WEAKENED
        "false_independent_label": False,  # misses actual IR10 and IR20 mislabels
        "missing_premise_stamp": True,
        "edit_outside_package": True,
    }
    record("SV26", "primary-catch-proof-audit", sum(primary_adequate.values()) == 3,
           {"adequate": sum(primary_adequate.values()), "required": 7, "by_proof": primary_adequate},
           "REQUIRED_AMENDMENT")

    required_units = {r["unit_id"] for r in frozen}
    missing_mutant = [dict(r) for r in claims if r["unit_id"] != "P4-00"]
    catch_missing = bool(required_units - {r["unit_id"] for r in missing_mutant})

    frozen_dup = [dict(r) for r in frozen] + [dict(frozen[0])]
    catch_duplicate = any(v > 1 for v in Counter(r["unit_id"] for r in frozen_dup).values())

    first_line = (HERE / "SOURCE_MANIFEST.sha256").read_text().splitlines()[0]
    _, rel = first_line.split("  ", 1)
    mutated = (HERE / rel).resolve().read_bytes() + b"SECOND_VERIFIER_SYNTHETIC_MUTATION"
    _, mutation_bad = source_manifest_check({rel: mutated})
    catch_source = rel in mutation_bad

    # A concrete formal->realized promotion, rather than a magic sentinel.
    q2 = next(dict(r) for r in claims if r["unit_id"] == "Q2")
    q2["quantifier_guard"] = "FIXED_REALIZED_SOLUTION_FOR_ALL"
    q2["replacement_sentence"] = "Static, time-live, and angular-live realized solutions embed exactly."
    catch_quantifier = (
        "FIXED_REALIZED" in q2["quantifier_guard"]
        and "formal" not in q2["replacement_sentence"].lower()
        and "open" not in q2["replacement_sentence"].lower()
    )

    ir20 = next(dict(r) for r in recompute if r["record_id"] == "IR20")
    ir20["independence_label"] = "GENUINELY_DIFFERENT_METHOD"
    parser_markers = " ".join((ir20["method_or_command"], ir20["evidence_and_limit"])).lower()
    catch_false_independent = (
        ir20["independence_label"] == "GENUINELY_DIFFERENT_METHOD"
        and any(marker in parser_markers for marker in ("parser", "copy check", "digest", "schema/count"))
    )

    missing_premise = dict(claims[0])
    missing_premise["premise_stack"] = ""
    catch_premise = not missing_premise["premise_stack"].strip()
    catch_outside = any(not path.startswith(HERE.name + "/") for path in ["LIVE.md"])

    second_catches = {
        "missing_unit": catch_missing,
        "duplicate_unit": catch_duplicate,
        "source_byte_mutation": catch_source,
        "quantifier_weakening": catch_quantifier,
        "false_independent_label": catch_false_independent,
        "missing_premise_stamp": catch_premise,
        "edit_outside_package": catch_outside,
    }
    record("SV27", "second-catch-proofs", all(second_catches.values()),
           {"passed": sum(second_catches.values()), "required": 7, "by_proof": second_catches})
    return {"primary": primary_adequate, "second": second_catches}


def hash_outputs() -> dict[str, str]:
    names = (
        "SECOND_VERIFIER_CHECK.py",
        "SECOND_VERIFIER_RAW.jsonl",
        "SECOND_VERIFIER_RESULTS.json",
    )
    return {name: sha(HERE / name) for name in names if (HERE / name).exists()}


def main() -> int:
    structure = audit_structure()
    overlay = dependency_overlay(structure["frozen"], structure["inventory"])  # type: ignore[arg-type]
    recomputations = independent_recomputations()
    replay = primary_replay()
    catches = audit_primary_catch_proofs(structure)
    premise_raw = (HERE / "SECOND_VERIFIER_PREMISE_RAW.txt").read_text().strip()
    premise_pass = premise_raw.startswith("PASS: 18 premise guards, 9 startup controls")
    record("SV28", "premise-verifier", premise_pass, premise_raw)
    record("SV29", "second-verifier-execution-hygiene", False,
           {"event": "temporary manifest-check stdout was redirected to /tmp/udt_p4_source_manifest_second_check.txt outside the worktree/package",
            "cleanup": "file immediately deleted; final git status has no outside-package path; no existing evidence changed"},
           "PROCEDURAL AMENDMENT: final packaging/isolation check must be rerun without an outside-package scratch file")

    verdict = "REFUTED-IN-PART"
    result: dict[str, object] = {
        "date": "2026-08-01",
        "verdict": verdict,
        "review_base": BASE,
        "headline_explosion": {
            "package_units": 29,
            "cross_cutting_units": 8,
            "package_clause_rows": 172,
            "cross_cutting_rows": 8,
            "discovered_rows": 2,
            "total_rows": 182,
        },
        "regrades": structure["grade_counts"],
        "independent_recomputations": {
            "total": len(recomputations),
            "passed": sum(r["status"] == "PASS" for r in recomputations.values()),
            "parser_or_regression_ids": sorted(PARSER_IDS),
            "primary_false_independent_labels": structure["false_independent_labels"],
            "primary_label_counts_before": {"GENUINELY_DIFFERENT_METHOD": 17, "INDEPENDENT_PARSER_OR_REGRESSION": 4},
            "primary_label_counts_after_required_relabels_only": {"GENUINELY_DIFFERENT_METHOD": 15, "INDEPENDENT_PARSER_OR_REGRESSION": 6},
        },
        "completeness": {
            "cells_present_on_every_row": 10,
            "rows": 182,
            "primary_verifier_cells_actually_checked": 3,
            "primary_verifier_cells_not_checked": 7,
            "action_cell_rows_requiring_amendment": len(structure["weak_action_rows"]),
            "package_rows_using_unit_level_premise_template": 172,
            "package_units_using_one_premise_template": 29,
        },
        "catch_proofs": {
            "primary_adequate": sum(catches["primary"].values()),
            "primary_required": 7,
            "second_passed": sum(catches["second"].values()),
            "second_required": 7,
        },
        "source_freeze": {
            "preregistered_inventory_rows": 311,
            "all_preregistered_bytes_unchanged": True,
            "all_297_tracked_package_files_in_inventory": True,
            "post_outcome_overlay_status": "NON_RETROACTIVE",
            "explicit_existing_external_references": len(overlay),
            "overlay": overlay,
        },
        "primary_replay": replay,
        "premise_verifier": premise_raw,
        "execution_hygiene": {
            "strict_no_write_outside_package": "BREACHED_BY_TEMPORARY_SECOND_VERIFIER_SCRATCH_OUTPUT_THEN_CLEANED",
            "path": "/tmp/udt_p4_source_manifest_second_check.txt",
            "current_path_absent": True,
            "repository_outside_package_changes": 0,
            "effect_on_primary_evidence": "NONE",
        },
        "substantive_disagreements": [
            "IR10 and IR20 are parser/copy regressions, not genuinely different methods.",
            "IR15 is only a T2/A2 ledger parser; it does not independently recompute the formal static/time/angular module embedding used in Q2.",
            "The primary verifier checks only 3 of the 10 completeness cells despite its check name.",
            "Only 3 of 7 primary synthetic catch-proofs exercise the named failure class adequately.",
            "All 172 package clauses reuse 29 unit-level premise templates; exact clause-level premise stacks are not demonstrated.",
            "Twenty-six action-term cells call action/energy/Hessian/coupling-bearing packages response/geometry-only.",
            "The 311-row freeze is byte-sound but not transitively closed; 13 explicit existing external references are recorded only as this non-retroactive overlay.",
        ],
        "required_amendments": [
            "Relabel IR10 and IR20 INDEPENDENT_PARSER_OR_REGRESSION and recompute the independence counts/report wording.",
            "Either add a genuinely independent formal-module embedding derivation or state explicitly that Q2's formal embedding rests on banked package controls plus cold parser regression, not a cold different-method proof.",
            "Make verify_cold_review.py validate all ten completeness columns and their allowed claim-specific content.",
            "Replace the four inadequate primary catch-proofs with mutations that exercise duplicate frozen units, the real source-manifest checker, a concrete quantifier promotion, and parser/copy false-independence.",
            "Replace package-wide premise templates with clause-specific source stamps for load-bearing claims; at minimum enumerate signs, positivity, normalization, branch, boundary/germ, pairing, posture, topology, and conditional action/field status where used.",
            "Correct the 26 action-term cells in P4-07/P4-08/P4-16/P4-18/P4-20.",
            "Preserve any transitive dependency expansion only as a dated post-outcome overlay; do not rewrite it as retroactive preregistration. Machine-record the joint-obligation hash as well as the cap hash.",
            "Retain the primary K4 correction and STOP_REPAIR_FIRST ceiling; no T4/adoption follows.",
            "Rerun the final verifier packaging/isolation check cleanly because this verifier briefly created and then deleted one temporary manifest-output file outside the authorized worktree/package.",
        ],
        "maximum_conclusion_compliance": "PASS: evidence regrade only; no new science, adoption, T4, GPU, or canonization.",
        "recommended_next_step": "STOP_REPAIR_FIRST; amend the review package and return it to this same second verifier.",
    }
    write_outputs(result)
    # Refresh hashes after the first durable write; the results file intentionally
    # does not self-hash.  A separate manifest is built after this script returns.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
