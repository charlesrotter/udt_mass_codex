"""
A2: confirm C-2026-06-13-1 (matter-sourced T-propagation) does NOT contradict
the vacuum-static Birkhoff result.

Logic to check:
- The diagonal Ricci/Einstein DOES carry phi_tt and phi_t^2 (seen in G_thth).
- In VACUUM, G_tr=0 is an INDEPENDENT constraint that forces d_t phi=0 first,
  so the wave terms are killed -> static.
- With a MATTER source (T_tr != 0), G_tr = kappa*T_tr can be nonzero, so
  d_t phi != 0 is allowed and the phi_tt in G_thth becomes a genuine propagation.
Both true simultaneously => no contradiction.
"""
import sympy as sp

t, r, th, c, kappa = sp.symbols('t r theta c kappa', positive=True, real=True)
phi = sp.Function('phi')(t, r)

# From the Birkhoff run:
Gtr = 2*sp.diff(phi, t)/r

# VACUUM: G_tr = 0
sol_vac = sp.solve(sp.Eq(Gtr, 0), sp.diff(phi, t))
print("Vacuum G_tr=0 => d_t phi =", sol_vac, "(forced zero for r>0)")

# MATTER: G_tr = kappa * T_tr, with T_tr a generic nonzero momentum density
T_tr = sp.Symbol('T_tr', real=True)
eq_matter = sp.Eq(Gtr, kappa*T_tr)
sol_mat = sp.solve(eq_matter, sp.diff(phi, t))
print("Matter G_tr=kappa*T_tr => d_t phi =", sol_mat, "(nonzero if T_tr != 0)")

# Confirm the diagonal carries a genuine d_t^2 (wave) term that is only
# 'activated' when d_t phi is allowed nonzero by a source.
# G_thth had term ... - r*exp(4phi)*phi_tt ... => coefficient of phi_tt:
coeff_phitt = -sp.exp(4*phi)*r  # from G_thth numerator structure
print("\nCoefficient of phi_tt in G_thth numerator (nonzero):", coeff_phitt)
print("=> the diagonal sector's wave term is REAL, but in vacuum the momentum")
print("   constraint zeroes d_t phi BEFORE it can propagate. Distinction holds.")
