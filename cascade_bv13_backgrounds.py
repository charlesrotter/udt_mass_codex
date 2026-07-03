"""bv13 numeric part 1: backgrounds (2 IVP shots TOTAL, augmented with the d/dphi_c Jacobi field).
Rungs: risefall m=3, Z=8, rho_c=1, phi_c=-ln(1101); N=0 a*=1.4813439655172531, N=5 a*=1.4928688994263575.
Saves dense profiles + seal data + W5(ii) Jacobi residuals to bv13_bg.npz / bv13_bg.json.
SHOT LEDGER kept explicitly.
"""
import numpy as np, json
from scipy.integrate import solve_ivp

Z = 8.0
PHI_C = -np.log(1101.0)
SHOTS = []

def makeU(a, m=3.0):
    def U(rho):  return 2.0*rho**m*np.exp(-a*(rho*rho-1.0))
    def Up(rho): return U(rho)*(m/rho - 2.0*a*rho)
    def Upp(rho):return Up(rho)*(m/rho - 2.0*a*rho) + U(rho)*(-m/rho**2 - 2.0*a)
    return U, Up, Upp

def rhs_aug(r, y, a):
    # background (phi,phip,rho,rhop) + Jacobi d/dphi_c (g,gp,h,hp)
    U, Up, Upp = makeU(a)
    phi, phip, rho, rhop, g, gp, h, hp = y
    e2p = np.exp(2.0*phi); em2p = np.exp(-2.0*phi)
    F = 4.0*em2p*rhop*rhop/(Z*rho*rho) - 2.0*phip*rhop/rho
    G = 2.0*phip*rhop - 0.25*Z*rho*e2p*phip*phip + 0.25*e2p*Up(rho)
    F_phi = -8.0*em2p*rhop*rhop/(Z*rho*rho)
    F_phip = -2.0*rhop/rho
    F_rho = -8.0*em2p*rhop*rhop/(Z*rho**3) + 2.0*phip*rhop/rho**2
    F_rhop = 8.0*em2p*rhop/(Z*rho*rho) - 2.0*phip/rho
    G_phi = -0.5*Z*rho*e2p*phip*phip + 0.5*e2p*Up(rho)
    G_phip = 2.0*rhop - 0.5*Z*rho*e2p*phip
    G_rho = -0.25*Z*e2p*phip*phip + 0.25*e2p*Upp(rho)
    G_rhop = 2.0*phip
    gpp = F_phi*g + F_phip*gp + F_rho*h + F_rhop*hp
    hpp = G_phi*g + G_phip*gp + G_rho*h + G_rhop*hp
    return [phip, F, rhop, G, gp, gpp, hp, hpp]

out = {}
prof = {}
for tag, a in (("N0", 1.4813439655172531), ("N5", 1.4928688994263575)):
    U, Up, Upp = makeU(a)
    seal = lambda r, y, *args: y[0]
    seal.terminal, seal.direction = True, +1
    y0 = [PHI_C, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0]   # Jacobi IC: g(0)=1 (d/dphi_c), fold-preserving
    sol = solve_ivp(rhs_aug, (0.0, 5.0e7), y0, args=(a,), method="LSODA",
                    rtol=1e-11, atol=1e-13, events=[seal], dense_output=True)
    SHOTS.append(f"{tag}: background+Jacobi augmented, a={a}, LSODA rtol=1e-11")
    assert sol.t_events[0].size, f"{tag}: no seal reached"
    r_s = float(sol.t_events[0][0])
    phi_s, phip_s, rho_s, rhop_s, g_s, gp_s, h_s, hp_s = sol.y_events[0][0]
    q = Z*rho_s**2*phip_s
    Lrho_s = Z*rho_s*phip_s**2 - Up(rho_s)
    rhopp_s = 2.0*phip_s*rhop_s - 0.25*Z*rho_s*np.exp(2*phi_s)*phip_s**2 + 0.25*np.exp(2*phi_s)*Up(rho_s)
    H_seal = 0.5*Z*rho_s**2*phip_s**2 - 2.0*np.exp(-2*phi_s)*rhop_s**2 - 2.0 + U(rho_s)
    # W5(ii) residuals at the seal for the shooting direction:
    beta = -g_s/phip_s
    R_dH = q*gp_s + (Z*rho_s*phip_s**2 + Up(rho_s))*h_s          # beta-NBC (= deltaH(r_s))
    R_v  = -4.0*np.exp(-2*phi_s)*hp_s + 8.0*np.exp(-2*phi_s)*rhop_s*g_s + Lrho_s*beta   # v(r_s)-NBC
    scale_v = abs(4.0*hp_s) + abs(Lrho_s*beta)
    out[tag] = dict(a=a, r_s=r_s, rho_s=rho_s, rhop_s=rhop_s, phip_s=phip_s, q=q,
                    H_seal=H_seal, Lrho_s=Lrho_s, rhopp_s=rhopp_s,
                    Lrho_plus_4rhopp=Lrho_s + 4.0*rhopp_s,
                    jac_g_s=g_s, jac_gp_s=gp_s, jac_h_s=h_s, jac_hp_s=hp_s,
                    W5ii_beta=beta, W5ii_R_deltaH=R_dH, W5ii_R_v=R_v, W5ii_R_v_scale=scale_v,
                    W5ii_R_v_rel=R_v/scale_v if scale_v else np.nan)
    # dense profiles for matrix assembly: store fine uniform sampling (grids built later by interp)
    rr = np.linspace(0.0, r_s, 200001)
    Y = sol.sol(rr)
    prof[tag+"_r"] = rr
    prof[tag+"_y"] = Y[:4]        # phi, phip, rho, rhop
    print(f"[{tag}] r_s={r_s:.6f} rho_s={rho_s:.8f} q={q:.8f} rhop_s={rhop_s:+.3e} H_seal={H_seal:+.3e}")
    print(f"       L_rho(r_s)={Lrho_s:+.6e}  L_rho+4rho''={Lrho_s+4*rhopp_s:+.3e}")
    print(f"       W5ii: beta={beta:+.6e} R_deltaH={R_dH:+.6e} R_v={R_v:+.6e} (rel {out[tag]['W5ii_R_v_rel']:+.3e})")
    # node counts (diagnostic: N check via interior rho' zeros)
    rhop_arr = Y[3]
    sgn = np.sign(rhop_arr[np.abs(rhop_arr) > 1e-12])
    nflip = int(np.sum(sgn[1:]*sgn[:-1] < 0))
    print(f"       interior rho' sign flips = {nflip}")
    out[tag]["rhop_sign_flips"] = nflip

out["SHOT_LEDGER"] = SHOTS
np.savez_compressed("bv13_bg.npz", **prof)
with open("bv13_bg.json", "w") as f: json.dump(out, f, indent=1, default=float)
print("saved bv13_bg.npz / bv13_bg.json ; shots used:", len(SHOTS))
