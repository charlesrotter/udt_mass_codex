"""Hostile probe: does AMPLITUDE (a(1) != 0) loading always terminate, or can it
saturate when given the 1/y slope profile (a_x = -a, F_x = -1/3 seeding B/y)?"""
import numpy as np
from scipy.integrate import solve_ivp

c = np.sqrt(3/(4*np.pi)); KMAX = 1-1e-10
def rhs(x, u):
    F, Fx, a, ax = u
    k = np.clip(c*a/F, -KMAX, KMAX); ak = abs(k)
    if ak < 1e-3:
        srcF = -(ak*ak/3 + ak**4/5)
        srca = np.pi*c*(8*ak/3 + 16*ak**3/15)*np.sign(k)
    else:
        L = np.log((1+ak)/(1-ak))
        srcF = 1 - L/(2*ak)
        srca = np.pi*c*((1+1/ak**2)*L - 2/ak)*np.sign(k)
    return [Fx, srcF-Fx, ax, srca-ax]
def ev(x, u): return abs(c*u[2]/u[0]) - (1-1e-6)
ev.terminal = True

def run(F0, Fx0, a0, ax0, xend=-30):
    s = solve_ivp(rhs, [0, xend], [F0, Fx0, a0, ax0], method='LSODA',
                  events=ev, rtol=1e-10, atol=1e-12, max_step=0.1)
    if s.t_events[0].size:
        return f"DEGENERATE y_dgn={np.exp(s.t_events[0][0]):.6g}"
    F, Fx, a, ax = s.y[:, -1]
    return f"ran to y={np.exp(xend):.1e}: k_end={c*a/F:.6f} F_end={F:.3e}"

print("amplitude loading, 1/y slope profile (a_x=-a), F_x0=-1/3:")
for k0 in [0.01, 0.05, 0.1, 0.23, 0.5, 0.683]:
    a0 = k0/c
    print(f"  k0={k0}: ", run(1.0, -1/3, a0, -a0))
print("amplitude loading, flat profile (a_x=0), F_x0=-1/3:")
for k0 in [0.05, 0.23, 0.683]:
    a0 = k0/c
    print(f"  k0={k0}: ", run(1.0, -1/3, a0, 0.0))
print("amplitude loading, SS profile (a_x=-a/2), steeper F slope F_x0=-1:")
for k0 in [0.05, 0.23]:
    a0 = k0/c
    print(f"  k0={k0}: ", run(1.0, -1.0, a0, -a0/2))
print("tiny SS amplitude check ('any nonzero'):")
for k0 in [0.005, 0.001]:
    a0 = k0/c
    print(f"  k0={k0}: ", run(1.0, -1/3, a0, -a0/2))
