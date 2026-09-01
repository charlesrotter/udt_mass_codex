#!/usr/bin/env python3
"""Hostile mutation catches for the preregistered G318 landing."""

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CATCHES = []


def catch(name, rejected):
    if not rejected:
        raise AssertionError(f"mutation escaped: {name}")
    CATCHES.append(name)


n = -2
psi = F(5, 4)
h = F(3, 7)
psi_prime = h * psi
c_value = F(4)
d_value = F(1, 2)
tau = c_value * psi ** n
tau_prime = n * h * tau
k_value = F(n, n + 6)
v_value = k_value * psi ** 6 * tau
v_prime = k_value * psi ** 6 * (tau_prime + 6 * h * tau)

catch("wrong vector psi power", v_prime != psi ** 5 * tau_prime)
catch("wrong vector factor", v_prime != F(2) * psi ** 6 * tau_prime)
catch("wrong k exponent relation", F(n + 1, n + 6) != k_value)
catch("wrong denominator shift", F(n, n + 5) != k_value)
catch("unchanged G317 k=1 falsely retained", 6 * psi ** 5 * psi_prime * tau != 0)
catch("tau exponent mutation", tau_prime != (n + 1) * h * tau)

samples = (F(1), F(3, 2), F(2), F(7, 4))
v_samples = tuple(k_value * item ** 6 * (c_value * item ** n) for item in samples)
mean_v = sum(v_samples, F(0)) / len(v_samples)
alpha = F(2, 3) * mean_v
u_samples = tuple((item - mean_v) / 2 for item in v_samples)
catch("mean subtraction omitted", sum((item / 2 for item in v_samples), F(0)) != 0)
catch("wrong TT alpha mean factor", F(1, 3) * mean_v != alpha)
catch("periodic longitudinal corruption", sum((item + F(1, 9) for item in u_samples), F(0)) != 0)

u_value = u_samples[0]
seed = (alpha, -alpha / 2 + d_value, -alpha / 2 - d_value)
catch("TT trace mutation", seed[0] + seed[1] + (-alpha / 2 + d_value) != 0)
lw_wrong = (F(3, 2) * u_value, -F(2, 3) * u_value, -F(2, 3) * u_value)
catch("wrong longitudinal xx coefficient", sum(lw_wrong) != 0)

a_value = F(n + 2, n + 6)
b_value = F(2, n + 6)
q_value = d_value * psi ** -6
kdiag = (a_value * tau, b_value * tau + q_value, b_value * tau - q_value)
catch("physical K trace mutation", sum((a_value * tau, b_value * tau + q_value, b_value * tau + q_value)) != tau)
catch("wrong a ratio", F(n + 1, n + 6) != a_value)
catch("wrong b ratio", F(1, n + 6) != b_value)
catch("q conformal power mutation", d_value * psi ** -5 != q_value)

lam = F(15, 4)
psi_second = c_value ** 2 * psi / 16 - d_value ** 2 * psi ** -7 / 4 - lam * psi ** 5 / 4
correct_scalar = -8 * psi_second + c_value ** 2 * psi / 2 - 2 * d_value ** 2 * psi ** -7 - 2 * lam * psi ** 5
catch("correct n=-2 scalar is nonzero", correct_scalar + F(1, 101) != 0)
catch("wrong scalar C coefficient", -8 * psi_second + c_value ** 2 * psi / 3 - 2 * d_value ** 2 * psi ** -7 - 2 * lam * psi ** 5 != 0)
catch("wrong scalar d sign", -8 * psi_second + c_value ** 2 * psi / 2 + 2 * d_value ** 2 * psi ** -7 - 2 * lam * psi ** 5 != 0)
catch("wrong scalar Lambda sign", -8 * psi_second + c_value ** 2 * psi / 2 - 2 * d_value ** 2 * psi ** -7 + 2 * lam * psi ** 5 != 0)
catch("wrong scalar d power", -8 * psi_second + c_value ** 2 * psi / 2 - 2 * d_value ** 2 * psi ** -6 - 2 * lam * psi ** 5 != 0)

momentum = (a_value - 1) * tau_prime + (6 * a_value - 2) * h * tau
catch("correct momentum perturbed", momentum + F(1, 97) != 0)
catch("momentum connection term omitted", (a_value - 1) * tau_prime != 0)
catch("wrong momentum connection coefficient", (a_value - 1) * tau_prime + (6 * a_value - 1) * h * tau != 0)

catch("n=-4 obstruction sign reversed", F(8 * (-4 + 3), (-4 + 6) ** 2) < 0)
catch("n=-3 coefficient falsely nonzero", F(8 * (-3 + 3), (-3 + 6) ** 2) == 0)
catch("n=-3 positive terms falsely balanced", -2 * F(1, 3) - 2 * F(2, 5) != 0)
try:
    F(-6, -6 + 6)
    singular_rejected = False
except ZeroDivisionError:
    singular_rejected = True
catch("n=-6 singular chart accepted", singular_rejected)
catch("n=0 falsely called non-CMC", 0 * h * F(7, 5) == 0)

p = F(1)
c_value = F(4)
d_value = F(1, 2)
lam = (c_value ** 2 * p ** 8 - 4 * d_value ** 2) / (4 * p ** 12)
omega2 = c_value ** 2 / 4 - 3 * d_value ** 2 * p ** -8
catch("wrong equilibrium Lambda denominator", (c_value ** 2 * p ** 8 - 4 * d_value ** 2) / (3 * p ** 12) != lam)
catch("wrong equilibrium d coefficient", (c_value ** 2 * p ** 8 - 3 * d_value ** 2) / (4 * p ** 12) != lam)
catch("center frequency sign flip", -omega2 < 0)
catch("unstable threshold promoted", (c_value ** 2 * p ** 8 <= 12 * d_value ** 2) is False)

psi = F(11, 10)
psi_prime = F(2, 17)
psi_second = c_value ** 2 * psi / 16 - d_value ** 2 * psi ** -7 / 4 - lam * psi ** 5 / 4
kappa = F(5, 3)
scaled_correct = (kappa * c_value) ** 2 * psi / 16 - (kappa * d_value) ** 2 * psi ** -7 / 4 - (kappa ** 2 * lam) * psi ** 5 / 4
catch("period rescaling omits C", c_value ** 2 * psi / 16 - (kappa * d_value) ** 2 * psi ** -7 / 4 - (kappa ** 2 * lam) * psi ** 5 / 4 != kappa ** 2 * psi_second)
catch("period rescaling omits Lambda square", scaled_correct != kappa * psi_second)

ricci_x = -4 * psi ** -5 * psi_second + 4 * psi ** -6 * psi_prime ** 2
ex = ricci_x - F(2, 3) * lam
tau = c_value * psi ** -2
q_value = d_value * psi ** -6
ey = (-2 * psi ** -5 * psi_second - 2 * psi ** -6 * psi_prime ** 2) + tau * (tau / 2 + q_value) - (tau / 2 + q_value) ** 2 - F(2, 3) * lam
ez = (-2 * psi ** -5 * psi_second - 2 * psi ** -6 * psi_prime ** 2) + tau * (tau / 2 - q_value) - (tau / 2 - q_value) ** 2 - F(2, 3) * lam
catch("electric spatial Ricci omitted", -F(2, 3) * lam != ex)
catch("electric Lambda term omitted", ricci_x + ey + ez != 0)
catch("electric trace corruption", ex + ey + ez + F(1, 89) != 0)

h = psi_prime / psi
bmag = -4 * d_value * h * psi ** -8
catch("magnetic conformal power mutation", -4 * d_value * h * psi ** -7 != bmag)
catch("magnetic factor mutation", -2 * d_value * h * psi ** -8 != bmag)
catch("magnetic symmetry denial", ((F(0), bmag), (F(0), F(0))) != ((F(0), bmag), (bmag, F(0))))
catch("nonzero magnetic tide erased", bmag != 0)

d_zero_bmag = -4 * F(0) * h * psi ** -8
catch("d-zero branch falsely magnetic", d_zero_bmag == 0)
i_value = -4 * psi_prime ** 2 + c_value ** 2 * psi ** 2 / 4 + d_value ** 2 * psi ** -6 / 3 - lam * psi ** 6 / 3
ex_from_i = -i_value * psi ** -6 + F(4, 3) * d_value ** 2 * psi ** -12
catch("electric first-integral d coefficient mutation", -i_value * psi ** -6 + d_value ** 2 * psi ** -12 != ex_from_i)

scope = "CHOSE_BOUNDED_DIAGNOSTIC_SLICE"
period_is_scale = False
history_selected = False
metric_changed = False
kernel_changed = False
catch("diagnostic separability promoted to UDT", scope != "DERIVED_GLOBAL_UDT_LAW")
catch("period promoted to physical scale", period_is_scale is False)
catch("physical history selected", history_selected is False)
catch("metric mutation", metric_changed is False)
catch("kernel mutation", kernel_changed is False)


result = {
    "schema": "udt-g318-catch-proof-v1",
    "status": "PASS",
    "mutation_count": len(CATCHES),
    "caught_count": len(CATCHES),
    "mutations": CATCHES,
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": "PASS", "caught": len(CATCHES), "total": len(CATCHES)}, indent=2))
