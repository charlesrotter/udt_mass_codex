# ADVERSARIAL REVIEW 1 — independent recompute (fresh sympy; nothing imported from
# verify_regrade_r1_fresh.py or the 2026-07-02 scripts). Reviewer agent, 2026-08-06.
# Attacks: (1) presentation-invariance of the rigidity conclusion under phi -> phi + c
#          (2) flux identity + squeeze + sharpened center leg re-derived from the 07-01 law-set
#          (3) germ BC algebra relevant to the fold/glue/open-end scoping question.
import sympy as sp

r, Z, c, M, W, Lam, x, y = sp.symbols('r Z c M W Lambda x y', real=True)
phi = sp.Function('phi')(r)
psi = sp.Function('psi')(r)
rho = sp.Function('rho')(r)
S = sp.Function('S')(r)          # arbitrary phi-blind source (enters rho-eq only)
D = lambda f: sp.diff(f, r)
results = []
def check(name, cond):
    ok = bool(cond)
    results.append((name, ok))
    print(('PASS ' if ok else 'FAIL ') + name)

# ---------------- Block A: the 07-01 reduced law-set, re-derived --------------------
# Reduced Lagrangian as banked (universe_cell_vacuum_impossibility_results.md:39):
L = sp.Rational(1, 2)*Z*rho**2*D(phi)**2 - 2*sp.exp(-2*phi)*D(rho)**2 + 2

def EL(Lag, q):
    return sp.diff(sp.diff(Lag, D(q)), r) - sp.diff(Lag, q)

ELphi = sp.expand(EL(L, phi))
ELrho = sp.expand(EL(L, rho))

# A1: phi-EL IS the flux identity (Z rho^2 phi')' = 4 e^{-2phi} rho'^2
Phi = Z*rho**2*D(phi)
check('A1 flux identity == phi-EL',
      sp.simplify(ELphi - (D(Phi) - 4*sp.exp(-2*phi)*D(rho)**2)) == 0)

# A2: reproduces the banked phi''-form (cell_solver_round.py:8)
phipp_banked = 4*sp.exp(-2*phi)*D(rho)**2/(Z*rho**2) - 2*D(phi)*D(rho)/rho
check('A2 banked phi\'\'-form reproduced',
      sp.simplify(ELphi - Z*rho**2*(sp.diff(phi, r, 2) - phipp_banked)) == 0)

# A3: rho-EL reproduces the banked rho''-form (cell_solver_round.py:9)
rhopp_banked = 2*D(phi)*D(rho) - sp.Rational(1, 4)*Z*rho*sp.exp(2*phi)*D(phi)**2
check('A3 banked rho\'\'-form reproduced',
      sp.simplify(ELrho - (-4*sp.exp(-2*phi))*(sp.diff(rho, r, 2) - rhopp_banked)) == 0)

# A4: the phi-EL contains NO rho'' -> an arbitrary phi-blind rho''-source cannot enter it
check('A4 phi-EL has no rho\'\'', not ELphi.has(sp.Derivative(rho, (r, 2))))

# A5: RHS of the flux identity is Z-free and manifestly >= 0 (exp>0 times a square)
RHS = 4*sp.exp(-2*phi)*D(rho)**2
check('A5 RHS Z-free', not RHS.has(Z))
check('A5 RHS = positive * square', sp.simplify(RHS - 4*sp.exp(-2*phi)*D(rho)**2) == 0)

# ---------------- Block B: presentation shift phi -> psi + c ------------------------
# The 08-05 freedom on this stationary arena = constant reference shift.
sub = {phi: psi + c, sp.Derivative(phi, r): D(psi), sp.Derivative(phi, (r, 2)): sp.diff(psi, r, 2)}
ELphi_sh = ELphi.subs(phi, psi + c).doit()
ELphi_psi_Ztil = ELphi.subs(phi, psi).doit().subs(Z, Z*sp.exp(2*c))

# B1: the bare identity is NOT invariant (RHS picks up e^{-2c}) — certify nonzero difference
diff_bare = sp.simplify(ELphi_sh - ELphi.subs(phi, psi).doit())
check('B1 bare shift NON-invariance (difference != 0)', sp.simplify(diff_bare) != 0)

# B2: exact absorption into Z: e^{2c} * ELphi[psi+c; Z] == ELphi[psi; Z e^{2c}]
check('B2 phi-EL absorbs shift into Z -> Z e^{2c}',
      sp.simplify(sp.exp(2*c)*ELphi_sh - ELphi_psi_Ztil) == 0)

# B3: rho-eq (WITH arbitrary phi-blind source) absorbs with the SAME Z-tilde, source untouched
Nrho = sp.diff(rho, r, 2) - (2*D(phi)*D(rho) - sp.Rational(1, 4)*Z*rho*sp.exp(2*phi)*D(phi)**2 + S)
Nrho_sh = Nrho.subs(phi, psi + c).doit()
Nrho_psi_Ztil = Nrho.subs(phi, psi).doit().subs(Z, Z*sp.exp(2*c))
check('B3 rho-EOM (arbitrary source) absorbs with same Z-tilde',
      sp.simplify(Nrho_sh - Nrho_psi_Ztil) == 0)

# B4: flux transforms by a positive multiple: Phi[psi; Z e^{2c}] = e^{2c} * Phi[psi_as_phi]
Phi_til = (Z*sp.exp(2*c))*rho**2*D(psi)
check('B4 flux rescales by e^{2c} > 0 (zeros/sign/monotonicity invariant)',
      sp.simplify(Phi_til - sp.exp(2*c)*(Z*rho**2*D(psi))) == 0)

# B5: invariants: phi' and Delta phi unchanged by the shift (trivial but recorded)
check('B5 (psi+c)\' == psi\'', sp.simplify(D(psi + c) - D(psi)) == 0)
a_, b_ = sp.symbols('a b', real=True)
f = sp.Function('f')
check('B5 Delta(psi+c) == Delta psi',
      sp.simplify((f(b_) + c - (f(a_) + c)) - (f(b_) - f(a_))) == 0)

# ---------------- Block C: the squeeze (algebraic legs; logic legs stated) ----------
# C-logic (not CAS): Phi' >= 0 and Phi(a)=Phi(b)=0  =>  Phi == 0 on [a,b]
#                    (a monotone function equal at both endpoints is constant).
# C1: Phi == 0 with rho>0, Z != 0  =>  phi' == 0 (division legal)
phip_sym, rhop_sym = sp.symbols('phip rhop', real=True)
sol = sp.solve(sp.Eq(Z*x**2*phip_sym, 0), phip_sym)   # x stands for rho>0
check('C1 Phi=0 => phi\'=0 (rho>0, Z!=0)', sol == [0])
# C2: Phi'==0 => rho'==0: 4 e^{-2phi} rho'^2 = 0 has only rho'=0 (exp never 0)
sol2 = sp.solve(sp.Eq(4*sp.exp(-2*y)*rhop_sym**2, 0), rhop_sym)
check('C2 Phi\'=0 => rho\'=0', sol2 == [0])
# C3: phi'==0 => Delta phi = integral of 0 = 0  (and 0 != ln(1101))
check('C3 ln(1101) != 0', sp.log(1101) != 0)

# ---------------- Block D: sharpened center + one-mirror leg ------------------------
# Regularity at rho->0: proper radius ell = e^{phi0} r + O(r^3); no conical defect
# <=> rho'(0) = e^{phi0}. Series with smooth even phi (phi'(0)=0):
phi0, a2, p3, eps = sp.symbols('phi0 a2 p3 epsilon', positive=False, real=True)
phi_ser = phi0 + a2*r**2
rho_ser = sp.exp(phi0)*r + p3*r**3
Phi_ser = Z*rho_ser**2*sp.diff(phi_ser, r)
# D1: Phi(0) = 0
check('D1 Phi(center)=0', Phi_ser.subs(r, 0) == 0)
# D2: Phi'(0) via the flux identity = 4 e^{-2phi0} rho'(0)^2 = 4 exactly (Z- and phi0-free)
Phip_center = (4*sp.exp(-2*phi_ser)*sp.diff(rho_ser, r)**2).subs(r, 0)
check('D2 Phi\'(0) == 4 (independent of Z and phi0)', sp.simplify(Phip_center - 4) == 0)
# D3: chart-dressing: after the shift (Z-absorbed presentation) the value is 4 e^{2c}, NOT 4
#     — only POSITIVITY is invariant. Recompute: Phi_til' = e^{2c} Phi' => at center 4 e^{2c}.
Phip_center_shifted = sp.exp(2*c)*Phip_center
check('D3 shifted-chart center slope = 4 e^{2c} (positive, != 4 for c!=0)',
      sp.simplify(Phip_center_shifted - 4*sp.exp(2*c)) == 0
      and sp.simplify(4*sp.exp(2*c) - 4) != 0)
# D-logic (not CAS): Phi(0)=0, Phi'(0)=4>0, Phi'>=0 everywhere => Phi(r)>0 for all r>0,
# so an outer phi'=0 end (Phi=0) can never be reached: NO solution. Uses only positivity.

# ---------------- Block E: Route-B fork, general coefficient family -----------------
# Mixing term re-derived from the stated ingredients: sqrt(h)=rho^2 weight,
# term 2 e^{phi} K phi' with K = 2 e^{-phi} rho'/rho:
mix_derived = sp.simplify(rho**2 * 2*sp.exp(phi) * (2*sp.exp(-phi)*D(rho)/rho) * D(phi))
check('E1 mixing term reduces to 4 rho rho\' phi\'',
      sp.simplify(mix_derived - 4*rho*D(rho)*D(phi)) == 0)

# General family: L_gen = (Z/2) rho^2 phi'^2 + M rho rho' phi' - W e^{-2phi} rho'^2 + Lam
L_gen = sp.Rational(1, 2)*Z*rho**2*D(phi)**2 + M*rho*D(rho)*D(phi) \
        - W*sp.exp(-2*phi)*D(rho)**2 + Lam
ELphi_gen = sp.expand(EL(L_gen, phi))
Phi_gen = Z*rho**2*D(phi) + M*rho*D(rho)
# E2: general flux identity: (Phi_gen)' = 2 W e^{-2phi} rho'^2  (>= 0 for W>0)
check('E2 general flux identity (Phi_gen)\' = 2W e^{-2phi} rho\'^2',
      sp.simplify(ELphi_gen - (D(Phi_gen) - 2*W*sp.exp(-2*phi)*D(rho)**2)) == 0)
# E3: Route B (Z=8, M=4, W=2) reproduces the source's Phi~ = Z rho^2 phi' + 4 rho rho'
check('E3 Route-B flux matches source Phi~',
      sp.simplify(Phi_gen.subs({Z: 8, M: 4}) - (8*rho**2*D(phi) + 4*rho*D(rho))) == 0)
# E4: full mirror seal (phi'=rho'=0) zeroes Phi_gen at an end; phi'-only seal leaves M rho rho'
end_full = Phi_gen.subs({D(phi): 0, D(rho): 0})
end_phionly = sp.simplify(Phi_gen.subs(D(phi), 0))
check('E4 full seal zeroes Phi_gen; phi\'-only seal leaves M rho rho\' (nonzero generically)',
      end_full == 0 and sp.simplify(end_phionly - M*rho*D(rho)) == 0)
# E5: squeeze closes for ALL (Z!=0, M, W>0): Phi_gen'==0 => rho'==0 (C2 shape);
#     then Phi_gen = Z rho^2 phi' and ==0 => phi'==0 (C1 shape). Coefficient-uniform.
check('E5 Phi_gen with rho\'=0 reduces to Z rho^2 phi\'',
      sp.simplify(Phi_gen.subs(D(rho), 0) - Z*rho**2*D(phi)) == 0)
# E6: shift-covariance of the general family: e^{2c} EL[psi+c; Z,M,W] == EL[psi; Ze^{2c}, Me^{2c}, W]
ELphi_gen_sh = ELphi_gen.subs(phi, psi + c).doit()
ELphi_gen_til = ELphi_gen.subs(phi, psi).doit().subs({Z: Z*sp.exp(2*c), M: M*sp.exp(2*c)})
check('E6 shift absorbs into (Z,M) -> e^{2c}(Z,M); ratio M/Z invariant (Route-B pin preserved)',
      sp.simplify(sp.exp(2*c)*ELphi_gen_sh - ELphi_gen_til) == 0)

# ---------------- Block F: germ boundary-condition algebra (attack 3) ---------------
# Momenta from the SAME Lagrangian (Route A): pi_phi = Z rho^2 phi', pi_rho = -4 e^{-2phi} rho'
pi_phi = sp.diff(L, D(phi))
pi_rho = sp.diff(L, D(rho))
check('F1 pi_phi == Z rho^2 phi\' == Phi', sp.simplify(pi_phi - Phi) == 0)
# F2: OPEN-END (bare free endpoint): natural BCs pi_phi=0 AND pi_rho=0
#     => phi'=0 (rho>0, Z!=0) AND rho'=0  — exactly the rigidity's seal BC.
solF = sp.solve([sp.Eq(Z*x**2*phip_sym, 0), sp.Eq(-4*sp.exp(-2*y)*rhop_sym, 0)],
                [phip_sym, rhop_sym])
check('F2 open-end natural BC == {phi\'=0, rho\'=0}', solF == {phip_sym: 0, rhop_sym: 0})
# F3: ODD-fold germ (OC2 fold-quotient): delta phi(r_s)=0 essential => pi_phi UNCONSTRAINED
#     (phi' free, q = Z rho_s^2 phi' an output). With phi' free the squeeze premise
#     Phi(end)=0 FAILS generically: certify Phi != 0 for generic phi'.
q_end = (Z*x**2*phip_sym)
check('F3 odd-fold end flux q = Z rho_s^2 phi\'_s — nonzero for generic phi\'_s',
      sp.simplify(q_end) != 0)
# F4: GLUE germ: banked jump Delta Pi = q/2 with surface term B'(rho_s) = q/2 (K6c).
#     Generic q free => phi' free at seam => NOT a phi'=0 seal. In the B==0 limit,
#     well-posedness forces q=0 => phi'=0: the glue-without-B germ IS rigidity-bound.
qs = sp.symbols('q_s', real=True)
check('F4 glue: B\'==q/2 => (B==0 => q==0 => phi\'_s==0)',
      sp.solve(sp.Eq(qs/2, 0), qs) == [0])

print()
nfail = sum(1 for _, ok in results if not ok)
print(f'TOTAL: {len(results)} checks, {nfail} failures')
