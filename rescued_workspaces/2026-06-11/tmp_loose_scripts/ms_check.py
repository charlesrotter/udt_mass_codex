import numpy as np
from scipy.integrate import solve_ivp

# UDT vacuum ODE (flux form):
#   J' = r^2 * mu^2 * phi
#   phi' = J * e^{2phi} / r^2
# Locked: phi0 = -cos(pi/5), mu^2 = pi/3, r* = 6.9875

mu2 = np.pi/3
rstar = 6.9875
phi0 = -np.cos(np.pi/5)
print("phi0 =", phi0)
print("mu2 =", mu2)

def rhs(r, y):
    phi, J = y
    if r == 0:
        return [0.0, 0.0]
    dphi = J*np.exp(2*phi)/r**2
    dJ = r**2*mu2*phi
    return [dphi, dJ]

# integrate from small r0 to avoid singularity at 0
r0 = 1e-6
# initial conditions: phi(0)=phi0, J(0)=0
y0 = [phi0, 0.0]
sol = solve_ivp(rhs, [r0, rstar], y0, rtol=1e-10, atol=1e-12, dense_output=True, max_step=0.001)
phi_end, J_end = sol.y[0,-1], sol.y[1,-1]
print("phi(r*) =", phi_end)
print("J(r*) =", J_end)
em2phi = np.exp(-2*phi_end)
print("e^{-2phi(r*)} =", em2phi)
print("lapse e^{-phi} =", np.exp(-phi_end))
m_MS = (rstar/2)*(1 - em2phi)
print("m_MS(r*) =", m_MS)
