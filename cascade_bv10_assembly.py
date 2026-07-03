"""bv10_assembly.py -- E4/E3/E5 final numbers:
 (1) assembled theta0 = z*_eff(gamma) + SigmaP  vs my direct measurements
 (2) quantization closure z_c_eff(gamma) vs Theta*sqrt(x_c)
 (3) d*(N) ladder inversion (predict d* from the closure; compare banked pins)
 (4) handover/overlap quantification (bottom transient vs per-cycle P_n turn-on)
Only banked pins + my own E2 formula + my own bottom-system integrations are used.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
import sympy as sp

XC = 1.0/1101.0
SQXC = np.sqrt(XC)

# ---------------- bottom system ----------------
def rhs(z, y, gamma):
    v, vz, psi, p = y
    return [vz, p*vz - v + 1.0, p, gamma*np.exp(-2.0*psi)*vz*vz - p*p]

def run_bottom(gamma, z_end=400.0):
    ev = lambda z, y, g: y[1]
    ev.direction = 0
    sol = solve_ivp(rhs, (0.0, z_end), [0.0]*4, args=(gamma,), method="DOP853",
                    rtol=1e-11, atol=1e-13, events=[ev], dense_output=True, max_step=0.05)
    zn = sol.t_events[0]; zn = zn[zn > 1e-6]
    offs = zn - np.arange(1, len(zn)+1)*np.pi
    pair = 0.5*(offs[1:] + offs[:-1])
    zz = np.linspace(0.75*z_end, z_end, 100)
    zc = float(np.mean(zz*np.exp(-sol.sol(zz)[2]/2.0)))
    return float(pair[-1]), zc, offs

# spline z*(gamma), z_c(gamma) on a grid
gg = np.array([0.4,0.5,0.6,0.688,0.8,0.9,1.0,1.078,1.2,1.4,1.6,1.8,2.0,2.2,2.334,
               2.5,2.7,3.0,3.5,4.066,4.5])
zs, zc = [], []
for g in gg:
    a, b, _ = run_bottom(g)
    zs.append(a); zc.append(b)
zstar_f = CubicSpline(gg, zs)
zc_f = CubicSpline(np.log(gg), np.log(zc))
def zc_of_gamma(g): return float(np.exp(zc_f(np.log(g))))
def zstar_of_gamma(g): return float(zstar_f(g))

# ---------------- family coefficients (exact, sympy) ----------------
def fam(m, d):
    a_ = (m/2.0)*(1.0 - d)
    rho = sp.symbols('rho', positive=True)
    U = 2*rho**m*sp.exp(-sp.Float(a_)*(rho**2 - 1))
    dU = [float(sp.diff(U, rho, k).subs(rho, 1)) for k in range(5)]
    s1 = abs(dU[2]/4.0)
    dt = dU[1]/4.0
    c3 = dU[3]/(12.0*s1)
    c4 = dU[4]/(48.0*s1)
    return dt, s1, c3, c4

def assemble(Z, m, d, N, theta0_guess=0.3*np.pi):
    """theta0 = z*(gamma) + K*Z*(1-xc)^2/(3 Theta) + (3/2) c3 dhat Theta, Theta self-consistent."""
    dt, s1, c3, c4 = fam(m, d)
    dh = dt/s1
    gamma = 4.0*dt*dt/(Z*s1*s1*XC*XC)
    K = 2.0 + (15.0/16.0)*c3*c3 - 1.5*c3 + 0.75*c4
    th0 = theta0_guess
    for _ in range(50):
        Theta = (N+1)*np.pi + th0
        SP_E = K*Z*(1.0-XC)**2/(3.0*Theta)
        SP_d = 1.5*c3*dh*Theta
        th0_new = zstar_of_gamma(gamma)*np.pi/np.pi + SP_E + SP_d  # z* returned in rad? (it's rad)
        th0_new = zstar_of_gamma(gamma) + SP_E + SP_d
        if abs(th0_new - th0) < 1e-14: break
        th0 = th0_new
    Theta = (N+1)*np.pi + th0
    return dict(gamma=gamma, zstar=zstar_of_gamma(gamma), SP_E=SP_E, SP_d=SP_d,
                theta0=th0, Theta=Theta, K=K, c3=c3, c4=c4, dh=dh, s1=s1)

print("=== (1) assembled theta0 vs direct measurement ===")
rows = [
    ("Z8 m3 N=8 ", 8.0, 3, 0.003917043, 8, 0.320867),
    ("Z1 m3 N=8 ", 1.0, 3, 0.001393766, 8, 0.2533),      # banked direct measurement
    ("Z8 m4 N=8 ", 8.0, 4, 0.003914956, 8, 0.332005),    # my shot (not in claimed test set)
    ("Z8 m2 N=8 ", 8.0, 2, 0.003919133, 8, 0.309724),    # my shot
    ("Z8 m3 N=22", 8.0, 3, 0.002128889, 22, 0.161471),   # my shot
]
tab = {}
for name, Z, m, d, N, meas in rows:
    A = assemble(Z, m, d, N)
    tab[name] = A
    print(f"{name}: gamma={A['gamma']:.4f} z*={A['zstar']/np.pi:.5f}pi SP_E={A['SP_E']/np.pi:.5f}pi "
          f"SP_d={A['SP_d']/np.pi:.5f}pi -> pred {A['theta0']/np.pi:.4f}pi  meas {meas:.4f}pi  "
          f"diff {(A['theta0']/np.pi-meas):+.4f}pi ({100*(A['theta0']/np.pi-meas)/meas:+.1f}%)")

print()
print("=== (2) quantization closure z_c_eff(gamma) vs Theta*sqrt(x_c) ===")
meas_Theta = {"Z8 m3 N=8 ": 29.282368, "Z8 m4 N=8 ": 29.317359,
              "Z8 m2 N=8 ": 29.247362, "Z8 m3 N=22": 72.763907,
              "Z1 m3 N=8 ": (8+1.2533)*np.pi}
for name, Z, m, d, N, meas in rows:
    g = tab[name]['gamma']
    zc_v = zc_of_gamma(g)
    rhs_v = meas_Theta[name]*SQXC
    print(f"{name}: z_c_eff={zc_v:.5f}  Theta*sqrt(xc)={rhs_v:.5f}  ratio={zc_v/rhs_v:.5f} "
          f"({100*(zc_v/rhs_v-1):+.2f}%)")

print()
print("=== (3) d*(N) ladder inversion, stageB family (Z8 m3) + c2 (Z1 m3) ===")
banked = {(8.0,3,4): 0.005166481, (8.0,3,8): 0.003917043, (8.0,3,16): 0.002663394,
          (8.0,3,22): 0.002128889, (1.0,3,8): 0.001393766, (1.0,3,4): 0.001853444}
def closure_res(d, Z, m, N):
    A = assemble(Z, m, d, N)
    return zc_of_gamma(A['gamma']) - A['Theta']*SQXC
for (Z, m, N), dstar in banked.items():
    try:
        d_pred = brentq(closure_res, 0.5*dstar, 1.6*dstar, args=(Z, m, N), xtol=1e-12)
        print(f"Z{Z:.0f} m{m} N={N:2d}: d_pred={d_pred:.9f}  banked d*={dstar:.9f}  "
              f"err={100*(d_pred/dstar-1):+.2f}%")
    except ValueError as e:
        print(f"Z{Z:.0f} m{m} N={N:2d}: no root in bracket ({e})")

print()
print("=== (4) handover: bottom-system transient vs per-cycle P_n turn-on (Z8 m3 N=8) ===")
g = tab["Z8 m3 N=8 "]['gamma']
zst, zcv, offs = run_bottom(g)
pair = 0.5*(offs[1:] + offs[:-1])
print("bottom pair-averaged offsets (pi units) vs node n:")
print("  n:      ", " ".join(f"{i+1:7d}" for i in range(min(10, len(pair)))))
print("  off/pi: ", " ".join(f"{o/np.pi:7.4f}" for o in pair[:10]))
print("  (z*_inf = %.4f pi; transient residual per node = off_n - z*_inf)" % (zst/np.pi))
# P_n at the same nodes: E_n = E_s*(n/(N+1))^2 approx (flux law), E_s = Z(1-xc)^2/Theta^2
A = tab["Z8 m3 N=8 "]
Th = meas_Theta["Z8 m3 N=8 "]
E_s = 8.0*(1-XC)**2/Th**2
print("  P_n/pi (E-part formula) at n=1..10:",
      " ".join(f"{(A['K']*E_s*(n/9.0)**2 + 1.5*A['c3']*A['dh']):7.4f}" for n in range(1, 11)))
res_trans = np.abs(pair[:12] - zst)
Pn = np.array([A['K']*E_s*(n/9.0)**2 + 1.5*A['c3']*A['dh'] for n in range(1, 13)])
both = np.minimum(res_trans/np.pi, Pn)
print(f"  overlap metric sum_n min(|transient_n|, P_n)/pi = {np.sum(both):.5f}  (pi units)")
