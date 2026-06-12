#!/usr/bin/env python3
"""VERIFIER EPSILON — independent reproduction of checks 3 and 4.

Phase = TT<->EE distance-from-in-phase, on canonical Branch-C N=2 polynomial profile.
TT kernel: W_TT = r^2 e^{-3 phi0}. Source mode delta_phi = cos(qr+alpha).
A linear functional int W * f gives a phasor; the TT<->EE phase diff folded to [0,90]:
  0  = in-phase / anti-phase (aligned)
  90 = quadrature.
psi_old (in-phase channel): int W * delta_phi   (no derivative)
psi_new (flux channel)    : int W * d_r delta_phi  (one radial derivative -> +90 rotation of mode)
"""
import math
import numpy as np

# Canonical Branch-C N=2 polynomial profile (independent re-derivation of params)
mu_g  = math.pi*math.sqrt(math.pi/3.0)/13.0
r_CMB = 9.164
cphi  = math.cos(math.pi/5.0)
def phi0(r):
    x = mu_g*r
    return 1.5*x - cphi*x*x + (2.0/3.0)*x**3

rg = np.linspace(1e-3, r_CMB-1e-3, 8000)
p0 = phi0(rg)

# TT reference kernel
W_TT = rg**2 * np.exp(-3.0*p0)

def phasor(W, q, deriv=False):
    """Return (c, s) = coefficients of cos(alpha), sin(alpha) for the functional
       int W * f(qr+alpha), f=cos (deriv=False) or f = d_r cos = -q sin (deriv=True).
       For deriv we drop the overall q (constant scaling, doesn't change phase)."""
    if not deriv:
        c = np.trapz(W*np.cos(q*rg), rg)
        s = np.trapz(W*np.sin(q*rg), rg)
    else:
        # d_r cos(qr+a) = -q[sin(qr)cos a + cos(qr) sin a]; coeff of cos a = -int W sin, of sin a = -int W cos
        c = np.trapz(W*(-np.sin(q*rg)), rg)
        s = np.trapz(W*(-np.cos(q*rg)), rg)
    return c, s

def beta(W, q, deriv=False):
    c,s = phasor(W,q,deriv)
    return math.atan2(s,c)

def dist_inphase(deg):
    a = abs(deg) % 180.0
    return min(a, 180.0-a)

def tt_ee_phase(W_EE_kernel, q, deriv):
    bTT = beta(W_TT, q, deriv=False)
    bEE = beta(W_EE_kernel, q, deriv=deriv)
    d = math.degrees(((bEE-bTT+math.pi)%(2*math.pi))-math.pi)
    return dist_inphase(d)

qs = np.linspace(20,700,40)

print("="*70)
print("CHECK 3: Phase-vs-weight for psi_new = int W d_r(delta_phi).")
print("  Distance-from-in-phase (deg), median over q in [20,700].")
print("="*70)

weights = {
    "bare e^{2phi0}/r^2"            : np.exp(2.0*p0)/rg**2,
    "bare const (W=1)"             : np.ones_like(rg),
    "flat 1/r"                     : 1.0/rg,
    "W^EE=(rCMB-r)/(rCMB r)e^{2phi0}": (r_CMB-rg)/(r_CMB*rg)*np.exp(2.0*p0),
    "TT-like r^2 e^{-3phi0}"       : rg**2*np.exp(-3.0*p0),
}
print(f"  {'weight':>34} {'median dist-from-inphase (deg)':>32}")
results3 = {}
for name,Wk in weights.items():
    meds = float(np.median([tt_ee_phase(Wk,q,deriv=True) for q in qs]))
    results3[name]=meds
    print(f"  {name:>34} {meds:32.2f}")
vals = list(results3.values())
print(f"  => range across weights: {min(vals):.1f} to {max(vals):.1f} deg")
print(f"     W^EE value (claimed ~66): {results3['W^EE=(rCMB-r)/(rCMB r)e^{2phi0}']:.1f} deg")

print()
print("="*70)
print("CHECK 4: Phase-vs-eps. psi = psi_old(int W^EE delta_phi) + eps*psi_new(int W^EE d_r delta_phi)")
print("  Median TT<->EE dist-from-in-phase over q in [20,700], folded to [0,90].")
print("="*70)
W_EE = (r_CMB-rg)/(r_CMB*rg)*np.exp(2.0*p0)
W_new = W_EE.copy()
eps_grid = [0.0,0.25,0.5,1.0,2.0,4.0]
print(f"  {'eps':>8} {'median dist-from-inphase (deg)':>32}")
results4=[]
for ep in eps_grid:
    ds=[]
    for q in qs:
        bTT = beta(W_TT,q,deriv=False)
        c_old,s_old = phasor(W_EE,q,deriv=False)
        c_new,s_new = phasor(W_new,q,deriv=True)
        C = c_old + ep*c_new
        S = s_old + ep*s_new
        bEE = math.atan2(S,C)
        d = math.degrees(((bEE-bTT+math.pi)%(2*math.pi))-math.pi)
        ds.append(dist_inphase(d))
    med=float(np.median(ds))
    results4.append((ep,med))
    print(f"  {ep:8.2f} {med:32.2f}")
print(f"  eps=0 baseline (claimed ~21): {results4[0][1]:.1f} deg")
print(f"  monotonicity: {[round(m,1) for _,m in results4]}")
