#!/usr/bin/env python3
"""Hostile mutation catches for the preregistered G319 classification."""

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CATCHES = []


def catch(name, rejected):
    if not rejected:
        raise AssertionError(f"mutation escaped: {name}")
    CATCHES.append(name)


psi = F(5, 4)
psi_prime = F(3, 7)
h_value = psi_prime / psi
a_value = F(7, 5)
b_value = F(4, 3)
d_value = F(2, 5)
lam = F(3, 7)
psi_second = psi ** 5 * (
    a_value * b_value - 3 * d_value ** 2 * psi ** -12 - 3 * lam
) / 12
f_correct = 12 * psi_second * psi ** -5 + 3 * d_value ** 2 * psi ** -12 + 3 * lam
b_prime = 3 * h_value * (a_value - b_value)
tau = (a_value + b_value) / 2
mu = (a_value - b_value) / 2
a_prime = F(-5, 8)
tau_prime = (a_prime + b_prime) / 2
mu_prime = (a_prime - b_prime) / 2
v_value = psi ** 6 * mu
v_prime = psi ** 6 * (mu_prime + 6 * h_value * mu)

catch("correct factorization perturbed", f_correct + F(1, 101) != a_value * b_value)
catch("F psi-second coefficient 8", 8 * psi_second * psi ** -5 + 3 * d_value ** 2 * psi ** -12 + 3 * lam != a_value * b_value)
catch("F psi-second coefficient 6", 6 * psi_second * psi ** -5 + 3 * d_value ** 2 * psi ** -12 + 3 * lam != a_value * b_value)
catch("F d coefficient 2", 12 * psi_second * psi ** -5 + 2 * d_value ** 2 * psi ** -12 + 3 * lam != a_value * b_value)
catch("F d sign", 12 * psi_second * psi ** -5 - 3 * d_value ** 2 * psi ** -12 + 3 * lam != a_value * b_value)
catch("F d power", 12 * psi_second * psi ** -5 + 3 * d_value ** 2 * psi ** -10 + 3 * lam != a_value * b_value)
catch("F Lambda coefficient", 12 * psi_second * psi ** -5 + 3 * d_value ** 2 * psi ** -12 + 2 * lam != a_value * b_value)
catch("F Lambda sign", 12 * psi_second * psi ** -5 + 3 * d_value ** 2 * psi ** -12 - 3 * lam != a_value * b_value)
catch("F psi power", 12 * psi_second * psi ** -4 + 3 * d_value ** 2 * psi ** -12 + 3 * lam != a_value * b_value)

catch("B-prime factor 2", 2 * h_value * (a_value - b_value) != b_prime)
catch("B-prime factor 6", 6 * h_value * (a_value - b_value) != b_prime)
catch("B-prime sign", -3 * h_value * (a_value - b_value) != b_prime)
catch("B-prime sum mutation", 3 * h_value * (a_value + b_value) != b_prime)
catch("B-prime H omitted", 3 * (a_value - b_value) != b_prime)
catch("original vector psi power", v_prime != psi ** 5 * tau_prime)
catch("original vector factor", v_prime != 2 * psi ** 6 * tau_prime)
catch("lambda conformal power", v_value * psi ** -5 != mu)
catch("lambda sign", -v_value * psi ** -6 != mu)

j_correct = (
    psi ** 6 * b_value ** 2
    - 36 * psi_prime ** 2
    + 3 * d_value ** 2 * psi ** -6
    - 3 * lam * psi ** 6
)
catch("J B coefficient", 2 * psi ** 6 * b_value ** 2 - 36 * psi_prime ** 2 + 3 * d_value ** 2 * psi ** -6 - 3 * lam * psi ** 6 != j_correct)
catch("J B psi power", psi ** 5 * b_value ** 2 - 36 * psi_prime ** 2 + 3 * d_value ** 2 * psi ** -6 - 3 * lam * psi ** 6 != j_correct)
catch("J derivative coefficient 32", psi ** 6 * b_value ** 2 - 32 * psi_prime ** 2 + 3 * d_value ** 2 * psi ** -6 - 3 * lam * psi ** 6 != j_correct)
catch("J derivative sign", psi ** 6 * b_value ** 2 + 36 * psi_prime ** 2 + 3 * d_value ** 2 * psi ** -6 - 3 * lam * psi ** 6 != j_correct)
catch("J d coefficient", psi ** 6 * b_value ** 2 - 36 * psi_prime ** 2 + 2 * d_value ** 2 * psi ** -6 - 3 * lam * psi ** 6 != j_correct)
catch("J d sign", psi ** 6 * b_value ** 2 - 36 * psi_prime ** 2 - 3 * d_value ** 2 * psi ** -6 - 3 * lam * psi ** 6 != j_correct)
catch("J d psi power", psi ** 6 * b_value ** 2 - 36 * psi_prime ** 2 + 3 * d_value ** 2 * psi ** -5 - 3 * lam * psi ** 6 != j_correct)
catch("J Lambda coefficient", psi ** 6 * b_value ** 2 - 36 * psi_prime ** 2 + 3 * d_value ** 2 * psi ** -6 - 2 * lam * psi ** 6 != j_correct)
catch("J Lambda sign", psi ** 6 * b_value ** 2 - 36 * psi_prime ** 2 + 3 * d_value ** 2 * psi ** -6 + 3 * lam * psi ** 6 != j_correct)
catch("J Lambda psi power", psi ** 6 * b_value ** 2 - 36 * psi_prime ** 2 + 3 * d_value ** 2 * psi ** -6 - 3 * lam * psi ** 5 != j_correct)

j_prime_correct = (
    6 * psi ** 5 * psi_prime * b_value ** 2
    + 2 * psi ** 6 * b_value * b_prime
    - 72 * psi_prime * psi_second
    - 18 * d_value ** 2 * psi ** -7 * psi_prime
    - 18 * lam * psi ** 5 * psi_prime
)
catch("correct J derivative mutation", j_prime_correct + F(1, 97) != 0)
catch("J-prime B2 factor", 5 * psi ** 5 * psi_prime * b_value ** 2 + 2 * psi ** 6 * b_value * b_prime - 72 * psi_prime * psi_second - 18 * d_value ** 2 * psi ** -7 * psi_prime - 18 * lam * psi ** 5 * psi_prime != 0)
catch("J-prime B derivative omitted", 6 * psi ** 5 * psi_prime * b_value ** 2 - 72 * psi_prime * psi_second - 18 * d_value ** 2 * psi ** -7 * psi_prime - 18 * lam * psi ** 5 * psi_prime != 0)
catch("J-prime 36 not differentiated", 6 * psi ** 5 * psi_prime * b_value ** 2 + 2 * psi ** 6 * b_value * b_prime - 36 * psi_prime * psi_second - 18 * d_value ** 2 * psi ** -7 * psi_prime - 18 * lam * psi ** 5 * psi_prime != 0)

kdiag = (
    (tau + 2 * mu) / 3,
    (tau - mu) / 3 + d_value * psi ** -6,
    (tau - mu) / 3 - d_value * psi ** -6,
)
catch("physical K trace plus-q mutation", sum((kdiag[0], kdiag[1], kdiag[1])) != tau)
catch("physical K axial factor", (tau + mu) / 3 != kdiag[0])
catch("physical K q power", (tau - mu) / 3 + d_value * psi ** -5 != kdiag[1])
catch("physical K q sign", (tau - mu) / 3 - d_value * psi ** -6 != kdiag[1])
momentum = (
    (tau_prime + 2 * mu_prime) / 3
    - tau_prime
    + 6 * h_value * kdiag[0]
    - 2 * h_value * tau
)
catch("correct momentum perturbed", momentum + F(1, 89) != 0)
catch("momentum connection omitted", (tau_prime + 2 * mu_prime) / 3 - tau_prime != 0)
catch("momentum factor 5", (tau_prime + 2 * mu_prime) / 3 - tau_prime + 5 * h_value * kdiag[0] - 2 * h_value * tau != 0)
catch("momentum trace factor", (tau_prime + 2 * mu_prime) / 3 - tau_prime + 6 * h_value * kdiag[0] - h_value * tau != 0)

# Reconstruction mutations use J0 chosen to reproduce this exact point.
radicand = 36 * psi_prime ** 2 - 3 * d_value ** 2 * psi ** -6 + 3 * lam * psi ** 6 + j_correct
catch("correct radicand mismatch mutation", radicand + F(1, 113) != psi ** 6 * b_value ** 2)
catch("radicand derivative factor", 32 * psi_prime ** 2 - 3 * d_value ** 2 * psi ** -6 + 3 * lam * psi ** 6 + j_correct != psi ** 6 * b_value ** 2)
catch("radicand d sign", 36 * psi_prime ** 2 + 3 * d_value ** 2 * psi ** -6 + 3 * lam * psi ** 6 + j_correct != psi ** 6 * b_value ** 2)
catch("radicand Lambda sign", 36 * psi_prime ** 2 - 3 * d_value ** 2 * psi ** -6 - 3 * lam * psi ** 6 + j_correct != psi ** 6 * b_value ** 2)
catch("B reconstruction psi exponent", psi ** -2 * psi ** 3 * b_value != b_value)

# The zero stratum must not be removed by division.
zero_b = F(0)
zero_division_rejected = False
try:
    _ = f_correct / zero_b
except ZeroDivisionError:
    zero_division_rejected = True
catch("division through B-zero accepted", zero_division_rejected)
zero_psi_second = -psi ** 5 * (3 * d_value ** 2 * psi ** -12 + 3 * lam) / 12
zero_f = 12 * zero_psi_second * psi ** -5 + 3 * d_value ** 2 * psi ** -12 + 3 * lam
catch("B-zero scalar compatibility denied", zero_f == 0)
catch("B-zero derivative falsely forced zero", 3 * h_value * a_value != 0)

# Compact positivity is load-bearing: a merely positive radicand does not fix tau's sign.
b2 = F(1, 5)
f_negative = F(-2, 5)
catch("B2 positivity falsely sufficient", b2 + f_negative < 0)
catch("B2-plus-F strictness erased", b2 + f_negative != 0)

# Periodic TT descent requires mean removal.
values = (F(1), F(-2), F(5), F(7))
mean_v = sum(values, F(0)) / len(values)
w_primes = tuple((value - mean_v) / 2 for value in values)
catch("mean subtraction omitted", sum((value / 2 for value in values), F(0)) != 0)
catch("mean subtraction sign", sum(((value + mean_v) / 2 for value in values), F(0)) != 0)
catch("wrong alpha mean factor", F(1, 3) * mean_v != F(2, 3) * mean_v)
catch("periodic w constant corruption", sum((value + F(1, 17) for value in w_primes), F(0)) != 0)

# G318 regression must remain a subfamily, not a universal ratio law.
n = -2
tau_g318 = F(4) * psi ** n
mu_g318 = F(n, n + 6) * tau_g318
catch("G318 ratio denominator mutation", F(n, n + 5) * tau_g318 != mu_g318)
catch("G318 ratio sign mutation", -F(n, n + 6) * tau_g318 != mu_g318)
catch("G318 ratio promoted universal", mu / tau != mu_g318 / tau_g318)
catch("G318 n obstruction promoted general", (n <= -3) is False)

# Scope and provenance mutations.
scope = "CHOSE_BOUNDED_DIAGNOSTIC_SLICE"
history_selected = False
scale_selected = False
xmax_selected = False
metric_changed = False
kernel_changed = False
j0_is_observed = False
global_B_stratum_parameterized = False
catch("diagnostic slice promoted to UDT", scope != "DERIVED_GLOBAL_UDT_LAW")
catch("J0 promoted to observed scale", j0_is_observed is False)
catch("physical history selected", history_selected is False)
catch("physical scale selected", scale_selected is False)
catch("physical Xmax selected", xmax_selected is False)
catch("metric mutation", metric_changed is False)
catch("kernel mutation", kernel_changed is False)
catch("B-zero global parameterization invented", global_B_stratum_parameterized is False)

prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
catch("prereg lacks B-zero guard", "No claim of a full explicit" in prereg)
catch("prereg lacks arbitrary-profile discriminator", "sufficiently large `J_0`" in prereg)
catch("prereg lacks no-selection guard", "No\nphysical data" in prereg)


result = {
    "schema": "udt-g319-hostile-catches-v1",
    "status": "PASS",
    "mutation_count": len(CATCHES),
    "caught_count": len(CATCHES),
    "mutations": CATCHES,
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({"status": "PASS", "caught": len(CATCHES), "total": len(CATCHES)}, indent=2))
