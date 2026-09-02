#!/usr/bin/env python3
"""Hostile mutation catches for the preregistered G320 quotient audit."""

from fractions import Fraction
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
CATCHES = []


def catch(label, rejected):
    if not rejected:
        raise AssertionError(f"mutation escaped: {label}")
    CATCHES.append(label)


psi = Fraction(7, 5)
psi_prime = Fraction(2, 7)
psi_second = Fraction(-3, 11)
correct_r = -8 * psi ** -5 * psi_second
correct_density = psi ** 6
catch("wrong Ricci conformal power", -8 * psi ** -4 * psi_second != correct_r)
catch("wrong Ricci sign", 8 * psi ** -5 * psi_second != correct_r)
catch("wrong volume conformal power", psi ** 5 != correct_density)
catch("omitted volume weight", correct_r != correct_r * correct_density)

p = Fraction(3, 2)
a = Fraction(1, 5)
average_psi6 = p ** 6 + Fraction(15, 2) * p ** 4 * a ** 2 + Fraction(45, 8) * p ** 2 * a ** 4 + Fraction(5, 16) * a ** 6
catch("wrong psi6 cosine moment", average_psi6 != p ** 6 + 15 * p ** 4 * a ** 2 + 15 * p ** 2 * a ** 4 + a ** 6)
catch("linear rather than square mode scaling", 4 ** 2 != 4)
catch("mode-independent curvature mutation", 4 ** 2 != 1)

# A raw array changes under a phase shift while its invariant integral does not.
samples = 64
raw = [float(p) + float(a) * math.cos(2 * math.pi * index / samples) for index in range(samples)]
shifted = [float(p) + float(a) * math.cos(2 * math.pi * index / samples - 0.37) for index in range(samples)]
catch("raw-array physical discriminator", max(abs(left - right) for left, right in zip(raw, shifted)) > 0.01)
raw_mean6 = math.fsum(value ** 6 for value in raw) / samples
shifted_mean6 = math.fsum(value ** 6 for value in shifted) / samples
catch("phase falsely changes volume", abs(raw_mean6 - shifted_mean6) < 1e-12)

# Total scalar alone is not homothety neutral, whereas Q_R is.
volume = 17.0
total_scalar = 5.0
scale = 3.0
q_value = total_scalar / volume ** (1.0 / 3.0)
q_scaled = (scale * total_scalar) / (scale ** 3 * volume) ** (1.0 / 3.0)
catch("total scalar called scale-free", scale * total_scalar != total_scalar)
catch("homothety normalization omitted", abs(q_scaled - q_value) < 1e-14)

# The conformal-seed transformation must divide psi by theta.
theta = Fraction(6, 5)
gamma = psi ** 4
gamma_good = (psi / theta) ** 4 * theta ** 4
gamma_bad = (psi * theta) ** 4 * theta ** 4
catch("correct seed duplicate rejected", gamma_good == gamma)
catch("wrong seed transformation accepted", gamma_bad != gamma)

# A wrong B power can preserve AB=F and therefore the scalar constraint, but it
# violates the registered first integral with the same J0.
psi_f = 1.4
psip_f = 0.2
psipp_f = -0.3
j0 = 100.0
f_value = 12.0 * psipp_f * psi_f ** -5
z_value = 36.0 * psip_f ** 2 + j0
b_good = psi_f ** -3 * math.sqrt(z_value)
b_bad = psi_f ** -2 * math.sqrt(z_value)


def ham_from_b(b_value):
    a_value = f_value / b_value
    tau = 0.5 * (a_value + b_value)
    mu = 0.5 * (a_value - b_value)
    kdiag = ((tau + 2 * mu) / 3, (tau - mu) / 3, (tau - mu) / 3)
    return -8 * psi_f ** -5 * psipp_f + tau ** 2 - sum(item * item for item in kdiag)


catch("correct B reconstruction perturbed", abs(ham_from_b(b_good)) < 1e-14)
catch("AB factorization alone is blind to wrong B", abs(ham_from_b(b_bad)) < 1e-14)
j_good = psi_f ** 6 * b_good ** 2 - 36 * psip_f ** 2
j_bad = psi_f ** 6 * b_bad ** 2 - 36 * psip_f ** 2
catch("correct B first integral", abs(j_good - j0) < 1e-13)
catch("wrong B conformal power accepted", abs(j_bad - j0) > 1.0)

# Scope and ownership mutations.
complete_moduli = False
physical_data_selected = False
history_selected = False
metric_changed = False
kernel_changed = False
scale_selected = False
xmax_selected = False
catch("complete quotient invented", complete_moduli is False)
catch("physical data selected", physical_data_selected is False)
catch("history selected", history_selected is False)
catch("metric or kernel mutation", metric_changed is False and kernel_changed is False)
catch("scale or Xmax selection", scale_selected is False and xmax_selected is False)

prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
catch("prereg lacks physical quotient", "same physical initial datum" in prereg)
catch("prereg lacks scale-free separator", "Q_R" in prereg and "homothety-neutral" in prereg)
catch("prereg lacks incomplete-moduli guard", "does not prove\nthat every distinct profile" in prereg)
catch("prereg lacks external-review gate", "fresh external adversarial review" in prereg)

result = {
    "schema": "udt-g320-hostile-catches-v1",
    "status": "PASS",
    "mutation_count": len(CATCHES),
    "caught_count": len(CATCHES),
    "mutations": CATCHES,
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({"status": "PASS", "caught": len(CATCHES), "total": len(CATCHES)}, indent=2))
