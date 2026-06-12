"""Smarter F3 resolution scan: find one eigenvalue near E=200, examine U(r) drift."""
import sys
sys.path.insert(0, "/home/udt-admin/UDT")
import numpy as np
from scipy.optimize import brentq
from lib.scalar import solve as scalar_solve, extract_phi2
from lib.dirac_formT import shoot, wavefunction

PHI0 = 0.001
MU = np.sqrt(np.pi / 3)
R_STAR = 7.0 - 1.0 / 80.0
R_MIN = 0.1
KAPPA = -1

E_target = 200.0

for n_steps in [4001, 8001, 16001, 32001]:
    r, phi, J, phip, ov = scalar_solve(PHI0, R_STAR, n_steps, MU, r_min=R_MIN)
    phi2 = extract_phi2(r, phi, PHI0)
    e2phi = np.exp(2 * phi); ephi = np.exp(phi)
    # Bracket: do small coarse scan near 200 (window 195-205)
    E_lo = 195.0
    E_hi = 205.0
    n_brac = 200
    E_scan = np.linspace(E_lo, E_hi, n_brac)
    from lib.dirac_formT import gpu_scan
    bc = gpu_scan(E_scan, KAPPA, r, phip, e2phi, phi0=PHI0, phi2=phi2)
    # find first sign change
    E_pick = None
    for i in range(len(bc) - 1):
        if np.isfinite(bc[i]) and np.isfinite(bc[i+1]) and bc[i]*bc[i+1] < 0:
            E_pick = brentq(lambda E: shoot(E, KAPPA, r, phip, e2phi,
                                              phi0=PHI0, phi2=phi2)[0],
                             E_scan[i], E_scan[i+1], xtol=1e-10)
            break
    if E_pick is None:
        print(f"N={n_steps}: no E_pick in [{E_lo},{E_hi}]")
        continue
    G, F = wavefunction(E_pick, KAPPA, r, phip, e2phi, ephi,
                         phi0=PHI0, phi2=phi2)
    X = G*G + F*F
    Y = F*F - G*G
    Z = G*F
    U = X * np.exp(-2*phi)
    V = Y * np.exp(-2*phi)
    r_lo, r_hi = 0.30*R_STAR, 0.80*R_STAR
    mask = (r >= r_lo) & (r <= r_hi)
    log_U_swing = float(np.log(U[mask].max()) - np.log(U[mask].min()))
    # alpha fit
    alpha, _ = np.polyfit(phi[mask], np.log(X[mask]), 1)
    # Direct numerical integral of (2 kappa/r) cos Theta dr
    integrand = (2*KAPPA/r) * (V / U)
    direct_int = float(np.trapezoid(integrand[mask], r[mask]))
    # IBP bound
    g = 2*KAPPA/r; k = 2*E_pick*np.exp(2*phi)
    gok = g/k
    gok_prime = np.gradient(gok, r)
    bound_boundary = 2.0 * float(np.max(np.abs(gok[mask])))
    bound_integral = float(np.trapezoid(np.abs(gok_prime[mask]), r[mask]))
    bound_total = bound_boundary + bound_integral
    # Identity test
    Uprime_num = np.gradient(U, r)
    Uprime_target = (2*KAPPA/r) * V
    relerr_Uprime = float(np.max(np.abs(Uprime_num[mask] - Uprime_target[mask])) /
                           max(np.max(np.abs(Uprime_target[mask])), 1e-12))
    print(f'N={n_steps:5d}  dr={(r[1]-r[0])*1e4:6.2f}e-4  E_pick={E_pick:.6f}  '
          f'log_U_swing={log_U_swing:+.4e}  trap_int={direct_int:+.4e}  '
          f'IBP_bound={bound_total:.4e}  alpha={alpha:+.4f}  Uprime_relerr={relerr_Uprime:.3e}',
          flush=True)
