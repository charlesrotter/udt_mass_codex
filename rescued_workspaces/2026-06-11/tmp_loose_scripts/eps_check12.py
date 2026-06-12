#!/usr/bin/env python3
"""VERIFIER EPSILON — independent reproduction of checks 1 and 2."""
import numpy as np
import sympy as sp

print("="*70)
print("CHECK 1: Static scalar T_{tr} = d_t phi * d_r phi = 0 for phi=phi(r)")
print("="*70)
t, r, th = sp.symbols('t r theta', real=True)
# A genuinely static scalar field depends only on r
phi_static = sp.Function('phi')(r)
# Canonical scalar stress-energy off-diagonal piece T_{tr} ~ d_t phi d_r phi
# (the gradient-gradient term; for any scalar, T_{mu nu} contains d_mu phi d_nu phi)
dt_phi = sp.diff(phi_static, t)
dr_phi = sp.diff(phi_static, r)
T_tr = dt_phi * dr_phi
print("  phi = phi(r) (static)")
print("  d_t phi =", dt_phi)
print("  d_r phi =", dr_phi)
print("  T_tr = d_t phi * d_r phi =", sp.simplify(T_tr))
print("  => T_tr == 0 :", sp.simplify(T_tr) == 0)

# Contrast: a time-dependent field would give nonzero
phi_dyn = sp.Function('phi')(t, r)
T_tr_dyn = sp.diff(phi_dyn, t) * sp.diff(phi_dyn, r)
print("  (contrast) time-dependent phi(t,r): T_tr =", T_tr_dyn, " (nonzero in general)")
print("  CONCLUSION: canonical static scalar sources NO T_tr; the Route-E off-diagonal")
print("              source must come from the matter momentum-flux, not the canonical scalar.")

print()
print("="*70)
print("CHECK 2: Continuity quadrature. delta_rho=cos(qr), solve nabla^2 chi = delta_rho,")
print("         J_r = d_r chi, measure phase offset J_r vs delta_rho. Expect ~90 deg.")
print("="*70)

def solve_poisson_dirichlet(rgrid, source):
    """Solve d^2 chi/dr^2 = source, Dirichlet chi=0 at both ends. FD tridiagonal."""
    n = len(rgrid)
    h = rgrid[1]-rgrid[0]
    A = np.zeros((n,n)); b = source.astype(float).copy()
    A[0,0]=1.0; b[0]=0.0
    A[-1,-1]=1.0; b[-1]=0.0
    for i in range(1,n-1):
        A[i,i-1]=1.0/h**2
        A[i,i]=-2.0/h**2
        A[i,i+1]=1.0/h**2
    return np.linalg.solve(A,b)

def measure_offset(rgrid, sig_a, sig_b, q):
    """Phase offset (deg) between two monochromatic-at-q signals, via lstsq projection
    onto cos(qr), sin(qr) over interior 25-75% to avoid Dirichlet boundary layers."""
    n=len(rgrid); lo,hi=int(0.25*n),int(0.75*n)
    rr=rgrid[lo:hi]
    a=sig_a[lo:hi]-np.mean(sig_a[lo:hi])
    b=sig_b[lo:hi]-np.mean(sig_b[lo:hi])
    M=np.vstack([np.cos(q*rr), np.sin(q*rr)]).T
    ca,*_=np.linalg.lstsq(M,a,rcond=None)
    cb,*_=np.linalg.lstsq(M,b,rcond=None)
    pa=np.arctan2(ca[1],ca[0]); pb=np.arctan2(cb[1],cb[0])
    off=np.degrees(pb-pa)
    while off>180: off-=360
    while off<=-180: off+=360
    return off

qs=[15.0,30.0,75.0,150.0,300.0,600.0]
print(f"  {'q':>8} {'wavelength':>11} {'|offset(deg)|':>14}")
offs=[]
for q in qs:
    lam=2*np.pi/q
    L=25.0*lam
    n=5000
    rgrid=np.linspace(0.0,L,n)
    drho=np.cos(q*rgrid)
    chi=solve_poisson_dirichlet(rgrid,drho)
    Jr=np.gradient(chi,rgrid)
    off=measure_offset(rgrid,drho,Jr,q)
    offs.append(abs(off))
    print(f"  {q:8.1f} {lam:11.4f} {abs(off):14.3f}")
print(f"  mean |offset| = {np.mean(offs):.3f} deg ; max dev from 90 = {np.max(np.abs(np.array(offs)-90)):.3f} deg")
print(f"  QUADRATURE (~90 deg) CONFIRMED: {np.max(np.abs(np.array(offs)-90))<2.0}")
