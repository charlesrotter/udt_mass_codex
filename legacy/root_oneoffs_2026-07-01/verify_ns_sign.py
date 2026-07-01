"""INDEPENDENT HOSTILE VERIFIER -- the nonstationary sign adjudication.
Agent: ns-verify (Opus 4.8 1M), 2026-06-13.
I build the dilation-tie 4-metric and the C1 dilation action FROM SCRATCH,
derive the reduced EL myself, and read the principal-part signature.
I do NOT trust ns_scan_symbol.py or v_a3.py reduced forms; I rederive both
the action weight AND the metric-determinant from the metric.
"""
import sympy as sp

print("="*70)
print("AXIS 1: THE SIGN, FROM SCRATCH")
print("="*70)

T, r, th = sp.symbols('T r theta', real=True)
P = sp.Function('phi')
phi = P(T, r, th)

# Canonical dilation tie (CANON C-2026-06-10-1): g_tt*g_rr = -1, areal.
# Lorentzian signature (-,+,+,+). g_tt = -e^{-2phi} reads phi off the clock.
gtt = -sp.exp(-2*phi)
grr =  sp.exp( 2*phi)
gthth = r**2
gphph = r**2*sp.sin(th)**2

# Full 4-determinant and its sign (independent check)
g4det = gtt*grr*gthth*gphph         # = -e^{-2}*e^{2}*r^2*... = -r^4 sin^2
print("g4 det =", sp.simplify(g4det), " (must be < 0 => Lorentzian)")
sqrtmg = sp.sqrt(-g4det)            # sqrt(-g)
sqrtmg = sp.simplify(sqrtmg)
print("sqrt(-g) =", sqrtmg)         # r^2 sin th

gTT = 1/gtt; gRR = 1/grr; gThTh = 1/gthth
print("g^{TT} =", sp.simplify(gTT), "  g^{rr} =", sp.simplify(gRR))

# ---- THE ACTION. The C1 dilation kinetic density.
# Question: what is the canonical weight? The action stated EVERYWHERE in
# this corpus (wint_symcheck, ns_scan_symbol, and v_a1_a2 as
# L=-(c/8)sqrt(-g) g^{mn} f_m f_n / f with f=e^{-2phi}) is the
# dilaton/sigma-model kinetic term.  Let me derive BOTH the e^{-2phi}-weighted
# form (ns) and the 1/f form (v_a1_a2) and confirm they're the SAME object.
c = sp.Symbol('c', positive=True)

# Form 1 (ns_scan_symbol): L1 = (c/2) e^{-2phi} g^{ab} phi_a phi_b sqrt(-g)
K = gTT*sp.diff(phi,T)**2 + gRR*sp.diff(phi,r)**2 + gThTh*sp.diff(phi,th)**2
L1 = sp.Rational(1,1)*(c/2)*sp.exp(-2*phi)*K*sqrtmg

# Form 2 (v_a1_a2): L2 = -(c/8) sqrt(-g) g^{ab} f_a f_b / f, f = e^{-2phi}
f = sp.exp(-2*phi)
Kf = gTT*sp.diff(f,T)**2 + gRR*sp.diff(f,r)**2 + gThTh*sp.diff(f,th)**2
L2 = -(c/8)*sqrtmg*Kf/f

print("\nDo the two stated action forms agree (up to overall const)?")
ratio12 = sp.simplify(L1/L2)
print("  L1/L2 =", ratio12, " (constant => same object)")

# Use L1 (the e^{-2phi} form). Derive EL.
def EL_of(L):
    pT=sp.diff(phi,T); pr=sp.diff(phi,r); pth=sp.diff(phi,th)
    return (sp.diff(L,phi)
            - sp.diff(sp.diff(L,pT),T)
            - sp.diff(sp.diff(L,pr),r)
            - sp.diff(sp.diff(L,pth),th))
EL = sp.simplify(EL_of(L1)/sp.exp(-2*phi)/sp.sin(th))
EL = sp.expand(EL)

phiTT=sp.Derivative(phi,T,2); phirr=sp.Derivative(phi,r,2)
phithh=sp.Derivative(phi,th,2)
cTT=sp.simplify(EL.coeff(phiTT))
cRR=sp.simplify(EL.coeff(phirr))
cTh=sp.simplify(EL.coeff(phithh))
print("\nPRINCIPAL PART (my own EL, e^{-2phi} action):")
print("  coeff(phi_TT)   =", cTT)
print("  coeff(phi_rr)   =", cRR)
print("  coeff(phi_thth) =", cTh)
print("  cTT/cRR =", sp.simplify(cTT/cRR), " (NEG=>hyperbolic)")
print("  cTT/cTh =", sp.simplify(cTT/cTh))

# ---- Now reproduce v_a3.py's reduced Lagrangian INDEPENDENTLY.
# v_a3 works with f(T,r) spherical, variable f (not phi). Reduce L2 in f,
# spherical (drop theta), and read the time/radial kinetic signs.
print("\n"+"="*70)
print("v_a3 CROSS-CHECK: reduce the action in f(T,r), spherical")
print("="*70)
Tr,rr = sp.symbols('T r', positive=True)
F = sp.Function('f', positive=True)(Tr,rr)
# spherical metric in terms of f = e^{-2phi}: g_tt=-f, g_rr=1/f, sqrt(-g)=r^2 sin
# g^{tt}=-1/f, g^{rr}=f.  L2 = -(c/8) sqrt(-g) g^{ab} f_a f_b / f
# = -(c/8) r^2 sin * ( -1/f * f_T^2 + f * f_r^2 ) / f
# = -(c/8) r^2 sin * ( -f_T^2/f^2 + f_r^2 )
Lred_mine = -(c/8)*rr**2*( -sp.diff(F,Tr)**2/F**2 + sp.diff(F,rr)**2 )
print("MY reduced L (drop sin):")
print("  L_red =", Lred_mine)
print("  => time kinetic sign:  +f_T^2/(... )? coefficient of f_T^2 =",
      sp.simplify(Lred_mine.coeff(sp.diff(F,Tr)**2)))
print("  => radial kinetic: coefficient of f_r^2 =",
      sp.simplify(Lred_mine.coeff(sp.diff(F,rr)**2)))

# v_a3 line 23 wrote: L = -(c/8) r^2 ( f_r^2 + f_T^2/f^2 )  [SAME sign]
Lred_va3 = -(c/8)*rr**2*( sp.diff(F,rr)**2 + sp.diff(F,Tr)**2/F**2 )
print("\nv_a3 line-23 reduced L:")
print("  L_va3 =", Lred_va3)
print("  sign of f_T^2 term:", sp.simplify(Lred_va3.coeff(sp.diff(F,Tr)**2)))

diff = sp.simplify(Lred_mine - Lred_va3)
print("\n MY L_red - v_a3 L_red =", diff,
      "\n (nonzero in f_T^2 => v_a3 has the f_T^2 sign FLIPPED)")
print("  difference is purely the f_T^2 term?:",
      sp.simplify(diff - (c/4)*rr**2*sp.diff(F,Tr)**2/F**2)==0)
