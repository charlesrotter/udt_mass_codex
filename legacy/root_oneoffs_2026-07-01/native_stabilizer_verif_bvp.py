import numpy as np
from scipy.integrate import solve_bvp

# Independent BVP solver for the charge-1 hedgehog profile, flat phi=0.
# Energy (per the derived radial integrands, flat):
#   E2 ~ xi/2 * integral [ r^2 Theta'^2 (2 + sin^2T) ... ] -- use the
#   standard Skyrme hedgehog energy functional that follows from L2+L4.
# Use the well-known reduced energy (flat) for the hedgehog n with profile T(r):
#   E = 4pi integral_0^inf { (xi/2)[ r^2 T'^2 + 2 sin^2 T ]
#                          + (kappa/2)[ 2 sin^2 T T'^2 + sin^4 T / r^2 ] } dr
# (This is the standard Skyrme-model hedgehog energy; L2 gives r^2T'^2+2sin^2T,
#  L4 gives sin^2T(2T'^2 + sin^2T/r^2). We DERIVE its EL and solve.)
# EL of  f = a(r,T) T'^2 + b(r,T):  d/dr(2 a T') - a_T T'^2 - b_T = 0.
# a = (xi/2) r^2 + kappa sin^2 T ;  b = xi sin^2 T + (kappa/2) sin^4 T / r^2

def make_rhs(xi, kappa):
    def a(r,T):   return 0.5*xi*r**2 + kappa*np.sin(T)**2
    def aT(r,T):  return kappa*2*np.sin(T)*np.cos(T)
    def bT(r,T):  return xi*2*np.sin(T)*np.cos(T) + (kappa/2)*4*np.sin(T)**3*np.cos(T)/r**2
    def rhs(r, y):
        T, Tp = y
        # d/dr(2 a T') = a_T T'^2 + b_T
        # 2 a T'' + 2 a_r T' + 2 a_T T' * T' = a_T T'^2 + b_T   (a_r from r^2 term)
        ar = xi*r
        Tpp = (aT(r,T)*Tp**2 + bT(r,T) - 2*ar*Tp - 2*aT(r,T)*Tp*Tp) / (2*a(r,T))
        return np.vstack([Tp, Tpp])
    return rhs

def bc(ya, yb):
    return np.array([ya[0]-np.pi, yb[0]-0.0])  # Theta(core)=pi, Theta(seal)=0

def solve_profile(xi, kappa, rc=1e-3, rmax=None, N=4000):
    L = np.sqrt(kappa/xi)
    if rmax is None: rmax = rc + 40*L
    r = np.linspace(rc, rmax, N)
    # initial guess: linear pi->0
    Tg = np.pi*(1 - (r-rc)/(rmax-rc))
    Tpg = np.full_like(r, -np.pi/(rmax-rc))
    y0 = np.vstack([Tg, Tpg])
    sol = solve_bvp(make_rhs(xi,kappa), bc, r, y0, max_nodes=200000, tol=1e-8)
    return sol, L

def width_half(sol, rc):
    # find r where Theta = pi/2
    rs = np.linspace(sol.x[0], sol.x[-1], 20000)
    Ts = sol.sol(rs)[0]
    idx = np.argmin(np.abs(Ts - np.pi/2))
    return rs[idx]

def energies(sol, xi, kappa):
    rs = np.linspace(sol.x[0], sol.x[-1], 40000)
    T, Tp = sol.sol(rs)
    e2 = xi*(rs**2*Tp**2 + 2*np.sin(T)**2)        # *4pi/2 factors common
    e4 = kappa*(2*np.sin(T)**2*Tp**2 + np.sin(T)**4/rs**2)
    E2 = np.trapz(e2, rs); E4 = np.trapz(e4, rs)
    return E2, E4

print("=== Width vs sqrt(kappa/xi), flat, virial ===")
for kappa in [0.25, 1.0, 4.0, 9.0]:
    xi = 1.0
    sol, L = solve_profile(xi, kappa)
    if not sol.success:
        print(f"kappa={kappa}: BVP FAILED ({sol.message})"); continue
    rc = sol.x[0]
    w = width_half(sol, rc)
    E2, E4 = energies(sol, xi, kappa)
    print(f"kappa={kappa:4}: (w-rc)/L = {(w-rc)/L:.3f}  E2/E4 = {E2/E4:.4f}  resid~{sol.rms_residuals.max():.1e}")

print("=== Cell-size independence (kappa=xi=1) ===")
for mult in [8, 20, 40]:
    xi=kappa=1.0; L=1.0; rc=1e-3
    sol,_=solve_profile(xi,kappa, rc=rc, rmax=rc+mult*L)
    w=width_half(sol,rc)
    print(f"cell={mult}L: (w-rc)/L = {(w-rc)/L:.3f}  success={sol.success}")
