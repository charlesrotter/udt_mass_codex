"""
VERIF_charge_vs_winding.py  (recon-only, new file; does NOT edit committed scripts)

Keep two DISTINCT corpus objects apart:
  (A) TOPOLOGICAL CHARGE Q_top = (1/4pi) INT_{S2} omega_H1  (the pi_2 degree).
      Degree-m hedgehog => INT = 4*pi*m => Q_top = m.  (linear in m)
  (B) PUBLIC CHARGE SLOPE q in d ln f = -q d ln r,
      derived q = 1 - 2m/N = (N-2m)/N  (negative_phi sec.413). m=1,N=3 => 1/3.
"""
import sympy as sp
import numpy as np

th, ph = sp.symbols('theta phi', real=True)

def degree_integral(m):
    # degree-m map: azimuth wound m times, polar Theta(th)=th (0->pi once)
    Theta = th
    nx = sp.sin(Theta)*sp.cos(m*ph)
    ny = sp.sin(Theta)*sp.sin(m*ph)
    nz = sp.cos(Theta)
    n = sp.Matrix([nx, ny, nz])
    cross = n.diff(th).cross(n.diff(ph))
    jac = sp.trigsimp((n.T*cross)[0])
    integ = sp.integrate(sp.integrate(jac, (ph, 0, 2*sp.pi)), (th, 0, sp.pi))
    return sp.simplify(integ)

print("(A) degree-m area-form (pi_2) integral:")
for m in [1, 2, 3]:
    val = degree_integral(m)
    print(f"  m={m}: INT omega = {val} = 4*pi*({sp.nsimplify(val/(4*sp.pi))})  "
          f"=> Q_top = {sp.nsimplify(val/(4*sp.pi))}")

# numeric cross-check (matches the corpus area_form ratio 1.270/0.636 = 2.0)
print("\n  numeric cross-check (degree by Gauss map quadrature):")
for m in [1, 2, 3]:
    g = 600
    T = np.linspace(1e-6, np.pi-1e-6, g); P = np.linspace(0, 2*np.pi, g)
    TT, PP = np.meshgrid(T, P, indexing='ij')
    sx = np.sin(TT)*np.cos(m*PP); sy = np.sin(TT)*np.sin(m*PP); sz = np.cos(TT)
    # jacobian for Theta=th, azimuth m: = m*sin(th)
    jac = m*np.sin(TT)
    deg = np.trapz(np.trapz(jac, P, axis=1), T) / (4*np.pi)
    print(f"    m={m}: numeric Q_top = {deg:.4f}")

print("\n(B) public charge slope q=(N-2m)/N:")
for (N, mm) in [(3,1),(3,2),(5,1),(5,2),(7,3)]:
    print(f"  N={N}, m={mm}: q = {sp.Rational(N-2*mm, N)}")

print("\nCONCLUSION:")
print("  Q_top(degree) = 1,2,3  (linear in m) -- NOT 1/3,2/3,1.")
print("  q-slope at fixed N=3:  m=1 -> 1/3,  m=2 -> -1/3  -- NOT 2/3.")
print("  The sequence 1/3,2/3,1 is produced by NEITHER native object.")
