"""th2: bottom system REFINED with the (Z/4)phi'^2 source restored (derived, no fit):
v_zz - p v_z + v = 1 - beta p^2 e^{2psi},  psi_z = p,  p_z = gamma e^{-2psi} v_z^2 - p^2,
beta = Z|s1|x_c^2/(4 dt)  [= the u_p source-offset ratio at the bottom scale].
Compare z*_eff and first node vs the beta=0 version and vs measured (Z8N8: first 1.2161pi,
theta0 decomposition needs z*_eff; Z1N8 for the Z-check).
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
XC = 1.0/1101.0

def bottom_beta(gamma, beta, zmax=120.0):
    def f(z, y):
        v, vz, psi, p = y
        return [vz, p*vz - v + 1.0 - beta*p*p*np.exp(2.0*psi),
                p, gamma*np.exp(-2.0*psi)*vz*vz - p*p]
    s = solve_ivp(f, (0.0, zmax), [0.,0.,0.,0.], rtol=1e-11, atol=1e-13, dense_output=True)
    zz = np.linspace(1e-3, zmax, 300001)
    vz = s.sol(zz)[1]
    idx = np.where(np.sign(vz[:-1])*np.sign(vz[1:]) < 0)[0]
    nodes = np.array([brentq(lambda z: s.sol(z)[1], zz[i], zz[i+1], xtol=1e-12) for i in idx])
    lad = np.mod(nodes, np.pi)
    mask = zz > 0.75*zmax
    psi = s.sol(zz[mask])[2]
    zc_eff = float(np.sqrt(np.mean(zz[mask]**2/np.exp(psi))))
    return nodes[0], float(np.mean(lad[-6:])), zc_eff

cases = [("Z8N8", 8.0, 2.994055, 5.875565e-3, 2.334, 1.2161),
         ("Z1N8", 1.0, 2.996865, 2.090649e-3/1.0, 2.358, None)]
# dt for c2: 1.5*d*(1+...) -- use exact: fam A1m3 par=1.5*(1-1.3937663900757328e-3)
import sympy as sp
rho = sp.Symbol('rho', positive=True)
par_c2 = 1.5*(1-1.3937663900757328e-3)
U2 = 2*rho**3*sp.exp(-par_c2*(rho**2-1))
dt_c2 = float(sp.diff(U2, rho).subs(rho,1))/4; s1_c2 = -float(sp.diff(U2, rho, 2).subs(rho,1))/4
cases[1] = ("Z1N8", 1.0, s1_c2, dt_c2, 2.358, None)

print(f"{'case':>6}{'beta':>10}{'1st/pi':>9}{'z*eff/pi':>10}{'zc_eff':>8}")
for tag, Z, s1, dt, gam, meas1 in cases:
    beta = Z*s1*XC*XC/(4.0*dt)
    for b in (0.0, beta):
        n1, zst, zce = bottom_beta(gam, b)
        print(f"{tag:>6}{b:>10.2e}{n1/np.pi:>9.4f}{zst/np.pi:>10.4f}{zce:>8.4f}")
    if meas1: print(f"   [measured first node {meas1:.4f} pi]")
