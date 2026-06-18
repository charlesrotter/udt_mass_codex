#!/usr/bin/env python3
"""
phase1_core_regularity.py -- PHASE-1a step 2: reconcile the TWO candidate radial
operators and pin the CORE regularity honestly. (No result forced.)

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A. OBSERVE.

The honest reduction (phase1_master_project.py) gave, for the WARP AMPLITUDE
h(t,r) that multiplies the FIXED P2(theta) angular pattern:
      d_t^2 h - d_r^2 h - (2/r) d_r h = 0        (barrier-FREE radial Helmholtz)
  =>  -H'' - (2/r) H' = w^2 H,   regular sol  H = j_0(w r).

The TEXTBOOK Regge-Wheeler master scalar Psi uses a DIFFERENT variable; its
operator is -Psi'' + [l(l+1)/r^2] Psi = w^2 Psi with regular sol Psi = r j_l(w r).

These are NOT contradictory -- they are two parametrizations of the SAME physical
l=2 vacuum GW DOF, related by the field redefinition. The PHYSICS (which w are
allowed) depends ONLY on the regularity of the PHYSICAL metric perturbation at
the core and the wall BC -- NOT on which variable we name. This script makes the
core-regularity choice VISIBLE and computes the spectrum under each, so the
choice is auditable (not smuggled).

PHYSICAL METRIC PERTURBATION:  delta g_thth = eps r^2 h(t,r) P2(theta).
Core regularity of the geometry (finite curvature at r->0):
  - h(t,r) finite and smooth at r=0  <=>  amplitude h ~ j_0-type (h(0) finite).
  - For the warp r^2 h to carry the l=2 angular pattern WITHOUT a conical/curvature
    singularity, the standard requirement is that the perturbation behave as the
    regular l=2 tensor harmonic ~ r^l near the core in the RW variable, i.e.
    Psi = r * (amplitude) ~ r^{l+1}.

We report BOTH spectra and state the premise for each. THIS IS THE PREMISE THAT
CHARLES MUST ADJUDICATE (core BC = chosen, tagged provisional).
"""
import numpy as np
from scipy.special import spherical_jn
from scipy.optimize import brentq
import sys
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from spectral_cheb import cheb_interval


def jl_dirichlet(l, n, R=1.0):
    xs = np.linspace(1e-6, (n + l + 5) * np.pi, 300000)
    f = spherical_jn(l, xs)
    z = []
    for i in range(len(xs) - 1):
        if f[i] * f[i + 1] < 0:
            z.append(brentq(lambda x: spherical_jn(l, x), xs[i], xs[i + 1]))
        if len(z) >= n:
            break
    return np.array(z[:n]) / R


def jl_neumann(l, n, R=1.0):
    def g(x):
        return spherical_jn(l, x) + x * spherical_jn(l, x, derivative=True)
    xs = np.linspace(1e-6, (n + l + 6) * np.pi, 300000)
    fv = np.array([g(x) for x in xs])
    z = []
    for i in range(len(xs) - 1):
        if fv[i] * fv[i + 1] < 0:
            z.append(brentq(g, xs[i], xs[i + 1]))
        if len(z) >= n:
            break
    return np.array(z[:n]) / R


print("=" * 78)
print("PHASE-1a step 2: TWO core-regularity premises, BOTH spectra reported.")
print("=" * 78)

R = 1.0
print("""
PREMISE A (amplitude regularity, from the honest Phase-0 reduction):
  the warp AMPLITUDE h obeys -h'' - (2/r) h' = w^2 h ; regular sol j_0(wr);
  core BC = h(0) finite (Neumann-like on amplitude). The angular l=2 lives in
  the FIXED P2 factor. -> w-ladder = zeros of j_0 (Dirichlet wall) etc.
  TAG: chosen core BC = 'amplitude finite at core'. Relax-test = PREMISE B.

PREMISE B (RW master-scalar regularity, textbook l=2 GW):
  master Psi = r * (amplitude), operator -Psi'' + 6/r^2 Psi = w^2 Psi,
  regular sol Psi = r j_2(wr) ~ r^3; core BC = Psi ~ r^{l+1} (the regular l=2
  tensor-harmonic branch, no curvature singularity). -> w-ladder = zeros of j_2.
  TAG: chosen core BC = 'regular l=2 tensor harmonic r^{l+1}'.
""")

print("--- Spectra under each premise (R=1, first 6 modes) ---")
for lbl, l in [("PREMISE A (amplitude, l=0-type radial ladder)", 0),
               ("PREMISE B (RW l=2 master, j_2 ladder)", 2),
               ("  [for reference: l=3 RW]", 3),
               ("  [for reference: l=4 RW]", 4)]:
    wD = jl_dirichlet(l, 6, R)
    wN = jl_neumann(l, 6, R)
    print(f"\n{lbl}:")
    print("  Dirichlet wall w_n:", wD)
    print("    ratios w_n/w_1 :", wD / wD[0])
    print("  Neumann   wall w_n:", wN)
    print("    ratios w_n/w_1 :", wN / wN[0])

print("""
HONEST READ:
  Both premises give a FIXED-ratio Bessel-zero ladder that scales exactly as 1/R
  (box-controlled). They differ only in WHICH Bessel order sets the ratios:
   - Premise A: j_0 zeros = n*pi exactly => ratios are the integers 1,2,3,4,...
   - Premise B: j_2 zeros => ratios 1, 1.5780, 2.1381, ... (the l=2 cavity ladder)
  NEITHER is richer than a single-l spherical-cavity ladder. The l>=2 angular
  label changes the ladder's offset/ratios but NOT its box-controlled character.
  The choice between A and B is a CORE-BC premise for Charles to adjudicate; it
  does not change the box-control verdict.
""")

# numeric confirmation that j_0 zeros are exactly n*pi (Premise A ratios = integers)
wA = jl_dirichlet(0, 6, R)
print("Premise A check: j_0 Dirichlet zeros / pi =", wA / np.pi, "(=> integers 1..6)")
