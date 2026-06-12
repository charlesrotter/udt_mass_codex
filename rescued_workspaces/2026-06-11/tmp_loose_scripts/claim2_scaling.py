import sympy as sp
# Scaling argument. Transformation: r -> s*r, m -> m/s, keeping m*r fixed. E -> E/s (mass-like).
# A unit-normalized mode under r->s*r: INT(G^2+F^2)dr=1. If we define rescaled functions
# Gs(r)=G(r/s)/sqrt(s) so that INT Gs^2 dr=1, etc.
# We must check each term of source = -2 sigma[ k(F^2-G^2)/r + PHI'(F^2+F^2) + m e^PHI GF ]
# scales as 1/s^2 (like the LHS vacuum operator phi''+2phi'/r-2phi'^2).

s = sp.symbols('s', positive=True)
# Under r->s r: phi is dimensionless (scale-invariant field), phi(r)->phi(r/s) for a stretched solution.
# LHS operator: phi''+2phi'/r-2phi'^2. With phi_s(r)=phi(r/s):
r=sp.symbols('r',positive=True)
phi=sp.Function('phi')
phi_s=phi(r/s)
LHS=sp.diff(phi_s,r,2)+2*sp.diff(phi_s,r)/r-2*sp.diff(phi_s,r)**2
# evaluate at r-> compare with original at u=r/s
u=sp.symbols('u',positive=True)
LHS_sub=LHS.subs(r,s*u)
LHS0=(sp.diff(phi(u),u,2)+2*sp.diff(phi(u),u)/u-2*sp.diff(phi(u),u)**2)
print("LHS(stretched)/LHS0 at u=r/s :", sp.simplify(LHS_sub/LHS0), " (expect 1/s^2)")

# RHS source terms. Unit-norm mode: Gs(r)=G(r/s)/sqrt(s). Then INT Gs^2 dr = INT G(u)^2 du =1. good.
# term1: k(Fs^2-Gs^2)/r  with PHI scale-invariant (PHIs(r)=PHI(r/s)), PHIp_s(r)=PHIp(r/s)/s
G=sp.Function('G'); Fn=sp.Function('F'); PHI=sp.Function('PHI')
Gs=G(r/s)/sp.sqrt(s); Fs=Fn(r/s)/sp.sqrt(s)
PHIs=PHI(r/s); PHIps=sp.diff(PHIs,r)
mm=sp.symbols('m',positive=True); k=sp.symbols('kappa')
# rescaled mass m->m/s
term1=k*(Fs**2-Gs**2)/r
term2=PHIps*(Fs**2+Gs**2)
term3=(mm/s)*sp.exp(PHIs)*Gs*Fs
for nm,term,orig in [("k(F^2-G^2)/r",term1, k*(Fn(u)**2-G(u)**2)/u),
                     ("PHI'(F^2+G^2)",term2, sp.diff(PHI(u),u)*(Fn(u)**2+G(u)**2)),
                     ("m e^PHI GF",term3, mm*sp.exp(PHI(u))*G(u)*Fn(u))]:
    sub=term.subs(r,s*u)
    ratio=sp.simplify(sub/orig)
    print(f"  {nm:18s}: scaled/orig = {ratio}  (expect 1/s^2 = s^-2)")
