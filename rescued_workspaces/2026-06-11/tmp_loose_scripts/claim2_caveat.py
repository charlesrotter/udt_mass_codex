import sympy as sp
# The covariance is a statement about a SYMMETRY of the equations, not that physics is scaleless.
# It REQUIRES m->m/s (i.e. m is rescaled along with r). If instead you hold m FIXED (a physical,
# dimensionful electron mass) and only stretch r->s r, then m e^{PHI}GF does NOT scale as 1/s^2:
s,u=sp.symbols('s u',positive=True); m=sp.symbols('m',positive=True)
G=sp.Function('G');F=sp.Function('F');PHI=sp.Function('PHI');k=sp.symbols('kappa')
c=s**sp.Rational(-1,2)  # unit-norm amplitude
# FIXED m (no m->m/s):
mass_term_fixed = m*sp.exp(PHI(u))*(c*G(u))*(c*F(u))  # at radius s u, =c^2 m e^{PHI}GF
# its ratio to original mass term m e^{PHI}GF:
print("mass term ratio with m FIXED (no m->m/s):", sp.simplify(c**2), "= 1/s  (NOT 1/s^2!)")
print(" -> kappa & PHI' terms scale 1/s^2 but mass term scales 1/s => MISMATCH if m held fixed.")
print(" => covariance holds ONLY for the combined (r->sr, m->m/s) scaling. A FIXED physical mass m")
print("    BREAKS term-by-term covariance: the mass channel scales differently (1/s vs 1/s^2).")
print()
print("INTERPRETATION: the claim's 'scale covariance' is the statement that the ONLY scale in the")
print("problem is set by m (everything else dimensionless). m IS a physical scale; the covariance")
print("just says E/m is dimensionless & m-independent in units of m. It does NOT claim the theory")
print("has no scale. The negative ('back-reaction does not BREAK the covariance that's already")
print("there') is correct: classical mean-field source respects the same scaling as vacuum.")
