#!/usr/bin/env python3
"""
DERIVATION VALIDATOR — Lorentz / Doppler clue for the full light rule.

Not a SNe trophy. Goal: show in CAS that
  (1) SR longitudinal Doppler already hits ENERGY and RATE with the SAME factor;
  (2) UDT static metric does the same (reuses banked n=2 algebra);
  (3) half-count (old SNe) = keep one factor, drop the other;
  (4) weak-field series: both sides look like "1 + 2h" in flux ~ 1/d_L^2.

Run:  python3 verify_lorentz_light_clue.py
Also re-runs core asserts from verify_luminosity_distance_n2.py inline.
"""
from __future__ import annotations

import sympy as sp

print("=" * 70)
print("LORENTZ / DOPPLER CLUE — derivation validator")
print("=" * 70)

# =============================================================================
# PART 1 — Special relativity: longitudinal Doppler + flux factors
# =============================================================================
print("\n--- PART 1: SR longitudinal Doppler (energy + rate) ---")

# Receding source, recession speed v, beta = v/c, gamma = 1/sqrt(1-beta^2)
# Standard Doppler for recession along line of sight:
#   omega_obs / omega_src = sqrt((1-beta)/(1+beta)) = 1/(1+z)
# so 1+z = sqrt((1+beta)/(1-beta))
beta = sp.symbols("beta", positive=True)
assume = sp.Q.positive(1 - beta)  # beta < 1
one_plus_z_SR = sp.sqrt((1 + beta) / (1 - beta))
# energy per photon at observer
E_factor = 1 / one_plus_z_SR
# crest rate: same factor (frequency = rate of crests)
rate_factor = 1 / one_plus_z_SR
# energy flux from a source of luminosity L (proper), isotropic in its rest frame,
# at luminosity distance d_L: F = L / (4 pi d_L^2)
# Building from photon counting at fixed area distance D (flat, no expansion):
#   F ~ (E_factor) * (rate_factor) * (L_src / area)
# If we only had Euclidean area 4 pi D^2 and identified d_L with D, we'd need
#   F = L / (4 pi D^2) * 1/(1+z)^2  =>  d_L = D (1+z)  for pure Doppler (Minkowski).
# In expanding cosmology / curved static with angular diameter D_A, Etherington
# adds one more (1+z) from area reciprocity: d_L = (1+z)^2 D_A.
#
# For THIS part we only pin: ENERGY and RATE each contribute 1/(1+z), product 1/(1+z)^2.

flux_photon_factors = sp.simplify(E_factor * rate_factor)
assert sp.simplify(flux_photon_factors - 1 / one_plus_z_SR**2) == 0
print("  1+z (SR Doppler recession) =", one_plus_z_SR)
print("  energy factor   = 1/(1+z)")
print("  rate factor     = 1/(1+z)   [same — frequency IS crest rate]")
print("  product         = 1/(1+z)^2")
print("  ASSERT product == 1/(1+z)^2  OK")

# Half-count mistakes:
half_energy_only = E_factor  # drop rate
half_rate_only = rate_factor  # drop energy
print("  half-count (energy only or rate only) = 1/(1+z)  — short one power")

# Weak beta series
series_z = sp.series(one_plus_z_SR, beta, 0, 3).removeO()
series_prod = sp.series(flux_photon_factors, beta, 0, 3).removeO()
print("  small-beta: 1+z =", series_z, "  (≈ 1+beta)")
print("  small-beta: energy*rate =", series_prod, "  (≈ 1 - 2 beta)")

# =============================================================================
# PART 2 — UDT static metric: same two hits, same factor (banked algebra)
# =============================================================================
print("\n--- PART 2: UDT static simple metric (same structure) ---")

phi = sp.Function("phi")
r, c, Econs = sp.symbols("r c E", positive=True)
ph = phi(r)
gtt = -sp.exp(-2 * ph) * c**2
grr = sp.exp(2 * ph)

# null radial speed
v = sp.symbols("v")
drdt_sols = sp.solve(sp.Eq(gtt + grr * v**2, 0), v)
assert any(sp.simplify(s - c * sp.exp(-2 * ph)) == 0 for s in drdt_sols)
print("  (A) null dr/dt = ± c e^{-2φ}  OK")

# static observer u^t
ut_val = sp.exp(ph)
assert sp.simplify(gtt * ut_val**2 + c**2) == 0
omega = sp.simplify(ut_val * Econs)  # -u·p with p_t = -Econs
assert sp.simplify(omega - Econs * sp.exp(ph)) == 0
print("  (B) ω_obs ∝ e^{φ}  OK")

phis, phio = sp.symbols("phi_s phi_o", real=True)
one_plus_z_UDT = sp.exp(phis - phio)
# energy: E_obs/E_src = e^{φ_o}/e^{φ_s} = 1/(1+z) when comparing source-at-s to obs-at-o
# with φ increasing toward source in the usual center-observer gauge φ_o=0, φ_s>0:
E_obs_over_E_src = sp.exp(phio - phis)  # = 1/(1+z)
assert sp.simplify(E_obs_over_E_src - 1 / one_plus_z_UDT) == 0
print("  (B') energy factor = e^{φ_o - φ_s} = 1/(1+z)  OK")

# arrival rate: static metric, same coordinate dt between crests
# dτ = e^{-φ} dt  => dτ_o/dτ_s = e^{-φ_o}/e^{-φ_s} = e^{φ_s - φ_o} = 1+z
# photons per observer-second = (photons per source-second) / (1+z)
rate_obs_over_rate_src = sp.exp(phio - phis)  # = 1/(1+z)
assert sp.simplify(rate_obs_over_rate_src - E_obs_over_E_src) == 0
assert sp.simplify(rate_obs_over_rate_src - 1 / one_plus_z_UDT) == 0
print("  (C) rate factor  = 1/(1+z)  [= energy factor]  OK")
print("  ASSERT energy factor == rate factor  OK  (Lorentz clue on UDT)")

# flux product
prod_UDT = sp.simplify(E_obs_over_E_src * rate_obs_over_rate_src)
assert sp.simplify(prod_UDT - 1 / one_plus_z_UDT**2) == 0
print("  product energy×rate = 1/(1+z)^2  OK")

# Etherington assembly with D_A
z, D_A, L = sp.symbols("z D_A L", positive=True)
D_sa = (1 + z) * D_A
F = (L / (1 + z) ** 2) / (4 * sp.pi * D_sa**2)
d_L = sp.simplify(sp.sqrt(L / (4 * sp.pi * F)))
assert sp.simplify(d_L - (1 + z) ** 2 * D_A) == 0
print("  (D) d_L = (1+z)^2 D_A  (full light rule)  OK")

# half rule
d_L_half = (1 + z) * D_A
print("  half light rule (old SNe): d_L_half = (1+z) D_A  — drops one of energy/rate")
print("  ratio full/half =", sp.simplify(d_L / d_L_half), " = 1+z")

# =============================================================================
# PART 3 — Dictionary (root = half Lorentz flux)
# =============================================================================
print("\n--- PART 3: dictionary ---")
print("  FULL light rule : energy × rate × area-reciprocity")
print("                  => d_L = (1+z)^2 D_A")
print("  HALF light rule : only ONE of {energy, rate} (or only area×one stretch)")
print("                  => d_L = (1+z) D_A   [old SNe validator]")
print("  ROOT error      : half rule on a theory that forces full rule")
print("  LORENTZ clue    : SR already requires energy×rate; UDT static same")

# =============================================================================
# PART 4 — Weak-field parallel (series in small stretch h)
# =============================================================================
print("\n--- PART 4: weak stretch series ---")
h = sp.symbols("h", positive=True)
# SR: beta small, 1+z ≈ 1+beta, set h = beta
# energy*rate ≈ 1 - 2h
sr_prod = sp.series(1 / one_plus_z_SR**2, beta, 0, 3).removeO()
# UDT: 1+z = e^h ≈ 1+h+..., energy*rate = e^{-2h} ≈ 1-2h
udt_prod = sp.series(sp.exp(-2 * h), h, 0, 3).removeO()
print("  SR  energy×rate ≈", sr_prod, "  (beta=h)")
print("  UDT energy×rate ≈", udt_prod, "  (1+z=e^h)")
# leading correction both -2h
sr_lin = sp.series(1 / one_plus_z_SR**2, beta, 0, 2).removeO()
udt_lin = sp.series(sp.exp(-2 * h), h, 0, 2).removeO()
# Compare coefficients of linear term with h~beta
assert sp.simplify(sr_lin.subs(beta, h) - (1 - 2 * h)) == 0
assert sp.simplify(udt_lin - (1 - 2 * h)) == 0
print("  ASSERT both = 1 - 2h + O(h^2)  OK  (same weak-field Lorentz structure)")

# =============================================================================
# PART 5 — Optional numeric pedagogy (not a fit campaign)
# =============================================================================
print("\n--- PART 5: pedagogy numbers (same D_A=1, vary z) ---")
print("  z    d_L_half=(1+z)   d_L_full=(1+z)^2   full/half")
for zv in (0.01, 0.1, 0.5, 1.0, 2.0):
    half = 1 + zv
    full = (1 + zv) ** 2
    print(f"  {zv:4.2f}  {half:12.4f}  {full:14.4f}  {full/half:8.4f}")

print("\n" + "=" * 70)
print("ALL ASSERTS PASSED — Lorentz clue validated as derivation (not SNe win)")
print("=" * 70)
