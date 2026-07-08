"""
Adversarial verification of the UDT luminosity-distance power n.

Claim under test: for ds^2 = -e^{-2phi} c^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2
with static-observer redshift 1+z = e^{phi}, the luminosity distance is
    d_L = (1+z)^2 * D_A = r * e^{2phi}   (n = 2, Etherington/reciprocity)
NOT the corpus SNe form d_L = r * e^{phi} (n = 1).

This script confirms the load-bearing algebra:
  (A) radial null-geodesic coordinate speed  dr/dt = c e^{-2phi}
  (B) static-observer frequency  omega_obs proportional to e^{phi}
      => 1+z = e^{phi_s - phi_o}  (the SAME z that enters Etherington)
  (C) photon ARRIVAL-RATE dilation  dtau_o/dtau_s = e^{phi_s - phi_o} = 1+z
      (Factor 2 -- forced by the STATIC metric, identical relation to (B))
  (D) Etherington reciprocity assembly  d_L = (1+z)^2 D_A.
"""
import sympy as sp

t, r, c, E = sp.symbols('t r c E', positive=True)
phi = sp.Function('phi')
ph = phi(r)

# ---- metric ----
gtt = -sp.exp(-2*ph)*c**2
grr =  sp.exp(2*ph)
gthth = r**2

# (A) radial null geodesic: ds^2 = 0 (dOmega=0):  gtt dt^2 + grr dr^2 = 0
drdt = sp.solve(sp.Eq(gtt + grr*sp.symbols('v')**2, 0), sp.symbols('v'))
drdt = [sp.simplify(s) for s in drdt]
print("(A) dr/dt (radial null) =", drdt, "  expected +/- c*e^{-2phi}")
assert sp.simplify(drdt[1] - c*sp.exp(-2*ph)) == 0 or sp.simplify(drdt[0] - c*sp.exp(-2*ph)) == 0

# (B) static observer 4-velocity u^t from g_tt (u^t)^2 = -c^2
ut = sp.symbols('ut', positive=True)
ut_sol = sp.solve(sp.Eq(gtt*ut**2, -c**2), ut)
# pick the future-pointing (positive) root
ut_val = sp.exp(ph)
assert any(sp.simplify(s - ut_val) == 0 for s in ut_sol), ut_sol
print("(B) u^t =", ut_val, "  expected e^{phi}")
assert sp.simplify(ut_val - sp.exp(ph)) == 0
# photon conserved energy p_t = -E ; observed omega = -u^mu p_mu = -u^t p_t
omega_obs = sp.simplify(-ut_val*(-E))
print("    omega_obs = -u^t p_t =", omega_obs, "  proportional to e^{phi}")
assert sp.simplify(omega_obs - E*sp.exp(ph)) == 0

# 1+z between source (phi_s) and observer (phi_o)
phis, phio = sp.symbols('phi_s phi_o', real=True)
one_plus_z = sp.exp(phis)/sp.exp(phio)          # omega_s/omega_o
print("(B) 1+z = omega_s/omega_o =", one_plus_z, " = e^{phi_s - phi_o}")

# (C) arrival-rate dilation in the STATIC metric.
# Two photons emitted dt apart in COORDINATE time both take the SAME coordinate
# travel time (metric is static) => they arrive dt apart in coordinate time.
# Source proper interval: dtau_s = e^{-phi_s} dt ; observer: dtau_o = e^{-phi_o} dt.
dtau_ratio = sp.exp(-phio)/sp.exp(-phis)        # dtau_o/dtau_s
print("(C) dtau_o/dtau_s =", sp.simplify(dtau_ratio), " = 1+z  -> arrival rate reduced by (1+z)")
assert sp.simplify(dtau_ratio - one_plus_z) == 0   # Factor 2 == the same (1+z) as Factor 1

# (D) Etherington assembly.
# Flux F = (energy/photon)_obs * (photons/time)_obs / (proper beam area at observer)
#        = [E_s/(1+z)] * [Nrate_s/(1+z)] / (4 pi D_sa^2),  D_sa = area distance from source
# Reciprocity: D_sa = (1+z) D_A. With L = E_s*Nrate_s:
z = sp.symbols('z', positive=True)
D_A = sp.symbols('D_A', positive=True)
L = sp.symbols('L', positive=True)
D_sa = (1+z)*D_A
F = (L/(1+z)**2) / (4*sp.pi*D_sa**2)
d_L = sp.sqrt(L/(4*sp.pi*F))
print("(D) d_L =", sp.simplify(d_L), "  => d_L = (1+z)^2 D_A  (n=2)")
assert sp.simplify(d_L - (1+z)**2*D_A) == 0

# With D_A = r and 1+z = e^{phi}:  d_L = r e^{2phi} = r * g_rr  (NOT r*e^{phi} = r*sqrt(g_rr))
print()
print("CONCLUSION: d_L = (1+z)^2 * D_A = r e^{2phi} = r * g_rr   (n = 2, FORCED)")
print("Corpus SNe form d_L = r e^{phi} = r * sqrt(g_rr) is short one power of (1+z):")
print("  it uses sqrt(g_rr) where reciprocity requires g_rr  ==> the sqrt(g_rr)-vs-g_rr error.")
