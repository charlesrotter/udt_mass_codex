#!/usr/bin/env python3
"""
ADVERSARIAL independent verification of the UDT derived-SNe-law claim.
Zero reuse of the repo's score() beyond re-implementing offset-marginalized WLS
from scratch. Tests: (B) reproduce FLAT 0.162; (A) one-power vs two-power
Etherington fragility; (C) discriminating power vs a basket of curved forms.
"""
import numpy as np

DATA = "/home/udt-admin/UDT/data/Pantheon+SH0ES.dat"
d = np.genfromtxt(DATA, names=True, dtype=None, encoding=None)
mask = (d['IS_CALIBRATOR'].astype(int) == 0) & (d['zHD'] > 0.01)
z = d['zHD'][mask]; m = d['m_b_corr'][mask]; s = d['m_b_corr_err_DIAG'][mask]
w = 1.0/s**2
N = len(z)
u = np.log1p(z)
print(f"Independent load: N={N}, z in [{z.min():.4f},{z.max():.4f}]")

def fit(shape, label, npar=0):
    """Offset-marginalized weighted least squares on mu=5log10(shape)+off."""
    mu = 5.0*np.log10(shape)
    dd = m - mu
    off = np.sum(w*dd)/np.sum(w)          # analytic WLS optimum for a pure offset
    r = dd - off
    rms = np.sqrt(np.mean(r**2))
    wrms = np.sqrt(np.sum(w*r**2)/np.sum(w))
    chi2 = np.sum(w*r**2)
    dof = N-1-npar
    # linear residual-vs-log10z tilt (slope), to see leftover ramp
    A = np.vstack([np.log10(z), np.ones(N)]).T
    slope = np.linalg.lstsq(A, r, rcond=None)[0][0]
    print(f"  {label:38s} RMS={rms:.4f} wRMS={wrms:.4f} chi2/dof={chi2/dof:.3f} tilt/dex={slope:+.4f}")
    return rms, r

print("\n== (B) reproduce + (A) one vs two power Etherington ==")
fit((1+z)*u,            "FLAT one-power (1+z)ln(1+z)")
fit((1+z)**2*u,         "Etherington two-power (1+z)^2 ln(1+z)")
fit(u,                  "zero-power  ln(1+z)")
fit(z,                  "frozen-linear d_L=z")

print("\n== (C) basket of simple curved 1-shape-param-free forms ==")
fit(z*(1+z/2),          "z(1+z/2)")
fit(z*np.sqrt(1+z),     "z*sqrt(1+z)")
fit(np.sinh(z),         "sinh(z)")
fit(z+z**2/2,           "z+z^2/2")
fit(z*(1+0.5*z),        "z(1+0.5z)  a=0.5 fixed")
fit(z*(1+z)**0.5,       "z(1+z)^0.5")
fit((1+z)*z/(1+z/2),    "(1+z)z/(1+z/2)")
fit(np.log1p(z)*(1+0.8*z), "ln(1+z)(1+0.8z)")

# flat-LCDM Om=0.3
Om=0.3
def lcdm(zz):
    out=np.empty_like(zz)
    for i,zi in enumerate(zz):
        g=np.linspace(0,zi,512); E=np.sqrt(Om*(1+g)**3+(1-Om))
        out[i]=(1+zi)*np.trapz(1/E,g)
    return out
fit(lcdm(z),            "flat-LCDM Om=0.3 (ref)")

print("\n== (C-b) two-power basket: does ANY alt curved form fit under two-power dual too? ==")
# If the DUALITY is what matters, apply the (1+z)^2 dual to alternatives' D_A too.
# Here treat each 'shape' above already as d_L; the point is the spread of RMS.

print("\n== best a for one-param mildly-curved family d_L=z(1+a z) ==")
best=None
for a in np.linspace(-0.5,1.5,4001):
    sh=z*(1+a*z)
    if np.any(sh<=0): continue
    mu=5*np.log10(sh); dd=m-mu; off=np.sum(w*dd)/np.sum(w)
    rms=np.sqrt(np.mean((dd-off)**2))
    if best is None or rms<best[1]: best=(a,rms)
print(f"  argmin a={best[0]:+.4f} RMS={best[1]:.4f}  (compare FLAT one-power above)")
