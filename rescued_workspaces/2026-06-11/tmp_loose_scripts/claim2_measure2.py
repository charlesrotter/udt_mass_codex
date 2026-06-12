import sympy as sp
# Clean setup. Original mode: G(u),F(u),PHI(u) solves the system at scale 1, normalized by
#   INT W[PHI,u](G^2+F^2) du = 1.
# Stretched mode at scale s: define functions at radius r as
#   Gtil(r) = c(s) G(r/s),  Ftil(r)=c(s) F(r/s),  PHItil(r)=PHI(r/s)   (phi scale-invariant field)
#   with rescaled m_til = m/s  (and E_til=E/s).
# c(s) is FIXED by requiring the stretched mode is unit-normed in the SAME measure:
#   INT W[PHItil,r] (Gtil^2+Ftil^2) dr = 1.
# Then evaluate source_til(r) and compare to source(u=r/s): is source_til = source/s^2 ?
s = sp.symbols('s', positive=True)
u = sp.symbols('u', positive=True)
# Represent PHI by a generic scale-invariant profile; use a concrete analytic one to be safe.
a0=sp.Rational(1,2)
PHIf=lambda x: a0*sp.exp(-(x-3)**2)
G=sp.Function('G'); F=sp.Function('F')
k=sp.symbols('kappa'); m=sp.symbols('m',positive=True)

def source_at(Gx,Fx,PHIx,PHIpx,mass,x):
    return -2*(-1)*( k*(Fx**2-Gx**2)/x + PHIpx*(Fx**2+Gx**2) + mass*sp.exp(PHIx)*Gx*Fx )

measures = {
 'W=1 (flat dr, claim)':   lambda x,Px: 1,
 'W=e^{PHI}':              lambda x,Px: sp.exp(Px),
 'W=e^{2PHI} (g_rr)':      lambda x,Px: sp.exp(2*Px),
 'W=r^2 (3-volume)':       lambda x,Px: x**2,
 'W=r^2 e^{PHI}':          lambda x,Px: x**2*sp.exp(Px),
}
r=sp.symbols('r',positive=True)
for nm,Wf in measures.items():
    # norm at scale1: I1 = INT W(u,PHI(u)) (G^2+F^2) du.  We only need the s-scaling of c.
    # stretched: Gtil(r)=c G(r/s); norm = c^2 INT W(r,PHI(r/s))(G(r/s)^2+F(r/s)^2) dr
    #   sub r=s u, dr=s du: = c^2 s INT W(s u, PHI(u)) (G^2+F^2) du.
    # The s-dependence enters only via W(s u, PHI(u))/W(u,PHI(u)).
    Wsu = Wf(s*u, PHIf(u))     # W evaluated at radius s*u, with PHI=PHI(u) (since PHItil(su)=PHI(u))
    Wu  = Wf(u,   PHIf(u))
    rat = sp.simplify(Wsu/Wu)  # the per-point s-factor (under integral)
    # If rat = s^p (const power), then c^2 s * s^p = 1 => c = s^{-(1+p)/2}.
    # find p:
    pexp = sp.simplify(sp.diff(sp.log(rat), s)*s)  # = p if rat=s^p
    print(f"{nm:24s}: W(su)/W(u) = {rat} ,  power p(s) = {sp.simplify(pexp)}")
