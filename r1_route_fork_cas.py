"""r1_route_fork_cas.py -- R1 (route-fork native derivation): CAS verification of every
symbolic claim in r1_route_fork_native_derivation.md.

Task (PURSUIT_CHARTER_2026-07-04.md par.3, step R1): does the positional-dilation principle --
via the SAME derivation logic that forced everything else in the native action -- FORCE Route A,
FORCE Route B, or leave the fork FREE?

Frame (all cited, inherited):
  Constrained two-player metric  ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 + h_AB dx^A dx^B
  (native_field_equations_constrained_two_player_results.md:90);  sqrt(-g) = c sqrt(h) (phi-free).
  Native action skeleton  S = INT c sqrt(h)[ (Z/2)phi'^2 + R2 + W_chi*K2 + L_m ]
  (native_geometric_action_results.md:13);  K_AB = (1/2)e^{-phi} d_r h_AB;  K2 = K_AB K^AB - K^2;
  W_chi = e^{2phi} (G) / 1 (P).
  Route B package: kinetic := -e^{2phi} R_L integrated by parts -> sqrt(h)[4phi'^2 + 2e^phi K phi']
  i.e. Z=8 + mixing coefficient mu=2 on  mu*sqrt(h)e^phi K phi'  (native_geometric_action:73-77).
  Round reduction per 4pi steradian: Lbar_G^A=(Z/2)rho^2 phi'^2 + 2 - 2rho'^2;
  Lbar_P^A = same with e^{-2phi} on rho'^2 (d2b_no_structure_in_G.md par.2; d2c_part1_mixing.py).

General rule-admissible family used below: kinetic-sector coefficient pair (Z, mu):
  Lbar^{(Z,mu)} = (Z/2)rho^2 phi'^2 + 2*mu*rho*rho'*phi' + 2 - 2*W*rho'^2   (W=1 G, e^{-2phi} P)
  Route A = (Z free, mu=0);  Route B = (Z=8, mu=2).
Run: python3 r1_route_fork_cas.py  (all symbolic, CPU, seconds; no solves)
"""
import sympy as sp

r, t, th, lam, aa, c = sp.symbols('r t theta lambda a c', real=True)
Z, mu = sp.symbols('Z mu', positive=True)          # Z>0 (banked probe range); mu>=0 handled below
muR = sp.Symbol('mu', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)

checks = []
def check(name, cond):
    ok = bool(cond)
    checks.append((name, ok))
    print(('PASS ' if ok else 'FAIL ') + name)

rp_, pp_ = rho.diff(r), phi.diff(r)

# =============================================================== A. frame + shift-weight table
# h_AB = rho^2 diag(1, sin^2 th)   (round transverse block)
h = sp.Matrix([[rho**2, 0], [0, rho**2*sp.sin(th)**2]])
hinv, hp = h.inv(), h.diff(r)
K_AB = sp.Rational(1, 2)*sp.exp(-phi)*hp
K = (hinv*K_AB).trace()
KK = (hinv*K_AB*hinv*K_AB).trace()          # K_AB K^AB
K2 = KK - K**2
sqrth = rho**2*sp.sin(th)                    # sqrt(det h), th in (0,pi)
R2ang = 2/rho**2                             # intrinsic curvature of the round 2-sphere

# g4 = diag(-e^{-2phi}c^2, e^{2phi}, h): det = -c^2 * det h  => sqrt(-g)=c*sqrt(h), phi-free
g4det = (-sp.exp(-2*phi)*c**2) * sp.exp(2*phi) * h.det()
check('A1: sqrt(-g) = c sqrt(h) is phi-FREE (dilation factors cancel; the measure carries no'
      ' shift-weight)', sp.simplify(g4det + c**2*h.det()) == 0)

# shift phi -> phi + lam: K_AB -> e^{-lam}K_AB (h fixed), e^{k phi} -> e^{k lam} e^{k phi}, phi' inv.
def shifted(expr):
    return expr.subs(phi, phi + lam)
w = {}
w['phip2']   = sp.simplify(shifted(pp_**2)/pp_**2)                       # kinetic
w['R2']      = sp.simplify(shifted(R2ang)/R2ang)                        # intrinsic transverse
w['K2']      = sp.simplify(shifted(K2)/K2)                              # extrinsic quadratic
w['e2f_K2']  = sp.simplify(shifted(sp.exp(2*phi)*K2)/(sp.exp(2*phi)*K2))
w['mix']     = sp.simplify(shifted(sp.exp(phi)*K*pp_)/(sp.exp(phi)*K*pp_))
w['e2f_KK']  = sp.simplify(shifted(sp.exp(2*phi)*KK)/(sp.exp(2*phi)*KK))
w['e2f_Ksq'] = sp.simplify(shifted(sp.exp(2*phi)*K**2)/(sp.exp(2*phi)*K**2))
check('A2: shift-weight table -- phi\'^2:0, R2:0, K2:-2, e^{2phi}K2:0, e^phi K phi\':0,'
      ' e^{2phi}K_ABK^AB:0, e^{2phi}K^2:0  (weights as e^{k lam} factors)',
      w['phip2'] == 1 and w['R2'] == 1 and sp.simplify(w['K2'] - sp.exp(-2*lam)) == 0
      and w['e2f_K2'] == 1 and w['mix'] == 1 and w['e2f_KK'] == 1 and w['e2f_Ksq'] == 1)

# =============================================================== B. the two admission criteria
# B1 -- flatness-VALUE criterion (the banked one, native_geometric_action (A)): on the flat
# reference (phi=0, rho=r) the angular-mismatch density must be ZERO; phi-sector candidates
# all vanish there trivially (phi'=0) -- the criterion has NO GRIP on the phi-sector.
flat = {phi: sp.Integer(0), rho: r}
def onflat(expr):
    e = expr
    for k, v in [(phi.diff(r, 2), 0), (pp_, 0), (rho.diff(r, 2), 0), (rp_, 1)]:
        e = e.subs(k, v)
    return sp.simplify(e.subs(phi, 0).subs(rho, r))
check('B1a: flat-VALUE: R2 + e^{2phi}K2 = 0 for ANY phi on round flat-embedding rho=r'
      ' (the banked G cancellation)',
      sp.simplify((R2ang + sp.exp(2*phi)*K2).subs({rp_: 1, rho: r})) == 0)
check('B1b: flat-VALUE excludes the separate K-quadratics: e^{2phi}K^2 -> 4/r^2 != 0,'
      ' e^{2phi}K_ABK^AB -> 2/r^2 != 0 on flat',
      sp.simplify(onflat(sp.exp(2*phi)*K**2) - 4/r**2) == 0
      and sp.simplify(onflat(sp.exp(2*phi)*KK) - 2/r**2) == 0)
check('B1c: flat-VALUE has NO GRIP on the phi-sector: phi\'^2 -> 0 and e^phi K phi\' -> 0 on flat'
      ' (both vanish; neither is excluded nor required)',
      onflat(pp_**2) == 0 and onflat(sp.exp(phi)*K*pp_) == 0)

# B2 -- flatness-as-STATIONARITY would be a DIFFERENT criterion; it is INADMISSIBLE as the
# forcing rule because it kills the banked Branch P itself (P's source 4e^{-2phi} already
# fails flat), not just the mixing term.
def EL(L, q):
    return sp.simplify(sp.diff(L, q) - sp.diff(sp.diff(L, q.diff(r)), r))
LP_A = (Z/2)*rho**2*pp_**2 + 2 - 2*sp.exp(-2*phi)*rp_**2
LG_A = (Z/2)*rho**2*pp_**2 + 2 - 2*rp_**2
Lmix = 2*mu*rho*rp_*pp_                       # round reduction of  mu sqrt(h) e^phi K phi'  per sr
LG_B = LG_A.subs(Z, 8) + Lmix.subs(mu, 2)
LP_B = LP_A.subs(Z, 8) + Lmix.subs(mu, 2)
check('B2a: flat-STATIONARITY fails for banked Route-A Branch P: phi-EL residual on flat'
      ' = +4 (the P source 4e^{-2phi}rho\'^2) != 0',
      sp.simplify(onflat(EL(LP_A, phi)) - 4) == 0)
check('B2b: flat-STATIONARITY fails for Route-B Branch G: residual -4 (reproduces d2c M4b)',
      sp.simplify(onflat(EL(LG_B, phi)) + 4) == 0)

# =============================================================== C. Route B package provenance
# C1: R_L = Ricci scalar of the 2D longitudinal block  diag(-e^{-2phi}c^2, e^{2phi})
gL = sp.Matrix([[-sp.exp(-2*phi)*c**2, 0], [0, sp.exp(2*phi)]])
gLinv = gL.inv()
x2 = [t, r]
def christoffel(g, ginv, xs):
    n = len(xs)
    Gam = [[[sp.simplify(sum(ginv[a, d]*(g[d, b].diff(xs[cc]) + g[d, cc].diff(xs[b])
             - g[b, cc].diff(xs[d])) for d in range(n))/2) for cc in range(n)]
            for b in range(n)] for a in range(n)]
    return Gam
Gam = christoffel(gL, gLinv, x2)
def ricci_scalar(g, ginv, Gam, xs):
    n = len(xs)
    Ric = sp.zeros(n)
    for b in range(n):
        for cc in range(n):
            expr = 0
            for a in range(n):
                expr += Gam[a][b][cc].diff(xs[a]) - Gam[a][b][a].diff(xs[cc])
                for d in range(n):
                    expr += Gam[a][a][d]*Gam[d][b][cc] - Gam[a][cc][d]*Gam[d][b][a]
            Ric[b, cc] = sp.simplify(expr)
    return sp.simplify(sum(ginv[b, cc]*Ric[b, cc] for b in range(n) for cc in range(n)))
R_L = ricci_scalar(gL, gLinv, Gam, x2)
check('C1: longitudinal 2D-block Ricci  R_L = 2e^{-2phi}(phi\'\' - 2phi\'^2)  (from scratch)',
      sp.simplify(R_L - 2*sp.exp(-2*phi)*(phi.diff(r, 2) - 2*pp_**2)) == 0)

# C2: the IBP identity behind Route B:  sqrt(h)(-e^{2phi}R_L) = sqrt(h)(4phi'^2 + 2e^phi K phi')
#     - d/dr(2 sqrt(h) phi')   [uses (sqrt h)' = sqrt(h) e^phi K]
lhs = sqrth*(-sp.exp(2*phi)*R_L)
rhs = sqrth*(4*pp_**2 + 2*sp.exp(phi)*K*pp_) - sp.diff(2*sqrth*pp_, r)
check('C2: Route-B IBP package EXACT: -sqrt(h)e^{2phi}R_L = sqrt(h)[4phi\'^2 + 2e^phi K phi\']'
      ' - (2 sqrt(h) phi\')\'  => Z=8 and mu=2 are ONE integrand (inseparable, as banked)',
      sp.simplify(lhs - rhs) == 0)

# C3: linearity in the block coefficient c_L: coefficient c_L*(-e^{2phi}R_L) gives Z-contribution
#     8 c_L and mixing 2 c_L; an independent invariant kinetic (Z0/2)phi'^2 may coexist.
cL, Z0 = sp.symbols('c_L Z_0', positive=True)
lhs3 = sqrth*(Z0/2*pp_**2 + cL*(-sp.exp(2*phi))*R_L)
rhs3 = sqrth*((Z0/2 + 4*cL)*pp_**2 + 2*cL*sp.exp(phi)*K*pp_) - sp.diff(2*cL*sqrth*pp_, r)
check('C3: general rule-compliant kinetic sector = (Z0/2 + 4c_L)phi\'^2 + 2c_L e^phi K phi\''
      ' + bdry: TOTAL (Z, mu) = (Z0 + 8c_L, 2c_L) -- a TWO-parameter family; A=(Z0,0), B=(0,1)',
      sp.simplify(lhs3 - rhs3) == 0)

# =============================================================== D. no orphan shift-weight
check('D1: L_G^A and L_G^B are BOTH exactly shift-invariant (no uncompensated weight that'
      ' would REQUIRE the mixing term as a compensator); L_P^A breaks by the known'
      ' -2(e^{-2lam}-1)e^{-2phi}rho\'^2 only (chi-pinning-licensed)',
      sp.simplify(shifted(LG_A) - LG_A) == 0
      and sp.simplify(shifted(LG_B) - LG_B) == 0
      and sp.simplify(shifted(LP_A) - LP_A + 2*(sp.exp(-2*lam) - 1)*sp.exp(-2*phi)*rp_**2) == 0)

# =============================================================== E. the general (Z, mu) family
LG = (Z/2)*rho**2*pp_**2 + 2*mu*rho*rp_*pp_ + 2 - 2*rp_**2
LP = (Z/2)*rho**2*pp_**2 + 2*mu*rho*rp_*pp_ + 2 - 2*sp.exp(-2*phi)*rp_**2
Phi_flux = sp.diff(LG, pp_)     # = Z rho^2 phi' + 2 mu rho rho'
check('E1: general-G flux  Phi = Z rho^2 phi\' + 2 mu rho rho\';  phi-EOM = -(Phi)\' = 0'
      ' (conserved for every (Z,mu))',
      sp.simplify(Phi_flux - (Z*rho**2*pp_ + 2*mu*rho*rp_)) == 0
      and sp.simplify(EL(LG, phi) + sp.diff(Phi_flux, r)) == 0)

# E2: deformed flat-analog for GENERAL (Z, mu): rho = a r + b, phi = phi0 - (2mu/Z) ln rho
a_, b_, phi0 = sp.symbols('a b phi_0', real=True)
rho_f = a_*r + b_
phi_f = phi0 - (2*mu/Z)*sp.log(rho_f)
subs_f = {phi.diff(r, 2): phi_f.diff(r, 2), pp_: phi_f.diff(r), phi: phi_f,
          rho.diff(r, 2): rho_f.diff(r, 2), rp_: rho_f.diff(r), rho: rho_f}
check('E2a: the deformed flat-analog  rho = ar+b, phi = phi0 - (2mu/Z)ln rho  solves BOTH'
      ' general-(Z,mu) G EOMs: deformation exponent s = 2mu/Z (Route B: s=1/2, d2c M4c;'
      ' Route A mu=0: s=0 = flat). THE R2 OBSERVABLE IS THE RATIO s.',
      sp.simplify(EL(LG, phi).subs(subs_f)) == 0
      and sp.simplify(EL(LG, rho).subs(subs_f)) == 0)
check('E2b: at mu=0 flat itself solves G (control): residual of flat in the mu=0 G phi-EOM = 0',
      sp.simplify(onflat(EL(LG.subs(mu, 0), phi))) == 0)

# E3: kinetic-block identity in the shifted field phit = phi + (2mu/Z) ln rho
phit = sp.Function('phitilde')(r)
kin = (Z/2)*rho**2*pp_**2 + 2*mu*rho*rp_*pp_
subs_t = {pp_: phit.diff(r) - (2*mu/Z)*rp_/rho, phi: phit - (2*mu/Z)*sp.log(rho)}
check('E3: kinetic block == (Z/2)rho^2 phitilde\'^2 - (2mu^2/Z)rho\'^2  with'
      ' phitilde = phi + (2mu/Z)ln rho  (at Z=8,mu=2: minus rho\'^2 exactly = d2c M5)',
      sp.simplify(kin.subs(subs_t) - ((Z/2)*rho**2*phit.diff(r)**2 - (2*mu**2/Z)*rp_**2)) == 0
      and sp.simplify((kin.subs(subs_t) - ((Z/2)*rho**2*phit.diff(r)**2 - rp_**2))
                      .subs({Z: 8, mu: 2})) == 0)

# E4: VACUUM-G Lagrangian isomorphism: L_G^{(Z,mu)}(phi,rho) == L_G^{(Z,0)}(psi,sigma) under the
#     CONSTANT rescaling  psi = k*phitilde, sigma = rho/k,  k^2 = 2/(2 + 2mu^2/Z).
kcon = sp.sqrt(2/(2 + 2*mu**2/Z))
psi = sp.Function('psi')(r)
sig = sp.Function('sigma', positive=True)(r)
LG_tilde = (Z/2)*rho**2*phit.diff(r)**2 - (2 + 2*mu**2/Z)*rp_**2 + 2   # = L_G^{(Z,mu)} in tilde vars
LG_target = ((Z/2)*sig**2*psi.diff(r)**2 - 2*sig.diff(r)**2 + 2)       # Route-A-form, same Z
iso = {phit.diff(r): psi.diff(r)/kcon, phit: psi/kcon,
       rp_: kcon*sig.diff(r), rho: kcon*sig}
check('E4: VACUUM-G isomorphism EXACT: L_G^{(Z,mu)} == L_G^{(Z,0)} under psi = k*phitilde,'
      ' sigma = rho/k, k^2 = Z/(Z + mu^2)  -- in vacuum G the mixing term is DYNAMICALLY'
      ' invisible up to a constant field rescaling',
      sp.simplify(LG_tilde.subs(iso) - LG_target) == 0
      and sp.simplify(kcon**2 - Z/(Z + mu**2)) == 0)

# E5: the isomorphism FAILS in Branch P: the rho'^2 coefficient in tilde vars is
#     2 e^{-2 phitilde} rho^{4mu/Z} + 2mu^2/Z  -- EXPLICITLY rho-dependent iff mu != 0,
#     so no constant rescaling removes mu (the routes are physically inequivalent where the
#     depth field is anchored: P source, matter coupling a(phi), junctions).
LP_tilde = sp.simplify(LP.subs(subs_t))
coeff_claim = (Z/2)*rho**2*phit.diff(r)**2 - (2*sp.exp(-2*phit)*rho**(4*mu/Z) + 2*mu**2/Z)*rp_**2 + 2
check('E5: Branch-P in tilde vars: gradient coefficient = 2e^{-2phitilde}rho^{4mu/Z} + 2mu^2/Z'
      ' (rho-dependent iff mu!=0): NO field redefinition equates the routes in P',
      sp.simplify(LP_tilde - coeff_claim) == 0)

# E6: the E4 map does NOT preserve the metric observables: g_rr = e^{2phi} reads
#     e^{2 psi/k} * (k sigma)^{-4mu/Z} in the new variables -- explicit rho(=k sigma) dependence
#     iff mu != 0, so (psi, sigma) is NOT the dilation/areal pair of any UDT metric of the same
#     form; the isomorphism is dynamics-only, not physics.
grr = sp.exp(2*phi)
grr_new = sp.simplify(grr.subs({phi: phit - (2*mu/Z)*sp.log(rho)}).subs(
    {phit: psi/kcon, rho: kcon*sig}))
e6_diff = sp.expand_log(sp.log(grr_new) - (2*psi/kcon - (4*mu/Z)*sp.log(kcon*sig)), force=True)
check('E6: g_rr = e^{2phi} -> e^{2psi/k}(k sigma)^{-4mu/Z}: the vacuum-G isomorphism does NOT'
      ' preserve the metric anchoring (clock/ruler slaved to areal radius iff mu != 0)'
      ' [compared in log space]',
      sp.simplify(e6_diff) == 0)

# E7: even-fold natural BCs for the general family: momenta map nondegenerate for all mu when
#     Z>0, W>0: det = -rho^2(4 W Z + 4 mu^2) != 0  => phi'=rho'=0 pins survive family-wide.
pPv, rPv, rhos, phis = sp.symbols('phip rhop rho_s phi_s', real=True)
W = sp.Symbol('W', positive=True)
Pi_phi = Z*rhos**2*pPv + 2*mu*rhos*rPv
pi_rho = -4*W*rPv + 2*mu*rhos*pPv
solBC = sp.solve([Pi_phi, pi_rho], [pPv, rPv], dict=True)
det = sp.det(sp.Matrix([[Z*rhos**2, 2*mu*rhos], [2*mu*rhos, -4*W]]))
check('E7: general-(Z,mu) even-fold natural BCs uniquely force phi\'=rho\'=0'
      ' (det = -rho^2(4WZ + 4mu^2) != 0 for Z>0): fold structure is family-robust',
      solBC == [{pPv: 0, rPv: 0}]
      and sp.simplify(det + rhos**2*(4*W*Z + 4*mu**2)) == 0)

# =============================================================== F. symmetry relocation
check('F1: the odd-reflection phi -> 2a - phi is NOT a bulk symmetry of L_G^B'
      ' (Delta L = -16 rho rho\' phi\' + 8a-independent... exact residual -2*(2 mixing)):'
      ' the mixing term flips sign under phi-reflection',
      sp.simplify(LG_B.subs(phi, 2*aa - phi).subs(pp_, -pp_) - LG_B + 8*rho*rp_*pp_) == 0)
LG_B_tilde = 4*rho**2*phit.diff(r)**2 - 3*rp_**2 + 2
check('F2: in phitilde the Route-B G Lagrangian is phitilde-value-free and even in phitilde\''
      ' => its bulk symmetries are phitilde -> phitilde + c and phitilde -> 2a - phitilde:'
      ' Route B RELOCATES the shift/fold symmetry class from phi to phitilde',
      sp.simplify(LG_B_tilde.subs(phit, 2*aa - phit).subs(phit.diff(r), -phit.diff(r))
                  - LG_B_tilde) == 0
      and sp.simplify(LG_B_tilde.subs(phit, phit + aa) - LG_B_tilde) == 0
      and sp.simplify(LG_B.subs(subs_t.copy() | {mu: 2, Z: 8}).subs({mu: 2, Z: 8})
                      - LG_B_tilde) == 0)

# =============================================================== G. kinetic-signature note
# The reduced kinetic quadratic form q(phi',rho') = (Z/2)rho^2 phi'^2 + 2mu rho phi'rho' - 2W rho'^2
# is INDEFINITE for every (Z>0, mu, W>0) -- incl. mu=0 -- (conformal-mode-type indefiniteness),
# so no ghost/health criterion DISCRIMINATES the routes at this level.
Mkin = sp.Matrix([[Z*rhos**2, 2*mu*rhos], [2*mu*rhos, -4*W]])/2
check('G1: kinetic 2x2 form indefinite for ALL (Z>0, mu, W>0): det = -rho^2(WZ + mu^2) < 0'
      ' both at mu=0 and mu!=0 -- signature does not discriminate the routes',
      sp.simplify(sp.det(Mkin) + rhos**2*(W*Z + mu**2)) == 0)

# ===============================================================
n_ok = sum(1 for _, ok in checks if ok)
print(f"\n{n_ok}/{len(checks)} checks PASS")
if n_ok != len(checks):
    raise SystemExit(1)
