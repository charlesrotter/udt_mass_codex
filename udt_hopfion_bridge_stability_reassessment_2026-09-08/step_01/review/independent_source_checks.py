"""New exact source-fidelity anchors; no author/source implementation imports.

Finite anchors do not re-prove continuum quantifiers or recertify carrier numerics.
"""
from fractions import Fraction as F
import json


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def ricci_from_brackets(a, c):
    # Reconstruct curvature in a left-invariant orthonormal frame.
    bracket = [[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for i, j, k, value in [(0, 1, 2, 2*c/a**2),
                           (1, 2, 0, 2/c), (2, 0, 1, 2/c)]:
        bracket[i][j][k] = value
        bracket[j][i][k] = -value
    connection = [[[sum((bracket[i][j][k], -bracket[j][k][i],
                         bracket[k][i][j]))/2 for k in range(3)]
                   for j in range(3)] for i in range(3)]

    def curvature(i, j, k, ell):
        return sum(connection[j][k][m]*connection[i][m][ell]
                   - connection[i][k][m]*connection[j][m][ell]
                   - bracket[i][j][m]*connection[m][k][ell]
                   for m in range(3))

    return [[sum(curvature(i, j, k, i) for i in range(3))
             for k in range(3)] for j in range(3)]


def boost(v, beta, gamma):
    return (gamma*(v[0]-beta*v[3]), v[1], v[2],
            gamma*(v[3]-beta*v[0]))


results = {"classification": "new exact rational finite source anchors; not old-artifact replay",
           "berger": [], "sky": [], "constraints": []}
for a, c in [(F(1), F(3, 2)), (F(3, 2), F(1)), (F(1), F(1))]:
    ric = ricci_from_brackets(a, c)
    horizontal, vertical = 4/a**2-2*c**2/a**4, 2*c**2/a**4
    expected = [[(horizontal if i < 2 else vertical) if i == j else F(0)
                 for j in range(3)] for i in range(3)]
    assert ric == expected
    results["berger"].append({"a": str(a), "c": str(c),
                              "ricci": [[str(v) for v in row] for row in ric],
                              "gap": str(ric[2][2]-ric[0][0])})

for beta in [F(0), F(3, 5), F(-3, 5)]:
    gamma = F(1) if beta == 0 else F(5, 4)
    for n in [(F(1), F(0), F(0)), (F(3, 5), F(0), F(4, 5)),
              (F(0), F(0), F(1))]:
        tangent = (F(0), F(1), F(0))
        second = (-n[2], F(0), n[0])
        k = boost((F(1), *n), beta, gamma)
        assert -k[0]**2+dot(k[1:], k[1:]) == 0

        def projective_differential(v):
            dk = boost((F(0), *v), beta, gamma)
            return tuple((dk[i]*k[0]-k[i]*dk[0])/k[0]**2 for i in range(1, 4))

        t, s = projective_differential(tangent), projective_differential(second)
        norm_ratio = dot(t, t)/dot(tangent, tangent)
        area_square_ratio = dot(t, t)*dot(s, s)-dot(t, s)**2
        assert norm_ratio == 1/(gamma*(1-beta*n[2]))**2
        assert area_square_ratio == norm_ratio**2
        results["sky"].append({"beta": str(beta), "n": [str(x) for x in n],
                               "tangent_square_ratio": str(norm_ratio),
                               "two_area_square_ratio": str(area_square_ratio)})

# Both branches, both signs of C; derive K eigenvalues and reconstruct
# Hamiltonian directly from trace/norm rather than substituting a saved residual.
R, Lambda = F(7, 2), F(7, 4)
for C in [F(2), F(-2)]:
    radicand = 2*(R+2*C**2-2*Lambda)
    assert radicand == 16
    for branch in [F(-1), F(1)]:
        b = -C+branch*4
        eig = [(C-b)/2, (C-b)/2, (C+b)/2]
        residual = R+sum(eig)**2-dot(eig, eig)-2*Lambda
        assert residual == 0
        results["constraints"].append({"C": str(C), "branch": str(branch),
                                       "K_eigenvalues": [str(x) for x in eig],
                                       "Hamiltonian_residual": str(residual)})

# Nonvacuity controls: genuinely incorrect physical identifications/coefficients
# are contradicted by recomputed quantities. These are finite controls, not a
# general-purpose proof or comprehensive mutation harness.
results["nonvacuity_controls"] = {
    "nonround_ricci_not_isotropic": results["berger"][0]["gap"] != "0",
    "round_projector_denominator_zero": results["berger"][2]["gap"] == "0",
    "boost_not_round_target_isometry": any(r["tangent_square_ratio"] != "1"
                                           for r in results["sky"]),
}
bad_b = -F(2)+F(2)  # Wrong sqrt coefficient: sqrt(4) in place of sqrt(16).
bad_eig = [(F(2)-bad_b)/2, (F(2)-bad_b)/2, (F(2)+bad_b)/2]
bad_residual = R+sum(bad_eig)**2-dot(bad_eig, bad_eig)-2*Lambda
assert bad_residual != 0
results["nonvacuity_controls"]["wrong_root_Hamiltonian_residual"] = str(bad_residual)
print(json.dumps(results, indent=2, sort_keys=True))
