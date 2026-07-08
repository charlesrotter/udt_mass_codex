#!/usr/bin/env python3
"""
OBSERVE test: does UDT's DERIVED redshift law fit Pantheon+ ?

Frozen derived law (from the two founding postulates; data-blind):
    1 + z = 1/(1 - k r),   phi(r) = -ln(1 - k r),   r = areal radius.

Canonical UDT duality (udt_canonical_geometry.md:120,1932-1936):
    D_A = r ;  reciprocity  d_L = D_A (1+z) = r (1+z)   (NO second (1+z); not FLRW).

Closed form:
    1+z = 1/(1-kr)  =>  kr = z/(1+z)  =>  r(z) = z/[k(1+z)]
    d_L(z) = r(z)(1+z) = z/k          <-- STRICTLY LINEAR in z (coasting law)
    mu(z)  = 5 log10(d_L/10pc) = 5 log10(z) + const
  => k is fully degenerate with the magnitude offset; the DERIVED SHAPE is mu = 5 log10(z)+M.

We fit only the single offset (marginalizes k and absolute magnitude M), then score.
Reference models: flat-LCDM (Om=0.3, offset free) and the repo's UDT locked-cubic (0.166 mag).
Diagonal errors used (fast, honest first look); full STAT+SYS covariance noted separately.
"""
import numpy as np

DATA = "/home/udt-admin/UDT/data/Pantheon+SH0ES.dat"
c_km = 299792.458  # km/s

# ---- load ----
with open(DATA) as f:
    header = f.readline().split()
col = {name: i for i, name in enumerate(header)}
rows = [ln.split() for ln in f.readlines() if ln.strip()] if False else None
data = np.genfromtxt(DATA, names=True, dtype=None, encoding=None)

zHD   = data['zHD']
mb    = data['m_b_corr']            # standardized apparent magnitude
mberr = data['m_b_corr_err_DIAG']
iscal = data['IS_CALIBRATOR'].astype(int)

# standard Pantheon+ cosmology cut: drop SH0ES calibrators, keep z>0.01
mask = (iscal == 0) & (zHD > 0.01)
z  = zHD[mask]
m  = mb[mask]
s  = mberr[mask]
w  = 1.0 / s**2
N  = len(z)
print(f"N SNe used (IS_CALIBRATOR==0, zHD>0.01): {N}")

def score(mu_model, label):
    """Fit a single additive offset by weighted least squares; report RMS & chi2/dof."""
    # residual r = m - (mu_model + off); best off = weighted mean of (m - mu_model)
    d = m - mu_model
    off = np.sum(w * d) / np.sum(w)
    resid = d - off
    rms = np.sqrt(np.mean(resid**2))
    wrms = np.sqrt(np.sum(w * resid**2) / np.sum(w))
    chi2 = np.sum(w * resid**2)
    dof = N - 1
    print(f"  [{label}]  offset={off:+.4f}  RMS={rms:.4f} mag  wRMS={wrms:.4f}  "
          f"chi2/dof={chi2/dof:.3f}  ({chi2:.1f}/{dof})")
    return resid, rms, chi2/dof

# ---- Model A: DERIVED UDT law  d_L = z/k  ->  shape mu = 5 log10(z) ----
muA = 5.0 * np.log10(z)          # + const absorbed by offset (== fitting k)
print("\nModel A: UDT DERIVED law  1+z=1/(1-kr)  =>  d_L=z/k  =>  mu=5log10(z)+const")
residA, rmsA, cA = score(muA, "UDT derived (linear d_L)")

# ---- Model B: flat-LCDM reference (Om=0.3), offset absorbs H0 ----
Om = 0.3
def dL_lcdm_over_c_H0(zz):
    # d_L = (1+z) * integral_0^z dz'/E(z'),  in units of c/H0 (offset absorbs it)
    out = np.empty_like(zz)
    for i, zi in enumerate(zz):
        zz_grid = np.linspace(0, zi, 512)
        E = np.sqrt(Om * (1 + zz_grid)**3 + (1 - Om))
        out[i] = (1 + zi) * np.trapz(1.0 / E, zz_grid)
    return out
muB = 5.0 * np.log10(dL_lcdm_over_c_H0(z))   # + const via offset
print("\nModel B: flat-LCDM (Om=0.3), H0 via offset")
residB, rmsB, cB = score(muB, "flat-LCDM Om=0.3")

# ---- Model C: repo UDT locked-cubic (mu_g=0.2473 Gpc^-1), d_L=r*e^phi ----
mu_g = 0.2473
def phi_cubic(r):
    return 1.5*mu_g*r - np.cos(np.pi/5)*mu_g**2*r**2 + (2.0/3.0)*mu_g**3*r**3
# invert z = e^phi -1 for r(z) by bisection
def r_of_z_cubic(zt):
    lo, hi = 0.0, 60.0
    for _ in range(80):
        mid = 0.5*(lo+hi)
        if np.exp(phi_cubic(mid)) - 1.0 < zt: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)
r_c = np.array([r_of_z_cubic(zi) for zi in z])
dL_c = r_c * np.exp(phi_cubic(r_c))          # Gpc
muC = 5.0 * np.log10(dL_c)                    # + const via offset
print("\nModel C: repo UDT locked-cubic (phi = 3/2 mu_g r - cos(pi/5) mu_g^2 r^2 + 2/3 mu_g^3 r^3)")
residC, rmsC, cC = score(muC, "UDT locked-cubic")

# ---- residual trend vs z for the DERIVED law (how it misses, if it does) ----
print("\nDERIVED-law residual (m - model - offset) binned in log10(z):")
lz = np.log10(z)
edges = np.linspace(lz.min(), lz.max(), 9)
for a, b in zip(edges[:-1], edges[1:]):
    mb_ = (lz >= a) & (lz < b)
    if mb_.sum() > 0:
        print(f"  z in [{10**a:.4f},{10**b:.4f}]  n={mb_.sum():4d}  "
              f"mean_resid={np.mean(residA[mb_]):+.4f}  median={np.median(residA[mb_]):+.4f}")

print("\nSUMMARY  (RMS mag / chi2dof):")
print(f"  UDT derived linear d_L=z/k : {rmsA:.4f} / {cA:.3f}")
print(f"  flat-LCDM Om=0.3           : {rmsB:.4f} / {cB:.3f}")
print(f"  UDT locked-cubic (repo)    : {rmsC:.4f} / {cC:.3f}")
