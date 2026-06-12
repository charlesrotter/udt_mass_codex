"""C2: the gauge proof. Attack lines:
 (i) uniqueness of continuation of the interface jet (Lipschitz analysis +
     numeric forward/backward shooting consistency),
 (ii) scale covariance: threshold surface measured at an outer radius Y maps
     exactly to the interface threshold (X1 ratio 1.00003),
 (iii) amplitude scaling is NOT a symmetry (check), so the rescaling used
     must be the y-shift only.
"""
import numpy as np
from el_core import run_flow, rhs, classify, threshold, SQ3, ev_seal, ev_Fzero
from scipy.integrate import solve_ivp

# (i) Lipschitz/branch analysis numeric probe: integrate inward to t1, then
# back outward; recover jet?  Do it across an F=1 crossing and near large kappa.
def roundtrip(gamma, c, t1):
    sol, sealed = run_flow(gamma, c, Tmax=t1, rtol=1e-12, atol=1e-14)
    u1 = sol.y[:, -1]
    back = solve_ivp(rhs, (sol.t[-1], 0.0), u1, method='LSODA',
                     rtol=1e-12, atol=1e-14, max_step=1.0)
    u0 = back.y[:, -1]
    err = np.abs(u0 - np.array([1.0, gamma, 0.0, c])).max()
    k1 = SQ3*u1[2]/u1[0]
    return err, k1

for gamma, c, t1 in [(1/3, 0.05, 3.0), (0.0, 0.1, 1.0), (1/3, 0.19, 1.2), (1/3, 0.036, 8.0)]:
    err, k1 = roundtrip(gamma, c, t1)
    print(f"roundtrip g={gamma:.4f} c={c} t1={t1}: jet recovery err={err:.2e} "
          f"(kappa at turn={k1:.4f})")

# near-seal roundtrip (kappa close to 1: Lipschitz degrading)
sol, sealed = run_flow(1/3, 0.2, Tmax=60.0, rtol=1e-12, atol=1e-14, dense=True)
tseal = sol.t[-1]
for frac in [0.9, 0.99, 0.999]:
    t1 = tseal*frac
    u1 = sol.sol(t1)
    back = solve_ivp(rhs, (t1, 0.0), u1, method='LSODA', rtol=1e-12, atol=1e-14,
                     max_step=1.0)
    u0 = back.y[:, -1]
    err = np.abs(u0 - np.array([1.0, 1/3, 0.0, 0.2])).max()
    k1 = SQ3*u1[2]/u1[0]
    print(f"near-seal roundtrip frac={frac}: kappa={k1:.8f} err={err:.2e}")

# (ii) scale covariance: the t-system is autonomous => starting the same jet
# at outer radius Y and at 1 gives identical threshold. Verify numerically by
# integrating in y directly from Y=3.7 (no t-shift trick: raw y-integration).
def rhs_y(y, u):
    F, Fp, A, Ap = u
    k = SQ3*A/F
    k = min(max(k, -1+1e-15), 1-1e-15)
    L = np.log((1+k)/(1-k))
    H = L/(2*k) - 1 if abs(k) > 1e-4 else k*k/3
    Pa = SQ3*(L*(1+k*k)-2*k)/(8*k*k) if abs(k) > 1e-4 else SQ3*k/3
    return [Fp, (-H - 2*y*Fp)/y**2, Ap, (2*Pa - 2*y*Ap)/y**2]

def ev_seal_y(y, u): return SQ3*u[2]/u[0] - (1-1e-9)
ev_seal_y.terminal = True

def classify_at_Y(gamma, c, Y):
    # same JET in scale-covariant variables: F(Y)=1, Y F'(Y) = -gamma,
    # a(Y)=0, Y a'(Y) = -c   (t-jet (F,F_t,a,a_t)=(1,g,0,c) at t-origin ln(1/Y))
    u0 = [1.0, -gamma/Y, 0.0, -c/Y]
    sol = solve_ivp(rhs_y, (Y, Y*np.exp(-60)), u0, method='LSODA',
                    events=[ev_seal_y], rtol=1e-11, atol=1e-13)
    return 'TERM' if len(sol.t_events[0]) else 'SAT'

gamma = 1/3
Y = 3.7
lo, hi = 0.02, 0.06
assert classify_at_Y(gamma, lo, Y) == 'SAT' and classify_at_Y(gamma, hi, Y) == 'TERM'
while hi-lo > 1e-6*hi:
    m = 0.5*(lo+hi)
    if classify_at_Y(gamma, m, Y) == 'TERM': hi = m
    else: lo = m
cY = 0.5*(lo+hi)
c1 = threshold(gamma, 0.02, 0.06, tol_rel=1e-6, Tmax=80.0)
print(f"\nscale covariance: c*(at Y=3.7, rescaled jet)={cY:.7f}  c*(at 1)={c1:.7f} "
      f" ratio={cY/c1:.6f} (X1 seal ratio 1.00003)")

# (iii) amplitude scaling is NOT a symmetry: (F,a)->(2F,2a) same kappa but
# (y^2 F')' scales while RHS doesn't. Show classification changes:
def classify_amp(gamma, c, lam):
    from el_core import run_flow as rf
    sol, sealed = rf(gamma*1.0, c, Tmax=60.0, F0=lam, a0=0.0)
    # note: F0=lam, F_t=gamma, a_t=c  -> rescaled amplitude, same jet angles? crude probe
    return 'TERM' if sealed else 'SAT'
print("amplitude-rescaled jet (F0=2, same gamma,c near c*):",
      classify_amp(gamma, c1*1.05, 2.0), " vs original:", 'TERM')
