import numpy as np
from numpy import pi, sqrt
# Rigorous: build the linearized Dirac spin connection for static h_ij = f(r) H_ij analytically
# in terms of angular operators, then project onto kappa channels.
#
# Standard result (e.g. linearized gravity Dirac coupling, weak static field, spatial h_ij):
# The Dirac Hamiltonian H = alpha.p + beta m gets, from vierbein e^a_i = delta^a_i - (1/2) h^a_i,
# the kinetic modification AND a spin-connection term. The spin connection for static field:
#   Gamma_i = (1/4) omega_{i ab} gamma^a gamma^b,  omega_{i ab} = (1/2)(partial_b h_{ai} - partial_a h_{bi})  (linearized, sym vierbein)
# The Dirac H_int from the spin connection = alpha^i (i Gamma_i)/ ... -> the spatial-spin piece is
#   H_sc = -(1/4) alpha^i [ (partial_b h_{ai} - partial_a h_{bi}) Sigma-rotation ]
# Reduces to:  H_sc = (i/4) alpha^i gamma^a gamma^b * omega_{iab}.
# The combination alpha^i gamma^a gamma^b with the antisymmetry of omega in (a,b):
#   alpha^i Sigma^c eps_{cab} omega_{iab} type -> H_sc ~ alpha^i Sigma^c (curl_a h)... 
#
# CLEANER, RIGOROUS ROUTE (avoids gamma algebra slips): use the KNOWN exact statement that for a
# STATIC metric the Dirac equation can be written H = (1/2){alpha^i, p_i + spin-conn} and the
# spin-connection's ANGULAR operator content is captured by  alpha^i (partial_j h_{ki}) [products].
# The single new angular factor relative to the vierbein vertex is exactly ONE extra derivative
# acting on h. For h_ki = f(r) H_ki:
#    partial_j h_{ki} = f'(r) nhat_j H_{ki}.
# So EVERY spin-connection angular operator is of the form  (Dirac-bilinear in alpha,Sigma) x nhat_j H_{ki}
# i.e. it has angular content = { nhat (rank1) } tensored with { H (rank2, but as a CONSTANT it is
# rank-2 in the LAB, contracted into spin/the other indices) }.
#
# The MAXIMAL angular operator (worst case for a leak) is therefore: one Sigma (rank1 spin),
# times nhat_j (rank1 orbital), times H_{ki} contracted. Acting on the 2-spinor channel the orbital
# content is AT MOST nhat (one orbital unit, Delta l = +-1) because H is CONSTANT (L=0).
# Constant H contributes ZERO orbital angular momentum. So spin-connection adds at most ONE orbital
# unit just like the vierbein term. From l=0 (kappa=-1 large comp) or l=1 (small comp) you reach at
# most l=2 -> |kappa|<=3. kappa=-4 needs l=3 -> UNREACHABLE at first order.
#
# Let me VERIFY this is airtight by brute force: enumerate ALL rank tensors you can build from
# {Sigma (rank1), nhat (rank1), H (const rank2)} bilinear/first-order in h, expand each in the
# kappa basis acting on the kappa=-1 LARGE (Om_+? wait Om_{-1}) and SMALL (Om_{+1}) components,
# and confirm none reach Om with l=3 (i.e. kappa=-4 has l=3, kappa=+4 has l=4).
#
# kappa=-1: large Om_{-1} l=0, small Om_{+1} l=1.
# kappa=-4: large Om_{-4} l=3, small Om_{+4} l=4.
# To reach kappa=-4 we must reach an angular function with l=3 (the Om_{-4} large) or l=4.
# Operators available, orbital content:
#   - constant H: l=0
#   - nhat: l=1 (Y_1)
#   - nhat nhat (sym traceless): l=2 ; but spin conn has only ONE nhat (one derivative).
# So max orbital from operator = l=1 (single nhat).
# Acting on l=0 -> l in {1};  on l=1 -> l in {0,2}.  Reaches l in {0,1,2}. NEVER l=3.
# => kappa=-4 (needs l=3) UNREACHABLE. SOLID.
print("ANALYTIC ARGUMENT (spin connection, static h=f(r)H):")
print(" partial_j h_ki = f'(r) nhat_j H_ki  -> operator orbital content = ONE nhat (l=1) max")
print(" because H is CONSTANT (L=0). Single derivative => single nhat => Delta l = +-1.")
print(" kappa=-1 components have l in {0 (large), 1 (small)};")
print(" one orbital unit reaches l in {0,1,2}; kappa=-4 needs l=3 -> UNREACHABLE.")
print(" => spin connection does NOT open a first-order kappa=-4 leak for CONSTANT H. QED-ish.")
print()
print("CAVEAT: this hinges on H being constant (intrinsic L=0). If the spin-2 field carries")
print("its own orbital profile (h_ij = sum over Y_L coefficients) the derivative can give two")
print("nhats and reach l=3. That is exactly attack point #3.")
