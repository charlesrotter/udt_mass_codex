import sympy as sp
r, th = sp.symbols('r theta', positive=True)
al = sp.Function('alpha'); be = sp.Function('beta'); si = sp.Function('sigma')
A=al(r); Bb=be(r); Sg=si(r)
Ap=sp.diff(A,r); Bp=sp.diff(Bb,r); Sp=sp.diff(Sg,r)
Sn=sp.sin(th); Sa=sp.Abs(Sn); c2=Sn**2

# g2 (from before), fixed theta:
g2 = (2*r*A*c2*Ap + 2*r*A*Bp + 2*r*Bb*Ap + 2*r*Bb*Bp/c2
      - 3*A**2*c2 - 2*A*Bb - 3*Bb**2/c2 - 4*Sg**2
      + 2*r**2*Sp**2 - 2*r**2*Ap*Bp )/(4*r**4*Sa)
# NOTE: reconstruct full g2 = residual + B ; B = -1/2(Ap*Bp - Sp^2)/sqrt(a0 b0), sqrt(a0 b0)=r^2 Sa
B = -sp.Rational(1,2)*(Ap*Bp - Sp**2)/(r**2*Sa)
g2full = sp.simplify( ( (2*r*A*c2*Ap + 2*r*A*Bp + 2*r*Bb*Ap + 2*r*Bb*Bp/c2
      - 3*A**2*c2 - 2*A*Bb - 3*Bb**2/c2 - 4*Sg**2)/(4*r**4*Sa) ) + B )
print("recon check g2full - g2 =", sp.simplify(g2full - g2))

# Integrate value*velocity terms by parts:  f(values)*v  ->  -Integral( d/dr[f] * (value) ) essentially
# We want INT g2 dr in a total-derivative-free ("EL/Beltrami") form.
# Use: the variational (Euler-Lagrange) operator kills total r-derivatives.
# So irreducible content of INT g2 dr is captured by testing EL derivatives w.r.t alpha,beta,sigma.
def EL(L, f):
    fr=sp.diff(f,r)
    return sp.diff(L,f) - sp.diff(sp.diff(L,fr), r)
for name,f in [('alpha',A),('beta',Bb),('sigma',Sg)]:
    e=sp.simplify(EL(g2,f))
    print(f"EL_{name}[g2] =", e)
