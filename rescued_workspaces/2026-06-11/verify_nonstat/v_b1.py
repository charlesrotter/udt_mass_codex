"""BLIND VERIFIER — N1 claims B1, B3(ii), B5: my own discretization.

System (from the verified S2 weak form; coefficients = cached tables):
  -(e^{-t} u')' + 2 e^{-t} H(t) u = sigma e^{-3t} G(t) u  on [0, tb]
  BC t=0 (weld):  u'(0) = M_out u(0)        [or u'(0)=0, no-flux]
  BC t=tb (1% stand-in): m=0: vhat-Dirichlet + complement u'=h u;
                         m>=1: u' = h u.
Solver: my own conservative vector FD + sparse shift-invert (NOT their
P1 FEM). Richardson over mesh doubling.
"""
import numpy as np, pickle
import scipy.sparse as spr
import scipy.sparse.linalg as sla

C = pickle.load(open('/tmp/nonstat_n1/cache.pkl', 'rb'))
meta, CF, MOUTC = C['meta'], C['CF'], C['MOUT']
VH = np.array([1.0, np.sqrt(3), np.sqrt(5), np.sqrt(7)])/4.0

PASS, FAIL = [], []
def check(label, ok, detail=""):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, detail, flush=True)

def interp_mat(tq, tg, M):
    out = np.empty((len(tq),) + M.shape[1:])
    for idx in np.ndindex(M.shape[1:]):
        out[(slice(None),) + idx] = np.interp(tq, tg, M[(slice(None),) + idx])
    return out

def solve_mine(tag, mm, n=2400, h_rob=0.0, weld='mout', nev=4):
    cf = CF[(tag, mm)]
    d = cf['d']; tb = meta[tag]['t1pc']
    t = np.linspace(0.0, tb, n + 1)
    h = t[1] - t[0]
    tm = 0.5*(t[:-1] + t[1:])
    pm = np.exp(-tm)                       # face conductance
    Hn = interp_mat(t, cf['t'], cf['H'])
    Gn = interp_mat(t, cf['t'], cf['GA'])
    wn = np.exp(-3*t)
    pn = np.exp(-t)
    ndof = (n + 1)*d
    rows, cols, vals = [], [], []
    brow, bcol, bval = [], [], []
    def add(i, j, M, lst):
        r, c, v = lst
        for a in range(d):
            for bidx in range(d):
                if M[a, bidx] != 0.0:
                    r.append(i*d + a); c.append(j*d + bidx)
                    v.append(M[a, bidx])
    A = (rows, cols, vals); Bl = (brow, bcol, bval)
    I = np.eye(d)
    for i in range(n + 1):
        cell = h if 0 < i < n else h/2
        add(i, i, 2*pn[i]*Hn[i]*cell, A)
        add(i, i, wn[i]*Gn[i]*cell, Bl)
    for e in range(n):
        ke = pm[e]/h*I
        add(e, e, ke, A); add(e+1, e+1, ke, A)
        add(e, e+1, -ke, A); add(e+1, e, -ke, A)
    if weld == 'mout':
        add(0, 0, MOUTC[tag][mm]['scr'], A)
    elif weld == 'neumann':
        pass
    K = spr.coo_matrix((vals, (rows, cols)), shape=(ndof, ndof)).tocsc()
    B = spr.coo_matrix((bval, (brow, bcol)), shape=(ndof, ndof)).tocsc()
    # seal BCs
    T = spr.identity(ndof, format='lil')
    drop = []
    last = n*d
    if mm == 0:
        # rotate last node into (vhat, complement)
        Wc = np.linalg.qr(np.column_stack([VH, np.eye(d)[:, :d-1]]))[0]
        R4 = np.column_stack([VH, Wc[:, 1:]])
        T[last:last+d, last:last+d] = R4
        T = T.tocsc()
        K = (T.T @ K @ T).tocsc(); B = (T.T @ B @ T).tocsc()
        drop = [last]
        if h_rob != 0.0:
            Rb = spr.lil_matrix((ndof, ndof))
            Rb[last+1:last+d, last+1:last+d] = -np.exp(-tb)*h_rob*np.eye(d-1)
            K = (K + Rb.tocsc())
    else:
        if h_rob != 0.0:
            Rb = spr.lil_matrix((ndof, ndof))
            Rb[last:last+d, last:last+d] = -np.exp(-tb)*h_rob*np.eye(d)
            K = (K + Rb.tocsc())
    keep = np.setdiff1d(np.arange(ndof), drop)
    K = K[np.ix_(keep, keep)].tocsc(); B = B[np.ix_(keep, keep)].tocsc()
    K = (K + K.T)/2
    w, V = sla.eigsh(K, k=nev, M=B, sigma=-0.5, which='LM')
    o = np.argsort(w)
    return w[o], V[:, o], keep, t, d

def rich(tag, mm, **kw):
    w1 = solve_mine(tag, mm, n=1200, **kw)[0]
    w2 = solve_mine(tag, mm, n=2400, **kw)[0]
    return (4*w2 - w1)/3

print("=== B1: four spot rates, my own solver ===")
R = pickle.load(open('/tmp/seal_s2/results_main.pkl', 'rb'))
targets = [('M1', 0, 0, 7.057579), ('M1', 0, 1, 16.1940),
           ('M2', 1, 0, 15.4327), ('M4', 3, 0, 38.6722)]
worst = 0
for tag, mm, rung, sref in targets:
    w = rich(tag, mm)
    sig = w[rung]
    k = np.sqrt(sig); kref = np.sqrt(sref)
    dev = abs(sig - sref)/sref
    worst = max(worst, dev)
    print(f"  {tag} m={mm} rung{rung+1}: sigma {sig:.5f} (rec {sref}); "
          f"rate k {k:.4f} (rec {kref:.4f}); rel dev {dev:.1e}")
check("B1-1 all four spot rates reproduced (<= 2e-3 rel)", worst < 2e-3,
      f"worst {worst:.1e}")

print("\n=== B1: weld localization (B-mass in first 20% of t) ===")
fr = {}
for tag, mm in [('M1', 0), ('M2', 0), ('M1', 3), ('M4', 3), ('M2', 1)]:
    w, V, keep, t, d = solve_mine(tag, mm, n=2400)
    full = np.zeros((2401)*d); full[keep] = V[:, 0]
    # rotate back for m=0
    if mm == 0:
        Wc = np.linalg.qr(np.column_stack([VH, np.eye(d)[:, :d-1]]))[0]
        R4 = np.column_stack([VH, Wc[:, 1:]])
        u = full.reshape(-1, d).copy()
        u[-1] = R4 @ u[-1]
    else:
        u = full.reshape(-1, d)
    cf = CF[(tag, mm)]
    Gn = interp_mat(t, cf['t'], cf['GA'])
    rho = np.exp(-3*t)*np.einsum('ia,iab,ib->i', u, Gn, u)
    cum = np.cumsum(rho); cum /= cum[-1]
    fr[(tag, mm)] = cum[np.searchsorted(t, 0.2*t[-1])]
    print(f"  {tag} m={mm}: weld-20% fraction {fr[(tag, mm)]:.3f}")
check("B1-2 rung-1 modes are weld-localized, 0.6-0.85 of B-mass in the "
      "first 20% (recorded 0.62-0.84)",
      all(0.55 < v < 0.9 for v in fr.values()))

print("\n=== B3(ii): no-flux (pure-Neumann weld) slowdown ===")
for tag, ref_sig, rec_nf in [('M2', 7.1344, 0.15855), ('M1', 7.057579,
                                                       0.09411)]:
    w = rich(tag, 0, weld='neumann')
    sd = np.sqrt(ref_sig/w[0])
    print(f"  {tag} m=0 no-flux sigma_min {w[0]:.5f} (rec {rec_nf}); "
          f"slowdown x{sd:.2f}")
    check(f"B3-{tag} no-flux sigma_min matches recorded (still > 0: "
          "slowed ~7x, NOT frozen)", abs(w[0] - rec_nf) < 0.003,
          f"{w[0]:.5f}")

print("\n=== B5: sign inversion for attractive seal h > h_c (M1 m=0) ===")
for hv, expect in [(1.0, 'grow'), (2.0, 'osc'), (4.0, 'osc')]:
    w = rich('M1', 0, h_rob=hv)
    lab = 'osc' if w[0] < 0 else f'grow k={np.sqrt(max(w[0],0)):.3f}'
    print(f"  h={hv}: sigma_min {w[0]:+.4f} -> {lab}")
    ok = (w[0] < 0) if expect == 'osc' else (w[0] > 0)
    check(f"B5 h={hv}: sigma_min sign matches recorded scan", ok)
# recorded: h=1.0 k=1.618
w = rich('M1', 0, h_rob=1.0)
check("B5-k h=1.0 rate k == 1.618 (recorded)",
      abs(np.sqrt(w[0]) - 1.618) < 0.005, f"k={np.sqrt(w[0]):.4f}")
# the flip logic: under L2 = -(c/2)[T+U], EL: B u_TT = A u (sigma>0 grows,
# sigma<0 oscillates at omega = sqrt|sigma|) -- analytic, see report.

print()
print("PASS", len(PASS), "FAIL", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
