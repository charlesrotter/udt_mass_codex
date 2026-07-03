"""bv14 blind spot-verifier: background shots for the 5 table rows.
One IVP shot per rung (LSODA, rtol=1e-12, atol=1e-14, dense_output).
Everything downstream is evaluated off the single dense interpolant -> no extra shots.
Saves per rung: seal scalars + Gauss-point fields for grids {400, 800, M, 2M} + node
phi',rho' (translation vector) + fine-grid fields (continuum-form validation).
"""
import numpy as np, json, time, os
from scipy.integrate import solve_ivp

SCR = os.path.dirname(os.path.abspath(__file__))
LN1101 = float(np.log(1101.0))
PHI_C = -LN1101

ROWS = [
    dict(tag="row1_m3Z8_belowN0",  m=3.0, Z=8.0, a=1.4813439655),
    dict(tag="row2_m3Z8_aboveN0",  m=3.0, Z=8.0, a=1.5099953390),
    dict(tag="row3_m3Z1_fund",     m=3.0, Z=1.0, a=1.4942743252),
    dict(tag="row4_m3Z8_belowN15", m=3.0, Z=8.0, a=1.4958369026),
    dict(tag="row5_m2Z8_fund",     m=2.0, Z=8.0, a=0.9860738239),
]

def makeU(a, m):
    def U(rho):   return 2.0 * rho**m * np.exp(-a*(rho*rho - 1.0))
    def Up(rho):  return U(rho) * (m/rho - 2.0*a*rho)
    def Upp(rho): return Up(rho)*(m/rho - 2.0*a*rho) + U(rho)*(-m/rho**2 - 2.0*a)
    return U, Up, Upp

def rhs(r, y, Z, Up):
    phi, phip, rho, rhop = y
    e2p = np.exp(2.0*phi)
    sigma = 0.25 * e2p * Up(rho)
    phipp = 4.0*rhop*rhop/(e2p*Z*rho*rho) - 2.0*phip*rhop/rho
    rhopp = 2.0*phip*rhop - 0.25*Z*rho*e2p*phip*phip + sigma
    return [phip, phipp, rhop, rhopp]

LEDGER = {"budget_declared": "5 primary + up to 3 spares (hard cap 8)", "shots": []}

def shoot(row, r_max, rtol, atol):
    U, Up, Upp = makeU(row["a"], row["m"])
    seal = lambda r, y, *a: y[0]
    seal.terminal, seal.direction = True, +1
    collapse = lambda r, y, *a: y[2] - 1e-9
    collapse.terminal, collapse.direction = True, -1
    t0 = time.time()
    sol = solve_ivp(rhs, (0.0, r_max), [PHI_C, 0.0, 1.0, 0.0], args=(row["Z"], Up),
                    method="LSODA", rtol=rtol, atol=atol, events=[seal, collapse],
                    dense_output=True)
    dt = time.time() - t0
    status = "no-seal"
    if sol.t_events[1].size: status = "collapse"
    elif sol.t_events[0].size: status = "seal"
    LEDGER["shots"].append(dict(tag=row["tag"], r_max=r_max, rtol=rtol, atol=atol,
                                status=status, wall_s=round(dt, 1)))
    return sol, status

GAUSS = 0.5/np.sqrt(3.0)   # 2-pt Gauss offsets +-1/(2 sqrt 3) around element midpoint (in h units)

for row in ROWS:
    tag = row["tag"]; a, m, Z = row["a"], row["m"], row["Z"]
    U, Up, Upp = makeU(a, m)
    sol, status = shoot(row, r_max=5.0e4, rtol=1e-12, atol=1e-14)
    print(f"[{tag}] status={status}")
    if status != "seal":
        print(f"  !! {tag}: no seal within r_max — spare shot decision needed"); continue
    r_s = float(sol.t_events[0][0])
    phi_s, phip_s, rho_s, rhop_s = [float(v) for v in sol.y_events[0][0]]
    q = Z * rho_s**2 * phip_s
    # EOM-exact rho'' at seal
    rhopp_s = float(rhs(r_s, [phi_s, phip_s, rho_s, rhop_s], Z, Up)[3])
    Lrho_s = -4.0 * rhopp_s
    Lrho_alt = Z * rho_s * phip_s**2 - Up(rho_s)         # continuum L_rho at seal (phi_s=0)
    Up1 = float(Up(1.0)); Upp1 = float(Upp(1.0))
    s1 = Upp1 / 4.0
    M = int(max(800, np.ceil(40.0 * r_s * np.sqrt(abs(s1)) / (2.0*np.pi))))
    cons_res = U(rho_s) - (2.0 - q*q/(2.0*Z*rho_s**2))
    # H drift over the cell (sanity)
    rr = np.linspace(0.0, r_s, 4001)
    ph, php, rh, rhp = sol.sol(rr)
    H = 0.5*Z*rh**2*php**2 - 2.0*rhp**2/np.exp(2.0*ph) - 2.0 + U(rh)
    scal = dict(tag=tag, a=a, m=m, Z=Z, r_s=r_s, phi_s=phi_s, phip_s=phip_s,
                rho_s=rho_s, rhop_s=rhop_s, q=q, Lrho_s=Lrho_s, Lrho_alt=Lrho_alt,
                Up1=Up1, Upp1=Upp1, s1=s1, M=M, cons_res=cons_res,
                H_drift=float(np.max(np.abs(H))),
                ms_seal=float(rh[-1]*(1-rhp[-1]**2/np.exp(2*ph[-1]))/rh[-1]))
    print("  " + json.dumps({k: v for k, v in scal.items() if k != 'tag'}, default=float))
    arrays = {}
    grids = sorted({400, 800, M, 2*M})
    for Mg in grids:
        h = r_s / Mg
        rn = np.arange(Mg+1) * h
        mid = (np.arange(Mg) + 0.5) * h
        rg = np.concatenate([mid - GAUSS*h, mid + GAUSS*h])   # [gp1 all elems, gp2 all elems]
        yg = sol.sol(rg); yn = sol.sol(rn)
        arrays[f"g{Mg}_gp_y"] = yg          # 4 x 2Mg
        arrays[f"g{Mg}_node_phip"] = yn[1]
        arrays[f"g{Mg}_node_rhop"] = yn[3]
    # fine grid for continuum-form quadrature validation
    rf = np.linspace(0.0, r_s, 200001)
    arrays["fine_r"] = rf
    arrays["fine_y"] = sol.sol(rf)
    np.savez_compressed(os.path.join(SCR, f"bv14_bg_{tag}.npz"), **arrays)
    scal["grids"] = grids
    with open(os.path.join(SCR, f"bv14_bg_{tag}.json"), "w") as f:
        json.dump(scal, f, indent=1, default=float)

with open(os.path.join(SCR, "bv14_shot_ledger.json"), "w") as f:
    json.dump(LEDGER, f, indent=1)
print("\nLEDGER:", json.dumps(LEDGER, indent=1))
