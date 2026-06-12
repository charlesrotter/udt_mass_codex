"""
Route 2 corrected: canonical radial stress h = f' dL/df' - L  (Legendre),
so h_tot = (1/4) y^2 f'^2 - c_n f^n.  Exact identities + closure demands.
"""
import sympy as sp
y, q, lam, w = sp.symbols('y q lambda w', positive=True)
nn = sp.Symbol('n')
s = q*(1-q)/2; f0 = y**(-q); J = -s*y**(-q)
c_n = J*f0**(1-nn)/nn
PASS=0; FAIL=0
def check(name, ez):
    global PASS, FAIL
    ok = sp.simplify(sp.powsimp(sp.expand(ez), force=True)) == 0
    print(("PASS" if ok else "FAIL"), name)
    if ok: PASS+=1
    else: FAIL+=1; print("   residual:", sp.simplify(ez))

F = sp.Function('F')(y)
eom_Fpp = (2*nn*c_n*F**(nn-1) - 2*y*sp.diff(F,y))/y**2   # (1/2)(y^2 f')' = n c_n f^{n-1}

# C4: generic on-shell C1-flux identity:
# d/dy[(1/4) y^2 f'^2] = -(1/2) y f'^2 + c_n (f^n)'      (exchange = c_n (f^n)')
lhs = sp.diff(sp.Rational(1,4)*y**2*sp.diff(F,y)**2, y).subs(sp.diff(F,y,2), eom_Fpp)
rhs = -sp.Rational(1,2)*y*sp.diff(F,y)**2 + c_n*sp.diff(F**nn, y)
check("C4 d/dy[C1 flux] = -(1/2) y f'^2 + c_n (f^n)'  (exact on-shell, all n,q)",
      sp.expand(lhs - rhs))

# C5: total canonical stress h_tot = (1/4)y^2 f'^2 - c_n f^n:
lhs2 = sp.diff(sp.Rational(1,4)*y**2*sp.diff(F,y)**2 - c_n*F**nn, y).subs(sp.diff(F,y,2), eom_Fpp)
rhs2 = -sp.Rational(1,2)*y*sp.diff(F,y)**2 - sp.diff(c_n, y)*F**nn
check("C5 d h_tot/dy = -(1/2) y f'^2 - c_n'(y) f^n  (exact on-shell, all n,q)",
      sp.expand(lhs2 - rhs2))

# C6: closure demand A' (conserved radial stress on the background collar):
leak = sp.powsimp((-sp.Rational(1,2)*y*sp.diff(f0,y)**2 - sp.diff(c_n,y)*f0**nn), force=True)
lc = sp.simplify(leak/y**(-2*q-1))
solA = sp.solve(sp.Eq(lc,0), nn)
print("C6 closure-A' (h_tot conserved): n =", [sp.simplify(v) for v in solA])
nA = solA[0]
check("C6b n_A' = -2(1-q)/q", sp.simplify(nA + 2*(1-q)/q))
print("    at q=1/3: n =", nA.subs(q,sp.Rational(1,3)), " -> nu^2 =",
      sp.nsimplify(17-8*nA.subs(q,sp.Rational(1,3))), "(nu = 7)")

# C7: same demand in the t = ln y frame (the collar's self-similar translation):
t = sp.Symbol('t'); G = sp.Function('G')(t)   # f as function of t
Lt = sp.Rational(1,4)*sp.exp(t)*sp.diff(G,t)**2 + (sp.exp(t)*c_n*F**nn).subs(
        [(F, G), (y, sp.exp(t))])
ht = sp.diff(G,t)*sp.diff(Lt, sp.diff(G,t)) - Lt
dht_explicit = -sp.diff(Lt, t)  # on-shell: dh_t/dt = -dL/dt|explicit
bg = sp.exp(-q*t)
expr = dht_explicit.subs([(sp.diff(G,t), -q*bg), (G, bg)])
expr = sp.powsimp(sp.expand(expr), force=True)
coef = sp.simplify(expr/sp.exp((1-2*q)*t))
solT = sp.solve(sp.Eq(coef,0), nn)
print("C7 closure in t=ln y frame: n =", [sp.simplify(v) for v in solT])
check("C7b t-frame and y-frame closures coincide", sp.simplify(solT[0] - nA))

# C8: closure demand B (source's own density bookkeeping: exchange = d(source density)/dy
#     <=> c_n'(y) f^n = 0 on background):
solB = sp.solve(sp.Eq(sp.simplify(sp.diff(c_n,y)*f0**nn*y**(2*q+1)), 0), nn)
print("C8 closure-B: n =", solB, "-> nu =", [sp.sqrt(17-8*v) for v in solB])

# C9: literal demand 'exchange = the completion's own flux = 0' (ultralocal => no flux):
exch = sp.powsimp(c_n*sp.diff(f0**nn, y), force=True)
print("C9 exchange on background =", sp.simplify(exch), " (n-free, nonzero: NO n closes it)")
check("C9b exchange is n-independent", sp.simplify(sp.diff(exch, nn)))

# C10: additive-normalization freedom b(y): L_src -> c_n f^n + b(y) changes no f-jet,
# shifts h_tot by -b, leak by -b'. Exhibit b for ANY target n:
b0 = sp.Symbol('b0'); b = b0*y**(-2*q)
cond = sp.simplify(lc - sp.diff(b,y)/y**(-2*q-1))
bs = sp.solve(sp.Eq(cond,0), b0)
print("C10 b0(n,q) restoring closure-A' for ANY n:", sp.simplify(bs[0]))
check("C10b residual zero", sp.simplify(cond.subs(b0, bs[0])))
# same freedom breaks it for the would-be selected n:
print("C10c for n = n_A', adding b0=1 breaks closure:",
      sp.simplify(cond.subs([(nn,nA),(b0,1)])) != 0)

print(f"\nConservation leg: {PASS} PASS / {FAIL} FAIL")
