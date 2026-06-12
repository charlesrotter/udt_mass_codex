import sympy as sp
# ATTACK 1: For a scalar field phi (the ONLY matter field with a stress tensor in canonical UDT),
# T_{ti} = d_t phi d_i phi - g_{ti} L.  For STATIC phi (d_t phi=0) and diagonal background (g_ti=0):
# T_{ti} = 0 identically.  A perturbation delta_phi(r,theta,phi) that is also static (d_t=0) gives
# T_{ti} STILL = 0 to first order:  T_{tr} = d_t phi d_r phi = (d_t delta_phi)(...) = 0 if d_t delta_phi=0.
# So a STATIC scalar (background OR static perturbation) has T_{ti}=0 EXACTLY.
t,r,th,ph = sp.symbols('t r theta phi_coord')
P = sp.Function('P')  # scalar field
phi_field = P(r,th,ph)  # static (no t)
# canonical scalar T_{mu nu} = d_mu phi d_nu phi - g_{mu nu}(1/2 (dphi)^2 + V)
T_tr = sp.diff(phi_field,t)*sp.diff(phi_field,r)
print("T_tr for static scalar (no g_ti term):", T_tr)  # = 0 since d_t=0
# Time-dependent scalar needed for T_ti != 0:
phi_dyn = sp.Function('Pd')(t,r,th,ph)
T_tr_dyn = sp.diff(phi_dyn,t)*sp.diff(phi_dyn,r)
print("T_tr for time-dependent scalar:", T_tr_dyn, " (nonzero ONLY if d_t phi != 0)")
