"""BLIND VERIFIER C3: driverless coupled (F,a) inward flow — finite-depth degeneration?

Independent EL system (sphere-integrated action, x = ln y):
   F_xx + F_x = 1 - L/(2k)                       [EL-correct: (y^2F')' = P_F/(8pi)]
   a_xx + a_x = pi*c*[(1+1/k^2)L - 2/k],  k = c a / F, c = sqrt(3/4pi)
Agent-variant dynamics (if the 4pi was dropped in the F kinetic):
   F_xx + F_x = 4pi*(1 - L/(2k))                 [(y^2F')' = P_F/2]

IC classes at y=1 (x=0):
   SS  : F=1, F_x=-1/3, a = k0 F/c, a_x = -a/2   (self-similar loading)
   MOM : F=1, F_x in {-1/3, 0}, a=0, a_x = -cload (momentum-only)
Event: k -> 1 (f_min = F(1-k) -> 0). Integrate to x=-14 (y~8e-7).
"""
import numpy as np
from scipy.integrate import solve_ivp

c = np.sqrt(3/(4*np.pi))
KMAX = 1 - 1e-10

def rhs_factory(fpref):
    def rhs(x, u):
        F, Fx, a, ax = u
        k = c*a/F
        k = np.clip(k, -KMAX, KMAX)
        ak = abs(k)
        if ak < 1e-3:   # series branch (avoids catastrophic cancellation)
            srcF = fpref*(-(ak*ak/3 + ak**4/5 + ak**6/7))
            srca = np.pi*c*(8*ak/3 + 16*ak**3/15 + 24*ak**5/35)*np.sign(k)
        else:
            L = np.log((1+ak)/(1-ak))
            srcF = fpref*(1 - L/(2*ak))
            srca = np.pi*c*((1+1/ak**2)*L - 2/ak)*np.sign(k)
        return [Fx, srcF - Fx, ax, srca - ax]
    return rhs

def ev_deg(x, u):
    F, Fx, a, ax = u
    return abs(c*a/F) - (1 - 1e-6)
ev_deg.terminal = True
def ev_Fzero(x, u): return u[0] - 1e-8
ev_Fzero.terminal = True

def run(F0, Fx0, a0, ax0, fpref=1.0, xend=-14, rtol=1e-10, atol=1e-12, method='LSODA'):
    sol = solve_ivp(rhs_factory(fpref), [0, xend], [F0, Fx0, a0, ax0],
                    method=method, events=[ev_deg, ev_Fzero],
                    rtol=rtol, atol=atol, dense_output=True, max_step=0.1)
    out = {'status': 'ran to xend', 'y_end': np.exp(xend)}
    if sol.t_events[0].size:
        out['status'] = 'DEGENERATE k->1'
        out['y_dgn'] = float(np.exp(sol.t_events[0][0]))
    elif sol.t_events[1].size:
        out['status'] = 'F->0'
        out['y_dgn'] = float(np.exp(sol.t_events[1][0]))
    F, Fx, a, ax = sol.y[:, -1]
    out['k_end'] = float(c*a/F); out['F_end'] = float(F)
    out['sol'] = sol
    return out

print("=== SS (self-similar) loading, EL-correct dynamics ===")
k_exact_el = 0.683095
for k0 in [0.05, 0.230329, 0.5, k_exact_el, 0.816497]:
    a0 = k0/c
    r = run(1.0, -1/3, a0, -a0/2)
    print(f"  k0={k0:.6f}: {r['status']}, y_dgn={r.get('y_dgn', float('nan')):.6g}, "
          f"k_end={r['k_end']:.4f}")

print("\n=== SS loading, agent-variant dynamics (4pi-dropped F kinetic) ===")
for k0 in [0.230329, k_exact_el, 0.816497]:
    a0 = k0/c
    r = run(1.0, -1/3, a0, -a0/2, fpref=4*np.pi)
    print(f"  k0={k0:.6f}: {r['status']}, y_dgn={r.get('y_dgn', float('nan')):.6g}, "
          f"k_end={r['k_end']:.4f}")

print("\n=== MOM (momentum-only) loading, EL-correct, F_x0=-1/3 ===")
for cl in [0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]:
    r = run(1.0, -1/3, 0.0, -cl)
    print(f"  cload={cl}: {r['status']}, y_dgn={r.get('y_dgn', float('nan')):.6g}, "
          f"k_end={r['k_end']:.6f}, F_end={r['F_end']:.4g}")

print("\n=== MOM loading, EL-correct, F_x0=0 (vacuum-start) ===")
for cl in [0.001, 0.01, 0.05, 0.1, 0.2, 0.5]:
    r = run(1.0, 0.0, 0.0, -cl)
    print(f"  cload={cl}: {r['status']}, y_dgn={r.get('y_dgn', float('nan')):.6g}, "
          f"k_end={r['k_end']:.6f}, F_end={r['F_end']:.4g}")

print("\n=== MOM with OUTWARD momentum sign (a_x0=+cload), F_x0=-1/3 ===")
for cl in [0.05, 0.2]:
    r = run(1.0, -1/3, 0.0, +cl)
    print(f"  cload={cl}: {r['status']}, y_dgn={r.get('y_dgn', float('nan')):.6g}, "
          f"k_end={r['k_end']:.6f}")

print("\n=== deep-window check: 'saturating' candidates run to x=-30 (y~9e-14) ===")
for label, ic in [("MOM cload=0.01 Fx0=-1/3", (1.0, -1/3, 0.0, -0.01)),
                  ("MOM cload=0.05 Fx0=-1/3", (1.0, -1/3, 0.0, -0.05)),
                  ("MOM cload=0.05 Fx0=0",    (1.0, 0.0, 0.0, -0.05))]:
    r = run(*ic, xend=-30)
    print(f"  {label}: {r['status']}, y_dgn={r.get('y_dgn', float('nan')):.6g}, "
          f"k_end={r['k_end']:.6f}, F_end={r['F_end']:.4g}")

print("\n=== tolerance/method robustness (SS k0=0.683095) ===")
for rt, at, meth in [(1e-8, 1e-10, 'LSODA'), (1e-10, 1e-12, 'LSODA'),
                     (1e-12, 1e-13, 'LSODA'), (1e-10, 1e-12, 'Radau'),
                     (1e-10, 1e-12, 'DOP853')]:
    a0 = k_exact_el/c
    r = run(1.0, -1/3, a0, -a0/2, rtol=rt, atol=at, method=meth)
    print(f"  {meth} rtol={rt}: y_dgn={r.get('y_dgn', float('nan')):.8g}")

print("\n=== nature of approach: f_min, slopes, action density near event (SS k0=0.683095) ===")
a0 = k_exact_el/c
r = run(1.0, -1/3, a0, -a0/2)
sol = r['sol']
xe = sol.t_events[0][0] if sol.t_events[0].size else sol.t[-1]
for dx in [0.3, 0.1, 0.03, 0.01, 0.003, 0.001]:
    x = xe + dx
    F, Fx, a, ax = sol.sol(x)
    k = c*a/F
    L = np.log((1+k)/(1-k))
    fmin = F*(1-k)
    # per-solid-angle action density at the degenerating pole (th=pi):
    # (1/4)[y^2 f_y^2 + |grad f|^2/f] at th=pi: f_y dy = (F_x - (aY')...) use
    # pole value: f = F(1-k); df/dx = Fx(1-k) - (c ax - k c... ) compute directly:
    dfdx = Fx - c*ax  # since f_pole = F - c a... wait Y10(pi) = -c => f = F - c a
    f_pole = F - c*a
    dens_rad = 0.25*dfdx**2          # y^2 f_y^2 = (df/dx)^2
    # angular gradient at pole vanishes (sin th = 0); use max over sphere instead:
    # |grad f|^2/f = F^2 k^2 sin^2/ (F(1+k cos)) -> max near th where 1+k cos small
    dens_ang_int = 0.25*(3*(a)**2/(2*F))*((2*k+(k*k-1)*L)/k**3)/(4*np.pi)  # sphere avg
    print(f"  x-xe={dx:.3f} (y={np.exp(x):.5f}): k={k:.6f} f_min={fmin:.3e} "
          f"F={F:.4f} pole action dens={dens_rad:.4g} avg ang dens={dens_ang_int:.4g}")
