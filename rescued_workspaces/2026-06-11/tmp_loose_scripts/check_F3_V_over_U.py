"""Check structure of V(r)/U(r) and the U slow drift at F3 mid."""
import sys
sys.path.insert(0, "/home/udt-admin/UDT")
import numpy as np
from scipy.ndimage import uniform_filter1d
from lib.scalar import solve as scalar_solve, extract_phi2
from lib.dirac_formT import find_eigenvalues, wavefunction

PHI0 = 0.001
MU = np.sqrt(np.pi/3)
R_STAR = 7.0 - 1.0/80.0
N_STEPS = 4001
R_MIN = 0.1
KAPPA = -1

r, phi, J, phip, ov = scalar_solve(PHI0, R_STAR, N_STEPS, MU, r_min=R_MIN)
phi2 = extract_phi2(r, phi, PHI0)
e2phi = np.exp(2*phi); ephi = np.exp(phi)
evals = find_eigenvalues(KAPPA, r, phip, e2phi, phi0=PHI0, phi2=phi2,
                         E_min=0.1, E_max=400.0, n_scan=40000, n_modes=1500)
E_pick = evals[len(evals)//2]
print(f"F3 mid mode E = {E_pick:.4f}, kappa={KAPPA}")

G, F = wavefunction(E_pick, KAPPA, r, phip, e2phi, ephi, phi0=PHI0, phi2=phi2)
X = G*G + F*F
Y = F*F - G*G
Z = G*F
U = X * np.exp(-2*phi)
V = Y * np.exp(-2*phi)
W = Z * np.exp(-2*phi)

# Smooth over ~one oscillation period
k = 2 * E_pick * np.exp(2*phi)
local_period_pts = 2*np.pi / k / (r[1]-r[0])  # array
print(f"local pts/period: min={local_period_pts.min():.2f} max={local_period_pts.max():.2f}")
win = int(np.ceil(local_period_pts.max())) + 4  # one period

smooth_V = uniform_filter1d(V, size=win, mode='nearest')
smooth_U = uniform_filter1d(U, size=win, mode='nearest')
smooth_W = uniform_filter1d(W, size=win, mode='nearest')

# Show V_smooth / U_smooth at several r
r_lo, r_hi = 0.30*R_STAR, 0.80*R_STAR
mask = (r >= r_lo) & (r <= r_hi)

idxs_show = np.linspace(np.argmax(mask), len(r) - np.argmax(mask[::-1]) - 1, 8).astype(int)
print("\nr        phi       U        smooth_U   smooth_V/smooth_U   2kappa/r * smooth_V")
for i in idxs_show:
    print(f"{r[i]:.3f}   {phi[i]:.4f}   {U[i]:.4e}   {smooth_U[i]:.4e}   "
          f"{smooth_V[i]/smooth_U[i]:+.4e}   {(2*KAPPA/r[i])*smooth_V[i]:+.4e}")

# Now compute U from integrating U' = (2kappa/r) V using both smooth_V and raw V
# Compare to numerical U gradient
Uprime_num = np.gradient(U, r)
Uprime_target = (2*KAPPA/r) * V
relerr_Uprime = np.max(np.abs(Uprime_num[mask] - Uprime_target[mask])) / max(np.max(np.abs(Uprime_target[mask])), 1e-12)
print(f"\nU' identity test:  max rel err |U'_num - (2kappa/r)V| / max|...| = {relerr_Uprime:.4e}")
# But that target oscillates rapidly; let's compute smoothed version
Uprime_smooth_num = np.gradient(smooth_U, r)
target_smooth = (2*KAPPA/r) * smooth_V
print(f"Smoothed U'_target = (2kappa/r) smooth_V at sample r:")
for i in idxs_show:
    print(f"  r={r[i]:.3f}  d(smooth_U)/dr={Uprime_smooth_num[i]:+.4e}  "
          f"(2kappa/r)*smooth_V={target_smooth[i]:+.4e}")

# What's the slow drift in U? Try: U slow obeys U'_slow = (2kappa/r) <V>_slow
# Integrate: U(r) - U(r0) = int (2kappa/r) smooth_V dr
U_pred = smooth_U[idxs_show[0]] + np.cumsum((2*KAPPA/r) * smooth_V * (r[1]-r[0]))
U_pred = U_pred - U_pred[idxs_show[0]] + smooth_U[idxs_show[0]]
print("\nPredicted U from integrating (2kappa/r) smooth_V:")
for i in idxs_show:
    print(f"  r={r[i]:.3f}  smooth_U_actual={smooth_U[i]:.4e}  U_pred={U_pred[i]:.4e}")
