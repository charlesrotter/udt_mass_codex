"""microphysics_E0_bv_H_adversarial.py -- BLIND VERIFIER attack 2 on the H_amb == 0 claim.

(a) analytic: sympy proof that for the T3 reduced system
      Lbar = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2 - U(rho)
    (i)  the EL equations of Lbar are EXACTLY the T3 EOMs (doc header lines 19-20),
    (ii) H = phi' pi_phi + rho' pi_rho - Lbar (the DOC corner form,
         embedded_cell_closure_H_amb_results.md:29) equals the E0 expression
         (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 + U(rho),
    (iii) dH/dr == 0 ON-SHELL (autonomy / conservation),
    (iv) H(0) = U(rho_c) - 2  ->  = 0 iff the transversality closure U(rho_c)=2.
(b) numeric vacuity test: the EXACT E0 H expression evaluated on
    (1) a deliberately PERTURBED (non-solution) profile  -> must read NONZERO,
    (2) an OFF-CLOSURE exact solution (U scaled by 1.02, so U(rho_c)=2.04)
        -> H must be CONSERVED at +0.04, NOT 0
    (proves the E0 column is a real functional, zero only because of the closure).
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

LN1101 = float(np.log(1101.0))
PHI_C = -LN1101

# ---------------------------------------------------------------- (a) sympy
r = sp.symbols('r')
Z = sp.symbols('Z', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
Ufun = sp.Function('U')
Pp, Rp = phi.diff(r), rho.diff(r)

Lbar = sp.Rational(1, 2) * Z * rho**2 * Pp**2 - 2 * sp.exp(-2 * phi) * Rp**2 + 2 - Ufun(rho)

# EL equations
EL_phi = sp.diff(sp.diff(Lbar, Pp), r) - sp.diff(Lbar, phi)
EL_rho = sp.diff(sp.diff(Lbar, Rp), r) - sp.diff(Lbar, rho)
# T3 EOMs (doc lines 19-20), as residuals phi'' - RHS, rho'' - RHS:
sigma = sp.exp(2 * phi) / 4 * Ufun(rho).diff(rho)
eom_phi = phi.diff(r, 2) - (4 * sp.exp(-2 * phi) * Rp**2 / (Z * rho**2) - 2 * Pp * Rp / rho)
eom_rho = rho.diff(r, 2) - (2 * Pp * Rp - sp.Rational(1, 4) * Z * rho * sp.exp(2 * phi) * Pp**2 + sigma)

# (i) EL_phi should be Z rho^2 * eom_phi ; EL_rho should be -4 e^{-2phi} * eom_rho
chk1 = sp.simplify(EL_phi - Z * rho**2 * eom_phi)
chk2 = sp.simplify(EL_rho - (-4 * sp.exp(-2 * phi)) * eom_rho)
print("(i)  EL(Lbar) == T3 EOMs:", chk1 == 0 and chk2 == 0, f"  (residuals: {chk1}, {chk2})")

# (ii) doc corner form == E0 expression
pi_phi = sp.diff(Lbar, Pp)
pi_rho = sp.diff(Lbar, Rp)
H_doc = Pp * pi_phi + Rp * pi_rho - Lbar
H_E0 = sp.Rational(1, 2) * Z * rho**2 * Pp**2 - 2 * sp.exp(-2 * phi) * Rp**2 - 2 + Ufun(rho)
print("(ii) H_doc(q'pi - Lbar) == H_E0 expr:", sp.simplify(H_doc - H_E0) == 0)
print("     pi_phi == Z rho^2 phi' (q-flux):", sp.simplify(pi_phi - Z * rho**2 * Pp) == 0)
print("     pi_rho == -4 e^{-2phi} rho'    :", sp.simplify(pi_rho + 4 * sp.exp(-2 * phi) * Rp) == 0)

# (iii) dH/dr on-shell
dH = sp.diff(H_E0, r)
sub = {phi.diff(r, 2): sp.solve(eom_phi, phi.diff(r, 2))[0],
       rho.diff(r, 2): sp.solve(eom_rho, rho.diff(r, 2))[0]}
print("(iii) dH/dr on-shell == 0 (autonomy):", sp.simplify(dH.subs(sub)) == 0)

# (iv) H at the even fold ICs
H_fold = H_E0.subs({Pp: 0, Rp: 0})
print("(iv) H(fold: phi'=rho'=0) =", sp.simplify(H_fold), " -> 0 iff U(rho_c)=2 (transversality closure)")

# ---------------------------------------------------------------- (b) numeric vacuity
def sl_A1(m, a, scale=1.0):
    def U(x):  return scale * 2.0 * x**m * np.exp(-a * (x * x - 1.0))
    def Up(x): return U(x) * (m / x - 2.0 * a * x)
    return U, Up


def rhs_f(Zv, Up):
    def f(t, y):
        p, pp, R, Rp_ = y
        e2p = np.exp(2.0 * p)
        return (pp, 4.0 * Rp_**2 / (e2p * Zv * R * R) - 2.0 * pp * Rp_ / R,
                Rp_, 2.0 * pp * Rp_ - 0.25 * Zv * R * e2p * pp * pp + 0.25 * e2p * Up(R))
    return f


def H_E0_expr(Zv, U, p, pp, R, Rp_):
    """EXACT expression from microphysics_E0_extract.py line 185."""
    e2p = np.exp(2.0 * p)
    return 0.5 * Zv * R**2 * pp**2 - 2.0 * Rp_**2 / e2p - 2.0 + U(R)


Zv = 8.0
a_star = 1.4813439682566742
U, Up = sl_A1(3.0, a_star)
seal = lambda t, y: y[0]; seal.terminal, seal.direction = True, +1
sol = solve_ivp(rhs_f(Zv, Up), (0.0, 1e6), [PHI_C, 0.0, 1.0, 0.0], method="DOP853",
                rtol=1e-11, atol=1e-13, events=[seal], dense_output=True)
r_s = float(sol.t_events[0][0])
rr = np.linspace(0, r_s, 3001)
p, pp, R, Rp_ = sol.sol(rr)
H_true = H_E0_expr(Zv, U, p, pp, R, Rp_)
print(f"\n[b0] true solution:            max|H| = {np.max(np.abs(H_true)):.3e}  (expect ~1e-10)")

# (b1) perturbed NON-solution profiles fed to the SAME expression
pert = 0.05 * np.sin(np.pi * rr / r_s)
H_p1 = H_E0_expr(Zv, U, p, pp, R + pert, Rp_)
H_p2 = H_E0_expr(Zv, U, p + pert, pp, R, Rp_)
H_p3 = H_E0_expr(Zv, U, p, pp + 0.01 * np.sin(np.pi * rr / r_s), R, Rp_)
print(f"[b1] perturbed rho (+0.05 sin): max|H| = {np.max(np.abs(H_p1)):.3e}  (must be >> 1e-10)")
print(f"     perturbed phi (+0.05 sin): max|H| = {np.max(np.abs(H_p2)):.3e}")
print(f"     perturbed phi'(+0.01 sin): max|H| = {np.max(np.abs(H_p3)):.3e}")

# (b2) OFF-CLOSURE exact solution: U -> 1.02*U  =>  U(1) = 2.04, transversality closure broken
U2, Up2 = sl_A1(3.0, a_star, scale=1.02)
sol2 = solve_ivp(rhs_f(Zv, Up2), (0.0, 1e6), [PHI_C, 0.0, 1.0, 0.0], method="DOP853",
                 rtol=1e-11, atol=1e-13, events=[seal], dense_output=True)
tend = float(sol2.t_events[0][0]) if sol2.t_events[0].size else float(sol2.t[-1])
rr2 = np.linspace(0, tend, 3001)
p2, pp2, R2, Rp2 = sol2.sol(rr2)
H_off = H_E0_expr(Zv, U2, p2, pp2, R2, Rp2)
print(f"[b2] off-closure solution (U(1)=2.04): H in [{np.min(H_off):.6f}, {np.max(H_off):.6f}]"
      f"  (expect conserved at +0.04, NOT 0; drift {np.max(H_off)-np.min(H_off):.2e})")
