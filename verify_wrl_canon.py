"""
Independent adversarial verification of canon C-2026-07-09-1 (WR-L).
Zero-context re-derivation. Does NOT read the authors' out.json.

Checks:
  1a. Does the affine re-centering axiom FORCE the functional equation
      F(phi0+dphi) = F(phi0) + (1-F(phi0)) F(dphi)?  (derive it from scratch)
  1b. C^1 solutions of that FE with F(0)=0 -> are they exactly 1-e^{-lam*phi}?
      Any missed branches?
  2.  Wall conditions near eps=1-r/X->0, A=eps^alpha:
      (i)   optical  int dr/A     divergence   -> alpha condition
      (ii)  proper   int dr/sqrt(A) finiteness  -> alpha condition
      (iii) G^theta_theta = A''/2 + A'/r finite  -> alpha condition
      Is alpha=1 the UNIQUE common point? Does alpha>=2 sneak past (iii)?
  Also: independently verify G^theta_theta formula from the full metric.
"""
import sympy as sp

print("="*70)
print("STEP 1a: derive the functional equation from the re-centering axiom")
print("="*70)
# Setup: u = r/X = F(phi). Seat at r0 with depth phi0.
# Axiom pieces:
#   phi-additive re-centering (forced by A12=A1A2):  phi' = phi - phi0
#   affine areal re-centering (WR-L axiom):           r' = r - r0, X' = X - r0
#   same embedding in new frame:                      r'/X' = F(phi')
# with r = X F(phi), r0 = X F(phi0).
X = sp.symbols('X', positive=True)
F = sp.Function('F')
phi, phi0, dphi = sp.symbols('phi phi0 dphi', real=True)

r   = X*F(phi)
r0  = X*F(phi0)
lhs_ratio = (r - r0)/(X - r0)          # r'/X' expressed via F
lhs_ratio = sp.simplify(lhs_ratio)
print("r'/X' = (r-r0)/(X-r0) =", lhs_ratio)
# The axiom sets this equal to F(phi'):  F(phi-phi0).
# Substitute phi = phi0 + dphi so phi' = dphi:
axiom = sp.Eq(lhs_ratio.subs(phi, phi0+dphi), F(dphi))
print("Axiom (phi=phi0+dphi):", axiom)
# Solve for F(phi0+dphi):
Fsum = sp.solve(axiom, F(phi0+dphi))[0]
Fsum = sp.simplify(Fsum)
print("=> F(phi0+dphi) =", Fsum)
claim = F(phi0) + (1 - F(phi0))*F(dphi)
print("   claimed FE   =", claim)
print("   MATCH:", sp.simplify(Fsum - claim) == 0)

print()
print("="*70)
print("STEP 1b: solve the FE  F(a+b)=F(a)+(1-F(a))F(b),  F(0)=0")
print("="*70)
# Substitution G = 1 - F  =>  G(a+b) = G(a) G(b) (multiplicative Cauchy).
a, b, lam = sp.symbols('a b lam', real=True)
G = sp.Function('G')
# Check the reduction symbolically at the functional level:
# 1 - [F(a)+(1-F(a))F(b)]  ==  (1-F(a))(1-F(b))
Fa, Fb = sp.symbols('Fa Fb')
lhs = 1 - (Fa + (1-Fa)*Fb)
rhs = (1-Fa)*(1-Fb)
print("G(a+b) form check: 1-FE  ==  (1-Fa)(1-Fb):", sp.simplify(lhs-rhs)==0)
# Multiplicative Cauchy, continuous, G(0)=1, G>0 (since G(x)=G(x/2)^2>=0, nonvanishing):
#   G(x)=e^{c x}. For F(inf)=1 need G(inf)=0 => c<0 => c=-lam, lam>0.
# Verify the proposed solution satisfies the ORIGINAL FE:
Fsol = 1 - sp.exp(-lam*phi)
def FE(fexpr, va, vb):
    fa = fexpr.subs(phi, va); fb = fexpr.subs(phi, vb)
    fab = fexpr.subs(phi, va+vb)
    return sp.simplify(fab - (fa + (1-fa)*fb))
print("F=1-e^{-lam phi} satisfies FE:", FE(Fsol, a, b) == 0)
print("F(0)=0:", Fsol.subs(phi,0)==0)
# Adversarial: any polynomial/other continuous branch? multiplicative Cauchy
# continuous solutions are ONLY exp (or identically 0 -> F=1 degenerate).
# Test a decoy F = phi/(1+phi) (Moebius) - should FAIL the FE:
decoy = phi/(1+phi)
print("decoy F=phi/(1+phi) satisfies FE:", FE(decoy, a, b) == 0, "(expect False)")
# Map to A: A=e^{-2phi} => e^{-lam phi}=A^{lam/2}=A^s ; r/X=1-A^s ; A=(1-r/X)^(1/s)
print("=> r/X = 1 - A^s,  A=(1-r/X)^alpha, alpha=1/s ; L is alpha=1")

print()
print("="*70)
print("STEP 2: verify G^theta_theta = A''/2 + A'/r from the FULL metric")
print("="*70)
t, rr, th, ph = sp.symbols('t r theta phi_ang', real=True)
Afun = sp.Function('A')(rr)
g = sp.diag(-Afun, 1/Afun, rr**2, rr**2*sp.sin(th)**2)
ginv = g.inv()
coords = [t, rr, th, ph]
n = 4
# Christoffel
Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
for l in range(n):
    for i in range(n):
        for j in range(n):
            s = 0
            for m in range(n):
                s += ginv[l,m]*(sp.diff(g[m,i],coords[j])+sp.diff(g[m,j],coords[i])-sp.diff(g[i,j],coords[m]))
            Gamma[l][i][j] = sp.simplify(s/2)
# Ricci
Ric = sp.zeros(n)
for i in range(n):
    for j in range(n):
        s = 0
        for l in range(n):
            s += sp.diff(Gamma[l][i][j], coords[l]) - sp.diff(Gamma[l][i][l], coords[j])
            for m in range(n):
                s += Gamma[l][l][m]*Gamma[m][i][j] - Gamma[l][j][m]*Gamma[m][i][l]
        Ric[i,j] = sp.simplify(s)
Rscalar = sp.simplify(sum(ginv[i,i]*Ric[i,i] for i in range(n)))
# Einstein mixed G^theta_theta = g^{th th}(Ric_thth - 1/2 g_thth R)
G_th_th = sp.simplify(ginv[2,2]*(Ric[2,2] - sp.Rational(1,2)*g[2,2]*Rscalar))
target = sp.diff(Afun,rr,2)/2 + sp.diff(Afun,rr)/rr
print("G^theta_theta - (A''/2 + A'/r) =", sp.simplify(G_th_th - target))
print("  (0 confirms the formula in the doc/canon)")

print()
print("--- wall behavior: A=eps^alpha, eps=1-r/X, dr=-X d eps ---")
alpha, eps = sp.symbols('alpha epsilon', positive=True)
A_eps = eps**alpha
# (i) optical int dr/A = int eps^{-alpha}(X d eps): near 0 finite iff -alpha>-1 (alpha<1);
#     DIVERGES (infinite optical reach) iff alpha>=1.
print("(i) optical  int eps^{-alpha} d eps exponent:", -alpha,
      "-> diverges (inf reach) iff alpha>=1")
# (ii) proper int dr/sqrt(A)=int eps^{-alpha/2}: finite iff alpha/2<1 (alpha<2)
print("(ii) proper  int eps^{-alpha/2} d eps: finite iff alpha<2")
# (iii) A'' in terms of eps
A_of_r = (1 - rr/X)**alpha
App = sp.simplify(sp.diff(A_of_r, rr, 2))
Ap  = sp.simplify(sp.diff(A_of_r, rr))
print("A'' =", App, "  ~ eps^(alpha-2), coeff alpha(alpha-1)/X^2")
print("A'  =", Ap)
# Evaluate half-A'' + A'/r leading exponent for representative alphas in band and outside
for av in [sp.Rational(1,2), sp.Integer(1), sp.Rational(3,2), sp.Integer(2), sp.Integer(3)]:
    Aa = (1-rr/X)**av
    Gth = sp.diff(Aa,rr,2)/2 + sp.diff(Aa,rr)/rr
    # limit r->X
    lim = sp.limit(Gth, rr, X, '-')
    optical = "inf(ok)" if av>=1 else "finite(FAIL)"
    proper  = "finite(ok)" if av<2 else "inf(FAIL)"
    print(f"  alpha={av}: optical {optical:12s} proper {proper:12s} G^th_th(wall)={lim}")
print()
print("Band from (i)&(ii): 1<=alpha<2. Within it, finite G^th_th only at alpha=1.")
print("alpha>=2 gives finite G^th_th too, but is KILLED by proper-room (ii).")
