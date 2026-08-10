#!/usr/bin/env python3
"""Independent stdlib/Fraction verifier; imports neither SymPy nor production code."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
I = ((F(1), F(0)), (F(0), F(1)))
ETA = ((F(-1), F(0)), (F(0), F(1)))


def M(rows: list[list[int | F]]) -> tuple[tuple[F, F], tuple[F, F]]:
    return tuple(tuple(F(value) for value in row) for row in rows)  # type: ignore[return-value]


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def tr(a):
    return ((a[0][0], a[1][0]), (a[0][1], a[1][1]))


def inv(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0:
        raise ZeroDivisionError("singular matrix")
    return ((a[1][1] / det, -a[0][1] / det), (-a[1][0] / det, a[0][0] / det))


def scale(value: F, a=I):
    return tuple(tuple(value * a[i][j] for j in range(2)) for i in range(2))


def D(z: F):
    return ((1 / z, F(0)), (F(0), z))


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--source-snapshot-root",
        type=Path,
        help="verify manifest hashes from an isolated authorized source snapshot instead of git show",
    )
    args = parser.parse_args()
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object = "") -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": str(detail)})

    manifest = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    check("source_count", len(manifest) == 17, len(manifest))
    check("source_unique", len({row["path"] for row in manifest}) == 17)
    for index, row in enumerate(manifest, start=1):
        data = (
            (args.source_snapshot_root / row["path"]).read_bytes()
            if args.source_snapshot_root
            else subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        )
        check(f"source_{index:02d}", hashlib.sha256(data).hexdigest() == row["sha256"], row["path"])

    cases = read_tsv(HERE / "OVERLAP_CASE_ARENA.tsv")
    axes = read_tsv(HERE / "AUDIT_AXIS_ARENA.tsv")
    atlas = read_tsv(HERE / "OVERLAP_OWNERSHIP_ATLAS.tsv")
    check("arena_counts", len(cases) == 12 and len(axes) == 12, (len(cases), len(axes)))
    check("atlas_count", len(atlas) == 144, len(atlas))
    keys = {(row["case_id"], row["axis_id"]) for row in atlas}
    check("atlas_unique_complete", len(keys) == 144 and keys == {(c["case_id"], a["axis_id"]) for c in cases for a in axes})
    by_key = {(row["case_id"], row["axis_id"]): row for row in atlas}
    check("associativity_not_path_independence", by_key[("C04", "A10")]["disposition"] == "OPEN_NOT_DECIDED_BY_SUPPLIED_DATA")
    check("loop_can_be_associative", by_key[("C10", "A04")]["disposition"] == "ASSOCIATIVE_CARRY_DERIVED_FOR_GENUINE_COMMON_ATLAS" and by_key[("C10", "A10")]["disposition"] == "LOOP_HOLONOMY_NONTRIVIAL")
    check("independent_surfaces_not_forced", by_key[("C03", "A12")]["disposition"] == "OPEN_NOT_DECIDED_BY_SUPPLIED_DATA")
    check("middle_mismatch_not_erased", by_key[("C05", "A12")]["disposition"] == "MIDDLE_CALIBRATION_MISMATCH_SURVIVES")
    check("degenerate_not_filtered", by_key[("C12", "A12")]["disposition"] == "DEGENERATE_OR_UNDEFINED")

    # Different exact matrices from the production controller.
    A = M([[1, 2], [1, 3]])
    B = M([[2, 1], [3, 2]])
    C = mul(B, A)
    Q = M([[2, 3], [1, 2]])
    check("true_chain", mul(B, A) == C, C)
    check("true_obstruction", mul(inv(C), mul(B, A)) == I)
    check("associativity", mul(mul(Q, B), A) == mul(Q, mul(B, A)))
    check("wrong_order_catch", mul(A, B) != C)

    SA = M([[1, 2], [0, 1]])
    SB = M([[3, 0], [0, 2]])
    SC = M([[1, 0], [3, 1]])
    Ag = mul(SB, mul(A, inv(SA)))
    Bg = mul(SC, mul(B, inv(SB)))
    Cg = mul(SC, mul(C, inv(SA)))
    check("frame_chain", mul(Bg, Ag) == Cg)
    check("frame_obstruction", mul(inv(Cg), mul(Bg, Ag)) == mul(SA, mul(I, inv(SA))))

    sA, sB, sC = scale(F(2)), scale(F(7)), scale(F(11))
    As = mul(sB, mul(A, inv(sA)))
    Bs = mul(sC, mul(B, inv(sB)))
    Cs = mul(sC, mul(C, inv(sA)))
    check("common_scale_cancels", mul(Bs, As) == Cs)

    RA, RB, RC = D(F(2)), D(F(5)), D(F(7))
    Ar = mul(RB, mul(A, inv(RA)))
    Br = mul(RC, mul(B, inv(RB)))
    Cr = mul(RC, mul(C, inv(RA)))
    check("reciprocal_basis_cancels", mul(Br, Ar) == Cr)

    Sin = M([[1, 3], [0, 1]])
    Sout = M([[1, 0], [2, 1]])
    Ain = mul(Sin, A)
    Bout = mul(B, inv(Sout))
    middle = mul(Sout, inv(Sin))
    check("middle_transition_closes", mul(Bout, mul(middle, Ain)) == C)
    check("middle_omission_red", mul(Bout, Ain) != C)
    check("unmatched_reset_red", mul(inv(C), mul(B, mul(D(F(11)), A))) != I)

    hB = mul(tr(inv(A)), mul(ETA, inv(A)))
    hC = mul(tr(inv(B)), mul(hB, inv(B)))
    check("metric_AB", mul(tr(A), mul(hB, A)) == ETA)
    check("metric_BC", mul(tr(B), mul(hC, B)) == hB)
    check("metric_AC", mul(tr(C), mul(hC, C)) == ETA)
    H = M([[F(13, 5), F(12, 5)], [F(12, 5), F(13, 5)]])
    direct_path = mul(C, H)
    omega = mul(inv(direct_path), C)
    check("holonomy_isometry", mul(tr(H), mul(ETA, H)) == ETA)
    check("alternate_path_metric_compatible", mul(tr(direct_path), mul(hC, direct_path)) == ETA)
    check("metric_compatibility_not_descent", omega == inv(H) and omega != I, omega)
    check("triangle_reversal", mul(inv(A), mul(inv(B), direct_path)) == inv(omega))

    return_edge = mul(H, inv(C))
    loop = mul(return_edge, mul(B, A))
    check("loop_holonomy", loop == H and loop != I)
    check("loop_reverse", mul(inv(A), mul(inv(B), inv(return_edge))) == inv(H))

    z1, z2, z3 = F(2), F(5), F(7)
    scalar_triangle = mul(inv(D(z3)), mul(D(z2), D(z1)))
    check("reciprocal_multiplication", mul(D(z2), D(z1)) == D(z1 * z2))
    check("scalar_obstruction", scalar_triangle == D(z1 * z2 / z3) and scalar_triangle != I)
    check("scalar_closed_control", mul(inv(D(z1 * z2)), mul(D(z2), D(z1))) == I)

    diagA = M([[A[0][0], 0], [0, A[1][1]]])
    diagB = M([[B[0][0], 0], [0, B[1][1]]])
    check("mixing_shortcut_red", mul(diagB, diagA) != C)

    singular = M([[2, 4], [3, 6]])
    try:
        inv(singular)
        singular_caught = False
    except ZeroDivisionError:
        singular_caught = True
    check("singular_inverse_caught", singular_caught)

    failed = [item["name"] for item in checks if not item["passed"]]
    result = {
        "schema": "udt-three-observer-overlap-independent-v1",
        "implementation": "python_stdlib_fraction_no_sympy_or_production_import",
        "checks_total": len(checks),
        "checks_passed": len(checks) - len(failed),
        "checks_failed": len(failed),
        "failed": failed,
        "checks": checks,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
