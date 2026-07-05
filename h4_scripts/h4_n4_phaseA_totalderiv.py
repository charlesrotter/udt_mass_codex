import sympy as sp
r, th = sp.symbols('r theta', positive=True)

# ---- Claim 1: g1 = d/dr[ -(alpha sin^2 + beta)/(r|sin|) ]  (exact total r-derivative) ----
al = sp.Function('alpha')(r); be = sp.Function('beta')(r); si = sp.Function('sigma')(r)
S = sp.Abs(sp.sin(th)); c2 = sp.sin(th)**2
alp=sp.diff(al,r); bep=sp.diff(be,r); sip=sp.diff(si,r)
g1 = (al*c2 + be - r*(alp*c2 + bep))/(r**2*S)
Pot = -(al*c2 + be)/(r*S)
print("Claim1  g1 - d/dr(Pot) =", sp.simplify(g1 - sp.diff(Pot,r)))

# ---- Build g2 from second Taylor coeff (general perts, fixed theta) ----
a,b,s,av,bv,sv = sp.symbols('a b s av bv sv', real=True)
g = -sp.Rational(1,2)*(av*bv - sv**2)/sp.sqrt(a*b - s**2)
a0=r**2; b0=r**2*sp.sin(th)**2; s0=0; av0=2*r; bv0=sp.diff(b0,r); sv0=0
subs0={a:a0,b:b0,s:s0,av:av0,bv:bv0,sv:sv0}
slots=[a,b,s,av,bv,sv]
alv,bev,siv = al,be,si
pertvals=[alv,bev,siv,alp,bep,sip]
g2=0
for i,(s1,p1) in enumerate(zip(slots,pertvals)):
    for j,(s2,p2) in enumerate(zip(slots,pertvals)):
        g2+=sp.Rational(1,2)*sp.diff(g,s1,s2).subs(subs0)*p1*p2
g2=sp.expand(sp.simplify(g2))

# ---- Reduce INT g2 dr by parts: subtract total derivatives to find irreducible kernel ----
# Strategy: the only non-integrable-to-total-derivative pieces are quadratic in velocities.
# Extract velocity-velocity part (set value-perts' contributions that are total-derivs aside)
# Do it cleanly: integrate g2 - (candidate total deriv) and check residual has no (value*velocity) or (value*value) that isn't itself a boundary term.
# Direct test: compute INT_0^inf g2 dr for a COMPACT test profile numerically-symbolic and compare to
# INT of the bilinear kernel  B = -1/2 (alp*bep - sip**2)/sqrt(a0 b0).
B = -sp.Rational(1,2)*(alp*bep - sip**2)/sp.sqrt(a0*b0)
diff = sp.simplify(g2 - B)
print("\ng2 - bilinearKernel B  (should be a total r-derivative if B is the whole story):")
print(sp.simplify(diff))
