#!/usr/bin/env python3
"""Exact nonlinear Cartan atlas for the registered UDT toric coframe."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import sympy as sp


HERE = Path(__file__).resolve().parent
DIM = 4
PAIRS = tuple((i, j) for i in range(DIM) for j in range(i + 1, DIM))
ETA = (-1, 1, 1, 1)

u0, u1, s0, s1, a0, a1, h0, h1, f2, f3 = sp.symbols(
    "u0 u1 s0 s1 a0 a1 h0 h1 f2 f3", real=True
)
CHANNELS = (u0, u1, s0, s1, a0, a1, h0, h1, f2, f3)
FAMILY = {
    u0: "PHI_ANHOLONOMY",
    u1: "PHI_ANHOLONOMY",
    s0: "ANGULAR_COMMON",
    s1: "ANGULAR_COMMON",
    a0: "ANGULAR_RECIPROCAL",
    a1: "ANGULAR_RECIPROCAL",
    h0: "ANGULAR_SHEAR",
    h1: "ANGULAR_SHEAR",
    f2: "CONNECTION_CURVATURE_1",
    f3: "CONNECTION_CURVATURE_2",
}
DERIV = {
    (direction, channel): sp.Symbol(f"E{direction}_{channel}", real=True)
    for direction in (0, 1)
    for channel in CHANNELS
}
DERIV_FAMILY = {symbol: FAMILY[channel] for (direction, channel), symbol in DERIV.items()}

# Sparse exterior forms: sorted basis-index tuple -> scalar coefficient.
Form = dict[tuple[int, ...], sp.Expr]


def clean(form: Form, substitutions: dict[sp.Symbol, sp.Expr] | None = None) -> Form:
    out: Form = {}
    for key, value in form.items():
        if substitutions:
            value = value.subs(substitutions)
        value = sp.factor(sp.expand(value))
        if value != 0:
            out[key] = value
    return out


def add(*forms: Form) -> Form:
    out: defaultdict[tuple[int, ...], sp.Expr] = defaultdict(lambda: sp.Integer(0))
    for form in forms:
        for key, value in form.items():
            out[key] += value
    return clean(dict(out))


def scale(value: sp.Expr, form: Form) -> Form:
    return clean({key: value * coefficient for key, coefficient in form.items()})


def wedge(left: Form, right: Form) -> Form:
    out: defaultdict[tuple[int, ...], sp.Expr] = defaultdict(lambda: sp.Integer(0))
    for left_key, left_value in left.items():
        for right_key, right_value in right.items():
            if set(left_key).intersection(right_key):
                continue
            inversions = sum(i > j for i in left_key for j in right_key)
            key = tuple(sorted(left_key + right_key))
            out[key] += (-1) ** inversions * left_value * right_value
    return clean(dict(out))


def one(index: int) -> Form:
    return {(index,): sp.Integer(1)}


K0 = sp.Matrix([[s0 / 2 - a0, h0], [0, s0 / 2 + a0]])
K1 = sp.Matrix([[s1 / 2 - a1, h1], [0, s1 / 2 + a1]])

DTHETA: list[Form] = [
    {(0, 1): u1},
    {(0, 1): u0},
    {(0, 1): f2, (0, 2): K0[0, 0], (0, 3): K0[0, 1],
     (1, 2): K1[0, 0], (1, 3): K1[0, 1]},
    {(0, 1): f3, (0, 3): K0[1, 1], (1, 3): K1[1, 1]},
]


def d_scalar(expression: sp.Expr) -> Form:
    return clean({
        (0,): sum(sp.diff(expression, channel) * DERIV[(0, channel)] for channel in CHANNELS),
        (1,): sum(sp.diff(expression, channel) * DERIV[(1, channel)] for channel in CHANNELS),
    })


def basis_form(key: tuple[int, ...]) -> Form:
    return {key: sp.Integer(1)} if key else {(): sp.Integer(1)}


def d_basis(key: tuple[int, ...]) -> Form:
    out: Form = {}
    for position, index in enumerate(key):
        term = wedge(basis_form(key[:position]), DTHETA[index])
        term = wedge(term, basis_form(key[position + 1 :]))
        out = add(out, scale((-1) ** position, term))
    return out


def exterior_d(form: Form) -> Form:
    out: Form = {}
    for key, coefficient in form.items():
        out = add(
            out,
            wedge(d_scalar(coefficient), basis_form(key)),
            scale(coefficient, d_basis(key)),
        )
    return out


MC_SUBS = {
    DERIV[(0, s1)]: DERIV[(1, s0)] - u1 * s0 - u0 * s1,
    DERIV[(0, a1)]: DERIV[(1, a0)] - u1 * a0 - u0 * a1,
    DERIV[(0, h1)]: (
        DERIV[(1, h0)] - u1 * h0 - u0 * h1 - 2 * a0 * h1 + 2 * a1 * h0
    ),
}


def form_string(form: Form) -> str:
    if not form:
        return "0"
    return " + ".join(
        f"({sp.sstr(value)}) theta{''.join(map(str, key))}"
        for key, value in sorted(form.items())
    )


def write_tsv(name: str, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def solve_connection() -> tuple[list[list[Form]], list[list[Form]], dict[sp.Symbol, sp.Expr]]:
    unknowns: list[sp.Symbol] = []
    lower: list[list[Form]] = [[{} for _ in range(DIM)] for _ in range(DIM)]
    for a, b in PAIRS:
        form: Form = {}
        for c in range(DIM):
            symbol = sp.Symbol(f"w{a}{b}_{c}", real=True)
            unknowns.append(symbol)
            form[(c,)] = symbol
        lower[a][b] = form
        lower[b][a] = scale(-1, form)

    mixed = [[scale(ETA[a], lower[a][b]) for b in range(DIM)] for a in range(DIM)]
    equations: list[sp.Expr] = []
    for a in range(DIM):
        torsion = DTHETA[a]
        for b in range(DIM):
            torsion = add(torsion, wedge(mixed[a][b], one(b)))
        equations.extend(torsion.get(pair, sp.Integer(0)) for pair in PAIRS)

    matrix, rhs = sp.linear_eq_to_matrix(equations, unknowns)
    solution_set = sp.linsolve((matrix, rhs), unknowns)
    solutions = list(solution_set)
    if len(solutions) != 1 or len(solutions[0]) != len(unknowns):
        raise AssertionError("Levi-Civita connection was not uniquely solved")
    solution = dict(zip(unknowns, solutions[0]))
    lower = [[clean(form, solution) for form in row] for row in lower]
    mixed = [[scale(ETA[a], lower[a][b]) for b in range(DIM)] for a in range(DIM)]
    return lower, mixed, solution


def curvature(mixed: list[list[Form]]) -> tuple[list[list[Form]], list[list[Form]]]:
    omega: list[list[Form]] = [[{} for _ in range(DIM)] for _ in range(DIM)]
    lower: list[list[Form]] = [[{} for _ in range(DIM)] for _ in range(DIM)]
    for a in range(DIM):
        for b in range(DIM):
            value = exterior_d(mixed[a][b])
            for c in range(DIM):
                value = add(value, wedge(mixed[a][c], mixed[c][b]))
            omega[a][b] = clean(value, MC_SUBS)
            lower[a][b] = scale(ETA[a], omega[a][b])
    return omega, lower


def riemann_component(
    curvature_lower: list[list[Form]], a: int, b: int, c: int, d: int
) -> sp.Expr:
    sign = 1
    if a == b or c == d:
        return sp.Integer(0)
    if a > b:
        a, b = b, a
        sign *= -1
    if c > d:
        c, d = d, c
        sign *= -1
    return sign * curvature_lower[a][b].get((c, d), 0)


def contractions(curvature_lower: list[list[Form]]) -> tuple[list[list[sp.Expr]], sp.Expr]:
    ricci = [[sp.Integer(0) for _ in range(DIM)] for _ in range(DIM)]
    for b in range(DIM):
        for d in range(DIM):
            ricci[b][d] = sp.factor(sum(
                ETA[a] * riemann_component(curvature_lower, a, b, a, d)
                for a in range(DIM)
            ))
    scalar = sp.factor(sum(ETA[b] * ricci[b][b] for b in range(DIM)))
    return ricci, scalar


def coupling_graph(curvature_lower: list[list[Form]]) -> list[dict[str, object]]:
    derivative_hits: defaultdict[tuple[str, str], list[str]] = defaultdict(list)
    quadratic_hits: defaultdict[tuple[str, str], list[str]] = defaultdict(list)
    all_variables = CHANNELS + tuple(DERIV.values())

    for a, b in PAIRS:
        for c, d in PAIRS:
            expression = sp.expand(curvature_lower[a][b].get((c, d), 0))
            component = f"Omega{a}{b}_{c}{d}"
            if expression == 0:
                continue
            polynomial = sp.Poly(expression, *all_variables)
            for monomial, coefficient in polynomial.terms():
                if coefficient == 0:
                    continue
                structural: list[sp.Symbol] = []
                derivatives: list[sp.Symbol] = []
                for variable, exponent in zip(all_variables, monomial):
                    target = derivatives if variable in DERIV_FAMILY else structural
                    target.extend([variable] * exponent)
                if len(derivatives) == 1 and not structural:
                    family = DERIV_FAMILY[derivatives[0]]
                    derivative_hits[(family, family)].append(component)
                elif not derivatives and len(structural) == 2:
                    families = sorted(FAMILY[item] for item in structural)
                    quadratic_hits[(families[0], families[1])].append(component)
                else:
                    raise AssertionError(
                        f"unexpected curvature monomial in {component}: {monomial} coefficient={coefficient}"
                    )

    rows: list[dict[str, object]] = []
    for kind, hits in (("DERIVATIVE", derivative_hits), ("QUADRATIC", quadratic_hits)):
        for left, right in sorted(hits):
            components = hits[(left, right)]
            rows.append({
                "coupling_kind": kind,
                "family_left": left,
                "family_right": right,
                "term_count": len(components),
                "component_count": len(set(components)),
                "components": ";".join(sorted(set(components))),
            })
    return rows


def completion_rows() -> list[dict[str, str]]:
    assessments = {
        "FC01": ("EXACT_ON_REGULAR_INTERIOR", "PHYSICAL_BOUNDARY_JETS_AND_FUNCTIONAL_OPEN"),
        "FC02": ("EXACT_AWAY_FROM_CAP", "ADAPTED_CAP_CHART_AND_PRIMITIVE_CAP_JETS_REQUIRED"),
        "FC03": ("EXACT_AWAY_FROM_CAPS", "TWO_ADAPTED_CAP_CHARTS_AND_GLUE_REQUIRED"),
        "FC04": ("EXACT_AWAY_FROM_CAPS", "TWO_ADAPTED_CAP_CHARTS_AND_UNIMODULAR_GLUE_REQUIRED"),
        "FC05": ("EXACT_AWAY_FROM_CAPS", "CAP_CHARTS_AND_LENS_GLUE_REQUIRED"),
        "FC06": ("EXACT_ON_REGULAR_COMPLEMENT", "NONPRIMITIVE_COLLAPSE_IS_SINGULAR_OR_ORBIFOLD"),
        "FC07": ("EXACT_IN_LOCAL_TORUS_CHARTS", "CHANNELS_MUST_GLUE_UNDER_GL2Z_MONODROMY"),
        "FC08": ("EXACT_OFF_REFLECTION_FIXED_SET", "COFRAME_LIFT_PARITY_AND_INTERFACE_JETS_REQUIRED"),
        "FC09": ("EXACT_IN_ORIENTED_LOCAL_CHARTS", "ORIENTATION_TWIST_AND_DET_MINUS_ONE_GLUE_REQUIRED"),
        "FC10": ("EXACT_ON_EACH_FIXED_RANK_REGULAR_STRATUM", "FINE_COFRAME_MAY_FAIL_AT_RANK_TRANSITION"),
        "FC11": ("LOCAL_WITNESS_IF_PLANE_IS_CONNECTION_HORIZONTAL", "GENERAL_ANHOLONOMIC_NO_ORBIT_BRANCH_NOT_GLOBALLY_COVERED"),
        "FC12": ("EXACT_ON_REGULAR_TORIC_INTERIOR", "PROFILE_ENDPOINT_AND_CAP_CLASS_REMAIN_OPEN"),
    }
    rows = []
    with (HERE / "COMPLETION_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            local, obstruction = assessments[row["class_id"]]
            rows.append({
                **row,
                "local_cartan_status": local,
                "global_obstruction": obstruction,
                "selection_status": "REGISTERED_NOT_SELECTED",
            })
    return rows


def abstract_second_bianchi() -> dict[str, int]:
    """Coefficient ledger for dOmega+wOmega-Omegaw by noncommuting word."""
    # d(domega)=0; d(omega wedge omega)=domega wedge omega-omega wedge domega.
    terms = [
        ("domega*omega", 1),
        ("omega*domega", -1),
        ("omega*domega", 1),
        ("omega*omega*omega", 1),
        ("domega*omega", -1),
        ("omega*omega*omega", -1),
    ]
    totals: defaultdict[str, int] = defaultdict(int)
    for word, coefficient in terms:
        totals[word] += coefficient
    return dict(totals)


def main() -> None:
    checks: dict[str, str] = {}

    with (HERE / "CHANNEL_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        registered_channels = list(csv.DictReader(handle, delimiter="\t"))
    if [row["symbol"] for row in registered_channels] != [str(item) for item in CHANNELS]:
        raise AssertionError("registered channel universe differs from calculation")
    checks["registered_channel_universe_exact"] = "PASS"
    with (HERE / "OUTPUT_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        registered_outputs = list(csv.DictReader(handle, delimiter="\t"))
    if [row["output_id"] for row in registered_outputs] != [f"O{i:02d}" for i in range(1, 12)]:
        raise AssertionError("registered output universe differs from calculation")
    checks["registered_output_universe_exact"] = "PASS"

    print("stage=structure_and_integrability", flush=True)
    d2_raw = [exterior_d(form) for form in DTHETA]
    d2_reduced = [clean(form, MC_SUBS) for form in d2_raw]
    if any(d2_reduced):
        raise AssertionError({index: form_string(form) for index, form in enumerate(d2_reduced) if form})
    checks["coframe_integrability_after_right_maurer_cartan"] = "PASS"

    expected_mc = {
        "sigma": DERIV[(0, s1)] - DERIV[(1, s0)] + u1 * s0 + u0 * s1,
        "alpha": DERIV[(0, a1)] - DERIV[(1, a0)] + u1 * a0 + u0 * a1,
        "shear": (
            DERIV[(0, h1)] - DERIV[(1, h0)] + u1 * h0 + u0 * h1
            + 2 * a0 * h1 - 2 * a1 * h0
        ),
    }
    diagonal_minus = d2_raw[2][(0, 1, 2)]
    shear_raw = d2_raw[2][(0, 1, 3)]
    diagonal_plus = d2_raw[3][(0, 1, 3)]
    reconstructed_mc = {
        "sigma": sp.factor(diagonal_minus + diagonal_plus),
        "alpha": sp.factor((diagonal_plus - diagonal_minus) / 2),
        "shear": sp.factor(shear_raw),
    }
    if any(sp.simplify(reconstructed_mc[name] - expected) != 0
           for name, expected in expected_mc.items()):
        raise AssertionError((reconstructed_mc, expected_mc))
    checks["three_maurer_cartan_components_exposed"] = "PASS"

    print("stage=levi_civita_connection", flush=True)
    lower_connection, mixed_connection, solution = solve_connection()
    if len(solution) != 24:
        raise AssertionError("connection coefficient count")
    checks["connection_24_slots_uniquely_solved"] = "PASS"

    for a in range(DIM):
        torsion = DTHETA[a]
        for b in range(DIM):
            torsion = add(torsion, wedge(mixed_connection[a][b], one(b)))
        if clean(torsion):
            raise AssertionError(("torsion", a, torsion))
    checks["torsion_zero_exact"] = "PASS"
    if any(add(lower_connection[a][b], lower_connection[b][a])
           for a in range(DIM) for b in range(DIM)):
        raise AssertionError("connection metric antisymmetry")
    checks["connection_metric_antisymmetry"] = "PASS"

    print("stage=curvature", flush=True)
    curvature_mixed, curvature_lower = curvature(mixed_connection)
    for a in range(DIM):
        for b in range(DIM):
            if add(curvature_lower[a][b], curvature_lower[b][a]):
                raise AssertionError(("curvature antisymmetry", a, b))
    checks["curvature_metric_antisymmetry"] = "PASS"
    for a, b in PAIRS:
        for c, d in PAIRS:
            if sp.simplify(
                curvature_lower[a][b].get((c, d), 0)
                - curvature_lower[c][d].get((a, b), 0)
            ) != 0:
                raise AssertionError(("Riemann pair exchange", a, b, c, d))
    checks["riemann_pair_exchange_symmetry"] = "PASS"

    ricci, scalar_curvature = contractions(curvature_lower)
    if any(sp.simplify(ricci[a][b] - ricci[b][a]) != 0
           for a in range(DIM) for b in range(DIM)):
        raise AssertionError("Ricci symmetry")
    checks["ricci_symmetry"] = "PASS"

    # Regression bridge to the independently banked neutral coordinate-jet
    # scalar-curvature result. Frame derivatives contain anholonomy terms even
    # when coordinate second derivatives are zero.
    rate_names = tuple(
        f"d{direction}_{name}"
        for direction in (0, 1)
        for name in ("phi", "sigma", "alpha", "k", "S10", "S11", "S20", "S21")
    )
    rates = dict(zip(rate_names, sp.symbols(" ".join(rate_names), real=True)))
    neutral_subs = {symbol: sp.Integer(0) for symbol in DERIV.values()}
    neutral_subs.update({
        u0: rates["d0_phi"], u1: rates["d1_phi"],
        s0: rates["d0_sigma"], s1: rates["d1_sigma"],
        a0: rates["d0_alpha"], a1: rates["d1_alpha"],
        h0: rates["d0_k"], h1: rates["d1_k"],
        f2: rates["d0_S11"] - rates["d1_S10"],
        f3: rates["d0_S21"] - rates["d1_S20"],
        DERIV[(0, u0)]: rates["d0_phi"] ** 2,
        DERIV[(1, u1)]: -rates["d1_phi"] ** 2,
        DERIV[(0, s0)]: rates["d0_phi"] * rates["d0_sigma"],
        DERIV[(1, s1)]: -rates["d1_phi"] * rates["d1_sigma"],
    })
    old_result = json.loads(
        (HERE.parent / "udt_metric_orchestra_rehearsal_2026-07-25" / "ALGEBRA_RESULT.json")
        .read_text(encoding="utf-8")
    )
    old_rate = sp.sympify(old_result["exact_objects"]["scalar_curvature_rate_form"], locals=rates)
    if sp.simplify(scalar_curvature.subs(neutral_subs) - old_rate) != 0:
        raise AssertionError(("neutral scalar regression", scalar_curvature.subs(neutral_subs), old_rate))
    checks["neutral_scalar_curvature_matches_banked_orchestra"] = "PASS"

    first_bianchi: list[Form] = []
    for a in range(DIM):
        residual: Form = {}
        for b in range(DIM):
            residual = add(residual, wedge(curvature_mixed[a][b], one(b)))
        residual = clean(residual, MC_SUBS)
        first_bianchi.append(residual)
    if any(first_bianchi):
        raise AssertionError({a: form_string(value) for a, value in enumerate(first_bianchi) if value})
    checks["first_bianchi_exact"] = "PASS"

    second = abstract_second_bianchi()
    if any(second.values()):
        raise AssertionError(second)
    checks["second_bianchi_graded_algebra_exact"] = "PASS"

    structure_rows = [
        {"coframe_leg": f"theta{a}", "dtheta": form_string(DTHETA[a])}
        for a in range(DIM)
    ]
    write_tsv("STRUCTURE_EQUATIONS.tsv", ["coframe_leg", "dtheta"], structure_rows)

    integrability_rows = [
        {"identity": name, "raw_expression": sp.sstr(expression), "reduced": "0"}
        for name, expression in expected_mc.items()
    ]
    integrability_rows.append({
        "identity": "scalar_frame_commutator",
        "raw_expression": "[E0,E1]h = -u1 E0(h) - u0 E1(h) - f2 E2(h) - f3 E3(h)",
        "reduced": "-u1 E0(h) - u0 E1(h) for torus-invariant h",
    })
    write_tsv("COFRAME_INTEGRABILITY.tsv", ["identity", "raw_expression", "reduced"], integrability_rows)

    connection_rows = []
    for a, b in PAIRS:
        for c in range(DIM):
            connection_rows.append({
                "lower_pair": f"{a}{b}",
                "basis_leg": str(c),
                "coefficient": sp.sstr(lower_connection[a][b].get((c,), 0)),
            })
    write_tsv(
        "CONNECTION_COEFFICIENTS.tsv",
        ["lower_pair", "basis_leg", "coefficient"],
        connection_rows,
    )
    nonzero_connection = sum(row["coefficient"] != "0" for row in connection_rows)

    curvature_rows = []
    nonzero_curvature = 0
    for a, b in PAIRS:
        for c, d in PAIRS:
            expression = curvature_lower[a][b].get((c, d), 0)
            nonzero_curvature += int(expression != 0)
            curvature_rows.append({
                "lower_pair": f"{a}{b}",
                "two_form_leg": f"{c}{d}",
                "coefficient": sp.sstr(expression),
                "zero_status": "NONZERO_EXACT" if expression != 0 else "ZERO_EXACT",
            })
    write_tsv(
        "CURVATURE_COMPONENTS.tsv",
        ["lower_pair", "two_form_leg", "coefficient", "zero_status"],
        curvature_rows,
    )

    contraction_rows = []
    for a in range(DIM):
        for b in range(a, DIM):
            contraction_rows.append({
                "parent_output": "O04",
                "contraction": f"Ricci{a}{b}",
                "expression": sp.sstr(ricci[a][b]),
            })
    contraction_rows.append({
        "parent_output": "O04",
        "contraction": "scalar_curvature",
        "expression": sp.sstr(scalar_curvature),
    })
    write_tsv(
        "CURVATURE_CONTRACTIONS.tsv",
        ["parent_output", "contraction", "expression"],
        contraction_rows,
    )

    graph_rows = coupling_graph(curvature_lower)
    write_tsv(
        "NONLINEAR_CHANNEL_GRAPH.tsv",
        ["coupling_kind", "family_left", "family_right", "term_count", "component_count", "components"],
        graph_rows,
    )
    quadratic_pairs = {
        tuple(sorted((row["family_left"], row["family_right"])))
        for row in graph_rows if row["coupling_kind"] == "QUADRATIC"
    }
    families = sorted(set(FAMILY.values()))
    adjacency = {family: set() for family in families}
    for left, right in quadratic_pairs:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    pending = [families[0]]
    while pending:
        node = pending.pop()
        if node in seen:
            continue
        seen.add(node)
        pending.extend(adjacency[node] - seen)
    if seen != set(families):
        raise AssertionError(("disconnected nonlinear graph", seen, families))
    checks["six_family_quadratic_graph_connected"] = "PASS"
    absent_pairs = {
        tuple(sorted(("PHI_ANHOLONOMY", "CONNECTION_CURVATURE_1"))),
        tuple(sorted(("PHI_ANHOLONOMY", "CONNECTION_CURVATURE_2"))),
    }
    if absent_pairs.intersection(quadratic_pairs):
        raise AssertionError("direct phi-connection-curvature edge unexpectedly present")
    checks["no_direct_phi_connection_curvature_quadratic_edge"] = "PASS"

    completions = completion_rows()
    if len(completions) != 12 or len({row["class_id"] for row in completions}) != 12:
        raise AssertionError("completion universe coverage")
    if next(row for row in completions if row["class_id"] == "FC11")["local_cartan_status"].startswith("EXACT"):
        raise AssertionError("FC11 global toric overclaim")
    checks["twelve_completion_classes_exactly_once"] = "PASS"
    checks["FC11_general_non_toric_scope_preserved"] = "PASS"
    write_tsv(
        "COMPLETION_APPLICABILITY.tsv",
        ["class_id", "class_name", "frozen_source", "local_cartan_status", "global_obstruction", "selection_status"],
        completions,
    )

    write_tsv(
        "IDENTITY_DYNAMICS_LEDGER.tsv",
        ["object", "status", "meaning", "does_not_supply"],
        [
            {"object": "coframe_structure", "status": "DERIVED_IN_REGISTERED_DOMAIN", "meaning": "exact exterior derivatives of the complete coframe", "does_not_supply": "on_shell_profile"},
            {"object": "right_Maurer_Cartan", "status": "DERIVED_IDENTITY", "meaning": "integrability of D and its structural channels", "does_not_supply": "field_equation"},
            {"object": "Levi_Civita_connection", "status": "DERIVED_GIVEN_METRIC", "meaning": "unique torsion_free metric_compatible connection", "does_not_supply": "action_or_source"},
            {"object": "Riemann_curvature", "status": "DERIVED_GIVEN_METRIC", "meaning": "nonlinear geometric response of arbitrary off_shell amplitudes", "does_not_supply": "physical_response_law"},
            {"object": "first_and_second_Bianchi", "status": "DERIVED_IDENTITIES", "meaning": "geometric consistency of curvature and torsion", "does_not_supply": "dynamics_or_selector"},
            {"object": "global_local_response_one_form", "status": "OPEN_NOT_DERIVED", "meaning": "required directional response linking inventory to geometry", "does_not_supply": "not_available"},
            {"object": "density_to_geometry_map", "status": "OPEN_NOT_DERIVED", "meaning": "required before any density bracket", "does_not_supply": "not_available"},
        ],
    )

    result = {
        "status": "PASS",
        "scope": "exact nonlinear regular toric coframe; arbitrary smooth x0,x amplitudes; off shell",
        "counts": {
            "registered_channels": len(CHANNELS),
            "registered_outputs": len(registered_outputs),
            "channel_families": len(set(FAMILY.values())),
            "connection_pair_labeled_slots": len(connection_rows),
            "nonzero_connection_slots": nonzero_connection,
            "curvature_pair_labeled_slots": len(curvature_rows),
            "generic_four_dimensional_Riemann_algebraic_slots": 20,
            "nonzero_curvature_coefficients": nonzero_curvature,
            "curvature_contraction_summaries": len(contraction_rows),
            "nonlinear_graph_rows": len(graph_rows),
            "quadratic_family_pairs_present": len(quadratic_pairs),
            "quadratic_family_pairs_possible_with_self": len(families) * (len(families) + 1) // 2,
            "direct_quadratic_family_pairs_absent": ["PHI_ANHOLONOMY--CONNECTION_CURVATURE_1", "PHI_ANHOLONOMY--CONNECTION_CURVATURE_2"],
            "completion_classes": len(completions),
        },
        "checks": checks,
        "interpretation": {
            "cartan_and_bianchi": "DERIVED_GEOMETRIC_IDENTITIES_IN_REGISTERED_DOMAIN",
            "physical_response_one_form": "NOT_SUPPLIED_BY_IDENTITIES",
            "action_source_boundary_density": "OPEN_NOT_INPUT",
            "density_sweep": "DEFERRED",
        },
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
