"""Stage-2a CAS (clean) -- off-round pi2 axisymmetric co-relaxed matter. Pointwise symbolic algebra."""
import sympy as sp

# pointwise POSITIVE symbols (no r-derivatives needed for the pointwise stress/EOM-coefficient checks)
rho, s, fr, fth, N, xi, kap = sp.symbols('rho s f_r f_theta N xi kappa', positive=True)
th, f = sp.symbols('theta f', positive=True)
S = sp.sin(th); C = sp.cos(th); sf = sp.sin(f); cf = sp.cos(f)

a = rho**2*sp.exp(s)                 # h_thth
b = rho**2*sp.exp(-s)*S**2           # h_psps
sqrtg = rho**2*S                     # sqrt(g) = sqrt(g_rr a b), g_rr=1  (exact)

# matter densities via INDEPENDENT metric symbols aa,bb (for the Hilbert stress), then substitute
aa, bb = sp.symbols('aa bb', positive=True)
L2 = sp.Rational(1,2)*xi*(fr**2 + fth**2/aa + N**2*sf**2/bb)
L4 = sp.Rational(1,2)*kap*((N*sf*fr)**2/bb + (N*sf*fth)**2/(aa*bb))     # F_rp^2/(grr bb) + F_thp^2/(aa bb)
Lm = L2 + L4
metric = {aa: a, bb: b}

print("=== (3) f Euler-Lagrange coefficients (dens = sqrt(g) L_m) ===")
dens = sqrtg*Lm.subs(metric)
Acoef = sp.simplify(sp.diff(dens, fr)/fr)
Bcoef = sp.simplify(sp.diff(dens, fth)/fth)
pot   = sp.simplify(sp.diff(dens, f))
print("A/f_r =", Acoef)
print("B/f_th=", Bcoef)
print("pot   =", sp.simplify(pot))

A0 = xi*rho**2*S + kap*N**2*sf**2/S
B0 = xi*S + kap*N**2*sf**2/(rho**2*S)
pot0 = (N**2*sf*cf/S)*(xi + kap*fr**2 + kap*fth**2/rho**2)
print("\n(9) ROUND-LIMIT (s=0) f-PDE recovery:")
print("  A/f_r - A0 =", sp.simplify((Acoef - A0).subs(s, 0)))
print("  B/f_th- B0 =", sp.simplify((Bcoef - B0).subs(s, 0)))
print("  pot  - pot0=", sp.simplify((pot - pot0).subs(s, 0)))
print("  off-round A/f_r =", sp.simplify(Acoef), "\n  off-round B/f_th=", sp.simplify(Bcoef))

print("\n=== (4)(5) live shear source + rho^2/2 emergence ===")
dSm_ds = sp.simplify(sp.diff(dens, s))
Ttt = 2*aa*sp.diff(Lm, aa) + Lm
Tpp = 2*bb*sp.diff(Lm, bb) + Lm
Ts  = sp.simplify((Ttt - Tpp).subs(metric))
print("T_s = T^t_t - T^p_p =", Ts)
print("(5) dSm/ds - (rho^2 sin/2) T_s =", sp.simplify(dSm_ds - (rho**2*S/2)*Ts), "   (expect 0)")
Tshear_live = sp.simplify(dSm_ds/S)
print("Tshear_live = dSm/ds/sin = (rho^2/2) T_s =", Tshear_live)

print("\n=== (10) rigid hedgehog: L2-only T_s at s=0,f=theta,N=1 ===")
Ts_L2 = sp.simplify((2*aa*sp.diff(L2, aa) + L2 - 2*bb*sp.diff(L2, bb) - L2).subs(metric))
print("T_s(L2) =", Ts_L2)
print("T_s(L2)|_{s=0,f=theta,N=1} =", sp.simplify(Ts_L2.subs(s, 0).subs(f, th).subs(N, 1)), "(expect 0)")

print("\n=== (4-design-check) design-doc candidate sign ===")
cand_L2 = (xi/rho**2)*(fth**2*sp.exp(-s) - N**2*sf**2*sp.exp(s)/S**2)
print("cand_T_s(L2) + derived T_s(L2) =", sp.simplify(cand_L2 + Ts_L2), " (0 => design SIGN-FLIPPED)")

print("\n=== (6) rho-EOM matter force (pointwise dSm/drho) + round structure ===")
dSm_drho = sp.simplify(sp.diff(dens, rho))
print("dSm/drho =", dSm_drho)
print("dSm/drho (s=0) =", sp.simplify(dSm_drho.subs(s, 0)))
print("  compare per-theta integrand of  xi rho f_r^2 * sin  (I_r) and  -kap N^2 sin^2 f f_th^2/(rho^3 sin) (I_4th/rho^3):")
Ir_ig = xi*rho*fr**2*S            # xi rho * (integrand of I_r=1/2 int sin f_r^2)  -> matches?
I4th_ig = kap*N**2*sf**2*fth**2/(rho**3*S)
print("  dSm/drho(s=0) - [xi rho f_r^2 sin - kap N^2 sin^2 f f_th^2/(rho^3 sin)] =",
      sp.simplify(dSm_drho.subs(s, 0) - (Ir_ig - I4th_ig)))

print("\n=== (7) phi-blindness ===")
phi = sp.symbols('phi')
print("dSm/dphi =", sp.diff(dens, phi), " (0 => matter directly phi-blind; no phi in L_m)")
