"""C4: boundary layer verification (independent engine).
 (a) on-flow gradient log law: slope of P_X vs ln(1/mu) -> -Y_X(1)/4,
     ALL components at lmax=3 (closed form already verified at lmax=1).
 (b) layer slope: d(mu_tt - mu_t)/d ln(1/mu) -> -N^2/2 = -2, -4.5, -8.
 (c) touchdown exponent p = -mu_t tau / mu -> 1 on lmax=3 flow.
 (d) sign/size of the tau^2 ln(1/tau) correction: S1 claims
     mu = v* tau + (N^2/4) tau^2 ln(1/tau); my analytics give MINUS.
"""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from v_engine import integrate, fmin_exact, gradP, GL, Ymat

flows = {}
for lmax in (1, 2, 3):
    sol, sealed, q = integrate(1.0, 0.30, lmax, fstop=0.002, dense=True,
                               Nq=1500)
    assert sealed
    flows[lmax] = (sol, q)

print("=== (a) gradient log law, lmax=3: slope of P_X vs ln(1/mu) ===")
sol, q = flows[3]
n = 4
v = np.sqrt(2*np.arange(n) + 1.0)        # Y_l(u=+1)
t_stop = sol.t_events[0][0]
pole = lambda t: float(sol.sol(t)[:n] @ v)
mus = (0.1, 0.03, 0.01, 0.003)
G = []
for mu in mus:
    tl = brentq(lambda t: pole(t) - mu, 0.2*t_stop, t_stop)
    G.append(gradP(sol.sol(tl)[:n], q))
G = np.array(G); ln = np.log(1/np.array(mus))
slopes = (G[-1] - G[-2])/(ln[-1] - ln[-2])
print("  measured slopes:", " ".join(f"{s:+.4f}" for s in slopes))
print("  predicted -Y/4 :", " ".join(f"{s:+.4f}" for s in -v/4))

print("\n=== (b) layer coefficient -N^2/2 per truncation ===")
for lmax in (1, 2, 3):
    sol, q = flows[lmax]
    n = lmax + 1
    vv = np.sqrt(2*np.arange(n) + 1.0)
    t_stop = sol.t_events[0][0]
    pol = lambda t: float(sol.sol(t)[:n] @ vv)
    rows = []
    for mu in (0.03, 0.01, 0.003):
        tl = brentq(lambda t: pol(t) - mu, 0.2*t_stop, t_stop)
        g = gradP(sol.sol(tl)[:n], q)
        rows.append(2*float(g @ vv))     # = mu_tt - mu_t
    s = (rows[-1] - rows[-2])/(np.log(1/0.003) - np.log(1/0.01))
    print(f"  lmax={lmax}: slope {s:+.4f}  target {-(lmax+1)**2/2:+.1f}"
          f"  (ratio {s/(-(lmax+1)**2/2):.4f})")

print("\n=== (c)+(d) touchdown on lmax=3 flow ===")
sol, q = flows[3]
n = 4; vv = np.sqrt(2*np.arange(n) + 1.0)
t_stop = sol.t_events[0][0]
z = sol.sol(t_stop)
mu_c, mut_c = float(z[:n] @ vv), float(z[n:] @ vv)
# refine t* by integrating the layer ODE with frozen remainder from cutoff
N2 = 16.0
g = gradP(z[:n], q)
R = 2*float(g @ vv) + (N2/2)*np.log(1/mu_c)
def lay(t, w):
    return [w[1], w[1] - (N2/2)*np.log(1/max(w[0], 1e-16)) + R]
evd = lambda t, w: w[0] - 1e-10
evd.terminal, evd.direction = True, -1
ls = solve_ivp(lay, (0, 2.0), [mu_c, mut_c], rtol=1e-12, atol=1e-15,
               events=evd, max_step=0.001)
tstar = t_stop + ls.t_events[0][0]
vstar = abs(ls.y_events[0][0][1])
print(f"t* = {tstar:.6f}, v* = {vstar:.4f}")
print("  tau        mu          p=-mu_t*tau/mu   (mu-v*tau)/(tau^2 ln(1/tau))")
for tau in (0.05, 0.02, 0.01, 0.005, 0.003):
    t = tstar - tau
    if t > t_stop:   # past cutoff: use layer ODE solution
        idx = np.argmin(np.abs(ls.t - (t - t_stop)))
        mu, mut = ls.y[0][idx], ls.y[1][idx]
        src = "layerODE"
    else:
        zz = sol.sol(t)
        mu, mut = float(zz[:n] @ vv), float(zz[n:] @ vv)
        src = "flow"
    p = -mut*tau/mu
    corr = (mu - vstar*tau)/(tau**2*np.log(1/tau))
    print(f"  {tau:7.4f}  {mu:10.6f}   {p:8.4f}        {corr:+9.3f}  [{src}]"
          f"   (S1 sign claim: +N^2/4 = +4; my analytics: -4)")
