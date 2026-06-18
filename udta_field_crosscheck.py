"""
udta_field_crosscheck.py
Field<->particle cross-check for the exponent a.
Anchors: committed angular Lagrangian (complete_metric_batched.py header) and
the Misner-Sharp mass. Category-A, DATA-BLIND, sympy CPU. Nothing committed touched.

Committed stress (xi=kap=1 units in code; keep symbolic here):
  X = e^{-2phi} Theta'^2   (this is g^{rr} Theta'^2: the metric contraction, NOT a mass weight)
  Y = sin^2 T / r^2        (carries NO phi)
  rho = (xi/2)(X+2Y) + (kap/2)(2XY+Y^2)
Misner-Sharp:  m(r) = r(1-e^{-2phi}),  m'(r) = 8 pi r^2 rho   (G=c=1 in code)
"""
import sympy as sp

phi, r, xi, kap, Tp, a = sp.symbols('phi r xi kap Tp a', real=True)
T = sp.Function('T')(r)
s = sp.sin(sp.Symbol('T'))   # treat sinT as a static angular shape factor

# --- committed energy density (as in code, the GR-coupled source) ---
X = sp.exp(-2*phi)*Tp**2
Y = s**2/r**2
rho_committed = (xi/2)*(X+2*Y) + (kap/2)*(2*X*Y+Y**2)
print("COMMITTED rho (GR-coupled, NO mass-dilation weight):")
print("  rho =", sp.expand(rho_committed))
print()
print("phi-content of committed rho: ONLY via X=e^{-2phi}Tp^2 (= g^{rr}, the metric")
print("  contraction of the radial gradient). The Y (angular) and Y^2 (L4 angular)")
print("  terms carry NO phi. So the committed source is a STANDARD minimally-coupled")
print("  field: phi enters only as the inverse metric, exactly as GR prescribes.")
print("  => committed code corresponds to weight e^{(a+1)phi}=1 i.e. a=-1 (GR).")
print()

# --- Now insert the UDT mass-dilation weight e^{(a+1)phi} on the source ---
# Per the field-eqn derivation, the modification is a UNIFORM weight on the matter
# action: L_matter -> e^{(a+1)phi} L_matter (equivalently on T^mu_nu / rho).
W = sp.exp((a+1)*phi)
rho_udt = W * rho_committed
print("UDT-weighted rho = e^{(a+1)phi} * rho_committed.")
print()

# --- Misner-Sharp mass with the UDT proper measure ---
# The field's gravitating mass is the MS mass:  M(R) = INT_0^R 8 pi r^2 rho dr  (areal r).
# Question: how does the field's TOTAL mass-energy scale with a uniform shift phi->phi+delta?
# Take phi = const = p (a uniform depth) to isolate the phi-SCALING of the energy,
# holding the angular profile T(r) fixed (the shape) -- this is the cleanest probe.
p = sp.Symbol('p', real=True)
rho_udt_const = rho_udt.subs(phi, p)
# Decompose by phi-power:
# X-term ~ e^{-2p}; Y-term ~ e^{0}; XY ~ e^{-2p}; Y^2 ~ e^{0}; all times e^{(a+1)p}
terms = sp.expand(rho_udt_const)
print("rho (uniform depth p), expanded:")
print("  ", terms)
print()
# collect powers of e^{p}
e = sp.exp(p)
poly_in_e = sp.collect(sp.expand(terms.rewrite(sp.exp)), e)
print("The X-built (gradient/'kinetic') pieces scale as e^{(a+1)p} * e^{-2p} = e^{(a-1)p}")
print("The Y-built (angular/'potential') pieces scale as e^{(a+1)p} * e^{0}  = e^{(a+1)p}")
print()
print("KEY OBSERVATION: the committed source has TWO sectors that scale DIFFERENTLY")
print("under the weight: kinetic ~ e^{(a-1)p}, angular ~ e^{(a+1)p}. They share a")
print("common phi-scaling ONLY when... they never do (differ by e^{-2p} always).")
print("So 'the field's mass scales as a single e^{?p}' is ILL-DEFINED unless one")
print("sector dominates or a is chosen to make a target sector match the point-mass.")
print()

# --- What 'a' would make the MS mass scale like a POINT rest mass m0 e^{a phi}? ---
# The MS mass M is an ENERGY/c^2. A point rest energy seen from afar scales (Route A)
# as e^{-phi} (a=-1) or (Route B) e^{+phi} (a=+1). The field has no single exponent;
# its energy is a SUM of e^{(a-1)p} (kinetic) and e^{(a+1)p} (angular) pieces.
print("FIELD<->PARTICLE MAP (honest):")
print("  Point particle: ONE exponent a. Field energy: a SUM of e^{(a-1)p} and")
print("  e^{(a+1)p}. There is NO single a that makes the field energy scale as a")
print("  pure e^{a p} unless one sector is dropped. The map is UNDER-DETERMINED by")
print("  the committed Lagrangian ALONE: it needs the physical choice of WHICH")
print("  field invariant represents 'the rest mass m' (kinetic? angular? MS-total?).")
print()
print("  If 'rest mass' == total MS energy at fixed shape, the field gives a")
print("  phi-DEPENDENT SPECTRUM of exponents (a-1 and a+1), NOT a single a.")
print("  This is the additional input the honesty gate requires.")
