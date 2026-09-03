#!/usr/bin/env python3
"""Exact bounded G336 second-normal response on the G335 silent set."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "eba7a42a"


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def sign(value: F) -> int:
    return (value > 0) - (value < 0)


def boost_from_half_tangent(t: F) -> tuple[F, F]:
    denominator = 1 - t * t
    return 2 * t / denominator, (1 + t * t) / denominator


def verify_sources(checks: list[str]) -> None:
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    require(len(rows) == 6, "six_frozen_sources", checks)
    for row in rows:
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts,
                f"source_{row['source_id']}_path_safe", checks)
        source_root = ROOT / "sources" if (ROOT / "sources").is_dir() else ROOT
        path = (source_root / relative).resolve()
        require(path.is_relative_to(source_root.resolve()),
                f"source_{row['source_id']}_contained", checks)
        payload = path.read_bytes() if path.is_file() else b""
        expected_bytes = int(row["bytes"])
        expected_digest = row["sha256"]
        if (len(payload) != expected_bytes
                or hashlib.sha256(payload).hexdigest() != expected_digest):
            replay = subprocess.run(
                ["git", "show", f"{PREREG_COMMIT}:{relative.as_posix()}"],
                cwd=ROOT,
                capture_output=True,
                check=False,
            )
            if replay.returncode:
                raise AssertionError(f"source_{row['source_id']}_frozen_git_available")
            payload = replay.stdout
        require(len(payload) == expected_bytes, f"source_{row['source_id']}_bytes", checks)
        require(hashlib.sha256(payload).hexdigest() == expected_digest,
                f"source_{row['source_id']}_sha256", checks)


class Jet2:
    """Value and first two derivatives of a one-variable rational function."""

    __slots__ = ("v", "d1", "d2")

    def __init__(self, value=0, first=0, second=0):
        self.v = F(value)
        self.d1 = F(first)
        self.d2 = F(second)

    @staticmethod
    def lift(value):
        return value if isinstance(value, Jet2) else Jet2(value)

    def __add__(self, other):
        other = self.lift(other)
        return Jet2(self.v + other.v, self.d1 + other.d1, self.d2 + other.d2)

    __radd__ = __add__

    def __neg__(self):
        return Jet2(-self.v, -self.d1, -self.d2)

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        return Jet2(
            self.v * other.v,
            self.d1 * other.v + self.v * other.d1,
            self.d2 * other.v + 2 * self.d1 * other.d1 + self.v * other.d2,
        )

    __rmul__ = __mul__

    def inverse(self):
        if not self.v:
            raise ZeroDivisionError("zero jet")
        return Jet2(
            1 / self.v,
            -self.d1 / self.v**2,
            2 * self.d1**2 / self.v**3 - self.d2 / self.v**2,
        )

    def __truediv__(self, other):
        return self * self.lift(other).inverse()

    def __rtruediv__(self, other):
        return self.lift(other) * self.inverse()


def identity(n: int = 3) -> list[list[F]]:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def inverse_fraction(matrix: list[list[F]]) -> list[list[F]]:
    n = len(matrix)
    augmented = [list(matrix[i]) + identity(n)[i] for i in range(n)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    augmented[row][j] - factor * augmented[column][j]
                    for j in range(2 * n)
                ]
    return [row[n:] for row in augmented]


def weighted_metric_jets(x_value: F, weight_1: F, weight_2: F):
    x = Jet2(x_value, 1, 0)
    one = Jet2(1)
    radial = x * (one - x)
    f = weight_1 * x + weight_2 * (one - x)
    eta = (x / f, (one - x) / f)
    zeta = (Jet2(weight_2) / f, Jet2(-weight_1) / f)
    metric = [[Jet2(0) for _ in range(3)] for _ in range(3)]
    metric[0][0] = 1 / (4 * radial * f)
    metric[1][1] = radial / f * zeta[0] * zeta[0] + eta[0] * eta[0]
    metric[1][2] = metric[2][1] = (
        radial / f * zeta[0] * zeta[1] + eta[0] * eta[1]
    )
    metric[2][2] = radial / f * zeta[1] * zeta[1] + eta[1] * eta[1]
    return (
        [[metric[i][j].v for j in range(3)] for i in range(3)],
        [[metric[i][j].d1 for j in range(3)] for i in range(3)],
        [[metric[i][j].d2 for j in range(3)] for i in range(3)],
    )


def coordinate_geometry(x_value: F, weight_1: F, weight_2: F):
    """Direct exact coordinate reconstruction, independent of the Ricci projector formula."""
    metric, dmetric, ddmetric = weighted_metric_jets(x_value, weight_1, weight_2)
    inverse = inverse_fraction(metric)
    dinverse = [[
        -sum(inverse[i][a] * dmetric[a][b] * inverse[b][j]
             for a in range(3) for b in range(3))
        for j in range(3)
    ] for i in range(3)]
    christoffel = [[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    dchristoffel = [[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for i in range(3):
            for j in range(3):
                for ell in range(3):
                    first = dmetric[ell][j] if i == 0 else F(0)
                    first += dmetric[ell][i] if j == 0 else F(0)
                    first -= dmetric[i][j] if ell == 0 else F(0)
                    second = ddmetric[ell][j] if i == 0 else F(0)
                    second += ddmetric[ell][i] if j == 0 else F(0)
                    second -= ddmetric[i][j] if ell == 0 else F(0)
                    christoffel[upper][i][j] += inverse[upper][ell] * first / 2
                    dchristoffel[upper][i][j] += (
                        dinverse[upper][ell] * first + inverse[upper][ell] * second
                    ) / 2
    ricci = [[F(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            value = dchristoffel[0][i][j]
            if j == 0:
                value -= sum(dchristoffel[k][i][k] for k in range(3))
            for k in range(3):
                for ell in range(3):
                    value += christoffel[k][i][j] * christoffel[ell][k][ell]
                    value -= christoffel[ell][i][k] * christoffel[k][j][ell]
            ricci[i][j] = value
    scalar = sum(inverse[i][j] * ricci[i][j]
                 for i in range(3) for j in range(3))
    return metric, inverse, ricci, scalar


def check_coordinate_ricci(
    x: F, weight_1: F, weight_2: F, checks: list[str], tag: str
) -> F:
    metric, _, ricci, scalar = coordinate_geometry(x, weight_1, weight_2)
    xi = [F(0), weight_1, weight_2]
    eta = [sum(metric[i][j] * xi[j] for j in range(3)) for i in range(3)]
    xi_norm = sum(eta[i] * xi[i] for i in range(3))
    require(xi_norm == 1, f"coordinate_{tag}_xi_unit", checks)
    horizontal_eigenvalue = (scalar - 2) / 2
    for i in range(3):
        for j in range(3):
            expected = (
                horizontal_eigenvalue * metric[i][j]
                + (2 - horizontal_eigenvalue) * eta[i] * eta[j]
            )
            require(ricci[i][j] == expected,
                    f"coordinate_{tag}_ricci_projector_{i}_{j}", checks)
    return scalar


def derive() -> dict:
    checks: list[str] = []
    verify_sources(checks)
    coordinate_records: list[dict] = []
    silent_records: list[dict] = []

    coordinate_samples = (
        (F(1, 3), F(1, 4), F(1, 4)),
        (F(2, 3), F(1, 4), F(1, 4)),
        (F(1, 3), F(1), F(1)),
        (F(2, 5), F(2), F(3)),
        (F(3, 7), F(3, 2), F(5, 4)),
        (F(4, 9), F(5, 3), F(7, 5)),
    )
    scalar_values: list[F] = []
    for index, (x, weight_1, weight_2) in enumerate(coordinate_samples):
        scalar = check_coordinate_ricci(
            x, weight_1, weight_2, checks, f"{index}"
        )
        scalar_values.append(scalar)
        coordinate_records.append({
            "x": str(x), "w1": str(weight_1), "w2": str(weight_2), "R": str(scalar)
        })
    require(scalar_values[0] == 0 and scalar_values[1] == 0,
            "equal_quarter_weight_R_zero", checks)
    require(scalar_values[3] != scalar_values[4],
            "unequal_weight_controls_distinct", checks)

    mus = tuple(F(i, 12) for i in range(13))
    b_magnitudes = (F(1, 2), F(1), F(2), F(7, 3))
    half_tangents = tuple(F(i, 10) for i in range(-8, 9))
    strict_silent_case_count = 0
    vertical_boundary_case_count = 0
    strict_boost_case_count = 0
    boundary_boost_case_count = 0
    interior_case_count = 0
    horizontal_endpoint_case_count = 0
    double_silent_count = 0

    # Each coordinate R is a member of the complete positive-weight family. For each R, mu,
    # and nonzero b, C and Lambda below put the datum exactly on the G332 constraint and G335
    # first-order-silent set. The algebra is rational and both signs of b are retained.
    for scalar_index, scalar in enumerate(scalar_values):
        for mu in mus:
            for magnitude in b_magnitudes:
                for branch_sign in (-1, 1):
                    b = branch_sign * magnitude
                    C = b * (1 - 2 * mu)
                    Lambda = scalar / 2 - 2 * b * b * mu + 3 * b * b * mu * mu
                    q0 = (b - C) / 2 - b * mu
                    radicand = 2 * (scalar + 2 * C * C - 2 * Lambda)
                    root_component = b + C
                    require(q0 == 0,
                            f"silent_{scalar_index}_{mu}_{b}_q0", checks)
                    require(root_component * root_component == radicand,
                            f"silent_{scalar_index}_{mu}_{b}_constraint", checks)
                    if mu < 1:
                        require(radicand > 0,
                                f"silent_{scalar_index}_{mu}_{b}_radicand_strict", checks)
                    else:
                        require(radicand == 0,
                                f"silent_{scalar_index}_{mu}_{b}_vertical_branch_boundary", checks)

                    ricci_vv = (scalar - 2) / 2 + (6 - scalar) * mu / 2
                    k_horizontal = (C - b) / 2
                    k_vertical = (C + b) / 2
                    k2_vv = k_horizontal * k_horizontal * (1 - mu)
                    k2_vv += k_vertical * k_vertical * mu
                    expected_k2 = b * b * mu * (1 - mu)
                    require(k2_vv == expected_k2,
                            f"silent_{scalar_index}_{mu}_{b}_k2", checks)

                    s_adm = Lambda - ricci_vv + 2 * k2_vv
                    s_middle = 1 + (Lambda - 3) * mu + 3 * b * b * mu * mu * (1 - mu)
                    s_reduced = 1 + (scalar - 6) * mu / 2 + b * b * mu * mu
                    require(s_adm == s_middle == s_reduced,
                            f"silent_{scalar_index}_{mu}_{b}_three_forms", checks)

                    h_horizontal = (b - C) / 2
                    h_vertical = -(C + b) / 2
                    hv_norm2 = (
                        h_horizontal * h_horizontal * (1 - mu)
                        + h_vertical * h_vertical * mu
                    )
                    require(hv_norm2 == b * b * mu * (1 - mu),
                            f"silent_{scalar_index}_{mu}_{b}_hv_norm", checks)

                    if F(0) < mu < F(1):
                        interior_case_count += 1
                        require(hv_norm2 > 0,
                                f"silent_{scalar_index}_{mu}_{b}_interior_hv", checks)
                        k_zero = 1 - s_reduced / (2 * hv_norm2)
                        s_zero = s_reduced + 2 * (k_zero - 1) * hv_norm2
                        s_low = s_reduced + 2 * (k_zero - 2) * hv_norm2
                        s_high = s_reduced + 2 * k_zero * hv_norm2
                        require(s_zero == 0 and s_low < 0 and s_high > 0,
                                f"silent_{scalar_index}_{mu}_{b}_carry_all_signs", checks)
                    else:
                        if mu == 0:
                            horizontal_endpoint_case_count += 1
                        else:
                            vertical_boundary_case_count += 1
                        require(hv_norm2 == 0,
                                f"silent_{scalar_index}_{mu}_{b}_endpoint_hv_zero", checks)
                        for carry_parameter in (F(-7), F(0), F(11, 3)):
                            s_carried = s_reduced + 2 * carry_parameter * hv_norm2
                            require(s_carried == s_reduced,
                                    f"silent_{scalar_index}_{mu}_{b}_endpoint_carry", checks)

                    if s_reduced == 0:
                        double_silent_count += 1

                    for half_tangent in half_tangents:
                        sh, ch = boost_from_half_tangent(half_tangent)
                        require(ch * ch - sh * sh == 1,
                                f"boost_{scalar_index}_{mu}_{b}_{half_tangent}_lorentz", checks)
                        h00 = 2 * s_reduced * sh * sh
                        h01 = 2 * s_reduced * sh * ch
                        h11 = 2 * s_reduced * ch * ch
                        require(-h00 + h11 == 2 * s_reduced,
                                f"boost_{scalar_index}_{mu}_{b}_{half_tangent}_trace", checks)
                        require(h00 * h11 - h01 * h01 == 0,
                                f"boost_{scalar_index}_{mu}_{b}_{half_tangent}_rank", checks)
                        phi_second = s_reduced * sh * sh
                        require(phi_second == h00 / 2,
                                f"boost_{scalar_index}_{mu}_{b}_{half_tangent}_phi", checks)
                        if half_tangent == 0:
                            require(phi_second == 0,
                                    f"boost_{scalar_index}_{mu}_{b}_zero_blind", checks)
                        if mu < 1:
                            strict_boost_case_count += 1
                        else:
                            boundary_boost_case_count += 1

                    if len(silent_records) < 30 and mu in (F(0), F(1, 2), F(1)):
                        silent_records.append({
                            "R": str(scalar), "mu": str(mu), "b": str(b),
                            "C": str(C), "Lambda": str(Lambda),
                            "s1": str(s_reduced), "sign": sign(s_reduced),
                            "Hv_norm_squared": str(hv_norm2),
                            "stratum": "strict" if mu < 1 else "vertical_branch_boundary",
                        })
                    if mu < 1:
                        strict_silent_case_count += 1

    # Exact equal-weight R=0 sign triplet required by the preregistration. b^2=2 is
    # represented through its minimal polynomial; every formula here depends only on b^2.
    sign_triplet = []
    for b_squared, expected_sign in ((F(1), -1), (F(2), 0), (F(4), 1)):
        scalar = F(0)
        mu = F(1, 2)
        C = F(0)
        Lambda = -b_squared / 4
        s1 = 1 + (scalar - 6) * mu / 2 + b_squared * mu * mu
        require(sign(s1) == expected_sign,
                f"triplet_{b_squared}_sign", checks)
        require(2 * (scalar + 2 * C * C - 2 * Lambda) == b_squared,
                f"triplet_{b_squared}_constraint", checks)
        for branch in (-1, 1):
            require(branch * branch * b_squared == b_squared,
                    f"triplet_{b_squared}_branch_{branch}", checks)
            sign_triplet.append({
                "R": "0", "mu": "1/2", "C": "0", "b_squared": str(b_squared),
                "b_branch": branch, "Lambda": str(Lambda), "s1": str(s1),
                "sign": expected_sign,
            })
            if expected_sign == 0:
                double_silent_count += 1
    require({row["sign"] for row in sign_triplet} == {-1, 0, 1},
            "triplet_realizes_all_signs", checks)

    # Endpoint identities and the general interior double-silent surface.
    for scalar in scalar_values:
        for b in (F(-3), F(3)):
            require(1 + (scalar - 6) * F(0) / 2 + b * b * F(0) == 1,
                    f"horizontal_endpoint_{scalar}_{b}", checks)
            Lambda_vertical = scalar / 2 + b * b
            s_vertical = 1 + (scalar - 6) / 2 + b * b
            require(s_vertical == Lambda_vertical - 2,
                    f"vertical_endpoint_{scalar}_{b}", checks)

    zero_surface_controls = 0
    for scalar in (F(-4), F(0), F(2), F(5)):
        for mu in (F(1, 4), F(1, 2), F(3, 4), F(1)):
            numerator = (6 - scalar) * mu - 2
            if numerator > 0:
                b_squared = numerator / (2 * mu * mu)
                s1 = 1 + (scalar - 6) * mu / 2 + b_squared * mu * mu
                require(s1 == 0, f"zero_surface_{scalar}_{mu}", checks)
                zero_surface_controls += 1
    require(zero_surface_controls > 0, "zero_surface_exercised", checks)
    require(double_silent_count > 0, "exact_double_silent_exercised", checks)

    landing = (
        "G336_INHERITED_SILENT_SECOND_JET_IS_EXACT_BUT_SIGN_INDEFINITE"
        "__INTERIOR_CLASSIFICATION_DEPENDS_ON_DIRECTION_CARRY"
        "__STRICT_HORIZONTAL_ENDPOINT_IS_POSITIVE_AND_CARRY_INDEPENDENT"
        "__VERTICAL_ENDPOINT_IS_BRANCH_MEETING_BOUNDARY"
        "__DOUBLE_SILENT_STRATUM_REQUIRES_HIGHER_JET"
    )
    return {
        "package": "G336",
        "grade": "DERIVED_CONDITIONAL_BOUNDED"
                 "__EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_REPAIRS",
        "landing": landing,
        "classifications": [
            "INHERITED_LIE_CARRY_SECOND_JET_EXACT",
            "SILENT_SET_SPLITS_POSITIVE_ZERO_NEGATIVE",
            "INTERIOR_SILENT_SECOND_RESPONSE_CARRY_DEPENDENT",
            "STRICT_HORIZONTAL_ENDPOINT_SECOND_RESPONSE_CARRY_INDEPENDENT_AT_THIS_ORDER",
            "VERTICAL_ENDPOINT_EXCLUDED_FROM_STRICT_FAMILY_AS_BRANCH_MEETING_BOUNDARY",
            "DOUBLE_SILENT_STRATUM_REQUIRES_THIRD_JET",
            "UNIVERSAL_SECOND_ORDER_TURN_ON_REFUTED",
        ],
        "analytic_result": {
            "silent_condition": "C=b(1-2mu)",
            "ricci_vv": "(R-2)/2+(6-R)mu/2",
            "K_squared_vv": "b^2 mu(1-mu)",
            "inherited_s1": "1+(R-6)mu/2+b^2 mu^2",
            "interior_zero_surface": "b^2=((6-R)mu-2)/(2mu^2)",
            "general_unit_first_carry": "s1(W)=s1(Lie)+2<Hv,W-Hv>",
            "Hv_norm_squared_at_silence": "b^2 mu(1-mu)",
            "horizontal_endpoint": "s1=1",
            "vertical_endpoint": "s1=Lambda-2",
            "pair_second_jet": "2s1[[sinh^2,sinh*cosh],[sinh*cosh,cosh^2]]",
            "terminal_second_jet": "s1 sinh(z)^2",
        },
        "strict_silent_case_count": strict_silent_case_count,
        "vertical_boundary_case_count": vertical_boundary_case_count,
        "strict_boost_case_count": strict_boost_case_count,
        "boundary_boost_case_count": boundary_boost_case_count,
        "total_boost_controls": strict_boost_case_count + boundary_boost_case_count,
        "interior_case_count": interior_case_count,
        "horizontal_endpoint_case_count": horizontal_endpoint_case_count,
        "double_silent_sample_count": double_silent_count,
        "zero_surface_controls": zero_surface_controls,
        "checks_passed": len(checks),
        "checks_sha256": hashlib.sha256("\n".join(checks).encode()).hexdigest(),
        "check_examples": checks[:20] + checks[-20:],
        "coordinate_records": coordinate_records,
        "silent_records": silent_records,
        "sign_triplet": sign_triplet,
        "scope": {
            "complete_positive_weight_family": "analytic Ricci-projector proof; exact coordinate controls",
            "both_G332_branches": True,
            "all_strict_silent_directions": "analytic in 0<=mu<1; exact rational controls",
            "vertical_mu_one": "branch-meeting closure boundary only",
            "all_finite_boosts": "analytic; rational half-rapidity controls",
            "general_first_direction_carry": "analytic at initial silence",
            "third_higher_jet_double_silent": "OPEN",
            "arbitrary_pair_second_carry_observer_time": "OPEN",
            "explicit_development_stability_occupancy_matter_scale_Xmax_observation": "OPEN",
            "topology_inputs_used": [],
            "observational_inputs_used": [],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = derive()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(json.dumps({
        "checks_passed": result["checks_passed"],
        "strict_silent_cases": result["strict_silent_case_count"],
        "strict_boost_cases": result["strict_boost_case_count"],
        "vertical_boundary_cases": result["vertical_boundary_case_count"],
        "landing": result["landing"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
