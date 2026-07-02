"""LEMMA D — CAS verification of the two-scale/averaged derivation steps.

System (banked, cell_solver_universe_T3.py, CAS-verified upstream):
  phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
  rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4) U'(rho)
  Phi   = Z rho^2 phi'   (=> Phi' = 4 e^{-2phi} rho'^2 exactly; step 0)
  IC: phi(0)=phi_c=-ln(1101), phi'(0)=0, rho(0)=1, rho'(0)=0
  Seal: phi(r_s)=0 AND rho'(r_s)=0 (the DOUBLE closure), q = Phi(r_s).

Steps verified here (every truncation flagged with its order):
  S0  Phi' identity (EXACT).
  S1  O(eps) linearization  rho=1+u, U'(1+x)=4*dt+4*s1*x  ->
      u'' - 2 phi' u' + k^2 u = S,  k^2=e^{2phi}[(Z/4)phi'^2 - s1],
      S = e^{2phi}[dt - (Z/4) phi'^2].               [TRUNC: O(u^2, dt*u)]
  S2  u = e^{phi} w kills the u' term IDENTICALLY (exact identity;
      w-eq carries k^2 + phi'' - phi'^2).
  S3  WKB envelope: w = kap^{-1/2} cos(int kap) leaves residual
      O(kap''/kap, (kap'/kap)^2) -> u-envelope a = C e^{phi/2} Q^{-1/4},
      Q = (Z/4)phi'^2 - s1  (so k = e^{phi} sqrt(Q)).
      [TRUNC: WKB O((k'/k^2)^2); kap^2 ~ k^2 needs |phi''-phi'^2| << k^2]
  S4  cycle-averaged flux: <Phi'> = 2 a^2 Q.        [TRUNC: drops a'^2/2
      relative a^2 k^2/2, WKB-small; <rho^{-2}>=1+O(a^2)]
  S5  closed slow system in phi:  d(Phi^2)/dphi = 4 Z a^2 Q e_extra...
      with a = C e^{phi/2} Q^{-1/4}:  d(Phi^2)/dphi = 4 Z C^2 sqrt(Q) e^{phi}
      Q ~= |s1|  [TRUNC: relative (Z/4)phi'^2/|s1|, measured <~1% at seal]
      ->  Phi^2 = 4 Z C^2 sqrt(|s1|) (e^{phi} - x_c),  x_c=e^{phi_c}=1/1101
      (Phi(phi_c)=0 exact from phi'(0)=0; ramp pre-onset flux folded in,
       checked numerically in lemD_reshoot.py).
  S6  phase integral: Theta = int_0^{r_s} k dr
      = sqrt(Z)|s1|^{1/4} sqrt(1-x_c) / C            [same TRUNC as S5]
  S7  assemble:
      q      = Phi(phi=0) = 2 sqrt(Z) C |s1|^{1/4} sqrt(1-x_c)
             = 2 Z sqrt(|s1|) (1-x_c) / Theta
      a_seal = C Q_s^{-1/4}  (e^{phi_s/2}=1)
      R1:  a_seal = q / (2 sqrt(Z (1-x_c)) (|s1| Q_s)^{1/4})   [launch-free]
      R2:  a_seal = sqrt(Z (1-x_c)) (|s1|/Q_s)^{1/4} / Theta   [phase law]
      s1-CANCELLATION: in R2, |s1| survives ONLY inside (|s1|/Q_s)^{1/4}
      = (1 + (Z/4)phi_s'^2/|s1|)^{-1/4} = 1 + O(0.2%..1%): a_seal ~ sqrt(Z)/Theta.
  S8  consistency with EXACT Theorem B: U(rho_s)=2-q^2/(2 Z rho_s^2)
      expanded to O(delta^2) reproduces R1's leading term
      |rho_s-1| ~ q/(2 rho_s sqrt(Z |s1|)) -- i.e. the averaged route
      rederives Theorem B at O(eps) AND adds the q-equation (S7),
      which Theorems A/B leave as an unevaluated shape integral.
  S9  family constants, exact in d: dt(d)=U'(1)/4, s1(d)=U''(1)/4 for
      A1(m), A2(k=3), A3 at param = stuck*(1-d).
"""
import sympy as sp

r = sp.Symbol('r')
Z, s1, dt, C, xc = sp.symbols('Z s1 dt C x_c', positive=True)  # s1 here = |s1| where noted
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
u = sp.Function('u')(r)
w = sp.Function('w')(r)

ok = lambda name, expr: print(f"  [{'PASS' if expr else 'FAIL'}] {name}")

print("S0: Phi' = 4 e^{-2phi} rho'^2 (EXACT)")
phipp = 4*sp.exp(-2*phi)*rho.diff(r)**2/(Z*rho**2) - 2*phi.diff(r)*rho.diff(r)/rho
Phi = Z*rho**2*phi.diff(r)
Phip = Phi.diff(r).subs(phi.diff(r, 2), phipp)
ok("Phi' identity", sp.simplify(Phip - 4*sp.exp(-2*phi)*rho.diff(r)**2) == 0)

print("S1: linearization — EXACT once U' is truncated linearly (only TRUNC: U''' u^2/2)")
s1s = sp.Symbol('s1s')  # signed s~1
rho_lin = 1 + u
Up_lin = 4*dt + 4*s1s*u                     # U'(1+u) = 4 dt + 4 s1 u + O(u^2)  <- the ONE truncation
rhopp_full = (2*phi.diff(r)*rho_lin.diff(r)
              - sp.Rational(1, 4)*Z*rho_lin*sp.exp(2*phi)*phi.diff(r)**2
              + sp.exp(2*phi)/4*Up_lin)
k2 = sp.exp(2*phi)*(Z*phi.diff(r)**2/4 - s1s)
S = sp.exp(2*phi)*(dt - Z*phi.diff(r)**2/4)
resid1 = sp.expand(rho_lin.diff(r, 2) - rhopp_full
                   - (u.diff(r, 2) - 2*phi.diff(r)*u.diff(r) + k2*u - S))
ok("u''-2phi'u'+k^2 u = e^{2phi}[dt-(Z/4)phi'^2]  (EXACT given linear-U')",
   sp.simplify(resid1) == 0)

print("S2: u = e^{phi} w elimination (EXACT identity)")
u_sub = sp.exp(phi)*w
expr = u_sub.diff(r, 2) - 2*phi.diff(r)*u_sub.diff(r) + (k2 + 0)*u_sub
kap2 = k2 + phi.diff(r, 2) - phi.diff(r)**2
ok("u''-2phi'u'+k^2u == e^{phi}[w'' + (k^2+phi''-phi'^2) w]",
   sp.simplify(expr - sp.exp(phi)*(w.diff(r, 2) + kap2*w)) == 0)

print("S3: WKB residual for w = kap^{-1/2} cos(int kap)  (TRUNC order shown)")
kap = sp.Function('kappa', positive=True)(r)
th = sp.Symbol('theta')
# w = kap^{-1/2} cos(theta), theta' = kap; compute w'' + kap^2 w
wf = kap**sp.Rational(-1, 2)*sp.cos(sp.Integral(kap, r).doit())  # symbolic: do by hand
# manual: w'' + kap^2 w = kap^{-1/2} cos(th) * [ (3/4)(kap'/kap)^2 - kap''/(2 kap) ]
# verify by direct differentiation with theta as an antiderivative
theta = sp.Function('theta')(r)
wexp = kap**sp.Rational(-1, 2)*sp.cos(theta)
wpp = wexp.diff(r, 2).subs({theta.diff(r, 2): kap.diff(r), theta.diff(r): kap})
resid3 = sp.simplify(wpp + kap**2*wexp)
expected3 = kap**sp.Rational(-1, 2)*sp.cos(theta)*(sp.Rational(3, 4)*(kap.diff(r)/kap)**2
                                                   - kap.diff(r, 2)/(2*kap))
ok("residual = w * [(3/4)(kap'/kap)^2 - kap''/(2 kap)]  (WKB TRUNC O((kap'/kap^2)^2))",
   sp.simplify(resid3 - expected3) == 0)

print("S4: cycle average <u'^2> with u=a cos(theta), theta'=k  (TRUNC: a'^2 term)")
a_, k_ = sp.symbols('a k', positive=True)
thv = sp.Symbol('theta')
up = -a_*k_*sp.sin(thv)   # + a' cos(theta), dropped: TRUNC O((a'/ak)^2), WKB-small
avg = sp.integrate(up**2, (thv, 0, 2*sp.pi))/(2*sp.pi)
ok("<u'^2> = a^2 k^2 / 2", sp.simplify(avg - a_**2*k_**2/2) == 0)
# => <Phi'> = 4 e^{-2phi} <u'^2> = 2 a^2 e^{-2phi} k^2 = 2 a^2 Q   [by k^2 = e^{2phi} Q]

print("S5: closed slow system  (TRUNC: Q ~= |s1|, rel err (Z/4)phi'^2/|s1|)")
phv = sp.Symbol('phi')
Y = sp.Function('Y')(phv)   # Y = Phi^2
# dY/dphi = 2 Phi Phi'/phi' = 2 Z rho^2 <Phi'> ~= 2 Z * 2 a^2 Q ; a^2 = C^2 e^{phi} Q^{-1/2}
# => dY/dphi = 4 Z C^2 e^{phi} sqrt(Q) ~= 4 Z C^2 sqrt(s1) e^{phi}   (s1 = |s1| here)
sol = sp.dsolve(sp.Eq(Y.diff(phv), 4*Z*C**2*sp.sqrt(s1)*sp.exp(phv)), Y,
                ics={Y.subs(phv, sp.log(xc)): 0})
Y_sol = sol.rhs
ok("Phi^2 = 4 Z C^2 sqrt|s1| (e^phi - x_c)",
   sp.simplify(Y_sol - 4*Z*C**2*sp.sqrt(s1)*(sp.exp(phv) - xc)) == 0)

print("S6: phase integral Theta = int k dr = int k * (Z rho^2/Phi) dphi  (rho~1: O(a))")
Phi_of_phi = sp.sqrt(Y_sol)
k_of_phi = sp.exp(phv)*sp.sqrt(s1)          # Q ~= |s1|, same TRUNC as S5
integrand = k_of_phi*Z/Phi_of_phi
Theta = sp.integrate(integrand, (phv, sp.log(xc), 0))
Theta_expected = sp.sqrt(Z)*s1**sp.Rational(1, 4)*sp.sqrt(1 - xc)/C
ok("Theta = sqrt(Z) |s1|^{1/4} sqrt(1-x_c) / C",
   sp.simplify(sp.powsimp(Theta - Theta_expected, force=True)) == 0)

print("S7: assemble q, a_seal, R1, R2 + s1-cancellation")
Qs = sp.Symbol('Q_s', positive=True)
q_expr = sp.sqrt(Y_sol.subs(phv, 0))                       # q = Phi(0)
a_seal = C*Qs**sp.Rational(-1, 4)                          # e^{phi_s/2}=1
R1 = q_expr/(2*sp.sqrt(Z*(1 - xc))*(s1*Qs)**sp.Rational(1, 4))
ok("R1: a_seal == q/(2 sqrt(Z(1-x_c)) (|s1| Q_s)^{1/4})",
   sp.simplify(sp.powsimp(R1 - a_seal, force=True)) == 0)
Theta_sym = sp.Symbol('Theta', positive=True)
C_of_Theta = sp.sqrt(Z)*s1**sp.Rational(1, 4)*sp.sqrt(1 - xc)/Theta_sym
R2 = (C_of_Theta*Qs**sp.Rational(-1, 4)).rewrite(sp.Pow)
print("    R2: a_seal =", sp.simplify(R2), "  -> s1 survives ONLY as (|s1|/Q_s)^{1/4}")
ok("R2 s1-cancellation: d(a_seal)/d(s1) == 0 when Q_s -> s1 (phi'_s -> 0 limit)",
   sp.simplify(R2.subs(Qs, s1).diff(s1)) == 0)
q_of_Theta = sp.simplify(q_expr.subs(C, C_of_Theta))
print("    q(Theta) =", sp.powsimp(q_of_Theta, force=True), "  [q Theta = 2 Z sqrt|s1| (1-x_c)]")

print("S8: Theorem B (EXACT) expanded reproduces R1 leading term")
d_ = sp.Symbol('delta_s')
rho_s = 1 + d_
U_exp = 2 + 4*dt*d_ + 2*s1s*d_**2          # U(1)=2, U'(1)=4dt, U''(1)=4s1  + O(d^3) TRUNC
q2 = sp.Symbol('q', positive=True)**2
thmB = sp.Eq(U_exp, 2 - q2/(2*Z*rho_s**2))
# leading (dt -> 0, rho_s -> 1 in the q-term, s1s = -|s1|):
lead = sp.solve(thmB.subs({dt: 0, s1s: -s1}).subs(rho_s, 1), d_**2)
print("    delta_s^2 =", lead, " -> |rho_s-1| ~ q/(2 sqrt(Z |s1|))  [matches R1 head]")

print("S9: exact family constants dt(d), s1(d)")
rr, dd = sp.symbols('rho d', positive=True)
fams = {}
for m in (2, 3, 4):
    a = sp.Rational(m, 2)*(1 - dd)
    U = 2*rr**m*sp.exp(-a*(rr**2 - 1))
    fams[f"A1m{m}"] = U
U = 2*rr**2*sp.exp(-sp.Rational(2, 3)*(1 - dd)*(rr**3 - 1)); fams["A2k3"] = U
b = 1 - dd
U = 2*rr**2*(1 + b)/(1 + b*rr**4); fams["A3"] = U
for name, U in fams.items():
    dt_d = sp.simplify(U.diff(rr).subs(rr, 1)/4)
    s1_d = sp.simplify(U.diff(rr, 2).subs(rr, 1)/4)
    print(f"    {name}:  dt(d) = {dt_d}    s1(d) = {sp.expand(s1_d)}")
