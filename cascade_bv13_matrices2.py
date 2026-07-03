"""bv13 numeric part 2 (v2, bug-fixed): symmetric outer-product assembly + independent validation
of x^T Q x against fine quadrature of the continuum quadratic form, then W3/W4/W5(i)/W6 counts.
"""
import numpy as np, json, time
from scipy.linalg import eigvalsh, lu_factor, lu_solve

Z = 8.0
BG = np.load("bv13_bg.npz")
INFO = json.load(open("bv13_bg.json"))
RES = {}

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
    return dict(cku=0.5*Z*rho**2, ckv=-2.0*em2p, cc1=2.0*Z*rho*phip,
                cc2=8.0*em2p*rhop, cmu=-4.0*em2p*rhop**2,
                cmv=0.5*Z*phip**2 - 0.5*Upp(rho))

def assemble(tag, M):
    info = INFO[tag]; r_s = info["r_s"]; phip_s = info["phip_s"]
    a = info["a"]; U, Up, Upp = makeU(a)
    h = r_s/M
    C = coeffs(tag, (np.arange(M)+0.5)*h)
    dim = 2*M+3
    iu = np.arange(M); ib = M; iv = M+1+np.arange(M+1); ia = 2*M+2
    Q = np.zeros((dim, dim))
    def uidx(j):
        return (iu[j], 1.0) if j < M else (ib, -phip_s)
    def rank1(c, f_idx, f_w, g_idx, g_w):
        # adds c*(f.x)(g.x) symmetrically
        for fi, fw in zip(f_idx, f_w):
            for gi, gw in zip(g_idx, g_w):
                Q[fi, gi] += 0.5*c*fw*gw
                Q[gi, fi] += 0.5*c*fw*gw
    for j in range(M):
        (il, wl), (ir_, wr) = uidx(j), uidx(j+1)
        jvl, jvr = iv[j], iv[j+1]
        du_i, du_w = (il, ir_), (-wl, wr)
        ub_i, ub_w = (il, ir_), (0.5*wl, 0.5*wr)
        dv_i, dv_w = (jvl, jvr), (-1.0, 1.0)
        vb_i, vb_w = (jvl, jvr), (0.5, 0.5)
        rank1(C["cku"][j]/h, du_i, du_w, du_i, du_w)
        rank1(C["ckv"][j]/h, dv_i, dv_w, dv_i, dv_w)
        rank1(C["cc1"][j],   du_i, du_w, vb_i, vb_w)
        rank1(C["cc2"][j],   ub_i, ub_w, dv_i, dv_w)
        rank1(C["cmu"][j]*h, ub_i, ub_w, ub_i, ub_w)
        rank1(C["cmv"][j]*h, vb_i, vb_w, vb_i, vb_w)
    rank1(info["Lrho_s"], (ib,), (1.0,), (iv[M],), (1.0,))
    rank1(Up(1.0), (ia,), (1.0,), (iv[0],), (1.0,))
    return Q, dict(iu=iu, ib=ib, iv=iv, ia=ia, h=h, phip_s=phip_s, M=M, r_s=r_s)

# ---------- validation: x^T Q x vs fine-quadrature continuum form on smooth test fields ----------
def continuum_form(tag, ufun, vfun, alpha, beta, K=400001):
    info = INFO[tag]; r_s = info["r_s"]; a = info["a"]; U, Up, Upp = makeU(a)
    r = np.linspace(0.0, r_s, K)
    C = coeffs(tag, r)
    u, v = ufun(r), vfun(r)
    up = np.gradient(u, r); vp = np.gradient(v, r)
    integ = (C["cku"]*up**2 + C["ckv"]*vp**2 + C["cc1"]*v*up + C["cc2"]*u*vp
             + C["cmu"]*u**2 + C["cmv"]*v**2)
    val = np.trapezoid(integ, r)
    val += info["Lrho_s"]*beta*vfun(np.array([r_s]))[0] + Up(1.0)*alpha*vfun(np.array([0.0]))[0]
    return val

def validate(tag):
    info = INFO[tag]; r_s = info["r_s"]; phip_s = info["phip_s"]
    beta = 0.7; alpha = 1.3
    ufun = lambda r: np.sin(2.5*np.pi*r/r_s) + 0.3*(r/r_s)**2 - phip_s*beta*(r/r_s)**3*(3-2*(r/r_s))*0  # generic
    # impose essential constraint u(r_s) = -phip_s*beta exactly: add a correction
    base = lambda r: np.sin(2.5*np.pi*r/r_s) + 0.3*(r/r_s)**2
    corr = -phip_s*beta - base(np.array([r_s]))[0]
    ufun = lambda r: base(r) + corr*(r/r_s)**2
    vfun = lambda r: np.cos(1.7*np.pi*r/r_s) - 0.2*(r/r_s)
    ref = continuum_form(tag, ufun, vfun, alpha, beta)
    outs = []
    for M in (400, 800, 1600):
        Q, ix = assemble(tag, M)
        rr = np.arange(M+1)*ix["h"]
        x = np.zeros(Q.shape[0])
        x[ix["iu"]] = ufun(rr[:M]); x[ix["ib"]] = beta
        x[ix["iv"]] = vfun(rr); x[ix["ia"]] = alpha
        outs.append(float(x @ Q @ x))
    print(f"[validate {tag}] continuum={ref:.8f}  discrete(M=400,800,1600)={outs}")
    return ref, outs

for tag in ("N0", "N5"):
    validate(tag)

# ---------- counts ----------
def inertia(Q, tolfac=1e-10):
    d = np.sqrt(np.abs(np.diag(Q))); d[d == 0] = 1.0
    Qs = Q/np.outer(d, d)
    w = eigvalsh(Qs)
    tol = tolfac*np.max(np.abs(w))
    return int(np.sum(w < -tol)), int(np.sum(w > tol)), int(np.sum(np.abs(w) <= tol))

def run(tag, M):
    t0 = time.time()
    Q, ix = assemble(tag, M)
    dim = Q.shape[0]
    iu, ib, iv, ia = ix["iu"], ix["ib"], ix["iv"], ix["ia"]
    r = {}
    r["free"] = inertia(Q)
    qhat = [i for i in range(dim) if i != ia and i != iv[0]]
    r["qhat"] = inertia(Q[np.ix_(qhat, qhat)])
    if M <= 800:
        fixed = [i for i in range(dim) if i != ia and i != ib]
        anch = [i for i in range(dim) if i != iu[0]]
        r["fixed"] = inertia(Q[np.ix_(fixed, fixed)])
        r["anchored"] = inertia(Q[np.ix_(anch, anch)])
    vside = list(iv[1:]); uside = list(iu) + [ib]
    A = Q[np.ix_(uside, uside)]; V = Q[np.ix_(vside, vside)]; B = Q[np.ix_(uside, vside)]
    lu = lu_factor(V)
    S = A - B @ lu_solve(lu, B.T)
    r["Vhat"] = inertia(V); r["S_u"] = inertia(S)
    # W5(i) translation
    rr = np.arange(M+1)*ix["h"]
    phi_n, phip_n, rho_n, rhop_n = background(tag, rr)
    t = np.zeros(dim)
    t[iu] = -phip_n[:M]; t[ib] = 1.0; t[iv] = -rhop_n; t[ia] = 1.0
    num = float(t @ Q @ t); den = float(t @ t)*ix["h"]
    r["translation_rayleigh"] = num/den
    r["translation_QtT"] = num
    # residual vector norm |Q t| restricted to interior rows (kernel check), scaled
    qt = Q @ t
    r["Qt_maxabs_over_Qmax"] = float(np.max(np.abs(qt))/np.max(np.abs(Q)))
    print(f"[{tag} M={M}] ({time.time()-t0:.1f}s)")
    for k, v in r.items(): print(f"    {k:26s} = {v}")
    return r

for tag in ("N0", "N5"):
    RES[tag] = {}
    for M in (200, 400, 800, 1600):
        RES[tag][str(M)] = run(tag, M)
        with open("bv13_matrix_results2.json", "w") as f:
            json.dump(RES, f, indent=1, default=float)
print("saved bv13_matrix_results2.json")
