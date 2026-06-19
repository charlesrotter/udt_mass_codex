"""
gravity_local_kinetic_escape.py (2026-06-18)
THE ONE ESCAPE: does adding an explicit Jordan-frame scalar kinetic term
   -(omega_BD / F) (dF)^2   (or equivalently an X (dphi)^2 term)
to the f(phi)R action restore PPN gamma=1 / Cassini compliance?

Einstein-frame total kinetic coefficient for action
   S = INT sqrt(-g)[ F R + X (dphi)^2 ],   F = e^{-8phi} (units aside)
is   K_E = (3/2)(F'/F)^2 + 2 X / F   (standard conformal result; signs by convention).
Brans-Dicke with omega: K_E = (omega + 3/2)(d ln F)^2.
PPN gamma_BD = (1+omega)/(2+omega).  Cassini: omega > ~40000.

We ask: what X makes omega large? And does ANY finite X give gamma=1 (omega->inf)?
"""
import sympy as sp
omega = sp.symbols('omega')
gamma = (1+omega)/(2+omega)
print("Brans-Dicke PPN gamma(omega) = (1+omega)/(2+omega):")
print("  omega=0   -> gamma =", gamma.subs(omega,0))
print("  omega->inf-> gamma ->", sp.limit(gamma, omega, sp.oo), " (GR)")
print("  Cassini gamma=1 to 2.3e-5 needs omega >", sp.solve(sp.Eq(1-gamma, sp.Rational(23,1000000)),omega)[0])
print()
print("So GR/Cassini is recovered ONLY in the omega->infinity limit, i.e. when the")
print("EXPLICIT scalar kinetic term X (dphi)^2 DOMINATES the (3/2)(F'/F)^2=96 conformal")
print("piece by a factor > ~40000.  That requires X chosen LARGE BY HAND.")
print()
print("KEY POINT for UDT: the c^4 coefficient FIXES the conformal piece at 96 (omega=0).")
print("To rescue Cassini the action would need an ADDED large bare phi-kinetic term")
print("(>~40000*64) that is NOT present in the f(phi)R action as written (premise A6).")
print("Adding it is a NEW posited mechanism (Principle 1 violation unless DERIVED).")
print()
print("NOTE: the SLAVED computation gave gamma=9 (not the independent-field 1/2),")
print("because phi=-1/2 ln(g_tt) ties the scalar to the metric. Either way gamma != 1")
print("by O(1): the c^4-on-R coupling is Cassini-incompatible without an imported")
print("large kinetic term.  The corpus's PPN PASS used a DIFFERENT action (C1 kinetic),")
print("NOT f(phi)R -- and §240.4 explicitly RULED OUT the F_R(phi)R / Einstein-Hilbert form.")
