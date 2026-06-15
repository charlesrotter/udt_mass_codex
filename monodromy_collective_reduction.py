#!/usr/bin/env python3
"""
monodromy_collective_reduction.py — UDT mass codex. GATED OBSERVE, DATA-BLIND.

The collective-coordinate reduction (sympy, exact) + the canonical structure of
the iso-rotation phase chi, to settle whether ANY single-valuedness condition
(classical OR Bohr-Sommerfeld) selects discrete depths D_n.

This is the rigorous backing for Tasks 2-4. It does NOT assume the LLM#3
mechanism; it derives the canonical structure and reads off what single-valuedness
can and cannot do.
"""
import sympy as sp

print("="*78)
print("COLLECTIVE-COORDINATE REDUCTION OF L2+L4 ON THE FINITE CELL")
print("="*78)

t = sp.symbols('t', real=True)
chi = sp.Function('chi', real=True)(t)      # iso-rotation phase about the easy axis (target-3)
Lam3 = sp.symbols('Lambda_3', positive=True) # iso-inertia about easy axis (a function of D)
D = sp.symbols('D', real=True)               # cell depth
E0 = sp.symbols('E0', positive=True)         # static soliton energy (a function of D)

chidot = sp.diff(chi, t)

# The settled reduction (n3_direction_distribution): promoting the rigid internal
# orientation R in SO(3) to a slow collective coordinate, the iso-rotation kinetic
# energy about the easy axis is (1/2) Lambda_3 chidot^2. The static (potential)
# part is the soliton energy E0(D). chi is the ONLY angular collective coordinate
# that is genuinely CYCLIC (period 2pi, the SO(3)/U(1) about the easy axis).
L_eff = sp.Rational(1,2)*Lam3*chidot**2 - E0
print("\nReduced effective Lagrangian (settled, n3_direction_distribution):")
print("  L_eff(chi, chidot; D) = (1/2) Lambda_3(D) chidot^2 - E0(D)")
print("  ", L_eff)

# Canonical momentum conjugate to chi:
p_chi = sp.diff(L_eff, chidot)
print("\nCanonical momentum p_chi = dL/d(chidot):")
print("  p_chi =", p_chi, "  = Lambda_3(D) * chidot")

# chi is CYCLIC (L_eff has no explicit chi) => p_chi is CONSERVED:
print("\nL_eff has NO explicit chi  =>  d/dt(p_chi) = 0  =>  p_chi = const (conserved).")
print("So chi is a genuine cyclic coordinate; p_chi = Lambda_3(D) chidot = const = J.")

# Equation of motion: chi(t) = (J / Lambda_3) t + chi_0  -- UNIFORM rotation at
# rate omega = J/Lambda_3.  The rotation RATE omega is FREE (any J >= 0 allowed
# classically): the depth D does NOT fix omega.
print("\nEOM: chidot = J/Lambda_3(D) = omega = CONST. chi(t) = omega t + chi0.")

print("\n" + "="*78)
print("TASK 3 — CLASSICAL (hbar-FREE) SINGLE-VALUEDNESS: does it select D_n?")
print("="*78)
print("""
Classical single-valuedness of the iso-rotation: chi is an SO(3)/U(1) angle, so
chi and chi+2pi are the SAME physical configuration. Over a TIME period T of the
rotation, the accumulated phase is

    Delta chi = omega * T = 2 pi  (one full revolution; T = 2pi/omega).

This Delta chi = 2 pi n is satisfied for EVERY omega (just wait n revolutions);
it imposes NO condition on omega and therefore NO condition on D. The rotation
rate omega = J/Lambda_3(D) is a FREE classical initial datum — for ANY depth D
there is a perfectly good single-valued uniform rotation. The phase closes for
all D.

=> CLASSICAL SINGLE-VALUEDNESS DOES NOT SELECT DISCRETE D. (No D_n.)
   The accumulated phase per period is 2 pi for ALL D, identically: there is no
   Theta(D) function whose roots pick out depths. The depth D and the rotation
   rate omega are INDEPENDENT continuous data; single-valuedness ties chi's
   period to omega, NOT to D.
""")

print("="*78)
print("TASK 4 — THE BOHR-SOMMERFELD FALLBACK (RIDES hbar — flagged LOUDLY)")
print("="*78)
print("""
The ONLY way a condition on chi can constrain D is to quantize the conserved
momentum p_chi = J itself:

    J_chi = oint p_chi dchi = p_chi * 2 pi = 2 pi Lambda_3(D) omega
          = 2 pi hbar (n + nu)            <-- Bohr-Sommerfeld, RIDES hbar.

But note WHAT this quantizes: it fixes the ANGULAR MOMENTUM J = hbar(n+nu) of the
iso-rotor (the SPIN of the soliton), i.e. it builds a ROTATIONAL BAND on a SINGLE
soliton (energy E_n = E0(D) + J^2/(2 Lambda_3(D)) = E0 + hbar^2(n+nu)^2/(2 Lam3)),
NOT a quantization of the DEPTH D. For FIXED D this is a tower of spin states on
ONE cell; it does not select which depths D exist. D remains a free continuum;
the integer n labels the soliton's spin, not a depth rung.

To turn this into a DEPTH ladder one would have to ADD a constraint linking J to
D (e.g. demand the rotor's energy equal the static depth energy, or impose a
self-consistency E0(D)=J^2/2Lambda_3 — an IMPORTED relation, not native). With
no such native link, Bohr-Sommerfeld quantizes SPIN, not DEPTH.

=> Even RIDING hbar, the natural single-valuedness condition gives a SPIN tower
   on a cell of ANY depth, NOT a discrete depth ladder. The depth stays continuous
   (consistent with NEGATIVES #39/#43). hbar adds a spin quantum number, not a
   depth quantization.
""")

# Show the rotational-band energy structure symbolically (for completeness)
hbar, n, nu = sp.symbols('hbar n nu', real=True, positive=True)
J = hbar*(n+nu)
E_band = E0 + J**2/(2*Lam3)
print("Rotational band (rides hbar): E_n(D) =", E_band)
print("  -> at FIXED D, a tower in n (spin); D is NOT quantized by this.")

print("\n" + "="*78)
print("MASS PATTERN (Task 5): is there any depth ladder to report? NO.")
print("="*78)
print("""
Since no D_n are selected (classical) and Bohr-Sommerfeld quantizes spin not depth,
there is NO native discrete depth ladder D_n and hence NO M(D_n) sequence from this
mechanism. The Misner-Sharp mass m(D)=(c^2 r/2G)(1-e^{-2phi}) and the soliton
energy E0(D) remain CONTINUOUS in D (the #39/#43 continuum is NOT lifted by the
angular monodromy). The only discrete structure hbar adds is the spin tower
E_n = E0(D) + hbar^2(n+nu)^2/(2 Lambda_3(D)) on a cell of arbitrary depth — an
O(1)-spaced rotational band (n^2 spacing), NOT a large lepton-like hierarchy and
NOT a depth selection.
""")
print("VERDICT: NO-MONODROMY (no depth-dependent angular monodromy; classical")
print("single-valuedness selects no D_n; even Bohr-Sommerfeld quantizes SPIN not DEPTH).")
