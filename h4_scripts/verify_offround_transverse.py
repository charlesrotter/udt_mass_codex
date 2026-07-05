import sympy as sp

r = sp.symbols('r')
# General ANISOTROPIC diagonal transverse metric h_AB = diag(P(r), Q(r)),
# constant on the surface (K is ultralocal in transverse coords, so this
# captures the full extrinsic structure of the W_chi*K term for the general
# (non-round, anisotropic) case).
P = sp.Function('P')(r)
Q = sp.Function('Q')(r)
phi = sp.Function('phi')(r)
# W(phi): keep symbolic. Test both branches by substitution.
W = sp.Function('W')(phi)

# --- Build the extrinsic invariant K from scratch ---
# K_AB = 1/2 e^{-phi} d_r h_AB
e = sp.exp(-phi)
h = sp.diag(P, Q)
hinv = sp.diag(1/P, 1/Q)
Kdd = sp.Rational(1,2)*e*sp.diag(sp.diff(P,r), sp.diff(Q,r))   # K_AB (lower)
Kud = hinv*Kdd                                                 # K^A_B
Ktr = sp.trace(Kud)                                            # K
KabKab = sp.trace(Kud*Kud)                                     # K_AB K^AB
calK = sp.simplify(KabKab - Ktr**2)                            # 𝒦
sqrth = sp.sqrt(P*Q)

Lw = sp.simplify(sqrth*W*calK)   # extrinsic Lagrangian density (per surface pt)

# ================= GROUND TRUTH: direct Euler-Lagrange in P and Q ==========
def EL(field):
    dfield = sp.diff(field, r)
    return sp.diff(Lw, field) - sp.diff(sp.diff(Lw, dfield), r)
# Careful: sympy diff wrt P(r) treats P and P' independently? Use variational.
# Do it properly via a param perturbation.
eps = sp.symbols('eps')
def EL_var(field):
    # returns delta S / delta field  = dL/dfield - d/dr(dL/dfield')
    fp = sp.diff(field, r)
    dL_df  = sp.diff(Lw, field)
    dL_dfp = sp.diff(Lw, fp)
    return sp.simplify(dL_df - sp.diff(dL_dfp, r))

EL_P = EL_var(P)
EL_Q = EL_var(Q)

# ================= CLOSED-FORM TENSOR from the derivation ==================
# delta S_W/delta h_AB = W sqrt(h)[ 1/2 h^AB 𝒦 - 2 K^{AC}K_C^B + 2 K K^{AB} ] - d_r pi^AB
# pi^AB = sqrt(h) W e^{-phi} (K^AB - K h^AB)
Kuu = hinv*Kdd*hinv          # K^{AB} (upper)
# (K^{AC}K_C^B) = Kuu * (h * ... ) ; K_C^B = h_{CD}K^{DB} -> Kud form: K^{AC}K_C^{B}
KAC_KCB = Kuu*h*Kuu   # = K^{AC} h_{CD} K^{DB} = K^{AC} K_C{}^{B}
Hinv = hinv
algebraic = sp.zeros(2,2)
for A in range(2):
    for B in range(2):
        algebraic[A,B] = W*sqrth*( sp.Rational(1,2)*Hinv[A,B]*calK
                                    - 2*KAC_KCB[A,B]
                                    + 2*Ktr*Kuu[A,B] )
pi = sqrth*W*e*(Kuu - Ktr*Hinv)   # pi^{AB}
mom = sp.diff(pi, r)
# delta S / delta h_AB  = algebraic^{..}?? indices: algebraic and pi are UPPER AB.
# But delta S/delta h_AB is a LOWER-index density. The relation:
#   dL/dh_AB (lower) uses  dh^CD/dh_AB etc.  We derived the UPPER-index closed form
#   as (2/sqrt h) dS/dh_AB = E^AB. Equivalent statement to compare against direct
#   EL in P=h_11, Q=h_22:   dS/dh_11 = (sqrt h /2) E^{11}? NO.
# Cleanest: compare directly the SCALAR variations.
# dS/dP = dS/dh_11. In our closed form the object with lower indices is
#   T_lower_AB = dL/dh_AB - d_r(dL/dhdot_AB).
# dL/dhdot_AB = pi_lower? We have pi^AB (upper). For diagonal, dL/dP' = pi^{11}? check.
dL_dPp = sp.simplify(sp.diff(Lw, sp.diff(P,r)))
dL_dQp = sp.simplify(sp.diff(Lw, sp.diff(Q,r)))
print("check pi^{11} vs dL/dP':", sp.simplify(dL_dPp - pi[0,0]))
print("check pi^{22} vs dL/dQ':", sp.simplify(dL_dQp - pi[1,1]))

# algebraic part: dL/dP (at fixed P') should equal algebraic[0,0]? Our algebraic
# is the UPPER-index (2/sqrt h factor absent). Let's test dL/dP vs algebraic[0,0].
dL_dP = sp.simplify(sp.diff(Lw, P))
dL_dQ = sp.simplify(sp.diff(Lw, Q))
print("check dL/dP  vs algebraic[0,0]:", sp.simplify(dL_dP - algebraic[0,0]))
print("check dL/dQ  vs algebraic[1,1]:", sp.simplify(dL_dQ - algebraic[1,1]))

# Full EL vs closed form (lower index component = algebraic - d_r pi):
ELclosed_P = sp.simplify(algebraic[0,0] - sp.diff(pi[0,0], r))
ELclosed_Q = sp.simplify(algebraic[1,1] - sp.diff(pi[1,1], r))
print("FULL EL_P match:", sp.simplify(EL_P - ELclosed_P))
print("FULL EL_Q match:", sp.simplify(EL_Q - ELclosed_Q))

# ================= 𝒦 ∝ e^{-2phi} universal (any h)  =======================
lam = sp.symbols('lambda')
calK_shift = calK.subs(phi, phi+lam)
print("𝒦(phi+lam)/𝒦(phi) =", sp.simplify(calK_shift/calK), " (should be e^{-2 lam})")

# ================= Branch cancellation for GENERAL (anisotropic) h ==========
# dW_chi 𝒦 / dphi:  Branch G W=e^{2phi}; Branch P W=1
WG = sp.exp(2*phi); WP = sp.Integer(1)
dG = sp.simplify(sp.diff(WG*calK, phi))
dP = sp.simplify(sp.diff(WP*calK, phi))
print("Branch G  d(e^{2phi}𝒦)/dphi =", dG, " (expect 0)")
print("Branch P  d(𝒦)/dphi + 2𝒦 =", sp.simplify(dP + 2*calK), " (expect 0 -> source = -2𝒦)")
