# ATTACK 3: the identification chi (transport potential, Phase B) propto delta_phi (metric scalar
# that TEMPERATURE reads, Tolman delta_T/T = -delta_phi).
#
# Phase B: Laplacian chi = sigma ~ -delta_rho   (chi = reservoir potential)
# Phase C step: h_tr propto d_r delta_phi  -- requires h_tr's source J_r = d_r chi to give
#   h_tr ~ J_r ~ d_r chi, AND chi to be identified with delta_phi.
#
# Question: is chi = delta_phi?
# - delta_phi is the METRIC scalar perturbation (Tolman temperature: delta_T/T=-delta_phi).
#   In canonical UDT, delta_phi solves the linearized SCREENED KG: Box delta_phi = mu^2 delta_phi + S,
#   i.e. (Laplacian - mu^2) delta_phi = S  with S ~ delta_rho-like source.
# - chi is the TRANSPORT/reservoir potential: Laplacian chi = -delta_rho  (UNSCREENED Poisson, mu=0).
#
# These are DIFFERENT Green's functions:
#   delta_phi(q) = -S(q)/(q^2 + mu^2)        [screened, Yukawa]
#   chi(q)       = +delta_rho(q)/q^2          [unscreened, Coulomb]
# If both sourced by the SAME density delta_rho ~ cos(qr), then BOTH are ~cos(qr) (same phase!),
# but with DIFFERENT amplitude transfer functions:
#   delta_phi(q) ~ 1/(q^2+mu^2) * cos
#   chi(q)       ~ 1/q^2        * cos
# So chi and delta_phi are PHASE-ALIGNED (both even functionals of the same cos source) but
# NOT EQUAL (different transfer functions). The phase alignment is what the quadrature argument
# needs (h_tr ~ d_r chi ~ d_r[cos] ~ sin, quadrature vs delta_phi~cos). 
#
# VERDICT on attack 3: chi != delta_phi as fields, but they are PHASE-ALIGNED (both ~cos of the
# same density mode). The quadrature conclusion needs only phase-alignment, which HOLDS as long as
# BOTH are sourced by the SAME delta_rho with sign-definite (phase-preserving) Green functions.
# That is plausible but ASSERTED: it requires (a) the recycling sinks/sources co-located with the
# SAME density that sources delta_phi, and (b) both Green functions sign-definite/phase-preserving.
# Phase B asserts (a) ("sinks/sources co-located with density structure"); (b) holds for Poisson/Yukawa.
import sympy as sp
q,mu = sp.symbols('q mu',positive=True)
print("delta_phi(q) transfer (screened):", 1/(q**2+mu**2))
print("chi(q) transfer (unscreened):    ", 1/q**2)
print("Both even in source -> phase-aligned to delta_rho (cos). NOT equal fields.")
print("Quadrature needs only phase-alignment of chi to delta_phi: HOLDS if co-sourced.")
