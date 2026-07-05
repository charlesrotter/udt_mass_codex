import sympy as sp

r, x, y = sp.symbols('r x y')
phi = sp.Function('phi')(r)   # phi longitudinal, r only
lam = sp.symbols('lambda')

print("="*70)
print("CHECK A: FULLY GENERAL non-diagonal h_AB(r,x,y): universal e^{-2phi} scaling")
print("="*70)
# fully general symmetric 2-metric with FULL (r,x,y) dependence, non-diagonal
P = sp.Function('P')(r,x,y)
Q = sp.Function('Q')(r,x,y)
S = sp.Function('S')(r,x,y)
h = sp.Matrix([[P, S],[S, Q]])
hinv = h.inv()
e = sp.exp(-phi)
# K_AB = 1/2 e^{-phi} d_r h_AB  (only r-derivative)
Kdd = sp.Rational(1,2)*e*sp.Matrix([[sp.diff(P,r), sp.diff(S,r)],[sp.diff(S,r), sp.diff(Q,r)]])
Kud = hinv*Kdd
Ktr = sp.trace(Kud)
KabKab = sp.trace(Kud*Kud)
calK = sp.simplify(KabKab - Ktr**2)
# universal scaling: 𝒦(phi+lam)/𝒦(phi) should be e^{-2 lam} regardless of h
ratio = sp.simplify(calK.subs(phi, phi+lam)/calK)
print("  𝒦(phi+lam)/𝒦(phi) =", ratio, " (expect exp(-2*lambda))")
dcheck = sp.simplify(sp.diff(calK, phi) + 2*calK)
print("  d𝒦/dphi + 2𝒦 =", dcheck, " (expect 0)")

# Branch cancellations, general h
WG = sp.exp(2*phi)
print("  Branch G d(e^{2phi}𝒦)/dphi =", sp.simplify(sp.diff(WG*calK, phi)), " (expect 0)")
print("  Branch P d(𝒦)/dphi + 2𝒦 =", sp.simplify(sp.diff(calK,phi)+2*calK), " (expect 0)")

print("="*70)
print("CHECK B: 𝒦 = -2 det(K^A_B) = -2 k1 k2 (sign-flip claim), general non-diag")
print("="*70)
detKud = sp.simplify(Kud.det())
print("  𝒦 + 2 det(K^A_B) =", sp.simplify(calK + 2*detKud), " (expect 0)")

print("="*70)
print("CHECK C: NON-DIAGONAL h(r) tensor EL vs closed form (independent variation)")
print("="*70)
# h depends on r only, but NON-DIAGONAL: h=[[P,S],[S,Q]], vary all 3 comps
P = sp.Function('P')(r); Q = sp.Function('Q')(r); S = sp.Function('S')(r)
W = sp.Function('W')(phi)   # keep branch symbolic
h = sp.Matrix([[P,S],[S,Q]])
hinv = h.inv()
sqrth = sp.sqrt(h.det())
e = sp.exp(-phi)
dh = sp.Matrix([[sp.diff(P,r), sp.diff(S,r)],[sp.diff(S,r), sp.diff(Q,r)]])
Kdd = sp.Rational(1,2)*e*dh
Kud = hinv*Kdd
Ktr = sp.trace(Kud)
KabKab = sp.trace(Kud*Kud)
calK = KabKab - Ktr**2
Lw = sp.simplify(sqrth*W*calK)

def EL_var(field):
    fp = sp.diff(field, r)
    return sp.simplify(sp.diff(Lw, field) - sp.diff(sp.diff(Lw, fp), r))

# closed-form tensor:  E^{AB} algebraic = W sqrt(h)[1/2 h^AB 𝒦 - 2 K^{AC}K_C^B + 2 K K^{AB}]
Kuu = hinv*Kdd*hinv
KAC_KCB = Kuu*h*Kuu          # K^{AC} h_{CD} K^{DB} = K^{AC} K_C{}^{B}
alg = sp.zeros(2,2)
for A in range(2):
    for B in range(2):
        alg[A,B] = W*sqrth*( sp.Rational(1,2)*hinv[A,B]*calK - 2*KAC_KCB[A,B] + 2*Ktr*Kuu[A,B] )
pi = sqrth*W*e*(Kuu - Ktr*hinv)

# Relationship between scalar EL wrt component and tensor: for h_AB with A!=B,
# h_12 = h_21 = S appears TWICE in the symmetric matrix, so dS carries a factor 2.
# Test each scalar EL against the appropriate closed-form combination.
EL_P = EL_var(P); EL_Q = EL_var(Q); EL_S = EL_var(S)
closed_P = sp.simplify(alg[0,0] - sp.diff(pi[0,0], r))
closed_Q = sp.simplify(alg[1,1] - sp.diff(pi[1,1], r))
# off-diagonal: dL/dS = dL/dh_12 + dL/dh_21 = 2 * (tensor_12); expect EL_S = 2*(alg[0,1]-d_r pi[0,1])
closed_S = sp.simplify(2*(alg[0,1] - sp.diff(pi[0,1], r)))
print("  EL_P - closed_P =", sp.simplify(EL_P - closed_P))
print("  EL_Q - closed_Q =", sp.simplify(EL_Q - closed_Q))
print("  EL_S - 2*closed_S_offdiag =", sp.simplify(EL_S - closed_S))
# also confirm pi identification via kinetic momentum
print("  dL/dP' - pi^{11} =", sp.simplify(sp.diff(Lw, sp.diff(P,r)) - pi[0,0]))
print("  dL/dS' - 2 pi^{12} =", sp.simplify(sp.diff(Lw, sp.diff(S,r)) - 2*pi[0,1]))

print("="*70)
print("CHECK D: does K_AB carry a phi' term? (would break the 'no phi cross-term' claim)")
print("="*70)
# K_AB = 1/2 e^{-phi} d_r h_AB : purely algebraic in phi, no phi'. Confirm 𝒦 has no phi'.
print("  d𝒦/d(phi') present? :", sp.diff(calK, sp.diff(phi,r)), " (expect 0)")

print("="*70)
print("CHECK E: G^(2)_AB = 0 for a genuinely non-round (r,theta)-warped 2-metric")
print("="*70)
th, ps = sp.symbols('theta psi')
# fully non-round: both components arbitrary functions of theta AND with cross term
F = sp.Function('F')(th); Gf = sp.Function('G')(th); H = sp.Function('H')(th)
g2 = sp.Matrix([[F, H],[H, Gf]])
g2i = g2.inv()
coords=[th,ps]
n=2
def christ(g):
    gi=g.inv()
    Ga=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                s=0
                for sd in range(n):
                    s+=gi[l,sd]*(sp.diff(g[sd,m],coords[k])+sp.diff(g[sd,k],coords[m])-sp.diff(g[m,k],coords[sd]))
                Ga[l][m][k]=sp.together(s/2)
    return Ga
Ga=christ(g2)
Ric=sp.zeros(n,n)
for m in range(n):
    for k in range(n):
        s=0
        for l in range(n):
            s+=sp.diff(Ga[l][m][k],coords[l])-sp.diff(Ga[l][m][l],coords[k])
            for p in range(n):
                s+=Ga[l][l][p]*Ga[p][m][k]-Ga[l][k][p]*Ga[p][m][l]
        Ric[m,k]=sp.simplify(s)
Rs=sp.simplify(sum(g2i[i,j]*Ric[i,j] for i in range(2) for j in range(2)))
G2=sp.simplify(Ric - sp.Rational(1,2)*g2*Rs)
print("  G^(2) =", G2)
