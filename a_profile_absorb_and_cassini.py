# a_profile_absorb_and_cassini.py
# MAP+OBSERVE support for udt_a_profile_MAP_results.md (2026-06-18).
# Tests:
#  (A) Is a POSITION-VARYING weight W(phi(r)) on the source still absorbable
#      by the Bianchi tautology? (general W, then W=exp(int (a(phi)+1) dphi)).
#  (B) Does the self-consistent-phi extra structure change the absorbability?
#  (C) Cassini PPN: what order n at which a(phi)=-1+c_n phi^n is allowed.
#  NO particle mass derived. NO verdict targeted. NOT canon.

import sympy as sp

r = sp.symbols('r', positive=True)
phi = sp.Function('phi')(r)
print("="*70)
print("(A) GENERAL POSITION-VARYING WEIGHT: is W(phi(r)) T absorbable?")
print("="*70)
# The left side is the STANDARD Einstein tensor (P2, the chosen GR-leak,
# carried over unchanged from prior passes). Contracted Bianchi: nabla_mu G^{mu nu}=0
# IDENTICALLY for ANY metric. So for G = kappa0 W T:
#   0 = nabla_mu(kappa0 W T^{mu nu}) = kappa0 [ W nabla_mu T^{mu nu} + (nabla_mu W) T^{mu nu} ]
#   => nabla_mu T^{mu nu} = -(d ln W/dphi) (partial_mu phi) T^{mu nu}     [the exchange law]
# Now define T~ = W T. Then nabla_mu T~^{mu nu}
#   = W nabla_mu T^{mu nu} + (nabla_mu W) T^{mu nu}
#   = W[ -(d ln W/dphi) partial phi T ] + (dW/dphi partial phi) T
#   = -W' /W *W ... let's do it symbolically with W an ARBITRARY function of phi.

W = sp.Function('W')(phi)            # arbitrary weight as a function of phi (=> of r)
T = sp.Function('T')(r)              # a generic source component (schematic scalar stand-in)
# schematic 1D "divergence" d/dr to expose the algebraic cancellation structure
# (full covariant version done in prose; the algebraic tautology is chart-independent).
dlnW = sp.diff(sp.log(W), r)         # d ln W/dr = (dW/dphi)(dphi/dr)/W
exchange = -dlnW * T                 # nabla T = -(dlnW/dr) T   (the Bianchi-forced law)
# Build nabla(W T) using the exchange law for nabla T:
nabla_WT = sp.diff(W, r)*T + W*exchange
print("nabla(W*T) using the Bianchi-forced exchange law nabla T = -(dlnW/dr) T:")
print("  =", sp.simplify(nabla_WT))
print("  -> EXACTLY ZERO for ARBITRARY W(phi).  W can be exp(int (a(phi)+1) dphi).")
print()
print("CONCLUSION (A): the tautology nabla(W T)=0 holds for ANY scalar weight W,")
print("including a NON-CONSTANT a(phi). Position-varying a(phi) does NOT, by itself,")
print("break the absorbability. T~=W T is still covariantly conserved -> relabels to GR.")
print()

print("="*70)
print("(A2) WHY it is robust: the cancellation is W'-vs-W' structural, exponent-free")
print("="*70)
a = sp.Function('a')(phi)
Wexp = sp.exp(sp.Integral(a+1, phi))   # W = exp(int (a(phi)+1) dphi); dW/dphi = (a+1)W
dWdphi = sp.diff(Wexp, phi)
print("d/dphi exp(int (a(phi)+1) dphi) =", sp.simplify(dWdphi), " = (a(phi)+1)*W  [checks]")
print("So d ln W/dphi = a(phi)+1, exactly the local exchange rate. The Bianchi")
print("identity uses d ln W/dphi WHATEVER its phi-dependence -> cancellation is exact.")
print()

print("="*70)
print("(B) DOES SELF-CONSISTENT phi (phi IS the metric) add a non-absorbable piece?")
print("="*70)
# Metric: g_tt=-e^{-2phi}c0^2, g_rr=e^{2phi}, areal r. Compute Box_g phi and check
# the identity Box_g phi = -G^th_th (banked prior). The question: with a(phi) varying,
# does the th-th equation Box_g phi = -kappa0 W T^th_th carry a SECOND, non-scalar weight?
c0 = sp.symbols('c0', positive=True)
g_tt = -sp.exp(-2*phi)*c0**2
g_rr =  sp.exp(2*phi)
g_thth = r**2
g_phph = r**2*sp.sin(sp.Symbol('th'))**2
th = sp.Symbol('th')
g = sp.diag(g_tt, g_rr, g_thth, r**2*sp.sin(th)**2)
ginv = g.inv()
coords = [sp.Symbol('t'), r, th, sp.Symbol('ph')]
detg = g.det()
sqrtmg = sp.sqrt(-detg)
# Box_g phi = (1/sqrt(-g)) d_mu( sqrt(-g) g^{mu nu} d_nu phi ); phi depends on r only
Box = sp.simplify( sp.diff(sqrtmg*ginv[1,1]*sp.diff(phi, r), r) / sqrtmg )
print("Box_g phi =", sp.simplify(Box))
# G^th_th of this metric (compute via Ricci); reuse known result from prior doc:
# G^th_th = (2 r phi'^2 - r phi'' - 2 phi') e^{-2phi}/r. Check identity:
phir = sp.diff(phi, r); phirr = sp.diff(phi, r, 2)
G_thth = (2*r*phir**2 - r*phirr - 2*phir)*sp.exp(-2*phi)/r
print("Box_g phi + G^th_th =", sp.simplify(Box + G_thth), " (0 => identity confirmed)")
print()
print("So th-th eqn: Box_g phi = -kappa0 W(phi) T^th_th. The weight on the matter")
print("source-of-phi is the SAME scalar W(phi); the self-variation lives in the")
print("Box_g operator (geometry side), which is exponent-free. No SECOND weight.")
print("=> self-consistency does NOT manufacture a non-absorbable object from a(phi).")
print()

print("="*70)
print("(C) CASSINI / PPN ORDER: how fast may a(phi) peel from -1 at phi=0?")
print("="*70)
# The non-absorbable fingerprint runs as F(phi)=exp(-int_0^phi (a+1) dphi').
# Write a(phi) = -1 + sum_{k>=n} c_k phi^k  (a(0) forced = -1, see prose).
# Then (a+1) = c_n phi^n + ... ; int_0^phi (a+1) = c_n phi^{n+1}/(n+1)+...
# The PPN gamma deviation in such a source-weight model scales with the LEADING
# departure of the matter coupling from metric-locked. We expose the phi-order.
n = sp.symbols('n', integer=True, positive=True)
phi_s = sp.symbols('phi', real=True)
cn = sp.symbols('c_n', real=True)
ap1 = cn*phi_s**n                      # leading (a+1)
F = sp.exp(-sp.integrate(ap1, (phi_s, 0, phi_s)))
print("Leading (a+1) = c_n phi^n ; fingerprint F(phi)=exp(-int_0^phi (a+1)) =")
print("   F =", sp.simplify(F), "  ~ 1 - c_n phi^{n+1}/(n+1) + ...")
for nval in [0, 1, 2]:
    Fn = sp.exp(-sp.integrate(cn*phi_s**nval, (phi_s, 0, phi_s)))
    print("   n=%d: (a+1)=c_n phi^%d -> F ~" % (nval, nval),
          sp.series(Fn, phi_s, 0, 4).removeO())
print()
print("In the solar system phi ~ U/c^2 ~ 1e-6 (Sun's potential). The fractional")
print("departure of the matter ruler from the metric ruler over a lab/solar path is")
print("~ c_n phi^{n+1}. PPN gamma picks up a deviation ~ this size.")
print("Cassini: |gamma-1| < 2.3e-5  with phi_solar ~ 1e-6 ... 1e-8 (planetary).")
print("=> any n>=0 with O(1) c_n is FAR below Cassini (phi^{n+1} <= 1e-6).")
print("   Even n=0 (a+1 = const != 0, i.e. a constant != -1) gives departure ~phi ~1e-6,")
print("   which is < 2.3e-5 -> Cassini does NOT by itself force a(0)=-1 numerically;")
print("   it bounds the CONSTANT part |a+1| < ~20 at solar phi. a(0)=-1 comes from the")
print("   PRINCIPLE (equivalence principle / no fifth force), NOT from Cassini alone.")
print("   Cassini's real bite: bounds the LOW-ORDER coefficients; the n-th order")
print("   departure is allowed for ANY n>=0 because solar phi is tiny.")
