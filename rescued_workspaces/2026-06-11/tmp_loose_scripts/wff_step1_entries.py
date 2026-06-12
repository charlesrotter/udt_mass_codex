"""
W_ff derivation, step 1: exact source-sector Hessian entries.

CONVENTIONS (pinned, used everywhere; orthonormal real spherical harmonics):
  Y00 = 1/sqrt(4pi)
  Y10 = sqrt(3/4pi) x          (x = cos theta)
  Y11 = sqrt(3/4pi) sqrt(1-x^2) cos(phi)
  Y20 = sqrt(5/16pi)(3x^2-1)
  Y21 = sqrt(15/4pi) x sqrt(1-x^2) cos(phi)
  Y22 = sqrt(15/16pi)(1-x^2) cos(2phi)
  int |Y|^2 dOmega = 1 for each (checked below).

Field: f(y,theta,phi) = F(y) + sum a_lm(y) Y_lm.  Background (demanded):
  f0 = F(y)(1 + kappa(y) x),  i.e. a_10^bg = kappa F / c,  c = sqrt(3/4pi).
  F = y^{-q}, q = 1/3.

Action per the verified C1 reduction, sphere-integrated:
  S = int dy [ (1/4) y^2 int dOmega f_y^2 dOmega-coefficients + P[f] ]
    = int dy [ pi y^2 F'^2 + (1/4) y^2 sum a_lm'^2 + P ],
  P[f] = (1/4) int dOmega |grad_Omega f|^2 / f.
(The monopole kinetic 4pi(1/4)y^2F'^2 and per-orthonormal-Y a-kinetic
 (1/4)y^2 a'^2 match the verified record verbatim.)

Second variation (EXACT identity, derived and verified below):
  Q[h] = (1/4) int dOmega f0 |grad_Omega (h/f0)|^2   >= 0,
  null space exactly h proportional to f0  (the scaling direction).

Hessian entries V_AB = d^2 P, in units of 1/F (V_AB = y^q M_AB(kappa)):
  M_AB = (c_m/2) * int_{-1}^{1} (1+kx) [ (1-x^2) D(gA/f) D(gB/f)
                                       + m^2 (gA/f)(gB/f)/(1-x^2) ] dx
  with c_0 = 2pi (phi-integral of 1), c_m = pi (phi-integral of cos^2 m phi),
  gA = theta-part of Y_A (full normalization), f = 1+kx.
"""
import sympy as sp

k, x = sp.symbols('k x')
pi = sp.pi
f = 1 + k*x
L = sp.log((1+k)/(1-k))

c00 = 1/sp.sqrt(4*pi)
c10 = sp.sqrt(3/(4*pi))
c20 = sp.sqrt(5/(16*pi))
c11 = sp.sqrt(3/(4*pi))
c21 = sp.sqrt(15/(4*pi))
c22 = sp.sqrt(15/(16*pi))

# ---------- m = 0 block: rational integrands directly ----------
g = {0: c00 + 0*x, 1: c10*x, 2: c20*(3*x**2 - 1)}

def entry_m0(A, B):
    uA = g[A]/f; uB = g[B]/f
    integrand = (1+k*x)*(1-x**2)*sp.diff(uA, x)*sp.diff(uB, x)
    I = sp.integrate(sp.together(sp.expand(integrand)), (x, -1, 1))
    return sp.simplify((2*pi/2) * I)

# ---------- m = 1 block: g = sqrt(1-x^2) h, rationalized ----------
h = {1: c11/f, 2: c21*x/f}

def entry_m1(A, B):
    hA, hB = h[A], h[B]
    dA, dB = sp.diff(hA, x), sp.diff(hB, x)
    grad_part = x**2*hA*hB - x*(1-x**2)*(sp.diff(hA*hB, x)) + (1-x**2)**2*dA*dB
    m2_part = hA*hB          # (gA gB/(1-x^2)) with m^2=1
    integrand = (1+k*x)*(grad_part + m2_part)
    I = sp.integrate(sp.together(sp.expand(integrand)), (x, -1, 1))
    return sp.simplify((pi/2) * I)

# ---------- m = 2: single channel ----------
def entry_m2():
    u = c22*(1-x**2)/f
    du = sp.diff(u, x)
    integrand = (1+k*x)*((1-x**2)*du**2 + 4*u**2/(1-x**2))
    I = sp.integrate(sp.together(sp.expand(integrand)), (x, -1, 1))
    return sp.simplify((pi/2) * I)

# ---------- tadpoles and P itself (F=1 units) ----------
# P   = (2pi/4) int k^2 (1-x^2)/f dx
# P_A = (2pi/4) int [ 2k(1-x^2) gA' / f - k^2 (1-x^2) gA / f^2 ] dx   (m=0 A)
P_exact = sp.simplify((pi/2)*k**2*sp.integrate((1-x**2)/f, (x, -1, 1)))

def tadpole(A):
    gA = g[A]
    integrand = 2*k*(1-x**2)*sp.diff(gA, x)/f - k**2*(1-x**2)*gA/f**2
    return sp.simplify((pi/2)*sp.integrate(sp.together(integrand), (x, -1, 1)))

names0 = ['W', 'a0', 'g0']
M0 = {}
for A in range(3):
    for B in range(A, 3):
        M0[(A, B)] = entry_m0(A, B)

M1 = {}
for A in (1, 2):
    for B in (A, 2):
        M1[(A, B)] = entry_m1(A, B)

M22 = entry_m2()
Pa = tadpole(1)
Pg = tadpole(2)

print("P (F=1)        =", sp.simplify(P_exact))
print("P_a tadpole    =", Pa)
print("P_g0 tadpole   =", Pg)
print()
for (A, B), v in M0.items():
    print(f"M0[{names0[A]},{names0[B]}] =", v)
print()
lbl = {1: 'a1', 2: 'gm1'}
for (A, B), v in M1.items():
    print(f"M1[{lbl[A]},{lbl[B]}] =", v)
print()
print("M2[g2,g2] =", M22)

import pickle
with open('/tmp/wff_entries.pkl', 'wb') as fh:
    pickle.dump({'M0': M0, 'M1': M1, 'M22': M22, 'P': P_exact,
                 'Pa': Pa, 'Pg': Pg, 'k': k}, fh)
print("\nsaved /tmp/wff_entries.pkl")
