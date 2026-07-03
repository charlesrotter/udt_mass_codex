"""Spare shot #6: row1 at FULL banked a* (1.4813439655172531) vs truncated (1.4813439655).
Tests a*-truncation sensitivity of the soft S_u negative and the pair. One IVP shot."""
import numpy as np, json, os
from scipy.integrate import solve_ivp
from scipy import sparse
import scipy.sparse.linalg as spla
import bv14_lib as L

SCR = os.path.dirname(os.path.abspath(__file__))
A_FULL = 1.4813439655172531
m, Z = 3.0, 8.0
PHI_C = -float(np.log(1101.0))
U, Up, Upp = L.makeU(A_FULL, m)

def rhs(r, y):
    phi, phip, rho, rhop = y
    e2p = np.exp(2.0*phi)
    return [phip, 4.0*rhop*rhop/(e2p*Z*rho*rho) - 2.0*phip*rhop/rho,
            rhop, 2.0*phip*rhop - 0.25*Z*rho*e2p*phip*phip + 0.25*e2p*Up(rho)]

seal = lambda r, y: y[0]; seal.terminal, seal.direction = True, +1
sol = solve_ivp(rhs, (0.0, 5e4), [PHI_C, 0.0, 1.0, 0.0], method="LSODA",
                rtol=1e-12, atol=1e-14, events=[seal], dense_output=True)
r_s = float(sol.t_events[0][0])
phi_s, phip_s, rho_s, rhop_s = [float(v) for v in sol.y_events[0][0]]
q = Z*rho_s**2*phip_s
rhopp_s = rhs(r_s, [phi_s, phip_s, rho_s, rhop_s])[3]
info = dict(tag="row1_afull", a=A_FULL, m=m, Z=Z, r_s=r_s, phip_s=phip_s,
            rho_s=rho_s, rhop_s=rhop_s, q=q, Lrho_s=-4.0*rhopp_s,
            Up1=float(Up(1.0)), M=6348)
print(json.dumps({k: info[k] for k in ("r_s", "rho_s", "rhop_s", "q")}))
# fake 'arr' with the grid data expected by assemble/translation
Mg = 6348
h = r_s/Mg
GA = 0.5/np.sqrt(3.0)
mid = (np.arange(Mg)+0.5)*h
rg = np.concatenate([mid-GA*h, mid+GA*h]); rn = np.arange(Mg+1)*h
arr = {f"g{Mg}_gp_y": sol.sol(rg), f"g{Mg}_node_phip": sol.sol(rn)[1],
       f"g{Mg}_node_rhop": sol.sol(rn)[3]}
Q, ix = L.assemble(info, arr, Mg)
iu, ib, iv, ia = ix["iu"], ix["ib"], ix["iv"], ix["ia"]
of = L.order_free(ix); Qf = Q[np.ix_(of, of)]
oh = L.order_drop(ix, {ia, iv[0]}); Qh = Q[np.ix_(oh, oh)]
ov = np.array(list(iv[1:])); Vh = Q[np.ix_(ov, ov)]
bf, bh, bv = L.inertia_band(Qf), L.inertia_band(Qh), L.inertia_band(Vh)
print(f"pair=({bh['n_neg']-bv['n_neg']},{bv['n_pos']}) hyp={bf['n_neg']==1+bh['n_neg']}"
      f" Qf=({bf['n_neg']},{bf['n_zero']},{bf['n_pos']})")
mass = np.full(ix["dim"], h); mass[iv[0]] *= 0.5; mass[iv[-1]] *= 0.5
mass[ib] = 1.0; mass[ia] = 1.0
w, V = spla.eigsh(Q.tocsc(), k=8, M=sparse.diags(mass).tocsc(), sigma=0.0, which="LM")
t = L.translation(info, arr, Mg, ix); tB = t*mass
ovl = np.abs(V.T @ tB)/(np.sqrt(float(t@tB))*np.sqrt((V*(mass[:, None]*V)).sum(0)))
o = np.argsort(np.abs(w))
print("near0:", [f"{w[i]:+.4e}(ov{ovl[i]:.2f})" for i in o])
led = json.load(open(os.path.join(SCR, "bv14_shot_ledger.json")))
led["shots"].append(dict(tag="row1_afull_SPARE6", r_max=5e4, rtol=1e-12, atol=1e-14,
                         status="seal", purpose="a*-truncation sensitivity"))
json.dump(led, open(os.path.join(SCR, "bv14_shot_ledger.json"), "w"), indent=1)
