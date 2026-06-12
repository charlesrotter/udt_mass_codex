"""F1 low-mode (sub-barrier ground state E~1) check at convergence."""
import sys
sys.path.insert(0, "/home/udt-admin/UDT")
import numpy as np
from scipy.optimize import brentq
from lib.scalar import solve as scalar_solve, extract_phi2
from lib.dirac_formT import shoot, wavefunction, find_eigenvalues, gpu_scan

PHI0 = -float(np.cos(np.pi / 5))
MU = np.sqrt(np.pi / 3)
R_STAR = 7.0 - 1.0 / 80.0
R_MIN = 0.1
KAPPA = -1

for n_steps in [4001, 8001, 16001]:
    r, phi, J, phip, ov = scalar_solve(PHI0, R_STAR, n_steps, MU, r_min=R_MIN)
    phi2 = extract_phi2(r, phi, PHI0)
    e2phi = np.exp(2 * phi); ephi = np.exp(phi)
    # Find ground state E_1 (lowest eigenvalue, expected ~0.943 for Branch-M)
    evals = find_eigenvalues(KAPPA, r, phip, e2phi, phi0=PHI0, phi2=phi2,
                              E_min=0.1, E_max=20.0, n_scan=20000, n_modes=5)
    if not evals:
        print(f'N={n_steps}: no evals')
        continue
    # First (sub-barrier) and second (super-barrier) mode
    for idx, E_pick in enumerate(evals[:3]):
        G, F = wavefunction(E_pick, KAPPA, r, phip, e2phi, ephi,
                             phi0=PHI0, phi2=phi2)
        X = G*G + F*F
        U = X * np.exp(-2*phi)
        r_lo, r_hi = 0.30*R_STAR, 0.80*R_STAR
        mask = (r >= r_lo) & (r <= r_hi)
        log_U_swing = float(np.log(U[mask].max()) - np.log(U[mask].min()))
        # alpha fit
        alpha, _ = np.polyfit(phi[mask], np.log(X[mask]), 1)
        # IBP bound
        g = 2*KAPPA/r; k = 2*E_pick*np.exp(2*phi)
        gok = g/k
        gok_prime = np.gradient(gok, r)
        bound_boundary = 2.0 * float(np.max(np.abs(gok[mask])))
        bound_integral = float(np.trapezoid(np.abs(gok_prime[mask]), r[mask]))
        bound_total = bound_boundary + bound_integral
        # Min k in window
        k_in = k[mask]
        print(f'N={n_steps:5d}  mode_idx={idx}  E={E_pick:.6f}  '
              f'log_U_swing={log_U_swing:.4e}  IBP_bound={bound_total:.4e}  '
              f'obs/bound={log_U_swing/bound_total:.3f}  '
              f'k_min={k_in.min():.3f} k_max={k_in.max():.3f}  alpha={alpha:+.4f}',
              flush=True)
