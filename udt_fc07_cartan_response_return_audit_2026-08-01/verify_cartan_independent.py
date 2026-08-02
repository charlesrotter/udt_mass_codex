#!/usr/bin/env python3
"""No-SymPy independent reconstruction of the FC07 Cartan/response result."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
MATS = (
    ("W01", "M_IDENTITY", ((1, 0), (0, 1))),
    ("W02", "M_MINUS_IDENTITY", ((-1, 0), (0, -1))),
    ("W03", "M_ORDER4_ROTATION", ((0, -1), (1, 0))),
    ("W04", "M_ORDER6_ELLIPTIC", ((0, -1), (1, 1))),
    ("W05", "M_PARABOLIC", ((1, 1), (0, 1))),
    ("W06", "M_HYPERBOLIC", ((2, 1), (1, 1))),
    ("W07", "M_EXCHANGE", ((0, 1), (1, 0))),
    ("W08", "M_ORIENTATION_REVERSING_GLIDE", ((1, 1), (0, -1))),
)


def mat(value):
    return [[F(item) for item in row] for row in value]


def zeros(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def tr(A):
    return sum(A[i][i] for i in range(len(A)))


def transpose(A):
    return [list(row) for row in zip(*A)]


def add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def scale(c, A):
    return [[F(c) * item for item in row] for row in A]


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def inv2(A):
    determinant = det2(A)
    assert determinant
    return scale(F(1, 1) / determinant, [[A[1][1], -A[0][1]], [-A[1][0], A[0][0]]])


def equal(A, B):
    return A == B


def rank2(A):
    if det2(A):
        return 2
    return 1 if any(item for row in A for item in row) else 0


def comm(A, B):
    return sub(mul(A, B), mul(B, A))


@dataclass(frozen=True)
class Jet:
    value: F
    first: F = F(0)
    second: F = F(0)

    @staticmethod
    def take(value):
        return value if isinstance(value, Jet) else Jet(F(value))

    def __add__(self, other):
        other = Jet.take(other)
        return Jet(self.value + other.value, self.first + other.first, self.second + other.second)

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.value, -self.first, -self.second)

    def __sub__(self, other):
        return self + (-Jet.take(other))

    def __rsub__(self, other):
        return Jet.take(other) - self

    def __mul__(self, other):
        other = Jet.take(other)
        return Jet(
            self.value * other.value,
            self.first * other.value + self.value * other.first,
            self.second * other.value + 2 * self.first * other.first + self.value * other.second,
        )

    __rmul__ = __mul__

    def reciprocal(self):
        v, p, q = self.value, self.first, self.second
        return Jet(1 / v, -p / v**2, 2 * p**2 / v**3 - q / v**2)

    def __truediv__(self, other):
        return self * Jet.take(other).reciprocal()


def jet_inv2(A):
    determinant = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / determinant, -A[0][1] / determinant], [-A[1][0] / determinant, A[0][0] / determinant]]


def independent_coordinate_curvature(H, D, E):
    # Build a two-jet metric in coordinates (r,y1,y2) and differentiate the
    # Christoffel formula directly, without using the production matrix identities.
    g = [[Jet(F(int(i == j))) for j in range(3)] for i in range(3)]
    for i in range(2):
        for j in range(2):
            g[i + 1][j + 1] = Jet(H[i][j], D[i][j], E[i][j])
    block_inv = jet_inv2([[g[1][1], g[1][2]], [g[2][1], g[2][2]]])
    ginv = [[Jet(F(0)) for _ in range(3)] for _ in range(3)]
    ginv[0][0] = Jet(F(1))
    for i in range(2):
        for j in range(2):
            ginv[i + 1][j + 1] = block_inv[i][j]

    def partial(entry: Jet, direction: int) -> Jet:
        return Jet(entry.first, entry.second) if direction == 0 else Jet(F(0))

    gamma = [[[
        sum(
            (
                ginv[upper][q]
                * (partial(g[q][right], left) + partial(g[q][left], right) - partial(g[left][right], q))
                / 2
            )
            for q in range(3)
        )
        for right in range(3)] for left in range(3)] for upper in range(3)]

    def gamma_partial(entry: Jet, direction: int) -> F:
        return entry.first if direction == 0 else F(0)

    R = [[[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for acted in range(3):
            for left in range(3):
                for right in range(3):
                    R[upper][acted][left][right] = (
                        gamma_partial(gamma[upper][right][acted], left)
                        - gamma_partial(gamma[upper][left][acted], right)
                        + sum(
                            gamma[upper][left][mid].value * gamma[mid][right][acted].value
                            - gamma[upper][right][mid].value * gamma[mid][left][acted].value
                            for mid in range(3)
                        )
                    )
    g0 = [[entry.value for entry in row] for row in g]
    lower = lambda first, acted, left, right: sum(g0[first][u] * R[u][acted][left][right] for u in range(3))
    ricci = [[sum(R[u][acted][u][right] for u in range(3)) for right in range(3)] for acted in range(3)]
    ginv0 = [[entry.value for entry in row] for row in ginv]
    scalar = sum(ginv0[i][j] * ricci[i][j] for i in range(3) for j in range(3))
    return lower, ricci, scalar


def table(name):
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    checks = []
    rows = {row["candidate_id"]: row for row in table("MONODROMY_CARTAN_RESPONSE_ATLAS.tsv")}
    hodge = {row["candidate_id"]: row for row in table("HODGE_RETURN_CHANNEL.tsv")}
    holonomy = {row["candidate_id"]: row for row in table("CONSTANT_SCREEN_HOLONOMY_ATLAS.tsv")}
    H0 = mat(((2, F(1, 3)), (F(1, 3), 5)))
    varying = 0
    unique = 0
    for wid, name, raw_M in MATS:
        M = mat(raw_M)
        H1 = mul(transpose(M), mul(H0, M))
        Delta = sub(H1, H0)
        Hmid = scale(F(1, 2), add(H0, H1))
        K = mul(inv2(Hmid), Delta)
        dk = det2(K)
        tk = tr(K)
        varying += int(bool(dk))
        checks.extend((tk == 0, equal(mul(K, K), scale(-dk, eye(2)))))
        ker = 2 - rank2(sub(transpose(M), eye(2)))
        b1 = 1 + ker
        unique += int(b1 == 1)
        constant_exists = name not in {"M_PARABOLIC", "M_HYPERBOLIC"}
        fixed_dimension = 2 + (2 - rank2(sub(M, eye(2))))
        expected_holonomy = (
            "UNIQUE_HOLONOMY_FIXED_LORENTZIAN_RECIPROCAL_TWO_PLANE"
            if constant_exists and fixed_dimension == 2
            else ("FIXED_THREE_SPACE_NO_UNIQUE_RECIPROCAL_TWO_PLANE" if constant_exists and fixed_dimension == 3 else ("TRIVIAL_HOLONOMY_NO_PROPER_PLANE_SELECTION" if constant_exists else "NO_CONSTANT_POSITIVE_SCREEN_SUBFAMILY"))
        )
        row = rows[wid]
        checks.extend(
            (
                row["monodromy_id"] == name,
                F(row["generic_det_K_mid_ell2"]) == dk,
                F(row["generic_tr_K_mid_ell"]) == tk,
                F(row["generic_spatial_curvature_operator_det_ell6"]) == -dk**3,
                int(row["b1_mapping_torus"]) == b1,
                int(hodge[wid]["b1"]) == b1,
                (hodge[wid]["unique_harmonic_line"] == "YES") == (b1 == 1),
                holonomy[wid]["holonomy_ruling"] == expected_holonomy,
                holonomy[wid]["relative_response"] == "ZERO_CONSTANT_SCREEN",
            )
        )
        Bset = (mat(((0, 1), (1, 0))), mat(((1, 1), (0, 1))))
        for B in Bset:
            Binv = inv2(B)
            Mp = mul(Binv, mul(M, B))
            H0p = mul(transpose(B), mul(H0, B))
            H1p = mul(transpose(Mp), mul(H0p, Mp))
            Dp = sub(H1p, H0p)
            Hmp = scale(F(1, 2), add(H0p, H1p))
            Kp = mul(inv2(Hmp), Dp)
            checks.extend((equal(Kp, mul(Binv, mul(K, B))), det2(Kp) == dk))
    checks.extend((varying == 6, unique == 4))

    # Four direct coordinate-curvature probes using a two-jet implementation.
    probes = (
        (mat(((2, F(1, 3)), (F(1, 3), 5))), mat(((1, 2), (2, -1))), mat(((3, 1), (1, -2)))),
        (mat(((3, 1), (1, 2))), mat(((0, 2), (2, 1))), mat(((-1, 3), (3, 4)))),
        (mat(((5, -1), (-1, 1))), mat(((2, 1), (1, -3))), mat(((0, -2), (-2, 1)))),
        (mat(((4, F(1, 2)), (F(1, 2), 3))), mat(((-2, 3), (3, 2))), mat(((1, 0), (0, -1)))),
    )
    for H, D, E in probes:
        lower, ricci, scalar_direct = independent_coordinate_curvature(H, D, E)
        Hinv = inv2(H)
        A = mul(Hinv, D)
        K = scale(F(1, 2), A)
        Kdot = sub(scale(F(1, 2), mul(Hinv, E)), scale(F(1, 2), mul(A, A)))
        T = add(Kdot, mul(K, K))
        radial = scale(-1, mul(H, T))
        tangent = -det2(D) / 4
        ricrr = -tr(T)
        ricscreen_end = scale(-1, add(Kdot, scale(tr(K), K)))
        ricscreen = mul(H, ricscreen_end)
        scalar_formula = -2 * tr(Kdot) - tr(mul(K, K)) - tr(K) ** 2
        checks.extend(
            (
                all(lower(0, i + 1, 0, j + 1) == radial[i][j] for i in range(2) for j in range(2)),
                lower(1, 2, 1, 2) == tangent,
                ricci[0][0] == ricrr,
                all(ricci[i + 1][j + 1] == ricscreen[i][j] for i in range(2) for j in range(2)),
                scalar_direct == scalar_formula,
                det2(K) == det2(D) / (4 * det2(H)),
            )
        )

    # Independent rank-one projector commutator response.
    for S in (mat(((2, 1), (1, -3))), mat(((1, 0), (0, 4))), mat(((0, 1), (1, 0)))):
        P = mat(((1, 0, 0), (0, 0, 0), (0, 0, 0)))
        Q = sub(eye(3), P)
        connections = [zeros(3, 3) for _ in range(3)]
        for direction in range(2):
            for screen in range(2):
                connections[direction + 1][screen + 1][0] = S[screen][direction]
                connections[direction + 1][0][screen + 1] = -S[screen][direction]
        DP = [comm(C, P) for C in connections]
        response = mul(Q, mul(comm(DP[1], DP[2]), Q))
        checks.extend((response[1][2] == det2(S), response[2][1] == -det2(S), all(response[0][j] == response[j][0] == 0 for j in range(3))))

    assert all(checks), [index for index, ok in enumerate(checks) if not ok]
    result = {
        "schema": "udt.fc07_cartan_response_return.independent.v1",
        "status": "PASS",
        "implementation": "stdlib_Fraction_plus_independent_second_jet_coordinate_Riemann",
        "check_count": len(checks),
        "monodromy_controls": 8,
        "basis_covariance_controls": 16,
        "coordinate_two_jet_probes": 4,
        "projector_response_probes": 3,
        "generic_varying_controls": varying,
        "unique_H1_completions": unique,
        "constant_unique_reciprocal_pair_planes": sum(row["holonomy_ruling"].startswith("UNIQUE_HOLONOMY") for row in holonomy.values()),
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
