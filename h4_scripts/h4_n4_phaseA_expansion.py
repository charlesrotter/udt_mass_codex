import sympy as sp

# ============================================================
# PHASE A: O(amplitude^2) expansion of the net-flux integrand
#   source density  D = sqrt(h) K = -1/2 e^{-2phi} (a'b'-s'^2)/sqrt(ab-s^2)
#   (per d theta d psi ; primes = d/dr ; a=h_thth, b=h_pspsi, s=h_thpsi)
# Frame C(a): pull e^{-2phi0} out as constant prefactor 'w0' over the
#   localized core (ambient slowly varying). Compute geometric part.
# Expand about round ambient a0=r^2, b0=r^2 sin^2 th, s0=0.
# ============================================================
r, th = sp.symbols('r theta', positive=True)
# independent algebraic slots: values a,b,s and velocities av,bv,sv
a,b,s,av,bv,sv = sp.symbols('a b s av bv sv', real=True)

g = -sp.Rational(1,2)*(av*bv - sv**2)/sp.sqrt(a*b - s**2)   # geometric density (e^{-2phi0} pulled out)

# background values
a0 = r**2
b0 = r**2*sp.sin(th)**2
s0 = sp.Integer(0)
av0 = sp.diff(a0,r)   # 2r
bv0 = sp.diff(b0,r)   # 2r sin^2
sv0 = sp.Integer(0)

# perturbation symbols (functions of r,theta): alpha=da, beta=db, sigma=ds
# and their r-derivatives ap,bp,cp  (velocity perturbations)
al,be,si = sp.symbols('alpha beta sigma', real=True)     # value perts
alp,bep,sip = sp.symbols('alpha_p beta_p sigma_p', real=True)  # velocity perts (d/dr of perts)

subs0 = {a:a0,b:b0,s:s0,av:av0,bv:bv0,sv:sv0}
slots = [a,b,s,av,bv,sv]
perts = [al,be,si,alp,bep,sip]

# first order
g1 = 0
for slot,p in zip(slots,perts):
    g1 += sp.diff(g,slot).subs(subs0)*p
g1 = sp.simplify(g1)

# second order (1/2 Hessian contraction)
g2 = 0
for i,(s1,p1) in enumerate(zip(slots,perts)):
    for j,(s2,p2) in enumerate(zip(slots,perts)):
        g2 += sp.Rational(1,2)*sp.diff(g,s1,s2).subs(subs0)*p1*p2
g2 = sp.simplify(g2)

print("="*70)
print("FIRST-ORDER geometric density g1 (per dth dpsi):")
sp.pprint(g1)
print()
print("SECOND-ORDER geometric density g2:")
g2c = sp.simplify(sp.expand(g2))
sp.pprint(g2c)
print()

# ---- angular integral over psi (0..2pi) trivial (perts indep of psi if axisym) times dtheta.
# For the MONOPOLE net flux we need  dG = integral over (theta,psi) of (g1 or g2).
# First check: is g1 a total r-derivative in the sense that INT g1 dtheta dpsi dr = 0?
# N2 claim: the shape pieces are total r-derivatives. Let's test by checking whether
# INT_theta g1 (with psi->2pi factor) equals d/dr of something for arbitrary alpha,beta.
# We treat alpha,beta,sigma as INDEPENDENT functions of r (drop theta-dep for the ell=0 test won't work;
# keep general). Instead: verify the standard N2 linear result form.

# Substitute the ambient explicitly and simplify g1:
print("="*70)
print("g1 fully simplified (ambient substituted):")
print(g1)
