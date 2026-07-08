#!/usr/bin/env python3
"""
OBSERVE test: does UDT's HOMOGENEOUS FREED-TRANSVERSE law fit Pantheon+ ?

Prior test (sne_test_derived_law.py): the radial-only derived law with the
transverse geometry FROZEN to D_A = r gave d_L = z/k (strictly linear), which
is falsely too shallow at high z (0.28 mag RMS, ~1 mag ramp).

Now FREE the transverse geometry and derive it from the SAME homogeneity
postulate: a homogeneous space has CONSTANT SPATIAL CURVATURE, which fixes the
areal radius D_A as a function of PROPER distance Δs.

Derivation (data-blind shapes):
  redshift law           1+z = e^{k·Δs}   =>   Δs = (1/k) ln(1+z)  = u/k,  u≡ln(1+z)
  constant-curvature D_A(Δs):
      FLAT   : D_A = Δs
      OPEN   : D_A = (1/κ) sinh(κ·Δs)          (negative curvature)
      CLOSED : D_A = (1/κ) sin (κ·Δs)          (positive curvature)
  UDT static duality (udt_canonical_geometry.md §12.8, ~line 1932):
      d_L = D_A·(1+z)   (ONE power of (1+z), NOT FLRW's two)

=> luminosity-distance forms (a ≡ κ/k, the ONLY dimensionless shape param; k = offset):
      FLAT   : d_L = (1+z)·u / k                          (parameter-free shape)
      OPEN   : d_L ∝ (1+z)·sinh(a·u)/a                    (fit a)
      CLOSED : d_L ∝ (1+z)·sin (a·u)/a                    (fit a)
  a→0 limit: sinh(au)/a, sin(au)/a → u, both reduce to FLAT (verified below).
  low-z FLAT: d_L=(1+z)ln(1+z)/k ≈ (z+z²/2)/k  (curvature sanity check).

Same loader / cuts / scoring as the VALIDATED sne_test_derived_law.py.
"""
import numpy as np

DATA = "/home/udt-admin/UDT/data/Pantheon+SH0ES.dat"

# ---- load (IDENTICAL to sne_test_derived_law.py) ----
data = np.genfromtxt(DATA, names=True, dtype=None, encoding=None)
zHD   = data['zHD']
mb    = data['m_b_corr']
mberr = data['m_b_corr_err_DIAG']
iscal = data['IS_CALIBRATOR'].astype(int)
mask = (iscal == 0) & (zHD > 0.01)
z  = zHD[mask]
m  = mb[mask]
s  = mberr[mask]
w  = 1.0 / s**2
N  = len(z)
u  = np.log(1.0 + z)          # u = ln(1+z) = k·Δs
print(f"N SNe used (IS_CALIBRATOR==0, zHD>0.01): {N}")

def score(mu_model, label, npar_shape=0):
    """Fit one additive offset by weighted LS; report RMS & chi2/dof."""
    d = m - mu_model
    off = np.sum(w * d) / np.sum(w)
    resid = d - off
    rms = np.sqrt(np.mean(resid**2))
    wrms = np.sqrt(np.sum(w * resid**2) / np.sum(w))
    chi2 = np.sum(w * resid**2)
    dof = N - 1 - npar_shape
    print(f"  [{label}]  off={off:+.4f}  RMS={rms:.4f} mag  wRMS={wrms:.4f}  "
          f"chi2/dof={chi2/dof:.3f}  ({chi2:.1f}/{dof})")
    return resid, rms, chi2/dof, chi2

def chi2_of_offset(mu_model):
    d = m - mu_model
    off = np.sum(w * d) / np.sum(w)
    return np.sum(w * (d - off)**2)

# ============================================================
# Sanity check: a->0 reduces open/closed to flat
for a in (1e-4, 1e-3):
    assert np.allclose(np.sinh(a*u)/a, u, rtol=1e-6), "sinh limit"
    assert np.allclose(np.sin (a*u)/a, u, rtol=1e-6), "sin limit"
# low-z curvature sanity: (1+z)ln(1+z) vs z+z^2/2 at small z
zz = np.array([0.01, 0.02, 0.05])
approx = zz + zz**2/2
exact  = (1+zz)*np.log(1+zz)
print("low-z FLAT sanity  (1+z)ln(1+z) vs z+z^2/2:",
      {f"{zi:.2f}": (round(float(e),6), round(float(a),6)) for zi,e,a in zip(zz,exact,approx)})

# ============================================================
# Form 1: FLAT  d_L ∝ (1+z)·u      (parameter-free shape)
shapeF = (1.0 + z) * u
muF = 5.0*np.log10(shapeF)
print("\nForm 1 FLAT  d_L=(1+z)·ln(1+z)/k  (parameter-free shape):")
residF, rmsF, cF, chi2F = score(muF, "FLAT", npar_shape=0)

# ============================================================
# Form 2: OPEN  d_L ∝ (1+z)·sinh(a·u)/a  (fit a)
def mu_open(a):
    shp = (1.0+z) * np.sinh(a*u)/a
    return 5.0*np.log10(shp)
# Form 3: CLOSED d_L ∝ (1+z)·sin(a·u)/a  (fit a);  a·u_max < pi to stay monotone
def mu_closed(a):
    shp = (1.0+z) * np.sin(a*u)/a
    return 5.0*np.log10(shp)

def fit_a(mu_fun, a_lo, a_hi, label, guard=None):
    # coarse grid then golden-ish refine
    grid = np.linspace(a_lo, a_hi, 400)
    best = None
    for a in grid:
        if guard is not None and not guard(a):
            continue
        c = chi2_of_offset(mu_fun(a))
        if best is None or c < best[1]:
            best = (a, c)
    # refine around best
    a0 = best[0]; da = (a_hi-a_lo)/400
    grid2 = np.linspace(a0-da, a0+da, 400)
    for a in grid2:
        if a<=0: continue
        if guard is not None and not guard(a):
            continue
        c = chi2_of_offset(mu_fun(a))
        if c < best[1]:
            best = (a, c)
    return best

u_max = u.max()
print(f"\n(u_max = ln(1+z_max) = {u_max:.4f}; CLOSED needs a·u_max < π => a < {np.pi/u_max:.3f})")

aO, _ = fit_a(mu_open, 1e-3, 5.0, "OPEN")
print(f"\nForm 2 OPEN  d_L∝(1+z)·sinh(a·u)/a   best-fit a = {aO:.4f}")
residO, rmsO, cO, chi2O = score(mu_open(aO), f"OPEN a={aO:.3f}", npar_shape=1)

aC, _ = fit_a(mu_closed, 1e-3, np.pi/u_max*0.999, "CLOSED",
              guard=lambda a: a*u_max < np.pi)
print(f"\nForm 3 CLOSED d_L∝(1+z)·sin(a·u)/a    best-fit a = {aC:.4f}")
residC, rmsC, cC, chi2C = score(mu_closed(aC), f"CLOSED a={aC:.3f}", npar_shape=1)

# ============================================================
# Benchmarks (identical machinery to validated script)
muA = 5.0*np.log10(z)                                  # FROZEN linear d_L=z/k
print("\nBenchmark: FROZEN linear (transverse D_A=r) d_L=z/k:")
residLIN, rmsLIN, cLIN, _ = score(muA, "FROZEN linear")

Om = 0.3
def dL_lcdm(zz):
    out = np.empty_like(zz)
    for i, zi in enumerate(zz):
        g = np.linspace(0, zi, 512)
        E = np.sqrt(Om*(1+g)**3 + (1-Om))
        out[i] = (1+zi)*np.trapz(1.0/E, g)
    return out
muB = 5.0*np.log10(dL_lcdm(z))
print("\nBenchmark: flat-LCDM Om=0.3:")
residB, rmsB, cB, _ = score(muB, "flat-LCDM", npar_shape=0)

mu_g = 0.2473
def phi_cubic(r): return 1.5*mu_g*r - np.cos(np.pi/5)*mu_g**2*r**2 + (2.0/3.0)*mu_g**3*r**3
def r_of_z_cubic(zt):
    lo, hi = 0.0, 60.0
    for _ in range(80):
        mid = 0.5*(lo+hi)
        if np.exp(phi_cubic(mid))-1.0 < zt: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)
r_c = np.array([r_of_z_cubic(zi) for zi in z])
muCub = 5.0*np.log10(r_c*np.exp(phi_cubic(r_c)))
print("\nBenchmark: repo UDT locked-cubic:")
residCub, rmsCub, cCub, _ = score(muCub, "locked-cubic", npar_shape=0)

# ============================================================
# Residual trend vs z (binned in log10 z)
def trend(resid, label):
    print(f"\nResidual trend vs z  [{label}]  (m - model - offset), binned in log10(z):")
    lz = np.log10(z); edges = np.linspace(lz.min(), lz.max(), 9)
    for a, b in zip(edges[:-1], edges[1:]):
        mm = (lz>=a)&(lz<b)
        if mm.sum()>0:
            print(f"  z∈[{10**a:.4f},{10**b:.4f}] n={mm.sum():4d}  "
                  f"mean={np.mean(resid[mm]):+.4f}  median={np.median(resid[mm]):+.4f}")
trend(residF, "FLAT")
trend(residO, f"OPEN a={aO:.3f}")
trend(residC, f"CLOSED a={aC:.3f}")
trend(residLIN, "FROZEN linear")

# ============================================================
print("\n" + "="*60)
print("SUMMARY  (RMS mag / chi2dof):")
print(f"  UDT FLAT   (1+z)·u/k  param-free : {rmsF:.4f} / {cF:.3f}")
print(f"  UDT OPEN   sinh, a={aO:.3f}       : {rmsO:.4f} / {cO:.3f}")
print(f"  UDT CLOSED sin,  a={aC:.3f}       : {rmsC:.4f} / {cC:.3f}")
print(f"  ---- benchmarks ----")
print(f"  flat-LCDM Om=0.3                 : {rmsB:.4f} / {cB:.3f}")
print(f"  UDT locked-cubic (repo)          : {rmsCub:.4f} / {cCub:.3f}")
print(f"  FROZEN linear d_L=z/k            : {rmsLIN:.4f} / {cLIN:.3f}")
