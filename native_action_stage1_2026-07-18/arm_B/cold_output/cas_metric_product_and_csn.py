from sympy import simplify, symbols
from sympy.functions import exp

phi = symbols("phi", real=True)
c = symbols("c", nonzero=True)
Omega = symbols("Omega", positive=True)

g_tt = -exp(-2 * phi) * c**2
g_pp = exp(2 * phi)

print("Representative product (-g_tt/c^2) * g_pp =")
print(simplify((-g_tt / c**2) * g_pp))
print()

g_tt_scaled = Omega**2 * g_tt
g_pp_scaled = Omega**2 * g_pp

print("After common rescaling, (-g_tt/c^2) * g_pp =")
print(simplify((-g_tt_scaled / c**2) * g_pp_scaled))
