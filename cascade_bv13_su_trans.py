"""bv13: (1) S_u inertia at M=3200 (convergence of n_neg(S_u)); (2) translation-mode
Q(t,t) via memory-free element sums at M up to 25600 (grid-scaling of the W5(i) zero).
Also S_u under the ALTERNATE v0-free split (v0 grouped into V) for the fork's downstream effect.
"""
import numpy as np, json, time
from scipy.linalg import eigvalsh, lu_factor, lu_solve

Z = 8.0
BG = np.load("bv13_bg.npz")
INFO = json.load(open("bv13_bg.json"))

def makeU(a, m=3.0):
    def U(rho):  return 2.0*rho**m*np.exp(-a*(rho*rho-1.0))
    def Up(rho): return U(rho)*(m/rho - 2.0*a*rho)
    def Upp(rho):return Up(rho)*(m/rho - 2.0*a*rho) + U(rho)*(-m/rho**2 - 2.0*a)
    return U, Up, Upp

def background(tag, r):
    rr = BG[tag+"_r"]; Y = BG[tag+"_y"]
    return [np.interp(r, rr, Y[i]) for i in range(4)]

def coeffs(tag, r):
    a = INFO[tag]["a"]; U, Up, Upp = makeU(a)
    phi, phip, rho, rhop = background(tag, r)
    em2p = np.exp(-2.0*phi)
    return (0.5*Z*rho**2, -2.0*em2p, 2.0*Z*rho*phip, 8.0*em2p*rhop,
            -4.0*em2p*rhop**2, 0.5*Z*phip**2 - 0.5*Upp(rho))

# ---------- (2) translation element-sum ----------
def trans_Qtt(tag, M):
    info = INFO[tag]; r_s = info["r_s"]; phip_s = info["phip_s"]
    a = info["a"]; U, Up, Upp = makeU(a)
    h = r_s/M
    nodes = np.arange(M+1)*h
    phi_n, phip_n, rho_n, rhop_n = background(tag, nodes)
    u = -phip_n.copy(); u[M] = -phip_s*1.0   # u_M = -phip_s*beta, beta=1 (consistent)
    v = -rhop_n
    rm = (np.arange(M)+0.5)*h
    cku, ckv, cc1, cc2, cmu, cmv = coeffs(tag, rm)
    du = np.diff(u); dv = np.diff(v)
    ub = 0.5*(u[:-1]+u[1:]); vb = 0.5*(v[:-1]+v[1:])
    val = np.sum(cku*du*du/h + ckv*dv*dv/h + cc1*du*vb + cc2*ub*dv + cmu*h*ub*ub + cmv*h*vb*vb)
    val += info["Lrho_s"]*1.0*v[M] + Up(1.0)*1.0*v[0]      # beta=1, alpha=1
    den = (np.sum(u[:M]**2) + 1.0 + np.sum(v**2) + 1.0)*h
    return float(val), float(val/den)

print("=== W5(i): translation Q(t,t) vs M (element sums) ===")
for tag in ("N0", "N5"):
    prev = None
    for M in (800, 1600, 3200, 6400, 12800, 25600):
        qtt, ray = trans_Qtt(tag, M)
        ratio = "" if prev is None else f"  ratio={prev/qtt:+.2f}"
        print(f"[{tag} M={M:6d}] Q(t,t)={qtt:+.6e}  rayleigh={ray:+.6e}{ratio}")
        prev = qtt

# ---------- (1) S_u at M=3200 (both v0 conventions) ----------
def blocks(tag, M, v0_in_V=False):
    """assemble the Q_hat blocks directly (u-side: u_0..u_{M-1}, beta; v-side: v_1..v_M [+v_0 if v0_in_V])."""
    info = INFO[tag]; r_s = info["r_s"]; phip_s = info["phip_s"]
    a = info["a"]; U, Up, Upp = makeU(a)
    h = r_s/M
    rm = (np.arange(M)+0.5)*h
    cku, ckv, cc1, cc2, cmu, cmv = coeffs(tag, rm)
    nu = M+1                      # u_0..u_{M-1}, beta
    v_off = 1 if v0_in_V else 0   # v-side node j has index j-1+v_off (j from 1-v_off? ...)
    nv = M + v_off                # v_1..v_M, or v_0..v_M
    A = np.zeros((nu, nu)); V = np.zeros((nv, nv)); B = np.zeros((nu, nv))
    def uidx(j): return (j, 1.0) if j < M else (M, -phip_s)
    def vidx(j):                  # global v node j=0..M -> V index or None (constrained to 0)
        if j == 0 and not v0_in_V: return None
        return j-1+v_off
    for j in range(M):
        (il, wl), (ir_, wr) = uidx(j), uidx(j+1)
        kl, kr = vidx(j), vidx(j+1)
        # u'^2
        c = cku[j]/h
        A[il, il] += c*wl*wl; A[ir_, ir_] += c*wr*wr; A[il, ir_] += -c*wl*wr; A[ir_, il] += -c*wl*wr
        # u^2 mass
        c = cmu[j]*h*0.25
        A[il, il] += c*wl*wl; A[ir_, ir_] += c*wr*wr; A[il, ir_] += c*wl*wr; A[ir_, il] += c*wl*wr
        # v'^2 and v^2
        ck = ckv[j]/h; cm = cmv[j]*h*0.25
        for (ki, si) in ((kl, -1.0), (kr, 1.0)):
            if ki is None: continue
            for (kj, sj) in ((kl, -1.0), (kr, 1.0)):
                if kj is None: continue
                V[ki, kj] += ck*si*sj + cm*0.25/0.25*0  # kinetic
        for (ki, ai) in ((kl, 0.5), (kr, 0.5)):
            if ki is None: continue
            for (kj, aj) in ((kl, 0.5), (kr, 0.5)):
                if kj is None: continue
                V[ki, kj] += cm*4.0*ai*aj*0 + cmv[j]*h*ai*aj
        # cross cc1 * du * vbar : B[u, v]
        for (ii, ww, s) in ((ir_, wr, 1.0), (il, wl, -1.0)):
            for (kj, aj) in ((kl, 0.5), (kr, 0.5)):
                if kj is None: continue
                B[ii, kj] += cc1[j]*s*ww*aj
        # cross cc2 * ubar * dv
        for (ii, ww) in ((il, wl), (ir_, wr)):
            for (kj, sj) in ((kl, -1.0), (kr, 1.0)):
                if kj is None: continue
                B[ii, kj] += cc2[j]*0.5*ww*sj
    # endpoint: L_rho * beta * v_M
    B[M, vidx(M)] += info["Lrho_s"]
    # (alpha dropped; U' alpha v0 term absent from Q_hat)
    return A, V, B

def inertia(Qm, tolfac=1e-10):
    d = np.sqrt(np.abs(np.diag(Qm))); d[d == 0] = 1.0
    Qs = Qm/np.outer(d, d)
    w = eigvalsh(Qs)
    tol = tolfac*np.max(np.abs(w))
    return int(np.sum(w < -tol)), int(np.sum(w > tol)), int(np.sum(np.abs(w) <= tol))

print("\n=== S_u inertia convergence (v0=0 split) + alternate v0-in-V split ===")
for tag in ("N0", "N5"):
    for M in (1600, 3200):
        for v0f in (False, True):
            t0 = time.time()
            A, V, B = blocks(tag, M, v0_in_V=v0f)
            lu = lu_factor(V)
            S = A - B @ lu_solve(lu, B.T)
            nn, npos, nz = inertia(S)
            lab = "v0-in-V" if v0f else "v0=0   "
            print(f"[{tag} M={M} {lab}] n_neg(S_u)={nn} n_pos={npos} n_zero={nz}  ({time.time()-t0:.0f}s)")
