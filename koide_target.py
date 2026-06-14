"""
UDT lepton-spectrum target analysis.
Result (derived, given measured masses):
  - Koide Q = 2/3 to 5 figures.
  - Equivalent to 3 phases spaced 2pi/3 (=N=3) on a bounded amplitude,
    amplitude sqrt(2) FORCED by Q=2/3, single free phase delta and scale M.
  - Electron light = phase 2.3 deg from the node of (1+sqrt2 cos), NOT exponential.
  - Degenerate (ZZ3-exact) limit -> Q=1/3 = this program's single-cell null result.
  - delta = 0.22227 ~ 2/9 = 2 q^2  (q=1/3 native)  [coincidence to derive-or-kill].
Target for the next computation: does the N=3 winding soliton, with ZZ3 broken by
the phi back-reaction, yield deviations sqrt2*cos(delta+2pi i/3) with delta=2q^2 ?
"""
import numpy as np
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
m = np.array([me, mmu, mtau]); sm = np.sqrt(m); M = sm.mean()
eps = sm/M - 1.0
Q = m.sum()/sm.sum()**2
delta = np.arccos(eps[2]/np.sqrt(2))

print(f"Koide Q            = {Q:.6f}   (target 2/3 = {2/3:.6f})")
print(f"sum(eps^2)         = {(eps**2).sum():.6f}   (=3  <=>  Q=2/3)")
print(f"forced amplitude   = sqrt2 = {np.sqrt(2):.5f}")
print(f"forced spacing     = 120 deg = N=3")
print(f"free phase delta   = {delta:.5f} rad ;  2/9 = {2/9:.5f} = 2 q^2 (q=1/3)")

# reconstruct masses with EQUAL 120-deg spacing (i=1->e, 2->mu, 0->tau):
phases = delta + 2*np.pi*np.array([1,2,0])/3.0
rebuilt = (M*(1+np.sqrt(2)*np.cos(phases)))**2     # m = [M(1+sqrt2 cos)]^2
print("\nreconstructed m (MeV):", np.round(rebuilt,3))
print("measured      m (MeV):", np.round(m,3))
print("max rel. error       :", float(np.max(np.abs(rebuilt-m)/m)))

# node proximity of the electron
node = np.degrees(np.arccos(-1/np.sqrt(2)))
phi_e = np.degrees(delta+2*np.pi*1/3)
print(f"\nelectron phase {phi_e:.2f} deg vs node {node:.2f} deg -> {node-phi_e:+.2f} deg (why m_e is small)")

# ZZ3 breaking sweep: amplitude 0 (degenerate) -> sqrt2 (real)
print("\nZZ3-breaking amplitude  ->  Koide Q:")
for a in [0, 0.05, 0.3, 0.8, np.sqrt(2)]:
    e = a*np.cos(delta+2*np.pi*np.arange(3)/3); mm=(1+e)**2
    print(f"  a={a:5.3f}  Q={mm.sum()/np.sqrt(mm).sum()**2:.4f}")
