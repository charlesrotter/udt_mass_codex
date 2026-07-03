"""T5: exact-action ray probe S[bg + eps*(deflated soft mode)], moving folds included.
Handling (stated): configuration at eps = fields (phi+eps*u, rho+eps*v) on [eps*alpha, r_s+eps*beta];
  - background r>r_s: nonlinear ODE continuation from the seal state (1 shot/rung, ledgered);
  - background r<0: even mirror (exact — EOM autonomous, phi'(0)=rho'(0)=0);
  - mode fields u,v: P1 from the 8M grid; r>r_s linear extrapolation of the last element
    (sensitivity: constant extrapolation also computed); r<0 even mirror.
  - Delta S = [bulk integral of (L_eps - L_0) on identical per-element 4-pt Gauss nodes]
    + endpoint segments with their own Gauss nodes (cancellation-safe).
Fit: symmetric part -> c2, c4; antisymmetric -> c1, c3. c2 vs lambda(grid) is a built-in
validation of the moving-endpoint handling (S(eps) = S(0) + eps^2 x^T Q x + O(eps^3)).
usage: python3 s3_t5.py <tag>
"""
import numpy as np, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s3_lib import SCR, load_bg, build, mass_vec, deflated_near0, wnorm, makeU
from scipy.integrate import solve_ivp

M0 = dict(B00=6348, SM2=5963, SZ1=6835)
tag = sys.argv[1]
Mg = M0[tag]*8
bg = load_bg(tag)
r_s = bg['r_s']; Z = bg['Z']
U, Up, Upp = makeU(bg['a'], bg['m'])

# ---- deflated soft mode at 8M (recompute; cheap)
Q, ix, t = build(bg, Mg)
mass = mass_vec(ix)
wD, VD, _ = deflated_near0(Q, mass, t, k=8)
neg = [j for j in range(len(wD)) if wD[j] < 0]
assert len(neg) == 1
lam = float(wD[neg[0]])
x = VD[:, neg[0]]; x = x/wnorm(x, mass)
h = ix['h']
u_n = np.empty(Mg+1)
u_n[:Mg] = x[ix['iu']]
beta = float(x[ix['ib']]); alpha = float(x[ix['ia']])
u_n[Mg] = -bg['phip_s']*beta          # essential odd-fold constraint value
v_n = x[ix['iv']].copy()

# ---- background extension past the seal: ONE nonlinear ODE continuation (ledgered shot)
def rhs(r, y):
    phi, phip, rho, rhop = y
    e2p = np.exp(2.0*phi)
    return [phip,
            4.0*rhop*rhop/(e2p*Z*rho*rho) - 2.0*phip*rhop/rho,
            rhop,
            2.0*phip*rhop - 0.25*Z*rho*e2p*phip*phip + 0.25*e2p*Up(rho)]

y_seal = bg['sol'].sol(r_s)
t0 = time.time()
EXT_SPAN = 1.0   # past-seal solution collapses (rho->0) at ~+1.5; guard with event
collapse = lambda r, y: y[2] - 0.05
collapse.terminal = True; collapse.direction = -1
ext = solve_ivp(rhs, (r_s, r_s + EXT_SPAN), list(y_seal), method='LSODA',
                rtol=1e-12, atol=1e-14, dense_output=True, events=[collapse])
shot = dict(kind='seal_extension_shot', tag=tag, span=[float(r_s), float(r_s+EXT_SPAN)],
            rtol=1e-12, atol=1e-14, success=bool(ext.success), wall_s=round(time.time()-t0, 2))
led_f = os.path.join(SCR, 's3_shot_ledger.json')
led = json.load(open(led_f)) if os.path.exists(led_f) else {'declared': 'see s3_predictions.md', 'nonlinear_shots': []}
led['nonlinear_shots'].append(shot)
json.dump(led, open(led_f, 'w'), indent=1)
assert ext.success

def bgf(r):
    """background (phi, phip, rho, rhop) with mirror below 0 and continuation above r_s."""
    r = np.asarray(r, dtype=float)
    out = np.empty((4, r.size))
    rm = np.abs(r)                      # even mirror: phi,rho even; phip,rhop odd
    inside = rm <= r_s
    if inside.any():
        y = bg['sol'].sol(rm[inside]); out[:, inside] = y
    if (~inside).any():
        y = ext.sol(rm[~inside]); out[:, ~inside] = y
    sgn = np.sign(r) + (r == 0)
    out[1] *= sgn; out[3] *= sgn
    return out

def modef(r, extmode='linear'):
    """P1 mode fields (u, u', v, v') with mirror below 0, extrapolation above r_s."""
    r = np.asarray(r, dtype=float)
    rm = np.abs(r); sgn = np.sign(r) + (r == 0)
    rc = np.clip(rm, 0.0, r_s)
    j = np.minimum((rc/h).astype(int), Mg-1)
    xi = rc/h - j
    u = (1-xi)*u_n[j] + xi*u_n[j+1]; up = (u_n[j+1]-u_n[j])/h
    v = (1-xi)*v_n[j] + xi*v_n[j+1]; vp = (v_n[j+1]-v_n[j])/h
    over = rm > r_s
    if over.any():
        if extmode == 'linear':
            du = (u_n[Mg]-u_n[Mg-1])/h; dv = (v_n[Mg]-v_n[Mg-1])/h
            u[over] = u_n[Mg] + du*(rm[over]-r_s); up[over] = du
            v[over] = v_n[Mg] + dv*(rm[over]-r_s); vp[over] = dv
        else:
            u[over] = u_n[Mg]; up[over] = 0.0
            v[over] = v_n[Mg]; vp[over] = 0.0
    up *= sgn; vp *= sgn                # even fields -> odd derivatives
    return u, up, v, vp

def Lag(phi, phip, rho, rhop):
    return 0.5*Z*rho**2*phip**2 - 2.0*np.exp(-2.0*phi)*rhop**2 + 2.0 - U(rho)

# per-element 4-pt Gauss on the mode grid (bulk)
gx = np.array([-0.8611363115940526, -0.3399810435848563, 0.3399810435848563, 0.8611363115940526])
gw = np.array([0.3478548451374539, 0.6521451548625461, 0.6521451548625461, 0.3478548451374539])
mids = (np.arange(Mg) + 0.5)*h
rq = (mids[:, None] + 0.5*h*gx[None, :]).ravel()
wq = np.tile(0.5*h*gw, Mg)
BG = bgf(rq)
L0 = Lag(*BG)

def seg_int(a, b, eps, extmode):
    """integral of L_eps over [a,b] with 64-pt composite Gauss."""
    if abs(b-a) < 1e-300: return 0.0
    n = 16
    edges = np.linspace(a, b, n+1)
    m = 0.5*(edges[:-1]+edges[1:]); hw = 0.5*(edges[1]-edges[0])
    rr = (m[:, None] + hw*gx[None, :]).ravel()
    ww = np.tile(hw*gw, n)
    phi, phip, rho, rhop = bgf(rr)
    u, up, v, vp = modef(rr, extmode)
    return float(np.sum(ww*Lag(phi+eps*u, phip+eps*up, rho+eps*v, rhop+eps*vp)))

def fold_root(eps, extmode='linear'):
    """Exact perturbed outer fold: phi_eps(R*) = 0 (the ESSENTIAL constraint of the
    variational class; enforcing it only to O(eps) leaks the boundary force into c2)."""
    r = r_s + eps*beta
    for _ in range(8):
        phi, phip, _, _ = bgf(np.array([r]))
        u, up, _, _ = modef(np.array([r]), extmode)
        f = float(phi[0] + eps*u[0]); fp = float(phip[0] + eps*up[0])
        dr = -f/fp
        r += dr
        if abs(dr) < 1e-14*max(1.0, r_s):
            break
    return r, abs(f)

def dS(eps, extmode='linear'):
    u, up, v, vp = modef(rq, extmode)
    dbulk = float(np.sum(wq*(Lag(BG[0]+eps*u, BG[1]+eps*up, BG[2]+eps*v, BG[3]+eps*vp) - L0)))
    Rstar, fres = fold_root(eps, extmode)
    so = seg_int(r_s, Rstar, eps, extmode)
    # inner endpoint is FREE configuration data (no essential constraint): r_c(eps) = eps*alpha
    si = -seg_int(0.0, eps*alpha, eps, extmode)
    return dbulk + so + si

eps_max = 0.3/max(abs(alpha), abs(beta))   # fold shifts stay well inside the valid extension
epss = eps_max*np.array([0.01, 0.03, 0.1, 0.3, 1.0])
rows = []
for e in epss:
    dp = dS(e); dm = dS(-e)
    dpc = dS(e, 'const')
    sym = 0.5*(dp+dm)/e**2; asym = 0.5*(dp-dm)/e
    rows.append(dict(eps=float(e), dS_plus=dp, dS_minus=dm, c2_eff=float(sym),
                     c1_eff=float(asym), ext_sens=float(abs(dp-dpc)/max(abs(dp), 1e-300))))
    print(f'eps={e:9.3e}  dS+={dp:+.6e} dS-={dm:+.6e}  c2_eff={sym:+.4e} c1_eff={asym:+.3e} extsens={rows[-1]["ext_sens"]:.1e}', flush=True)

# quartic fit of symmetric part: c2 + c4 eps^2
E2 = np.array([r['eps']**2 for r in rows]); C2 = np.array([r['c2_eff'] for r in rows])
A = np.vstack([np.ones_like(E2), E2]).T
coef, *_ = np.linalg.lstsq(A, C2, rcond=None)
out = dict(tag=tag, M=Mg, lam_grid=lam, alpha=alpha, beta=beta, eps_max=float(eps_max),
           rows=rows, c2_fit=float(coef[0]), c4_fit=float(coef[1]),
           lam_star_richardson=dict(B00=-6.55e-7, SM2=-3.84e-7, SZ1=-4.4e-8)[tag])
json.dump(out, open(os.path.join(SCR, f's3_t5_{tag}.json'), 'w'), indent=1)
print(json.dumps({k: out[k] for k in ('tag', 'lam_grid', 'c2_fit', 'c4_fit', 'eps_max')}))
