"""Diagnostic: examine U(r) = X(r) e^{-2 phi(r)} at F3 mid-spectrum mode."""
import sys
sys.path.insert(0, "/home/udt-admin/UDT")
import numpy as np
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
print(f"phi range: [{phi.min():.4f}, {phi.max():.4f}]  dphi = {phi.max()-phi.min():.4f}")

evals = find_eigenvalues(KAPPA, r, phip, e2phi, phi0=PHI0, phi2=phi2,
                         E_min=0.1, E_max=400.0, n_scan=40000, n_modes=1500)
print(f"Found {len(evals)} modes; E range [{evals[0]:.3f}, {evals[-1]:.3f}]")

# Take mid mode
E_pick = evals[len(evals)//2]
print(f"\nMid mode E = {E_pick:.4f}")

G, F = wavefunction(E_pick, KAPPA, r, phip, e2phi, ephi, phi0=PHI0, phi2=phi2)
X = G*G + F*F
U = X * np.exp(-2*phi)

# Examine: at fit window 0.30..0.80 * r_star, what is U doing?
r_lo, r_hi = 0.30*R_STAR, 0.80*R_STAR
mask = (r >= r_lo) & (r <= r_hi)
print(f"\nFit window r in [{r_lo:.3f}, {r_hi:.3f}], {mask.sum()} points")
print(f"U over window: min={U[mask].min():.4e} max={U[mask].max():.4e} mean={U[mask].mean():.4e}")
print(f"U_max/U_min = {U[mask].max()/U[mask].min():.4f}")
print(f"log_U range = {np.log(U[mask].max())-np.log(U[mask].min()):.4f}")

# Smooth log U with running mean over many oscillations
from scipy.ndimage import uniform_filter1d
log_U = np.log(U)
win_pts = 100  # roughly 1 oscillation period at k=440 has 2pi/440/dr = 0.014/0.0017 = ~8 pts
smooth_log_U = uniform_filter1d(log_U, size=win_pts, mode='nearest')

# Fit smoothed log_U vs phi over window
slope_raw, intc_raw = np.polyfit(phi[mask], log_U[mask], 1)
slope_smooth, intc_smooth = np.polyfit(phi[mask], smooth_log_U[mask], 1)
print(f"\nRaw fit slope of log_U vs phi: {slope_raw:.4f}  -> alpha = 2 + slope = {2+slope_raw:.4f}")
print(f"Smoothed (running mean win={win_pts}) fit slope: {slope_smooth:.4f} -> alpha = {2+slope_smooth:.4f}")

# Show a few sample U values
print(f"\nSample U(r) values across fit window:")
idxs = np.linspace(np.argmax(mask), len(r) - np.argmax(mask[::-1]) - 1, 6).astype(int)
for i in idxs:
    print(f"  r={r[i]:.3f}  phi={phi[i]:.4f}  X={X[i]:.4e}  U={U[i]:.4e}  log(U)={np.log(U[i]):.4f}")

# Also check: what is X behaving like? Should grow like e^{2 phi}.
slope_X, intc_X = np.polyfit(phi[mask], np.log(X[mask]), 1)
print(f"\nFit slope log(X) vs phi (= alpha_fit): {slope_X:.4f}")

# Compute average slope on smoothed log_X
log_X = np.log(X)
smooth_log_X = uniform_filter1d(log_X, size=win_pts, mode='nearest')
slope_X_smooth, _ = np.polyfit(phi[mask], smooth_log_X[mask], 1)
print(f"Fit slope of smoothed log(X) vs phi: {slope_X_smooth:.4f}")

# Pull out k(r) and check WKB momentum
k = 2 * E_pick * np.exp(2*phi)
print(f"\nk(r) over window: min={k[mask].min():.2f} max={k[mask].max():.2f}")
print(f"local wavelength: min={2*np.pi/k[mask].max():.5f} max={2*np.pi/k[mask].min():.5f}")
print(f"grid dr = {r[1]-r[0]:.5f}")
print(f"points per wavelength: min={2*np.pi/k[mask].max()/(r[1]-r[0]):.2f}")
