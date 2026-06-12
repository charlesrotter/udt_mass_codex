import sympy as sp
# Does a DIFFERENT normalization measure break the 1/s^2 scaling?
# The Dirac conserved norm on this metric: INT psi^dagger psi sqrt(g_3) ... For metric
# ds^2=-e^{-2phi}dt^2+e^{2phi}dr^2+r^2dOmega^2, the conserved current j^0=psibar gamma^0 psi,
# probability = INT j^0 sqrt(-g)/sqrt(-g_tt) ... let's enumerate candidate measures and their
# scaling weight w(r), test if "Gs(r)=G(r/s)/N(s)" with the corresponding N keeps source ~1/s^2.
s,r,u=sp.symbols('s r u',positive=True)
G=sp.Function('G'); Fn=sp.Function('F'); PHI=sp.Function('PHI')
k=sp.symbols('kappa'); mm=sp.symbols('m',positive=True)

# General: suppose the unit-norm condition is INT W(r)(G^2+F^2)dr=1 with weight W(r) that has
# scaling dimension: under r->s r and a stretched solution, W_s(r)=s^a * W(r/s) for some a.
# Then Gs(r)=G(r/s)/sqrt(N), N=INT W_s Gs0... The amplitude rescale factor is set by N.
# Let's just parametrize: Gs(r) = G(r/s) * c(s), and find c(s) from each candidate measure, then
# check the source scaling.
candidates={
 'flat dr (claim)':        sp.Integer(1),            # W=1
 'e^{PHI} (psibar psi-ish)': sp.exp(PHI(r/s)),       # W=e^{PHI}, scale-invariant field
 'e^{2PHI} (g_rr)':         sp.exp(2*PHI(r/s)),
 'r^2 (volume)':            (r)**2,                  # W=r^2 -> has scaling dim
 'r^2 e^{PHI}':             r**2*sp.exp(PHI(r/s)),
}
c=sp.symbols('c',positive=True)
for nm,Wexpr in candidates.items():
    # norm: INT W * (G_s^2+F_s^2) dr =1 with G_s=c*G(r/s). substitute r=s u:
    # = c^2 * s * INT W(su... ) (G(u)^2+F(u)^2) du... need W expressed.
    Gs=c*G(r/s); Fs=c*Fn(r/s)
    Wsub=Wexpr.subs(r,s*u)
    integrand=(Wsub*(G(u)**2+Fn(u)**2))*s   # dr=s du
    # require = c^2 * s * INT Wsub_in_u (...) du =1; the u-integral's s-dependence:
    # extract s-power of Wsub (treat W(u) integral as O(1))
    # We track the s-scaling of c: c^2 * s * (s-power of Wsub averaged). 
    # For W=1: c^2*s=1 => c=s^{-1/2}. For W=r^2: Wsub=s^2 u^2 => c^2*s*s^2=1 => c=s^{-3/2}. etc.
    sp_pow=sp.Poly(sp.powsimp(Wsub/Wexpr.subs(r,u)) if False else 1,s)  # fallback
    # do it directly: get exponent of s in Wsub relative to W(u)
    # Wsub/W(u):
    Wu=Wexpr.subs(r,u)
    rat=sp.simplify(Wsub/Wu)
    print(f"{nm:26s}: W_sub/W(u) = {rat}", end="  ")
    # solve c: c^2 * s * rat = const (s-indep). 
    # total s-power = 2*log... solve c^2*s*rat = s^0 => 
    spow=sp.simplify(sp.log(rat)/sp.log(s)) if rat.free_symbols=={s} or rat.has(s) else sp.Integer(0)
    # robust: if rat is s^a:
    a=sp.degree(sp.Poly(rat,s)) if rat.is_polynomial(s) and rat!=1 else (0 if rat==1 else None)
    # handle exp(PHI): rat=1 (scale-invariant) since PHI(s u /s)=PHI(u)... check:
    print(" (W with PHI is scale-inv =>rat=1)" if rat==1 else f" a={a}")
