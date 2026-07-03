"""bv10_E3_bottom.py -- integrate the claimed bottom system independently:
    v_zz = p v_z - v + 1 ;  psi_z = p ;  p_z = gamma e^{-2 psi} v_z^2 - p^2 ;  zero ICs.
Extract:
  z*_eff(gamma)  = lim_n (zeta_n - n pi), zeta_n = n-th zero of v_z (n=1 at ~pi for gamma=0)
  z_c_eff(gamma) = lim zeta * e^{-psi/2}
gamma per rung = 4 dt^2 / (Z s1^2 x_c^2), dt = m d*/2, s1 = |[(m-2a*)^2 - m - 2a*]/2|, a* = (m/2)(1-d*).
"""
import numpy as np
from scipy.integrate import solve_ivp

XC = 1.0/1101.0

def rhs(z, y, gamma):
    v, vz, psi, p = y
    return [vz, p*vz - v + 1.0, p, gamma*np.exp(-2.0*psi)*vz*vz - p*p]

def run_bottom(gamma, z_end=400.0, rtol=1e-11, atol=1e-13):
    ev = lambda z, y, g: y[1]           # v_z zeros
    ev.direction = 0
    sol = solve_ivp(rhs, (0.0, z_end), [0.0, 0.0, 0.0, 0.0], args=(gamma,),
                    method="DOP853", rtol=rtol, atol=atol, events=[ev],
                    dense_output=True, max_step=0.05)
    zn = sol.t_events[0]
    zn = zn[zn > 1e-6]                   # drop the trivial zero at launch
    offs = zn - np.arange(1, len(zn)+1)*np.pi
    # z_c: fit psi ~ 2 ln(zeta) - 2 ln(z_c) at large zeta
    zz = np.linspace(0.7*z_end, z_end, 200)
    vv = sol.sol(zz)
    zc_run = zz*np.exp(-vv[2]/2.0)
    return zn, offs, zc_run, sol

def tail_limit(seq):
    """Average the last few and estimate residual trend."""
    s = np.asarray(seq, float)
    return s[-1], s[-1] - s[-2], np.mean(s[-5:])

if __name__ == "__main__":
    print("=== sanity gamma -> 0 (expect offsets -> 0) ===")
    zn, offs, zc, _ = run_bottom(1e-8, z_end=60.0)
    print("  first offsets/pi:", np.round(offs[:5]/np.pi, 6))

    print("\n=== gamma grid: z*_eff and z_c_eff ===")
    print("gamma    z*_eff/pi (last, half-sum)   z_c_eff (last, mean5)   d(off)")
    for gamma in (0.5, 1.0, 1.5, 2.0, 2.334, 2.358, 2.5, 3.0, 4.0, 6.0, 10.0):
        zn, offs, zc, _ = run_bottom(gamma)
        # offsets oscillate as they converge -> average consecutive pairs
        pair = 0.5*(offs[1:] + offs[:-1])
        zstar = pair[-1]
        zc_l, zc_d, zc_m = tail_limit(zc)
        print(f"{gamma:7.3f}  {offs[-1]/np.pi:+.5f} {pair[-1]/np.pi:+.5f}      "
              f"{zc_l:.5f} {zc_m:.5f}          {(offs[-1]-offs[-2])/np.pi:+.2e}")

    print("\n=== rung gammas (computed from banked d* pins ONLY) ===")
    def fam_m(mm, d):
        a = (mm/2.0)*(1.0 - d)
        f1 = mm - 2.0*a
        dt = f1/2.0
        s1 = abs((f1*f1 - mm - 2.0*a)/2.0)
        return a, dt, s1
    rungs = [
        ("stageB Z8 m3 N=8",  8.0, 3.0, 0.003917043, 8),
        ("c2     Z1 m3 N=8",  1.0, 3.0, 0.001393766, 8),
        ("c5     Z8 m4 N=8",  8.0, 4.0, 0.003914956, 8),
        ("c1     Z8 m2 N=8",  8.0, 2.0, 0.003919133, 8),
        ("stageB Z8 m3 N=4",  8.0, 3.0, 0.005166481, 4),
        ("stageB Z8 m3 N=16", 8.0, 3.0, 0.002663394, 16),
        ("stageB Z8 m3 N=22", 8.0, 3.0, 0.002128889, 22),
        ("c2     Z1 m3 N=4",  1.0, 3.0, 0.001853444, 4),
    ]
    print("rung                Z  m   d*          gamma     z*_eff/pi   z_c_eff")
    out = {}
    for name, Z, mm, d, N in rungs:
        a, dt, s1 = fam_m(mm, d)
        gamma = 4.0*dt*dt/(Z*s1*s1*XC*XC)
        zn, offs, zc, _ = run_bottom(gamma)
        pair = 0.5*(offs[1:] + offs[:-1])
        zc_l, zc_d, zc_m = tail_limit(zc)
        out[name] = (gamma, pair[-1], zc_m, s1, dt, a)
        print(f"{name:18s} {Z:3.0f} {mm:2.0f}  {d:.9f}  {gamma:8.4f}  {pair[-1]/np.pi:+.5f}   {zc_m:.5f}")
