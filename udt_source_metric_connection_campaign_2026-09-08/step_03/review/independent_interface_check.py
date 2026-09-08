"""Exact event-jet curvature review; no author imports or result reads."""
from fractions import Fraction as F
import json
import platform


def zeros(*shape):
    if not shape:
        return F(0)
    return [zeros(*shape[1:]) for _ in range(shape[0])]


def curvature(ginv, first, second):
    """Direct coordinate Levi-Civita derivative and Ricci from metric jets."""
    d = len(ginv)
    connection = zeros(d, d, d)
    inverse_derivative = zeros(d, d, d)
    derivative_connection = zeros(d, d, d, d)
    for k in range(d):
        for a in range(d):
            for b in range(d):
                inverse_derivative[k][a][b] = -sum(
                    ginv[a][i] * first[k][i][j] * ginv[j][b]
                    for i in range(d) for j in range(d))
    for a in range(d):
        for b in range(d):
            for c in range(d):
                connection[a][b][c] = sum(
                    ginv[a][e] * (first[b][e][c] + first[c][e][b]
                                   - first[e][b][c]) / 2 for e in range(d))
                for k in range(d):
                    derivative_connection[k][a][b][c] = sum(
                        (inverse_derivative[k][a][e]
                         * (first[b][e][c] + first[c][e][b] - first[e][b][c])
                         + ginv[a][e]
                         * (second[k][b][e][c] + second[k][c][e][b]
                            - second[k][e][b][c])) / 2 for e in range(d))
    ricci = zeros(d, d)
    for a in range(d):
        for b in range(d):
            ricci[a][b] = sum(
                derivative_connection[c][c][a][b]
                - derivative_connection[b][c][a][c]
                + sum(connection[c][c][e] * connection[e][a][b]
                      - connection[c][b][e] * connection[e][a][c]
                      for e in range(d)) for c in range(d))
    scalar = sum(ginv[a][b] * ricci[a][b]
                 for a in range(d) for b in range(d))
    return connection, ricci, scalar


checks = []
red_paths = []
values = {}


def flat(value):
    if isinstance(value, list):
        return [item for sub in value for item in flat(sub)]
    return [value]


def accept_zero(value):
    assert all(item == 0 for item in flat(value)), str(value)


def check(name, value):
    accept_zero(value)
    checks.append(name)


def require_red(name, mutant_residual):
    try:
        accept_zero(mutant_residual)
    except AssertionError:
        red_paths.append({"name": name, "status": "RED",
                          "residual": [str(v) for v in flat(mutant_residual)]})
    else:
        raise AssertionError("mutant unexpectedly accepted: " + name)


eta = [[F(-1 if a == 0 else 1) if a == b else F(0)
        for b in range(4)] for a in range(4)]
identity3 = [[F(a == b) for b in range(3)] for a in range(3)]

for seed in (0, 1, 4, 7):
    first = zeros(4, 4, 4)
    second = zeros(4, 4, 4, 4)
    for k in range(4):
        for a in range(1, 4):
            for b in range(1, 4):
                first[k][a][b] = F(((k+2)*(a+b+1)+a*b+seed) % 11-5, 7)
                for l in range(4):
                    second[k][l][a][b] = F(
                        ((k+1)*(l+1)+2*a*b+a+b+seed) % 13-6, 11)
    _, ricci4, scalar4 = curvature(eta, first, second)
    first3 = [[[first[k+1][a+1][b+1] for b in range(3)]
               for a in range(3)] for k in range(3)]
    second3 = [[[[second[k+1][l+1][a+1][b+1] for b in range(3)]
                 for a in range(3)] for l in range(3)] for k in range(3)]
    connection3, ricci3, scalar3 = curvature(identity3, first3, second3)
    K = [[-first[0][a+1][b+1]/2 for b in range(3)] for a in range(3)]
    Ktrace = sum(K[i][i] for i in range(3))
    Kdot = [[-second[0][0][a+1][b+1]/2
             for b in range(3)] for a in range(3)]
    DK = zeros(3, 3, 3)
    for k in range(3):
        for a in range(3):
            for b in range(3):
                DK[k][a][b] = -second[k+1][0][a+1][b+1]/2 - sum(
                    connection3[e][k][a]*K[e][b]
                    + connection3[e][k][b]*K[a][e] for e in range(3))
    H = scalar3 + Ktrace*Ktrace - sum(v*v for row in K for v in row)
    M = [sum(DK[j][i][j]-DK[i][j][j] for j in range(3)) for i in range(3)]
    einstein00 = ricci4[0][0] + scalar4/2
    evolution_geometry = [[ricci3[a][b] + Ktrace*K[a][b]
                           - 2*sum(K[a][c]*K[c][b] for c in range(3))
                           for b in range(3)] for a in range(3)]
    check(f"metric_jet_{seed}_ricci_symmetry",
          [[ricci4[a][b]-ricci4[b][a] for b in range(4)] for a in range(4)])
    check(f"metric_jet_{seed}_hamiltonian", H-2*einstein00)
    check(f"metric_jet_{seed}_momentum", [M[i]+ricci4[0][i+1] for i in range(3)])
    check(f"metric_jet_{seed}_spatial_evolution",
          [[Kdot[a][b]-evolution_geometry[a][b]+ricci4[a+1][b+1]
            for b in range(3)] for a in range(3)])
    values[f"jet_{seed}"] = {"H": str(H), "M": list(map(str, M)),
                              "Ric00": str(ricci4[0][0]), "R": str(scalar4)}
    if seed == 0:
        require_red("reversed_normal_projection", H+2*einstein00)
        require_red("reversed_momentum_projection",
                    [M[i]-ricci4[0][i+1] for i in range(3)])
        require_red("wrong_spatial_Ricci_sign",
                    [[Kdot[a][b]-evolution_geometry[a][b]-ricci4[a+1][b+1]
                      for b in range(3)] for a in range(3)])


def contract(matrix, left, right):
    return sum(matrix[a][b]*left[a]*right[b]
               for a in range(4) for b in range(4))


q = [F(-5, 2), F(3, 2), F(2), F(0)]
ell = [-q[0], q[1], q[2], q[3]]
normal = [F(1), F(0), F(0), F(0)]
nu = -q[0]
other_null = [F(1), F(0), F(0), F(1)]
k = [1/(2*nu), -q[1]/(2*nu*nu), -q[2]/(2*nu*nu), F(0)]
check("q_null", contract(eta, ell, ell))
check("cross_null_normalization", contract(eta, ell, k)+1)
check("second_null", contract(eta, k, k))

for case, (A0, C, n, lambda_c, alpha) in enumerate((
        (F(3,5), F(-7,3), F(5,2), F(11,7), F(2,3)),
        (F(-2), F(3), F(7,4), F(-1), F(-5,2)),
        (F(1), F(2), F(1), F(3), F(0)),
        (F(-3), F(0), F(2), F(0), F(2)))):
    P = [[A0*eta[a][b]+C*n*q[a]*q[b] for b in range(4)] for a in range(4)]
    einstein = [[alpha*P[a][b]-lambda_c*eta[a][b]
                 for b in range(4)] for a in range(4)]
    einstein_trace = sum(eta[a][b]*einstein[a][b]
                         for a in range(4) for b in range(4))
    ricci = [[einstein[a][b]-einstein_trace*eta[a][b]/2
              for b in range(4)] for a in range(4)]
    scalar = sum(eta[a][b]*ricci[a][b] for a in range(4) for b in range(4))
    lambda_eff = lambda_c-alpha*A0
    beta = alpha*C*n
    mixed = [[eta[a][a]*(ricci[a][b]-scalar*eta[a][b]/4)
              for b in range(4)] for a in range(4)]
    check(f"frame_{case}_scalar", scalar-4*lambda_eff)
    check(f"frame_{case}_same_null", contract(ricci, ell, ell))
    check(f"frame_{case}_mixed_null", contract(ricci, ell, k)+lambda_eff)
    check(f"frame_{case}_complementary_null", contract(ricci, k, k)-beta)
    check(f"frame_{case}_observer_Ricci",
          contract(ricci, normal, normal)+lambda_eff-beta*nu*nu)
    check(f"frame_{case}_tracefree_nilpotence",
          [[sum(mixed[a][c]*mixed[c][b] for c in range(4))
            for b in range(4)] for a in range(4)])
    check(f"frame_{case}_Ricci_square",
          sum(eta[a][a]*eta[b][b]*ricci[a][b]**2
              for a in range(4) for b in range(4))-4*lambda_eff**2)
    check(f"frame_{case}_normal_source",
          einstein[0][0]-lambda_eff-beta*nu*nu)
    check(f"frame_{case}_momentum_source",
          [-einstein[0][i]-beta*nu*q[i] for i in range(1,4)])
    values[f"frame_{case}"] = {
        "lambda_eff": str(lambda_eff), "beta": str(beta),
        "Ric_ell_ell": str(contract(ricci, ell, ell)),
        "Ric_ell_k": str(contract(ricci, ell, k)),
        "Ric_k_k": str(contract(ricci, k, k)),
        "Ric_N_N": str(contract(ricci, normal, normal)),
        "P_N_N": str(P[0][0]), "G352_Gamma": str(n*nu)}
    if case == 0:
        require_red("failed_metric_term_absorption", scalar-4*lambda_c)
        require_red("same_null_erasure_false_pass", contract(ricci, k, k))
        require_red("clock_rate_mistaken_for_tensor_readout", P[0][0]-n*nu)
        # Any residual can define a conserved tensor, but a class requirement
        # adds nontrivial content. Flat g gives a metric-proportional residual
        # which cannot equal this independently prescribed nonzero null term.
        residual_defined = [[lambda_c*eta[a][b]/alpha
                             for b in range(4)] for a in range(4)]
        identity_residual = [[lambda_c*eta[a][b]-alpha*residual_defined[a][b]
                              for b in range(4)] for a in range(4)]
        check("residual_defined_tautology", identity_residual)
        require_red("tautology_does_not_match_independent_class",
                    [[residual_defined[a][b]-P[a][b]
                      for b in range(4)] for a in range(4)])

print(json.dumps({"python": platform.python_version(),
                  "arithmetic": "stdlib fractions.Fraction exact rational",
                  "checks_passed": len(checks), "checks": checks,
                  "red_paths": red_paths, "values": values},
                 sort_keys=True, indent=2))
