"""th2: launch phase z*(z_c) of the universal bottom ODE, exact numeric integration.
g'' - [2 zeta/(zeta^2+z_c^2)] g' + g = 0, g(0)=-1, g'(0)=0; project on tail basis
u_J = sin z - z cos z, u_Y = cos z + z sin z at z_max; z* = atan2(-beta, alpha) mod pi.
Also: direct node ladder of g' (no basis) -> first-node phase and asymptotic node phase,
to check the projection convention against the actual node positions.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

def inject(z_c, zeta_max=200.0):
    def f(z, y):
        g, gp = y
        return [gp, 2*z/(z*z + z_c*z_c)*gp - g]
    s = solve_ivp(f, (0.0, zeta_max), [-1.0, 0.0], rtol=1e-12, atol=1e-14, dense_output=True)
    z = zeta_max
    g, gp = s.y[:, -1]
    uJ, uY = np.sin(z) - z*np.cos(z), np.cos(z) + z*np.sin(z)
    uJp, uYp = z*np.sin(z), z*np.cos(z)
    W = uJ*uYp - uY*uJp
    al, be = (g*uYp - gp*uY)/W, (gp*uJ - g*uJp)/W
    return al, be, s

print(f"{'z_c':>8}{'alpha':>10}{'beta':>10}{'z*/pi (atan2(-b,a))':>22}{'node ladder mod pi (late)':>28}{'1st gp-node/pi':>16}")
for z_c in (0.05, 0.2, 0.4, 0.6, 0.8, 0.8825, 0.885, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4):
    al, be, s = inject(z_c)
    zstar = np.mod(np.arctan2(-be, al), np.pi)
    # direct node ladder of g'
    zz = np.linspace(0.05, 200.0, 400001)
    gp = s.sol(zz)[1]
    idx = np.where(np.sign(gp[:-1]) != np.sign(gp[1:]))[0]
    nodes = []
    for i in idx:
        try:
            nodes.append(brentq(lambda z: s.sol(z)[1], zz[i], zz[i+1], xtol=1e-12))
        except ValueError:
            pass
    nodes = np.array(nodes)
    late = np.mod(nodes[-5:], np.pi)  # late-ladder phase
    first = nodes[0] if len(nodes) else np.nan
    print(f"{z_c:>8.4f}{al:>10.4f}{be:>10.4f}{zstar/np.pi:>22.4f}{np.mean(late)/np.pi:>28.4f}{first/np.pi:>16.4f}")
