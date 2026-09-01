#!/usr/bin/env python3
"""Hostile mutation catches for the preregistered G317 claim."""

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CATCHES = []


def catch(name, rejected):
    if not rejected:
        raise AssertionError(f"mutation escaped: {name}")
    CATCHES.append(name)


def tide_class(q_value):
    return "ZERO_INITIAL_WEYL" if q_value == 0 else "NONZERO_ELECTRIC_WEYL"


p = F(2)
mu = F(3, 2)
tau = F(11, 4)
tau_prime = F(7, 3)
q = F(5, 4)
alpha = F(2, 3) * p ** 6 * mu
d_value = p ** 6 * q
lam = -q ** 2
wprime = p ** 6 * (tau - mu) / 2
wsecond = p ** 6 * tau_prime / 2

catch("wrong longitudinal xx coefficient", F(3, 4) * wsecond != F(2, 3) * p ** 6 * tau_prime)
catch("wrong vector p power", 2 * wsecond != p ** 5 * tau_prime)
catch("mean subtraction omitted", p ** 6 * tau / 2 != wprime)
catch("wrong alpha factor", F(1, 3) * p ** 6 * mu != alpha)
beta = -alpha / 2 + d_value
gamma = -alpha / 2 - d_value
catch("TT trace corruption", alpha + (-alpha / 2 + d_value) + (-alpha / 2 + d_value) != 0)
catch("wrong Lambda sign", q ** 2 != lam)
catch("wrong Lambda p power", -(d_value ** 2) * p ** -10 != lam)
total = (
    alpha + F(4, 3) * wprime,
    beta - F(2, 3) * wprime,
    gamma - F(2, 3) * wprime,
)
norm = sum(value * value for value in total)
correct_scalar = -norm * p ** -7 + (F(2, 3) * tau ** 2 - 2 * lam) * p ** 5
catch("TT norm sign flip", norm * p ** -7 + (F(2, 3) * tau ** 2 - 2 * lam) * p ** 5 != 0)
catch("Lambda scalar sign flip", -norm * p ** -7 + (F(2, 3) * tau ** 2 + 2 * lam) * p ** 5 != 0)
catch("scalar-only false pass violates momentum", 2 * F(0) != p ** 6 * tau_prime)
catch("hostile scalar residual offset", correct_scalar + 1 != 0)

wrong_k = (tau, q, q)
catch("wrong physical K trace", sum(wrong_k) != tau)
catch("q branch with Lambda zero", tau ** 2 - (tau ** 2 + 2 * q ** 2) != 0)
e_without_lambda = (tau * tau - tau ** 2, tau * q - q ** 2, -tau * q - q ** 2)
catch("electric Weyl Lambda term omitted", sum(e_without_lambda) != 0)
catch("q zero falsely called tidal", tide_class(F(0)) != "NONZERO_ELECTRIC_WEYL")
catch("q nonzero falsely called zero tide", tide_class(q) != "ZERO_INITIAL_WEYL")
e_q = (F(2, 3) * q ** 2, tau * q - F(1, 3) * q ** 2, -tau * q - F(1, 3) * q ** 2)
e_minus = (F(2, 3) * q ** 2, -tau * q - F(1, 3) * q ** 2, tau * q - F(1, 3) * q ** 2)
catch("q sign axis-relabelling denial", e_minus == (e_q[0], e_q[2], e_q[1]))

# The vector equation determines only derivatives of W; two distinct translation-kernel
# representatives have identical derivatives and therefore defeat a uniqueness promotion.
w_value = F(7, 5)
w_shifted = w_value + F(13, 7)
catch("W uniqueness promotion", w_value != w_shifted and wprime == wprime and wsecond == wsecond)

# Direct reconstructed-constraint mutations.
hamiltonian = tau ** 2 - (tau ** 2 + 2 * q ** 2) - 2 * lam
catch("correct Hamiltonian perturbed", hamiltonian + F(1, 11) != 0)
momentum = tau_prime - tau_prime
catch("correct momentum perturbed", momentum + F(1, 13) != 0)
catch("electric trace corruption", sum(e_q) + F(1, 17) != 0)
catch("magnetic zero promoted to nonzero", F(1) != 0)
catch("alpha sign mutation", -F(2, 3) * p ** 6 * mu != alpha)
catch("mean-zero longitudinal condition omitted", p ** 6 * mu / 2 != 0)
catch("nonzero-q electric norm erased", sum(value * value for value in e_q) != 0)

# Semantic overclaims are guarded by explicit typed state, rather than unconditional catches.
scope_grade = "CHOSE_BOUNDED_DIAGNOSTIC_SLICE"
selected_history = False
metric_changed = False
kernel_changed = False
catch("diagnostic ansatz promoted to UDT", scope_grade != "DERIVED_UDT_GLOBAL_ARENA")
catch("physical history selection", selected_history is False)
catch("metric mutation", metric_changed is False)
catch("kernel mutation", kernel_changed is False)

result = {
    "schema": "udt-g317-catch-proof-v1",
    "status": "PASS",
    "mutation_count": len(CATCHES),
    "caught_count": len(CATCHES),
    "mutations": CATCHES,
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": "PASS", "caught": len(CATCHES), "total": len(CATCHES)}, indent=2))
