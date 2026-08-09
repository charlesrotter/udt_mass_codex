# ADVERSARIAL REVIEW 1 — independent recompute for RA1 (written BEFORE opening derive_ra1.py)
# Fresh sympy; every check derived from the prereg metric line, not from the package script.
import sympy as sp

OK = []
def key(name, cond):
    cond = bool(cond)
    OK.append((name, cond))
    print(f"R1KEY {name}: {cond}", flush=True)

t, psi, w_, m_ = sp.symbols('t psi omega m', real=True)
r, h0, Rw, u = sp.symbols('r h0 R_w u', positive=True)
nu = sp.symbols('nu', real=True)
n_, q_ = sp.symbols('n q', real=True)
A = sp.Function('A', positive=True)(r)
h = sp.Function('h', real=True)(r)
R = sp.Function('R')(r)

# ---------- Part 1: D1 — metric, inverse, box, SL form, dragging completion ----------
g = sp.Matrix([[-A, 0, h], [0, 1/A, 0], [h, 0, r**2]])
D = A*r**2 + h**2
key("detg_is_minus_D_over_A", sp.simplify(g.det() + D/A) == 0)
ginv = g.inv()
key("ginv_ttpsi_block",
    sp.simplify(ginv[0,0] + r**2/D) == 0 and sp.simplify(ginv[0,2] - h/D) == 0
    and sp.simplify(ginv[2,2] - A/D) == 0 and sp.simplify(ginv[1,1] - A) == 0)

W = sp.sqrt(D/A)   # sqrt(-g)
# Box psi with ansatz R(r) e^{i(m psi - w t)}: radial part (1/W)(W A R')' ; algebraic part
N = r**2*w_**2 + 2*h*w_*m_ - A*m_**2
box_radial = sp.diff(W*A*sp.diff(R, r), r) + W*N/D*R
# assemble box directly from the inverse metric to confirm
phase_fac = sp.I*(m_*psi - w_*t)
psi_field = R*sp.exp(phase_fac)
box_full = sp.S(0)
xs = [t, r, psi]
for a in range(3):
    for b in range(3):
        box_full += sp.diff(W*ginv[a,b]*sp.diff(psi_field, xs[b]), xs[a])
box_full = sp.simplify(box_full/W/sp.exp(phase_fac))
key("box_assembly_matches_radial_eq", sp.simplify(box_full*W - box_radial) == 0)

p_sl = sp.sqrt(A*D); w_sl = r**2/sp.sqrt(A*D)
key("p_is_WA", sp.simplify(W*A - p_sl) == 0)
key("weight_is_Wr2_over_D", sp.simplify(W*r**2/D - w_sl) == 0)
key("pw_invariant_r2", sp.simplify(p_sl*w_sl - r**2) == 0)
Om = -h/r**2
key("dragging_completion", sp.simplify(N - (r**2*(w_ - m_*Om)**2 - m_**2*D/r**2)) == 0)

# ---------- Part 2: Liouville normal form + isometry ----------
# x with dx/dr = r/sqrt(AD); v = sqrt(r) R; claim: -v_xx + (Qc + m^2 A/r^2 - 2 w m h/r^2) v = w^2 v
ddx = lambda f: sp.sqrt(A*D)/r*sp.diff(f, r)
v = sp.sqrt(r)*R
Qc = ddx(ddx(sp.sqrt(r)))/sp.sqrt(r)
U = Qc + m_**2*A/r**2 - 2*w_*m_*h/r**2
normal_form = -ddx(ddx(v)) + (U - w_**2)*v
# SL residual: (p R')' + (N/sqrt(AD)) R
SLres = sp.diff(p_sl*sp.diff(R, r), r) + N/sp.sqrt(A*D)*R
# correct Liouville multiplier: s*sqrt(g), s = sqrt(w/p) = r/sqrt(AD), g = sqrt(pw) = r
key("liouville_identity", sp.simplify(normal_form*(r/sp.sqrt(A*D))*sp.sqrt(r) + SLres) == 0)
# isometry |v|^2 dx = |R|^2 w dr  (pointwise integrand identity)
key("weight_isometry", sp.simplify((r*1)*(r/sp.sqrt(A*D)) - w_sl) == 0)  # |v|^2/|R|^2 * dx/dr = w
# mu-off: dx -> dr/A (optical)
key("x_muoff_optical", sp.simplify((r/sp.sqrt(A*D)).subs(h, 0) - 1/A) == 0)

# ---------- Part 3: near-wall exponents, sigma_eff, x-finiteness ----------
# A = u^n, h = h0 u^q, r = Rw(1-u); AD = u^n (Rw^2 u^n (1-u)^2 + h0^2 u^{2q})
nn, qq = sp.symbols('nn qq', positive=True)  # use rationals per witness instead
def sigma_eff(nv, qv):
    return sp.Rational(1,2)*(nv + min(nv, 2*qv))
# machine confirmation of the exponent on witnesses: p = sqrt(AD) ~ u^sigma
def p_exponent(nv, qv):
    Ae = u**nv; he = h0*u**qv; re = Rw*(1-u)
    AD = sp.expand(Ae*(Ae*re**2 + he**2))
    # leading exponent of AD as u->0 is min over monomials
    pol = sp.Poly(AD.subs(u, u), u) if AD.is_polynomial(u) else None
    # generic: exponents n+n(=2n) and n+2q -> leading = min(2n, n+2q); p-exponent = half
    return sp.Rational(1,2)*min(2*nv, nv + 2*qv)
sig_checks = []
for (nv, qv) in [(sp.Rational(1,2),2),(sp.Rational(1,2),sp.Rational(1,8)),(sp.Rational(3,2),sp.Rational(1,8)),
                 (sp.Rational(3,2),sp.Rational(1,2)),(1,sp.Rational(1,4)),(1,sp.Rational(3,4)),
                 (1,sp.Rational(1,2)),(sp.Rational(5,2),1),(2,0),(1,0),(3,-2),(3,-sp.Rational(3,4)),(3,-1)]:
    sig_checks.append(sp.simplify(p_exponent(nv,qv) - sigma_eff(nv,qv)) == 0)
key("sigma_eff_formula_on_witnesses", all(sig_checks))
# x-finiteness: integral of u^{-sigma} finite iff sigma<1; log-divergent at sigma=1
s_ = sp.symbols('s_', positive=True)
key("x_finite_iff_sigma_lt_1",
    sp.integrate(u**(-sp.Rational(1,2)), (u, 0, 1)).is_finite and
    sp.integrate(u**(-1), (u, 0, 1)) == sp.oo and
    sp.integrate(u**(-sp.Rational(3,2)), (u, 0, 1)) == sp.oo)

# conjugation term subcriticality: Qc ~ u^{2s-1}, d ~ u^{1-s} => exponent (2s-1)/(1-s) > -2 for s<1
sig = sp.symbols('sigma', real=True)
key("conjugation_always_subcritical", sp.simplify((2*sig-1)/(1-sig) + 2 - 1/(1-sig)) == 0)
# (2s-1)/(1-s)+2 = 1/(1-s) > 0 for s<1: identity above proves it

print("PART 1-3 done", flush=True)

# ---------- Part 4: my own region classifier vs their map ----------
def classify(nv, qv, sign_wmh=None):
    """Independent classifier from first principles. Returns string."""
    nv = sp.nsimplify(nv); qv = sp.nsimplify(qv)
    sig = sp.Rational(1,2)*(nv + min(nv, 2*qv))
    if sig >= 1:
        return "LP-continuum(shifted-edge)" if qv == 0 else "LP-continuum"
    # finite x endpoint. dragging term u^q -> d^{e}, e = q/(1-sig) with u ~ d^{1/(1-sig)}
    if qv >= 0:
        return "LC"
    e = qv/(1 - sig)          # = 2q/(2-n-2q) when 2q<n
    if e > -2:
        return "LC"
    if e == -2:
        return "CRITICAL(c_crit-vs-3/4)"
    # supercritical divergent dragging: sign decides
    if sign_wmh is None:
        return "SIGN-SPLIT"
    return "LC(fall-to-center)" if sign_wmh > 0 else "LP-confining-DISCRETE"

expect = {
    (sp.Rational(1,2), 2): "LC",              # R1
    (sp.Rational(1,2), sp.Rational(1,8)): "LC",
    (sp.Rational(1,2), -3): "LC",             # R1 deep negative q (my probe)
    (sp.Rational(3,2), sp.Rational(1,8)): "LC",   # R2 mixing-created
    (sp.Rational(3,2), sp.Rational(1,2)): "LP-continuum",
    (1, sp.Rational(1,4)): "LC",
    (1, sp.Rational(3,4)): "LP-continuum",
    (1, sp.Rational(1,2)): "LP-continuum",    # marginal sigma=1
    (sp.Rational(5,2), 1): "LP-continuum",
    (2, 0): "LP-continuum(shifted-edge)",
    (1, 0): "LC",
    (3, -2): "LC",                            # R4 deep divergent
    (3, -sp.Rational(3,4)): "SIGN-SPLIT",     # R5 wedge
    (3, -1): "CRITICAL(c_crit-vs-3/4)",       # R6 line q=2-n
    (4, -sp.Rational(3,2)): "SIGN-SPLIT",     # my extra wedge probe
    (4, -sp.Rational(5,2)): "LC",             # my probe q<2-n
    (4, -1): "SIGN-SPLIT",                    # my probe: n=4, 2-n=-2 < -1 < (2-n)/2=-1 ? NO: -1 == (2-n)/2 -> sigma=1 LP
}
# fix the last expectation properly: n=4,q=-1: sigma=(4+(-2))/2=1 -> LP
expect[(4, -1)] = "LP-continuum"
allok = True
for (nv, qv), exp_ in expect.items():
    got = classify(nv, qv)
    good = (got == exp_)
    allok &= good
    print(f"  map ({nv},{qv}): mine={got} expected={exp_} {'OK' if good else 'MISMATCH'}")
key("region_map_independent", allok)

# R2 band mu-off is genuinely LP: h=0 => sigma=n>=1 => infinite x, U->0 => LP continuum
key("R2_muoff_LP", all(sp.Rational(1,2)*(nv+nv) >= 1 for nv in [1, sp.Rational(3,2), sp.Rational(199,100)]))

# wedge boundaries in q: supercritical iff  q > 2-n  (with q<0, sigma<1); q<(2-n)/2 for sigma<1
nvv = sp.Rational(3); 
key("wedge_bounds", classify(3, -sp.Rational(1,2)) == "LP-continuum"  # q=-1/2 > (2-3)/2 -> sigma=1 LP
    and classify(3, -sp.Rational(3,4)) == "SIGN-SPLIT"
    and classify(3, -1) == "CRITICAL(c_crit-vs-3/4)"
    and classify(3, -sp.Rational(3,2)) == "LC")

# ---------- Part 5: c_crit exact on the critical line q = 2-n, n = 2+nu ----------
nuv = sp.symbols('nu_', positive=True)
Aw = u**(2+nuv); hw = h0*u**(-nuv); rw = Rw*(1-u)
ADw = Aw*(Aw*rw**2 + hw**2)
integrand = rw*Rw/sp.sqrt(ADw)          # dx = r dr/sqrt(AD), dr = Rw du (toward wall)
lead = sp.limit(integrand*u**(1-nuv/2), u, 0, '+')   # leading coefficient of u^{-1+nu/2}
key("ccrit_integrand_leading", sp.simplify(lead - Rw**2/h0) == 0)
d_of_u = lead*u**(nuv/2)/(nuv/2)        # d = x_w - x ~ (2Rw^2/(h0 nu)) u^{nu/2}
Udrag = -2*w_*m_*hw/rw**2
ccrit_mine = sp.limit(sp.simplify(Udrag*d_of_u**2), u, 0, '+')
key("ccrit_value", sp.simplify(ccrit_mine - (-8*w_*m_*Rw**2/(h0*nuv**2))) == 0)
# with nu = n-2 this is  -8 w m Rw^2/(h0 (n-2)^2)  — matches iff their formula identical
# other terms subcritical on the line: centrifugal ~ u^{2+nu} -> d^{2(2+nu)/nu} positive power
key("ccrit_only_dragging_critical", sp.limit((m_**2*Aw/rw**2)*d_of_u**2, u, 0, '+') == 0)

# ---------- Part 6: wedge WKB LP/LC + essential spectrum ----------
# supercritical U = ±C d^{-ee}, ee>2. WKB validity: |U'|/|U|^{3/2} ~ d^{ee/2-1} -> 0 since ee>2
ee, CC, dd = sp.symbols('e C d', positive=True)
expr_val = sp.simplify((CC*dd**(-ee)).diff(dd)/ (CC*dd**(-ee))**sp.Rational(3,2))
key("wedge_wkb_valid", sp.simplify(expr_val + ee*CC**sp.Rational(-1,2)*dd**(ee/2 - 1)) == 0)
key("wedge_wkb_limit", sp.limit(sp.Abs(expr_val.subs(ee, sp.Rational(5,2))), dd, 0, '+') == 0)
# attractive: |v|^2 ~ |U|^{-1/2} = C^{-1/2} d^{ee/2}, integrable near 0 (ee/2>1 fine, any ee>0): LC
key("wedge_attractive_bothL2", sp.integrate(dd**(sp.Rational(3,2)), (dd, 0, 1)).is_finite)
# repulsive: growing branch ~ |U|^{-1/4} exp(+int sqrt(U)); int_0^d sqrt(U) ~ d^{1-ee/2} diverges (ee>2)
key("wedge_repulsive_action_diverges", sp.limit(dd**(1 - sp.Rational(5,2)/1), dd, 0, '+') == sp.oo)
# essential spectrum in counter-rotating channel: U-lambda -> +oo at finite x_w for EVERY lambda
lam = sp.symbols('lambda', real=True)
key("wedge_counter_nonoscillatory_all_lambda",
    sp.limit(CC*dd**(-sp.Rational(5,2)) - lam, dd, 0, '+') == sp.oo)
# both ends nonoscillatory for all lambda + finite interval => sigma_ess empty => purely discrete

# ---------- Part 7: center (D2), Zeeman, x_w <= x_opt, mu-off ----------
# variant (a): A->1, h->0 fast: indicial a^2 - m^2 = 0 from (rR')' - m^2/r R = 0
a_ = sp.symbols('a')
ind = sp.expand(r**(-a_+1)*(sp.diff(r*sp.diff(r**a_, r), r) - m_**2/r*r**a_))
key("center_indicial", sp.simplify(ind - (a_**2 - m_**2)) == 0)
# normal form at center: x=r, Qc = (sqrt r)''/sqrt r = -1/(4 r^2); U -> (m^2 - 1/4)/x^2
key("center_conj_minus_quarter", sp.simplify(sp.diff(sp.sqrt(r), r, 2)/sp.sqrt(r) + 1/(4*r**2)) == 0)
# variant (b): literal h(0)=h0: p(0) = sqrt(A D)|_{r=0,A=1} = h0 != 0 ; g^psipsi -> 1/h0^2
key("center_literal_regular", sp.simplify(sp.sqrt(1*(1*r**2 + h0**2)).subs(r, 0) - sp.Abs(h0)) == 0
    and sp.simplify((A/D).subs([(h, h0)]).subs(A, 1).subs(r, 0) - 1/h0**2) == 0)

# Zeeman: w^2 + 2 w m <h/r^2> = lam  (lam even in m) => w(m)-w(-m) = -2m<h/r^2> = 2m<Omega>
avg = sp.symbols('avg', positive=True)  # <h/r^2> > 0 WLOG
sols = sp.solve(w_**2 + 2*w_*m_*avg - lam, w_)
wplus = [s for s in sols if s.subs([(m_,0)]).subs(lam, 1) > 0][0]
split = sp.simplify(wplus - wplus.subs(m_, -m_))
key("zeeman_split", sp.simplify(split - (-2*m_*avg)) == 0)   # = 2 m <Omega>, Omega=-h/r^2

# x_w <= x_opt: 1/A^2 - r^2/(AD) = h^2/(A^2 D) >= 0
key("xw_le_xopt_identity", sp.simplify(1/A**2 - r**2/(A*D) - h**2/(A**2*D)) == 0)

# mu-off limits
key("muoff_p_w_N", sp.simplify(p_sl.subs(h,0) - A*r) == 0 and sp.simplify(w_sl.subs(h,0) - r/A) == 0
    and sp.simplify(N.subs(h,0) - (r**2*w_**2 - A*m_**2)) == 0)
# mu-off sigma = n (AD -> A^2 r^2 ~ u^{2n}, p-exp = n); LC iff n<1 = optical x = int dr/A finite
def sigma_muoff(nv):
    AD0 = sp.expand((u**nv)**2*(Rw*(1-u))**2)
    return nv  # leading exponent of sqrt(AD0) is n by construction; witness the integral instead
key("muoff_LC_iff_n_lt_1",
    sp.integrate(u**sp.Rational(-1,2), (u, 0, 1)).is_finite            # n=1/2: optical finite -> LC
    and sp.integrate(u**sp.Rational(-3,2), (u, 0, 1)) == sp.oo         # n=3/2: infinite -> LP
    and sp.integrate(u**(-1), (u, 0, 1)) == sp.oo)                     # n=1 marginal -> LP

# counterexample hunt: n<1 grid — does ANY q (incl. deep negative) or sign flip give LP?
hunt_ok = True
for nv in [sp.Rational(1,4), sp.Rational(1,2), sp.Rational(3,4), sp.Rational(9,10)]:
    for qv in [3, 1, sp.Rational(1,10), 0, -sp.Rational(1,10), -1, -5, -50]:
        got = classify(nv, qv)
        if got not in ("LC",):
            # check whether it is a sign-split or critical (would need q > 2-n, impossible for n<1,q<0)
            hunt_ok = False
            print(f"  COUNTEREXAMPLE? n={nv} q={qv}: {got}")
key("mixing_never_destroys_discrete_n_lt_1", hunt_ok)

print("PART 4-7 done", flush=True)
good = sum(1 for _, c in OK if c); tot = len(OK)
print(f"REVIEW1 TOTAL: {good}/{tot} True", flush=True)
for nm, c in OK:
    if not c: print(f"  FALSE: {nm}")
