"""bv13 numeric part 2: discretized constrained second-variation forms; W3/W4/W5(i)/W6.
Own scheme: P1 elements, midpoint quadrature, uniform grid on [0, r_s].
Variables (FREE/Q_ext): u_0..u_{M-1}, beta, v_0..v_M, alpha  (u_M == -phip_s * beta essential).
Q_hat: drop alpha, impose v_0=0.  FIXED: drop alpha,beta (=> u_M=0).  ANCHORED: FREE minus u_0.
All counts primary on Jacobi-equilibrated congruent matrix (inertia-invariant), raw as cross-check.
Checkpoints results into bv13_matrix_results.json incrementally.
"""
import numpy as np, json, time
from scipy.linalg import eigvalsh, lu_factor, lu_solve

Z = 8.0
RES = {}
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

def assemble(tag, M):
    info = INFO[tag]; a = info["a"]; r_s = info["r_s"]; phip_s = info["phip_s"]
    U, Up, Upp = makeU(a)
    h = r_s/M
    rm = (np.arange(M)+0.5)*h
    phi, phip, rho, rhop = background(tag, rm)
    em2p = np.exp(-2.0*phi)
    cku = 0.5*Z*rho**2
    ckv = -2.0*em2p
    cc1 = 2.0*Z*rho*phip
    cc2 = 8.0*em2p*rhop
    cmu = -4.0*em2p*rhop**2
    cmv = 0.5*Z*phip**2 - 0.5*Upp(rho)
    dim = 2*M+3
    iu = np.arange(M); ib = M; iv = M+1+np.arange(M+1); ia = 2*M+2
    Q = np.zeros((dim, dim))
    def add(i, j, w):
        Q[i, j] += w/2.0; Q[j, i] += w/2.0
    # u dof index per node j=0..M (u_M -> beta with weight -phip_s)
    def unode(j):
        return (iu[j], 1.0) if j < M else (ib, -phip_s)
    for j in range(M):
        (il, wl), (ir_, wr) = unode(j), unode(j+1)
        jvl, jvr = iv[j], iv[j+1]
        # u'^2: cku/h (du)^2, du = wr u_r - wl u_l
        c = cku[j]/h
        add(il, il, 2*c*wl*wl); add(ir_, ir_, 2*c*wr*wr); add(il, ir_, -2*c*wl*wr)
        # v'^2
        c = ckv[j]/h
        add(jvl, jvl, 2*c); add(jvr, jvr, 2*c); add(jvl, jvr, -2*c)
        # cc1 * du * vbar   (du=(wr u_r - wl u_l), vbar=(v_l+v_r)/2)
        c = cc1[j]*0.5
        for (ii, ww) in ((ir_, wr), (il, -wl)):
            add(ii, jvl, c*ww); add(ii, jvr, c*ww)
        # cc2 * ubar * dv
        c = cc2[j]*0.5
        for (jj, sv) in ((jvr, 1.0), (jvl, -1.0)):
            add(il, jj, c*wl*sv); add(ir_, jj, c*wr*sv)
        # cmu * h * ubar^2
        c = cmu[j]*h*0.25
        add(il, il, 2*c*wl*wl); add(ir_, ir_, 2*c*wr*wr); add(il, ir_, 2*c*wl*wr)
        # cmv * h * vbar^2
        c = cmv[j]*h*0.25
        add(jvl, jvl, 2*c); add(jvr, jvr, 2*c); add(jvl, jvr, 2*c)
    # endpoint bilinears
    rho_s = info["rho_s"]
    Lrho_s = info["Lrho_s"]
    add(ib, iv[M], Lrho_s)          # L_rho(r_s) * beta * v(r_s)
    add(ia, iv[0], Up(1.0))         # U'(rho_c) * alpha * v(0)
    return Q, dict(iu=iu, ib=ib, iv=iv, ia=ia, h=h, phip_s=phip_s, M=M)

def inertia(Q, label, tolfac=1e-10):
    d = np.sqrt(np.abs(np.diag(Q)))
    d[d == 0] = 1.0
    Qs = Q/np.outer(d, d)
    w = eigvalsh(Qs)
    tol = tolfac*np.max(np.abs(w))
    nneg = int(np.sum(w < -tol)); npos = int(np.sum(w > tol)); nz = int(len(w)-nneg-npos)
    return nneg, npos, nz, float(w[0]), float(w[-1])

def submatrix(Q, keep):
    return Q[np.ix_(keep, keep)]

for tag in ("N0", "N5"):
    RES[tag] = {}
    for M in (200, 400, 800, 1600):
        t0 = time.time()
        Q, ix = assemble(tag, M)
        dim = Q.shape[0]
        iu, ib, iv, ia = ix["iu"], ix["ib"], ix["iv"], ix["ia"]
        free = list(range(dim))
        qhat = [i for i in free if i != ia and i != iv[0]]
        fixed = [i for i in free if i != ia and i != ib]
        anch = [i for i in free if i != iu[0]]
        r = {}
        r["free"] = inertia(Q, "free")
        r["qhat"] = inertia(submatrix(Q, qhat), "qhat")
        if M <= 800:
            r["fixed"] = inertia(submatrix(Q, fixed), "fixed")
            r["anchored"] = inertia(submatrix(Q, anch), "anchored")
        # Haynsworth split of Q_hat: v-side = v_1..v_M ; u-side = u_0..u_{M-1}, beta
        vside = [i for i in iv[1:]]
        uside = list(iu) + [ib]
        Qh = Q  # use full Q with selections (v0, alpha excluded)
        A = submatrix(Q, uside)
        V = submatrix(Q, vside)
        B = Q[np.ix_(uside, vside)]
        lu = lu_factor(V)
        S = A - B @ lu_solve(lu, B.T)
        # equilibrated inertia of V and S
        r["Vhat"] = inertia(V, "Vhat")
        r["S_u"] = inertia(S, "S_u")
        # W5(i): translation vector in FREE column
        rr_nodes = np.arange(M+1)*ix["h"]
        phi_n, phip_n, rho_n, rhop_n = background(tag, rr_nodes)
        t = np.zeros(dim)
        t[iu] = -phip_n[:M]
        t[ib] = 1.0
        t[iv] = -rhop_n
        t[ia] = 1.0
        num = float(t @ Q @ t)
        num_ld = float(t.astype(np.longdouble) @ Q.astype(np.longdouble) @ t.astype(np.longdouble))
        den = float(t @ t)*ix["h"]
        r["translation_QtT"] = num
        r["translation_QtT_longdouble"] = num_ld
        r["translation_rayleigh"] = num/den
        # essential-constraint check for t: u_M implied = -phip_s*beta = -phip_s vs -phip(r_s): exact
        RES[tag][str(M)] = r
        print(f"[{tag} M={M}] done in {time.time()-t0:.1f}s")
        for k, v in r.items():
            print(f"    {k:28s} = {v}")
        with open("bv13_matrix_results.json", "w") as f:
            json.dump(RES, f, indent=1, default=float)
print("checkpointed bv13_matrix_results.json")
