"""r1_bv_main.py -- BLIND ADVERSARIAL VERIFIER for r1_route_fork_native_derivation.md.

Independent re-derivation: my own reductions from the SOURCE-doc action
  S = INT c sqrt(h) [ (Z/2) phi'^2 + R^{(2)}[h] + W_chi * Kc + mu e^phi K phi' + L_m ]
  Kc = K_AB K^AB - K^2,  K_AB = (1/2) e^{-phi} d_r h_AB,  W_chi = e^{2phi}(G) / 1(P)
(native_field_equations_constrained_two_player_results.md sec.5,
 native_geometric_action_results.md), my own Christoffel/Ricci code, my own EL
operator (2nd order).  NOT copied from r1_route_fork_cas.py.

Verifier: do NOT commit.
"""
import sympy as sp

r, t, th, ps, lam, c = sp.symbols('r t theta psi lambda c', real=True)
aa = sp.Symbol('a_refl', real=True)
Z, mu = sp.symbols('Z mu', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)
pp = phi.diff(r); rp = rho.diff(r)

results = []
def chk(name, cond):
    ok = bool(cond)
    results.append((name, ok))
    print(('PASS ' if ok else '*** FAIL ') + name)

# ---------------------------------------------------------------- my own geometry toolkit
def christ(g, xs):
    n = len(xs); gi = g.inv()
    return [[[sp.simplify(sum(gi[a, d]*(g[d, b].diff(xs[cc]) + g[d, cc].diff(xs[b])
              - g[b, cc].diff(xs[d])) for d in range(n))/2) for cc in range(n)]
             for b in range(n)] for a in range(n)]

def ricci_scal(g, xs):
    n = len(xs); Gam = christ(g, xs); gi = g.inv()
    R = 0
    for b in range(n):
        for cc in range(n):
            e = 0
            for a in range(n):
                e += Gam[a][b][cc].diff(xs[a]) - Gam[a][cc][b].diff(xs[cc]) if False else 0
            # standard: Ric_bc = d_a Gam^a_bc - d_c Gam^a_ba + Gam^a_ad Gam^d_bc - Gam^a_cd Gam^d_ba
            e = 0
            for a in range(n):
                e += sp.diff(Gam[a][b][cc], xs[a]) - sp.diff(Gam[a][b][a], xs[cc])
                for d in range(n):
                    e += Gam[a][a][d]*Gam[d][b][cc] - Gam[a][cc][d]*Gam[d][b][a]
            R += gi[b, cc]*e
    return sp.simplify(R)

def EL(L, q):
    """2nd-order Euler-Lagrange for density L(q,q',q''; r)."""
    out = sp.diff(L, q) - sp.diff(sp.diff(L, q.diff(r)), r)
    if L.has(q.diff(r, 2)):
        out += sp.diff(sp.diff(L, q.diff(r, 2)), r, 2)
    return sp.simplify(out)

def onflat(e):
    """Evaluate at the banked flat reference phi=0, rho=r (derivatives first)."""
    e = e.subs({phi.diff(r, 3): 0, phi.diff(r, 2): 0, pp: 0,
                rho.diff(r, 3): 0, rho.diff(r, 2): 0, rp: 1})
    return sp.simplify(e.subs({phi: 0, rho: r}))

# ---------------------------------------------------------------- 0. MY OWN round reduction
h = sp.Matrix([[rho**2, 0], [0, rho**2*sp.sin(th)**2]])
hi = h.inv()
K_AB = sp.Rational(1, 2)*sp.exp(-phi)*h.diff(r)
Ktr = sp.simplify((hi*K_AB).trace())
KK = sp.simplify((hi*K_AB*hi*K_AB).trace())
Kc = sp.simplify(KK - Ktr**2)
# R^{(2)} of the transverse 2-metric, computed (not quoted):
R2 = ricci_scal(h, [th, ps])
chk('R0a: R^{(2)}[rho^2 Omega] = 2/rho^2 (own Ricci code)',
    sp.simplify(R2 - 2/rho**2) == 0)
chk('R0b: K = 2e^{-phi}rho\'/rho, Kc = -2e^{-2phi}rho\'^2/rho^2 (own reduction)',
    sp.simplify(Ktr - 2*sp.exp(-phi)*rp/rho) == 0
    and sp.simplify(Kc + 2*sp.exp(-2*phi)*rp**2/rho**2) == 0)

# per-steradian densities (sqrt h = rho^2, sin th dropped consistently):
sq = rho**2
LG_A = sp.expand(sq*((Z/2)*pp**2 + R2 + sp.exp(2*phi)*Kc))        # Branch G, Route A
LP_A = sp.expand(sq*((Z/2)*pp**2 + R2 + Kc))                       # Branch P, Route A
Lmix = sp.expand(sq*(mu*sp.exp(phi)*Ktr*pp))                       # the mixing term
chk('R0c: reductions reproduce the banked forms: L_G^A=(Z/2)rho^2phi\'^2+2-2rho\'^2;'
    ' L_P^A=...-2e^{-2phi}rho\'^2; mixing=2mu rho rho\'phi\'',
    sp.simplify(LG_A - ((Z/2)*rho**2*pp**2 + 2 - 2*rp**2)) == 0
    and sp.simplify(LP_A - ((Z/2)*rho**2*pp**2 + 2 - 2*sp.exp(-2*phi)*rp**2)) == 0
    and sp.simplify(Lmix - 2*mu*rho*rp*pp) == 0)

LG = LG_A + Lmix          # general (Z, mu) Branch G
LP = LP_A + Lmix          # general (Z, mu) Branch P
LG_B = LG.subs({Z: 8, mu: 2}); LP_B = LP.subs({Z: 8, mu: 2})

# ---------------------------------------------------------------- A. shift weights, GENERAL h
h11, h12, h22 = [sp.Function(f)(r) for f in ('h11', 'h12', 'h22')]
hg = sp.Matrix([[h11, h12], [h12, h22]])
hgi = hg.inv()
Kg = sp.Rational(1, 2)*sp.exp(-phi)*hg.diff(r)
Kgtr = sp.simplify((hgi*Kg).trace())
KgKg = sp.simplify((hgi*Kg*hgi*Kg).trace())
Kcg = KgKg - Kgtr**2
def wt(e):
    return sp.simplify(sp.expand(e.subs(phi, phi + lam)/e))
chk('A1(gen-h): sqrt(-g) = c sqrt(det h) is phi-free (4D det = -c^2 det h exactly)',
    sp.simplify((-sp.exp(-2*phi)*c**2)*sp.exp(2*phi)*hg.det() + c**2*hg.det()) == 0)
chk('A2(gen-h): weights -- phi\'^2: e^0; Kc: e^{-2lam}; e^{2phi}Kc: e^0;'
    ' MIXING e^phi K phi\': EXACTLY e^0 (both branches, general transverse h)',
    wt(pp**2) == 1 and sp.simplify(wt(Kcg) - sp.exp(-2*lam)) == 0
    and wt(sp.exp(2*phi)*Kcg) == 1 and wt(sp.exp(phi)*Kgtr*pp) == 1)

# ---------------------------------------------------------------- B. the two criteria
chk('B1a: VALUE criterion: R2 + e^{2phi}Kc = 0 on rho=r for ANY phi (banked G cancellation)',
    sp.simplify((R2 + sp.exp(2*phi)*Kc).subs({rp: 1, rho: r})) == 0)
chk('B1b: VALUE excludes standalone K-quadratics on flat: e^{2phi}K^2 -> 4/r^2,'
    ' e^{2phi}K_ABK^AB -> 2/r^2 (nonzero)',
    sp.simplify(onflat(sp.exp(2*phi)*Ktr**2) - 4/r**2) == 0
    and sp.simplify(onflat(sp.exp(2*phi)*KK) - 2/r**2) == 0)
chk('B1c: VALUE has no grip on the phi-sector: phi\'^2 and e^phi K phi\' both -> 0 on flat',
    onflat(pp**2) == 0 and onflat(sp.exp(phi)*Ktr*pp) == 0)

# B2 -- THE LOAD-BEARING DISAMBIGUATION. My own EL, my own flat sub.
chk('B2a: flat-STATIONARITY kills banked Route-A Branch P: phi-EL(L_P^A) on flat = +4'
    ' (and the banked eq form Z(r^2phi\')\'=4e^{-2phi} is reproduced)',
    sp.simplify(onflat(EL(LP_A, phi)) - 4) == 0
    and sp.simplify(EL(LP_A, phi) - (4*sp.exp(-2*phi)*rp**2 - Z*sp.diff(rho**2*pp, r))) == 0)
chk('B2b: flat-STATIONARITY kills Route-B G: phi-EL(L_G^B) on flat = -4;'
    ' general mu: residual = -2mu (any mu != 0 dies)',
    sp.simplify(onflat(EL(LG_B, phi)) + 4) == 0
    and sp.simplify(onflat(EL(LG, phi)) + 2*mu) == 0)
chk('B2c (verifier extension, SCOPE test): TRANSVERSE-scoped stationarity spares BOTH:'
    ' rho-EL on flat = 0 for L_P^A, L_G^B, L_P^B, L_G^A -- the only reading that catches'
    ' the mixing term is phi-EOM stationarity, which kills banked P',
    onflat(EL(LP_A, rho)) == 0 and onflat(EL(LG_B, rho)) == 0
    and onflat(EL(LP_B, rho)) == 0 and onflat(EL(LG_A, rho)) == 0)
chk('B2d (control): flat SOLVES Route-A G fully (phi-EL and rho-EL = 0 on flat)',
    onflat(EL(LG_A, phi)) == 0 and onflat(EL(LG_A, rho)) == 0)

# ---------------------------------------------------------------- C. Z=8 provenance
gL = sp.Matrix([[-sp.exp(-2*phi)*c**2, 0], [0, sp.exp(2*phi)]])
R_L = ricci_scal(gL, [t, r])
chk('C1: R_L = 2e^{-2phi}(phi\'\' - 2phi\'^2) (own Christoffel/Ricci, from scratch)',
    sp.simplify(R_L - 2*sp.exp(-2*phi)*(phi.diff(r, 2) - 2*pp**2)) == 0)
sqh = rho**2*sp.sin(th)
chk('C2: IBP package exact: sqrt(h)(-e^{2phi}R_L) = sqrt(h)[4phi\'^2 + 2e^phi K phi\']'
    ' - d/dr(2 sqrt(h) phi\')  => (Z, mu) = (8, 2) one integrand',
    sp.simplify(sqh*(-sp.exp(2*phi)*R_L)
                - (sqh*(4*pp**2 + 2*sp.exp(phi)*Ktr*pp) - sp.diff(2*sqh*pp, r))) == 0)
cL, Z0 = sp.symbols('c_L Z_0', positive=True)
chk('C3: with block coefficient c_L and independent kinetic Z0: total (Z, mu)'
    ' = (Z0 + 8c_L, 2c_L) exactly (the two-parameter provenance decomposition)',
    sp.simplify(sqh*(Z0/2*pp**2 - cL*sp.exp(2*phi)*R_L)
                - (sqh*((Z0/2 + 4*cL)*pp**2 + 2*cL*sp.exp(phi)*Ktr*pp)
                   - sp.diff(2*cL*sqh*pp, r))) == 0)

# --- C4: the THREE curvature objects give DIFFERENT theories (EL is IBP-blind).
# object 1: -e^{2phi} R_L (the Route-B package)
S1 = sq*(-sp.exp(2*phi)*R_L)
# object 2: e^{2phi} R^{(3)}, R3 of the 3-metric diag(e^{2phi}, rho^2, rho^2 sin^2)
g3 = sp.Matrix([[sp.exp(2*phi), 0, 0], [0, rho**2, 0], [0, 0, rho**2*sp.sin(th)**2]])
R3 = ricci_scal(g3, [r, th, ps])
chk('C4a: R^{(3)} - (R^{(2)} + Kc) = 4e^{-2phi}(phi\'rho\' - rho\'\')/rho (own computation);'
    ' at rho=r this is EXACTLY the banked native_geometric_action:47 form 4e^{-2phi}phi\'/r',
    sp.simplify(R3 - (R2 + Kc + 4*sp.exp(-2*phi)*(pp*rp - rho.diff(r, 2))/rho)) == 0
    and sp.simplify((R3 - (R2 + Kc)).subs({rho.diff(r, 2): 0, rp: 1}).subs(rho, r)
                    - 4*sp.exp(-2*phi)*pp/r) == 0)
S2 = sq*(-sp.exp(2*phi)*R3)
# object 3: weighted 4D R: e^{2phi} R_4 on the full metric
g4 = sp.Matrix([[-sp.exp(-2*phi)*c**2, 0, 0, 0], [0, sp.exp(2*phi), 0, 0],
                [0, 0, rho**2, 0], [0, 0, 0, rho**2*sp.sin(th)**2]])
R4 = ricci_scal(g4, [t, r, th, ps])
S3 = sq*(-sp.exp(2*phi)*R4)
d12 = sp.simplify(EL(S1, phi) - EL(S2, phi))
d13 = sp.simplify(EL(S1, phi) - EL(S3, phi))
d23 = sp.simplify(EL(S2, phi) - EL(S3, phi))
chk('C4b: the three curvature objects are pairwise DIFFERENT THEORIES: phi-EL differences'
    ' nonzero (EL is IBP-blind, so these are real dynamical differences, not boundary terms)',
    d12 != 0 and d13 != 0 and d23 != 0)
chk('C4c: weighted-4D object carries an e^{+2phi}-type potential absent from the R_L package:'
    ' EL difference (S3 vs S1) survives at phi\'=0, phi\'\'=0 (derivative-free content)',
    sp.simplify(d13.subs({phi.diff(r, 2): 0, pp: 0})) != 0)

# ---------------------------------------------------------------- D. no-orphan audit
def shift(e):
    return e.subs(phi, phi + lam)
mat_a = sp.Function('a_m')(r)   # phi-blind matter stand-in -(1/2)A a'^2 - V(rho,a)
Am = sp.Function('A_m', positive=True)(rho)
Vm = sp.Function('V_m')(rho)
Lm = -sp.Rational(1, 2)*Am*mat_a.diff(r)**2 - Vm
bdry = sp.diff(2*sqh*pp, r)     # the Route-B IBP boundary term
chk('D1: FULL shift audit: L_G^A + L_m, L_G^B + L_m, and the IBP boundary term are ALL'
    ' exactly shift-invariant; L_P^A breaks ONLY by the Kc piece'
    ' -2(e^{-2lam}-1)e^{-2phi}rho\'^2 (weight -2, chi-pinning-licensed);'
    ' NO orphan weight exists for the weight-0 mixing term to compensate',
    sp.simplify(shift(LG_A + Lm) - (LG_A + Lm)) == 0
    and sp.simplify(shift(LG_B + Lm) - (LG_B + Lm)) == 0
    and sp.simplify(shift(bdry) - bdry) == 0
    and sp.simplify(shift(LP_A) - LP_A + 2*(sp.exp(-2*lam) - 1)*sp.exp(-2*phi)*rp**2) == 0)
chk('D2: the point-particle coupling a(phi)dtau = e^{phi}e^{-phi}dt is weight-0 (static)',
    sp.simplify(shift(sp.exp(phi)*sp.exp(-phi)) - 1) == 0)
chk('D3: a weight-0 term CANNOT compensate the P-branch weight -2 residue:'
    ' shift(mixing) - mixing = 0 identically, while the residue is lam-dependent',
    sp.simplify(shift(Lmix) - Lmix) == 0)

# ---------------------------------------------------------------- E. the (Z, mu) sheet
chk('E-sheet: EVERY (Z, mu) point is rule-admissible: general L_G^{(Z,mu)} exactly'
    ' shift-invariant (RULE-1); flat VALUE of the full transverse+phi sector = 0 (RULE-2);'
    ' weights pure exponentials e^0 (RULE-3)',
    sp.simplify(shift(LG) - LG) == 0
    and onflat(sq*((Z/2)*pp**2 + R2 + sp.exp(2*phi)*Kc + mu*sp.exp(phi)*Ktr*pp)) == 0)

Phi_flux = sp.diff(LG, pp)
chk('E1: general flux Phi = Z rho^2 phi\' + 2 mu rho rho\'; G phi-EOM = conservation of Phi',
    sp.simplify(Phi_flux - (Z*rho**2*pp + 2*mu*rho*rp)) == 0
    and sp.simplify(EL(LG, phi) + sp.diff(Phi_flux, r)) == 0)

a_, b_, p0 = sp.symbols('a_c b_c phi_0', real=True)
rho_f = a_*r + b_
phi_f = p0 - (2*mu/Z)*sp.log(rho_f)
def onfam(e):
    e = e.subs({phi.diff(r, 2): phi_f.diff(r, 2), pp: phi_f.diff(r),
                rho.diff(r, 2): rho_f.diff(r, 2), rp: rho_f.diff(r)})
    return sp.simplify(e.subs({phi: phi_f, rho: rho_f}))
chk('E2a: flat-analog rho=ar+b, phi=phi0-(2mu/Z)ln rho solves BOTH general-(Z,mu) G EOMs'
    ' => vacuum-deformation exponent s = 2mu/Z (A: 0; B: 1/2); clock e^{-2phi} prop rho^{2s}',
    onfam(EL(LG, phi)) == 0 and onfam(EL(LG, rho)) == 0
    and sp.simplify(sp.expand_log(sp.log(sp.exp(-2*phi_f))
                    - sp.log(sp.exp(-2*p0)*rho_f**(2*(2*mu/Z))), force=True)) == 0)
chk('E2b: control: at mu=0 flat solves G',
    onflat(EL(LG.subs(mu, 0), phi)) == 0 and onflat(EL(LG.subs(mu, 0), rho)) == 0)

phit = sp.Function('phit')(r)
tosub = {pp: phit.diff(r) - (2*mu/Z)*rp/rho, phi: phit - (2*mu/Z)*sp.log(rho)}
kin = (Z/2)*rho**2*pp**2 + 2*mu*rho*rp*pp
chk('E3: kinetic identity: kin = (Z/2)rho^2 phit\'^2 - (2mu^2/Z)rho\'^2,'
    ' phit = phi + (2mu/Z)ln rho (Route B: -rho\'^2 exactly)',
    sp.simplify(kin.subs(tosub) - ((Z/2)*rho**2*phit.diff(r)**2 - (2*mu**2/Z)*rp**2)) == 0)

kk = sp.sqrt(Z/(Z + mu**2))
psi_ = sp.Function('psi_f')(r)
sg = sp.Function('sigma_f', positive=True)(r)
LG_til = (Z/2)*rho**2*phit.diff(r)**2 - (2 + 2*mu**2/Z)*rp**2 + 2
chk('E4: vacuum-G isomorphism: LG^{(Z,mu)} == LG^{(Z,0)}(psi,sigma) under psi=k*phit,'
    ' sigma=rho/k, k^2 = Z/(Z+mu^2) (re-derived); Route B: k^2 = 2/3',
    sp.simplify(sp.expand(LG.subs(tosub)) - LG_til) == 0
    and sp.simplify(LG_til.subs({phit.diff(r): psi_.diff(r)/kk, phit: psi_/kk,
                                 rp: kk*sg.diff(r), rho: kk*sg})
                    - ((Z/2)*sg**2*psi_.diff(r)**2 - 2*sg.diff(r)**2 + 2)) == 0
    and sp.simplify(kk**2 - Z/(Z + mu**2)) == 0
    and sp.Rational(2, 3) == sp.nsimplify((kk**2).subs({Z: 8, mu: 2})))
chk('E5: Branch P in tilde vars: gradient coeff = 2e^{-2phit}rho^{4mu/Z} + 2mu^2/Z'
    ' (rho-dependent iff mu != 0): the isomorphism FAILS wherever the depth field is anchored',
    sp.simplify(sp.expand(LP.subs(tosub))
                - ((Z/2)*rho**2*phit.diff(r)**2
                   - (2*sp.exp(-2*phit)*rho**(4*mu/Z) + 2*mu**2/Z)*rp**2 + 2)) == 0)
grr_new = sp.exp(2*(phit - (2*mu/Z)*sp.log(rho))).subs({phit: psi_/kk, rho: kk*sg})
chk('E6: anchoring failure: g_rr = e^{2phi} -> e^{2psi/k}(k sigma)^{-4mu/Z}'
    ' (log-space compare); mu=0 collapses to e^{2psi} (k=1)',
    sp.simplify(sp.expand_log(sp.log(grr_new)
                - (2*psi_/kk - (4*mu/Z)*sp.log(kk*sg)), force=True)) == 0)

# E6b (my sharpening of the anchoring argument): Route-B G admits NO phi==const solution
# with rho' != 0 -- so no Route-B solution has flat OBSERVABLES; an anchoring-preserving
# equivalence is impossible because the solution SETS differ at observable level.
cst = sp.Symbol('phi_c', real=True)
elphi_const = sp.simplify(EL(LG, phi).subs({phi.diff(r, 2): 0, pp: 0, phi: cst}))
elrho_const = sp.simplify(EL(LG, rho).subs({phi.diff(r, 2): 0, pp: 0, phi: cst}))
# phi-EOM with phi'=0: -(2 mu rho rho')' = -2mu(rho'^2 + rho rho'') = 0 => rho rho'' = -rho'^2
# rho-EOM with phi'=0: 4 rho'' = 0 => rho'' = 0. Together: rho'^2 = 0.
chk('E6b (verifier extension): Route-B/any-mu G has NO phi==const solution with rho\'!=0:'
    ' phi-EOM forces rho rho\'\'=-rho\'^2 while rho-EOM forces rho\'\'=0 => rho\'=0;'
    ' flat observables are Route-A-reachable, Route-B-unreachable (exact, mu!=0)',
    sp.simplify(elphi_const + 2*mu*(rp**2 + rho*rho.diff(r, 2))) == 0
    and sp.simplify(elrho_const - 4*rho.diff(r, 2)) == 0)

# E7: even-fold natural BCs across the whole sheet
pPv, rPv, rhs_ = sp.symbols('phip rhop rho_s', real=True)
W = sp.Symbol('W', positive=True)
Lsym = (Z/2)*rhs_**2*pPv**2 + 2*mu*rhs_*rPv*pPv + 2 - 2*W*rPv**2
Pi_phi = sp.diff(Lsym, pPv); pi_rho = sp.diff(Lsym, rPv)
sol = sp.solve([Pi_phi, pi_rho], [pPv, rPv], dict=True)
Mm = sp.Matrix([[sp.diff(Pi_phi, pPv), sp.diff(Pi_phi, rPv)],
                [sp.diff(pi_rho, pPv), sp.diff(pi_rho, rPv)]])
chk('E7: even-fold natural BCs (Pi_phi = pi_rho = 0) uniquely force phi\'=rho\'=0 for ALL'
    ' (Z>0, mu, W>0): det = -4rho^2(WZ + mu^2) != 0 -- fold pins family-robust',
    sol == [{pPv: 0, rPv: 0}]
    and sp.simplify(Mm.det() + 4*rhs_**2*(W*Z + mu**2)) == 0)

# E8: flux-without-twist (sec 6.3): odd+odd canon (Delta phi = 0) with mu != 0 carries
# Phi = (2mu/Z)*Z*ln(rho2/rho1)/I. Derivation: phi' = (Phi - 2 mu rho rho')/(Z rho^2), so
# Delta phi = (Phi/Z) I - (2mu/Z) ln(rho2/rho1) with I = INT dr/rho^2.
PhiS, I_, r1_, r2_ = sp.symbols('Phi_c I rho_1 rho_2', positive=True)
dphi = (PhiS/Z)*I_ - (2*mu/Z)*sp.log(r2_/r1_)
solq = sp.solve(sp.Eq(dphi, 0), PhiS)
chk('E8: Delta phi = 0 (canon odd+odd) => Phi = 2 mu ln(rho2/rho1)/I  (at Z=8, mu=2:'
    ' Phi = 4 ln(rho2/rho1)/I = d2b E3); mu=0 => Phi=0 (no flux without twist)',
    len(solq) == 1 and sp.simplify(solq[0] - 2*mu*sp.log(r2_/r1_)/I_) == 0
    and sp.simplify(solq[0].subs(mu, 2) - 4*sp.log(r2_/r1_)/I_) == 0)

# ---------------------------------------------------------------- F. symmetry relocation
pv, rv, pd, rd = sp.symbols('phi_v rho_v phid rhod', real=True)  # plain symbols, no subs traps
LGB_sym = 4*rv**2*pd**2 + 4*rv*rd*pd + 2 - 2*rd**2
refl = LGB_sym.subs(pd, -pd)                       # phi -> 2a - phi: values drop out (no phi value in L), phi' -> -phi'
chk('F1: phi-reflection flips the mixing term only: L(refl) - L = -8 rho rho\' phi\''
    ' (NOT a bulk symmetry of Route-B G)',
    sp.simplify(refl - LGB_sym + 8*rv*rd*pd) == 0)
ptd = sp.Symbol('phitd', real=True)
LGB_til = 4*rv**2*ptd**2 - 3*rd**2 + 2
chk('F2: in phitilde: L_G^B = 4rho^2 phit\'^2 - 3rho\'^2 + 2 (phit-value-free, even in phit\')'
    ' => shift AND reflection symmetries live in phitilde',
    sp.simplify(sp.expand(LG_B.subs({pp: phit.diff(r) - rp/(2*rho),
                                     phi: phit - sp.log(rho)/2}))
                - (4*rho**2*phit.diff(r)**2 - 3*rp**2 + 2)) == 0
    and sp.simplify(LGB_til.subs(ptd, -ptd) - LGB_til) == 0)

# ---------------------------------------------------------------- G. signature non-discriminator
Mk = sp.Matrix([[Z*rhs_**2, 2*mu*rhs_], [2*mu*rhs_, -4*W]])/2
chk('G1: kinetic quadratic form indefinite for ALL (Z>0, mu>=0, W>0): det = -rho^2(WZ+mu^2) < 0'
    ' including mu=0 -- ghost-type health does NOT discriminate the routes',
    sp.simplify(Mk.det()*4 + rhs_**2*(4*W*Z + 4*mu**2)) == 0)

# ----------------------------------------------------------------
nok = sum(1 for _, ok in results if ok)
print(f"\n{nok}/{len(results)} verifier checks PASS")
if nok != len(results):
    raise SystemExit(1)
