import sympy as sp
s,u,r=sp.symbols('s u r',positive=True)
k=sp.symbols('kappa'); m=sp.symbols('m',positive=True)
G=sp.Function('G'); F=sp.Function('F'); PHI=sp.Function('PHI')

# stretched mode: Gtil(r)=c*G(r/s), PHItil(r)=PHI(r/s), m_til=m/s.
# source_til(r) = -2(-1)[ k(Ft^2-Gt^2)/r + PHIt'(Ft^2+Gt^2) + (m/s)e^{PHIt} Gt Ft ]
c=sp.symbols('c',positive=True)
Gt=c*G(r/s); Ft=c*F(r/s)
PHIt=PHI(r/s); PHItp=sp.diff(PHIt,r)
src_til = 2*( k*(Ft**2-Gt**2)/r + PHItp*(Ft**2+Gt**2) + (m/s)*sp.exp(PHIt)*Gt*Ft )
# original source at u:
src_u   = 2*( k*(F(u)**2-G(u)**2)/u + sp.diff(PHI(u),u)*(F(u)**2+G(u)**2) + m*sp.exp(PHI(u))*G(u)*F(u) )
# substitute r=s u in src_til and form ratio:
src_til_u = src_til.subs(r,s*u)
ratio = sp.simplify(src_til_u / src_u)
print("source_til(su)/source(u) =", ratio, "   [with c the amplitude factor]")
print()
# Now plug each measure's c:
for nm,cval in [('W=1 / e^{PHI} (c=s^-1/2)', s**sp.Rational(-1,2)),
                ('W=r^2 (c=s^-3/2)',         s**sp.Rational(-3,2))]:
    rr=sp.simplify(ratio.subs(c,cval))
    print(f"  {nm:28s}: source ratio = {rr}")
    print(f"      -> term-by-term? source has factor c^2/s-structure. expected 1/s^2 means ratio=s^-2.")
