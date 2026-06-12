"""
V3 -- M2 numeric leg, recomputed from bg_M2.dat with verifier-derived
closed forms (V1/V1b symbolic results), data-blind to the audit's printout.

Adjudicates:
  - T_w magnitude vs the k-refusal on the trust regions (claim: 3-6%)
  - audit-scheme (q,w) degeneracy locus X^2+7XY-2Y^2 entered inside the
    5% trust region (claim) -- plus verifier's areal-scheme locus Y = 3X
  - flip-ratio maps in BOTH schemes (audit: -(X-Y)(X+2Y)/D;
    areal: -(X-Y)/(3X-Y)) on the trust regions
Header trust radii read from the file itself: 1% t<1.1680, 5% t<1.5313.
"""
import numpy as np

dat = np.loadtxt('/tmp/seal_s1/lib/bg_M2.dat')
t, y = dat[:, 0], dat[:, 1]
F, a1, g2, h3 = dat[:, 2], dat[:, 3], dat[:, 4], dat[:, 5]
Ft, a1t, g2t, h3t = dat[:, 6], dat[:, 7], dat[:, 8], dat[:, 9]
s3, s5, s7 = np.sqrt(3), np.sqrt(5), np.sqrt(7)
t1, t5 = 1.1680, 1.5313

uu = np.linspace(-0.999, 0.999, 801)
st2 = 1 - uu**2

def harm(i):
    f = (F[i] + a1[i]*s3*uu + g2[i]*(s5/2)*(3*uu**2 - 1)
         + h3[i]*(s7/2)*(5*uu**3 - 3*uu))
    f_u = a1[i]*s3 + g2[i]*3*s5*uu + h3[i]*(s7/2)*(15*uu**2 - 3)
    f_t = (Ft[i] + a1t[i]*s3*uu + g2t[i]*(s5/2)*(3*uu**2 - 1)
           + h3t[i]*(s7/2)*(5*uu**3 - 3*uu))
    return f, f_u, f_t

def region(tmax):
    res = dict(rw=[], rq=[], D=[], yox=[], rth_a=[], rth_e=[], De=[])
    for i in range(len(t)):
        if t[i] > tmax or y[i] <= 0:
            continue
        f, f_u, f_t = harm(i)
        if np.any(f <= 0):
            continue
        st = np.sqrt(st2)
        f_r = -f_t/y[i]
        f_th = -st*f_u
        # verifier closed forms (V1): per unit c
        Tq = 0.25*f_r*f_th*st
        Tw = 0.25*f_th**2/f*st
        Tk = -0.25*y[i]**2*f_r**2*st
        X = f_t**2/4.0
        Y = st2*f_u**2/(4.0*f)
        D = X**2 + 7*X*Y - 2*Y**2          # audit-scheme det poly
        De = Y*(3*X - Y)                   # areal-scheme det poly (~ -det)
        den = np.maximum(np.abs(Tk), 1e-300)
        res['rw'].append(np.abs(Tw)/den)
        res['rq'].append(np.abs(Tq)/den)
        res['D'].append(D)
        res['De'].append(De)
        with np.errstate(divide='ignore', invalid='ignore'):
            res['yox'].append(Y/np.maximum(X, 1e-300))
            res['rth_a'].append(-(X - Y)*(X + 2*Y)/D)
            res['rth_e'].append(-(X - Y)/(3*X - Y))
    return {k_: np.array(v_) for k_, v_ in res.items()}

print("locus values: audit Y/X* = (7+sqrt57)/4 = %.4f ; areal Y/X* = 3"
      % ((7 + np.sqrt(57))/4))
for tag, tm in (("TRUST 1% (t<=1.1680)", t1), ("TRUST 5% (t<=1.5313)", t5),
                ("FULL RECORD", t.max())):
    R = region(tm)
    print(f"\n===== {tag} =====")
    print(f"  max |T_w|/|T_k| = {R['rw'].max():.4f}   "
          f"max |T_q|/|T_k| = {R['rq'].max():.4f}")
    print(f"  audit D = X^2+7XY-2Y^2: min = {R['D'].min():.3e} "
          f"({'LOCUS ENTERED' if R['D'].min() < 0 else 'not entered'})")
    print(f"  areal D' = Y(3X-Y):     min = {R['De'].min():.3e} "
          f"({'AREAL LOCUS (Y=3X) ENTERED' if R['De'].min() < 0 else 'not entered'})")
    print(f"  Y/X range: [{np.nanmin(R['yox']):.4f}, {np.nanmax(R['yox']):.4f}]")
    fin = np.isfinite(R['rth_a'])
    print(f"  audit dpth flip map range: [{R['rth_a'][fin].min():.4f}, "
          f"{R['rth_a'][fin].max():.4f}] (spherical -1)")
    fin = np.isfinite(R['rth_e'])
    print(f"  areal dpth flip map range: [{R['rth_e'][fin].min():.4f}, "
          f"{R['rth_e'][fin].max():.4f}] (Y->0 limit -1/3)")

# depth profile of the w/k ratio
print("\nprofile (t, max_u |T_w|/|T_k|, max_u Y/X):")
for tp in (0.25, 0.5, 0.75, 1.0, 1.168, 1.35, 1.5313, 1.8, 2.0, 2.1):
    i = int(np.argmin(np.abs(t - tp)))
    f, f_u, f_t = harm(i)
    if np.any(f <= 0):
        continue
    st = np.sqrt(st2)
    f_r = -f_t/y[i]; f_th = -st*f_u
    Tw = 0.25*f_th**2/f*st
    Tk = -0.25*y[i]**2*f_r**2*st
    X = f_t**2/4.0; Y = st2*f_u**2/(4.0*f)
    print(f"  t={t[i]:.3f}  |T_w|/|T_k|={np.max(np.abs(Tw)/np.maximum(np.abs(Tk),1e-300)):8.4f}"
          f"  max Y/X={np.nanmax(Y/np.maximum(X,1e-300)):8.4f}")
