"""Quick test of sympy substitution of phi(r,th,phc) with a concrete form."""
import sympy as sp
import numpy as np

r, th, phc = sp.symbols('r tt ppc', real=True, positive=True)
phi = sp.Function('phi')(r, th, phc)

# Gamma^{3}_{1,1} = -phi_phc * exp(2 phi) / (r^2 sin^2 th)
phi_phc = sp.diff(phi, phc)
gamma = -phi_phc * sp.exp(2*phi) / (r**2 * sp.sin(th)**2)

# Concrete phi(r, th, phc) for m=1 perturbation
A2 = 0.03156295029608829
A3 = 0.005656770825770722
eps = 1e-3
r_CMB = 9.164
phi0_form = A2*r**2 + A3*r**3
Y21_form = sp.sqrt(15/(4*sp.pi)) * sp.sin(th) * sp.cos(th) * sp.cos(phc)
R_form = eps * 4 * (r/r_CMB) * (1 - r/r_CMB)
phi_concrete = phi0_form + R_form * Y21_form

# Substitute
gamma_sub = gamma.subs(phi, phi_concrete).doit()
print("gamma_sub keys:", gamma_sub.free_symbols)

# Evaluate at (r=3, th=pi/4, phc=pi/6)
val = gamma_sub.subs({r: 3.0, th: float(np.pi/4), phc: float(np.pi/6)}).evalf(20)
print(f"sympy gamma value: {val}")

# Direct numpy evaluation
def Y21(th, ph):
    return np.sqrt(15.0/(4*np.pi)) * np.sin(th) * np.cos(th) * np.cos(ph)

def R(r):
    x = r/r_CMB
    return 4.0*x*(1-x)

def dY21_dph(th, ph):
    return -np.sqrt(15.0/(4*np.pi)) * np.sin(th) * np.cos(th) * np.sin(ph)

def phi_num(r,th,ph):
    return A2*r**2 + A3*r**3 + eps*R(r)*Y21(th,ph)

def phi_phc_num(r,th,ph):
    return eps*R(r)*dY21_dph(th,ph)

r_v, th_v, phc_v = 3.0, np.pi/4, np.pi/6
gamma_num = -phi_phc_num(r_v,th_v,phc_v) * np.exp(2*phi_num(r_v,th_v,phc_v)) / (r_v**2 * np.sin(th_v)**2)
print(f"numpy gamma value: {gamma_num}")
print(f"abs diff: {abs(float(val)-gamma_num)}")
