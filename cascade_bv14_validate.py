"""bv14 validation at coarse grids (M=400, 800), all 5 rungs:
 (a) x^T Q x vs fine-quadrature continuum form on smooth test fields (assembly check)
 (b) band-LDL slicing inertia vs dense eigvalsh inertia for Q_free, Qhat, Vhat (+anch/fixed)
 (c) explicit S_u dense inertia vs Haynsworth identity route
 (d) hyperbolic-pair identity n_neg(Q) = 1 + n_neg(Qhat)
 (e) bordered-deflation count vs dense projected deflation
 (f) translation Rayleigh quotient at 400 vs 800 (O(h^2) ratio ~ 4)
"""
import numpy as np, json
from bv14_lib import (load, assemble, makeU, order_free, order_drop, inertia_band,
                      inertia_dense_eig, explicit_Su_Vhat, translation, diagscale)

TAGS = ["row1_m3Z8_belowN0", "row2_m3Z8_aboveN0", "row3_m3Z1_fund",
        "row4_m3Z8_belowN15", "row5_m2Z8_fund"]

def continuum_ref(info, arr, ufun, upfun, vfun, vpfun, alpha, beta):
    from bv14_lib import coeffs
    r = arr["fine_r"]; y = arr["fine_y"]
    C = coeffs(info, y[0], y[1], y[2], y[3])
    u, up, v, vp = ufun(r), upfun(r), vfun(r), vpfun(r)
    integ = (C["cku"]*up**2 + C["ckv"]*vp**2 + C["cc1"]*v*up + C["cc2"]*u*vp
             + C["cmu"]*u**2 + C["cmv"]*v**2)
    val = np.trapezoid(integ, r)
    val += info["Lrho_s"]*beta*vfun(np.array([info["r_s"]]))[0]
    val += info["Up1"]*alpha*vfun(np.array([0.0]))[0]
    return float(val)

for tag in TAGS:
    info, arr = load(tag)
    r_s, phip_s = info["r_s"], info["phip_s"]
    beta, alpha = 0.6, 0.9
    # test fields, analytic derivatives; essential constraint u(r_s) = -phip_s*beta exact
    k1 = 3.3*np.pi/r_s; k2 = 1.3*np.pi/r_s
    base = lambda r: np.cos(k1*r)*(0.5 + r/r_s)
    basep = lambda r: -k1*np.sin(k1*r)*(0.5 + r/r_s) + np.cos(k1*r)/r_s
    cc = -phip_s*beta - base(np.array([r_s]))[0]
    ufun = lambda r: base(r) + cc*(r/r_s)**3
    upfun = lambda r: basep(r) + 3.0*cc*r**2/r_s**3
    vfun = lambda r: np.sin(k2*r) + 0.4 - 0.5*(r/r_s)**2
    vpfun = lambda r: k2*np.cos(k2*r) - r/r_s**2
    ref = continuum_ref(info, arr, ufun, upfun, vfun, vpfun, alpha, beta)
    print(f"\n===== {tag} =====")
    vals = []
    for Mg in (400, 800):
        Q, ix = assemble(info, arr, Mg)
        rr = np.arange(Mg+1)*ix["h"]
        x = np.zeros(ix["dim"])
        x[ix["iu"]] = ufun(rr[:Mg]); x[ix["ib"]] = beta
        x[ix["iv"]] = vfun(rr); x[ix["ia"]] = alpha
        vals.append(float(x @ (Q @ x)))
    print(f"  (a) continuum={ref:.10f} discrete400={vals[0]:.10f} discrete800={vals[1]:.10f}"
          f"  relerr=({abs(vals[0]-ref)/abs(ref):.2e},{abs(vals[1]-ref)/abs(ref):.2e})"
          f"  ratio={(vals[0]-ref)/(vals[1]-ref):+.2f} (expect ~4)")
    rqs = {}
    for Mg in (400, 800):
        Q, ix = assemble(info, arr, Mg)
        iu, ib, iv, ia = ix["iu"], ix["ib"], ix["iv"], ix["ia"]
        of = order_free(ix)
        Qf = Q[np.ix_(of, of)]
        oh = order_drop(ix, {ia, iv[0]})
        Qh = Q[np.ix_(oh, oh)]
        ov = np.array(list(iv[1:]))
        Vh = Q[np.ix_(ov, ov)]
        # band counts
        bf = inertia_band(Qf); bh = inertia_band(Qh); bv = inertia_band(Vh)
        # dense counts
        df = inertia_dense_eig(Qf.toarray()); dh = inertia_dense_eig(Qh.toarray())
        dv = inertia_dense_eig(Vh.toarray())
        S, _ = explicit_Su_Vhat(Q, ix)
        ds = inertia_dense_eig(S)
        hayn_lhs = dh["n_neg"]; hayn_rhs = dv["n_neg"] + ds["n_neg"]
        idroute_Su = bh["n_neg"] - bv["n_neg"]
        print(f"  (b/c/d) M={Mg}: Qfree band=({bf['n_neg']},{bf['n_zero']},{bf['n_pos']})"
              f" dense=({df['n_neg']},{df['n_zero']},{df['n_pos']})"
              f" | Qhat band=({bh['n_neg']},{bh['n_zero']},{bh['n_pos']})"
              f" dense=({dh['n_neg']},{dh['n_zero']},{dh['n_pos']})"
              f" | Vhat band=({bv['n_neg']},{bv['n_zero']},{bv['n_pos']})"
              f" dense=({dv['n_neg']},{dv['n_zero']},{dv['n_pos']})")
        print(f"          S_u dense=({ds['n_neg']},{ds['n_zero']},{ds['n_pos']})"
              f" identity-route n_neg(S_u)={idroute_Su}"
              f" Haynsworth {hayn_lhs}=={hayn_rhs}:{hayn_lhs==hayn_rhs}"
              f" hyperbolic {df['n_neg']}==1+{dh['n_neg']}:{df['n_neg']==1+dh['n_neg']}"
              f" pair=({idroute_Su},{bv['n_pos']})")
        # anchored / fixed (band vs dense)
        oa = order_drop(ix, {iu[0]})
        Qa = Q[np.ix_(oa, oa)]
        oaf = order_drop(ix, {iu[0], ia, iv[0]})
        Qah = Q[np.ix_(oaf, oaf)]
        oxf = order_drop(ix, {ia, ib, iv[0]})
        Qxf = Q[np.ix_(oxf, oxf)]
        ba, da = inertia_band(Qa), inertia_dense_eig(Qa.toarray())
        bah, dah = inertia_band(Qah), inertia_dense_eig(Qah.toarray())
        bxf, dxf = inertia_band(Qxf), inertia_dense_eig(Qxf.toarray())
        print(f"          anch Q band=({ba['n_neg']},{ba['n_zero']},{ba['n_pos']}) dense=({da['n_neg']},{da['n_zero']},{da['n_pos']})"
              f" | anch Qhat band/dense n_neg={bah['n_neg']}/{dah['n_neg']}"
              f" | fixed(v0=0) band/dense n_neg={bxf['n_neg']}/{dxf['n_neg']}")
        # (e) deflation: bordered vs dense projected
        t = translation(info, arr, Mg, ix)
        tf = t[of]
        bdefl = inertia_band(Qf, border=tf)
        # dense projected deflation
        Qs_d, ts_d = diagscale(Qf, tf)
        A = Qs_d.toarray()
        tn = ts_d/np.linalg.norm(ts_d)
        # Householder: reflect tn -> e0, take rows 1:
        w = tn.copy(); w[0] += np.sign(tn[0]) if tn[0] != 0 else 1.0
        w /= np.linalg.norm(w)
        H = np.eye(len(tn)) - 2.0*np.outer(w, w)
        Cn = H[:, 1:]
        ddefl = inertia_dense_eig(Cn.T @ A @ Cn)
        num = float(t @ (Q @ t)); den = float(t @ t)*ix["h"]
        rqs[Mg] = num/den
        print(f"  (e) M={Mg}: deflated band=({bdefl['n_neg']},{bdefl['n_zero']},{bdefl['n_pos']})"
              f" dense=({ddefl['n_neg']},{ddefl['n_zero']},{ddefl['n_pos']})"
              f" | drop n_neg: free->defl {bf['n_neg']}->{bdefl['n_neg']}")
        print(f"      translation RQ={rqs[Mg]:+.6e}  tQt={num:+.6e}")
    print(f"  (f) RQ ratio 400/800 = {rqs[400]/rqs[800]:+.3f} (O(h^2) expect ~4)")
