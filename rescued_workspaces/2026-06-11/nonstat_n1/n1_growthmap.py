"""
N1 script 2: THE GROWTH-RATE MAP.
Under the same-minus dynamics every sigma > 0 generalized eigenmode of
(A,B) evolves as exp(+-sqrt(sigma) T): rate k = sqrt(sigma).
Tables: rates per member/block/rung at the reference configuration
(h = 0 family point, banked screened D_+, t_b = 1% trust); the theta
family scan; the outer bracket; mode spatial structure (B-density
localization, channel content, weld value/flux, homogeneity overlap);
physical conversion (e-fold vs interior crossing time, t_b, t_seal).
Self-contained from cache.pkl + results pickles (verified in setup).
"""
import numpy as np, pickle

C = pickle.load(open('/tmp/nonstat_n1/cache.pkl', 'rb'))
R = pickle.load(open('/tmp/seal_s2/results_main.pkl', 'rb'))
S = pickle.load(open('/tmp/seal_s2/results_sens.pkl', 'rb'))
meta, fine, CF, MODES, NOFLUX, VH = (C['meta'], C['fine'], C['CF'],
                                     C['MODES'], C['NOFLUX'], C['VH'])
PASSN = []
def checkN(name, ok, detail=""):
    PASSN.append((name, bool(ok)))
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")

print("=== T1: growth rates k = sqrt(sigma) (weld-time units), h=0, "
      "banked scr D_+, t_b = 1% ===")
print("member  block   k1       k2       k3       k4")
for tag in ('M1', 'M2', 'M4'):
    for mm in range(4):
        k = np.sqrt(np.array(R[(tag, mm, 'ladder')]))
        print(f"  {tag}   m={mm}  " + " ".join(f"{v:8.4f}" for v in k))

print("\n=== T2: the (rung, m) near-degeneracy structure ===")
print("sigma organized by N = rung + m (rung = 1.. radial):")
for tag in ('M1', 'M2', 'M4'):
    print(f"  {tag}:")
    for Nd in (1, 2, 3, 4):
        row = []
        for mm in range(min(Nd, 4)):
            r = Nd - mm
            if r >= 1 and r <= 4:
                row.append((mm, R[(tag, mm, 'ladder')][r-1]))
        spread = max(v for _, v in row)/min(v for _, v in row)
        print(f"    N={Nd}: " + "  ".join(f"m={mm}:{v:9.4f}" for mm, v
              in row) + f"   spread {spread:.4f}x")

print("\n=== T3: theta-family scan: rate of the LOWEST mode vs seal "
      "Robin h (sigma_min from production scan) ===")
HS = R[('M1', 0, 'scan')][0]
print("  h:" + " ".join(f"{h:8.1f}" if np.isfinite(h) else "     Dir"
                        for h in HS))
for tag in ('M1', 'M2', 'M4'):
    for mm in range(4):
        row = np.array(R[(tag, mm, 'scan')][1])
        lab = ["%8.3f" % np.sqrt(v) if v > 0 else "  osc   " for v in row]
        print(f"  {tag} m={mm}: " + " ".join(lab))
print("  ('osc' = sigma_min < 0: that direction OSCILLATES under the "
      "flip -- the attractive-seal sector h > h_c is the stable one; "
      "all other directions in those configs still grow)")

print("\n=== T4: outer-bracket robustness of the lowest rate (M2, h=0; "
      "production sens table) ===")
for name, (r0, _) in S['S1'].items():
    lab = ["%7.3f" % np.sqrt(v) if v > 0 else "  osc  " for v in r0]
    print(f"  {name:22s} k_min per m: " + " ".join(lab))

print("\n=== T5: mode spatial structure (my FEM modes, reference "
      "config) ===")
def structure(tag, mm, k):
    d = CF[(tag, mm)]['d']
    dd = MODES[(tag, mm)]
    u = dd['modes'][k]; s = dd['sgrid']
    cf_t, cf_GA = CF[(tag, mm)]['t'], CF[(tag, mm)]['GA']
    # B-density on the grid
    rho = np.empty(len(s))
    for i, t in enumerate(s):
        j = min(np.searchsorted(cf_t, t) - 1, len(cf_t) - 2); j = max(j, 0)
        w = (t - cf_t[j])/(cf_t[j+1] - cf_t[j])
        G = (1-w)*cf_GA[j] + w*cf_GA[j+1]
        rho[i] = np.exp(-3*t)*(u[i] @ G @ u[i])
    cum = np.cumsum(rho); cum /= cum[-1]
    tb = s[-1]
    t25 = s[np.searchsorted(cum, 0.25)]; t50 = s[np.searchsorted(cum, 0.5)]
    t75 = s[np.searchsorted(cum, 0.75)]
    fr_weld = cum[np.searchsorted(s, 0.2*tb)]
    fr_seal = 1 - cum[np.searchsorted(s, 0.8*tb)]
    # channel content (B-weighted)
    chan = np.zeros(d)
    for i, t in enumerate(s):
        chan += np.exp(-3*t)*u[i]**2
    chan /= chan.sum()
    du0 = (u[1] - u[0])/(s[1] - s[0])
    return dict(t25=t25, t50=t50, t75=t75, frw=fr_weld, frs=fr_seal,
                chan=chan, u0=u[0], du0=du0, utb=u[-1], tb=tb)

for tag in ('M1', 'M2', 'M4'):
    for mm in range(4):
        st = structure(tag, mm, 0)
        ls = C['LBLK'][mm]
        print(f"  {tag} m={mm} rung1: B-mass quartiles t = "
              f"{st['t25']:.2f}/{st['t50']:.2f}/{st['t75']:.2f} of tb="
              f"{st['tb']:.2f}; weld20% {st['frw']:.2f} seal20% "
              f"{st['frs']:.2f}; channel weights " +
              " ".join(f"l={l}:{w:.2f}" for l, w in zip(ls, st['chan'])))
st = structure('M2', 0, 1)
print(f"  M2 m=0 rung2: quartiles {st['t25']:.2f}/{st['t50']:.2f}/"
      f"{st['t75']:.2f}; weld20% {st['frw']:.2f} seal20% {st['frs']:.2f}")

print("\n=== T6: homogeneity-direction overlap (m=0 rung 1 and the "
      "no-flux soft mode vs the scaling direction u = X(t)) ===")
def overlap_with_X(tag, dd, k):
    u = dd['modes'][k]; s = dd['sgrid']
    ft, fX = fine[tag]['t'], fine[tag]['X']
    Xi = np.array([np.interp(s, ft, fX[:, j]) for j in range(4)]).T
    cf_t, cf_GA = CF[(tag, 0)]['t'], CF[(tag, 0)]['GA']
    num = den1 = den2 = 0.0
    for i, t in enumerate(s):
        j = min(np.searchsorted(cf_t, t) - 1, len(cf_t) - 2); j = max(j, 0)
        w = (t - cf_t[j])/(cf_t[j+1] - cf_t[j])
        G = (1-w)*cf_GA[j] + w*cf_GA[j+1]
        wq = (s[1]-s[0])*(0.5 if i in (0, len(s)-1) else 1.0)
        num += wq*np.exp(-3*t)*(u[i] @ G @ Xi[i])
        den1 += wq*np.exp(-3*t)*(u[i] @ G @ u[i])
        den2 += wq*np.exp(-3*t)*(Xi[i] @ G @ Xi[i])
    return num/np.sqrt(den1*den2)
for tag in ('M1', 'M2', 'M4'):
    o_ref = overlap_with_X(tag, MODES[(tag, 0)], 0)
    o_nf = overlap_with_X(tag, NOFLUX[tag], 0)
    print(f"  {tag}: <mode1, X>_B (banked D_+) = {o_ref:+.3f};  "
          f"no-flux soft mode = {o_nf:+.3f};  no-flux sigma = "
          f"{NOFLUX[tag]['sig'][0]:.4f} (rate {np.sqrt(NOFLUX[tag]['sig'][0]):.3f})")

print("\n=== T7: physical conversion ===")
print("interior crossing time T_x = Int_0^tb e^-t sqrt(G_00(t)) dt "
      "(slowest-channel signal time across the trusted interior):")
for tag in ('M1', 'M2', 'M4'):
    cf_t, cf_GA = CF[(tag, 0)]['t'], CF[(tag, 0)]['GA']
    tb = meta[tag]['t1pc']
    sel = cf_t <= tb
    Tx = np.trapezoid(np.exp(-cf_t[sel])*np.sqrt(cf_GA[sel, 0, 0]),
                      cf_t[sel])
    sig1 = R[(tag, 0, 'ladder')][0]
    k1 = np.sqrt(sig1)
    print(f"  {tag}: T_x = {Tx:.4f}; e-fold time 1/k1 = {1/k1:.4f} "
          f"(= {1/k1/Tx:.2f} crossings); tb = {tb:.3f}, t_seal = "
          f"{meta[tag]['tseal']:.3f}; gamma = {meta[tag]['gamma']}")
print("rate-vs-gamma: k1(M1,gamma=1)/k1(M4,gamma=0.5) = "
      f"{np.sqrt(R[('M1',0,'ladder')][0]/R[('M4',0,'ladder')][0]):.4f}"
      "  (c-independence M1 vs M2: "
      f"{np.sqrt(R[('M2',0,'ladder')][0]/R[('M1',0,'ladder')][0]):.4f})")

# UV statement check: rates grow without bound along the rung ladder
for tag in ('M1',):
    sig = R[(tag, 0, 'ladder')]
    checkN("N1-G1 rate ladder is increasing (UV-unbounded growth in the "
           "quadratic theory; Sturm-Liouville sigma_n -> inf)",
           np.all(np.diff(sig) > 0), f"{np.round(np.sqrt(sig),3)}")
deg = []
for tag in ('M1', 'M2', 'M4'):
    for Nd in (2, 3, 4):
        vals = [R[(tag, mm, 'ladder')][Nd-mm-1] for mm in range(Nd)
                if Nd-mm-1 <= 3]
        deg.append(max(vals)/min(vals))
checkN("N1-G2 (rung+m) near-degeneracy: every N-shell spread <= 1.01x "
       "for N<=4 across members", max(deg) < 1.01,
       f"max spread {max(deg):.4f}x")
n = sum(1 for _, ok in PASSN if ok)
print(f"\nN1-GROWTHMAP PASS {n}/{len(PASSN)}")
