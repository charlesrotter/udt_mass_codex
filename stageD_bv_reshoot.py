#!/usr/bin/env python3
"""BLIND VERIFIER independent re-shoot of 3 Stage-D rungs (N=23, 30, 35).
Everything re-implemented from the EOMs printed in cell_solver_universe_T3.py's
docstring (the banked object definition) — NO reuse of the survey's scripts:
  - integrator: my own fixed-step classical RK4 (pure python floats), two step
    sizes (h, h/2) for a Richardson-style convergence check;
  - seal event: my own bisection on phi(r)=0 within the crossing step;
  - root find in d: my own bisection on f(d) = rho'(r_s);
  - counting: my own graduated-floor interior-sign-change counter
    (floors 1e-1..1e-12, 4/decade, plateau >= 2 decades).
EOMs (Z=8, potential-only sigma):
  phi'' = 4 rho'^2 e^{-2phi}/(Z rho^2) - 2 phi' rho'/rho
  rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4) U'(rho)
Family A1 m=3: U(rho)=2 rho^3 exp(-a(rho^2-1)), a = 1.5(1-d), rho_c=1,
phi_c = -ln(1101), phi'(0)=rho'(0)=0. Seal = first upward phi=0 crossing.
Bounded: 3 rungs x ~45 bisections x ~0.5s shots, single process.
"""
import math, json, time

Z = 8.0
PHI_C = -math.log(1101.0)

def rhs(y, a):
    phi, phip, rho, rhop = y
    e2p = math.exp(2.0 * phi)
    U = 2.0 * rho**3 * math.exp(-a * (rho * rho - 1.0))
    Up = U * (3.0 / rho - 2.0 * a * rho)
    phipp = 4.0 * rhop * rhop / (e2p * Z * rho * rho) - 2.0 * phip * rhop / rho
    rhopp = 2.0 * phip * rhop - 0.25 * Z * rho * e2p * phip * phip + 0.25 * e2p * Up
    return (phip, phipp, rhop, rhopp)

def rk4_step(y, h, a):
    k1 = rhs(y, a)
    y2 = tuple(y[i] + 0.5 * h * k1[i] for i in range(4))
    k2 = rhs(y2, a)
    y3 = tuple(y[i] + 0.5 * h * k2[i] for i in range(4))
    k3 = rhs(y3, a)
    y4 = tuple(y[i] + h * k3[i] for i in range(4))
    k4 = rhs(y4, a)
    return tuple(y[i] + (h / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4))

def shoot(d, h, r_max=6000.0, record=False):
    """Integrate to the first upward phi=0 crossing; return (rhop_s, seal_state, r_s, traj)."""
    a = 1.5 * (1.0 - d)
    y = (PHI_C, 0.0, 1.0, 0.0)
    r = 0.0
    traj = [(r,) + y] if record else None
    nmax = int(r_max / h) + 1
    for _ in range(nmax):
        ynew = rk4_step(y, h, a)
        rnew = r + h
        if y[0] < 0.0 <= ynew[0]:
            # refine crossing: bisection on sub-integration from y over [0,h]
            lo, hi = 0.0, h
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                ym = integrate_sub(y, mid, a)
                if ym[0] >= 0.0: hi = mid
                else: lo = mid
            r_s = r + 0.5 * (lo + hi)
            ys = integrate_sub(y, 0.5 * (lo + hi), a)
            if record:
                traj.append((r_s,) + ys)
            return ys[3], ys, r_s, traj
        y, r = ynew, rnew
        if record:
            traj.append((r,) + y)
        if y[2] < 1e-9:
            return None, y, r, traj    # collapse
    return None, y, r, traj            # no seal in range

def integrate_sub(y, dr, a, nsub=8):
    """RK4 sub-integrate a distance dr from state y (several substeps for accuracy)."""
    if dr == 0.0:
        return y
    hh = dr / nsub
    for _ in range(nsub):
        y = rk4_step(y, hh, a)
    return y

def find_root(d_lo, d_hi, h):
    f_lo, *_ = shoot(d_lo, h)
    f_hi, *_ = shoot(d_hi, h)
    assert f_lo is not None and f_hi is not None and f_lo * f_hi < 0, \
        f"no bracket: f({d_lo})={f_lo}, f({d_hi})={f_hi}"
    lo, hi, flo = d_lo, d_hi, f_lo
    for _ in range(45):
        mid = 0.5 * (lo + hi)
        fm, *_ = shoot(mid, h)
        if fm is None: raise RuntimeError("shot failed mid-bisection")
        if flo * fm <= 0.0: hi = mid
        else: lo, flo = mid, fm
    return 0.5 * (lo + hi), hi - lo

def graded_count(vals):
    """My own graduated-floor counter: interior sign changes of vals above
    relative floors 10^{-k/4}, k=4..48; plateau needs >= 9 consecutive (2 decades)."""
    fmax = max(abs(v) for v in vals)
    prof = []
    for k in range(4, 49):
        fr = 10.0 ** (-k / 4.0)
        kept = [v for v in vals if abs(v) > fr * fmax]
        c = sum(1 for u, w in zip(kept, kept[1:]) if u * w < 0.0)
        prof.append((fr, c))
    # longest plateau of identical count with length >= 9
    best = None
    i = 0
    while i < len(prof):
        j = i
        while j + 1 < len(prof) and prof[j + 1][1] == prof[i][1]:
            j += 1
        if j - i >= 8 and (best is None or (j - i) > (best[1] - best[0])):
            best = (i, j, prof[i][1])
        i = j + 1
    if best is None:
        return None, prof
    return best[2], prof

TARGETS = {   # sweep's claims, used ONLY to seed the bracket (+-0.4%) and compare after
    23: 2.0577417608e-03,
    30: 1.6590880518e-03,
    35: 1.4509827346e-03,
}

results = {}
for N, d_sweep in TARGETS.items():
    t0 = time.time()
    row = {}
    for h in (0.05, 0.025):
        d_root, wid = find_root(d_sweep * 0.996, d_sweep * 1.004, h)
        row[h] = d_root
        print(f"N={N} h={h}: d_root={d_root:.10e} (bis width {wid:.1e}) "
              f"vs sweep {d_sweep:.10e} -> rel dev {(d_root/d_sweep-1):+.3e}  [{time.time()-t0:.0f}s]",
              flush=True)
    # characterize at the h=0.025 root
    d_root = row[0.025]
    f_s, ys, r_s, traj = shoot(d_root, 0.025, record=True)
    interior = traj[1:-1]
    delta = [p[3] - 1.0 for p in interior]
    rhop = [p[4] for p in interior]
    Nd, prof_d = graded_count(delta)
    Np, prof_p = graded_count(rhop)
    rho_s = ys[2]
    q = Z * rho_s * rho_s * ys[1]
    a_seal = abs(rho_s - 1.0)
    print(f"N={N}: my N_delta={Nd} N_rhop={Np}  rho_s={rho_s:.6f} "
          f"a_seal={a_seal:.6f} q={q:.5f} r_s={r_s:.4f} phi_s={ys[0]:.2e} rhop_s={f_s:.2e}")
    # plateau sanity: show profile ends
    print(f"   N_delta profile head {[c for _,c in prof_d[:6]]} tail {[c for _,c in prof_d[-6:]]}")
    print(f"   N_rhop  profile head {[c for _,c in prof_p[:6]]} tail {[c for _,c in prof_p[-6:]]}")
    results[N] = dict(d_root_h05=row[0.05], d_root_h025=row[0.025], d_sweep=d_sweep,
                      N_delta=Nd, N_rhop=Np, rho_s=rho_s, q=q, a_seal=a_seal, r_s=r_s)

json.dump(results, open("/home/udt-admin/udt_mass_codex/stageD_bv_reshoot_results.json", "w"), indent=1)
print("\n-> stageD_bv_reshoot_results.json")
