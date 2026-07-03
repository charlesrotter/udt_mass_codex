"""bv15 backgrounds: shots 1-2 (own shooter, own machinery).
EOMs (banked, cell_solver_universe_T3.py header):
  phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
  rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4) U'(rho)
U(rho) = 2 rho^m exp(-a (rho^2-1))  (risefall, rho_c=1), phi_c = -ln(1101), phi'(0)=rho'(0)=0.
"""
import numpy as np, pickle, json, os
from scipy.integrate import solve_ivp

SCR = os.path.dirname(os.path.abspath(__file__))
PHI_C = -float(np.log(1101.0))


def makeU(a, m):
    def U(rho):   return 2.0 * rho**m * np.exp(-a*(rho*rho - 1.0))
    def Up(rho):  return U(rho) * (m/rho - 2.0*a*rho)
    def Upp(rho): return Up(rho)*(m/rho - 2.0*a*rho) + U(rho)*(-m/rho**2 - 2.0*a)
    return U, Up, Upp


def rhs_factory(Z, Up):
    def rhs(r, y):
        phi, phip, rho, rhop = y
        e2p = np.exp(2.0*phi)
        phipp = 4.0*rhop*rhop/(e2p*Z*rho*rho) - 2.0*phip*rhop/rho
        rhopp = 2.0*phip*rhop - 0.25*Z*rho*e2p*phip*phip + 0.25*e2p*Up(rho)
        return [phip, phipp, rho*0 + rhop, rhopp]
    return rhs


def shoot(tag, Z, a, m, r_end, terminal_seal):
    U, Up, Upp = makeU(a, m)
    rhs = rhs_factory(Z, Up)
    seal = lambda r, y: y[0]
    seal.terminal, seal.direction = bool(terminal_seal), +1
    collapse = lambda r, y: y[2] - 1e-9
    collapse.terminal, collapse.direction = True, -1
    sol = solve_ivp(rhs, (0.0, r_end), [PHI_C, 0.0, 1.0, 0.0], method="DOP853",
                    rtol=1e-12, atol=1e-14, events=[seal, collapse], dense_output=True)
    assert sol.t_events[1].size == 0, "rho collapse hit"
    assert sol.t_events[0].size >= 1, "no seal crossing"
    r_s = float(sol.t_events[0][0])
    phi_s, phip_s, rho_s, rhop_s = [float(x) for x in sol.y_events[0][0]]
    # gates: H_tot drift, MS marginality at both edges, seal residual
    rr = np.linspace(0.0, r_s, 20001)
    phi, phip, rho, rhop = sol.sol(rr)
    e2p = np.exp(2.0*phi)
    H = 0.5*Z*rho**2*phip**2 - 2.0*rhop**2/e2p - 2.0 + U(rho)
    msf = rhop**2/e2p          # 2m/rho = 1 - rho'^2 e^{-2phi} ... marginality: 2m/rho -> 1
    q = Z*rho_s**2*phip_s
    rhopp_s = 2.0*phip_s*rhop_s - 0.25*Z*rho_s*np.exp(2*phi_s)*phip_s**2 \
              + 0.25*np.exp(2*phi_s)*Up(rho_s)
    info = dict(tag=tag, Z=Z, a=a, m=m, r_s=r_s, phi_s=phi_s, phip_s=phip_s,
                rho_s=rho_s, rhop_s=rhop_s, q=q, rhopp_s=float(rhopp_s),
                Lrho_s=float(-4.0*rhopp_s), Up1=float(2.0*(m - 2.0*a)),
                H_drift=float(np.max(np.abs(H))),
                ms_core=float(1.0 - msf[0]), ms_seal=float(1.0 - msf[-1]),
                U_seal=float(U(rho_s)),
                U_seal_identity_res=float(U(rho_s) - (2.0 - q*q/(2.0*Z*rho_s**2))),
                nfev=sol.nfev, r_end_reached=float(sol.t[-1]))
    with open(os.path.join(SCR, f"bv15_bg_{tag}.pkl"), "wb") as f:
        pickle.dump(dict(info=info, sol=sol), f)
    return info


if __name__ == "__main__":
    out = {}
    # SHOT 1: B00
    out["B00"] = shoot("B00", Z=8.0, a=1.4813439655172531, m=3.0,
                       r_end=577.5026522756837 + 2.0, terminal_seal=False)
    # SHOT 2: SZ1
    out["SZ1"] = shoot("SZ1", Z=1.0, a=1.4942743252, m=3.0, r_end=1.0e4, terminal_seal=True)
    json.dump(out, open(os.path.join(SCR, "bv15_bg_info.json"), "w"), indent=1)
    for t, i in out.items():
        print(t, json.dumps(i, indent=1))
