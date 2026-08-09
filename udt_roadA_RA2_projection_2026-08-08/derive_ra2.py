#!/usr/bin/env python3
"""RA2 — the ladder's angular projection. PHASE 1 (BLIND: symbols + region-coverage
rational witnesses; NO observational value anywhere in this phase; F-RETRO).
Contract: PREREGISTRATION.md (frozen, e0355637). Ground: RA1 DERIVATION_NOTES
(normal form, region map, Weyl spacing, Zeeman), D1/D4 dictionaries, O2 measures.
Phase-2 code is appended ONLY after the PHASE1-BANKED marker exists in
PHASE1_NOTES.md (ordering machine-evidenced by file mtimes + the marker).
Bounded: single foreground CPU process; sympy + small dense eigensolves; <8 min.
Scope stamps travel: SS9 lock-form ansatz; W1 metric-native scalar probe (tagged
choice); equatorial slice (spherical = named inheritance); fixed-(m,omega) pencil
analyticity (P-RA1-7). F-MUOFF: mixing terms stay in from the first line.
"""
import sys, time
import numpy as np
import sympy as sp
from scipy import linalg as sla
from scipy.integrate import quad

T0 = time.time()
KEYS = {}
def key(name, cond, note=""):
    KEYS[name] = bool(cond)
    print(f"KEY {name}: {KEYS[name]}" + (f"  [{note}]" if note else ""))

# ---------------------------------------------------------------- symbolic layer
def phase1_symbolic():
    print("== Phase-1 symbolic layer ==")
    r = sp.Symbol('r', positive=True)
    omega, mm = sp.symbols('omega m', real=True)
    Af = sp.Function('A', positive=True)(r); hf = sp.Function('h')(r)
    Df = Af*r**2 + hf**2
    p = sp.sqrt(Af*Df); w = r**2/sp.sqrt(Af*Df)
    Rf = sp.Function('R')(r)
    Nf = r**2*omega**2 + 2*hf*omega*mm - Af*mm**2
    SL = sp.diff(p*sp.diff(Rf, r), r) + Nf/sp.sqrt(Af*Df)*Rf   # RA1 D1 exact eq
    key("RA2_S1b_pw_r2", sp.simplify(p*w - r**2) == 0)
    # Liouville normal form recheck (RA1_K8): x'(r)=r/sqrt(AD), v=sqrt(r)R
    phi = r/sp.sqrt(Af*Df)
    Dx = lambda f: sp.diff(f, r)/phi
    v = sp.sqrt(r)*Rf
    Qc = Dx(Dx(sp.sqrt(r)))/sp.sqrt(r)
    NF = -Dx(Dx(v)) + (Qc + mm**2*Af/r**2 - 2*omega*mm*hf/r**2)*v - omega**2*v
    # DECIDABLE-FORM RESTATEMENT (disclosed, arc precedent): sympy cannot cancel
    # nested radicals of an abstract Function (no positivity assumption travels), so
    # the generic-(A,h,R) identity is checked on CONCRETE generic-position rational
    # functions (positive on (0,1)) at exact rational r, with (omega,m) symbolic.
    A_c = 1/(1 + r**2); h_c = r**2/(2 + r); R_c = (1 + r/3)/(1 + r)
    subsmap = {Af: A_c, hf: h_c, Rf: R_c}
    d1 = (NF + sp.sqrt(r)*SL/w).subs(subsmap).doit()
    d2 = (NF - sp.sqrt(r)*SL/w).subs(subsmap).doit()
    def vanishes(e):
        return all(sp.simplify(sp.radsimp(e.subs(r, rv))) == 0
                   for rv in [sp.Rational(1, 3), sp.Rational(1, 2), sp.Rational(3, 5)])
    key("RA2_S1_normalform", vanishes(d1) or vanishes(d2))
    # D1 dictionary: d_A = r(z), finite screen r -> R_w
    n, z, Rw = sp.symbols('n z R_w', positive=True)
    Az = (1 - r/Rw)**n
    r_of_z = Rw*(1 - (1 + z)**(-2/n))
    key("RA2_S2a_depth_dictionary", sp.simplify(Az.subs(r, r_of_z) - (1+z)**(-2)) == 0)
    key("RA2_S2b_finite_screen", sp.limit(r_of_z, z, sp.oo) == Rw)
    # proper rate d ell_p/dx = sqrt(D)/r  (the projection kernel), mu-off limit sqrt(A)
    dlp_dx = (1/sp.sqrt(Af))/phi
    key("RA2_S3_proper_rate", sp.simplify(dlp_dx - sp.sqrt(Df)/r) == 0)
    key("RA2_S8_muoff_kernel", sp.simplify((sp.sqrt(Df)/r).subs(hf, 0) - sp.sqrt(Af)) == 0)
    # theta_k = lambda_p/r_bar at a common shell: ratios shed every shell factor
    ok, oj = sp.symbols('omega_k omega_j', positive=True)
    rb = sp.Symbol('rbar', positive=True)
    Ab = sp.Function('Abar', positive=True)(rb); hb = sp.Function('hbar')(rb)
    theta = lambda om: (2*sp.pi/om)*sp.sqrt(Ab + hb**2/rb**2)/rb
    key("RA2_S4_ratio_shellfree", sp.simplify(theta(ok)/theta(oj) - oj/ok) == 0)
    return dict(NF=NF, SL=SL, r_of_z=r_of_z, theta_ratio=theta(ok)/theta(oj))

def phase1_symbolic_b(carry):
    print("== Phase-1 symbolic layer (b): ladder law, band form, wedge exponents ==")
    # harmonic-ladder ratio law: ell_k ~ k + beta  (scale cancels)
    k_, b_ = sp.symbols('k beta', real=True)
    rho = (k_ + 1 + b_)/(k_ + b_)
    key("RA2_S5a_ratio_monotone", sp.simplify(sp.diff(rho, b_) + 1/(k_ + b_)**2) == 0)
    key("RA2_S5b_ratio_to_1", sp.limit(rho, k_, sp.oo) == 1)
    rho1 = sp.Symbol('rho_1', positive=True)
    bsol = sp.solve(sp.Eq((2 + b_)/(1 + b_), rho1), b_)
    key("RA2_S5c_offset_rigidity", len(bsol) == 1 and
        sp.simplify(bsol[0] - (2 - rho1)/(rho1 - 1)) == 0,
        "first ratio fixes beta; then EVERY higher ratio is determined")
    # band form in m (P-a): omega^2 + 2 eps c m omega - a - eps b m^2 = 0, expand
    a_, bb_, c_ = sp.symbols('a b c', positive=True)
    m_ = sp.Symbol('m', real=True); eps = sp.Symbol('epsilon', positive=True)
    W = sp.Symbol('W')
    roots = sp.solve(sp.Eq(W**2 + 2*eps*c_*m_*W - a_ - eps*bb_*m_**2, 0), W)
    wpos = [s for s in roots if sp.limit(s, eps, 0) == sp.sqrt(a_)][0]
    ser = sp.series(wpos, eps, 0, 2).removeO()
    pred = sp.sqrt(a_) + eps*(bb_*m_**2/(2*sp.sqrt(a_)) - c_*m_)
    key("RA2_S6a_band_form", sp.simplify(ser - pred) == 0,
        "omega_k(m) = omega_k0 + m<Omega> + m^2<A/r^2>/(2 omega_k0); <Omega>=-c")
    split = sp.simplify(ser.subs(m_, 1) - ser.subs(m_, -1))
    key("RA2_S6b_zeeman_doubling", sp.simplify(split + 2*eps*c_) == 0,
        "omega_k(m)-omega_k(-m) = 2m<Omega>_k (RA1_K22 form)")
    mstar = sp.solve(sp.diff(pred, m_), m_)
    key("RA2_S6c_band_extremum", len(mstar) == 1 and
        sp.simplify(mstar[0] - c_*sp.sqrt(a_)/bb_) == 0,
        "dos accumulation at m* = omega_k0 <h/r^2>/<A/r^2>; m*=0 iff h=0")
    # wedge witness exponents (RA1 §3 recheck at the Phase-1 witness point)
    nw, qw = sp.Rational(3), sp.Rational(-3, 4)
    sig = (nw + sp.Min(nw, 2*qw))/2
    key("RA2_S7a_wedge_sigma", sig == sp.Rational(3, 4) and sig < 1)
    e_drag = 2*qw/(2 - nw - 2*qw)
    key("RA2_S7b_wedge_supercritical", e_drag < -2, "dragging exponent -3 < -2")
    key("RA2_S7c_wedge_membership", (2 - nw) < qw < (2 - nw)/2)
    # float-atom audit of the symbolic layer (F-RETRO analog of RA1_K28)
    floats = set()
    for e in [carry['NF'], carry['SL'], carry['r_of_z'], carry['theta_ratio'],
              rho, ser, pred]:
        floats |= {aa for aa in sp.preorder_traversal(e) if isinstance(aa, sp.Float)}
    key("RA2_S9_symbolic_floatfree", len(floats) == 0)

# ---------------------------------------------------------------- numeric layer
# Witness values: small rationals chosen for REGION COVERAGE of RA1's completed map
# (the O2/RA1 witness pattern), NOT fitted; R_w = 1 (scale-free ratios), c0 = 1.
# Center completion (ledgered, P-RA2-6): h = h0 (r/R_w)^2 (1-r/R_w)^q — the D2-SS3
# regular completion of RA1's P-RA1-8(a); prefactor -> 1 at the wall so the frozen
# near-wall class is EXACT at leading order; D3 classification untouched (endpoint-local).
WITNESSES = {
    'R1':  dict(n=0.5, q=1.0,   h0=0.5),   # n<1 slab (survives mu-off)
    'R2':  dict(n=1.5, q=0.0,   h0=0.5),   # mixing-created band, q=0 bounded edge
    'R2b': dict(n=2.0, q=-0.5,  h0=0.5),   # mixing-created line n=2, q<0
    'R4':  dict(n=3.0, q=-1.5,  h0=0.5),   # deep divergent mixing
    'R5w': dict(n=3.0, q=-0.75, h0=0.5),   # chiral wedge (counter-rot channel, m=-1)
}

def coeffs(n, q, h0):
    A = lambda rr: (1.0 - rr)**n
    h = lambda rr: h0*rr**2*(1.0 - rr)**q
    return A, h

def grid(rmin=1e-4, umin=1e-5, N=700):
    left = np.geomspace(rmin, 0.5, N//2)
    right = 1.0 - np.geomspace(umin, 0.5, N - N//2)
    return np.unique(np.concatenate([left, right]))

def assemble(n, q, h0, m, rr, wallBC='D'):
    A, h = coeffs(n, q, h0)
    Av = A(rr); hv = h(rr); Dv = Av*rr**2 + hv**2; sq = np.sqrt(Av*Dv)
    rmid = 0.5*(rr[:-1] + rr[1:])
    Am = A(rmid); hm = h(rmid); pm = np.sqrt(Am*(Am*rmid**2 + hm**2))
    d = np.diff(rr); Nn = len(rr)
    ci = np.empty(Nn); ci[0] = d[0]/2; ci[-1] = d[-1]/2; ci[1:-1] = 0.5*(d[:-1] + d[1:])
    T = np.zeros((Nn, Nn))
    for i in range(Nn - 1):
        kk = pm[i]/d[i]
        T[i, i] += kk; T[i+1, i+1] += kk; T[i, i+1] -= kk; T[i+1, i] -= kk
    K = T + np.diag(Av*m*m/sq*ci)
    M = np.diag(rr**2/sq*ci)
    C = np.diag(2.0*hv*m/sq*ci)
    keep = np.ones(Nn, bool)
    if m != 0: keep[0] = False        # center: regular branch r^{|m|} (Dirichlet)
    if wallBC == 'D': keep[-1] = False  # wall: Dirichlet representative of the FREE datum
    idx = np.where(keep)[0]
    sub = lambda X: X[np.ix_(idx, idx)]
    aux = dict(rr=rr, hv=hv, sq=sq, ci=ci, wv=rr**2/sq)
    return sub(K), sub(M), sub(C), idx, aux

def solve_sym(n, q, h0, m_in_K, rr, wallBC='D', nev=30):
    """Symmetric solve of K(m^2) R = omega^2 M R (dragging C OFF; used for m=0
    spectra and as the unperturbed operator for the Zeeman first-order check)."""
    K, M, C, idx, aux = assemble(n, q, h0, m_in_K, rr, wallBC)
    s = 1.0/np.sqrt(np.diag(M))
    Ks = (K*s).T*s
    ev, Vs = np.linalg.eigh(0.5*(Ks + Ks.T))
    pos = ev > 1e-12
    om = np.sqrt(ev[pos][:nev])
    V = (Vs[:, pos][:, :nev].T*s).T   # back to R-vectors
    return om, V, idx, aux

def qep(n, q, h0, m, rr, wallBC='D'):
    """Quadratic pencil omega^2 M + omega C - K = 0 via companion linearization.
    M, C diagonal -> invert M and use the standard eigensolver (fast, no QZ)."""
    K, M, C, idx, aux = assemble(n, q, h0, m, rr, wallBC)
    Nn = K.shape[0]; Z = np.zeros((Nn, Nn)); I = np.eye(Nn)
    Minv = 1.0/np.diag(M)
    Aa = np.block([[-np.diag(Minv*np.diag(C)), Minv[:, None]*K], [I, Z]])
    ev = np.linalg.eigvals(Aa)
    ev = ev[np.isfinite(ev)]
    real = ev[np.abs(ev.imag) <= 1e-7*np.maximum(1.0, np.abs(ev.real))].real
    return np.sort(real), aux

def xw_num(n, q, h0, rmin, umin):
    A, h = coeffs(n, q, h0)
    f = lambda rr: rr/np.sqrt(A(rr)*(A(rr)*rr**2 + h(rr)**2))
    val, _ = quad(f, rmin, 1.0 - umin, limit=400)
    return val

def mode_avg(f_nodes, Rvec, idx, aux):
    wgt = (aux['wv']*aux['ci'])[idx]
    return float(np.sum(f_nodes[idx]*Rvec**2*wgt)/np.sum(Rvec**2*wgt))

def report_ladder(tag, om, xw):
    om5 = om[:5]
    beta = om[:8]*xw/np.pi - np.arange(1, min(9, len(om) + 1))
    print(f"  {tag}: omega_1..5 = " + " ".join(f"{o:.5f}" for o in om5))
    print(f"    ratios omega_k/omega_1 (=ell_k/ell_1) = " +
          " ".join(f"{o/om5[0]:.4f}" for o in om5))
    print(f"    spacings = " + " ".join(f"{d:.5f}" for d in np.diff(om[:6])) +
          f"   pi/x_w = {np.pi/xw:.5f}")
    print(f"    beta_k = omega_k x_w/pi - k = " + " ".join(f"{b:+.4f}" for b in beta))
    return beta

def phase1_numeric():
    print("== Phase-1 numeric layer (region witnesses; rationals for coverage) ==")
    rmin, umin, N = 1e-4, 1e-5, 700
    rr = grid(rmin, umin, N)
    # N1 convergence (R1, m=0): two grids
    omA, _, _, _ = solve_sym(**WITNESSES['R1'], m_in_K=0, rr=grid(rmin, umin, 600))
    omB, _, _, _ = solve_sym(**WITNESSES['R1'], m_in_K=0, rr=grid(rmin, umin, 900))
    drift = np.max(np.abs(omA[:5]/omB[:5] - 1))
    key("RA2_N1_convergence", drift < 1e-2, f"5-level grid drift {drift:.2e}")
    # N2 Weyl spacing + ladder tables per witness (m=0 symmetric channel).
    # High-k modes need the finer grid (discretization-limited above k~10 at N=700).
    rrW = grid(rmin, umin, 1400)
    weyl_ok, betas = True, {}
    for tag, wpar in WITNESSES.items():
        if tag == 'R5w':
            continue
        om, V, idx, aux = solve_sym(**wpar, m_in_K=0, rr=rrW)
        xw = xw_num(wpar['n'], wpar['q'], wpar['h0'], rmin, umin)
        betas[tag] = report_ladder(f"{tag} (m=0, wall=D)", om, xw)
        dev = abs(np.mean(np.diff(om[9:20]))/(np.pi/xw) - 1)
        print(f"    Weyl dev (k=10..20): {dev:.2e}")
        weyl_ok &= dev < 0.02
    key("RA2_N2_weyl_spacing", weyl_ok, "mean spacing k=10..20 within 2% of pi/x_w")
    # N3 Zeeman doubling first-order check (R1, small h0, |m|=1)
    rrq = grid(rmin, umin, 520)   # common QEP grid (bounded runtime)
    n1, q1, h01 = 0.5, 1.0, 0.1
    om0, V0, idx0, aux0 = solve_sym(n1, q1, h01, m_in_K=1, rr=rrq)
    Omega_nodes = -(aux0['hv']/aux0['rr']**2)
    omP, _ = qep(n1, q1, h01, +1, rrq); omM, _ = qep(n1, q1, h01, -1, rrq)
    omP = omP[omP > 1e-8]; omM = omM[omM > 1e-8]
    ok3, msg = True, []
    for k in range(3):
        Ok = mode_avg(Omega_nodes, V0[:, k], idx0, aux0)
        split = omP[k] - omM[k]
        ok3 &= abs(split - 2*Ok) <= 0.1*abs(2*Ok)
        msg.append(f"k={k+1}: {split:+.5f} vs 2<Omega>={2*Ok:+.5f}")
    key("RA2_N3_zeeman_first_order", ok3, "; ".join(msg))
    # N4 the wall datum moves the offset (R2: Dirichlet vs Neumann truncation)
    omD, _, _, _ = solve_sym(**WITNESSES['R2'], m_in_K=0, rr=rr, wallBC='D')
    omN, _, _, _ = solve_sym(**WITNESSES['R2'], m_in_K=0, rr=rr, wallBC='N')
    xw2 = xw_num(1.5, 0.0, 0.5, rmin, umin)
    bD = report_ladder("R2 (m=0, wall=D)", omD, xw2)
    bN = report_ladder("R2 (m=0, wall=N)", omN, xw2)
    # Neumann-wall spectrum has a zero mode (dropped by the >0 filter), so its
    # nonzero ladder sits ~+1/2 in beta relative to Dirichlet: the free wall datum
    # MOVES the offset (Robin family interpolates); interlacing check included.
    interlace = np.all(omN[:5] > omD[:5]) and np.all(omN[:5] < omD[1:6])
    key("RA2_N4_wall_datum_offset", abs((bN[4] - bD[4]) - 0.5) < 0.15 and interlace,
        f"beta_5 shift = {bN[4]-bD[4]:+.3f} (~ +1/2); zero-mode interlacing holds")
    # N5 wedge counter-rotating channel: intrinsic (truncation-insensitive) ladder
    wpar = WITNESSES['R5w']; ladders = {}
    for um in (1e-4, 1e-6):
        rrw = grid(rmin, um, 520)
        ev, _ = qep(wpar['n'], wpar['q'], wpar['h0'], -1, rrw)
        ladders[um] = (ev[ev > 1e-8][:5], -ev[ev < -1e-8][::-1][:5])
    dc = np.max(np.abs(ladders[1e-4][0][:3]/ladders[1e-6][0][:3] - 1))
    dco = np.max(np.abs(ladders[1e-4][1][:3]/ladders[1e-6][1][:3] - 1))
    key("RA2_N5_wedge_intrinsic", dc < 0.02,
        f"counter-rot drift {dc:.2e} vs co-rot drift {dco:.2e} under 100x cutoff change")
    xww = xw_num(wpar['n'], wpar['q'], wpar['h0'], rmin, 1e-6)
    betas['R5w'] = report_ladder("R5w counter-rot (m=-1, intrinsic)", ladders[1e-6][0], xww)
    print(f"  R5w co-rotating (extension-dependent, caution): " +
          " ".join(f"{o:.5f}" for o in ladders[1e-6][1][:5]))
    # N6 doubling in an LC region (R2, h0=0.5, |m|=1): paired lines, sign of split
    omP2, _ = qep(1.5, 0.0, 0.5, +1, rrq); omM2, _ = qep(1.5, 0.0, 0.5, -1, rrq)
    omP2 = omP2[omP2 > 1e-8]; omM2 = omM2[omM2 > 1e-8]
    splits = omP2[:3] - omM2[:3]
    key("RA2_N6_doublet_sign", np.all(splits < 0),
        "omega_k(+1) < omega_k(-1): sign = sign(m<Omega>), <Omega> < 0 for h0>0; "
        + " ".join(f"{s:+.5f}" for s in splits))
    print("  fractional doublet splittings (R2,h0=1/2,|m|=1): " +
          " ".join(f"{abs(s)/o:.4f}" for s, o in zip(splits, omM2[:3])))
    return betas

def run_phase1():
    carry = phase1_symbolic()
    phase1_symbolic_b(carry)
    phase1_numeric()
    npass = sum(KEYS.values()); ntot = len(KEYS)
    print(f"\nPHASE-1 KEYS: {npass}/{ntot} True   (runtime {time.time()-T0:.1f}s)")
    assert npass == ntot, [k for k, v in KEYS.items() if not v]

# ============================ PHASE 2 (appended AFTER the PHASE1-BANKED marker;
# the ONLY place observational values appear; see PHASE2_COMPARISON.md) ==========
def run_phase2():
    print("=" * 70); print("RA2 PHASE 2 — the frozen comparison (MAP-S4 discipline)")
    print("=" * 70)
    # ATTRIBUTED MEASUREMENTS: Planck 2018 results I (arXiv:1807.06205), TT spectrum
    # peak positions (peaks-and-troughs table); entered here for the first time.
    ELL = np.array([220.6, 538.1, 809.8, 1147.8, 1446.8, 1779.0, 2075.0])
    SIG = np.array([0.6, 1.3, 1.0, 2.3, 1.6, 3.0, 8.0])
    kk = np.arange(1, 8)
    print("measured TT peaks (Planck 2018 I):", ELL)
    print("measured ratios ell_k/ell_1:", np.round(ELL/ELL[0], 4))
    print("measured successive ratios:", np.round(ELL[1:]/ELL[:-1], 4))
    print("pre-stated MAP-S4 fact honored: second-to-first = "
          f"{ELL[1]/ELL[0]:.4f} (non-integer)")
    # 2-parameter comb fit ell_k = a (k + beta)  [the Phase-1 asymptotic law]
    a_fit = np.sum((kk - kk.mean())*(ELL - ELL.mean()))/np.sum((kk - kk.mean())**2)
    c_fit = ELL.mean() - a_fit*kk.mean()
    beta_fit = c_fit/a_fit
    pred = a_fit*(kk + beta_fit)
    res = ELL - pred
    frac = res/ELL
    beta_meas = ELL/a_fit - kk
    print(f"comb fit: a = {a_fit:.2f}, beta = {beta_fit:+.4f}")
    print("residuals (ell units):", np.round(res, 1))
    print("fractional residuals:", np.round(frac, 4))
    print("per-peak offsets beta_k^meas:", np.round(beta_meas, 4))
    odd = beta_meas[0::2]; even = beta_meas[1::2]
    print(f"alternation: mean odd-peak beta {odd.mean():+.4f} vs even {even.mean():+.4f}")
    K2 = {}
    def k2(name, cond, note=""):
        K2[name] = bool(cond)
        print(f"KEY {name}: {K2[name]}" + (f"  [{note}]" if note else ""))
    k2("RA2_P2_K1_comb_fit", abs(a_fit - 310.1) < 0.5 and abs(beta_fit + 0.306) < 0.01,
       "scale ~310.1, offset ~ -0.306")
    # Phase-1-banked plain-LC Dirichlet offset band (from PHASE1_NOTES, m=0 witnesses):
    BAND = (-0.42, -0.26)
    k2("RA2_P2_K2_offset_in_band", BAND[0] < beta_fit < BAND[1] and
       np.all((beta_meas > BAND[0]) & (beta_meas < BAND[1])),
       "measured global AND per-peak offsets inside the pre-banked Dirichlet band")
    k2("RA2_P2_K3_comb_level", 0.005 < np.max(np.abs(frac)) < 0.04,
       f"comb matches at the 1-3% level (max |frac res| {np.max(np.abs(frac)):.3f})")
    k2("RA2_P2_K4_precision_mismatch", np.max(np.abs(res)/SIG) > 5,
       f"comb residuals >> measurement errors (max {np.max(np.abs(res)/SIG):.0f} sigma)")
    # region-witness first ratios (Phase-1 banked) vs measured
    RHO1 = dict(R1=2.5082, R2=2.7886, R2b=2.5691, R4=2.4235, R5w=1.3304)
    rho1m = ELL[1]/ELL[0]
    for tag, rho in RHO1.items():
        print(f"  {tag}: rho1 = {rho:.4f} vs measured {rho1m:.4f} "
              f"({100*(rho/rho1m - 1):+.2f}%)")
    k2("RA2_P2_K5_deep_mixing_closest", min(RHO1, key=lambda t: abs(RHO1[t] - rho1m)) == 'R4',
       "R4 witness within 0.7% of the measured first ratio")
    k2("RA2_P2_K6_wedge_mismatch", abs(RHO1['R5w']/rho1m - 1) > 0.3,
       "the intrinsic wedge channel's low-k comb is far too dense at its witness")
    k2("RA2_P2_K7_alternation_unmodeled", even.mean() - odd.mean() > 0.02,
       "even/odd offset alternation present in data; witness anharmonicity is monotone")
    npass = sum(K2.values())
    print(f"\nPHASE-2 KEYS: {npass}/{len(K2)} True   (runtime {time.time()-T0:.1f}s)")
    assert npass == len(K2), [k for k, v in K2.items() if not v]

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'phase1'
    if mode == 'phase1':
        run_phase1()
    elif mode == 'phase2':
        run_phase2()  # appended ONLY after the PHASE1-BANKED marker (F-RETRO)
