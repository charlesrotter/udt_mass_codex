import numpy as np
from scipy.integrate import solve_ivp
Z = 8.0
def rhs(r, y):
    phi, rho, phip, rhop = y
    return [phip, rhop, 4*np.exp(-2*phi)*rhop**2/(Z*rho**2) - 2*phip*rhop/rho,
            2*phip*rhop - (Z/4)*rho*np.exp(2*phi)*phip**2]
def E_of(y): return (Z/2)*y[1]**2*y[2]**2 - 2*np.exp(-2*y[0])*y[3]**2
def ev(r, y): return y[1] - 1e-4
ev.terminal = True
ev.direction = -1
y0 = [0.0, 1.0, 1.0, 0.0]
sol = solve_ivp(rhs, (1.0, 3.0), y0, rtol=1e-12, atol=1e-14, dense_output=True, events=ev)
rr = np.linspace(1.0, sol.t[-1], 100)
ys = sol.sol(rr)
E = np.array([E_of(ys[:, i]) for i in range(100)])
print("orbit from a rho-turning point (rho'=0, phi'=1, E=+4):"
      f" stops at r={sol.t[-1]:.4f} rho={sol.y[1,-1]:.2e}")
print(f"E0={E[0]:+.6f}  max|dE| up to collapse = {np.max(np.abs(E - E[0])):.2e}")
print("rho' at end:", sol.y[3, -1], "-> rho turned DOWN from the turning point and collapses;")
print("phi' was nonzero at the turning point -> a rho-turning point is NOT a seal")
