"""LEMMA D — spot-check re-shoots (2 IVP shots) of banked rungs to verify the
INTERMEDIATE claims of the averaged system on actual trajectories:
  (i)   flux law:      Phi^2 / (e^phi - x_c)  ->  4 Z C^2 sqrt|s1|  (constant, osc zone)
  (ii)  envelope law:  a_i e^{-phi_i/2} Q_i^{1/4} -> C  (same constant, at |rho-1| extrema)
  (iii) phase:         Theta_meas = int_0^{r_s} k dr,  k = e^phi sqrt(Q); vs (N+1)pi
  (iv)  ramp onset:    Phi^2 at the first extremum (how much flux the ramp contributes)
Rungs: stageB A1(m=3) Z=8 N=8 (a* = 1.4941240) and c2 A1(m=3) Z=1 N=8 (d* = 1.393766e-3).
Budget: 2 shots.
"""
import sys
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, make_risefall_slice
from scipy.integrate import solve_ivp
from scipy.signal import argrelextrema

XC = 1.0 / 1101.0

def shoot(Z, Up):
    seal = lambda r, y, *a: y[0]; seal.terminal, seal.direction = True, +1
    return solve_ivp(rhs, (0.0, 5.0e7), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                     method="LSODA", rtol=1e-10, atol=1e-12, events=[seal],
                     dense_output=True)

def analyze(tag, Z, m, a_param, N):
    U, Up, lab = make_risefall_slice(a_param, m=m)
    sol = shoot(Z, Up)
    r_s = sol.t_events[0][0]
    rr = np.linspace(0.0, r_s, 400001)
    phi, phip, rho, rhop = sol.sol(rr)
    # exact family constants at this a_param: dt = U'(1)/4, s1 = -U''(1)/4
    h = 1e-6
    dt = Up(1.0) / 4.0
    s1 = -(Up(1.0 + h) - Up(1.0 - h)) / (2 * h) / 4.0
    q = Z * rho[-1] ** 2 * phip[-1]
    Phi = Z * rho ** 2 * phip
    Q = 0.25 * Z * phip ** 2 + s1
    k = np.exp(phi) * np.sqrt(Q)
    Theta = np.trapezoid(k, rr)
    Qs = Q[-1]
    print(f"\n===== {tag}:  {lab}  Z={Z}  N={N}")
    print(f"  r_s={r_s:.2f}  rho_s={rho[-1]:.6f}  q={q:.6f}  dt={dt:.6e}  |s1|={s1:.6f}")
    print(f"  (iii) Theta_meas = {Theta:.4f} = ({Theta/np.pi:.4f}) pi ;  (N+1)pi = {(N+1)*np.pi:.4f}"
          f"  -> theta_0/pi = {Theta/np.pi - (N+1):.4f}")
    # C from the three independent routes
    C_theta = np.sqrt(Z) * s1 ** 0.25 * np.sqrt(1 - XC) / Theta          # S6 inverted
    # (i) flux law over the oscillation zone: sample at rho' nodes (staircase midpoints between)
    up_nodes = rr[1:-1][argrelextrema(np.abs(rhop[1:-1]), np.less)[0]]   # near rho'=0
    fluxC2 = []
    for rn in up_nodes:
        i = np.searchsorted(rr, rn)
        fluxC2.append(Phi[i] ** 2 / (np.exp(phi[i]) - XC) / (4 * Z * np.sqrt(s1)))
    fluxC2 = np.array(fluxC2)
    # (ii) envelope at extrema of (rho-1-offset)
    up_off = (dt - 0.25 * Z * phip ** 2) / Q          # adiabatic particular solution
    osc = rho - 1.0 - up_off
    imax = argrelextrema(np.abs(osc), np.greater)[0]
    imax = imax[np.abs(osc[imax]) > 1e-4]             # skip sub-noise early wiggles
    Cenv = np.abs(osc[imax]) * np.exp(-phi[imax] / 2.0) * Q[imax] ** 0.25
    print(f"  C routes:  C_theta(S6) = {C_theta:.5e}")
    with np.printoptions(precision=3, suppress=False):
        print(f"  (i) flux C^2/(C_theta^2) at rho'-nodes (last 10 of {len(fluxC2)}):")
        print("      ", fluxC2[-10:] / C_theta ** 2)
        print(f"  (ii) envelope C/C_theta at |osc| extrema ({len(Cenv)} found):")
        print("      ", Cenv / C_theta)
    # (iv) ramp/onset flux fraction at first counted extremum
    if len(imax):
        i0 = imax[0]
        print(f"  (iv) at 1st extremum: r={rr[i0]:.1f} ({rr[i0]/r_s:.2%} of r_s), phi={phi[i0]:.3f},"
              f" Phi^2/q^2 = {Phi[i0]**2/q**2:.4f}, e^phi = {np.exp(phi[i0]):.4f}")
        print(f"       launch check: |osc| at 1st extremum / (dt/|s1|) = {np.abs(osc[i0])/(dt/s1):.4f}"
              f"   e^{{(phi-phi_c)/2}} there = {np.exp((phi[i0]-PHI_C)/2):.2f}")
    # seal amplitude vs table
    print(f"  a_osc(seal) = |rho_s-1-u_p| = {np.abs(rho[-1]-1-up_off[-1]):.6f}"
          f"   a_pred(R1) = {q/(2*np.sqrt(Z*(1-XC))*(s1*Qs)**0.25):.6f}")

analyze("stageB N=8", Z=8.0, m=3.0, a_param=1.4941240, N=8)
analyze("c2 N=8",     Z=1.0, m=3.0, a_param=1.5 * (1.0 - 1.393766e-3), N=8)
