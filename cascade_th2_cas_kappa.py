"""th2 CAS: small-amplitude expansion of the exact per-half-cycle phase
  P + pi = int sqrt(q~/w~) dw over the orbit  (w~ = W/2|s1|, q~ = Q/|s1|)
with  w~ = E + (2dh - 2E) w - (1-3E) w^2 + (c3 - 4E) w^3 + (c4 + 5E) w^4
      q~ = 1 + E (1 - 4w + 10 w^2),      E = eps^2 = Phi^2/(4 Z |s1|),
      dh = dt/|s1| (treated O(E)),  c3 = U'''(1)/(12|s1|), c4 = U''''(1)/(48|s1|).
Output: P = pi[ kA*E + kB*dh + kC*dh^2/E + ... ]  -- the analytic kappa decomposition,
then numeric validation against the exact quadrature.
Also: symbolic U''', U'''' per banked family at the stuck point.
"""
import sympy as sp

E, dh, c3, c4, th = sp.symbols('E dh c3 c4 theta', real=True)
w = sp.Symbol('w', real=True)
eps = sp.Symbol('eps', positive=True)

wt = E + (2*dh - 2*E)*w - (1 - 3*E)*w**2 + (c3 - 4*E)*w**3 + (c4 + 5*E)*w**4
qt = 1 + E*(1 - 4*w + 10*w**2)

# scale: w = eps*W, E = eps^2, dh = d2*eps^2  (d2 = dh/E kept O(1))
d2 = sp.Symbol('d2', real=True)
Wv = sp.Symbol('Wv', real=True)
wt_s = wt.subs({w: eps*Wv, E: eps**2, dh: d2*eps**2})
wt_s = sp.expand(wt_s/eps**2)     # = 1 - Wv^2 + eps*(...) + eps^2*(...)
# roots Wv_pm as series in eps
a1, a2, b1, b2 = sp.symbols('a1 a2 b1 b2')
Wp = 1 + a1*eps + a2*eps**2
Wm = -1 + b1*eps + b2*eps**2
solp = sp.solve([sp.expand(wt_s.subs(Wv, Wp)).coeff(eps, 1),
                 sp.expand(wt_s.subs(Wv, Wp)).coeff(eps, 2)], [a1, a2], dict=True)[0]
solm = sp.solve([sp.expand(wt_s.subs(Wv, Wm)).coeff(eps, 1),
                 sp.expand(wt_s.subs(Wv, Wm)).coeff(eps, 2)], [b1, b2], dict=True)[0]
Wp_ = Wp.subs(solp); Wm_ = Wm.subs(solm)
c_ = sp.expand((Wp_ + Wm_)/2); A_ = sp.expand((Wp_ - Wm_)/2)
# substitute Wv = c + A sin(theta); factor out A^2 cos^2(theta):
Wv_th = c_ + A_*sp.sin(th)
integrand2 = sp.expand(wt_s.subs(Wv, Wv_th))        # w~/eps^2 as function of theta
# h(theta) = wt_s / (A^2 cos^2 th) ; expand in eps. Do it via series:
# write integrand2 = A_^2 cos^2 th * h ; h = integrand2/(A_^2 cos^2 th) -- series safe because
# integrand2 vanishes at th=+-pi/2 by construction (roots) at each eps order.
h = sp.cancel(sp.series(integrand2, eps, 0, 3).removeO() )
h = sp.simplify(h)
cos2 = sp.cos(th)**2
# do polynomial division order by order in eps:
h_ser = sp.Poly(sp.expand(sp.series(integrand2, eps, 0, 3).removeO()), eps)
terms = {k[0]: v for k, v in h_ser.terms()}
# order 0: (1 - sin^2) = cos^2 -> h0 = 1... build h = sum eps^k * (terms[k]/ (A0^2? ) ...)
# A_^2 cos^2 th also has eps-series; easier: h_full = integrand2/(A_**2*cos2), series it with sin->s
s_ = sp.Symbol('s_')
expr = (integrand2/(A_**2*cos2)).subs(sp.sin(th), s_).subs(sp.cos(th)**2, 1-s_**2)
expr_ser = sp.series(sp.together(expr), eps, 0, 3).removeO()
expr_ser = sp.expand(sp.cancel(expr_ser))
# check no 1/(1-s^2) singular leftovers:
h0 = expr_ser.coeff(eps, 0); h1 = expr_ser.coeff(eps, 1); h2 = expr_ser.coeff(eps, 2)
h0s, h1s, h2s = [sp.cancel(sp.factor(x)) for x in (h0, h1, h2)]
print("h0 =", h0s); print("h1 =", h1s); print("h2 =", h2s)

# integrand of P+pi: sqrt(q~)/sqrt(w~) dw ; dw = A cos th dth ; sqrt(w~) = eps*A*cos th*sqrt(h)
# => P+pi = int sqrt(q~ / h) dth,  q~ at w = eps*Wv_th, E=eps^2:
qt_th = qt.subs({w: eps*Wv_th, E: eps**2})
F = sp.sqrt(qt_th/expr_ser.subs(s_, sp.sin(th)))
F_ser = sp.series(F, eps, 0, 3).removeO()
F_ser = sp.expand(sp.simplify(F_ser))
P_plus_pi = sp.integrate(F_ser, (th, -sp.pi/2, sp.pi/2))
P = sp.expand(sp.simplify(P_plus_pi - sp.pi))
P = sp.collect(P, eps)
print("\nP (analytic, to O(eps^2); dh = d2*eps^2):")
sp.pprint(P)
# back-substitute d2 = dh/E, eps^2 = E:
Pfin = sp.simplify(P.subs(d2, dh/E).subs(eps, sp.sqrt(E)))
print("\nP =")
sp.pprint(sp.collect(sp.expand(Pfin), [E, dh]))
