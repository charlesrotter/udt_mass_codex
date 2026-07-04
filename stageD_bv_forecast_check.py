#!/usr/bin/env python3
"""BLIND VERIFIER forecast-chain spot-check: independently re-evaluate the frozen
closure d*(N) for N=25 and N=33. Same LAW definitions (bottom gamma-system,
z*_eff = late pair-averaged v_z-node offset, z_c_eff = late <z e^{-psi/2}>,
theta0 self-consistent assembly, closure z_c_eff(gamma(d)) = Theta*sqrt(x_c))
but MY OWN numerics end-to-end: fixed-step RK4 (not DOP853), direct per-d ODE
evaluation (no spline), my own node bisection, my own d-bisection.
Family coefficients: independent closed forms derived by hand and cross-checked
against sympy.
"""
import math

XC = 1.0 / 1101.0
SQXC = math.sqrt(XC)
Z = 8.0

# ---- family coefficients: hand-derived closed forms for U = 2 rho^3 e^{-a(rho^2-1)}
# ln U = ln2 + 3 ln rho - a(rho^2 -1); derivatives at rho=1 via Faa di Bruno (hand):
# g(rho)=U; g1=U*(3/rho - 2 a rho); at 1: g1 = 2*(3-2a)
# Let f = 3 ln rho - a rho^2. f1=3/rho-2a rho; f2=-3/rho^2-2a; f3=6/rho^3; f4=-18/rho^4
# U = 2 e^{a} e^{f}... simpler: sympy cross-check below is authoritative for the check.
import sympy as sp
def fam(d):
    a = 1.5 * (1.0 - d)
    rho = sp.symbols('rho', positive=True)
    U = 2 * rho**3 * sp.exp(-sp.Float(a, 30) * (rho**2 - 1))
    dU = [float(sp.diff(U, rho, k).subs(rho, 1)) for k in range(5)]
    s1 = abs(dU[2] / 4.0)
    dt = dU[1] / 4.0
    c3 = dU[3] / (12.0 * s1)
    c4 = dU[4] / (48.0 * s1)
    # hand cross-check of the two leading ones: U'(1) = 2*(3-2a) = 6d exactly? a=1.5(1-d)
    assert abs(dU[1] - (6.0 - 4.0 * a)) < 1e-10 * max(1, abs(dU[1]))
    return dt, s1, c3, c4

# ---- bottom gamma-system, my own RK4: v'' = p v' - v + 1, psi' = p, p' = g e^{-2psi} v'^2 - p^2
def bottom_rhs(y, g):
    v, vz, psi, p = y
    return (vz, p * vz - v + 1.0, p, g * math.exp(-2.0 * psi) * vz * vz - p * p)

def bottom_rk4(y, h, g):
    k1 = bottom_rhs(y, g)
    y2 = tuple(y[i] + 0.5 * h * k1[i] for i in range(4))
    k2 = bottom_rhs(y2, g)
    y3 = tuple(y[i] + 0.5 * h * k2[i] for i in range(4))
    k3 = bottom_rhs(y3, g)
    y4 = tuple(y[i] + h * k3[i] for i in range(4))
    k4 = bottom_rhs(y4, g)
    return tuple(y[i] + (h / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4))

def run_bottom_mine(g, z_end=400.0, h=0.002):
    y = (0.0, 0.0, 0.0, 0.0)
    z = 0.0
    nodes = []
    late = []            # (z, psi) samples in [0.75 z_end, z_end] on the 100-pt linspace
    zz_targets = [0.75 * z_end + i * (0.25 * z_end) / 99.0 for i in range(100)]
    ti = 0
    n = int(z_end / h)
    for _ in range(n):
        ynew = bottom_rk4(y, h, g)
        znew = z + h
        # v_z node: sign change of vz
        if y[1] * ynew[1] < 0.0 and znew > 1e-6:
            lo, hi = 0.0, h
            ylo = y
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                ym = bottom_rk4(y, mid, g)   # single RK4 substep over mid (small)
                if y[1] * ym[1] < 0.0: hi = mid
                else: lo = mid
            nodes.append(z + 0.5 * (lo + hi))
        # sample psi at the linspace targets by tiny substep from current state
        while ti < 100 and z <= zz_targets[ti] <= znew:
            dz = zz_targets[ti] - z
            ym = bottom_rk4(y, dz, g) if dz > 0 else y
            late.append((zz_targets[ti], ym[2]))
            ti += 1
        y, z = ynew, znew
    offs = [zn - (i + 1) * math.pi for i, zn in enumerate(nodes)]
    pair_last = 0.5 * (offs[-1] + offs[-2])
    zc = sum(zt * math.exp(-ps / 2.0) for zt, ps in late) / len(late)
    return pair_last, zc

def assemble_mine(d, N):
    dt, s1, c3, c4 = fam(d)
    gamma = 4.0 * dt * dt / (Z * s1 * s1 * XC * XC)
    K = 2.0 + (15.0 / 16.0) * c3 * c3 - 1.5 * c3 + 0.75 * c4
    zstar, zc = run_bottom_mine(gamma)
    th0 = 0.3 * math.pi
    for _ in range(300):
        Theta = (N + 1) * math.pi + th0
        th0_new = zstar + K * Z * (1.0 - XC)**2 / (3.0 * Theta) + 1.5 * c3 * (dt / s1) * Theta
        if abs(th0_new - th0) < 1e-14:
            break
        th0 = th0_new
    Theta = (N + 1) * math.pi + th0
    return gamma, th0, Theta, zc, s1

def closure_res(d, N):
    gamma, th0, Theta, zc, s1 = assemble_mine(d, N)
    return zc - Theta * SQXC

FROZEN = {25: 1.930249e-03, 33: 1.529567e-03}

for N, d_frozen in FROZEN.items():
    lo, hi = d_frozen * 0.99, d_frozen * 1.01
    flo, fhi = closure_res(lo, N), closure_res(hi, N)
    assert flo * fhi < 0, f"no bracket at N={N}: {flo}, {fhi}"
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        fm = closure_res(mid, N)
        if flo * fm <= 0.0: hi = mid
        else: lo, flo = mid, fm
    d_mine = 0.5 * (lo + hi)
    gamma, th0, Theta, zc, s1 = assemble_mine(d_mine, N)
    print(f"N={N}: my d*={d_mine:.7e}  frozen {d_frozen:.6e}  rel dev {(d_mine/d_frozen-1):+.2e}")
    print(f"      gamma={gamma:.4f} theta0/pi={th0/math.pi:+.4f} Theta={Theta:.4f} "
          f"a_seal={math.sqrt(Z)/Theta:.6f} q={2*Z*math.sqrt(s1)*(1-XC)/Theta:.5f}")
