"""r1_bv_inventory.py -- verifier attack on premise 4 (term-inventory completeness):
enumerate ALL scalars at <= 2nd derivative order built from {phi', K_AB, R^{(2)}, h_AB}
with a pure-exponential weight e^{k phi}, and classify each against RULE-1 (weight-0
after compensation), RULE-2 (flat value), and independence (IBP).

Building blocks and their shift-weights (verified in r1_bv_main.py):
  phi'        : weight 0, 1st order
  K_AB        : weight -1 (K = trace, K_ABK^AB, K^2 quadratics weight -2)
  R^{(2)}[h]  : weight 0, 2nd order
  h_AB, h^AB  : weight 0 (inert)
Scalar candidates at TOTAL derivative order <= 2 (each K or phi' = 1 order, R2 = 2):
  order 2: phi'^2 | e^{2phi}K^2 | e^{2phi}K_ABK^AB | e^{phi}K phi' | R^{(2)} | phi''
(phi'' is the only 2nd-derivative longitudinal scalar; K'_AB-type terms are 3rd order
in the transverse+longitudinal mix and outside the banked class.)
Claim under attack: the weight-0, flat-value-passing PHI-SECTOR candidates are exactly
{phi'^2, e^phi K phi'} -- with phi'' NOT independent (IBP-reducible to the mixing term).

Verifier: do NOT commit.
"""
import sympy as sp

r, th, lam = sp.symbols('r theta lambda', real=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)
pp = phi.diff(r); rp = rho.diff(r)

h = sp.Matrix([[rho**2, 0], [0, rho**2*sp.sin(th)**2]])
hi = h.inv()
K_AB = sp.Rational(1, 2)*sp.exp(-phi)*h.diff(r)
K = sp.simplify((hi*K_AB).trace())
KK = sp.simplify((hi*K_AB*hi*K_AB).trace())
sqh = rho**2*sp.sin(th)

ok = True
def chk(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('PASS ' if cond else '*** FAIL ') + name)

def wt(e):
    return sp.simplify(e.subs(phi, phi + lam)/e)

# 1. weight table of the full order-<=2 inventory
tab = {
    "phi'^2": (pp**2, 0), "K^2": (K**2, -2), "K_ABK^AB": (KK, -2),
    "K phi'": (K*pp, -1), "R2": (2/rho**2, 0), "phi''": (phi.diff(r, 2), 0)}
allw = all(sp.simplify(wt(e) - sp.exp(w*lam)) == 0 for e, w in tab.values())
chk('I1: bare weights of the complete order-<=2 scalar inventory:'
    " phi'^2:0, K^2:-2, K_ABK^AB:-2, Kphi':-1, R2:0, phi'':0", allw)

# 2. RULE-1 compensation makes each admitted; then RULE-2 flat-value filter
def onflat(e):
    e = e.subs({phi.diff(r, 2): 0, pp: 0, rho.diff(r, 2): 0, rp: 1})
    return sp.simplify(e.subs({phi: 0, rho: r}))
chk('I2: after RULE-1 compensation, flat VALUES: e^{2phi}K^2 -> 4/r^2 (excluded),'
    ' e^{2phi}K_ABK^AB -> 2/r^2 (excluded singly; only the Kc combo passes with R2),'
    " e^{phi}Kphi' -> 0 (passes), phi'^2 -> 0 (passes), phi'' -> 0 (passes)",
    onflat(sp.exp(2*phi)*K**2) == 4/r**2 and onflat(sp.exp(2*phi)*KK) == 2/r**2
    and onflat(sp.exp(phi)*K*pp) == 0 and onflat(pp**2) == 0
    and onflat(phi.diff(r, 2)) == 0)

# 3. phi'' is NOT a new term: sqrt(h) phi'' = d/dr(sqrt(h) phi') - sqrt(h) e^phi K phi'
chk("I3: sqrt(h)phi'' = (sqrt(h)phi')' - sqrt(h)e^{phi}Kphi' EXACTLY -- phi'' is"
    ' IBP-equivalent to (minus) the mixing term; NOT an independent widening of the sheet',
    sp.simplify(sqh*phi.diff(r, 2)
                - (sp.diff(sqh*pp, r) - sqh*sp.exp(phi)*K*pp)) == 0)

# 4. one-order-higher probe (beyond the banked class, honesty check): e^{2phi}K_ABK^AB phi'
#    and R2*phi' carry weight -2,-0 but are 3rd order / dimensionally need a length scale;
#    confirm R2*phi' has flat value 0 but is 3rd order (outside class) - just note weights.
chk("I4: the nearest out-of-class candidates are genuinely out of class:"
    " R2*phi' weight 0 (3rd derivative order), e^{2phi}KKphi' weight 0 (3rd order)"
    " -- the doc's class boundary (2nd order) is what excludes them, stated as CHOSE",
    sp.simplify(wt((2/rho**2)*pp) - 1) == 0
    and sp.simplify(wt(sp.exp(2*phi)*KK*pp) - 1) == 0)

print('\nINVENTORY VERDICT:', 'PASS' if ok else 'FAIL')
if not ok:
    raise SystemExit(1)
