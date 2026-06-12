"""C6: BC classification at the seal (independent).

Background: gamma=1, c=2*c*_3 (my value), lmax=3, fstop=0.002.

Checks:
 F1 rank-one law: 4 mu (vhat.H.vhat)/N^2 -> 1.
 F2 remainder structure: H - vv^T/(4mu): complement block bounded,
    CROSS block vhat<->complement ~ ln(1/mu)  [S1 untested].
 F3 homogeneity null vector H.X=0; X.vhat/|X| -> 0.
 F4 m=0 fluctuation ODE xi_tautau + xi_tau = 2 H(tau) xi solved on the
    frozen background: Friedrichs branch ~ tau, sigma=0 branch -> const;
    action integral of sigma=0 branch grows ~ ln(1/tau).
 F5 m=1 potential M_l1: MY formula vs S1 formula vs 2D finite-difference
    of the full P; log slope vs candidate coefficients
    (2l+1)l(l+1)/(2D) [mine], /(4D) [S1 code], /(8D) [S1 claim].
 F6 m>=2 potentials bounded.
"""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from scipy.special import lpmv
from math import factorial
from v_engine import integrate, fmin_exact, gradP, hessP, GL, Ymat

n = 4
v = np.sqrt(2*np.arange(n) + 1.0)
vhat = v/2.0                      # |v|^2 = 16
cs3 = 0.141649
c_bg = 2*cs3
sol, sealed, q = integrate(1.0, c_bg, 3, fstop=0.002, dense=True, Nq=1500)
assert sealed
qH = GL(4000, 3)
t_stop = sol.t_events[0][0]
pole = lambda t: float(sol.sol(t)[:n] @ v)
polet = lambda t: float(sol.sol(t)[n:] @ v)
v_star = abs(polet(t_stop))
t_star = t_stop + pole(t_stop)/v_star
print(f"background: c={c_bg:.6f}; t_stop={t_stop:.5f}, t*={t_star:.5f}, "
      f"v*={v_star:.4f}  (S1: t_stop 2.13424, v* ~7)")

def state(mu):
    tl = brentq(lambda t: pole(t) - mu, 0.2*t_stop, t_stop)
    return tl, sol.sol(tl)[:n]

# Dip-pole slope D = -f_u(+1)
dY1 = Ymat(np.array([1.0]), 3)[1][:, 0]

mus = (0.1, 0.03, 0.01, 0.003)
print("\n=== F1/F2: Hessian structure ===")
W = np.linalg.qr(np.column_stack([vhat, np.eye(4)[:, :3]]))[0][:, 1:]
cross_hist, comp_hist, rk1_hist = [], [], []
for mu in mus:
    tl, X = state(mu)
    H = hessP(X, qH)
    rk1 = 4*mu*float(vhat @ H @ vhat)/16.0
    R = H - np.outer(v, v)/(4*mu)
    cross = W.T @ H @ vhat          # should grow ~ ln(1/mu) per my calc
    comp = np.linalg.eigvalsh(W.T @ H @ W)
    rk1_hist.append(rk1); cross_hist.append(cross); comp_hist.append(comp)
    print(f"  mu={mu:6.3f}: rank1 ratio {rk1:.4f}; "
          f"|cross| {np.linalg.norm(cross):8.4f}; comp eigs "
          + " ".join(f"{e:+8.4f}" for e in comp))
ln = np.log(1/np.array(mus))
cr = np.array([np.linalg.norm(c) for c in cross_hist])
print(f"  cross-norm growth per unit ln(1/mu): "
      f"{(cr[-1]-cr[-2])/(ln[-1]-ln[-2]):.4f}  "
      f"(nonzero => Hess remainder NOT bounded; log cross-coupling)")
print(f"  complement-eig drift mu 0.01->0.003: "
      f"{np.abs(comp_hist[-1]-comp_hist[-2]).max():.5f} (bounded if small)")

print("\n=== F3: homogeneity null vector ===")
tl, X = state(0.003)
H = hessP(X, qH)
print(f"  |H.X|_max = {np.abs(H @ X).max():.2e}; "
      f"X.vhat/|X| = {abs(X @ vhat)/np.linalg.norm(X):.5f} (-> 0)")

print("\n=== F4: m=0 fluctuation ODE on frozen background ===")
# tau grid: background exists for mu >= 0.002 i.e. tau >= ~0.002/v*
def Hof_tau(tau):
    t = t_star - tau
    X = sol.sol(t)[:n]
    return hessP(X, GL(2000, 3))
tau0, tau1 = 0.04, 0.00032
taus = np.geomspace(tau0, tau1, 60)
Hs = [Hof_tau(tt) for tt in taus]
from scipy.interpolate import interp1d
Hflat = interp1d(np.log(taus), np.array([h.ravel() for h in Hs]).T,
                 kind='cubic', fill_value='extrapolate')
def rhs(tau, w):
    xi, et = w[:4], w[4:]
    H = Hflat(np.log(max(tau, tau1))).reshape(4, 4)
    return np.concatenate([et, -et + 2*H @ xi])  # xi'' + xi' = 2H xi
for tag, xi0, et0 in (("sigma=0 (xi=vhat, xi'=0)", vhat, np.zeros(4)),
                      ("sigma=1 (xi=tau0*vhat, xi'=vhat)", tau0*vhat, vhat)):
    # integrate DOWN in tau (toward the seal): variable tau decreasing
    s = solve_ivp(lambda T, w: -rhs(np.exp(-T), w)*np.exp(-T),
                  (np.log(1/tau0), np.log(1/tau1)),
                  np.concatenate([xi0, et0]), method='LSODA',
                  rtol=1e-9, atol=1e-12, dense_output=True)
    # report pole-component alpha = xi.vhat and action accumulation
    out = []
    act = 0.0
    Ts = np.linspace(np.log(1/tau0), np.log(1/tau1), 4000)
    al_prev = None
    acts = []
    for i, T in enumerate(Ts):
        tau = np.exp(-T)
        w = s.sol(T); xi = w[:4]
        H = Hflat(np.log(max(tau, tau1))).reshape(4, 4)
        dens = 0.25*np.dot(w[4:], w[4:]) + 0.5*float(xi @ H @ xi)
        if i > 0:
            act += dens*(tau_prev - tau)
        tau_prev = tau
        acts.append(act)
        out.append((tau, float(xi @ vhat)))
    sel = [0, 1500, 3000, 3600, 3999]
    print(f"  {tag}:")
    print("    tau:   " + " ".join(f"{out[i][0]:9.5f}" for i in sel))
    print("    alpha: " + " ".join(f"{out[i][1]:+9.5f}" for i in sel))
    print("    action(tau0->tau): "
          + " ".join(f"{acts[i]:9.4f}" for i in sel))
    # log-divergence test: action vs ln(1/tau) slope on last decade
    sl = (acts[3999] - acts[3000])/(Ts[3999] - Ts[3000])
    print(f"    d action/d ln(1/tau) (last stretch) = {sl:.4f} "
          f"(>0 const => log divergence; ->0 => finite)")

print("\n=== F5: m=1 potentials ===")
def Mlm_mine(l, m, X, q):
    K2 = 2*(2*l + 1)*factorial(l - m)/factorial(l + m)
    u = q.x
    f = X @ q.Y; fu = X @ q.dY
    P = lpmv(m, l, u)
    dP = ((l + m)*lpmv(m, l - 1, u) - l*u*lpmv(m, l, u))/(1 - u**2)
    gY2 = (1 - u**2)*dP**2 + m*m*P**2/(1 - u**2)
    T1 = (q.w @ (gY2/f))
    T2 = (q.w @ ((1 - u**2)*fu*dP*P/f**2))
    T3 = (q.w @ ((1 - u**2)*fu**2*P**2/f**3))
    # M = <T1 - 2T2 + T3> with <> = (1/2)Int du and phi-avg cos^2 = 1/2
    return (K2/4.0)*(T1 - 2*T2 + T3)

def M_fd2d(l, m, X, b_frac=0.02, Nphi=64):
    """arbitration: 2D finite-difference of full P."""
    K = np.sqrt(2*(2*l + 1)*factorial(l - m)/factorial(l + m))
    qq = GL(2000, 3)
    u = qq.x
    phi = (np.arange(Nphi) + 0.5)*2*np.pi/Nphi
    f0 = X @ qq.Y; f0u = X @ qq.dY
    P = lpmv(m, l, u)
    dP = ((l + m)*lpmv(m, l - 1, u) - l*u*lpmv(m, l, u))/(1 - u**2)
    mu = fmin_exact(X)[0]
    def Pfull(b):
        # f(u,phi) = f0 + b K P cos(m phi)
        co = np.cos(m*phi)[None, :]; si = np.sin(m*phi)[None, :]
        f = f0[:, None] + b*K*P[:, None]*co
        fu = f0u[:, None] + b*K*dP[:, None]*co
        fph = -b*K*m*P[:, None]*si
        integ = ((1 - u**2)[:, None]*fu**2 + fph**2/(1 - u**2)[:, None])/f
        return (qq.w @ integ).mean()/8.0   # (1/4)*(1/2 du)*(phi avg)
    b = b_frac*mu
    Q = (Pfull(b) + Pfull(-b) - 2*Pfull(0.0))/b**2
    return 2*Q

q2 = GL(2000, 3)
print("  mu      D       l  M_mine     M_S1form   M_fd2d")
Mlog = {1: [], 2: [], 3: []}
Ds = []
for mu in mus:
    tl, X = state(mu)
    D = -float(X @ dY1)
    Ds.append(D)
    for l in (1, 2, 3):
        Mm = Mlm_mine(l, 1, X, q2)
        Ms1 = Mm/2.0   # S1 code = (mine)/2 algebraically (shown offline)
        Mfd = M_fd2d(l, 1, X)
        Mlog[l].append(Mm)
        print(f"  {mu:5.3f} {D:8.3f}  {l}  {Mm:9.4f}  {Ms1:9.4f}  {Mfd:9.4f}")
for l in (1, 2, 3):
    A_fit = (Mlog[l][-1] - Mlog[l][-2])/(ln[-1] - ln[-2])
    Dm = np.mean(Ds[-2:])
    print(f"  l={l}: fitted log slope {A_fit:.4f}; candidates: "
          f"mine (2l+1)l(l+1)/(2D)={(2*l+1)*l*(l+1)/(2*Dm):.4f}, "
          f"S1code /(4D)={(2*l+1)*l*(l+1)/(4*Dm):.4f}, "
          f"S1claim /(8D)={(2*l+1)*l*(l+1)/(8*Dm):.4f}")

print("\n=== F6: m>=2 bounded ===")
for (l, m) in ((2, 2), (3, 2), (3, 3)):
    seq = [Mlm_mine(l, m, state(mu)[1], q2) for mu in (0.1, 0.01, 0.003)]
    print(f"  M_{l}{m} (mine): " + " ".join(f"{x:9.4f}" for x in seq)
          + f"   drift {abs(seq[-1]-seq[0]):.4f}")
