"""Q2a + Q3: full-strain depth delta_t = -(1/2)log(lambda_timelike) of C_A=A^dagA.
Its transport 1-form is the boost connection omega^0_1; its exterior derivative (N3 loop-
period density) is the boost curvature 2-form R^0_1. Compute EXACTLY, time-live, for the
GENERAL diagonal metric  ds^2 = -e^{2A(t,x)}c^2 dt^2 + e^{2B(t,x)}dx^2, then specialize:
  LOCK (UDT):  A=-phi, B=+phi  (reciprocal lock g_tt g_xx = -c^2)
  UNLOCKED:   A,B independent  (Q3 F-GENERIC test)
"""
import sympy as sp

t, x = sp.symbols('t x', real=True)
c = sp.symbols('c', positive=True)
A = sp.Function('A')(t, x)
B = sp.Function('B')(t, x)

# orthonormal coframe  E0 = e^{A} c dt,  E1 = e^{B} dx
# boost connection omega^0_1 = f dt + h dx solved from Cartan dE^a = -omega^a_b ^ E^b
# Standard 2D result: omega^0_1 = (A_x e^{A-B}/1)*? -- solve directly.
f, h = sp.symbols('f h')  # placeholders; solve via structure eqs
# dE^0 = -c e^{A} A_x dt^dx (only x-deriv survives) ; but also t-deriv of e^A gives dt^dt=0
dE0 = sp.simplify(sp.diff(sp.exp(A)*c, x))   # coeff of dx^dt in dE0 = d(e^A c dt): = (e^A c)_x dx^dt
dE1 = sp.simplify(sp.diff(sp.exp(B), t))     # coeff of dt^dx in dE1 = d(e^B dx): = (e^B)_t dt^dx
# Write omega^0_1 = P dt + Q dx. Cartan: dE^0 + omega^0_1 ^ E^1 = 0 ; dE^1 + omega^1_0 ^ E^0 = 0
# omega^1_0 = omega^0_1 (boost). E^1=e^B dx, E^0=e^A c dt.
P, Q = sp.symbols('P Q')
# dE^0 = d(e^A c dt) = (e^A c)_x dx^dt = -(e^A c)_x dt^dx
# omega^0_1 ^ E^1 = (P dt+Q dx)^(e^B dx) = P e^B dt^dx
# eq0: -(e^A c)_x + P e^B = 0  -> P = (e^A c)_x e^{-B}
Psol = sp.simplify(sp.diff(sp.exp(A)*c, x)*sp.exp(-B))
# dE^1 = d(e^B dx) = (e^B)_t dt^dx
# omega^1_0 ^ E^0 = (P dt+Q dx)^(e^A c dt) = Q e^A c dx^dt = -Q e^A c dt^dx
# eq1: (e^B)_t - Q e^A c = 0 -> Q = (e^B)_t e^{-A}/c
Qsol = sp.simplify(sp.diff(sp.exp(B), t)*sp.exp(-A)/c)
print("depth 1-form  omega^0_1 = P dt + Q dx (GENERAL diagonal):")
print("  P (dt comp) =", sp.simplify(Psol))
print("  Q (dx comp) =", sp.simplify(Qsol))

# curvature R^0_1 = d omega^0_1  (boost: no omega^0_b^omega^b_1 term in 2D single boost)
R01 = sp.simplify(sp.diff(Qsol, t) - sp.diff(Psol, x))   # coeff of dt^dx
print("\nN3 loop-period density  R^0_1|_{dt^dx} (GENERAL diagonal, EXACT):")
sp.pprint(sp.simplify(R01))

print("\n--- LOCK (UDT reciprocal lock):  A=-phi, B=+phi ---")
phi = sp.Function('phi')(t, x)
R01_lock = sp.simplify(R01.subs({A: -phi, B: phi}).doit())
sp.pprint(sp.simplify(R01_lock))

print("\n--- static reduction of lock (phi_t=0 check) ---")
phix = sp.Function('phi')(x)
R01_static = sp.simplify(R01.subs({A: -phix, B: phix}).doit())
sp.pprint(sp.simplify(R01_static))
