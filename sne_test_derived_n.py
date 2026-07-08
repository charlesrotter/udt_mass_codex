#!/usr/bin/env python3
"""
DERIVED-n SNe re-test.  Settles the corpus n trichotomy for d_L = D_A*(1+z)^n.

Derivation (see accompanying report): for the UDT static metric
    ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi} dr^2 + D_A(r)^2 dOmega^2,   1+z = e^{phi},
photons on null geodesics + photon-number conservation force Etherington:
    d_L = (1+z)^2 D_A     (n = 2),
NOT the n=1 form d_L = r e^{phi} in udt_canonical_geometry.md sec 12.8 (line 1932).
Note e^{2phi}=g_rr=(1+z)^2, so n=1 (d_L=r e^{phi}=r sqrt(g_rr)) is the SQUARE ROOT
of n=2 (d_L=r e^{2phi}=r g_rr): a dropped arrival-rate factor.

Freed-transverse-geometry forms (data-blind shapes), same loader/cuts/scoring as
the validated sne_test_transverse_geometry.py:
    1+z = e^{k*Ds}  =>  Ds = (1/k) ln(1+z) = u/k,   u = ln(1+z)
    constant-curvature D_A(Ds):  FLAT: Ds ;  OPEN: sinh(a*u)/a ;  CLOSED: sin(a*u)/a
    d_L = (1+z)^n * D_A(Ds).   Offset absorbs k and absolute magnitude M.
We run n=1 (corpus SNe form) AND n=2 (derived) side by side.
"""
import numpy as np

DATA = "/home/udt-admin/UDT/data/Pantheon+SH0ES.dat"

# ---- load (IDENTICAL to sne_test_transverse_geometry.py) ----
data = np.genfromtxt(DATA, names=True, dtype=None, encoding=None)
zHD   = data['zHD']; mb = data['m_b_corr']; mberr = data['m_b_corr_err_DIAG']
iscal = data['IS_CALIBRATOR'].astype(int)
mask = (iscal == 0) & (zHD > 0.01)
z = zHD[mask]; m = mb[mask]; s = mberr[mask]; w = 1.0/s**2
N = len(z); u = np.log(1.0+z)
print(f"N SNe used (IS_CALIBRATOR==0, zHD>0.01): {N}")

def score(mu_model, label, npar_shape=0):
    d = m - mu_model
    off = np.sum(w*d)/np.sum(w)
    resid = d - off
    rms = np.sqrt(np.mean(resid**2))
    chi2 = np.sum(w*resid**2); dof = N-1-npar_shape
    print(f"  [{label:28s}] RMS={rms:.4f} mag  chi2/dof={chi2/dof:.4f}  ({chi2:.1f}/{dof})")
    return rms, chi2/dof

def chi2off(mu_model):
    d = m - mu_model; off = np.sum(w*d)/np.sum(w)
    return np.sum(w*(d-off)**2)

def D_A_flat():   return u
def D_A_open(a):  return np.sinh(a*u)/a
def D_A_closed(a):return np.sin(a*u)/a

def fit_a(DA_fun, n, a_lo, a_hi, guard=None):
    def mu(a): return 5.0*np.log10((1.0+z)**n * DA_fun(a))
    grid = np.linspace(a_lo, a_hi, 600); best=None
    for a in grid:
        if a<=0 or (guard and not guard(a)): continue
        c = chi2off(mu(a))
        if best is None or c<best[1]: best=(a,c)
    a0=best[0]; da=(a_hi-a_lo)/600
    for a in np.linspace(a0-da, a0+da, 600):
        if a<=0 or (guard and not guard(a)): continue
        c=chi2off(mu(a))
        if c<best[1]: best=(a,c)
    return best[0]

u_max = u.max()
print(f"(u_max = ln(1+z_max) = {u_max:.4f};  CLOSED needs a*u_max < pi => a < {np.pi/u_max:.3f})\n")

for n in (1, 2):
    print(f"==================  n = {n}   [d_L = (1+z)^{n} * D_A]  ==================")
    score(5.0*np.log10((1.0+z)**n * D_A_flat()), f"FLAT   (param-free)")
    aO = fit_a(D_A_open,   n, 1e-3, 6.0)
    score(5.0*np.log10((1.0+z)**n * D_A_open(aO)),  f"OPEN   a={aO:.3f}", npar_shape=1)
    aC = fit_a(D_A_closed, n, 1e-3, np.pi/u_max*0.999, guard=lambda a: a*u_max<np.pi)
    score(5.0*np.log10((1.0+z)**n * D_A_closed(aC)),f"CLOSED a={aC:.3f}", npar_shape=1)
    print()

# ---- benchmarks (identical machinery) ----
print("==================  benchmarks  ==================")
Om=0.3
def dL_lcdm(zz):
    out=np.empty_like(zz)
    for i,zi in enumerate(zz):
        g=np.linspace(0,zi,512); E=np.sqrt(Om*(1+g)**3+(1-Om))
        out[i]=(1+zi)*np.trapz(1.0/E,g)
    return out
score(5.0*np.log10(dL_lcdm(z)), "flat-LCDM Om=0.3")

mu_g=0.2473
def phi_cubic(r): return 1.5*mu_g*r-np.cos(np.pi/5)*mu_g**2*r**2+(2.0/3.0)*mu_g**3*r**3
def r_of_z(zt):
    lo,hi=0.0,60.0
    for _ in range(80):
        mid=0.5*(lo+hi)
        if np.exp(phi_cubic(mid))-1.0<zt: lo=mid
        else: hi=mid
    return 0.5*(lo+hi)
r_c=np.array([r_of_z(zi) for zi in z])
score(5.0*np.log10(r_c*np.exp(phi_cubic(r_c))), "UDT locked-cubic (n=1)")
# same cubic but with the DERIVED n=2 optics:
score(5.0*np.log10(r_c*np.exp(2*phi_cubic(r_c))), "UDT locked-cubic (n=2 derived)")
