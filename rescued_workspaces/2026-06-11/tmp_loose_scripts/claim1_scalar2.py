import sympy as sp
# The sign of T_{mu nu} for a scalar depends on convention but more importantly:
# Let's derive T^r_r - T^t_t DIRECTLY from the same variational definition used for Dirac,
# to keep conventions consistent: delta S_matter/delta phi = -(1/2)T^{mn} dg_mn/dphi sqrt(-g)
# = -sqrt(-g)(T^r_r - T^t_t).  So whatever T is, the QUANTITY that sources phi is
#   -(T^r_r - T^t_t)  appearing as  dS/dphi/sqrt(-g).
# Let's compute dS_scalar/dphi DIRECTLY by varying the scalar action wrt phi and read off
# the source, bypassing T entirely. This is the self-consistent check.

phi, r, th, t = sp.symbols('phi r theta t', real=True)
phir = sp.Function('phi')(r)
psi = sp.Function('psi')(r)

# Canonical massless scalar: S = -(1/2) INT g^{mn} d_m psi d_n psi sqrt(-g)
# (mostly-plus signature, standard).  With psi=psi(r):
g_rr = sp.exp(2*phir)
sqrtmg = r**2*sp.sin(th)   # = r^2 sin th
grr_inv = sp.exp(-2*phir)
Lagr = -sp.Rational(1,2)*grr_inv*sp.diff(psi,r)**2 * sqrtmg
# vary wrt phir (no derivatives of phi in this term): dL/dphi
dS = sp.diff(Lagr, phir)
dS = sp.simplify(dS)
print("dS_scalar/dphi =", dS)
print("dS/sqrt(-g) =", sp.simplify(dS/sqrtmg))
# This should equal -(T^r_r - T^t_t).  So T^r_r - T^t_t = -dS/sqrt(-g):
print("=> T^r_r - T^t_t = -(dS/sqrt(-g)) =", sp.simplify(-dS/sqrtmg))
print("claimed -e^{-2phi}psi'^2 =", sp.simplify(-sp.exp(-2*phir)*sp.diff(psi,r)**2))
print("MATCH claim:", sp.simplify(-dS/sqrtmg + sp.exp(-2*phir)*sp.diff(psi,r)**2)==0)
