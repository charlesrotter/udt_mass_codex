"""th2 final assembly: corrected predictions (no new shots; measured theta0 reused from
th2_results.json), full contribution decomposition per rung."""
import json, sys
import numpy as np
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from th2_predict_measure import (fam_constants, make_slice, bottom, sumP_quad, XC)

res = json.load(open("th2_results.json"))
print(f"{'rung':>18}{'z*eff':>8}{'geo':>7}{'anh':>7}{'off':>7}{'SPq':>7}{'hi.ord':>7}"
      f"{'pred':>8}{'meas':>8}{'diff':>8}   (all /pi)")
out = []
for R in res:
    Z, kind, par, N = R['Z'], R['kind'], R['par'], R['N']
    dt, s1, c3h, c4h = fam_constants(kind, par)
    gamma = 4.0*dt*dt/(Z*s1*s1*XC*XC)
    zstar = R['zstar']          # bottom() unchanged, reuse
    U, Upf, lab = make_slice(kind, par)
    th0 = zstar
    for _ in range(4):
        Theta = (N+1)*np.pi + th0
        SP_q = sumP_quad(Z, U, s1, Theta)
        th0 = zstar + SP_q
    geo = 2.0*Z*(1.0-XC)**2/(3.0*Theta)
    anh = (15.0*c3h*c3h/16.0 - 1.5*c3h + 0.75*c4h)*Z*(1.0-XC)**2/(3.0*Theta)
    off = (N+1)*np.pi*1.5*c3h*(dt/s1)
    hiord = SP_q - (geo+anh+off)
    diff = th0 - R['th0_meas']
    print(f"{R['tag']:>18}{zstar/np.pi:>8.4f}{geo/np.pi:>7.4f}{anh/np.pi:>7.4f}{off/np.pi:>7.4f}"
          f"{SP_q/np.pi:>7.4f}{hiord/np.pi:>7.4f}{th0/np.pi:>8.4f}{R['th0_meas']/np.pi:>8.4f}"
          f"{diff/np.pi:>8.4f}")
    out.append(dict(tag=R['tag'], Z=Z, N=N, kind=kind, gamma=gamma, zstar_pi=zstar/np.pi,
                    geo_pi=geo/np.pi, anh_pi=anh/np.pi, off_pi=off/np.pi, SPq_pi=SP_q/np.pi,
                    pred_pi=th0/np.pi, meas_pi=R['th0_meas']/np.pi, diff_pi=diff/np.pi,
                    c3h=c3h, c4h=c4h, dt=dt, s1=s1, zc_eff=R['zc_eff'], zc_req=R['zc_req']))
json.dump(out, open("th2_final_table.json","w"), indent=1)
# quadrature-vs-analytic kappa validation at small amplitude (m=3 family):
from th2_predict_measure import P_excess
import numpy as np
dt, s1, c3h, c4h = fam_constants("A1m3", 1.4941244349239216)
kappaE = 2.0 + 15.0*c3h*c3h/16.0 - 1.5*c3h + 0.75*c4h
print(f"\nkappa_E analytic = {kappaE:.5f} (c3h={c3h:.5f}, c4h={c4h:.5f}, dh={dt/s1:.5e})")
U, Upf, lab = make_slice("A1m3", 1.4941244349239216)
for E in (1e-4, 4e-4, 1.6e-3, 6.4e-3):
    Phi = np.sqrt(4.0*8.0*s1*E)
    P = P_excess(Phi, 8.0, U, s1)
    P_an = np.pi*(E*kappaE + 1.5*c3h*(dt/s1))
    print(f"  E={E:9.2e}: P_quad={P:12.6e}  P_analytic={P_an:12.6e}  ratio={P/P_an:8.5f}")
