"""Numeric spot-checks: (a) E and J=W-2Er conserved along generic orbits; (b) attempt to
shoot a 'regular center' backwards: start from regular-center-like data at small r and
watch the phi-EOM blow up / self-inconsistency; (c) E<0 orbits never reach rho'=0."""
import numpy as np
from scipy.integrate import solve_ivp

Z = 8.0

def rhs(r, y):
    phi, rho, phip, rhop = y
    phipp = 4*np.exp(-2*phi)*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
    rhopp = 2*phip*rhop - (Z/4)*rho*np.exp(2*phi)*phip**2
    return [phip, rhop, phipp, rhopp]

def E_of(y):
    phi, rho, phip, rhop = y
    return (Z/2)*rho**2*phip**2 - 2*np.exp(-2*phi)*rhop**2

def W_of(y):
    phi, rho, phip, rhop = y
    return -4*np.exp(-2*phi)*rho*rhop

print("(a) conservation along generic orbits:")
for y0 in ([0.3, 1.0, 0.4, 0.7], [-0.2, 2.0, -0.3, 1.5], [0.0, 1.0, 1.0, 0.0]):
    sol = solve_ivp(rhs, (1.0, 6.0), y0, rtol=1e-12, atol=1e-14, dense_output=True)
    rr = np.linspace(1.0, sol.t[-1], 50)
    ys = sol.sol(rr)
    E = np.array([E_of(ys[:, i]) for i in range(len(rr))])
    J = np.array([W_of(ys[:, i]) - 2*E[i]*rr[i] for i in range(len(rr))])
    print(f"  y0={y0}: E0={E[0]:+.6f}  max|dE|={np.max(np.abs(E-E[0])):.2e}  "
          f"max|dJ|={np.max(np.abs(J-J[0])):.2e}  (integrated to r={sol.t[-1]:.2f})")

print("\n(b) 'regular center' shooting: y(eps) = [phi0, e^{phi0} eps, phip_c, e^{phi0}]")
print("    phi-EOM forces phi' ~ (4 e^{-2phi0}/Z)/r near 0 -> track e^{-phi}rho' and rho*phi'")
for phi0 in (0.0, 0.5):
    for eps in (1e-3, 1e-4, 1e-5):
        y0 = [phi0, np.exp(phi0)*eps, 0.0, np.exp(phi0)]
        sol = solve_ivp(rhs, (eps, 1.0), y0, rtol=1e-11, atol=1e-13, dense_output=True)
        yend = sol.y[:, -1]
        # measure the induced phi' at r=10*eps vs the predicted 4 e^{-2phi0}/(Z r)
        r_probe = 10*eps
        yp = sol.sol(r_probe)
        pred = 4*np.exp(-2*phi0)/(Z*r_probe)
        print(f"  phi0={phi0} eps={eps:.0e}: E(start)={E_of(y0):+.4f}  "
              f"phi'({r_probe:.0e})={yp[2]:+.4e} vs forced 4e^-2phi0/(Z r)={pred:+.4e}  "
              f"ratio={yp[2]/pred:+.3f}")

print("\n(c) E<0 orbit: e^{-phi}rho' stays >= sqrt(-E/2) (never a seal):")
y0 = [0.0, 1.0, 0.0, 1.0]   # E = -2
sol = solve_ivp(rhs, (1.0, 20.0), y0, rtol=1e-12, atol=1e-14, dense_output=True)
rr = np.linspace(1.0, sol.t[-1], 200)
ys = sol.sol(rr)
q = np.exp(-ys[0])*ys[3]
print(f"  E0={E_of(y0):+.4f}; min over run of e^-phi rho' = {q.min():.6f} (bound = 1.0)")
y0 = [0.2, 1.0, 0.1, -1.2]  # E<0, contracting
sol = solve_ivp(rhs, (1.0, 50.0), y0, rtol=1e-12, atol=1e-14, dense_output=True,
                events=lambda r, y: y[1] - 1e-6)
print(f"  contracting E={E_of(y0):+.4f} orbit: rho -> {sol.y[1,-1]:.3e} at r={sol.t[-1]:.4f}"
      f" (collapse; rho'={sol.y[3,-1]:+.3f} never 0)")
