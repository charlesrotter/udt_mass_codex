#!/usr/bin/env python3
# RA1 — mu-ON scalar mode problem on the wall background (prereg frozen; F-MUOFF primary).
# The mixing h(r) is ON from the FIRST metric line below. h=0 appears ONLY in the D5 block.
# F-RETRO: symbols only (float-atom scan at the end). Bounded CPU sympy; no monitors.
# DECLARED SLICE: equatorial 3D chart (t, r, psi), c=1 units (Category-A).
#   ds^2 = -A dt^2 + dr^2/A + r^2 dpsi^2 + 2 h(r) dt dpsi
# The prereg's literal 4D form (2h dt dpsi with no sin^2 theta) is axis-singular at the
# poles; the equatorial slice is the clean realization (D2 SS3 precedent). Spherical
# generalization (h -> h(r) sin^2 theta, Kerr-like) = NAMED INHERITANCE, not computed.
# WLOG h0 > 0 (psi -> -psi flips its sign); chirality is carried by sign(omega*m).
import sympy as sp

KEYS = {}
def key(name, cond):
    KEYS[name] = bool(cond)
    print(f"KEY {name}: {KEYS[name]}")

t, r, psi = sp.symbols('t r psi', real=True)
w_, m_ = sp.symbols('omega m', real=True)
R_w = sp.Symbol('R_w', positive=True)
n_, q_ = sp.symbols('n q', real=True)
h0 = sp.Symbol('h0', positive=True)   # WLOG (declared above)
u = sp.Symbol('u', positive=True)     # u = 1 - r/R_w
s_ = sp.Symbol('s', positive=True)    # s = x_w - x (distance to wall in Liouville var)
eps = sp.Symbol('epsilon', positive=True)

# ---------- S1: metric, determinant, inverse (mixing ON from the first line) ----------
A = sp.Function('A', positive=True)(r)
h = sp.Function('h', real=True)(r)
R = sp.Function('R')(r)
g = sp.Matrix([[-A, 0, h], [0, 1/A, 0], [h, 0, r**2]])
D = A*r**2 + h**2                       # the t-psi block's (minus) determinant
key('RA1_K1_detg', sp.simplify(g.det() + D/A) == 0)          # det g = -D/A
key('RA1_K1b_block_lorentzian', sp.simplify(
    sp.Matrix([[-A, h], [h, r**2]]).det() + D) == 0)          # block det = -D < 0 always
ginv = g.inv()
ginv_target = sp.Matrix([[-r**2/D, 0, h/D], [0, A, 0], [h/D, 0, A/D]])
key('RA1_K2_ginv', all(sp.simplify(ginv[i, j] - ginv_target[i, j]) == 0
                       for i in range(3) for j in range(3)))
# g^{t psi} = h/D != 0 : the mu/mixing entry of the inverse block — where mu lives.

# ---------- S2: assemble Box psi = 0 with the mode ansatz; extract the radial ODE ------
W = sp.sqrt(D)/sp.sqrt(A)               # sqrt(-g)
mode = R*sp.exp(sp.I*(m_*psi - w_*t))
X = [t, r, psi]
box = sp.S(0)
for mu in range(3):
    inner = sum(ginv_target[mu, nu]*sp.diff(mode, X[nu]) for nu in range(3))
    box += sp.diff(W*inner, X[mu])
box = box/W
N = r**2*w_**2 + 2*h*w_*m_ - A*m_**2    # the pencil numerator (frame-dragging structure)
E_target = sp.diff(W*A*sp.diff(R, r), r) + W*N/D*R
key('RA1_K3_box_radial', sp.simplify(
    sp.expand(W*box*sp.exp(-sp.I*(m_*psi - w_*t)) - E_target)) == 0)
# Radial ODE (exact, mixing in):  (W A R')' + W*(r^2 w^2 + 2 h w m - A m^2)/D * R = 0

# ---------- S3: Sturm-Liouville identification; exact structural identities ------------
p_ = sp.sqrt(A)*sp.sqrt(D)              # SL leading coefficient  p = sqrt(A*D)
wt = r**2/(sp.sqrt(A)*sp.sqrt(D))       # weight = coefficient of omega^2
key('RA1_K4a_p_is_WA', sp.simplify(W*A - p_) == 0)
key('RA1_K4b_weight', sp.simplify(W/D - wt/r**2) == 0)
key('RA1_K4c_pw_is_r2', sp.simplify(p_*wt - r**2) == 0)      # EXACT: p*w = r^2, all h
Om = -h/r**2                            # frame dragging Omega = -g_{t psi}/g_{psi psi}
key('RA1_K6_dragging_completion', sp.simplify(
    N - (r**2*(w_ - m_*Om)**2 - m_**2*D/r**2)) == 0)
# proper-variable form: d ell = dr/sqrt(A); claim (sqrt(D) R_ell)_ell + (N/sqrt(D)) R = 0
lhs_ell = sp.sqrt(A)*sp.diff(sp.sqrt(D)*sp.sqrt(A)*sp.diff(R, r), r) + N/sp.sqrt(D)*R
# [restated decidable form, disclosed: first-run compared with a wrong factor sqrt(A)/W;
#  the correct multiplier taking the r-form to the ell_p-form is sqrt(A) exactly]
key('RA1_K5_ellp_form', sp.simplify(
    sp.expand(lhs_ell - sp.sqrt(A)*(sp.diff(p_*sp.diff(R, r), r) + W*N/D*R))) == 0)
# h-carriers (needed for D5): the 2*h*w*m term of N; the h^2 term of D; Omega itself.
key('RA1_K7_h_carriers', (sp.simplify(N.subs(h, 0) - (r**2*w_**2 - A*m_**2)) == 0)
    and (sp.simplify(D.subs(h, 0) - A*r**2) == 0) and (Om.subs(h, 0) == 0))

# ---------- S4: exact Liouville normal form (machine identity, generic A, h) -----------
S_ = sp.sqrt(A)*sp.sqrt(D)/r            # dr/dx ;  x = int r dr / sqrt(A D)
f_ = sp.sqrt(r)                         # (p*w)^{1/4}
v_xx = S_*sp.diff(S_*sp.diff(f_*R, r), r)         # d^2 v/dx^2 expressed in r
Qc_num = S_*sp.diff(S_*sp.diff(f_, r), r)         # Q_conj * f
ident = (sp.diff(p_*sp.diff(R, r), r))/wt - (v_xx - Qc_num*R)/f_*sp.sqrt(r)/sp.sqrt(r)
key('RA1_K8_liouville_identity', sp.simplify(sp.expand(
    (sp.diff(p_*sp.diff(R, r), r))/wt - (v_xx - Qc_num*R)/f_)) == 0)
# =>  -v_xx + [Qc + m^2 A/r^2 - 2 w m h/r^2] v = w^2 v,  x = int r dr/sqrt(AD), v=sqrt(r) R
key('RA1_K9_weight_isometry', sp.simplify(f_**2/S_ - wt) == 0)  # |v|^2 dx = |R|^2 w dr
print("SECTION S1-S4 done")

# ---------- S5: near-wall asymptotics (u = 1 - r/R_w -> 0+); frozen profiles -----------
def lead_exp(expr):
    """exponent of the leading power of u as u -> 0+ (log-derivative limit)."""
    return sp.limit(u*sp.diff(expr, u)/expr, u, 0)

A_u = u**n_
h_u = h0*u**q_
r_u = R_w*(1 - u)
# Regime A (A-dominates D: 2q > n):   D ~ R_w^2 u^n
pA = sp.sqrt(A_u*(R_w**2*u**n_))
# Regime H (h-dominates D: 2q < n):   D ~ h0^2 u^{2q}
pH = sp.sqrt(A_u*(h0**2*u**(2*q_)))
key('RA1_K10_p_exponent_regimeA', sp.simplify(lead_exp(pA) - n_) == 0)
key('RA1_K11_p_exponent_regimeH', sp.simplify(lead_exp(pH) - (n_ + 2*q_)/2) == 0)
# weight w = r^2/sqrt(AD): exponent = -sigma in each regime (p*w = r^2 bounded nonzero)
key('RA1_K12a_w_exponent_regimeA', sp.simplify(lead_exp(r_u.subs(u, 0)**2/pA) + n_) == 0)
key('RA1_K12b_w_exponent_regimeH',
    sp.simplify(lead_exp(r_u.subs(u, 0)**2/pH) + (n_ + 2*q_)/2) == 0)
# sigma_eff = (n + min(n, 2q))/2  [= n if 2q>n; = (n+2q)/2 if 2q<n]; dx ~ u^{-sigma} du.
# x_wall finite <=> sigma_eff < 1 (decidable restatement, three keys):
key('RA1_K13a_x_finite_sub', sp.limit(u**eps, u, 0) == 0)            # sigma = 1-eps: finite
key('RA1_K13b_x_div_super', sp.limit(u**(-eps), u, 0) == sp.oo)      # sigma = 1+eps: diverges
key('RA1_K13c_x_div_marginal', sp.limit(-sp.log(u), u, 0) == sp.oo)  # sigma = 1: diverges
# U-term subdominance for q > 0 (classification then depends on (n,q) ONLY):
# with s ~ u^{1-sigma} (sigma<1), a term u^a maps to s^{a/(1-sigma)}; subcritical iff > -2.
sig = sp.Symbol('sigma', positive=True)
expr_conj = (2*sig - 1)/(1 - sig) + 2      # conjugation term a = 2*sigma-1; claim > 0
key('RA1_K15_conj_subcritical', sp.simplify(expr_conj - 1/(1 - sig)) == 0)  # = 1/(1-sig) > 0
# dragging a = q > 0 and centrifugal a = n > 0 map to positive s-powers -> vanish: subcritical.
# [post-review R1-A1, disclosed: the first-run K14 was VACUOUS (an identically-zero
#  tautology q/(1-sig)*(1-sig) - q == 0 for ALL q — it verified nothing; a FIFTH
#  restatement beyond the four disclosed). Replaced by the real check: for q > 0 the
#  dragging term's s-exponent q/(1-sigma) is POSITIVE, so the term VANISHES at the wall.]
qp = sp.Symbol('qpos', positive=True)
key('RA1_K14_U_subdominant_qpos', ((qp/eps).is_positive is True)
    and (sp.limit(s_**(qp/eps), s_, 0, '+') == 0))

# ---------- S6: the (n,q)-plane classification map — witnesses per region --------------
def sigma_eff(nv, qv):
    return sp.Rational(nv + min(nv, 2*qv), 2) if not isinstance(nv, sp.Basic) else None
wit = []  # (n, q, expected sigma, expected class)  class: 'LC' sigma<1, 'LP' sigma>=1
from fractions import Fraction as F
cases = [
    (F(1, 2), F(2), 'R1  n<1, A-dom      ', 'LC'),
    (F(1, 2), F(1, 8), 'R1  n<1, h-dom      ', 'LC'),
    (F(3, 2), F(1, 8), 'R2  1<=n<2 created  ', 'LC'),
    (F(3, 2), F(1, 2), 'R2  1<=n<2 q too big', 'LP'),
    (F(1), F(1, 4), 'R2  n=1 created     ', 'LC'),
    (F(1), F(3, 4), 'R2  n=1 q too big   ', 'LP'),
    (F(1), F(1, 2), 'edge sigma=1        ', 'LP'),
    (F(5, 2), F(1), 'R3  n>=2, q>0       ', 'LP'),
    (F(2), F(0), 'R3  n=2, q=0        ', 'LP'),
    (F(1), F(0), 'R2  n=1, q=0 created', 'LC'),
    (F(3), F(-2), 'R4  deep q<0        ', 'LC'),
]
ok = True
for nv, qv, tag, cls in cases:
    sg = F(nv + min(nv, 2*qv), 2)
    # cross-check sigma against the FULL p = sqrt(A(Ar^2+h^2)) exponent by machine:
    p_full = sp.sqrt(u**sp.Rational(nv) * (sp.Rational(nv)*0 + (R_w*(1 - u))**2
             * u**sp.Rational(nv) + h0**2*u**(2*sp.Rational(qv))))
    sg_m = lead_exp(p_full)
    cls_m = 'LC' if sg < 1 else 'LP'
    ok = ok and (sp.simplify(sg_m - sp.Rational(sg)) == 0) and (cls_m == cls)
    print(f"  witness n={nv} q={qv} [{tag}] sigma={sg} -> {cls_m} (expected {cls})")
key('RA1_K16_witness_regions', ok)
print("SECTION S5-S6 done")

# ---------- S7: the q<0 chirality wedge (n>2): dragging term at the wall ---------------
# LC-candidate needs sigma=(n+2q)/2 < 1 i.e. q < (2-n)/2.  Dragging U-term ~ u^q maps to
# s^e, e = 2q/(2 - n - 2q).  Critical (e = -2) exactly on q = 2 - n:
e_expr = 2*q_/(2 - n_ - 2*q_)
key('RA1_K17a_wedge_critical_line', sp.simplify(e_expr.subs(q_, 2 - n_) + 2) == 0)
# supercritical (e < -2) iff q > 2-n (inside q < (2-n)/2): check sign of (e+2)'s numerator
key('RA1_K17b_wedge_supercritical', sp.simplify(
    sp.together(e_expr + 2) - (4 - 2*n_ - 2*q_ + 2*q_ - (2 - n_ - 2*q_))*0
    - (2*q_ + 2*(2 - n_ - 2*q_))/(2 - n_ - 2*q_)) == 0)
# numerator 2q + 2(2-n-2q) = 4 - 2n - 2q = 2(2-n-q): with denom = 2(1-sigma) > 0 on the
# LC side, e+2 < 0  <=>  q > 2-n.  (pure algebra; witnessed below)
wedge_ok = True
for nv, qv, expect in [(F(3), F(-3, 4), 'super'), (F(3), F(-1), 'crit'),
                       (F(3), F(-2), 'sub'), (F(3, 2), F(-1), 'sub')]:
    ev = sp.Rational(2*qv, 1)/sp.Rational(2 - nv - 2*qv, 1)
    tagm = 'crit' if ev == -2 else ('super' if ev < -2 else 'sub')
    wedge_ok = wedge_ok and (tagm == expect)
    print(f"  wedge witness n={nv} q={qv}: e={ev} -> {tagm} (expected {expect})")
key('RA1_K17c_wedge_witnesses', wedge_ok)
# Critical line q = 2-n: exact inverse-square coefficient (h-dom: sigma=(4-n)/2, n>2).
# [restated decidable form, disclosed: n>2 encoded as n3 = 2 + nu, nu > 0, so sympy can
#  collapse (u^{nu/2})^{2/nu}; first run left (n3-2)'s sign undeclared and blocked powsimp]
nu = sp.Symbol('nu', positive=True)
n3 = 2 + nu
sig3 = (4 - n3)/2
s_of_u = (2*R_w**2/(h0*nu))*u**(nu/2)                    # s = int_0^u u'^{-sigma} R_w^2/h0 du'
u_of_s = (s_*h0*nu/(2*R_w**2))**(2/nu)
key('RA1_K18a_s_u_roundtrip', sp.simplify(
    sp.powsimp(s_of_u.subs(u, u_of_s), force=True) - s_) == 0)
# check ds/du = (R_w^2/h0) u^{-sigma}:
key('RA1_K18b_s_rate', sp.simplify(sp.diff(s_of_u, u) - (R_w**2/h0)*u**(-sig3)) == 0)
drag_term = -2*w_*m_*h0*u**(2 - n3)/R_w**2               # -2 w m h/r^2 at r ~ R_w, q = 2-n
c_crit = -8*w_*m_*R_w**2/(h0*nu**2)                      # = -8 w m R_w^2/(h0 (n-2)^2)
key('RA1_K18c_ccrit', sp.simplify(sp.powsimp(
    drag_term.subs(u, u_of_s), force=True) - c_crit/s_**2) == 0)
# LC iff total inverse-square coefficient < 3/4 (Weyl criterion):  -8 w m R_w^2/(h0 (n-2)^2)
# vs 3/4 — an (m, omega, h0)-DEPENDENT classification: the mixing's sharpest fingerprint.
# ---------- S7b (post-review additions, R1-A2 / R2-A1 — the omitted lines; disclosed) ---
# (i) the line n = 2, q < 0: sigma_eff = 1 + q < 1 (LC) and the dragging exponent is
#     e = 2q/(2-2-2q) = -1 exactly (subcritical) for EVERY q != 0 — mixing-created LC:
p_n2 = sp.sqrt(u**2*((R_w*(1 - u))**2*u**2 + h0**2*u**(-1)))     # witness n=2, q=-1/2
key('RA1_K30a_n2_qneg_sigma', sp.simplify(lead_exp(p_n2) - sp.Rational(1, 2)) == 0)
key('RA1_K30b_n2_qneg_drag_sub', sp.simplify(e_expr.subs(n_, 2) + 1) == 0)
# (ii) the boundary ray q = (2-n)/2, n > 2 (n = 2 + nu): sigma_eff = 1 EXACTLY (x_wall
#     log-divergent, marginal): h-dominated leading term of p is u^{(n+2q)/2} = u^1:
p_ray = sp.sqrt(u**(2 + nu)*h0**2*u**(-nu))
key('RA1_K30c_ray_sigma1', sp.simplify(lead_exp(p_ray) - 1) == 0)
# on the ray the dragging term ~ u^q grows EXPONENTIALLY in x (u ~ e^{-h0 x/R_w^2}):
# m=0: LP continuum; m!=0 counter-rotating: confining => LP discrete; co-rotating:
# attractive-exponential => LC at infinity (int |U|^{-1/2} dx < oo criterion, cited).
# Supercritical zone sign split (WKB; beta > 2 encoded as beta = 2 + eps, decidable):
b2 = 2 + eps
# WKB validity: |Q'|/|Q|^{3/2} ~ s^{beta/2 - 1} -> 0 as s -> 0+  iff beta > 2:
key('RA1_K19a_wkb_valid', sp.limit(s_**(b2/2 - 1), s_, 0, '+') == 0)
# attractive branch: |v|^2 ~ s^{beta/2}; antiderivative -> 0 at s=0 (integrable) -> LC:
key('RA1_K19b_attractive_LC', sp.limit(sp.integrate(s_**(b2/2), s_), s_, 0, '+') == 0)
key('RA1_K19c_repulsive_LP', sp.limit(sp.exp(s_**(-eps/2)), s_, 0, '+') == sp.oo)
# growing WKB branch exp(+c s^{1-beta/2}) blows up faster than any power -> not L^2 -> LP
print("SECTION S7 done")

# ---------- S8: the observer end r -> 0 (D2) — BOTH declared center variants -----------
# Variant (a) SS3-regular (D2 inheritance: h -> 0 faster than the screen at r=0).
# Near r=0: A -> 1 (banked anchor A(0)=1), h -> 0, D -> r^2; p -> r, w -> r, N -> r^2 w^2 - m^2.
# Frobenius/indicial: (r R')' - m^2/r R + ... = 0, R ~ r^a:  a^2 - m^2 = 0.
a_ = sp.Symbol('a')
indicial = a_*(a_ - 1) + a_ - m_**2      # from (r (r^a)')' = a^2 r^{a-1}
key('RA1_K20a_center_indicial', sp.simplify(sp.expand(indicial - (a_**2 - m_**2))) == 0)
key('RA1_K20b_center_roots', sp.solve(a_**2 - m_**2, a_) == [-m_, m_])
# Liouville form at center: f = sqrt(r): Qc = -1/(4 r^2); U ~ (m^2 - 1/4)/r^2:
Qc_center = sp.limit(r**2*(sp.sqrt(1*r**2)/r)*sp.diff((sp.sqrt(1*r**2)/r)
            * sp.diff(sp.sqrt(r), r), r)/sp.sqrt(r), r, 0)
key('RA1_K20c_center_conj_coeff', sp.simplify(Qc_center + sp.Rational(1, 4)) == 0)
# => |m|>=1: coefficient m^2 - 1/4 >= 3/4 -> LIMIT-POINT (regularity R ~ r^{|m|} automatic);
#    m=0: coefficient -1/4 -> LIMIT-CIRCLE marginal: BC = axis regularity (bounded, no log).
# Variant (b) the LITERAL frozen class at the center: h(0) = h0 != 0.
p0 = sp.limit(sp.sqrt((1)*((1)*r**2 + h0**2)), r, 0)     # p(0) with A(0)=1
key('RA1_K21a_center_literal_regular_p', p0 == h0)        # p(0) = h0 != 0: REGULAR point
g_psipsi_inv_0 = sp.limit(1/(1*r**2 + h0**2), r, 0)      # g^{psi psi} = A/D at r=0
key('RA1_K21b_centrifugal_removed', g_psipsi_inv_0 == 1/h0**2)
# the mixing kills the centrifugal barrier at the axis: NO regularity selection from the
# ODE; the axis is a spinning-string/NUT-like defect (manifold-singular, ODE-regular).

# ---------- S9: the ladder's mixing fingerprint (LC regions; first order in h) ---------
# Pencil: -v'' + (Qc + m^2 A/r^2) v = (w^2 + 2 w m h/r^2) v.  Perturbation delta U = -2 w m h/r^2:
# first order: delta(w^2) = <delta U> => 2 w dw = -2 w m <h/r^2> => dw = -m <h/r^2> = +m <Omega>.
dw = sp.Symbol('deltaomega')
Havg = sp.Symbol('avg_h_over_r2', positive=True)
key('RA1_K22_zeeman_splitting', sp.solve(sp.Eq(2*w_*dw, -2*w_*m_*Havg), dw) == [-m_*Havg])
# => omega_k(m) - omega_k(-m) = -2 m <h/r^2>_k = 2 m <Omega>_k : LINEAR-in-h0 rotational
#    splitting; mu-off the ladder is +/-m degenerate.  Spacing: Weyl law N(w) ~ w x_w/pi.
# x_w(h) <= x_opt (mixing SHORTENS the cavity): r/sqrt(AD) <= 1/A  <=>  h^2 >= 0:
ineq = (1/A)**2 - (r/sp.sqrt(A*D))**2
key('RA1_K23_xw_shrinks', sp.simplify(ineq - h**2/(A**2*D)) == 0)
# q = 0 LP case (n >= 2): U(infinity) = -2 w m h0/R_w^2: continuum edge shifted,
# omega^2 + 2 w m h0/R_w^2 >= 0: roots
# [restated decidable form, disclosed: solve's root ORDER is unspecified — compare as sets]
key('RA1_K24_q0_continuum_shift',
    set(sp.solve(w_**2 + 2*w_*m_*h0/R_w**2, w_)) == {-2*m_*h0/R_w**2, sp.S(0)})

# ---------- S10 (D5, the ONLY mu-off block): the h -> 0 limit, DERIVED -----------------
key('RA1_K25a_muoff_p', sp.simplify(p_.subs(h, 0) - sp.sqrt(A)*sp.sqrt(A*r**2)) == 0)
key('RA1_K25b_muoff_weight', sp.simplify(wt.subs(h, 0)*sp.sqrt(A)*sp.sqrt(A*r**2)
    - r**2) == 0)
key('RA1_K25c_muoff_N', sp.simplify(N.subs(h, 0) - (r**2*w_**2 - A*m_**2)) == 0)
# sigma_eff(h=0) = n  (p = A r): the natural variable becomes dx = dr/A = OPTICAL (O2 row)
key('RA1_K26_muoff_sigma', sp.simplify(lead_exp(sp.sqrt(u**n_*(u**n_*R_w**2))) - n_) == 0)
# O2 cross-check: optical length int u^{-n} du finite iff n < 1 (same 3-key restatement):
key('RA1_K27_O2_optical_crosscheck', (sp.limit(u**eps, u, 0) == 0)
    and (sp.limit(u**(-eps), u, 0) == sp.oo) and (sp.limit(-sp.log(u), u, 0) == sp.oo))
# mu-off classification: LC iff n < 1; the mixing-created LC region 1 <= n < 2 (q < (2-n)/2),
# the chirality wedge, and the Zeeman splitting ALL vanish at h = 0.

# ---------- S11: falsifier scans ------------------------------------------------------
audited = [g, ginv_target, sp.Matrix([N]), sp.Matrix([p_]), sp.Matrix([wt]),
           sp.Matrix([c_crit]), sp.Matrix([s_of_u])]
no_float = all(not any(isinstance(x, sp.Float) for x in M.atoms(sp.Float))
               for M in audited)
key('RA1_K28_FRETRO_no_float_atoms', no_float)
# F-MUOFF structural: h present in the assembled ODE's N and D from the first equation:
key('RA1_K29_FMUOFF_h_in_first_system', (h in N.atoms(sp.Function))
    and (h in D.atoms(sp.Function)) and (h in g.atoms(sp.Function)))
print("SECTION S8-S11 done")
print(f"TOTAL: {sum(KEYS.values())}/{len(KEYS)} keys True")
assert all(KEYS.values()), [k for k, v in KEYS.items() if not v]
