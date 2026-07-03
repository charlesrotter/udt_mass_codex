"""th2: SELF-CONSISTENT universal bottom system (new this derivation).
v_zz - p v_z + v = 1 ; psi_z = p ; p_z = gamma e^{-2psi} v_z^2 - p^2 ; zero ICs.
gamma = 4 dt^2 / (Z s1^2 x_c^2).
Outputs: first v_z-node phase, late node-ladder phase mod pi (z*_eff),
z_c_eff from p(z) ~ 2 z/(z^2+z_c^2), and e^psi/zeta^2 -> 1/z_c_eff^2.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

def run(gamma, zmax=80.0):
    def f(z, y):
        v, vz, psi, p = y
        return [vz, p*vz - v + 1.0, p, gamma*np.exp(-2.0*psi)*vz*vz - p*p]
    s = solve_ivp(f, (0.0, zmax), [0.0, 0.0, 0.0, 0.0], rtol=1e-11, atol=1e-13,
                  dense_output=True)
    zz = np.linspace(1e-3, zmax, 200001)
    v, vz, psi, p = s.sol(zz)
    sgn = np.sign(vz)
    idx = np.where(sgn[:-1]*sgn[1:] < 0)[0]
    nodes = np.array([brentq(lambda z: s.sol(z)[1], zz[i], zz[i+1], xtol=1e-12) for i in idx])
    # z_c_eff from late p: p = 2z/(z^2+zc^2) -> zc^2 = z(2-p z)/p  (average over last stretch)
    mask = zz > 0.7*zmax
    zc2 = zz[mask]*(2.0 - p[mask]*zz[mask])/p[mask]
    zc_eff_p = np.sqrt(np.mean(zc2))
    zc_eff_psi = np.sqrt(np.mean(zz[mask]**2/np.exp(psi[mask])))
    late = np.mod(nodes[-6:], np.pi)
    return nodes, zc_eff_p, zc_eff_psi, np.mean(late), s

print(f"{'gamma':>8}{'1st node/pi':>12}{'ladder z*/pi':>14}{'zc_eff(p)':>11}{'zc_eff(psi)':>12}")
for gam in (0.5, 1.0, 1.5, 2.0, 2.335, 2.355, 3.0, 4.0, 6.0):
    nodes, zcp, zcpsi, zstar, s = run(gam)
    print(f"{gam:>8.3f}{nodes[0]/np.pi:>12.4f}{zstar/np.pi:>14.4f}{zcp:>11.4f}{zcpsi:>12.4f}")

# compare against measured stageB N=8: first node zeta = 1.2161 pi, z_c = 0.8825
