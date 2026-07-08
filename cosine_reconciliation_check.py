"""cosine_reconciliation_check.py -- OBSERVE how the banked "round-cell cosine"
   e^{-phi/2} = A cos(k r)  relates to the NATIVE two-player VACUUM scalar equation.

DATA-BLIND: no 1101, 7.004, C, mu_g, r_*, phi_*, lepton/CMB/BAO numbers. Symbolic +
generic O(1) constants only. We are after the FORM and the STRUCTURAL relationship.

Objects:
 (A) native two-player VACUUM (matter off), Branch P.  cell_solver_f2d.py:17-19 /
     native_field_equations_...results.md line 154,176:
        phi'' = (4/Z) e^{-2phi} rho'^2/rho^2  -  2 phi' rho'/rho
        rho'' = 2 phi' rho'  -  (Z/4) rho e^{2phi} phi'^2
     equivalently  (rho^2 phi')' = (4/Z) e^{-2phi} rho'^2   (areal gauge rho=r: rho'=1).
 (B) banked cosine (cascade_lemD_universal.py:3-6, cascade_bv9_cas.py:97-113):
        v = e^{-phi/2},  v' = -kappa sqrt(1 - x_c v^2)  =>  v = A cos(k r),
        A = 1/sqrt(x_c),  k = kappa sqrt(x_c).
"""
import sympy as sp
import numpy as np
from scipy.integrate import solve_ivp

ok = lambda name, cond: print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
print("="*78)
print("PART 0 -- confirm the equivalence (rho^2 phi')' = (4/Z) e^{-2phi} rho'^2")
print("="*78)
r, Z = sp.symbols('r Z', positive=True)
phi = sp.Function('phi'); rho = sp.Function('rho')
phi_r, rho_r = phi(r), rho(r)
phipp_rhs = (4/Z)*sp.exp(-2*phi_r)*rho_r.diff(r)**2/rho_r**2 - 2*phi_r.diff(r)*rho_r.diff(r)/rho_r
# (rho^2 phi')' expanded, substituting phi'' -> phipp_rhs, should equal (4/Z)e^{-2phi} rho'^2
div_form = sp.diff(rho_r**2*phi_r.diff(r), r)               # 2 rho rho' phi' + rho^2 phi''
div_form = div_form.subs(sp.Derivative(phi_r, (r, 2)), phipp_rhs)
target = (4/Z)*sp.exp(-2*phi_r)*rho_r.diff(r)**2
ok("(rho^2 phi')' == (4/Z) e^{-2phi} rho'^2  (identity from the phi-EOM)",
   sp.simplify(div_form - target) == 0)

print()
print("="*78)
print("PART 1 (Q1a) -- does the cosine solve the FULL phi-eq in AREAL gauge rho=r ?")
print("     check (r^2 phi')' =?= (4/Z) e^{-2phi}   with phi=-2 ln(A cos(k r))")
print("="*78)
A, k = sp.symbols('A k', positive=True)
phi_cos = -2*sp.log(A*sp.cos(k*r))
lhs = sp.diff(r**2*sp.diff(phi_cos, r), r)
rhs = (4/Z)*sp.exp(-2*phi_cos)
lhs_s = sp.simplify(sp.expand_trig(lhs))
rhs_s = sp.simplify(rhs)
print("  LHS (r^2 phi')'      =", sp.simplify(lhs))
print("  RHS (4/Z) e^{-2phi}  =", rhs_s)
residual_areal = sp.simplify(lhs - rhs)
ok("cosine solves the areal-gauge phi-eq identically (residual==0)", residual_areal == 0)
print("  residual (LHS-RHS)   =", residual_areal)
# report the prior hand-calc forms explicitly
print("  [prior hand-calc]  LHS = 4 k r tan(kr) + 2 k^2 r^2 sec^2(kr):",
      sp.simplify(lhs - (4*k*r*sp.tan(k*r) + 2*k**2*r**2*sp.sec(k*r)**2)) == 0)
print("  [prior hand-calc]  RHS = (4/Z) A^4 cos^4(kr):",
      sp.simplify(rhs - (4/Z)*A**4*sp.cos(k*r)**4) == 0)

print()
print("="*78)
print("PART 2 (Q1b) -- is rho=r consistent with the VACUUM rho-eq for this phi ?")
print("     rho''=0 forces:  2 phi' = (Z/4) r e^{2phi} phi'^2   (or phi'=0)")
print("="*78)
# rho-eq: rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 ; sub rho=r, rho'=1, rho''=0
# do it concretely for the cosine phi:
phic = phi_cos
rho_eq_resid = 0 - (2*sp.diff(phic, r)*1 - (Z/4)*r*sp.exp(2*phic)*sp.diff(phic, r)**2)
print("  rho-eq residual at rho=r for the cosine phi (want 0):")
print("   ", sp.simplify(rho_eq_resid))
ok("rho=r is a CONSISTENT vacuum solution for the cosine phi (residual==0)",
   sp.simplify(rho_eq_resid) == 0)
# general statement: the vacuum forces 2 phi' = (Z/4) r e^{2phi} phi'^2 when rho=r
print("  => rho=r requires phi to satisfy 2 phi' = (Z/4) r e^{2phi} phi'^2, a DIFFERENT ODE;")
print("     a generic/cosine phi does NOT -> the areal check is moot, use the COUPLED system.")

print()
print("="*78)
print("PART 3 (Q2) -- v'=-kappa sqrt(1-x_c v^2) is a first integral of v'' = -k^2 v (FLAT)")
print("="*78)
kappa, xc = sp.symbols('kappa x_c', positive=True)
v = sp.Function('v')(r)
vprime_law = -kappa*sp.sqrt(1 - xc*v**2)
# differentiate the flux law, substitute v' back:
vpp = sp.diff(vprime_law, r).doit()
vpp = vpp.subs(sp.Derivative(v, r), vprime_law)
vpp = sp.simplify(vpp)
print("  v'' from differentiating the flux law =", vpp)
ok("v'' = -(kappa^2 x_c) v  (flat harmonic, k^2 = kappa^2 x_c)",
   sp.simplify(vpp + kappa**2*xc*v) == 0)
# and A cos(k r) solves v''=-k^2 v with A=1/sqrt(xc), k=kappa sqrt(xc):
vcos = (1/sp.sqrt(xc))*sp.cos(kappa*sp.sqrt(xc)*r)
ok("v=A cos(k r), A=1/sqrt(x_c), k=kappa sqrt(x_c) solves v''=-k^2 v",
   sp.simplify(sp.diff(vcos, r, 2) + kappa**2*xc*vcos) == 0)
print("  => the cosine solves a CONSTANT-COEFFICIENT harmonic eq: NO r^2 term, NO e^{-2phi}.")

print()
print("="*78)
print("PART 4 (Q3) -- what the FULL coupled two-player VACUUM system actually gives")
print("     numeric, BOUNDED, DATA-BLIND: finite core rho_c>0, phi'(r_c)=0, phi(r_c)=phi_c")
print("="*78)

def rhs_P(r_, y, Zv):
    ph, rh, php, rhp = y
    e2m = np.exp(-2*ph); e2p = np.exp(2*ph)
    phpp = 4*e2m*rhp**2/(Zv*rh**2) - 2*php*rhp/rh
    rhpp = 2*php*rhp - (Zv/4)*rh*e2p*php**2
    return [php, rhp, phpp, rhpp]

def ev_v0(r_, y, Zv):   # v = e^{-phi/2} -> 0  i.e. phi -> +inf  (edge). trigger when phi large.
    return 30.0 - y[0]
ev_v0.terminal = True; ev_v0.direction = -1
def ev_rho0(r_, y, Zv): return y[1]      # rho -> 0 collapse
ev_rho0.terminal = True; ev_rho0.direction = -1

rc = 0.5
# generic O(1) choices; rho'(r_c) must be NONZERO or the mirror core is a trivial fixed point (reported).
# span the sign options: expanding (rhop>0), contracting (rhop<0), nonzero phi'_c both signs.
cases = [
    dict(Z=8.0, phi_c=0.0,  rho_c=0.7071, rhop_c=1.0,  phip_c=0.0),
    dict(Z=8.0, phi_c=0.5,  rho_c=1.0,    rhop_c=1.0,  phip_c=0.0),
    dict(Z=1.0, phi_c=0.0,  rho_c=0.7071, rhop_c=1.0,  phip_c=0.0),
    dict(Z=8.0, phi_c=0.0,  rho_c=0.7071, rhop_c=0.3,  phip_c=0.0),
    dict(Z=8.0, phi_c=0.0,  rho_c=1.0,    rhop_c=-1.0, phip_c=0.0),   # CONTRACTING core
    dict(Z=8.0, phi_c=0.0,  rho_c=1.0,    rhop_c=1.0,  phip_c=0.5),   # phi'_c>0
    dict(Z=8.0, phi_c=0.0,  rho_c=1.0,    rhop_c=1.0,  phip_c=-0.5),  # phi'_c<0
]
# first: DEMONSTRATE the mirror-core (rhop_c=0, phip_c=0) is a trivial fixed point
y0triv = [0.0, 0.7071, 0.0, 0.0]
sol0 = solve_ivp(rhs_P, (rc, rc+5.0), y0triv, args=(8.0,), rtol=1e-9, atol=1e-12, max_step=0.01)
dphi = float(np.max(np.abs(sol0.y[0]-sol0.y[0,0]))); drho = float(np.max(np.abs(sol0.y[1]-sol0.y[1,0])))
print(f"  MIRROR CORE (phi'=rho'=0): max|dphi|={dphi:.2e} max|drho|={drho:.2e}  "
      f"-> {'TRIVIAL fixed point (flat, no structure)' if dphi<1e-8 and drho<1e-8 else 'nontrivial'}")
print()
print(f"  {'case':<34}{'edge?':<10}{'r_edge-r_c':<12}{'rho@edge':<10}{'v-shape'}")
for cs in cases:
    Zv = cs['Z']
    y0 = [cs['phi_c'], cs['rho_c'], cs['phip_c'], cs['rhop_c']]
    sol = solve_ivp(rhs_P, (rc, rc+50.0), y0, args=(Zv,),
                    events=[ev_v0, ev_rho0], rtol=1e-10, atol=1e-13, max_step=0.01,
                    dense_output=True)
    rr = sol.t; ph = sol.y[0]; rh = sol.y[1]
    vv = np.exp(-ph/2)
    hit_v = sol.t_events[0].size > 0
    hit_rho = sol.t_events[1].size > 0
    rho_min = float(np.min(rh))
    if hit_v:
        edge = 'v->0(phi^inf)'; r_edge = sol.t_events[0][0]-rc; rho_edge = sol.y_events[0][0][1]
    elif hit_rho or rho_min <= 1e-6 or not sol.success:
        edge = 'rho->0 collapse'; r_edge = rr[-1]-rc; rho_edge = rho_min
    else:
        edge = 'none(<50)'; r_edge = np.nan; rho_edge = rh[-1]
    # shape of v: fit A cos(k r) over the integrated span and report relative residual
    # (blind: generic fit, we only report qualitative closeness)
    if len(rr) > 5 and edge != 'rho->0 collapse':
        # cosine has v''/v = -k^2 < 0 CONSTANT; monotone-saturating profile has v''/v ~ 0.
        vp = np.gradient(vv, rr); vpp = np.gradient(vp, rr)
        ratio = vpp/vv
        rmid = slice(len(rr)//4, 3*len(rr)//4)
        shape = f"v''/v mean={np.mean(ratio[rmid]):+.4f} std={np.std(ratio[rmid]):.4f}  (cos=>neg const)"
    else:
        shape = "(collapse: v-shape n/a)"
    tag = f"Z={Zv},rhop={cs['rhop_c']:+},phip={cs['phip_c']:+}"
    rr_edge_s = f"{r_edge:.3f}" if not np.isnan(r_edge) else "  -  "
    print(f"  {tag:<34}{edge:<14}{'':2}{rr_edge_s:<12}{rho_edge:<10.4f}{shape}")

print()
print("  (v''/v ~ const & negative  => cosine-like harmonic; strongly r-varying => NOT a pure cosine)")
print()
print("  DETAIL for case 1 (Z=8, phi_c=0, rho_c=0.7071, rhop_c=1): sampled profile")
Zv = 8.0
y0 = [0.0, 0.7071, 0.0, 1.0]
sol = solve_ivp(rhs_P, (rc, rc+50.0), y0, args=(Zv,), events=[ev_v0, ev_rho0],
                rtol=1e-10, atol=1e-13, max_step=0.005, dense_output=True)
rr = sol.t
print(f"    {'r-r_c':>8}{'phi':>10}{'rho':>10}{'v=e^-ph/2':>12}{'rho/r':>10}")
for frac in np.linspace(0, 1, 9):
    i = min(int(frac*(len(rr)-1)), len(rr)-1)
    print(f"    {rr[i]-rc:>8.4f}{sol.y[0,i]:>10.4f}{sol.y[1,i]:>10.4f}"
          f"{np.exp(-sol.y[0,i]/2):>12.5f}{sol.y[1,i]/rr[i]:>10.4f}")
if sol.t_events[0].size:
    print(f"    EDGE: v->0 (phi->inf) at r-r_c = {sol.t_events[0][0]-rc:.4f}  (FINITE) ;"
          f" rho there = {sol.y_events[0][0][1]:.4f}")
elif sol.t_events[1].size:
    print(f"    EDGE: rho->0 at r-r_c = {sol.t_events[1][0]-rc:.4f}  (FINITE)")
else:
    print("    NO finite edge within r-r_c<50")
print()
print("  ---- literal AREAL Branch-P phi-eq  (r^2 phi')' = (4/Z) e^{-2phi}, rho=r imposed ----")
print("       (the eq as written in the doc; RHS>0 always => forcing VANISHES as phi->+inf)")
def rhs_areal(r_, y, Zv):
    ph, php = y
    # (r^2 phi')' = 2 r phi' + r^2 phi'' = (4/Z) e^{-2phi}  => phi'' = (4/Z)e^{-2phi}/r^2 - 2 phi'/r
    phpp = (4/Zv)*np.exp(-2*ph)/r_**2 - 2*php/r_
    return [php, phpp]
for phip0 in (0.0, 0.5, -0.5):
    s = solve_ivp(rhs_areal, (rc, rc+50.0), [0.0, phip0], args=(8.0,),
                  events=[lambda r_, y, Zv: 30.0-y[0]], rtol=1e-10, atol=1e-13, max_step=0.01)
    s.t_events  # noqa
    ph_end = s.y[0,-1]; v_end = np.exp(-ph_end/2)
    edge = "v->0 FINITE" if (30.0-s.y[0,-1] < 1e-3 and s.t[-1] < rc+49.9) else "no edge(<50)"
    print(f"    phi'_c={phip0:+.1f}:  phi(end)={ph_end:+.4f}  v(end)={v_end:.4f}  r_end-r_c={s.t[-1]-rc:.2f}  -> {edge}")
print()
print("DONE.")
