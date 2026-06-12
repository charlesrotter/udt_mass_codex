import sympy as sp
# Use the already-computed JSON expressions to check claim 4 precisely.
# Q1b_transverse_httheta_on_cos_mode from phaseA_results.json shows +q^2 r^2 term => elliptic for h_ttheta
# Q2_operator_on_radial_cos_mode_htr_longitudinal: H0*(-2 r phi' - e^{2phi}+1) e^{-2phi} cos(qr)/r^2 -> NO q^2 => algebraic
t,r,th,ph=sp.symbols('t r theta phi_coord',real=True)
q,H0=sp.symbols('q H0',positive=True)
phi=sp.Function('phi')(r)

# h_tr longitudinal radial mode operator (from JSON Q2):
htr_op = H0*(-2*r*sp.diff(phi,r) - sp.exp(2*phi)+1)*sp.exp(-2*phi)*sp.cos(q*r)/r**2
print("h_tr radial operator has q^2?:", htr_op.has(q**2), "-> algebraic/constraint (no 2nd-deriv principal symbol in q)")

# h_ttheta transverse radial mode (from JSON Q1b_transverse_httheta_on_cos_mode):
hang_op = H0*(q**2*r**2 + 4*r**2*sp.diff(phi,r)**2 - 2*r**2*sp.diff(phi,r,r) - 4*r*sp.diff(phi,r) - 2*sp.exp(2*phi)+2)*sp.exp(-2*phi)*sp.cos(q*r)/(2*r**2)
print("h_ttheta transverse operator has q^2?:", hang_op.has(q**2), "-> ELLIPTIC (q^2 principal symbol present)")
