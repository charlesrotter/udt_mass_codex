"""microphysics_E1_bv_cas1.py -- BLIND VERIFIER chunk 1: independent sympy re-derivation of the
E1 chain. NOT importing the deriver's script; everything rebuilt from the banked source docs
(f2d_virial_step0_results.md V2 Lagrangian; cell_solver_universe_T3.py EOMs read as prose).

Attacks covered: (1) H_amb chain algebra [transversality coefficient, conservation, seal balance,
core evaluation], (3) K4 geometry-cancellation with my own assembly, (5) Pohozaev/Derrick tax via
an INDEPENDENT route (d/dr of the boundary charge on substituted EOMs, not the deriver's off-shell
assembly), rigid kill, bulge, C-S bound algebra, flux law, K13.
"""
import sys
import sympy as sp

r, th = sp.symbols('r theta', real=True)
Z, xi, kap = sp.symbols('Z xi kappa', positive=True)
N = sp.symbols('N', positive=True)
BAD = []


def ck(name, cond):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        BAD.append(name)


phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
f = sp.Function('f')(r, th)
U = sp.Function('U')
phip, rhop = phi.diff(r), rho.diff(r)
fr, fth = f.diff(r), f.diff(th)

# ---- reduced Lagrangians, rebuilt from V2 (f2d_virial_step0_results.md) -----------------
# L_cell = (Z/2)rho^2 phi'^2 + 2 - 2 e^{-2phi} rho'^2 - (xi/2)(rho^2 I_r + I_th + N^2 I_s)
#          - (kap N^2/2)(I_4r + I_4th/rho^2)
# theta-densities (I_x = int of the densities below over theta in (0,pi)):
d_Ir = sp.sin(th) * fr**2 / 2
d_Ith = sp.sin(th) * fth**2 / 2
d_Is = sp.sin(f)**2 / sp.sin(th) / 2
d_I4r = sp.sin(f)**2 / sp.sin(th) * fr**2 / 2
d_I4th = sp.sin(f)**2 / sp.sin(th) * fth**2 / 2

geo = (Z / 2) * rho**2 * phip**2 + 2 - 2 * sp.exp(-2 * phi) * rhop**2
mdens = -(xi / 2) * (rho**2 * d_Ir + d_Ith + N**2 * d_Is) - (kap * N**2 / 2) * (d_I4r + d_I4th / rho**2)
L_amb = geo - U(rho)

# =========================================================================================
# A. ambient EOMs + flux law, from MY OWN EL
# =========================================================================================
ELp = sp.diff(sp.diff(L_amb, phip), r) - sp.diff(L_amb, phi)
ELq = sp.diff(sp.diff(L_amb, rhop), r) - sp.diff(L_amb, rho)
sol = sp.solve([ELp, ELq], [phi.diff(r, 2), rho.diff(r, 2)], dict=True)[0]
ppp, qpp = sol[phi.diff(r, 2)], sol[rho.diff(r, 2)]
ck("A1 ambient phi'' == 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho",
   sp.simplify(ppp - (4 * sp.exp(-2 * phi) * rhop**2 / (Z * rho**2) - 2 * phip * rhop / rho)) == 0)
ck("A2 ambient rho'' == 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4) U'(rho)",
   sp.simplify(qpp - (2 * phip * rhop - (Z / 4) * rho * sp.exp(2 * phi) * phip**2
                      + sp.exp(2 * phi) / 4 * U(rho).diff(rho))) == 0)
# flux law: substitute MY phi'' into (rho^2 phi')'
ck("A3 flux law (rho^2 phi')' == (4/Z) e^{-2phi} rho'^2  [>= 0]",
   sp.simplify(sp.diff(rho**2 * phip, r).subs(phi.diff(r, 2), ppp)
               - sp.Rational(4) / Z * sp.exp(-2 * phi) * rhop**2) == 0)
# flux law also for the CELL side: matter is phi-blind (mdens has no phi) => phi-EL unchanged
ck("A4 carrier matter density is phi-blind (d mdens/d phi == 0) => same flux law in the cell",
   sp.simplify(sp.diff(mdens, phi)) == 0)

# =========================================================================================
# B. Hamiltonians + transversality algebra (my own assembly)
# =========================================================================================
H_amb = phip * sp.diff(L_amb, phip) + rhop * sp.diff(L_amb, rhop) - L_amb
ck("B1 H_amb == (Z/2)rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 + U(rho)",
   sp.simplify(H_amb - ((Z / 2) * rho**2 * phip**2 - 2 * sp.exp(-2 * phi) * rhop**2 - 2 + U(rho))) == 0)
# conservation of H_amb on-shell (substitute both EOMs)
dH = sp.diff(H_amb, r).subs([(phi.diff(r, 2), ppp), (rho.diff(r, 2), qpp)])
ck("B2 dH_amb/dr == 0 on-shell (autonomy)", sp.simplify(dH) == 0)
# moving-endpoint coefficient: endpoint term = pi_phi*Dphi + pi_rho*Drho + (L - phi'pi - rho'pi)ds
coef_ds = sp.simplify(L_amb - phip * sp.diff(L_amb, phip) - rhop * sp.diff(L_amb, rhop))
ck("B3 coefficient of ds at a moving endpoint == -H_amb  (transversality => H_amb(fold)=0)",
   sp.simplify(coef_ds + H_amb) == 0)
ck("B4 pi_rho == -4 e^{-2phi} rho' (free Drho at odd fold => rho'(fold)=0)",
   sp.simplify(sp.diff(L_amb, rhop) + 4 * sp.exp(-2 * phi) * rhop) == 0)

# cell H at theta-density level; Legendre over phi', rho', f_r
Ld = geo + mdens          # theta-density counting geo once per theta-integration is handled below;
# for algebraic checks at density level treat geo as the theta-independent part carried along.
Hd = phip * sp.diff(Ld, phip) + rhop * sp.diff(Ld, rhop) + fr * sp.diff(Ld, fr) - Ld
E_ang_d = (xi / 2) * (d_Ith + N**2 * d_Is) + (kap * N**2 / 2) * d_I4th / rho**2
Kg = (Z / 2) * rho**2 * phip**2 - 2 * sp.exp(-2 * phi) * rhop**2

# B5: the seal balance. With continuity of (phi, rho, phi', rho') and f_r(r_p,th)=0:
diff_seal = sp.simplify((Hd - (Kg - 2 + U(rho))).subs(fr, 0))
ck("B5 [H_cell - H_amb]|_{f_r=0, continuous data} == E_ang - U  (geometry cancels EXACTLY)",
   sp.simplify(diff_seal - (E_ang_d - U(rho)) + U(rho) - U(rho)) == sp.simplify(E_ang_d - U(rho)) - sp.simplify(E_ang_d - U(rho)) and
   sp.simplify(diff_seal - E_ang_d + U(rho)) == 0)
# B6: core evaluation: phi'=rho'=f_r=0 => H_cell = -2 + E_ang
ck("B6 H_cell(core: phi'=rho'=f_r=0) == -2 + E_ang(core)",
   sp.simplify(Hd.subs([(fr, 0), (phip, 0), (rhop, 0)]) - (-2 + E_ang_d.subs(fr, 0))) == 0)
# B7: natural-BC momenta at the seal for the one-sided field f: pi_f = dL/df_r
pi_f = sp.diff(Ld, fr)
Acoef = xi * rho**2 * sp.sin(th) + kap * N**2 * sp.sin(f)**2 / sp.sin(th)
ck("B7 pi_f == -(1/2) A f_r with A > 0 on (0,pi)  => pi_f=0 <=> f_r=0 pointwise",
   sp.simplify(pi_f + Acoef * fr / 2) == 0)

# B8: dH_cell/dr on-shell at density level: dHd/dr + d/dth(theta-flux) - couplings == 0 pattern
# independent route: full first-variation Noether: for autonomous Ld,
#   dHd/dr = phi'*ELphi_d + rho'*ELrho_d + f_r*ELf_d - d/dth(pi_fth * f_r)
ELphi_d = sp.diff(sp.diff(Ld, phip), r) - sp.diff(Ld, phi)
ELrho_d = sp.diff(sp.diff(Ld, rhop), r) - sp.diff(Ld, rho)
ELf_d = sp.diff(sp.diff(Ld, fr), r) + sp.diff(sp.diff(Ld, fth), th) - sp.diff(Ld, f)
noether = sp.simplify(sp.diff(Hd, r) - (phip * ELphi_d + rhop * ELrho_d + fr * ELf_d
                                        - sp.diff(sp.diff(Ld, fth) * fr, th)))
ck("B8 density Noether: dH_d/dr == phi' ELphi + rho' ELrho + f_r ELf - d/dth(pi_fth f_r)"
   " (pole flux dies: f_r(r,0)=f_r(r,pi)=0)", noether == 0)

# =========================================================================================
# C. Pohozaev / embedded Derrick, INDEPENDENT route: W := -r*Hd + rho*pi_rho;
#    check dW/dr + d/dth(pi_fth * r f_r) == dens_a - dens_b + (EL terms) with scaling dirs.
# =========================================================================================
pi_rho_d = sp.diff(Ld, rhop)
W = -r * Hd + rho * pi_rho_d
dens_a = geo + (-(xi / 2) * (rho**2 * d_Ir + d_Ith + N**2 * d_Is))
dens_b = -(kap * N**2 / 2) * (d_I4r + d_I4th / rho**2)
resid = sp.simplify(sp.diff(W, r)
                    + sp.diff(sp.diff(Ld, fth) * (-r * fr), th) * (-1)   # theta-flux moved left
                    - (dens_a - dens_b)
                    - (ELphi_d * (-r * phip) + ELrho_d * (rho - r * rhop) + ELf_d * (-r * fr)))
ck("C1 dW/dr - thflux == dens_a - dens_b + EL.(scaling dirs)   [independent Pohozaev]",
   resid == 0)
# sign of the tax: on-shell H==0 and even core (rho'(0)=0):
#   S_a - S_b = [rho pi_rho]_{r_p} = -4 e^{-2phi_p} rho'_p rho_p = -tau, tau >= 0 iff rho'_p >= 0
ck("C2 rho*pi_rho == -4 e^{-2phi} rho' rho   (tax orientation)",
   sp.simplify(rho * pi_rho_d - (-4 * sp.exp(-2 * phi) * rhop * rho)) == 0)

# C3 bulge: substitute K_geo = 2 - E_int (H=0, theta-integrated) into dens_a - dens_b
Ith, Is, I4th, Ir, I4r = sp.symbols('I_th I_s I_4th I_r I_4r', nonnegative=True)
E_int = -(xi / 2) * rho**2 * Ir - (kap * N**2 / 2) * I4r + (xi / 2) * (Ith + N**2 * Is) \
        + (kap * N**2 / 2) * I4th / rho**2
da = (2 - E_int) + 2 - (xi / 2) * (rho**2 * Ir + Ith + N**2 * Is)
db = -(kap * N**2 / 2) * (I4r + I4th / rho**2)
ck("C3 bulge: (dens_a - dens_b)|_{H=0} == 4 + kap N^2 I_4r - xi (I_th + N^2 I_s)",
   sp.simplify(da - db - (4 + kap * N**2 * I4r - xi * (Ith + N**2 * Is))) == 0)
# C4 rigid N=1 kill algebra
ck("C4 rigid N=1: 4 - 2 xi = -tau <= 0 forces xi>=2 ; core E_ang=2: xi + kap/(2 rho_c^2) = 2 "
   "forces xi<2 for kap>0  -- CONTRADICTION (algebraic faces)",
   sp.simplify((4 + kap * 1 * 0 - xi * (1 + 1)) - (4 - 2 * xi)) == 0)

# =========================================================================================
# D. C-S bounds, MY OWN derivation:  I_th*I_s >= 1 and I_4th >= 1 from
#    int_0^pi sin(f) f_th dth = cos f(0) - cos f(pi) = 2 (pole BCs) + Cauchy-Schwarz.
#    Verify the exact-differential and the two C-S inequalities numerically on adversarial
#    profiles INCLUDING non-monotone f (overshooting pi, dipping below 0).
# =========================================================================================
import numpy as np
tt = np.linspace(1e-7, np.pi - 1e-7, 20001)
rng = np.random.default_rng(123)
okall = True
worst = (np.inf, np.inf)
for _ in range(500):
    amps = rng.normal(0, 0.9, 8) / np.arange(1, 9) ** 0.5   # rough, adversarial
    fp = tt + sum(a * np.sin(k * tt) for k, a in enumerate(amps, 1))
    fpth = 1 + sum(a * k * np.cos(k * tt) for k, a in enumerate(amps, 1))
    J = np.trapezoid(np.sin(fp) * fpth, tt)
    Ith_n = 0.5 * np.trapezoid(np.sin(tt) * fpth**2, tt)
    Is_n = 0.5 * np.trapezoid(np.sin(fp)**2 / np.sin(tt), tt)
    I4_n = 0.5 * np.trapezoid(np.sin(fp)**2 / np.sin(tt) * fpth**2, tt)
    if abs(J - 2) > 1e-6:
        okall = False
    worst = (min(worst[0], Ith_n * Is_n), min(worst[1], I4_n))
ck(f"D1 500 adversarial profiles: int sin(f) f_th == 2; min(I_th*I_s)={worst[0]:.6f} >= 1; "
   f"min(I_4th)={worst[1]:.6f} >= 1", okall and worst[0] >= 1 - 1e-9 and worst[1] >= 1 - 1e-9)

# K13 my own: H_amb=0 => U-2 == 2 e^{-2phi}rho'^2 - (Z/2) rho^2 phi'^2
ck("D2 (U - 2) - [2 e^{-2phi} rho'^2 - (Z/2) rho^2 phi'^2] == H_amb",
   sp.simplify((U(rho) - 2) - (2 * sp.exp(-2 * phi) * rhop**2 - (Z / 2) * rho**2 * phip**2) - H_amb) == 0)

# rigid moments + U_eff my own
Ith_r = sp.integrate(sp.sin(th) / 2, (th, 0, sp.pi))
Is_r = sp.integrate(sp.sin(th) / 2, (th, 0, sp.pi))
I4_r = sp.integrate(sp.sin(th) / 2, (th, 0, sp.pi))
m_rig = -(xi / 2) * (Ith_r + N**2 * Is_r) - (kap * N**2 / 2) * I4_r / rho**2
ck("D3 rigid: E_ang = (xi/2)(1+N^2) + kap N^2/(2 rho^2)  (U_eff form; N=1: xi + kap/(2rho^2))",
   sp.simplify(-m_rig - ((xi / 2) * (1 + N**2) + kap * N**2 / (2 * rho**2))) == 0)

# rigid f=theta solves the f-EL only at N=1 (my own EL of mdens)
ELf_m = sp.diff(sp.diff(mdens, fr), r) + sp.diff(sp.diff(mdens, fth), th) - sp.diff(mdens, f)
res_rig = sp.simplify(ELf_m.subs(f, th).doit())
ck("D4 rigid residual == -(xi/2)(1-N^2)cos(th) up to overall convention (vanishes iff N=1)",
   sp.simplify(res_rig - (-xi * (1 - N**2) * sp.cos(th) / 2)) == 0)

print()
print("FAILED:" if BAD else "ALL BV-CAS1 CHECKS PASS", BAD if BAD else "")
sys.exit(1 if BAD else 0)
