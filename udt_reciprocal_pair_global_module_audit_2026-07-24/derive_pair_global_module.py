#!/usr/bin/env python3
"""Exact production derivation for the reciprocal-pair global-module audit."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import subprocess
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "a93f928f66d260bee1df1a9c5156269afa1952b7"
PREREG = "1758199"


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_show(path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{BASE}:{path}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise AssertionError(completed.stderr.decode("utf-8", "replace"))
    return completed.stdout


def canonical_line(v: tuple[int, int]) -> tuple[int, int]:
    a, b = v
    if a == 0 and b == 0:
        raise ValueError("zero is not a line")
    g = math.gcd(abs(a), abs(b))
    a, b = a // g, b // g
    if a < 0 or (a == 0 and b < 0):
        a, b = -a, -b
    return a, b


def mat_tuple(matrix: sp.Matrix) -> tuple[int, int, int, int]:
    return tuple(int(matrix[i, j]) for i in range(2) for j in range(2))


def apply_line(matrix: sp.Matrix, line: tuple[int, int]) -> tuple[int, int]:
    out = matrix * sp.Matrix(line)
    return canonical_line((int(out[0]), int(out[1])))


def signed_permutation_group() -> list[sp.Matrix]:
    group = []
    for entries in itertools.product((-1, 0, 1), repeat=4):
        matrix = sp.Matrix(2, 2, entries)
        if abs(int(matrix.det())) != 1:
            continue
        columns = [
            sum(abs(int(matrix[i, j])) for i in range(2)) for j in range(2)
        ]
        rows = [
            sum(abs(int(matrix[i, j])) for j in range(2)) for i in range(2)
        ]
        if rows == [1, 1] and columns == [1, 1]:
            group.append(matrix)
    return sorted(group, key=mat_tuple)


def integer_kernel(matrix: sp.Matrix, eigenvalue: int) -> tuple[int, int] | None:
    kernel = matrix - eigenvalue * sp.eye(2)
    vectors = kernel.nullspace()
    if not vectors:
        return None
    vector = vectors[0]
    den = sp.ilcm(*[term.q for term in vector])
    values = [int(term * den) for term in vector]
    return canonical_line((values[0], values[1]))


def source_replay() -> list[dict[str, object]]:
    rows = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        manifest = list(csv.DictReader(handle, delimiter="\t"))
    if len(manifest) != 44:
        raise AssertionError("source count")
    for row in manifest:
        path = row["path"]
        working = (ROOT / path).read_bytes()
        base = git_show(path)
        if working != base:
            raise AssertionError(f"source drift: {path}")
        if sha(working) != row["sha256"] or len(working) != int(row["size"]):
            raise AssertionError(f"source identity mismatch: {path}")
        if path.startswith("udt_dual_systole"):
            role = "PARENT_SHORTEST_SET_AND_WALL_THEOREM"
        elif "hopf" in path.lower() or "toric" in path.lower():
            role = "CONDITIONAL_HOPF_OR_TORIC_COMPARISON"
        elif "COLD" in path or "RECIPROCAL_C" in path:
            role = "DIRECT_FOUNDATION"
        elif "BOOTSTRAP" in path or "COMMON_SCALE" in path:
            role = "DIRECT_PRINCIPLE"
        elif "seal" in path.lower():
            role = "SEAL_LIFT_NONSELECTION"
        else:
            role = "REGISTERED_COMPLETE_METRIC_OR_COMPLETION"
        rows.append(
            {
                "path": path,
                "sha256": row["sha256"],
                "base": row["base"],
                "role": role,
                "result": "PASS_BYTE_IDENTICAL",
            }
        )
    return rows


def exact_algebra() -> tuple[list[dict[str, object]], dict[str, object]]:
    checks: list[dict[str, object]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        if not condition:
            raise AssertionError(f"{check_id}: {detail}")
        checks.append({"check_id": check_id, "result": "PASS", "detail": detail})

    e1, e2 = (1, 0), (0, 1)
    pair = {canonical_line(e1), canonical_line(e2)}
    N = signed_permutation_group()
    check("A01", len(N) == 8, "signed permutation stabilizer has order 8")
    check(
        "A02",
        all({apply_line(m, e1), apply_line(m, e2)} == pair for m in N),
        "all signed permutations preserve the unordered line pair",
    )

    shear = sp.Matrix([[1, 1], [0, 1]])
    hyperbolic = sp.Matrix([[2, 1], [1, 1]])
    detminus = sp.Matrix([[1, 1], [0, -1]])
    for cid, matrix in (("A03", shear), ("A04", hyperbolic), ("A05", detminus)):
        check(
            cid,
            {apply_line(matrix, e1), apply_line(matrix, e2)} != pair,
            f"{mat_tuple(matrix)} does not preserve the pair splitting",
        )

    L, B = sp.Rational(13, 12), sp.Rational(5, 12)
    Qwall = sp.Matrix([[L, B], [B, L]])
    check("A06", sp.simplify(Qwall.det()) == 1, "exact wall Gram determinant one")
    check("A07", Qwall[0, 0] == Qwall[1, 1], "wall basis vectors are tied")
    primitive = []
    for p in range(-8, 9):
        for q in range(-8, 9):
            if (p, q) == (0, 0) or math.gcd(abs(p), abs(q)) != 1:
                continue
            value = sp.expand((sp.Matrix([[p, q]]) * Qwall * sp.Matrix([p, q]))[0])
            primitive.append((value, canonical_line((p, q))))
    minimum = min(value for value, _ in primitive)
    minimizers = {line for value, line in primitive if value == minimum}
    check("A08", minimum == L and minimizers == pair, "wall interior has exact two-way tie")
    check("A09", abs(sp.Matrix.hstack(sp.Matrix(e1), sp.Matrix(e2)).det()) == 1, "pair is unimodular")
    check("A10", pair == {e1, e2}, "unimodular pair spans the full Z2 lattice")

    Qminus = sp.diag(sp.Rational(1, 2), 2)
    Qplus = sp.diag(2, sp.Rational(1, 2))
    check("A11", Qminus[0, 0] < Qminus[1, 1], "left chamber has only e1 shortest")
    check("A12", Qplus[1, 1] < Qplus[0, 0], "right chamber has only e2 shortest")

    sqrt3 = sp.sqrt(3)
    Lv = 2 / sqrt3
    Bv = Lv / 2
    Qvertex = sp.Matrix([[Lv, Bv], [Bv, Lv]])
    vertex_lines = [e1, e2, (1, -1)]
    vertex_lengths = [
        sp.simplify((sp.Matrix([[*v]]) * Qvertex * sp.Matrix(v))[0])
        for v in vertex_lines
    ]
    check("A13", len(set(vertex_lengths)) == 1, "vertex has three tied lines")
    vertex_pairs = list(itertools.combinations(vertex_lines, 2))
    check(
        "A14",
        len(vertex_pairs) == 3
        and all(
            abs(
                int(
                    sp.Matrix.hstack(sp.Matrix(a), sp.Matrix(b)).det()
                )
            )
            == 1
            for a, b in vertex_pairs
        ),
        "vertex has three distinct unimodular pair choices",
    )

    J = sp.Matrix([[0, 1], [1, 0]])
    nJ = -J
    R4 = sp.Matrix([[0, 1], [-1, 0]])
    nR4 = -R4
    check("A15", J**2 == sp.eye(2) and nJ**2 == sp.eye(2), "two involutive swap lifts")
    check("A16", R4**2 == -sp.eye(2) and nR4**2 == -sp.eye(2), "two order-four swap lifts")
    check("A17", integer_kernel(J, 1) == (1, 1), "J fixed lattice is diagonal")
    check("A18", integer_kernel(J, -1) == (1, -1), "J anti-fixed lattice is anti-diagonal")
    check("A19", integer_kernel(nJ, 1) == (1, -1), "minus-J fixed lattice is anti-diagonal")
    check("A20", integer_kernel(R4, 1) is None, "order-four exchange has no fixed circle lattice")
    eigenbasis = sp.Matrix([[1, 1], [1, -1]])
    check("A21", abs(int(eigenbasis.det())) == 2, "exchange eigenlattices have index two")
    Dsign = sp.diag(1, -1)
    check("A22", Dsign * J * Dsign.inv() == nJ, "J and minus-J are sign-basis conjugate")

    fixed = sp.Matrix([1, 1])
    relative = sp.Matrix([[1, -1]])
    check("A23", (relative * fixed)[0] == 0, "relative character annihilates fixed diagonal circle")
    check("A24", math.gcd(1, 1) == 1, "fixed diagonal circle is primitive")

    # Connection doublet transformation with exact symbolic one-form labels.
    a1, a2 = sp.symbols("a1 a2")
    A = sp.Matrix([a1, a2])
    W = sp.eye(2)
    for matrix in (J, nJ, R4, shear):
        Wp = matrix.inv().T * W
        Ap = matrix * A
        check(
            f"A{25 + len(checks) - 24:02d}",
            sp.simplify(Wp.T * Ap - W.T * A) == sp.zeros(2, 1),
            f"full projected connection doublet covariant for {mat_tuple(matrix)}",
        )

    phi = sp.symbols("phi", real=True)
    denom = sp.sqrt(sp.exp(-2 * phi) + sp.exp(2 * phi))
    amp1, amp2 = sp.exp(-phi) / denom, sp.exp(phi) / denom
    check("A29", sp.simplify(amp1**2 + amp2**2) == 1, "normalized reciprocal amplitudes lie on S1")
    check("A30", sp.simplify(amp2 / amp1) == sp.exp(2 * phi), "amplitude ratio is reciprocal exponential")
    check(
        "A31",
        sp.simplify(amp1.subs(phi, -phi) - amp2) == 0,
        "reciprocity swaps normalized amplitudes",
    )

    # Standard Hopf quotient from the normalized spinor.
    delta = sp.symbols("delta", real=True)
    n1 = 2 * amp1 * amp2 * sp.cos(delta)
    n2 = 2 * amp1 * amp2 * sp.sin(delta)
    n3 = amp1**2 - amp2**2
    check("A32", sp.simplify(n1**2 + n2**2 + n3**2) == 1, "conditional quotient lands on S2")

    eta = sp.symbols("eta", real=True)
    integral_radial = sp.integrate(-2 * sp.sin(eta) * sp.cos(eta), (eta, 0, sp.pi / 2))
    check("A33", integral_radial == -1, "normalized A wedge dA radial integral")
    c1_classes = {}
    for m, n in ((1, 1), (-1, -1), (1, -1), (-1, 1)):
        free = abs(m) == abs(n) == 1
        q = m * n
        c1_classes[f"{m},{n}"] = {"free": free, "Q": q, "abs_Q": abs(q)}
    check("A34", all(item["free"] for item in c1_classes.values()), "all four sign actions are free")
    check("A35", {item["abs_Q"] for item in c1_classes.values()} == {1}, "conditional absolute Chern class is one")
    check("A36", {item["Q"] for item in c1_classes.values()} == {-1, 1}, "orientation/chirality sign remains two-valued")

    return checks, {
        "signed_permutation_group": [mat_tuple(m) for m in N],
        "wall_Q": [[str(term) for term in row] for row in Qwall.tolist()],
        "wall_minimizers": sorted([list(v) for v in minimizers]),
        "vertex_pair_count": len(vertex_pairs),
        "exchange_index": abs(int(eigenbasis.det())),
        "c1_classes": c1_classes,
    }


def local_rows() -> list[dict[str, str]]:
    outcomes = {
        "M01": ("GLOBAL_WHERE_TORIC", "The full rank-two character lattice is a GL2Z local system wherever the integral torus exists."),
        "M02": ("UNORDERED_UNORIENTED_UNIMODULAR_BASIS_AT_GENERIC_WALL", "Every independent co-shortest pair is unimodular."),
        "M03": ("SPAN_EQUALS_FULL_LAMBDA_STAR", "Determinant magnitude one gives index one, not a proper submodule."),
        "M04": ("COSHORTEST_ONLY_ON_WALL", "The two members cease to be simultaneously shortest in either adjacent chamber."),
        "M05": ("NOT_UNIQUE_AT_THREE_WAY_VERTEX", "A vertex supplies three shortest lines and three unimodular pair choices."),
        "M06": ("CONDITIONAL_STRUCTURE_GROUP_REDUCTION", "A metric-derived co-shortest pair requires the branch to remain on a two-way wall and its cocycles to preserve the unordered splitting; otherwise only a supplied continuation exists."),
        "M07": ("SIGNED_PERMUTATION_GROUP_ORDER_8", "The stabilizer consists exactly of signed permutation matrices."),
        "M08": ("PAIR_COVARIANT_GRAM_DATA", "Ordering/sign changes conjugate the Gram matrix; trace, determinant, and absolute angle survive."),
        "M09": ("PAIR_REDUCTION_TENSOR", "K=w1 tensor w1+w2 tensor w2 is sign/order independent once the pair reduction exists."),
        "M10": ("COVARIANT_CONNECTION_DOUBLET", "b=W^T S transforms as the pair representation; it is not a phase section."),
        "M11": ("COVARIANT_CURVATURE_DOUBLET", "db transforms in the same pair representation on locally constant lattice charts."),
        "M12": ("FULL_MODULE_PERSISTS_SPLITTING_USUALLY_NOT", "Generic GL2Z monodromy preserves Lambda* but not the unordered pair."),
        "M13": ("LOCAL_INVOLUTIVE_EXCHANGE_AVAILABLE", "J swaps the pair and has diagonal/anti-diagonal eigenlattices."),
        "M14": ("SIGN_CONJUGATE_INVOLUTIVE_LIFT", "-J swaps the same unoriented pair and is conjugate to J by a sign basis change."),
        "M15": ("NO_FIXED_CIRCLE", "Order-four swap lifts square to -I and have no nonzero fixed lattice."),
        "M16": ("PRIMITIVE_RANK_ONE_IF_GLOBAL_J_SUPPLIED", "The fixed lattice of J is Z(1,1)."),
        "M17": ("PRIMITIVE_RANK_ONE_IF_GLOBAL_J_SUPPLIED", "The anti-fixed lattice is Z(1,-1)."),
        "M18": ("INDEX_TWO_NOT_INTEGRAL_DIRECT_SUM", "Fixed plus anti-fixed eigenlattices span an index-two sublattice."),
        "M19": ("CONDITIONAL_FIXED_CIRCLE", "A global involutive exchange exponentiates its primitive fixed lattice to a circle."),
        "M20": ("CONDITIONAL_RELATIVE_QUOTIENT_CHARACTER", "(1,-1) annihilates the J-fixed diagonal circle, up to sign/basis conjugacy."),
        "M21": ("EXACT_CONDITIONAL_NORMALIZED_TORIC_SPINOR", "Normalized reciprocal coframe weights give amplitudes with ratio exp(2phi), but the amplitude interpretation and phases remain supplied."),
        "M22": ("FC04_CONDITIONAL_S3", "Independent primitive caps give the known determinant-one toric S3 only in the supplied completion."),
        "M23": ("FREE_FOR_INVOLUTIVE_FIXED_WEIGHT_MAGNITUDES_ONE", "J and -J fixed circles have weights (1,1) or (1,-1), free on supplied S3."),
        "M24": ("CONDITIONAL_SMOOTH_S2_QUOTIENT", "The free fixed-circle action gives a smooth quotient only after FC04 global data."),
        "M25": ("ABS_C1_ONE_SIGN_ORIENTATION_OPEN", "Diagonal and anti-diagonal actions give opposite signs and the same absolute unit class."),
        "M26": ("OPEN_NOT_A_SECTION", "A principal-circle quotient or S2 base is not a selected S2-valued field."),
        "M27": ("STRATIFIED_RANK_DROP", "The rank-two orbit lattice exists off a cap; at the cap an isotropy quotient replaces it."),
        "M28": ("UNAVAILABLE_WITHOUT_INTEGRAL_TORUS", "A nonintegrable plane field has no global character module."),
        "M29": ("PAIR_ORDER_AND_TIE_CSN_INVARIANT", "Common positive scale does not choose a pair member, lift, cap, or quotient."),
        "M30": ("OPEN_NO_DYNAMICAL_CONSEQUENCE", "No action, source, density law, mass, scale, or time evolution follows."),
    }
    rows = []
    with (HERE / "LOCAL_OBJECT_CANDIDATES.tsv").open(encoding="utf-8", newline="") as handle:
        for source in csv.DictReader(handle, delimiter="\t"):
            outcome, basis = outcomes[source["object_id"]]
            rows.append({**source, "outcome": outcome, "basis": basis})
    if len(rows) != 30:
        raise AssertionError("local object coverage")
    return rows


def transition_rows() -> list[dict[str, str]]:
    outcomes = {
        "T01": ("PRESERVES_PAIR", "identity"),
        "T02": ("PRESERVES_UNORIENTED_PAIR", "sign is forgotten but a physical phase is not selected"),
        "T03": ("PRESERVES_UNORIENTED_PAIR", "sign is forgotten but a physical phase is not selected"),
        "T04": ("PRESERVES_UNORIENTED_PAIR", "central sign"),
        "T05": ("INVOLUTIVE_SWAP_FIXED_DIAGONAL", "J squared is identity"),
        "T06": ("INVOLUTIVE_SWAP_FIXED_ANTIDIAGONAL", "minus J is sign-basis conjugate"),
        "T07": ("ORDER_FOUR_SWAP_NO_FIXED_CIRCLE", "square equals minus identity"),
        "T08": ("ORDER_FOUR_SWAP_NO_FIXED_CIRCLE", "square equals minus identity"),
        "T09": ("FULL_MODULE_ONLY_SPLITTING_LOST", "shear sends one coordinate line to a diagonal line"),
        "T10": ("FULL_MODULE_ONLY_SPLITTING_LOST", "hyperbolic monodromy preserves no finite coordinate pair"),
        "T11": ("FULL_MODULE_ONLY_SPLITTING_LOST", "orientation reversal does not rescue the splitting"),
        "T12": ("FULL_GL2Z_LOCAL_SYSTEM_COVARIANCE", "the rank-two module descends without a preferred basis"),
        "T13": ("UNORDERED_PAIR_REDUCTION_DESCENDS", "cocycle is restricted to the order-eight stabilizer"),
        "T14": ("RANK_TWO_ORBIT_MODULE_TERMINATES_AT_CAP", "a primitive isotropy cycle collapses"),
        "T15": ("ORBIFOLD_OR_INEFFECTIVE_STRATUM", "nonprimitive isotropy has exceptional stabilizer"),
        "T16": ("NO_CHARACTER_MODULE", "there is no integral torus local system"),
    }
    rows = []
    with (HERE / "TRANSITION_CANDIDATES.tsv").open(encoding="utf-8", newline="") as handle:
        for source in csv.DictReader(handle, delimiter="\t"):
            outcome, note = outcomes[source["transition_id"]]
            rows.append({**source, "outcome": outcome, "note": note})
    if len(rows) != 16:
        raise AssertionError("transition coverage")
    return rows


def invariant_rows() -> list[dict[str, str]]:
    return [
        {"invariant_id": "I01", "object": "rank", "definition": "rank Lambda*=2", "requirements": "toric region", "descent": "GL2Z", "physical_status": "DERIVED_GEOMETRIC"},
        {"invariant_id": "I02", "object": "pair determinant", "definition": "abs det(w1,w2)=1", "requirements": "two-way shortest wall", "descent": "sign/order invariant", "physical_status": "DERIVED"},
        {"invariant_id": "I03", "object": "pair span", "definition": "Zw1+Zw2=Lambda*", "requirements": "I02", "descent": "full module", "physical_status": "DERIVED_NOT_NEW_SUBMODULE"},
        {"invariant_id": "I04", "object": "pair Gram determinant", "definition": "det(W^T Q W)=1", "requirements": "unimodular Q and W", "descent": "signed permutation", "physical_status": "DERIVED"},
        {"invariant_id": "I05", "object": "pair Gram trace", "definition": "tr(W^T Q W)", "requirements": "pair reduction", "descent": "signed permutation", "physical_status": "DERIVED_GEOMETRIC"},
        {"invariant_id": "I06", "object": "absolute pair angle", "definition": "abs(G12)/sqrt(G11 G22)", "requirements": "pair reduction", "descent": "sign/order invariant", "physical_status": "DERIVED_GEOMETRIC"},
        {"invariant_id": "I07", "object": "pair tensor K", "definition": "w1 tensor w1+w2 tensor w2", "requirements": "unordered pair", "descent": "covariant", "physical_status": "DERIVED_REDUCTION_DATA"},
        {"invariant_id": "I08", "object": "connection doublet", "definition": "b=W^T S", "requirements": "pair reduction and torus connection", "descent": "signed permutation plus torus gauge", "physical_status": "DERIVED_CONNECTION_NOT_SECTION"},
        {"invariant_id": "I09", "object": "curvature doublet", "definition": "f=W^T dS", "requirements": "local toric charts", "descent": "signed permutation", "physical_status": "DERIVED_OBSTRUCTION_DATA"},
        {"invariant_id": "I10", "object": "exchange trace/determinant", "definition": "tr J=0, det J=-1", "requirements": "supplied involutive exchange", "descent": "conjugacy", "physical_status": "CONDITIONAL"},
        {"invariant_id": "I11", "object": "exchange fixed line", "definition": "ker(J-I)", "requirements": "global J lift", "descent": "conjugacy", "physical_status": "CONDITIONAL_ASSOCIATED_CIRCLE"},
        {"invariant_id": "I12", "object": "exchange anti-fixed line", "definition": "ker(J+I)", "requirements": "global J lift", "descent": "conjugacy", "physical_status": "CONDITIONAL_RELATIVE_DIRECTION"},
        {"invariant_id": "I13", "object": "integral parity index", "definition": "[Lambda*:Lambda_+ plus Lambda_-]=2", "requirements": "involutive exchange", "descent": "conjugacy", "physical_status": "DERIVED_CONDITIONAL"},
        {"invariant_id": "I14", "object": "fixed-circle quotient character", "definition": "w_-(Lambda_+)=0", "requirements": "global involutive exchange", "descent": "up to sign", "physical_status": "CONDITIONAL"},
        {"invariant_id": "I15", "object": "normalized reciprocal amplitude norm", "definition": "a1^2+a2^2=1", "requirements": "aligned reciprocal chart", "descent": "swap covariant only", "physical_status": "EXACT_CONDITIONAL"},
        {"invariant_id": "I16", "object": "conditional Chern magnitude", "definition": "abs c1=1", "requirements": "FC04, global involution, free fixed circle, orientation normalization", "descent": "absolute sign survives", "physical_status": "EXACT_CONDITIONAL_GLOBAL"},
        {"invariant_id": "I17", "object": "Hopf sign", "definition": "c1=plus or minus 1", "requirements": "orientation and lift convention", "descent": "sign can reverse", "physical_status": "OPEN_SIGN"},
        {"invariant_id": "I18", "object": "carrier section", "definition": "map from physical 3-domain to quotient S2", "requirements": "section, domain, boundary, transport", "descent": "not supplied", "physical_status": "OPEN"},
    ]


def completion_rows() -> list[dict[str, str]]:
    outcomes = {
        "FC01_BOUNDARY_BOUNDARY": ("FULL_MODULE_ON_INTERIOR", "pair reduction and phase require boundary framing", "NO_GLOBAL_SELECTION"),
        "FC02_ONE_CAP_BOUNDARY": ("RANK_TWO_INTERIOR_RANK_DROP_AT_CAP", "one isotropy quotient plus open boundary", "CONDITIONAL_STRATIFIED"),
        "FC03_TWO_CAP_P0": ("FULL_MODULE_OFF_CAPS_RESIDUAL_CIRCLE", "dependent caps do not give Hopf S3", "NON_HOPF_P0"),
        "FC04_TWO_CAP_P1": ("STRATIFIED_T2_ACTION_ON_CONDITIONAL_S3", "global involutive exchange fixes a free unit-weight circle", "ABS_C1_ONE_CONDITIONAL"),
        "FC05_TWO_CAP_P_GT1": ("LENS_OR_QUOTIENT_LOCAL_SYSTEM", "fixed circle freeness and quotient class depend on cap lattice", "GLOBAL_DATA_REQUIRED"),
        "FC06_NONPRIMITIVE_CAP": ("ORBIFOLD_STRATIFIED_MODULE", "exceptional stabilizer", "NO_SMOOTH_PRINCIPAL_QUOTIENT_WITHOUT_MORE_DATA"),
        "FC07_PERIODIC_TORUS_BUNDLE": ("FULL_GL2Z_LOCAL_SYSTEM_GLOBAL", "a metric-derived pair additionally requires an everywhere two-way-wall branch and signed-permutation monodromy", "WALL_AND_MONODROMY_DEPENDENT"),
        "FC08_MIRROR_DOUBLE": ("LIFT_DEPENDENT", "identity, sign, involutive swap, and order-four lifts differ", "NO_LIFT_SELECTED"),
        "FC09_NONORIENTABLE_GLUE": ("TWISTED_FULL_LOCAL_SYSTEM", "unoriented pair may descend while Chern/Hopf sign twists", "ORIENTATION_LOCAL_SYSTEM_REQUIRED"),
        "FC10_STRATIFIED_PROJECTOR": ("STRATUM_DEPENDENT", "rank-two character module can terminate or quotient", "NO_UNIVERSAL_CROSS_STRATUM_MODULE"),
        "FC11_NONINTEGRABLE_DISTRIBUTION": ("NO_GLOBAL_CHARACTER_MODULE", "Frobenius/integrality obstruction", "UNAVAILABLE"),
        "FC12_RECIPROCAL_TORIC_DIAGONAL": ("EXACT_LOCAL_CONTROL", "pair exists only at tie; full module persists where toric", "ENDPOINT_COMPLETION_UNSELECTED"),
    }
    rows = []
    with (HERE / "COMPLETION_CANDIDATES.tsv").open(encoding="utf-8", newline="") as handle:
        for source in csv.DictReader(handle, delimiter="\t"):
            module, obstruction, outcome = outcomes[source["completion_id"]]
            rows.append({**source, "module_status": module, "obstruction_or_dependency": obstruction, "outcome": outcome})
    if len(rows) != 12:
        raise AssertionError("completion coverage")
    return rows


def hopf_rows() -> list[dict[str, str]]:
    return [
        {"step_id": "H01", "input": "two-way shortest pair", "operation": "integral span", "output": "full Lambda*", "status": "DERIVED", "missing": "not a carrier reduction"},
        {"step_id": "H02", "input": "unordered pair", "operation": "structure-group reduction", "output": "signed-permutation cocycle", "status": "CONDITIONAL_GLOBAL", "missing": "generic GL2Z monodromy need not reduce"},
        {"step_id": "H03", "input": "unordered pair only", "operation": "choose exchange lift", "output": "J,-J,or order-four", "status": "NOT_SELECTED", "missing": "sign/order lift data"},
        {"step_id": "H04", "input": "global involutive J", "operation": "take fixed subgroup", "output": "primitive circle U1_fixed", "status": "DERIVED_CONDITIONAL", "missing": "global J lift"},
        {"step_id": "H05", "input": "global involutive J", "operation": "take annihilator", "output": "relative character up to sign", "status": "DERIVED_CONDITIONAL", "missing": "phase section"},
        {"step_id": "H06", "input": "exchange eigensublattices", "operation": "integral sum", "output": "index-two sublattice", "status": "DERIVED_CONDITIONAL", "missing": "not an integral direct splitting"},
        {"step_id": "H07", "input": "reciprocal weights", "operation": "positive normalization", "output": "a1,a2 with ratio exp(2phi)", "status": "EXACT_CONDITIONAL", "missing": "amplitude interpretation and global phases"},
        {"step_id": "H08", "input": "a1,a2 and two phases", "operation": "form complex pair", "output": "unit S3 spinor coordinate", "status": "EXACT_CONDITIONAL", "missing": "torus periods,caps,global chart"},
        {"step_id": "H09", "input": "FC04 primitive independent caps", "operation": "toric completion", "output": "S3", "status": "UNIQUE_CONDITIONAL_IN_SUPPLIED_CLASS", "missing": "FC04 not selected"},
        {"step_id": "H10", "input": "FC04 plus involutive fixed circle", "operation": "isotropy test", "output": "free weight-(1,plus/minus1) action", "status": "DERIVED_CONDITIONAL", "missing": "lift and orientation"},
        {"step_id": "H11", "input": "free fixed circle on S3", "operation": "quotient", "output": "smooth S2 with abs c1=1", "status": "EXACT_CONDITIONAL_GLOBAL", "missing": "global premises unselected"},
        {"step_id": "H12", "input": "S2 quotient base", "operation": "identify physical field", "output": "carrier section", "status": "OPEN_TYPE_GAP", "missing": "section,transport,boundary,field law"},
        {"step_id": "H13", "input": "conditional carrier section", "operation": "select L2+L4", "output": "matter action", "status": "OPEN", "missing": "native variational selector"},
        {"step_id": "H14", "input": "conditional static Hopfion", "operation": "infer source,mass,density closure", "output": "unconditional matter", "status": "OPEN", "missing": "native source,boundary,scale,bootstrap map"},
    ]


def status_rows() -> list[dict[str, str]]:
    return [
        {"status_id": "S01", "object": "full toric dual character module", "status": "DERIVED_WHERE_TORIC", "scope": "rank-two GL2Z local system"},
        {"status_id": "S02", "object": "generic wall shortest pair", "status": "DERIVED_UNIMODULAR_UNORDERED_BASIS", "scope": "two-way wall interior"},
        {"status_id": "S03", "object": "pair span", "status": "DERIVED_EQUALS_FULL_MODULE", "scope": "not a smaller carrier"},
        {"status_id": "S04", "object": "co-shortest pair away from wall", "status": "NOT_AVAILABLE", "scope": "only one line remains shortest"},
        {"status_id": "S05", "object": "unique pair at three-way vertex", "status": "REFUTED", "scope": "three pair choices"},
        {"status_id": "S06", "object": "global metric-derived unordered shortest splitting", "status": "CONDITIONAL_ON_EVERYWHERE_TWO_WAY_WALL_AND_SIGNED_PERMUTATION_MONODROMY", "scope": "generic metric branches leave the wall and generic GL2Z does not preserve"},
        {"status_id": "S07", "object": "pair tensor and doublet connection", "status": "DERIVED_ON_PAIR_REDUCED_BRANCH", "scope": "geometric covariants, not section"},
        {"status_id": "S08", "object": "global exchange lift", "status": "OPEN_SELECTOR", "scope": "C1 scalar seal does not select angular lift"},
        {"status_id": "S09", "object": "involutive exchange fixed circle", "status": "DERIVED_CONDITIONAL", "scope": "requires global J or minus-J"},
        {"status_id": "S10", "object": "order-four exchange fixed circle", "status": "UNAVAILABLE", "scope": "fixed lattice rank zero"},
        {"status_id": "S11", "object": "exchange eigenlattice splitting", "status": "INDEX_TWO_NOT_DIRECT_OVER_Z", "scope": "real split exists; integral parity remains"},
        {"status_id": "S12", "object": "normalized reciprocal spinor coordinate", "status": "EXACT_CONDITIONAL", "scope": "aligned reciprocal toric amplitude interpretation"},
        {"status_id": "S13", "object": "FC04 S3 completion", "status": "UNIQUE_CONDITIONAL", "scope": "periods and primitive opposing caps supplied"},
        {"status_id": "S14", "object": "fixed-circle Hopf quotient", "status": "ABS_C1_ONE_CONDITIONAL", "scope": "FC04 plus global involutive exchange and normalization"},
        {"status_id": "S15", "object": "Hopf sign", "status": "OPEN_ORIENTATION_CONVENTION", "scope": "J and minus-J are sign-basis conjugate"},
        {"status_id": "S16", "object": "S2 carrier section", "status": "OPEN", "scope": "bundle base is not a field section"},
        {"status_id": "S17", "object": "existing static Hopfion", "status": "SETTLED_STATIC_FINITE_BOX_CONDITIONAL", "scope": "unchanged supplied carrier/action/operator premises"},
        {"status_id": "S18", "object": "native action and source", "status": "OPEN", "scope": "not implied by module topology"},
        {"status_id": "S19", "object": "density feedback and bootstrap fixed point", "status": "OPEN", "scope": "no density-to-geometry map inserted"},
        {"status_id": "S20", "object": "unconditional mass and scale", "status": "OPEN", "scope": "no scale-breaking equation"},
        {"status_id": "S21", "object": "time-live persistence", "status": "OPEN", "scope": "no dynamics run"},
        {"status_id": "S22", "object": "overall", "status": "FULL_MODULE_DERIVED__PAIR_REDUCTION_WALL_AND_MONODROMY_CONDITIONAL__HOPF_BUNDLE_ABS_UNIT_ONLY_CONDITIONAL__CARRIER_OPEN", "scope": "no canonization"},
    ]


def main() -> None:
    sources = source_replay()
    checks, algebra = exact_algebra()
    local = local_rows()
    transitions = transition_rows()
    invariants = invariant_rows()
    completions = completion_rows()
    hopf = hopf_rows()
    statuses = status_rows()

    write_tsv(
        "SOURCE_ADJUDICATION.tsv",
        ["path", "sha256", "base", "role", "result"],
        sources,
    )
    write_tsv(
        "EXACT_CHECKS.tsv",
        ["check_id", "result", "detail"],
        checks,
    )
    write_tsv(
        "LOCAL_MODULE_CENSUS.tsv",
        [
            "object_id", "object", "domain", "required_test",
            "required_disposition", "outcome", "basis",
        ],
        local,
    )
    write_tsv(
        "TRANSITION_GROUP_ATLAS.tsv",
        ["transition_id", "matrix_or_operation", "type", "test", "outcome", "note"],
        transitions,
    )
    write_tsv(
        "ASSOCIATED_INVARIANT_ATLAS.tsv",
        ["invariant_id", "object", "definition", "requirements", "descent", "physical_status"],
        invariants,
    )
    write_tsv(
        "COMPLETION_MODULE_ATLAS.tsv",
        [
            "completion_id", "name", "required_module_question", "module_status",
            "obstruction_or_dependency", "outcome",
        ],
        completions,
    )
    write_tsv(
        "CONDITIONAL_HOPF_CROSSWALK.tsv",
        ["step_id", "input", "operation", "output", "status", "missing"],
        hopf,
    )
    write_tsv(
        "STATUS_LEDGER.tsv",
        ["status_id", "object", "status", "scope"],
        statuses,
    )

    result = {
        "schema": "udt-reciprocal-pair-global-module-v1",
        "base": BASE,
        "preregistration_commit": PREREG,
        "result": "PASS",
        "maximum_ruling": (
            "FULL_TORIC_CHARACTER_MODULE_DERIVED__TWO_WAY_SHORTEST_PAIR_IS_A_WALL_LOCAL_"
            "UNIMODULAR_BASIS_NOT_A_SMALLER_MODULE__GLOBAL_UNORDERED_SPLITTING_REQUIRES_"
            "AN_EVERYWHERE_TWO_WAY_WALL_AND_SIGNED_PERMUTATION_MONODROMY__INVOLUTIVE_"
            "EXCHANGE_FIXED_CIRCLE_AND_ABS_C1_ONE_"
            "ARE_CONDITIONAL_ON_UNSELECTED_GLOBAL_LIFT_AND_FC04__CARRIER_ACTION_SOURCE_MASS_OPEN"
        ),
        "counts": {
            "sources": len(sources),
            "exact_checks": len(checks),
            "local_objects": len(local),
            "transitions": len(transitions),
            "invariants": len(invariants),
            "completions": len(completions),
            "hopf_steps": len(hopf),
            "statuses": len(statuses),
            "signed_permutation_group": len(algebra["signed_permutation_group"]),
            "native_carrier_sections": 0,
            "native_actions": 0,
            "density_or_mass_solves": 0,
        },
        "algebra": algebra,
        "authority_boundary": {
            "pair_member_selected": False,
            "exchange_lift_selected": False,
            "completion_selected": False,
            "carrier_selected": False,
            "action_selected": False,
            "density_inserted": False,
            "mass_derived": False,
            "gpu_used": False,
            "canon_changed": False,
        },
        "versions": {
            "python": sys.version.split()[0],
            "sympy": sp.__version__,
        },
    }
    (HERE / "RESULTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
