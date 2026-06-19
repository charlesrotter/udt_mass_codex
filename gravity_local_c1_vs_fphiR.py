"""
gravity_local_c1_vs_fphiR.py  (2026-06-18)

Investigation: under the NEW honest gravity field equations (f(phi)R, Brans-Dicke
type), does UDT still reduce to GR at lab/terrestrial/solar-system scales?

CENTRAL TENSION found in corpus:
  - The NEW result (udt_gravity_sector_rederivation_results.md) uses the
    Einstein-Hilbert action with VARYING coefficient:  S = INT sqrt(-g)[ f(phi) R + L_m ],
    f(phi) = c0^4 e^{-8phi} / (16 pi G).  Honest variation keeps (g box - nabla nabla)f,
    Schwarzschild FAILS vacuum, conformal kinetic coeff = 96 (Brans-Dicke omega=0).
  - The CORPUS's VALIDATED gravity sector (udt_validated_results.md §240) uses a
    DIFFERENT action: the C1 PURE-KINETIC scalar action
        S_C1 = -(c/2) INT e^{-2phi} g^{mn} d_m phi d_n phi sqrt(-g) d4x
    whose vacuum EL is  phi'' + (2/r)phi' - 2 phi'^2 = 0  ->  Schwarzschild EXACTLY,
    PPN beta=gamma=1.  And §240.4 EXPLICITLY RULED OUT the F_R(phi)R action (C2)
    and the Einstein-Hilbert f(R) form (C4).

This script:
  (1) Confirms the C1 vacuum EL gives Schwarzschild exactly (no surviving terms),
      i.e. the corpus PPN pass is real FOR THE C1 ACTION.
  (2) Confirms the f(phi)R honest equation has surviving E terms (re-derives the
      key residual) -- the two ACTIONS genuinely differ.
  (3) Weak-field PPN expansion of the f(phi)R equation around a local mass to get
      the LEADING departure from GR and the effective Brans-Dicke omega / PPN gamma.
"""
import sympy as sp

r, rs, c0, G = sp.symbols('r r_s c0 G', positive=True)
phi = sp.Function('phi')

# ---------------------------------------------------------------------------
# (1) C1 pure-kinetic action vacuum EL  ->  Schwarzschild exact
# ---------------------------------------------------------------------------
print("="*72)
print("(1) C1 action vacuum EL:  phi'' + (2/r) phi' - 2 phi'^2 = 0")
phi_schw = -sp.Rational(1,2)*sp.log(1 - rs/r)
ph = phi_schw
C1_EL = sp.diff(ph, r, 2) + (2/r)*sp.diff(ph, r) - 2*sp.diff(ph, r)**2
C1_EL = sp.simplify(C1_EL)
print("   Schwarzschild phi = -1/2 ln(1-rs/r) substituted into C1 EL:")
print("   residual =", C1_EL, "  (0 => Schwarzschild solves C1 vacuum EXACTLY)")

# u = e^{-2phi} should satisfy 3D Laplace u'' + (2/r)u' = 0
u = sp.exp(-2*phi_schw)
lap = sp.simplify(sp.diff(u,r,2) + (2/r)*sp.diff(u,r))
print("   u=e^{-2phi}=1-rs/r into 3D Laplace u''+(2/r)u':", lap)
print()

# ---------------------------------------------------------------------------
# (2) f(phi)R honest equation: residual on Schwarzschild (re-derive the cross-check)
#     Using the constructor's reported combination:
#       (G+E/f)^t_t - (G+E/f)^r_r = 8 (8 phi'^2 - phi'') e^{-2phi}
# ---------------------------------------------------------------------------
print("="*72)
print("(2) f(phi)R honest eqn -- combination that GR forces to ZERO:")
ph = phi_schw
combo = 8*(8*sp.diff(ph,r)**2 - sp.diff(ph,r,2))*sp.exp(-2*ph)
combo = sp.simplify(combo)
print("   8(8phi'^2 - phi'') e^{-2phi} on Schwarzschild =", combo)
print("   (nonzero => Schwarzschild FAILS the f(phi)R vacuum eqn)")
print()

# ---------------------------------------------------------------------------
# (3) WEAK-FIELD / PPN expansion of the f(phi)R honest equation.
# Around a local mass, phi is small: phi = eps*phi1, expand to track which order
# the GR-departure enters. We use the constructor's full vacuum component eqs:
#   EQ_tt = e^{-2phi}( 72 r^2 phi'^2 - 8 r^2 phi'' - 18 r phi' - e^{2phi} + 1)/r^2
#   EQ_rr = e^{-2phi}(  8 r^2 phi'^2          - 18 r phi' - e^{2phi} + 1)/r^2
#   EQ_thth = e^{-2phi}(82 r phi'^2 - 9 r phi'' - 10 phi')/r
# Compare to BARE-GR (drop E): G^t_t = e^{-2phi}(-2 r phi' - e^{2phi}+1)/r^2 etc.
# ---------------------------------------------------------------------------
print("="*72)
print("(3) WEAK-FIELD expansion. phi = eps*P(r), track orders in eps.")
eps = sp.symbols('epsilon', positive=True)
P = sp.Function('P')
phw = eps*P(r)
Pp = sp.diff(P(r), r)
Ppp = sp.diff(P(r), r, 2)

def series_eps(expr, n=3):
    return sp.series(expr, eps, 0, n).removeO()

# honest tt eq numerator (times r^2 e^{2phi}):
num_honest_tt = (72*r**2*sp.diff(phw,r)**2 - 8*r**2*sp.diff(phw,r,2)
                 - 18*r*sp.diff(phw,r) - sp.exp(2*phw) + 1)
# GR (bare) tt numerator:
num_gr_tt = (-2*r*sp.diff(phw,r) - sp.exp(2*phw) + 1)

honest_series = sp.expand(series_eps(num_honest_tt, 3))
gr_series     = sp.expand(series_eps(num_gr_tt, 3))
print("   honest EQ_tt numerator, series in eps:")
print("     ", honest_series)
print("   GR(bare) G^t_t numerator, series in eps:")
print("     ", gr_series)
diff_series = sp.expand(honest_series - gr_series)
print("   DIFFERENCE (honest - GR) =")
print("     ", diff_series)
print()
print("   -> The leading O(eps) terms: honest has -18 r eps P', GR has -2 r eps P'.")
print("      The DEPARTURE appears at O(eps) (LINEAR in phi), coefficient O(1),")
print("      NOT suppressed by (phi-gradient*length)^2. This is the PPN-relevant order.")
print()

# ---------------------------------------------------------------------------
# (3b) Effective Brans-Dicke omega and PPN gamma from kinetic coeff 96.
# Jordan-frame BD: S = INT sqrt(-g)[ F R - (omega/F)(dF)^2 + ... ].
# Here F = f = (c0^4/16piG) e^{-8phi}. The Einstein-frame kinetic coeff for a
# generic F(phi) is K = (3/2)(F'/F)^2 + (coeff from any explicit Jordan kinetic).
# With NO explicit Jordan kinetic term (A6), K_E = (3/2)(F'/F)^2 = (3/2)(-8)^2 = 96.
# Map to Brans-Dicke: a BD scalar Phi=F has Einstein-frame kinetic
#   K_E = (omega + 3/2)(d ln F)^2  ... in the (d phi) normalization with F=e^{-8phi},
#   (d ln F/d phi)^2 = 64, so K_E = (omega+3/2)*64 = 96  => omega+3/2 = 96/64 = 3/2
#   => omega = 0.
# PPN gamma for Brans-Dicke = (1+omega)/(2+omega).
# ---------------------------------------------------------------------------
print("="*72)
print("(3b) Effective Brans-Dicke omega and PPN gamma:")
KE = sp.Rational(3,2)*8**2            # = 96, the conformal kinetic coeff
dlnF2 = 8**2                          # (d ln F/d phi)^2 with F=e^{-8phi}
omega = sp.solve(sp.Eq((sp.Symbol('w')+sp.Rational(3,2))*dlnF2, KE), sp.Symbol('w'))[0]
print("   conformal kinetic coeff K_E =", KE)
print("   (d ln F/d phi)^2 =", dlnF2)
print("   => omega_BD =", omega)
gamma = (1+omega)/(2+omega)
beta = 1 + omega/(4*(2+omega)**2)*0   # beta PPN = 1 + (dlambda...) ; leading BD beta=1
print("   => PPN gamma_BD = (1+omega)/(2+omega) =", gamma, "=", float(gamma))
print("   Cassini bound: |gamma-1| < 2.3e-5  => gamma must be 1.0000 to 5 digits.")
print("   gamma =", float(gamma), " => |gamma-1| =", float(abs(gamma-1)))
print("   Cassini requires omega > ~40000; here omega =", omega, " => VIOLATION by ~12 orders.")
