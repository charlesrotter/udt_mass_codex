"""
BLIND VERIFIER library for sealed-cavity S2. Everything here is
re-implemented from the frozen conventions (s2_anchors.py header +
bg_*.dat headers); no package code is imported. DATA-BLIND.

Conventions used (re-stated):
  f(y,u) = F + a1 Y1 + g2 Y2 + h3 Y3;  Y0=1, Y1=sqrt3 u,
  Y2=(sqrt5/2)(3u^2-1), Y3=(sqrt7/2)(5u^3-3u);  t = ln(1/y)
  P = (1/4)<|grad_Om f|^2/f> = (1/8) Int (1-u^2) f_u^2/f du (axisym)
  EL background: X_tt - X_t = 2 P_X;  X(0)=(1,0,0,0), X_t(0)=(gamma,-c,0,0)
  Mode problem per m-block: A u = sigma B u,
    A = -(e^-t u')' + 2 e^-t H^(m)(t) u,  B = e^-3t G^(m)(t), omega^2=-sigma
  H^(m) = Hessian (second variation) of P in real harmonics with <R^2>=1
  G^(m)_A = <R R'/f^2>,  G^(m)_B = <R R'/f^3>
  outer: u'(0) = M_out u(0), M_out = diag(gamma + D_+(l)) - c C,
    C = <R Y1 R'>; D_+ per banked closed form (q=1/3, tau0=6 sqrt(lam))
  inner at t_b: m=0 Dirichlet on vhat=(1,s3,s5,s7)/4, Robin u'=h u on
    complement; m>=1 Robin u'=h u all directions.
"""
import numpy as np
from scipy.special import lpmv
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import scipy.linalg as sla

S3, S5, S7 = 3**0.5, 5**0.5, 7**0.5
YP1 = np.array([1.0, S3, S5, S7])
VH = YP1/4.0                       # |YP1| = 4
# orthonormal complement of VH (own QR)
WC = np.linalg.qr(np.column_stack([VH, np.eye(4)[:, :3]]))[0][:, 1:]

def Yr(u):
    u = np.asarray(u, float)
    return np.array([np.ones_like(u), S3*u, (S5/2)*(3*u*u - 1),
                     (S7/2)*(5*u**3 - 3*u)])

def Yru(u):
    u = np.asarray(u, float)
    return np.array([np.zeros_like(u), S3*np.ones_like(u), 3*S5*u,
                     (S7/2)*(15*u*u - 3)])

class Q:
    def __init__(self, N):
        x, w = np.polynomial.legendre.leggauss(N)
        self.x, self.w, self.s = x, w, 1 - x**2
        self.Y, self.Yu = Yr(x), Yru(x)

Q12, Q40 = Q(1200), Q(4000)

# ---------------- potential ----------------
def Pval(X, q=Q12):
    f = X @ q.Y; fu = X @ q.Yu
    return (q.w @ (q.s*fu*fu/f))/8.0

def Pgrad_fd(X, q=Q12, eps=1e-6):
    g = np.empty(4)
    for i in range(4):
        e = np.zeros(4); e[i] = eps
        g[i] = (Pval(X + e, q) - Pval(X - e, q))/(2*eps)
    return g

def Pgrad(X, q=Q12):
    f = X @ q.Y; fu = X @ q.Yu
    return (q.s*(2*fu*q.Yu/f - fu*fu*q.Y/f**2)) @ q.w / 8.0

def fmin_of(X, ngrid=601):
    """min of cubic f over [-1,1] by dense grid + local refine."""
    ug = np.linspace(-1, 1, ngrid)
    fv = X @ Yr(ug)
    i = int(np.argmin(fv))
    lo, hi = max(i-1, 0), min(i+1, ngrid-1)
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda u: float(X @ Yr(np.array([u]))[:, 0]),
                        bounds=(ug[lo], ug[hi]), method='bounded',
                        options={'xatol': 1e-12})
    return min(float(r.fun), fv[0], fv[-1])

# ---------------- background flows (own integration) ----------------
def flow(gamma, c, fstop=0.002, Tmax=10.0, grad=Pgrad, q=Q12):
    def rhs(t, z):
        X, Xt = z[:4], z[4:]
        return np.concatenate([Xt, Xt + 2*grad(X, q)])
    def ev(t, z):
        return fmin_of(z[:4]) - fstop
    ev.terminal, ev.direction = True, -1
    z0 = np.array([1.0, 0, 0, 0, gamma, -c, 0, 0])
    sol = solve_ivp(rhs, (0, Tmax), z0, method='DOP853', rtol=1e-11,
                    atol=1e-12, dense_output=True, events=ev)
    return sol

# ---------------- per-m angular blocks (own assembly) ----------------
LBLK = {0: [0, 1, 2, 3], 1: [1, 2, 3], 2: [2, 3], 3: [3]}

def dPlm(l, m, u):
    """(1-u^2) dP/du = (l+m) P_{l-1}^m - l u P_l^m (standard identity)."""
    return ((l + m)*lpmv(m, l - 1, u) - l*u*lpmv(m, l, u))/(1 - u**2)

class Blk:
    """R_lm = c_lm P_l^m(u) sqrt2 cos(m phi); c_lm fixed NUMERICALLY by
    <R^2> = 1 (no factorial formulas -- independent route)."""
    def __init__(self, m, q=Q12):
        self.m, self.q = m, q
        ls = LBLK[m]; self.ls = ls
        if m == 0:
            self.R, self.dR = q.Y, q.Yu
        else:
            P = np.array([lpmv(m, l, q.x) for l in ls])
            dP = np.array([dPlm(l, m, q.x) for l in ls])
            c = np.array([1.0/np.sqrt(0.5*(q.w @ (P[i]**2)))
                          for i in range(len(ls))])
            self.R = c[:, None]*P
            self.dR = c[:, None]*dP
        self.d = len(ls)

    def mats(self, Xarr):
        """Xarr (nt,4) -> H, GA, GB arrays (nt,d,d). Own second-variation
        integrand: Hess_ij = (1/2)< grad Ri.grad Rj/f
          - [(grad f.grad Ri)Rj + (i<->j)]/f^2 + |grad f|^2 Ri Rj/f^3 >,
        with phi averages already folded (same-m real harmonics)."""
        q = self.q; m, d = self.m, self.d
        Xarr = np.atleast_2d(Xarr)
        f = Xarr @ q.Y          # (nt, Nq)
        fu = Xarr @ q.Yu
        s = q.s
        H = np.empty((len(Xarr), d, d))
        GA = np.empty_like(H); GB = np.empty_like(H)
        for i in range(d):
            for j in range(i, d):
                gg = s*self.dR[i]*self.dR[j]
                if m:
                    gg = gg + m*m*self.R[i]*self.R[j]/s
                rr = self.R[i]*self.R[j]
                rd = self.dR[i]*self.R[j] + self.dR[j]*self.R[i]
                I = gg/f - (s*fu)*rd/f**2 + (s*fu**2)*rr/f**3
                H[:, i, j] = H[:, j, i] = (I @ q.w)/4.0   # (1/2)*(1/2)Int du
                GA[:, i, j] = GA[:, j, i] = ((rr/f**2) @ q.w)/2.0
                GB[:, i, j] = GB[:, j, i] = ((rr/f**3) @ q.w)/2.0
        return H, GA, GB

    def gaunt(self):
        q = self.q; d = self.d
        C = np.empty((d, d))
        for i in range(d):
            for j in range(d):
                C[i, j] = (q.w @ (self.R[i]*S3*q.x*self.R[j]))/2.0
        return C

BLKS = {m: Blk(m) for m in range(4)}

# ---------------- 2D finite-difference second variation ----------------
def P_full_2d(X, m, b, nu=800, nphi=256):
    """P = (1/4)(1/4pi) Int [ (1-u^2) f_u^2 + f_phi^2/(1-u^2) ] / f dOm
    for f = bg(u) + sum_c b_c R_c(u,phi), R_c = c P sqrt2 cos(m phi)."""
    x, w = np.polynomial.legendre.leggauss(nu)
    phi = np.linspace(0, 2*np.pi, nphi, endpoint=False)
    B = Blk(m, Q(nu)) if m else None
    Yx, Yux = Yr(x), Yru(x)
    fbg = (X @ Yx)[:, None] + 0*phi[None, :]
    fbgu = (X @ Yux)[:, None] + 0*phi[None, :]
    if m == 0:
        Rl = Yx; dRl = Yux
        cosf = np.ones_like(phi); sinf = np.zeros_like(phi); mm = 0
    else:
        Rl, dRl = B.R, B.dR
        cosf = np.sqrt(2)*np.cos(m*phi); sinf = np.sqrt(2)*np.sin(m*phi)
        mm = m
    f = fbg + np.einsum('c,cx,p->xp', b, Rl, cosf)
    fu = fbgu + np.einsum('c,cx,p->xp', b, dRl, cosf)
    fp = -mm*np.einsum('c,cx,p->xp', b, Rl, sinf)
    s = (1 - x**2)[:, None]
    integ = (s*fu**2 + fp**2/s)/f
    return 0.25*(w @ integ).mean()/2.0   # (1/2)Int du x (1/2pi)Int dphi

def hess_fd_2d(X, m, eps=3e-5):
    d = len(LBLK[m])
    H = np.empty((d, d))
    P0 = P_full_2d(X, m, np.zeros(d))
    for i in range(d):
        for j in range(i, d):
            if i == j:
                e = np.zeros(d); e[i] = eps
                H[i, i] = (P_full_2d(X, m, e) - 2*P0
                           + P_full_2d(X, m, -e))/eps**2
            else:
                epp = np.zeros(d); epp[i] = eps; epp[j] = eps
                epm = np.zeros(d); epm[i] = eps; epm[j] = -eps
                H[i, j] = H[j, i] = (P_full_2d(X, m, epp)
                                     - P_full_2d(X, m, epm)
                                     - P_full_2d(X, m, -epm)
                                     + P_full_2d(X, m, -epp))/(4*eps**2)
    return H

# ---------------- D_+ and M_out ----------------
import mpmath as mp
mp.mp.dps = 30
QTHIRD = mp.mpf(1)/3
def Dplus(lam, nu):
    if lam == 0:
        return float((1 + mp.mpf(nu))/6)
    tau0 = 6*mp.sqrt(lam); nu = mp.mpf(nu)
    K = mp.besselk(nu, tau0)
    Kp = -(mp.besselk(nu - 1, tau0) + mp.besselk(nu + 1, tau0))/2
    return float((1 - 2*QTHIRD)/2 - mp.sqrt(lam)*Kp/K)
NU_S, NU_U = 3.0, float(mp.sqrt(17))

def mout(gamma, c, m, scale=1.0, nu=NU_S, zero_dp=False):
    C = BLKS[m].gaunt()
    dp = [0.0 if zero_dp else scale*Dplus(l*(l + 1), nu) for l in LBLK[m]]
    M = np.diag([gamma + v for v in dp]) - c*C
    return 0.5*(M + M.T)

# ---------------- coefficient tables ----------------
class Tables:
    def __init__(self, sol, m, t5, nt=961):
        self.t = np.linspace(0.0, t5, nt)
        X = np.array([sol.sol(t)[:4] for t in self.t])
        self.H, self.GA, self.GB = BLKS[m].mats(X)
        self.d = BLKS[m].d
    def at(self, tq, which='A'):
        tq = np.clip(tq, self.t[0], self.t[-1])
        Gt = self.GA if which == 'A' else self.GB
        d = self.d
        H = np.empty((len(tq), d, d)); G = np.empty_like(H)
        for i in range(d):
            for j in range(d):
                H[:, i, j] = np.interp(tq, self.t, self.H[:, i, j])
                G[:, i, j] = np.interp(tq, self.t, Gt[:, i, j])
        return H, G

# ---------------- own FEM (vector P1, 2-pt Gauss) ----------------
GP = np.array([-1, 1])/np.sqrt(3.0)   # 2-pt Gauss on [-1,1]
def fem_assemble(tab, tb, Mout, N=200, which='A', m=0):
    """returns K0 (no inner-h term), Bm, boundary projector Pb, kept idx,
    after the m=0 vhat rotation/drop. Mout: matrix or 'dir'."""
    d = tab.d
    s = np.linspace(0.0, tb, N + 1)
    he = np.diff(s)
    # gauss points per element
    tg = 0.5*(s[:-1] + s[1:])[:, None] + 0.5*he[:, None]*GP[None, :]
    Hg, Gg = tab.at(tg.ravel(), which)
    Hg = Hg.reshape(N, 2, d, d); Gg = Gg.reshape(N, 2, d, d)
    pg = np.exp(-tg); qg = 2*np.exp(-tg)[..., None, None]*Hg
    wg = np.exp(-3*tg)[..., None, None]*Gg
    # linear shapes at gauss pts: N1 = (1-xi)/2, N2 = (1+xi)/2; dN = +-1/h
    n1 = (1 - GP)/2; n2 = (1 + GP)/2
    ndof = (N + 1)*d
    K = np.zeros((ndof, ndof)); B = np.zeros((ndof, ndof))
    # weights: int over element = (h/2) sum_g (1 each for 2pt)
    for g in range(2):
        wfac = he/2
        # stiffness p * u'v': u' = (u2-u1)/h
        kp = wfac*pg[:, g]/he**2          # (N,)
        # mass-type blocks
        q11 = (wfac*n1[g]*n1[g])[:, None, None]*qg[:, g]
        q12 = (wfac*n1[g]*n2[g])[:, None, None]*qg[:, g]
        q22 = (wfac*n2[g]*n2[g])[:, None, None]*qg[:, g]
        w11 = (wfac*n1[g]*n1[g])[:, None, None]*wg[:, g]
        w12 = (wfac*n1[g]*n2[g])[:, None, None]*wg[:, g]
        w22 = (wfac*n2[g]*n2[g])[:, None, None]*wg[:, g]
        for e in range(N):
            i0, i1 = e*d, (e + 1)*d
            Ie = np.eye(d)*kp[e]
            K[i0:i0+d, i0:i0+d] += Ie + q11[e]
            K[i1:i1+d, i1:i1+d] += Ie + q22[e]
            K[i0:i0+d, i1:i1+d] += -Ie + q12[e]
            K[i1:i1+d, i0:i0+d] += -Ie + q12[e]
            B[i0:i0+d, i0:i0+d] += w11[e]
            B[i1:i1+d, i1:i1+d] += w22[e]
            B[i0:i0+d, i1:i1+d] += w12[e]
            B[i1:i1+d, i0:i1+d+0] += 0  # placeholder
            B[i1:i1+d, i0:i0+d] += w12[e]
    drop = []
    if isinstance(Mout, str) and Mout == 'dir':
        drop += list(range(d))
    else:
        K[:d, :d] += Mout                  # p(0) = 1
    last = N*d
    Pb = np.zeros((ndof, ndof))            # multiplies (-e^{-tb} h)
    if m == 0 and d == 4:
        R4 = np.column_stack([VH, WC])
        T = np.eye(ndof); T[last:last+d, last:last+d] = R4
        K = T.T @ K @ T; B = T.T @ B @ T
        drop += [last]
        for k in range(1, d):
            Pb[last+k, last+k] = 1.0
    else:
        for k in range(d):
            Pb[last+k, last+k] = 1.0
    keep = np.setdiff1d(np.arange(ndof), drop)
    K = 0.5*(K + K.T); B = 0.5*(B + B.T)
    return (K[np.ix_(keep, keep)], B[np.ix_(keep, keep)],
            Pb[np.ix_(keep, keep)]*np.exp(-tb))

def fem_eigs(tab, tb, Mout, h, N=200, which='A', m=0, nev=6, dir_in=False):
    K, B, Pb = fem_assemble(tab, tb, Mout, N, which, m)
    if dir_in:
        # full Dirichlet at t_b: drop all last-node dofs (after rotation
        # for m=0 the vhat dof is already dropped; drop the rest too)
        n = K.shape[0]; d = tab.d
        nl = d - 1 if (m == 0 and d == 4) else d
        keep = np.arange(n - nl)
        Kr, Br = K[np.ix_(keep, keep)], B[np.ix_(keep, keep)]
        return sla.eigh(Kr, Br, eigvals_only=True,
                        subset_by_index=[0, nev - 1])
    Kh = K - h*Pb
    return sla.eigh(Kh, B, eigvals_only=True, subset_by_index=[0, nev - 1])

# ---------------- own shooting (forward 0 -> t_b) ----------------
def shoot_det(tab, tb, sig, h, Mout, which='A', m=0, dir_out=False):
    d = tab.d
    if dir_out:
        U0 = np.zeros((d, d)); V0 = np.eye(d)
    else:
        U0 = np.eye(d); V0 = Mout.copy()
    z0 = np.concatenate([U0.ravel(), V0.ravel()])
    def rhs(t, z):
        U = z[:d*d].reshape(d, d); V = z[d*d:].reshape(d, d)
        Hm, Gm = tab.at(np.array([t]), which)
        A = V + (2*Hm[0] - sig*np.exp(-2*t)*Gm[0]) @ U
        return np.concatenate([V.ravel(), A.ravel()])
    sol = solve_ivp(rhs, (0.0, tb), z0, method='DOP853',
                    rtol=1e-11, atol=1e-12)
    U = sol.y[:d*d, -1].reshape(d, d); V = sol.y[d*d:, -1].reshape(d, d)
    if m == 0 and d == 4:
        Rm = np.vstack([VH @ U, WC.T @ (V - h*U)])
    else:
        Rm = V - h*U
    nrm = np.maximum(np.linalg.norm(np.vstack([U, V]), axis=0), 1e-300)
    return np.linalg.det(Rm/nrm)

def refine(tab, tb, sig0, h, Mout, which='A', m=0, span=None):
    f = lambda s: shoot_det(tab, tb, s, h, Mout, which, m)
    span = span or max(0.02*abs(sig0), 0.05)
    a, b = sig0 - span, sig0 + span
    fa, fb = f(a), f(b)
    k = 0
    while fa*fb > 0 and k < 10:
        a -= span; b += span; span *= 1.5
        fa, fb = f(a), f(b); k += 1
    if fa*fb > 0:
        return np.nan
    return brentq(f, a, b, xtol=1e-9, rtol=1e-12)

# ---------------- members ----------------
HEAD = {
    'M1': dict(gamma=1.0, c=None), 'M2': dict(gamma=1.0, c=None),
    'M3': dict(gamma=1.0, c=None), 'M4': dict(gamma=0.5, c=None)}
def load_members(tags=('M1', 'M2', 'M3', 'M4')):
    mem = {}
    for tag in tags:
        hdr = open(f"/tmp/seal_s1/lib/bg_{tag}.dat").read(2500)
        gam = float(hdr.split("gamma=")[1].split()[0])
        c = float(hdr.split(" c=")[1].split()[0])
        t1 = float(hdr.split("<1% t<")[1].split()[0])
        t5 = float(hdr.split("<5% t<")[1].split()[0])
        tseal = float(hdr.split("t_seal*(linear-layer extrap)=")[1]
                      .split(";")[0])
        dat = np.loadtxt(f"/tmp/seal_s1/lib/bg_{tag}.dat")
        mem[tag] = dict(gamma=gam, c=c, t1pc=t1, t5pc=t5, tseal=tseal,
                        yseal=float(np.exp(-tseal)), dat=dat)
    return mem
